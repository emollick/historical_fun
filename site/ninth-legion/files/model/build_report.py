# Assembles report/index.html from style.css, the table fragments and the two SVG charts.
import pathlib, re
R = pathlib.Path(__file__).parent
S = R.parent
style = (R / "style.css").read_text()
stones = (R / "frag_britain_stones.html").read_text()
tiles = (R / "frag_britain_tiles.html").read_text()
chart_t = (S / "model/chart_timeline.svg").read_text()
chart_p = (S / "model/chart_probability.svg").read_text()

def edcs(i): return f"https://edcs.hist.uzh.ch/monument/EDCS-{i}"
def edh(i): return f"https://edh.ub.uni-heidelberg.de/edh/inschrift/HD{i}"
def rib(n): return f"https://romaninscriptionsofbritain.org/inscriptions/{n}"

officer_rows = [
 ("Q. Petillius Cerialis","legate",'<a href="https://www.thelatinlibrary.com/tacitus/tac.ann14.shtml">Tacitus, <i>Ann.</i> 14.32</a>',"Boudican revolt","60/61","secure"),
 ("C. Caristanius Fronto","legate <i>in Britannia</i>",f'<a href="{edcs("16201163")}">ILS 9485</a>',"command under Vespasian (d. 79); cos. 90","c. 76–79","secure"),
 ("L. Roscius Aelianus","tribune, with a vexillation on the Rhine",f'<a href="{edcs("05801602")}">ILS 1025</a>',"<i>expeditio Germanica</i> 83; cos. 100","83","secure"),
 ("C. Velius Rufus","prefect of vexillations of nine legions",f'<a href="{edh("031653")}">ILS 9200</a>',"Domitian's German war","c. 83–89","secure"),
 ("L. Burbuleius Optatus Ligarianus","<i>tribunus laticlavius</i>",f'<a href="{edcs("20600417")}">ILS 1066</a>',"cos. in office 19 May 135 (diploma)","c. 113–117 (Birley: 118–122)","career"),
 ("Ti. Claudius Vitalis","centurion",f'<a href="{edcs("19700276")}">ILS 2656</a>',"decorated twice in the Dacian wars, then XX V.V. twice","c. 109–115","career"),
 ("L. Valerius Proclus","centurion (last post)",f'<a href="{edh("042822")}">ILS 2666b</a>',"decorated <i>bello Dacico</i>, four posts earlier","c. 116–120","career"),
 ("L. Decrius Longinus","<i>praefectus castrorum</i>",f'<a href="{edh("027393")}">AE 1913, 215</a>',"primipilate of XXII Deiotariana (last attested 119)","c. 110–120","career"),
 ("Anonymous eques, Mersch","tribune",f'<a href="{edh("011186")}">CIL XIII 4030</a>',"monument dated late in Hadrian's reign by its style","c. 105–125","style"),
 ("Anonymous eques, Rome","tribune, then procurator of &ldquo;the new province of Arabia&rdquo;",f'<a href="{edh("013966")}">CIL VI 41280</a>',"Arabia created 106","after 106; probably under Trajan or Hadrian","open"),
 ("L. Latinius Macer","<i>primus pilus</i>, <i>praefectus castrorum</i>",f'<a href="{edh("014357")}">AE 1968, 323</a> (Aachen)',"none on the stone","c. 105–125 by the Nijmegen context","context"),
 ("M. Cocceius Severus","<i>primus pilus</i>, then prefect of X Gemina",f'<a href="{edcs("05400409")}">CIL V 7159</a>',"X Gemina at Nijmegen until c. 104","no usable terminus","open"),
 ("T. Aninius Sextius Florentinus","legate",f'<a href="{edcs("21200156")}">CIL III 87</a> (Petra)',"governor of Arabia 2 Dec 127 (P. Yadin 16); procos. Narbonensis 123/4 or 124/5","c. 121–124; cannot end before c. 122/3","career, tight"),
 ("L. Aemilius Karus","tribune (first of two)",f'<a href="{edcs("17800486")}">ILS 1077</a>',"cos. in office 19 March 144 (diplomas); Arabia 142","c. 121–125 (bounds 118–127)","career"),
 ("L. Novius Crispinus","tribune",f'<a href="{edh("031258")}">ILS 1070</a>',"cos. designate 149/150; praetor c. 135","c. 124–128 (bounds 120–130)","career"),
 ("Q. Camurius Numisius Iunior","tribune",f'<a href="{edcs("23000342")}">CIL XI 5670</a>',"a Q. Numisius Iunior cos. 8 Feb 161","c. 105–118 if father of the consul; c. 139–143 if the consul","disputed"),
 ("L. Servaeus Sabinus","centurion",f'<a href="{edh("025791")}">AE 1930, 109</a>',"stone reads VIII; emended","under Trajan or Hadrian","open"),
 ("Aelius Asclepiades","<i>miles leg. IX</i>",f'<a href="{edcs("11500706")}">CIL X 1769</a>',"nomen Aelius only","no usable terminus","open"),
]
off = ['<div class="tablewrap"><table><thead><tr><th>Officer or soldier</th><th>Post in the Ninth</th><th>Inscription</th><th>Fixed point (cos. = consul)</th><th>Service in the Ninth</th><th>Basis</th></tr></thead><tbody>']
for n,p,i,f,s,b in officer_rows:
    off.append(f'<tr><td>{n}</td><td>{p}</td><td class="ref">{i}</td><td>{f}</td><td>{s}</td><td class="small">{b}</td></tr>')
off.append('</tbody></table></div>')
officers = "\n".join(off)

html = (R / "template.html").read_text()
for k,v in {"{{STYLE}}":style,"{{STONES}}":stones,"{{TILES}}":tiles,"{{OFFICERS}}":officers,"{{CHART_TIMELINE}}":chart_t,"{{CHART_PROB}}":chart_p}.items():
    assert k in html, k
    html = html.replace(k, v)
(R / "index.html").write_text(html)
print("wrote", len(html), "bytes")
