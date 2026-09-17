"""Build HTML table fragments for the report from the data JSON files."""
import json, collections, html, re, os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "")
def esc(s): return html.escape(str(s if s is not None else ""))

# ---------- Britain: stones ----------
recs = json.load(open(S + "britain_inscriptions.json"))
order = ["RIB 3047","RIB 3042","RIB 254","RIB 255","RIB 256","RIB 257","RIB 260","RIB 659","RIB 673","RIB 680","RIB 665"]
stones = [r for r in recs if r["ref"] in order]
stones.sort(key=lambda r: order.index(r["ref"]) if r["ref"] in order else 99)
rows = []
for r in stones:
    site = r["site"].split(",")[0].split(" (")[0]
    date = r.get("rib_date") or ""
    if not date or date.startswith("(no"):
        date = f'{r.get("date_from") or "?"}-{r.get("date_to") or "?"} (inferred from context)'
    rows.append(f'<tr><td class="ref"><a href="{esc(r["url"])}">{esc(r["ref"])}</a></td><td>{esc(site)}</td><td>{esc(r.get("object",""))}</td><td>{esc((r.get("person") or "").split(";")[0])}</td><td>{esc(r.get("rank") or "")}</td><td>{esc(date)}</td></tr>')
open("frag_britain_stones.html","w").write('<div class="tablewrap"><table><thead><tr><th>Ref.</th><th>Site</th><th>Object</th><th>Person</th><th>Rank / role</th><th>RIB date</th></tr></thead><tbody>' + "\n".join(rows) + '</tbody></table></div>')

# ---------- Britain: tile stamps by site and numeral form ----------
tiles = [r for r in recs if r["ref"].startswith("RIB 2462") and "17" not in r["ref"].split(".")[0][-2:]]
tiles = [r for r in recs if r["ref"].startswith("RIB 2462") and not r["ref"].startswith("RIB 2462.17")]
def form(r):
    t = r.get("text_diplomatic") or ""
    if "VIIII" in t or "VI[III" in t or re.search(r"V\[", t): return "VIIII"
    if "IX" in t: return "IX"
    return "?"
def site(r):
    s = r["site"]
    s = s.replace("Possibly from Slack but more probably from York","York (prob.)").replace("(?)","").replace("Castleford (Lagentium)","Castleford")
    s = s.split(" (")[0].strip()
    return s
c = collections.Counter((site(r), form(r)) for r in tiles)
sites = collections.Counter(site(r) for r in tiles)
rows = []
for s, n in sites.most_common():
    ix, vi, q = c[(s,"IX")], c[(s,"VIIII")], c[(s,"?")]
    rows.append(f'<tr><td>{esc(s)}</td><td class="num">{n}</td><td class="num">{ix}</td><td class="num">{vi}</td><td class="num">{q}</td></tr>')
rows.append(f'<tr class="total"><td>Total (RIB 2462.1-16)</td><td class="num">{len(tiles)}</td><td class="num">{sum(v for (s,f),v in c.items() if f=="IX")}</td><td class="num">{sum(v for (s,f),v in c.items() if f=="VIIII")}</td><td class="num">{sum(v for (s,f),v in c.items() if f=="?")}</td></tr>')
open("frag_britain_tiles.html","w").write('<div class="tablewrap"><table><thead><tr><th>Findspot</th><th class="num">Stamps</th><th class="num">Numeral IX</th><th class="num">Numeral VIIII</th><th class="num">Numeral lost</th></tr></thead><tbody>' + "\n".join(rows) + '</tbody></table></div>')
print("stones", len(stones), "tiles", len(tiles), dict(sites))

# ---------- Officers table ----------
off = json.load(open(S + "officers.json"))
def urlof(e):
    u = e.get("url") or ""
    m = re.search(r"https?://\S+?(?=[\s;)]|$)", u)
    return m.group(0) if m else ""
rows_o = []
keep = ["Petillius", "Caristanius", "Roscius", "Velius", "Burbuleius", "Florentinus", "Karus", "Crispinus", "Numisius", "Mersch", "Latinius", "Decrius", "Valerius L. f. Proclus", "Vitalis", "Servaeus", "Asclepiades"]
short = {"Q. Petillius Cerialis Caesius Rufus":"Q. Petillius Cerialis","C. Caristanius C. f. Ser. Fronto":"C. Caristanius Fronto","L. Roscius M. f. Qui. Aelianus Maecius Celer":"L. Roscius Aelianus","C. Velius Salvi f. Rufus":"C. Velius Rufus","L. Burbuleius L. f. Quir. Optatus Ligarianus":"L. Burbuleius Optatus Ligarianus","T. (CIL: L.) Aninius L. f. Pap. Sextius Florentinus":"T. Aninius Sextius Florentinus","L. Aemilius L. f. Cam. Karus (Carus)":"L. Aemilius Karus","L. Novius Crispinus Martialis Saturninus":"L. Novius Crispinus","Q. Camurius Q. f. Lem. Numisius Iunior":"Q. Camurius Numisius Iunior","[---]us, equestrian officer from Mersch (anonymous)":"Anonymous equestrian, Mersch","L. Latinius L. f. Publilia Macer, Verona":"L. Latinius Macer","L. Decrius L. f. Ser. Longinus":"L. Decrius Longinus","L. Valerius L. f. Proclus":"L. Valerius Proclus","Ti. Claudius Ti. f. [Ga]l. Vitalis":"Ti. Claudius Vitalis","L. Servaeus Sabinus":"L. Servaeus Sabinus","Aelius Asclepiades, natione Cilix":"Aelius Asclepiades"}
rankshort = {"Petillius":"legate","Caristanius":"legate","Roscius":"tribune (laticlave), vexillation","Velius":"prefect of vexillations","Burbuleius":"tribunus laticlavius","Florentinus":"legate","Karus":"tribune (laticlave)","Crispinus":"tribune (laticlave)","Numisius":"tribune (laticlave implied)","Mersch":"tribune (equestrian)","Latinius":"primus pilus, praefectus castrorum","Decrius":"praefectus castrorum","Proclus":"centurion","Vitalis":"centurion","Servaeus":"centurion","Asclepiades":"miles"}
fixed = {"Petillius":"Boudican revolt, Tac. Ann. 14.32","Caristanius":"command under Vespasian (d. 79); cos. 90","Roscius":"expeditio Germanica 83; cos. 100","Velius":"Domitianic German war","Burbuleius":"cos. suff. in office 19 May 135 (diploma)","Florentinus":"governor of Arabia 2 Dec 127 (P. Yadin 16); procos. Narbonensis 123/4 or 124/5","Karus":"cos. suff. in office 19 March 144 (diplomas); Arabia 142","Crispinus":"cos. designate 149/150; legate III Aug. 147-9; praetor c. 135","Numisius":"a Q. Numisius Iunior cos. suff. 8 Feb 161 (diploma)","Mersch":"none (monument late-Hadrianic on style)","Latinius":"none","Decrius":"primipilate of XXII Deiotariana (last attested 119)","Proclus":"decorated bello Dacico 101-6, four posts later","Vitalis":"two Dacian-war decorations, then XX V.V. twice","Servaeus":"none (numeral on stone reads VIII)","Asclepiades":"nomen Aelius only"}
for e in off:
    n = e["name"]
    key = next((k for k in keep if k in n), None)
    if not key: continue
    k2 = "Proclus" if key.startswith("Valerius") else key
    imp = e["implied_service_in_IX"]["most_likely"]
    imp = re.sub(r"\s*\(.*", "", imp) if k2 != "Numisius" else "c. 105-118 if father of the consul; c. 139-143 if the consul himself"
    if k2 == "Asclepiades": imp = "no usable terminus"
    ref = e["inscription_ref"].split(";")[0].split(",")[0] if k2 not in ("Petillius",) else "Tacitus, Ann. 14.32"
    ref = re.sub(r"\s*\(.*?\)", "", ref)
    u = urlof(e)
    refcell = f'<a href="{esc(u)}">{esc(ref)}</a>' if u else esc(ref)
    rows_o.append(f'<tr><td>{esc(short.get(n,n))}</td><td>{esc(rankshort[k2])}</td><td class="ref">{refcell}</td><td>{esc(fixed[k2])}</td><td>{esc(imp)}</td></tr>')
open("frag_officers.html","w").write('<div class="tablewrap"><table><thead><tr><th>Officer or soldier</th><th>Post in the Ninth</th><th>Inscription</th><th>Fixed point</th><th>Implied service in the Ninth</th></tr></thead><tbody>' + "\n".join(rows_o) + '</tbody></table></div>')
print("officers rows", len(rows_o))
