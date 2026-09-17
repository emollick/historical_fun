"""
Figures for the report, written as inline SVG fragments into report-src/figs/.
1. fig_distance.svg : a bearing-and-distance plot of the places named in the scenarios, centred on the
   1587 settlement site, with rings at 25, 50, 75 and 100 statute miles. It is a diagram of the computed
   straight-line distances (data/distances_from_roanoke.csv), not a map.
2. fig_scenarios.svg : horizontal bars of the model's scenario probabilities with the sensitivity range
   (data/model_results.json), written only if that file exists.
"""
import csv, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "report-src", "figs")
os.makedirs(FIG, exist_ok=True)

# ---------- 1. distance plot ----------
rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "distances_from_roanoke.csv"))))
short = {
 "Dasamonquepeuc (Manns Harbor)": "Dasamonquepeuc",
 "Port Ferdinando / Hatarask inlet (approx.)": "Port Ferdinando",
 "Kenricks Mounts / Chicamacomico (Rodanthe)": "Kenricks Mounts",
 "Croatoan: Cape Creek site 31DR1 (Buxton)": "Croatoan (Cape Creek)",
 "Wokokon (Ocracoke)": "Wokokon",
 "Site X / Site Y, Salmon Creek (near Merry Hill)": "Site X and Y, Salmon Creek",
 "Edenton (reported findspot region of the 1937 Dare Stone)": "Edenton (Dare Stone)",
 "Chowanoke, main town of the Chowanoc (near Harrellsville)": "Chowanoke",
 "Windsor (Cashie River, Tuscarora country)": "Cashie River (Tuscarora)",
 "Weldon (Roanoke River fall line)": "Roanoke River fall line",
 "Bath (Pamlico River)": "Pamlico River",
 "Chesepian towns, Lynnhaven / Great Neck (Virginia Beach)": "Chesepian towns",
 "Jamestown (1607)": "Jamestown",
}
W, H = 720, 620
cx, cy = 400, 330
scale = 2.55  # px per statute mile
def xy(mi, brg):
    a = math.radians(brg)
    return cx + scale*mi*math.sin(a), cy - scale*mi*math.cos(a)

s = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="figd-t figd-d" xmlns="http://www.w3.org/2000/svg">',
     '<title id="figd-t">Straight-line distances from the Roanoke settlement site</title>',
     '<desc id="figd-d">Places named in the scenarios plotted by bearing and straight-line distance from the 1587 settlement site, with rings at 25, 50, 75 and 100 statute miles.</desc>']
for r in (25, 50, 75, 100):
    cls = "ring" if r == 50 else "grid"
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*scale:.1f}" fill="none" class="{cls}"/>')
    s.append(f'<text x="{cx+4}" y="{cy - r*scale - 4:.1f}" class="tick">{r} mi</text>')
s.append(f'<text x="{cx+8}" y="{cy - 50*scale + 14:.1f}" class="note">"50 miles into the maine"</text>')
s.append(f'<circle cx="{cx}" cy="{cy}" r="5" class="dot copper"/>')
s.append(f'<text x="{cx+9}" y="{cy+5}" class="place" font-weight="600">Roanoke Island settlement</text>')
# label offsets to avoid collisions (dx, dy, anchor)
off = {
 "Dasamonquepeuc": (-8, 18, "end"), "Port Ferdinando": (8, 16, "start"), "Kenricks Mounts": (8, 4, "start"),
 "Croatoan (Cape Creek)": (8, 4, "start"), "Wokokon": (-8, 14, "end"), "Site X and Y, Salmon Creek": (-8, -6, "end"),
 "Edenton (Dare Stone)": (-8, 14, "end"), "Chowanoke": (-8, -6, "end"), "Cashie River (Tuscarora)": (-8, 18, "end"),
 "Roanoke River fall line": (8, -6, "start"), "Pamlico River": (-8, 4, "end"), "Chesepian towns": (8, -4, "start"), "Jamestown": (8, 4, "start"),
}
for r in rows:
    name = short[r["place"]]; mi = float(r["statute_miles"]); brg = float(r["bearing_deg"])
    x, y = xy(mi, brg)
    main = r["on_mainland"] == "yes"
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if main else 4.5}" class="dot{"" if main else " copper"}"/>')
    dx, dy, anc = off.get(name, (8, 4, "start"))
    s.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="place" text-anchor="{anc}">{name} <tspan class="tick">{mi:.0f}</tspan></text>')
# legend
s.append(f'<circle cx="24" cy="{H-40}" r="5" class="dot"/><text x="34" y="{H-36}" class="note">mainland</text>')
s.append(f'<circle cx="110" cy="{H-40}" r="4.5" class="dot copper"/><text x="120" y="{H-36}" class="note">Outer Banks island or inlet</text>')
s.append(f'<text x="24" y="{H-16}" class="note">Numbers are statute miles in a straight line; water routes are longer. North is up.</text>')
s.append('</svg>')
open(os.path.join(FIG, "fig_distance.svg"), "w").write("\n".join(s))
print("wrote fig_distance.svg")

# ---------- 2. scenario bars ----------
mr = os.path.join(ROOT, "data", "model_results.json")
if os.path.exists(mr):
    m = json.load(open(mr))
    items = m["headline"]          # list of {label, p, lo, hi, lead}
    W2 = 720; rowh = 34; top = 28; left = 250; barw = 400
    H2 = top + rowh*len(items) + 46
    t = [f'<svg class="chart" viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="figs-t figs-d" xmlns="http://www.w3.org/2000/svg">',
         '<title id="figs-t">Scenario probabilities with sensitivity ranges</title>',
         '<desc id="figs-d">Horizontal bars show the reported probability of each scenario; the line through each bar shows the range across the sensitivity cases.</desc>']
    for g in (0, 25, 50, 75, 100):
        x = left + barw*g/100
        t.append(f'<line x1="{x:.1f}" y1="{top-6}" x2="{x:.1f}" y2="{top + rowh*len(items)}" class="grid"/>')
        t.append(f'<text x="{x:.1f}" y="{top + rowh*len(items) + 18}" class="tick" text-anchor="middle">{g}%</text>')
    for i, it in enumerate(items):
        y = top + i*rowh
        w = barw*it["p"]/100
        cls = "bar" + ("" if it.get("lead") else " mute") + (" copper" if it.get("copper") else "")
        t.append(f'<rect x="{left}" y="{y+6}" width="{w:.1f}" height="20" rx="0" class="{cls}"/>')
        t.append(f'<rect x="{left+w-4:.1f}" y="{y+6}" width="4" height="20" rx="3" class="{cls}"/>')
        lo, hi = left + barw*it["lo"]/100, left + barw*it["hi"]/100
        t.append(f'<line x1="{lo:.1f}" y1="{y+16}" x2="{hi:.1f}" y2="{y+16}" class="range"/>')
        t.append(f'<line x1="{lo:.1f}" y1="{y+11}" x2="{lo:.1f}" y2="{y+21}" class="range"/><line x1="{hi:.1f}" y1="{y+11}" x2="{hi:.1f}" y2="{y+21}" class="range"/>')
        t.append(f'<text x="{left-10}" y="{y+21}" class="rowlab" text-anchor="end">{it["label"]}</text>')
        t.append(f'<text x="{max(hi, left+w)+8:.1f}" y="{y+21}" class="val">{it["p"]:.0f}</text>')
    t.append(f'<text x="12" y="{H2-6}" class="note">Bar: reported value. Line: lowest to highest value across the nineteen alternative weightings in section {m.get("model_section","")}.</text>')
    t.append('</svg>')
    open(os.path.join(FIG, "fig_scenarios.svg"), "w").write("\n".join(t))
    print("wrote fig_scenarios.svg")
else:
    print("model_results.json not present; scenario figure skipped")
