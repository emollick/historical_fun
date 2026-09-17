"""Figures: last-digit shares (tokens vs distinct values), the number sequences themselves
(value against position), and the distinct-count growth curves of the homophone simulations
(from results/stats_homophone_sim.json and results/stats_calibrated_reuse.json).
Writes results/stats_last_digits.svg, stats_sequence_plots.svg, stats_growth_curves.svg."""
import os, json
import numpy as np
from stats_common import *
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

C = load_ciphers()
COLORS = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a"}
TEXT, TEXT2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": TEXT,
                     "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "axes.edgecolor": GRID, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})

# ---- last digits ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
w = 0.27
for ax, level in zip(axes, ("tokens", "types")):
    for j, k in enumerate((1, 2, 3)):
        x = C[k] if level == "tokens" else np.array(sorted(set(C[k].tolist())))
        share = np.bincount(x % 10, minlength=10) / len(x)
        ax.bar(np.arange(10) + (j - 1) * w, share, width=w * 0.92, color=COLORS[k], label=f"B{k} (n={len(x)})")
    ax.axhline(0.1, color=TEXT2, lw=1, ls="--")
    ax.text(9.4, 0.103, "uniform 10%", color=TEXT2, fontsize=8, ha="right", va="bottom")
    ax.set_xticks(range(10)); ax.set_xlabel("last digit")
    ax.set_title("all numbers (tokens)" if level == "tokens" else "distinct values only (types)", loc="left", fontsize=10)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axes[0].set_ylabel("share of numbers")
axes[0].legend(frameon=False, fontsize=8)
fig.suptitle("Last digits: the token-level skew of B2 (a genuine cipher) comes from re-used favourites; distinct values are near-uniform in all three",
             x=0.01, ha="left", fontsize=10, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(RESULTS, "stats_last_digits.svg"))

# ---- sequences -----------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(11, 8.5))
titles = {1: "B1 - locality: lag-1 rank correlation 0.20", 2: "B2 - contents (solved): lag-1 rank correlation 0.20",
          3: "B3 - names: lag-1 rank correlation 0.49, numbers rise in runs (second half larger)"}
for ax, k in zip(axes, (1, 2, 3)):
    x = C[k]
    ax.plot(np.arange(1, len(x) + 1), x, color=COLORS[k], lw=0.9)
    ax.scatter(np.arange(1, len(x) + 1), x, s=5, color=COLORS[k])
    ax.set_yscale("log"); ax.set_ylim(0.8, 4000)
    ax.set_title(titles[k], loc="left", fontsize=10, color=TEXT)
    ax.set_ylabel("number (log scale)")
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if k == 1:
        ax.axhline(1322, color=TEXT2, lw=0.8, ls="--"); ax.text(3, 1450, "1322 words in the DOI", color=TEXT2, fontsize=8)
axes[2].set_xlabel("position in the cipher")
fig.suptitle("The three number sequences in pamphlet order", x=0.01, ha="left", fontsize=11, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(RESULTS, "stats_sequence_plots.svg"))
print("wrote figures")


# ---- growth curves ----------------------------------------------------------------
def place_labels(items, min_gap):
    """items: list of (y, text, color, bold); returns y positions pushed apart by min_gap."""
    order = sorted(range(len(items)), key=lambda i: items[i][0])
    ys = [items[i][0] for i in order]
    for j in range(1, len(ys)):
        if ys[j] - ys[j - 1] < min_gap:
            ys[j] = ys[j - 1] + min_gap
    # centre back around the original mean
    shift = (np.mean([items[i][0] for i in order]) - np.mean(ys))
    ys = [y + shift for y in ys]
    out = [None] * len(items)
    for j, i in enumerate(order):
        out[i] = ys[j]
    return out


with open(os.path.join(RESULTS, "stats_homophone_sim.json")) as f:
    H = json.load(f)
CAL = None
if os.path.exists(os.path.join(RESULTS, "stats_calibrated_reuse.json")):
    with open(os.path.join(RESULTS, "stats_calibrated_reuse.json")) as f:
        CAL = json.load(f)
CN = {"B1": COLORS[1], "B2": COLORS[2], "B3": COLORS[3]}
panel_models = {
    "B1": ["DOI_fitted_prose", "DOI_random_prose", "LONG2906_fitted_prose", "LONG2906_random_prose", "iid_loguniform"],
    "B3": ["DOI_fitted_prose", "DOI_random_prose", "LONG975_fitted_prose", "LONG975_random_prose", "iid_loguniform"],
    "B2": ["DOI_fitted_B2text", "DOI_random_B2text"],
}
labels_m = {"DOI_fitted_prose": "DOI key, fitted encoder", "DOI_random_prose": "DOI key, random homophones",
            "LONG2906_fitted_prose": "2906-word key, fitted encoder", "LONG2906_random_prose": "2906-word key, random homophones",
            "LONG975_fitted_prose": "975-word key, fitted encoder", "LONG975_random_prose": "975-word key, random homophones",
            "iid_loguniform": "i.i.d. log-uniform numbers", "DOI_fitted_B2text": "fitted encoder, B2's own text",
            "DOI_random_B2text": "random homophones, B2's own text", "CAL_DOI": "DOI key, reuse calibrated",
            "CAL_LONG": "long key, reuse calibrated"}
greys = ["#52514e", "#8a8984", "#b3b2ad", "#d0cfca", "#e0dfda", "#7a6f5a", "#a89f8c"]
fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
for ax, tname in zip(axes, ["B1", "B3", "B2"]):
    T = H["targets"][tname]
    curves = []
    for i, m in enumerate(panel_models[tname]):
        S = T["models"][m]
        curves.append((S["growth_checkpoints"], S["growth_mean"], S["growth_p2.5"], S["growth_p97.5"], greys[i], labels_m[m], "-"))
    if CAL and tname in CAL["targets"]:
        for j, (m, S) in enumerate(CAL["targets"][tname]["models"].items()):
            lab = f"{'DOI' if m == 'DOI' else m + '-word'} key, reuse calibrated (r={S['r_calibrated']:.2f})"
            curves.append((S["growth_checkpoints"], S["growth_mean"], S["growth_p2.5"], S["growth_p97.5"], greys[5 + j], lab, "--"))
    for xs, mean, lo, hi, col, lab, ls in curves:
        ax.fill_between(xs, lo, hi, color=col, alpha=0.25, lw=0)
        ax.plot(xs, mean, color=col, lw=1.2, ls=ls)
    xs = curves[0][0]
    ax.plot(xs, T["observed"]["growth"], color=CN[tname], lw=2.4)
    items = [(c[1][-1], c[5], c[4], False) for c in curves] + [(T["observed"]["growth"][-1], f"{tname} observed", CN[tname], True)]
    ymax = max(max(c[3]) for c in curves) * 1.05
    ys = place_labels(items, ymax * 0.045)
    for (y0, text, col, bold), y in zip(items, ys):
        ax.annotate(text, xy=(xs[-1], y0), xytext=(xs[-1] * 1.04, y), color=col if bold else TEXT2, fontsize=7,
                    va="center", fontweight="bold" if bold else "normal",
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.6))
    ax.set_title(f"{tname}: distinct numbers vs position", loc="left", fontsize=10, color=TEXT)
    ax.set_xlabel("numbers read so far"); ax.set_ylabel("distinct numbers")
    ax.set_xlim(0, xs[-1] * 1.9); ax.set_ylim(0, ymax); ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
fig.suptitle("Growth of the number of distinct cipher numbers: observed vs simulated encoders (bands = central 95% of 1000 simulations)",
             x=0.01, ha="left", fontsize=11, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(RESULTS, "stats_growth_curves.svg"))
print("wrote growth figure")
