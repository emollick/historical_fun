#!/usr/bin/env python3
"""Which English translation of Don Quixote does Double Falsehood's wording follow, if any?
DF word n-grams (normalised, n = 3 and 4) absent from every play in the corpus (SH, FL, FX, BF, BE, MA, JAC, R18, ADAPT,
THEO, CTRL) are matched against the Cardenio chapters (Part I, 23-36) of Shelton 1612/1652, Phillips 1687 and Motteux 1700.
Reports hits per 1000 words of translation, hits unique to one translation, and the phrases themselves."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from normalize import normalize_tokens
segs = load_segments()
def grams(toks, n): return set(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))
df_toks = sum((r['tokens'] for r in segs if r['key'] == 'df_double_falsehood'), [])
corpus_grams = {3: set(), 4: set()}
for r in segs:
    if r['group'] in ('DF', 'SRC'): continue
    for n in (3, 4): corpus_grams[n] |= grams(r['tokens'], n)
tr = {'shelton': 'corpus/shelton/cardenio_ch23_36.txt',
      'phillips': 'corpus/raw_external/phillips_don_quixote_1687/phillips_dq_partI_ch23-36_cardenio.clean.txt',
      'motteux': 'corpus/raw_external/motteux_don_quixote_1700/motteux_dq_partI_ch23-36_cardenio.clean.txt'}
toks = {k: normalize_tokens(open(v, encoding='utf-8').read()) for k, v in tr.items()}
res = {}
for n in (3, 4):
    dfg = grams(df_toks, n) - corpus_grams[n]
    hits = {k: dfg & grams(t, n) for k, t in toks.items()}
    print(f'\nn={n}: DF phrases absent from the play corpus: {len(dfg)}')
    for k in tr:
        others = set().union(*(hits[o] for o in tr if o != k))
        uniq = hits[k] - others
        print(f'  {k:9s} words={len(toks[k]):6d} hits={len(hits[k]):3d} per1000={len(hits[k])/len(toks[k])*1000:.3f} unique={len(uniq)}')
        print('     unique:', '; '.join(sorted(' '.join(g) for g in uniq))[:1500])
        res[f'{k}_{n}'] = {'words': len(toks[k]), 'hits': sorted(' '.join(g) for g in hits[k]), 'unique': sorted(' '.join(g) for g in uniq)}
    common = set.intersection(*hits.values())
    print('  shared by all three:', '; '.join(sorted(' '.join(g) for g in common))[:1200])
    res[f'common_{n}'] = sorted(' '.join(g) for g in common)
json.dump(res, open('data/results/translations_test.json', 'w'), indent=1)
