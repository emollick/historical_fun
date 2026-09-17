#!/usr/bin/env python3
"""Make data/map_report.svg from data/map_overview.svg (figures.py output): drop the in-image caption and footnote,
which the report carries as a figcaption, and trim the canvas to the legend."""
import pathlib, re
data = pathlib.Path(__file__).resolve().parent.parent / 'data'
s = (data / 'map_overview.svg').read_text(encoding='utf-8')
s = re.sub(r'<text x="12" y="715"[^>]*>[^<]*</text>\s*', '', s)
s = re.sub(r'<text x="12" y="855"[^>]*>[^<]*</text>\s*', '', s)
# move legend up by 14 px and cut the canvas
def shift(m):
    y = float(m.group(2)); return f'{m.group(1)}"{y-14:g}"'
s = re.sub(r'(<line [^>]*?y1=)"(7\d\d|8\d\d)"', shift, s)
s = re.sub(r'(<line [^>]*?y2=)"(7\d\d|8\d\d)"', shift, s)
s = re.sub(r'(<text x="(?:60|600)" y=)"(7\d\d|8\d\d)"', shift, s)
s = s.replace('width="961" height="887" viewBox="0 0 961 887"', 'width="961" height="852" viewBox="0 0 961 852"')
s = s.replace('<rect x="0" y="697" width="961" height="190" fill="#fff"/>', '<rect x="0" y="697" width="961" height="155" fill="#fff"/>')
(data / 'map_report.svg').write_text(s, encoding='utf-8')
print('map_report.svg', len(s))
