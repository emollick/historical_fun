"""Collect the key numbers of every stats_* result file into markdown tables
(results/stats_summary_tables.md) so the notes can quote them without transcription errors."""
import os, json
import numpy as np
from stats_common import *

R = lambda name: json.load(open(os.path.join(RESULTS, name)))
L = []
def add(s=""):
    L.append(s)

# ---- digits -----------------------------------------------------------------------
d = R("stats_digits.json")
add("### Digit tests (stats_02_digits.py; Monte-Carlo p-values, 100 000 draws, seed 20260914)")
add("| test | B1 | B2 | B3 |"); add("|---|---|---|---|")
def row(label, fn):
    add(f"| {label} | " + " | ".join(fn(d["ciphers"][f"B{k}"]) for k in (1, 2, 3)) + " |")
row("last digit vs uniform, all numbers: chi2 (9 df), p", lambda r: f"{r['tokens']['last_digit_chi2']:.1f}, p={r['tokens']['last_digit_p_mc']:.2g}")
row("same, type-randomised null (reuse kept), p", lambda r: f"p={r['tokens']['last_digit_p_type_randomised']:.3f}")
row("last digit vs uniform, distinct values: chi2, p", lambda r: f"{r['types']['last_digit_chi2']:.1f}, p={r['types']['last_digit_p_mc']:.3f}")
row("share even, all numbers (binomial p)", lambda r: f"{r['tokens']['even_frac']:.3f} (p={r['tokens']['even_p_binomial']:.2g})")
row("share even, distinct values (binomial p)", lambda r: f"{r['types']['even_frac']:.3f} (p={r['types']['even_p_binomial']:.2g})")
row("share ending 0 or 5, distinct values (p vs 0.20)", lambda r: f"{r['types']['ending_0_or_5_frac']:.3f} (p={r['types']['ending_0_or_5_p_vs_0.20']:.2g})")
row("share with repeated final digits (dd), distinct values (p vs 0.10)", lambda r: f"{r['types']['repdigit_ending_frac']:.3f} (p={r['types']['repdigit_ending_p_binomial_vs_0.10']:.2g})")
row("last two digits uniform, distinct values (MC p)", lambda r: f"p={r['types']['last_two_digits_chi2_p_mc']:.2g}")
row("first digit vs Benford, all numbers: chi2, p", lambda r: f"{r['tokens']['first_digit_tests']['benford']['chi2']:.1f}, p={r['tokens']['first_digit_tests']['benford']['p_mc']:.2g}")
row("first digit vs Benford, distinct values: chi2, p", lambda r: f"{r['types']['first_digit_tests']['benford']['chi2']:.1f}, p={r['types']['first_digit_tests']['benford']['p_mc']:.2g}")
row("first digit vs uniform on [1,1322], distinct values: p", lambda r: f"p={r['types']['first_digit_tests']['uniform_1_1322']['p_mc']:.2g}")
add()
add("| comparison (chi-square homogeneity, permutation p, 20 000 perms) | last digit, all numbers | last digit, distinct values | first digit, all numbers | first digit, distinct values | share even (Fisher p) |")
add("|---|---|---|---|---|---|")
for a, b in ((1, 2), (3, 2), (1, 3)):
    t = d["pairwise"][f"B{a}_vs_B{b}_tokens"]; y = d["pairwise"][f"B{a}_vs_B{b}_types"]
    add(f"| B{a} vs B{b} | chi2={t['last']['chi2']:.1f}, p={t['last']['p_perm']:.3g} | chi2={y['last']['chi2']:.1f}, p={y['last']['p_perm']:.2f} | "
        f"chi2={t['first']['chi2']:.1f}, p={t['first']['p_perm']:.3g} | chi2={y['first']['chi2']:.1f}, p={y['first']['p_perm']:.2f} | "
        f"{t['even']['frac_a']:.3f} vs {t['even']['frac_b']:.3f} (p={t['even']['p_fisher']:.2f}) |")
add()

# ---- sequential -----------------------------------------------------------------------
s = R("stats_sequential.json")
add("### Serial structure vs shuffles of the same cipher (stats_03_sequential.py; 20 000 permutations)")
add("| statistic | B1 obs (null mean +- sd), p | B2 obs (null), p | B3 obs (null), p |"); add("|---|---|---|---|")
names = [("lag1_pearson", "lag-1 autocorrelation (Pearson)"), ("lag2_pearson", "lag-2 autocorrelation (Pearson)"),
         ("lag1_spearman", "lag-1 rank autocorrelation"), ("lag2_spearman", "lag-2 rank autocorrelation"),
         ("runs_up_down", "runs up and down (count)"), ("close_pairs_le5", "adjacent pairs with |a-b| <= 5 (one-sided: more)"),
         ("close_pairs_le10", "adjacent pairs with |a-b| <= 10 (one-sided: more)"), ("close_pairs_le1", "adjacent pairs with |a-b| <= 1"),
         ("adjacent_equal_last_digit", "adjacent pairs with the same last digit"), ("adjacent_equal_first_digit", "adjacent pairs with the same first digit"),
         ("trend_spearman", "trend: Spearman rho(position, value)"), ("half_mean_diff", "mean of first half minus second half"),
         ("large_number_gap_variance", "variance of gaps between large numbers")]
for key, label in names:
    cells = []
    for k in (1, 2, 3):
        v = s["ciphers"][f"B{k}"].get(key)
        if v is None:
            cells.append("-"); continue
        cells.append(f"{v['observed']:.3g} ({v['null_mean']:.3g} +- {v['null_sd']:.2g}), p={v['p_perm']:.2g}")
    add(f"| {label} | " + " | ".join(cells) + " |")
for k in (1, 2, 3):
    v = s["ciphers"][f"B{k}"]["runs_up_down"]; lp = s["ciphers"][f"B{k}"]["large_number_positions"]
    add(f"- B{k}: runs test asymptotic z = {v['asymptotic_z']:.2f} (p = {v['asymptotic_p']:.3g}); positions of the {lp['n_large']} numbers above {lp['threshold']:.0f}: KS vs uniform p = {lp['ks_p']:.3f}")
add()
add("Alphabetic runs in the DOI decode (longest non-decreasing run of decoded letters; p = share of 5000 shuffles of the same letters with a run at least as long):")
add("| key | B1 | B2 | B3 |"); add("|---|---|---|---|")
ar = s["alphabetic_runs_in_DOI_decode"]
for kv, label in (("pamphlet_numbering", "pamphlet numbering (as cipher 2 was decoded)"), ("gillogly_split", "straight count, self-evident split (Gillogly's Table I)"), ("straight", "straight count")):
    cells = []
    for k in (1, 2, 3):
        v = ar[f"{kv}_B{k}"]; q = v["longest_nondecreasing_run_break_oob"]
        cells.append(f"{int(q['observed'])} ('{v['longest_run_text']}' at {v['longest_run_start_pos']}), null {q['null_mean']:.1f}, p={q['p_perm']:.2g}")
    add(f"| {label} | " + " | ".join(cells) + " |")
add()
e = R("stats_serial_extras.json")
add("### Serial extras (stats_08_serial_extras.py; 5000 permutations)")
add("| statistic | B2, letter-preserving shuffle: obs (null), p | B2, full shuffle | B1, full shuffle | B3, full shuffle |"); add("|---|---|---|---|---|")
for key in ["lag1_spearman", "lag2_spearman", "lag1_pearson", "close_le5", "close_le10", "runs_up_down", "longest_ascending_run", "ascending_runs_ge4", "ascending_runs_ge6", "mean_ascending_run"]:
    cells = []
    for blk in ["B2_letter_preserving_shuffle", "B2_full_shuffle", "B1_full_shuffle", "B3_full_shuffle"]:
        v = e[blk][key]
        p = v["p_greater"] if key not in ("runs_up_down",) else v["p_less"]
        cells.append(f"{v['obs']:.3g} ({v['null_mean']:.3g} +- {v['null_sd']:.2g}), p={p:.2g}")
    add(f"| {key} | " + " | ".join(cells) + " |")
add()

# ---- homophone simulation -----------------------------------------------------------------
h = R("stats_homophone_sim.json")
add("### Homophone-reuse simulation (stats_04_homophone_sim.py; 1000 simulations per model)")
f = h["fit"]
add(f"Encoder fitted to B2: reuse probability by number of homophones already used d: " +
    ", ".join(f"d={b['d_lo']}-{b['d_hi']}: {b['p']:.2f} (n={b['n']})" for b in f["p_reuse_by_d"] if b["p"] is not None) +
    f"; overall {f['p_reuse_global']:.3f}; logistic on log d: {f['logistic_beta_logd'][0]:.2f} + {f['logistic_beta_logd'][1]:.2f} log d; "
    f"reuse weight count^gamma with gamma = {f['gamma']:.1f}; new-number weight exp(-n/tau) with tau = {f['tau']:.0f} "
    f"(log-likelihood {f['tau_loglik_max']:.1f} vs {f['tau_loglik_uniform']:.1f} for uniform choice among unused homophones); slip rate {f['slip_rate']:.4f}.")
add()
metrics = [("distinct", "distinct numbers"), ("types_once_frac", "share of types used once"), ("top1", "count of the commonest number"),
           ("top10_share", "share of tokens in the 10 commonest"), ("zipf_slope30", "Zipf slope (top 30)"), ("lag1_spearman", "lag-1 rank autocorrelation"),
           ("runs_z", "runs-up-and-down z"), ("close_le5", "adjacent pairs |a-b|<=5"), ("adj_equal_last_digit", "adjacent same last digit"),
           ("zero_end_frac_types", "share of types ending in 0"), ("even_frac_types", "share of types even"), ("frac_le_100", "share of numbers <= 100"), ("median", "median")]
for tname in ("B1", "B3", "B2"):
    T = h["targets"][tname]
    add(f"**{tname}** (observed value | simulated mean +- sd | percentile of the observed value among simulations)")
    add("| statistic | observed | " + " | ".join(T["models"].keys()) + " |")
    add("|---|---|" + "---|" * len(T["models"]))
    for key, label in metrics:
        cells = []
        for m, S in T["models"].items():
            v = S[key]; cells.append(f"{v['sim_mean']:.3g} +- {v['sim_sd']:.2g} (pct {v['percentile']:.3f})")
        add(f"| {label} | {T['observed'][key]:.3g} | " + " | ".join(cells) + " |")
    add(f"- top-10 counts observed: {T['observed']['top10']}; simulated means: " + "; ".join(f"{m}: {[round(v,1) for v in S['top10_sim_mean']]}" for m, S in T["models"].items()))
    add()
if os.path.exists(os.path.join(RESULTS, "stats_calibrated_reuse.json")):
    c = R("stats_calibrated_reuse.json")
    add("### Calibrated-reuse (best-case) homophonic models (stats_09_calibrated_reuse.py)")
    for tname in ("B1", "B3"):
        T = c["targets"][tname]
        add(f"**{tname}**: " + "; ".join(f"{m}: reuse probability calibrated to r = {S['r_calibrated']:.2f}, tau = {S['tau']:.0f}" for m, S in T["models"].items()))
        add("| statistic | observed | " + " | ".join(T["models"].keys()) + " |"); add("|---|---|" + "---|" * len(T["models"]))
        for key, label in metrics:
            cells = [f"{S[key]['sim_mean']:.3g} +- {S[key]['sim_sd']:.2g} (pct {S[key]['percentile']:.3f})" for m, S in T["models"].items()]
            add(f"| {label} | {T['observed'][key]:.3g} | " + " | ".join(cells) + " |")
        for m, S in T["models"].items():
            add(f"- {m}: top-10 counts observed {S['top10_obs']}, simulated mean {[round(v,1) for v in S['top10_sim_mean']]}, 2.5% {[round(v,1) for v in S['top10_sim_p2.5']]}, 97.5% {[round(v,1) for v in S['top10_sim_p97.5']]}")
        add()

# ---- scan-forward mixed encoder -----------------------------------------------------------
if os.path.exists(os.path.join(RESULTS, "stats_scan_forward.json")):
    sf = R("stats_scan_forward.json")
    add(f"### Scan-forward mixed encoder (stats_10_scan_forward.py; {sf['nsim']} simulations per grid point, seed {sf['seed']})")
    b = sf["b2_forward_moves"]
    add(f"B2: nearest-forward-homophone moves {b['forward_moves']} of {b['n_steps']} steps against {b['forward_null_mean']:.1f} +- {b['forward_null_sd']:.1f} "
        f"under letter-preserving shuffles (p = {b['forward_p']:.4f}); nearest-backward moves {b['backward_moves']} against "
        f"{b['backward_null_mean']:.1f} +- {b['backward_null_sd']:.1f} (p = {b['backward_p']:.3f}).")
    add()
    ser = [("lag1_pearson", "lag-1 autocorrelation (Pearson)"), ("lag1_spearman", "lag-1 autocorrelation (rank)"),
           ("lag2_pearson", "lag-2 autocorrelation (Pearson)"), ("lag2_spearman", "lag-2 autocorrelation (rank)"),
           ("mean_ascending_run", "mean length of strictly rising runs"), ("ascending_runs_ge4", "rising runs of length >= 4"),
           ("ascending_runs_ge6", "rising runs of length >= 6"), ("longest_ascending_run", "longest rising run"),
           ("rise_share", "share of rising steps"), ("runs_z", "runs-up-and-down z"), ("close_le10", "adjacent pairs |a-b| <= 10"),
           ("trend_spearman", "trend (rank correlation of value with position)"), ("half_mean_diff", "mean of first half minus second half"),
           ("large_pos_ks_p", "KS p for positions of the top-decile numbers"), ("distinct", "distinct numbers"), ("median", "median")]
    for tname in ("B2", "B1", "B3"):
        T = sf["targets"][tname]
        add(f"**{tname}** (q = probability of taking the nearest forward homophone; otherwise the fitted encoder for B2, the calibrated encoder for B1/B3; simulated mean +- sd, percentile of the observed value)")
        add("| statistic | observed | " + " | ".join(T["models"].keys()) + " |")
        add("|---|---|" + "---|" * len(T["models"]))
        for key, label in ser:
            cells = [f"{S[key]['sim_mean']:.3g} +- {S[key]['sim_sd']:.2g} ({S[key]['percentile']:.2f})" for m, S in T["models"].items()]
            add(f"| {label} | {T['observed'][key]:.3g} | " + " | ".join(cells) + " |")
        add()

# ---- autocorrelation function ---------------------------------------------------------------
if os.path.exists(os.path.join(RESULTS, "stats_acf.json")):
    ac = R("stats_acf.json")
    add(f"### Autocorrelation at lags 1-10 and block-level variance (stats_11_acf.py; {ac['nshuffle']} shuffles, {ac['nsim']} simulations per model, seed {ac['seed']})")
    add("Block ratio = variance of the means of consecutive blocks of 10 / 20 / 50 numbers divided by its value for exchangeable data (about 1). "
        "'detrended' = after removing a least-squares line of value on position (the calibrated encoders drift upward because they spend the early words of the key first).")
    for tname in ("B1", "B2", "B3"):
        Rc = ac["ciphers"][tname]
        add(f"**{tname}**")
        add("| statistic | " + " | ".join(f"lag {k}" for k in ac["lags"]) + " |"); add("|---|" + "---|" * len(ac["lags"]))
        for kind, label in (("pearson", "Pearson"), ("spearman", "rank"), ("pearson_detr", "Pearson, detrended")):
            o = Rc[kind]
            add(f"| observed ({label}) | " + " | ".join(f"{v:.3f}" for v in o["obs"]) + " |")
            add(f"| shuffles 97.5 % ({label}) | " + " | ".join(f"{v:.3f}" for v in o["p97.5"]) + " |")
            add(f"| percentile of observed among shuffles ({label}) | " + " | ".join(f"{v:.3f}" for v in o["percentile"]) + " |")
            for m, S in Rc["models"].items():
                add(f"| {m} mean +- sd ({label}) | " + " | ".join(f"{a:.3f} +- {b:.3f}" for a, b in zip(S[kind]["sim_mean"], S[kind]["sim_sd"])) + " |")
                add(f"| percentile of observed among {m} ({label}) | " + " | ".join(f"{v:.2f}" for v in S[kind]["percentile"]) + " |")
        for kind, label in (("block_ratio", "block ratio"), ("block_ratio_detr", "block ratio, detrended")):
            o = Rc[kind]
            add(f"- {label} (blocks of {ac['blocks']}): observed {[round(v, 2) for v in o['obs']]}; shuffles {[round(v, 2) for v in o['sim_mean']]} +- {[round(v, 2) for v in o['sim_sd']]}, "
                f"upper-tail p {[round(v, 4) for v in o['p_upper']]}; " + "; ".join(f"{m}: {[round(v, 2) for v in S[kind]['sim_mean']]} +- {[round(v, 2) for v in S[kind]['sim_sd']]} (pct {[round(v, 2) for v in S[kind]['percentile']]})" for m, S in Rc["models"].items()))
        add()

# ---- letter frequencies -----------------------------------------------------------------
lf = R("stats_letterfreq.json")
add("### Letter frequencies of the DOI decode (stats_05_letterfreq.py; 4000 locally shuffled keys)")
add("| key | cipher | decoded (out of range) | KL to English | KL to key initials | chi2 vs re-weighted-key expectation (p, MC) | KL to English under the null (mean) | p(closer to English than null) | letters with z > 3 |")
add("|---|---|---|---|---|---|---|---|---|")
for kname in ("resolved", "straight"):
    for cname in ("B1", "B3", "B2"):
        r = lf["keys"][kname]["ciphers"][cname]; v = r["vs_local_shuffle_null"]
        add(f"| {kname} | {cname} | {r['n_decoded']} ({r['n_out_of_range']}) | {r['vs_english']['kl_obs_ref']:.3f} | {r['vs_key_initials']['kl_obs_ref']:.3f} | "
            f"{v['chi2']:.1f} (p={v['p_mc']:.3f}) | {v['kl_null_vs_english_mean']:.3f} | {v['p_closer_to_english_than_null']:.3f} | {r['letters_z_gt_3']} |")
add()
for cname in ("B1", "B3", "B2"):
    r = lf["keys"]["resolved"]["ciphers"][cname]
    top = sorted(zip(ALPHA, r["probs"]), key=lambda t: -t[1])[:10]
    add(f"- {cname} decode (pamphlet numbering), commonest letters: " + ", ".join(f"{c} {p:.3f}" for c, p in top))
add("- English (Norvig): " + ", ".join(f"{c} {p:.3f}" for c, p in sorted(zip(ALPHA, lf['english_probs']), key=lambda t: -t[1])[:10]))
add("- key initials (pamphlet numbering): " + ", ".join(f"{c} {p:.3f}" for c, p in sorted(zip(ALPHA, lf['keys']['resolved']['key_initial_probs']), key=lambda t: -t[1])[:10]))
add()

# ---- capacity -----------------------------------------------------------------------
cp = R("stats_capacity.json")
add("### Capacity of cipher 3 (stats_06_capacity.py; 20 000 Monte-Carlo lists of 30 entries)")
add("| scenario | description | mean letters | sd | 1st pct | 5th pct | P(total <= 618) |"); add("|---|---|---|---|---|---|---|")
for k, v in cp["scenarios"].items():
    add(f"| {k} | {v['description']} | {v['mean']:.0f} | {v['sd']:.0f} | {v['p1']:.0f} | {v['p5']:.0f} | {v['P_total_le_618']:.4f} |")
add()
for k, v in cp["associate_pools"].items():
    add(f"- name lengths, {k}: n = {v['n']}, first name mean {v['first_mean']:.2f}, surname mean {v['last_mean']:.2f}, full name mean {v['full_mean']:.2f} (sd {v['full_sd']:.2f})")
for k, v in cp["relative_pools"].items():
    add(f"- name lengths, {k}: n = {v['n']}, first name mean {v['first_mean']:.2f}, surname mean {v['last_mean']:.2f}")
add(f"- {cp['n_counties_1822']} Virginia counties/cities formed by 1822: mean name length {cp['county_name_len_mean']:.2f} letters, shortest {cp['county_name_len_min']}")
add()
with open(os.path.join(RESULTS, "stats_summary_tables.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
