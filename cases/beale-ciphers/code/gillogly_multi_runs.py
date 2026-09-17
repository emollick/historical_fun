"""Task 4 (supplement) - how unlikely is it to see SEVERAL long alphabetic runs in one 520-letter
sequence?  Statistic: number of maximal runs of length >= L (non-decreasing, and "+0/+1" step runs)
in B1 decoded with a key; null = permutations of B1's own numbers and i.i.d. uniform numbers.

Run from the case folder:  python3 code/gillogly_multi_runs.py   (NSIM_MULTI env, default 200000)
Output: results/gillogly_multi_runs.json
"""
import os, sys, json, time
from collections import Counter, OrderedDict
import numpy as np
from beale_common import *
import b2_decode as D

NSIM = int(os.environ.get('NSIM_MULTI', '200000'))

# --- keys/relations (same definitions as gillogly_strings.py, duplicated so that importing that
#     module does not re-run its Monte Carlo)
class G:
    pass
def arr_from_letters(d, size=3000):
    a = np.full(size, -1, dtype=np.int8)
    for n, ch in d.items():
        if 0 < n < size:
            a[n] = ord(ch.lower()) - 97
    return a
G.KEYS = OrderedDict()
G.KEYS['gillogly_table1'] = arr_from_letters(gillogly_table1())
_enc = {n: ws[0][0] for n, ws in D.resolved.items()}; _enc[95] = 'u'; _enc[811] = 'y'; _enc[1005] = 'x'
G.KEYS['pamphlet_encoder_key'] = arr_from_letters(_enc)
G.KEY_LEN = {k: int(np.max(np.nonzero(v >= 0)[0])) for k, v in G.KEYS.items()}
G.MAIN_KEYS = ('gillogly_table1', 'pamphlet_encoder_key')
_A = np.arange(26)
G.R_NONDEC = (_A[None, :] >= _A[:, None]).astype(np.int8)
G.R_STEP = ((_A[None, :] == _A[:, None]) | (_A[None, :] == _A[:, None] + 1)).astype(np.int8)
def _decode_arr(nums, key):
    nums = np.asarray(nums); out = np.full(len(nums), -1, dtype=np.int8)
    ok = (nums > 0) & (nums < len(key)); out[ok] = key[nums[ok]]; return out
G.decode_arr = staticmethod(_decode_arr)
import math
def _pval_report(counts_ge, N):
    p = counts_ge / N
    return {'p': p, 'se': math.sqrt(max(p * (1 - p), 0) / N), 'upper95_if_zero': (3.0 / N if counts_ge == 0 else None), 'N': N, 'count': int(counts_ge)}
G.pval_report = staticmethod(_pval_report)
BATCH = 50000
rng = np.random.default_rng(20260915)
C1 = np.asarray(load_cipher(1))

def count_runs_ge_vec(Lm, R, L):
    """number of maximal runs of length >= L per row."""
    N, n = Lm.shape
    cur = (Lm[:, 0] >= 0).astype(np.int16)
    cnt = np.zeros(N, dtype=np.int16)
    for i in range(1, n):
        a, b = Lm[:, i - 1], Lm[:, i]
        ok = (a >= 0) & (b >= 0)
        cont = np.zeros(N, dtype=bool); cont[ok] = R[a[ok], b[ok]].astype(bool)
        cnt += ((~cont) & (cur >= L)).astype(np.int16)      # a run ends here
        cur = np.where(cont, cur + 1, (b >= 0).astype(np.int16))
    cnt += (cur >= L).astype(np.int16)
    return cnt

out = OrderedDict({'nsim': NSIM})
for kname in G.MAIN_KEYS:
    key = G.KEYS[kname]; codes = G.decode_arr(C1, key)
    ent = OrderedDict()
    for rel, R, Ls in (('nondecreasing', G.R_NONDEC, (8, 10, 11)), ('step01', G.R_STEP, (8, 10))):
        obs = {L: int(count_runs_ge_vec(codes[None, :], R, L)[0]) for L in Ls}
        res = {}
        for L in Ls:
            c_perm, c_unif = Counter(), Counter()
            t0 = time.time()
            for b0 in range(0, NSIM, BATCH):
                m = min(BATCH, NSIM - b0)
                idx = np.argsort(rng.random((m, len(C1))), axis=1)
                c_perm.update(Counter(count_runs_ge_vec(codes[idx], R, L).tolist()))
                draw = rng.integers(1, G.KEY_LEN[kname] + 1, size=(m, 520))
                c_unif.update(Counter(count_runs_ge_vec(key[draw], R, L).tolist()))
            def rep(c):
                tot = sum(c.values()); k = sum(v for x, v in c.items() if x >= obs[L])
                return {'histogram': dict(sorted(c.items())), 'P_ge_observed': G.pval_report(k, tot)}
            res[L] = {'observed_count': obs[L], 'permutation': rep(c_perm), 'uniform_numbers': rep(c_unif), 'seconds': round(time.time() - t0, 1)}
            print('  done', kname, rel, L, file=sys.stderr, flush=True)
        ent[rel] = res
    out[kname] = ent
json.dump(out, open(os.path.join(RESULTS, 'gillogly_multi_runs.json'), 'w'), indent=1)
if __name__ == '__main__':
    for kname, ent in out.items():
        if kname == 'nsim': continue
        for rel, res in ent.items():
            for L, r in res.items():
                print(kname, rel, 'L>=%d' % L, 'observed', r['observed_count'], 'perm P', r['permutation']['P_ge_observed'], 'unif P', r['uniform_numbers']['P_ge_observed'])
