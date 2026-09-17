"""Collect every number the report quotes into results/tables.json and print them."""
import json, os, sys
import numpy as np
from collections import Counter
R = sys.argv[1] if len(sys.argv) > 1 else 'results'
def margin(rec, ty): o = rec['ngrams'][ty]; return o['lincoln'] - o['hay']
def vote(rec, lo=4, hi=10):
    c = Counter()
    for n in range(lo, hi+1):
        d = margin(rec, f'c{n}'); c['lincoln' if d > 0 else 'hay' if d < 0 else 'tie'] += 1
    c.pop('tie', None); return c.most_common(1)[0][0] if c else 'tie'
T = {}
bands = [(50, 100), (100, 200), (200, 400)]
for design in ['ownhand', 'grieve', 'ownhand_all']:
    p = f'{R}/{design}/results.json'
    if not os.path.exists(p): continue
    r = json.load(open(p)); t = r['tests']
    D = {'sizes': r['sizes'], 'target': r['target_words'], 'nseq': r['nseq'], 'sets': {}}
    for setname, recs_all in t.items():
        S = {}
        for lo, hi in bands:
            recs = [v for v in recs_all.values() if lo <= v['words'] < hi]
            if not recs: continue
            row = {'n': len(recs)}
            for ty in ['w1', 'w2', 'w3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c12', 'c14', 'c16']:
                row[ty] = round(np.mean([margin(v, ty) > 0 for v in recs]), 3)
            row['vote'] = round(np.mean([vote(v) == 'lincoln' for v in recs]), 3)
            S[f'{lo}-{hi}'] = row
        # all
        recs = list(recs_all.values())
        S['all'] = {'n': len(recs), 'vote': round(np.mean([vote(v) == 'lincoln' for v in recs]), 3)}
        D['sets'][setname] = S
    D['specials'] = {k: {'words': v['words'], 'truth': v['truth'], 'vote': vote(v), 'margins': {ty: round(margin(v, ty), 3) for ty in ['w1','w2','w3','c4','c5','c6','c7','c8','c9','c10','c12','c14','c16']}} for k, v in t['specials'].items()}
    T[design] = D
    print(f"\n## {design} sizes={r['sizes']} nseq={r['nseq']}")
    for setname, S in D['sets'].items():
        for band, row in S.items():
            if band == 'all': print(f"  {setname:22s} all n={row['n']:4d} vote L-share={row['vote']:.3f}"); continue
            print(f"  {setname:22s} {band:8s} n={row['n']:4d} " + ' '.join(f"{ty}={row[ty]:.2f}" for ty in ['w1','w2','c4','c6','c8','c10','c12','c16']) + f" vote={row['vote']:.2f}")
    print("  specials:", {k: (v['vote'], v['margins']['c8']) for k, v in D['specials'].items()})
json.dump(T, open(f'{R}/tables.json', 'w'), indent=1)
