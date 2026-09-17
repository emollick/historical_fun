"""Task 4: homophone-reuse structure - simulator and comparison.

Encoder model fitted to cipher 2 (letters from the alignment in stats_00_key_check.py,
key = pamphlet numbering with 811=y, 1005=x, 95=u):
  * for each plaintext letter L, with probability p_reuse(d) (d = number of distinct numbers
    already used for L; estimated from B2 in bins of d) the encoder re-uses one of them,
    choosing number n with weight count(n)^gamma (gamma fitted by likelihood);
  * otherwise it takes a not-yet-used homophone of L with weight exp(-n/tau) (tau fitted by
    maximum likelihood on B2's first uses: the encoder preferred early words of the key);
  * a slip (number written +-1) with the rate observed in B2.
Alternative encoders: (a) 'random' - uniform over all homophones of the letter, no memory;
(b) the fitted and random encoders with a hypothetical longer key of 2906 (for B1-length
texts) or 975 words (B3-length), whose initials are taken from the pamphlet's own narrative
prose; (c) i.i.d. uniform numbers on [1, max observed]; (d) i.i.d. log-uniform numbers on
[1, max observed] (a 'human-invented numbers' proxy: scale-free preference for small numbers,
Benford first digits, no memory).
Plaintexts: random windows of the three 'Beale' letters (English prose in the same hand),
and for B3 additionally a synthetic 30-entry list of real Virginia names (task 6).
Writes results/stats_homophone_sim.json and results/stats_growth_curves.svg.
"""
import os, json, sys
from collections import Counter, defaultdict
import numpy as np
from scipy import stats
from stats_common import *

import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

SEED = 20260914
NSIM = int(os.environ.get("NSIM", "1000"))
rng = np.random.default_rng(SEED)
C = load_ciphers()

with open(os.path.join(RESULTS, "stats_key_check.json")) as f:
    KC = json.load(f)
KEY = KC["best_initials"]                       # resolved key, index n-1 -> initial letter
records = KC["b2_alignment"]["records"]
HOM = defaultdict(list)
for i, c in enumerate(KEY):
    if c:
        HOM[c].append(i + 1)
HOM = {k: np.array(v) for k, v in HOM.items()}

# ---------------------------------------------------------------- 1. fit the encoder to B2
used = defaultdict(Counter)
events = []
for r in records:
    L, n = r["intended"], r["number"]
    if L is None:
        continue
    U = used[L]
    d = len(U)
    avail_new = len(HOM.get(L, [])) - len([x for x in U if x in set(HOM.get(L, []).tolist())])
    events.append({"L": L, "n": n, "d": d, "reuse": n in U, "error": r["error"],
                   "counts": dict(U), "avail_new": avail_new})
    U[n] += 1
ev = [e for e in events if e["d"] > 0 and e["avail_new"] > 0]   # a new choice was possible
bins = [(1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 12), (13, 99)]
p_reuse_bins = []
for lo, hi in bins:
    sel = [e for e in ev if lo <= e["d"] <= hi]
    k = sum(e["reuse"] for e in sel)
    p_reuse_bins.append({"d_lo": lo, "d_hi": hi, "n": len(sel), "reuse": k,
                         "p": (k + 0.5) / (len(sel) + 1) if sel else None})
p_reuse_global = sum(e["reuse"] for e in ev) / len(ev)
# logistic fit of reuse on log(d)
X = np.array([[1.0, np.log(e["d"])] for e in ev]); y = np.array([e["reuse"] for e in ev], float)
def nll(beta):
    z = X @ beta; return float(np.sum(np.log1p(np.exp(z)) - y * z))
from scipy.optimize import minimize
beta = minimize(nll, np.zeros(2)).x
def p_reuse(d):
    return 1 / (1 + np.exp(-(beta[0] + beta[1] * np.log(max(d, 1)))))

# gamma: reuse choice ∝ count^gamma (events with reuse and >= 2 used numbers)
rev = [e for e in events if e["reuse"] and len(e["counts"]) >= 2]
def ll_gamma(g):
    s = 0.0
    for e in rev:
        c = np.array(list(e["counts"].values()), float); w = c ** g
        s += np.log(w[list(e["counts"]).index(e["n"])] / w.sum())
    return s
gammas = np.linspace(0, 3, 31); lls = [ll_gamma(g) for g in gammas]
gamma = float(gammas[int(np.argmax(lls))])

# tau: new-choice weight exp(-n/tau) over unused correct homophones
nev = [e for e in events if (not e["reuse"]) and (not e["error"]) and e["L"] in HOM]
def ll_tau(tau):
    s = 0.0
    for e in nev:
        H = HOM[e["L"]]; unused = np.array([h for h in H if h not in e["counts"]])
        if e["n"] not in unused:
            continue
        w = np.exp(-unused / tau); s += np.log(w[np.where(unused == e["n"])[0][0]] / w.sum())
    return s
taus = np.exp(np.linspace(np.log(20), np.log(3000), 60)); llt = [ll_tau(t) for t in taus]
tau = float(taus[int(np.argmax(llt))])
ll_tau_uniform = ll_tau(1e9)
# rank-based alternative: weight exp(-rank/rho), rank = ordinal position among the homophones
def ll_rho(rho):
    s = 0.0
    for e in nev:
        H = HOM[e["L"]]; unused = np.array([h for h in H if h not in e["counts"]])
        if e["n"] not in unused:
            continue
        rk = np.arange(1, len(unused) + 1); w = np.exp(-rk / rho)
        s += np.log(w[np.where(unused == e["n"])[0][0]] / w.sum())
    return s
rhos = np.exp(np.linspace(np.log(0.5), np.log(300), 60)); llr = [ll_rho(r) for r in rhos]
rho = float(rhos[int(np.argmax(llr))])
eps = sum(e["error"] for e in events) / len(events)
fit = {"n_events": len(events), "n_events_reuse_possible": len(ev), "p_reuse_global": p_reuse_global,
       "p_reuse_by_d": p_reuse_bins, "logistic_beta_logd": beta.tolist(),
       "gamma": gamma, "gamma_loglik": dict(zip([f"{g:.1f}" for g in gammas], lls)),
       "tau": tau, "tau_loglik_max": max(llt), "tau_loglik_uniform": ll_tau_uniform,
       "rho_rank_model": rho, "rho_loglik_max": max(llr), "n_new_choice_events": len(nev),
       "slip_rate": eps}
print(f"fit: p_reuse(global)={p_reuse_global:.3f}; by d: " +
      ", ".join(f"d={b['d_lo']}-{b['d_hi']}:{b['p']:.2f}(n={b['n']})" for b in p_reuse_bins if b['p'] is not None))
print(f"     logistic on log d: beta={beta}; gamma={gamma}; tau={tau:.0f} (loglik {max(llt):.1f} vs uniform {ll_tau_uniform:.1f}); "
      f"rank model rho={rho:.1f} (loglik {max(llr):.1f}); slips={eps:.4f}")

# ---------------------------------------------------------------- 2. encoders
class Key:
    def __init__(self, initials):
        self.hom = defaultdict(list)
        for i, c in enumerate(initials):
            if c:
                self.hom[c].append(i + 1)
        self.hom = {k: np.array(v) for k, v in self.hom.items()}
        self.K = len(initials)


def encode_fitted(text, key, rng, p_reuse_fn=p_reuse, gamma=gamma, tau=tau, eps=eps):
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
    slip = rng.random(len(out)) < eps
    out[slip] = np.maximum(1, out[slip] + rng.choice([-1, 1], size=int(slip.sum())))
    return out


def encode_random(text, key, rng):
    out = []
    for L in text:
        if L in key.hom:
            out.append(int(rng.choice(key.hom[L])))
    return np.array(out)


def iid_uniform(L, vmax, rng):
    return rng.integers(1, vmax + 1, size=L)


def iid_loguniform(L, vmax, rng):
    u = rng.random(L) * np.log(vmax + 1)
    return np.clip(np.floor(np.exp(u)).astype(int), 1, vmax)


# ---------------------------------------------------------------- 3. statistics of a sequence
CHECK = np.arange(20, 800, 20)


def growth(x, L):
    seen = set(); g = []
    cnt = 0
    for i, v in enumerate(x):
        if v not in seen:
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
        "growth": growth(x, n),
    }


SCALARS = ["distinct", "distinct_frac", "types_once_frac", "top1", "top10_sum", "top10_share", "zipf_slope30",
           "lag1_pearson", "lag1_spearman", "lag2_spearman", "runs_z", "close_le5", "close_le10",
           "adj_equal_last_digit", "even_frac_types", "zero_end_frac_types", "chi2_last_digit_types",
           "chi2_benford_types", "max", "median", "mean", "n_gt_1322", "frac_le_100"]

# ---------------------------------------------------------------- 4. keys and plaintexts
doi_key = Key(KEY)
with open(os.path.join(DATA, "narrative_anonymous_author.txt")) as f:
    narr = f.read()
with open(os.path.join(DATA, "morriss_statement.txt")) as f:
    narr += " " + f.read()
narr_words = narr.split()
narr_ini = [word_initial(w) for w in narr_words]
narr_ini = [c for c in narr_ini if c]
print("narrative words available for long keys:", len(narr_ini))
long_keys = {2906: Key(narr_ini[:2906]), 975: Key(narr_ini[:975])}
prose = load_prose_letters()
print("prose letters available for plaintext windows:", len(prose))
names_pt = None
fn = os.path.join(RESULTS, "stats_capacity_names_plaintext.txt")
if os.path.exists(fn):
    with open(fn) as f:
        names_pt = letters_only(f.read())
    print("names-list plaintext letters:", len(names_pt))
b2_pt = KC["plaintext_763"]


def filtered(text, key):
    """drop letters that the key cannot encode (e.g. 'z' in the Declaration), so that every
    simulated cipher has exactly L numbers."""
    return "".join(c for c in text if c in key.hom)


prose_for = {id(k): filtered(prose, k) for k in [doi_key] + list(long_keys.values())}
names_for = {id(k): filtered(names_pt, k) for k in [doi_key] + list(long_keys.values())} if names_pt else {}
for k in [doi_key] + list(long_keys.values()):
    missing = sorted(set(ALPHA) - set(k.hom))
    print(f"key with {k.K} positions: letters absent from key {missing}; usable prose letters {len(prose_for[id(k)])}")


def window(L, rng, key=doi_key):
    src = prose_for[id(key)]
    s = rng.integers(0, len(src) - L)
    return src[s:s + L]


def run_model(name, L, gen, nsim=NSIM):
    rows = []
    for _ in range(nsim):
        x = gen()
        rows.append(seq_stats(x))
    return rows


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
    return out


results = {"seed": SEED, "nsim": NSIM, "fit": fit, "targets": {}}
targets = {"B1": (C[1], 520, 2906), "B3": (C[3], 618, 975), "B2": (C[2], len(C[2]), None)}
for tname, (obs_x, L, longK) in targets.items():
    obs = seq_stats(obs_x)
    vmax = int(obs_x.max())
    models = {
        "DOI_fitted_prose": lambda: encode_fitted(window(L, rng, doi_key), doi_key, rng),
        "DOI_random_prose": lambda: encode_random(window(L, rng, doi_key), doi_key, rng),
        "iid_uniform": lambda: iid_uniform(L, vmax, rng),
        "iid_loguniform": lambda: iid_loguniform(L, vmax, rng),
    }
    if longK:
        lk = long_keys[longK]
        models[f"LONG{longK}_fitted_prose"] = lambda: encode_fitted(window(L, rng, lk), lk, rng)
        models[f"LONG{longK}_random_prose"] = lambda: encode_random(window(L, rng, lk), lk, rng)
    if tname == "B3" and names_pt:
        # 618-letter windows of the synthetic names list (wrapped around: it has ~1400 letters)
        def names_window(key):
            src = names_for[id(key)] * 3
            s = rng.integers(0, len(names_for[id(key)]))
            return src[s:s + L]
        models["DOI_fitted_names"] = lambda: encode_fitted(names_window(doi_key), doi_key, rng)
        models["LONG975_fitted_names"] = lambda: encode_fitted(names_window(long_keys[975]), long_keys[975], rng)
    if tname == "B2":
        # posterior predictive check: the fitted model applied to B2's own plaintext (the
        # printed cipher has 762 numbers for 763 letters; use the first 762 letters)
        b2_text = filtered(b2_pt, doi_key)[:L]
        models["DOI_fitted_B2text"] = lambda: encode_fitted(b2_text, doi_key, rng)
        models["DOI_random_B2text"] = lambda: encode_random(b2_text, doi_key, rng)
    results["targets"][tname] = {"observed": {k: obs[k] for k in SCALARS + ["growth", "top10"]}, "models": {}}
    for mname, gen in models.items():
        rows = run_model(mname, L, gen)
        summ = summarize(rows, obs)
        summ["top10_sim_mean"] = np.mean([r["top10"] for r in rows], axis=0).tolist()
        results["targets"][tname]["models"][mname] = summ
        keys_show = ["distinct", "types_once_frac", "top1", "top10_share", "zipf_slope30", "lag1_spearman", "runs_z", "close_le5", "zero_end_frac_types"]
        print(f"{tname} {mname:26s} " + " ".join(f"{k}={summ[k]['obs']:.3g}|{summ[k]['sim_mean']:.3g}±{summ[k]['sim_sd']:.2g}(pct {summ[k]['percentile']:.3f})"
                                                 for k in keys_show if k in summ))
        sys.stdout.flush()

save_json(results, "stats_homophone_sim.json")

# The growth-curve figure is drawn by stats_07_figures.py from the saved JSON.
print('done')
