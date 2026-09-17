#!/usr/bin/env python3
"""Per-scene linguistic markers for target plays and per-play/group reference distributions."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from collections import defaultdict
segs = load_segments()
KEYS = ['ye', 'em', 'hath', 'has', 'doth', 'does', 'ith', 'tis', 'sir', 'thou', 'I_am', 'im', 'ill', 'dont', 'its', 'fem_proxy']
targets = sys.argv[1].split(',') if len(sys.argv) > 1 else ['df_double_falsehood', 'collab_henry8', 'collab_tnk']
out = {}
for t in targets:
    print('==', t)
    print(f"{'scene':6s} {'words':>5s} " + ' '.join(f"{k[:6]:>6s}" for k in KEYS) + '  nverse')
    for r in segs:
        if r['key'] != t: continue
        m = markers(r); out[f"{t}|{r['act']}.{r['scene']}"] = m
        print(f"{r['act']}.{r['scene']:<4d} {m['n_words']:5d} " + ' '.join(f"{m[k]:6.2f}" for k in KEYS) + f"  {m['n_verse']}")
# reference: per play, then group mean and sd (plays as units)
plays = defaultdict(list)
for r in segs: plays[r['key']].append(r)
ref = defaultdict(list)
for k, rs in plays.items():
    g = rs[0]['group']
    toks = sum((r['tokens'] for r in rs), []); vl = sum((r['verse_lines'] for r in rs), [])
    m = markers({'tokens': toks, 'verse_lines': vl})
    ref[g].append((k, m))
print('\n== group reference (mean ± sd across plays)')
print(f"{'group':6s} {'n':>3s} " + ' '.join(f"{k[:6]:>11s}" for k in KEYS))
for g in ['SH', 'FL', 'BF', 'FX', 'MA', 'JAC', 'ADAPT', 'R18', 'THEO', 'THEOT', 'THEOV', 'CTRL', 'DF']:
    ms = [m for _, m in ref[g]]
    if not ms: continue
    line = f"{g:6s} {len(ms):3d} "
    for k in KEYS:
        v = np.array([m[k] for m in ms], dtype=float); v = v[~np.isnan(v)]
        line += f"{v.mean():5.2f}±{v.std():4.2f} "
    print(line)
json.dump({'scenes': out, 'plays': {k: m for g in ref for k, m in ref[g]}}, open('data/results/markers.json', 'w'), indent=1)
