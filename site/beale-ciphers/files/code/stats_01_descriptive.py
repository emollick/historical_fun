"""Task 1: descriptive statistics of the three Beale ciphers, side by side.
Writes results/stats_descriptive.json, results/stats_descriptive_tables.md and
results/stats_hist_values.svg.  Straight-count key length is 1321 words (1322 with
"self-evident" split, as in Gillogly 1980, Table I); the pamphlet's own printed numbering
runs to 1310.
"""
import os
from collections import Counter
import numpy as np
from stats_common import *

import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

C = load_ciphers()
KEYLEN = 1322   # Gillogly's count of the DOI as printed in the pamphlet
COLORS = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a"}   # fixed slots: B1 blue, B2 orange, B3 aqua
TEXT, TEXT2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e1"


def describe(x):
    x = np.asarray(x)
    cnt = Counter(x.tolist())
    n = len(x)
    distinct = len(cnt)
    singles = sum(1 for v in cnt.values() if v == 1)
    top = cnt.most_common(15)
    large = sorted(int(v) for v in x if v > KEYLEN)
    first = Counter(int(str(v)[0]) for v in x)
    last = Counter(int(v % 10) for v in x)
    nd = Counter(len(str(v)) for v in x)
    types = np.array(sorted(cnt))
    first_t = Counter(int(str(v)[0]) for v in types)
    last_t = Counter(int(v % 10) for v in types)
    q = np.percentile(x, [10, 25, 50, 75, 90])
    d = {
        "n": n, "min": int(x.min()), "max": int(x.max()), "mean": float(x.mean()),
        "median": float(np.median(x)), "sd": float(x.std(ddof=1)),
        "quantiles_10_25_50_75_90": q.tolist(),
        "distinct": distinct, "distinct_frac": distinct / n,
        "tokens_per_type": n / distinct,
        "types_used_once": singles, "types_used_once_frac": singles / distinct,
        "tokens_that_are_singletons_frac": singles / n,
        "top15": [[int(v), int(c)] for v, c in top],
        "top10_token_share": sum(c for _, c in top[:10]) / n,
        "n_gt_keylen": len(large), "frac_gt_keylen": len(large) / n,
        "n_gt_1005_maxB2": int((x > 1005).sum()), "n_gt_975_maxB3": int((x > 975).sum()),
        "large_values": large,
        "large_by_hundreds": {f"{h}-{h+99}": int(((x >= h) & (x < h + 100)).sum())
                              for h in range(1300, 3000, 100) if ((x >= h) & (x < h + 100)).sum()},
        "frac_le_100": float((x <= 100).mean()), "frac_le_200": float((x <= 200).mean()),
        "frac_le_500": float((x <= 500).mean()), "frac_le_1000": float((x <= 1000).mean()),
        "first_digit_tokens": [first.get(d, 0) for d in range(1, 10)],
        "last_digit_tokens": [last.get(d, 0) for d in range(10)],
        "first_digit_types": [first_t.get(d, 0) for d in range(1, 10)],
        "last_digit_types": [last_t.get(d, 0) for d in range(10)],
        "ndigits_tokens": [nd.get(k, 0) for k in range(1, 5)],
        "even_frac_tokens": float((x % 2 == 0).mean()),
        "even_frac_types": float((types % 2 == 0).mean()),
    }
    return d


res = {k: describe(C[k]) for k in (1, 2, 3)}
save_json(res, "stats_descriptive.json")

# ---- markdown tables -------------------------------------------------------------
L = []
L.append("| statistic | B1 (locality) | B2 (contents, solved) | B3 (names) |")
L.append("|---|---|---|---|")
rows = [
    ("numbers (tokens)", "n", "{:d}"), ("minimum", "min", "{:d}"), ("maximum", "max", "{:d}"),
    ("mean", "mean", "{:.1f}"), ("median", "median", "{:.0f}"), ("s.d.", "sd", "{:.1f}"),
    ("distinct values (types)", "distinct", "{:d}"), ("distinct / n", "distinct_frac", "{:.3f}"),
    ("tokens per type", "tokens_per_type", "{:.2f}"),
    ("types used exactly once", "types_used_once", "{:d}"),
    ("share of types used once", "types_used_once_frac", "{:.3f}"),
    ("share of tokens that are singletons", "tokens_that_are_singletons_frac", "{:.3f}"),
    ("token share of the 10 commonest values", "top10_token_share", "{:.3f}"),
    ("numbers > 1322 (DOI length)", "n_gt_keylen", "{:d}"),
    ("share > 1322", "frac_gt_keylen", "{:.3f}"),
    ("numbers > 1005 (largest in B2)", "n_gt_1005_maxB2", "{:d}"),
    ("share <= 100", "frac_le_100", "{:.3f}"), ("share <= 200", "frac_le_200", "{:.3f}"),
    ("share <= 500", "frac_le_500", "{:.3f}"), ("share <= 1000", "frac_le_1000", "{:.3f}"),
    ("share even (tokens)", "even_frac_tokens", "{:.3f}"), ("share even (types)", "even_frac_types", "{:.3f}"),
]
for label, key, fmt in rows:
    L.append(f"| {label} | " + " | ".join(fmt.format(res[k][key]) for k in (1, 2, 3)) + " |")
L.append("")
L.append("Quantiles (10/25/50/75/90 %): " + "; ".join(
    f"B{k}: " + "/".join(f"{v:.0f}" for v in res[k]["quantiles_10_25_50_75_90"]) for k in (1, 2, 3)))
L.append("")
L.append("Most reused values (value x count):")
for k in (1, 2, 3):
    L.append(f"- B{k}: " + ", ".join(f"{v} x{c}" for v, c in res[k]["top15"]))
L.append("")
L.append("Values above 1322 in B1: " + ", ".join(str(v) for v in res[1]["large_values"]))
L.append("")
L.append("| digit table | B1 tokens | B2 tokens | B3 tokens | B1 types | B2 types | B3 types |")
L.append("|---|---|---|---|---|---|---|")
for d in range(1, 10):
    L.append(f"| first digit {d} | " + " | ".join(str(res[k]['first_digit_tokens'][d-1]) for k in (1,2,3)) +
             " | " + " | ".join(str(res[k]['first_digit_types'][d-1]) for k in (1,2,3)) + " |")
for d in range(10):
    L.append(f"| last digit {d} | " + " | ".join(str(res[k]['last_digit_tokens'][d]) for k in (1,2,3)) +
             " | " + " | ".join(str(res[k]['last_digit_types'][d]) for k in (1,2,3)) + " |")
for nd in range(1, 5):
    L.append(f"| {nd}-digit numbers | " + " | ".join(str(res[k]['ndigits_tokens'][nd-1]) for k in (1,2,3)) + " | | | |")
with open(os.path.join(RESULTS, "stats_descriptive_tables.md"), "w") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))

# ---- histogram figure -----------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": TEXT,
                     "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
                     "axes.edgecolor": GRID, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
fig, axes = plt.subplots(4, 1, figsize=(8.5, 9.5), gridspec_kw={"height_ratios": [1, 1, 1, 1.3]})
bins = np.arange(0, 3001, 50)
labels = {1: f"B1 - locality ({len(C[1])} numbers)", 2: f"B2 - contents, solved ({len(C[2])} numbers as printed)",
          3: f"B3 - names ({len(C[3])} numbers)"}
for ax, k in zip(axes[:3], (1, 2, 3)):
    ax.hist(C[k], bins=bins, color=COLORS[k], edgecolor=SURFACE, linewidth=0.6)
    ax.axvline(KEYLEN, color=TEXT2, lw=1, ls="--")
    ax.text(KEYLEN + 15, ax.get_ylim()[1] * 0.85, "1322 = words in the DOI", color=TEXT2, fontsize=8)
    ax.set_title(labels[k], loc="left", color=TEXT, fontsize=10)
    ax.set_xlim(0, 3000)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_ylabel("count per bin of 50")
axes[2].set_xlabel("cipher number")
ax = axes[3]
for k in (1, 2, 3):
    xs = np.sort(C[k]); ys = np.arange(1, len(xs) + 1) / len(xs)
    ax.step(xs, ys, where="post", color=COLORS[k], lw=2, label=f"B{k}")
ax.set_xlim(0, 1400); ax.set_ylim(0, 1)
ax.axvline(KEYLEN, color=TEXT2, lw=1, ls="--")
ax.set_xlabel("cipher number (0-1400 shown)"); ax.set_ylabel("cumulative share of numbers")
ax.set_title("Empirical cumulative distribution - all three ciphers lean to low numbers", loc="left",
             color=TEXT, fontsize=10)
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.suptitle("Beale ciphers: distribution of the numbers", x=0.01, ha="left", fontsize=12, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(os.path.join(RESULTS, "stats_hist_values.svg"))
print("wrote", os.path.join(RESULTS, "stats_hist_values.svg"))
