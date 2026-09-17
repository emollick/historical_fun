#!/usr/bin/env python3
"""Extract OWDA (Cook et al. 2015, Sci. Adv. 1:e1500561; NOAA study 19419, doi:10.25921/rjm6-mq74)
JJA scPDSI for the grid cell nearest Strasbourg (48.58N, 7.75E) and its neighbours.
Input : sources/climate/owda.nc  (downloaded from
        https://www.ncei.noaa.gov/pub/data/paleo/treering/reconstructions/europe/owda.nc)
Output: data/owda_strasbourg_1500-1600.csv, data/owda_strasbourg_1515-1519_summary.csv
Wet = positive PDSI; dry = negative.
"""
import xarray as xr, numpy as np, pandas as pd, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ds = xr.open_dataset(os.path.join(base, "sources/climate/owda.nc"), decode_times=False)
pdsi = ds["pdsi"]
years = ds["time"].values.astype(int)
LAT0, LON0 = 48.58, 7.75
cell = pdsi.sel(lat=LAT0, lon=LON0, method="nearest")
lat_c, lon_c = float(cell.lat), float(cell.lon)
print(f"Nearest OWDA cell to Strasbourg: lat={lat_c}, lon={lon_c}")
# 3x3 neighbourhood (+-0.5 deg) and 5x5 (+-1 deg)
def box(dlat, dlon):
    sub = pdsi.sel(lat=slice(lat_c-dlat-1e-6, lat_c+dlat+1e-6), lon=slice(lon_c-dlon-1e-6, lon_c+dlon+1e-6))
    return sub
b3 = box(0.5, 0.5); b5 = box(1.0, 1.0)
df = pd.DataFrame({"year": years, "pdsi_strasbourg_cell": cell.values})
df["pdsi_mean_3x3"] = b3.mean(dim=("lat","lon"), skipna=True).values
df["pdsi_mean_5x5"] = b5.mean(dim=("lat","lon"), skipna=True).values
# individual neighbour cells
for la in b3.lat.values:
    for lo in b3.lon.values:
        df[f"pdsi_{la:.2f}N_{lo:.2f}E"] = pdsi.sel(lat=la, lon=lo).values
# Additional reference cells: Basel (47.56N,7.59E), Colmar (48.08N,7.36E), Freiburg (47.99N,7.85E), Karlsruhe (49.01N,8.40E), Nancy (48.69N,6.18E)
for name,(la,lo) in {"basel":(47.56,7.59),"colmar":(48.08,7.36),"freiburg":(47.99,7.85),"karlsruhe":(49.01,8.40),"nancy":(48.69,6.18),"stuttgart":(48.78,9.18)}.items():
    c = pdsi.sel(lat=la, lon=lo, method="nearest")
    df[f"pdsi_{name}_{float(c.lat):.2f}N_{float(c.lon):.2f}E"] = c.values
win = df[(df.year>=1500)&(df.year<=1600)].copy()
# ranks within 1500-1600 (1 = wettest, 101 = driest) and (1 = driest)
for col in ["pdsi_strasbourg_cell","pdsi_mean_3x3","pdsi_mean_5x5"]:
    win[col+"_rank_wettest1"] = win[col].rank(ascending=False, method="min").astype(int)
    win[col+"_rank_driest1"] = win[col].rank(ascending=True, method="min").astype(int)
    win[col+"_pctile_1500_1600"] = win[col].rank(pct=True).round(3)
win.to_csv(os.path.join(base, "data/owda_strasbourg_1500-1600.csv"), index=False, float_format="%.3f")
full = df[(df.year>=1000)&(df.year<=2012)]
summ = win[(win.year>=1510)&(win.year<=1525)][["year","pdsi_strasbourg_cell","pdsi_strasbourg_cell_rank_wettest1","pdsi_strasbourg_cell_rank_driest1","pdsi_mean_3x3","pdsi_mean_3x3_rank_wettest1","pdsi_mean_5x5","pdsi_mean_5x5_rank_wettest1"]].copy()
# percentile within 1000-2012 for the cell
s_full = full["pdsi_strasbourg_cell"]
summ["cell_pctile_1000_2012"] = [round((s_full < v).mean(),3) for v in summ["pdsi_strasbourg_cell"]]
summ.to_csv(os.path.join(base, "data/owda_strasbourg_1515-1519_summary.csv"), index=False, float_format="%.3f")
pd.set_option("display.width", 250)
print(summ.to_string(index=False))
print("\n1500-1600 stats for cell: mean %.3f sd %.3f min %.3f (yr %d) max %.3f (yr %d)" % (
    win.pdsi_strasbourg_cell.mean(), win.pdsi_strasbourg_cell.std(), win.pdsi_strasbourg_cell.min(), win.loc[win.pdsi_strasbourg_cell.idxmin(),"year"], win.pdsi_strasbourg_cell.max(), win.loc[win.pdsi_strasbourg_cell.idxmax(),"year"]))
print("1000-2012 stats for cell: mean %.3f sd %.3f" % (s_full.mean(), s_full.std()))
print("\nNeighbour cells 1515-1519:")
cols = [c for c in df.columns if c.startswith("pdsi_4") ]
print(df[(df.year>=1514)&(df.year<=1520)][["year"]+cols].to_string(index=False))
print("\nReference cells 1514-1520:")
cols = [c for c in df.columns if any(k in c for k in ["basel","colmar","freiburg","karlsruhe","nancy","stuttgart"])]
print(df[(df.year>=1514)&(df.year<=1520)][["year"]+cols].to_string(index=False))
