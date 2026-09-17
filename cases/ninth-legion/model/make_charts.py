"""Generate inline SVG charts (theme-aware via CSS classes) from career_model_results.json."""
import json
res = json.load(open("career_model_results.json"))
base = res["base_numisius_father"]
half = res["numisius_same_p35"]

# ---------- Chart 1: timeline with per-officer 90% bands and medians ----------
Y0, Y1 = 100, 165
W, H = 900, 360
L, R, T, B = 215, 20, 40, 40
def x(y): return L + (y - Y0) / (Y1 - Y0) * (W - L - R)
rows = [
  ("RIB 665, York gate", "fixed", 107.9, 108.9, None, "last dated text (Trajan's 12th tribunician year)"),
  ("Burbuleius, tribune", "band", 110, 118, 115, "consul 135; senatorial tribune of the Ninth"),
  ("Valerius Proclus, centurion", "band", 112, 124, 118, "discharged from the Ninth (ILS 2666b)"),
  ("Florentinus, legate", "band", base["Florentinus_start"]["p05"], base["Florentinus"]["p95"], base["Florentinus"]["median"], "Arabia by 2 Dec 127; Narbonensis 123/4 or 124/5"),
  ("Karus, tribune", "band", base["Karus"]["p05"], base["Karus"]["p95"], base["Karus"]["median"], "consul 144"),
  ("Crispinus, tribune", "band", base["Crispinus"]["p05"], base["Crispinus"]["p95"], base["Crispinus"]["median"], "consul 150"),
  ("Numisius Iunior, tribune", "band2", 161-27, 161-17, 161-22, "only if he is the consul of 161"),
  ("VI Victrix reaches Britain", "fixed", 122, 124.5, None, "Laelianus, consul 145; RIB 1427"),
  ("expeditio Britannica", "fixed", 123, 126, None, "Sabinus, Agrippa; Spanish levy 123"),
]
rh = (H - T - B) / len(rows)
svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Timeline of the dated evidence for Legio IX Hispana, AD 100 to 165" class="chart">']
# scenario shading
for (a, b, lab) in [(122, 130, "Britain c. 122-130"), (132, 136, "Bar Kokhba"), (161, 162, "Elegeia")]:
    svg.append(f'<rect x="{x(a):.1f}" y="{T-18}" width="{x(b)-x(a):.1f}" height="{H-T-B+18}" class="scen"/>')
    if lab.startswith("Britain"):
        svg.append(f'<text x="{x(b)-3:.1f}" y="{T-6}" class="scenlab" text-anchor="end">{lab}</text>')
    else:
        svg.append(f'<text x="{x(a)+3:.1f}" y="{T-6}" class="scenlab">{lab}</text>')
# axis
for y in range(Y0, Y1+1, 5):
    xx = x(y)
    svg.append(f'<line x1="{xx:.1f}" y1="{T}" x2="{xx:.1f}" y2="{H-B}" class="grid"/>')
    if y % 10 == 0:
        svg.append(f'<text x="{xx:.1f}" y="{H-B+16}" class="tick" text-anchor="middle">{y}</text>')
svg.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-6}" class="axis" text-anchor="middle">year AD</text>')
for i, (name, kind, a, b, med, note) in enumerate(rows):
    cy = T + rh * (i + 0.5)
    svg.append(f'<text x="{L-8}" y="{cy+4:.1f}" class="rowlab" text-anchor="end">{name}</text>')
    if kind == "fixed":
        svg.append(f'<rect x="{x(a):.1f}" y="{cy-7:.1f}" width="{max(x(b)-x(a),3):.1f}" height="14" class="fixed"/>')
    else:
        cls = "band" if kind == "band" else "band alt"
        svg.append(f'<rect x="{x(a):.1f}" y="{cy-8:.1f}" width="{x(b)-x(a):.1f}" height="16" rx="3" class="{cls}"/>')
        svg.append(f'<line x1="{x(med):.1f}" y1="{cy-10:.1f}" x2="{x(med):.1f}" y2="{cy+10:.1f}" class="median"/>')
    svg.append(f'<text x="{x(b)+6:.1f}" y="{cy+4:.1f}" class="note">{note}</text>')
svg.append('</svg>')
open("chart_timeline.svg", "w").write("\n".join(svg))

# ---------- Chart 2: P(legion still existed in year Y) ----------
W2, H2 = 900, 300
L2, R2, T2, B2 = 60, 20, 20, 40
def x2(y): return L2 + (y - 115) / (165 - 115) * (W2 - L2 - R2)
def y2(p): return T2 + (1 - p) * (H2 - T2 - B2)
svg = [f'<svg viewBox="0 0 {W2} {H2}" width="100%" role="img" aria-label="Probability that the legion still existed in a given year, from the career model" class="chart">']
for p in [0, 0.25, 0.5, 0.75, 1.0]:
    svg.append(f'<line x1="{L2}" y1="{y2(p):.1f}" x2="{W2-R2}" y2="{y2(p):.1f}" class="grid"/>')
    svg.append(f'<text x="{L2-8}" y="{y2(p)+4:.1f}" class="tick" text-anchor="end">{int(p*100)}%</text>')
for yv in range(115, 166, 5):
    svg.append(f'<text x="{x2(yv):.1f}" y="{H2-B2+16}" class="tick" text-anchor="middle">{yv}</text>')
svg.append(f'<text x="{(L2+W2-R2)/2:.0f}" y="{H2-6}" class="axis" text-anchor="middle">year AD</text>')
for (a, b) in [(132, 136), (161, 162)]:
    svg.append(f'<rect x="{x2(a):.1f}" y="{T2}" width="{x2(b)-x2(a):.1f}" height="{H2-T2-B2}" class="scen"/>')
def path(series, cls):
    pts = " ".join(f"{x2(int(y)):.1f},{y2(p):.1f}" for y, p in sorted(series.items(), key=lambda kv: int(kv[0])))
    return f'<polyline points="{pts}" class="{cls}"/>'
svg.append(path(base["P_exists_by_year"], "line main"))
svg.append(path(half["P_exists_by_year"], "line alt"))
svg.append(f'<text x="{x2(138):.1f}" y="{y2(0.55):.1f}" class="note">Numisius Iunior = consul of 161 (35% weight)</text>')
svg.append(f'<text x="{x2(133.5):.1f}" y="{y2(0.10):.1f}" class="note">consul of 161 is his son</text>')
svg.append('</svg>')
open("chart_probability.svg", "w").write("\n".join(svg))
print("charts written")
