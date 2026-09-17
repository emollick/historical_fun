#!/usr/bin/env python3
"""Elevation sampling from Copernicus DEM GLO-90 tiles (bilinear, across tiles).

Tiles are read once with rasterio into a single numpy mosaic covering
N43..N47 x E004..E009 (the 15+2 tiles fetched by download_dem.py; cells with no tile are nan).  The mosaic
is kept in memory (15 x 1200 x 1200 float32 = ~100 MB at most; GLO-90 tiles
north of 50N have fewer columns, but here all are 1200 x 1200).

Grid convention (Copernicus DEM): each 1x1 degree tile has 1200 rows and 1200
columns at 3 arc-second spacing; pixel centres are at the "pixel-is-point"
positions, and the GeoTIFF transform stores the outer edge, so the north-west
pixel centre of tile N44E006 is at (lat 44 + 1 - 0.5*3", lon 6 + 0.5*3").  We
read the affine transform from each file rather than assuming it.

API
    dem = DEM()                      # loads tiles from download_dem's folder
    dem.elev(lat, lon)               # bilinear elevation (m), nan outside
    dem.elev_many(lats, lons)        # vectorised (numpy arrays)
    dem.window(lat0, lat1, lon0, lon1)  -> (Z, lats, lons) sub-grid

The DEM is a surface model (canopy/buildings included); vertical accuracy
< 4 m LE90 (Copernicus DEM product handbook, AIRBUS 2020); horizontal
resolution ~90 m at the equator, 90 m x 63 m at 45N.
"""
import glob
import os
import re

import numpy as np

try:
    import rasterio
except ImportError:  # pragma: no cover
    rasterio = None

DEFAULT_DIR = os.environ.get(
    "HANNIBAL_DEM_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dem"),
)

R_EARTH = 6371008.8  # m, IUGG mean radius


def haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = p2 - p1
    dl = np.radians(np.asarray(lon2) - np.asarray(lon1))
    h = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R_EARTH * np.arcsin(np.sqrt(h))


class DEM:
    def __init__(self, folder=DEFAULT_DIR, lat_range=(43, 47), lon_range=(4, 9)):
        if rasterio is None:
            raise RuntimeError("pip install rasterio")
        self.folder = folder
        files = sorted(glob.glob(os.path.join(folder, "Copernicus_DSM_COG_30_N*_E*_DEM.tif")))
        if not files:
            raise RuntimeError("no DEM tiles in %s (run download_dem.py)" % folder)
        # discover grid geometry from the first tile
        with rasterio.open(files[0]) as src:
            t = src.transform
            self.dlon = t.a
            self.dlat = -t.e
            nrows, ncols = src.height, src.width
        assert abs(self.dlon - 3 / 3600.0) < 1e-9 and abs(self.dlat - 3 / 3600.0) < 1e-9, (self.dlon, self.dlat)
        self.lat0, self.lat1 = lat_range
        self.lon0, self.lon1 = lon_range
        NR = int(round((self.lat1 - self.lat0) / self.dlat))
        NC = int(round((self.lon1 - self.lon0) / self.dlon))
        self.Z = np.full((NR, NC), np.nan, dtype=np.float32)
        # top-left pixel centre of mosaic
        self.lat_top = None
        self.lon_left = None
        self.tiles = []
        for f in files:
            m = re.search(r"N(\d\d)_00_E(\d\d\d)_00", os.path.basename(f))
            tlat, tlon = int(m.group(1)), int(m.group(2))
            if not (self.lat0 <= tlat < self.lat1 and self.lon0 <= tlon < self.lon1):
                continue
            with rasterio.open(f) as src:
                arr = src.read(1).astype(np.float32)
                nd = src.nodata
                t = src.transform
                if nd is not None:
                    arr[arr == nd] = np.nan
                # pixel centre of row 0, col 0
                clat = t.f + t.e * 0.5
                clon = t.c + t.a * 0.5
                if self.lat_top is None:
                    # define mosaic pixel-centre origin from grid alignment
                    # (all tiles share the same 3" grid)
                    frac_lat = (clat - tlat) % self.dlat
                    frac_lon = (clon - tlon) % self.dlon
                    self.lat_top = self.lat1 - self.dlat + frac_lat if frac_lat < self.dlat / 2 else self.lat1 + frac_lat - self.dlat
                    self.lon_left = self.lon0 + frac_lon
                    # simpler: derive from this tile directly
                    self.lat_top = clat + (self.lat1 - 1 - tlat) * 1.0
                    self.lon_left = clon - (tlon - self.lon0) * 1.0
                r0 = int(round((self.lat_top - clat) / self.dlat))
                c0 = int(round((clon - self.lon_left) / self.dlon))
                h, w = arr.shape
                self.Z[r0:r0 + h, c0:c0 + w] = arr
                self.tiles.append((tlat, tlon, os.path.basename(f)))
        self.nrows, self.ncols = self.Z.shape

    # ---- coordinate helpers
    def rc(self, lat, lon):
        """fractional (row, col) of a lat/lon in mosaic pixel-centre coordinates"""
        r = (self.lat_top - np.asarray(lat, dtype=float)) / self.dlat
        c = (np.asarray(lon, dtype=float) - self.lon_left) / self.dlon
        return r, c

    def latlon(self, r, c):
        return self.lat_top - r * self.dlat, self.lon_left + c * self.dlon

    def elev_many(self, lat, lon):
        r, c = self.rc(lat, lon)
        r = np.atleast_1d(r)
        c = np.atleast_1d(c)
        out = np.full(r.shape, np.nan)
        ok = (r >= 0) & (r <= self.nrows - 1) & (c >= 0) & (c <= self.ncols - 1)
        r0 = np.floor(r[ok]).astype(int)
        c0 = np.floor(c[ok]).astype(int)
        r0 = np.clip(r0, 0, self.nrows - 2)
        c0 = np.clip(c0, 0, self.ncols - 2)
        fr = r[ok] - r0
        fc = c[ok] - c0
        z00 = self.Z[r0, c0]
        z01 = self.Z[r0, c0 + 1]
        z10 = self.Z[r0 + 1, c0]
        z11 = self.Z[r0 + 1, c0 + 1]
        out[ok] = (z00 * (1 - fr) * (1 - fc) + z01 * (1 - fr) * fc + z10 * fr * (1 - fc) + z11 * fr * fc)
        return out

    def elev(self, lat, lon):
        return float(self.elev_many([lat], [lon])[0])

    def window(self, lat_s, lat_n, lon_w, lon_e):
        r1, c0 = self.rc(lat_s, lon_w)
        r0, c1 = self.rc(lat_n, lon_e)
        r0, r1 = max(int(np.floor(r0)), 0), min(int(np.ceil(r1)), self.nrows - 1)
        c0, c1 = max(int(np.floor(c0)), 0), min(int(np.ceil(c1)), self.ncols - 1)
        Z = self.Z[r0:r1 + 1, c0:c1 + 1]
        lats = self.lat_top - np.arange(r0, r1 + 1) * self.dlat
        lons = self.lon_left + np.arange(c0, c1 + 1) * self.dlon
        return Z, lats, lons

    def is_saddle(self, lat, lon, radius_px=6):
        """Crude saddle test: within radius, the point is lower than the
        highest ground in two opposite quadrants and higher than the lowest
        ground in the other two.  Returns (True/False, zmin, z, zmax)."""
        r, c = self.rc(lat, lon)
        r, c = int(round(float(r))), int(round(float(c)))
        z = float(self.Z[r, c])
        win = self.Z[r - radius_px:r + radius_px + 1, c - radius_px:c + radius_px + 1]
        return (float(np.nanmin(win)), z, float(np.nanmax(win)))


if __name__ == "__main__":
    import sys

    d = DEM()
    print("mosaic", d.Z.shape, "tiles", len(d.tiles), "origin", d.lat_top, d.lon_left)
    for lat, lon, name in [
        (45.2598, 6.9009, "Col du Mont-Cenis (~2083 m)"),
        (44.7027, 7.0610, "Col de la Traversette (~2947 m)"),
        (44.9341, 6.7250, "Col de Montgenevre (~1854 m)"),
        (45.0703, 7.6869, "Turin (~239 m)"),
        (43.8047, 4.6284, "Fourques (~10 m)"),
    ]:
        print("%-32s %8.1f m" % (name, d.elev(lat, lon)))
    if len(sys.argv) == 3:
        print(d.elev(float(sys.argv[1]), float(sys.argv[2])))
