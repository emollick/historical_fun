#!/usr/bin/env python3
"""Orthographic and compounding conventions that shifted between the 1820s and the 1880s,
counted in the Beale letters, the anonymous narrative, Morriss's statement and the control
samples (early = printed 1810-1846 from 1805-1843 writing; late = 1858-1904).
Caveat: the Beale letters exist only as printed in 1885; the compositor may have modernised."""
import os, re, csv, collections
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(B, 'data', 'controls', 'samples'); R = os.path.join(B, 'results')
man = list(csv.DictReader(open(os.path.join(B, 'data', 'controls', 'manifest.csv'))))
PAIRS = [  # (label, early-favoured regex, late-favoured regex)
    ('every thing / everything', r'\bevery thing\b', r'\beverything\b'),
    ('any thing / anything', r'\bany thing\b', r'\banything\b'),
    ('some thing / something', r'\bsome thing\b', r'\bsomething\b'),
    ('every one / everyone', r'\bevery one\b', r'\beveryone\b'),
    ('any one / anyone', r'\bany one\b', r'\banyone\b'),
    ('some one / someone', r'\bsome one\b', r'\bsomeone\b'),
    ('in the mean time / meantime', r'\bmean time\b', r'\bmeantime\b'),
    ('&c. / etc.', r'&c', r'\betc\b'),
    ('-our / -or (honour, favour, labour...)', r'\b(?:hon|fav|lab|col|vig|neighb|behavi|endeav|ard|rig|hum|od)ou(?:r|rs|red|rable|rably|ring|rite|rers?)\b', r'\b(?:hon|fav|lab|col|vig|neighb|behavi|endeav|ard|rig|hum|od)o(?:r|rs|red|rable|rably|ring|rite|rers?)\b'),
    ('enquir- / inquir-', r'\benquir', r'\binquir'),
    ('-ence / -ense (pretence, defence, offence)', r'\b(?:pret|def|off)ence', r'\b(?:pret|def|off)ense'),
    ('shew / show', r'\bshew', r'\bshow'),
    ('connexion / connection', r'\bconnexion', r'\bconnection'),
    ('untill / until', r'\buntill\b', r'\buntil\b'),
]
def count(txt, rx): return len(re.findall(rx, txt, flags=re.I))
groups = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
words = collections.Counter()
texts = {}
for m in man:
    txt = open(os.path.join(S, m['sample']), encoding='utf-8').read()
    key = m['sample'][:-4]
    if m['group'] == 'beale':
        if key in ('beale_letters', 'narrative', 'morriss'): g = key
        else: continue
    else: g = m['group']
    words[g] += len(txt.split())
    for lab, e, l in PAIRS:
        groups[g][lab][0] += count(txt, e); groups[g][lab][1] += count(txt, l)
rows = ['# Orthographic / compounding conventions (early-favoured : late-favoured counts)\n',
        '| convention | Beale letters | narrative (1885) | Morriss stmt | early controls (1805-46) | late controls (1858-1904) |', '|---|---|---|---|---|---|']
out = []
for lab, e, l in PAIRS:
    cells = []
    for g in ('beale_letters', 'narrative', 'morriss', 'early', 'late'):
        a, b = groups[g][lab]; cells.append(f'{a} : {b}')
        out.append(dict(convention=lab, group=g, early_form=a, late_form=b, words=words[g]))
    rows.append(f'| {lab} | ' + ' | '.join(cells) + ' |')
rows.append(f'\nWords: letters {words["beale_letters"]}, narrative {words["narrative"]}, Morriss {words["morriss"]}, early controls {words["early"]}, late controls {words["late"]}.')
# per-author early controls for the two most telling conventions
rows.append('\nPer early-control author, "every thing : everything" and "-our : -or" (to see whether original editions kept the old forms):\n')
per = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
for m in man:
    if m['group'] != 'early': continue
    txt = open(os.path.join(S, m['sample']), encoding='utf-8').read()
    for lab, e, l in PAIRS[:1] + PAIRS[8:9] + PAIRS[7:8]:
        per[m['author_key']][lab][0] += count(txt, e); per[m['author_key']][lab][1] += count(txt, l)
rows.append('| author | every thing : everything | -our : -or | &c. : etc. |\n|---|---|---|---|')
for a, d in per.items():
    rows.append(f"| {a} | {d[PAIRS[0][0]][0]} : {d[PAIRS[0][0]][1]} | {d[PAIRS[8][0]][0]} : {d[PAIRS[8][0]][1]} | {d[PAIRS[7][0]][0]} : {d[PAIRS[7][0]][1]} |")
open(os.path.join(R, 'lang_spelling_conventions.md'), 'w').write('\n'.join(rows) + '\n')
with open(os.path.join(R, 'lang_spelling_conventions.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('\n'.join(rows))
