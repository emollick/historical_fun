import json, math, csv
# --- geodesy helpers (local flat-earth, feet) ---
lat0=41.8693; lon0=-87.6419
ftlat=364567.0; ftlon=364567.0*math.cos(math.radians(lat0))
def xy(lon,lat): return ((lon-lon0)*ftlon,(lat-lat0)*ftlat)
def lonlat(x,y): return (lon0+x/ftlon, lat0+y/ftlat)
# --- Cook County parcel 17-16-324-029 (Fire Academy) polygon ---
g=json.load(open('../parcels/cook_parcels_2021_block.geojson'))
poly=[f for f in g['features'] if f['properties']['pin10']=='1716324029'][0]['geometry']['coordinates'][0][0]
P=[xy(*p) for p in poly]
# parcel SW corner = vertex with min (x+y) roughly; find vertex nearest (-55,-80)
sw=min(P,key=lambda p: math.hypot(p[0]+55.4,p[1]+80.7))
se=min(P,key=lambda p: math.hypot(p[0]-264.5,p[1]+74.9))
nw=min(P,key=lambda p: math.hypot(p[0]+60.1,p[1]-113.2))
ne=min(P,key=lambda p: math.hypot(p[0]-259.7,p[1]-119.0))
# x-axis unit vector along south edge (SW->SE), y-axis perpendicular (rotate +90 deg)
ex=(se[0]-sw[0], se[1]-sw[1]); L=math.hypot(*ex); ex=(ex[0]/L, ex[1]/L)
ey=(-ex[1], ex[0])
bearing_x=math.degrees(math.atan2(ex[0],ex[1]))%360
print('parcel south edge length %.1f ft, bearing %.2f deg (grid east)'%(L,bearing_x))
# 1871 origin O = parcel SW corner shifted 18.3 ft west along the DeKoven north line
WEST_OFFSET=18.3   # ft: 1871 lot-line vertices in the parcel are offset by this (see REPORT)
O=(sw[0]-WEST_OFFSET*ex[0], sw[1]-WEST_OFFSET*ex[1])
def to_plan(p):   # local ft -> 1871 plan ft (x east along DeKoven N line, y north along Jefferson E line)
    dx,dy=p[0]-O[0],p[1]-O[1]
    return (dx*ex[0]+dy*ex[1], dx*ey[0]+dy*ey[1])
def from_plan(x,y):
    return (O[0]+x*ex[0]+y*ey[0], O[1]+x*ex[1]+y*ey[1])
rows=[]
def add(name,x,y,src,res):
    lx,ly=from_plan(x,y); lon,lat=lonlat(lx,ly)
    rows.append((name,round(x,1),round(y,1),round(lat,6),round(lon,6),src,res))
# parcel corners in plan coords
for nm,p in [('Academy parcel SW corner',sw),('Academy parcel SE corner',se),('Academy parcel NW corner',nw),('Academy parcel NE corner',ne)]:
    x,y=to_plan(p); add(nm,x,y,'Cook County parcel polygon (PIN 17-16-324-029), 2021 GIS','survey-grade GIS parcel (few ft)')
print('parcel vertices in plan coords:')
for p in P:
    x,y=to_plan(p); print('   %7.1f %7.1f'%(x,y))
# 1871 block (School Section Addition Block 38) per Greeley-Carlson 1891 plate 28 + 1833 plat (358 ft) + G-sub (100.75) + alley 15 + N half ~100
BW=358.4; S_HALF=100.75; ALLEY=15.0; N_HALF=100.0
add('Block 38 SW corner (Jefferson E line x DeKoven N line) = plan origin',0,0,'derived: parcel SW corner - 18.3 ft (lot-line vertex offsets)','estimate +-2 ft')
add('Block 38 SE corner (Clinton W line x DeKoven N line)',BW,0,'1833 plat width 358 ft; G-sub 83.4+E1/2 lot13 25+5x50','+-2 ft')
add('Block 38 NW corner (Jefferson E line x Taylor S line)',0,S_HALF+ALLEY+N_HALF,'S half 100.75 (G-sub 5x20.15) + alley 15 + N half ~100 (1875 survey of adjoining blocks 99.55-100.83)','+-2 ft')
add('Block 38 NE corner',BW,S_HALF+ALLEY+N_HALF,'as above','+-2 ft')
add('Alley south line at O\'Leary lot (x=133.4..158.4)',145.9,S_HALF,'G-sub depth 100.75; parcel vertex 15-ft alley segment','+-1 ft')
add('Alley north line',145.9,S_HALF+ALLEY,'15-ft alley (Musham plan; parcel vertex)','+-1 ft')
# lots on DeKoven, north side (F sub): lot 14 = 58.4 W, lots 13..8 = 50 ft each
xl=0
lots=[('lot 14 (G-sub 1874: 5 lots 20.15 x 83.4 facing Jefferson)',58.4),('lot 13',50),('lot 12',50),('lot 11',50),('lot 10',50),('lot 9',50),('lot 8',50)]
for nm,w in lots:
    add('Block 38 %s west line on DeKoven'%nm,xl,0,'Greeley-Carlson 1891 pl.28 (4.03 px/ft) + parcel vertices','+-1.5 ft'); xl+=w
add('O\'Leary lot (137) = E 1/2 lot 12, SW corner (street line)',133.4,0,'Musham 1940 plan (saloon-face calibrated) + 1891 numbering + Bales lot refs','+-1.5 ft')
add('O\'Leary lot SE corner (street line)',158.4,0,'','')
add('O\'Leary lot NE corner (alley)',158.4,S_HALF,'','')
add('O\'Leary lot NW corner (alley)',133.4,S_HALF,'','')
add('O\'Leary barn SW corner (20 ft E-W x 16 ft N-S at alley, W side of lot)',133.4,S_HALF-16,'Musham plan: barn 16x20 on alley, passage on E side; Andreas: S line 8 ft N of Dalton rear','+-3 ft')
add('O\'Leary barn SE corner',153.4,S_HALF-16,'','')
add('O\'Leary barn NE corner',153.4,S_HALF,'','')
add('O\'Leary barn NW corner',133.4,S_HALF,'','')
add('O\'Leary cottages (double, 16 wide x 36 N-S) SW corner',137.0,2.0,'Andreas 36 ft N-S front nearly on street line; Musham plan 16 ft wide, ~3 ft in from W line','+-3 ft')
add('O\'Leary cottages NE corner',153.0,38.0,'','')
add('Dalton house (135) SW corner on O\'Leary E line',158.4,38.0,'Andreas: on W line of lot, front 2 ft S of O\'Leary N line, 40 ft deep, 4 ft above ground on posts','+-3 ft')
add('Dalton house NE corner (width ~20 ft estimated from Musham plan)',178.4,78.0,'','width is estimate')
add('Dalton shed 12x20 at alley, W side of lot',158.4,S_HALF-12,'Andreas 12x20 shed at rear on W side; Musham plan','+-3 ft')
add('Dalton 8-ft fence from house to shed on lot W line',158.4,78.0,'Andreas','')
add('133 (Lee/Canavan/Forbes) = E 1/2 lot 11 west line',183.4,0,'','')
# south side of DeKoven (Block 37, H-sub): H lots 3-6 face Jefferson 100 deep; private alley 8.5; H lots 2,1 = 25 each; lots 18-21 = 50 each
DEK=60.0
add('Block 38 south part, NW corner (Jefferson E line x DeKoven S line)',0,-DEK,'DeKoven 60 ft (1891 plate, Musham, Sanborn 1906)','+-2 ft')
xs=0
for nm,w in [('orig. lots 15-17 = H-sub 1883 lots 3-6 (100 ft deep, face Jefferson)',100),('private alley 8.5',8.5),('H lot 2 (No.140)',25),('H lot 1 (No.138)',25),('lot 18 W (No.136)',25),('lot 18 E (No.134, Catherine Sullivan)',25),('lot 19 W (No.132)',25),('lot 19 E (No.130, William White)',25),('lot 20 W (No.128)',25),('lot 20 E (No.126)',25),('lot 21 W (No.124)',25),('lot 21 E (No.122)',25)]:
    add('Block 38 (S of DeKoven) %s west line on DeKoven S line'%nm,xs,-DEK,'1891 pl.28 H-sub dims + 1891/1906 house numbers at 25-ft granularity + Bales (White E1/2 lot 19) + Andreas affidavit (137 = E1/2 lot 12)','+-2 ft'); xs+=w
add('South side lots north half depth (H lots 1-2: 100.6 ft)',0,-DEK-100.6,'1891 pl.28 H-sub','')
# modern Fire Academy building footprint (Chicago building footprints dataset, bldg_id 369839) converted to plan coords
for nm,(x,y) in [('CFD Fire Academy front wing SW corner',(65.6,13.6)),('CFD Fire Academy front wing SE corner',(217.7,14.1)),('CFD Fire Academy front wing NE corner',(217.5,80.6)),('CFD Fire Academy front wing rear wall at x=127',(127.2,80.5)),('CFD Fire Academy west wing NW corner',(32.3,188.6)),('CFD Fire Academy rear wing NE corner',(117.4,181.8))]:
    add(nm,x,y,'Chicago Building Footprints (data.cityofchicago.org syp8-uezg) via parcels/chicago_footprints_block.geojson','GIS footprint, +-3 ft')

with open('plan_coordinates.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['feature','x_ft_east_of_Jefferson_E_line','y_ft_north_of_DeKoven_N_line','lat','lon','source','resolution']); w.writerows(rows)
print('origin O lat/lon:', lonlat(*O))
for r in rows: print(r)
