"""Autocorrelation function (lags 1-10) and block-level variance of B1, B2 and B3, against shuffles
of each cipher and against the scan-forward mixed encoder of stats_10 at the q values that come
closest to each cipher's lag-1 autocorrelation (B2: q = 0.1; B1: q = 0.1, 0.2; B3: q = 0.3, 0.6).
The question: is the serial dependence of B3 the saw-tooth kind that forward scanning produces
(correlation confined to rising runs, decaying fast with lag), or the slow-wave kind (correlation
persisting over many lags, block means varying far more than chance)?
Writes results/stats_acf.json and results/stats_acf.svg.
"""
import os, json, sys
import numpy as np
from scipy import stats
from stats_common import *
from stats_simlib import *
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

SEED = 20260917
NSIM = int(os.environ.get("NSIM", "300"))
NSHUF = 2000
LAGS = list(range(1, 11))
BLOCKS = [10, 20, 50]
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
prose_doi = filtered(prose, doi_key)


def acf(x, rank=False):
    x = np.asarray(x, float)
    if rank:
        x = stats.rankdata(x)
    return np.array([np.corrcoef(x[:-k], x[k:])[0, 1] for k in LAGS])


def detrend(x):
    """Residuals of an ordinary least-squares line of value on position (removes linear drift, including the
    upward drift the calibrated encoder produces by spending the early words of the key first)."""
    x = np.asarray(x, float); t = np.arange(len(x), dtype=float)
    b = np.polyfit(t, x, 1)
    return x - np.polyval(b, t)


def block_ratios(x):
    """Variance of block means divided by its i.i.d. expectation (var(x)/b); about 1 for exchangeable data."""
    x = np.asarray(x, float); out = []
    for b in BLOCKS:
        n = len(x) // b * b
        m = x[:n].reshape(-1, b).mean(1)
        out.append(m.var(ddof=1) / (x.var(ddof=1) / b))
    return np.array(out)


def encode_scan(text, key, rng, q, p_reuse_fn, tau):
    """Same encoder as stats_10_scan_forward.py: with probability q take the nearest forward homophone."""
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


def window(L):
    s = rng.integers(0, len(prose_doi) - L)
    return prose_doi[s:s + L]


def summ(sim, obs):
    sim = np.asarray(sim, float)
    return {"obs": [float(v) for v in obs], "sim_mean": sim.mean(0).tolist(), "sim_sd": sim.std(0).tolist(),
            "p2.5": np.percentile(sim, 2.5, axis=0).tolist(), "p97.5": np.percentile(sim, 97.5, axis=0).tolist(),
            "percentile": (sim <= np.asarray(obs)).mean(0).tolist()}


MODELS = {"B1": [0.1, 0.2], "B2": [0.1], "B3": [0.3, 0.6]}
results = {"seed": SEED, "nsim": NSIM, "nshuffle": NSHUF, "lags": LAGS, "blocks": BLOCKS, "ciphers": {}}
FIGURE_ONLY = bool(os.environ.get("FIGURE_ONLY"))   # FIGURE_ONLY=1 redraws the figure from the saved JSON
if FIGURE_ONLY:
    with open(os.path.join(RESULTS, "stats_acf.json")) as f:
        results = json.load(f)
for tname, k in (() if FIGURE_ONLY else (("B1", 1), ("B2", 2), ("B3", 3))):
    x = np.array(C[k]); L = len(x)
    def allstats(y):
        yd = detrend(y)
        return {"pearson": acf(y), "spearman": acf(y, True), "block_ratio": block_ratios(y),
                "pearson_detr": acf(yd), "spearman_detr": acf(yd, True), "block_ratio_detr": block_ratios(yd)}
    KEYS = ["pearson", "spearman", "block_ratio", "pearson_detr", "spearman_detr", "block_ratio_detr"]
    obs = allstats(x)
    sh = {k: [] for k in KEYS}
    for _ in range(NSHUF):
        st = allstats(rng.permutation(x))
        for k in KEYS:
            sh[k].append(st[k])
    R = {"n": L}
    for k in KEYS:
        R[k] = summ(sh[k], obs[k])
    for k in ("block_ratio", "block_ratio_detr"):
        arr = np.array(sh[k]); R[k]["p_upper"] = [perm_pvalue(int((arr[:, i] >= obs[k][i]).sum()), NSHUF) for i in range(len(BLOCKS))]
    obs_p, obs_b = obs["pearson"], obs["block_ratio"]
    R["lag2_over_lag1_pearson"] = float(obs_p[1] / obs_p[0]) if obs_p[0] > 0.05 else None
    R["models"] = {}
    pr = p_reuse_fit if tname == "B2" else (lambda d, r=CAL["targets"][tname]["models"]["DOI"]["r_calibrated"]: r)
    for q in MODELS[tname]:
        sm = {k: [] for k in KEYS}; ratio = []
        for _ in range(NSIM):
            st = allstats(encode_scan(window(L), doi_key, rng, q, pr, tau0))
            for k in KEYS:
                sm[k].append(st[k])
            a = st["pearson"]; ratio.append(a[1] / a[0] if a[0] > 0.05 else np.nan)
        ratio = np.array(ratio); ratio = ratio[~np.isnan(ratio)]
        M = {k: summ(sm[k], obs[k]) for k in KEYS}
        M["lag2_over_lag1_pearson_sim_mean"] = float(ratio.mean()) if len(ratio) else None
        M["lag2_over_lag1_pearson_sim_sd"] = float(ratio.std()) if len(ratio) else None
        R["models"][f"DOI_q{q:.1f}"] = M
    results["ciphers"][tname] = R
    print(tname, "ACF pearson obs", np.round(obs_p, 3).tolist())
    print("   shuffle 97.5%", np.round(R["pearson"]["p97.5"], 3).tolist())
    for m, S in R["models"].items():
        print("   ", m, "sim mean", np.round(S["pearson"]["sim_mean"], 3).tolist(), "pct", np.round(S["pearson"]["percentile"], 2).tolist())
    print("   detrended ACF obs", np.round(obs["pearson_detr"], 3).tolist())
    for m, S in R["models"].items():
        print("   ", m, "detrended sim mean", np.round(S["pearson_detr"]["sim_mean"], 3).tolist(), "pct", np.round(S["pearson_detr"]["percentile"], 2).tolist())
    print("   block ratios obs", np.round(obs_b, 2).tolist(), "shuffle p_upper", R["block_ratio"]["p_upper"],
          "| models:", {m: np.round(S["block_ratio"]["sim_mean"], 2).tolist() for m, S in R["models"].items()})
    print("   detrended block ratios obs", np.round(obs["block_ratio_detr"], 2).tolist(), "shuffle p_upper", R["block_ratio_detr"]["p_upper"],
          "| models:", {m: (np.round(S["block_ratio_detr"]["sim_mean"], 2).tolist(), np.round(S["block_ratio_detr"]["percentile"], 2).tolist()) for m, S in R["models"].items()})
    sys.stdout.flush()
if not FIGURE_ONLY:
    save_json(results, "stats_acf.json")

# ---- figure -----------------------------------------------------------------------------------
COL = {"B1": "#2a78d6", "B2": "#eb6834", "B3": "#1baf7a"}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
TITLE = {"B1": "Cipher 1 (520 numbers)", "B2": "Cipher 2 (762, solved)", "B3": "Cipher 3 (618)"}
fig, axes = plt.subplots(2, 3, figsize=(11, 6.6), sharey=True)
fig.patch.set_facecolor(SURF)
lags = np.array(LAGS)
for j, tname in enumerate(("B1", "B2", "B3")):
    R = results["ciphers"][tname]
    for i, kind in enumerate(("pearson", "pearson_detr")):
        ax = axes[i, j]; ax.set_facecolor(SURF)
        ax.fill_between(lags, R[kind]["p2.5"], R[kind]["p97.5"], color=GRID, lw=0, label="shuffles, central 95 %")
        if i == 1:
            for (m, S), ls in zip(R["models"].items(), ["--", ":"]):
                ax.fill_between(lags, S[kind]["p2.5"], S[kind]["p97.5"], color=COL[tname], alpha=0.12, lw=0)
                ax.plot(lags, S[kind]["sim_mean"], ls=ls, color=INK2, lw=1.6, label=f"scan-forward q = {m.split('q')[1]}")
        ax.plot(lags, R[kind]["obs"], "-o", color=COL[tname], lw=2, ms=5, label=f"{tname} observed")
        ax.set_ylim(-0.22, 0.72)
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(TITLE[tname] + (", trend removed" if i else ""), color=INK, fontsize=10.5, loc="left")
        ax.set_xticks(lags); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
        for sp_ in ("top", "right"):
            ax.spines[sp_].set_visible(False)
        ax.tick_params(colors=INK2)
        if i == 1:
            ax.set_xlabel("lag", color=INK2)
            ax.legend(frameon=False, fontsize=8, loc="upper right", labelcolor=INK2, handlelength=2.2)
        elif j == 2:
            ax.legend(frameon=False, fontsize=8, loc="upper right", labelcolor=INK2, handlelength=2.2)
    axes[0, 0].set_ylabel("autocorrelation (Pearson)", color=INK2)
    axes[1, 0].set_ylabel("autocorrelation (Pearson)", color=INK2)
fig.suptitle("Autocorrelation of the number sequence, lags 1-10: against shuffles (top); trend removed, against the scan-forward encoder (bottom)",
             x=0.01, ha="left", fontsize=10, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(RESULTS, "stats_acf.svg"), facecolor=SURF)
print("figure written")
