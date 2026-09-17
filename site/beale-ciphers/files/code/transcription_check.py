"""Task 5 - cross-check our Wikisource-derived cipher numbers against independent transcriptions:
  * Gillogly 1980, Table II (B1)                      sources/gillogly_1980_plain.txt
  * George Love's copy of B2 "from Remington"          sources/love_plain.txt
  * unmuseum.org "The Beale Papers" (Wayback capture)  sources/unmuseum_bealepap_wayback_plain.txt (B1, B2, B3)
Run from the case folder:  python3 code/transcription_check.py
"""
import os, re, json, difflib
from beale_common import *

ours = {1: load_cipher(1), 2: load_cipher(2), 3: load_cipher(3)}


def compare(name, a, b, raw_b=None):
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            diffs.append({'op': tag, 'ours_pos': i1 + 1, 'ours': a[i1:i2], 'theirs_pos': j1 + 1, 'theirs': b[j1:j2],
                          'theirs_raw': raw_b[j1:j2] if raw_b else None})
    return {'source': name, 'ours_len': len(a), 'theirs_len': len(b), 'differences': diffs}


out = []
# Gillogly Table II
g2, raw = gillogly_table2()
out.append(compare('Gillogly 1980 Table II (B1)', ours[1], g2, raw))
# Love / Remington B2
t = open(os.path.join(SOURCES, 'love_plain.txt'), encoding='utf-8').read()
i = t.index(' 115, 73, 24, 807'); j = t.index('140, 288.', i) + len('140, 288.')
block = t[i:j]
toks = re.findall(r'(\d+)(\*?)(/[\d,]+)?', block)
love = [int(a) for a, _, _ in toks]
love_raw = [a + b + (c or '') for a, b, c in toks]
out.append(compare("Love (copy of Remington) B2", ours[2], love, love_raw))
love_flags = [(k + 1, r) for k, r in enumerate(love_raw) if '*' in r or '/' in r]
# unmuseum
u = open(os.path.join(SOURCES, 'unmuseum_bealepap_wayback_plain.txt'), encoding='utf-8').read()
runs = []
for m in re.finditer(r'(?:\d+\s*,\s*){200,}\d+', u):
    runs.append([int(x) for x in re.findall(r'\d+', m.group(0))])
runs_by_first = {r[0]: r for r in runs}
for n, first in ((1, 71), (2, 115), (3, 317)):
    r = runs_by_first.get(first)
    out.append(compare('unmuseum.org bealepap.htm (Wayback) B%d' % n, ours[n], r if r else []))
json.dump({'comparisons': out, 'love_annotated_entries': love_flags}, open(os.path.join(RESULTS, 'transcription_check.json'), 'w'), indent=1)

if __name__ == '__main__':
    for c in out:
        print('%s: ours %d numbers, theirs %d numbers, %d difference blocks' % (c['source'], c['ours_len'], c['theirs_len'], len(c['differences'])))
        for d in c['differences']:
            print('    ', d)
    print('Love annotated entries (position, raw):', love_flags)
