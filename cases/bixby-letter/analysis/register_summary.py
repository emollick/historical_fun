"""Register-matched validation: how n-gram tracing behaves on known pieces of the
Bixby letter's register (Lincoln's elevated letters and addresses 1861-65; Hay's 1861
eulogies and 1864 condolence), and where the Bixby letter falls among them."""
import json, sys, math
import numpy as np
from collections import Counter

def kde(x, pts, bw):
    return np.mean(np.exp(-0.5*((x-pts)/bw)**2))/(bw*math.sqrt(2*math.pi))

def margin(rec, ty):
    o = rec['ngrams'][ty]; return o['lincoln'] - o['hay']

def vote(rec, lo=4, hi=10):
    c = Counter()
    for n in range(lo, hi+1):
        d = margin(rec, f'c{n}'); c['lincoln' if d > 0 else 'hay' if d < 0 else 'tie'] += 1
    c.pop('tie', None); return c.most_common(1)[0][0] if c else 'tie'

# Hay pieces in which more than a quarter of the words are quoted from others (corpus/hay_warprose/notes.md)
QUOTED = {'hay_ellsworth_07','hay_ellsworth_09','hay_ellsworth_15','hay_ellsworth_16','hay_ellsworth_18','hay_ellsworth_19','hay_ellsworth_21',
          'hay_baker_06','hay_baker_09','hay_baker_18','hay_baker_19','hay_baker_20','hay_baker_24','hay_baker_25','hay_baker_27','hay_baker_34'}

def logistic(reg, sp, types):
    """Leave-one-source-out logistic regression on the vector of margins."""
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    ids = list(reg); X = np.array([[margin(reg[i], t) for t in types] for i in ids]); y = np.array([1 if reg[i]['truth']=='hay' else 0 for i in ids])
    src = [i.split('#')[0] if not i.startswith('hay_') else i.rsplit('_',1)[0] for i in ids]
    preds = np.zeros(len(ids))
    for s in sorted(set(src)):
        tr = np.array([k for k, g in enumerate(src) if g != s]); te = np.array([k for k, g in enumerate(src) if g == s])
        sc = StandardScaler().fit(X[tr]); m = LogisticRegression(C=0.3, max_iter=2000).fit(sc.transform(X[tr]), y[tr])
        preds[te] = m.predict_proba(sc.transform(X[te]))[:, 1]
    acc_l = np.mean(preds[y==0] < 0.5); acc_h = np.mean(preds[y==1] >= 0.5)
    sc = StandardScaler().fit(X); m = LogisticRegression(C=0.3, max_iter=2000).fit(sc.transform(X), y)
    out = {'cv_acc_lincoln': acc_l, 'cv_acc_hay': acc_h, 'n_l': int((y==0).sum()), 'n_h': int((y==1).sum()), 'p_hay': {}}
    for k, v in sp.items():
        out['p_hay'][k] = float(m.predict_proba(sc.transform(np.array([[margin(v, t) for t in types]])))[0, 1])
    out['cv_p_lincoln_pieces'] = [float(p) for p in preds[y==0]]; out['cv_p_hay_pieces'] = [float(p) for p in preds[y==1]]
    return out

def run(design, types=None, quiet=False, drop_quoted=False):
    r = json.load(open(f'results/{design}/results.json'))
    reg = r['tests']['register']; sp = r['tests']['specials']
    if drop_quoted: reg = {k: v for k, v in reg.items() if k not in QUOTED}
    types = types or ['w1','w2','w3'] + [f'c{n}' for n in range(3, 17)]
    L = [v for v in reg.values() if v['truth'] == 'lincoln']
    H = [v for v in reg.values() if v['truth'] == 'hay']
    bix = sp['bixby']
    rows = {}
    if not quiet:
        print(f"\n##### {design}{' (quotation-heavy Hay pieces dropped)' if drop_quoted else ''}: register pieces L={len(L)} H={len(H)}; sizes={r['sizes']} nseq={r['nseq']}")
        print(f"{'type':>4} {'accL':>5} {'accH':>5} | {'L mean':>7} {'L sd':>5} {'H mean':>7} {'H sd':>5} | {'bixby':>7} {'pctL':>5} {'pctH':>5} {'LR':>7}")
    for ty in types:
        dl = np.array([margin(v, ty) for v in L]); dh = np.array([margin(v, ty) for v in H])
        accl = (dl > 0).mean(); acch = (dh < 0).mean()
        d = margin(bix, ty)
        pl = (dl <= d).mean(); ph = (dh >= d).mean()
        bwl = 1.06*dl.std()*len(dl)**-0.2; bwh = 1.06*dh.std()*len(dh)**-0.2
        lr = kde(d, dl, bwl)/max(kde(d, dh, bwh), 1e-12)
        rows[ty] = dict(accL=accl, accH=acch, Lmean=dl.mean(), Lsd=dl.std(), Hmean=dh.mean(), Hsd=dh.std(), bixby=d, pctL=pl, pctH=ph, LR=lr)
        if not quiet:
            print(f"{ty:>4} {accl:5.2f} {acch:5.2f} | {dl.mean():+.3f} {dl.std():.3f} {dh.mean():+.3f} {dh.std():.3f} | {d:+.3f} {pl:5.2f} {ph:5.2f} {lr:7.2f}")
    vl = Counter(vote(v) for v in L); vh = Counter(vote(v) for v in H)
    rows['vote'] = dict(L=dict(vl), H=dict(vh), bixby=vote(bix))
    lg = logistic(reg, sp, types); rows['logistic'] = lg
    if not quiet:
        print(f"vote c4-10: Lincoln pieces -> {dict(vl)}; Hay pieces -> {dict(vh)}; Bixby -> {vote(bix)}")
        print(f"logistic on margin vector, leave-one-source-out: acc Lincoln {lg['cv_acc_lincoln']:.2f} (n={lg['n_l']}), Hay {lg['cv_acc_hay']:.2f} (n={lg['n_h']}); P(hay): " + ', '.join(f"{k}={v:.2f}" for k, v in lg['p_hay'].items()))
        # per-source accuracy for Lincoln pieces at c8 and vote
        src = Counter(); srcn = Counter()
        for k, v in reg.items():
            s = k.split('#')[0]; srcn[s] += 1
            if v['truth'] == 'lincoln' and vote(v) == 'lincoln': src[s] += 1
            if v['truth'] == 'hay' and vote(v) == 'hay': src[s] += 1
        print("per-source vote accuracy:", {s: f"{src[s]}/{srcn[s]}" for s in srcn})
    return rows

if __name__ == '__main__':
    out = {}
    for d in sys.argv[1:] or ['ownhand_register', 'grieve_register', 'ownhand_all_register']:
        try: out[d] = run(d); out[d + '_clean'] = run(d, drop_quoted=True)
        except FileNotFoundError as e: print(d, 'not ready', e)
    json.dump(out, open('results/register_summary.json', 'w'), indent=1, default=float)
