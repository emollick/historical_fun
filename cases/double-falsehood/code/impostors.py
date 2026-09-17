#!/usr/bin/env python3
"""General Impostors (GI) verification (Koppel & Winter 2014; Kestemont et al. 2016) at scene level.
For a target scene and a candidate author, repeat: sample a random 50% of features and a random subset of impostor
documents; check whether the nearest document (min-max / cosine distance on MFW) belongs to the candidate. Score = share of
iterations won by the candidate. Run for candidates SH and FL (and THEO when available) against impostors drawn from
Jacobean dramatists (JAC, MA, BF, FX, BE) and 18th-century plays (R18).
Usage: python3 impostors.py --target df_double_falsehood --candidates SH,FL --size 800 --iters 200
"""
import sys, os, json, argparse, random, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *

def minmax(a, b):
    return 1 - np.minimum(a, b).sum() / max(1e-9, np.maximum(a, b).sum())

def cos(a, b):
    return 1 - (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

ap = argparse.ArgumentParser()
ap.add_argument('--target', default='df_double_falsehood'); ap.add_argument('--candidates', default='SH,FL')
ap.add_argument('--size', type=int, default=800); ap.add_argument('--iters', type=int, default=200); ap.add_argument('--nfeat', type=int, default=300)
ap.add_argument('--impostor_groups', default='JAC,MA,BF,FX,BE,R18'); ap.add_argument('--exclude_keys', default='')
ap.add_argument('--out', default='')
a = ap.parse_args()
random.seed(1); np.random.seed(1)
segs = load_segments()
plays, meta = play_tokens(segs)
cands = a.candidates.split(','); igroups = set(a.impostor_groups.split(','))
excl = set(a.exclude_keys.split(',')) | {a.target}
docs = []  # (label, key, tokens)
for k, (g, auth, d) in meta.items():
    if k in excl: continue
    if g in cands: lab = g
    elif g in igroups: lab = 'IMP:' + (auth if g == 'JAC' else g)
    else: continue
    for ch in chunk(plays[k], a.size):
        docs.append((lab, k, ch))
vec = MFW(a.nfeat, exclude=ERA_MARKED).fit([d[2] for d in docs])
X = vec.transform([d[2] for d in docs]); labs = np.array([d[0] for d in docs]); keys = np.array([d[1] for d in docs])
# z-score
mu = X.mean(0); sd = X.std(0) + 1e-9; Z = (X - mu) / sd
targets = [r for r in segs if r['key'] == a.target]
T = (vec.transform([r['tokens'] for r in targets]) - mu) / sd
imp_idx = np.where(np.char.startswith(labs.astype(str), 'IMP:'))[0]
res = []
for ti, r in enumerate(targets):
    t = T[ti]
    scores = {}
    for c in cands:
        cidx = np.where(labs == c)[0]
        wins = 0
        for it in range(a.iters):
            f = np.random.rand(Z.shape[1]) < 0.5
            imp = np.random.choice(imp_idx, size=min(len(imp_idx), 300), replace=False)
            ci = np.random.choice(cidx, size=min(len(cidx), 300), replace=False)
            pool = np.concatenate([ci, imp])
            D = np.array([cos(t[f], Z[j][f]) for j in pool])
            # nearest document
            j = pool[D.argmin()]
            if labs[j] == c: wins += 1
        scores[c] = wins / a.iters
    res.append({'act': r['act'], 'scene': r['scene'], 'n_words': r['n_words'], 'gi': scores})
    print(f"{r['act']}.{r['scene']:<3d} w={r['n_words']:5d} " + ' '.join(f"GI({c})={scores[c]:.2f}" for c in cands))
if a.out: json.dump(res, open(a.out, 'w'), indent=1)
