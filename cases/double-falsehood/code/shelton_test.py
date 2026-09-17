#!/usr/bin/env python3
"""Does Double Falsehood echo Shelton's wording specifically in the Cardenio chapters (I.23-36)?
For n = 3 and 4: DF word n-grams (normalised) that occur in a given Shelton chapter set but nowhere in the play corpus
(SH, FL, FX, BF, BE, MA, JAC, R18, ADAPT excluding DF). Compare the Cardenio chapters against every other window of
14 consecutive Part I chapters and against Part II windows, per 1000 words of window."""
import sys, os, json, re, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from normalize import normalize_tokens
segs = load_segments()
def grams(toks, n): return set(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))
df = [r for r in segs if r['key'] == 'df_double_falsehood']
df_toks = sum((r['tokens'] for r in df), [])
corpus_grams = {3: set(), 4: set()}
for r in segs:
    if r['group'] in ('DF', 'SRC'): continue
    for n in (3, 4): corpus_grams[n] |= grams(r['tokens'], n)
chap = {}
for f in sorted(glob.glob('corpus/shelton/partI_ch*.txt')):
    k = int(re.search(r'ch(\d+)', f).group(1)); chap[k] = normalize_tokens(open(f).read())
print('chapters', len(chap), 'DF words', len(df_toks))
res = {}
for n in (3, 4):
    dfg = grams(df_toks, n) - corpus_grams[n]   # DF phrases not found in any play in the corpus
    print(f'\nn={n}: DF phrases absent from the play corpus: {len(dfg)}')
    rows = []
    for start in range(1, 40):
        ks = list(range(start, start + 14)); toks = sum((chap[k] for k in ks), [])
        g = grams(toks, n); hits = dfg & g
        rows.append((start, start + 13, len(toks), len(hits), len(hits) / len(toks) * 1000))
    for s, e, nw, h, rate in rows:
        flag = ' <== Cardenio chapters' if s == 23 else ''
        print(f'ch {s:2d}-{e:2d} words={nw:6d} hits={h:3d} per1000={rate:.3f}{flag}')
    res[n] = rows
    # examples for the Cardenio window
    ks = list(range(23, 37)); toks = sum((chap[k] for k in ks), []); hits = dfg & grams(toks, n)
    ex = sorted(' '.join(h) for h in hits)
    print('examples (Cardenio window):', '; '.join(ex[:80]))
    res[f'examples_{n}'] = ex
json.dump(res, open('data/results/shelton_test.json', 'w'), indent=1)
