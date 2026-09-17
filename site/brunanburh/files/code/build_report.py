#!/usr/bin/env python3
"""Assemble brunanburh_report.html from report_body.html by inlining CSS, SVGs and table fragments."""
import pathlib
here = pathlib.Path(__file__).parent
body = (here/'report_body.html').read_text(encoding='utf-8')
parts = {
 '{{CSS}}': (here/'report.css').read_text(encoding='utf-8'),
 '{{MAP}}': (here/'map.svg').read_text(encoding='utf-8'),
 '{{CHART}}': (here/'chart.svg').read_text(encoding='utf-8'),
 '{{TABLE_SEA}}': (here/'frag/table_sea.html').read_text(encoding='utf-8'),
 '{{TABLE_LAND}}': (here/'frag/table_land.html').read_text(encoding='utf-8'),
 '{{TABLE_MATRIX}}': (here/'frag/table_matrix.html').read_text(encoding='utf-8'),
 '{{TABLE_LOO}}': (here/'frag/table_loo.html').read_text(encoding='utf-8'),
}
for k, v in parts.items():
    assert body.count(k) == 1, k
    body = body.replace(k, v)
out = here/'brunanburh_report.html'
out.write_text(body, encoding='utf-8')
print(out, len(body))
