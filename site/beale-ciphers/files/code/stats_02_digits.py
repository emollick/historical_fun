"""Task 2: digit-preference tests.

For each cipher, on all numbers (tokens) and on the distinct values (types):
  * last digit vs uniform: Pearson chi-square (asymptotic p) and Monte-Carlo p (multinomial);
    for tokens also a 'type-randomised' null that keeps the observed reuse structure (each
    distinct value gets a random uniform last digit; the token-level statistic is recomputed)
    - the honest null for a homophonic cipher whose favourite numbers are reused;
  * first digit vs Benford, vs uniform-on-[1,max], vs uniform-on-[1,1322];
  * last / first digits of B1 and B3 vs B2 (chi-square homogeneity, permutation p);
  * even/odd share, repeated final digits (dd), round endings (0/5), last-two-digit uniformity.
Writes results/stats_digits.json.
"""
import os
from collections import Counter
import numpy as np
from scipy import stats
from stats_common import *

SEED = 20260914
NMC = 100_000
rng = np.random.default_rng(SEED)
C = load_ciphers()


def last_digits(x):
    return np.asarray(x) % 10


def first_digits(x):
    return np.array([int(str(int(v))[0]) for v in x])


def chi2_uniform(counts):
    counts = np.asarray(counts, float)
    exp = counts.sum() / len(counts)
    return float(((counts - exp) ** 2 / exp).sum())


def mc_multinomial_p(counts, probs, nmc, rng):
    """Monte-Carlo p-value for chi-square GOF: P(stat_sim >= stat_obs)."""
    counts = np.asarray(counts, float); probs = np.asarray(probs, float); probs /= probs.sum()
    n = int(counts.sum()); exp = n * probs
    obs = float(((counts - exp) ** 2 / exp).sum())
    sims = rng.multinomial(n, probs, size=nmc)
    st = ((sims - exp) ** 2 / exp).sum(axis=1)
    ge = int((st >= obs - 1e-12).sum())
    return obs, perm_pvalue(ge, nmc)


def benford_probs():
    return np.log10(1 + 1 / np.arange(1, 10))


def uniform_range_first_digit_probs(K):
    v = np.arange(1, K + 1)
    fd = np.array([int(str(i)[0]) for i in v])
    return np.array([(fd == d).mean() for d in range(1, 10)])


def homogeneity(a_counts, b_counts):
    tab = np.array([a_counts, b_counts], float)
    tab = tab[:, tab.sum(axis=0) > 0]
    chi, p, dof, _ = stats.chi2_contingency(tab, correction=False)
    return float(chi), int(dof), float(p)


def perm_homogeneity_p(a, b, nperm, rng, ncat):
    """Permutation p for the chi-square homogeneity statistic of two digit samples."""
    a = np.asarray(a); b = np.asarray(b)
    pooled = np.concatenate([a, b]); na = len(a)
    def stat(x, y):
        ca = np.bincount(x, minlength=ncat); cb = np.bincount(y, minlength=ncat)
        tab = np.array([ca, cb], float); tab = tab[:, tab.sum(axis=0) > 0]
        rowsum = tab.sum(axis=1, keepdims=True); colsum = tab.sum(axis=0, keepdims=True)
        exp = rowsum * colsum / tab.sum()
        return float(((tab - exp) ** 2 / exp).sum())
    obs = stat(a, b)
    ge = 0
    for _ in range(nperm):
        rng.shuffle(pooled)
        if stat(pooled[:na], pooled[na:]) >= obs - 1e-12:
            ge += 1
    return obs, perm_pvalue(ge, nperm)


out = {"seed": SEED, "n_mc": NMC, "ciphers": {}}
for k in (1, 2, 3):
    x = C[k]
    types = np.array(sorted(set(x.tolist())))
    mult = Counter(x.tolist())
    r = {}
    for level, arr in (("tokens", x), ("types", types)):
        ld = last_digits(arr); fd = first_digits(arr)
        ldc = np.bincount(ld, minlength=10); fdc = np.bincount(fd, minlength=10)[1:]
        n = len(arr)
        # last digit vs uniform
        chi = chi2_uniform(ldc); p_asym = float(stats.chi2.sf(chi, 9))
        _, p_mc = mc_multinomial_p(ldc, np.ones(10) / 10, NMC, rng)
        # first digit vs Benford, vs uniform[1,max], vs uniform[1,1322]
        fd_tests = {}
        for name, probs in (("benford", benford_probs()),
                            (f"uniform_1_{int(arr.max())}", uniform_range_first_digit_probs(int(arr.max()))),
                            ("uniform_1_1322", uniform_range_first_digit_probs(1322))):
            st, dof, pa = chi2_gof(fdc, probs, min_expected=5)
            _, pm = mc_multinomial_p(fdc, probs, NMC, rng)
            fd_tests[name] = {"chi2": st, "dof": dof, "p_asymptotic": pa, "p_mc": pm,
                              "expected_probs": probs.tolist()}
        # even / odd
        ne = int((arr % 2 == 0).sum())
        p_even = float(stats.binomtest(ne, n, 0.5).pvalue)
        # repeated final digits dd among numbers >= 10
        big = arr[arr >= 10]
        rep = int(((big // 10) % 10 == big % 10).sum())
        p_rep = float(stats.binomtest(rep, len(big), 0.10).pvalue)
        # round endings 0 or 5
        rnd = int(np.isin(arr % 10, [0, 5]).sum())
        p_rnd = float(stats.binomtest(rnd, n, 0.20).pvalue)
        # last two digits uniform (numbers >= 10 only; 100 cells, MC p)
        l2 = np.bincount(big % 100, minlength=100)
        _, p_l2 = mc_multinomial_p(l2, np.ones(100) / 100, 20_000, rng)
        r[level] = {
            "n": n, "last_digit_counts": ldc.tolist(), "last_digit_chi2": chi, "last_digit_dof": 9,
            "last_digit_p_asymptotic": p_asym, "last_digit_p_mc": p_mc,
            "last_digit_max_abs_dev_frac": float(np.abs(ldc / n - 0.1).max()),
            "first_digit_counts": fdc.tolist(), "first_digit_tests": fd_tests,
            "even_count": ne, "even_frac": ne / n, "even_p_binomial": p_even,
            "repdigit_ending_count": rep, "repdigit_ending_n": len(big),
            "repdigit_ending_frac": rep / len(big), "repdigit_ending_p_binomial_vs_0.10": p_rep,
            "ending_0_or_5_count": rnd, "ending_0_or_5_frac": rnd / n, "ending_0_or_5_p_vs_0.20": p_rnd,
            "last_two_digits_chi2_p_mc": p_l2,
        }
    # token-level last-digit test with the type-randomised null (keeps multiplicities)
    m = np.array([mult[v] for v in types])
    ldc_obs = np.bincount(last_digits(x), minlength=10)
    obs = chi2_uniform(ldc_obs)
    ge = 0
    for _ in range(NMC // 5):
        dig = rng.integers(0, 10, size=len(types))
        cnt = np.bincount(dig, weights=m, minlength=10)
        if chi2_uniform(cnt) >= obs - 1e-12:
            ge += 1
    r["tokens"]["last_digit_p_type_randomised"] = perm_pvalue(ge, NMC // 5)
    r["tokens"]["last_digit_type_randomised_nmc"] = NMC // 5
    # large vs small numbers (B1: above/below 1322) last digits
    if k == 1:
        lo, hi = x[x <= 1322], x[x > 1322]
        r["last_digit_gt1322_counts"] = np.bincount(last_digits(hi), minlength=10).tolist()
        r["last_digit_gt1322_n"] = int(len(hi))
        chi_hi = chi2_uniform(np.bincount(last_digits(hi), minlength=10))
        _, p_hi = mc_multinomial_p(np.bincount(last_digits(hi), minlength=10), np.ones(10) / 10, NMC, rng)
        r["last_digit_gt1322_p_mc"] = p_hi
        r["even_frac_gt1322"] = float((hi % 2 == 0).mean())
    out["ciphers"][f"B{k}"] = r

# pairwise comparisons of digit distributions (tokens and types)
pairs = {}
for (a, b) in ((1, 2), (3, 2), (1, 3)):
    for level in ("tokens", "types"):
        xa = C[a] if level == "tokens" else np.array(sorted(set(C[a].tolist())))
        xb = C[b] if level == "tokens" else np.array(sorted(set(C[b].tolist())))
        d = {}
        for which, fn, ncat in (("last", last_digits, 10), ("first", first_digits, 10)):
            ca = np.bincount(fn(xa), minlength=ncat); cb = np.bincount(fn(xb), minlength=ncat)
            chi, dof, p = homogeneity(ca, cb)
            _, pp = perm_homogeneity_p(fn(xa), fn(xb), 20_000, rng, ncat)
            d[which] = {"chi2": chi, "dof": dof, "p_asymptotic": p, "p_perm": pp, "n_perm": 20_000}
        # even share difference
        ea, eb = int((xa % 2 == 0).sum()), int((xb % 2 == 0).sum())
        tab = [[ea, len(xa) - ea], [eb, len(xb) - eb]]
        d["even"] = {"frac_a": ea / len(xa), "frac_b": eb / len(xb),
                     "p_fisher": float(stats.fisher_exact(tab)[1])}
        pairs[f"B{a}_vs_B{b}_{level}"] = d
out["pairwise"] = pairs

# a quick 'human digit preference' reference: Wagenaar-type findings are qualitative; we record
# the diagnostic statistics only.
save_json(out, "stats_digits.json")

# ---- print summary ---------------------------------------------------------------
for k in (1, 2, 3):
    r = out["ciphers"][f"B{k}"]
    for level in ("tokens", "types"):
        t = r[level]
        print(f"B{k} {level:6s} n={t['n']:4d} last-digit counts {t['last_digit_counts']} chi2={t['last_digit_chi2']:.1f} "
              f"p_asym={t['last_digit_p_asymptotic']:.4f} p_mc={t['last_digit_p_mc']:.4f}"
              + (f" p_type_rand={t['last_digit_p_type_randomised']:.4f}" if level == "tokens" else ""))
        print(f"      even {t['even_frac']:.3f} (p={t['even_p_binomial']:.3g}); dd-endings {t['repdigit_ending_frac']:.3f} "
              f"(p={t['repdigit_ending_p_binomial_vs_0.10']:.3g}); 0/5 endings {t['ending_0_or_5_frac']:.3f} (p={t['ending_0_or_5_p_vs_0.20']:.3g}); "
              f"last-two-digits p_mc={t['last_two_digits_chi2_p_mc']:.3g}")
        print(f"      first-digit counts {t['first_digit_counts']}; " + "; ".join(
            f"{nm}: chi2={v['chi2']:.1f} p_mc={v['p_mc']:.3g}" for nm, v in t["first_digit_tests"].items()))
    if k == 1:
        print(f"   B1 numbers >1322: n={r['last_digit_gt1322_n']} last digits {r['last_digit_gt1322_counts']} p_mc={r['last_digit_gt1322_p_mc']:.3f} even={r['even_frac_gt1322']:.2f}")
for name, d in pairs.items():
    print(name, {w: (round(v['chi2'], 1), round(v['p_perm'], 4)) for w, v in d.items() if w != 'even'},
          "even", round(d['even']['frac_a'], 3), round(d['even']['frac_b'], 3), "p", round(d['even']['p_fisher'], 4))
