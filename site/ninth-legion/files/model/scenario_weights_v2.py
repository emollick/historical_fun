"""
Scenario weighting for the end of Legio IX Hispana, with ranged likelihoods.

Differences from scenario_weights.py (the point-value weighting):
  * The two British-crisis items (E3 reinforcement/replacement and E4 attested losses) are merged into
    one item, because they describe the same episode and were being counted twice.
  * Every likelihood is given as a RANGE from a base reading to a sceptical reading, and the prior for
    Britain as a range; the posterior is computed for 100,000 random draws across those ranges.
    The headline probability is the median of that distribution and the 90% interval is reported,
    so that the stated confidence is the one the sensitivity analysis supports.
  * The three named point cases of scenario_weights.py (base, sceptic, sceptic + low prior) are kept for comparison.

Hypotheses:
  H1  ended in Britain c. 122-130 (destroyed, or defeated and disbanded)
  H2  survived, left Britain, lost in the Bar Kokhba war 132-136 (or disbanded after it)
  H3  survived to 161, destroyed at Elegeia (Dio 71.2)
  H4  other: an undocumented loss, amalgamation or disbandment elsewhere, c. 125-165
"""
import json
import numpy as np

H = ["H1", "H2", "H3", "H4"]

# (base, sceptical) likelihood for each hypothesis; H1 = 1 except where noted.
evidence = {
 "A. Officers' careers: securely dated service ends c. 123/124, probably c. 125-128; none secure after c. 130":
    {"H1": (1.0, 1.0), "H2": (0.35, 0.70), "H3": (0.08, 0.16), "H4": (0.30, 0.60)},
 "B. No base and no trace outside Britain after c. 122 (Nijmegen detachment only; fortress empty c. 125/130; no eastern inscription)":
    {"H1": (1.0, 1.0), "H2": (0.20, 0.40), "H3": (0.10, 0.20), "H4": (0.50, 1.00)},
 "C. A British crisis c. 122-125 with heavy losses, a 3,000-man legionary reinforcement, a Spanish levy and VI Victrix as a one-for-one replacement (Fronto, SHA, ILS 2726, 2735, RIB 3364, Wall hiatus)":
    {"H1": (1.0, 1.0), "H2": (0.50, 0.80), "H3": (0.50, 0.80), "H4": (0.60, 0.85)},
 "D. Dio 71.2 records a legion annihilated at Elegeia in 161":
    {"H1": (1.0, 1.0), "H2": (1.0, 1.0), "H3": (2.0, 3.0), "H4": (1.0, 1.0)},
 "E. No building stone of the Ninth on Hadrian's Wall":
    {"H1": (0.50, 0.30), "H2": (1.0, 1.0), "H3": (1.0, 1.0), "H4": (1.0, 1.0)},
}
prior_H1 = (0.30, 0.15)          # base, sceptical
rest_pattern = np.array([0.30, 0.25, 0.15])   # H2:H3:H4 proportions for the remainder

def posterior(priors, lik):
    p = np.array([priors[h] * np.prod([lik[e][h] for e in lik]) for h in H])
    return p / p.sum()

def point_case(t, prior_t=None):
    """t = 0 base reading, t = 1 sceptical reading, for every likelihood; prior_t likewise."""
    lik = {e: {h: v[h][0] + t * (v[h][1] - v[h][0]) for h in H} for e, v in evidence.items()}
    pt = t if prior_t is None else prior_t
    p1 = prior_H1[0] + pt * (prior_H1[1] - prior_H1[0])
    pri = dict(zip(H, [p1, *((1 - p1) * rest_pattern / rest_pattern.sum())]))
    return posterior(pri, lik)

rng = np.random.default_rng(20260914)
N = 100_000
draws = np.zeros((N, 4))
for i in range(N):
    lik = {}
    for e, v in evidence.items():
        lik[e] = {h: rng.uniform(min(v[h]), max(v[h])) for h in H}
    p1 = rng.uniform(min(prior_H1), max(prior_H1))
    pri = dict(zip(H, [p1, *((1 - p1) * rest_pattern / rest_pattern.sum())]))
    draws[i] = posterior(pri, lik)

def q(a): return {"p05": round(float(np.percentile(a, 5)), 3), "median": round(float(np.median(a)), 3),
                  "mean": round(float(a.mean()), 3), "p95": round(float(np.percentile(a, 95)), 3)}

out = {
 "evidence": evidence,
 "prior_H1_range": prior_H1,
 "point_cases": {
   "base (every likelihood and the prior at the base reading)": dict(zip(H, np.round(point_case(0), 3).tolist())),
   "sceptic (every likelihood at the sceptical reading, base prior)": dict(zip(H, np.round(point_case(1, prior_t=0), 3).tolist())),
   "sceptic and low prior for Britain (15%)": dict(zip(H, np.round(point_case(1, prior_t=1), 3).tolist())),
 },
 "distribution_over_draws": {h: q(draws[:, j]) for j, h in enumerate(H)},
 "P(H1 > 0.5)": round(float((draws[:, 0] > 0.5).mean()), 3),
 "P(H1 > 0.75)": round(float((draws[:, 0] > 0.75).mean()), 3),
}
# drop-one analysis at the median draw setting (t = 0.5)
lik_mid = {e: {h: (v[h][0] + v[h][1]) / 2 for h in H} for e, v in evidence.items()}
p1 = sum(prior_H1) / 2
pri_mid = dict(zip(H, [p1, *((1 - p1) * rest_pattern / rest_pattern.sum())]))
out["midpoint_case"] = dict(zip(H, np.round(posterior(pri_mid, lik_mid), 3).tolist()))
out["drop_one_at_midpoint"] = {}
for e in evidence:
    lik2 = {k: v for k, v in lik_mid.items() if k != e}
    out["drop_one_at_midpoint"]["without " + e[:1]] = dict(zip(H, np.round(posterior(pri_mid, lik2), 3).tolist()))
json.dump(out, open("scenario_weights_v2.json", "w"), indent=1)
for k, v in out.items():
    if k != "evidence": print(k, json.dumps(v))

# ---- Variant: triangular draws with the mode at the base reading (base reading treated as most likely,
#      sceptical reading as the bound), and the share of draws in which Britain ranks first.
draws_t = np.zeros((N, 4))
for i in range(N):
    lik = {}
    for e, v in evidence.items():
        lik[e] = {}
        for h in H:
            b, s = v[h]
            lik[e][h] = b if b == s else rng.triangular(min(b, s), b, max(b, s))
    b, s = prior_H1
    p1 = rng.triangular(min(b, s), b, max(b, s))
    pri = dict(zip(H, [p1, *((1 - p1) * rest_pattern / rest_pattern.sum())]))
    draws_t[i] = posterior(pri, lik)
out["triangular_mode_at_base"] = {h: q(draws_t[:, j]) for j, h in enumerate(H)}
out["P(Britain ranks first) uniform"] = round(float((draws.argmax(axis=1) == 0).mean()), 3)
out["P(Britain ranks first) triangular"] = round(float((draws_t.argmax(axis=1) == 0).mean()), 3)
json.dump(out, open("scenario_weights_v2.json", "w"), indent=1)
print("triangular", json.dumps(out["triangular_mode_at_base"]))
print("P(Britain first) uniform", out["P(Britain ranks first) uniform"], "triangular", out["P(Britain ranks first) triangular"])
