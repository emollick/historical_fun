"""Serial-structure extras.

(1) Why does the genuine cipher B2 show a lag-1 rank autocorrelation of about 0.2?  Null:
    permute B2's numbers only among positions that carry the same plaintext letter (letters
    from the alignment in stats_00_key_check.py).  This keeps every letter's set of
    homophones and the plaintext order and destroys any sequential habit of the encoder
    beyond letter identity.  If the autocorrelation survives, it is a property of the
    letter->number mapping plus English bigram structure (a feature a genuine cipher can
    have), not of the encoder's hand.
(2) Ascending runs of numbers ('sawtooth' writing): longest strictly ascending run, number
    of ascending runs of length >= 4 and >= 6, mean ascending-run length, for B1, B2, B3
    against full shuffles.
Writes results/stats_serial_extras.json.
"""
import os, json
from collections import defaultdict
import numpy as np
from scipy import stats
from stats_common import *

SEED = 20260914
NPERM = 5000
rng = np.random.default_rng(SEED)
C = load_ciphers()
with open(os.path.join(RESULTS, "stats_key_check.json")) as f:
    KC = json.load(f)
rec = KC["b2_alignment"]["records"]
x2 = np.array([r["number"] for r in rec]); L2 = [r["intended"] or "?" for r in rec]


def lag_spearman(x, lag):
    rk = stats.rankdata(x); return float(np.corrcoef(rk[:-lag], rk[lag:])[0, 1])


def lag_pearson(x, lag):
    return float(np.corrcoef(x[:-lag], x[lag:])[0, 1])


def close(x, tol):
    return int((np.abs(np.diff(x)) <= tol).sum())


def runs_updown(x):
    d = np.sign(np.diff(x.astype(float))); d = d[d != 0]
    return 1 + int((d[1:] != d[:-1]).sum())


def ascending_runs(x):
    """lengths of maximal strictly ascending runs (a run of length 1 = no rise)."""
    lens = []; cur = 1
    for a, b in zip(x[:-1], x[1:]):
        if b > a:
            cur += 1
        else:
            lens.append(cur); cur = 1
    lens.append(cur)
    return np.array(lens)


stat_fns = {
    "lag1_spearman": lambda v: lag_spearman(v, 1), "lag2_spearman": lambda v: lag_spearman(v, 2),
    "lag1_pearson": lambda v: lag_pearson(v, 1), "close_le5": lambda v: close(v, 5),
    "close_le10": lambda v: close(v, 10), "runs_up_down": runs_updown,
    "longest_ascending_run": lambda v: int(ascending_runs(v).max()),
    "ascending_runs_ge4": lambda v: int((ascending_runs(v) >= 4).sum()),
    "ascending_runs_ge6": lambda v: int((ascending_runs(v) >= 6).sum()),
    "mean_ascending_run": lambda v: float(ascending_runs(v).mean()),
}


def perm_summary(x, permute, nperm):
    obs = {k: f(x) for k, f in stat_fns.items()}
    sims = {k: np.empty(nperm) for k in stat_fns}
    for i in range(nperm):
        y = permute(x)
        for k, f in stat_fns.items():
            sims[k][i] = f(y)
    out = {}
    for k in stat_fns:
        s = sims[k]; o = obs[k]
        ge = int((s >= o - 1e-12).sum()); le = int((s <= o + 1e-12).sum())
        out[k] = {"obs": float(o), "null_mean": float(s.mean()), "null_sd": float(s.std()),
                  "p_greater": perm_pvalue(ge, nperm), "p_less": perm_pvalue(le, nperm),
                  "null_p2.5": float(np.percentile(s, 2.5)), "null_p97.5": float(np.percentile(s, 97.5))}
    return out


# (1) letter-preserving shuffle of B2
groups = defaultdict(list)
for i, L in enumerate(L2):
    groups[L].append(i)
groups = {k: np.array(v) for k, v in groups.items()}


def letter_shuffle(x):
    y = x.copy()
    for idx in groups.values():
        if len(idx) > 1:
            y[idx] = x[rng.permutation(idx)]
    return y


def full_shuffle(x):
    return rng.permutation(x)


res = {"seed": SEED, "n_perm": NPERM,
       "B2_letter_preserving_shuffle": perm_summary(x2, letter_shuffle, NPERM),
       "B2_full_shuffle": perm_summary(x2, full_shuffle, NPERM)}
for k in (1, 3):
    res[f"B{k}_full_shuffle"] = perm_summary(C[k], full_shuffle, NPERM)
save_json(res, "stats_serial_extras.json")
for name, d in res.items():
    if isinstance(d, dict):
        print(name)
        for k, v in d.items():
            print(f"   {k:24s} obs={v['obs']:8.3f} null={v['null_mean']:8.3f}±{v['null_sd']:.3f} p_greater={v['p_greater']:.4f} p_less={v['p_less']:.4f}")
