#!/usr/bin/env python3
"""NewspaperSG search via plain HTTP GET (default curl UA). Usage: sgsearch.py "query" [df] [dt] [nid] [maxpages]
Prints results and saves raw HTML under sg_raw/."""
import sys, re, html, subprocess, urllib.parse, os, json
q = sys.argv[1]; df = sys.argv[2] if len(sys.argv)>2 and sys.argv[2] not in ('-','') else ''
dt = sys.argv[3] if len(sys.argv)>3 and sys.argv[3] not in ('-','') else ''
nid = sys.argv[4] if len(sys.argv)>4 and sys.argv[4] not in ('-','') else ''
maxpages = int(sys.argv[5]) if len(sys.argv)>5 else 3
os.makedirs('sg_raw', exist_ok=True)
allres=[]; total=None
for page in range(1, maxpages+1):
    params=[('q',q),('size','100'),('sort','Oldest'),('page',str(page))]
    if df: params.append(('df',df))
    if dt: params.append(('dt',dt))
    if nid: params.append(('nid',nid))
    url='https://eresources.nlb.gov.sg/newspapers/search?'+urllib.parse.urlencode(params)
    out=subprocess.run(['curl','-sS','-c','sgjar.txt','-b','sgjar.txt',url],capture_output=True,text=True,timeout=120).stdout
    fn='sg_raw/'+re.sub(r'[^A-Za-z0-9]+','_',f'{q}_{df}_{dt}_{nid}_p{page}')[:120]+'.html'
    open(fn,'w').write(out)
    m=re.search(r'id="nlba_totalcount" value="(\d+)"',out)
    total=int(m.group(1)) if m else None
    blocks=re.findall(r'<a class="save-citation dropdown-item lh-sm" href="/newspapers/citations"(.*?)>\s*Save Citation',out,flags=re.S)
    res=[]
    for b in blocks:
        d=dict(re.findall(r'data-nlb-(\w+)="([^"]*)"',b))
        res.append({k:html.unescape(v) for k,v in d.items()})
    allres+=res
    if total is None or len(allres)>=total or not res: break
print(f"QUERY {q!r} df={df} dt={dt} nid={nid} -> total={total} fetched={len(allres)}")
for r in allres:
    acc='' if r.get('isaccessible')=='true' else ' [LOCKED]'
    print(f"--- {r.get('issuedate')} | {r.get('newspapertitle')} p.{r.get('pagenumber')} | {r.get('articletitle')} | {r.get('articleid')}{acc}")
    print("    "+(r.get('articleabstract') or '')[:400])
json.dump(allres, open('sg_raw/'+re.sub(r'[^A-Za-z0-9]+','_',f'{q}_{df}_{dt}_{nid}')[:120]+'.json','w'), indent=1)
