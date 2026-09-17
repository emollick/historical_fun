#!/usr/bin/env python3
"""geo_common.py - shared helpers for the Dyatlov Pass geospatial checks.

Provides: paths, WGS84 local metric projection around a reference point,
loading of data/coordinates.csv, and geodesic distance/bearing (spherical
haversine + local-ENU cross-check; both agree to <0.1 % over the <5 km scales
used here).
"""
import csv, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# WGS84
A = 6378137.0
F = 1 / 298.257223563
E2 = 2 * F - F * F

# Reference point for the local metric grid: tent site TL 18.10 (dyatlovpass.com map placemark)
REF_LAT, REF_LON = 61.7585389, 59.4294268


def metres_per_degree(lat_deg):
    """Metres per degree of latitude (M) and longitude (N cos phi) on the WGS84 ellipsoid."""
    phi = math.radians(lat_deg)
    s2 = math.sin(phi) ** 2
    M = A * (1 - E2) / (1 - E2 * s2) ** 1.5
    N = A / math.sqrt(1 - E2 * s2)
    return M * math.pi / 180, N * math.cos(phi) * math.pi / 180


MLAT, MLON = metres_per_degree(REF_LAT)


def to_xy(lat, lon, ref_lat=REF_LAT, ref_lon=REF_LON):
    """Local east/north metres relative to the reference point (equirectangular; fine for <10 km)."""
    return (lon - ref_lon) * MLON, (lat - ref_lat) * MLAT


def from_xy(x, y, ref_lat=REF_LAT, ref_lon=REF_LON):
    return ref_lat + y / MLAT, ref_lon + x / MLON


def haversine(lat1, lon1, lat2, lon2, R=6371008.8):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def bearing(lat1, lon1, lat2, lon2):
    """Initial compass bearing (deg clockwise from true north) from point 1 to point 2."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(x, y)) % 360


def load_coordinates():
    """Return dict id -> row (lat/lon as float) from data/coordinates.csv."""
    rows = {}
    with open(os.path.join(DATA, "coordinates.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["lat"] = float(r["lat"]); r["lon"] = float(r["lon"])
            rows[r["id"]] = r
    return rows


if __name__ == "__main__":
    print(f"metres/deg at {REF_LAT:.4f}N: lat {MLAT:.1f}, lon {MLON:.1f}")
    c = load_coordinates()
    for k, r in c.items():
        x, y = to_xy(r["lat"], r["lon"])
        print(f"{k:38s} {r['lat']:.7f} {r['lon']:.7f}  x={x:8.1f} y={y:8.1f}")
