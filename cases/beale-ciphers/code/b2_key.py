"""Task 1 - key reconstruction.

Builds (a) a straight consecutive count of the DOI words as printed in the 1885 pamphlet,
(b) the pamphlet's own printed numbering (from the parenthetical numbers), (c) the NARA
transcript count, and (d) Gillogly's Table I; writes CSV key tables to results/ and lists
every disagreement between them and every wording difference pamphlet vs NARA.

Run from the case folder:  python3 code/b2_key.py
"""
import os, json, difflib
from collections import OrderedDict
from beale_common import *

os.makedirs(RESULTS, exist_ok=True)

toks = parse_pamphlet_doi(split_hyphens=True)
toks_j = parse_pamphlet_doi(split_hyphens=False)
straight = straight_numbering(toks)
straight_j = straight_numbering(toks_j)
fw, bw, anomalies, last_marker = pamphlet_numbering(toks)
nara, _ = nara_tokens(split_hyphens=True)
gill = gillogly_table1()

# ---------- (a) straight count
rows = []
for n in range(1, max(len(straight), len(straight_j)) + 1):
    w = straight.get(n, ''); wj = straight_j.get(n, '')
    rows.append([n, w, initial(w) if w else '', wj, initial(wj) if wj else ''])
write_csv(os.path.join(RESULTS, 'key_straight_pamphlet_text.csv'), rows,
          ['n', 'word_hyphen_split', 'initial_hyphen_split', 'word_hyphen_joined', 'initial_hyphen_joined'])

# ---------- (b) pamphlet numbering
marked = {t['marker'] for t in toks if t['marker'] is not None}
rows = []
for n in range(1, max(fw) + 1):
    f = fw.get(n, []); b = bw.get(n, [])
    cand = []
    for w in f + b:
        if w not in cand: cand.append(w)
    inits = ''.join(sorted({initial(w) for w in cand}))
    rows.append([n, '|'.join(f), '|'.join(b), '|'.join(cand), inits,
                 'yes' if len(cand) > 1 else '', 'yes' if n in marked else '',
                 'continued' if n > last_marker else ''])
write_csv(os.path.join(RESULTS, 'key_pamphlet_numbering.csv'), rows,
          ['n', 'word_forward_count', 'word_backward_count', 'candidate_words', 'candidate_initials',
           'ambiguous', 'printed_marker', 'beyond_last_marker'])

# ---------- (c) NARA
write_csv(os.path.join(RESULTS, 'key_nara.csv'),
          [[i + 1, w, initial(w)] for i, w in enumerate(nara)], ['n', 'word', 'initial'])

# ---------- (d) Gillogly Table I
write_csv(os.path.join(RESULTS, 'key_gillogly_table1.csv'),
          [[n, gill[n]] for n in sorted(gill)], ['n', 'initial'])

# ---------- anomalies of the printed numbering
# offset of the pamphlet numbering relative to the straight count, checked at every printed marker
marker_offsets = []
for i, t in enumerate(toks):
    if t['marker'] is not None:
        marker_offsets.append({'marker': t['marker'], 'word': t['word'], 'straight_position': i + 1,
                               'marker_minus_straight': t['marker'] - (i + 1)})
json.dump({'tokenisation': 'letters+apostrophes; hyphens/dashes split words',
           'pamphlet_words_hyphen_split': len(toks), 'pamphlet_words_hyphen_joined': len(toks_j),
           'nara_words_hyphen_split': len(nara), 'gillogly_table1_words': len(gill),
           'last_printed_marker': last_marker,
           'segment_anomalies': anomalies,
           'marker_offsets_vs_straight_count': marker_offsets},
          open(os.path.join(RESULTS, 'pamphlet_numbering_anomalies.json'), 'w'), indent=1)

# ---------- wording differences pamphlet vs NARA (word level)
pw = [t['word'] for t in toks]
sm = difflib.SequenceMatcher(a=pw, b=nara, autojunk=False)
diffs = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    diffs.append([tag, i1 + 1, i2, ' '.join(pw[i1:i2]), j1 + 1, j2, ' '.join(nara[j1:j2]),
                  ' '.join(pw[max(0, i1 - 3):i1]) + ' [' + ' '.join(pw[i1:i2]) + '] ' + ' '.join(pw[i2:i2 + 3])])
write_csv(os.path.join(RESULTS, 'doi_pamphlet_vs_nara_wording.csv'), diffs,
          ['op', 'pamphlet_from', 'pamphlet_to', 'pamphlet_words', 'nara_from', 'nara_to', 'nara_words', 'context_pamphlet'])

# ---------- initial-letter comparison against Gillogly's Table I
rows = []
dis_straight, dis_pamph, dis_nara = [], [], []
for n in range(1, 1325):
    s = initial(straight[n]) if n in straight else ''
    p = ''.join(sorted({initial(w) for w in fw.get(n, []) + bw.get(n, [])}))
    na = initial(nara[n - 1]) if n <= len(nara) else ''
    g = gill.get(n, '')
    rows.append([n, straight.get(n, ''), s, '|'.join(dict.fromkeys(fw.get(n, []) + bw.get(n, []))), p,
                 nara[n - 1] if n <= len(nara) else '', na, g,
                 '' if s == g else 'X', '' if (g in p and len(p) == 1) else 'X', '' if na == g else 'X'])
    if s != g: dis_straight.append(n)
    if not (g in p and len(p) == 1): dis_pamph.append(n)
    if na != g: dis_nara.append(n)
write_csv(os.path.join(RESULTS, 'key_comparison_vs_gillogly_table1.csv'), rows,
          ['n', 'pamphlet_straight_word', 'pamphlet_straight_initial', 'pamphlet_numbering_words',
           'pamphlet_numbering_initials', 'nara_word', 'nara_initial', 'gillogly_initial',
           'straight_ne_gillogly', 'pamphlet_numbering_ne_gillogly', 'nara_ne_gillogly'])


def ranges(nums):
    out = []
    for n in nums:
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ['%d' % a if a == b else '%d-%d' % (a, b) for a, b in out]

summary = {
    'n_disagree_straight_vs_gillogly': len(dis_straight), 'ranges_straight_vs_gillogly': ranges(dis_straight),
    'n_disagree_pamphlet_numbering_vs_gillogly': len(dis_pamph), 'ranges_pamphlet_numbering_vs_gillogly': ranges(dis_pamph),
    'n_disagree_nara_vs_gillogly': len(dis_nara), 'ranges_nara_vs_gillogly': ranges(dis_nara),
    'nara_vs_gillogly_detail': [[n, nara[n - 1] if n <= len(nara) else '', gill.get(n, '')] for n in dis_nara],
}
json.dump(summary, open(os.path.join(RESULTS, 'key_comparison_summary.json'), 'w'), indent=1)

if __name__ == '__main__':
    print('pamphlet words: %d (hyphen-split) / %d (hyphen-joined); NARA %d; Gillogly %d' %
          (len(toks), len(toks_j), len(nara), len(gill)))
    print('\nPrinted-numbering anomalies (segments whose word count != marker step):')
    for a in anomalies:
        print('  marker (%d) after (%d): %d words for a step of %d : %s' %
              (a['segment_end_marker'], a['prev_marker'], a['words_in_segment'], a['marker_step'], a['words']))
    print('\nOffset (printed marker - straight position) at each marker:')
    prev = None
    for m in marker_offsets:
        if m['marker_minus_straight'] != prev:
            print('  from marker (%d) "%s": offset %+d' % (m['marker'], m['word'], m['marker_minus_straight']))
            prev = m['marker_minus_straight']
    print('\nWording differences pamphlet vs NARA (%d):' % len(diffs))
    for d in diffs:
        print('  %-7s pamphlet %4d-%-4d %-28s | NARA %4d-%-4d %-28s | %s' % (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
    print('\nInitial letters vs Gillogly Table I:')
    for k, v in summary.items():
        if k != 'nara_vs_gillogly_detail':
            print(' ', k, v)
    print('  NARA vs Gillogly detail:', summary['nara_vs_gillogly_detail'])
