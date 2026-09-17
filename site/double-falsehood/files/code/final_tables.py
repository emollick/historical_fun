#!/usr/bin/env python3
"""Aggregate every result into data/results/final_tables.json and print the tables used in the report."""
import json, os, numpy as np, collections
R = 'data/results'
def load(p):
    p = os.path.join(R, p); return json.load(open(p)) if os.path.exists(p) else None
SC = ['1.1','1.2','1.3','2.1','2.2','2.3','2.4','3.1','3.2','3.3','4.1','4.2','5.1','5.2']
out = {'scenes': {s: {} for s in SC}}
def sid(r): return f"{r['act']}.{r['scene']}"
# attribution runs
for fn, tag in [('df_SH_FL_mfw300_noera.json', 'c2'), ('df_SH_FL_R18_mfw300_noera.json', 'c3'), ('df_SH_FL_THEO_mfw300_noera.json', 'c3t'),
                ('df_SH_FL_THEO_R18_mfw300_noera.json', 'c4'), ('df_multi10_cap150_mfw300_noera.json', 'c10'), ('df_SH_FL_R18_char4_800.json', 'c3char4')]:
    d = load(fn)
    if not d: print('missing', fn); continue
    for r in d['df_double_falsehood']:
        s = sid(r); out['scenes'][s]['n_words'] = r['n_words']
        out['scenes'][s][tag] = {'delta_pred': r['delta_pred'], 'svm': {k: round(v, 3) for k, v in r['svm_prob'].items()}, 'delta': {k: round(v, 3) for k, v in r['delta'].items()}}
# impostors
for fn, tag in [('gi_df_SH_FL.json', 'gi2'), ('gi_df_SH_FL_THEO.json', 'gi3')]:
    d = load(fn)
    if not d: continue
    for r in d:
        out['scenes'][sid(r)][tag] = {k: round(v, 3) for k, v in r['gi'].items()}
# phrase links (3-gram, originals of adaptations excluded)
d = load('phrase_links_3_ext_noorig.json')
for k, v in d['scenes'].items():
    key, s = k.split('|')
    if key != 'df_double_falsehood': continue
    n = v['n_words']; L = v['links']
    out['scenes'][s]['links3'] = {a: round(L.get(a, 0) / n * 1000, 2) for a in ('Shakespeare', 'Fletcher', 'R18', 'Theobald')}
d = load('phrase_links_4_ext_noorig.json')
for k, v in d['scenes'].items():
    key, s = k.split('|')
    if key != 'df_double_falsehood': continue
    n = v['n_words']; L = v['links']
    out['scenes'][s]['links4'] = {a: round(L.get(a, 0) / n * 1000, 2) for a in ('Shakespeare', 'Fletcher', 'R18', 'Theobald')}
# markers
d = load('markers.json')
for k, m in d['scenes'].items():
    if not k.startswith('df_double'): continue
    s = k.split('|')[1]
    out['scenes'][s]['markers'] = {x: (None if m[x] is None or (isinstance(m[x], float) and np.isnan(m[x])) else round(m[x], 2)) for x in ('ye', 'em', 'hath', 'has', 'doth', 'does', 'tis', 'sir', 'thou', 'fem_proxy', 'n_verse')}
out['marker_groups'] = {g: {x: round(float(np.nanmean([m[x] for kk, m in d['plays'].items() if kk.startswith(pref)])), 2) for x in ('ye', 'em', 'hath', 'doth', 'sir', 'fem_proxy')}
                        for g, pref in [('SH', 'sh_'), ('FL', 'fl_'), ('MA', 'ma_'), ('JAC', 'jac_'), ('ADAPT', 'ad_'), ('R18', 'r18_'), ('THEO', 'theo_')]} if 'plays' in d else {}
# calibration: survival curves
bins = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 1.01]
def binned(rows, val, retkey='ret4'):
    res = []
    for lo, hi in zip(bins, bins[1:]):
        sel = [x for x in rows if x.get(retkey) is not None and lo <= x[retkey] < hi and x.get('n_words', 300) >= 300]
        res.append({'bin': [lo, hi], 'n': len(sel), 'mean': round(float(np.mean([val(x) for x in sel])), 3) if sel else None})
    return res
d = load('adapt_survival_SH_FL_R18_mfw300_noera_800.json')
if d:
    rows = d if isinstance(d, list) else d.get('scenes', d.get('rows', []))
    if isinstance(rows, dict): rows = [x for v in rows.values() for x in v]
    try:
        out['survival_svm3'] = binned(rows, lambda x: x['p_orig'] if 'p_orig' in x else x['svm_prob'][x['orig_class']])
    except Exception as e: print('survival parse', e, list(rows[0].keys()) if rows else None)
d = load('gi_survival.json')
if d:
    out['survival_gi'] = binned(d, lambda x: x['gi'][x['orig_class']])
    out['survival_gi_other'] = binned(d, lambda x: x['gi']['FL' if x['orig_class'] == 'SH' else 'SH'])
# H8/TNK validation with the 3-class model (SH,FL,R18) and with 2-class
H8_SH = {'1.1','1.2','2.3','2.4','3.2','5.1'}; TNK_SH = {'1.1','1.2','1.3','1.4','1.5','2.1','3.1','3.2','5.1','5.3','5.4'}
for fn, tag in [('collab_SH_FL_mfw300_noera.json', 'c2'), ('collab_SH_FL_R18_mfw300_noera.json', 'c3'), ('df_SH_FL_THEO_R18_mfw300_noera.json', 'c4'), ('df_multi10_cap150_mfw300_noera.json', 'c10')]:
    d = load(fn)
    if not d: continue
    val = {}
    for play, acc in (('collab_henry8', H8_SH), ('collab_tnk', TNK_SH)):
        if play not in d: continue
        for r in d[play]:
            s = sid(r); truth = 'SH' if s in acc else 'FL'
            val[f'{play[7:]}|{s}'] = {'truth': truth, 'delta': r['delta_pred'], 'svm': r['svm_pred'], 'p_truth': round(r['svm_prob'].get(truth, 0), 3), 'n_words': r['n_words']}
    ok_svm = sum(1 for v in val.values() if v['svm'] == v['truth']); ok_d = sum(1 for v in val.values() if v['delta'] == v['truth'])
    out[f'h8tnk_{tag}'] = {'scenes': val, 'svm_correct': ok_svm, 'delta_correct': ok_d, 'n': len(val)}
    print(f'H8/TNK {tag}: svm {ok_svm}/{len(val)} delta {ok_d}/{len(val)}')
# many-class validation
d = load('validate_many_800.json')
if d: out['validate_many_800'] = {k: {'acc': v['acc'], 'per_class': v['per_class'], 'false_SH_rate': v['false_SH_rate']} for k, v in d.items()}
# THEO validation
d = load('theo_validate.json')
if d: out['theo_validate'] = {k: {'n': v['n_scenes'], 'svm_pred': v['svm_pred'], 'mean_svm_prob': {c: round(p, 3) for c, p in v['mean_svm_prob'].items()}} for k, v in d.items()}
# nulls
for fn, tag in [('gi_null_rowe_fair_penitent.json', 'gi_null_rowe'), ('gi_null_theo_orestes.json', 'gi_null_orestes')]:
    d = load(fn)
    if d: out[tag] = {'max_SH': round(max(r['gi']['SH'] for r in d), 3), 'max_FL': round(max(r['gi']['FL'] for r in d), 3), 'mean_SH': round(float(np.mean([r['gi']['SH'] for r in d])), 3), 'n': len(d)}
# phrase-link calibration groups (3-gram no-orig)
d = load('phrase_links_3_ext_noorig.json'); dj = load('phrase_links_3_jac.json')
groups = collections.defaultdict(list)
for src in (d, dj):
    for k, v in src['scenes'].items():
        key, s = k.split('|'); n = v['n_words']
        if n < 250: continue
        L = v['links']; row = (L.get('Shakespeare', 0) / n * 1000, L.get('Fletcher', 0) / n * 1000, L.get('R18', 0) / n * 1000)
        if key == 'collab_henry8': g = 'SH scenes H8/TNK' if s in H8_SH else 'FL scenes H8/TNK'
        elif key == 'collab_tnk': g = 'SH scenes H8/TNK' if s in TNK_SH else 'FL scenes H8/TNK'
        elif key == 'df_double_falsehood': g = 'DF'
        elif key.startswith('dfocr'): g = 'DF OCR copy'
        elif key.startswith('theo_'): g = 'Theobald plays and poem'
        elif key.startswith('mest'): g = 'Mestayer'
        elif key.startswith('r18_'): g = '18C plays'
        elif key.startswith('jac_') or key.startswith('ma_'): g = 'Other Jacobean (Massinger, Shirley, Ford, Webster, Middleton)'
        else: g = key
        groups[g].append(row)
out['links3_groups'] = {g: {'n': len(rs), 'SH_mean': round(float(np.mean([r[0] for r in rs])), 2), 'SH_median': round(float(np.median([r[0] for r in rs])), 2), 'SH_p90': round(float(np.percentile([r[0] for r in rs], 90)), 2),
                             'FL_mean': round(float(np.mean([r[1] for r in rs])), 2), 'FL_median': round(float(np.median([r[1] for r in rs])), 2), 'FL_p90': round(float(np.percentile([r[1] for r in rs], 90)), 2),
                             'R18_mean': round(float(np.mean([r[2] for r in rs])), 2)} for g, rs in groups.items()}
# retention of adaptations (play level) for the figure
d = load('adapt_retention.json'); agg = collections.defaultdict(lambda: [0, 0.0])
for x in d:
    if x['ret4'] is None: continue
    agg[x['key']][0] += x['n_words']; agg[x['key']][1] += x['ret4'] * x['n_words']
out['retention_plays'] = {k: round(v[1] / v[0], 3) for k, v in agg.items()}
out['ocr_retention_of_df'] = {'n2': 0.801, 'n4': 0.616}
json.dump(out, open(os.path.join(R, 'final_tables.json'), 'w'), indent=1)
# print scene table
print(f"{'sc':4s} {'w':>5s} | {'c2':>3s} {'c3 FL/SH/R18':>14s} | {'c4 FL/SH/THEO/R18':>19s} | {'c10 top':>18s} | {'GI SH/FL/THEO':>14s} | {'links3 SH/FL/R18':>16s} | {'hath doth ye em fem':>20s}")
for s in SC:
    x = out['scenes'][s]
    c3 = x.get('c3', {}).get('svm', {}); c4 = x.get('c4', {}).get('svm', {}); c10 = x.get('c10', {}).get('svm', {}); g3 = x.get('gi3', {}); l3 = x.get('links3', {}); m = x.get('markers', {})
    top = sorted(c10.items(), key=lambda kv: -kv[1])[:2]
    print(f"{s:4s} {x.get('n_words', 0):5d} | {x.get('c2', {}).get('svm', {}).get('FL', 0):.2f} {c3.get('FL', 0):.2f}/{c3.get('SH', 0):.2f}/{c3.get('R18', 0):.2f} | {c4.get('FL', 0):.2f}/{c4.get('SH', 0):.2f}/{c4.get('THEO', 0):.2f}/{c4.get('R18', 0):.2f} | {' '.join(f'{k[:6]} {v:.2f}' for k, v in top):18s} | {g3.get('SH', 0):.2f}/{g3.get('FL', 0):.2f}/{g3.get('THEO', 0):.2f} | {l3.get('Shakespeare', 0):5.1f}/{l3.get('Fletcher', 0):5.1f}/{l3.get('R18', 0):5.1f} | {m.get('hath', 0):.2f} {m.get('doth', 0):.2f} {m.get('ye', 0):.2f} {m.get('em', 0):.2f} {m.get('fem_proxy', 0):.2f}")
print('survival svm3:', out.get('survival_svm3')); print('survival gi:', out.get('survival_gi')); print('gi nulls:', out.get('gi_null_rowe'), out.get('gi_null_orestes'))
print('marker groups:', json.dumps(out['marker_groups']))
