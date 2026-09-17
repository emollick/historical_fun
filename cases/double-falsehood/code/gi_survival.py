#!/usr/bin/env python3
"""GI (impostors) survival calibration: run the impostors verifier over adaptation scenes of Shakespeare and Fletcher originals
(excluding the original play from the candidate pool) and record GI(orig author) against wording retention."""
import sys, os, json, subprocess, time, numpy as np
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
T0 = time.time()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
segs = load_segments()
adapts = {}
for r in segs:
    if r['group'] == 'ADAPT':
        adapts.setdefault(r['key'], r['note'].split('orig=')[1].split(' by ')[0])
ret = {(x['key'], x['act'], x['scene']): x for x in json.load(open('data/results/adapt_retention.json'))}
rows = []
for k, ok in sorted(adapts.items()):
    oc = 'SH' if ok.startswith('sh') else ('FL' if ok.startswith('fl_') else None)
    if oc is None: continue
    out = f'data/results/gi_adapt_{k}.json'
    if not os.path.exists(out):
        if time.time() - T0 > BUDGET: print('BUDGET reached before', k, flush=True); continue
        subprocess.run(['python3', 'code/impostors.py', '--target', k, '--candidates', 'SH,FL', '--size', '800', '--iters', '100', '--exclude_keys', ok.replace('+', ','), '--out', out],
                   stdout=subprocess.DEVNULL)
    if not os.path.exists(out): print('MISSING', k, flush=True); continue
    for s in json.load(open(out)):
        rr = ret.get((k, s['act'], s['scene']), {})
        s.update({'key': k, 'orig': ok, 'orig_class': oc, 'ret4': rr.get('ret4')}); rows.append(s)
    print(k, oc, 'mean GI(orig)=%.2f' % np.mean([s['gi'][oc] for s in json.load(open(out))]), flush=True)
json.dump(rows, open('data/results/gi_survival.json', 'w'), indent=1)
bins = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 1.01]
for lo, hi in zip(bins, bins[1:]):
    sel = [s for s in rows if s['ret4'] is not None and lo <= s['ret4'] < hi and s['n_words'] >= 300]
    if sel: print(f"[{lo:.2f},{hi:.2f}) GI(orig)={np.mean([s['gi'][s['orig_class']] for s in sel]):.2f} GI(other)={np.mean([s['gi']['FL' if s['orig_class']=='SH' else 'SH'] for s in sel]):.2f} n={len(sel)}")
