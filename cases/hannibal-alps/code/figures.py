#!/usr/bin/env python3
"""Figures for the Hannibal terrain dossier (pure Python + numpy + Pillow).

  data/map_overview.svg      hillshaded overview map (DEM), rivers, routes R1-R7,
                             candidate cols with heights (JPEG hillshade embedded)
  data/profiles.svg          elevation profiles of the main routes, common axis
                             (distance from each route's Island)
  data/viewshed_panels.png   per-col panel: plain cells (<400 m) and the ones
                             visible from the col

Run after routes.py and viewshed.py:  python3 figures.py
"""
import base64
import io
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from dem import DEM

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

STYLE = {  # colour, dash pattern, width
    "R1": ("#d62728", "", 2.2), "R2": ("#ff7f0e", "6,3", 2.2), "R2b": ("#ff7f0e", "2,3", 1.3),
    "R3": ("#2ca02c", "9,4", 2.2), "R4": ("#1f77b4", "", 2.2), "R4c": ("#1f77b4", "2,3", 1.3),
    "R5": ("#9467bd", "6,3", 2.2), "R5g": ("#9467bd", "2,3", 1.3), "R6": ("#8c564b", "9,4", 2.2), "R6v": ("#8c564b", "2,3", 1.3),
    "R7": ("#17becf", "12,4", 2.0), "R3m": ("#2ca02c", "2,3", 1.0),
}
COL_LABELS = {"Col du Mont-Cenis": "Mont-Cenis 2083", "Col Clapier": "Clapier 2482", "Col du Petit Mont-Cenis": "Petit Mont-Cenis 2183",
              "Col du Petit-Saint-Bernard": "Petit-St-Bernard 2188", "Col de Montgenevre": "Montgenevre 1854",
              "Col de la Traversette": "Traversette 2947", "Col de Larche": "Larche 1991", "Col du Grand-Saint-Bernard": "Grand-St-Bernard 2469",
              "Col Agnel": "Agnel 2744", "Col de Cabre": "Cabre 1180", "Col de Grimone": "Grimone 1318", "Col de Vars": "Vars 2108",
              "Col de la Croix (Croce)": "Croix 2298"}
COL_OFF = {"Col du Mont-Cenis": (8, -6), "Col du Petit Mont-Cenis": (-118, 16), "Col Clapier": (8, 18), "Col Agnel": (-72, 16),
           "Col de la Traversette": (8, 4), "Col du Petit-Saint-Bernard": (8, -6), "Col de Montgenevre": (-112, -4), "Col de Vars": (8, 12),
           "Col de Larche": (8, 12), "Col de Cabre": (-70, 14), "Col de Grimone": (8, -4), "Col du Grand-Saint-Bernard": (8, 4)}
TOWN_OFF = {"Bourg-Saint-Maurice": (-118, 12), "Guillestre": (-62, 12), "Briancon": (-52, -4), "Modane": (-46, 12), "Susa": (-30, 12),
            "Saint-Jean-de-Maurienne": (-130, -4), "Moutiers": (4, 12), "Embrun": (-44, 12), "Gap": (-24, -4)}
TOWNS = ["Beaucaire", "Avignon", "Orange", "Montelimar", "Valence", "Lyon", "Grenoble", "Montmelian", "Albertville", "Moutiers",
         "Bourg-Saint-Maurice", "Saint-Jean-de-Maurienne", "Modane", "Susa", "Turin", "Aosta", "Ivrea", "Sisteron", "Gap", "Embrun",
         "Guillestre", "Briancon", "Barcelonnette", "Cuneo", "Saluzzo", "Die", "Geneva", "Martigny", "Crest", "Vercelli"]


def simplify_xy(pts, tol):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[j]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        best, bi = -1, -1
        for k in range(i + 1, j):
            x, y = pts[k]
            if L2 == 0:
                dd = math.hypot(x - x1, y - y1)
            else:
                t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / L2))
                dd = math.hypot(x - x1 - t * dx, y - y1 - t * dy)
            if dd > best:
                best, bi = dd, k
        if best > tol:
            keep[bi] = True
            stack += [(i, bi), (bi, j)]
    return [p for p, k in zip(pts, keep) if k]


def hillshade(Z, dx, dy, az=315.0, alt=45.0):
    Zf = np.where(np.isnan(Z), np.nanmin(Z), Z)
    gy, gx = np.gradient(Zf, dy, dx)
    slope = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    azr, altr = math.radians(az), math.radians(alt)
    hs = np.sin(altr) * np.cos(slope) + np.cos(altr) * np.sin(slope) * np.cos(azr - aspect)
    return np.clip(hs, 0, 1)


def hypso(Z):
    """soft hypsometric tint (RGB 0-255) for the map background."""
    z = np.where(np.isnan(Z), 0, Z)
    stops = [(0, (208, 224, 190)), (300, (222, 232, 184)), (800, (226, 214, 170)), (1500, (214, 196, 160)),
             (2300, (200, 190, 178)), (3000, (232, 232, 236)), (4800, (255, 255, 255))]
    out = np.zeros(Z.shape + (3,), dtype=np.float32)
    for k in range(len(stops) - 1):
        z0, c0 = stops[k]
        z1, c1 = stops[k + 1]
        m = (z >= z0) & (z < z1)
        t = ((z - z0) / (z1 - z0))[m][:, None]
        out[m] = np.array(c0) * (1 - t) + np.array(c1) * t
    out[z >= stops[-1][0]] = stops[-1][1]
    return out


def overview_map(dem, routes, rivers, places):
    lat_s, lat_n, lon_w, lon_e = 43.55, 46.45, 4.35, 8.35
    Z, lats, lons = dem.window(lat_s, lat_n, lon_w, lon_e)
    f = 5
    Zs = Z[::f, ::f]
    dy = dem.dlat * f * 111132.0
    dx = dem.dlon * f * 111320.0 * math.cos(math.radians(45.0))
    hs = hillshade(Zs, dx, dy)
    rgb = hypso(Zs) * (0.55 + 0.45 * hs[..., None])
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    rgb[np.isnan(Zs)] = (235, 240, 245)
    img = Image.fromarray(rgb, "RGB")
    H, W = Zs.shape
    # projection: image pixel = (lon, lat) linear
    lat_top, lon_left = float(lats[0]), float(lons[0])
    dlat_px = dem.dlat * f
    dlon_px = dem.dlon * f

    def xy(lat, lon):
        return ((lon - lon_left) / dlon_px, (lat_top - lat) / dlat_px)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=68, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DejaVu Sans, Arial, sans-serif">' % (W, H + 190, W, H + 190),
           '<image href="data:image/jpeg;base64,%s" x="0" y="0" width="%d" height="%d"/>' % (b64, W, H)]
    # rivers
    for name, r in rivers.items():
        for line in r["lines"]:
            pts = [xy(p[0], p[1]) for p in line if lat_s <= p[0] <= lat_n and lon_w <= p[1] <= lon_e]
            if len(pts) < 2:
                continue
            pts = simplify_xy(pts, 0.8)
            svg.append('<polyline fill="none" stroke="#3b7dd8" stroke-width="1.1" stroke-opacity="0.85" points="%s"/>' % " ".join("%.1f,%.1f" % p for p in pts))
    # rhone legs (thin grey)
    for name, leg in routes["rhone_legs"].items():
        pts = simplify_xy([xy(p[0], p[1]) for p in leg["path"]], 1.0)
        svg.append('<polyline fill="none" stroke="#333" stroke-width="1.2" stroke-dasharray="3,3" points="%s"/>' % " ".join("%.1f,%.1f" % p for p in pts))
    # routes
    order = ["R3m", "R2b", "R4c", "R5g", "R6v", "R7", "R6", "R5", "R4", "R3", "R2", "R1"]
    for rid in order:
        if rid not in routes["routes"]:
            continue
        col, dash, w = STYLE[rid]
        pts = simplify_xy([xy(p[0], p[1]) for p in routes["routes"][rid]["path"]], 1.0)
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        svg.append('<polyline fill="none" stroke="#ffffff" stroke-width="%.1f" stroke-opacity="0.6" points="%s"/>' % (w + 2.0, " ".join("%.1f,%.1f" % p for p in pts)))
        svg.append('<polyline fill="none" stroke="%s" stroke-width="%.1f"%s points="%s"/>' % (col, w, d, " ".join("%.1f,%.1f" % p for p in pts)))
    # towns
    for t in TOWNS:
        if t not in places:
            continue
        x, y = xy(places[t]["lat"], places[t]["lon"])
        if not (0 <= x <= W and 0 <= y <= H):
            continue
        svg.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#111"/>' % (x, y))
        ox, oy = TOWN_OFF.get(t, (4, -3))
        svg.append('<text x="%.1f" y="%.1f" font-size="10" fill="#111" stroke="#fff" stroke-width="2.5" paint-order="stroke">%s</text>' % (x + ox, y + oy, t.replace("Montelimar", "Montélimar").replace("Briancon", "Briançon").replace("Moutiers", "Moûtiers")))
    # cols
    for key, lab in COL_LABELS.items():
        if key not in places:
            continue
        x, y = xy(places[key]["lat"], places[key]["lon"])
        svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#000" stroke="#fff" stroke-width="1"/>' % (x, y - 6, x - 5, y + 4, x + 5, y + 4))
        ox, oy = COL_OFF.get(key, (7, 4))
        svg.append('<text x="%.1f" y="%.1f" font-size="11" font-weight="bold" fill="#000" stroke="#fff" stroke-width="3" paint-order="stroke">%s</text>' % (x + ox, y + oy, lab))
    # scale bar (100 km at 45N)
    km100 = 100.0 / (111.32 * math.cos(math.radians(45.0))) / dlon_px
    svg.append('<rect x="20" y="%d" width="%.1f" height="6" fill="#000"/><text x="20" y="%d" font-size="11">100 km</text>' % (H - 30, km100, H - 34))
    # legend
    y0 = H + 18
    svg.append('<rect x="0" y="%d" width="%d" height="190" fill="#fff"/>' % (H, W))
    svg.append('<text x="12" y="%d" font-size="13" font-weight="bold">Candidate routes of Hannibal, 218 BC. Hillshade: Copernicus GLO-90; routes: least-cost valley-floor paths between named waypoints</text>' % (y0))
    names = {"R1": "R1 Isère–Arc–Mont-Cenis", "R2": "R2 Isère–Arc–Clapier (Savine/Clarea)", "R2b": "R2b Petit Mont-Cenis variant",
             "R3": "R3 Isère–Tarentaise–Petit-St-Bernard", "R4": "R4 Durance–Montgenèvre", "R4c": "R4c Drôme–Cabre–Durance–Montgenèvre",
             "R5": "R5 Durance–Guil–Traversette", "R5g": "R5g Drôme–Grimone–Guil–Traversette (de Beer)", "R6": "R6 Durance–Ubaye–Larche",
             "R6v": "R6v via Col de Vars", "R7": "R7 Lyon–Geneva–Grand-St-Bernard", "R3m": "R3m to Vercelli/Milan"}
    x = 12
    y = y0 + 22
    for i, rid in enumerate(["R1", "R2", "R2b", "R3", "R3m", "R4", "R4c", "R5", "R5g", "R6", "R6v", "R7"]):
        col, dash, w = STYLE[rid]
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        cx = x + (i % 2) * 540
        cy = y + (i // 2) * 21
        svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%.1f"%s/>' % (cx, cy - 4, cx + 40, cy - 4, col, w, d))
        svg.append('<text x="%d" y="%d" font-size="11">%s</text>' % (cx + 48, cy, names[rid]))
    svg.append('<text x="12" y="%d" font-size="10" fill="#444">Blue lines: OSM river centrelines (Nominatim). Black dotted: Rhône legs from the crossings (Fourques/Beaucaire/Roquemaure) to the two "Island" options. Triangles: cols with map heights (m).</text>' % (y0 + 21 * 6 + 14))
    svg.append("</svg>")
    with open(os.path.join(DATA, "map_overview.svg"), "w") as f:
        f.write("\n".join(svg))


def profiles_svg(routes, profiles, out_name="profiles.svg", legend_below=False):
    main = ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]
    W, H = 1150, 620
    ml, mr, mt, mb = 60, 20, 40, 60
    if legend_below:
        mb = 60 + 9 * 17  # room under the axis for a one-column legend
        H = H + 9 * 17
    xmax = 420.0
    zmax = 3200.0
    pw, ph = W - ml - mr, H - mt - mb

    def X(km):
        return ml + km / xmax * pw

    def Y(z):
        return mt + (1 - z / zmax) * ph

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DejaVu Sans, Arial, sans-serif" font-size="11">' % (W, H, W, H),
           '<rect width="%d" height="%d" fill="#fff"/>' % (W, H)]
    for z in range(0, 3201, 500):
        svg.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ddd"/>' % (ml, Y(z), W - mr, Y(z)))
        svg.append('<text x="%d" y="%.1f" text-anchor="end">%d</text>' % (ml - 6, Y(z) + 4, z))
    for km in range(0, 421, 50):
        svg.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#ddd"/>' % (X(km), mt, X(km), H - mb))
        svg.append('<text x="%.1f" y="%d" text-anchor="middle">%d</text>' % (X(km), H - mb + 16, km))
    for sname, sm, col in [("800 stades", 800 * 0.1776, "#999"), ("800 stades (185 m)", 800 * 0.185, "#bbb")]:
        svg.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-dasharray="4,4"/>' % (X(sm), mt, X(sm), H - mb, col))
        svg.append('<text x="%.1f" y="%d" font-size="10" fill="#666" transform="rotate(-90 %.1f %d)">%s from the Island</text>' % (X(sm) - 3, mt + 200, X(sm) - 3, mt + 200, sname))
    svg.append('<text x="%d" y="%d" text-anchor="middle" font-size="12">distance from the Island along the valley-floor path (km)   — R1–R3, R7 from the Isère–Rhône confluence; R4–R6 from the Aygues–Rhône confluence</text>' % (ml + pw / 2, (H - mb + 34) if legend_below else (H - 12)))
    svg.append('<text x="14" y="%d" transform="rotate(-90 14 %d)" text-anchor="middle" font-size="12">elevation (m, Copernicus GLO-90)</text>' % (mt + ph / 2, mt + ph / 2))
    svg.append('<text x="%d" y="22" font-size="14" font-weight="bold">Elevation profiles of the candidate routes (sampled every 250 m; col = triangle; gate = circle; plain (&lt;400 m) = square)</text>' % ml)
    for k, rid in enumerate(main):
        p = profiles[rid]
        colr, dash, w = STYLE[rid]
        d = p["dist_km"]
        z = p["z"]
        pts = [(X(d[i]), Y(z[i])) for i in range(0, len(d), 2) if z[i] is not None and d[i] <= xmax]
        pts = simplify_xy(pts, 0.6)
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        svg.append('<polyline fill="none" stroke="%s" stroke-width="1.6"%s points="%s"/>' % (colr, da, " ".join("%.1f,%.1f" % q for q in pts)))
        ic, ig, ip = p["i_col"], p["i_gate"], p["i_plain"]
        for idx, shape in [(ic, "tri"), (ig, "circ"), (ip, "sq")]:
            if idx is None or z[idx] is None or d[idx] > xmax:
                continue
            x, y = X(d[idx]), Y(z[idx])
            if shape == "tri":
                svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="#000" stroke-width="0.7"/>' % (x, y - 7, x - 5, y + 3, x + 5, y + 3, colr))
            elif shape == "circ":
                svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="#000" stroke-width="0.7"/>' % (x, y, colr))
            else:
                svg.append('<rect x="%.1f" y="%.1f" width="7" height="7" fill="%s" stroke="#000" stroke-width="0.7"/>' % (x - 3.5, y - 3.5, colr))
        # legend
        name = routes["routes"][rid]["name"]
        lx, ly = ml + 10, mt + 14 + k * 16
        if legend_below:
            lx, ly = ml + 10, H - mb + 62 + k * 17
        svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"%s/>' % (lx, ly - 4, lx + 30, ly - 4, colr, da))
        svg.append('<text x="%d" y="%d">%s: %s (col %.0f m, Island→col %.0f km)</text>' % (lx + 36, ly, rid, name[:70], routes["routes"][rid]["col_z_dem"], routes["routes"][rid]["km_island_to_col"]))
    svg.append("</svg>")
    with open(os.path.join(DATA, out_name), "w") as f:
        f.write("\n".join(svg))


def viewshed_panels(dem, places):
    fn = os.path.join(DATA, "viewshed_cells.json")
    if not os.path.exists(fn):
        print("no viewshed_cells.json yet; skipping panels")
        return
    with open(fn) as f:
        cells = json.load(f)
    with open(os.path.join(DATA, "viewshed_output.json")) as f:
        vo = json.load(f)
    keys = list(cells.keys())
    n = len(keys)
    ncol = 5
    nrow = int(math.ceil(n / ncol))
    pw, ph = 300, 300
    W, H = ncol * pw, nrow * (ph + 34) + 30
    im = Image.new("RGB", (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 11)
    fontb = ImageFont.truetype(FONT_B, 12)
    for k, key in enumerate(keys):
        rec = vo["cols"][key]
        lat0, lon0 = rec["used"]["lat"], rec["used"]["lon"]
        lat_s, lat_n = lat0 - 0.85, lat0 + 0.85
        lon_w, lon_e = lon0 - 0.45, lon0 + 1.85
        Z, lats, lons = dem.window(lat_s, lat_n, lon_w, lon_e)
        f = max(1, int(round(Z.shape[1] / pw)))
        Zs = Z[::f, ::f]
        h, w = Zs.shape
        # background: elevation bands
        z = np.where(np.isnan(Zs), 0, Zs)
        rgb = np.zeros((h, w, 3), dtype=np.uint8)
        rgb[:] = (235, 235, 235)
        rgb[z < 1500] = (205, 205, 205)
        rgb[z < 800] = (225, 225, 225)
        rgb[z < 400] = (255, 245, 200)
        rgb[np.isnan(Zs)] = (240, 240, 250)
        panel = Image.fromarray(rgb, "RGB").resize((pw, ph))
        pd = ImageDraw.Draw(panel)

        def xy(la, lo):
            return ((lo - lon_w) / (lon_e - lon_w) * pw, (lat_n - la) / (lat_n - lat_s) * ph)

        for c in cells[key]:
            x, y = xy(c[0], c[1])
            pd.rectangle([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(200, 30, 30))
        # plain boundary lines
        x73, _ = xy(lat0, 7.3)
        pd.line([(x73, 0), (x73, ph)], fill=(150, 150, 255), width=1)
        _, y444 = xy(44.4, lon0)
        if 0 <= y444 <= ph:
            pd.line([(0, y444), (pw, y444)], fill=(150, 150, 255), width=1)
        x, y = xy(lat0, lon0)
        pd.polygon([(x, y - 6), (x - 5, y + 4), (x + 5, y + 4)], fill=(0, 0, 0))
        for t in ["Turin", "Susa", "Saluzzo", "Cuneo", "Ivrea", "Aosta", "Pinerolo", "Vercelli"]:
            if t in places:
                tx, ty = xy(places[t]["lat"], places[t]["lon"])
                if 0 <= tx < pw and 0 <= ty < ph:
                    pd.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(0, 0, 0))
                    pd.text((tx + 3, ty - 6), t, fill=(0, 0, 0), font=font)
        pd.rectangle([0, 0, pw - 1, ph - 1], outline=(120, 120, 120))
        ox, oy = (k % ncol) * pw, 30 + (k // ncol) * (ph + 34)
        im.paste(panel, (ox, oy))
        c = rec["col"]
        k1 = rec.get("knoll_+100")
        k3 = rec.get("knoll_+300")
        fv = rec.get("first_descent_point_with_plain")
        line1 = "%s (%.0f m): plain visible from col: %s, %.0f%% of azimuths" % (key, rec["used"]["z_dem"], "YES" if c["plain_visible"] else "no", 100 * c["frac_azimuths_plain_visible"])
        line2 = "first descent pt: %s; +100 m knoll: %s; +300 m knoll: %s" % (
            ("%.2f km" % fv["km_from_col"]) if fv else "none<=10km", ("%s %.0f%%" % ("yes" if k1["plain_visible"] else "no", 100 * k1["frac_azimuths_plain_visible"])) if k1 else "-",
            ("%s %.0f%%" % ("yes" if k3["plain_visible"] else "no", 100 * k3["frac_azimuths_plain_visible"])) if k3 else "-")
        dr.text((ox + 4, oy + ph + 2), line1, fill=(0, 0, 0), font=fontb)
        dr.text((ox + 4, oy + ph + 17), line2, fill=(0, 0, 0), font=font)
    dr.text((6, 6), "Viewshed of the Po plain (yellow: DEM < 400 m; red: plain cells in line of sight from the col, 0.25° rays to 120 km, k=0.13, observer 2 m; blue lines: 7.3E / 44.4N plain mask bounds)", fill=(0, 0, 0), font=fontb)
    im = im.convert("P", palette=Image.ADAPTIVE, colors=24)
    im.save(os.path.join(DATA, "viewshed_panels.png"), optimize=True)


def main():
    dem = DEM()
    with open(os.path.join(DATA, "routes.json")) as f:
        routes = json.load(f)
    with open(os.path.join(DATA, "profiles.json")) as f:
        profiles = json.load(f)
    with open(os.path.join(DATA, "places.json")) as f:
        places = json.load(f)
    rivers = {}
    if os.path.exists(os.path.join(DATA, "rivers.json")):
        with open(os.path.join(DATA, "rivers.json")) as f:
            rivers = json.load(f)
    overview_map(dem, routes, rivers, places)
    profiles_svg(routes, profiles)
    viewshed_panels(dem, places)
    for fn in ["map_overview.svg", "profiles.svg", "viewshed_panels.png"]:
        p = os.path.join(DATA, fn)
        if os.path.exists(p):
            print(fn, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    main()
