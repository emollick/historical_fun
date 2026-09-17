#!/usr/bin/env python3
"""Assemble hannibal_alps_report.html from report_body.html by inlining CSS, SVGs, PNGs (as data URIs) and table fragments."""
import pathlib, base64, re
here = pathlib.Path(__file__).resolve().parent
data = here.parent / 'data'
body = (here / 'report_body.html').read_text(encoding='utf-8')
def svg(path):
    t = pathlib.Path(path).read_text(encoding='utf-8')
    return re.sub(r'^<\?xml[^>]*\?>\s*', '', t)
def png(path):
    b = pathlib.Path(path).read_bytes()
    return 'data:image/png;base64,' + base64.b64encode(b).decode('ascii')
parts = {
 '{{CSS}}': (here / 'report.css').read_text(encoding='utf-8'),
 '{{CHART}}': svg(data / 'chart.svg'),
 '{{MAP}}': svg(data / 'map_report.svg') if (data / 'map_report.svg').exists() else svg(data / 'map_overview.svg'),
 '{{PROFILES}}': svg(data / 'profiles_report.svg') if (data / 'profiles_report.svg').exists() else svg(data / 'profiles.svg'),
 '{{VIEWSHED}}': svg(data / 'viewshed_report.svg') if (data / 'viewshed_report.svg').exists() else '',
 '{{TABLE_MATRIX}}': (here / 'frag/table_matrix.html').read_text(encoding='utf-8'),
 '{{TABLE_LOO}}': (here / 'frag/table_loo.html').read_text(encoding='utf-8'),
 '{{TABLE_VARIANTS}}': (here / 'frag/table_variants.html').read_text(encoding='utf-8'),
 '{{TABLE_ROUTES}}': (here / 'frag/table_routes.html').read_text(encoding='utf-8') if (here / 'frag/table_routes.html').exists() else '',
 '{{TABLE_C14}}': (here / 'frag/table_c14.html').read_text(encoding='utf-8') if (here / 'frag/table_c14.html').exists() else '',
}
for k, v in parts.items():
    n = body.count(k)
    assert n <= 1, (k, n)
    body = body.replace(k, v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', body)
assert not left, left
out = here.parent / 'hannibal_alps_report.html'
out.write_text(body, encoding='utf-8')
print(out, len(body))
