#!/usr/bin/env python3
"""Search dated full-text collections for early attestations of candidate anachronisms,
and VERIFY each hit against the OCR text (search engines match fuzzily: e.g. 'stampede'
matched 'stamped, or painted' in an 1824 tariff act).

Sources: (1) Chronicling America via the loc.gov JSON API (newspapers, dated by issue);
         (2) archive.org full-text search API (books; dates from item metadata, less reliable).
Output: results/lang_attestations.csv (term, source, date, title, verified snippet) and
        results/lang_attestations.md (earliest verified hits per term)."""
import json, re, csv, time, sys, os, html, urllib.parse, urllib.request, subprocess
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(B, 'results')
UA = 'Mozilla/5.0 (research script; historical linguistics)'
TERMS = {  # search term -> regex that must match the OCR as a whole word
    'stampede': r'\bstampede', 'stampeding': r'\bstampeding', 'stampeded': r'\bstampeded', 'stampedo': r'\bstampedo',
    'improvised': r'\bimprovised\b', 'improvise': r'\bimprovis', 'grizzlies': r'\bgrizzlies\b', 'grizzly bears': r'\bgrizzly bears\b',
    'objective point': r'\bobjective point\b', 'outfits': r'\boutfits\b', 'worth the candle': r'\bworth the candle\b',
    'ho for the': r'\bho\W{1,3}for the\b', 'well nigh': r'\bwell.nigh\b', 'encounter the expense': r'\bencounter the expense',
    'personating': r'\bpersonating\b', 'punctillio': r'\bpunctillio', 'reliable': r'\breliable\b', 'appliances': r'\bappliances\b',
    'tethered': r'\btethered\b', 'buffaloes': r'\bbuffaloes\b', 'exhilerating': r'\bexhilerating', 'systematize': r'\bsystematiz',
}
YEARS = (1800, 1835)

def get(url, timeout=120):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'replace')
        except Exception as e:
            time.sleep(4 * (attempt + 1)); err = e
    print('FAILED', url[:120], err, file=sys.stderr); return None

def loc_search(term, y0, y1, n=40):
    q = urllib.parse.quote(f'"{term}"')
    url = f'https://www.loc.gov/collections/chronicling-america/?q={q}&dates={y0}/{y1}&fo=json&c={n}&ops=PHRASE'
    raw = get(url)
    if not raw: return []
    try: d = json.loads(raw)
    except Exception: return []
    return [(r.get('date'), r.get('title'), r.get('id')) for r in d.get('results', [])]

def loc_ocr(resource_url):
    raw = get(resource_url.rstrip('/') + ('&' if '?' in resource_url else '?') + 'fo=json')
    if not raw: return ''
    try: d = json.loads(raw)
    except Exception: return ''
    ft = d.get('resource', {}).get('fulltext_file') or d.get('fulltext_service')
    if not ft: return ''
    txt = get(ft) or ''
    return html.unescape(re.sub(r'<[^>]+>', ' ', txt)).replace('\\n', ' ')   # OCR comes with literal \n sequences

def archive_fts(term, size=60):
    q = urllib.parse.quote(f'"{term}"')
    raw = get(f'https://be-api.us.archive.org/fts/v1/search?q={q}&size={size}')
    if not raw: return []
    try: d = json.loads(raw)
    except Exception: return []
    out = []
    for h in d.get('hits', {}).get('hits', []):
        f = h.get('fields', {})
        ident = (f.get('identifier') or [h.get('_id', '').split('|')[0]])[0]
        date = (f.get('meta_date') or [''])[0]; title = (f.get('meta_title') or [''])[0]
        hl = ' | '.join(h.get('highlight', {}).get('text', []))[:300]
        out.append((date, title, ident, hl))
    return out

rows = []
SOURCES = os.environ.get('ATTEST_SOURCES', 'loc,archive').split(',')
ONLY = os.environ.get('ATTEST_TERMS', '').split(',') if os.environ.get('ATTEST_TERMS') else list(TERMS)
if os.path.exists(os.path.join(R, 'lang_attestations.csv')):     # keep earlier rows from sources/terms not re-run
    rows = [r for r in csv.DictReader(open(os.path.join(R, 'lang_attestations.csv'))) if not (any(r['source'].startswith(s) for s in SOURCES) and r['term'] in ONLY)]
    for r in rows: r['verified'] = r['verified'] == 'True'
for term, rx in TERMS.items():
    if term not in ONLY: continue
    # --- Chronicling America
    hits = loc_search(term, *YEARS) if 'loc' in SOURCES else []
    print(term, 'loc hits', len(hits), file=sys.stderr)
    for date, title, rid in hits:
        ocr = loc_ocr(rid); m = re.search(rx, ocr, flags=re.I)
        snippet = re.sub(r'\s+', ' ', ocr[max(0, m.start() - 120): m.end() + 120]) if m else ''
        rows.append(dict(term=term, source='chroniclingamerica', date=date, title=title, url=rid, verified=bool(m), snippet=snippet))
        time.sleep(1.5)
    # --- archive.org full text (books): keep hits whose metadata date is before 1846; verify the term in the highlight
    for date, title, ident, hl in (archive_fts(term, size=100) if 'archive' in SOURCES else []):
        y = int(str(date)[:4]) if date and str(date)[:4].isdigit() else None
        if y is None or y > 1845: continue
        m = re.search(rx, hl.replace('{{{', '').replace('}}}', ''), flags=re.I)
        rows.append(dict(term=term, source='archive.org (metadata date; check the item)', date=str(date)[:10], title=str(title)[:120], url=f'https://archive.org/details/{ident}', verified=bool(m), snippet=hl.replace('{{{', '[').replace('}}}', ']')))
    time.sleep(2)
with open(os.path.join(R, 'lang_attestations.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['term', 'source', 'date', 'title', 'url', 'verified', 'snippet']); w.writeheader(); w.writerows(rows)
md = ['# Earliest verified attestations (searches limited to 1800-1835 newspapers and pre-1840 books)\n',
      '| term | source | date | title | snippet | url |', '|---|---|---|---|---|---|']
for term in TERMS:
    v = sorted([r for r in rows if r['term'] == term and r['verified']], key=lambda r: str(r['date']))
    nv = [r for r in rows if r['term'] == term and not r['verified']]
    if not v: md.append(f'| {term} | - | none verified | ({len(nv)} unverified search hits) | | |')
    for r in v[:4]: md.append(f"| {term} | {r['source']} | {r['date']} | {str(r['title'])[:60]} | {r['snippet'][:200]} | {r['url']} |")
open(os.path.join(R, 'lang_attestations.md'), 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
