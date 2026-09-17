#!/usr/bin/env python3
"""Assemble report.html from template.html + part_a.html + part_b.html and the model outputs.
Run after code/succession_model.py:  python3 build_report.py
"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..")
R = json.load(open(os.path.join(CASE, "data", "results.json")))
L = json.load(open(os.path.join(CASE, "data", "likelihood_table.json")))

def pct(x): return f"{100*x:.0f}"
b, s, g = R["base"], R["sceptical"], R["generous"]

def sens_table():
    cols = [("base", "Base"), ("sceptical", "Sceptical"), ("generous", "Generous"), ("prior_one_person_half", "One-person weights"), ("prior_literature", "Named-view weights")]
    rows = [
        ("Neferneferuaten = Nefertiti", lambda r: r["identity"].get("Nefertiti", 0)),
        ("Neferneferuaten = Meritaten", lambda r: r["identity"].get("Meritaten", 0)),
        ("Neferneferuaten a man (Smenkhkare renamed)", lambda r: r["identity"].get("Male", 0)),
        ("Smenkhkare a separate king", lambda r: r["separate_smenkhkare"]),
        ("Smenkhkare before her", lambda r: r["smenkhkare_before"]),
        ("Coregent of a living Akhenaten", lambda r: r["coregency"].get("yes", 0)),
        ("KV55 = Smenkhkare", lambda r: r["kv55"].get("Smenkhkare", 0)),
        ("KV55 = Akhenaten", lambda r: r["kv55"].get("Akhenaten", 0)),
        ("Nibhururiya = Akhenaten", lambda r: r["nibhururiya"].get("Akhenaten", 0)),
        ("Nibhururiya = Tutankhamun", lambda r: r["nibhururiya"].get("Tutankhamun", 0)),
        ("Widow = Nefertiti", lambda r: r["dahamunzu"].get("Nefertiti", 0)),
        ("Widow = Ankhesenamun", lambda r: r["dahamunzu"].get("Ankhesenamun", 0)),
    ]
    out = ["<table><tr><th>Question</th>" + "".join(f"<th class='n'>{c[1]}</th>" for c in cols) + "</tr>"]
    for lab, fn in rows:
        out.append(f"<tr><td>{lab}</td>" + "".join(f"<td class='n'>{pct(fn(R[c[0]]))}</td>" for c in cols) + "</tr>")
    out.append("</table>")
    return "\n".join(out)

def bar(v):
    return f"<span class='bar'><i style='width:{int(round(100*v))}%'></i></span>"

def likelihood_table():
    out = ["<table class='scores'><colgroup><col class='c1'><col class='c2'><col class='c3'><col class='c4'></colgroup><tr><th>Item</th><th>Bears on</th><th>Scores by state (base / sceptical / generous)</th><th>Sources</th></tr>"]
    for row in L:
        cells = []
        for key, vals in row["values"].items():
            k = html.escape(key.replace("id=", "").replace("sk=", "Smenkhkare ").replace("cg=", "coregency ").replace("kv=", "KV55 ").replace("nb=", "Nibhururiya "))
            cells.append(f"<div class='row'>{bar(vals['base'])}<span class='mono'>{vals['base']:.2f} / {vals['sceptical']:.2f} / {vals['generous']:.2f}</span><span class='state'>{k}</span></div>")
        out.append(f"<tr><td><span class='mono'>{row['code']}</span><br>{html.escape(row['title'])}</td><td class='small'>{html.escape(row['depends'])}</td><td>{''.join(cells)}</td><td class='small'>{html.escape(row['sources'])}</td></tr>")
    out.append("</table>")
    return "\n".join(out)

def results_table():
    cols = [("base", "Base"), ("sceptical", "Sceptical"), ("generous", "Generous"), ("egyptian_items_only", "Egyptian items only"), ("hittite_items_only", "Hittite items only")]
    def line(name, key, sub):
        return f"<tr><td>{name}</td>" + "".join(f"<td class='n'>{pct(R[c][key].get(sub, 0))}</td>" for c, _ in cols) + "</tr>"
    out = ["<table><tr><th>Question</th>" + "".join(f"<th class='n'>{t}</th>" for _, t in cols) + "</tr>"]
    idn = {"Nefertiti": "Nefertiti", "Meritaten": "Meritaten", "Tasherit": "Neferneferuaten-tasherit", "Male": "a man (Smenkhkare renamed)"}
    for sub in ["Nefertiti", "Meritaten", "Tasherit", "Male"]:
        out.append(line(f"Identity: {idn[sub]}", "identity", sub))
    for sub, lab in [("before_coreg", "Smenkhkare: coregent who died first"), ("before_sole", "Smenkhkare: between Akhenaten and her"), ("after", "Smenkhkare: after her"), ("same", "Smenkhkare: the same person")]:
        out.append(line(lab, "smenkhkare", sub))
    out.append(line("Coregency: yes", "coregency", "yes"))
    for sub in ["Smenkhkare", "Akhenaten", "AnotherSon"]:
        out.append(line(f"KV55: {sub if sub!='AnotherSon' else 'another son of Amenhotep III'}", "kv55", sub))
    for sub in ["Akhenaten", "Tutankhamun", "Smenkhkare"]:
        out.append(line(f"Nibhururiya: {sub}", "nibhururiya", sub))
    for sub in ["Nefertiti", "Meritaten", "Ankhesenamun"]:
        out.append(line(f"Widow: {sub}", "dahamunzu", sub))
    out.append("</table>")
    return "\n".join(out)

def loo_table():
    out = ["<table><tr><th>Item removed</th><th class='n'>Nefertiti</th><th class='n'>Separate Smenkhkare</th><th class='n'>Coregency</th><th class='n'>KV55 = Akhenaten</th><th class='n'>Nibhururiya = Tutankhamun</th></tr>"]
    for code, r in R["leave_one_out"].items():
        out.append(f"<tr><td><span class='mono'>{code}</span> {html.escape(r['title'][:90])}{'…' if len(r['title'])>90 else ''}</td><td class='n'>{pct(r['P_Nefertiti'])}</td><td class='n'>{pct(r['P_separate'])}</td><td class='n'>{pct(r['P_coreg'])}</td><td class='n'>{pct(r['P_kv55_Akh'])}</td><td class='n'>{pct(r['P_nib_Tut'])}</td></tr>")
    out.append("</table>")
    return "\n".join(out)

def figure(fname, caption):
    svg = open(os.path.join(CASE, "figures", fname), encoding="utf-8").read()
    return f"<figure class='fig'><div class='figwrap'>{svg}</div><figcaption class='cap'>{html.escape(caption)}</figcaption></figure>"

def top_states():
    names = {"before_coreg": "Smenkhkare a coregent who died first", "before_sole": "Smenkhkare between Akhenaten and her", "after": "Smenkhkare after her", "same": "one person"}
    out = ["<ol>"]
    for t in R["top_states"][:8]:
        idn = {"Tasherit": "Neferneferuaten-tasherit", "Male": "a man (Smenkhkare renamed)"}
        kvn = {"AnotherSon": "another son of Amenhotep III"}
        out.append(f"<li><span class='mono'>{pct(t['p'])}%</span> Neferneferuaten = {idn.get(t['id'], t['id'])}; {names[t['sk']]}; coregency {t['cg']}; KV55 = {kvn.get(t['kv'], t['kv'])}; Nibhururiya = {t['nb']}.</li>")
    out.append("</ol>")
    return "\n".join(out)

tpl = open(os.path.join(HERE, "template.html")).read() + open(os.path.join(HERE, "part_a.html")).read() + open(os.path.join(HERE, "part_b.html")).read()
loo = R["leave_one_out"]
subs = {
    "{{P_NEF}}": pct(b["identity"]["Nefertiti"]), "{{P_NEF_SCEP}}": pct(s["identity"]["Nefertiti"]), "{{P_NEF_GEN}}": pct(g["identity"]["Nefertiti"]),
    "{{P_SEP}}": pct(b["separate_smenkhkare"]), "{{P_BEFORE}}": pct(b["smenkhkare_before"]), "{{P_AFTER}}": pct(b["smenkhkare_after"]),
    "{{P_COREG}}": pct(b["coregency"]["yes"]), "{{P_KV_SM}}": pct(b["kv55"]["Smenkhkare"]), "{{P_KV_AKH}}": pct(b["kv55"]["Akhenaten"]),
    "{{P_NB_AKH}}": pct(b["nibhururiya"]["Akhenaten"]), "{{P_NB_TUT_SCEP}}": pct(s["nibhururiya"]["Tutankhamun"]),
    "{{P_DH_NEF}}": pct(b["dahamunzu"]["Nefertiti"]), "{{P_DH_MER}}": pct(b["dahamunzu"]["Meritaten"]), "{{P_DH_ANK}}": pct(b["dahamunzu"]["Ankhesenamun"]),
    "{{LOO_E06}}": pct(loo["E06"]["P_Nefertiti"]), "{{LOO_E02_DELTA}}": str(int(round(100*(b["identity"]["Nefertiti"] - loo["E02"]["P_Nefertiti"])))),
    "{{P_NEF_EG}}": pct(R["egyptian_items_only"]["identity"]["Nefertiti"]), "{{P_SAME_SCEP}}": pct(s["smenkhkare"].get("same", 0)),
    "{{P_MALE_SCEP}}": pct(s["identity"].get("Male", 0)), "{{P_MER}}": pct(b["identity"]["Meritaten"]), "{{P_MER_SCEP}}": pct(s["identity"]["Meritaten"]),
    "{{P_NSI}}": pct(b["models"].get("N-SI", 0)), "{{P_NSI_ONE}}": pct(R["prior_one_person_half"]["models"].get("N-SI", 0)),
    "{{FIG1}}": figure("fig1_leave_one_out.svg", "Figure 1. The Nefertiti figure with each of the 30 scored items removed in turn. Made for this report from the leave-one-out run of the scoring."),
    "{{FIG2}}": figure("fig2_sensitivity.svg", "Figure 2. The six main answers under the three readings and under two other starting weightings; the same numbers as Table 1. Made for this report from the scoring under five settings."),
    "{{SENS_TABLE}}": sens_table(), "{{LIKELIHOOD_TABLE}}": likelihood_table(), "{{RESULTS_TABLE}}": results_table(), "{{LOO_TABLE}}": loo_table(), "{{TOP_STATES}}": top_states(),
}
for k, v in subs.items():
    tpl = tpl.replace(k, v)
left = [w for w in ["{{"] if w in tpl]
open(os.path.join(HERE, "report.html"), "w").write(tpl)
open(os.path.join(CASE, "report.html"), "w").write(tpl)
print("written", len(tpl), "bytes; unresolved placeholders:", tpl.count("{{"))
