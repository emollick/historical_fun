#!/usr/bin/env python3
"""Draw the posterior chart (point estimate with Monte-Carlo 5-95% band) as an SVG that uses the report's CSS classes.
Reads ../data/evidence_model_output.json; writes ../data/chart.svg"""
import json, pathlib, html
here = pathlib.Path(__file__).resolve().parent
data = here.parent / 'data'
out = json.load(open(data / 'evidence_model_output.json', encoding='utf-8'))
import sys; sys.path.insert(0, str(here))
from evidence_table import SHORT
p = out['polybius_half']; mc = out['polybius_half_monte_carlo']  # headline run: Polybian items at half strength
order = sorted(p, key=lambda c: -p[c])
W, rowh, left, right, top = 760, 34, 250, 60, 30
H = top + rowh * len(order) + 40
xmax = max(0.5, max(mc[c]['p95'] for c in order) * 1.08)
def X(v): return left + (W - left - right) * v / xmax
s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Share of each candidate pass in the headline run of the evidence model, with 5 to 95 percent Monte-Carlo bands">']
s.append(f'<title>Posterior probability of each candidate pass</title>')
# axis ticks
tick = 0.1
v = 0.0
while v <= xmax + 1e-9:
    x = X(v)
    s.append(f'<line class="axis" x1="{x:.1f}" y1="{top-8}" x2="{x:.1f}" y2="{H-30}"/>')
    s.append(f'<text class="tick" x="{x:.1f}" y="{H-14}" text-anchor="middle">{int(round(v*100))}%</text>')
    v += tick
for i, c in enumerate(order):
    y = top + i * rowh
    cls = 'bar' if i == 0 else ('bar second' if i == 1 else 'bar other')
    if c.startswith('Other') or c.startswith('Some'): cls = 'bar other'
    s.append(f'<text class="lbl" x="{left-10}" y="{y+rowh*0.62:.1f}" text-anchor="end">{html.escape(SHORT.get(c, c))}</text>')
    s.append(f'<rect class="{cls}" x="{X(0):.1f}" y="{y+6}" width="{X(p[c])-X(0):.1f}" height="{rowh-14}" rx="1"/>')
    lo, hi = mc[c]['p05'], mc[c]['p95']
    ym = y + rowh/2 - 1
    s.append(f'<line class="range" x1="{X(lo):.1f}" y1="{ym:.1f}" x2="{X(hi):.1f}" y2="{ym:.1f}"/>')
    for e in (lo, hi):
        s.append(f'<line class="range" x1="{X(e):.1f}" y1="{ym-5:.1f}" x2="{X(e):.1f}" y2="{ym+5:.1f}"/>')
    s.append(f'<text class="val" x="{X(hi)+8:.1f}" y="{y+rowh*0.62:.1f}">{p[c]*100:.0f}% ({lo*100:.0f}–{hi*100:.0f})</text>')
s.append('</svg>')
(data / 'chart.svg').write_text('\n'.join(s), encoding='utf-8')
print('chart.svg written', H)
