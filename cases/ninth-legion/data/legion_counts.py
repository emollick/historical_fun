import json,subprocess,urllib.parse,csv,collections,os,time
RAW=os.path.dirname(os.path.abspath(__file__))+'/raw'
lk=json.load(open(RAW+'/edcs_indexes/lookups.json'))['d']; prov=lk['provinces']
pl={r[0]:r for r in json.load(open(RAW+'/edcs_indexes/places.json'))['d']}
S=json.load(open(RAW+'/edcs_indexes/searchable.json'))
idx={row[0]:row for row in S['d']}   # [id,g,m,ci,li,d,h]
LEGIONS=[
 ('IX Hispana','(VIIII|IX) ?/? ?Hisp'),
 ('XXII Deiotariana','XXII ?/? ?Deiot'),
 ('X Fretensis','(^|[^IVX])X ?/? ?Fret'),
 ('VI Ferrata','(^|[^IVX])VI ?/? ?Ferr'),
 ('III Cyrenaica','(^|[^IVX])III ?/? ?Cyren'),
 ('II Traiana','(^|[^IVXL])II ?/? ?Traian'),
 ('XII Fulminata','(^|[^IVX])XII ?/? ?Fulm'),
 ('XV Apollinaris','(^|[^IVX])XV ?/? ?Apol'),
 ('XVI Flavia','(^|[^IVX])XVI ?/? ?Fl(a|\\()'),
 ('XXX Ulpia Victrix','XXX ?/? ?Ulp'),
 ('I Minervia','(^|[^IVXL])I ?/? ?Minerv'),
 ('VI Victrix','(^|[^IVX])VI ?/? ?Vic'),
 ('X Gemina','(^|[^IVX])X ?/? ?Gem'),
 ('II Augusta','(^|[^IVXL])II ?/? ?Aug'),
 ('XX Valeria Victrix','(^|[^X])XX ?/? ?(Val|Vic|val|vic)'),
]
def band(d):
    if d is None or d==[]: return 'undated'
    if isinstance(d,list):
        f,t=d; f=f if f is not None else t; t=t if t is not None else f
        m=(f+t)/2
    else: m=d
    if m<70: return 'pre-70'
    if m<108: return '70-107'
    if m<=140: return '108-140'
    return 'later(141+)'
out=[]; log=[]
for name,rx in LEGIONS:
    url='https://edcs.hist.uzh.ch/api/search?'+urllib.parse.urlencode({'q':rx,'mode':'r'})
    fn=RAW+'/edcs_legion_'+name.replace(' ','_')+'.json'
    r=subprocess.run(['curl','-sS','-L','--retry','6','--retry-all-errors','--retry-delay','3','--max-time','180',url,'-o',fn,'-w','%{http_code}'],capture_output=True,text=True)
    try: ids=json.load(open(fn))
    except Exception as e: ids=None
    if not isinstance(ids,list):
        log.append((name,url,r.stdout,'ERR')); print(name,'ERR',r.stdout); continue
    log.append((name,url,r.stdout,len(ids))); print(name,len(ids),url,flush=True)
    byprov=collections.defaultdict(lambda: collections.Counter()); missing=0
    for i in ids:
        row=idx.get(int(i))
        if row is None: missing+=1; continue
        p=pl.get(row[1]); pv=prov[p[2]] if p and p[2] is not None and p[2]<len(prov) else 'unknown'
        byprov[pv][band(row[5])]+=1
    for pv,c in sorted(byprov.items(),key=lambda x:-sum(x[1].values())):
        tot=sum(c.values()); dated=tot-c['undated']
        out.append(dict(legion=name,database='EDCS',province=pv,count=tot,dated_count=dated,pre70=c['pre-70'],b70_107=c['70-107'],b108_140=c['108-140'],later141=c['later(141+)'],undated=c['undated'],notes=f'regex q={rx} (mode=r); total hits {len(ids)}; ids not in index {missing}'))
    # per-legion total row
    tot=sum(sum(c.values()) for c in byprov.values()); c=collections.Counter()
    for cc in byprov.values(): c.update(cc)
    out.append(dict(legion=name,database='EDCS',province='ALL',count=tot,dated_count=tot-c['undated'],pre70=c['pre-70'],b70_107=c['70-107'],b108_140=c['108-140'],later141=c['later(141+)'],undated=c['undated'],notes=f'regex q={rx}; date band = midpoint of EDCS date range; includes tile stamps/graffiti (categories not filtered)'))
    time.sleep(0.5)
cols=['legion','database','province','count','dated_count','pre70','b70_107','b108_140','later141','undated','notes']
with open(os.path.dirname(os.path.abspath(__file__))+'/legion_counts.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); [w.writerow(o) for o in out]
json.dump(log,open(RAW+'/edcs_legion_query_log.json','w'),indent=1)
print('done rows',len(out))
