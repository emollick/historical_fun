"""Task 3 - how the cipher-2 encoder chose homophones.

Uses the corrected cipher (the six isolated slips repaired, "108" -> "10, 8": 763 numbers, one per
plaintext letter) and the encoder's key (the pamphlet's own numbering, gaps resolved by the cipher,
with 95 = unalienable, 811 = y, 1005 = x).

Run from the case folder:  python3 code/b2_encoder_behaviour.py
Outputs: results/b2_encoder_behaviour.json, results/b2_encoder_behaviour.md, results/b2_corrected_cipher.txt
"""
import os, json, math
from collections import Counter, defaultdict, OrderedDict
import numpy as np
from beale_common import *
import b2_decode as D

C2 = D.C2
T = D.T
res = D.res['pamphlet_numbering_resolved']
exp = res['expected']

# ---------------- build the encoder's key (number -> word), letters as the encoder used them
enc_key = {n: ws[0] for n, ws in D.resolved.items()}
enc_key[95] = 'unalienable'          # the encoder's copy read "unalienable" (95 -> u, 96 -> 95 slip -> u)
enc_key[811] = 'y:fundamentally'     # used as y (no DOI word begins with y)
enc_key[1005] = 'x:have'             # used as x (no DOI word begins with x)
def enc_letter(n):
    w = enc_key.get(n)
    if w is None:
        return None
    return w[0] if ':' not in w else w[0]   # 'y:...' -> 'y', 'x:...' -> 'x'

# ---------------- corrected cipher: repair isolated slips so that every number gives its letter
corrected, corrections = [], []
i = 0
for pos, n in enumerate(C2):
    e = exp[pos]
    if e is None:
        corrections.append({'position': pos + 1, 'number': n, 'note': 'no plaintext letter aligned'})
        continue
    if enc_letter(n) == e:
        corrected.append(n); continue
    # try a split into two numbers (the "108" -> "10, 8" case) using the next expected letter
    s = str(n)
    fixed = False
    j = res['tpos'][pos]
    unmatched = [u[0] for u in res['unmatched_target_letters']]
    for k in range(1, len(s)):
        a, b = int(s[:k]), int(s[k:])
        if s[k] == '0':
            continue
        la, lb = enc_letter(a), enc_letter(b)
        if (j - 1 in unmatched and (la, lb) == (T[j - 1], T[j])) or (j + 1 in unmatched and (la, lb) == (T[j], T[j + 1])):
            corrected += [a, b]
            corrections.append({'position': pos + 1, 'number': n, 'read_as': [a, b], 'letters': la + lb,
                                'words': [enc_key[a], enc_key[b]]})
            fixed = True; break
    if fixed:
        continue
    cands = [n + 1, n - 1, n + 2, n - 2] + [int(s[:k] + s[k + 1:]) for k in range(len(s)) if len(s) > 1 and (s[:k] + s[k + 1:])[0] != '0']
    for m in cands:
        if enc_letter(m) == e:
            corrected.append(m); corrections.append({'position': pos + 1, 'number': n, 'read_as': m, 'letter': e,
                                                      'word': enc_key[m], 'kind': 'adjacent number' if abs(m - n) <= 2 else 'dropped digit'})
            fixed = True; break
    if not fixed:
        corrections.append({'position': pos + 1, 'number': n, 'note': 'UNREPAIRED', 'expected': e})
        corrected.append(n)
assert len(corrected) == len(T), (len(corrected), len(T))
assert all(enc_letter(n) == t for n, t in zip(corrected, T)), 'corrected cipher does not spell the message'
open(os.path.join(RESULTS, 'b2_corrected_cipher.txt'), 'w').write(' '.join(map(str, corrected)) + '\n')

# ---------------- homophone inventory of the key (as the encoder numbered it)
maxn = max(enc_key)
by_letter = defaultdict(list)
for n in sorted(enc_key):
    by_letter[enc_letter(n)].append(n)
rank_of = {n: by_letter[enc_letter(n)].index(n) + 1 for n in enc_key}

uses = Counter(corrected)
letter_uses = defaultdict(Counter)
for n in corrected:
    letter_uses[enc_letter(n)][n] += 1

per_letter = OrderedDict()
all_norm_ranks, all_ranks, first_flags = [], [], []
for L in sorted(letter_uses):
    H = len(by_letter[L])
    cnt = letter_uses[L]
    total = sum(cnt.values())
    numbers = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    ranks = [rank_of[n] for n in cnt.elements()]
    nr = [(r - 0.5) / H for r in ranks]          # normalised rank in (0,1); uniform choice -> mean 0.5
    all_norm_ranks += nr; all_ranks += ranks; first_flags += [r == 1 for r in ranks]
    top = numbers[0]
    per_letter[L] = {
        'uses': total, 'distinct_numbers': len(cnt), 'homophones_available': H,
        'numbers_used': [{'n': n, 'count': c, 'word': enc_key[n].split(':')[-1], 'rank_in_doi': rank_of[n]} for n, c in numbers],
        'most_used': {'n': top[0], 'count': top[1], 'share': round(top[1] / total, 3), 'rank_in_doi': rank_of[top[0]]},
        'share_top3_numbers': round(sum(c for _, c in numbers[:3]) / total, 3),
        'uses_at_rank1_(first_word_with_this_initial)': sum(1 for r in ranks if r == 1),
        'first_word_with_this_initial': {'n': by_letter[L][0], 'word': enc_key[by_letter[L][0]].split(':')[-1]},
        'mean_rank': round(float(np.mean(ranks)), 2), 'median_rank': float(np.median(ranks)),
        'mean_normalised_rank': round(float(np.mean(nr)), 3),
        'max_number_used': max(cnt), 'share_of_uses_with_n_le_100': round(sum(c for n, c in cnt.items() if n <= 100) / total, 3),
        'share_of_available_homophones_with_n_le_100': round(sum(1 for n in by_letter[L] if n <= 100) / H, 3),
        'reuse_rate_(1-distinct/uses)': round(1 - len(cnt) / total, 3),
    }

# ---------------- global statistics
N = len(corrected)
xy_free = [n for n in corrected if enc_letter(n) not in 'xy']
nr = np.array(all_norm_ranks)
global_stats = OrderedDict()
global_stats['letters_encoded'] = N
global_stats['distinct_numbers'] = len(uses)
global_stats['reuse_rate_overall'] = round(1 - len(uses) / N, 3)
global_stats['share_of_uses_that_are_the_FIRST_word_with_that_initial'] = round(float(np.mean(first_flags)), 3)
# expected share under uniform choice among homophones: mean over uses of 1/H
exp_first = float(np.mean([1 / per_letter[enc_letter(n)]['homophones_available'] for n in corrected]))
global_stats['expected_share_first_word_if_uniform_over_homophones'] = round(exp_first, 3)
global_stats['mean_normalised_rank_(0.5_if_uniform)'] = round(float(nr.mean()), 3)
global_stats['se_mean_normalised_rank'] = round(float(nr.std(ddof=1) / math.sqrt(len(nr))), 4)
global_stats['share_uses_n_le_100'] = round(sum(1 for n in corrected if n <= 100) / N, 3)
global_stats['share_uses_n_le_250'] = round(sum(1 for n in corrected if n <= 250) / N, 3)
global_stats['share_uses_n_le_500'] = round(sum(1 for n in corrected if n <= 500) / N, 3)
global_stats['share_uses_n_gt_816'] = round(sum(1 for n in corrected if n > 816) / N, 3)
global_stats['largest_number_other_than_1005'] = max(n for n in corrected if n != 1005)
global_stats['share_of_key_words_n_le_100'] = round(100 / maxn, 3)
global_stats['share_of_key_words_n_le_250'] = round(250 / maxn, 3)
# distribution of ranks: how many uses at rank 1,2,3,<=5,<=10
rk = np.array(all_ranks)
global_stats['rank_histogram'] = {'rank1': int((rk == 1).sum()), 'rank2': int((rk == 2).sum()), 'rank3': int((rk == 3).sum()),
                                  'rank4-5': int(((rk >= 4) & (rk <= 5)).sum()), 'rank6-10': int(((rk >= 6) & (rk <= 10)).sum()),
                                  'rank>10': int((rk > 10).sum())}
# doubled letters: same number twice?
doubles = []
for i in range(1, N):
    if T[i] == T[i - 1]:
        doubles.append({'pos': i, 'pair': T[i - 1] + T[i], 'numbers': [corrected[i - 1], corrected[i]], 'same': corrected[i - 1] == corrected[i]})
global_stats['doubled_letters'] = {'count': len(doubles), 'same_number_used_twice': sum(d['same'] for d in doubles),
                                   'detail': doubles}
# immediate reuse of a number for the same letter within a window
def reuse_within(w):
    c = 0
    for i in range(N):
        for j in range(max(0, i - w), i):
            if corrected[j] == corrected[i]:
                c += 1; break
    return c
global_stats['uses_that_repeat_a_number_seen_within_previous_10_numbers'] = reuse_within(10)
# preference for low numbers WITHIN each letter's homophone list (normalised rank quartiles)
global_stats['normalised_rank_quartile_shares'] = [round(float(((nr >= q / 4) & (nr < (q + 1) / 4)).mean()), 3) for q in range(4)]
# KS-type test of normalised ranks vs uniform(0,1) (scipy if available)
try:
    from scipy import stats
    ks = stats.kstest(nr, 'uniform')
    global_stats['ks_test_normalised_rank_vs_uniform'] = {'D': round(float(ks.statistic), 4), 'p': float(ks.pvalue)}
except Exception as e:  # pragma: no cover
    global_stats['ks_test_normalised_rank_vs_uniform'] = str(e)

out = OrderedDict([('corrections_applied_to_printed_cipher', corrections), ('global', global_stats), ('per_letter', per_letter)])
json.dump(out, open(os.path.join(RESULTS, 'b2_encoder_behaviour.json'), 'w'), indent=1)

# ---------------- markdown table
md = ['# Cipher 2 encoder behaviour', '',
      'Corrected cipher: %d numbers, %d distinct (results/b2_corrected_cipher.txt). Key = pamphlet numbering as resolved by the cipher, 95=unalienable, 811=y, 1005=x.' % (N, len(uses)), '',
      '| letter | uses | distinct nos. | homophones in key | first word (n) | uses of first word | most used n (count, rank) | mean rank | mean norm. rank | top-3 share | max n used |',
      '|---|---|---|---|---|---|---|---|---|---|---|']
for L, s in per_letter.items():
    f = s['first_word_with_this_initial']; m = s['most_used']
    md.append('| %s | %d | %d | %d | %s (%d) | %d | %d (%d, r%d) | %.1f | %.2f | %.2f | %d |' % (
        L, s['uses'], s['distinct_numbers'], s['homophones_available'], f['word'], f['n'],
        s['uses_at_rank1_(first_word_with_this_initial)'], m['n'], m['count'], m['rank_in_doi'], s['mean_rank'],
        s['mean_normalised_rank'], s['share_top3_numbers'], s['max_number_used']))
md += ['', '## Global', '']
for k, v in global_stats.items():
    if k not in ('doubled_letters',):
        md.append('- %s: %s' % (k, v))
dl = global_stats['doubled_letters']
md.append('- doubled letters in the message: %d; same number used for both: %d' % (dl['count'], dl['same_number_used_twice']))
md += ['', '## Corrections applied to the printed cipher', '']
for c in corrections:
    md.append('- ' + json.dumps(c))
open(os.path.join(RESULTS, 'b2_encoder_behaviour.md'), 'w').write('\n'.join(md) + '\n')

if __name__ == '__main__':
    print('\n'.join(md))
