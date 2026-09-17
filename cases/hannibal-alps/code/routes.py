#!/usr/bin/env python3
"""Hannibal 218 BC: terrain and route model for the candidate Alpine passes.

Turns the ancient distances and day-counts (Polybius 3.39.9-10, 3.42-56; Livy
21.31-38) into testable numbers for each candidate route, using the Copernicus
GLO-90 DEM (dem.py) and place coordinates geocoded with Nominatim (geocode.py,
data/places.json).

Method
  1. Each route is a chain of named waypoints (valley towns, cols).  Between
     consecutive waypoints the route is *densified along the valley floor* by a
     least-cost path on the DEM grid (A*, 16-neighbour moves) with the cost
        cost = horizontal distance + 8 x |elevation change|
     (a Naismith-type climb penalty: 8 m of walking per metre of height; cells
     steeper than 70 % cost four times more; cells with no data are barred).
     On a plain this is the straight line; in a valley it follows the floor
     and refuses to cut across spurs.  The grid path is simplified
     (Douglas-Peucker, 100 m) to remove the staircase of the raster.
  2. The straight chords between waypoints are also checked: elevation sampled every 250 m along each chord, any sample more
     than 150 m above both endpoints is flagged (it means the chord climbs over
     terrain); the number of failing chords is reported per route, and the
     least-cost path is what is used for all distances.
  3. Profiles are sampled every 250 m along the least-cost path (bilinear DEM).
  3b. Zigzag correction: the least-cost path takes the fall line where the
     ground is steep; a mule track cannot.  "zigzag25" lengths replace every
     250-m step steeper than 25 % by a traverse at 25 % (length |dz|/0.25).
  4. Segments: (a) Rhone crossing -> "Island"; (b) Island -> beginning of the
     ascent; (c) ascent start -> col; (d) col -> plain (first point below 400 m
     in the Po basin); (e) whole traverse (b-start..plain end).  Three
     definitions of "beginning of the ascent" are reported:
        gate     : a named mountain gate chosen per route (where the route leaves
                   the broad main valley into a confined Alpine valley);
        flat10   : the end of the last 10-km stretch of level valley (mean
                   gradient < 0.5 %) before the col, i.e. the point after which
                   the route climbs without a further 10 km of level going;
        z500     : first point above 500 m.
     Distances to every named waypoint are tabulated separately so the report
     can apply any other definition.
  5. Polybius' figures: 4 days crossing -> Island; 800 stades in 10 days along
     the river Island -> ascent; 1400 stades crossing -> ascent; 1200 stades
     for the Alps; 9 days to the summit, 2 there, ~4 down (15 in all); a broken
     stretch of 1.5 stades on the descent (3.54.5) with (Livy 21.36.2) a drop
     of about 1000 feet.  Stade = 177.6 m (Attic) and 185 m (Olympic/Roman
     equivalence of 8 stades to the mile) are both used.

Outputs (data/): routes.json, profiles.json, routes_output.csv,
routes_output.md, waypoint_distances.csv, chord_check.csv.
Usage: python3 routes.py            (about 10-20 min: pure-Python A* on ~150 segments)
       python3 routes.py --quick    (skip the least-cost path; chords only; for tests)
"""
import csv
import heapq
import json
import math
import os
import sys
import time

import numpy as np

from dem import DEM, haversine_m

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
STADES = {"attic_177.6": 177.6, "185": 185.0}
POLYBIUS = {
    "days_crossing_to_island": 4,
    "stades_island_to_ascent": 800,
    "days_island_to_ascent": 10,
    "stades_crossing_to_ascent": 1400,
    "stades_alps": 1200,
    "days_ascent_to_summit": 9,
    "days_at_summit": 2,
    "days_descent": 4,
    "days_alps_total": 15,
    "broken_path_stades": 1.5,
    "livy_precipice_feet": 1000,
}
PLAIN_Z = 400.0  # "the plain": first point below 400 m in the Po basin
CLIMB_PENALTY = 8.0
CLIFF = 0.70
STEP_M = 250.0

# ----------------------------------------------------------------- places
with open(os.path.join(DATA, "places.json")) as f:
    PL = json.load(f)

# manual points: river crossings, confluences, valley-floor points, and fixes
# for commune centroids that Nominatim placed on hillsides (each checked on the DEM)
MANUAL = {
    "Fourques-Arles crossing": (43.678, 4.620, "Rhone at the Arles/Fourques bridge (manual, 43.678N 4.620E)"),
    "Beaucaire-Tarascon crossing": (43.807, 4.648, "Rhone between Beaucaire and Tarascon (manual)"),
    "Roquemaure crossing": (44.047, 4.765, "Rhone at Roquemaure (manual)"),
    "Island (i): Isere-Rhone confluence": (44.985, 4.855, "confluence just north of Valence (manual)"),
    "Island (ii): Aygues-Rhone confluence": (44.120, 4.730, "Aygues (Eygues) mouth near Caderousse (manual)"),
    "Drome-Rhone confluence (Loriol)": (44.755, 4.785, "Drome mouth below Loriol (manual)"),
    "Aime": (45.5547, 6.6489, "Aime town on the Isere; Nominatim centroid of Aime-la-Plagne was on the hillside (manual)"),
    "Vinadio": (44.3080, 7.1730, "Vinadio village in the Stura valley; commune centroid was at 1975 m (manual)"),
    "Argentera": (44.3946, 6.9375, "Argentera village; commune centroid was at 2234 m (manual)"),
    "Chatillon (Aosta)": (45.7495, 7.6155, "Chatillon town on the Dora Baltea (manual)"),
    "Pont-Saint-Martin": (45.5975, 7.7970, "Pont-Saint-Martin town (manual)"),
    "Val Clarea upper": (45.160, 6.955, "upper Val Clarea below Col Clapier (manual valley-floor point)"),
    "Val Clarea lower": (45.145, 6.985, "lower Val Clarea (manual valley-floor point)"),
    "Novalesa": (45.1895, 6.9795, "Novalesa, Cenischia valley below the Mont-Cenis (manual)"),
    "Lus-la-Croix-Haute": (44.664, 5.706, "Lus-la-Croix-Haute, upper Buech, below Col de Grimone (manual)"),
    "Mont-Cenis plateau (lake)": (45.232, 6.938, "Mont-Cenis plateau by the (modern) lake, on the old road (manual)"),
    "Les Echelles": (45.4355, 5.7515, "Les Echelles, the Guiers gap on the Lyon-Chambery road (Col de Couz 627 m) (manual)"),
}


def P(key):
    if key in MANUAL:
        lat, lon, src = MANUAL[key]
        return {"name": key, "lat": lat, "lon": lon, "source": src}
    v = PL[key]
    return {"name": key, "lat": v["lat"], "lon": v["lon"], "source": v["source"]}


# ----------------------------------------------------------------- routes
ISERE_TRUNK = ["Island (i): Isere-Rhone confluence", "Romans", "Saint-Marcellin", "Tullins", "Voreppe", "Grenoble",
               "Pontcharra", "Montmelian"]
MAURIENNE = ["Aiguebelle", "La Chambre", "Saint-Jean-de-Maurienne", "Saint-Michel-de-Maurienne", "Modane"]
SUSA_TO_TURIN = ["Susa", "Bussoleno", "Sant'Ambrogio di Torino", "Avigliana", "Rivoli", "Turin"]
DURANCE_DIRECT = ["Island (ii): Aygues-Rhone confluence", "Avignon", "Cavaillon", "Pertuis", "Manosque", "Sisteron", "Tallard"]
DROME_CABRE = ["Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte", "Montelimar", "Loriol", "Crest", "Saillans",
               "Die", "Luc-en-Diois", "Col de Cabre", "La Beaume", "Aspres-sur-Buech", "Veynes", "Gap", "Tallard"]
DROME_GRIMONE = ["Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte", "Montelimar", "Loriol", "Crest", "Saillans",
                 "Die", "Col de Grimone", "Lus-la-Croix-Haute", "Aspres-sur-Buech", "Veynes", "Gap", "Tallard"]
UPPER_DURANCE = ["Chorges", "Embrun", "Guillestre"]
AOSTA_TO_TURIN = ["Aosta", "Chatillon (Aosta)", "Pont-Saint-Martin", "Ivrea", "Chivasso", "Turin"]

ROUTES = {
    "R1": dict(name="Isere - Arc (Maurienne) - Col du Mont-Cenis", col="Col du Mont-Cenis", island="Island (i): Isere-Rhone confluence",
               gate="Aiguebelle",
               wps=ISERE_TRUNK + MAURIENNE + ["Bramans", "Termignon", "Lanslebourg", "Col du Mont-Cenis", "Mont-Cenis plateau (lake)",
                                              "Novalesa"] + SUSA_TO_TURIN),
    "R2": dict(name="Isere - Arc - Ambin/Savine - Col Clapier - Val Clarea", col="Col Clapier", island="Island (i): Isere-Rhone confluence",
               gate="Aiguebelle",
               wps=ISERE_TRUNK + MAURIENNE + ["Bramans", "Le Planay (Bramans)", "Lac Savine", "Col Clapier", "Val Clarea upper",
                                              "Val Clarea lower", "Giaglione"] + SUSA_TO_TURIN),
    "R2b": dict(name="Isere - Arc - Ambin - Col du Petit Mont-Cenis - Mont-Cenis plateau", col="Col du Petit Mont-Cenis",
                island="Island (i): Isere-Rhone confluence", gate="Aiguebelle",
                wps=ISERE_TRUNK + MAURIENNE + ["Bramans", "Le Planay (Bramans)", "Col du Petit Mont-Cenis", "Mont-Cenis plateau (lake)",
                                               "Novalesa"] + SUSA_TO_TURIN),
    "R3": dict(name="Isere - Tarentaise - Col du Petit-Saint-Bernard - Aosta - Ivrea", col="Col du Petit-Saint-Bernard",
               island="Island (i): Isere-Rhone confluence", gate="Albertville",
               wps=ISERE_TRUNK + ["Albertville", "Moutiers", "Aime", "Bourg-Saint-Maurice", "Seez", "Col du Petit-Saint-Bernard",
                                  "La Thuile", "Pre-Saint-Didier", "Morgex"] + AOSTA_TO_TURIN),
    "R3m": dict(name="R3 but to the Insubrian plain: Ivrea - Vercelli - Novara - Milan", col="Col du Petit-Saint-Bernard",
                island="Island (i): Isere-Rhone confluence", gate="Albertville",
                wps=ISERE_TRUNK + ["Albertville", "Moutiers", "Aime", "Bourg-Saint-Maurice", "Seez", "Col du Petit-Saint-Bernard",
                                   "La Thuile", "Pre-Saint-Didier", "Morgex", "Aosta", "Chatillon (Aosta)", "Pont-Saint-Martin",
                                   "Ivrea", "Vercelli", "Novara", "Milan"]),
    "R4": dict(name="Durance (direct from Avignon) - Briancon - Col de Montgenevre - Susa", col="Col de Montgenevre",
               island="Island (ii): Aygues-Rhone confluence", gate="Sisteron",
               wps=DURANCE_DIRECT + UPPER_DURANCE + ["L'Argentiere-la-Bessee", "Briancon", "Col de Montgenevre", "Claviere",
                                                     "Cesana Torinese", "Oulx", "Exilles"] + SUSA_TO_TURIN),
    "R4c": dict(name="Rhone - Drome - Col de Cabre - Gap - Durance - Col de Montgenevre (Livy/de Beer approach)", col="Col de Montgenevre",
                island="Island (ii): Aygues-Rhone confluence", gate="Crest",
                wps=DROME_CABRE + UPPER_DURANCE + ["L'Argentiere-la-Bessee", "Briancon", "Col de Montgenevre", "Claviere",
                                                   "Cesana Torinese", "Oulx", "Exilles"] + SUSA_TO_TURIN),
    "R5": dict(name="Durance (direct) - Guil - Col de la Traversette - Po (Saluzzo)", col="Col de la Traversette",
               island="Island (ii): Aygues-Rhone confluence", gate="Sisteron",
               wps=DURANCE_DIRECT + UPPER_DURANCE + ["Chateau-Ville-Vieille", "Aiguilles", "Abries", "Ristolas", "L'Echalp",
                                                     "Refuge du Viso", "Col de la Traversette", "Pian del Re", "Crissolo", "Paesana",
                                                     "Saluzzo", "Carmagnola", "Turin"]),
    "R5g": dict(name="Rhone - Drome - Col de Grimone - Gap - Durance - Guil - Traversette (de Beer 1955)", col="Col de la Traversette",
                island="Island (ii): Aygues-Rhone confluence", gate="Crest",
                wps=DROME_GRIMONE + UPPER_DURANCE + ["Chateau-Ville-Vieille", "Aiguilles", "Abries", "Ristolas", "L'Echalp",
                                                     "Refuge du Viso", "Col de la Traversette", "Pian del Re", "Crissolo", "Paesana",
                                                     "Saluzzo", "Carmagnola", "Turin"]),
    "R5c": dict(name="Rhone - Drome - Col de Cabre - Gap - Durance - Guil - Traversette", col="Col de la Traversette",
                island="Island (ii): Aygues-Rhone confluence", gate="Crest",
                wps=DROME_CABRE + UPPER_DURANCE + ["Chateau-Ville-Vieille", "Aiguilles", "Abries", "Ristolas", "L'Echalp",
                                                   "Refuge du Viso", "Col de la Traversette", "Pian del Re", "Crissolo", "Paesana",
                                                   "Saluzzo", "Carmagnola", "Turin"]),
    "R6": dict(name="Durance (direct) - Ubaye - Col de Larche - Stura - Cuneo", col="Col de Larche",
               island="Island (ii): Aygues-Rhone confluence", gate="Sisteron",
               wps=DURANCE_DIRECT + ["Le Lauzet-Ubaye", "Barcelonnette", "Jausiers", "Larche", "Col de Larche", "Argentera",
                                     "Pietraporzio", "Vinadio", "Demonte", "Borgo San Dalmazzo", "Cuneo", "Savigliano", "Carmagnola",
                                     "Turin"]),
    "R6v": dict(name="Durance (direct) - Guillestre - Col de Vars - Ubaye - Col de Larche - Cuneo", col="Col de Larche",
                island="Island (ii): Aygues-Rhone confluence", gate="Sisteron",
                wps=DURANCE_DIRECT + UPPER_DURANCE + ["Col de Vars", "Jausiers", "Larche", "Col de Larche", "Argentera",
                                                      "Pietraporzio", "Vinadio", "Demonte", "Borgo San Dalmazzo", "Cuneo", "Savigliano",
                                                      "Carmagnola", "Turin"]),
    "R7": dict(name="Rhone - Lyon - Geneva - Valais - Col du Grand-Saint-Bernard - Aosta - Ivrea", col="Col du Grand-Saint-Bernard",
               island="Island (i): Isere-Rhone confluence", gate="Martigny",
               wps=["Island (i): Isere-Rhone confluence", "Vienne", "Lyon", "Bourgoin-Jallieu", "Les Echelles", "Chambery", "Annecy", "Geneva",
                    "Villeneuve (Vaud)", "Saint-Maurice (Valais)", "Martigny", "Orsieres", "Bourg-Saint-Pierre",
                    "Col du Grand-Saint-Bernard", "Saint-Rhemy-en-Bosses", "Etroubles"] + AOSTA_TO_TURIN),
}

# Rhone legs: crossing -> Island, along the river (left bank plain)
RHONE_LEGS = {
    "Fourques/Arles -> Island (ii) Aygues": ["Fourques-Arles crossing", "Beaucaire-Tarascon crossing", "Avignon", "Roquemaure crossing",
                                             "Island (ii): Aygues-Rhone confluence"],
    "Beaucaire-Tarascon -> Island (ii) Aygues": ["Beaucaire-Tarascon crossing", "Avignon", "Roquemaure crossing",
                                                 "Island (ii): Aygues-Rhone confluence"],
    "Roquemaure -> Island (ii) Aygues": ["Roquemaure crossing", "Island (ii): Aygues-Rhone confluence"],
    "Fourques/Arles -> Island (i) Isere": ["Fourques-Arles crossing", "Beaucaire-Tarascon crossing", "Avignon", "Roquemaure crossing",
                                           "Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte", "Montelimar", "Loriol",
                                           "Valence", "Island (i): Isere-Rhone confluence"],
    "Beaucaire-Tarascon -> Island (i) Isere": ["Beaucaire-Tarascon crossing", "Avignon", "Roquemaure crossing",
                                               "Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte", "Montelimar", "Loriol",
                                               "Valence", "Island (i): Isere-Rhone confluence"],
    "Roquemaure -> Island (i) Isere": ["Roquemaure crossing", "Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte",
                                       "Montelimar", "Loriol", "Valence", "Island (i): Isere-Rhone confluence"],
    "Beaucaire-Tarascon -> Drome confluence (Loriol)": ["Beaucaire-Tarascon crossing", "Avignon", "Roquemaure crossing",
                                                        "Island (ii): Aygues-Rhone confluence", "Bollene", "Pierrelatte", "Montelimar",
                                                        "Drome-Rhone confluence (Loriol)"],
}

# ----------------------------------------------------------------- geometry helpers
DEG = math.pi / 180.0


def gc_km(a, b):
    return float(haversine_m(a[0], a[1], b[0], b[1])) / 1000.0


def bearing(a, b):
    la1, lo1, la2, lo2 = a[0] * DEG, a[1] * DEG, b[0] * DEG, b[1] * DEG
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def interp_points(a, b, step_m=STEP_M):
    """points every step_m along the chord a->b (inclusive of a, exclusive of b)"""
    d = haversine_m(a[0], a[1], b[0], b[1])
    n = max(int(d // step_m), 1)
    t = np.arange(n) / n
    return np.c_[a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]


def simplify(pts, tol_m):
    """Douglas-Peucker on lat/lon points using a local metric projection."""
    if len(pts) < 3:
        return list(pts)
    lat0 = pts[0][0]
    kx = 111320.0 * math.cos(lat0 * DEG)
    ky = 111132.0
    xy = [((p[1] - pts[0][1]) * kx, (p[0] - pts[0][0]) * ky) for p in pts]
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        (x1, y1), (x2, y2) = xy[i], xy[j]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            x, y = xy[k]
            if L2 == 0:
                dist = math.hypot(x - x1, y - y1)
            else:
                t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
                dist = math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
            if dist > best:
                best, bi = dist, k
        if best > tol_m:
            keep[bi] = True
            stack.append((i, bi))
            stack.append((bi, j))
    return [p for p, k in zip(pts, keep) if k]


# ----------------------------------------------------------------- least-cost path
MOVES = [(dr, dc) for dr in (-2, -1, 0, 1, 2) for dc in (-2, -1, 0, 1, 2)
         if (dr, dc) != (0, 0) and not (abs(dr) == 2 and abs(dc) == 2) and not (abs(dr) == 2 and dc == 0) and not (dr == 0 and abs(dc) == 2)]
# = 8 king moves + 8 knight moves (16 directions)


def least_cost_path(dem, a, b, margin_km=6.0, max_cells=1_500_000):
    """A* on the DEM window around chord a->b. Returns list of (lat, lon) grid-cell centres."""
    lat_mid = 0.5 * (a[0] + b[0])
    dlat = margin_km / 111.132
    dlon = margin_km / (111.32 * math.cos(lat_mid * DEG))
    lat_s, lat_n = min(a[0], b[0]) - dlat, max(a[0], b[0]) + dlat
    lon_w, lon_e = min(a[1], b[1]) - dlon, max(a[1], b[1]) + dlon
    Z, lats, lons = dem.window(lat_s, lat_n, lon_w, lon_e)
    nr, nc = Z.shape
    if nr * nc > max_cells:
        raise RuntimeError("window too large: %d x %d" % (nr, nc))
    dy = dem.dlat * 111132.0
    dx = dem.dlon * 111320.0 * math.cos(lat_mid * DEG)
    move_d = {m: math.hypot(m[0] * dy, m[1] * dx) for m in MOVES}
    # nearest cells
    r0 = int(round((lats[0] - a[0]) / dem.dlat))
    c0 = int(round((a[1] - lons[0]) / dem.dlon))
    r1 = int(round((lats[0] - b[0]) / dem.dlat))
    c1 = int(round((b[1] - lons[0]) / dem.dlon))
    r0, r1 = min(max(r0, 0), nr - 1), min(max(r1, 0), nr - 1)
    c0, c1 = min(max(c0, 0), nc - 1), min(max(c1, 0), nc - 1)
    Zl = Z.tolist()  # python lists are faster for scalar access
    start, goal = (r0, c0), (r1, c1)

    def h(r, c):
        return math.hypot((r - r1) * dy, (c - c1) * dx)

    g = {start: 0.0}
    came = {}
    pq = [(h(r0, c0), 0.0, start)]
    closed = set()
    while pq:
        f, gu, u = heapq.heappop(pq)
        if u in closed:
            continue
        if u == goal:
            break
        closed.add(u)
        ur, uc = u
        zu = Zl[ur][uc]
        for m in MOVES:
            vr, vc = ur + m[0], uc + m[1]
            if vr < 0 or vc < 0 or vr >= nr or vc >= nc:
                continue
            zv = Zl[vr][vc]
            if zv != zv or zu != zu:  # nan
                continue
            d = move_d[m]
            dz = zv - zu
            cost = d + CLIMB_PENALTY * abs(dz)
            if abs(dz) > CLIFF * d:
                cost *= 4.0
            gv = gu + cost
            v = (vr, vc)
            if gv < g.get(v, float("inf")):
                g[v] = gv
                came[v] = u
                heapq.heappush(pq, (gv + h(vr, vc), gv, v))
    if goal not in g:
        raise RuntimeError("no path found")
    path = [goal]
    while path[-1] != start:
        path.append(came[path[-1]])
    path.reverse()
    return [(float(lats[r]), float(lons[c])) for r, c in path], len(closed)


# ----------------------------------------------------------------- profile machinery
def build_route(dem, keys, quick=False, log=None):
    """returns dict with waypoints, path (simplified lat/lon), and the per-waypoint cumulative distance."""
    wps = [P(k) for k in keys]
    path = [(wps[0]["lat"], wps[0]["lon"])]
    wp_dist = [0.0]
    chord_fail = []
    cum = 0.0
    for i in range(len(wps) - 1):
        a = (wps[i]["lat"], wps[i]["lon"])
        b = (wps[i + 1]["lat"], wps[i + 1]["lon"])
        # chord check
        pts = interp_points(a, b)
        z = dem.elev_many(pts[:, 0], pts[:, 1])
        za, zb = dem.elev(*a), dem.elev(*b)
        bad = np.nansum(z > max(za, zb) + 150.0)
        if bad:
            chord_fail.append((wps[i]["name"], wps[i + 1]["name"], int(bad), float(np.nanmax(z) - max(za, zb))))
        if quick:
            seg = [a, b]
        else:
            t0 = time.time()
            try:
                seg, nvis = least_cost_path(dem, a, b)
            except RuntimeError as e:
                if log:
                    print("   LCP failed %s -> %s: %s; widening" % (wps[i]["name"], wps[i + 1]["name"], e), file=log)
                seg, nvis = least_cost_path(dem, a, b, margin_km=12.0)
            seg = simplify(seg, 100.0)
            if log:
                print("   %-28s -> %-28s %6.1f km  cells %7d  %.1fs" % (wps[i]["name"][:28], wps[i + 1]["name"][:28],
                                                                        sum(gc_km(seg[j], seg[j + 1]) for j in range(len(seg) - 1)),
                                                                        nvis, time.time() - t0), file=log)
                log.flush()
        for j in range(len(seg) - 1):
            cum += gc_km(seg[j], seg[j + 1])
        path.extend(seg[1:])
        wp_dist.append(cum)
    return {"waypoints": wps, "path": path, "wp_dist_km": wp_dist, "chord_fail": chord_fail}


def resample(dem, path, step_m=STEP_M):
    """profile every step_m along the polyline: arrays dist_km, lat, lon, z."""
    d = [0.0]
    lat = [path[0][0]]
    lon = [path[0][1]]
    carry = 0.0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        L = haversine_m(a[0], a[1], b[0], b[1])
        s = step_m - carry
        while s < L:
            t = s / L
            lat.append(a[0] + (b[0] - a[0]) * t)
            lon.append(a[1] + (b[1] - a[1]) * t)
            d.append(d[-1] + step_m / 1000.0)
            s += step_m
        carry = L - (s - step_m)
    lat.append(path[-1][0])
    lon.append(path[-1][1])
    d.append(d[-1] + carry / 1000.0)
    lat, lon, d = np.array(lat), np.array(lon), np.array(d)
    z = dem.elev_many(lat, lon)
    return d, lat, lon, z


def cumulative_ascent(z, hysteresis=10.0):
    """total climb with a hysteresis filter (ignores oscillations smaller than 10 m)."""
    up = 0.0
    down = 0.0
    ref = z[0]
    direction = 0
    for v in z[1:]:
        if v != v:
            continue
        if direction >= 0:
            if v > ref:
                ref = v
            elif ref - v > hysteresis:
                direction = -1
                ref = v
            else:
                continue
        else:
            if v < ref:
                ref = v
            elif v - ref > hysteresis:
                direction = 1
                ref = v
            else:
                continue
    # simpler robust approach: smooth then sum positive differences
    zs = np.array([v for v in z if v == v])
    k = 5
    zsm = np.convolve(zs, np.ones(k) / k, mode="valid")
    dz = np.diff(zsm)
    return float(np.sum(dz[dz > 0])), float(-np.sum(dz[dz < 0]))


def running_gradient(d_km, z, window_km):
    """gradient over forward windows of window_km, as a fraction; nan-padded."""
    n = int(round(window_km / (STEP_M / 1000.0)))
    g = np.full(len(z), np.nan)
    for i in range(len(z) - n):
        g[i] = (z[i + n] - z[i]) / (window_km * 1000.0)
    return g


def idx_at(d_km, x):
    return int(np.argmin(np.abs(d_km - x)))


def ascent_start_flat(d_km, z, i_col, window_km=10.0, flat=0.005):
    """end of the last 10-km window before the col whose mean gradient is below 0.5 %:
    the point after which the route climbs without any further 10 km of level valley."""
    g = running_gradient(d_km, z, window_km)
    n = int(round(window_km / (STEP_M / 1000.0)))
    last = 0
    for i in range(0, max(0, i_col - n)):
        if g[i] == g[i] and g[i] < flat:
            last = i + n
    return min(last, i_col)


def effective_len_km(d_km, z, i0, i1, gmax=0.25):
    """path length if every 250-m step steeper than gmax is taken as a zigzag at gmax
    (a mule track cannot climb the straight fall-line the least-cost path takes)."""
    tot = 0.0
    for i in range(i0, i1):
        dd = (d_km[i + 1] - d_km[i]) * 1000.0
        dz = abs(z[i + 1] - z[i]) if (z[i + 1] == z[i + 1] and z[i] == z[i]) else 0.0
        tot += max(dd, dz / gmax)
    return tot / 1000.0


def ascent_start_z(d_km, z, i_col, zthr=500.0):
    for i in range(i_col):
        if z[i] == z[i] and z[i] >= zthr:
            return i
    return 0


def first_below(d_km, z, i_from, zthr=PLAIN_Z):
    for i in range(i_from, len(z)):
        if z[i] == z[i] and z[i] < zthr:
            return i
    return len(z) - 1


def steepest_window(d_km, z, i0, i1, window_km):
    n = int(round(window_km / (STEP_M / 1000.0)))
    best, bi = 0.0, i0
    for i in range(i0, max(i0, i1 - n)):
        g = (z[i] - z[i + n]) / (window_km * 1000.0)  # descent positive
        if g == g and g > best:
            best, bi = g, i
    return best, bi


# ----------------------------------------------------------------- main
def main():
    quick = "--quick" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    dem = DEM()
    os.makedirs(DATA, exist_ok=True)
    log = sys.stdout
    out_routes = {}
    profiles = {}
    rows = []
    wp_rows = []
    chord_rows = []

    # ---- Rhone legs
    rhone = {}
    for name, keys in RHONE_LEGS.items():
        print("Rhone leg:", name, file=log)
        r = build_route(dem, keys, quick=quick, log=log)
        d, lat, lon, z = resample(dem, r["path"])
        straight = gc_km((r["waypoints"][0]["lat"], r["waypoints"][0]["lon"]), (r["waypoints"][-1]["lat"], r["waypoints"][-1]["lon"]))
        rhone[name] = {"km_valley": float(d[-1]), "km_straight": straight, "km_chain": float(sum(
            gc_km((r["waypoints"][i]["lat"], r["waypoints"][i]["lon"]), (r["waypoints"][i + 1]["lat"], r["waypoints"][i + 1]["lon"]))
            for i in range(len(r["waypoints"]) - 1))),
            "km_per_day_4days": float(d[-1]) / POLYBIUS["days_crossing_to_island"],
            "stades_attic": float(d[-1]) * 1000 / STADES["attic_177.6"], "stades_185": float(d[-1]) * 1000 / STADES["185"],
            "waypoints": r["waypoints"], "path": r["path"]}
        for cf in r["chord_fail"]:
            chord_rows.append((name,) + cf)

    # ---- routes
    for rid, R in ROUTES.items():
        if only and rid not in only:
            continue
        print("Route", rid, R["name"], file=log)
        r = build_route(dem, R["wps"], quick=quick, log=log)
        d, lat, lon, z = resample(dem, r["path"])
        names = [w["name"] for w in r["waypoints"]]
        wpd = r["wp_dist_km"]
        i_col = idx_at(d, wpd[names.index(R["col"])])
        # snap the col index to the highest sample within +-1 km of the col waypoint
        lo, hi = max(0, i_col - 4), min(len(z) - 1, i_col + 4)
        i_col = lo + int(np.nanargmax(z[lo:hi + 1]))
        col_z = float(z[i_col])
        # ascent-start definitions
        i_gate = idx_at(d, wpd[names.index(R["gate"])])
        i_grad = ascent_start_flat(d, z, i_col)
        i_z500 = ascent_start_z(d, z, i_col)
        i_plain = first_below(d, z, i_col)
        # 800-stade marks from the Island
        marks = {}
        for sname, sm in STADES.items():
            x = POLYBIUS["stades_island_to_ascent"] * sm / 1000.0
            i800 = idx_at(d, x)
            # nearest named waypoint
            j = int(np.argmin([abs(w - x) for w in wpd]))
            marks[sname] = {"km": x, "lat": float(lat[i800]), "lon": float(lon[i800]), "z": float(z[i800]),
                            "nearest_waypoint": names[j], "nearest_waypoint_km": wpd[j]}
        asc_up, asc_down = cumulative_ascent(z[i_gate:i_plain + 1])
        g1 = running_gradient(d, z, 1.0)
        # descent aspect: bearing from col to the point 2 km down
        i2 = min(i_col + 8, len(z) - 1)
        asp = bearing((lat[i_col], lon[i_col]), (lat[i2], lon[i2]))
        steep500, i_st = steepest_window(d, z, i_col, i_plain, 0.5)
        steep1k, i_st1 = steepest_window(d, z, i_col, i_plain, 1.0)
        # per-definition segment table
        defs = {"gate:" + R["gate"]: i_gate, "flat10": i_grad, "z500": i_z500}
        rec = {"id": rid, "name": R["name"], "col": R["col"], "col_z_dem": col_z, "col_lat": float(lat[i_col]), "col_lon": float(lon[i_col]),
               "island": R["island"], "km_total_island_to_end": float(d[-1]), "km_island_to_col": float(d[i_col]),
               "km_col_to_plain": float(d[i_plain] - d[i_col]), "plain_point": {"lat": float(lat[i_plain]), "lon": float(lon[i_plain]),
                                                                              "z": float(z[i_plain]), "km": float(d[i_plain])},
               "z_min": float(np.nanmin(z)), "z_max": float(np.nanmax(z)), "descent_bearing_first2km": asp,
               "steepest_500m_descent_grade": steep500, "steepest_500m_descent_at_km_from_col": float(d[i_st] - d[i_col]),
               "steepest_1km_descent_grade": steep1k, "max_1km_ascent_grade_gate_to_col": float(np.nanmax(g1[i_gate:i_col])),
               "max_1km_descent_grade": float(-np.nanmin(g1[i_col:i_plain])) if i_plain > i_col else float("nan"),
               "chord_segments_failing_150m_test": len(r["chord_fail"]), "n_waypoints": len(names),
               "mark_800_stades": marks, "definitions": {}}
        for dname, i0 in defs.items():
            km_b = float(d[i0])  # island -> ascent start (along valley)
            km_c = float(d[i_col] - d[i0])
            km_d = float(d[i_plain] - d[i_col])
            km_e = float(d[i_plain] - d[i0])
            up_c, _ = cumulative_ascent(z[i0:i_col + 1])
            _, down_d = cumulative_ascent(z[i_col:i_plain + 1])
            eff_c = effective_len_km(d, z, i0, i_col)
            eff_d = effective_len_km(d, z, i_col, i_plain)
            straight_b = gc_km((lat[0], lon[0]), (lat[i0], lon[i0]))
            straight_c = gc_km((lat[i0], lon[i0]), (lat[i_col], lon[i_col]))
            straight_d = gc_km((lat[i_col], lon[i_col]), (lat[i_plain], lon[i_plain]))
            straight_e = gc_km((lat[i0], lon[i0]), (lat[i_plain], lon[i_plain]))
            rec["definitions"][dname] = {
                "start": {"lat": float(lat[i0]), "lon": float(lon[i0]), "z": float(z[i0]), "km_from_island": km_b},
                "b_island_to_ascent_km": km_b, "b_straight_km": straight_b,
                "b_stades_attic": km_b * 1000 / 177.6, "b_stades_185": km_b * 1000 / 185.0,
                "b_km_per_day_10d": km_b / 10.0,
                "c_ascent_to_col_km": km_c, "c_straight_km": straight_c, "c_climb_m": up_c, "c_mean_grade": (col_z - float(z[i0])) / (km_c * 1000) if km_c > 0 else float("nan"),
                "c_km_per_day_9d": km_c / 9.0, "c_climb_m_per_day_9d": up_c / 9.0,
                "c_zigzag25_km": eff_c, "c_zigzag25_km_per_day_9d": eff_c / 9.0,
                "d_col_to_plain_km": km_d, "d_straight_km": straight_d, "d_descent_m": down_d, "d_mean_grade": (col_z - float(z[i_plain])) / (km_d * 1000) if km_d > 0 else float("nan"),
                "d_km_per_day_4d": km_d / 4.0, "d_km_per_day_3d": km_d / 3.0,
                "d_zigzag25_km": eff_d, "d_zigzag25_km_per_day_4d": eff_d / 4.0,
                "e_alps_km": km_e, "e_straight_km": straight_e, "e_stades_attic": km_e * 1000 / 177.6, "e_stades_185": km_e * 1000 / 185.0,
                "e_km_per_day_13_marching": km_e / 13.0, "e_km_per_day_15d": km_e / 15.0,
                "e_cum_ascent_m": cumulative_ascent(z[i0:i_plain + 1])[0],
            }
            rows.append([rid, R["name"], dname, R["col"], round(col_z), round(km_b, 1), round(straight_b, 1), round(km_b * 1000 / 177.6), round(km_b * 1000 / 185.0),
                         round(km_b / 10, 1), round(km_c, 1), round(straight_c, 1), round(up_c), round(km_c / 9, 1), round(up_c / 9),
                         round(km_d, 1), round(straight_d, 1), round(down_d), round(km_d / 4, 1), round(km_d / 3, 1),
                         round(km_e, 1), round(straight_e, 1), round(km_e * 1000 / 177.6), round(km_e * 1000 / 185.0), round(km_e / 13, 1),
                         round(100 * rec["max_1km_ascent_grade_gate_to_col"], 1), round(100 * rec["max_1km_descent_grade"], 1),
                         round(100 * steep500, 1), round(asp), len(r["chord_fail"]), round(eff_c, 1), round(eff_d, 1)])
        for w, wd in zip(r["waypoints"], wpd):
            zw = dem.elev(w["lat"], w["lon"])
            wp_rows.append([rid, w["name"], round(wd, 1), round(wd * 1000 / 177.6), round(wd * 1000 / 185), round(zw) if zw == zw else "", w["lat"], w["lon"], w["source"]])
        for cf in r["chord_fail"]:
            chord_rows.append((rid,) + cf)
        out_routes[rid] = dict(rec, waypoints=r["waypoints"], wp_dist_km=wpd, path=[(round(a, 5), round(b, 5)) for a, b in r["path"]])
        profiles[rid] = {"dist_km": [round(float(x), 3) for x in d], "z": [None if v != v else round(float(v), 1) for v in z],
                         "lat": [round(float(x), 5) for x in lat], "lon": [round(float(x), 5) for x in lon],
                         "i_col": int(i_col), "i_gate": int(i_gate), "i_flat10": int(i_grad), "i_z500": int(i_z500), "i_plain": int(i_plain)}
        print("  -> %s: island->col %.1f km, col %.0f m, col->plain %.1f km, chord fails %d" % (rid, d[i_col], col_z, d[i_plain] - d[i_col], len(r["chord_fail"])), file=log)

    # ---- write outputs
    with open(os.path.join(DATA, "routes.json"), "w") as f:
        json.dump({"stades_m": STADES, "polybius": POLYBIUS, "plain_threshold_m": PLAIN_Z, "cost_model": "d + 8|dz| (x4 if slope>70%)",
                   "rhone_legs": rhone, "routes": out_routes}, f, indent=1)
    with open(os.path.join(DATA, "profiles.json"), "w") as f:
        json.dump(profiles, f)
    hdr = ["route", "name", "ascent_start_def", "col", "col_z_dem_m", "b_island_to_ascent_km", "b_straight_km", "b_stades_177.6", "b_stades_185",
           "b_km_per_day_10d", "c_ascent_to_col_km", "c_straight_km", "c_climb_m", "c_km_per_day_9d", "c_climb_m_per_day",
           "d_col_to_plain_km", "d_straight_km", "d_descent_m", "d_km_per_day_4d", "d_km_per_day_3d",
           "e_alps_km", "e_straight_km", "e_stades_177.6", "e_stades_185", "e_km_per_day_13d",
           "max_1km_ascent_grade_pct", "max_1km_descent_grade_pct", "steepest_500m_descent_pct", "descent_bearing_deg", "chord_fail_count",
           "c_zigzag25_km", "d_zigzag25_km"]
    with open(os.path.join(DATA, "routes_output.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(rows)
    with open(os.path.join(DATA, "waypoint_distances.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["route", "waypoint", "km_from_island", "stades_177.6", "stades_185", "z_dem_m", "lat", "lon", "source"])
        w.writerows(wp_rows)
    with open(os.path.join(DATA, "chord_check.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["route", "from", "to", "n_samples_over_150m", "max_excess_m"])
        w.writerows(chord_rows)
    # markdown copy
    with open(os.path.join(DATA, "routes_output.md"), "w") as f:
        f.write("# Route model output (routes.py)\n\nRhone legs (crossing -> Island), along the valley floor (least-cost path on the DEM):\n\n")
        f.write("| leg | km along valley | km straight | km chain | stades (177.6) | stades (185) | km/day over 4 days |\n|---|---|---|---|---|---|---|\n")
        for k, v in rhone.items():
            f.write("| %s | %.0f | %.0f | %.0f | %.0f | %.0f | %.1f |\n" % (k, v["km_valley"], v["km_straight"], v["km_chain"], v["stades_attic"], v["stades_185"], v["km_per_day_4days"]))
        f.write("\nRoutes (all distances along the valley-floor path unless marked straight):\n\n| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n")
        for r in rows:
            f.write("| " + " | ".join(str(x) for x in r) + " |\n")
        f.write("\nChord check (straight segments between named waypoints that climb >150 m above both endpoints; these are the segments the least-cost path re-routes):\n\n| route | from | to | samples over | max excess m |\n|---|---|---|---|---|\n")
        for c in chord_rows:
            f.write("| %s | %s | %s | %d | %.0f |\n" % c)
    print("wrote routes.json, profiles.json, routes_output.csv/.md, waypoint_distances.csv, chord_check.csv", file=log)


if __name__ == "__main__":
    main()
