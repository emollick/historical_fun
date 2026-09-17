#!/usr/bin/env python3
"""SVG figures for the report, generated from data/results/final_tables.json (no external libraries)."""
import json, os
T = json.load(open('data/results/final_tables.json'))
SC = ['1.1','1.2','1.3','2.1','2.2','2.3','2.4','3.1','3.2','3.3','4.1','4.2','5.1','5.2']
FL, SH, R18, THEO, OTH, INK, INK2, RULE = '#eb6834', '#2a78d6', '#8a8f9a', '#1baf7a', '#c9a227', '#15171c', '#555a66', '#d3d7de'
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
def text(x, y, s, size=12, anchor='start', fill=INK, weight='normal', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" {extra}>{esc(s)}</text>'

def fig_survival():
    W, H = 900, 380; L, R_, T_, B = 70, 300, 30, 60
    pw = W - L - R_; ph = H - T_ - B
    bins = T['survival_svm3']; gi = T['survival_gi']; gio = T['survival_gi_other']
    labels = ['0 to 5%', '5 to 15%', '15 to 30%', '30 to 50%', '50 to 70%', '70 to 100%']
    def X(i): return L + pw * (i + 0.5) / 6
    def Y(v): return T_ + ph * (1 - v)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Survival of the original author signal in adaptations by share of wording retained">']
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        out.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{L+pw}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        out.append(text(L - 8, Y(v) + 4, f'{v:.1f}', 11, 'end', INK2))
    for i, lab in enumerate(labels):
        out.append(text(X(i), H - B + 18, lab, 11.5, 'middle', INK2))
        out.append(text(X(i), H - B + 34, f'n={bins[i]["n"]}', 10.5, 'middle', INK2))
    out.append(text(L + pw / 2, H - 8, 'share of the adaptation\'s word 4-grams found in the original play (scenes of 39 adaptations, 1661 to 1772)', 12, 'middle', INK2))
    out.append(text(16, T_ + ph / 2, 'score for the original author', 12, 'middle', INK2, extra=f'transform="rotate(-90 16 {T_ + ph / 2:.0f})"'))
    for series, col, name, dash in ((bins, SH, 'SVM probability of the original author (3 classes)', ''), (gi, FL, 'impostors score GI for the original author', ''), (gio, OTH, 'GI for the wrong Jacobean author', '6,4')):
        pts = ' '.join(f'{X(i):.1f},{Y(b["mean"]):.1f}' for i, b in enumerate(series))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
        for i, b in enumerate(series):
            out.append(f'<circle cx="{X(i):.1f}" cy="{Y(b["mean"]):.1f}" r="4" fill="{col}"/>')
            dy = -9 if col != SH else (14 if abs(b['mean'] - gi[i]['mean']) < 0.06 else -9)
            out.append(text(X(i), Y(b['mean']) + dy, f'{b["mean"]:.2f}', 10.5, 'middle', col))
    # DF reference marks on the right
    xr = L + pw + 24
    out.append(text(xr, T_ + 6, 'Double Falsehood', 12, 'start', INK, 'bold'))
    marks = [('3.3', T['scenes']['3.3']['c3']['svm']['FL'], T['scenes']['3.3']['gi3']['FL'], 'Fletcher'), ('4.1', T['scenes']['4.1']['c3']['svm']['FL'], T['scenes']['4.1']['gi3']['FL'], 'Fletcher'),
             ('5.2', T['scenes']['5.2']['c3']['svm']['FL'], T['scenes']['5.2']['gi3']['FL'], 'Fletcher'), ('1.2', T['scenes']['1.2']['c3']['svm']['SH'], T['scenes']['1.2']['gi3']['SH'], 'Shakespeare'),
             ('3.2', T['scenes']['3.2']['c3']['svm']['SH'], T['scenes']['3.2']['gi3']['SH'], 'Shakespeare'), ('2.3', T['scenes']['2.3']['c3']['svm']['SH'], T['scenes']['2.3']['gi3']['SH'], 'Shakespeare')]
    out.append(text(xr, T_ + 22, 'scene: SVM / GI for the named author', 10.5, 'start', INK2))
    for j, (s, p, g, who) in enumerate(marks):
        y = T_ + 44 + j * 20
        col = FL if who == 'Fletcher' else SH
        out.append(f'<rect x="{xr}" y="{y-9}" width="10" height="10" fill="{col}"/>')
        out.append(text(xr + 16, y, f'{s} ({who}): {p:.2f} / {g:.2f}', 11.5, 'start', INK))
    for j, (col, name, dash) in enumerate(((SH, 'SVM P(original author)', ''), (FL, 'GI(original author)', ''), (OTH, 'GI(wrong author)', '6,4'))):
        y = T_ + 190 + j * 18
        out.append(f'<line x1="{xr}" y1="{y-4}" x2="{xr+26}" y2="{y-4}" stroke="{col}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
        out.append(text(xr + 32, y, name, 11.5, 'start', INK2))
    out.append('</svg>'); return '\n'.join(out)

def fig_scenes():
    W = 900; rowh = 24; L = 60; T_ = 46; bw = 300; gap = 30
    H = T_ + rowh * len(SC) + 66
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Scene by scene attribution of Double Falsehood">']
    out.append(text(L, 16, 'four-class SVM probability', 11.5, 'start', INK2))
    x2 = L + bw + gap
    out.append(text(x2, 16, 'impostors score', 11.5, 'start', INK2))
    x3 = x2 + 200 + gap
    out.append(text(x3, 16, 'Fletcher-only phrases per 1000 words', 11.5, 'start', INK2))
    for k, v in ((0, 0), (0.5, 0.5), (1, 1)):
        out.append(text(L + bw * k, 34, f'{k:.1f}', 10, 'middle', INK2))
        out.append(text(x2 + 200 * k, 34, f'{k:.1f}', 10, 'middle', INK2))
    for k in (0, 5, 10, 15, 20, 25):
        out.append(text(x3 + 200 * k / 26, 34, str(k), 10, 'middle', INK2))
    for i, s in enumerate(SC):
        y = T_ + i * rowh; d = T['scenes'][s]
        out.append(text(L - 8, y + 15, s, 12, 'end', INK, 'bold'))
        p = d['c4']['svm']; x = L
        for cls, col in (('FL', FL), ('SH', SH), ('THEO', THEO), ('R18', R18)):
            w = bw * p.get(cls, 0)
            out.append(f'<rect x="{x:.1f}" y="{y+3}" width="{w:.1f}" height="{rowh-7}" fill="{col}"/>'); x += w
        g = d['gi3']
        out.append(f'<line x1="{x2}" y1="{y+rowh/2:.1f}" x2="{x2+200}" y2="{y+rowh/2:.1f}" stroke="{RULE}"/>')
        out.append(f'<line x1="{x2+160}" y1="{y+3}" x2="{x2+160}" y2="{y+rowh-4}" stroke="{RULE}" stroke-dasharray="2,3"/>')
        out.append(f'<circle cx="{x2+200*g["FL"]:.1f}" cy="{y+rowh/2:.1f}" r="5" fill="{FL}"/>')
        out.append(f'<circle cx="{x2+200*g["SH"]:.1f}" cy="{y+rowh/2:.1f}" r="5" fill="{SH}"/>')
        l3 = d['links3']['Fletcher']
        out.append(f'<rect x="{x3}" y="{y+5}" width="{200*min(l3,26)/26:.1f}" height="{rowh-11}" fill="{FL}" opacity="0.85"/>')
        out.append(text(x3 + 200 * min(l3, 26) / 26 + 5, y + 16, f'{l3:.1f}', 10.5, 'start', INK2))
    # calibration bands for links
    for val, lab, col in ((T['links3_groups']['FL scenes H8/TNK']['FL_median'], 'Fletcher scenes of H8 and TNK', FL), (T['links3_groups']['SH scenes H8/TNK']['FL_median'], 'Shakespeare scenes', SH), (T['links3_groups']['18C plays']['FL_median'], '18th-century plays', R18)):
        xx = x3 + 200 * val / 26
        out.append(f'<line x1="{xx:.1f}" y1="{T_-4}" x2="{xx:.1f}" y2="{T_+rowh*len(SC)}" stroke="{col}" stroke-width="1.5" stroke-dasharray="4,3"/>')
    yk = T_ + rowh * len(SC) + 14
    out.append(text(L, yk, 'Bars: Fletcher (orange), Shakespeare (blue), Theobald (green), 18th-century (grey). Dots: impostors score for Fletcher (orange) and Shakespeare (blue); dotted line: 0.8 threshold.', 10.5, 'start', INK2))
    out.append(text(L, yk + 15, 'Right panel dashed lines: median of Fletcher scenes in Henry VIII and TNK (orange), of Shakespeare scenes (blue) and of 18th-century plays (grey).', 10.5, 'start', INK2))
    out.append('</svg>'); return '\n'.join(out)

def fig_validation():
    v = T['h8tnk_c3']['scenes']; keys = sorted(v, key=lambda k: (k.split('|')[0], [int(x) for x in k.split('|')[1].split('.')]))
    W = 900; cw = 17; L = 90; T_ = 40; H = 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Validation on Henry VIII and The Two Noble Kinsmen">']
    out.append(text(L, 14, 'Henry VIII (left) and The Two Noble Kinsmen (right): accepted hand above, model verdict below (SVM, Shakespeare / Fletcher / 18th-century)', 11.5, 'start', INK2))
    out.append(text(L - 8, T_ + 14, 'accepted', 11, 'end', INK2)); out.append(text(L - 8, T_ + 40, 'model', 11, 'end', INK2))
    x = L
    for k in keys:
        play, s = k.split('|'); r = v[k]
        col_t = SH if r['truth'] == 'SH' else FL; col_p = {'SH': SH, 'FL': FL}.get(r['svm'], R18)
        out.append(f'<rect x="{x}" y="{T_}" width="{cw-2}" height="20" fill="{col_t}"/>')
        out.append(f'<rect x="{x}" y="{T_+26}" width="{cw-2}" height="20" fill="{col_p}" opacity="{0.4 + 0.6 * r["p_truth"] if r["svm"] == r["truth"] else 1:.2f}"/>')
        out.append(text(x + cw / 2 - 1, T_ + 62, s, 8.5, 'middle', INK2, extra=f'transform="rotate(-60 {x + cw/2 - 1:.0f} {T_ + 62})"'))
        x += cw
        if play == 'henry8' and k == keys[16]: x += 18
    n = T['h8tnk_c3']; out.append(text(L, H - 10, f'{n["svm_correct"]} of {n["n"]} scenes agree with the accepted division (opacity of the lower row shows the model\'s probability for the accepted hand; disagreements are drawn solid).', 10.5, 'start', INK2))
    out.append('</svg>'); return '\n'.join(out)

def fig_links_groups():
    import statistics
    G = dict(T['links3_groups'])
    early = [T['scenes'][s]['links3'] for s in SC[:9]]; late = [T['scenes'][s]['links3'] for s in SC[9:]]
    G['DF early'] = {'n': 9, 'FL_median': statistics.median(x['Fletcher'] for x in early), 'SH_median': statistics.median(x['Shakespeare'] for x in early)}
    G['DF late'] = {'n': 5, 'FL_median': statistics.median(x['Fletcher'] for x in late), 'SH_median': statistics.median(x['Shakespeare'] for x in late)}
    order = ['FL scenes H8/TNK', 'SH scenes H8/TNK', 'Other Jacobean (Massinger, Shirley, Ford, Webster, Middleton)', '18C plays', 'Theobald plays and poem', 'DF early', 'DF late']
    names = {'FL scenes H8/TNK': 'Fletcher scenes, Henry VIII and TNK', 'SH scenes H8/TNK': 'Shakespeare scenes, Henry VIII and TNK', 'Other Jacobean (Massinger, Shirley, Ford, Webster, Middleton)': 'Massinger, Shirley, Ford, Webster, Middleton', '18C plays': '18th-century plays (Rowe, Hill, Thomson, Savage, Dennis)', 'Theobald plays and poem': "Theobald's own plays and poem (OCR)", 'DF early': 'Double Falsehood 1.1 to 3.2', 'DF late': 'Double Falsehood 3.3 to 5.2'}
    W = 900; L = 330; T_ = 40; rowh = 26; H = T_ + rowh * len(order) + 58; bw = 240
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Density of phrases unique to Fletcher and to Shakespeare by group">']
    out.append(text(L, 16, 'phrases unique to Fletcher (orange) and to Shakespeare (blue), median per 1000 words of scene', 11.5, 'start', INK2))
    for k in (0, 5, 10, 15): out.append(text(L + bw * k / 16, 30, str(k), 10, 'middle', INK2)); out.append(text(L + bw + 30 + bw * k / 16, 30, str(k), 10, 'middle', INK2))
    for i, g in enumerate(order):
        y = T_ + i * rowh; d = G[g]
        out.append(text(L - 8, y + 16, names[g] + f' (n={d["n"]})', 11.5, 'end', INK))
        out.append(f'<rect x="{L}" y="{y+4}" width="{bw*min(d["FL_median"],16)/16:.1f}" height="{rowh-9}" fill="{FL}"/>')
        out.append(text(L + bw * min(d['FL_median'], 16) / 16 + 4, y + 16, f'{d["FL_median"]:.1f}', 10.5, 'start', INK2))
        x2 = L + bw + 30
        out.append(f'<rect x="{x2}" y="{y+4}" width="{bw*min(d["SH_median"],16)/16:.1f}" height="{rowh-9}" fill="{SH}"/>')
        out.append(text(x2 + bw * min(d['SH_median'], 16) / 16 + 4, y + 16, f'{d["SH_median"]:.1f}', 10.5, 'start', INK2))
    out.append(text(30, H - 26, 'Word 3-grams found in exactly one author\'s corpus, per 1000 words of scene; each adaptation\'s original play is excluded from the index.', 10.5, 'start', INK2))
    out.append(text(30, H - 11, 'Fletcher-only phrases separate his scenes from everyone else\'s. Shakespeare-only phrases do not separate his scenes from other Jacobean writing.', 10.5, 'start', INK2))
    out.append('</svg>'); return '\n'.join(out)

figs = {'fig_survival.svg': fig_survival(), 'fig_scenes.svg': fig_scenes(), 'fig_validation.svg': fig_validation(), 'fig_links_groups.svg': fig_links_groups()}
for k, v in figs.items():
    open(os.path.join('figures', k), 'w').write(v); print('wrote', k, len(v))
