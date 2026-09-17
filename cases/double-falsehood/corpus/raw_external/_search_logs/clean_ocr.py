#!/usr/bin/env python3
"""Conservative cleaner for Internet Archive djvu.txt OCR of 18th-century printed books.
Usage: clean_ocr.py RAW OUT [--start REGEX] [--end REGEX] [--runhead REGEX ...] [--no-longs]
Writes OUT (cleaned UTF-8 text) and OUT + '.cleanstats.json'.
"""
import re, sys, json, unicodedata, argparse, collections
from wordfreq import zipf_frequency as Z

ap = argparse.ArgumentParser()
ap.add_argument('raw'); ap.add_argument('out')
ap.add_argument('--start', default=None, help='regex: cleaning starts at first line matching (inclusive)')
ap.add_argument('--end', default=None, help='regex: cleaning stops at first line matching after start (exclusive)')
ap.add_argument('--runhead', action='append', default=[], help='regex for running heads to drop (case-insensitive)')
ap.add_argument('--no-longs', action='store_true')
ap.add_argument('--keep-start', action='store_true', help='do not auto-trim leading noise')
a = ap.parse_args()

# ---- long-s (f -> s) correction --------------------------------------------
OVERRIDES = {  # ambiguous forms that are almost always long-s readings in these texts
 'fo':'so','fhe':'she','fir':'sir','fad':'sad','fee':'see','fun':'sun','fave':'save','fin':'sin','fend':'send',
 'flay':'slay','fhou':'shou','fhould':'should','fhall':'shall','fuch':'such','fome':'some','fince':'since',
 'fay':'say','fays':'says','faid':'said','fide':'side','fon':'son','fea':'sea','fold':'sold','fell':'sell',
 'fenfe':'sense','fenfes':'senses','fex':'sex','fate':'sate','fpeak':'speak','fpeaks':'speaks',
 'fear':'fear','feaft':'feast','fecret':'secret','fecrets':'secrets','feen':'seen','feem':'seem','feems':'seems',
 'feek':'seek','felf':'self','fent':'sent','fet':'set','fets':'sets','fhew':'shew','fhews':'shews','fhow':'show',
 'fhort':'short','fhot':'shot','fhut':'shut','fhun':'shun','fhare':'share','fharp':'sharp','fhame':'shame',
 'fhape':'shape','fhade':'shade','fhine':'shine','fhip':'ship','fhock':'shock','fhore':'shore','fhook':'shook',
 'fkill':'skill','fky':'sky','flave':'slave','flaves':'slaves','fleep':'sleep','flept':'slept','flow':'slow',
 'fmile':'smile','fmiles':'smiles','fnow':'snow','foft':'soft','fold':'sold','fole':'sole','folemn':'solemn',
 'fon':'son','fons':'sons','fong':'song','fongs':'songs','foon':'soon',
 'fouls':'souls','fource':'source','fpare':'spare','fpeed':'speed','fpend':'spend','fpirit':'spirit',
 'fpite':'spite','fport':'sport','fpot':'spot','fpread':'spread','fpring':'spring','ftaff':'staff','ftage':'stage',
 'ftand':'stand','ftar':'star','ftars':'stars','ftate':'state','ftay':'stay','ftep':'step','ftill':'still',
 'ftir':'stir','ftone':'stone','ftood':'stood','ftop':'stop','ftore':'store','ftorm':'storm','ftory':'story',
 'ftrong':'strong','fuffer':'suffer','fum':'sum','fure':'sure','fweet':'sweet','fwear':'swear',
 'fword':'sword','fworn':'sworn','fit':'sit','fat':'sat','fix':'six','fail':'sail','fails':'sails','feat':'seat',
 'fever':'sever','fine':'fine','fire':'fire','flip':'slip','flight':'slight','flew':'slew',
}
# words that must never be changed even though an s-variant is more frequent
PROTECT = {'fine','fire','fear','fall','falls','fell','fold','feel','fill','full','far','for','from','few','fed','feed',
           'fame','fat','fit','fix','fail','feat','fever','flew','flight','flip','fun','fee','fin','fend','fold','fell',
           'fore','fort','sole','fate','sate','fax','fig','fan','fang','fake','fake','fame'}
# remove PROTECT words from OVERRIDES except the deliberately chosen ambiguous ones
DELIBERATE = {'fo','fhe','fir','fad','fee','fun','fave','fin','fend','flay','fide','fon','fea','fold','fell','fame',
              'fate','feat','fever','flew','flight','flip','fit','fat','fix','fail','fails','fore','fort'}
for k in list(OVERRIDES):
    if k in PROTECT and k not in DELIBERATE: del OVERRIDES[k]
# Deliberate ambiguous mappings kept ONLY for the strongly-skewed cases; drop the rest so they stay unchanged.
for k in ['fold','fell','fame','fate','feat','fever','flew','flight','flip','fit','fat','fix','fail','fails','fore','fort','fine','fire','fear']:
    OVERRIDES.pop(k, None)

WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
stats = collections.Counter()
seen_repl = collections.Counter()

def candidates(w):
    idx=[i for i,c in enumerate(w) if c=='f']
    if not idx: return []
    out=set()
    if len(idx)<=4:
        for m in range(1, 1<<len(idx)):
            cs=list(w)
            for b,i in enumerate(idx):
                if m>>b & 1: cs[i]='s'
            out.add(''.join(cs))
    else:
        out.add(w.replace('f','s'))
    return list(out)

def fix_word(w):
    # w may contain apostrophes; handle segments
    if a.no_longs: return w
    if 'f' not in w: return w
    if w.isupper(): return w
    low = w.lower()
    if low in OVERRIDES:
        r = OVERRIDES[low]; stats['override']+=1; seen_repl[low+'>'+r]+=1
        return r.capitalize() if w[0].isupper() else r
    core = low.replace('’',"'")
    if "'" in core:
        parts = core.split("'")
        newparts=[]
        changed=False
        for p in parts:
            q = fix_word(p) if p else p
            if q!=p: changed=True
            newparts.append(q)
        if changed:
            r="'".join(newparts); stats['auto']+=1
            return r.capitalize() if w[0].isupper() else r
        return w
    if low in PROTECT: return w
    zo = Z(low,'en')
    if zo >= 3.0: return w
    best=None; bz=-1
    for c in candidates(low):
        zc=Z(c,'en')
        if zc>bz: best,bz=c,zc
    if best and bz>=3.0 and bz>=zo+1.0:
        stats['auto']+=1; seen_repl[low+'>'+best]+=1
        return best.capitalize() if w[0].isupper() else best
    return w

def fix_line(l):
    return WORD.sub(lambda m: fix_word(m.group(0)), l)

# ---- read & structure --------------------------------------------------------
t = open(a.raw, encoding='utf-8', errors='replace').read()
t = t.replace('\r','')
t = unicodedata.normalize('NFC', t)
t = t.replace('ſ','s').replace('­','')
lines = [l.rstrip() for l in t.split('\n')]

# region selection
s_idx, e_idx = 0, len(lines)
if a.start:
    rs=re.compile(a.start)
    for i,l in enumerate(lines):
        if rs.search(l): s_idx=i; break
    else:
        print("WARNING: start regex not found", file=sys.stderr)
if a.end:
    rex=re.compile(a.end)
    for i in range(s_idx+1, len(lines)):
        if rex.search(lines[i]): e_idx=i; break
    else:
        print("WARNING: end regex not found", file=sys.stderr)
lines = lines[s_idx:e_idx]

def letters(l): return sum(1 for c in l if c.isalpha())
def linescore(l):
    toks=[w.lower() for w in WORD.findall(l) if len(w)>1]
    if len(toks)<3: return None
    return sum(1 for w in toks if Z(w,'en')>=3.0 or Z(w.replace('f','s'),'en')>=3.5)/len(toks)

# auto-trim leading/trailing noise (microfilm targets, library plates)
if not a.keep_start and not a.start:
    first=0
    for i,l in enumerate(lines):
        sc=linescore(l)
        if letters(l)>=20 and sc is not None and sc>=0.6:
            first=i; break
    # back up to include a possible title page block just before (up to 12 lines with letters)
    j=first
    back=0
    while j>0 and back<14:
        k=j-1
        while k>=0 and lines[k].strip()=='': k-=1
        if k<0: break
        sc=linescore(lines[k])
        ok = letters(lines[k])>=4 and (sc is None or sc>=0.5) and not re.search(r'[|\\/#{}<>~^]', lines[k])
        if not ok: break
        j=k; back+=1
    lines=lines[j:]
    last=len(lines)
    for i in range(len(lines)-1,-1,-1):
        sc=linescore(lines[i])
        if letters(lines[i])>=20 and sc is not None and sc>=0.6:
            last=i+1; break
    lines=lines[:last+3]

# boilerplate
BOILER = re.compile(r'Digitized by the Internet Archive|in \d{4} with funding from|archive\.org/details|LYRASIS|Sloan Foundation', re.I)
lines=[l for l in lines if not BOILER.search(l)]

# running heads
rh=[re.compile(r, re.I) for r in a.runhead]
norm=lambda l: re.sub(r'[^a-z]','',l.lower())
counts=collections.Counter(norm(l) for l in lines if 0<len(l)<=45)
out=[]
PAGENUM=re.compile(r'^\s*[\[\(\|]?\s*\d{1,3}\s*[\]\)\|]?\s*$')
SIG=re.compile(r'^\s*[A-Z]{1,2}\s?[1-4]?\s*$')
for l in lines:
    if PAGENUM.match(l): stats['pagenum']+=1; continue
    if SIG.match(l): stats['sig']+=1; continue
    if any(r.search(l) for r in rh) and counts[norm(l)]>=2: stats['runhead']+=1; continue
    L=letters(l); n=len(l.strip())
    if n==0: out.append(''); continue
    if L<2: stats['noise']+=1; continue
    if L<=3 and n<=6 and not re.match(r'^[A-Z][a-z]{1,3}\.$', l.strip()): stats['noise']+=1; continue
    if n<15 and L/max(1,len(re.sub(r'\s','',l)))<0.5: stats['noise']+=1; continue
    out.append(l)

# join hyphenated line breaks
joined=[]
i=0
while i<len(out):
    l=out[i]
    if l.endswith('-') and i+1<len(out):
        # find next non-empty line
        k=i+1
        while k<len(out) and out[k]=='' : k+=1
        if k<len(out) and out[k] and out[k][0].islower() and re.search(r'[A-Za-z]{2,}-$', l):
            nxt=out[k]
            m=re.match(r'(\S+)(.*)', nxt)
            l=l[:-1]+m.group(1)
            out[k]=m.group(2).lstrip()
            stats['hyphen_join']+=1
    joined.append(l); i+=1
out=joined
# collapse blank lines
res=[]
for l in out:
    if l=='' and res and res[-1]=='': continue
    res.append(l)
# strip stray leading OCR punctuation like "| " or "* " at line start
res=[re.sub(r'^[\|\*\'"“”‘’\.,:;·•\-—_=\s]+(?=[A-Za-z])','',l) if not l.startswith('—') else l for l in res]
# collapse internal runs of spaces (ABBYY output double-spaces words)
res=[re.sub(r'[ \t]{2,}',' ',l) for l in res]
# long-s correction
res=[fix_line(l) for l in res]
txt='\n'.join(res).strip()+'\n'
open(a.out,'w',encoding='utf-8').write(txt)
words=len(WORD.findall(txt))
stats['words_out']=words; stats['lines_out']=len(res)
json.dump({'stats':dict(stats),'top_replacements':seen_repl.most_common(60),'start':a.start,'end':a.end}, open(a.out+'.cleanstats.json','w'), indent=1)
print(f"{a.out}: words={words} lines={len(res)} auto={stats['auto']} override={stats['override']} noise={stats['noise']} runhead={stats['runhead']} pagenum={stats['pagenum']}")
