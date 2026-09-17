#!/usr/bin/env python3
"""Verify Chronicling America (loc.gov) search hits for one term inside a year window against the page OCR.
Usage: lang_attest_window.py TERM Y0 Y1 REGEX [MAXHITS]
Writes results/lang_attest_window_<term>_<Y0>-<Y1>.csv (date, title, url, verified, snippet).
Search engine matching is fuzzy (e.g. 'stampede' matches 'stamped'), so only verified rows count."""
import json, re, csv, sys, os, time, html, urllib.parse, urllib.request
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
term, y0, y1, rx = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
n = int(sys.argv[5]) if len(sys.argv) > 5 else 40
UA = 'Mozilla/5.0 (research script; historical linguistics)'
def get(url, timeout=120):
    err = None
    for attempt in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout).read().decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(5 * (attempt + 1))
    print('FAILED', url[:100], err, file=sys.stderr); return None
q = urllib.parse.quote(f'"{term}"')
raw = get(f'https://www.loc.gov/collections/chronicling-america/?q={q}&dates={y0}/{y1}&fo=json&c={n}&ops=PHRASE&sb=date')
d = json.loads(raw) if raw else {}
res = d.get('results', [])
print(term, y0, y1, 'search total', d.get('pagination', {}).get('of'), 'fetched', len(res), file=sys.stderr)
rows = []
for r in res:
    rid = r.get('id'); date = r.get('date'); title = r.get('title')
    j = get(rid.rstrip('/') + ('&' if '?' in rid else '?') + 'fo=json')
    ocr = ''
    try:
        dj = json.loads(j) if j else {}
        ft = dj.get('resource', {}).get('fulltext_file') or dj.get('fulltext_service')
        if ft: ocr = html.unescape(re.sub(r'<[^>]+>', ' ', get(ft) or '')).replace('\\n', ' ')
    except Exception: pass
    m = re.search(rx, ocr, flags=re.I)
    snippet = re.sub(r'\s+', ' ', ocr[max(0, m.start() - 150): m.end() + 150]) if m else ''
    rows.append(dict(term=term, date=date, title=title, url=rid, verified=bool(m), snippet=snippet))
    print(date, '|', str(title)[:50], '|', 'VERIFIED' if m else 'no', '|', snippet[:160], file=sys.stderr)
    time.sleep(2)
out = os.path.join(B, 'results', f'lang_attest_window_{term.replace(" ", "_")}_{y0}-{y1}.csv')
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['term', 'date', 'title', 'url', 'verified', 'snippet']); w.writeheader(); w.writerows(rows)
print('wrote', out, 'verified', sum(r['verified'] for r in rows), 'of', len(rows), file=sys.stderr)
