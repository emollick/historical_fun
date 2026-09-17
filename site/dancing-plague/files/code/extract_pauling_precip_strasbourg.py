#!/usr/bin/env python3
"""Extract Pauling et al. 2006 (Clim. Dyn. 26:387-405; NOAA contribution 2007-054) gridded seasonal
precipitation reconstruction (0.5 deg) for the cell nearest Strasbourg (48.58N, 7.75E): spring (MAM) and summer (JJA).
Input files (NOAA): sources/climate/prec-pauling-sp.txt.gz, prec-pauling-su.txt.gz
Grid: 82 rows (70.75N..30.25N, step 0.5) x 140 cols (-29.75E..39.75E, step 0.5); block = 1 header line + 82 rows.
Units: mm per season (reconstructed values 1500-1900; observational 1901-2000).
Output: data/pauling2006_precip_strasbourg.csv
"""
import gzip, numpy as np, pandas as pd, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lats = np.round(70.75 - 0.5*np.arange(82), 2)
lons = np.round(-29.75 + 0.5*np.arange(140), 2)
LAT0, LON0 = 48.58, 7.75
i = int(np.argmin(abs(lats-LAT0))); j = int(np.argmin(abs(lons-LON0)))
print("nearest cell", lats[i], lons[j])
def read(season_file):
    out = {}
    with gzip.open(os.path.join(base,"sources/climate",season_file),"rt") as f:
        lines = f.read().splitlines()
    nblk = len(lines)//83
    for b in range(nblk):
        hdr = lines[b*83].split()
        yr = int(hdr[0])
        rows = lines[b*83+1:b*83+83]
        def tofloat(v):
            v=v.strip()
            return np.nan if v in ("","NA") else float(v)
        rr=[]
        for r in rows:
            vals=[tofloat(v) for v in r.rstrip("\n").split("\t")]
            if len(vals)!=140:
                # some rows carry a stray trailing token; keep the first 140
                vals=(vals+[np.nan]*140)[:140]
            rr.append(vals)
        grid=np.array(rr)
        assert grid.shape==(82,140), grid.shape
        out[yr] = {"cell": grid[i,j], "mean3x3": np.nanmean(grid[i-1:i+2, j-1:j+2]), "mean5x5": np.nanmean(grid[i-2:i+3, j-2:j+3])}
    return out
sp = read("prec-pauling-sp.txt.gz"); su = read("prec-pauling-su.txt.gz")
years = sorted(sp)
df = pd.DataFrame({"year": years,
    "MAM_precip_mm_cell": [sp[y]["cell"] for y in years], "MAM_precip_mm_3x3": [sp[y]["mean3x3"] for y in years],
    "JJA_precip_mm_cell": [su[y]["cell"] for y in years], "JJA_precip_mm_3x3": [su[y]["mean3x3"] for y in years]})
ref = df[(df.year>=1500)&(df.year<=1600)]
for c in ["MAM_precip_mm_cell","JJA_precip_mm_cell"]:
    m, s = ref[c].mean(), ref[c].std()
    df[c+"_anom_vs_1500-1600"] = df[c]-m
    df[c+"_z_1500-1600"] = (df[c]-m)/s
    df[c+"_rank_wettest1_1500-1600"] = df[c].where((df.year>=1500)&(df.year<=1600)).rank(ascending=False, method="min")
    m2, s2 = df[(df.year>=1901)&(df.year<=2000)][c].mean(), df[(df.year>=1901)&(df.year<=2000)][c].std()
    df[c+"_anom_vs_1901-2000"] = df[c]-m2
df.to_csv(os.path.join(base,"data/pauling2006_precip_strasbourg.csv"), index=False, float_format="%.2f")
pd.set_option("display.width",250)
print(df[(df.year>=1510)&(df.year<=1525)].to_string(index=False))
print("1500-1600 means: MAM %.1f (sd %.1f), JJA %.1f (sd %.1f); 1901-2000 means: MAM %.1f, JJA %.1f" % (
    ref.MAM_precip_mm_cell.mean(), ref.MAM_precip_mm_cell.std(), ref.JJA_precip_mm_cell.mean(), ref.JJA_precip_mm_cell.std(),
    df[(df.year>=1901)&(df.year<=2000)].MAM_precip_mm_cell.mean(), df[(df.year>=1901)&(df.year<=2000)].JJA_precip_mm_cell.mean()))
