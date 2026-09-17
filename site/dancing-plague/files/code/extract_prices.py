#!/usr/bin/env python3
"""Grain and bread prices for Strasbourg (Hanauer 1878 via Robert C. Allen's transcription) and Frankfurt (Elsas 1940 via
Lindert/Jacks GPIH file), 1500-1530.
Sources (downloaded copies in sources/climate/):
  gpih_Allen_Strasbourg_1313-1875.xlsx  <- https://gpih.ucdavis.edu/files/Allen_Strasbourg_1313-1875.xlsx
     Sheet 'Prices', block 'A1) Original Prices', source [1] = Hanauer, A., Etudes economiques sur l'Alsace ancienne et moderne
     (Strasbourg 1878). Units as given by Allen: grains and bread in 'Cent/Kg' (cents of a franc of 4.5 g Ag per kg; Allen notes
     'Hanauer's original prices are in francs of 4.5 gram Ag'); wine 'Francs/Litre'; wages 'Francs/Day'.
  nuffield_allen_strasbourg.xls <- https://www.nuffield.ox.ac.uk/media/2126/strasbourg.xls (same data)
  gpih_Frankfurt_1500-1800.xls <- https://gpih.ucdavis.edu/files/Frankfurt_1500-1800.xls  (Sheet 'Grains': Elsas, Umriss einer
     Geschichte der Preise und Loehne in Deutschland, vol. II (Leiden 1940), pp. 463-9; rye/oats/wheat/barley in pfennig per Achtel and g Ag per litre)
Output: data/prices_strasbourg_frankfurt_1500-1530.csv
"""
import pandas as pd, numpy as np, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = lambda f: os.path.join(base,"sources/climate",f)
x = pd.ExcelFile(S("gpih_Allen_Strasbourg_1313-1875.xlsx"))
pr = x.parse("Prices", header=None)
goods = pr.iloc[6].tolist(); units = pr.iloc[3].tolist()
hdr_row = 7
data = pr.iloc[hdr_row+1:].copy()
data.columns = range(data.shape[1])
data = data[pd.to_numeric(data[0], errors="coerce").notna()]
data[0] = data[0].astype(int)
cols = {}
for j,(g,u) in enumerate(zip(goods,units)):
    if isinstance(g,str) and g.strip() in ("Wheat","White Bread","Brown Bread","Rye","Barley","Oats","Wine") and j < 30:
        cols[j] = f"Strasbourg_{g.strip().replace(' ','')}_{str(u).replace('/','_per_')}"
out = data[[0]+list(cols)].rename(columns={0:"year", **cols}).set_index("year").astype(float)
# wages (Allen sheet 'Wages': carpenter, mason, labourer francs/day)
wg = x.parse("Wages", header=None); wd = wg.iloc[8:].copy(); wd.columns=range(wd.shape[1])
wd = wd[pd.to_numeric(wd[0], errors="coerce").notna()]; wd[0]=wd[0].astype(int)
wd = wd.set_index(0)
out["Strasbourg_wage_Mason_Francs_per_Day"] = pd.to_numeric(wd[3], errors="coerce")
out["Strasbourg_wage_Labourer_Francs_per_Day"] = pd.to_numeric(wd[4], errors="coerce")
# Frankfurt (Elsas)
f = pd.ExcelFile(S("gpih_Frankfurt_1500-1800.xls")).parse("Grains", header=None)
fd = f.iloc[12:].copy(); fd.columns=range(fd.shape[1]); fd = fd[pd.to_numeric(fd[0], errors="coerce").notna()]; fd[0]=fd[0].astype(int); fd=fd.set_index(0)
for j,name in {1:"Frankfurt_Rye_pfennig_per_Achtel",2:"Frankfurt_Oats_pfennig_per_Achtel",3:"Frankfurt_Wheat_pfennig_per_Achtel",
               15:"Frankfurt_Rye_gAg_per_litre",17:"Frankfurt_Wheat_gAg_per_litre"}.items():
    out[name] = pd.to_numeric(fd[j], errors="coerce")
win = out.loc[1500:1530].copy()
for c in ["Strasbourg_Wheat_Cent_per_Kg","Strasbourg_Rye_Cent_per_Kg","Strasbourg_WhiteBread_Cent_per_Kg","Frankfurt_Rye_pfennig_per_Achtel"]:
    if c in win:
        med = win[c].median()
        win[c+"_index_vs_1500-1530_median"] = (win[c]/med*100).round(0)
win.to_csv(os.path.join(base,"data/prices_strasbourg_frankfurt_1500-1530.csv"), float_format="%.2f")
pd.set_option("display.width",300); pd.set_option("display.max_columns",40)
print(win.loc[1505:1525].to_string())
print("\n1500-1530 medians:", {c: round(win[c].median(),2) for c in win.columns if "index" not in c})
# real wage check: kg of rye per day's labourer wage
w = win["Strasbourg_wage_Labourer_Francs_per_Day"]; r = win["Strasbourg_Rye_Cent_per_Kg"]/100
print("\nkg rye per labourer day-wage:", (w/r).loc[1510:1522].round(1).to_dict())
