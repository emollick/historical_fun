import json,sys,re,urllib.parse,subprocess,os
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def query(keys, years="", yearsTo="", start=0, order="asc"):
    url=("https://archivio.ilpiccolo.it/aviator/_resources/php/get_searchSolr.php?start_rows=%d&order_by=%s&search_keys=%s&newspapers=&years=%s&months=&days=&yearsTo=%s&monthsTo=&daysTo="
         %(start,order,urllib.parse.quote(keys),years,yearsTo))
    out=subprocess.run(["curl","-sSL","--max-time","120","-A",UA,url],capture_output=True).stdout
    return json.loads(out.decode('utf-8','ignore'))
def show(keys, years="", yearsTo="", maxpages=6, ctx=250, save=False, pattern=None):
    pat=re.compile(pattern or keys.replace('"','').replace('*',''), re.I)
    start=0; total=None; n=0
    while True:
        d=query(keys,years,yearsTo,start)
        resp=d['response']; total=resp['numFound']
        if start==0: print(f"### query={keys!r} years={years}-{yearsTo} numFound={total}")
        for doc in resp['docs']:
            n+=1
            txt=max((s for s in doc.get("search_case_insensitive",[]) if isinstance(s,str)), key=len, default="")
            meta={k:doc.get(k) for k in ('newspaper','issue','page','description','fascicolo','edition','id')}
            print("--", meta)
            flat=re.sub(r'\s+',' ',txt)
            hits=[m.start() for m in pat.finditer(flat)]
            for h in hits[:4]:
                print("   >", flat[max(0,h-ctx):h+ctx])
            if save:
                fn=f"ilpiccolo_ocr_{doc.get('newspaper')}_{doc.get('issue')}_p{doc.get('page')}.txt"
                open(fn,'w').write(txt)
        start+=9
        if start>=total or start>=9*maxpages: break
    print(f"### done: {n} docs shown of {total}\n")
if __name__=="__main__":
    args=sys.argv[1:]
    keys=args[0]; years=args[1] if len(args)>1 else ""; yearsTo=args[2] if len(args)>2 else ""
    save=('--save' in args); pattern=None
    for a in args:
        if a.startswith('--pat='): pattern=a[6:]
    show(keys,years,yearsTo,save=save,pattern=pattern)
