#!/usr/bin/env python3
"""Scene-length validation: leave-one-play-out classification of chunks among Shakespeare (SH), Fletcher (FL), Massinger (MA)
and, in a second run, 13 Jacobean dramatists + 18th-century plays (R18) as separate classes.
Feature sets: MFW-300 all words; MFW-300 minus era-marked tokens; char 4-grams (top 2000).
Classifiers: Cosine Delta (nearest centroid), Burrows Delta, linear SVM (standardised features).
"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from collections import defaultdict

def author_class(r):
    g = r['group']
    if g in ('SH', 'FL', 'MA', 'R18'): return g
    if g == 'JAC': return 'JAC_' + r['author'].replace('?', '')
    return None

def run(classes_mode, sizes=(300, 500, 800, 1200, 2000), out='data/results/validate_chunks.json', min_plays=3):
    segs = load_segments()
    plays, meta = play_tokens(segs)
    cls_of = {}
    for r in segs:
        c = author_class(r)
        if c is None: continue
        if classes_mode == 'three' and c not in ('SH', 'FL', 'MA'): continue
        if classes_mode == 'many' and c == 'R18': continue
        if classes_mode == 'many18' and c.startswith('JAC_'): continue
        cls_of[r['key']] = c
    # drop authors with too few plays
    cnt = Counter(cls_of.values())
    cls_of = {k: v for k, v in cls_of.items() if cnt[v] >= min_plays}
    keys = sorted(cls_of)
    print(classes_mode, 'plays:', len(keys), 'classes:', dict(Counter(cls_of.values())))
    results = {}
    for size in sizes:
        chunks = []  # (key, cls, tokens)
        for k in keys:
            for ch in chunk(plays[k], size):
                chunks.append((k, cls_of[k], ch))
        feats = {'mfw300': MFW(300), 'mfw300_noera': MFW(300, exclude=ERA_MARKED), 'char4': CharNgram(4, 2000)}
        for fname, vec in feats.items():
            vec.fit([c[2] for c in chunks])
            X = vec.transform([c[2] for c in chunks]); y = np.array([c[1] for c in chunks]); pk = np.array([c[0] for c in chunks])
            for clfname in ['cosine', 'burrows', 'svm']:
                pred = np.empty(len(y), dtype=object)
                for k in keys:
                    tr = pk != k; te = pk == k
                    if clfname in ('cosine', 'burrows'):
                        m = Delta(clfname).fit(X[tr], list(y[tr])); p, _ = m.predict(X[te]); pred[te] = p
                    else:
                        m = make_pipeline(StandardScaler(), LinearSVC(C=0.1, max_iter=5000)); m.fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
                acc = float((pred == y).mean())
                per = {c: float((pred[y == c] == c).mean()) for c in sorted(set(y))}
                conf = defaultdict(lambda: defaultdict(int))
                for a, b in zip(y, pred): conf[a][b] += 1
                results[f'{size}|{fname}|{clfname}'] = {'size': size, 'features': fname, 'clf': clfname, 'n_chunks': int(len(y)), 'acc': acc, 'per_class': per,
                                                        'confusion': {a: dict(b) for a, b in conf.items()}}
                print(f'{size:5d} {fname:14s} {clfname:8s} n={len(y):5d} acc={acc:.3f} ' + ' '.join(f'{c}={per[c]:.2f}' for c in sorted(per)))
    json.dump(results, open(out, 'w'), indent=1)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'three'
    run(mode, out=f'data/results/validate_chunks_{mode}.json')
