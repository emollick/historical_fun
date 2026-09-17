#!/usr/bin/env python3
"""Spatial context for the OWDA 1516-1518 drought: regional means and a map of JJA scPDSI 1517 (and 1515-1519 panel).
Output: data/owda_regional_means_1510-1525.csv, data/owda_map_1515-1519.png
"""
import xarray as xr, numpy as np, pandas as pd, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ds = xr.open_dataset(os.path.join(base,"sources/climate/owda.nc"), decode_times=False)
p = ds.pdsi
regions = {"UpperRhine_47.5-49.5N_7-8.5E": (47.5,49.5,7.0,8.5), "CentralEurope_46-52N_5-15E": (46,52,5,15),
           "France_43-50N_-4-7E": (43,50,-4,7), "Germany_47.5-54N_6-15E": (47.5,54,6,15), "Europe_all": (27,71,-12,45)}
rows=[]
for yr in range(1510,1526):
    r={"year":yr}
    for k,(la0,la1,lo0,lo1) in regions.items():
        sub = p.sel(time=yr, lat=slice(la0,la1), lon=slice(lo0,lo1))
        r[k+"_mean"] = float(sub.mean(skipna=True)); r[k+"_frac_below_-3"] = float((sub<-3).sum()/sub.notnull().sum())
    rows.append(r)
df=pd.DataFrame(rows); df.to_csv(os.path.join(base,"data/owda_regional_means_1510-1525.csv"), index=False, float_format="%.3f")
pd.set_option("display.width",250); print(df.to_string(index=False))
fig, axes = plt.subplots(1,5, figsize=(22,5.2))
for ax,yr in zip(axes, range(1515,1520)):
    g = p.sel(time=yr, lat=slice(42,55), lon=slice(-5,20))
    im = ax.pcolormesh(g.lon, g.lat, g.T, cmap="BrBG", vmin=-6, vmax=6, shading="auto")
    ax.plot(7.75,48.58,"k*",ms=10); ax.set_title(f"OWDA JJA scPDSI {yr}"); ax.set_aspect(1.4)
fig.colorbar(im, ax=axes, shrink=0.8, label="scPDSI (wet=+)"); fig.suptitle("Old World Drought Atlas (Cook et al. 2015) - star = Strasbourg")
fig.savefig(os.path.join(base,"data/owda_map_1515-1519.png"), dpi=110, bbox_inches="tight"); print("map saved")
