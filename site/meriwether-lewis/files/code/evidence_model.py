#!/usr/bin/env python3
"""Evidence weighting for the death of Meriwether Lewis: suicide (S), homicide (H), accident (A).

This is a judgement made explicit, not a measurement. Each evidence item carries a likelihood
range under each hypothesis (how probable the item is if that hypothesis is true), entered in
../data/evidence_items.json. The script draws every likelihood uniformly (log-uniform) inside
its range, multiplies across items, applies a prior, and reports the distribution of the
posterior, plus leave-one-out sensitivity and a "sceptic" run that halves every ratio's
distance from 1. Items judged independent are multiplied; items that share a source are
grouped so their ratios are not both counted (see the "group" field: only one draw per group
is used, chosen at random, unless "combine" is "product").

Usage: python3 evidence_model.py [../data/evidence_items.json] [N draws]
Outputs ../data/evidence_model_results.json and prints a summary table.
"""
import json, sys, math, random, statistics

path = sys.argv[1] if len(sys.argv) > 1 else "../data/evidence_items.json"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
GROUP_RULE = sys.argv[3] if len(sys.argv) > 3 else None   # override "one" / "product"
OUT = sys.argv[4] if len(sys.argv) > 4 else "../data/evidence_model_results.json"
random.seed(20260914)
spec = json.load(open(path))
if GROUP_RULE: spec["group_rule"] = GROUP_RULE
print("group_rule =", spec.get("group_rule","one"), "; N =", N)
items = spec["items"]
priors = spec["priors"]          # dict name -> {"S":..,"H":..,"A":..}
HYP = ["S", "H", "A"]

def draw_lik(item, shrink=1.0):
    out = {}
    for h in HYP:
        lo, hi = item["lik"][h]
        v = math.exp(random.uniform(math.log(lo), math.log(hi)))
        if shrink != 1.0:
            # move the ratio toward the S value to model a sceptic who discounts every item
            pass
        out[h] = v
    if shrink != 1.0:
        s = out["S"]
        for h in HYP:
            out[h] = s * (out[h] / s) ** shrink
    return out

def run(items, prior, shrink=1.0, skip=None, n=N):
    post = {h: [] for h in HYP}
    groups = {}
    for it in items:
        groups.setdefault(it.get("group", it["id"]), []).append(it)
    for _ in range(n):
        logp = {h: math.log(prior[h]) for h in HYP}
        for g, members in groups.items():
            use = [m for m in members if m["id"] != skip]
            if not use:
                continue
            if len(use) > 1 and spec.get("group_rule", "one") == "one":
                use = [random.choice(use)]
            for m in use:
                l = draw_lik(m, shrink)
                for h in HYP:
                    logp[h] += math.log(l[h])
        m = max(logp.values())
        z = sum(math.exp(v - m) for v in logp.values())
        for h in HYP:
            post[h].append(math.exp(logp[h] - m) / z)
    return {h: (statistics.median(v), sorted(v)[int(0.05*len(v))], sorted(v)[int(0.95*len(v))]) for h, v in post.items()}

results = {"priors": priors, "runs": {}}
for pname, prior in priors.items():
    for shrink, label in [(1.0, "base"), (0.5, "sceptic_half"), (0.25, "sceptic_quarter")]:
        r = run(items, prior, shrink, n=N//4 if shrink != 1.0 else N)
        results["runs"][f"{pname}/{label}"] = r
        print(f"{pname:>12} {label:>15}: " + "  ".join(f"{h} {r[h][0]*100:5.1f}% [{r[h][1]*100:4.1f}-{r[h][2]*100:4.1f}]" for h in HYP))

# leave-one-out on the main prior
main = spec.get("main_prior", list(priors)[0])
print("\nLeave-one-out (main prior, base likelihoods): posterior for S when each item is dropped")
loo = {}
base = run(items, priors[main], n=N//5)["S"][0]
for it in items:
    r = run(items, priors[main], skip=it["id"], n=N//5)
    loo[it["id"]] = r["S"][0]
    print(f"  drop {it['id']:<28} S = {r['S'][0]*100:5.1f}%  (base {base*100:5.1f}%)  {it['label']}")
results["leave_one_out_S"] = loo
results["base_S"] = base
results["group_rule"] = spec.get("group_rule","one")
json.dump(results, open(OUT, "w"), indent=1)
print("\nwrote", OUT)
