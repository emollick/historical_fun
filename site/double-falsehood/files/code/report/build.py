"""Assemble report.html from report_src.html by inlining the SVG figures from figures/."""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
src = open(os.path.join(HERE, 'report_src.html'), encoding='utf-8').read()
def fig(m):
    return open(os.path.join(ROOT, 'figures', m.group(1) + '.svg'), encoding='utf-8').read()
out = re.sub(r'<!--FIG:([a-z0-9_]+)-->', fig, src)
left = re.findall(r'<!--FIG:[^>]*-->', out)
if left: print('unfilled', left)
open(os.path.join(HERE, 'report.html'), 'w', encoding='utf-8').write(out)
open(os.path.join(ROOT, 'report.html'), 'w', encoding='utf-8').write(out)
print('wrote report.html', len(out), 'bytes')
