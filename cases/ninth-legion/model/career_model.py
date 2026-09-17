"""
Career-date Monte Carlo for the last attested existence of Legio IX Hispana.

Idea: each senatorial officer known to have served in the Ninth has a later,
securely dated fixed point (a consulship, a governorship on a papyrus). Working
back with the *normal* intervals of the senatorial cursus gives a distribution,
not a point, for when he served in the legion. The legion existed at least until
the latest of those service dates. Sampling the intervals gives P(legion still
existed in year Y) under stated assumptions.

Interval assumptions (all in years, AD dates):
  * Tribunus laticlavius held at age 18-24, normally c. 20 (A.R. Birley,
    Fasti of Roman Britain 1981, 4-35; Roman Government of Britain 2005, 228).
  * Suffect consulship of a non-patrician without consular father ("novus homo")
    normally at c. 42, range c. 39-46 (G. Alfoldy, Konsulat und Senatorenstand
    unter den Antoninen, 1977). So tribunate -> consulship ~ 22 years, 17-27.
  * Legionary legateship 2-4 years (normally 3); praetorian proconsulship
    (Narbonensis) one year by lot; a gap of 0-2 years between posts is normal.
Sensitivity to these choices is reported.
"""
import json, sys
import numpy as np

rng = np.random.default_rng(20260914)
N = 200_000

def tri(lo, mode, hi, size=N):
    return rng.triangular(lo, mode, hi, size)

def sim(p_numisius_same=0.0, karus_shift=0.0, crisp_shift=0.0):
    out = {}
    # --- L. Aemilius Karus: cos. suff. March 144 (Eck & Pangerl, ZPE 193, 2015).
    # tribunate of IX Hispana was one of two tribunates held before quaestorship.
    interval = tri(17, 22, 27) + karus_shift
    karus_end = 144 - interval            # year his tribunate in IX (or the pair) ended
    out["Karus"] = karus_end
    # --- L. Novius Crispinus Martialis Saturninus: cos. des. 149 -> cos. 150.
    # A.R. Birley 2005, 287: praetorship c. 135; "perhaps at a slightly later age".
    interval = tri(18, 24, 30) + crisp_shift   # A.R. Birley 2005, 287: praetor c. 135; tribunate mid-120s (bounds 120-130)
    crisp_end = 150 - interval
    out["Crispinus"] = crisp_end
    # --- L. Aninius Sextius Florentinus: legate IX -> procos. Narbonensis (1 yr)
    # -> leg. Aug. Arabiae, attested 2 Dec 127 (P. Yadin 16), died in office
    # before T. Haterius Nepos (attested 130). Eck 1983, 158 n. 376: proconsulate
    # 123/4 or 124/5. Model: proconsular year starts 123, 124 or 125 (w .4/.4/.2),
    # gap 0-2 yrs between legateship and proconsulate.
    procos_start = rng.choice([123, 124, 125], p=[0.4, 0.4, 0.2], size=N)
    gap = rng.choice([0, 1, 2], p=[0.5, 0.35, 0.15], size=N)
    flor_end = procos_start - gap        # last year he was with the legion
    flor_dur = rng.choice([2, 3, 4], p=[0.3, 0.45, 0.25], size=N)
    out["Florentinus"] = flor_end.astype(float)
    out["Florentinus_start"] = (flor_end - flor_dur).astype(float)
    # --- Q. Camurius Numisius Iunior: tribune of IX (CIL XI 5670). If identical
    # with the consul of 161 (Eck 1972), his tribunate ~ 161 - 22. Keppie 1989
    # argues the consul may be the tribune's son. Mixture with p_numisius_same.
    same = rng.random(N) < p_numisius_same
    num_end = np.where(same, 161 - tri(17, 22, 27), 100 + rng.uniform(0, 20, N))
    out["Numisius"] = num_end
    last = np.maximum.reduce([karus_end, crisp_end, flor_end, num_end])
    out["last_attested"] = last
    return out

def summarize(o):
    yrs = np.arange(115, 166)
    res = {"P_exists_by_year": {int(y): float((o["last_attested"] >= y).mean()) for y in yrs}}
    for k in ["Karus", "Crispinus", "Florentinus", "Florentinus_start", "Numisius", "last_attested"]:
        v = o[k]
        res[k] = {"p05": float(np.percentile(v, 5)), "p25": float(np.percentile(v, 25)),
                  "median": float(np.median(v)), "p75": float(np.percentile(v, 75)),
                  "p95": float(np.percentile(v, 95))}
    return res

if __name__ == "__main__":
    results = {}
    for label, kw in {
        "base_numisius_father": dict(p_numisius_same=0.0),
        "numisius_same_p35": dict(p_numisius_same=0.35),
        "numisius_same_p50": dict(p_numisius_same=0.5),
        "numisius_same_p100": dict(p_numisius_same=1.0),
        "late_careers_plus3": dict(p_numisius_same=0.0, karus_shift=3, crisp_shift=3),
        "early_careers_minus3": dict(p_numisius_same=0.0, karus_shift=-3, crisp_shift=-3),
    }.items():
        results[label] = summarize(sim(**kw))
    json.dump(results, open("career_model_results.json", "w"), indent=1)
    b = results["base_numisius_father"]
    print("Base case (Numisius consul of 161 = son of the tribune):")
    for k in ["Florentinus_start", "Florentinus", "Karus", "Crispinus", "last_attested"]:
        s = b[k]; print(f"  {k:18s} median {s['median']:.1f}  90% band {s['p05']:.1f}-{s['p95']:.1f}")
    for y in [117, 119, 120, 122, 124, 126, 128, 130, 132, 135, 140]:
        print(f"  P(legion existed in {y}) = {b['P_exists_by_year'][y]:.3f}")
    for lab in ["numisius_same_p35", "numisius_same_p50", "numisius_same_p100", "late_careers_plus3", "early_careers_minus3"]:
        s = results[lab]
        print(lab, "last attested median", round(s["last_attested"]["median"],1),
              "P(>=122)", round(s["P_exists_by_year"][122],3), "P(>=126)", round(s["P_exists_by_year"][126],3),
              "P(>=132)", round(s["P_exists_by_year"][132],3), "P(>=140)", round(s["P_exists_by_year"][140],3))
