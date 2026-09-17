#!/usr/bin/env python3
"""Extract Luterbacher et al. 2004 (Science 303:1499) summer (JJA) and Xoplaki et al. 2005 (GRL 32:L15713) spring (MAM)
gridded (0.5 deg) European temperature reconstructions for the cell nearest Strasbourg (48.58N, 7.75E).
Input: sources/climate/temp_luterbacher_su.txt.gz, temp_xoplaki_sp.txt.gz  (CRU SO&P mirror:
  https://crudata.uea.ac.uk/cru/projects/soap/pw/data/recon/luter04/ ; same data at NOAA europe-seasonal-files/)
Format assumed (checked below): block = header line 'year season' + 70 rows (69.75N..35.25N) x 130 cols (-24.75E..39.75E); missing=-99.999.
Values are absolute temperatures (deg C) for the season.
Output: data/luterbacher2004_xoplaki2005_temp_strasbourg.csv
"""
import gzip, numpy as np, pandas as pd, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAT0, LON0 = 48.58, 7.75
def read(fn):
    with gzip.open(os.path.join(base,"sources/climate",fn),"rt") as f:
        lines = f.read().splitlines()
    # detect block structure
    hdr_idx = [i for i,l in enumerate(lines) if len(l.split())==2 and l.split()[0].isdigit() and int(l.split()[0])>=1500]
    nrow = hdr_idx[1]-hdr_idx[0]-1
    ncol = len(lines[hdr_idx[0]+1].split())
    print(fn, "blocks", len(hdr_idx), "rows", nrow, "cols", ncol)
    lats = 69.75 - 0.5*np.arange(nrow)   # assumption: top row 69.75N (70N-35N domain)
    lons = -24.75 + 0.5*np.arange(ncol)  # assumption: 25W-40E domain
    i = int(np.argmin(abs(lats-LAT0))); j = int(np.argmin(abs(lons-LON0)))
    print("  assumed cell", lats[i], lons[j])
    out = {}
    for h in hdr_idx:
        yr = int(lines[h].split()[0])
        rows = lines[h+1:h+1+nrow]
        g = np.array([[float(v) for v in r.split()] for r in rows])
        g[g<=-99] = np.nan
        out[yr] = (g[i,j], np.nanmean(g[i-1:i+2,j-1:j+2]), g)
    return out, lats, lons
su, lats, lons = read("temp_luterbacher_su.txt.gz")
sp, _, _ = read("temp_xoplaki_sp.txt.gz")
years = sorted(su)
df = pd.DataFrame({"year": years, "MAM_T_cell_C": [sp[y][0] for y in years], "MAM_T_3x3_C": [sp[y][1] for y in years],
                   "JJA_T_cell_C": [su[y][0] for y in years], "JJA_T_3x3_C": [su[y][1] for y in years]})
for c in ["MAM_T_cell_C","JJA_T_cell_C"]:
    ref = df[(df.year>=1500)&(df.year<=1600)][c]; m,s = ref.mean(), ref.std()
    df[c+"_anom_1500-1600"] = df[c]-m; df[c+"_z_1500-1600"] = (df[c]-m)/s
    df[c+"_rank_warmest1_1500-1600"] = df[c].where((df.year>=1500)&(df.year<=1600)).rank(ascending=False, method="min")
    ref2 = df[(df.year>=1901)&(df.year<=2000)][c]; df[c+"_anom_1901-2000"] = df[c]-ref2.mean()
df.to_csv(os.path.join(base,"data/luterbacher2004_xoplaki2005_temp_strasbourg.csv"), index=False, float_format="%.2f")
pd.set_option("display.width",250)
print(df[(df.year>=1510)&(df.year<=1525)].to_string(index=False))
# sanity check: the 1517 summer grid vs. NOAA per-year file 1517-su.txt (same reconstruction, 6 values/line)
try:
    vals = [float(v) for l in open(os.path.join(base,"sources/climate/noaa_1517-su.txt")) for v in l.split()]
    g = np.array(vals); print("NOAA 1517-su.txt values:", len(vals), "-> rows", len(vals)/130)
    g = g.reshape(-1,130); g[g<=-999]=np.nan
    print("NOAA file value at assumed Strasbourg cell:", g[int(np.argmin(abs(lats-LAT0))), int(np.argmin(abs(lons-LON0)))], " CRU file:", su[1517][0])
    # print a small map row around Strasbourg for plausibility (should be ~17-19 C in JJA at 48.75N)
    print("Row 48.75N, lon 5.75..9.75:", np.round(su[1517][2][int(np.argmin(abs(lats-LAT0))), int(np.argmin(abs(lons-5.75))):int(np.argmin(abs(lons-9.75)))+1],2))
    print("Col 7.75E, lat 50.75..46.75:", np.round(su[1517][2][int(np.argmin(abs(lats-50.75))):int(np.argmin(abs(lats-46.75)))+1, int(np.argmin(abs(lons-LON0)))],2))
except Exception as e: print("check failed", e)
