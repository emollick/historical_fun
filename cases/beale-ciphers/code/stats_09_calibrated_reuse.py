"""Task 4, continued: the best-case homophonic model for B1 and B3.

The B2 encoder re-used numbers far more than B1/B3 do, and a memoryless homophone encoder far
less.  Here the reuse probability is a constant r, calibrated per target and key so that the
simulated number of distinct values matches the observed one on average (grid search, then
linear interpolation); gamma, tau and the slip rate stay at their B2-fitted values (tau is
scaled with key length for the long keys).  We then ask whether the remaining statistics of
B1/B3 (share of types used once, top-1 and top-10 counts, Zipf slope, growth-curve shape,
serial statistics) are compatible with ANY such homophonic encoding of English.
Writes results/stats_calibrated_reuse.json and results/stats_growth_curves_calibrated.svg.
"""
import os, json, sys
import numpy as np
from stats_common import *
from stats_simlib import *
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

SEED = 20260915
NSIM = int(os.environ.get("NSIM", "1000"))
rng = np.random.default_rng(SEED)
C = load_ciphers()
with open(os.path.join(RESULTS, "stats_homophone_sim.json")) as f:
    FIT = json.load(f)["fit"]
gamma, tau0, eps = FIT["gamma"], FIT["tau"], FIT["slip_rate"]
KC, doi_key, long_keys, prose, names_pt = load_keys_and_texts()
prose_for = {id(k): filtered(prose, k) for k in [doi_key] + list(long_keys.values())}


def window(L, key):
    src = prose_for[id(key)]
    s = rng.integers(0, len(src) - L)
    return src[s:s + L]


def sim(L, key, r, tau, n):
    rows = []
    for _ in range(n):
        rows.append(seq_stats(encode_fitted(window(L, key), key, rng, lambda d: r, gamma, tau, eps)))
    return rows


results = {"seed": SEED, "nsim": NSIM, "gamma": gamma, "tau_doi": tau0, "slip": eps, "targets": {}}
for tname, k, L, longK in (("B1", 1, 520, 2906), ("B3", 3, 618, 975)):
    obs = seq_stats(C[k])
    results["targets"][tname] = {"observed": {q: obs[q] for q in SCALARS + ["growth", "top10"]}, "models": {}}
    for kname, key in (("DOI", doi_key), (f"LONG{longK}", long_keys[longK])):
        tau = tau0 if kname == "DOI" else tau0 * key.K / doi_key.K
        grid = np.arange(0.0, 0.96, 0.1)
        means = []
        for r in grid:
            rows = sim(L, key, r, tau, 120)
            means.append(np.mean([x["distinct"] for x in rows]))
        means = np.array(means)
        # distinct count decreases with r; interpolate to the observed value
        r_star = float(np.interp(-obs["distinct"], -means, grid))
        rows = sim(L, key, r_star, tau, NSIM)
        summ = summarize(rows, obs)
        summ["r_calibrated"] = r_star; summ["tau"] = tau
        summ["grid"] = {"r": grid.tolist(), "mean_distinct": means.tolist()}
        results["targets"][tname]["models"][kname] = summ
        show = ["distinct", "types_once_frac", "top1", "top10_share", "zipf_slope30", "lag1_spearman", "runs_z", "close_le5", "frac_le_100", "median"]
        print(f"{tname} key={kname} r*={r_star:.2f} tau={tau:.0f}: " + " ".join(
            f"{q}={summ[q]['obs']:.3g}|{summ[q]['sim_mean']:.3g}±{summ[q]['sim_sd']:.2g}(pct {summ[q]['percentile']:.3f})" for q in show))
        print("     top10 obs", summ["top10_obs"], " sim mean", [round(v, 1) for v in summ["top10_sim_mean"]],
              " sim 97.5%", [round(v, 1) for v in summ["top10_sim_p97.5"]])
        sys.stdout.flush()
save_json(results, "stats_calibrated_reuse.json")

COLORS = {"B1": "#2a78d6", "B3": "#1baf7a"}
TEXT, TEXT2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": TEXT,
                     "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "axes.edgecolor": GRID, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, tname in zip(axes, ("B1", "B3")):
    T = results["targets"][tname]
    for i, (m, grey) in enumerate(zip(T["models"], ["#52514e", "#b3b2ad"])):
        S = T["models"][m]; xs = S["growth_checkpoints"]
        ax.fill_between(xs, S["growth_p2.5"], S["growth_p97.5"], color=grey, alpha=0.35, lw=0)
        ax.plot(xs, S["growth_mean"], color=grey, lw=1.2)
        ax.text(xs[-1] + 5, S["growth_mean"][-1] + (8 if i == 0 else -8), f"{m} key, reuse r={S['r_calibrated']:.2f}", color=TEXT2, fontsize=7, va="center")
    xs = T["models"]["DOI"]["growth_checkpoints"]
    ax.plot(xs, T["observed"]["growth"], color=COLORS[tname], lw=2.2)
    ax.text(xs[-1] + 5, T["observed"]["growth"][-1] + 20, f"{tname} observed", color=COLORS[tname], fontsize=8, fontweight="bold")
    ax.set_title(f"{tname}: distinct numbers vs position, reuse calibrated to the final count", loc="left", fontsize=9.5)
    ax.set_xlabel("numbers read so far"); ax.set_ylabel("distinct numbers")
    ax.set_xlim(0, xs[-1] * 1.55); ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.suptitle("Best-case homophonic encoders (bands = central 95% of 1000 simulations)", x=0.01, ha="left", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(RESULTS, "stats_growth_curves_calibrated.svg"))
print("wrote figure")
