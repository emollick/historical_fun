import json, html, os
_CASE=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT=os.path.join(_CASE, "figures", "")
SRC=os.path.join(_CASE, "")
FONT="Helvetica Neue, Helvetica, Arial, Liberation Sans, sans-serif"
SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#8a8984"; RULE="#e6e5e1"
BLUE="#2a78d6"; BLUE_L="#86b6ef"; ORANGE="#eb6834"; AQUA="#1baf7a"; VIOLET="#4a3aa7"
HALO=f'paint-order="stroke" stroke="{SURF}" stroke-width="3" stroke-linejoin="round"'
def esc(t): return html.escape(t, quote=True)

# ---------------- Figure 1: shares under each starting assumption ----------------
r=json.load(open(SRC+"data/evidence_model_results_one.json"))
runs=r["runs"]; pri=r["priors"]
assert pri["even_S_H"]=={"S":0.475,"H":0.475,"A":0.05} and pri["murder_leaning"]=={"S":0.2,"H":0.75,"A":0.05} and pri["suicide_leaning"]=={"S":0.7,"H":0.25,"A":0.05}
assert abs(pri["flat"]["S"]-1/3)<0.001
groups=[("even_S_H","Even start: 47.5 / 47.5 / 5"),("flat","Flat start: a third each"),
        ("murder_leaning","Murder-leaning start: 20 / 75 / 5"),("suicide_leaning","Suicide-leaning start: 70 / 25 / 5")]
settings=[("base","no discount"),("sceptic_half","every item halved"),("sceptic_quarter","every item quartered")]
W,H=900,640; L,R,T=300,860,100
GB=H-64
rowh=30; gaph=22
def x(v): return L+(R-L)*v/100.0
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="{SURF}"/>',
     f'<text x="24" y="34" font-size="17" font-weight="600" fill="{INK}">Share for self-infliction under each starting assumption</text>',
     f'<text x="24" y="56" fill="{INK2}">Dot: the middle value of 100,000 random runs. Line: the central 90 percent of those runs.</text>',
     f'<text x="24" y="74" fill="{INK2}">Start: the shares assumed for self-inflicted / homicide / accident before any evidence is weighed.</text>']
for v in (0,25,50,75,100):
    svg.append(f'<line x1="{x(v):.1f}" y1="{T+4}" x2="{x(v):.1f}" y2="{GB}" stroke="{RULE}" stroke-width="1"/>')
    svg.append(f'<text x="{x(v):.1f}" y="{GB+18}" text-anchor="middle" fill="{INK2}">{v}%</text>')
svg.append(f'<line x1="{x(85):.1f}" y1="{T+4}" x2="{x(85):.1f}" y2="{GB}" stroke="{INK2}" stroke-width="1" stroke-dasharray="4 4"/>')
svg.append(f'<text x="{x(85)-6:.1f}" y="{T+2}" text-anchor="end" fill="{INK2}" font-size="12">headline judgment, about 85</text>')
y=T+16
rows=[]
for gk,gl in groups:
    svg.append(f'<text x="24" y="{y+4}" font-weight="600" fill="{INK}">{esc(gl)}</text>')
    y+=gaph
    for sk,sl in settings:
        S=runs[f"{gk}/{sk}"]["S"]; med,lo,hi=[v*100 for v in S]
        svg.append(f'<text x="{L-12}" y="{y+4}" text-anchor="end" fill="{INK2}">{esc(sl)}</text>')
        svg.append(f'<line x1="{x(lo):.1f}" y1="{y}" x2="{x(hi):.1f}" y2="{y}" stroke="{BLUE_L}" stroke-width="3" stroke-linecap="round"/>')
        svg.append(f'<circle cx="{x(med):.1f}" cy="{y}" r="6" fill="{BLUE}" stroke="{SURF}" stroke-width="2"/>')
        svg.append(f'<text x="{x(med)+11:.1f}" y="{y+4}" fill="{INK}" font-size="12" font-variant-numeric="tabular-nums" {HALO}>{med:.0f}</text>')
        rows.append((gl,sl,med,lo,hi))
        y+=rowh
    y+=8
assert y-rowh <= GB-10, (y,GB)
svg.append(f'<text x="24" y="{H-26}" fill="{MUTED}" font-size="11.5">Items that rest on one underlying fact count once per run. Every figure depends on the sixteen scored items, their ranges and the start chosen.</text>')
svg.append(f'<text x="24" y="{H-10}" fill="{MUTED}" font-size="11.5">Data: data/evidence_model_results_one.json.</text>')
svg.append('</svg>')
open(OUT+"fig2_shares_by_prior.svg","w",encoding="utf-8").write("\n".join(svg))
print("fig1 rows:",[(g[:6],s[:8],round(m),round(lo),round(hi)) for g,s,m,lo,hi in rows])

# ---------------- Figure 2: the night as each source tells it ----------------
W=1100; L,R=310,960; T0=130
def hx(hh): return L+(R-L)*(hh-17.0)/15.0
def t(hm):
    h,m=map(int,hm.split(":")); v=h+m/60.0
    return v if v>=17 else v+24
sunset,twi_end,moonset,twi_start,sunrise=t("17:31"),t("17:57"),t("18:35"),t("05:37"),t("06:02")
ROWH=76
rows=[
 ("James Neelly, letter of 18 October 1809","(with John Brahan's letter of the same day)",
  [("arrival",sunset,None,True,"about sunset","start",12),
   ("shots",t("03:00"),None,True,"about three o'clock","end",-12),
   ("death",sunrise,None,True,"lived until sunrise (Brahan)","start",12),
   ("servants",t("03:15"),None,False,"woken by her; ‘came in but too late’","start",12)]),
 ("Democratic Clarion, 20 October 1809","Nashville newspaper; the first printed report",
  [("shots",t("22:00"),(t("20:00"),t("24:00")),False,"some time before midnight","middle",0),
   ("death",t("07:00"),None,True,"about seven o'clock","start",12),
   ("servants",twi_start,None,True,"came at daylight","end",-12)]),
 ("Alexander Wilson, letter of 18 May 1810","Mrs Grinder's fullest telling, seven months on",
  [("arrival",sunset,None,True,"about sunset","start",12),
   ("shots",t("00:30"),(t("20:30"),t("04:30")),False,"after ‘several hours’ of pacing; no hour given","middle",0),
   ("death",sunrise,None,True,"as the sun rose above the trees","start",12),
   ("servants",twi_start,None,True,"sent for as day broke","end",-12)]),
 ("Gilbert Russell, statement of 26 November 1811","two years on; authenticity disputed",
  [("shots",t("00:30"),(t("20:00"),t("05:00")),False,"some time in the night","middle",0)]),
]
GB=T0+22+ROWH*len(rows)-20
H=GB+156
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="{SURF}"/>',
     f'<text x="24" y="34" font-size="17" font-weight="600" fill="{INK}">The night of 10 to 11 October 1809 as each source tells it</text>',
     f'<text x="24" y="56" fill="{INK2}">Local mean time at Grinder&#x27;s Stand. Each row is one account, dated when it was written.</text>',
     f'<text x="24" y="74" fill="{INK2}">A filled mark is a time the source states. A hollow mark is a time given only in words; a dashed line shows the stretch the words allow.</text>']
sky_y=T0-30
for a,b,col in ((17,sunset,"#dcdad3"),(sunset,twi_end,"#a8a69e"),(twi_end,twi_start,"#5e5c57"),(twi_start,sunrise,"#a8a69e"),(sunrise,32,"#dcdad3")):
    svg.append(f'<rect x="{hx(a):.1f}" y="{sky_y}" width="{hx(b)-hx(a):.1f}" height="10" fill="{col}"/>')
for hh in (sunset,moonset,twi_start,sunrise):
    svg.append(f'<line x1="{hx(hh):.1f}" y1="{sky_y-4}" x2="{hx(hh):.1f}" y2="{sky_y+14}" stroke="{INK2}" stroke-width="1"/>')
dx=4
svg.append(f'<text x="{hx(sunset)-dx:.1f}" y="{sky_y-8}" text-anchor="end" fill="{INK2}" font-size="11.5">sunset 17:31</text>')
svg.append(f'<text x="{hx(moonset)+dx:.1f}" y="{sky_y-8}" fill="{INK2}" font-size="11.5">moonset 18:35 (4% lit): no moon after this</text>')
svg.append(f'<text x="{hx(twi_start)-dx:.1f}" y="{sky_y-8}" text-anchor="end" fill="{INK2}" font-size="11.5">first light 05:37</text>')
svg.append(f'<text x="{hx(sunrise)+dx:.1f}" y="{sky_y-8}" fill="{INK2}" font-size="11.5">sunrise 06:02</text>')
for hh in range(17,33):
    xx=hx(hh)
    svg.append(f'<line x1="{xx:.1f}" y1="{T0}" x2="{xx:.1f}" y2="{GB}" stroke="{RULE}" stroke-width="1"/>')
    if hh%2==0 or hh==17 or hh==32:
        lab="midnight" if hh==24 else (f"{hh}:00" if hh<24 else f"{hh-24}:00")
        svg.append(f'<text x="{xx:.1f}" y="{GB+18}" text-anchor="middle" fill="{INK2}" font-size="12">{lab}</text>')
svg.append(f'<text x="{hx(20.5):.1f}" y="{GB+36}" text-anchor="middle" fill="{MUTED}" font-size="11.5">evening of 10 October</text>')
svg.append(f'<text x="{hx(28.5):.1f}" y="{GB+36}" text-anchor="middle" fill="{MUTED}" font-size="11.5">morning of 11 October</text>')
COL={"arrival":BLUE,"shots":ORANGE,"servants":AQUA,"death":VIOLET}
def mark(kind,xx,yy,filled=True):
    col=COL[kind]
    f=col if filled else SURF; s=SURF if filled else col
    sw=2 if filled else 2.2
    if kind=="arrival": return f'<circle cx="{xx:.1f}" cy="{yy}" r="6.5" fill="{f}" stroke="{s}" stroke-width="{sw}"/>'
    if kind=="shots":   return f'<polygon points="{xx:.1f},{yy-8} {xx+7.5:.1f},{yy+6} {xx-7.5:.1f},{yy+6}" fill="{f}" stroke="{s}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if kind=="servants":return f'<polygon points="{xx:.1f},{yy-8} {xx+8:.1f},{yy} {xx:.1f},{yy+8} {xx-8:.1f},{yy}" fill="{f}" stroke="{s}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return f'<rect x="{xx-6.5:.1f}" y="{yy-6.5}" width="13" height="13" rx="2" fill="{f}" stroke="{s}" stroke-width="{sw}"/>'
y=T0+22
for name,sub,marks in rows:
    svg.append(f'<text x="24" y="{y-2}" font-weight="600" fill="{INK}" font-size="12.5">{esc(name)}</text>')
    svg.append(f'<text x="24" y="{y+14}" fill="{INK2}" font-size="11.5">{esc(sub)}</text>')
    svg.append(f'<line x1="{L}" y1="{y+6}" x2="{R}" y2="{y+6}" stroke="{RULE}" stroke-width="1"/>')
    for kind,xx,span,filled,label,anc,off in marks:
        lane = y+34 if kind=="servants" else y+6
        if span:
            svg.append(f'<line x1="{hx(span[0]):.1f}" y1="{lane}" x2="{hx(span[1]):.1f}" y2="{lane}" stroke="{COL[kind]}" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round"/>')
        svg.append(mark(kind,hx(xx),lane,filled))
        ly = lane-10 if span else lane+4
        svg.append(f'<text x="{hx(xx)+off:.1f}" y="{ly}" text-anchor="{anc}" fill="{INK}" font-size="11.5" {HALO}>{esc(label)}</text>')
    y+=ROWH
ly=GB+64; lx=24
for kind,lab in (("arrival","arrival at the stand"),("shots","the two shots"),("servants","the servants reach him"),("death","death")):
    svg.append(mark(kind,lx+8,ly,True)); svg.append(f'<text x="{lx+22}" y="{ly+4}" fill="{INK2}" font-size="12">{lab}</text>')
    lx+=175
svg.append(f'<line x1="{lx-6}" y1="{ly}" x2="{lx+22}" y2="{ly}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 5"/>')
svg.append(mark("shots",lx+8,ly,False))
svg.append(f'<text x="{lx+30}" y="{ly+4}" fill="{INK2}" font-size="12">time given only in words</text>')
foot=["Filled marks are times the source states by the clock or by the sun; sunset, daylight and sunrise sit at their computed times.",
      "Hollow marks sit where the words put them: ‘before midnight’ is drawn as 20:00 to midnight, ‘in the night’ as 20:00 to 05:00,",
      "‘several hours’ of pacing as 20:30 to 04:30, and the servants Neelly says she woke as just after the shots.",
      "Sources: section 2 and the table in section 4 of this report; sun and moon times from data/astronomy_1809.txt."]
for i,line in enumerate(foot):
    svg.append(f'<text x="24" y="{GB+92+16*i}" fill="{MUTED}" font-size="11.5">{esc(line)}</text>')
svg.append('</svg>')
open(OUT+"fig1_night_by_source.svg","w",encoding="utf-8").write("\n".join(svg))
print("fig2 written", W, H)
