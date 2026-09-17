#!/usr/bin/env python3
"""Query Open Library search-inside API; log to query_log.tsv; save raw JSON under raw/.
usage: olq.py [-l LIMIT] [-t TAG] [-q] QUERY...   (each positional arg is a separate query)
prints Bales fragments (identifier greatchicagofire0000bale) with {{{ }}} markers kept; \n shown as ⏎
"""
import sys, json, time, os, urllib.request, urllib.parse, ssl, re, fcntl
W=os.path.dirname(os.path.abspath(__file__))
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
BALES='greatchicagofire0000bale'
LOG=os.path.join(W,'query_log.tsv'); RAW=os.path.join(W,'raw'); os.makedirs(RAW,exist_ok=True)
STATE=os.path.join(W,'.qcount')
def nextid():
    with open(STATE,'a+') as f:
        fcntl.flock(f,fcntl.LOCK_EX); f.seek(0); s=f.read().strip(); n=int(s) if s else 0; n+=1
        f.seek(0); f.truncate(); f.write(str(n)); f.flush()
    return n
def query(q, limit=20, tag='', quiet=False, extra=None):
    n=nextid(); qid='q%04d'%n
    params={'q':q,'limit':str(limit)}
    if extra: params.update(extra)
    url='https://openlibrary.org/search/inside.json?'+urllib.parse.urlencode(params)
    status=0; body=b''; err=''
    for attempt in range(6):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json'})
            with urllib.request.urlopen(req,timeout=120) as r:
                status=r.status; body=r.read()
            break
        except urllib.error.HTTPError as e:
            status=e.code; body=e.read(); err=str(e)
            if e.code in (429,500,502,503,504):
                wait=10*(attempt+1); sys.stderr.write(f'{qid} HTTP {e.code}; backoff {wait}s\n'); time.sleep(wait); continue
            break
        except Exception as e:
            err=str(e); sys.stderr.write(f'{qid} error {e}; retry\n'); time.sleep(5*(attempt+1))
    fn=os.path.join(RAW,qid+'.json')
    with open(fn,'wb') as f: f.write(body)
    frags=[]; total=-1; nhits=0; bales_score=''
    try:
        d=json.loads(body); total=d['hits']['total']; hits=d['hits']['hits']; nhits=len(hits)
        for h in hits:
            if h['fields']['identifier'][0]==BALES:
                frags=h['highlight']['text']; bales_score=h.get('_score')
    except Exception as e:
        err=(err+' parse:'+str(e)).strip()
    ts=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    with open(LOG,'a') as f:
        f.write('\t'.join([ts,qid,tag,q.replace('\t',' '),str(limit),str(status),str(total),str(nhits),str(len(frags)),err.replace('\t',' ')])+'\n')
    if not quiet:
        print(f'## {qid} [{tag}] q={q!r} status={status} total={total} hits={nhits} bales_frags={len(frags)} score={bales_score} {err}')
        for t in frags: print('   >', t.replace('\n','⏎'))
    return frags
if __name__=='__main__':
    args=sys.argv[1:]; limit=20; tag=''; quiet=False; qs=[]
    i=0
    while i<len(args):
        a=args[i]
        if a=='-l': limit=int(args[i+1]); i+=2; continue
        if a=='-t': tag=args[i+1]; i+=2; continue
        if a=='-q': quiet=True; i+=1; continue
        qs.append(a); i+=1
    for k,q in enumerate(qs):
        query(q,limit=limit,tag=tag,quiet=quiet)
        if k<len(qs)-1: time.sleep(1.0)
