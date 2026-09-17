"""Build register.json: known texts of the Bixby letter's register (personal, elevated,
condoling or ceremonial prose of 1861-65) by Lincoln and by Hay, cut into pieces of
about 140 words, for a register-matched validation of every method.
Lincoln pieces come from Basler (autograph items in vols IV, VII, VIII, with source codes)
and from Lapsley's edition for 1862-63 (Basler vols V-VI are not available in full text).
Hay pieces come from hay_warprose.jsonl (his 1861 magazine eulogies) and his 1864
condolence fragment. Every piece records its parent text so the parent can be removed
from the candidate pools."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designs
from ngt import _SENT_SPLIT, word_count

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET, MINW, MAXW = 140, 90, 250

LINCOLN_BASLER = {  # id: (label, note)
 'basler-IV-0294': ('Farewell address at Springfield, 11 Feb 1861 (AD)', 'first version only'),
 'basler-IV-0931': ('To Mrs. John C. Fremont, 12 Sept 1861 (ADfS)', ''),
 'basler-VII-0606': ('To Albert G. Hodges, 4 April 1864 (ADfS)', ''),
 'basler-VII-0654': ('Address at Sanitary Fair, Baltimore, 18 April 1864 (AD)', ''),
 'basler-VII-0708': ('To Ulysses S. Grant, 30 April 1864 (ALS)', ''),
 'basler-VII-0765': ('Response to Methodists, 18 May 1864 (ADS)', ''),
 'basler-VIII-0090': ('To Henry W. Hoffman, 10 Oct 1864 (ALS)', ''),
 'basler-VIII-0334': ('To William T. Sherman, 26 Dec 1864 (ALS)', ''),
 'basler-VIII-0388': ('To Mrs. Charles J. Faulkner, 9 Jan 1865 (ALS)', ''),
 'basler-VIII-0434': ('To Ulysses S. Grant, 19 Jan 1865 (ALS)', ''),
 'basler-VIII-0657': ('Reply to Notification Committee, 1 March 1865 (AD)', ''),
 'basler-VIII-0724': ('To Thurlow Weed, 15 March 1865 (ALS)', ''),
}
LINCOLN_LAPSLEY = {  # id: (label, parent basler id if the same text is in a Basler pool)
 'L6-0134': ('To Reverdy Johnson, 26 July 1862', None),
 'L6-0135': ('To Cuthbert Bullitt, 28 July 1862', None),
 'L6-0150': ('To Horace Greeley, 22 Aug 1862', None),
 'L6-0204': ('To George B. McClellan, 13 Oct 1862', None),
 'L6-0232': ('To Carl Schurz, 24 Nov 1862', None),
 'L6-0294': ('To Joseph Hooker, 26 Jan 1863', None),
 'L6-0308': ('To Alexander Reed, 22 Feb 1863', None),
 'L6-0476': ('To Ulysses S. Grant, 9 Aug 1863', None),
 'L6-0481': ('To James H. Hackett, 17 Aug 1863', None),
 'L6-0509': ('To Andrew Johnson, 11 Sept 1863', None),
 'L7-0012': ('To James H. Hackett, 2 Nov 1863', None),
 'L7-0116': ('To Carl Schurz, 13 March 1864', 'basler-VII-0563'),
 'L7-0122': ('To Mrs. Horace Mann, 5 April 1864', None),
 'L7-0276': ('Response to a serenade, 10 Nov 1864 (AD; Basler text OCR-damaged, Lapsley text used)', 'basler-VIII-0194'),
}
SPECIAL_LINCOLN = ['gettysburg', 'second_inaugural', 'mccullough', 'ellsworth', 'gurney']

SALUT = re.compile(r"^\s*(\(Private[^)]*\)\s*)?(\[Private\.?\]\s*)?([A-Z][A-Z .,'-]{1,40}(:--|--|:)\s*|My (dear|esteemed) (Sir|Madam|friend|General [A-Za-z]+)[.:,—-]*\s*(Washington, )?([A-Z][a-z]+\.? \d{1,2},? \d{4}\.?\s*)?)", re.M)
HEADLINE = re.compile(r"^(\(Private[^)]*\)|\[Private\.?\]|EXECUTIVE MANSION.*|WASHINGTON.*|WAR DEPARTMENT.*|[A-Z][A-Za-z]+ \d{1,2},? \d{4}\.?|[A-Z .,'-]{3,60}[.:,]?|.*\b\d{4}\.\s*[A-Z .,'-]{0,40})$")
TRAIL = re.compile(r"(Yours,?( very)?( truly)?|Yours very truly|Respectfully|Your Ob(edien)?t\.? Serv(an)?t|Very truly your friend|Your obedient servant)[,.]?\s*[\s\S]{0,60}$")

def clean_lapsley(t):
    lines = t.split('\n')
    # drop leading dateline/address lines: short lines before the first line with >= 8 words
    i = 0
    while i < len(lines) and (len(lines[i].split()) < 8 or HEADLINE.match(lines[i].strip())): i += 1
    body = '\n'.join(lines[i:])
    body = re.sub(r'^EXECUTIVE MANSION[^\n]*\d{4}\.\s*', '', body)
    body = re.sub(r"^[A-Z][A-Z .,'-]{2,40}(:--|--|:)\s*", '', body)
    body = SALUT.sub('', body, count=1)
    body = TRAIL.sub('', body).strip()
    body = re.sub(r'\.{4,}', '.', body)
    body = re.sub(r'\[[^\]]{0,400}\]', ' ', body)  # editorial insertions in Lapsley
    body = body.replace('--', ' — ')
    body = re.sub(r'\s+', ' ', body)
    return body

def clean_basler(t):
    body = SALUT.sub('', t, count=1)
    body = TRAIL.sub('', body).strip()
    return re.sub(r'\s+', ' ', body)

def chunk(text, target=TARGET, minw=MINW):
    sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    pieces, cur, n = [], [], 0
    for s in sents:
        w = word_count(s)
        if n and n + w > target * 1.35 and n >= minw:
            pieces.append(' '.join(cur)); cur, n = [], 0
        cur.append(s); n += w
        if n >= target:
            pieces.append(' '.join(cur)); cur, n = [], 0
    if cur:
        if n < minw and pieces: pieces[-1] = pieces[-1] + ' ' + ' '.join(cur)
        else: pieces.append(' '.join(cur))
    return pieces

def add(out, base, text, author, label, parents, single=False):
    text = text.strip()
    pieces = [text] if word_count(text) <= MAXW else chunk(text)
    if single: pieces = pieces[:1]
    for k, p in enumerate(pieces):
        if word_count(p) < MINW: continue
        pid = base if len(pieces) == 1 else f'{base}#{k}'
        out[pid] = {'author': author, 'label': label, 'text': p, 'parents': parents, 'words': word_count(p)}

def main():
    out = {}
    L = {r['id']: r for r in designs.load_lincoln()}
    for i, (label, note) in LINCOLN_BASLER.items():
        add(out, i, clean_basler(L[i]['text']), 'lincoln', label, [i], single=(note == 'first version only'))
    lap = {}
    for ln in open(os.path.join(HERE, 'lapsley.jsonl'), encoding='utf-8'):
        r = json.loads(ln); lap[r['id']] = r
    for i, (label, parent) in LINCOLN_LAPSLEY.items():
        add(out, i, clean_lapsley(lap[i]['text']), 'lincoln', label, [parent] if parent else [])
    for k in SPECIAL_LINCOLN:
        sp = designs.SPECIALS[k]
        add(out, 'sp_' + k, clean_lapsley(sp['text']), 'lincoln', sp['label'], [])
    # Hay
    sp = designs.SPECIALS['hay_condolence_1864']
    out['sp_hay_condolence_1864'] = {'author': 'hay', 'label': sp['label'], 'text': sp['text'], 'parents': [], 'words': word_count(sp['text'])}
    wp = os.path.join(HERE, '..', 'corpus', 'hay_warprose.jsonl')
    if os.path.exists(wp):
        for ln in open(wp, encoding='utf-8'):
            r = json.loads(ln)
            if r.get('word_count', word_count(r['text'])) >= MINW:
                out[r['id']] = {'author': 'hay', 'label': f"{r.get('title')} ({r.get('source')}, {r.get('year')})", 'text': r['text'], 'parents': [], 'words': word_count(r['text'])}
    json.dump(out, open(os.path.join(HERE, 'register.json'), 'w'), indent=1)
    from collections import Counter
    c = Counter(v['author'] for v in out.values())
    print('register pieces:', dict(c))
    for k, v in out.items():
        print(f"{k:28s} {v['author']:8s} {v['words']:4d} {v['label'][:50]} | {v['text'][:60]!r}")

if __name__ == '__main__':
    main()
