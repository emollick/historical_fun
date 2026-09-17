#!/usr/bin/env python3
"""Assemble the Dyatlov Pass report from styles.css and the HTML fragments in frags/.
Order is fixed below."""
import os, sys
R = os.path.dirname(os.path.abspath(__file__))
ORDER = ["masthead", "opening", "verdict", "facts", "forensic", "terrain", "model", "rivals", "reconstruction", "residue", "overturn", "new", "sources"]
css = open(os.path.join(R, "styles.css"), encoding="utf-8").read()
parts = []
missing = []
for name in ORDER:
    p = os.path.join(R, "frags", name + ".html")
    if os.path.exists(p):
        parts.append(f"<!-- {name} -->\n" + open(p, encoding="utf-8").read())
    else:
        missing.append(name)
html = f"""<title>Kholat Syakhl, 1–2 February 1959</title>
<meta name="description" content="Dyatlov Pass: the slab-avalanche model tested against the 1959 case file">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Sans+Narrow:wght@400;700&family=PT+Mono&display=swap">
<style>
{css}
</style>
<div class="wrap">
{chr(10).join(parts)}
</div>
"""
out = os.path.join(R, "dyatlov-pass-report.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", out, len(html), "bytes; missing fragments:", missing)
