#!/usr/bin/env python3
"""Tabulate documentary/phenological temperature evidence for 1510-1525:
 - Dobrovolný et al. 2010 (Clim. Change 101:69; NOAA study 9970, doi:10.25921/w3yg-xe03): seasonal (DJF, MAM, JJA, SON) and monthly (Apr-Aug)
   Central European temperature anomalies (deg C vs 1961-1990; SPLICED column) plus the raw DE/CH/CZ indices.
 - Glaser & Riemann 2009 (J. Quat. Sci. 24:437; NOAA contribution 2010-040): monthly temperature indices (-3..+3) for Germany/Central Europe 1500-2006.
 - Luterbacher et al. 2004 / Xoplaki et al. 2005 European land mean seasonal temperatures (NOAA contribution 2006-060).
 - Daux et al. 2012 grape harvest dates (NOAA 2012-129): Alsace, Burgundy, Switzerland (Leman), Germany regional composites (days after 31 Aug).
 - Chuine et al. 2004 (Nature 432:289): Burgundy Pinot noir GHD and reconstructed Apr-Aug temperature anomaly.
Output: data/documentary_temperature_1510-1525.csv
"""
import pandas as pd, numpy as np, os, re, io
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = lambda f: os.path.join(base, "sources/climate", f)
Y0, Y1 = 1510, 1525
out = pd.DataFrame({"year": range(Y0, Y1+1)}).set_index("year")
# Dobrovolny
for s in ["djf","mam","jja","son","apr","may","jun","jul","aug","ann"]:
    lines = [l for l in open(S(f"dobrovolny2010temperature-{s}-noaa.txt")) if not l.startswith("#")]
    df = pd.read_csv(io.StringIO("".join(lines)), sep="\t")
    df = df.set_index(df.columns[0])
    out[f"Dobrovolny_{s.upper()}_T_anom_C"] = df.loc[Y0:Y1, "SPLICED"]
    if s in ["mam","jja","apr","may","jun","jul","aug"]:
        for reg in ["DE.ind","CH.ind","CZ.ind"]:
            out[f"Dobrovolny_{s.upper()}_{reg}"] = df.loc[Y0:Y1, reg]
# Glaser monthly indices (section 2)
txt = open(S("glaser2009temperature.txt"), encoding="latin-1").read().splitlines()
i0 = [i for i,l in enumerate(txt) if l.startswith("Year     Jan")][0]
rows = []
for l in txt[i0+1:]:
    p = l.split()
    if len(p)==13 and p[0].isdigit(): rows.append([int(p[0])]+[int(v) for v in p[1:]])
    elif rows and not l.strip(): break
g = pd.DataFrame(rows, columns=["year"]+["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]).set_index("year")
for m in ["Mar","Apr","May","Jun","Jul","Aug"]:
    out[f"Glaser_{m}_Tindex"] = g.loc[Y0:Y1, m]
out["Glaser_MAM_sum"] = g.loc[Y0:Y1, ["Mar","Apr","May"]].sum(axis=1)
out["Glaser_JJA_sum"] = g.loc[Y0:Y1, ["Jun","Jul","Aug"]].sum(axis=1)
# Luterbacher European mean
lines = open(S("europe-seasonal-luterbacher2004.txt")).read().splitlines()
i0 = [i for i,l in enumerate(lines) if l.startswith("Year") and "DJF" in l][0]
rows = [l.split() for l in lines[i0+1:] if re.match(r"^\s*\d{4}\s", l)]
lu = pd.DataFrame(rows, columns=["year","DJF","MAM","JJA","SON","Annual"]).astype(float); lu["year"]=lu.year.astype(int); lu=lu.set_index("year")
ref = lu.loc[1500:1600]
for s in ["MAM","JJA"]:
    out[f"Luterbacher_EuropeMean_{s}_C"] = lu.loc[Y0:Y1, s]
    out[f"Luterbacher_EuropeMean_{s}_anom_vs_1500-1600"] = lu.loc[Y0:Y1, s] - ref[s].mean()
# Daux 2012 GHD: parse the three fixed-width data parts; assign each value to the header whose label START is nearest the value's END
txt = open(S("europe2012ghd.txt"), encoding="latin-1").read().splitlines()
ghd = {}
label_map = {"Als":"Alsace","Bur":"Burgundy","Germany":"Germany","Switzerland(Leman":"Switzerland_Leman","Spain":"Spain","Jura":"Jura","Northern":"NorthernLorraine_or_Rhone_or_Italy"}
hdr_idx = [i for i,l in enumerate(txt) if l.startswith("Year") and len(l.split())>3]
for h in hdr_idx:
    toks = [(m.group(0), m.start()) for m in re.finditer(r"\S+", txt[h])][1:]
    # collapse multi-word labels: a label starts where the gap to the previous token > 1 space
    labels=[]
    for t,pos in toks:
        if labels and pos - (labels[-1][1]+len(labels[-1][0])) <= 1: labels[-1]=(labels[-1][0]+" "+t, labels[-1][1])
        else: labels.append((t,pos))
    for l in txt[h+1:]:
        if not re.match(r"^\d{4}", l):
            if l.strip()=="" and any(k in ghd for k in [lab for lab,_ in labels]): break
            continue
        yr=int(l[:4])
        for m in re.finditer(r"\S+", l[4:]):
            end = 4+m.end()
            lab = min(labels, key=lambda L: abs((L[1]+len(L[0]))-end))[0]
            try: ghd.setdefault(lab,{})[yr]=float(m.group(0))
            except: pass
print("GHD series found:", {k:len(v) for k,v in ghd.items()})
for lab in ["Als","Bur","Germany","Switzerland(Leman Lake)","Jura","Spain","Northern Lorraine","Southern Rhone Valley","SouthernRhoneValley"]:
    if lab in ghd:
        out[f"GHD_{lab.replace(' ','_')}_days_after_31Aug"] = pd.Series(ghd[lab]).reindex(range(Y0,Y1+1))
# Chuine 2004 Burgundy
lines = open(S("burgundy2004.txt"), encoding="latin-1").read().splitlines()
secs = [i for i,l in enumerate(lines) if l.startswith("Year     Harvest date") or l.startswith("Year    temperature anomaly")]
def sec(i):
    d={}
    for l in lines[i:]:
        p=l.split()
        if len(p)==2 and p[0].isdigit(): d[int(p[0])]=float(p[1])
        elif d and (l.startswith("Column") or l.startswith("DATA")): break
    return pd.Series(d)
chuine_ghd = sec(secs[0]); chuine_t = sec(secs[1])
out["Chuine2004_Burgundy_GHD_days_after_1Sep"] = chuine_ghd.reindex(range(Y0,Y1+1))
out["Chuine2004_Burgundy_AprAug_T_anom_C"] = chuine_t.reindex(range(Y0,Y1+1))
out.to_csv(os.path.join(base,"data/documentary_temperature_1510-1525.csv"), float_format="%.2f")
pd.set_option("display.width",300); pd.set_option("display.max_columns",80)
print(out.loc[1514:1520].T.to_string())
