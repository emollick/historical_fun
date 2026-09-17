#!/usr/bin/env python3
"""Compass-rose figure of the Po-plain viewshed for each candidate col, from data/viewshed_output.json.
Wedges: sector of azimuths from which any Po-plain cell (<400 m) is in line of sight, from the col itself (dark)
and from the best vantage point within 1.5 km and 300 m above the col (light). Writes data/viewshed_report.svg."""
import json, math, pathlib
here = pathlib.Path(__file__).resolve().parent
data = here.parent / 'data'
d = json.load(open(data / 'viewshed_output.json', encoding='utf-8'))
ORDER = ['Col de la Traversette', 'Col Clapier', 'Col du Mont-Cenis', 'Col du Petit Mont-Cenis', 'Col de Montgenevre',
         'Col de Larche', 'Col du Petit-Saint-Bernard', 'Col du Grand-Saint-Bernard', 'Col Agnel']
LABEL = {'Col de la Traversette': 'Traversette', 'Col Clapier': 'Clapier', 'Col du Mont-Cenis': 'Mont-Cenis',
         'Col du Petit Mont-Cenis': 'Petit Mont-Cenis', 'Col de Montgenevre': 'Montgenèvre', 'Col de Larche': 'Larche',
         'Col du Petit-Saint-Bernard': 'Petit St Bernard', 'Col du Grand-Saint-Bernard': 'Grand St Bernard', 'Col Agnel': 'Agnel'}
MAPH = {'Col de la Traversette': 2947, 'Col Clapier': 2482, 'Col du Mont-Cenis': 2083, 'Col du Petit Mont-Cenis': 2183,
        'Col de Montgenevre': 1854, 'Col de Larche': 1991, 'Col du Petit-Saint-Bernard': 2188, 'Col du Grand-Saint-Bernard': 2469, 'Col Agnel': 2744}
cols, rows = 3, 3
cw, ch = 310, 180
W, H = cols * cw + 20, rows * ch + 30
R = 46
def wedge(cx, cy, a0, a1, r, cls, fill):
    a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
    x0, y0 = cx + r * math.cos(a0r), cy + r * math.sin(a0r)
    x1, y1 = cx + r * math.cos(a1r), cy + r * math.sin(a1r)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'<path class="{cls}" d="M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f} Z" style="fill:{fill};stroke:none"/>'
s = [f'<svg class="vs" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="For each candidate col, the compass sector from which the Po plain is in line of sight">',
     '<title>Where the Po plain can be seen from</title>',
     '<style>.vs text{font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;fill:var(--ink,#182129)} .vs .nm{font-family:"Newsreader",Georgia,serif;font-size:15px;font-weight:600} .vs .sm{font-size:10px;fill:var(--ink-2,#4A5B66)} .vs .ring{fill:var(--snow,#FAFBFC);stroke:var(--rule,#C4CED5)} .vs .tick{stroke:var(--rule,#C4CED5)} .vs .n{font-size:9px;fill:var(--ink-3,#71838E)}</style>']
for i, name in enumerate(ORDER):
    c = d['cols'][name]
    gx, gy = 10 + (i % cols) * cw, 10 + (i // cols) * ch
    cx, cy = gx + 60, gy + 78
    s.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{R}"/>')
    for a in (0, 90, 180, 270):
        ar = math.radians(a - 90)
        s.append(f'<line class="tick" x1="{cx + (R-4)*math.cos(ar):.1f}" y1="{cy + (R-4)*math.sin(ar):.1f}" x2="{cx + (R+4)*math.cos(ar):.1f}" y2="{cy + (R+4)*math.sin(ar):.1f}"/>')
    s.append(f'<text class="n" x="{cx}" y="{cy-R-7}" text-anchor="middle">N</text><text class="n" x="{cx+R+9}" y="{cy+3}" text-anchor="middle">E</text>')
    best = c['vantage_scan'].get('best') or {}
    br = best.get('azimuth_range_with_plain')
    if br and best.get('plain_visible'):
        s.append(wedge(cx, cy, br[0], br[1], R - 2, 'w2', 'var(--second-soft,#D3E4EC)'))
    cr = c['col'].get('azimuth_range_with_plain')
    if cr and c['col'].get('plain_visible'):
        a0, a1 = cr
        if a1 - a0 < 3: a0, a1 = (a0 + a1) / 2 - 1.5, (a0 + a1) / 2 + 1.5
        s.append(wedge(cx, cy, a0, a1, R - 2, 'w1', 'var(--accent,#A3690F)'))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="2.2" style="fill:var(--ink,#182129)"/>')
    tx = gx + 118
    s.append(f'<text class="nm" x="{tx}" y="{gy+26}">{LABEL[name]}</text>')
    s.append(f'<text class="sm" x="{tx}" y="{gy+42}">{MAPH[name]} m</text>')
    fc = 100 * c['col']['frac_azimuths_plain_visible']
    near = c['col'].get('nearest_plain')
    s.append(f'<text class="sm" x="{tx}" y="{gy+62}">col: {("%.1f%% of bearings" % fc) if fc > 0 else "no plain in sight"}</text>')
    s.append(f'<text class="sm" x="{tx}" y="{gy+76}">{("nearest plain %.0f km" % near["km"]) if near else "nearest plain: none"}</text>')
    f = c.get('first_descent_point_with_plain')
    s.append(f'<text class="sm" x="{tx}" y="{gy+92}">descent: {("view %.2g km down (%.0f%%)" % (f["km_from_col"], 100*f["frac_azimuths_plain_visible"])) if f else "none within 10 km"}</text>')
    vs = c['vantage_scan']
    fb = 100 * best.get('frac_azimuths_plain_visible', 0) if best else 0
    s.append(f'<text class="sm" x="{tx}" y="{gy+108}">near col: {vs["n_with_plain_visible"]} of {vs["n_points"]} points see it</text>')
    s.append(f'<text class="sm" x="{tx}" y="{gy+122}">best {fb:.1f}%{(" at %d m" % round(best["z"])) if best and fb > 0 else ""}</text>')
s.append('</svg>')
(data / 'viewshed_report.svg').write_text('\n'.join(s), encoding='utf-8')
print('written', W, H)
