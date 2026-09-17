#!/usr/bin/env python3
"""Calibrate the 'anachronism count': for the Beale letters (+cipher 2 plaintext) and for
2716-word samples of genuine 1805-1843 American writing, count the word types whose Google
Books (American English) frequency before 1822 is very low relative to 1850-1900.
Inputs: results/lang_ngram_letters.csv and results/lang_ngram_calib_<author>.csv (from
lang_ngram_query.py).  Output: results/lang_ngram_calibration.md/.csv"""
import os, csv, glob, math
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.join(B, 'results')
STOP = set('''the of and to a in that it is was i for be as with his he by on at not this which have from or are but had were you my an all so their they one we been will if more no her its them would there our when who what has him me your do than any some into can may should these could up then now out very only such upon other those us shall must did might over after also being here where how well before too again most much through both same own ever never yet still each while about against because under between since without thus hence whether either neither nor though although until unless even indeed perhaps quite rather almost always often sometimes soon already once whose whom myself himself themselves itself yourself ourselves another every few many less least far further last first next several whatever whenever wherever off down back away along across among within around during above below near till'''.split())
def load(f):
    rows = []
    for r in csv.DictReader(open(f)):
        if r['proper'] or r['word'] in STOP or len(r['word']) < 3 or r['word'] == 'etc': continue
        try: pre = float(r['pre1822_mean']); late = float(r['mean_1850_1900']); yrs = int(r['pre1822_years'])
        except Exception: continue
        rows.append(dict(word=r['word'], pre=pre, late=late, yrs=yrs, ratio=(pre / late if late > 0 else float('inf'))))
    return rows
def stats(rows):
    n = len(rows)
    def frac(cond): return sum(1 for r in rows if cond(r)) / n
    return dict(n_types=n,
        absent_pre1822=frac(lambda r: r['yrs'] == 0),
        rare_pre1822_lt1e7=frac(lambda r: r['pre'] < 1e-7 and r['late'] > 0),
        ratio_lt_0_1=frac(lambda r: r['late'] > 1e-8 and r['ratio'] < 0.1),
        ratio_lt_0_25=frac(lambda r: r['late'] > 1e-8 and r['ratio'] < 0.25),
        strong=frac(lambda r: r['late'] > 3e-8 and r['ratio'] < 0.05),
        examples_strong=[r['word'] for r in sorted(rows, key=lambda r: r['ratio']) if r['late'] > 3e-8 and r['ratio'] < 0.05][:12])
out = {}
for f in sorted(glob.glob(os.path.join(R, 'lang_ngram_calib_*.csv'))) + [os.path.join(R, 'lang_ngram_letters.csv'), os.path.join(R, 'lang_ngram_narrative.csv')]:
    if not os.path.exists(f): continue
    name = os.path.basename(f).replace('lang_ngram_', '').replace('calib_', '').replace('.csv', '')
    out[name] = stats(load(f))
md = ['# Calibration of the anachronism count (Google Books en-US-2019, smoothing 0)\n',
      'Content-word types (function words, proper nouns, <3 letters excluded). "ratio" = mean relative frequency 1780-1821 / mean 1850-1900. '
      '"strong" = ratio < 0.05 with a 1850-1900 frequency above 3e-8 (i.e. words that were common later but essentially unattested before 1822).\n',
      '| text | content types | % absent pre-1822 | % pre-1822 freq < 1e-7 | % ratio < 0.1 | % ratio < 0.25 | % strong | strong examples |', '|---|---|---|---|---|---|---|---|']
with open(os.path.join(R, 'lang_ngram_calibration.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['text', 'n_types', 'absent_pre1822', 'rare_lt1e7', 'ratio_lt_0_1', 'ratio_lt_0_25', 'strong', 'strong_examples'])
    for k, s in out.items():
        w.writerow([k, s['n_types'], f"{s['absent_pre1822']:.4f}", f"{s['rare_pre1822_lt1e7']:.4f}", f"{s['ratio_lt_0_1']:.4f}", f"{s['ratio_lt_0_25']:.4f}", f"{s['strong']:.4f}", ' '.join(s['examples_strong'])])
        md.append(f"| {k} | {s['n_types']} | {100*s['absent_pre1822']:.1f} | {100*s['rare_pre1822_lt1e7']:.1f} | {100*s['ratio_lt_0_1']:.1f} | {100*s['ratio_lt_0_25']:.1f} | {100*s['strong']:.2f} | {', '.join(s['examples_strong'])} |")
ctrl = [s for k, s in out.items() if k not in ('letters', 'narrative')]
if ctrl:
    import statistics as st
    for key in ['ratio_lt_0_1', 'ratio_lt_0_25', 'strong', 'rare_pre1822_lt1e7']:
        vals = [s[key] for s in ctrl]; L = out.get('letters', {}).get(key)
        md.append(f"\n{key}: genuine 1805-1843 controls mean {100*st.mean(vals):.2f}% (sd {100*(st.pstdev(vals) if len(vals)>1 else 0):.2f}, n={len(vals)}, max {100*max(vals):.2f}%); Beale letters {100*L:.2f}% -> z = {(L-st.mean(vals))/(st.pstdev(vals) or 1e-9):+.1f}; controls above the letters' value: {sum(1 for v in vals if v >= L)}/{len(vals)}")
open(os.path.join(R, 'lang_ngram_calibration.md'), 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
