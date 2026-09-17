"""Draw the two figures for the Bixby letter report from the saved n-gram tracing results.

Usage: python3 make_figures.py <results_dir> <out_dir>
Writes figure1.svg, figure2.svg (standalone, light colours), figure1_inline.svg, figure2_inline.svg
(for the report page, colours from the page's CSS variables) and figure1_data.csv, figure2_data.csv.
"""
import json, sys, os, csv

RES, OUT = sys.argv[1], sys.argv[2]
TYPES = ['w1', 'w2', 'w3'] + [f'c{i}' for i in range(3, 17)]
XLAB = ['1', '2', '3'] + [str(i) for i in range(3, 17)]

def load(p):
    return json.load(open(os.path.join(RES, p)))

def acc(counts, truth):
    tot = sum(counts.values()); return counts.get(truth, 0) / tot

# ---- data ----
letter = {}
for name, p in [('paper', 'grieve_specials_50/results.json'), ('ownhand', 'ownhand_specials_50/results.json')]:
    b = load(p)['tests']['specials']['bixby']['ngrams']
    letter[name] = [b[t]['lincoln'] - b[t]['hay'] for t in TYPES]
accs = {}
for name, d in [('paper', 'grieve'), ('ownhand', 'ownhand')]:
    reg = load(f'{d}_register/summary.json')['register']
    accs[(name, 'lincoln_pieces')] = [acc(reg[t]['lincoln'], 'lincoln') for t in TYPES]
    accs[(name, 'hay_pieces')] = [acc(reg[t]['hay'], 'hay') for t in TYPES]
g = load('grieve/summary.json'); o = load('ownhand/summary.json')
accs[('paper', 'lincoln_ordinary')] = [acc(g['loo_lincoln_pre1860'][t]['lincoln'], 'lincoln') for t in TYPES]
accs[('ownhand', 'lincoln_ordinary')] = [acc(o['loo_lincoln_war_own'][t]['lincoln'], 'lincoln') for t in TYPES]

with open(os.path.join(OUT, 'figure1_data.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['ngram', 'margin_paper_design', 'margin_ownhand_design'])
    for i, t in enumerate(TYPES): w.writerow([t, f'{letter["paper"][i]:.4f}', f'{letter["ownhand"][i]:.4f}'])
with open(os.path.join(OUT, 'figure2_data.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['ngram', 'paper_lincoln_ordinary', 'paper_lincoln_pieces', 'paper_hay_pieces', 'ownhand_lincoln_ordinary', 'ownhand_lincoln_pieces', 'ownhand_hay_pieces'])
    for i, t in enumerate(TYPES):
        w.writerow([t] + [f'{accs[(d, s)][i]:.3f}' for d in ('paper', 'ownhand') for s in ('lincoln_ordinary', 'lincoln_pieces', 'hay_pieces')])

# ---- colours ----
LIGHT = dict(ink='#1C1B18', ink2='#5A574E', rule='#C9C6B9', paper='#EFEEE7', paper2='#E5E3D9', accentsoft='#E9DCA8',
             blue='#2a78d6', orange='#eb6834', violet='#4a3aa7', gray='#898781')
DARK = dict(blue='#3987e5', orange='#d95926', violet='#9085e9')
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'

def style(inline):
    if inline:
        base = (".bx .ink{fill:var(--ink)} .bx .ink2{fill:var(--ink-2)} .bx .rule{stroke:var(--rule)} .bx .axis{stroke:var(--ink-2)} "
                ".bx .ring{stroke:var(--paper-2)} .bx .band{fill:var(--accent-soft);opacity:.55} "
                f".bx .blue{{stroke:{LIGHT['blue']}}} .bx .bluef{{fill:{LIGHT['blue']}}} .bx .orange{{stroke:{LIGHT['orange']}}} .bx .orangef{{fill:{LIGHT['orange']}}} "
                f".bx .violet{{stroke:{LIGHT['violet']}}} .bx .violetf{{fill:{LIGHT['violet']}}} .bx .gray{{stroke:{LIGHT['gray']}}} .bx .grayf{{fill:{LIGHT['gray']}}} ")
        dark = (f".bx .blue{{stroke:{DARK['blue']}}} .bx .bluef{{fill:{DARK['blue']}}} .bx .orange{{stroke:{DARK['orange']}}} .bx .orangef{{fill:{DARK['orange']}}} "
                f".bx .violet{{stroke:{DARK['violet']}}} .bx .violetf{{fill:{DARK['violet']}}} ")
        # every dark rule carries its own guard, so a forced light theme keeps the light colours
        rules = [r.strip() for r in dark.split('} ') if r.strip()]
        media = "@media (prefers-color-scheme: dark){" + " ".join(':root:not([data-theme="light"]) ' + r + "}" for r in rules) + "} "
        forced = " ".join(':root[data-theme="dark"] ' + r + "}" for r in rules) + " "
        return "<style>" + base + media + forced + "</style>"
    c = LIGHT
    return ("<style>" + f".bx .ink{{fill:{c['ink']}}} .bx .ink2{{fill:{c['ink2']}}} .bx .rule{{stroke:{c['rule']}}} .bx .axis{{stroke:{c['ink2']}}} "
            f".bx .ring{{stroke:{c['paper2']}}} .bx .band{{fill:{c['accentsoft']};opacity:.55}} "
            f".bx .blue{{stroke:{c['blue']}}} .bx .bluef{{fill:{c['blue']}}} .bx .orange{{stroke:{c['orange']}}} .bx .orangef{{fill:{c['orange']}}} "
            f".bx .violet{{stroke:{c['violet']}}} .bx .violetf{{fill:{c['violet']}}} .bx .gray{{stroke:{c['gray']}}} .bx .grayf{{fill:{c['gray']}}} " + "</style>")

def text(x, y, s, cls='ink2', size=12, anchor='start', weight='normal', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>'

def polyline(pts, cls):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" class="{cls}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'

def dots(pts, cls):
    return ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="{cls} ring" stroke-width="2"/>' for x, y in pts)

def xaxis(x0, step, ybase, gap_after_words):
    out = []
    for i, lab in enumerate(XLAB):
        x = x0 + i * step + (gap_after_words if i >= 3 else 0)
        out.append(text(x, ybase + 16, lab, 'ink2', 11, 'middle'))
    wx = x0 + step  # centre of the three word positions
    out.append(text(wx, ybase + 32, 'words', 'ink2', 11, 'middle'))
    cx = x0 + 3 * step + gap_after_words + 6.5 * step
    out.append(text(cx, ybase + 32, 'characters', 'ink2', 11, 'middle'))
    return ''.join(out)

def xpos(i, x0, step, gap):
    return x0 + i * step + (gap if i >= 3 else 0)

# ---- figure 1: the letter's margins ----
def figure1(inline):
    W, H = 720, 380
    L, R, T, B = 56, 150, 30, 56
    x0 = L + 8; gap = 14; step = (W - L - R - 16 - gap) / 16
    ymin, ymax = -0.15, 0.05
    def Y(v): return T + (ymax - v) / (ymax - ymin) * (H - T - B)
    size = 'style="width:100%;height:auto"' if inline else f'width="{W}" height="{H}"'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" {size} class="bx" role="img" aria-label="Dot plot of the letter\'s n-gram tracing margins at seventeen string lengths under two designs" font-family=\'{FONT}\'>', style(inline)]
    if not inline: s.append(f'<rect width="{W}" height="{H}" fill="{LIGHT["paper2"]}"/>')
    for v in [-0.15, -0.10, -0.05, 0.0, 0.05]:
        y = Y(v); cls = 'axis' if abs(v) < 1e-9 else 'rule'
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W - R + 8}" y2="{y:.1f}" class="{cls}" stroke-width="1"/>')
        s.append(text(L - 8, y + 4, ('+' if v > 0 else '') + f'{v:.2f}'.replace('-', '−'), 'ink2', 11, 'end'))
    s.append(text(L - 8, T - 12, 'Lincoln’s share minus Hay’s', 'ink2', 11, 'start'))
    s.append(text(W - R + 8, Y(0.05) + 14, 'above the line: the letter looks more like Lincoln', 'ink2', 11, 'end', extra='font-style="italic"'))
    s.append(text(W - R + 8, Y(-0.15) - 6, 'below the line: the letter looks more like Hay', 'ink2', 11, 'end', extra='font-style="italic"'))
    series = [('paper', 'gray', 'grayf', 'Paper’s design: all 17 to Hay'), ('ownhand', 'violet', 'violetf', 'Own-hand design: 8 to Hay, 9 to Lincoln')]
    for name, lc, fc, label in series:
        pts = [(xpos(i, x0, step, gap), Y(v)) for i, v in enumerate(letter[name])]
        s.append(polyline(pts[:3], lc)); s.append(polyline(pts[3:], lc)); s.append(dots(pts, fc))
    # legend (top right, inside the plot's top band)
    lx = L + 8; ly = T + 6
    for k, (name, lc, fc, label) in enumerate(series):
        yy = ly + k * 18
        s.append(f'<line x1="{lx}" y1="{yy}" x2="{lx + 18}" y2="{yy}" class="{lc}" stroke-width="2"/><circle cx="{lx + 9}" cy="{yy}" r="4" class="{fc} ring" stroke-width="2"/>')
        s.append(text(lx + 26, yy + 4, label, 'ink', 12))
    s.append(xaxis(x0, step, H - B + 4, gap))
    s.append(text(W - R + 8, H - 6, 'string length (n-grams of words, then of characters)', 'ink2', 11, 'end'))
    s.append('</svg>')
    return ''.join(s)

# ---- figure 2: accuracy by string length, two panels ----
def figure2(inline):
    W, H = 720, 416
    T, B = 80, 56
    PL, PW, GAP = 46, 316, 30
    ymin, ymax = 0, 1
    def Y(v): return T + (ymax - v) / (ymax - ymin) * (H - T - B)
    size = 'style="width:100%;height:auto"' if inline else f'width="{W}" height="{H}"'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" {size} class="bx" role="img" aria-label="Two line charts of attribution accuracy by string length under the paper\'s design and the own-hand design" font-family=\'{FONT}\'>', style(inline)]
    if not inline: s.append(f'<rect width="{W}" height="{H}" fill="{LIGHT["paper2"]}"/>')
    series = [('lincoln_ordinary', 'gray', 'grayf', 'Lincoln, ordinary known texts (each tested with itself left out of the pool)'),
              ('lincoln_pieces', 'blue', 'bluef', 'Lincoln, elevated wartime pieces (63)'),
              ('hay_pieces', 'orange', 'orangef', 'Hay, elevated pieces (57)')]
    # legend row at top
    for k, ((key, lc, fc, label), (lx, ly)) in enumerate(zip(series, [(PL, 16), (PL, 36), (PL + 340, 36)])):
        s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 18}" y2="{ly}" class="{lc}" stroke-width="2"/><circle cx="{lx + 9}" cy="{ly}" r="4" class="{fc} ring" stroke-width="2"/>')
        s.append(text(lx + 26, ly + 4, label, 'ink', 12))
    for p, (name, title) in enumerate([('paper', 'Paper’s design'), ('ownhand', 'Own-hand design')]):
        px = PL + p * (PW + GAP)
        x0 = px + 10; gap = 10; step = (PW - 20 - gap) / 16
        s.append(text(px, T - 14, title, 'ink', 12, 'start', 'bold'))
        # band for the majority-vote lengths c4..c10 (indices 4..10)
        bx1 = xpos(4, x0, step, gap) - step / 2; bx2 = xpos(10, x0, step, gap) + step / 2
        s.append(f'<rect x="{bx1:.1f}" y="{T}" width="{bx2 - bx1:.1f}" height="{H - T - B}" class="band"/>')
        for v in [0, 0.25, 0.5, 0.75, 1.0]:
            y = Y(v)
            s.append(f'<line x1="{px}" y1="{y:.1f}" x2="{px + PW}" y2="{y:.1f}" class="{"axis" if v == 0 else "rule"}" stroke-width="1"/>')
            if p == 0: s.append(text(px - 6, y + 4, f'{int(v * 100)}%', 'ink2', 11, 'end'))
        s.append(text((bx1 + bx2) / 2, Y(0.035), 'lengths that decide the majority vote', 'ink2', 10, 'middle', extra='font-style="italic"'))
        for key, lc, fc, label in series:
            vals = accs[(name, key)]
            pts = [(xpos(i, x0, step, gap), Y(v)) for i, v in enumerate(vals)]
            s.append(polyline(pts[:3], lc)); s.append(polyline(pts[3:], lc)); s.append(dots(pts, fc))
        # direct label: the low point of the Lincoln elevated line among character lengths
        vals = accs[(name, 'lincoln_pieces')]
        i_min = min(range(3, len(TYPES)), key=lambda i: vals[i])
        x, y = xpos(i_min, x0, step, gap), Y(vals[i_min])
        s.append(text(x, y + 20, f'{round(vals[i_min] * 100)}% right', 'ink', 11, 'middle', 'bold'))
        # x axis
        s.append(xaxis(x0, step, H - B + 4, gap))
    s.append(text(W - 8, H - 6, 'string length', 'ink2', 11, 'end'))
    s.append('</svg>')
    return ''.join(s)

for n, fn in [(1, figure1), (2, figure2)]:
    open(os.path.join(OUT, f'figure{n}.svg'), 'w', encoding='utf-8').write(fn(False))
    open(os.path.join(OUT, f'figure{n}_inline.svg'), 'w', encoding='utf-8').write(fn(True))
print('written to', OUT)
