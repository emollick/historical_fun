#!/usr/bin/env python3
"""Generate the markdown tables used in dossiers/terrain.md from the data files.

Reads data/routes.json, data/routes_output.csv, data/waypoint_distances.csv,
data/viewshed_output.json, data/pleiades_output.json and writes
data/terrain_tables.md.  Run after routes.py, viewshed.py and pleiades.py.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

MAIN = ["R1", "R2", "R2b", "R3", "R4", "R4c", "R5", "R5g", "R5c", "R6", "R6v", "R7"]
COLMAP = {"R1": "Col du Mont-Cenis", "R2": "Col Clapier", "R2b": "Col du Petit Mont-Cenis", "R3": "Col du Petit-Saint-Bernard",
          "R4": "Col de Montgenevre", "R4c": "Col de Montgenevre", "R5": "Col de la Traversette", "R5g": "Col de la Traversette",
          "R5c": "Col de la Traversette", "R6": "Col de Larche", "R6v": "Col de Larche", "R7": "Col du Grand-Saint-Bernard"}
MAPH = {"Col du Mont-Cenis": 2083, "Col Clapier": 2482, "Col du Petit Mont-Cenis": 2183, "Col du Petit-Saint-Bernard": 2188,
        "Col de Montgenevre": 1854, "Col de la Traversette": 2947, "Col de Larche": 1991, "Col du Grand-Saint-Bernard": 2469, "Col Agnel": 2744}


def band(kmd, lo=12, hi=25):
    if kmd != kmd:
        return "?"
    return "in band" if lo <= kmd <= hi else ("slow" if kmd < lo else "fast")


def main():
    R = json.load(open(os.path.join(DATA, "routes.json")))
    V = json.load(open(os.path.join(DATA, "viewshed_output.json")))
    PLE = json.load(open(os.path.join(DATA, "pleiades_output.json")))
    W = list(csv.DictReader(open(os.path.join(DATA, "waypoint_distances.csv"))))
    out = []
    # ---- Table A: key results (gate definition)
    out.append("### Table A. Key results per candidate (ascent start = named gate; distances along the valley-floor path)\n")
    out.append("| route | col (map m / DEM m) | Island -> gate km (stades 177.6 / 185) | gate -> col km (climb m) | km/day over 9 d | col -> plain km | km/day over 4 d (3 d) | gate -> plain km (stades 177.6 / 185) | km/day over 13 marching d | steepest 500 m on descent (% , km from col) | plain visible from col (% azimuths) |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for rid in MAIN:
        r = R["routes"][rid]
        gate = [k for k in r["definitions"] if k.startswith("gate")][0]
        d = r["definitions"][gate]
        col = r["col"]
        vs = V["cols"].get(col, {}).get("col", {})
        out.append("| %s %s | %s %d / %.0f | %s %.0f (%.0f / %.0f) | %.0f (+%.0f) | %.1f | %.0f | %.1f (%.1f) | %.0f (%.0f / %.0f) | %.1f | %.0f%% at %.1f km | %s (%.1f%%) |" % (
            rid, r["name"], col.replace("Col ", ""), MAPH[col], r["col_z_dem"], gate.split(":")[1], d["b_island_to_ascent_km"], d["b_stades_attic"], d["b_stades_185"],
            d["c_ascent_to_col_km"], d["c_climb_m"], d["c_km_per_day_9d"], d["d_col_to_plain_km"], d["d_km_per_day_4d"], d["d_km_per_day_3d"],
            d["e_alps_km"], d["e_stades_attic"], d["e_stades_185"], d["e_km_per_day_13_marching"],
            100 * r["steepest_500m_descent_grade"], r["steepest_500m_descent_at_km_from_col"],
            "yes" if vs.get("plain_visible") else "no", 100 * vs.get("frac_azimuths_plain_visible", 0)))
    # ---- Table B: three definitions of the ascent start
    out.append("\n### Table B. Sensitivity to the definition of the 'beginning of the ascent'\n")
    out.append("| route | definition | start (m, km from Island) | b: Island->start km (stades 177.6) | c: start->col km, zigzag-corrected km, km/day/9d | e: start->plain km (stades 177.6), km/day/13d |")
    out.append("|---|---|---|---|---|---|")
    for rid in MAIN:
        r = R["routes"][rid]
        for dn, d in r["definitions"].items():
            out.append("| %s | %s | %.0f m, %.0f km | %.0f (%.0f) | %.0f, %.0f, %.1f | %.0f (%.0f), %.1f |" % (
                rid, dn, d["start"]["z"], d["start"]["km_from_island"], d["b_island_to_ascent_km"], d["b_stades_attic"],
                d["c_ascent_to_col_km"], d["c_zigzag25_km"], d["c_zigzag25_km_per_day_9d"], d["e_alps_km"], d["e_stades_attic"], d["e_km_per_day_13_marching"]))
    # ---- Table C: Rhone legs
    out.append("\n### Table C. Rhone crossing -> 'Island' (Polybius 3.49.5: four days' march)\n")
    out.append("| leg | km along valley | km straight | stades (177.6 / 185) | km/day over 4 days | band 12-25 |")
    out.append("|---|---|---|---|---|---|")
    for k, v in R["rhone_legs"].items():
        out.append("| %s | %.0f | %.0f | %.0f / %.0f | %.1f | %s |" % (k, v["km_valley"], v["km_straight"], v["stades_attic"], v["stades_185"], v["km_per_day_4days"], band(v["km_per_day_4days"])))
    # ---- Table D: 800-stade marks
    out.append("\n### Table D. Where 800 stades from the Island falls (Polybius 3.50.1) and the straight-line ('crow') distances\n")
    out.append("| route | 800 st @177.6 m = 142.1 km falls at | 800 st @185 m = 148.0 km falls at | Island->gate straight km | gate->col straight km | col->plain straight km | gate->plain straight km |")
    out.append("|---|---|---|---|---|---|---|")
    for rid in MAIN:
        r = R["routes"][rid]
        m = r["mark_800_stades"]
        gate = [k for k in r["definitions"] if k.startswith("gate")][0]
        d = r["definitions"][gate]
        out.append("| %s | %s (%.0f m; nearest waypoint %s at %.0f km) | %s (nearest %s at %.0f km) | %.0f | %.0f | %.0f | %.0f |" % (
            rid, "%.3fN %.3fE" % (m["attic_177.6"]["lat"], m["attic_177.6"]["lon"]), m["attic_177.6"]["z"], m["attic_177.6"]["nearest_waypoint"], m["attic_177.6"]["nearest_waypoint_km"],
            "%.3fN %.3fE" % (m["185"]["lat"], m["185"]["lon"]), m["185"]["nearest_waypoint"], m["185"]["nearest_waypoint_km"],
            d["b_straight_km"], d["c_straight_km"], d["d_straight_km"], d["e_straight_km"]))
    # ---- Table E: named-point distances
    out.append("\n### Table E. Cumulative distance from the Island at named points (km; stades at 177.6 m in brackets)\n")
    want = {"R1": ["Grenoble", "Montmelian", "Aiguebelle", "Saint-Jean-de-Maurienne", "Modane", "Lanslebourg", "Col du Mont-Cenis", "Susa", "Turin"],
            "R2": ["Modane", "Bramans", "Le Planay (Bramans)", "Lac Savine", "Col Clapier", "Giaglione", "Susa", "Turin"],
            "R3": ["Montmelian", "Albertville", "Moutiers", "Bourg-Saint-Maurice", "Col du Petit-Saint-Bernard", "Aosta", "Ivrea", "Turin"],
            "R4": ["Avignon", "Cavaillon", "Manosque", "Sisteron", "Tallard", "Embrun", "Guillestre", "L'Argentiere-la-Bessee", "Briancon", "Col de Montgenevre", "Susa", "Turin"],
            "R4c": ["Loriol", "Crest", "Die", "Luc-en-Diois", "Col de Cabre", "Gap", "Tallard", "Guillestre", "Briancon", "Col de Montgenevre", "Turin"],
            "R5": ["Sisteron", "Tallard", "Guillestre", "Abries", "Refuge du Viso", "Col de la Traversette", "Pian del Re", "Paesana", "Saluzzo", "Turin"],
            "R5g": ["Loriol", "Crest", "Die", "Col de Grimone", "Gap", "Guillestre", "Col de la Traversette", "Saluzzo", "Turin"],
            "R6": ["Sisteron", "Tallard", "Le Lauzet-Ubaye", "Barcelonnette", "Jausiers", "Col de Larche", "Vinadio", "Cuneo", "Savigliano", "Turin"],
            "R7": ["Lyon", "Les Echelles", "Geneva", "Martigny", "Col du Grand-Saint-Bernard", "Aosta", "Ivrea", "Turin"]}
    for rid, names in want.items():
        out.append("- **%s**: " % rid + "; ".join("%s %s (%s)" % (w["waypoint"], w["km_from_island"], w["stades_177.6"]) for w in W if w["route"] == rid and w["waypoint"] in names))
    # ---- Table F: viewshed
    out.append("\n### Table F. Viewshed of the Po plain (viewshed.py; plain = DEM < 400 m, east of 7.3E, north of 44.4N; 0.25 deg rays to 120 km; k = 0.13; observer 2 m)\n")
    out.append("| col | DEM height (m) | from the col: plain visible, % of azimuths, nearest plain km | first point on the descent with plain visible (km from col; % az) | +100 m knoll | +300 m knoll | vantage scan: cells <=1.5 km & <=300 m above seeing plain / scanned; best % az (height, distance) |")
    out.append("|---|---|---|---|---|---|---|")
    for key, rec in V["cols"].items():
        c = rec["col"]
        fv = rec.get("first_descent_point_with_plain")
        k1, k3 = rec.get("knoll_+100"), rec.get("knoll_+300")
        sc = rec.get("vantage_scan", {})
        b = sc.get("best")
        out.append("| %s | %.0f | %s, %.1f%%, %s | %s | %s | %s | %s |" % (
            key, rec["used"]["z_dem"], "yes" if c["plain_visible"] else "no", 100 * c["frac_azimuths_plain_visible"],
            ("%.0f km" % c["nearest_plain"]["km"]) if c["plain_visible"] else "-",
            ("%.2f km; %.1f%%" % (fv["km_from_col"], 100 * fv["frac_azimuths_plain_visible"])) if fv else ("none within 10 km" if rec["descent_points"] else "n/a (not on a modelled route)"),
            ("%s %.1f%% (%.0f m, %.0f m away)" % ("yes" if k1["plain_visible"] else "no", 100 * k1["frac_azimuths_plain_visible"], k1["z"], k1["dist_m"])) if k1 else "none within 2.5 km",
            ("%s %.1f%% (%.0f m, %.0f m away)" % ("yes" if k3["plain_visible"] else "no", 100 * k3["frac_azimuths_plain_visible"], k3["z"], k3["dist_m"])) if k3 else "none within 2.5 km",
            ("%d / %d; best %.1f%% (%.0f m, %.0f m away)" % (sc.get("n_with_plain_visible", 0), sc.get("n_points", 0), 100 * b["frac_azimuths_plain_visible"], b["z"], b["dist_m"])) if b else "-"))
    # ---- Table H: crossing -> plain totals against Polybius' 1400 + 1200 = 2600 stades
    out.append("\n### Table H. Rhone crossing -> Po plain in total, against Polybius 3.39.9-10 (1400 + 1200 = 2600 stades = 462 km at 177.6 m, 481 km at 185 m)\n")
    out.append("| route | Island | crossing option | crossing->Island km | Island->plain km | total km | total stades (177.6 / 185) | % of 2600 st (177.6) |")
    out.append("|---|---|---|---|---|---|---|---|")
    legs = R["rhone_legs"]
    for rid in MAIN:
        r = R["routes"][rid]
        isl = "Isere" if "Isere" in r["island"] else "Aygues"
        ip = r["km_island_to_col"] + r["km_col_to_plain"]
        for cname in ["Fourques/Arles", "Beaucaire-Tarascon", "Roquemaure"]:
            leg = [v for k, v in legs.items() if k.startswith(cname) and isl in k]
            if not leg:
                continue
            tot = leg[0]["km_valley"] + ip
            out.append("| %s | %s | %s | %.0f | %.0f | %.0f | %.0f / %.0f | %.0f%% |" % (rid, isl, cname, leg[0]["km_valley"], ip, tot, tot * 1000 / 177.6, tot * 1000 / 185, 100 * tot * 1000 / 177.6 / 2600))
    # ---- Table G: Pleiades
    out.append("\n### Table G. Pleiades (Alcyone) phases in 218 BC at 45 N, proleptic Julian calendar (pleiades.py)\n")
    out.append("| event | sun -0.833 (true) | h = 6 | h = 7.5 | h = 9 | h = 11 (Schoch) | pyephem cross-check agrees |")
    out.append("|---|---|---|---|---|---|---|")
    for ev in ["morning_setting", "evening_setting", "acronychal_rising", "heliacal_rising"]:
        s = PLE["skyfield"][ev]
        p = PLE["pyephem"][ev]
        agree = all(s[k]["date"] == p[k]["date"] for k in PLE["thresholds_deg"])
        out.append("| %s | %s | %s | %s | %s | %s | %s |" % (ev.replace("_", " "), s["true (sun -0.833)"]["date"], s["h=6"]["date"], s["h=7.5"]["date"], s["h=9"]["date"], s["h=11 (Schoch)"]["date"], "yes" if agree else "NO"))
    with open(os.path.join(DATA, "terrain_tables.md"), "w") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
