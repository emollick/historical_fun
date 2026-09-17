#!/usr/bin/env python3
"""Leave-one-play-out validation at scene length (800-word chunks) with many author classes:
SH, FL, MA, every Jacobean dramatist with >= 3 plays, R18 and THEO. Features: 300 MFW minus era-marked tokens.
Classifiers: Cosine Delta and calibrated linear SVM. Reports per-class recall and the confusion matrix, so the reader
can see how often a Shakespeare scene is recognised as Shakespeare among Jacobean candidates and how often another
author's scene is mislabelled Shakespeare."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from attribute import make_vec
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from collections import Counter, defaultdict
SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 800
segs = load_segments(); plays, meta = play_tokens(segs)
def cls(r):
    g = r['group']
    if g in ('SH', 'FL', 'MA', 'R18', 'THEO'): return g
    if g == 'JAC': return 'JAC_' + r['author'].replace('?', '')
    return None
cls_of = {}
for r in segs:
    c = cls(r)
    if c: cls_of[r['key']] = c
cnt = Counter(cls_of.values()); cls_of = {k: v for k, v in cls_of.items() if cnt[v] >= 3}
keys = sorted(cls_of); print('plays', len(keys), dict(Counter(cls_of.values())), flush=True)
chunks = [(k, cls_of[k], ch) for k in keys for ch in chunk(plays[k], SIZE)]
vec = make_vec('mfw300_noera').fit([c[2] for c in chunks])
X = vec.transform([c[2] for c in chunks]); y = np.array([c[1] for c in chunks]); pk = np.array([c[0] for c in chunks])
res = {}
for clfname in ('cosine', 'svm'):
    pred = np.empty(len(y), dtype=object)
    for k in keys:
        tr = pk != k; te = pk == k
        if clfname == 'cosine':
            m = Delta('cosine').fit(X[tr], list(y[tr])); p, _ = m.predict(X[te]); pred[te] = p
        else:
            m = make_pipeline(StandardScaler(), LinearSVC(C=0.1, max_iter=5000)); m.fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
    acc = float((pred == y).mean()); per = {c: float((pred[y == c] == c).mean()) for c in sorted(set(y))}
    conf = defaultdict(lambda: defaultdict(int))
    for a, b in zip(y, pred): conf[a][b] += 1
    # how often non-Shakespeare chunks are labelled SH
    false_sh = {c: float((pred[y == c] == 'SH').mean()) for c in sorted(set(y)) if c != 'SH'}
    res[clfname] = {'acc': acc, 'per_class': per, 'confusion': {a: dict(b) for a, b in conf.items()}, 'false_SH_rate': false_sh, 'n_chunks': int(len(y))}
    print(f'{clfname}: acc={acc:.3f}', ' '.join(f'{c}={per[c]:.2f}' for c in sorted(per)), flush=True)
    print('   labelled SH although not:', ' '.join(f'{c}={false_sh[c]:.2f}' for c in sorted(false_sh)), flush=True)
json.dump(res, open(f'data/results/validate_many_{SIZE}.json', 'w'), indent=1)
