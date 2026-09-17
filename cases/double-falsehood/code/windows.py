#!/usr/bin/env python3
"""Sliding-window attribution inside a play: consecutive windows of `win` tokens (step `step`) scored with the same
Cosine Delta / calibrated SVM machinery as attribute.py. Usage: python3 windows.py --target df_double_falsehood --classes SH,FL,R18 --win 400 --step 200"""
import sys, os, json, argparse, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from attribute import build_training, fit_models
ap = argparse.ArgumentParser()
ap.add_argument('--target', default='df_double_falsehood'); ap.add_argument('--classes', default='SH,FL,R18')
ap.add_argument('--features', default='mfw300_noera'); ap.add_argument('--size', type=int, default=800)
ap.add_argument('--win', type=int, default=400); ap.add_argument('--step', type=int, default=200); ap.add_argument('--out', default='')
a = ap.parse_args()
classes = a.classes.split(',')
segs = load_segments()
Xtr, ytr, pk = build_training(segs, classes, a.size, exclude_keys={a.target})
vec, delta, svm = fit_models(Xtr, ytr, a.features)
rows = []
for r in segs:
    if r['key'] != a.target: continue
    toks = r['tokens']
    starts = list(range(0, max(1, len(toks) - a.win + 1), a.step)) if len(toks) >= a.win else [0]
    for s in starts:
        w = toks[s:s + a.win]
        X = vec.transform([w]); pred, D = delta.predict(X); P = svm.predict_proba(X)[0]
        rows.append({'act': r['act'], 'scene': r['scene'], 'start': s, 'end': min(len(toks), s + a.win), 'n': len(w),
                     'delta': {c: float(D[0, j]) for j, c in enumerate(delta.classes)}, 'svm': {c: float(P[j]) for j, c in enumerate(svm.classes_)}})
for x in rows:
    d = x['delta']; p = x['svm']
    print(f"{x['act']}.{x['scene']:<2d} [{x['start']:5d}-{x['end']:5d}] delta " + ' '.join(f"{c}={d[c]:.2f}" for c in sorted(d)) + '  svm ' + ' '.join(f"{c}={p[c]:.2f}" for c in sorted(p)))
if a.out: json.dump(rows, open(a.out, 'w'), indent=1)
