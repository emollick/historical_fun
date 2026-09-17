#!/usr/bin/env python3
"""Builds an inline SVG map (equirectangular, cos-lat corrected) of the British Isles
with the candidate sites, the coalition start points and the modelled routes.
Coastline: Natural Earth 1:50m (public domain), clipped by routes.py's companion step.
Output: map.svg (styled through CSS classes so the host page's theme applies)."""
import json, math
coast=json.load(open('data/british_isles_coast_50m.json'))
LON0,LON1,LAT0,LAT1=-10.6,1.9,50.0,59.2
K=60.0; C=math.cos(math.radians(55.0))
W=(LON1-LON0)*C*K; H=(LAT1-LAT0)*K
def xy(lat,lon): return ((lon-LON0)*C*K, (LAT1-lat)*K)
def fmt(p): return f"{p[0]:.1f},{p[1]:.1f}"
out=[]
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" class="bmap" role="img" aria-labelledby="bmap-title bmap-desc">')
out.append('<title id="bmap-title">Candidate sites for Brunanburh and the routes to them</title>')
out.append('<desc id="bmap-desc">Map of Britain and Ireland showing the six candidate battlefields, the start points of the Dublin fleet, the Scots, the Cumbrians and the West Saxons, and the sea and Roman-road routes modelled in routes.py.</desc>')
out.append('<rect width="100%" height="100%" class="bmap-sea"/>')
# coast
paths=[]
for seg in coast:
    pts=[xy(lat,lon) for lon,lat in seg]
    paths.append('M'+' L'.join(fmt(p) for p in pts))
out.append('<path class="bmap-coast" d="'+' '.join(paths)+'"/>')
# routes (subset, from routes.py waypoints)
SEA={
 'dub-dee':[(53.345,-6.20),(53.37,-6.04),(53.42,-3.30),(53.38,-3.22)],
 'dub-solway':[(53.345,-6.20),(53.37,-6.04),(54.10,-4.75),(54.42,-4.36),(54.75,-3.75),(54.97,-3.27)],
 'dub-humber-N':[(53.345,-6.20),(53.37,-6.04),(54.20,-5.50),(54.90,-5.40),(55.25,-5.85),(55.70,-6.55),(56.35,-7.10),(56.85,-6.90),(57.45,-6.85),(58.05,-5.90),(58.65,-5.05),(58.70,-3.40),(58.64,-3.00),(58.15,-3.30),(57.72,-1.95),(57.47,-1.75),(57.15,-2.00),(56.70,-2.40),(56.28,-2.55),(55.92,-2.10),(55.62,-1.60),(55.01,-1.35),(54.50,-0.55),(54.12,-0.05),(53.58,0.11)],
 'dub-humber-S':[(53.345,-6.20),(52.97,-5.95),(52.20,-6.15),(51.90,-5.35),(51.15,-4.75),(50.05,-5.75),(49.95,-5.15),(50.20,-3.60),(50.50,-2.40),(50.55,-1.25),(50.72,0.25),(51.12,1.40),(51.38,1.48),(52.08,1.62),(52.62,1.78),(52.95,1.30),(52.98,0.45),(53.15,0.38),(53.58,0.11)],
}
LAND={
 'dere':[(56.40,-3.45),(56.12,-3.94),(55.99,-3.86),(55.94,-3.06),(55.60,-2.69),(55.28,-2.31),(54.97,-2.02),(54.82,-1.74),(54.67,-1.68),(54.38,-1.63),(54.09,-1.38),(53.96,-1.08),(53.88,-1.26),(53.72,-1.36),(53.636,-1.267),(53.52,-1.13),(53.408,-1.383)],
 'west':[(56.40,-3.45),(56.12,-3.94),(55.71,-3.62),(55.47,-3.66),(55.108,-3.254),(54.89,-2.94),(54.65,-2.72),(54.40,-2.60),(54.05,-2.80),(53.81,-2.53),(53.55,-2.63),(53.39,-2.58),(53.19,-2.89),(53.343,-2.987)],
 'strath':[(55.90,-4.45),(55.71,-3.62)],
 'wessex-chester':[(51.063,-1.308),(51.75,-1.26),(52.13,-0.99),(52.66,-1.83),(52.72,-2.55),(52.83,-2.75),(53.19,-2.89)],
 'wessex-humber':[(51.063,-1.308),(51.51,-0.09),(52.24,-0.27),(52.77,-0.38),(53.23,-0.54),(53.52,-1.13)],
}
for k,pts in SEA.items():
    out.append(f'<polyline class="bmap-sea-route r-{k}" points="'+' '.join(fmt(xy(*p)) for p in pts)+'"/>')
for k,pts in LAND.items():
    out.append(f'<polyline class="bmap-land-route r-{k}" points="'+' '.join(fmt(xy(*p)) for p in pts)+'"/>')
SITES=[('Bromborough',53.343,-2.987,'site',-8,14),('Brinsworth',53.408,-1.383,'site',6,14),('Went valley',53.636,-1.267,'site',6,-4),('Burnswark',55.108,-3.254,'site',-64,-6),('Lanchester',54.822,-1.740,'site',6,4),('Burnley',53.789,-2.248,'site',-46,-6),
       ('Dublin',53.345,-6.20,'start',-40,-8),('Scone',56.40,-3.45,'start',6,-4),('Govan',55.90,-4.45,'start',-40,-6),('Winchester',51.063,-1.308,'start',6,12),('York',53.96,-1.08,'town',6,-3),('Chester',53.19,-2.89,'town',-48,10),('Humber',53.60,-0.30,'label',4,-2)]
for name,lat,lon,cls,dx,dy in SITES:
    x,y=xy(lat,lon)
    if cls!='label':
        r = 4.5 if cls=='site' else 3
        out.append(f'<circle class="bmap-{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')
    out.append(f'<text class="bmap-lbl bmap-lbl-{cls}" x="{x+dx:.1f}" y="{y+dy:.1f}">{name}</text>')
out.append('</svg>')
open('map.svg','w').write('\n'.join(out))
print('map.svg written', f'{W:.0f}x{H:.0f}', 'bytes', sum(len(s) for s in out))
