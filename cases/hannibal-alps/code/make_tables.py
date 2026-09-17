#!/usr/bin/env python3
"""Build the HTML table fragments for the report from the evidence-model output and the evidence table.
Writes frag/table_matrix.html, frag/table_loo.html, frag/table_variants.html"""
import json, pathlib, html, math
here = pathlib.Path(__file__).resolve().parent
data = here.parent / 'data'
frag = here / 'frag'; frag.mkdir(exist_ok=True)
out = json.load(open(data / 'evidence_model_output.json', encoding='utf-8'))
from evidence_table import CANDS, EVIDENCE, SHORT
p = out['point']; ph = out['polybius_half']
def pct(v): return f'{100*v:.0f}%' if v >= 0.005 else '<1%'
# matrix of ranges
rows = ['<div class="tablewrap"><table><thead><tr><th>Line of evidence</th>' + ''.join(f'<th class="num">{html.escape(SHORT[c])}</th>' for c in CANDS) + '</tr></thead><tbody>']
for it in EVIDENCE:
    rows.append('<tr><td>' + html.escape(it) + '</td>' + ''.join(
        '<td class="num">%s–%s</td>' % (('%.2g' % EVIDENCE[it][c][0]).rstrip('0').rstrip('.'), ('%.2g' % EVIDENCE[it][c][1]).rstrip('0').rstrip('.')) for c in CANDS) + '</tr>')
rows.append('<tr class="hl"><td><b>Headline run (Polybian items at half strength)</b></td>' + ''.join(f'<td class="num"><b>{pct(ph[c])}</b></td>' for c in CANDS) + '</tr>')
rows.append('<tr><td>Full model (every item at full strength)</td>' + ''.join(f'<td class="num">{pct(p[c])}</td>' for c in CANDS) + '</tr>')
rows.append('</tbody></table></div>')
(frag / 'table_matrix.html').write_text('\n'.join(rows), encoding='utf-8')
# leave one out
loo = out['polybius_half_leave_one_out']
rows = ['<div class="tablewrap"><table><thead><tr><th>Item dropped (headline run)</th>' + ''.join(f'<th class="num">{html.escape(SHORT[c])}</th>' for c in CANDS) + '</tr></thead><tbody>']
rows.append('<tr><td>None</td>' + ''.join(f'<td class="num">{pct(ph[c])}</td>' for c in CANDS) + '</tr>')
for it in loo:
    rows.append('<tr><td>' + html.escape(it) + '</td>' + ''.join(f'<td class="num">{pct(loo[it][c])}</td>' for c in CANDS) + '</tr>')
rows.append('</tbody></table></div>')
(frag / 'table_loo.html').write_text('\n'.join(rows), encoding='utf-8')
# variants
names = [('polybius_half', 'Headline run: Polybian items at half strength, the rest at full strength'), ('point', 'Full model: every item at full strength'),
         ('polybius_half_flat_prior', 'Headline run with a flat prior'), ('tempered_half', 'Every item at half strength'),
         ('collapsed_by_source', 'Each source family counted as one item'), ('tempered_half_collapsed', 'Halved and collapsed')]
rows = ['<div class="tablewrap"><table><thead><tr><th>Variant</th>' + ''.join(f'<th class="num">{html.escape(SHORT[c])}</th>' for c in CANDS) + '</tr></thead><tbody>']
for k, label in names:
    rows.append('<tr><td>' + label + '</td>' + ''.join(f'<td class="num">{pct(out[k][c])}</td>' for c in CANDS) + '</tr>')
for k, s in out['polybius_half_scenarios'].items():
    rows.append('<tr><td>Scenario, headline run: ' + html.escape(k) + (' (' + html.escape(s['note']) + ')' if s.get('note') else '') + '</td>' + ''.join(f'<td class="num">{pct(s["posterior"][c])}</td>' for c in CANDS) + '</tr>')
rows.append('<tr><td>Best case for each candidate (its high ends, rivals\' low ends)</td>' + ''.join(f'<td class="num">{pct(out["best_case_share"][c])}</td>' for c in CANDS) + '</tr>')
rows.append('</tbody></table></div>')
(frag / 'table_variants.html').write_text('\n'.join(rows), encoding='utf-8')
print('tables written')
