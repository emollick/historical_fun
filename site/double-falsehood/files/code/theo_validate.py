#!/usr/bin/env python3
"""Can the Theobald class be recognised at scene length? Leave-one-play-out over Theobald's own plays (THEO) and a
sample of 18th-century plays (R18) and the OCR copy of Double Falsehood: train SH/FL/THEO/R18 (and SH/FL/THEO) without
the held-out play, score its ~800-word pseudo-scenes, report where they land."""
import sys, os, json, time, numpy as np
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
T0 = time.time()
OUT = 'data/results/theo_validate.json'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from attribute import build_training, fit_models, score_scenes
segs = load_segments()
theo = sorted({r['key'] for r in segs if r['group'] == 'THEO'})
r18 = ['r18_rowe_fair_penitent', 'r18_rowe_lady_jane_gray', 'r18_hill_athelwold', 'r18_thomson_sophonisba', 'r18_savage_overbury',
       'r18_dennis_liberty_asserted', 'r18_manley_lucius', 'r18_philips_briton']
ctrl = ['mestayer_perfidious_brother', 'dfocr_double_falsehood', 'df_double_falsehood']
out = json.load(open(OUT)) if os.path.exists(OUT) else {}
for classes in (['SH', 'FL', 'THEO', 'R18'], ['SH', 'FL', 'THEO']):
    cname = ','.join(classes)
    for k in theo + r18 + ctrl:
        if f'{cname}|{k}' in out: continue
        if time.time() - T0 > BUDGET: print('BUDGET reached before', cname, k, flush=True); continue
        Xtr, ytr, pk = build_training(segs, classes, 800, exclude_keys={k, 'df_double_falsehood', 'dfocr_double_falsehood'})
        vec, delta, svm = fit_models(Xtr, ytr, 'mfw300_noera')
        st = [r for r in segs if r['key'] == k and r['n_words'] >= 250]
        sc = score_scenes(st, vec, delta, svm)
        from collections import Counter
        dp = Counter(s['delta_pred'] for s in sc); sp = Counter(s['svm_pred'] for s in sc)
        mean_p = {c: float(np.mean([s['svm_prob'][c] for s in sc])) for c in classes}
        out[f'{cname}|{k}'] = {'classes': classes, 'key': k, 'n_scenes': len(sc), 'delta_pred': dict(dp), 'svm_pred': dict(sp), 'mean_svm_prob': mean_p, 'scenes': sc}
        print(f"{cname:16s} {k:30s} n={len(sc):2d} delta={dict(dp)} svm={dict(sp)} meanP=" + ' '.join(f'{c}={mean_p[c]:.2f}' for c in classes), flush=True)
        json.dump(out, open(OUT, 'w'), indent=1)
print('done', len(out))
