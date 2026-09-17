"""Empirical calibration of n-gram tracing margins at the Bixby letter's length.
For each design and n-gram type, take known texts of 100-200 words (leave-one-out
results for the two candidate corpora), record the margin d = overlap(Lincoln) - overlap(Hay),
and place the questioned texts on those two distributions: percentile in each, and a
Gaussian-kernel density likelihood ratio L(d|Lincoln)/L(d|Hay)."""
import json, sys, math
import numpy as np
from collections import Counter

def kde(x, pts, bw):
    return np.mean(np.exp(-0.5*((x-pts)/bw)**2))/(bw*math.sqrt(2*math.pi))

def analyse(design, lsets, hset, lo=100, hi=200, types=None, out=None):
    r=json.load(open(f'results/{design}/results.json')); t=r['tests']
    types = types or ['w1','w2','w3']+[f'c{n}' for n in range(3,17)]
    L=[v for s in lsets for v in t[s].values() if lo<=v['words']<hi]
    H=[v for v in t[hset].values() if lo<=v['words']<hi]
    rows=[]
    print(f"\n##### design={design} band={lo}-{hi} nL={len(L)} nH={len(H)}")
    print(f"{'type':>4} {'L mean':>7} {'L sd':>6} {'H mean':>7} {'H sd':>6} | " + " ".join(f"{k:>18}" for k in ['bixby','gettysburg','mccullough','ellsworth','gurney','hay_condol','boker','garrison']))
    for ty in types:
        dl=np.array([v['ngrams'][ty]['lincoln']-v['ngrams'][ty]['hay'] for v in L])
        dh=np.array([v['ngrams'][ty]['lincoln']-v['ngrams'][ty]['hay'] for v in H])
        bwl=1.06*dl.std()*len(dl)**-0.2; bwh=1.06*dh.std()*len(dh)**-0.2
        line=f"{ty:>4} {dl.mean():+.3f} {dl.std():.3f} {dh.mean():+.3f} {dh.std():.3f} | "
        for sp in ['bixby','gettysburg','mccullough','ellsworth','gurney','hay_condolence_1864','boker_1863','garrison_1865']:
            rec=t['specials'][sp]; d=rec['ngrams'][ty]['lincoln']-rec['ngrams'][ty]['hay']
            pl=(dl<=d).mean(); ph=(dh>=d).mean()
            lr=kde(d,dl,bwl)/max(kde(d,dh,bwh),1e-12)
            line+=f"{d:+.3f} {pl:.2f}/{ph:.2f} {lr:6.2g} "
            rows.append({'design':design,'type':ty,'text':sp,'d':d,'pct_L':pl,'pct_H':ph,'LR':lr})
        print(line)
    if out:
        json.dump(rows, open(out,'w'), indent=1)
    return rows

if __name__=='__main__':
    allrows=[]
    allrows+=analyse('ownhand', ['loo_lincoln_war_own'], 'loo_hay_war')
    allrows+=analyse('grieve', ['loo_lincoln_pre1860'], 'loo_hay')
    allrows+=analyse('ownhand_all', ['loo_lincoln_own'], 'loo_hay')
    json.dump(allrows, open('results/lr_rows.json','w'), indent=1)
