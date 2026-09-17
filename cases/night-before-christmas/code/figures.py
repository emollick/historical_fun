"""
figures.py -- build inline SVG figures for the report from the JSON results.
All fills reference CSS custom properties (--s1.., --ink, --ink2, --grid) so the
same SVG renders in light and dark themes. Output: data/results/fig_*.svg
"""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis
OUT = analysis.OUT
MOORE, LIV = analysis.MOORE, analysis.LIV

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def strip_plot(groups, poem_marks, xlabel, title, xmin=None, xmax=None, width=760, row_h=34,
               left=180, right=30, top=54, bottom=44, ticks=None, fmt='{:+.2f}', note=None, zero_line=True):
    """groups: list of (label, values, color_var); poem_marks: list of (label, x, color_var).
    Jittered dot strips, one row per group, with the poem as a vertical marker line."""
    allv = [v for _, vals, _ in groups for v in vals] + [x for _, x, _ in poem_marks]
    lo = min(allv) if xmin is None else xmin; hi = max(allv) if xmax is None else xmax
    pad = (hi - lo) * 0.06 or 0.1; lo -= pad; hi += pad
    n = len(groups); H = top + n * row_h + bottom
    def X(v): return left + (v - lo) / (hi - lo) * (width - left - right)
    s = [f'<svg viewBox="0 0 {width} {H}" width="100%" role="img" aria-label="{esc(title)}" font-family="inherit" font-size="12">']
    s.append(f'<text x="{left}" y="18" fill="var(--ink)" font-weight="600" font-size="13">{esc(title)}</text>')
    if ticks is None:
        step = (hi - lo) / 5
        mag = 10 ** math.floor(math.log10(step)); step = round(step / mag) * mag or mag
        t0 = math.ceil(lo / step) * step
        ticks = [t0 + i * step for i in range(int((hi - t0) / step) + 1)]
    for t in ticks:
        x = X(t)
        s.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + n*row_h}" stroke="var(--grid)" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{top + n*row_h + 16}" text-anchor="middle" fill="var(--ink2)" font-size="11">{fmt.format(t)}</text>')
    if zero_line and lo < 0 < hi:
        x = X(0)
        s.append(f'<line x1="{x:.1f}" y1="{top-4}" x2="{x:.1f}" y2="{top + n*row_h}" stroke="var(--ink2)" stroke-width="1" stroke-dasharray="3 3"/>')
    rng = np.random.RandomState(7)
    for i, (label, vals, col) in enumerate(groups):
        yc = top + i * row_h + row_h / 2
        s.append(f'<text x="{left-10}" y="{yc+4:.1f}" text-anchor="end" fill="var(--ink)" font-size="12">{esc(label)}</text>')
        if i:
            s.append(f'<line x1="{left}" y1="{top + i*row_h:.1f}" x2="{width-right}" y2="{top + i*row_h:.1f}" stroke="var(--grid)" stroke-width="1"/>')
        for v in vals:
            jy = yc + rng.uniform(-row_h * 0.28, row_h * 0.28)
            s.append(f'<circle cx="{X(v):.1f}" cy="{jy:.1f}" r="4" fill="var({col})" fill-opacity="0.75" stroke="var(--surface)" stroke-width="1"/>')
        if len(vals) >= 3:
            m = float(np.mean(vals))
            s.append(f'<line x1="{X(m):.1f}" y1="{yc-11:.1f}" x2="{X(m):.1f}" y2="{yc+11:.1f}" stroke="var(--ink)" stroke-width="2"/>')
    for label, x, col in poem_marks:
        s.append(f'<line x1="{X(x):.1f}" y1="{top-6}" x2="{X(x):.1f}" y2="{top + n*row_h + 2}" stroke="var({col})" stroke-width="2.5"/>')
        s.append(f'<text x="{X(x):.1f}" y="{top-10}" text-anchor="middle" fill="var({col})" font-size="11" font-weight="600">{esc(label)}</text>')
    s.append(f'<text x="{(left + width - right)/2:.1f}" y="{H-8}" text-anchor="middle" fill="var(--ink2)" font-size="11">{esc(xlabel)}</text>')
    if note:
        s.append(f'<text x="{left}" y="{H-8}" fill="var(--ink2)" font-size="10">{esc(note)}</text>')
    s.append('</svg>')
    return '\n'.join(s)

def fig_margins(fs_list=('mfw300', 'char4', 'char3'), refs=('both', 'anapestic'), dist='cosine'):
    M = json.load(open(os.path.join(OUT, f'margins_{dist}.json')))
    figs = {}
    for fs in fs_list:
        for ref in refs:
            key = f'{fs}|{ref}'
            if key not in M: continue
            recs = M[key]['records']; pm = M[key]['poem_margin']
            def vals(a, f=None):
                return [r['margin'] for r in recs if r['author'] == a and (f is None or r['form'] == f)]
            groups = [('Moore, other metres', vals(MOORE, 'other'), '--s1'),
                      ('Moore, anapestic', vals(MOORE, 'anapestic'), '--s1'),
                      ('Livingston, anapestic', vals(LIV, 'anapestic'), '--s2'),
                      ('Livingston, other metres', vals(LIV, 'other'), '--s2')]
            title = {'both': 'Reference: all verse of both men', 'anapestic': 'Reference: anapestic verse of both men only',
                     'both_neutral': 'Reference: all verse, metre-driven features removed'}[ref]
            name = {'mfw300': '300 most frequent words', 'mfw200': '200 most frequent words', 'mfw100': '100 most frequent words',
                    'char4': 'character 4-grams', 'char3': 'character 3-grams', 'phone': 'phoneme frequencies'}[fs]
            svg = strip_plot(groups, [('the poem (1823 text)', pm['1823'], '--s3')],
                             'distance to Livingston minus distance to Moore (positive = nearer Moore)',
                             f'{name}. {title}', fmt='{:+.2f}')
            figs[f'fig_margins_{fs}_{ref}'] = svg
    return figs

def fig_gi():
    G = json.load(open(os.path.join(OUT, 'gi_calibration.json')))
    A = json.load(open(os.path.join(OUT, 'attribute_1823.json')))
    figs = {}
    for fs, recs in G.items():
        groups = []
        for cand, lab in ((MOORE, 'Moore'), (LIV, 'Livingston')):
            t = [r['score'] for r in recs if r['candidate'] == cand and r['true']]
            f = [r['score'] for r in recs if r['candidate'] == cand and not r['true']]
            groups.append((f'candidate {lab}: samples truly by {lab}', t, '--s1' if cand == MOORE else '--s2'))
            groups.append((f'candidate {lab}: samples by the other man', f, '--s1' if cand == MOORE else '--s2'))
        pm = [('poem vs Moore', A[fs]['gi_moore_vs_controls+liv'], '--s1'), ('poem vs Livingston', A[fs]['gi_liv_vs_controls+moore'], '--s2')]
        name = {'mfw200': '200 most frequent words', 'char4': 'character 4-grams'}.get(fs, fs)
        figs[f'fig_gi_{fs}'] = strip_plot(groups, pm, 'General Impostors score (share of trials in which the candidate beat every impostor)',
                                          f'Impostors method, {name}', xmin=0, xmax=1, fmt='{:.1f}', zero_line=False, left=300, width=860)
    return figs

def fig_metre_shift():
    J = json.load(open(os.path.join(OUT, 'metre_shift.json')))
    rows = J['phone_rows'] if 'phone_rows' in J else None
    return {}

def fig_validation_table():
    V = json.load(open(os.path.join(OUT, 'validate.json')))
    return V

if __name__ == '__main__':
    figs = {}
    try: figs.update(fig_margins())
    except Exception as e: print('margins figure skipped:', e)
    try: figs.update(fig_gi())
    except Exception as e: print('gi figure skipped:', e)
    for k, v in figs.items():
        open(os.path.join(OUT, k + '.svg'), 'w').write(v)
    print('wrote', list(figs))
