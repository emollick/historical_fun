"""Figures for the Beale report: cipher-1 strip with the alphabetic run, the encoder's offsets, number histograms.
Inline SVG using CSS custom properties so the page theme colours them."""
import re, json, os
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(B,'results')
doi=re.sub(r'\(\d+\)','',open(f'{B}/data/primary/doi_pamphlet_as_printed.txt',encoding='utf-8').read())
words=re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",doi)
def offset(n):
    if n<=241: return 0
    if n<=466: return 1
    if n<=505: return 11
    if n<=620: return 10
    if n<=666: return 11
    return 12
def key(n, enc=True):
    if enc:
        if n==95: return 'U'
        if n==811: return 'Y'
        if n==1005: return 'X'
        i=n+offset(n)-1
    else:
        i=n-1
    return words[i][0].upper() if i<len(words) else '?'
c1=[int(x) for x in open(f'{B}/data/primary/cipher1.txt').read().split()]
c2=[int(x) for x in open(f'{B}/data/primary/cipher2.txt').read().split()]
c3=[int(x) for x in open(f'{B}/data/primary/cipher3.txt').read().split()]

# ---------- Table 1: strip of cipher 1, positions 184..210, two rows: straight count vs encoder's key
def strip():
    lo,hi=184,210   # 1-based inclusive
    n=hi-lo+1
    cw=34; left=118; top=18
    W=left+n*cw+12; H=150
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="f1t" font-family="var(--mono)" font-size="12">']
    s.append('<title id="f1t">Cipher 1, positions 184 to 210, decoded with a plain count of the Declaration and with the encoder\'s miscounted numbering</title>')
    # highlight band for 188-204 (17 letters) and lighter for 205-207
    x0=left+(188-lo)*cw; x1=left+(204-lo+1)*cw
    s.append(f'<rect x="{x0}" y="{top+62}" width="{x1-x0}" height="40" rx="3" fill="var(--accent-soft)"/>')
    x2=left+(206-lo)*cw; x3=left+(207-lo+1)*cw
    s.append(f'<rect x="{x2}" y="{top+62}" width="{x3-x2}" height="40" rx="3" fill="var(--accent-soft)" opacity="0.55"/>')
    s.append(f'<text x="{left-8}" y="{top+12}" text-anchor="end" fill="var(--ink-2)" font-size="11">position</text>')
    s.append(f'<text x="{left-8}" y="{top+36}" text-anchor="end" fill="var(--ink-2)" font-size="11">number</text>')
    s.append(f'<text x="{left-8}" y="{top+60}" text-anchor="end" fill="var(--ink-2)" font-size="11">plain count</text>')
    s.append(f'<text x="{left-8}" y="{top+88}" text-anchor="end" fill="var(--ink)" font-size="11" font-weight="700">encoder\'s key</text>')
    for k,p in enumerate(range(lo,hi+1)):
        x=left+k*cw+cw/2; num=c1[p-1]
        s.append(f'<text x="{x}" y="{top+12}" text-anchor="middle" fill="var(--ink-2)" font-size="10">{p}</text>')
        s.append(f'<text x="{x}" y="{top+36}" text-anchor="middle" fill="var(--ink)">{num}</text>')
        s.append(f'<text x="{x}" y="{top+60}" text-anchor="middle" fill="var(--ink-2)">{key(num,False)}</text>')
        a=key(num,True); w='700' if 188<=p<=207 else '400'
        s.append(f'<text x="{x}" y="{top+90}" text-anchor="middle" fill="var(--ink)" font-size="15" font-weight="{w}">{a}</text>')
    s.append(f'<text x="{x0}" y="{top+122}" fill="var(--ink-2)" font-size="11" font-family="var(--body)">Seventeen letters in alphabetical order (A to O, position 188 to 204), then H for 301 where 302 would give O, then P, P.</text>')
    s.append('</svg>')
    open(os.path.join(OUT,'table1_alphabet_strip.svg'),'w').write('\n'.join(s))

# ---------- Figure 1: offsets the encoder used, by cipher number, with the pamphlet's printed anomalies
def offsets_fig():
    W,H=760,240; L,R,T,Bm=54,64,22,52
    pw=W-L-R; ph=H-T-Bm
    xmax=1010; ymin,ymax=-1,13
    def X(n): return L+pw*n/xmax
    def Y(o): return T+ph*(ymax-o)/(ymax-ymin)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="f2t" font-family="var(--mono)" font-size="11">']
    s.append('<title id="f2t">Offset between the cipher-2 encoder\'s word numbers and a plain word count, by cipher number, with the pamphlet\'s printed numbering anomalies</title>')
    for o in (0,4,8,12):
        s.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(o)}" y2="{Y(o)}" stroke="var(--rule)" stroke-width="1"/>')
        s.append(f'<text x="{L-6}" y="{Y(o)+4}" text-anchor="end" fill="var(--ink-2)">+{o}</text>')
    for n in (0,250,500,750,1000):
        s.append(f'<text x="{X(n)}" y="{H-Bm+16}" text-anchor="middle" fill="var(--ink-2)">{n}</text>')
    s.append(f'<text x="{L+pw/2}" y="{H-8}" text-anchor="middle" fill="var(--ink-2)" font-family="var(--body)" font-size="12">cipher-2 number (word number in the encoder\'s Declaration)</text>')
    # pamphlet anomalies: printed label where the step is wrong -> vertical dashed marks
    for n,lab in ((250,'(250): 11 words'),(480,'(480) printed twice'),(510,'(510): 9 words'),(640,'(640): 11 words'),(680,'(680): 11 words')):
        s.append(f'<line x1="{X(n)}" x2="{X(n)}" y1="{T}" y2="{H-Bm}" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="3 4"/>')
    # labels for anomalies staggered
    labs=[(250,'(250)',0),(480,'(480) twice',0),(510,'(510)',14),(640,'(640)',0),(680,'(680)',14)]
    for n,lab,dy in labs:
        s.append(f'<text x="{X(n)+4}" y="{T+10+dy}" fill="var(--accent)" font-size="10">{lab}</text>')
    # encoder offsets: one dot per distinct number used in cipher 2
    seen=sorted(set(c2))
    for n in seen:
        if n in (95,811,1005): continue
        w=words[n+offset(n)-1] if n+offset(n)-1<len(words) else '?'
        s.append(f'<circle cx="{X(n)}" cy="{Y(offset(n))}" r="3.2" fill="var(--ink)" stroke="var(--paper)" stroke-width="1.5"><title>{n} = {w} (offset +{offset(n)})</title></circle>')
    # special numbers as hollow
    for n,l in ((811,'811 = y'),(1005,'1005 = x')):
        s.append(f'<circle cx="{X(n)}" cy="{Y(12)}" r="4" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>')
        s.append(f'<text x="{X(n)}" y="{Y(12)+16}" text-anchor="middle" fill="var(--ink)" font-size="10">{l}</text>')
    s.append('</svg>')
    open(os.path.join(OUT,'figure1_offsets.svg'),'w').write('\n'.join(s))

# ---------- Figure 2: value histograms of the three ciphers (shared scale, bins of 50 up to 1050, then a ">1050" bin)
def hist_fig():
    bins=list(range(0,1051,50))
    def counts(c):
        h=[0]*(len(bins)-1); over=0
        for v in c:
            if v>1050: over+=1
            else: h[min((v-1)//50,len(h)-1)]+=1
        return h,over
    data=[('Cipher 1 (520 numbers, largest 2906)',c1),('Cipher 2 (762 numbers, largest 1005)',c2),('Cipher 3 (618 numbers, largest 975)',c3)]
    W=720; rowh=120; H=rowh*3+30; L=54; R=70; T=8
    pw=W-L-R; nb=len(bins)-1; bw=pw/(nb+1)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="f3t" font-family="var(--mono)" font-size="11">']
    s.append('<title id="f3t">Histograms of the numbers in the three ciphers, bins of fifty</title>')
    ymax=max(max(counts(c)[0]) for _,c in data)
    ymax=max(ymax, max(counts(c)[1] for _,c in data))
    for r,(name,c) in enumerate(data):
        h,over=counts(c); y0=T+r*rowh; ph=rowh-34
        share=sum(1 for v in c if v<=100)/len(c)
        s.append(f'<text x="{L}" y="{y0+12}" fill="var(--ink)" font-family="var(--body)" font-size="13" font-weight="600">{name}</text>')
        s.append(f'<text x="{W-R+64}" y="{y0+12}" text-anchor="end" fill="var(--ink-2)" font-family="var(--body)" font-size="12">{share*100:.0f}% at or below 100</text>')
        base=y0+18+ph
        s.append(f'<line x1="{L}" x2="{W-R+bw+4}" y1="{base}" y2="{base}" stroke="var(--rule)"/>')
        for i,v in enumerate(h+[over]):
            x=L+i*bw+1; hh=ph*v/ymax if ymax else 0
            fill='var(--accent)' if i<nb else 'var(--ink-2)'
            lab=(f'{bins[i]+1}-{bins[i+1]}' if i<nb else 'above 1050')
            s.append(f'<rect x="{x}" y="{base-hh}" width="{bw-2}" height="{hh}" fill="{fill}" rx="1"><title>{lab}: {v} numbers</title></rect>')
        # y ticks
        s.append(f'<text x="{L-6}" y="{y0+18+ph*0+10}" text-anchor="end" fill="var(--ink-2)">{ymax}</text>')
        s.append(f'<text x="{L-6}" y="{base}" text-anchor="end" fill="var(--ink-2)">0</text>')
        if r==2:
            for i,bv in enumerate(bins):
                if bv%250==0:
                    s.append(f'<text x="{L+i*bw}" y="{base+14}" text-anchor="middle" fill="var(--ink-2)">{bv}</text>')
            s.append(f'<text x="{L+nb*bw+bw/2}" y="{base+14}" text-anchor="middle" fill="var(--ink-2)">&gt;1050</text>')
    s.append(f'<line x1="{L+21*bw}" x2="{L+21*bw}" y1="{T}" y2="{H-30}" stroke="var(--ink-2)" stroke-dasharray="2 3"/>')
    s.append('</svg>')
    open(os.path.join(OUT,'figure2_histograms.svg'),'w').write('\n'.join(s))
strip(); offsets_fig(); hist_fig()
print(os.listdir(OUT))
print('distinct c2 numbers (excluding 95/811/1005):',len(set(c2)-{95,811,1005}), 'distinct total',len(set(c2)))
