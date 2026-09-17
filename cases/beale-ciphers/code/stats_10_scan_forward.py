"""Could a 'scan-forward' habit explain the serial structure?

A book-cipher encoder who, for the next letter, scans the key forward from the word he has
just used and takes the first word with the right initial produces rising runs of numbers.
We (1) measure in B2 how often the next number is exactly the nearest forward homophone of
the previous one (against the fitted memoryless model), and (2) simulate a mixed encoder that
scans forward with probability q and otherwise behaves like the fitted (or reuse-calibrated)
encoder, for B1- and B3-length English prose with the DOI key and the long keys, over a grid
of q, recording the serial statistics that distinguish B3 (lag-1/lag-2 autocorrelation,
ascending runs, first-vs-second-half mean, clustering of large numbers).
Writes results/stats_scan_forward.json.
"""
import os, json, sys
from collections import defaultdict
import numpy as np
from scipy import stats
from stats_common import *
from stats_simlib import *

SEED = 20260916
NSIM = int(os.environ.get("NSIM", "300"))
rng = np.random.default_rng(SEED)
C = load_ciphers()
with open(os.path.join(RESULTS, "stats_homophone_sim.json")) as f:
    FIT = json.load(f)["fit"]
gamma, tau0, eps = FIT["gamma"], FIT["tau"], FIT["slip_rate"]
beta = FIT["logistic_beta_logd"]
p_reuse_fit = lambda d: 1 / (1 + np.exp(-(beta[0] + beta[1] * np.log(max(d, 1)))))
with open(os.path.join(RESULTS, "stats_calibrated_reuse.json")) as f:
    CAL = json.load(f)
KC, doi_key, long_keys, prose, names_pt = load_keys_and_texts()
prose_for = {id(k): filtered(prose, k) for k in [doi_key] + list(long_keys.values())}


def ascending_runs(x):
    lens = []; cur = 1
    for a, b in zip(x[:-1], x[1:]):
        if b > a:
            cur += 1
        else:
            lens.append(cur); cur = 1
    lens.append(cur)
    return np.array(lens)


def serial_stats(x):
    x = np.asarray(x); n = len(x); rk = stats.rankdata(x)
    ar = ascending_runs(x)
    half = n // 2
    thr = np.percentile(x, 90); idx = np.where(x > thr)[0]
    ks = stats.kstest((idx + 0.5) / n, "uniform").pvalue if len(idx) > 3 else np.nan
    d = np.sign(np.diff(x.astype(float))); d = d[d != 0]
    runs = 1 + int((d[1:] != d[:-1]).sum()); ne = len(d) + 1
    return {"lag1_pearson": float(np.corrcoef(x[:-1], x[1:])[0, 1]),
            "lag1_spearman": float(np.corrcoef(rk[:-1], rk[1:])[0, 1]),
            "lag2_spearman": float(np.corrcoef(rk[:-2], rk[2:])[0, 1]),
            "lag2_pearson": float(np.corrcoef(x[:-2], x[2:])[0, 1]),
            "mean_ascending_run": float(ar.mean()), "ascending_runs_ge4": int((ar >= 4).sum()),
            "ascending_runs_ge6": int((ar >= 6).sum()), "longest_ascending_run": int(ar.max()),
            "rise_share": float((np.diff(x) > 0).mean()),
            "runs_z": float((runs - (2 * ne - 1) / 3) / np.sqrt((16 * ne - 29) / 90)),
            "half_mean_diff": float(x[:half].mean() - x[half:].mean()),
            "trend_spearman": float(stats.spearmanr(np.arange(n), x).correlation),
            "large_pos_ks_p": float(ks), "large_gap_var": float(np.var(np.diff(idx))) if len(idx) > 3 else np.nan,
            "distinct": len(set(x.tolist())), "close_le10": int((np.abs(np.diff(x)) <= 10).sum()),
            "median": float(np.median(x))}


SER = list(serial_stats(C[3]).keys())

# ---- (1) forward moves in B2 ---------------------------------------------------------
rec = KC["b2_alignment"]["records"]
x2 = np.array([r["number"] for r in rec]); L2 = [r["intended"] for r in rec]
def nearest_forward(prev, L, key):
    H = key.hom.get(L)
    if H is None:
        return None
    later = H[H > prev]
    return int(later[0]) if len(later) else int(H[0])
def nearest_backward(prev, L, key):
    H = key.hom.get(L)
    if H is None:
        return None
    earlier = H[H < prev]
    return int(earlier[-1]) if len(earlier) else None
fwd = sum(1 for i in range(1, len(x2)) if L2[i] and nearest_forward(x2[i - 1], L2[i], doi_key) == x2[i])
bwd = sum(1 for i in range(1, len(x2)) if L2[i] and nearest_backward(x2[i - 1], L2[i], doi_key) == x2[i])
# chance level: shuffle B2's numbers within letter classes
groups = defaultdict(list)
for i, L in enumerate(L2):
    groups[L].append(i)
fwd_null = []; bwd_null = []
for _ in range(2000):
    y = x2.copy()
    for idx in groups.values():
        idx = np.array(idx)
        if len(idx) > 1:
            y[idx] = x2[rng.permutation(idx)]
    fwd_null.append(sum(1 for i in range(1, len(y)) if L2[i] and nearest_forward(y[i - 1], L2[i], doi_key) == y[i]))
    bwd_null.append(sum(1 for i in range(1, len(y)) if L2[i] and nearest_backward(y[i - 1], L2[i], doi_key) == y[i]))
fwd_null = np.array(fwd_null); bwd_null = np.array(bwd_null)
b2_fwd = {"forward_moves": fwd, "forward_null_mean": float(fwd_null.mean()), "forward_null_sd": float(fwd_null.std()),
          "forward_p": perm_pvalue(int((fwd_null >= fwd).sum()), 2000),
          "backward_moves": bwd, "backward_null_mean": float(bwd_null.mean()), "backward_null_sd": float(bwd_null.std()),
          "backward_p": perm_pvalue(int((bwd_null >= bwd).sum()), 2000), "n_steps": len(x2) - 1}
print("B2 nearest-forward-homophone moves:", fwd, "vs letter-shuffle null", f"{fwd_null.mean():.1f}±{fwd_null.std():.1f}",
      "p=", b2_fwd["forward_p"], "| nearest-backward:", bwd, "vs", f"{bwd_null.mean():.1f}±{bwd_null.std():.1f}", "p=", b2_fwd["backward_p"])

# ---- (2) the mixed encoder ------------------------------------------------------------
def encode_scan(text, key, rng, q, p_reuse_fn, tau):
    out = []; prev = 0
    usedc = {L: {} for L in key.hom}
    w_new = {L: np.exp(-key.hom[L] / tau) for L in key.hom}
    unused = {L: np.ones(len(key.hom[L]), bool) for L in key.hom}
    for L in text:
        if L not in key.hom:
            continue
        H = key.hom[L]
        if rng.random() < q:
            later = H[H > prev]; n = int(later[0]) if len(later) else int(H[0])
            j = int(np.where(H == n)[0][0]); unused[L][j] = False
        else:
            U = usedc[L]; d = len(U); can_new = unused[L].any()
            if d > 0 and ((not can_new) or rng.random() < p_reuse_fn(d)):
                nums = list(U); w = np.array([U[v] for v in nums], float) ** gamma
                n = nums[rng.choice(len(nums), p=w / w.sum())]
            else:
                w = w_new[L] * unused[L]; j = rng.choice(len(w), p=w / w.sum())
                n = int(H[j]); unused[L][j] = False
        usedc[L][n] = usedc[L].get(n, 0) + 1
        out.append(n); prev = n
    return np.array(out)


def window(L, key):
    src = prose_for[id(key)]; s = rng.integers(0, len(src) - L)
    return src[s:s + L]


results = {"seed": SEED, "nsim": NSIM, "b2_forward_moves": b2_fwd, "targets": {}}
QS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
for tname, k, L, longK in (("B1", 1, 520, 2906), ("B3", 3, 618, 975), ("B2", 2, len(C[2]), None)):
    obs = serial_stats(C[k])
    results["targets"][tname] = {"observed": obs, "models": {}}
    keyset = [("DOI", doi_key)] + ([(f"LONG{longK}", long_keys[longK])] if longK else [])
    for kname, key in keyset:
        tau = tau0 if kname == "DOI" else tau0 * key.K / doi_key.K
        # reuse: B2-fitted for B2; calibrated constant for B1/B3
        if tname == "B2":
            pr = p_reuse_fit
        else:
            r = CAL["targets"][tname]["models"][kname]["r_calibrated"]; pr = (lambda d, r=r: r)
        for q in QS:
            rows = [serial_stats(encode_scan(window(L, key), key, rng, q, pr, tau)) for _ in range(NSIM)]
            summ = {}
            for s in SER:
                sim = np.array([rw[s] for rw in rows], float); sim = sim[~np.isnan(sim)]
                o = obs[s]
                summ[s] = {"obs": o, "sim_mean": float(sim.mean()), "sim_sd": float(sim.std()),
                           "p2.5": float(np.percentile(sim, 2.5)), "p97.5": float(np.percentile(sim, 97.5)),
                           "percentile": float((sim <= o).mean())}
            results["targets"][tname]["models"][f"{kname}_q{q:.1f}"] = summ
            show = ["lag1_pearson", "lag1_spearman", "lag2_spearman", "mean_ascending_run", "ascending_runs_ge6", "rise_share", "half_mean_diff", "trend_spearman", "large_pos_ks_p", "distinct", "median"]
            print(f"{tname} {kname} q={q:.1f}: " + " ".join(f"{s}={summ[s]['obs']:.3g}|{summ[s]['sim_mean']:.3g}±{summ[s]['sim_sd']:.2g}({summ[s]['percentile']:.2f})" for s in show))
            sys.stdout.flush()
save_json(results, "stats_scan_forward.json")
print("done")
