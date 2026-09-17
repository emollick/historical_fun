#!/usr/bin/env python3
"""dem_slope.py - slope analysis of the Kholat Syakhl east slope (Dyatlov Pass) from Copernicus GLO-30.

Input : raw/Copernicus_DSM_COG_10_N61_00_E059_00_DEM.tif  (Copernicus DEM GLO-30, tile N61/E059,
        public AWS bucket copernicus-dem-30m; float32 metres above EGM2008; grid 1" lat x 2" lon
        at this latitude band, i.e. ~31 m x ~29 m; PixelIsPoint georeferencing)
        data/coordinates.csv
Output: out/slopes_at_sites.csv       slope/aspect at every candidate site for several window sizes
        out/profile_tent_cedar.csv    profile tent -> cedar every 25 m
        out/profile_upslope.csv       profile 0-300 m directly upslope of the tent (two directions)
        out/dem_summary.json / .md    headline numbers used in the write-up
        out/map_dem.png, out/profile_tent_cedar.png
Every number in the write-up's slope section comes from this script.
"""
import csv, json, math, os
import numpy as np
import tifffile
from scipy.interpolate import RegularGridInterpolator
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from geo_common import RAW, OUT, DATA, load_coordinates, to_xy, from_xy, MLAT, MLON, REF_LAT, REF_LON, haversine, bearing

DEM_PATH = os.path.join(RAW, "Copernicus_DSM_COG_10_N61_00_E059_00_DEM.tif")
LON0, LAT0 = 59.0, 62.0          # ModelTiepoint: raster (0,0) is the point 59.0E 62.0N (GTRasterType = PixelIsPoint)
DLON, DLAT = 1 / 1800, 1 / 3600  # ModelPixelScale (deg): 2" in longitude, 1" in latitude
NOISE_SIGMA = 1.5                # m, assumed random relative vertical error of GLO-30 per pixel (spec: <2 m LE90 for slopes <20 %)
RNG = np.random.default_rng(42)

# ---------------------------------------------------------------- load DEM window
with tifffile.TiffFile(DEM_PATH) as tf:
    page = tf.pages[0]
    tags = {t.name: t.value for t in page.tags.values() if t.name in ("ModelPixelScaleTag", "ModelTiepointTag", "GeoKeyDirectoryTag")}
    full = page.asarray()
assert tuple(round(v, 12) for v in tags["ModelPixelScaleTag"][:2]) == (round(DLON, 12), round(DLAT, 12)), tags
assert tags["ModelTiepointTag"][3:5] == (LON0, LAT0), tags
LAT_MIN, LAT_MAX, LON_MIN, LON_MAX = 61.70, 61.80, 59.35, 59.50
r0, r1 = int(round((LAT0 - LAT_MAX) / DLAT)), int(round((LAT0 - LAT_MIN) / DLAT)) + 1
c0, c1 = int(round((LON_MIN - LON0) / DLON)), int(round((LON_MAX - LON0) / DLON)) + 1
Z = full[r0:r1, c0:c1].astype(float)
lats = LAT0 - np.arange(r0, r1) * DLAT          # pixel-centre latitudes (descending)
lons = LON0 + np.arange(c0, c1) * DLON          # pixel-centre longitudes
X = (lons - REF_LON) * MLON                     # metres east of TL 18.10
Y = (lats - REF_LAT) * MLAT                     # metres north of TL 18.10 (descending with row)
DX = DLON * MLON                                # 29.34 m
DY = DLAT * MLAT                                # 30.96 m
XX, YY = np.meshgrid(X, Y)
del full

# bilinear interpolator on (y ascending, x ascending)
Zi = Z[::-1, :]
Yasc = Y[::-1]
interp = RegularGridInterpolator((Yasc, X), Zi, method="linear", bounds_error=False, fill_value=np.nan)
def z_at(x, y):
    return float(interp((y, x)))

# ---------------------------------------------------------------- slope helpers
def horn_slope(Zarr, i, j):
    """Horn (1981) 3x3 gradient at pixel (i,j); returns slope deg, aspect deg (downhill compass), gradient."""
    z = Zarr[i - 1:i + 2, j - 1:j + 2]
    gx = ((z[0, 2] + 2 * z[1, 2] + z[2, 2]) - (z[0, 0] + 2 * z[1, 0] + z[2, 0])) / (8 * DX)   # east
    gy = ((z[0, 0] + 2 * z[0, 1] + z[0, 2]) - (z[2, 0] + 2 * z[2, 1] + z[2, 2])) / (8 * DY)   # north (row 0 is north)
    return math.degrees(math.atan(math.hypot(gx, gy))), math.degrees(math.atan2(-gx, -gy)) % 360, (gx, gy)

def plane_fit(Zarr, x0, y0, radius):
    """Least-squares plane through all pixel centres within `radius` of (x0,y0). Returns slope, aspect, n, rms."""
    m = (XX - x0) ** 2 + (YY - y0) ** 2 <= radius ** 2
    n = int(m.sum())
    if n < 4:
        return float("nan"), float("nan"), n, float("nan")
    A = np.column_stack([np.ones(n), XX[m] - x0, YY[m] - y0])
    coef, *_ = np.linalg.lstsq(A, Zarr[m], rcond=None)
    resid = Zarr[m] - A @ coef
    b, c = coef[1], coef[2]
    return math.degrees(math.atan(math.hypot(b, c))), math.degrees(math.atan2(-b, -c)) % 360, n, float(np.sqrt(np.mean(resid ** 2)))

def nearest_ij(x, y):
    return int(round((Y[0] - y) / DY)), int(round((x - X[0]) / DX))

# ---------------------------------------------------------------- sites
C = load_coordinates()
sites = ["tent_dyatlovpass_map", "tent_TL1810_office", "tent_TL1810_field", "tent_prosecutors_2019", "tent_borzenkov_gps_2009",
         "new_monument_sculpture", "tent_semyashkin_2010_as_published", "cedar", "dyatlov", "slobodin", "kolmogorova", "den_flooring",
         "labaz", "kholat_syakhl_summit_map", "kholat_syakhl_summit_dem", "pass_memorial_osm", "helipad_1959"]
radii = [30, 50, 100, 150]
rows = []
mc_cache = {}
for sid in sites:
    r = C[sid]; x, y = to_xy(r["lat"], r["lon"]); i, j = nearest_ij(x, y)
    hs, ha, _ = horn_slope(Z, i, j)
    rec = {"id": sid, "lat": r["lat"], "lon": r["lon"], "x_m": round(x, 1), "y_m": round(y, 1),
           "z_bilinear_m": round(z_at(x, y), 1), "z_nearest_pixel_m": round(float(Z[i, j]), 1),
           "horn3x3_slope_deg": round(hs, 1), "horn3x3_aspect_deg": round(ha, 0)}
    for R in radii:
        s, a, n, rms = plane_fit(Z, x, y, R)
        rec[f"plane_r{R}_slope_deg"] = round(s, 1); rec[f"plane_r{R}_aspect_deg"] = round(a, 0) if not math.isnan(a) else ""
        rec[f"plane_r{R}_npix"] = n; rec[f"plane_r{R}_rms_m"] = round(rms, 2) if not math.isnan(rms) else ""
    # Monte Carlo: random vertical noise -> spread of slope estimates
    if sid.startswith("tent") or sid == "new_monument_sculpture":
        hs_mc, p50_mc, p100_mc = [], [], []
        for _ in range(200):
            Zn = Z + RNG.normal(0, NOISE_SIGMA, Z.shape)
            hs_mc.append(horn_slope(Zn, i, j)[0]); p50_mc.append(plane_fit(Zn, x, y, 50)[0]); p100_mc.append(plane_fit(Zn, x, y, 100)[0])
        rec["mc_sd_horn_deg"] = round(float(np.std(hs_mc)), 2); rec["mc_sd_plane_r50_deg"] = round(float(np.std(p50_mc)), 2)
        rec["mc_sd_plane_r100_deg"] = round(float(np.std(p100_mc)), 2)
    rows.append(rec)
keys = list(rows[0].keys())
for r in rows:
    for k in keys:
        r.setdefault(k, "")
with open(os.path.join(OUT, "slopes_at_sites.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

# ---------------------------------------------------------------- profile tent -> cedar
tent = C["tent_dyatlovpass_map"]; cedar = C["cedar"]
tx, ty = to_xy(tent["lat"], tent["lon"]); cx, cy = to_xy(cedar["lat"], cedar["lon"])
L = math.hypot(cx - tx, cy - ty)
ux, uy = (cx - tx) / L, (cy - ty) / L
brg = bearing(tent["lat"], tent["lon"], cedar["lat"], cedar["lon"])
def profile(x0, y0, ux, uy, smax, step=25.0):
    out = []
    s_arr = np.arange(0, smax + 1e-6, step)
    for s in s_arr:
        x, y = x0 + ux * s, y0 + uy * s
        z = z_at(x, y)
        zp, zm = z_at(x0 + ux * (s + 12.5), y0 + uy * (s + 12.5)), z_at(x0 + ux * (s - 12.5), y0 + uy * (s - 12.5))
        z50p, z50m = z_at(x0 + ux * (s + 25), y0 + uy * (s + 25)), z_at(x0 + ux * (s - 25), y0 + uy * (s - 25))
        z100p, z100m = z_at(x0 + ux * (s + 50), y0 + uy * (s + 50)), z_at(x0 + ux * (s - 50), y0 + uy * (s - 50))
        lat, lon = from_xy(x, y)
        out.append({"dist_m": round(s, 1), "lat": round(lat, 6), "lon": round(lon, 6), "elev_m": round(z, 1),
                    "grad25_deg": round(math.degrees(math.atan((zm - zp) / 25)), 1),
                    "grad50_deg": round(math.degrees(math.atan((z50m - z50p) / 50)), 1),
                    "grad100_deg": round(math.degrees(math.atan((z100m - z100p) / 100)), 1)})
    return out
prof = profile(tx, ty, ux, uy, L)
# elevation drop of each 25 m segment ("local gradient of the segment", positive = descending toward the cedar)
for k in range(len(prof)):
    if k + 1 < len(prof):
        dz = prof[k]["elev_m"] - prof[k + 1]["elev_m"]
        prof[k]["segment_grad_deg"] = round(math.degrees(math.atan(dz / 25)), 1)
    else:
        prof[k]["segment_grad_deg"] = ""
# body positions projected on the line
for sid in ["kolmogorova", "slobodin", "dyatlov", "den_flooring"]:
    px, py = to_xy(C[sid]["lat"], C[sid]["lon"])
    C[sid]["along_m"] = (px - tx) * ux + (py - ty) * uy
    C[sid]["offset_m"] = -(px - tx) * uy + (py - ty) * ux
with open(os.path.join(OUT, "profile_tent_cedar.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(prof[0].keys())); w.writeheader(); w.writerows(prof)

# ---------------------------------------------------------------- upslope profiles (two definitions of "directly upslope")
asp100 = rows[0]["plane_r100_aspect_deg"]  # downhill compass direction of the 200-m plane at TL 18.10
up_dir = (asp100 + 180) % 360
def unit_from_bearing(b):
    return math.sin(math.radians(b)), math.cos(math.radians(b))
sx, sy = to_xy(C["kholat_syakhl_summit_dem"]["lat"], C["kholat_syakhl_summit_dem"]["lon"])
Ls = math.hypot(sx - tx, sy - ty); brg_summit = bearing(tent["lat"], tent["lon"], C["kholat_syakhl_summit_dem"]["lat"], C["kholat_syakhl_summit_dem"]["lon"])
ups = {}
for name, b in [("fall_line_up", up_dir), ("toward_summit", brg_summit)]:
    uxu, uyu = unit_from_bearing(b)
    ups[name] = {"bearing_deg": round(b, 1), "profile": profile(tx, ty, uxu, uyu, 300)}
with open(os.path.join(OUT, "profile_upslope.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["direction", "bearing_deg", "dist_up_m", "lat", "lon", "elev_m", "grad25_deg", "grad50_deg", "grad100_deg"])
    for name, d in ups.items():
        for p in d["profile"]:
            w.writerow([name, d["bearing_deg"], p["dist_m"], p["lat"], p["lon"], p["elev_m"], -p["grad25_deg"], -p["grad50_deg"], -p["grad100_deg"]])
# NB: in the upslope csv the gradient sign is flipped so that positive = rising away from the tent.

# ---------------------------------------------------------------- summary numbers
def seg_slope(p, s0, s1):
    z0 = next(q["elev_m"] for q in p if abs(q["dist_m"] - s0) < 1e-6); z1 = next(q["elev_m"] for q in p if abs(q["dist_m"] - s1) < 1e-6)
    return math.degrees(math.atan((z1 - z0) / (s1 - s0)))
summary = {
    "dem": "Copernicus DEM GLO-30 (COG tile N61_00_E059_00, AWS public bucket, md5 0c15753d8bd0c99d05fafaa78e819443)",
    "dem_grid_m": {"dx_east": round(DX, 2), "dy_north": round(DY, 2)},
    "tent_used": "tent_dyatlovpass_map (TL 18.10)",
    "tent_elev_m": rows[0]["z_bilinear_m"], "cedar_elev_m": round(z_at(cx, cy), 1),
    "tent_to_cedar_horizontal_m": round(L, 1), "tent_to_cedar_haversine_m": round(haversine(tent["lat"], tent["lon"], cedar["lat"], cedar["lon"]), 1),
    "tent_to_cedar_bearing_deg": round(brg, 1),
    "tent_to_cedar_drop_m": round(rows[0]["z_bilinear_m"] - z_at(cx, cy), 1),
    "tent_to_cedar_mean_slope_deg": round(math.degrees(math.atan((rows[0]["z_bilinear_m"] - z_at(cx, cy)) / L)), 1),
    "profile_max_grad25_deg": max(p["grad25_deg"] for p in prof), "profile_max_grad100_deg": max(p["grad100_deg"] for p in prof),
    "profile_first_500m_mean_slope_deg": round(seg_slope(prof, 0, 500), 1),
    "profile_500_1000m_mean_slope_deg": round(seg_slope(prof, 500, 1000), 1),
    "profile_1000m_to_cedar_mean_slope_deg": round(math.degrees(math.atan((next(q["elev_m"] for q in prof if abs(q["dist_m"] - 1000) < 1e-6) - z_at(cx, cy)) / (L - 1000))), 1),
    "bodies_along_line_m": {sid: {"along_m": round(C[sid]["along_m"], 1), "offset_m": round(C[sid]["offset_m"], 1), "from_cedar_m": round(L - C[sid]["along_m"], 1),
                                   "elev_m": round(z_at(*to_xy(C[sid]["lat"], C[sid]["lon"])), 1)} for sid in ["kolmogorova", "slobodin", "dyatlov", "den_flooring"]},
    "tent_to_summit_dem_m": round(Ls, 1), "tent_to_summit_bearing_deg": round(brg_summit, 1),
    "upslope": {name: {"bearing_deg": d["bearing_deg"],
                       "rise_0_100m_deg": round(-seg_slope(d["profile"], 0, 100), 1), "rise_100_200m_deg": round(-seg_slope(d["profile"], 100, 200), 1),
                       "rise_0_200m_deg": round(-seg_slope(d["profile"], 0, 200), 1), "rise_200_300m_deg": round(-seg_slope(d["profile"], 200, 300), 1),
                       "max_grad25_within_200m_deg": round(max(-p["grad25_deg"] for p in d["profile"] if p["dist_m"] <= 200), 1),
                       "max_grad50_within_200m_deg": round(max(-p["grad50_deg"] for p in d["profile"] if p["dist_m"] <= 200), 1),
                       "elev_at_200m": next(p["elev_m"] for p in d["profile"] if abs(p["dist_m"] - 200) < 1e-6)} for name, d in ups.items()},
    "noise_sigma_m": NOISE_SIGMA,
}
# steepest 100-m plane anywhere within 300 m above the tent (along the fall line band)
best = (0, None)
for i in range(1, Z.shape[0] - 1):
    for j in range(1, Z.shape[1] - 1):
        x, y = X[j], Y[i]
        d = math.hypot(x - tx, y - ty)
        if d <= 300 and (x - tx) * math.sin(math.radians(up_dir)) + (y - ty) * math.cos(math.radians(up_dir)) > 0:
            s = horn_slope(Z, i, j)[0]
            if s > best[0]:
                best = (s, (round(x, 0), round(y, 0), round(float(Z[i, j]), 1)))
summary["max_horn_slope_within_300m_above_tent"] = {"slope_deg": round(best[0], 1), "x_y_z": best[1]}
# also the max Horn slope anywhere in the 0-1.5 km descent corridor (100 m either side of the line)
corr = []
for i in range(1, Z.shape[0] - 1):
    for j in range(1, Z.shape[1] - 1):
        x, y = X[j], Y[i]
        along = (x - tx) * ux + (y - ty) * uy; off = -(x - tx) * uy + (y - ty) * ux
        if 0 <= along <= L and abs(off) <= 100:
            corr.append((horn_slope(Z, i, j)[0], along))
corr.sort(reverse=True)
summary["descent_corridor_horn_slope"] = {"max_deg": round(corr[0][0], 1), "at_along_m": round(corr[0][1], 0), "n_pixels": len(corr),
                                          "mean_deg": round(float(np.mean([c[0] for c in corr])), 1)}
with open(os.path.join(OUT, "dem_summary.json"), "w") as f:
    json.dump(summary, f, indent=1)

# ---------------------------------------------------------------- terrarium cross-check (Mapzen/AWS terrain tiles z=14)
try:
    from PIL import Image
    def tile_xy(lat, lon, z=14):
        n = 2 ** z; xt = (lon + 180) / 360 * n
        yt = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
        return xt, yt
    tiles = {}
    for xt in (10895, 10896, 10897):
        for yt in (4592, 4593, 4594):
            im = np.array(Image.open(os.path.join(RAW, "terrarium", f"14_{xt}_{yt}.png")).convert("RGB")).astype(float)
            tiles[(xt, yt)] = im[..., 0] * 256 + im[..., 1] + im[..., 2] / 256 - 32768
    def terr_z(lat, lon):
        xt, yt = tile_xy(lat, lon); tx_, ty_ = int(xt), int(yt)
        arr = tiles.get((tx_, ty_))
        if arr is None: return float("nan")
        return float(arr[min(255, int((yt - ty_) * 256)), min(255, int((xt - tx_) * 256))])
    diffs = []
    for p in prof:
        zt = terr_z(p["lat"], p["lon"])
        if not math.isnan(zt): diffs.append(zt - p["elev_m"])
    tz_tent = terr_z(tent["lat"], tent["lon"])
    # terrarium slope over +-30 m along the fall line
    uxu, uyu = unit_from_bearing(up_dir)
    la1, lo1 = from_xy(tx + uxu * 30, ty + uyu * 30); la2, lo2 = from_xy(tx - uxu * 30, ty - uyu * 30)
    terr_slope = math.degrees(math.atan((terr_z(la1, lo1) - terr_z(la2, lo2)) / 60))
    summary["terrarium_crosscheck"] = {"tent_elev_m": round(tz_tent, 1), "profile_mean_diff_terr_minus_cop_m": round(float(np.mean(diffs)), 1),
                                       "profile_rms_diff_m": round(float(np.sqrt(np.mean(np.square(diffs)))), 1), "n": len(diffs),
                                       "fall_line_slope_over_60m_deg": round(terr_slope, 1)}
    with open(os.path.join(OUT, "dem_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
except Exception as e:
    summary["terrarium_crosscheck"] = f"failed: {e}"

# ---------------------------------------------------------------- figures
ls = LightSource(azdeg=315, altdeg=35)
fig, ax = plt.subplots(figsize=(11, 8.5))
xmin, xmax, ymin, ymax = -1000, 2000, -900, 1000
mx = (X >= xmin) & (X <= xmax); my = (Y >= ymin) & (Y <= ymax)
Zc = Z[np.ix_(my, mx)]; Xc = X[mx]; Yc = Y[my]
rgb = ls.shade(Zc, cmap=plt.cm.gist_earth, vert_exag=1.5, dx=DX, dy=DY, blend_mode="overlay", vmin=550, vmax=1150)
ax.imshow(rgb, extent=[Xc[0] - DX / 2, Xc[-1] + DX / 2, Yc[-1] - DY / 2, Yc[0] + DY / 2], origin="upper", interpolation="nearest")
cs = ax.contour(Xc, Yc, Zc, levels=np.arange(540, 1160, 20), colors="k", linewidths=0.35, alpha=0.7)
ax.clabel(cs, levels=np.arange(600, 1160, 100), fmt="%d", fontsize=7)
ax.plot([tx, cx], [ty, cy], "-", color="crimson", lw=1.5, label="tent -> cedar line (profile)")
uxu, uyu = unit_from_bearing(up_dir)
ax.plot([tx, tx + uxu * 300], [ty, ty + uyu * 300], "--", color="orange", lw=1.5, label="fall line 300 m upslope")
pts = [("tent_dyatlovpass_map", "Tent TL 18.10", "^", "red"), ("tent_prosecutors_2019", "Tent (prosecutors 2019)", "^", "magenta"),
       ("new_monument_sculpture", "sculpture", "s", "grey"), ("cedar", "Cedar", "*", "green"), ("den_flooring", "Den / ravine bodies", "P", "blue"),
       ("dyatlov", "Dyatlov", "o", "k"), ("slobodin", "Slobodin", "o", "k"), ("kolmogorova", "Kolmogorova", "o", "k"),
       ("labaz", "Labaz", "D", "brown"), ("kholat_syakhl_summit_dem", "Kholat Syakhl summit (DEM max 1096 m)", "^", "white"),
       ("pass_memorial_osm", "Pass memorial (OSM)", "X", "purple"), ("helipad_1959", "1959 helipad", "h", "cyan")]
for sid, lab, mk, col in pts:
    x, y = to_xy(C[sid]["lat"], C[sid]["lon"])
    ax.plot(x, y, marker=mk, color=col, markeredgecolor="k", ms=9 if mk != "o" else 6, ls="none", label=lab)
    if sid in ("dyatlov", "slobodin", "kolmogorova"):
        ax.annotate(lab[0], (x, y), textcoords="offset points", xytext=(4, 4), fontsize=8)
ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_aspect("equal")
ax.set_xlabel("metres east of tent TL 18.10"); ax.set_ylabel("metres north of tent TL 18.10")
ax.set_title("Kholat Syakhl east slope - Copernicus GLO-30 hillshade, 20 m contours (61.75-61.77 N, 59.41-59.47 E)")
ax.legend(loc="lower right", fontsize=7, ncol=2)
sec = ax.secondary_xaxis("top", functions=(lambda x: REF_LON + x / MLON, lambda lo: (lo - REF_LON) * MLON)); sec.set_xlabel("longitude (deg E)")
sec2 = ax.secondary_yaxis("right", functions=(lambda y: REF_LAT + y / MLAT, lambda la: (la - REF_LAT) * MLAT)); sec2.set_ylabel("latitude (deg N)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "map_dem.png"), dpi=150); plt.close(fig)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
d = [p["dist_m"] for p in prof]; e = [p["elev_m"] for p in prof]
a1.plot(d, e, "-", color="k", lw=1.5, label="Copernicus GLO-30 (bilinear)")
for sid, lab in [("kolmogorova", "Kolmogorova"), ("slobodin", "Slobodin"), ("dyatlov", "Dyatlov"), ("den_flooring", "den/ravine")]:
    a = C[sid]["along_m"]; a1.axvline(a, color="grey", ls=":", lw=1); a1.text(a, max(e) - 20, lab, rotation=90, va="top", ha="right", fontsize=8)
a1.axvline(0, color="red", lw=1); a1.text(5, max(e) - 5, "tent", color="red", fontsize=9)
a1.axvline(L, color="green", lw=1); a1.text(L - 5, min(e) + 5, "cedar", color="green", fontsize=9, ha="right")
a1.set_ylabel("elevation (m, EGM2008)"); a1.grid(alpha=0.3); a1.legend(loc="upper right", fontsize=8)
a1.set_title(f"Profile tent (TL 18.10) -> cedar: {L:.0f} m, drop {summary['tent_to_cedar_drop_m']:.0f} m, mean slope {summary['tent_to_cedar_mean_slope_deg']:.1f} deg, bearing {brg:.0f} deg")
a2.plot(d, [p["grad25_deg"] for p in prof], "-", color="tab:blue", lw=0.9, label="gradient over 25 m")
a2.plot(d, [p["grad100_deg"] for p in prof], "-", color="tab:red", lw=1.5, label="gradient over 100 m")
a2.axhline(28, color="orange", ls="--", lw=1, label="28 deg (Gaume-Puzrin weak-layer angle)")
a2.axhline(23, color="grey", ls="--", lw=1, label="23 deg (often quoted mean)")
a2.set_ylabel("slope (deg, + = descending)"); a2.set_xlabel("distance from tent along line (m)"); a2.grid(alpha=0.3); a2.legend(fontsize=8, loc="upper right")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "profile_tent_cedar.png"), dpi=150); plt.close(fig)

# ---------------------------------------------------------------- markdown printout
md = ["# DEM slope summary (generated by dem_slope.py)", "", f"DEM: {summary['dem']}; grid {DX:.1f} m (E) x {DY:.1f} m (N).", "",
      "## Slope/aspect at candidate sites", "", "| site | z (m) | Horn 3x3 slope / aspect | plane r=30 m (n) | plane r=50 m (n) | plane r=100 m (n) | plane r=150 m (n) | MC sd (Horn / r50 / r100) |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['id']} | {r['z_bilinear_m']} | {r['horn3x3_slope_deg']} deg / {r['horn3x3_aspect_deg']:.0f} | {r['plane_r30_slope_deg']} ({r['plane_r30_npix']}) | {r['plane_r50_slope_deg']} deg/{r['plane_r50_aspect_deg']} ({r['plane_r50_npix']}) | {r['plane_r100_slope_deg']} deg/{r['plane_r100_aspect_deg']} ({r['plane_r100_npix']}) | {r['plane_r150_slope_deg']} deg/{r['plane_r150_aspect_deg']} ({r['plane_r150_npix']}) | {r.get('mc_sd_horn_deg','')} / {r.get('mc_sd_plane_r50_deg','')} / {r.get('mc_sd_plane_r100_deg','')} |")
md += ["", "## Summary", "", "```", json.dumps(summary, indent=1), "```", "", "## Upslope profiles (positive = rising away from the tent)", ""]
for name, dct in ups.items():
    md += [f"### {name} (bearing {dct['bearing_deg']} deg)", "", "| up (m) | elev (m) | grad25 | grad50 | grad100 |", "|---|---|---|---|---|"]
    for p in dct["profile"]:
        md.append(f"| {p['dist_m']:.0f} | {p['elev_m']} | {-p['grad25_deg']:.1f} | {-p['grad50_deg']:.1f} | {-p['grad100_deg']:.1f} |")
    md.append("")
md += ["## Profile tent -> cedar (every 25 m)", "", "| dist (m) | elev (m) | grad25 | grad50 | grad100 | segment |", "|---|---|---|---|---|---|"]
for p in prof:
    md.append(f"| {p['dist_m']:.0f} | {p['elev_m']} | {p['grad25_deg']} | {p['grad50_deg']} | {p['grad100_deg']} | {p['segment_grad_deg']} |")
open(os.path.join(OUT, "dem_summary.md"), "w").write("\n".join(md))
print("\n".join(md[:40]))
print(json.dumps(summary, indent=1))
