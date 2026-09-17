#!/usr/bin/env python3
"""Aggregate every scene-level result for Double Falsehood into one table (data/results/df_summary.json and a printed view)."""
import json, glob, os, numpy as np
R = 'data/results'
scenes = ['1.1','1.2','1.3','2.1','2.2','2.3','2.4','3.1','3.2','3.3','4.1','4.2','5.1','5.2']
def load(fn):
    p = os.path.join(R, fn)
    return json.load(open(p)) if os.path.exists(p) else None
tab = {s: {} for s in scenes}
def put(tag, res, key=lambda x: None):
    for x in res:
        s = f"{x['act']}.{x['scene']}"
        if s in tab: tab[s][tag] = key(x)
# two-class and three-class Delta/SVM
for fn, tag in [('df_SH_FL_mfw300_noera.json', '2c'), ('df_SH_FL_R18_mfw300_noera.json', '3c'), ('df_SH_FL_R18_mfw300_800.json', '3c_all'),
                ('df_SH_FL_R18_char4_800.json', '3c_char4'), ('df_SH_FL_R18_mfw500_noera_800.json', '3c_500'), ('df_SH_FL_R18_mfw150_noera_800.json', '3c_150'),
                ('df_SH_FL_R18_mfw300_noera_lateSH.json', '3c_late'), ('df_multiclass_mfw300_noera.json', '16c'),
                ('df_SH_FL_THEO_mfw300_noera.json', 'theo3'), ('df_SH_FL_THEO_R18_mfw300_noera.json', 'theo4')]:
    d = load(fn)
    if d:
        res = d['df_double_falsehood']
        put(tag + '_delta', res, lambda x: x['delta_pred'])
        put(tag + '_svm', res, lambda x: {k: round(v, 2) for k, v in x['svm_prob'].items()})
g = load('gi_df_SH_FL.json')
if g: put('gi', g, lambda x: {k: round(v, 2) for k, v in x['gi'].items()})
g = load('gi_df_SH_FL_THEO.json')
if g: put('gi_theo', g, lambda x: {k: round(v, 2) for k, v in x['gi'].items()})
m = load('markers.json')
if m:
    for k, v in m['scenes'].items():
        if k.startswith('df_double_falsehood|'):
            s = k.split('|')[1]
            if s in tab: tab[s]['markers'] = {x: round(v[x], 2) for x in ['ye', 'em', 'hath', 'doth', 'has', 'does', 'fem_proxy', 'n_words']}
p = load('phrase_links_3.json')
if p:
    for k, v in p['scenes'].items():
        if k.startswith('df_double_falsehood|'):
            s = k.split('|')[1]
            if s in tab: tab[s]['links'] = {x: v['links'].get(x, 0) for x in ['Shakespeare', 'Fletcher', 'Beaumont+Fletcher', 'Fletcher+other', 'Shirley', 'R18', 'Theobald']}
json.dump(tab, open(os.path.join(R, 'df_summary.json'), 'w'), indent=1)
print(f"{'scene':6s} {'2c':4s} {'3c':4s} {'3c_svm(FL/SH/R18)':22s} {'16c':10s} {'GI SH/FL':10s} {'links SH/FL/R18':18s} {'ye/em/hath/fem':16s}")
for s in scenes:
    t = tab[s]
    sv = t.get('3c_svm', {}); gi = t.get('gi', {}); ln = t.get('links', {}); mk = t.get('markers', {})
    print(f"{s:6s} {t.get('2c_delta','-'):4s} {t.get('3c_delta','-'):4s} {sv.get('FL','-')}/{sv.get('SH','-')}/{sv.get('R18','-'):<8} {t.get('16c_delta','-'):10s} {gi.get('SH','-')}/{gi.get('FL','-'):<6} {ln.get('Shakespeare','-')}/{ln.get('Fletcher','-')}/{ln.get('R18','-'):<10} {mk.get('ye','-')}/{mk.get('em','-')}/{mk.get('hath','-')}/{mk.get('fem_proxy','-')}")
