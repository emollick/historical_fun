#!/usr/bin/env python3
"""
calibrate.py -- independent IntCal20 calibration of the radiocarbon dates reported for the
Col de la Traversette mire (sites G5/G5a, upper Guil valley, 2573-2580 m) by
Mahaney et al. 2017, Archaeometry 59(1): 164-178 (doi 10.1111/arcm.12231), Table 1, p. 171.

Pure Python 3 (no numpy). Method: standard probabilistic calibration (as in OxCal / calib /
rcarbon): for each calendar year t the likelihood of the measured 14C age r +- s given the
curve mu(t) +- sig(t) is a normal density with variance s^2 + sig(t)^2; the posterior over t
uses a flat prior and is normalised to 1. Ranges are highest-posterior-density (HPD) sets at
68.3 % and 95.4 %. No Bayesian sequence model is imposed, deliberately: the point is to see
what each measurement can say on its own.

Curve: IntCal20 (Reimer et al. 2020, Radiocarbon 62, doi 10.1017/RDC.2020.41), file
intcal20.14c fetched from https://intcal.org/curves/intcal20.14c (columns: CAL BP, 14C age,
Sigma, Delta14C, Sigma). The curve is tabulated at 1-year steps over 0-5000 cal BP (5-year
steps further back); it is linearly interpolated to an integer-year grid.

Calendar convention: cal BP = years before AD 1950. Astronomical year y = 1950 - calBP;
historical year: y >= 1 -> AD y ; y <= 0 -> (1 - y) BC (there is no year 0). Under this
convention 218 BC is astronomical -217 = 2167 cal BP; Mahaney et al. write 2168 cal BP for
218 BC (the naive 1950 + 218). The one-year difference is immaterial and is ignored below:
the "Hannibal window" is taken as 230-200 BC inclusive = cal BP 2149-2179 (astronomical
-229 .. -199), i.e. 31 calendar years, and a narrower 220-215 BC window is also reported.

Usage: python3 calibrate.py [path/to/intcal20.14c] [outdir]
Outputs: outdir/radiocarbon_calibration.json, outdir/radiocarbon_calibration.md,
         outdir/radiocarbon_curve_40cm.svg
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CURVE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "intcal20.14c")
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "data")

# Dates exactly as printed in Mahaney et al. 2017 (Part I), Table 1, p. 171.
# "All 14C dates are from peat samples in two cores and one trench" (p. 170).
# Labs: UBA = Queen's University Belfast 14CHRONO (AMS); Beta = Beta Analytic;
# Ta = University of Tartu radiocarbon laboratory (conventional).
DATES = [
    # lab code, 14C BP, 1-sigma error, depth cm, bed as labelled by the authors
    ("Beta-305008", 1130, 30, 26, "post-invasion beds (top of subsection I)"),
    ("UBA-24875",   2070, 31, 40, "MAD bed, upper part (40 cm)"),
    ("Ta-3021",     2530, 90, 40, "MAD bed, upper part (40 cm)"),
    ("UBA-23647",   3537, 28, 45, "MAD bed, lower part (45 cm)"),
    ("Ta-3022",     3270, 100, 50, "MAD bed, lower part (50 cm)"),
    ("UBA-24876",   3282, 28, 50, "MAD bed, lower part (50 cm)"),
    ("Beta-305009", 3170, 30, 65, "pre-invasion beds (base of core, 65 cm)"),
    # --- Additional AMS dates, sections G5B, G5C, G5D (2-9 m from G5), from Mahaney et al. 2017,
    # "Notes on magnetic susceptibility in the Guil Valley alluvial mire...", Mediterranean Archaeology
    # and Archaeometry 17(1): 23-35, p. 29 (doi 10.5281/zenodo.258081). The authors put "218 BC" at
    # 33 cm (G5B), 50 cm (G5C) and 45 cm (G5D) by Bayesian interpolation between these dates.
    ("UBA-30324", 1393, 49, 22, "G5B, above churned zone (22 cm)"),
    ("UBA-30321", 2678, 41, 36, "G5B, churned zone (35-37 cm)"),
    ("UBA-30331", 1842, 41, 45, "G5C (45 cm)"),
    ("UBA-30330", 2190, 35, 51, "G5C (51 cm) -- authors' 218 BC bed at 50 cm"),
    ("UBA-30330b", 2523, 36, 58, "G5C (58 cm) [lab number printed as UBA-30330 twice; sic]"),
    ("UBA-30318", 1724, 38, 35, "G5D (35 cm)"),
    ("UBA-30315", 2329, 55, 45, "G5D (45 cm) -- authors' 218 BC bed at 45 cm"),
]

# What the authors printed as calibrated (IntCal13, OxCal 4.2.4) for comparison: mu, sigma, 2-sigma from/to (cal BP)
AUTHORS_CAL = {
    "Beta-305008": (1035, 48, 1173, 962),
    "UBA-24875":   (2042, 46, 2125, 1949),
    "Ta-3021":     (2587, 117, 2769, 2357),
    "UBA-23647":   (3811, 52, 3895, 3720),
    "Ta-3022":     (3509, 118, 3820, 3249),
    "UBA-24876":   (3511, 36, 3573, 3450),
    "Beta-305009": (3398, 33, 3454, 3345),
}

HANNIBAL_BP = 2167          # 218 BC, astronomical -217
WINDOW_WIDE = (2149, 2179)  # 230-200 BC inclusive
WINDOW_NARROW = (2164, 2169)  # 220-215 BC inclusive


def load_curve(path):
    calbp, c14, sig = [], [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            calbp.append(float(parts[0])); c14.append(float(parts[1])); sig.append(float(parts[2]))
    # file is descending in cal BP; make ascending
    rows = sorted(zip(calbp, c14, sig))
    return rows


def interpolate(rows, tmin, tmax):
    """Return dict t -> (mu, sigma) for integer t in [tmin, tmax] by linear interpolation."""
    out = {}
    i = 0
    n = len(rows)
    for t in range(tmin, tmax + 1):
        while i < n - 2 and rows[i + 1][0] < t:
            i += 1
        t0, m0, s0 = rows[i]
        t1, m1, s1 = rows[i + 1]
        if t1 == t0:
            out[t] = (m0, s0)
        else:
            w = (t - t0) / (t1 - t0)
            out[t] = (m0 + w * (m1 - m0), s0 + w * (s1 - s0))
    return out


def calibrate(r, s, curve, tmin, tmax):
    post = {}
    tot = 0.0
    for t in range(tmin, tmax + 1):
        mu, sg = curve[t]
        v = s * s + sg * sg
        p = math.exp(-0.5 * (r - mu) ** 2 / v) / math.sqrt(2 * math.pi * v)
        post[t] = p
        tot += p
    for t in post:
        post[t] /= tot
    return post


def hpd(post, level):
    items = sorted(post.items(), key=lambda kv: kv[1], reverse=True)
    acc = 0.0
    chosen = set()
    for t, p in items:
        chosen.add(t)
        acc += p
        if acc >= level:
            break
    ts = sorted(chosen)
    ranges = []
    start = prev = ts[0]
    for t in ts[1:]:
        if t == prev + 1:
            prev = t
        else:
            ranges.append((start, prev))
            start = prev = t
    ranges.append((start, prev))
    # probability in each range
    out = []
    for a, b in ranges:
        pr = sum(post[t] for t in range(a, b + 1))
        out.append((a, b, pr))
    return out


def summary_stats(post):
    ts = sorted(post)
    mean = sum(t * post[t] for t in ts)
    var = sum((t - mean) ** 2 * post[t] for t in ts)
    acc = 0.0
    median = None
    for t in ts:
        acc += post[t]
        if median is None and acc >= 0.5:
            median = t
    return mean, math.sqrt(var), median


def mass(post, a, b):
    return sum(post.get(t, 0.0) for t in range(a, b + 1))


def to_hist(calbp):
    y = 1950 - calbp
    return f"AD {y}" if y >= 1 else f"{1 - y} BC"


def fmt_range(a, b, pr):
    # a < b in cal BP => b is older; print older first in BC/AD
    return f"{to_hist(b)} to {to_hist(a)} (cal BP {b}-{a}, {100*pr:.1f} %)"


def ward_wilson(dates):
    """Chi-square test of homogeneity for uncalibrated 14C ages (Ward & Wilson 1978)."""
    w = [1.0 / (s * s) for _, r, s in dates]
    xbar = sum(wi * r for wi, (_, r, _) in zip(w, dates)) / sum(w)
    T = sum((r - xbar) ** 2 / (s * s) for _, r, s in dates)
    df = len(dates) - 1
    err = math.sqrt(1.0 / sum(w))
    return xbar, err, T, df


def chi2_sf_1df(x):
    # survival function of chi-square with 1 dof = erfc(sqrt(x/2))
    return math.erfc(math.sqrt(x / 2.0))


def main():
    rows = load_curve(CURVE)
    tmin, tmax = 0, 6000
    curve = interpolate(rows, tmin, tmax)
    results = []
    md = []
    md.append("# IntCal20 calibration of the Traversette mire radiocarbon dates\n")
    md.append("Source of the measurements: Mahaney et al. 2017, Archaeometry 59(1), Table 1 (p. 171); "
              "material: peat (p. 170). Calibration here: IntCal20 (Reimer et al. 2020), flat prior, "
              "no sequence model, HPD ranges. Authors' own values (IntCal13/OxCal 4.2.4) shown for comparison. "
              "Hannibal window = 230-200 BC (cal BP 2149-2179).\n")
    md.append("| Lab code | 14C BP | Depth (cm) | Bed (authors) | 68.3 % HPD (IntCal20) | 95.4 % HPD (IntCal20) | Median | P(230-200 BC) | P(220-215 BC) | Authors' 2-sigma (IntCal13, cal BP) |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for lab, r, s, depth, bed in DATES:
        post = calibrate(r, s, curve, tmin, tmax)
        h68 = hpd(post, 0.683)
        h95 = hpd(post, 0.954)
        mean, sd, med = summary_stats(post)
        p_wide = mass(post, *WINDOW_WIDE)
        p_narrow = mass(post, *WINDOW_NARROW)
        p_younger = mass(post, 0, HANNIBAL_BP - 1)   # calendar years after 218 BC
        p_older = mass(post, HANNIBAL_BP + 1, tmax)  # calendar years before 218 BC
        a = AUTHORS_CAL.get(lab)
        rec = {
            "lab": lab, "c14_bp": r, "error": s, "depth_cm": depth, "bed": bed, "material": "peat",
            "intcal20": {
                "hpd68": [{"from_calBP": b, "to_calBP": a_, "from": to_hist(b), "to": to_hist(a_), "p": round(pr, 4)} for a_, b, pr in h68],
                "hpd95": [{"from_calBP": b, "to_calBP": a_, "from": to_hist(b), "to": to_hist(a_), "p": round(pr, 4)} for a_, b, pr in h95],
                "mean_calBP": round(mean, 1), "sd_years": round(sd, 1), "median_calBP": med, "median": to_hist(med),
                "p_230_200BC": round(p_wide, 4), "p_220_215BC": round(p_narrow, 4),
                "p_after_218BC": round(p_younger, 4), "p_before_218BC": round(p_older, 4),
                "full_95_span_years": max(b for _, b, _ in h95) - min(a_ for a_, _, _ in h95) + 1,
            },
            "authors_intcal13": ({"mu_calBP": a[0], "sigma": a[1], "two_sigma_from_calBP": a[2], "two_sigma_to_calBP": a[3],
                                  "two_sigma_from": to_hist(a[2]), "two_sigma_to": to_hist(a[3]),
                                  "includes_218BC": (a[3] <= HANNIBAL_BP <= a[2])} if a else None),
        }
        results.append(rec)
        md.append("| %s | %d ± %d | %d | %s | %s | %s | %s | %.1f %% | %.1f %% | %d-%d (%s to %s)%s |" % (
            lab, r, s, depth, bed,
            "; ".join(fmt_range(a_, b, pr) for a_, b, pr in h68),
            "; ".join(fmt_range(a_, b, pr) for a_, b, pr in h95),
            to_hist(med), 100 * p_wide, 100 * p_narrow,
            *( (a[2], a[3], to_hist(a[2]), to_hist(a[3]), "" if rec["authors_intcal13"]["includes_218BC"] else " -- excludes 218 BC") if a else (0, 0, "n/a", "n/a", "") )))

    # Homogeneity test of the two dates from the same 40 cm level
    pair = [(d[0], d[1], d[2]) for d in DATES if d[0] in ("UBA-24875", "Ta-3021")]
    xbar, err, T, df = ward_wilson(pair)
    pval = chi2_sf_1df(T)
    comb = calibrate(xbar, err, curve, tmin, tmax)
    comb95 = hpd(comb, 0.954)
    comb68 = hpd(comb, 0.683)
    pair_rec = {
        "dates": [p[0] for p in pair],
        "weighted_mean_bp": round(xbar, 1), "weighted_mean_err": round(err, 1),
        "chi2_T": round(T, 2), "df": df, "chi2_crit_5pct": 3.84, "p_value": pval,
        "consistent_at_5pct": T < 3.84,
        "note": "If T > 3.84 the two measurements cannot be estimates of the same true age at the 5 % level, "
                "so combining them (or treating them as 'bracketing' one event) is not statistically justified.",
        "combined_if_taken_anyway": {
            "hpd68": [{"from": to_hist(b), "to": to_hist(a_), "p": round(pr, 4)} for a_, b, pr in comb68],
            "hpd95": [{"from": to_hist(b), "to": to_hist(a_), "p": round(pr, 4)} for a_, b, pr in comb95],
            "p_230_200BC": round(mass(comb, *WINDOW_WIDE), 4),
        },
    }

    # Curve-shape diagnostics for the period 500 BC - AD 100 (cal BP 2449-1849): the 14C age
    # range spanned, slope, and how many calendar years map into the 1-sigma band of UBA-24875.
    diag = {}
    seg = [(t, curve[t][0], curve[t][1]) for t in range(1849, 2450)]
    diag["curve_500BC_to_AD100"] = {
        "c14_min": min(m for _, m, _ in seg), "c14_max": max(m for _, m, _ in seg),
        "note": "IntCal20 between 500 BC and AD 100; the Hallstatt plateau (c. 800-400 BC, ~2450 14C BP) "
                "ends near 400 BC, after which the curve falls steeply to c. 2100 BP by c. 150 BC, then wiggles."
    }
    # Calendar years whose curve value lies within 1 sigma (measurement + curve) of each 40 cm date
    for lab, r, s in pair:
        yrs = [t for t, m, sg in seg if abs(r - m) <= math.sqrt(s * s + sg * sg)]
        diag[f"{lab}_calendar_years_within_1sigma_of_curve_500BC_AD100"] = {
            "n_years": len(yrs), "earliest": to_hist(max(yrs)) if yrs else None, "latest": to_hist(min(yrs)) if yrs else None}
    diag["curve_at_218BC"] = {"calBP": HANNIBAL_BP, "c14_age": curve[HANNIBAL_BP][0], "sigma": curve[HANNIBAL_BP][1]}
    diag["curve_values_selected"] = {to_hist(t): curve[t][0] for t in [2399, 2349, 2299, 2249, 2199, 2167, 2149, 2099, 2049, 1999, 1949]}

    out = {"curve": "IntCal20 (Reimer et al. 2020), https://intcal.org/curves/intcal20.14c",
           "method": "flat-prior probabilistic calibration, HPD ranges, integer-year grid on the 1-yr IntCal20 table; no sequence model",
           "hannibal_window_wide": "230-200 BC = cal BP 2149-2179", "hannibal_window_narrow": "220-215 BC",
           "dates": results, "forty_cm_pair_test": pair_rec, "diagnostics": diag}
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "radiocarbon_calibration.json"), "w") as f:
        json.dump(out, f, indent=1)

    md.append("")
    md.append("## The two dates from the 40 cm level (the 'bracketing' pair)\n")
    md.append(f"UBA-24875 (2070 ± 31 BP) and Ta-3021 (2530 ± 90 BP) come from the same depth. Ward & Wilson test: "
              f"weighted mean {xbar:.0f} ± {err:.0f} BP, T = {T:.2f} (df = 1, critical value 3.84 at 5 %), p = {pval:.2g}. "
              f"{'They are statistically consistent.' if T < 3.84 else 'They are NOT statistically consistent: they cannot be two measurements of one true age. Either the level contains peat of two different ages (reworking), or one measurement is wrong.'}")
    md.append("")
    md.append("Mass of each 40 cm date in the 230-200 BC window: " + ", ".join(
        f"{r['lab']} {100*r['intcal20']['p_230_200BC']:.1f} %" for r in results if r["depth_cm"] == 40))
    md.append("")
    md.append("Curve at 218 BC: 14C age %.0f ± %.0f BP (IntCal20)." % (curve[HANNIBAL_BP][0], curve[HANNIBAL_BP][1]))
    md.append("Selected curve values (14C BP): " + ", ".join(f"{k}: {v:.0f}" for k, v in diag["curve_values_selected"].items()))
    with open(os.path.join(OUTDIR, "radiocarbon_calibration.md"), "w") as f:
        f.write("\n".join(md) + "\n")

    # SVG: curve 600 BC - AD 200 with the two 40 cm dates as 1-sigma and 2-sigma bands
    write_svg(curve, pair, os.path.join(OUTDIR, "radiocarbon_curve_40cm.svg"))
    print("\n".join(md))


def write_svg(curve, pair, path):
    t0, t1 = 1749, 2549  # cal BP range (AD 201 .. 600 BC)
    W, H = 900, 520
    ml, mr, mt, mb = 70, 20, 30, 50
    ys = [curve[t][0] for t in range(t0, t1 + 1)]
    ymin, ymax = 1800, 2700
    def X(t): return ml + (t1 - t) / (t1 - t0) * (W - ml - mr)   # older to the left
    def Y(y): return mt + (ymax - y) / (ymax - ymin) * (H - mt - mb)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="white"/>']
    # bands for the two dates (2 sigma light, 1 sigma darker)
    colors = {"UBA-24875": "#1f77b4", "Ta-3021": "#d62728"}
    for lab, r, sd in pair:
        c = colors.get(lab, "#555")
        s.append(f'<rect x="{ml}" y="{Y(r+2*sd):.1f}" width="{W-ml-mr}" height="{Y(r-2*sd)-Y(r+2*sd):.1f}" fill="{c}" fill-opacity="0.10"/>')
        s.append(f'<rect x="{ml}" y="{Y(r+sd):.1f}" width="{W-ml-mr}" height="{Y(r-sd)-Y(r+sd):.1f}" fill="{c}" fill-opacity="0.22"/>')
        s.append(f'<text x="{W-mr-5}" y="{Y(r)+4:.1f}" text-anchor="end" fill="{c}">{lab} {r}±{sd} BP</text>')
    # curve envelope (1 sigma)
    up = " ".join(f"{X(t):.1f},{Y(curve[t][0]+curve[t][1]):.1f}" for t in range(t0, t1 + 1))
    lo = " ".join(f"{X(t):.1f},{Y(curve[t][0]-curve[t][1]):.1f}" for t in range(t1, t0 - 1, -1))
    s.append(f'<polygon points="{up} {lo}" fill="#444" fill-opacity="0.25" stroke="none"/>')
    s.append('<polyline points="' + " ".join(f"{X(t):.1f},{Y(curve[t][0]):.1f}" for t in range(t0, t1 + 1)) + '" fill="none" stroke="#222" stroke-width="1.5"/>')
    # 218 BC line
    s.append(f'<line x1="{X(2167):.1f}" y1="{mt}" x2="{X(2167):.1f}" y2="{H-mb}" stroke="#2ca02c" stroke-width="2" stroke-dasharray="6,4"/>')
    s.append(f'<text x="{X(2167)+4:.1f}" y="{mt+14}" fill="#2ca02c">218 BC</text>')
    # axes
    s.append(f'<line x1="{ml}" y1="{H-mb}" x2="{W-mr}" y2="{H-mb}" stroke="#000"/>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{H-mb}" stroke="#000"/>')
    for yr in range(-600, 201, 100):
        t = 1950 - yr
        lab = f"{1-yr} BC" if yr <= 0 else f"AD {yr}"
        s.append(f'<line x1="{X(t):.1f}" y1="{H-mb}" x2="{X(t):.1f}" y2="{H-mb+5}" stroke="#000"/>')
        s.append(f'<text x="{X(t):.1f}" y="{H-mb+18}" text-anchor="middle">{lab}</text>')
    for y in range(ymin, ymax + 1, 100):
        s.append(f'<line x1="{ml-5}" y1="{Y(y):.1f}" x2="{ml}" y2="{Y(y):.1f}" stroke="#000"/>')
        s.append(f'<text x="{ml-8}" y="{Y(y)+4:.1f}" text-anchor="end">{y}</text>')
    s.append(f'<text x="{(W+ml)/2:.0f}" y="{H-8}" text-anchor="middle">calendar year</text>')
    s.append(f'<text x="14" y="{H/2:.0f}" transform="rotate(-90 14 {H/2:.0f})" text-anchor="middle">radiocarbon age (14C BP)</text>')
    s.append(f'<text x="{ml+10}" y="{H-mb-10}" fill="#222">IntCal20 curve (line = mean, grey = 1 sigma); bands = the two 14C dates from the 40 cm level of the Traversette mire (dark = 1 sigma, light = 2 sigma)</text>')
    s.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(s))


if __name__ == "__main__":
    main()
