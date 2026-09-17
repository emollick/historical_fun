#!/usr/bin/env python3
"""Viewshed test of Polybius 3.54.2 and Livy 21.35.8 for each candidate col.

Polybius 3.54.2: from the summit of the pass Hannibal "pointed out to them the
plains of the Po" (ta peri ton Padon pedia) and the direction of Rome; Livy
21.35.8: "in promunturio quodam, unde longe ac late prospectus erat,
consistere iussis militibus Italiam ostentat subiectosque Alpinis montibus
Circumpadanos campos".

Test: from the col itself, from points along the descent (every 250 m for the
first 3 km, then every 1 km to 10 km), and from the nearest ground 100 m and
300 m higher than the col within 2.5 km (a knoll a general could climb), and
from every DEM cell within 1.5 km of the col that is 0-300 m above it
(vantage scan, 3-cell stride), is any terrain of the Po plain in line of sight?

  * DEM: Copernicus GLO-90 (surface model; 90 x 65 m cells at 45 N; modern
    tree cover and buildings are in the surface, which can only hide plain
    that would otherwise be visible, never create visibility).
  * Rays: 0.25 deg azimuth steps (1440 rays), samples every 90 m to 120 km,
    positions by the spherical direct geodesic, elevation by bilinear
    interpolation.
  * Earth curvature and standard refraction: effective height
        z_eff = z - (1 - k) d^2 / (2 R),  k = 0.13, R = 6371.0088 km.
  * Observer height 2 m above the DEM surface.
  * "Po plain" target = DEM cells below 400 m, east of 7.3 E and north of
    44.4 N (the Piedmont plain from Cuneo/Saluzzo to Ivrea and Vercelli; the
    Ligurian hills and the upper Cuneo plateau, which lie above 400 m, are
    excluded by the height rule).
  * A ray sample is visible when its elevation angle from the observer is
    >= the maximum elevation angle of all nearer samples on that ray.

Outputs: data/viewshed_output.json, data/viewshed_output.md, and
data/viewshed_cells.json (coarse grid of visible-plain cells per col, for the
figure).  Usage: python3 viewshed.py
"""
import json
import math
import os

import numpy as np

from dem import DEM

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
R_M = 6371008.8
K_REFR = 0.13
AZ_STEP = 0.25
MAX_KM = 120.0
SAMPLE_M = 90.0
OBS_H = 2.0
PLAIN_Z = 400.0
PLAIN_LON = 7.3
PLAIN_LAT = 44.4

# cols: (route id whose profile gives the descent, place key)
COLS = [
    ("R1", "Col du Mont-Cenis"),
    ("R2", "Col Clapier"),
    ("R2b", "Col du Petit Mont-Cenis"),
    ("R3", "Col du Petit-Saint-Bernard"),
    ("R4", "Col de Montgenevre"),
    ("R5", "Col de la Traversette"),
    ("R6", "Col de Larche"),
    ("R7", "Col du Grand-Saint-Bernard"),
    (None, "Col Agnel"),
]
# Col de la Croix (Colle della Croce): Nominatim returned nothing and the DEM bottleneck
# between the Guil and Pellice basins is 2496 m, not the map height, so it is left out.
MANUAL_COLS = {}


def dest(lat, lon, brg_deg, d_m):
    """spherical direct geodesic (vectorised). lat/lon scalars, brg/d arrays broadcastable."""
    la1 = math.radians(lat)
    lo1 = math.radians(lon)
    b = np.radians(brg_deg)
    dr = d_m / R_M
    la2 = np.arcsin(np.sin(la1) * np.cos(dr) + np.cos(la1) * np.sin(dr) * np.cos(b))
    lo2 = lo1 + np.arctan2(np.sin(b) * np.sin(dr) * np.cos(la1), np.cos(dr) - np.sin(la1) * np.sin(la2))
    return np.degrees(la2), np.degrees(lo2)


class Viewshed:
    def __init__(self, dem):
        self.dem = dem
        self.az = np.arange(0.0, 360.0, AZ_STEP)
        self.d = np.arange(SAMPLE_M, MAX_KM * 1000.0 + 1, SAMPLE_M)
        self.curv = (1.0 - K_REFR) * self.d ** 2 / (2.0 * R_M)

    def run(self, lat, lon, z_obs=None, keep_cells=False):
        dem = self.dem
        z0 = (dem.elev(lat, lon) if z_obs is None else z_obs) + OBS_H
        B, D = np.meshgrid(self.az, self.d, indexing="ij")
        la, lo = dest(lat, lon, B, D)
        z = dem.elev_many(la.ravel(), lo.ravel()).reshape(la.shape)
        zeff = z - self.curv[None, :]
        tan = (zeff - z0) / D
        tan_nan = np.where(np.isnan(tan), -np.inf, tan)
        prev_max = np.maximum.accumulate(tan_nan, axis=1)
        prev_max = np.concatenate([np.full((tan.shape[0], 1), -np.inf), prev_max[:, :-1]], axis=1)
        visible = (tan_nan >= prev_max) & ~np.isnan(z)
        plain = (z < PLAIN_Z) & (lo >= PLAIN_LON) & (la >= PLAIN_LAT) & ~np.isnan(z)
        vp = visible & plain
        any_vp = vp.any(axis=1)
        res = {"z_obs": float(z0 - OBS_H), "plain_visible": bool(any_vp.any()), "frac_azimuths_plain_visible": float(any_vp.mean()),
               "n_visible_plain_samples": int(vp.sum())}
        if any_vp.any():
            # nearest visible plain sample
            dd = np.where(vp, D, np.inf)
            i = np.unravel_index(np.argmin(dd), dd.shape)
            res["nearest_plain"] = {"km": float(D[i] / 1000.0), "azimuth": float(B[i]), "lat": float(la[i]), "lon": float(lo[i]), "z": float(z[i])}
            dd2 = np.where(vp, D, -np.inf)
            j = np.unravel_index(np.argmax(dd2), dd2.shape)
            res["farthest_plain"] = {"km": float(D[j] / 1000.0), "azimuth": float(B[j]), "lat": float(la[j]), "lon": float(lo[j]), "z": float(z[j])}
            azs = self.az[any_vp]
            res["azimuth_range_with_plain"] = [float(azs.min()), float(azs.max())]
        if keep_cells:
            # aggregate visible plain samples to a 0.02 deg grid for drawing
            cl = np.round(la[vp] / 0.02).astype(int)
            cn = np.round(lo[vp] / 0.02).astype(int)
            cells = sorted(set(zip(cl.tolist(), cn.tolist())))
            res["cells_0.02deg"] = [[c[0] * 0.02, c[1] * 0.02] for c in cells]
        return res


def saddle_search(dem, lat, lon, box_m=1200.0):
    """lowest DEM cell in the box that is a saddle: around a ring of radius 3 cells the
    sign of (z_ring - z_centre) changes 4 times.  Returns (lat, lon, z) or None."""
    dlat = box_m / 111132.0
    dlon = box_m / (111320.0 * math.cos(math.radians(lat)))
    Z, lats, lons = dem.window(lat - dlat, lat + dlat, lon - dlon, lon + dlon)
    nr, nc = Z.shape
    best = None
    ring = [(-3, 0), (-2, 2), (0, 3), (2, 2), (3, 0), (2, -2), (0, -3), (-2, -2)]
    for i in range(3, nr - 3):
        for j in range(3, nc - 3):
            zc = Z[i, j]
            signs = [np.sign(Z[i + a, j + b] - zc) for a, b in ring]
            changes = sum(1 for k in range(8) if signs[k] != signs[(k + 1) % 8] and signs[k] != 0 and signs[(k + 1) % 8] != 0)
            if changes >= 4 and (best is None or zc < best[2]):
                best = (float(lats[i]), float(lons[j]), float(zc))
    return best


def higher_ground(dem, lat, lon, dz, radius_m=2500.0):
    """nearest cell at least dz above the col's DEM height within radius."""
    z0 = dem.elev(lat, lon)
    dlat = radius_m / 111132.0
    dlon = radius_m / (111320.0 * math.cos(math.radians(lat)))
    Z, lats, lons = dem.window(lat - dlat, lat + dlat, lon - dlon, lon + dlon)
    LA, LO = np.meshgrid(lats, lons, indexing="ij")
    dist = np.hypot((LA - lat) * 111132.0, (LO - lon) * 111320.0 * math.cos(math.radians(lat)))
    ok = (Z >= z0 + dz) & (dist <= radius_m)
    if not ok.any():
        return None
    dist = np.where(ok, dist, np.inf)
    i = np.unravel_index(np.argmin(dist), dist.shape)
    return {"lat": float(LA[i]), "lon": float(LO[i]), "z": float(Z[i]), "dist_m": float(dist[i]), "dz_target": dz}


def main():
    dem = DEM()
    vs = Viewshed(dem)
    with open(os.path.join(DATA, "places.json")) as f:
        PL = json.load(f)
    with open(os.path.join(DATA, "profiles.json")) as f:
        PR = json.load(f)
    out = {"method": __doc__, "params": {"az_step_deg": AZ_STEP, "max_km": MAX_KM, "sample_m": SAMPLE_M, "k": K_REFR, "observer_h_m": OBS_H,
                                         "plain": {"z_below": PLAIN_Z, "lon_east_of": PLAIN_LON, "lat_north_of": PLAIN_LAT}}, "cols": {}}
    cells = {}
    md = ["# Viewshed test (viewshed.py)\n",
          "Target: Po plain = DEM < 400 m, east of 7.3E, north of 44.4N. Rays every 0.25 deg to 120 km; curvature + refraction k=0.13; observer 2 m.\n",
          "| col | DEM height at col (m) | plain visible from col | % azimuths (col) | nearest plain from col (km) | first descent point with plain visible (km from col) | % az there | +100 m knoll: visible / % az | +300 m knoll: visible / % az | vantage scan (cells <=1.5 km, <=300 m above): n seeing plain / n scanned; best % az |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for rid, key in COLS:
        if key in MANUAL_COLS:
            lat, lon = MANUAL_COLS[key]
            src = "manual nominal coordinate"
        else:
            lat, lon = PL[key]["lat"], PL[key]["lon"]
            src = PL[key]["source"]
        sad = saddle_search(dem, lat, lon)
        # the geocoded col positions were checked against the DEM (heights within 40 m of the
        # map heights, see terrain.md); the crude saddle search is kept only as a diagnostic.
        rec = {"geocoded": {"lat": lat, "lon": lon, "z_dem": dem.elev(lat, lon), "source": src}, "saddle_dem_diagnostic": sad}
        rec["used"] = {"lat": lat, "lon": lon, "z_dem": dem.elev(lat, lon)}
        print("%-28s geocoded z=%.0f saddle=%s" % (key, rec["geocoded"]["z_dem"], sad))
        # 1. the col
        r_col = vs.run(lat, lon, keep_cells=True)
        cells[key] = r_col.pop("cells_0.02deg")
        rec["col"] = r_col
        # 2. descent points
        desc = []
        first_vis = None
        if rid and rid in PR:
            p = PR[rid]
            i_col = p["i_col"]
            idx = list(range(i_col + 1, i_col + 13)) + list(range(i_col + 16, i_col + 41, 4))
            for i in idx:
                if i >= len(p["lat"]):
                    break
                r = vs.run(p["lat"][i], p["lon"][i])
                r.update({"km_from_col": round(p["dist_km"][i] - p["dist_km"][i_col], 3), "lat": p["lat"][i], "lon": p["lon"][i]})
                desc.append(r)
                if first_vis is None and r["plain_visible"]:
                    first_vis = r
        rec["descent_points"] = desc
        rec["first_descent_point_with_plain"] = first_vis
        # 3. knolls
        for dz in (100, 300):
            hg = higher_ground(dem, lat, lon, dz)
            if hg:
                r = vs.run(hg["lat"], hg["lon"])
                r.update(hg)
                rec["knoll_+%d" % dz] = r
            else:
                rec["knoll_+%d" % dz] = None
        # 4. vantage scan: every DEM cell within 1.5 km of the col and 0-300 m above it (3-cell stride)
        best = None
        n_scan = 0
        n_vis = 0
        z0 = rec["used"]["z_dem"]
        Zw, la_w, lo_w = dem.window(lat - 1.5 / 111.132, lat + 1.5 / 111.132, lon - 1.5 / (111.32 * math.cos(math.radians(lat))), lon + 1.5 / (111.32 * math.cos(math.radians(lat))))
        for ii in range(0, Zw.shape[0], 3):
            for jj in range(0, Zw.shape[1], 3):
                zz = Zw[ii, jj]
                if zz != zz or zz < z0 or zz > z0 + 300:
                    continue
                dist = math.hypot((la_w[ii] - lat) * 111132.0, (lo_w[jj] - lon) * 111320.0 * math.cos(math.radians(lat)))
                if dist > 1500:
                    continue
                n_scan += 1
                r = vs.run(float(la_w[ii]), float(lo_w[jj]))
                if r["plain_visible"]:
                    n_vis += 1
                if best is None or r["frac_azimuths_plain_visible"] > best["frac_azimuths_plain_visible"]:
                    best = dict(r, lat=float(la_w[ii]), lon=float(lo_w[jj]), z=float(zz), dist_m=dist)
        rec["vantage_scan"] = {"n_points": n_scan, "n_with_plain_visible": n_vis, "best": best}
        print("   vantage scan: %d points within 1.5 km and <=300 m above; %d see the plain; best %.1f%% at %s" % (
            n_scan, n_vis, 100 * (best["frac_azimuths_plain_visible"] if best else 0), ("%.0f m, %.0f m away" % (best["z"], best["dist_m"])) if best else "-"))
        out["cols"][key] = rec
        k1, k3 = rec["knoll_+100"], rec["knoll_+300"]
        md.append("| %s | %.0f | %s | %.1f | %s | %s | %s | %s | %s | %s |" % (
            key, rec["used"]["z_dem"], "yes" if r_col["plain_visible"] else "no", 100 * r_col["frac_azimuths_plain_visible"],
            ("%.1f" % r_col["nearest_plain"]["km"]) if r_col["plain_visible"] else "-",
            ("%.2f" % first_vis["km_from_col"]) if first_vis else ("none within 10 km" if desc else "n/a"),
            ("%.1f" % (100 * first_vis["frac_azimuths_plain_visible"])) if first_vis else "-",
            ("%s / %.1f (%.0f m, %.0f m away)" % ("yes" if k1["plain_visible"] else "no", 100 * k1["frac_azimuths_plain_visible"], k1["z"], k1["dist_m"])) if k1 else "none within 2.5 km",
            ("%s / %.1f (%.0f m, %.0f m away)" % ("yes" if k3["plain_visible"] else "no", 100 * k3["frac_azimuths_plain_visible"], k3["z"], k3["dist_m"])) if k3 else "none within 2.5 km",
            "%d / %d; best %.1f%% (%.0f m, %.0f m away)" % (n_vis, n_scan, 100 * (best["frac_azimuths_plain_visible"] if best else 0), best["z"] if best else 0, best["dist_m"] if best else 0)))
        print("   col: plain visible=%s frac=%.3f; first descent pt=%s; knoll100=%s knoll300=%s" % (
            r_col["plain_visible"], r_col["frac_azimuths_plain_visible"], first_vis["km_from_col"] if first_vis else None,
            k1["plain_visible"] if k1 else None, k3["plain_visible"] if k3 else None))
    with open(os.path.join(DATA, "viewshed_output.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(DATA, "viewshed_cells.json"), "w") as f:
        json.dump(cells, f)
    with open(os.path.join(DATA, "viewshed_output.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print("wrote viewshed_output.json/.md, viewshed_cells.json")


if __name__ == "__main__":
    main()
