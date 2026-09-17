import json, sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results','other')
def bands(w):
    return '50-99' if w<100 else '100-199' if w<200 else '200-400'
def summarize_clf(path):
    r=json.load(open(path)); classes=r['classes']
    li=classes.index('lincoln'); hi=classes.index('hay')
    print('==',os.path.basename(path), 'classes', classes)
    rows={}
    for v in r['val']:
        b=bands(v['words']); t=v['truth']; p=v['probs']
        pred=classes[int(np.argmax(p))]
        rows.setdefault((b,t),[]).append((pred==t, p[hi]))
    for k in sorted(rows):
        acc=np.mean([a for a,_ in rows[k]]); n=len(rows[k]); ph=np.mean([q for _,q in rows[k]])
        print(f'  {k[0]:8s} {k[1]:8s} n={n:4d} acc={acc:.3f} mean P(hay)={ph:.2f}')
    # calibration: among val docs with P(hay) in bins, fraction truly hay (lincoln/hay only)
    vals=[v for v in r['val'] if v['truth'] in ('lincoln','hay')]
    ph=np.array([v['probs'][hi] for v in vals]); truth=np.array([v['truth']=='hay' for v in vals])
    for lo,hi_ in [(0,.1),(.1,.3),(.3,.5),(.5,.7),(.7,.9),(.9,1.01)]:
        m=(ph>=lo)&(ph<hi_)
        if m.sum(): print(f'  P(hay) in [{lo:.1f},{hi_:.1f}): n={m.sum():4d} actually hay={truth[m].mean():.2f}')
    print('  specials:')
    for k,v in r['specials'].items():
        print(f'    {k:22s} truth={str(v["truth"]):16s} P(lincoln)={v["probs"].get("lincoln",0):.3f} P(hay)={v["probs"].get("hay",0):.3f}', {c:round(p,3) for c,p in v['probs'].items() if c not in ('lincoln','hay')})
    for name,items in r['extra'].items():
        if not items: continue
        ph=[it['probs'].get('hay',0) for it in items]
        print(f'  extra {name}: n={len(items)} mean P(hay)={np.mean(ph):.2f} share called hay={np.mean([p>0.5 for p in ph]):.2f}')
def summarize_delta(path):
    r=json.load(open(path)); print('==',os.path.basename(path))
    for metric in ('burrows','cosine'):
        rows={}
        for v in r['val']:
            s=v['scores']; b=bands(v['words']); t=v['truth']
            pred=min(s,key=lambda a:s[a][metric])
            rows.setdefault((b,t),[]).append(pred==t)
        for k in sorted(rows): print(f'  {metric:8s} {k[0]:8s} {k[1]:8s} n={len(rows[k]):4d} acc={np.mean(rows[k]):.3f}')
        print('  specials:')
        for k,v in r['specials'].items():
            s=v['scores']; print(f'    {metric} {k:22s} truth={str(v["truth"]):16s}', {a:round(s[a][metric],3) for a in s})
for f in sorted(os.listdir(OUT)):
    p=os.path.join(OUT,f)
    if f.startswith('clf'): summarize_clf(p)
    elif f.startswith('delta'): summarize_delta(p)
