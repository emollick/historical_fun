from PIL import Image, ImageDraw, ImageFont
import csv, math
S=4.0  # px per ft
X0,X1,Y0,Y1=-60,420,-175,240
W=int((X1-X0)*S); H=int((Y1-Y0)*S)
im=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(im)
def P(x,y): return (int((x-X0)*S), int((Y1-y)*S))
def rect(x0,y0,x1,y1,fill=None,outline=(0,0,0),width=1):
    d.rectangle([P(x0,y1),P(x1,y0)],fill=fill,outline=outline,width=width)
def line(x0,y0,x1,y1,fill=(0,0,0),width=1):
    d.line([P(x0,y0),P(x1,y1)],fill=fill,width=width)
def text(x,y,s,fill=(0,0,0),font=None,anchor='la'):
    d.text(P(x,y),s,fill=fill,font=font,anchor=anchor)
try:
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
except Exception:
    F=FB=FS=ImageFont.load_default()
BW=358.4; SH=100.75; AL=15.0; NH=100.0
# streets
rect(-40,-175,0,240,fill=(235,235,235),outline=None)          # Jefferson 40
rect(BW,-175,BW+40,240,fill=(235,235,235),outline=None)       # Clinton 40
rect(-60,-60,420,0,fill=(235,235,235),outline=None)           # DeKoven 60
rect(-60,SH+AL+NH,420,SH+AL+NH+60,fill=(235,235,235),outline=None)  # Taylor 60
text(-20,100,'S. JEFFERSON ST. (40 ft, 1871)',font=F,anchor='mm'); text(BW+20,100,'S. CLINTON ST. (40 ft, 1906)',font=F,anchor='mm')
text(180,-30,'DE KOVEN STREET  (60 ft)',font=FB,anchor='mm'); text(180,SH+AL+NH+30,'W. TAYLOR STREET (60 ft)',font=FB,anchor='mm')
# block outlines
rect(0,0,BW,SH+AL+NH,outline=(0,0,0),width=2)
rect(0,SH,BW,SH+AL,fill=(220,220,220),outline=(0,0,0)); text(180,SH+7.5,'ALLEY 15 ft (ordinance 1855, on N 1/4 line of orig. Blk 38)',font=FS,anchor='mm')
rect(0,-160.6,BW,-60,outline=(0,0,0),width=2)
# lot lines north side (lots 14..8) and north half (1..7)
xs=[0,58.4,108.4,158.4,208.4,258.4,308.4,358.4]
names=['14','13','12','11','10','9','8']; nnames=['1','2','3','4','5','6','7']
for i,x in enumerate(xs):
    line(x,0,x,SH,width=1); line(x,SH+AL,x,SH+AL+NH,width=1)
    if i<7:
        text((xs[i]+xs[i+1])/2,60,'lot '+names[i],font=F,anchor='mm',fill=(90,90,90))
        text((xs[i]+xs[i+1])/2,SH+AL+50,'lot '+nnames[i],font=F,anchor='mm',fill=(90,90,90))
for x in [83.4,133.4,183.4,233.4,283.4,333.4]:   # half-lot lines (25 ft) dashed
    for yy in range(0,int(SH),4): line(x,yy,x,min(yy+2,SH),fill=(120,120,120))
nums=[('143?',70.9),('141',95.9),('139',120.9),('137',145.9),('135',170.9),('133',195.9),('131',220.9),('129',245.9),('127',270.9),('125',295.9),('123',320.9),('121',345.9)]
for n,x in nums: text(x,-6,n,font=F,anchor='mm')
# G-sub (1874) lots along Jefferson, W 1/2 lot 13 + lot 14 (83.4 x 100.75) -- shown dotted
for yy in [20.15,40.3,60.45,80.6]:
    for xx in range(0,83,4): line(xx,yy,min(xx+2,83.4),yy,fill=(150,150,150))
text(41.7,95,'G re-sub 1874 (5 x 20.15 ft)',font=FS,anchor='mm',fill=(120,120,120))
# south side: H lots (orig 15-17) 0-100, private alley 8.5, H2,H1 25 each, lots 18-21 50 each
sx=[0,100,108.5,133.5,158.5,208.5,258.5,308.5,358.5]
for x in sx: line(x,-160.6,x,-60)
for x in [183.5,233.5,283.5,333.5]:
    for yy in range(-160,-60,4): line(x,yy,x,min(yy+2,-60),fill=(120,120,120))
for yy in [-85,-110,-135]: line(0,yy,100,yy)
text(50,-110,'orig. lots 15-17\n(H re-sub 1883)\n100 ft deep',font=FS,anchor='mm',fill=(90,90,90)); text(104.2,-110,'8.5 ft\nprivate\nalley',font=FS,anchor='mm',fill=(90,90,90))
for n,x in [('140',121),('138',146),('136',171),('134',196),('132',221),('130',246),('128',271),('126',296),('124',321),('122',346)]:
    text(x,-66,n,font=F,anchor='mm')
for n,x in [('lot 18',183.5),('lot 19',233.5),('lot 20',283.5),('lot 21',333.5)]:
    text(x,-120,n,font=F,anchor='mm',fill=(90,90,90))
text(196,-90,'Catherine\nSullivan (134)\n[1869-71 dir.]',font=FS,anchor='mm',fill=(0,0,160)); text(246,-90,'William\nWhite (130)\n[1869-71 dir.;\nBales: E1/2 lot 19]',font=FS,anchor='mm',fill=(0,0,160))
# buildings from Musham plan (digitised)
rows=list(csv.DictReader(open('musham_plan_digitized.csv')))
for r in rows:
    try:
        x0=float(r['x_west_ft']); x1=float(r['x_east_ft']); y0=float(r['y_south_ft']); y1=float(r['y_north_ft'])
    except ValueError: continue
    if 'lot lines' in r['feature']: continue
    col=(255,230,200)
    if 'barn' in r['feature'].lower() and "O'Leary" in r['feature']: col=(255,120,120)
    rect(x0,y0,x1,y1,fill=col,outline=(120,60,0))
    text((x0+x1)/2,(y0+y1)/2,r['label_on_plan'].split(' / ')[0],font=FS,anchor='mm')
# Dalton per Andreas (40 ft deep, on W line of lot); width estimate 20
rect(158.4,38,178.4,78,outline=(200,0,0),width=2); text(168.4,72,'Dalton per Andreas\n(front 38, rear 78,\nwidth est.)',font=FS,anchor='mm',fill=(200,0,0))
line(158.4,78,158.4,88.75,fill=(200,0,0),width=3); text(150,83,'8-ft fence',font=FS,anchor='rm',fill=(200,0,0))
rect(158.4,88.75,178.4,SH,outline=(200,0,0),width=2)
# barn per plat-based placement (20 E-W x 16 N-S, W side of lot, on alley) 
rect(133.4,SH-16,153.4,SH,outline=(180,0,0),width=2)
# passage east of barn
text(156,92,'passage',font=FS,anchor='mm',fill=(120,0,0))
# candidate Sullivan positions and sightlines
cands=[('S1 front of 134 (own house; Andreas 1885)',(196,-64)),('S2 front of White\'s 130 (inquiry; Bales)',(246,-64)),('S3 head of White\'s lot, W corner',(233.5,-62)),('S4 head of White\'s lot, E corner',(258.5,-62))]
targets=[('barn SW',(133.4,SH-16)),('barn SE',(153.4,SH-16)),('barn NE (alley)',(153.4,SH))]
cols=[(0,120,0),(0,0,220),(150,0,150),(200,120,0)]
out=[]
for (cn,(cx,cy)),col in zip(cands,cols):
    d.ellipse([P(cx-2,cy+2),P(cx+2,cy-2)],fill=col)
    text(cx,cy-12,cn.split(' (')[0],font=FS,anchor='mm',fill=col)
    for tn,(tx,ty) in targets:
        line(cx,cy,tx,ty,fill=col,width=1)
        # crossing of Dalton front (y=38), rear (y=78), and lot line x=158.4
        def xat(y): return cx+(tx-cx)*(y-cy)/(ty-cy)
        out.append((cn,tn,round(xat(38),1),round(xat(78),1),round(math.hypot(tx-cx,ty-cy),1)))
# modern parcel and Academy footprint
parcel=[(337.5,114.8),(337.6,99.8),(338.3,0),(18.3,0),(17.6,114.8),(17.2,194),(337.0,194),(337.5,114.8)]
for i in range(len(parcel)-1):
    (a,b),(c,e)=parcel[i],parcel[i+1]; n=int(math.hypot(c-a,e-b)/6)+1
    for k in range(0,n,2):
        line(a+(c-a)*k/n,b+(e-b)*k/n,a+(c-a)*(k+1)/n,b+(e-b)*(k+1)/n,fill=(0,90,200))
acad=[(65.6,13.6),(65.3,75.1),(32.9,75.0),(32.3,188.6),(101.6,188.3),(102.0,181.7),(117.4,181.8),(117.5,90.8),(127.5,91.0),(127.2,80.5),(217.5,80.6),(217.7,14.1),(65.6,13.6)]
for i in range(len(acad)-1):
    (a,b),(c,e)=acad[i],acad[i+1]; line(a,b,c,e,fill=(0,90,200),width=2)
text(150,45,'CFD Fire Academy (1961) front wing - modern footprint',font=FS,anchor='mm',fill=(0,90,200))
text(60,150,'Academy\nwest wing',font=FS,anchor='mm',fill=(0,90,200)); text(180,-170,'blue dashed = Cook County parcel 17-16-324-029 (2021); blue solid = Chicago building footprint',font=FS,anchor='mm',fill=(0,90,200))
# scale bar and north
x=300; y=225
for k in range(0,100,10): rect(x+k,y,x+k+10,y+4,fill=(0,0,0) if (k//10)%2==0 else (255,255,255))
text(x,y+8,'0',font=FS,anchor='mm'); text(x+50,y+8,'50',font=FS,anchor='mm'); text(x+100,y+8,'100 ft',font=FS,anchor='mm')
line(400,200,400,230,width=2); text(400,235,'N (grid; true N is ~1 deg E of grid N)',font=FS,anchor='mm')
text(-55,235,"Block 38, School Section Addition - 137 De Koven St., 8 Oct 1871. x = ft east of 1871 Jefferson E line; y = ft north of De Koven N line. Buildings from Musham 1940 plan (+-2 ft) & Andreas 1885; lots from 1835 'F' sub via 1891 Greeley-Carlson & 1906 Sanborn; NOT a survey.",font=FS,anchor='la')
im.save('block38_plan_1871.png'); print(im.size)
print('sightline crossings (x at Dalton front y=38, x at Dalton rear y=78, distance ft):')
for o in out: print(o)
