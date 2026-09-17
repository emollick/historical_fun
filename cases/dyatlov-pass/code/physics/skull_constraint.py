"""Constraint on the loader of Thibeaux-Brignolle's temporal fracture.

Replacement for section D of slab_impact.py, whose range (0.06-3 kN) overlaps the
fracture threshold (2.5-10 kN) and so does not exclude snow.

A block of snow can transmit at most F = sigma_c * A, where sigma_c is the pressure at
which the snow crushes rather than pushes and A the area it bears on.  This script
prints (1) the force cap for a grid of crushing pressures and contact areas and (2) the
crushing pressure that would be needed to reach the cadaver-test thresholds over each
area.  Nothing here discriminates the tent from the ravine.

Inputs and where they come from
  Fracture:  depressed area 9 x 7 cm, bone piece 3 x 3.5 x 2 cm driven onto the dura
             (autopsy act, case file vol. 1, sheet 353).
  Threshold: temporo-parietal fracture 2.5-10 kN, mean 5.2 kN, flat 5 x 10 cm plate or
             2.54 cm disc (Allsop, Perl, Warner 1991, SAE 912907); 5.6-9.9 kN
             (Yoganandan & Pintar 2004, Clin. Biomech. 19:225).
  Snow:      Gaume & Puzrin 2021, Methods, MPM parameters: pre-consolidation pressure
             p0 = 30 kPa (slab, 300 kg/m3) and p0w = 100 kPa (wind slab, 400 kg/m3),
             hardening with compaction (their Eq. 48).
             Mellor 1975, IAHS Publ. 114, Fig. 17 (p. 277): uniaxial compressive strength
             of dry, coherent snow under rapid loading, read from the plot as about
             300-700 kPa at 0.40 g/cm3 and 500-950 kPa at 0.46 g/cm3 (site densities:
             Popovnin 2019 0.40; Borzenkov 458 kg/m3).  The same figure puts tensile
             strength at 0.40 g/cm3 near 190 kPa against the 6-10 kPa the 2021 paper
             assigns its slab, so a young natural slab sits at or below the band.
"""
areas = {  # cm^2
    "bone piece 3 x 3.5 cm": 3 * 3.5,
    "Allsop plate 5 x 10 cm": 50.0,
    "depression 9 x 7 cm": 63.0,
    "section D largest area": 100.0,
}
pressures = {  # kPa
    "GP21 slab p0 (300 kg/m3)": 30,
    "GP21 wind slab p0w (400 kg/m3)": 100,
    "section D hardest snow": 300,
    "Mellor 1975, 0.40 g/cm3, lower": 300,
    "Mellor 1975, 0.40 g/cm3, upper": 700,
    "Mellor 1975, 0.46 g/cm3, upper": 950,
}
thresholds = {"Allsop floor": 2.5, "Allsop mean": 5.2, "Allsop ceiling": 10.0}  # kN

print("== 1. Force cap F = sigma_c * A (kN) ==")
print(f"{'':36s}" + "".join(f"{k[:22]:>24s}" for k in areas))
for pn, p in pressures.items():
    row = "".join(f"{p*1e3*a*1e-4/1e3:24.2f}" for a in areas.values())
    print(f"{pn:36s}{row}")
print()
print("== 2. Crushing pressure needed to reach each threshold (kPa) ==")
print(f"{'':36s}" + "".join(f"{k[:22]:>24s}" for k in areas))
for tn, t in thresholds.items():
    row = "".join(f"{t*1e3/(a*1e-4)/1e3:24.0f}" for a in areas.values())
    print(f"{tn + ' ' + str(t) + ' kN':36s}{row}")
print()
print("Reading: over the whole depression the 2.5 kN floor needs about 400 kPa and the 5.2 kN")
print("mean about 800 kPa; over the bone piece alone 2.4 and 5.0 MPa (ice or rock, not snow).")
print("At the 100 kPa the 2021 model assigns its wind slab, a face on the whole depression gives")
print("0.6 kN.  Mellor's rapid-loading band for laboratory snow at the site densities reaches")
print("400-950 kPa.  So: a soft or medium slab is excluded as the sole loader; a hard, well-")
print("sintered slab or crust bearing on most of the depression with the head backed, or a hard")
print("object between snow and bone, is not.  A constraint, not an exclusion; no share moves.")
