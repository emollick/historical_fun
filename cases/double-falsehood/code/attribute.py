#!/usr/bin/env python3
"""Scene-level attribution engine.
Train on whole plays of the chosen classes (chunked to `size` tokens), then score every scene of the target play(s):
Cosine Delta distance to each class centroid, and a calibrated linear-SVM probability (Platt via CalibratedClassifierCV).
Usage: python3 attribute.py --classes SH,FL --targets collab_henry8,collab_tnk --features mfw300_noera --size 800
"""
import sys, os, json, argparse, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.calibration import CalibratedClassifierCV

def class_of(r, classes):
    g = r['group']
    if g in classes: return g
    if g == 'JAC' and ('JAC' in classes): return 'JAC'
    if g == 'JAC' and ('JAC_' + r['author'].replace('?', '')) in classes: return 'JAC_' + r['author'].replace('?', '')
    if g == 'R18' and 'R18' in classes: return 'R18'
    return None

def build_training(segs, classes, size, exclude_keys=(), late_only=False):
    plays, meta = play_tokens([r for r in segs if r['key'] not in exclude_keys])
    X = []; y = []; pk = []
    for r in segs:
        pass
    seen = set()
    for r in segs:
        if r['key'] in seen or r['key'] in exclude_keys: continue
        c = class_of(r, classes)
        if c is None: continue
        if late_only and c == 'SH' and r['date'] < 1600: continue
        seen.add(r['key'])
        for ch in chunk(plays[r['key']], size):
            X.append(ch); y.append(c); pk.append(r['key'])
    return X, np.array(y), np.array(pk)

def make_vec(name):
    if name == 'mfw300': return MFW(300)
    if name == 'mfw300_noera': return MFW(300, exclude=ERA_MARKED)
    if name == 'mfw500_noera': return MFW(500, exclude=ERA_MARKED)
    if name == 'mfw150_noera': return MFW(150, exclude=ERA_MARKED)
    if name == 'char4': return CharNgram(4, 2000)
    if name == 'char3': return CharNgram(3, 1500)
    raise ValueError(name)

def fit_models(Xtr, ytr, vecname):
    vec = make_vec(vecname).fit(Xtr)
    X = vec.transform(Xtr)
    delta = Delta('cosine').fit(X, list(ytr))
    svm = make_pipeline(StandardScaler(), CalibratedClassifierCV(LinearSVC(C=0.1, max_iter=5000), cv=5))
    svm.fit(X, ytr)
    return vec, delta, svm

def score_scenes(segs_target, vec, delta, svm):
    docs = [r['tokens'] for r in segs_target]
    X = vec.transform(docs)
    pred, D = delta.predict(X)
    P = svm.predict_proba(X)
    out = []
    for i, r in enumerate(segs_target):
        d = {c: float(D[i, j]) for j, c in enumerate(delta.classes)}
        p = {c: float(P[i, j]) for j, c in enumerate(svm.classes_)}
        out.append({'key': r['key'], 'act': r['act'], 'scene': r['scene'], 'n_words': r['n_words'], 'head': r['head'][:50].replace('\n', ' '),
                    'delta': d, 'delta_pred': pred[i], 'svm_prob': p, 'svm_pred': max(p, key=p.get)})
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--classes', default='SH,FL'); ap.add_argument('--targets', default='collab_henry8,collab_tnk,df_double_falsehood')
    ap.add_argument('--features', default='mfw300_noera'); ap.add_argument('--size', type=int, default=800)
    ap.add_argument('--late', action='store_true'); ap.add_argument('--out', default=''); ap.add_argument('--cap', type=int, default=0)
    a = ap.parse_args()
    classes = a.classes.split(','); targets = a.targets.split(',')
    segs = load_segments()
    Xtr, ytr, pk = build_training(segs, classes, a.size, exclude_keys=set(targets), late_only=a.late)
    if a.cap:   # equal-corpus option: keep at most `cap` chunks per class, spread evenly over its plays
        rng = np.random.RandomState(1); keep = []
        for c in sorted(set(ytr)):
            idx = np.where(ytr == c)[0]
            keep.extend(idx if len(idx) <= a.cap else rng.choice(idx, a.cap, replace=False))
        keep = sorted(keep); Xtr = [Xtr[i] for i in keep]; ytr = ytr[keep]; pk = pk[keep]
        print('capped training chunks:', dict(zip(*np.unique(ytr, return_counts=True))))
    vec, delta, svm = fit_models(Xtr, ytr, a.features)
    res = {}
    for t in targets:
        st = [r for r in segs if r['key'] == t]
        res[t] = score_scenes(st, vec, delta, svm)
        print('==', t)
        for s in res[t]:
            dd = ' '.join(f"{c}={s['delta'][c]:.3f}" for c in sorted(s['delta']))
            pp = ' '.join(f"{c}={s['svm_prob'][c]:.2f}" for c in sorted(s['svm_prob']))
            print(f"{s['act']}.{s['scene']:<2d} w={s['n_words']:5d} delta-> {s['delta_pred']:8s} [{dd}]  svm-> {s['svm_pred']:8s} [{pp}]")
    if a.out: json.dump(res, open(a.out, 'w'), indent=1)
