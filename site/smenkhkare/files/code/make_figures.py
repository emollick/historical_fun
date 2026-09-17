"""Draw the two figures of the report as SVG files from data/results.json.

Figure 1: the Nefertiti figure with each of the 30 scored items removed in turn
          (the leave-one-out run of succession_model.py), as bars from the
          all-items value.
Figure 2: the six main answers under the base, sceptical and generous readings
          and under two other starting weightings.

Run from the case folder:  python3 code/make_figures.py
Writes figures/fig1_leave_one_out.svg and figures/fig2_sensitivity.svg.
Colours are CSS variables with fallbacks, so the same file is theme-aware when
inlined in the report and renders in fixed light colours on its own.
"""
import json
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = json.load(open(os.path.join(ROOT, "data", "results.json"), encoding="utf-8"))
L = json.load(open(os.path.join(ROOT, "data", "likelihood_table.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

FONT = "Gentium Plus, Source Serif 4, Georgia, serif"
INK = "var(--ink,#1b2130)"
MUTED = "var(--muted,#55606f)"
RULE = "var(--rule,#c6cdd0)"
PAPER = "var(--paper,#f8f9f7)"
BLUE = "var(--viz-blue,#2a78d6)"
RED = "var(--viz-red,#e34948)"
GREY = "var(--bar-track,#d5dde1)"

SHORT = {
    "E01": "Feminine endings on the throne name",
    "E02": "Neferneferuaten is Nefertiti's own name",
    "E03": "Epithets tying her to Akhenaten and to a husband",
    "E04": "Double cartouche on stela UC 410",
    "E05": "Paired-ruler scenes: a woman in the blue crown",
    "E06": "Box Carter 1k: three names in one protocol",
    "E07": "Meryre II's tomb: Smenkhkare with Meritaten",
    "E08": "Jar Carter 405: Akhenaten's names with Smenkhkare's",
    "E09": "Plain throne name only with Smenkhkare",
    "E10": "Pairi graffito: her year 3 in a temple of Amun",
    "E11": "Amarna jar dockets: years 1 to 3 after year 17",
    "E12": "Manetho: \"his daughter Akencheres\"",
    "E13": "Nefertiti's shabti with queenly titles only",
    "E14": "Masculine references beside her names",
    "E15": "Age of the daughter Neferneferuaten-tasherit",
    "E16": "Dayr Abu Hinnis: Nefertiti still queen in year 16",
    "E17": "Her burial outfit reused for Tutankhamun",
    "E18": "Two rulers sharing one throne name",
    "K01": "Age at death of the KV55 body",
    "K02": "Inscriptions in KV55",
    "K03": "The 2010 DNA pedigree",
    "K04": "Tutankhaten as \"King's Son\"",
    "D01": "The name Nibhururiya",
    "D02": "The Armaa synchronism",
    "D03": "Season of the king's death",
    "D04": "The widow's plea",
    "D05": "Lupakki's raid on Amka",
    "D06": "Hittite relative chronology",
    "D07": "The plea against the Egyptian succession",
    "D08": "\"A son he has not\"",
}
GROUPS = [("E", "Egyptian evidence"), ("K", "The KV55 body"), ("D", "The Hittite texts")]


def pct(v):
    return f"{v * 100:.0f}"


def fig1():
    base = R["base"]["identity"]["Nefertiti"] * 100
    loo = R["leave_one_out"]
    codes = [it["code"] for it in L]
    W = 760
    left, right = 318, 742
    x_lo, x_hi = 60, 100
    top = 76
    row = 21
    gap_group = 22
    bar_h = 13
    lbl_size = 12

    def X(v):
        return left + (v - x_lo) / (x_hi - x_lo) * (right - left)

    rows = []
    y = top
    for pre, name in GROUPS:
        rows.append(("group", name, y))
        y += gap_group
        for c in codes:
            if c.startswith(pre):
                rows.append(("item", c, y))
                y += row
        y += 6
    H = y + 30

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
             f'aria-label="The Nefertiti figure with each of the 30 scored items removed in turn" '
             f'font-family="{FONT}" font-size="{lbl_size}" style="max-width:100%;height:auto">')
    s.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    s.append(f'<text x="0" y="18" font-size="14" font-weight="700" fill="{INK}">What removing each piece of evidence does to the Nefertiti figure</text>')
    s.append(f'<text x="0" y="36" font-size="11.5" fill="{MUTED}">Each bar runs from the figure with every item counted ({base:.0f}%) to the figure with that one item left out.</text>')
    # legend
    s.append(f'<rect x="0" y="45" width="12" height="9" rx="2" fill="{BLUE}"/>'
             f'<text x="16" y="53" font-size="11.5" fill="{MUTED}">to the left: the item supports the identification</text>')
    s.append(f'<rect x="318" y="45" width="12" height="9" rx="2" fill="{RED}"/>'
             f'<text x="334" y="53" font-size="11.5" fill="{MUTED}">to the right: the item weighs against it</text>')
    # gridlines and ticks
    for v in range(x_lo, x_hi + 1, 10):
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{H - 26}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{H - 12}" text-anchor="middle" font-size="11" fill="{MUTED}" style="font-variant-numeric:tabular-nums">{v}%</text>')
    xb = X(base)
    s.append(f'<line x1="{xb:.1f}" y1="{top - 8}" x2="{xb:.1f}" y2="{H - 26}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<text x="{xb:.1f}" y="{top - 12}" text-anchor="middle" font-size="11" fill="{INK}">{base:.0f}% with every item</text>')
    for kind, key, yy in rows:
        if kind == "group":
            s.append(f'<text x="0" y="{yy + 12}" font-size="11" font-weight="700" letter-spacing=".04em" fill="{MUTED}">{escape(key.upper())}</text>')
            continue
        c = key
        v = loo[c]["P_Nefertiti"] * 100
        title = loo[c]["title"]
        label = SHORT[c]
        cy = yy + row / 2
        s.append(f'<g><title>{escape(c)}. {escape(title)}. Without this item the Nefertiti figure is {v:.1f}% (with every item {base:.1f}%).</title>')
        s.append(f'<text x="0" y="{cy + 4:.1f}" fill="{INK}"><tspan fill="{MUTED}" style="font-variant-numeric:tabular-nums">{c}</tspan>  {escape(label)}</text>')
        xv = X(v)
        d = v - base
        if abs(d) >= 0.05:
            x0, x1 = sorted([xb, xv])
            w = max(x1 - x0, 1.5)
            col = BLUE if d < 0 else RED
            r = 4 if w > 8 else 0
            yb = cy - bar_h / 2
            if d < 0:  # bar grows leftward from the baseline; rounded at the left (data) end
                path = (f'M{x1:.1f},{yb:.1f} H{x0 + r:.1f} a{r},{r} 0 0 0 -{r},{r} V{yb + bar_h - r:.1f} '
                        f'a{r},{r} 0 0 0 {r},{r} H{x1:.1f} Z')
            else:
                path = (f'M{x0:.1f},{yb:.1f} H{x1 - r:.1f} a{r},{r} 0 0 1 {r},{r} V{yb + bar_h - r:.1f} '
                        f'a{r},{r} 0 0 1 -{r},{r} H{x0:.1f} Z')
            s.append(f'<path d="{path}" fill="{col}"/>')
            if abs(d) >= 2:
                tx = xv - 5 if d < 0 else xv + 5
                anchor = "end" if d < 0 else "start"
                s.append(f'<text x="{tx:.1f}" y="{cy + 4:.1f}" text-anchor="{anchor}" font-size="11" fill="{INK}" style="font-variant-numeric:tabular-nums">{v:.0f}</text>')
        else:
            s.append(f'<circle cx="{xb:.1f}" cy="{cy:.1f}" r="2.2" fill="{MUTED}"/>')
        s.append('</g>')
    s.append('</svg>')
    open(os.path.join(OUT, "fig1_leave_one_out.svg"), "w", encoding="utf-8").write("\n".join(s))
    return H


def fig2():
    runs = [("base", "reading adopted here"), ("sceptical", "sceptical reading"), ("generous", "generous reading"),
            ("prior_one_person_half", "one-person weights"), ("prior_literature", "named-view weights")]
    rows = [
        ("Neferneferuaten was Nefertiti", lambda r: r["identity"].get("Nefertiti", 0)),
        ("Smenkhkare a separate king", lambda r: r["separate_smenkhkare"]),
        ("Smenkhkare reigned before her", lambda r: r["smenkhkare_before"]),
        ("She was made king while Akhenaten lived", lambda r: r["coregency"].get("yes", 0)),
        ("The KV55 body is Smenkhkare", lambda r: r["kv55"].get("Smenkhkare", 0)),
        ("Nibhururiya was Akhenaten", lambda r: r["nibhururiya"].get("Akhenaten", 0)),
    ]
    W = 760
    left, right = 300, 742
    top = 84
    row = 40
    H = top + row * len(rows) + 34

    def X(v):
        return left + v / 100 * (right - left)

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
             f'aria-label="The six main answers under other readings and other starting weights" '
             f'font-family="{FONT}" font-size="12" style="max-width:100%;height:auto">')
    s.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    s.append(f'<text x="0" y="18" font-size="14" font-weight="700" fill="{INK}">How far each answer moves when the evidence is weighed differently</text>')
    s.append(f'<text x="0" y="36" font-size="11.5" fill="{MUTED}">Percentages from the scoring in section 4; the grey bar spans the sceptical and the generous readings.</text>')
    # legend
    lx = 0
    s.append(f'<circle cx="{lx + 5}" cy="52" r="4.5" fill="{BLUE}"/><text x="{lx + 14}" y="56" font-size="11.5" fill="{MUTED}">reading adopted here</text>')
    s.append(f'<rect x="150" y="48" width="22" height="8" rx="2" fill="{GREY}"/><text x="177" y="56" font-size="11.5" fill="{MUTED}">from the sceptical to the generous reading</text>')
    s.append(f'<circle cx="430" cy="52" r="4" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.5"/><text x="440" y="56" font-size="11.5" fill="{MUTED}">other starting weights (one-person; named views)</text>')
    for v in range(0, 101, 25):
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{H - 26}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{H - 12}" text-anchor="middle" font-size="11" fill="{MUTED}" style="font-variant-numeric:tabular-nums">{v}%</text>')
    for i, (lab, fn) in enumerate(rows):
        cy = top + row * i + row / 2
        vals = {k: fn(R[k]) * 100 for k, _ in runs}
        lo, hi = vals["sceptical"], vals["generous"]
        a, b = sorted([lo, hi])
        tip = "; ".join(f"{name} {vals[k]:.0f}%" for k, name in runs)
        s.append(f'<g><title>{escape(lab)}: {escape(tip)}.</title>')
        s.append(f'<text x="0" y="{cy + 4:.1f}" fill="{INK}">{escape(lab)}</text>')
        s.append(f'<rect x="{X(a):.1f}" y="{cy - 4:.1f}" width="{max(X(b) - X(a), 2):.1f}" height="8" rx="4" fill="{GREY}"/>')
        # range end labels
        s.append(f'<text x="{X(a) - 6:.1f}" y="{cy + 4:.1f}" text-anchor="end" font-size="11" fill="{MUTED}" style="font-variant-numeric:tabular-nums">{a:.0f}</text>')
        s.append(f'<text x="{X(b) + 6:.1f}" y="{cy + 4:.1f}" text-anchor="start" font-size="11" fill="{MUTED}" style="font-variant-numeric:tabular-nums">{b:.0f}</text>')
        for k in ("prior_one_person_half", "prior_literature"):
            s.append(f'<circle cx="{X(vals[k]):.1f}" cy="{cy:.1f}" r="4" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.5"/>')
        s.append(f'<circle cx="{X(vals["base"]):.1f}" cy="{cy:.1f}" r="7" fill="{PAPER}"/>')
        s.append(f'<circle cx="{X(vals["base"]):.1f}" cy="{cy:.1f}" r="5" fill="{BLUE}"/>')
        s.append(f'<text x="{X(vals["base"]):.1f}" y="{cy - 9:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="{INK}" style="font-variant-numeric:tabular-nums">{vals["base"]:.0f}</text>')
        s.append('</g>')
    s.append('</svg>')
    open(os.path.join(OUT, "fig2_sensitivity.svg"), "w", encoding="utf-8").write("\n".join(s))
    return H


if __name__ == "__main__":
    h1 = fig1()
    h2 = fig2()
    print(f"figures written: fig1 {h1}px high, fig2 {h2}px high, in {OUT}")
