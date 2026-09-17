"""Task 4 - the Gillogly strings in cipher 1 (and cipher 3): reproduction of Gillogly's Table III,
alphabetic runs, exact / Monte-Carlo probabilities under three null models, and the "lazy hoaxer"
homophone-rank test.

Run from the case folder:  python3 code/gillogly_strings.py
      NSIM=20000 python3 ...   for a quick run (defaults: NSIM=1_000_000 exact-letter shuffles,
      NSIM_SUB=NSIM for the substitution-allowing statistics; seed 20260914)
Outputs: results/gillogly_strings.json, results/gillogly_runs.csv, results/b1_b3_decodes.csv

Statistics (all on the letter sequence obtained by decoding with a key; '?' = number outside key):
  S1  longest non-decreasing run (A<=B<=...), exact letters
  S2  longest "+0/+1" run (each letter equals the previous or is its alphabetic successor) - this is
      the model Gillogly used for his 1/13^13 estimate
  S3  longest non-decreasing run when at most 2 positions may be read as n-1 or n+1 (Gillogly's
      two off-by-one corrections)
  S4  as S3 but with unlimited off-by-one substitutions (very permissive; sensitivity only)
  S5  longest "+0/+1" run with at most 2 off-by-one substitutions
  S6, S7  as S3, S5 but with at most ONE substitution (the natural reading of B1 under the pamphlet key:
      17 exact letters + the single 301->302 slip)
"""
import os, sys, json, time, math
from collections import Counter, OrderedDict, defaultdict
import numpy as np
from beale_common import *
import b2_decode as D

NSIM = int(os.environ.get('NSIM', '1000000'))
NSIM_SUB = int(os.environ.get('NSIM_SUB', str(NSIM)))
SEED = 20260914
BATCH = 50000
KSUB = 2

C1, C3 = load_cipher(1), load_cipher(3)
g_nums, _ = gillogly_table2()
table3 = gillogly_table3()

# ---------------- keys as int8 arrays indexed by number (-1 = no word)
def arr_from_letters(d, size=3000):
    a = np.full(size, -1, dtype=np.int8)
    for n, ch in d.items():
        if 0 < n < size:
            a[n] = ord(ch.lower()) - 97
    return a

KEYS = OrderedDict()
KEYS['gillogly_table1'] = arr_from_letters(gillogly_table1())
nara, _ = nara_tokens()
KEYS['nara_straight'] = arr_from_letters({i + 1: w[0] for i, w in enumerate(nara)})
enc = {n: ws[0][0] for n, ws in D.resolved.items()}
enc[95] = 'u'; enc[811] = 'y'; enc[1005] = 'x'
KEYS['pamphlet_encoder_key'] = arr_from_letters(enc)
KEYS['pamphlet_straight'] = arr_from_letters({n: w[0] for n, w in D.straight.items()})
KEY_LEN = {k: int(np.max(np.nonzero(v >= 0)[0])) for k, v in KEYS.items()}
MAIN_KEYS = ('gillogly_table1', 'pamphlet_encoder_key')

# relations: R[a, b] = 1 if letter b may follow letter a inside a run
A26 = np.arange(26)
R_NONDEC = (A26[None, :] >= A26[:, None]).astype(np.int8)
R_STEP = ((A26[None, :] == A26[:, None]) | (A26[None, :] == A26[:, None] + 1)).astype(np.int8)
RELS = {'nondecreasing': R_NONDEC, 'step01': R_STEP}

def to_str(codes):
    return ''.join('?' if c < 0 else chr(97 + c).upper() for c in codes)

def decode_arr(nums, key):
    nums = np.asarray(nums)
    out = np.full(len(nums), -1, dtype=np.int8)
    ok = (nums > 0) & (nums < len(key))
    out[ok] = key[nums[ok]]
    return out

def cand_triples(nums, key):
    nums = np.asarray(nums)
    out = np.full((len(nums), 3), -1, dtype=np.int8)
    for k, d in enumerate((-1, 0, 1)):
        m = nums + d
        ok = (m > 0) & (m < len(key))
        out[ok, k] = key[m[ok]]
    return out

# ---------------- maximal runs (exact letters) under a relation
def maximal_runs(codes, R, minlen=5):
    runs, i, n = [], 0, len(codes)
    while i < n:
        if codes[i] < 0:
            i += 1; continue
        j = i
        while j + 1 < n and codes[j + 1] >= 0 and R[codes[j], codes[j + 1]]:
            j += 1
        if j - i + 1 >= minlen:
            runs.append((i, j - i + 1))
        i = j + 1
    return runs

def longest_exact(codes, R):
    return max((l for _, l in maximal_runs(codes, R, 1)), default=0)

# ---------------- vectorised: exact letters
def longest_exact_vec(Lm, R):
    N, n = Lm.shape
    cur = (Lm[:, 0] >= 0).astype(np.int16)
    best = cur.copy()
    for i in range(1, n):
        a, b = Lm[:, i - 1], Lm[:, i]
        ok = (a >= 0) & (b >= 0)
        cont = np.zeros(N, dtype=bool)
        cont[ok] = R[a[ok], b[ok]].astype(bool)
        cur = np.where(cont, cur + 1, (b >= 0).astype(np.int16))
        np.maximum(best, cur, out=best)
    return best

# ---------------- vectorised: with at most k off-by-one substitutions (k=None: unlimited)
def longest_sub_vec(Tm, R, k=KSUB):
    """Tm: (N, n, 3) candidate letters for n-1, n, n+1. Returns longest run length per row."""
    N, n, _ = Tm.shape
    K = (k + 1) if k is not None else 1
    cost = [1, 0, 1] if k is not None else [0, 0, 0]
    run = np.zeros((N, 3, K), dtype=np.int16)
    for c in range(3):
        if cost[c] < K:
            run[:, c, cost[c]] = (Tm[:, 0, c] >= 0)
    best = run.max(axis=(1, 2))
    for i in range(1, n):
        prev, cur = Tm[:, i - 1, :], Tm[:, i, :]
        newrun = np.zeros_like(run)
        for c in range(3):
            cc = cur[:, c]; valid = cc >= 0
            sc = cost[c]
            for j in range(K - sc):           # substitutions used before this position
                m = np.zeros(N, dtype=np.int16)
                for cp in range(3):
                    pp = prev[:, cp]
                    ok = (pp >= 0) & valid
                    cont = np.zeros(N, dtype=bool)
                    cont[ok] = R[pp[ok], cc[ok]].astype(bool)
                    np.maximum(m, np.where(cont, run[:, cp, j], 0), out=m)
                newrun[:, c, j + sc] = np.where(valid, m + 1, 0)
        run = newrun
        np.maximum(best, run.max(axis=(1, 2)), out=best)
    return best

def longest_sub_trace(tri, R, k=KSUB):
    """Scalar version with traceback: returns (length, [(pos, choice)])."""
    n = tri.shape[0]
    K = (k + 1) if k is not None else 1
    cost = [1, 0, 1] if k is not None else [0, 0, 0]
    NEG = -1
    run = np.zeros((n, 3, K), dtype=np.int32); prev = np.full((n, 3, K, 2), NEG, dtype=np.int32)
    for c in range(3):
        if cost[c] < K and tri[0, c] >= 0:
            run[0, c, cost[c]] = 1
    for i in range(1, n):
        for c in range(3):
            if tri[i, c] < 0:
                continue
            sc = cost[c]
            for j in range(K - sc):
                best, bp = 0, (NEG, NEG)
                for cp in range(3):
                    if tri[i - 1, cp] >= 0 and R[tri[i - 1, cp], tri[i, c]] and run[i - 1, cp, j] > best:
                        best, bp = run[i - 1, cp, j], (cp, j)
                run[i, c, j + sc] = best + 1; prev[i, c, j + sc] = bp
    i, c, j = np.unravel_index(np.argmax(run), run.shape)
    L = int(run[i, c, j])
    path = []
    while i >= 0 and c >= 0 and run[i, c, j] > 0:
        path.append((int(i), int(c)))
        cp, jp = prev[i, c, j]
        i, c, j = i - 1, cp, jp
        if cp < 0:
            break
    return L, path[::-1]

# ---------------- exact probability for i.i.d. letters (Markov chain, vectorised)
def exact_prob_run_ge(p, n, L, R, q_break=0.0):
    p = np.asarray(p, dtype=float); p = p / p.sum()
    Rf = R.astype(float)
    st = np.zeros((26, L))          # st[b, r]: current run ends in letter b with length r (1..L-1)
    start, done = 1.0, 0.0
    for _ in range(n):
        tot_letters = st.sum()
        new = np.zeros_like(st)
        cont = Rf.T @ st              # cont[b, r] = sum_a R[a,b] st[a, r]
        new[:, 2:] = (1 - q_break) * p[:, None] * cont[:, 1:L - 1]
        done += (1 - q_break) * float((p[:, None] * cont[:, L - 1:L]).sum())
        # runs restarting at b: from start, or from any state whose letter cannot be continued by b
        new[:, 1] = (1 - q_break) * p * (start + (tot_letters - cont.sum(axis=1)))
        start = q_break * (start + tot_letters)
        st = new
    return done

def mc_se(p, N):
    return math.sqrt(max(p * (1 - p), 0) / N)

def pval_report(counts_ge, N):
    p = counts_ge / N
    return {'p': p, 'se': mc_se(p, N), 'upper95_if_zero': (3.0 / N if counts_ge == 0 else None), 'N': N, 'count': int(counts_ge)}

def hist_p(cnt, thresholds):
    tot = sum(cnt.values())
    return {'histogram': dict(sorted(cnt.items())), 'N': tot,
            'P_ge': {int(L): pval_report(sum(c for l, c in cnt.items() if l >= L), tot) for L in sorted(set(thresholds))}}

# ============================================================== analyses
out = OrderedDict()
out['nsim'] = NSIM; out['nsim_sub'] = NSIM_SUB; out['seed'] = SEED; out['k_substitutions'] = KSUB

# --- 1. reproduce Gillogly's Table III
dec_g_from_g = to_str(decode_arr(g_nums, KEYS['gillogly_table1']))
dec_g_from_ours = to_str(decode_arr(C1, KEYS['gillogly_table1']))
diff_tab = [(i + 1, g_nums[i], table3[i], dec_g_from_g[i]) for i in range(520) if table3[i] != dec_g_from_g[i]]
diff_ours = [(i + 1, C1[i], g_nums[i], table3[i], dec_g_from_ours[i]) for i in range(520) if table3[i] != dec_g_from_ours[i]]
out['table3_reproduction'] = {'table3_len': len(table3), 'mismatches_using_gillogly_numbers': diff_tab,
                              'mismatches_using_our_B1_numbers_(pos, ours, gillogly, table3, ours_decoded)': diff_ours}

# --- 2. decodes of B1 and B3 under each key
decs = OrderedDict((k, {'B1': to_str(decode_arr(C1, a)), 'B3': to_str(decode_arr(C3, a))}) for k, a in KEYS.items())
rows = []
for i in range(max(len(C1), len(C3))):
    rows.append([i + 1, C1[i] if i < len(C1) else ''] + [decs[k]['B1'][i] if i < len(C1) else '' for k in KEYS] +
                [C3[i] if i < len(C3) else ''] + [decs[k]['B3'][i] if i < len(C3) else '' for k in KEYS])
write_csv(os.path.join(RESULTS, 'b1_b3_decodes.csv'), rows, ['position', 'B1_number'] + ['B1_' + k for k in KEYS] +
          ['B3_number'] + ['B3_' + k for k in KEYS])
out['decodes'] = decs
out['B1_numbers_out_of_range'] = {k: int(np.sum(decode_arr(C1, a) < 0)) for k, a in KEYS.items()}
out['B1_numbers_gt_1322'] = int(sum(1 for n in C1 if n > 1322))
out['key_lengths'] = KEY_LEN

# --- 3. the Gillogly string and the off-by-one claims
GS = 'ABFDEFGHIIJKLMMNOHPP'
pos_t3 = table3.find(GS); pos_ours = dec_g_from_ours.find(GS)
out['gillogly_string'] = {'string': GS, 'index0_in_table3': pos_t3, 'index0_in_our_decode': pos_ours,
                          'positions_1based': list(range(pos_ours + 1, pos_ours + 21)),
                          'numbers': C1[pos_ours:pos_ours + 20],
                          'decoded_under_each_key': {k: decs[k]['B1'][pos_ours:pos_ours + 20] for k in KEYS}}
out['off_by_one_claim_(194,195,301,302)'] = {k: {n: (chr(97 + a[n]).upper() if a[n] >= 0 else '?') for n in (194, 195, 301, 302)}
                                             for k, a in KEYS.items()}
out['key_words_194_195_301_302'] = {'pamphlet_numbering': {n: D.resolved.get(n) for n in (194, 195, 301, 302)},
                                    'nara': {n: nara[n - 1] for n in (194, 195, 301, 302)}}

# --- 4. observed statistics per cipher and key
runs_rows = []
obs = OrderedDict()
for k, a in KEYS.items():
    for cname, C in (('B1', C1), ('B3', C3)):
        codes = decode_arr(C, a); tri = cand_triples(C, a)
        for rel, R in RELS.items():
            for s, l in maximal_runs(codes, R, 5):
                runs_rows.append([cname, k, rel, s + 1, l, to_str(codes[s:s + l]), ' '.join(map(str, C[s:s + l]))])
        e = OrderedDict()
        e['S1_longest_nondecreasing_exact'] = longest_exact(codes, R_NONDEC)
        e['S2_longest_step01_exact'] = longest_exact(codes, R_STEP)
        e['n_nondecreasing_runs_ge5'] = len(maximal_runs(codes, R_NONDEC, 5))
        e['n_nondecreasing_runs_ge8'] = len(maximal_runs(codes, R_NONDEC, 8))
        e['n_step01_runs_ge5'] = len(maximal_runs(codes, R_STEP, 5))
        for sname, R, kk in (('S3_nondecreasing_le2_subs', R_NONDEC, KSUB), ('S4_nondecreasing_unlimited_subs', R_NONDEC, None),
                             ('S5_step01_le2_subs', R_STEP, KSUB), ('S6_nondecreasing_le1_sub', R_NONDEC, 1),
                             ('S7_step01_le1_sub', R_STEP, 1)):
            L, path = longest_sub_trace(tri, R, kk)
            e[sname] = L
            e[sname + '_letters'] = ''.join(chr(97 + tri[i, c]).upper() for i, c in path)
            e[sname + '_detail_(pos, printed_n, n_read, letter)'] = [(i + 1, int(C[i]), int(C[i] + c - 1), chr(97 + tri[i, c]).upper()) for i, c in path]
        obs[cname + '/' + k] = e
write_csv(os.path.join(RESULTS, 'gillogly_runs.csv'), runs_rows, ['cipher', 'key', 'relation', 'start_pos_1based', 'length', 'letters', 'numbers'])
out['observed'] = obs

# --- 5. null models
rng = np.random.default_rng(SEED)

def letter_dist(key):
    v = key[key >= 0]
    return np.bincount(v, minlength=26) / len(v)

null_i = OrderedDict()
for kname in MAIN_KEYS:
    key = KEYS[kname]; p = letter_dist(key)
    codes = decode_arr(C1, key); qb = float(np.mean(codes < 0))
    ent = {'letter_frequencies': {chr(97 + i).upper(): round(float(p[i]), 4) for i in range(26) if p[i] > 0},
           'break_fraction_in_B1': qb}
    for rel, R in RELS.items():
        ent['exact_P_' + rel + '_run_ge_L_n520'] = {L: exact_prob_run_ge(p, 520, L, R) for L in (5, 8, 10, 12, 14, 17, 20)}
        ent['exact_P_' + rel + '_run_ge_L_with_B1_breaks'] = {L: exact_prob_run_ge(p, 520, L, R, qb) for L in (5, 8, 10, 12, 14, 17, 20)}
    # uniform-26 model for comparison with Gillogly's arithmetic
    ent['uniform26_P_step01_run_ge_L_n520'] = {L: exact_prob_run_ge(np.ones(26) / 26, 520, L, R_STEP) for L in (14, 17, 20)}
    ent['uniform26_P_nondecreasing_run_ge_L_n520'] = {L: exact_prob_run_ge(np.ones(26) / 26, 520, L, R_NONDEC) for L in (14, 17, 20)}
    ent['gillogly_arithmetic_495_over_13^13'] = 495 / 13 ** 13
    # expected number of maximal non-decreasing runs of length >= L (approx (521-L)*h_L)
    h = {}
    for L in (5, 8, 10, 12, 14, 17):
        cum = p.copy()
        for _ in range(L - 1):
            cum = p * np.cumsum(cum)
        h[L] = float(cum.sum())
    ent['P_L_consecutive_iid_letters_nondecreasing'] = h
    ent['expected_number_of_nondecreasing_runs_ge_L_(approx)'] = {L: (521 - L) * v for L, v in h.items()}
    null_i[kname] = ent
out['null_i_iid_letters_exact'] = null_i

# (i-MC) i.i.d. letters with B1's break positions (sanity check of the DP), exact letters
def mc_iid_letters(p, breaks, N, R):
    cnt = Counter()
    for b0 in range(0, N, BATCH):
        m = min(BATCH, N - b0)
        Lm = rng.choice(26, size=(m, 520), p=p).astype(np.int8)
        Lm[:, breaks] = -1
        cnt.update(Counter(longest_exact_vec(Lm, R).tolist()))
    return cnt

null_i_mc = OrderedDict()
for kname in MAIN_KEYS:
    key = KEYS[kname]; codes = decode_arr(C1, key); breaks = np.nonzero(codes < 0)[0]
    t0 = time.time()
    e = {}
    for rel, R in RELS.items():
        cnt = mc_iid_letters(letter_dist(key), breaks, NSIM, R)
        e[rel] = hist_p(cnt, [10, 12, 14, 17, 20, obs['B1/' + kname]['S1_longest_nondecreasing_exact'], obs['B1/' + kname]['S2_longest_step01_exact']])
    e['seconds'] = round(time.time() - t0, 1)
    null_i_mc[kname] = e
out['null_i_iid_letters_mc'] = null_i_mc

# (ii) permutation test on B1's own numbers  /  (iii) i.i.d. uniform numbers 1..key length
def sim_numbers(kind, key, klen, N, stat):
    """kind: 'perm' or 'uniform'; stat: ('exact', R) or ('sub', R, k)."""
    cnt = Counter()
    nums = np.asarray(C1)
    tri_all = cand_triples(nums, key)
    for b0 in range(0, N, BATCH):
        m = min(BATCH, N - b0)
        if kind == 'perm':
            idx = np.argsort(rng.random((m, len(nums))), axis=1)
            if stat[0] == 'exact':
                cnt.update(Counter(longest_exact_vec(decode_arr(nums, key)[idx], stat[1]).tolist()))
            else:
                cnt.update(Counter(longest_sub_vec(tri_all[idx], stat[1], stat[2]).tolist()))
        else:
            draw = rng.integers(1, klen + 1, size=(m, 520))
            if stat[0] == 'exact':
                cnt.update(Counter(longest_exact_vec(key[draw], stat[1]).tolist()))
            else:
                Tm = np.stack([key[np.clip(draw + d, 0, len(key) - 1)] for d in (-1, 0, 1)], axis=-1)
                Tm[:, :, 0][draw - 1 <= 0] = -1
                cnt.update(Counter(longest_sub_vec(Tm, stat[1], stat[2]).tolist()))
    return cnt

STATS = OrderedDict([('S1_longest_nondecreasing_exact', ('exact', R_NONDEC)), ('S2_longest_step01_exact', ('exact', R_STEP)),
                     ('S3_nondecreasing_le2_subs', ('sub', R_NONDEC, KSUB)), ('S4_nondecreasing_unlimited_subs', ('sub', R_NONDEC, None)),
                     ('S5_step01_le2_subs', ('sub', R_STEP, KSUB)), ('S6_nondecreasing_le1_sub', ('sub', R_NONDEC, 1)),
                     ('S7_step01_le1_sub', ('sub', R_STEP, 1))])
for kind, label in (('perm', 'null_ii_permutation_of_B1_numbers'), ('uniform', 'null_iii_uniform_numbers')):
    ent = OrderedDict()
    for kname in MAIN_KEYS:
        key = KEYS[kname]; e = OrderedDict({'key_length': KEY_LEN[kname]})
        for sname, stat in STATS.items():
            t0 = time.time()
            N = NSIM if stat[0] == 'exact' else NSIM_SUB
            cnt = sim_numbers(kind, key, KEY_LEN[kname], N, stat)
            o = obs['B1/' + kname][sname]
            e[sname] = {'observed_B1': o, **hist_p(cnt, [10, 12, 14, 17, 20, o]), 'seconds': round(time.time() - t0, 1)}
            print('  done', label, kname, sname, 'N=%d' % N, '%.0fs' % (time.time() - t0), file=sys.stderr, flush=True)
        ent[kname] = e
    out[label] = ent

# --- 6. lazy-hoaxer ranks for the Gillogly string
from scipy import stats as sps
def rank_tables(key):
    by = defaultdict(list)
    for n in range(1, len(key)):
        if key[n] >= 0:
            by[int(key[n])].append(n)
    return by
lazy = OrderedDict()
for kname in MAIN_KEYS:
    key = KEYS[kname]; by = rank_tables(key)
    rows, nr = [], []
    for i in range(pos_ours, pos_ours + 20):
        n = C1[i]; c = int(key[n]) if n < len(key) and key[n] >= 0 else -1
        if c < 0:
            rows.append({'pos': i + 1, 'n': n, 'letter': '?'}); continue
        lst = by[c]; r = lst.index(n) + 1; H = len(lst); nr.append((r - 0.5) / H)
        rows.append({'pos': i + 1, 'n': n, 'letter': chr(97 + c).upper(), 'word': (D.resolved.get(n, ['?'])[0] if kname == 'pamphlet_encoder_key' else nara[n - 1]),
                     'rank_among_homophones': r, 'homophones': H, 'first_number_with_this_initial': lst[0]})
    ranks = [r['rank_among_homophones'] for r in rows if 'rank_among_homophones' in r]
    Hs = [r['homophones'] for r in rows if 'homophones' in r]
    k_obs = sum(1 for r in ranks if r == 1)
    dist = np.zeros(1); dist[0] = 1.0
    for H in Hs:
        q = 1.0 / H
        dist = np.concatenate([dist * (1 - q), [0]]) + np.concatenate([[0], dist * q])
    p_ge_uniform = float(dist[k_obs:].sum())
    # whole-B1 reference: normalised ranks and rank-1 share of all in-range B1 numbers
    allnr, allr1 = [], []
    for n in C1:
        if n < len(key) and key[n] >= 0:
            lst = by[int(key[n])]; allnr.append((lst.index(n) + 0.5) / len(lst)); allr1.append(lst[0] == n)
    n_in, n_r1 = len(allr1), int(sum(allr1))
    p_ge_hyper = float(sps.hypergeom.sf(k_obs - 1, n_in, n_r1, 20))
    # mean normalised rank of the 20 vs random 20-subsets of B1's in-range numbers (permutation, 100k)
    arr = np.array(allnr); m_obs = float(np.mean(nr))
    sims = np.array([arr[rng.choice(n_in, 20, replace=False)].mean() for _ in range(100000)])
    lazy[kname] = {'rows': rows, 'rank1_count': k_obs, 'rank_le3_count': sum(1 for r in ranks if r <= 3),
                   'mean_normalised_rank': m_obs, 'expected_rank1_if_uniform_over_homophones': float(sum(1 / H for H in Hs)),
                   'P_at_least_this_many_rank1_if_uniform_over_homophones': p_ge_uniform,
                   'whole_B1_in_range': n_in, 'whole_B1_rank1_count': n_r1, 'whole_B1_share_rank1': n_r1 / n_in,
                   'whole_B1_mean_normalised_rank': float(arr.mean()),
                   'P_at_least_this_many_rank1_if_20_random_B1_numbers_(hypergeometric)': p_ge_hyper,
                   'P_mean_normalised_rank_le_observed_if_20_random_B1_numbers': float(np.mean(sims <= m_obs))}
out['lazy_hoaxer_ranks'] = lazy
try:
    beh = json.load(open(os.path.join(RESULTS, 'b2_encoder_behaviour.json')))
    out['b2_encoder_reference'] = {'mean_normalised_rank': beh['global']['mean_normalised_rank_(0.5_if_uniform)'],
                                   'share_rank1': beh['global']['share_of_uses_that_are_the_FIRST_word_with_that_initial'],
                                   'share_n_le_100': beh['global']['share_uses_n_le_100']}
except Exception:
    pass
out['B1_share_numbers_le_100'] = float(np.mean(np.array(C1) <= 100))
out['B1_share_numbers_le_250'] = float(np.mean(np.array(C1) <= 250))

json.dump(out, open(os.path.join(RESULTS, 'gillogly_strings.json'), 'w'), indent=1, default=str)

if __name__ == '__main__':
    print('Table III reproduction: mismatches with Gillogly numbers:', diff_tab)
    print('  mismatches with our numbers:', diff_ours)
    print('B1 out of range per key:', out['B1_numbers_out_of_range'], '; >1322:', out['B1_numbers_gt_1322'])
    print('Gillogly string at index', pos_t3, '(Table III) /', pos_ours, '(ours); numbers', out['gillogly_string']['numbers'])
    print('  decoded under each key:', out['gillogly_string']['decoded_under_each_key'])
    print('off-by-one claims:', out['off_by_one_claim_(194,195,301,302)'])
    print('key words:', out['key_words_194_195_301_302'])
    for k, v in obs.items():
        print(k, {kk: vv for kk, vv in v.items() if 'detail' not in kk})
    for kname, e in null_i.items():
        print('null (i) exact DP', kname)
        for kk, vv in e.items():
            if isinstance(vv, dict) and 'P_' in kk or 'expected' in kk or 'uniform26' in kk:
                print('   ', kk, {L: '%.3g' % v for L, v in vv.items()})
        print('    gillogly 495/13^13 =', '%.3g' % e['gillogly_arithmetic_495_over_13^13'])
    for label in ('null_i_iid_letters_mc', 'null_ii_permutation_of_B1_numbers', 'null_iii_uniform_numbers'):
        print(label)
        for kname, e in out[label].items():
            for sname, v in e.items():
                if isinstance(v, dict) and 'P_ge' in v:
                    print('   %s %s obs=%s' % (kname, sname, v.get('observed_B1', '')), {L: ('%.2g±%.1g' % (r['p'], r['se']) if r['count'] else '<%.1g' % r['upper95_if_zero']) for L, r in v['P_ge'].items()})
    for kname, e in lazy.items():
        print('lazy', kname, {k: v for k, v in e.items() if k != 'rows'})
        for r in e['rows']:
            print('   ', r)
