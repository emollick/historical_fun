#!/usr/bin/env python3
"""Adaptation-layer calibration: score every scene of every adaptation whose original is by Shakespeare or Fletcher
with a classifier trained on Shakespeare vs Fletcher (optionally + 18th-century plays R18), EXCLUDING the original play
from training, and relate the result to the scene's wording retention (adapt_retention.json)."""
import sys, os, json, argparse, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from attribute import build_training, fit_models, score_scenes

ap = argparse.ArgumentParser()
ap.add_argument('--classes', default='SH,FL'); ap.add_argument('--features', default='mfw300_noera'); ap.add_argument('--size', type=int, default=800)
a = ap.parse_args()
classes = a.classes.split(',')
segs = load_segments()
ret = {(x['key'], x['act'], x['scene']): x for x in json.load(open('data/results/adapt_retention.json'))}
adapts = {}
for r in segs:
    if r['group'] == 'ADAPT':
        ok = r['note'].split('orig=')[1].split(' by ')[0]
        adapts.setdefault(r['key'], ok)
# original author class of each adaptation
orig_class = {}
for k, ok in adapts.items():
    if ok.startswith('sh_') or ok.startswith('shx_'): orig_class[k] = 'SH'
    elif ok.startswith('fl_'): orig_class[k] = 'FL'
    else: orig_class[k] = None   # Fletcher+other / Beaumont+Fletcher: skip
rows = []
cache = {}
for k, ok in sorted(adapts.items()):
    oc = orig_class[k]
    if oc is None: continue
    if ok not in cache:
        Xtr, ytr, pk = build_training(segs, classes, a.size, exclude_keys=set(ok.split('+')))
        cache[ok] = fit_models(Xtr, ytr, a.features)
    vec, delta, svm = cache[ok]
    st = [r for r in segs if r['key'] == k]
    sc = score_scenes(st, vec, delta, svm)
    for s in sc:
        rr = ret.get((k, s['act'], s['scene']), {})
        s.update({'orig': ok, 'orig_class': oc, 'ret4': rr.get('ret4'), 'ret2': rr.get('ret2'), 'adapter': st[0]['author'], 'date': st[0]['date']})
        rows.append(s)
    pc = np.mean([s['svm_prob'][oc] for s in sc]); dc = np.mean([s['delta_pred'] == oc for s in sc])
    print(f"{k:30s} orig={oc} scenes={len(sc):2d} mean ret4={np.nanmean([s['ret4'] or 0 for s in sc]):.2f} P(orig)={pc:.2f} delta-correct={dc:.2f}")
json.dump(rows, open(f"data/results/adapt_survival_{'_'.join(classes)}_{a.features}_{a.size}.json", 'w'), indent=1)
# binned summary
print('\nretention bin -> mean P(orig author) [svm], share delta-correct, n scenes')
bins = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 1.01]
for lo, hi in zip(bins, bins[1:]):
    sel = [s for s in rows if s['ret4'] is not None and lo <= s['ret4'] < hi and s['n_words'] >= 300]
    if not sel: continue
    print(f"[{lo:.2f},{hi:.2f}) P(orig)={np.mean([s['svm_prob'][s['orig_class']] for s in sel]):.2f} delta-correct={np.mean([s['delta_pred']==s['orig_class'] for s in sel]):.2f} n={len(sel)}")
