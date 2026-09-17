#!/usr/bin/env python3
"""Download Copernicus DEM GLO-90 tiles for the western Alps (Hannibal 218 BC study).

Source: the public AWS Open Data bucket of the Copernicus DEM GLO-90
(https://copernicus-dem-90m.s3.amazonaws.com/ ; ESA / Airbus, free licence,
see INFO/eula_F.pdf inside each tile prefix).  Each 1x1 degree tile is a
Cloud-Optimised GeoTIFF of 1200 rows x (1200 or fewer) columns, 3 arc-second
(~90 m) posting, WGS84 ellipsoidal lat/lon, heights in metres above EGM2008.
It is a *surface* model (DSM: tree canopy and buildings are included).

Coverage requested: N43..N45 x E004..E008 (15 tiles) plus N46 E004-E008 (5 tiles for R7 and the map) = lower Rhone at
Fourques/Beaucaire (43.8N 4.6E) to Lyon (45.8N), Turin (45.07N 7.68E) and the
Po plain to 8E.

Usage:
    python3 download_dem.py [DEST_DIR]
Default DEST_DIR is $HANNIBAL_DEM_DIR or the dem/ folder in the case folder, as
used by dem.py.  The download is idempotent (existing files with the right size are
kept).  Only the standard library is used.

The bucket also serves a listing per prefix
(?list-type=2&prefix=Copernicus_DSM_COG_30_N44_00_E006_00_DEM/), which this
script uses to confirm the exact key and the expected byte size before
downloading.
"""
import os
import re
import sys
import time
import urllib.request

BUCKET = "https://copernicus-dem-90m.s3.amazonaws.com/"
LATS = [43, 44, 45]
LONS = [4, 5, 6, 7, 8]
# five extra tiles north of 46N so the Swiss stretch of route R7 (Geneva-Martigny-
# Grand-Saint-Bernard) has a profile and the overview map has no gap; not needed for R1-R6.
EXTRA = [(46, 4), (46, 5), (46, 6), (46, 7), (46, 8)]

DEFAULT_DIR = os.environ.get(
    "HANNIBAL_DEM_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dem"),
)


def tile_prefix(lat, lon):
    return "Copernicus_DSM_COG_30_N%02d_00_E%03d_00_DEM/" % (lat, lon)


def tile_key(lat, lon):
    p = tile_prefix(lat, lon)
    return p + p[:-1] + ".tif"


def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hannibal-alps-terrain/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError("failed to fetch %s: %s" % (url, last))


def expected_size(lat, lon):
    """Confirm the exact key via the S3 listing and return its byte size (or None)."""
    listing = fetch(BUCKET + "?list-type=2&prefix=" + tile_prefix(lat, lon)).decode("utf-8", "replace")
    key = tile_key(lat, lon)
    m = re.search(r"<Key>%s</Key>.*?<Size>(\d+)</Size>" % re.escape(key), listing, re.S)
    return int(m.group(1)) if m else None


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    os.makedirs(dest, exist_ok=True)
    wanted = [(lat, lon) for lat in LATS for lon in LONS] + EXTRA
    for lat, lon in wanted:
        if True:
            key = tile_key(lat, lon)
            out = os.path.join(dest, os.path.basename(key))
            size = expected_size(lat, lon)
            if size is None:
                print("MISSING on bucket:", key)
                continue
            if os.path.exists(out) and os.path.getsize(out) == size:
                print("have", os.path.basename(out), size)
                continue
            t0 = time.time()
            data = fetch(BUCKET + key)
            if len(data) != size:
                raise RuntimeError("size mismatch for %s: %d vs %d" % (key, len(data), size))
            with open(out, "wb") as f:
                f.write(data)
            print("got ", os.path.basename(out), size, "bytes in %.1fs" % (time.time() - t0))
    print("done ->", dest)


if __name__ == "__main__":
    main()
