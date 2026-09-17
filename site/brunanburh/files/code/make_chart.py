#!/usr/bin/env python3
"""Horizontal bar chart of the model's posterior probabilities with 5-95% Monte-Carlo whiskers. Inline SVG styled by the page CSS."""
import json
d=json.load(open('evidence_model_output.json'))
point=d['point']; mc=d['mc']
short={
 'Bromborough (Wirral)':'Bromborough, Wirral',
 'Other, unidentified site':'Some other, unidentified place',
 'Went valley / Burghwallis (Wood 2013)':'Went valley / Burghwallis (Wood)',
 'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)':'Lancashire coast (Ribble to Burnley)',
 'Other Humber-bank sites (E. Riding, Barrow, Brough)':'Other Humber-bank sites',
 'Burnswark (Dumfriesshire)':'Burnswark, Dumfriesshire',
 'Brinsworth / Tinsley (Wood 1980)':'Brinsworth / Tinsley (Wood 1980)',
 'Lanchester (Co. Durham)':'Lanchester, Co. Durham',
 'Southern / inland (Bourn, Bromswold, Bourne, Axminster)':'Southern / inland (Bourn, Bromswold…)',
}
order=sorted(point, key=lambda c:-point[c])
W=760; left=300; right=70; top=18; rowh=34; H=top+rowh*len(order)+34
x0=left; x1=W-right; sc=(x1-x0)
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="chart" role="img" aria-labelledby="pchart-title pchart-desc">',
     '<title id="pchart-title">Probability that each candidate is the site of Brunanburh</title>',
     '<desc id="pchart-desc">Bars show the model point estimate; whiskers show the 5th to 95th percentile of the Monte-Carlo draws.</desc>']
# axis ticks
for tk in [0,.2,.4,.6,.8,1.0]:
    x=x0+sc*tk
    out.append(f'<line class="axis" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{H-30}"/>')
    out.append(f'<text class="tick" x="{x:.1f}" y="{H-12}" text-anchor="middle">{int(tk*100)}%</text>')
for i,c in enumerate(order):
    y=top+rowh*i+6; p=point[c]; lo=mc[c]['p05']; hi=mc[c]['p95']
    cls='bar other' if c=='Other, unidentified site' else 'bar'
    out.append(f'<text class="lbl" x="{x0-10}" y="{y+15}" text-anchor="end">{short[c]}</text>')
    out.append(f'<rect class="{cls}" x="{x0}" y="{y}" width="{max(1.5,sc*p):.1f}" height="20" rx="1.5"/>')
    yc=y+10
    out.append(f'<line class="range" x1="{x0+sc*lo:.1f}" y1="{yc}" x2="{x0+sc*hi:.1f}" y2="{yc}"/>')
    out.append(f'<line class="cap" x1="{x0+sc*lo:.1f}" y1="{yc-5}" x2="{x0+sc*lo:.1f}" y2="{yc+5}"/>')
    out.append(f'<line class="cap" x1="{x0+sc*hi:.1f}" y1="{yc-5}" x2="{x0+sc*hi:.1f}" y2="{yc+5}"/>')
    out.append(f'<text class="val" x="{x0+sc*hi+8:.1f}" y="{y+15}">{(f"{p*100:.1f}" if 0<p*100<0.5 else f"{p*100:.0f}")}%</text>')
out.append('</svg>')
open('chart.svg','w').write('\n'.join(out))
print('chart.svg written', H)
