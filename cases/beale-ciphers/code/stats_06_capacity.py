"""Task 6: can 618 symbols hold the list that paper 3 is said to contain?

The pamphlet (letter of 5 January 1822) says paper 3 holds "the names of all my associates"
(thirty men: the treasure is to be divided into thirty-one parts, one for Morriss) "and
opposite to the names of each one ... the names and residences of the relatives and others,
to whom they devise their respective portions".  We estimate the number of letters such a
list needs under several explicit assumptions, using real Virginia name lengths from USGenWeb
census transcriptions (Amherst County 1810 heads of household; Bedford County 1850; Botetourt
County 1850 name index) and the names of the Virginia counties that existed in 1822
(Wikipedia list, formation years).  Cipher 2 shows how this encoder wrote: one number per
letter, no spaces, numbers spelled out, only 'nov'/'dec'/'st' abbreviated.

Census files are read from data/census/ and the county list from data/va_counties_1822.json
(the parent directory can be set with BEALE_CENSUS_DIR); the downloads (from
https://www.us-census.org/pub/usgenweb/census/va/...) are not included in this folder; only
length statistics and a small random sample of names are stored here.  Writes results/stats_capacity.json.
"""
import os, re, json, glob
import numpy as np
from stats_common import *

SEED = 20260914
rng = np.random.default_rng(SEED)
SCRATCH = os.environ.get("BEALE_CENSUS_DIR", os.path.join(B, "data"))
CENSUS = os.path.join(SCRATCH, "census")


def clean(s):
    return re.sub(r"[^a-z]", "", s.lower())


def parse_amherst_1810():
    """PAGE LINE LAST-NAME FIRST-NAME (heads of household)."""
    names = []
    with open(os.path.join(CENSUS, "amherst_1810_index.txt"), encoding="latin-1") as f:
        for line in f:
            m = re.match(r"^\s*(\d+)\s+(\d+)\s+([A-Za-z'\-]+)\s+([A-Za-z'\-\.]+(?:\s+[A-Za-z'\-\.]+)*)\s*$", line)
            if m and "*" not in line:
                last, first = m.group(3), m.group(4)
                names.append((first, last))
    return names


def parse_bedford_1850():
    """LN HN FN LAST NAME FIRST NAME AGE SEX ... (fixed columns)."""
    rows = []
    for fn in sorted(glob.glob(os.path.join(CENSUS, "bedford_1850_pg*.txt"))):
        with open(fn, encoding="latin-1") as f:
            for line in f:
                m = re.match(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+([A-Za-z'\-]+)\s+(.{1,15}?)\s{2,}(\d+)\s+([MF])", line)
                if m:
                    rows.append({"last": m.group(4), "first": m.group(5).strip(), "age": int(m.group(6)),
                                 "sex": m.group(7)})
    return rows


def parse_botetourt_index():
    rows = []
    for fn in sorted(glob.glob(os.path.join(CENSUS, "botetourt_1850_indx-*.txt"))):
        with open(fn, encoding="latin-1") as f:
            for line in f:
                m = re.match(r"^\s*(\d+[ab]?)\s+(\d+)\s+([A-Za-z'\-]+)\s+(.{1,16}?)\s{2,}(\d+)\s", line)
                if m:
                    rows.append({"last": m.group(3), "first": m.group(4).strip(), "age": int(m.group(5))})
    return rows


def first_token(first):
    """first given name without middle initials/names ('James H.' -> 'james')."""
    t = re.split(r"[\s\.]+", first.strip())
    t = [x for x in t if x]
    return clean(t[0]) if t else ""


amherst = parse_amherst_1810()
bedford = parse_bedford_1850()
botetourt = parse_botetourt_index()
print(f"parsed: Amherst 1810 heads {len(amherst)}, Bedford 1850 persons {len(bedford)}, Botetourt 1850 index {len(botetourt)}")

# associates: adult men.  1810 heads of household (Amherst) are the closest in time; Bedford
# and Botetourt 1850 men aged >= 30 (born by 1820) as a check.
assoc_pools = {
    "amherst_1810_heads": [(first_token(f), clean(l)) for f, l in amherst],
    "bedford_1850_men_30plus": [(first_token(r["first"]), clean(r["last"])) for r in bedford
                                if r["sex"] == "M" and r["age"] >= 30],
    "botetourt_1850_index_30plus": [(first_token(r["first"]), clean(r["last"])) for r in botetourt if r["age"] >= 30],
}
# relatives: anybody (wives, children, siblings) - all persons in the 1850 files
rel_pools = {
    "bedford_1850_all": [(first_token(r["first"]), clean(r["last"])) for r in bedford],
    "botetourt_1850_all": [(first_token(r["first"]), clean(r["last"])) for r in botetourt],
}
for d in (assoc_pools, rel_pools):
    for k in d:
        d[k] = [(f, l) for f, l in d[k] if len(f) >= 2 and len(l) >= 2]   # drop initials-only / blanks

with open(os.path.join(SCRATCH, "va_counties_1822.json")) as f:
    counties = json.load(f)["counties_formed_by_1822"]
county_len = np.array([len(clean(c)) for c in counties])

def summarize(pool):
    fl = np.array([len(f) for f, _ in pool]); ll = np.array([len(l) for _, l in pool])
    return {"n": len(pool), "first_mean": float(fl.mean()), "first_median": float(np.median(fl)),
            "last_mean": float(ll.mean()), "last_median": float(np.median(ll)),
            "full_mean": float((fl + ll).mean()), "full_sd": float((fl + ll).std()),
            "full_p5": float(np.percentile(fl + ll, 5)), "full_p25": float(np.percentile(fl + ll, 25))}

res = {"seed": SEED, "n_counties_1822": len(counties), "county_name_len_mean": float(county_len.mean()),
       "county_name_len_min": int(county_len.min()), "county_name_len_median": float(np.median(county_len)),
       "associate_pools": {k: summarize(v) for k, v in assoc_pools.items()},
       "relative_pools": {k: summarize(v) for k, v in rel_pools.items()}}
for k, v in res["associate_pools"].items():
    print(f"  associates {k}: n={v['n']} first {v['first_mean']:.2f} last {v['last_mean']:.2f} full {v['full_mean']:.2f}")
for k, v in res["relative_pools"].items():
    print(f"  relatives  {k}: n={v['n']} first {v['first_mean']:.2f} last {v['last_mean']:.2f} full {v['full_mean']:.2f}")
print(f"  counties: {len(counties)} formed by 1822, mean name length {county_len.mean():.2f}, min {county_len.min()}")

# ---- scenarios: total letters for 30 entries, Monte Carlo over random draws ------------
NSIM = 20000
A = assoc_pools["amherst_1810_heads"]
R = rel_pools["bedford_1850_all"]
Afl = np.array([len(f) for f, _ in A]); All = np.array([len(l) for _, l in A])
Rfl = np.array([len(f) for f, _ in R]); Rll = np.array([len(l) for _, l in R])

def draw_totals(assoc_first, assoc_last, rel_first, rel_last, residence, extra_per_entry=0):
    """sum over 30 entries of the chosen components; each argument is a 1-D array of lengths to
    sample from (or None to omit)."""
    tot = np.zeros(NSIM)
    for arr in (assoc_first, assoc_last, rel_first, rel_last, residence):
        if arr is not None:
            idx = rng.integers(0, len(arr), size=(NSIM, 30))
            tot += arr[idx].sum(axis=1)
    return tot + 30 * extra_per_entry

initial = np.ones(1)   # a single initial letter
scenarios = {
    "S0_bare_minimum": {
        "description": "associate: first name + surname; relative: first name only (surname assumed shared); "
                       "residence: county name only, no word 'county', no state",
        "totals": draw_totals(Afl, All, Rfl, None, county_len)},
    "S1_relative_surname": {
        "description": "as S0 but the relative also gets a surname (a married sister or a mother would need one)",
        "totals": draw_totals(Afl, All, Rfl, Rll, county_len)},
    "S2_county_word": {
        "description": "as S1 plus the word 'county' (6 letters) after each county name, as B2 writes 'county of bedford'",
        "totals": draw_totals(Afl, All, Rfl, Rll, county_len, extra_per_entry=6)},
    "S3_county_and_state": {
        "description": "as S2 plus 'virginia' (8 letters) for each residence",
        "totals": draw_totals(Afl, All, Rfl, Rll, county_len, extra_per_entry=14)},
    "S4_initials_only": {
        "description": "extreme abbreviation: associate = initial + surname; relative = initial + surname; residence = county name",
        "totals": draw_totals(initial, All, initial, Rll, county_len)},
    "S5_initials_no_relative_surname": {
        "description": "associate = initial + surname; relative = first name only; residence = county name",
        "totals": draw_totals(initial, All, Rfl, None, county_len)},
    "S6_surnames_and_counties_only": {
        "description": "floor: associate surname + relative surname + county name, nothing else",
        "totals": draw_totals(None, All, None, Rll, county_len)},
}
res["n_mc"] = NSIM
res["scenarios"] = {}
for k, v in scenarios.items():
    t = v["totals"]
    res["scenarios"][k] = {"description": v["description"], "mean": float(t.mean()), "sd": float(t.std()),
                           "p1": float(np.percentile(t, 1)), "p5": float(np.percentile(t, 5)),
                           "p50": float(np.percentile(t, 50)), "p95": float(np.percentile(t, 95)),
                           "P_total_le_618": float((t <= 618).mean()), "mc_se": mc_se(float((t <= 618).mean()), NSIM)}
    s = res["scenarios"][k]
    print(f"{k:32s} mean {s['mean']:6.0f} sd {s['sd']:4.0f} p1 {s['p1']:5.0f} p5 {s['p5']:5.0f} p50 {s['p50']:5.0f}  P(<=618)={s['P_total_le_618']:.4f}")

# letters available per associate
res["letters_per_entry_available"] = 618 / 30
res["mean_full_name_amherst"] = float((Afl + All).mean())

# the same with the other pools (robustness)
rob = {}
for ak, av in assoc_pools.items():
    afl = np.array([len(f) for f, _ in av]); all_ = np.array([len(l) for _, l in av])
    t = draw_totals(afl, all_, Rfl, None, county_len)
    rob[ak] = {"S0_mean": float(t.mean()), "S0_p5": float(np.percentile(t, 5)), "P_le_618": float((t <= 618).mean())}
res["S0_by_associate_pool"] = rob
print("S0 by associate pool:", rob)

# ---- a synthetic 30-entry list as plaintext for the homophone simulator (task 4) -----------
# real 1810 Amherst heads of household as associates, 1850 Bedford persons as relatives,
# a random 1822 county each, written the way B2 writes ("... bedford county virginia")
ia = rng.choice(len(A), 30, replace=False); ir = rng.choice(len(R), 30, replace=False)
ic = rng.integers(0, len(counties), 30)
entries = []
for a, r, c in zip(ia, ir, ic):
    entries.append(f"{A[a][0]} {A[a][1]} {R[r][0]} {R[r][1]} {clean(counties[c])} county virginia")
names_pt = letters_only(" ".join(entries))
with open(os.path.join(RESULTS, "stats_capacity_names_plaintext.txt"), "w") as f:
    f.write("\n".join(entries) + "\n")
res["synthetic_list_entries"] = entries
res["synthetic_list_letters"] = len(names_pt)
print("synthetic 30-entry list:", len(names_pt), "letters; first entries:", entries[:3])
save_json(res, "stats_capacity.json")
