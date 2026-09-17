#!/usr/bin/env python3
"""Chain driver for Open Library search-inside fragments (Bales 2002, IA greatchicagofire0000bale).
chains.json: {id: {text, status, note, pri, pick, f_open, b_open, hist:[...]}}
commands:
  new ID "seed text" [note] [pri] [dirs: f|b|fb]   create chain (seed = verbatim fragment text)
  show ID...  | list
  step ID [ID...] [-b]             one query for the given chains (tails, or heads with -b)
  auto ALL|ID,ID,... [-n ROUNDS] [-g GROUP]   repeat rounds (forward then backward) until nothing open
  set ID key value | append ID "text" | prepend ID "text"
"""
import sys, os, json, re, time, fcntl
W=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,W)
import olq
CF=os.path.join(W,'chains.json')
ANCHOR='"loosened them as quick as I could"'
LOCKF=os.path.join(W,'.chains.lock')
class locked:
    def __enter__(self):
        self.f=open(LOCKF,'w'); fcntl.flock(self.f,fcntl.LOCK_EX); return self
    def __exit__(self,*a):
        fcntl.flock(self.f,fcntl.LOCK_UN); self.f.close()
def load():
    return json.load(open(CF)) if os.path.exists(CF) else {}
def save(c):
    tmp=CF+'.tmp'; json.dump(c,open(tmp,'w'),indent=1,ensure_ascii=False); os.replace(tmp,CF)
MAP=str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"','—':'-','–':'-','\n':' ','\t':' ','|':'I','¬':'-'})
def norm(s): return s.translate(MAP).lower()
def clean(frag): return frag.replace('{{{','').replace('}}}','').replace('\n',' ')
STOP=set('the a an of to in and or is was it i he she they that this you did do at on for with as be by not but had have has were are what when where which who whom his her my your our their its me him them we there then than so if q a live know see saw went go time fire barn house street night out up down about get got came come said say think one any no yes sir there here how much many first before after from into over all some more very just well would could should will can from'.split())
def content_words(ph):
    ws=[re.sub(r'[^a-z0-9]','',w.lower()) for w in ph.split()]
    return [w for w in ws if w and w not in STOP and (len(w)>=4 or (w.isdigit() and len(w)>=3))]
def phrase_from(text, back=False, k=6, shift=0):
    ws=text.split()
    # drop a trailing (or leading, when back) hyphenated word-fragment such as "ei-" / "shav-"
    if not back and shift==0 and ws and re.search(r'[A-Za-z]-$',ws[-1]): shift=1
    if back and shift==0 and ws and re.match(r'^-?[a-z]{1,4}[,.;]?$',ws[0]) : shift=1
    if len(ws)<k+shift: return None
    sel = ws[-(k+shift):len(ws)-shift] if not back else ws[shift:shift+k]
    ph=' '.join(sel)
    ph=re.sub(r'["\[\]\(\)\{\}\*]','',ph)
    ph=ph.strip(' .,;:!?-—\'')
    if len(re.sub(r'[^A-Za-z0-9]','',ph))<8: return None
    return ph
def overlap_ok(a,b):
    ra=re.sub(r'[^a-z0-9]','',a)[-12:]; rb=re.sub(r'[^a-z0-9]','',b)[-12:]
    n=min(len(ra),len(rb))
    return n==0 or ra[-n:]==rb[-n:]
def find_ext(chain_text, frag, phrase, back=False):
    nf=norm(frag); nph=re.sub(r'\s+',' ',norm(phrase))
    rx=re.compile(re.escape(nph).replace(r'\ ',r'\s+'))
    ms=list(rx.finditer(nf))
    if not ms: return None
    nc=norm(chain_text)
    for m in ms:
        i,j=m.start(),m.end()
        if not back:
            pos=nc.rfind(nph)
            if pos<0: return None
            before_chain=nc[:pos]; before_frag=nf[:i]
            ov=min(len(before_chain),len(before_frag))
            ok = ov==0 or before_chain[-ov:].strip()==before_frag[-ov:].strip() or overlap_ok(before_chain,before_frag)
            tail_chain=nc[pos+len(nph):]; new=frag[j:]
            k=0
            while k<len(tail_chain) and k<len(new) and norm(new[k])==tail_chain[k]: k+=1
            if k<len(tail_chain): ok=ok and tail_chain[k:].strip()==''
            return (new[k:], ok)
        else:
            pos=nc.find(nph)
            if pos<0: return None
            after_chain=nc[pos+len(nph):]; after_frag=nf[j:]
            ov=min(len(after_chain),len(after_frag))
            ok = ov==0 or after_chain[:ov].strip()==after_frag[:ov].strip() or overlap_ok(after_chain[::-1],after_frag[::-1])
            head_chain=nc[:pos]; new=frag[:i]
            k=0
            while k<len(head_chain) and k<len(new) and norm(new[-1-k])==head_chain[-1-k]: k+=1
            if k<len(head_chain): ok=ok and head_chain[:len(head_chain)-k].strip()==''
            return (new[:len(new)-k] if k else new, ok)
    return None
def dkey(back): return 'b_open' if back else 'f_open'
def step(ids, back=False, tag='chain'):
    C=load(); qs=[]; meta=[]
    for cid in ids:
        ch=C[cid]
        if ch.get('status')!='open' or not ch.get(dkey(back), not back): continue
        sh=ch.get('shift_b' if back else 'shift_f',0)
        k=ch.get('k_b' if back else 'k_f',6)
        ph=phrase_from(ch['text'],back=back,k=k,shift=sh)
        while ph and k<9 and len(content_words(ph))<2:
            k+=1; ph=phrase_from(ch['text'],back=back,k=k,shift=sh)
        if not ph:
            print(f'  {cid}: no phrase'); continue
        qs.append('"%s"'%ph); meta.append((cid,ph))
    if not qs: return {}
    if len(qs)<3: qs.append(ANCHOR)
    q=' '.join(qs)
    frags=olq.query(q,limit=10,tag=tag,quiet=True)
    res={}
    print(f'  Q{"<" if back else ">"}: {q}  -> {len(frags)} frags')
    with locked():
        C=load()
        for cid,ph in meta:
            ch=C[cid]; cands=[]
            for f in frags:
                r=find_ext(ch['text'],clean(f),ph,back=back)
                if r: cands.append(r)
            oks=[r for r in cands if r[1]]
            if ch.get('pick')=='last': oks=oks[::-1]; cands=cands[::-1]
            got = oks[0] if oks else (cands[0] if cands else None)
            key='shift_b' if back else 'shift_f'
            if not got:
                ch['fails']=ch.get('fails',0)+1
                if not ch.get('solo') and len(meta)>1:
                    ch['solo']=True
                    print(f'  {cid}: NO MATCH [{ph}] (batched) -> solo retry')
                else:
                    ch['solo']=False; ch[key]=ch.get(key,0)+1
                    if ch['fails']>=5: ch[dkey(back)]=False; ch['fails']=0; ch[key]=0; print(f'  {cid}: closing direction {dkey(back)}')
                    else: print(f'  {cid}: NO MATCH [{ph}] fails={ch["fails"]} -> {key}={ch[key]}')
                res[cid]=0; continue
            ch['solo']=False
            new,ok=got
            if not ok:
                ch['ambig']=ch.get('ambig',0)+1
                kk='k_b' if back else 'k_f'; ch[kk]=ch.get(kk,6)+2
                if ch['ambig']>=3: ch[dkey(back)]=False; ch['ambig']=0; ch[kk]=6; print(f'  {cid}: closing direction {dkey(back)} (ambiguous)')
                else: print(f'  {cid}: CONTEXT MISMATCH [{ph}] -> {kk}={ch[kk]}; frag part: {new!r}')
                res[cid]=0; continue
            ch['fails']=0; ch[key]=0; ch['k_f']=6; ch['k_b']=6; ch['ambig']=0
            if new.strip()=='':
                ch['nonew']=ch.get('nonew',0)+1; ch[key]=ch.get(key,0)+1
                if ch['nonew']>=3: ch[dkey(back)]=False; ch['nonew']=0; print(f'  {cid}: closing direction {dkey(back)} (no new text)')
                else: print(f'  {cid}: nothing new [{ph}]')
                res[cid]=0; continue
            ch['nonew']=0
            ch['text']= new+ch['text'] if back else ch['text']+new
            ch.setdefault('hist',[]).append(('B' if back else 'F')+':'+ph)
            print(f'  {cid}: +{len(new)} {"<-" if back else "->"} {new!r}')
            res[cid]=len(new)
        save(C)
    return res
def mutate(cmd,a,C):
    if cmd=='new':
        cid,seed=a[1],a[2]; note=a[3] if len(a)>3 else ''
        pri=int(a[4]) if len(a)>4 else 5
        dirs=a[5] if len(a)>5 else 'f'
        C[cid]={'text':clean(seed),'status':'open','note':note,'hist':[],'pri':pri,'f_open':'f' in dirs,'b_open':'b' in dirs,
                'pick':'last' if cid.startswith('D_') else 'first'}
        print('created',cid)
    elif cmd=='set':
        v=a[3]; C[a[1]][a[2]]= (v=='true') if v in ('true','false') else (int(v) if v.lstrip('-').isdigit() else v)
    elif cmd=='append': C[a[1]]['text']+=clean(a[2])
    elif cmd=='prepend': C[a[1]]['text']=clean(a[2])+C[a[1]]['text']
def main():
    a=sys.argv[1:]
    if not a: print(__doc__); return
    cmd=a[0]
    if cmd in ('new','set','append','prepend'):
        with locked():
            C=load(); mutate(cmd,a,C); save(C)
        return
    C=load()
    if cmd=='show':
        for cid in a[1:]:
            ch=C[cid]; print(f'=== {cid} [{ch.get("status")}] {ch.get("note","")} len={len(ch["text"])} f_open={ch.get("f_open")} b_open={ch.get("b_open")}\n{ch["text"]}\n')
    elif cmd=='list':
        for cid,ch in sorted(C.items(), key=lambda kv:(kv[1].get('pri',5),kv[0])):
            d=('F' if ch.get('f_open') else '-')+('B' if ch.get('b_open') else '-')
            print(f'{cid:16s} {ch.get("status"):6s} p{ch.get("pri",5)} {d} len={len(ch["text"]):6d} {ch.get("note","")[:34]:34s} head={ch["text"][:30]!r} tail={ch["text"][-30:]!r}')
    elif cmd=='step':
        back='-b' in a; ids=[x for x in a[1:] if not x.startswith('-')]
        step(ids,back=back)
    elif cmd=='auto':
        n=5; G=4
        if '-n' in a: n=int(a[a.index('-n')+1])
        if '-g' in a: G=int(a[a.index('-g')+1])
        ids=None if a[1]=='ALL' else a[1].split(',')
        for r in range(n):
            C=load()
            pool=ids if ids else sorted(C.keys(), key=lambda i:(not i.startswith('D_'),C[i].get('pri',5),i))
            any_live=False
            for back in (False,True):
                live=[i for i in pool if C[i].get('status')=='open' and C[i].get(dkey(back))]
                if not live: continue
                any_live=True
                print(f'-- round {r+1} {"BACK" if back else "FWD"} ({len(live)} open)')
                solo=[i for i in live if C[i].get('solo')]; rest=[i for i in live if not C[i].get('solo')]
                for i in solo: step([i],back=back); time.sleep(1.0)
                for g in range(0,len(rest),G): step(rest[g:g+G],back=back); time.sleep(1.0)
            if not any_live: print('all done'); break
    else: print(__doc__)
if __name__=='__main__': main()
