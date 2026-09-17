"""Shared pieces of the homophone simulator (see stats_04_homophone_sim.py for the model
description).  Everything is a plain function so other scripts can re-use it."""
import os, json
from collections import Counter, defaultdict
import numpy as np
from scipy import stats
from stats_common import *


class Key:
    def __init__(self, initials):
        self.hom = defaultdict(list)
        for i, c in enumerate(initials):
            if c:
                self.hom[c].append(i + 1)
        self.hom = {k: np.array(v) for k, v in self.hom.items()}
        self.K = len(initials)


def filtered(text, key):
    return "".join(c for c in text if c in key.hom)


def encode_fitted(text, key, rng, p_reuse_fn, gamma, tau, eps):
    """the fitted encoder: reuse with probability p_reuse_fn(d) (d = distinct numbers already
    used for the letter), reuse weights count^gamma, new numbers with weight exp(-n/tau),
    slips +-1 with probability eps."""
    out = []
    usedc = {L: {} for L in key.hom}
    w_new = {L: np.exp(-key.hom[L] / tau) for L in key.hom}
    unused = {L: np.ones(len(key.hom[L]), bool) for L in key.hom}
    for L in text:
        if L not in key.hom:
            continue
        U = usedc[L]; d = len(U)
        can_new = unused[L].any()
        if d > 0 and ((not can_new) or rng.random() < p_reuse_fn(d)):
            nums = list(U); w = np.array([U[x] for x in nums], float) ** gamma
            n = nums[rng.choice(len(nums), p=w / w.sum())]
        else:
            w = w_new[L] * unused[L]; idx = rng.choice(len(w), p=w / w.sum())
            n = int(key.hom[L][idx]); unused[L][idx] = False
        U[n] = U.get(n, 0) + 1
        out.append(n)
    out = np.array(out)
    if eps > 0:
        slip = rng.random(len(out)) < eps
        out[slip] = np.maximum(1, out[slip] + rng.choice([-1, 1], size=int(slip.sum())))
    return out


def encode_random(text, key, rng):
    return np.array([int(rng.choice(key.hom[L])) for L in text if L in key.hom])


CHECK = np.arange(20, 800, 20)


def growth(x):
    seen = set(); g = []
    for i, v in enumerate(x):
        seen.add(v)
        if (i + 1) in CHECK:
            g.append(len(seen))
    return g


def zipf_slope(counts, top=30):
    c = np.sort(np.asarray(counts))[::-1][:top]
    r = np.arange(1, len(c) + 1)
    if len(c) < 3:
        return np.nan
    return float(np.polyfit(np.log(r), np.log(c), 1)[0])


def seq_stats(x):
    x = np.asarray(x); n = len(x)
    cnt = Counter(x.tolist()); counts = np.array(sorted(cnt.values(), reverse=True))
    types = np.array(sorted(cnt))
    rk = stats.rankdata(x)
    d = np.sign(np.diff(x.astype(float))); d = d[d != 0]
    runs = 1 + int((d[1:] != d[:-1]).sum()) if len(d) else 0
    ne = len(d) + 1
    runs_z = (runs - (2 * ne - 1) / 3) / np.sqrt((16 * ne - 29) / 90) if ne > 2 else np.nan
    ld = x % 10; ldt = types % 10
    ldc_t = np.bincount(ldt, minlength=10)
    chi_ld_t = float(((ldc_t - len(types) / 10) ** 2 / (len(types) / 10)).sum())
    fd_t = np.array([int(str(v)[0]) for v in types]); fdc = np.bincount(fd_t, minlength=10)[1:]
    benf = np.log10(1 + 1 / np.arange(1, 10)) * len(types)
    chi_benf_t = float(((fdc - benf) ** 2 / benf).sum())
    top10 = counts[:10].tolist() + [0] * max(0, 10 - len(counts))
    return {
        "n": n, "distinct": len(cnt), "distinct_frac": len(cnt) / n, "reuse_rate": 1 - len(cnt) / n,
        "types_once_frac": float((counts == 1).mean()), "top1": int(counts[0]), "top10_sum": int(counts[:10].sum()),
        "top10_share": float(counts[:10].sum() / n), "top10": top10, "zipf_slope30": zipf_slope(counts),
        "lag1_pearson": float(np.corrcoef(x[:-1], x[1:])[0, 1]),
        "lag1_spearman": float(np.corrcoef(rk[:-1], rk[1:])[0, 1]),
        "lag2_spearman": float(np.corrcoef(rk[:-2], rk[2:])[0, 1]),
        "runs_z": float(runs_z),
        "close_le5": int((np.abs(np.diff(x)) <= 5).sum()), "close_le10": int((np.abs(np.diff(x)) <= 10).sum()),
        "adj_equal_last_digit": int((ld[1:] == ld[:-1]).sum()),
        "even_frac_types": float((types % 2 == 0).mean()), "zero_end_frac_types": float((ldt == 0).mean()),
        "chi2_last_digit_types": chi_ld_t, "chi2_benford_types": chi_benf_t,
        "max": int(x.max()), "median": float(np.median(x)), "mean": float(x.mean()),
        "n_gt_1322": int((x > 1322).sum()), "frac_le_100": float((x <= 100).mean()),
        "growth": growth(x),
    }


SCALARS = ["distinct", "distinct_frac", "types_once_frac", "top1", "top10_sum", "top10_share", "zipf_slope30",
           "lag1_pearson", "lag1_spearman", "lag2_spearman", "runs_z", "close_le5", "close_le10",
           "adj_equal_last_digit", "even_frac_types", "zero_end_frac_types", "chi2_last_digit_types",
           "chi2_benford_types", "max", "median", "mean", "n_gt_1322", "frac_le_100"]


def summarize(rows, obs):
    out = {}
    for k in SCALARS:
        sim = np.array([r[k] for r in rows], float)
        sim = sim[~np.isnan(sim)]
        o = obs[k]
        if len(sim) == 0:
            continue
        pct = float((sim <= o).mean())
        p_two = min(1.0, 2 * min((int((sim <= o).sum()) + 1) / (len(sim) + 1), (int((sim >= o).sum()) + 1) / (len(sim) + 1)))
        out[k] = {"obs": o, "sim_mean": float(sim.mean()), "sim_sd": float(sim.std()),
                  "sim_p2.5": float(np.percentile(sim, 2.5)), "sim_p97.5": float(np.percentile(sim, 97.5)),
                  "percentile": pct, "p_two_sided": p_two, "mc_se": mc_se(pct, len(sim))}
    g = np.array([r["growth"] for r in rows], float)
    out["growth_mean"] = g.mean(axis=0).tolist(); out["growth_p2.5"] = np.percentile(g, 2.5, axis=0).tolist()
    out["growth_p97.5"] = np.percentile(g, 97.5, axis=0).tolist()
    out["growth_obs"] = obs["growth"]
    out["growth_checkpoints"] = CHECK[:len(obs["growth"])].tolist()
    t10 = np.array([r["top10"] for r in rows], float)
    out["top10_sim_mean"] = t10.mean(axis=0).tolist()
    out["top10_sim_p2.5"] = np.percentile(t10, 2.5, axis=0).tolist()
    out["top10_sim_p97.5"] = np.percentile(t10, 97.5, axis=0).tolist()
    out["top10_obs"] = obs["top10"]
    return out


def load_keys_and_texts():
    with open(os.path.join(RESULTS, "stats_key_check.json")) as f:
        KC = json.load(f)
    doi_key = Key(KC["best_initials"])
    with open(os.path.join(DATA, "narrative_anonymous_author.txt")) as f:
        narr = f.read()
    with open(os.path.join(DATA, "morriss_statement.txt")) as f:
        narr += " " + f.read()
    narr_ini = [c for c in (word_initial(w) for w in narr.split()) if c]
    long_keys = {2906: Key(narr_ini[:2906]), 975: Key(narr_ini[:975])}
    prose = load_prose_letters()
    names_pt = None
    fn = os.path.join(RESULTS, "stats_capacity_names_plaintext.txt")
    if os.path.exists(fn):
        with open(fn) as f:
            names_pt = letters_only(f.read())
    return KC, doi_key, long_keys, prose, names_pt
