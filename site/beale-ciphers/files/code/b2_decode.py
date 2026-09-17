"""Task 2 - decode cipher 2 under each numbering, align to the plaintext, list every
disagreement, and derive the minimal key corrections.

Run from the case folder:  python3 code/b2_decode.py
Outputs (results/):
  b2_decodes.csv                      per-position decode under every key
  b2_disagreements_<key>.csv          every disagreement under that key
  b2_key_corrections.json             offset segmentation + isolated substitutions
  b2_printed_vs_decoded_plaintext.csv word-level diff printed plaintext vs decoded message
  b2_decode_summary.json / .md        the numbers quoted in the notes
"""
import os, json, re, difflib
from collections import Counter, defaultdict, OrderedDict
from beale_common import *

# The message as the cipher spells it (consensus reading of the literature; every letter is
# checked against the decode below).  763 letters.
INTENDED = ("i have deposited in the county of bedford about four miles from bufords in an excavation "
            "or vault six feet below the surface of the ground the following articles belonging jointly "
            "to the parties whose names are given in number three herewith the first deposit consisted of "
            "ten hundred and fourteen pounds of gold and thirty eight hundred and twelve pounds of silver "
            "deposited nov eighteen nineteen the second was made dec eighteen twenty one and consisted of "
            "nineteen hundred and seven pounds of gold and twelve hundred and eighty eight of silver also "
            "jewels obtained in st louis in exchange to save transportation and valued at thirteen thousand "
            "dollars the above is securely packed in iron pots with iron covers the vault is roughly lined "
            "with stone and the vessels rest on solid stone and are covered with others paper number one "
            "describes the exact locality of the vault so that no difficulty will be had in finding it")
T = INTENDED.replace(' ', '')

C2 = load_cipher(2)
toks = parse_pamphlet_doi()
straight = straight_numbering(toks)
fw, bw, anomalies, last_marker = pamphlet_numbering(toks)
nara, _ = nara_tokens()
gill = gillogly_table1()
P_letters, P_text = load_b2_plaintext_letters()


def single(m):
    return {n: [w] for n, w in m.items()}


KEYS = OrderedDict()
KEYS['straight_pamphlet_text'] = single(straight)
KEYS['pamphlet_numbering_forward'] = dict(fw)
KEYS['pamphlet_numbering_backward'] = dict(bw)
KEYS['nara_straight'] = single({i + 1: w for i, w in enumerate(nara)})
KEYS['gillogly_table1'] = {n: [ch.lower()] for n, ch in gill.items()}


def letters_for(key, n):
    ws = key.get(n)
    return {w[0].lower() for w in ws} if ws else set()


def word_at(key, n):
    ws = key.get(n)
    return '|'.join(ws) if ws else '-'


def nw_align(a, b, match=2, mismatch=-1, gap=-2):
    """Needleman-Wunsch global alignment; a = list of candidate-letter sets, b = string."""
    n, m = len(a), len(b)
    S = [[0] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        S[i][0] = i * gap; P[i][0] = 1
    for j in range(1, m + 1):
        S[0][j] = j * gap; P[0][j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            d = S[i - 1][j - 1] + (match if b[j - 1] in ai else mismatch)
            u = S[i - 1][j] + gap
            l = S[i][j - 1] + gap
            if d >= u and d >= l:
                S[i][j] = d; P[i][j] = 0
            elif u >= l:
                S[i][j] = u; P[i][j] = 1
            else:
                S[i][j] = l; P[i][j] = 2
    i, j, out = n, m, []
    while i > 0 or j > 0:
        p = P[i][j]
        if i > 0 and j > 0 and p == 0:
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        elif i > 0 and (j == 0 or p == 1):
            out.append((i - 1, None)); i -= 1
        else:
            out.append((None, j - 1)); j -= 1
    return out[::-1]


def analyse(name, key):
    cand = [letters_for(key, n) for n in C2]
    aln = nw_align(cand, T)
    exp = [None] * len(C2)
    tpos = [None] * len(C2)
    unmatched_T = []
    for i, j in aln:
        if i is not None and j is not None:
            exp[i] = T[j]; tpos[i] = j
        elif j is not None:
            unmatched_T.append(j)
    dis = []
    for i, n in enumerate(C2):
        ok = exp[i] is not None and exp[i] in cand[i]
        if not ok:
            ctx = ' '.join('%d=%s' % (k, word_at(key, k)) for k in range(n - 2, n + 3))
            j = tpos[i]
            pctx = (T[max(0, j - 6):j] + '[' + T[j] + ']' + T[j + 1:j + 7]) if j is not None else '(no letter)'
            dis.append([i + 1, n, ''.join(sorted(cand[i])) or '?', exp[i] or '(none)', word_at(key, n), ctx, pctx])
    n_ok = len(C2) - len(dis)
    return {'n_agree': n_ok, 'n_disagree': len(dis), 'unmatched_target_letters':
            [(j, T[j], T[max(0, j - 5):j + 6]) for j in unmatched_T], 'disagreements': dis, 'expected': exp,
            'cand': cand, 'tpos': tpos}


res = OrderedDict()
for name, key in KEYS.items():
    res[name] = analyse(name, key)
    write_csv(os.path.join(RESULTS, 'b2_disagreements_%s.csv' % name), res[name]['disagreements'],
              ['position', 'cipher_number', 'letter_obtained', 'letter_expected', 'key_word',
               'key_neighbours_n-2..n+2', 'plaintext_context'])

# ---- per-position decode table
rows = []
exp_ref = res['pamphlet_numbering_forward']['expected']
for i, n in enumerate(C2):
    rows.append([i + 1, n, exp_ref[i] or ''] + [''.join(sorted(letters_for(KEYS[k], n))) or '?' for k in KEYS])
write_csv(os.path.join(RESULTS, 'b2_decodes.csv'), rows, ['position', 'cipher_number', 'expected_letter'] +
          ['dec_' + k for k in KEYS])

# ---- resolve ambiguous pamphlet-gap numbers with the cipher
expected_by_number = defaultdict(Counter)
for i, n in enumerate(C2):
    if exp_ref[i]:
        expected_by_number[n][exp_ref[i]] += 1
ambig = []
for n in sorted(set(fw) | set(bw)):
    cands = list(dict.fromkeys(fw.get(n, []) + bw.get(n, [])))
    if len(cands) > 1 or n not in fw or n not in bw:
        used = expected_by_number.get(n)
        fits = [w for w in cands if used and w[0] in used]
        ambig.append({'n': n, 'forward': fw.get(n, []), 'backward': bw.get(n, []), 'used_in_B2_for': dict(used) if used else None,
                      'candidates_fitting_cipher': fits})
# ---- resolved pamphlet key: prefer the candidate the cipher pins down, else forward
resolved = {}
for n in sorted(set(fw) | set(bw)):
    cands = list(dict.fromkeys(fw.get(n, []) + bw.get(n, [])))
    used = expected_by_number.get(n)
    fits = [w for w in cands if used and w[0] in used]
    resolved[n] = [fits[0]] if fits else [cands[0]]
res['pamphlet_numbering_resolved'] = analyse('pamphlet_numbering_resolved', resolved)
write_csv(os.path.join(RESULTS, 'b2_disagreements_pamphlet_numbering_resolved.csv'),
          res['pamphlet_numbering_resolved']['disagreements'],
          ['position', 'cipher_number', 'letter_obtained', 'letter_expected', 'key_word', 'key_neighbours_n-2..n+2',
           'plaintext_context'])

# ---- offset segmentation relative to the straight count (dynamic programme)
# For each distinct cipher number take its majority expected letter; an offset d is "consistent"
# if the straight-count word n+d starts with that letter.
majority = {}
minority_errors = []
for n, c in expected_by_number.items():
    (lt, cnt), = c.most_common(1)
    majority[n] = lt
    for l2, c2 in c.items():
        if l2 != lt:
            minority_errors.append({'n': n, 'letter': l2, 'count': c2, 'majority_letter': lt})
occ = Counter(C2)
D = list(range(-15, 16))


def consistent(n, d):
    w = straight.get(n + d)
    return bool(w) and w[0] == majority[n]


def segment(lam, weight_by_occurrence=True):
    ns = sorted(majority)
    INF = float('inf')
    cost = {d: (0 if consistent(ns[0], d) else (occ[ns[0]] if weight_by_occurrence else 1)) for d in D}
    back = [{d: None for d in D}]
    for n in ns[1:]:
        newcost, newback = {}, {}
        w = occ[n] if weight_by_occurrence else 1
        best_prev = min(cost, key=cost.get)
        for d in D:
            stay = cost[d]
            switch = cost[best_prev] + lam
            if stay <= switch:
                base, prev = stay, d
            else:
                base, prev = switch, best_prev
            newcost[d] = base + (0 if consistent(n, d) else w)
            newback[d] = prev
        cost, back = newcost, back + [newback]
    d = min(cost, key=cost.get)
    total = cost[d]
    path = []
    for k in range(len(ns) - 1, -1, -1):
        path.append((ns[k], d))
        d = back[k][d]
    path = path[::-1]
    segs = []
    for n, d in path:
        if segs and segs[-1]['offset'] == d:
            segs[-1]['to'] = n; segs[-1]['numbers'].append(n)
        else:
            segs.append({'offset': d, 'from': n, 'to': n, 'numbers': [n]})
    unexplained = [{'n': n, 'offset': d, 'occurrences': occ[n], 'expected': majority[n],
                    'straight_word_at_n+d': straight.get(n + d)} for n, d in path if not consistent(n, d)]
    return {'lambda': lam, 'total_cost': total, 'segments': [{k: v for k, v in s.items() if k != 'numbers'} for s in segs],
            'unexplained': unexplained}


segmentations = {lam: segment(lam) for lam in (1, 2, 3, 5, 8, 12)}

# ---- the pamphlet's own offsets at the printed markers (for comparison with the DP)
marker_off = []
for i, t in enumerate(toks):
    if t['marker'] is not None:
        marker_off.append((t['marker'], (i + 1) - t['marker']))   # straight position - printed number

# ---- printed plaintext vs decoded message (word level)
pw = re.findall(r"[a-z]+", re.sub(r'[^a-z ]', ' ', P_text.lower().replace('$13,000', 'dollars13000')))
pw = re.findall(r"[a-z0-9$,]+", P_text.lower())
pw = [re.sub(r'[^a-z0-9$]', '', w) for w in pw]
pw = [w for w in pw if w]
tw = INTENDED.split()
sm = difflib.SequenceMatcher(a=tw, b=pw, autojunk=False)
pdiff = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        pdiff.append([tag, ' '.join(tw[i1:i2]), ' '.join(pw[j1:j2]), ' '.join(tw[max(0, i1 - 2):i1])])
write_csv(os.path.join(RESULTS, 'b2_printed_vs_decoded_plaintext.csv'), pdiff,
          ['op', 'decoded_message', 'printed_plaintext', 'preceding_words'])

# ---- facts about 95 / 811 / 1005 / 807
special = {}
for n in (95, 811, 1005, 807):
    special[n] = {'occurrences': occ[n], 'expected_letters': dict(expected_by_number[n]),
                  'pamphlet_numbering_word': fw.get(n), 'straight_count_word': straight.get(n),
                  'nara_word': nara[n - 1] if n <= len(nara) else None, 'gillogly_initial': gill.get(n)}
# words containing x / y anywhere in the pamphlet DOI (there is no initial x or y)
xy = {'words_with_initial_x': [n for n, w in straight.items() if w[0] == 'x'],
      'words_with_initial_y': [n for n, w in straight.items() if w[0] == 'y'],
      'words_containing_x_(straight_n:word)': {n: w for n, w in straight.items() if 'x' in w},
      'words_containing_y_(straight_n:word)': {n: w for n, w in straight.items() if 'y' in w and n > 700 and n < 900}}

# ---- how many cipher numbers are touched by the pamphlet's miscount?
n_shift = sum(1 for n in C2 if n >= 250)   # every number >= 250 maps differently under straight vs pamphlet count
distinct_shift = len({n for n in C2 if n >= 250})
wrong_under_nara = res['nara_straight']['n_disagree']
wrong_under_straight = res['straight_pamphlet_text']['n_disagree']

summary = OrderedDict()
summary['cipher2_numbers'] = len(C2)
summary['cipher2_distinct'] = len(set(C2))
summary['intended_message_letters'] = len(T)
summary['printed_plaintext_letters'] = len(P_letters)
summary['per_key'] = {k: {'n_agree': v['n_agree'], 'n_disagree': v['n_disagree'],
                          'unmatched_target_letters': v['unmatched_target_letters']} for k, v in res.items()}
summary['ambiguous_gap_numbers'] = ambig
summary['numbers_at_or_above_250_occurrences'] = n_shift
summary['numbers_at_or_above_250_distinct'] = distinct_shift
summary['numbers_in_155_250_occurrences'] = sum(1 for n in C2 if 155 <= n <= 250)
summary['numbers_in_155_250_distinct'] = len({n for n in C2 if 155 <= n <= 250})
summary['printed_marker_offsets_(straight_position_minus_printed_number)'] = marker_off
summary['offset_segmentation'] = segmentations
summary['minority_letter_uses'] = minority_errors
summary['special_numbers'] = special
summary['x_y_in_key'] = xy
summary['printed_vs_decoded_plaintext_diff'] = pdiff
json.dump(summary, open(os.path.join(RESULTS, 'b2_decode_summary.json'), 'w'), indent=1)

if __name__ == '__main__':
    print('cipher 2: %d numbers (%d distinct); intended message %d letters; printed plaintext %d letters' %
          (len(C2), len(set(C2)), len(T), len(P_letters)))
    for k, v in res.items():
        print('\n== key %s: %d agree, %d disagree; target letters without a number: %s' %
              (k, v['n_agree'], v['n_disagree'], v['unmatched_target_letters']))
        if v['n_disagree'] <= 40:
            for d in v['disagreements']:
                print('   pos %3d  n=%4d  got %-3s expected %s  key word %-14s | %s | %s' % tuple(d))
    print('\nAmbiguous gap numbers and what the cipher says:')
    for a in ambig:
        if a['used_in_B2_for']:
            print('  ', a)
    print('\nOffset segmentation vs straight count (lambda=3):')
    for s in segmentations[3]['segments']:
        print('   numbers %4d..%4d : encoder number n = straight word n%+d' % (s['from'], s['to'], s['offset']))
    print('   unexplained:', segmentations[3]['unexplained'])
    print('   cost by lambda:', {l: (s['total_cost'], len(s['segments'])) for l, s in segmentations.items()})
    print('\nPrinted-marker offsets (straight - printed):', marker_off[:1], '...', [m for m in marker_off if m[1] != 0][:3], '...')
    print('\nSpecial numbers:'); [print('  ', n, v) for n, v in special.items()]
    print('\nx/y availability:', {k: (v if not isinstance(v, dict) else len(v)) for k, v in xy.items()})
    print('   words containing x:', xy['words_containing_x_(straight_n:word)'])
    print('\nPrinted plaintext vs decoded message (word diff):')
    for d in pdiff:
        print('   %-8s decoded [%s]  printed [%s]  after "%s"' % tuple(d))
    print('\nminority uses:', minority_errors)
