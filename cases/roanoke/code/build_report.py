"""
Assemble report.html from report-src/*.html in name order.

- {{TOKEN}} placeholders are replaced from data/tokens.json (written by the model scripts).
- <h2> headings in sections after the header are numbered automatically.
- The table of contents is generated from the numbered <h2> ids.
Run: python3 code/build_report.py   (from the roanoke directory or anywhere)
"""
import json, os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "report-src")
OUT = os.path.join(ROOT, "report.html")
TOK = os.path.join(ROOT, "data", "tokens.json")

tokens = {}
if os.path.exists(TOK):
    tokens = json.load(open(TOK))
# inline SVG figures as FIG_<NAME> tokens (report-src/figs/fig_<name>.svg -> {{FIG_<NAME>}})
for f in glob.glob(os.path.join(SRC, "figs", "fig_*.svg")):
    key = "FIG_" + os.path.basename(f)[4:-4].upper()
    svg = open(f, encoding="utf-8").read()
    # drop any provenance metadata block and namespace the environment may have added
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S).replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")
    tokens[key] = svg

parts = sorted(glob.glob(os.path.join(SRC, "*.html")))
html = "".join(open(p, encoding="utf-8").read() for p in parts)

# number the h2s (skip any h2 with class="nonum")
n = 0
toc = []
def repl(m):
    global n
    attrs, inner = m.group(1), m.group(2)
    if 'nonum' in attrs:
        return m.group(0)
    n += 1
    idm = re.search(r'id="([^"]+)"', attrs)
    sid = idm.group(1) if idm else f"s{n}"
    toc.append((n, sid, re.sub(r"<[^>]+>", "", inner)))
    return f'<h2{attrs}>{n}. {inner}</h2>'
html = re.sub(r'<h2([^>]*)>(.*?)</h2>', repl, html, flags=re.S)

toc_html = "\n".join(f'<a href="#{sid}">{k}. {title}</a>' for k, sid, title in toc)
html = html.replace("{{TOC}}", toc_html)

missing = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)) - set(tokens)
for k, v in tokens.items():
    html = html.replace("{{" + k + "}}", str(v))
if missing:
    print("WARNING: unfilled tokens:", sorted(missing), file=sys.stderr)

open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {OUT}: {len(html)} bytes, {n} numbered sections, {len(missing)} unfilled tokens")
