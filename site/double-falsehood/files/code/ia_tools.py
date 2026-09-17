#!/usr/bin/env python3
"""Helpers for archive.org: find leaf numbers containing a phrase, and fetch page images.
usage: ia_tools.py search <identifier> <query>
       ia_tools.py page <identifier> <leaf> [outdir]
"""
import sys, json, urllib.request, urllib.parse, os, re
UA={'User-Agent':'Mozilla/5.0 research'}
def get(url):
    req=urllib.request.Request(url,headers=UA)
    return urllib.request.urlopen(req,timeout=120).read()
def meta(idn):
    return json.loads(get(f'https://archive.org/metadata/{idn}'))
def search(idn,q):
    m=meta(idn)
    server=m['server']; d=m['dir']
    # find the djvu.xml or the abbyy file name for doc param
    files=[f['name'] for f in m['files']]
    doc=None
    for f in files:
        if f.endswith('_djvu.xml'): doc=f[:-9]
    if doc is None: doc=idn
    url=f'https://{server}/fulltext/inside.php?item_id={idn}&doc={doc}&path={d}&q={urllib.parse.quote(q)}'
    j=json.loads(get(url))
    res=[]
    for mt in j.get('matches',[]):
        pages=sorted({p['page'] for p in mt.get('par',[])})
        res.append((pages, re.sub(r'\s+',' ',mt.get('text',''))[:300]))
    return res
def page(idn,leaf,outdir):
    os.makedirs(outdir,exist_ok=True)
    url=f'https://archive.org/download/{idn}/page/n{leaf}.jpg'
    data=get(url)
    fn=os.path.join(outdir,f'{idn}_n{leaf}.jpg')
    open(fn,'wb').write(data)
    return fn,len(data)
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='search':
        for pages,text in search(sys.argv[2],sys.argv[3]):
            print(pages,'|',text)
    elif cmd=='page':
        out=sys.argv[4] if len(sys.argv)>4 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','sources','documents','images')
        print(page(sys.argv[2],int(sys.argv[3]),out))
