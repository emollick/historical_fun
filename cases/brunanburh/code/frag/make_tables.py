#!/usr/bin/env python3
"""Generates HTML table fragments from routes_output.csv and evidence_model_output.json."""
import csv, json, html
rows=list(csv.DictReader(open('routes_output.csv')))
sea=[r for r in rows if r['mode']=='sea']; land=[r for r in rows if r['mode']=='land']
def esc(s): return html.escape(s)
T=['<div class="tablewrap"><table><thead><tr><th>Sea route (coast-hugging, headland to headland)</th><th class="num">km</th><th class="num">nautical miles</th><th class="num">days at 40 nmi/day</th><th class="num">days at 70 nmi/day</th><th class="num">days at 120 nmi/day</th></tr></thead><tbody>']
for r in sea:
    T.append(f"<tr><td>{esc(r['route'])}</td><td class='num'>{r['km']}</td><td class='num'>{r['nmi']}</td><td class='num'>{r['days_slow']}</td><td class='num'>{r['days_mid']}</td><td class='num'>{r['days_fast']}</td></tr>")
T.append('</tbody></table></div>')
open('frag/table_sea.html','w').write('\n'.join(T))
T=['<div class="tablewrap"><table><thead><tr><th>Land route (Roman roads, fort to fort)</th><th class="num">km</th><th class="num">days at 15 km/day</th><th class="num">days at 20 km/day</th><th class="num">days at 25 km/day</th></tr></thead><tbody>']
for r in land:
    T.append(f"<tr><td>{esc(r['route'])}</td><td class='num'>{r['km']}</td><td class='num'>{r['days_slow']}</td><td class='num'>{r['days_mid']}</td><td class='num'>{r['days_fast']}</td></tr>")
T.append('</tbody></table></div>')
open('frag/table_land.html','w').write('\n'.join(T))
d=json.load(open('evidence_model_output.json'))
cands=[c for c in d['point']]
short={'Bromborough (Wirral)':'Bromborough','Went valley / Burghwallis (Wood 2013)':'Went / Burghwallis','Brinsworth / Tinsley (Wood 1980)':'Brinsworth','Other Humber-bank sites (E. Riding, Barrow, Brough)':'Other Humber','Burnswark (Dumfriesshire)':'Burnswark','Lanchester (Co. Durham)':'Lanchester','Lancashire west coast (Ribble, Fylde, Wigan, Burnley)':'Lancashire coast','Southern / inland (Bourn, Bromswold, Bourne, Axminster)':'Southern / inland','Other, unidentified site':'Other'}
ev=d['evidence']
T=['<div class="tablewrap"><table><thead><tr><th>Evidence item</th>']+[f'<th class="num">{esc(short[c])}</th>' for c in cands if c!='Other, unidentified site']+['</tr></thead><tbody>']
for e,tab in ev.items():
    T.append('<tr><td>'+esc(e)+'</td>'+''.join(f"<td class='num'>{tab[c][0]:g}–{tab[c][1]:g}</td>" for c in cands if c!='Other, unidentified site')+'</tr>')
T.append('<tr class="hl"><td>Prior</td>'+''.join(f"<td class='num'>{d['prior'][c]:.2f}</td>" for c in cands if c!='Other, unidentified site')+'</tr>')
def pct(v, dec=None):
    # shares that would round to 0% are shown to one decimal; everything else as before
    x=v*100
    if dec is None: dec = 1 if 0<x<0.5 else 0
    return f'{x:.{dec}f}'
T.append('<tr class="hl"><td>Posterior (point; 5–95% of draws)</td>'+''.join(f"<td class='num'>{pct(d['point'][c])}%<br><span style='font-weight:400'>{pct(d['mc'][c]['p05'], 1 if d['mc'][c]['p95']*100<0.5 else 0)}–{pct(d['mc'][c]['p95'], 1 if d['mc'][c]['p95']*100<0.5 else 0)}</span></td>" for c in cands if c!='Other, unidentified site')+'</tr>')
T.append('</tbody></table></div>')
open('frag/table_matrix.html','w').write('\n'.join(T))
# leave-one-out table
lead='Bromborough (Wirral)'; OTHER='Other, unidentified site'
T=['<div class="tablewrap"><table><thead><tr><th>Remove this item</th><th class="num">Bromborough</th><th>Best rival</th><th class="num">Rival</th><th class="num">Unidentified</th></tr></thead><tbody>']
for e,p in d['leave_one_out'].items():
    rival=max((c for c in cands if c not in (lead,OTHER)), key=lambda c:p[c])
    T.append(f"<tr><td>{esc(e)}</td><td class='num'>{p[lead]*100:.0f}%</td><td>{esc(short[rival])}</td><td class='num'>{p[rival]*100:.0f}%</td><td class='num'>{p[OTHER]*100:.0f}%</td></tr>")
T.append('</tbody></table></div>')
open('frag/table_loo.html','w').write('\n'.join(T))
print('tables written')
