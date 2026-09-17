"""
calibrated_margins.py -- where does the disputed poem fall relative to KNOWN
56-line samples of each author, on the same scale?

For each feature set and reference set (whole corpora / anapestic verse only),
every known sample is scored leave-one-poem-out with margin = d(Livingston) -
d(Moore) (cosine delta to centroids; positive = nearer Moore). The poem's
margin is computed against the full reference. Output: per-author margin
distributions, the poem's margin, and its percentile within each author's
distribution, for the 1823 and 1844 texts.
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis
from stylo import make_samples, top_features, profile_attribution, counts_for

MOORE, LIV = analysis.MOORE, analysis.LIV
FS = {'mfw100': ('word', None, 100), 'mfw200': ('word', None, 200), 'mfw300': ('word', None, 300),
      'char3': ('char', 3, 500), 'char4': ('char', 4, 1000), 'phone': ('phone', None, 45)}

def run(dist='cosine'):
    moore, liv, ctrl = analysis.load_all()
    poems = {w: analysis.load_visit(w) for w in ('1823', '1844')}
    sm = make_samples(moore, 56); sl = make_samples(liv, 56)
    samples = sm + sl
    out = {}
    for fs, (kind, n, k) in FS.items():
        cnts = [counts_for(s, kind, n) for s in samples]
        pcs = {w: counts_for(p, kind, n) for w, p in poems.items()}
        for ref in ('both', 'anapestic', 'both_neutral'):
            recs = []
            for i, s in enumerate(samples):
                idx = [j for j, t in enumerate(samples) if j != i and not (t['poem_ids'] & s['poem_ids'])]
                if ref == 'anapestic':
                    idx = [j for j in idx if samples[j]['form_class'] == 'anapestic']
                rc = [cnts[j] for j in idx]; ra = [samples[j]['author'] for j in idx]
                feats = top_features(rc, k)
                if ref == 'both_neutral':
                    feats, _ = analysis.neutral_filter(feats, ctrl, kind, n)
                d = profile_attribution(cnts[i], rc, ra, feats, dist=dist)
                recs.append(dict(author=s['author'], form=s['form_class'], ids=s['ids'],
                                 margin=d[LIV] - d[MOORE]))
            idx = list(range(len(samples)))
            if ref == 'anapestic':
                idx = [j for j in idx if samples[j]['form_class'] == 'anapestic']
            rc = [cnts[j] for j in idx]; ra = [samples[j]['author'] for j in idx]
            feats = top_features(rc, k)
            if ref == 'both_neutral':
                feats, _ = analysis.neutral_filter(feats, ctrl, kind, n)
            pm = {w: (lambda d: d[LIV] - d[MOORE])(profile_attribution(pcs[w], rc, ra, feats, dist=dist)) for w in poems}
            def dist_of(a, f=None):
                return np.array([r['margin'] for r in recs if r['author'] == a and (f is None or r['form'] == f)])
            summary = {}
            for lab, a, f in (('moore_all', MOORE, None), ('moore_anap', MOORE, 'anapestic'),
                              ('liv_all', LIV, None), ('liv_anap', LIV, 'anapestic'), ('liv_other', LIV, 'other')):
                v = dist_of(a, f)
                summary[lab] = dict(n=int(len(v)), mean=float(v.mean()) if len(v) else None,
                                    sd=float(v.std()) if len(v) else None,
                                    min=float(v.min()) if len(v) else None, max=float(v.max()) if len(v) else None,
                                    pct_poem_1823=float((v < pm['1823']).mean() * 100) if len(v) else None,
                                    pct_poem_1844=float((v < pm['1844']).mean() * 100) if len(v) else None,
                                    frac_classified_moore=float((v > 0).mean()) if len(v) else None)
            out[f'{fs}|{ref}'] = dict(poem_margin=pm, summary=summary, records=recs)
            print(f"{fs:7s} {ref:13s} poem1823={pm['1823']:+.3f} poem1844={pm['1844']:+.3f} | " +
                  ' '.join(f"{lab}: mean={s['mean']:+.3f} n={s['n']} pct<poem={s['pct_poem_1823']:.0f}" for lab, s in summary.items() if s['n']))
    json.dump(out, open(os.path.join(analysis.OUT, f'margins_{dist}.json'), 'w'), indent=1)

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else 'cosine')
