"""Assemble report.html from report_src.html: inline the SVG figures (metadata
stripped) and fill numeric placeholders from the saved results."""
import re, json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
RES = os.path.join(ROOT, 'data/results')
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'report_src.html'), encoding='utf-8').read()

def svg(name):
    s = open(os.path.join(RES, name + '.svg'), encoding='utf-8').read()
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    s = re.sub(r'\s+xmlns:c2pa="[^"]*"', '', s)
    return s

def fig_repl(m):
    return svg(m.group(1))
out = re.sub(r'<!--FIG:([a-z0-9_]+)-->', fig_repl, src)

# numbers
J = json.load(open(os.path.join(RES, 'metre_shift.json')))
R = json.load(open(os.path.join(RES, 'rhymes.json')))
def fmt_matches(m):
    if isinstance(m, dict):
        return ', '.join(f"{k}" + (f" (×{v})" if v > 1 else '') for k, v in m.items())
    return ', '.join(m)
nums = {
    'phone_shift': f"{J.get('phone_mean_shift', float('nan')):.1f}",
    'phone_shift_n': str(len(J.get('phone_rows', []))),
    'phone_shift_pos': str(sum(1 for r in J.get('phone_rows', []) if r[2] > r[4])),
    'word_shift': f"{J.get('word_mean_shift', float('nan')):+.1f}",
    'rhymes_moore': fmt_matches(R['moore']['matches']),
    'rhymes_liv': fmt_matches(R['livingston']['matches']),
}
def num_repl(m):
    k = m.group(1)
    if k not in nums:
        print('missing number', k); return m.group(0)
    return nums[k]
out = re.sub(r'<!--NUM:([a-z_]+)-->', num_repl, out)
left = re.findall(r'<!--(FIG|NUM):[^>]*-->', out)
if left: print('unfilled placeholders:', left)
open(os.path.join(HERE, 'report.html'), 'w', encoding='utf-8').write(out)
print('wrote report.html', len(out), 'bytes')
