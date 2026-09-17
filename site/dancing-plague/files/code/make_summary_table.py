#!/usr/bin/env python3
"""Combine the extracted series into one per-year table for 1512-1521 (core 1515-1519).
Inputs: data/owda_strasbourg_1500-1600.csv, data/pauling2006_precip_strasbourg.csv, data/luterbacher2004_xoplaki2005_temp_strasbourg.csv,
        data/documentary_temperature_1510-1525.csv, data/prices_strasbourg_frankfurt_1500-1530.csv
Output: data/summary_by_year_1512-1521.csv (and a markdown print)
"""
import pandas as pd, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda f: os.path.join(base,"data",f)
o = pd.read_csv(D("owda_strasbourg_1500-1600.csv")).set_index("year")
p = pd.read_csv(D("pauling2006_precip_strasbourg.csv")).set_index("year")
l = pd.read_csv(D("luterbacher2004_xoplaki2005_temp_strasbourg.csv")).set_index("year")
d = pd.read_csv(D("documentary_temperature_1510-1525.csv")).set_index("year")
pr = pd.read_csv(D("prices_strasbourg_frankfurt_1500-1530.csv")).set_index("year")
yrs = range(1512,1522)
t = pd.DataFrame(index=yrs); t.index.name="year"
t["OWDA_JJA_scPDSI_cell"] = o["pdsi_strasbourg_cell"]
t["OWDA_rank_driest1_of_1500-1600"] = o["pdsi_strasbourg_cell_rank_driest1"]
t["OWDA_3x3_mean"] = o["pdsi_mean_3x3"]
t["Pauling_MAM_precip_anom_mm"] = p["MAM_precip_mm_cell_anom_vs_1500-1600"]
t["Pauling_MAM_rank_wettest1"] = p["MAM_precip_mm_cell_rank_wettest1_1500-1600"]
t["Pauling_JJA_precip_anom_mm"] = p["JJA_precip_mm_cell_anom_vs_1500-1600"]
t["Pauling_JJA_rank_wettest1"] = p["JJA_precip_mm_cell_rank_wettest1_1500-1600"]
t["Luterbacher_cell_MAM_T_anom_C"] = l["MAM_T_cell_C_anom_1500-1600"]
t["Luterbacher_cell_JJA_T_anom_C"] = l["JJA_T_cell_C_anom_1500-1600"]
t["Luterbacher_cell_JJA_rank_warmest1"] = l["JJA_T_cell_C_rank_warmest1_1500-1600"]
for c in ["Dobrovolny_DJF_T_anom_C","Dobrovolny_MAM_T_anom_C","Dobrovolny_JJA_T_anom_C","Dobrovolny_SON_T_anom_C","Dobrovolny_MAY_T_anom_C","Dobrovolny_JUN_T_anom_C","Dobrovolny_JUL_T_anom_C","Glaser_MAM_sum","Glaser_JJA_sum","GHD_Bur_days_after_31Aug","Chuine2004_Burgundy_AprAug_T_anom_C"]:
    t[c] = d[c]
for c in ["Strasbourg_Wheat_Cent_per_Kg","Strasbourg_Rye_Cent_per_Kg","Strasbourg_Rye_Cent_per_Kg_index_vs_1500-1530_median","Strasbourg_WhiteBread_Cent_per_Kg","Strasbourg_wage_Labourer_Francs_per_Day","Frankfurt_Rye_pfennig_per_Achtel"]:
    t[c] = pr[c]
t.to_csv(D("summary_by_year_1512-1521.csv"), float_format="%.2f")
pd.set_option("display.width",300); pd.set_option("display.max_columns",60)
print(t.T.to_string())
