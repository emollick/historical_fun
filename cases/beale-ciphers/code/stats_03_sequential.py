"""Task 3: sequential structure of the number sequences, each compared with shuffles of
the same cipher (permutation p-values; two-sided unless stated).

  * lag-1 / lag-2 Pearson autocorrelation of the numbers and of log(numbers); Spearman
    rank autocorrelation;
  * runs-up-and-down (ties dropped): count, asymptotic z, permutation p;
  * close consecutive pairs |a-b| <= 1, 5, 10 and exact adjacent repeats (one-sided: more
    than shuffles);
  * adjacent equal last digits / equal first digits (humans avoid repeating a digit);
  * trend along the sequence (Spearman rho of value vs position; first- vs second-half mean);
  * positions of the large numbers (>1322 in B1; upper decile elsewhere): KS vs uniform;
  * Gillogly-type alphabetic runs in the letters obtained with the DOI key (Gillogly's
    Table I numbering = straight count with "self-evident" split), vs shuffles of the same
    letters; also under the straight count.
Writes results/stats_sequential.json.
"""
import os, json
from collections import Counter
import numpy as np
from scipy import stats
from stats_common import *

SEED = 20260914
NPERM = 20_000
rng = np.random.default_rng(SEED)
C = load_ciphers()


def lag_corr(x, lag):
    x = np.asarray(x, float)
    a, b = x[:-lag], x[lag:]
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def runs_up_down(x):
    d = np.sign(np.diff(np.asarray(x, float)))
    d = d[d != 0]
    if len(d) == 0:
        return 0, 0
    runs = 1 + int((d[1:] != d[:-1]).sum())
    return runs, len(d) + 1   # n = number of values after tie removal


def close_pairs(x, tol):
    x = np.asarray(x)
    return int((np.abs(np.diff(x)) <= tol).sum())


def eq_adjacent(v):
    v = np.asarray(v)
    return int((v[1:] == v[:-1]).sum())


def perm_test(x, statfn, nperm, rng, alternative="two-sided"):
    x = np.array(x)
    obs = statfn(x)
    sims = np.empty(nperm)
    y = x.copy()
    for i in range(nperm):
        rng.shuffle(y)
        sims[i] = statfn(y)
    mu, sd = sims.mean(), sims.std()
    if alternative == "greater":
        ge = int((sims >= obs - 1e-12).sum())
    elif alternative == "less":
        ge = int((sims <= obs + 1e-12).sum())
    else:
        ge = int((np.abs(sims - mu) >= abs(obs - mu) - 1e-12).sum())
    p = perm_pvalue(ge, nperm)
    return {"observed": float(obs), "null_mean": float(mu), "null_sd": float(sd),
            "z": float((obs - mu) / sd) if sd > 0 else None, "p_perm": p,
            "p_mc_se": mc_se(p, nperm), "alternative": alternative, "n_perm": nperm}


def longest_monotone_run(letters, strict=False):
    """Longest run of alphabetically non-decreasing (or strictly increasing) letters."""
    best = cur = 1
    for a, b in zip(letters[:-1], letters[1:]):
        ok = (b > a) if strict else (b >= a)
        cur = cur + 1 if ok else 1
        best = max(best, cur)
    return best


def count_runs_ge(letters, L, strict=False):
    n = 0; cur = 1
    for a, b in zip(letters[:-1], letters[1:]):
        ok = (b > a) if strict else (b >= a)
        if ok:
            cur += 1
        else:
            if cur >= L: n += 1
            cur = 1
    if cur >= L: n += 1
    return n


def successor_steps(letters):
    """adjacent pairs where the second letter is the same as or the alphabetic successor of the first."""
    return sum(1 for a, b in zip(letters[:-1], letters[1:]) if 0 <= ord(b) - ord(a) <= 1)


out = {"seed": SEED, "n_perm": NPERM, "ciphers": {}}
for k in (1, 2, 3):
    x = C[k]
    r = {"n": len(x)}
    r["lag1_pearson"] = perm_test(x, lambda v: lag_corr(v, 1), NPERM, rng)
    r["lag2_pearson"] = perm_test(x, lambda v: lag_corr(v, 2), NPERM, rng)
    lx = np.log(x)
    r["lag1_pearson_log"] = perm_test(lx, lambda v: lag_corr(v, 1), NPERM, rng)
    r["lag2_pearson_log"] = perm_test(lx, lambda v: lag_corr(v, 2), NPERM, rng)
    rk = stats.rankdata(x)
    r["lag1_spearman"] = perm_test(rk, lambda v: lag_corr(v, 1), NPERM, rng)
    r["lag2_spearman"] = perm_test(rk, lambda v: lag_corr(v, 2), NPERM, rng)
    runs, n_eff = runs_up_down(x)
    mu = (2 * n_eff - 1) / 3; var = (16 * n_eff - 29) / 90
    r["runs_up_down"] = perm_test(x, lambda v: runs_up_down(v)[0], NPERM, rng)
    r["runs_up_down"].update({"n_after_ties": n_eff, "asymptotic_mean": mu,
                              "asymptotic_z": (runs - mu) / np.sqrt(var),
                              "asymptotic_p": float(2 * stats.norm.sf(abs((runs - mu) / np.sqrt(var))))})
    for tol in (0, 1, 5, 10):
        r[f"close_pairs_le{tol}"] = perm_test(x, lambda v, t=tol: close_pairs(v, t), NPERM, rng, "greater")
    r["adjacent_equal_last_digit"] = perm_test(x % 10, eq_adjacent, NPERM, rng)
    fd = np.array([int(str(v)[0]) for v in x])
    r["adjacent_equal_first_digit"] = perm_test(fd, eq_adjacent, NPERM, rng)
    pos = np.arange(len(x))
    rho = stats.spearmanr(pos, x).correlation
    r["trend_spearman"] = perm_test(x, lambda v: stats.spearmanr(pos, v).correlation, 5000, rng)
    half = len(x) // 2
    r["half_mean_diff"] = perm_test(x, lambda v: v[:half].mean() - v[half:].mean(), NPERM, rng)
    # positions of large numbers
    thr = 1322 if k == 1 else float(np.percentile(x, 90))
    idx = np.where(x > thr)[0]
    ks = stats.kstest((idx + 0.5) / len(x), "uniform")
    r["large_number_positions"] = {"threshold": thr, "n_large": int(len(idx)),
                                   "positions": idx.tolist(), "ks_stat": float(ks.statistic),
                                   "ks_p": float(ks.pvalue)}
    # gaps between large numbers vs shuffle (clustering): variance of gaps
    if len(idx) >= 5:
        def gapvar(v, t=thr):
            ii = np.where(v > t)[0]
            return float(np.var(np.diff(ii)))
        r["large_number_gap_variance"] = perm_test(x, gapvar, 5000, rng)
    out["ciphers"][f"B{k}"] = r

# ---- Gillogly-type alphabetic runs in the DOI decode --------------------------------
with open(os.path.join(RESULTS, "stats_key_best_initials.json")) as f:
    keys = json.load(f)
words = load_key_words()
split = []
for w in words:
    if w.lower().startswith("self-evident"):
        split += ["self", "evident"]
    else:
        split.append(w)
key_variants = {"gillogly_split": [word_initial(w) for w in split],
                "straight": [word_initial(w) for w in words],
                "pamphlet_numbering": keys["initials"]}
runs_out = {}
for kv, ini in key_variants.items():
    for k in (1, 2, 3):
        letters = decode(C[k], ini, oob="?")
        L = [c for c in letters if c != "?"]   # Gillogly dropped out-of-range numbers for the run
        # keep positions: treat '?' as a run breaker instead (more conservative); report both
        Lb = list(letters)
        d = {}
        d["longest_nondecreasing_run_skip_oob"] = perm_test(np.array(L), lambda v: longest_monotone_run(list(v)), 5000, rng, "greater")
        d["longest_nondecreasing_run_break_oob"] = perm_test(np.array(Lb), lambda v: longest_monotone_run(list(v)), 5000, rng, "greater")
        d["longest_strict_run_break_oob"] = perm_test(np.array(Lb), lambda v: longest_monotone_run(list(v), True), 5000, rng, "greater")
        d["n_nondecreasing_runs_ge5"] = perm_test(np.array(Lb), lambda v: count_runs_ge(list(v), 5), 5000, rng, "greater")
        d["successor_steps"] = perm_test(np.array(Lb), lambda v: successor_steps(list(v)), 5000, rng, "greater")
        # locate the longest run
        best = cur = 1; end = 0
        for i in range(1, len(Lb)):
            cur = cur + 1 if Lb[i] >= Lb[i - 1] else 1
            if cur > best:
                best, end = cur, i
        d["longest_run_text"] = "".join(Lb[end - best + 1:end + 1])
        d["longest_run_start_pos"] = end - best + 2
        runs_out[f"{kv}_B{k}"] = d
out["alphabetic_runs_in_DOI_decode"] = runs_out
save_json(out, "stats_sequential.json")

for k in (1, 2, 3):
    r = out["ciphers"][f"B{k}"]
    print(f"B{k}: " + "; ".join(f"{nm} obs={v['observed']:.3f} z={v['z']:.2f} p={v['p_perm']:.4f}"
          for nm, v in r.items() if isinstance(v, dict) and "observed" in v))
    print(f"    runs asymptotic z={r['runs_up_down']['asymptotic_z']:.2f} p={r['runs_up_down']['asymptotic_p']:.3f}; "
          f"large-number positions KS p={r['large_number_positions']['ks_p']:.3f} (n={r['large_number_positions']['n_large']})")
for nm, d in runs_out.items():
    print(nm, d["longest_run_text"], "@", d["longest_run_start_pos"],
          {q: (v["observed"], round(v["null_mean"], 2), v["p_perm"]) for q, v in d.items() if isinstance(v, dict)})
