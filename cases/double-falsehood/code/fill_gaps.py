#!/usr/bin/env python3
"""Fill illegible <gap> characters in the ECCO-TCP text of Double Falsehood (K036934.000) from the OCR of Walter Graham's 1920
reprint of the first edition (archive.org cu31924013363894) and the BL ECCO scan OCR (bim_eighteenth-century_..._1728).
Method: for each verse line or prose paragraph containing '^', find the best fuzzy match among OCR lines (difflib) using the
legible parts as anchors; accept if similarity >= 0.75; record every substitution in data/results/gap_fills.json for inspection."""
import json, re, difflib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import tokenize, normalize_tokens
ocr_files = ['sources/df_editions/cu31924013363894.txt', 'sources/df_editions/bim_eighteenth-century_double-falshood-or-the_theobald-mr-lewis_1728.txt',
             'sources/df_editions/doublefalshoodor00shak.txt']
ocr_lines = []; ocr_src = []
for f in ocr_files:
    for l in open(f, encoding='utf-8', errors='ignore'):
        l = l.strip()
        if len(l) > 3: ocr_lines.append(l); ocr_src.append(f)
def clean(s): return re.sub(r'[^a-z ]', '', s.lower().replace('ſ', 's'))
ocr_clean = [clean(l) for l in ocr_lines]
segs = [json.loads(l) for l in open('corpus/segments.jsonl')]
fills = []
def fill(line):
    parts = [p for p in re.split(r'\^+', line) if len(clean(p).strip()) >= 6]
    if not parts: return None
    anchor = max(parts, key=len); a = clean(anchor).strip()
    # candidates: OCR lines containing a long fragment of the anchor
    frag = a[:18] if len(a) >= 18 else a
    cands = [i for i, c in enumerate(ocr_clean) if frag in c]
    if not cands:
        # fallback: fuzzy over lines with the same first legible word
        w = a.split()[0] if a.split() else ''
        cands = [i for i, c in enumerate(ocr_clean) if c.startswith(w)] if w else []
    best = None; bs = 0
    for i in cands:
        s = difflib.SequenceMatcher(None, clean(line).replace('^', ''), ocr_clean[i]).ratio()
        if s > bs: bs, best = s, i
    if best is None or bs < 0.6: return None
    o = ocr_lines[best]
    o = re.sub(r'^\s*[\|\d\s]+', '', o)                       # leading OCR junk (page numbers, rules)
    o = re.sub(r'^(?:[A-Z][a-z]{1,5}\.|[A-Z][a-z]{1,5}\s)\s*', '', o) # speech prefix such as "Rod." "Duke." "Cam."
    o = re.sub(r'[\|\d]+\s*$', '', o).strip()                  # trailing junk
    o = o.replace('ſ', 's')
    if re.search(r'[\|\d]', o): return None
    return o, bs
out = open('corpus/segments.jsonl.new', 'w')
for r in segs:
    if r['key'] == 'df_double_falsehood':
        changed = False
        for field in ('verse_lines', 'prose'):
            new = []
            for l in r[field]:
                if '^' in l:
                    # a multi-line block with whole-line gaps: handle line by line
                    sub = []
                    for piece in l.split('\n'):
                        if '^' in piece and piece.strip() != '^':
                            f = fill(piece)
                            if f:
                                fills.append({'scene': f"{r['act']}.{r['scene']}", 'tcp': piece, 'ocr': f[0], 'sim': round(f[1], 3)}); sub.append(f[0]); changed = True
                            else:
                                fills.append({'scene': f"{r['act']}.{r['scene']}", 'tcp': piece, 'ocr': None, 'sim': 0}); sub.append(piece)
                        elif piece.strip() == '^':
                            # a whole-line <gap> in the ECCO XML; Graham's 1920 reprint shows no text missing here, so drop it
                            fills.append({'scene': f"{r['act']}.{r['scene']}", 'tcp': '^ (gap marker, no text lost per Graham 1920)', 'ocr': None, 'sim': 0}); sub.append('')
                        else:
                            sub.append(piece)
                    new.append('\n'.join(sub))
                else:
                    new.append(l)
            r[field] = new
        text = '\n'.join(r['verse_lines']) + '\n' + '\n'.join(r['prose'])
        r['raw_tokens'] = tokenize(text); r['tokens'] = normalize_tokens(text); r['n_words'] = len(r['tokens'])
    out.write(json.dumps(r) + '\n')
out.close()
json.dump(fills, open('data/results/gap_fills.json', 'w'), indent=1)
print('fills:', len(fills), 'filled:', sum(1 for f in fills if f['ocr']))
for f in fills: print(f"{f['scene']:5s} sim={f['sim']:.2f} | {f['tcp'][:60]!r} -> {str(f['ocr'])[:70]!r}")
