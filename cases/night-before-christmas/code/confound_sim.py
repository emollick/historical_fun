"""
confound_sim.py -- does a whole-corpus two-author classifier mistake an author's
rare anapestic poems for a rival whose corpus is mostly anapestic? Simulated with
control authors: A = an author who, like Moore, wrote mostly non-anapestic verse
with a few anapests; B = a rival corpus built to look like Livingston's (about
half anapestic). For each (A, B) pair: reference = all of A's samples + B's
samples (leave-one-poem-out for the tested sample); test every A sample.
Report the share of A's ANAPESTIC samples attributed to B versus the share of
A's OTHER samples attributed to B.
"""
import os, sys, json, random
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis
from stylo import make_samples, top_features, profile_attribution, counts_for

def build_B(samples_b, rng, n_anap=16, n_other=21):
    an = [s for s in samples_b if s['form_class'] == 'anapestic']
    ot = [s for s in samples_b if s['form_class'] != 'anapestic']
    rng.shuffle(an); rng.shuffle(ot)
    return an[:n_anap] + ot[:n_other]

def run(fs_list=(('word', None, 300), ('char', 4, 1000)), dist='cosine', seed=3, max_A_samples=95):
    rng = random.Random(seed)
    moore, liv, ctrl = analysis.load_all()
    by = defaultdict(list)
    for d in ctrl:
        by[d['author']].append(d)
    samples = {a: make_samples(ds, 56) for a, ds in by.items()}
    # A candidates: >= 3 anapestic samples and >= 20 other samples; B candidates: >= 16 anapestic samples
    A_auth = [a for a, ss in samples.items() if sum(s['form_class']=='anapestic' for s in ss) >= 3 and sum(s['form_class']!='anapestic' for s in ss) >= 20]
    B_auth = [a for a, ss in samples.items() if sum(s['form_class']=='anapestic' for s in ss) >= 16 and sum(s['form_class']!='anapestic' for s in ss) >= 21]
    print('A authors:', A_auth); print('B authors:', B_auth)
    results = []
    for kind, n, k in fs_list:
        fsname = f'{kind}{n or k}'
        cache = {}
        def C(s):
            key = id(s)
            if key not in cache: cache[key] = counts_for(s, kind, n)
            return cache[key]
        for A in A_auth:
            sa = list(samples[A]); rng.shuffle(sa)
            an = [s for s in sa if s['form_class']=='anapestic']; ot = [s for s in sa if s['form_class']!='anapestic']
            sa = an[:8] + ot[:max_A_samples - 8]
            for B in B_auth:
                if B == A: continue
                sb = build_B(samples[B], rng)
                allS = sa + sb; labels = [A]*len(sa) + [B]*len(sb)
                cnts = [C(s) for s in allS]
                rec = {'anapestic': [], 'other': []}
                for i, s in enumerate(sa):
                    idx = [j for j, t in enumerate(allS) if j != i and not (t['poem_ids'] & s['poem_ids'])]
                    feats = top_features([cnts[j] for j in idx], k)
                    d = profile_attribution(cnts[i], [cnts[j] for j in idx], [labels[j] for j in idx], feats, dist=dist)
                    rec[s['form_class']].append(d[B] < d[A])   # True = misattributed to B
                r = dict(features=fsname, A=A, B=B,
                         n_anap=len(rec['anapestic']), misattributed_anap=float(np.mean(rec['anapestic'])) if rec['anapestic'] else None,
                         n_other=len(rec['other']), misattributed_other=float(np.mean(rec['other'])) if rec['other'] else None)
                results.append(r)
                print(f"{fsname:8s} A={A[:22]:22s} B={B[:22]:22s} A-anapests -> B: {r['misattributed_anap']:.2f} (n={r['n_anap']}) | A-others -> B: {r['misattributed_other']:.2f} (n={r['n_other']})", flush=True)
    json.dump(results, open(os.path.join(analysis.OUT, 'confound_sim.json'), 'w'), indent=1)
    for fsname in set(r['features'] for r in results):
        rr = [r for r in results if r['features'] == fsname]
        print(fsname, 'mean misattribution of A anapests:', round(np.mean([r['misattributed_anap'] for r in rr]), 3),
              '| of A others:', round(np.mean([r['misattributed_other'] for r in rr]), 3), '| pairs:', len(rr))

if __name__ == '__main__':
    run()
