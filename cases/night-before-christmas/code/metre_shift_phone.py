"""Metre shift of Jackson's phoneme-pair statistic on the control authors.

For every control author with at least three anapestic and three other poems
(each with >= 12 favoured pairs, Jackson's rule), compute the mean share of
Livingston-favoured pairs in the author's anapestic poems and in the rest.
The pairs are the ten Livingston- and ten Moore-favoured pairs re-derived on our
corpora (replicate_full.json). Writes 'phone_rows' into metre_shift.json."""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis, replicate

OUT = analysis.OUT

def main():
    moore, liv, ctrl = analysis.load_all()
    R = json.load(open(os.path.join(OUT, 'replicate_full.json')))
    favL = [tuple(p.split()) for p in R['phoneme_pairs_discriminating']['livingston_favoured']]
    favM = [tuple(p.split()) for p in R['phoneme_pairs_discriminating']['moore_favoured']]
    by_author = {}
    for d in ctrl:
        by_author.setdefault(d['author'], []).append(d)
    rows = []
    for a, docs in sorted(by_author.items()):
        an = [d for d in docs if d['form_class'] == 'anapestic']
        ot = [d for d in docs if d['form_class'] != 'anapestic']
        if len(an) < 3 or len(ot) < 3:
            continue
        def shares(ds):
            v = []
            for d in ds:
                s, n = replicate.phoneme_share(replicate.phoneme_pairs(d['verse_lines']), favL, favM)
                if n >= 12 and not math.isnan(s):
                    v.append(s)
            return v
        va, vo = shares(an), shares(ot)
        if len(va) < 3 or len(vo) < 3:
            continue
        rows.append([a, len(va), float(np.mean(va)), len(vo), float(np.mean(vo))])
        print(f'{a:32s} anap n={len(va):3d} {np.mean(va):5.1f} | other n={len(vo):3d} {np.mean(vo):5.1f} | diff {np.mean(va)-np.mean(vo):+5.1f}')
    diffs = [r[2] - r[4] for r in rows]
    print('phoneme share: mean (anapestic - other) =', round(float(np.mean(diffs)), 2), 'n authors', len(rows),
          'positive', sum(x > 0 for x in diffs))
    J = json.load(open(os.path.join(OUT, 'metre_shift.json')))
    J['phone_rows'] = rows
    J['phone_mean_shift'] = float(np.mean(diffs))
    wd = [r[2] - r[4] for r in J['word_rows']]
    J['word_mean_shift'] = float(np.mean(wd))
    json.dump(J, open(os.path.join(OUT, 'metre_shift.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
