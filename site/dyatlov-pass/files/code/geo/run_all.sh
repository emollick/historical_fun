#!/bin/sh
# Re-run every computation (inputs in raw/ and data/; outputs in out/). Takes ~1 min.
set -e
cd "$(dirname "$0")"
python3 geo_common.py      # prints the local-metric coordinates of every point in data/coordinates.csv
python3 dem_slope.py       # DEM slopes, profiles, map (needs raw/Copernicus_*.tif, raw/terrarium/*.png)
python3 astro.py           # sun/moon tables
python3 weather.py         # GHCN tables, Burmantovo sheet, wind chill
python3 walking.py         # distances and walking-time envelopes (needs out/dem_summary.json)
python3 horizon.py         # terrain horizon at the tent, local sunset/sunrise
