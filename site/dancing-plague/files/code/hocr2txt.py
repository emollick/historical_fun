import re,glob,html,sys,os
d=sys.argv[1]; out=sys.argv[2]
o=open(out,'w')
for fn in sorted(glob.glob(d+'/p*.html')):
    s=open(fn,encoding='utf-8',errors='replace').read()
    n=int(re.search(r'p(\d+)\.html',fn).group(1))
    lines=[]
    for ln in re.findall(r'<span class="ocr_line"[^>]*>(.*?)</span>\s*(?=<span class="ocr_line"|</p>)',s,flags=re.S):
        words=re.findall(r'<span class="ocrx_word"[^>]*>(.*?)</span>',ln,flags=re.S)
        words=[html.unescape(re.sub('<[^>]+>','',w)).strip() for w in words]
        lines.append(' '.join(w for w in words if w))
    if not lines:
        txt=html.unescape(re.sub('<[^>]+>',' ',s)); lines=[' '.join(txt.split())]
    o.write(f'\n\n=== PAGE {n:04d} ===\n'+'\n'.join(lines))
o.close(); print(out, os.path.getsize(out))
