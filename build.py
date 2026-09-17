#!/usr/bin/env python3
"""Build the static site in site/ from cases/ and content/cases.py.

    python3 build.py            # writes site/ for the live site: reviewed cases only
    python3 build.py --dry-run  # prints what would be mirrored, writes nothing

Each case gets: site/<slug>/index.html (the case page), site/<slug>/report.html (the thread's
report as published, wrapped in a full HTML document, with the figures it references copied
beside it), and site/<slug>/files/ (the working folder mirrored, minus raw downloads and files
over the size cap, with an index page). The headline page is site/index.html.
"""
import fnmatch, html, json, os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "content"))
from cases import CASES, SITE as META, DATE, REPO_URL  # noqa: E402

SIZE_CAP = 2_000_000            # bytes; larger files stay in the repository only

def left_out_by_case():
    """Source files kept out of the public repository (copies of works still in copyright), from sources_left_out.csv:
    {slug: [(path inside the case, what it was, where it came from), ...]}."""
    import csv
    out = {}
    listing = ROOT / "sources_left_out.csv"
    if listing.exists():
        with listing.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                _, slug, rel = row["path"].split("/", 2)
                out.setdefault(slug, []).append((rel, row["what"], row["source"]))
    return out
LEFT_OUT = left_out_by_case()
GLOBAL_EXCLUDE = ["__pycache__", "*.pyc", ".DS_Store"]
FONTS = ("https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;1,400;1,500"
         "&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap")
def visible_cases():
    """Every case in content/cases.py, in order."""
    return list(CASES)


KIND_WORD = {"confirms": "Agrees with", "shifts": "Shifts", "overturns": "Overturns", "pending": "Not yet decided"}
STANDING_WORD = {"persuasive": "Strong", "argued": "Probable", "ranked": "Leading candidate", "open": "Unsettled"}
NUMBER_WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
               11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
               18: "eighteen", 19: "nineteen", 20: "twenty"}
DRY = "--dry-run" in sys.argv

esc = html.escape


def fmt_size(n):
    if n < 1024: return f"{n} B"
    if n < 1024 * 1024: return f"{n/1024:.0f} KB"
    return f"{n/1024/1024:.1f} MB"


def fmt_pct(p):
    if p is None: return ""
    if isinstance(p, float) and not p.is_integer():
        return f"{p:g}%"
    return f"{int(p)}%"


def head(title, depth, description=""):
    rel = "../" * depth
    desc = f'\n<meta name="description" content="{esc(description)}">' if description else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>{desc}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}assets/site.css">
</head>
<body>
<div class="wrap">
<nav class="topbar"><a href="{rel}">{esc(META['title'])}</a><span class="date">{esc(DATE)}</span></nav>
"""


def tail():
    return "\n</div>\n</body>\n</html>\n"


def meter(pct, label, caption=""):
    cap = f'<span class="caption">{esc(caption)}</span>' if caption else ""
    return (f'<div class="conf"><span class="num">{esc(label)}</span>'
            f'<div class="meter" role="img" aria-label="{esc(label)}"><span style="width:{pct}%"></span></div>{cap}</div>')


def badge(change):
    kind = change["kind"]
    return f'<span class="badge badge-{kind}">{KIND_WORD[kind]}</span>'


def change_line(change):
    q = f'<span class="qual">{esc(change["qualifier"])}</span>' if change.get("qualifier") else ""
    return f'<div class="change-line">{badge(change)}{q}</div>'


def opening(case, cls=""):
    """What happened, why it is a mystery, and how it was judged, stated before anything else."""
    out = ""
    for key, label in (("story", "What happened."), ("mystery", "Why it is a mystery."), ("judged", "How it was judged.")):
        if case.get(key): out += f'<p class="opening {key}{cls}"><strong>{label}</strong> {esc(case[key])}</p>'
    if not case.get("story") and case.get("argument"):   # entries not yet rewritten to the three-part opening
        out += f'<p class="opening argument{cls}"><strong>The argument.</strong> {esc(case["argument"])}</p>'
    return out


def standing_chip(case, note=True):
    st = case.get("standing")
    if not st: return ""
    out = f'<span class="standing s-{st["kind"]}">{STANDING_WORD[st["kind"]]}</span>'
    if note and st.get("note"):
        out += f'<p class="standing-note">{esc(st["note"])}</p>'
    return f'<div class="standing-wrap">{out}</div>'


def split_rows(case):
    if not case["split"]: return ""
    rows = []
    for row in case["split"]:
        lab, pct = row[0], row[1]
        disp = row[2] if len(row) > 2 else fmt_pct(pct)   # a third item shows a range in place of the bar's number
        width = min(100, max(0, float(pct)))
        rows.append(f'<div class="split-row"><span class="lab">{esc(lab)}</span><span class="num">{esc(disp)}</span>'
                    f'<div class="bar" role="img" aria-label="{esc(lab)}: {esc(disp)}"><span style="width:{width}%"></span></div></div>')
    note = f'<p class="split-note">{esc(case["split_note"])}</p>' if case.get("split_note") else ""
    return f'<div class="split">{"".join(rows)}{note}</div>'


def bullets(items, cls="bullets"):
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


# ----------------------------------------------------------------------------- reports
HEADISH = re.compile(r'\s*(<!--.*?-->|<title>.*?</title>|<meta[^>]*>|<link[^>]*>|<style[^>]*>.*?</style>)', re.S)
RELREF = re.compile(r'(?:src|href)="([^"#:]+)"')


def wrap_report(case, src_text, kind="Full report", up=0):
    """Turn the artifact-style fragment (title/link/style then body markup) into a full document."""
    i = 0
    while True:
        m = HEADISH.match(src_text, i)
        if not m: break
        i = m.end()
    head_part, body_part = src_text[:i], src_text[i:]
    title = re.search(r"<title>(.*?)</title>", head_part, re.S)
    title = title.group(1) if title else case["report_title"]
    nav = (f'<div id="mm-nav" style="font:14px/1.4 system-ui,-apple-system,\'Segoe UI\',sans-serif;padding:9px 16px;'
           f'background:#1B2026;color:#E6E8E3;display:flex;flex-wrap:wrap;gap:6px 22px">'
           f'<a href="{"../" * up or "./"}" style="color:#E6E8E3;text-decoration:none">&larr; Case page: {esc(case["title"])}</a>'
           f'<a href="{"../" * (up + 1)}" style="color:#E6E8E3;text-decoration:none">{esc(META["title"])}</a>'
           f'<span style="opacity:.7">{esc(kind)} · {esc(DATE)}</span>'
           f'<span style="opacity:.7;flex-basis:100%">{esc(META["byline"])}</span></div>\n')
    return (f"<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<style>html{{color-scheme:light dark}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>\n"
            f"{head_part.strip()}\n</head>\n<body>\n{nav}{body_part.strip()}\n</body>\n</html>\n")


def onsite_targets():
    """Each report page published off-site, mapped to the path of its copy on this site."""
    t = {}
    for c in visible_cases():
        if c.get("artifact"):
            t[c["artifact"]] = f'{c["slug"]}/report.html'
        for extra in c.get("extra_reports", []):
            if extra.get("artifact"):
                t[extra["artifact"]] = f'{c["slug"]}/{extra["out"]}/'
    return t


def onsite_links(text, out):
    """A link to a report's page off-site is pointed at the copy served here (nothing a page links to lives behind a login).
    A bare address in running text becomes a link reading "on this site"."""
    for url, target in onsite_targets().items():
        if url not in text:
            continue
        rel = os.path.relpath(SITE / target, out).replace(os.sep, "/") + ("/" if target.endswith("/") else "")
        text = text.replace(f'href="{url}"', f'href="{rel}"')
        text = text.replace(f'>{url}</a>', '>on this site</a>')
        text = re.sub(re.escape(url) + r'(?![\w/-])', f'<a href="{rel}">on this site</a>', text)
    return text


def copy_report(case, out, src_rel=None, kind="Full report", up=0):
    """Copy the case's report (or, with src_rel, another report kept in its folder, written as <out>/index.html)."""
    src = CASES_DIR / case["slug"] / (src_rel or case["report_src"])
    text = src.read_text(encoding="utf-8")
    # a diagram written as mermaid source renders only where a mermaid script runs; the same diagram, drawn once
    # from that source, is kept under templates/mermaid/<slug>-<n>.svg and put in its place
    blocks = list(re.finditer(r'<pre class="mermaid">.*?</pre>', text, re.S))
    for n, m in reversed(list(enumerate(blocks, 1))):
        drawn = ROOT / "templates" / "mermaid" / f"{case['slug']}-{n}.svg"
        if drawn.is_file():
            text = text[:m.start()] + '<div class="mermaid-drawn">' + drawn.read_text(encoding="utf-8") + '</div>' + text[m.end():]
    src_text = text  # the files the report references are read from the text as written, before any link is pointed on-site
    text = onsite_links(text, out)
    if not DRY:
        out.mkdir(parents=True, exist_ok=True)
        (out / ("index.html" if src_rel else "report.html")).write_text(wrap_report(case, text, kind, up), encoding="utf-8")
    # copy the files the report references relatively (figures, data links)
    copied = []
    for ref in sorted(set(RELREF.findall(src_text))):
        if ref.startswith(("http", "mailto", "data:", "/")): continue
        p = src.parent / ref
        if p.is_file():
            dest = out / ref
            if not DRY:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
            copied.append(ref)
    # copy the image files the case page's own figures use (a path relative to the report's folder, or to the case folder)
    for fig in (case.get("figures") or []) if src_rel is None else []:
        ref = fig.get("src")
        if not ref or ref.startswith(("http", "data:", "/")): continue
        for base in (src.parent, CASES_DIR / case["slug"]):
            p = base / ref
            if p.is_file():
                dest = out / ref
                if not DRY:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dest)
                if ref not in copied: copied.append(ref)
                break
    return copied


# ----------------------------------------------------------------------------- files mirror
def excluded_by(rel, size, case):
    parts = rel.split("/")
    for pat in GLOBAL_EXCLUDE:
        if any(fnmatch.fnmatch(p, pat) for p in parts): return "cache or system file"
    if any(fnmatch.fnmatch(rel, pat) for pat in case.get("site_keep", [])): pass
    elif any(fnmatch.fnmatch(rel, pat) for pat in case.get("site_exclude", [])): return "raw download"
    if size > SIZE_CAP: return f"over the {SIZE_CAP/1e6:.0f} MB cap"
    return ""


def mirror_files(case, out):
    base = CASES_DIR / case["slug"]
    inc, exc = [], []
    if not base.exists(): return inc, exc
    for dp, dns, fns in os.walk(base):
        dns.sort(); fns.sort()
        for fn in fns:
            p = Path(dp) / fn
            rel = p.relative_to(base).as_posix()
            size = p.stat().st_size
            why = excluded_by(rel, size, case)
            if why == "cache or system file": continue
            if why:
                exc.append((rel, size, why)); continue
            inc.append((rel, size))
            if not DRY:
                dest = out / "files" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
    return inc, exc


def files_page(case, inc, exc):
    slug = case["slug"]
    total = sum(s for _, s in inc); etotal = sum(s for _, s, _ in exc)
    groups = {}
    for rel, size in inc:
        top = rel.split("/")[0] if "/" in rel else "(top level)"
        groups.setdefault(top, []).append((rel, size))
    h = [head(f"Working files: {case['title']}", 2, f"Code, data and notes behind the {case['title']} report")]
    h.append(f'<nav class="crumb"><a href="../../">{esc(META["title"])}</a> › <a href="../">{esc(case["title"])}</a> › Working files</nav>')
    h.append(f'<header class="case-head"><p class="eyebrow">Working files</p><h1>{esc(case["title"])}: working files</h1>')
    h.append(f'<p class="files-summary">{len(inc)} files ({fmt_size(total)}) from the working folder behind this case.'
             + (f' {len(exc)} files ({fmt_size(etotal)}) are not included here; they are listed at the end.' if exc else '')
             + ' The README in the folder explains the layout and how to re-run the code.</p>'
             + (f'<p class="files-summary">{len(LEFT_OUT[slug])} further files from this folder, copies of published sources still in copyright, '
                f'are not in the public repository. <a href="../../sources-left-out/#{esc(slug)}">The list of sources left out</a> says what each was and where to obtain it.</p>'
                if LEFT_OUT.get(slug) else '')
             + '</header>')
    for top, items in groups.items():
        h.append(f'<section class="files-group"><h2>{esc(top)}/</h2><div class="table-wrap"><table class="files">')
        for rel, size in items:
            h.append(f'<tr><td><a href="{esc(rel)}">{esc(rel)}</a></td><td class="size">{fmt_size(size)}</td></tr>')
        h.append('</table></div></section>')
    if exc:
        reasons = case.get("exclude_reason", {})
        h.append('<section class="files-group"><h2>Not included here</h2>')
        if reasons:
            h.append('<p class="files-summary">' + " ".join(f"<code>{esc(k)}/</code>: {esc(v)}." for k, v in reasons.items()) + '</p>')
        h.append('<ul class="excluded">')
        for rel, size, why in exc:
            h.append(f'<li><code>{esc(rel)}</code> · {fmt_size(size)} · {esc(why)}</li>')
        h.append('</ul></section>')
    h.append(tail())
    return "\n".join(h)


def left_out_page():
    """One page listing, case by case, the source files kept out of the public repository and where each came from."""
    n = sum(len(v) for v in LEFT_OUT.values())
    titles = {c["slug"]: c["title"] for c in visible_cases()}
    h = [head("Sources left out", 1, "Copies of published sources still in copyright that were used but are not republished, with their sources")]
    h.append(f'<nav class="crumb"><a href="../">{esc(META["title"])}</a> › Sources left out</nav>')
    h.append('<header class="case-head"><p class="eyebrow">Working files</p><h1>Sources left out of the public repository</h1>'
             '<p class="files-summary">The working folders behind the cases held copies of published sources that the research downloaded: '
             'scans, OCR text, web pages, articles, search excerpts. Copies of works still in copyright are not republished here or in the repository. '
             f'This page lists each such file ({n} across {len(LEFT_OUT)} cases), what it was and where it came from, so that anyone re-running the code can fetch the same material. '
             'Copies of works in the public domain, and of material under an open licence, stay in the working files under their own terms.</p></header>')
    for slug in sorted(LEFT_OUT, key=lambda s: titles.get(s, s)):
        if slug not in titles: continue
        items = LEFT_OUT[slug]
        h.append(f'<section class="files-group" id="{esc(slug)}"><h2>{esc(titles[slug])} <span class="count">({len(items)} files)</span> · '
                 f'<a href="../{esc(slug)}/files/">working files</a></h2><div class="table-wrap"><table class="files left-out">'
                 '<thead><tr><th>File</th><th>What it was</th><th>Source</th></tr></thead>')
        for rel, what, source in items:
            m = re.search(r'https?://\S+', source)
            if m:
                url = m.group(0).rstrip('.,;:)')
                label = source.replace(m.group(0), '').strip(' :;,()') or url
                src = f'{esc(label)} <a href="{esc(url)}">{esc(url)}</a>' if label != url else f'<a href="{esc(url)}">{esc(url)}</a>'
            else:
                src = esc(source)
            h.append(f'<tr><td class="path">{esc(rel)}</td><td>{esc(what)}</td><td>{src}</td></tr>')
        h.append('</table></div></section>')
    h.append(tail())
    return "\n".join(h)


# ----------------------------------------------------------------------------- pages
def case_page(case, inc, exc, report_refs):
    slug = case["slug"]; ch = case["change"]
    pending = case["status"] != "delivered"
    total = sum(s for _, s in inc)
    h = [head(case["title"], 1, case["question"])]
    h.append(f'<nav class="crumb"><a href="../">{esc(META["title"])}</a> › {esc(case["title"])}</nav>')
    h.append(f'<header class="case-head"><p class="eyebrow">{esc(case["period"])}</p><h1>{esc(case["title"])}</h1>'
             f'<p class="question">{esc(case["question"])}</p>' + opening(case) +
             f'<div class="meta"><span>Method: {esc(case["method"])}</span><span>{esc(DATE)}</span></div></header>')
    if pending:
        h.append('<section class="section"><h2>Status</h2>' + change_line(ch) +
                 f'<p class="progress measure" style="margin-top:14px">{esc(case.get("progress", ""))}</p>'
                 f'<p class="change-block prior" style="margin-top:16px"><strong>What historians have said.</strong> {esc(ch["prior"])}</p></section>')
    else:
        h.append('<section class="section"><h2>Verdict</h2><div class="two-col"><div>'
                 f'<p class="verdict-lead">{esc(case["verdict"])}</p>'
                 + meter(case["confidence"], case["confidence_label"]) .replace('<div class="conf">', '<div class="conf" style="margin-top:16px">')
                 + standing_chip(case)
                 + '<div class="verdict-detail">' + "".join(f"<p>{esc(p)}</p>" for p in case["verdict_detail"]) + '</div>'
                 + '</div><div>' + split_rows(case) + '</div></div></section>')
        h.append(done_block(case))
        h.append('<section class="section"><h2>What is new here</h2>' + bullets(case["new"]) +
                 (f'<p class="aside-note"><strong>Already established by others.</strong> {esc(case["confirms_prior"])}</p>' if case["confirms_prior"] else "") + '</section>')
        h.append('<section class="section change-block"><h2>Where this verdict stands among historians</h2>' + change_line(ch) +
                 f'<p class="prior"><strong>What historians have said.</strong> {esc(ch["prior"])}</p>'
                 f'<p class="expl">{esc(ch["explanation"])}</p></section>')
        h.append('<section class="section"><h2>What would overturn it</h2>' + bullets(case["overturn"], "bullets muted") + '</section>')
        h.append('<section class="section"><h2>Limits</h2>' + bullets(case["fell_short"], "bullets muted") + '</section>')
        h.append('<div class="cta"><a class="button" href="report.html">Read the full report</a>'
                 + "".join(f'<a class="button secondary" href="{esc(href)}">{esc(label)}</a>' for label, href in case.get("extra_links", []))
                 + f'<a class="button secondary" href="files/">Working files ({len(inc)} files, {fmt_size(total)})</a></div>')
    foot = ['<footer class="foot">', f'<p>{esc(META["byline"])}</p>']
    if not pending:
        foot.append(f'<p>The full report is reproduced here with its figures'
                    + (f' ({len(report_refs)} files)' if report_refs else '') + ', code, data and notes.</p>')
        foot.append('<p>Raw downloads and files over 2 MB are kept out of this site; the working-files page lists them.'
                    + (' Copies of sources still in copyright are not republished; <a href="../sources-left-out/#' + esc(slug) + '">a list</a> says where each came from.' if LEFT_OUT.get(slug) else '') + '</p>')
    else:
        foot.append('<p>This case is not finished. Its verdict, report and files will appear here when it is.</p>')
    foot.append('</footer>')
    h.append("".join(foot))
    h.append(tail())
    return "\n".join(h)


def strip_dark_css(css):
    """Drop the dark-theme rules from a figure's stylesheet: figures sit in a light box whatever the page theme."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: out.append(css[i:]); break
        prelude = css[i:j]
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{": depth += 1
            elif css[k] == "}": depth -= 1
            k += 1
        block = css[i:k]
        p = prelude.lower()
        dark = ("prefers-color-scheme" in p and "dark" in p) or ("data-theme" in p and "dark" in p)
        if not dark: out.append(block)
        i = k
    return "".join(out)

def figure_block(fig, n):
    """One figure lifted from the report: inline markup (svg or html) or an image file copied beside the report."""
    cap = fig.get("caption", "")
    if fig.get("html"):
        body = fig["html"]
        m = re.match(r'\s*<svg\b([^>]*)>', body)
        if m and "viewBox" not in m.group(1):
            # give a fixed-size svg a viewBox so that it scales down in a narrow column
            w = re.search(r'\bwidth="([\d.]+)(?:px)?"', m.group(1)); h = re.search(r'\bheight="([\d.]+)(?:px)?"', m.group(1))
            if w and h:
                body = body[:m.end(1)] + f' viewBox="0 0 {w.group(1)} {h.group(1)}"' + body[m.end(1):]
        body = f'<div class="figbody">{body}</div>'
    else:
        body = f'<img src="{esc(fig["src"])}" alt="{esc(fig.get("alt", cap))}" loading="lazy">'
    css = f'<style>{strip_dark_css(fig["css"])}</style>' if fig.get("css") else ""
    return f'<figure class="fig" id="fig-{n}">{css}{body}<figcaption>{esc(cap)}</figcaption></figure>'


def done_block(case):
    """What was done for this case, in plain words, with the figures the report made."""
    paras = case.get("done") or []
    figs = case.get("figures") or []
    if not paras and not figs: return ""
    out = ['<section class="section done"><h2>What was done</h2>']
    out += [f'<p>{esc(p)}</p>' for p in paras]
    if figs:
        out.append('<div class="figures">' + "".join(figure_block(f, i + 1) for i, f in enumerate(figs)) + '</div>')
    out.append('</section>')
    return "".join(out)


def table_page_rows(cases, stats):
    rows = []
    for c in cases:
        slug = c["slug"]; ch = c["change"]; st = stats.get(slug, {})
        chip = ""
        mystery = c.get("mystery_short") or c["question"]
        thumb = ROOT / "templates" / "thumbs" / f"{slug}.png"
        cell_f = (f'<td class="tf"><a href="{esc(slug)}/#fig-{int(c.get("thumb", 0)) + 1}"><img src="assets/thumbs/{esc(slug)}.png" alt="" width="112" height="74" loading="lazy"></a></td>'
                  if thumb.is_file() else '<td class="tf"></td>')
        cell_m = (cell_f + f'<td class="tm-cell"><a class="tt" href="{esc(slug)}/">{esc(c["title"])}</a>{chip}'
                  f'<span class="tm">{esc(mystery)}</span></td>')
        if c["status"] == "delivered":
            verdict = c.get("verdict_short") or c["verdict"]
            conf = c.get("confidence_short") or (f'about {fmt_pct(c["confidence"])}' if c.get("confidence") is not None else "")
            hist = c.get("historians_short") or ch.get("qualifier", "")
            links = (f'<a href="{esc(slug)}/">Case page</a><a href="{esc(slug)}/report.html">Full report</a>'
                     + "".join(f'<a href="{esc(href if href.startswith("http") else slug + "/" + href)}">{esc(label)}</a>' for label, href in c.get("extra_links", []))
                     + f'<a href="{esc(slug)}/files/">Files ({st.get("n", 0)})</a>')
            rows.append(f'<tr id="{esc(slug)}">{cell_m}<td class="tv">{esc(verdict)}</td><td class="tc num">{esc(conf)}</td>'
                        f'<td class="te">{standing_chip(c, note=False)}</td>'
                        f'<td class="th">{badge(ch)}<span class="hq">{esc(hist)}</span></td><td class="tl">{links}</td></tr>')
        else:
            rows.append(f'<tr id="{esc(slug)}">{cell_m}<td class="tv">{esc(c.get("progress", ""))}</td><td class="tc"></td><td class="te"></td>'
                        f'<td class="th">{badge(ch)}</td><td class="tl"><a href="{esc(slug)}/">Case page</a></td></tr>')
    return "".join(rows)


def index_page(stats):
    cases = visible_cases()
    delivered = [c for c in cases if c["status"] == "delivered"]
    kinds = {k: sum(1 for c in delivered if c["change"]["kind"] == k) for k in ("confirms", "shifts", "overturns")}
    pending = [c for c in cases if c["status"] != "delivered"]
    n_word = NUMBER_WORD.get(len(cases), str(len(cases))).capitalize()
    tagline = META["tagline"].replace("{n}", n_word)
    intro = [p.replace("{n}", n_word.lower()) for p in META["intro"]]
    h = [head(META["title"], 0, tagline)]
    h.append('<header class="masthead"><p class="eyebrow">Verdicts from the sources · ' + esc(DATE) + '</p>'
             f'<h1>{esc(META["title"])}</h1><p class="tagline">{esc(tagline)}</p>'
             '<div class="intro">' + "".join(f"<p>{esc(p)}</p>" for p in intro) + '</div>'
             f'<p class="byline">{esc(META["byline"])}</p>')
    over_names = ", ".join(c["title"] for c in delivered if c["change"]["kind"] == "overturns")
    plain_shifts = [c["title"] for c in delivered if c["change"]["kind"] == "shifts"]
    shifts_prov = any(c["change"].get("qualifier", "").lower().startswith("provisionally") for c in delivered if c["change"]["kind"] == "shifts")
    sk = {k: sum(1 for c in delivered if c.get("standing", {}).get("kind") == k) for k in ("persuasive", "argued", "ranked", "open")}
    d_word = NUMBER_WORD.get(len(delivered), str(len(delivered))).capitalize()
    shift_names = ", ".join(plain_shifts)
    def nw(n): return NUMBER_WORD.get(n, str(n))
    parts = []
    if sk["persuasive"]: parts.append(f'<b>{nw(sk["persuasive"])}</b> rest{"s" if sk["persuasive"] == 1 else ""} on strong evidence')
    if sk["argued"]: parts.append(f'<b>{nw(sk["argued"])}</b> {"is" if sk["argued"] == 1 else "are"} probable')
    if sk["ranked"]: parts.append(f'<b>{nw(sk["ranked"])}</b> {"has" if sk["ranked"] == 1 else "have"} a leading candidate')
    if sk["open"]: parts.append(f'<b>{nw(sk["open"])}</b> {"is" if sk["open"] == 1 else "are"} unsettled')
    ladder = (", ".join(parts[:-1]) + (" and " if len(parts) > 1 else "") + parts[-1]) if parts else ""
    tally = (f'Of the <b>{d_word.lower()}</b> cases' + (f' ({len(pending)} of them not yet finished)' if pending else '')
             + (f', {ladder}. ' if ladder else '. ')
             + f'<b>{nw(kinds["confirms"]).capitalize()}</b> agree with a position some historians already hold; '
             + (f'<b>{nw(len(plain_shifts))}</b> ({esc(shift_names)}) {"provisionally " if shifts_prov else ""}shift{"s" if len(plain_shifts) == 1 else ""} part of the accepted account; ' if plain_shifts
                else 'none shifts part of the accepted account; ')
             + (f'<b>{nw(kinds["overturns"])}</b> ({esc(over_names)}) overturn{"s" if kinds["overturns"] == 1 else ""} a prevailing view.' if kinds["overturns"]
                else 'none overturns a prevailing view.'))
    h.append(f'<p class="tally">{tally}</p></header>')
    h.append('<main><div class="table-wrap cases-wrap"><table class="cases-table">'
             '<thead><tr><th class="tf"></th><th>The mystery</th><th>Verdict</th><th>How sure</th><th>Evidence</th><th>Historians</th><th>Read</th></tr></thead>'
             '<tbody>' + table_page_rows(cases, stats) + '</tbody></table></div></main>')
    h.append('<section class="howto"><h2>How to read the table</h2>')
    h.append('<div class="legend" aria-label="How far the evidence supports each verdict">')
    for kind, word, text in META["standing_legend"]:
        h.append(f'<div class="item"><span class="standing s-{kind}">{esc(word)}</span><p>{esc(text)}</p></div>')
    h.append('</div>')
    h.append('<div class="legend" aria-label="Where this verdict stands among historians">')
    for kind, word, text in META["legend"]:
        h.append(f'<div class="item"><span class="badge badge-{kind}">{esc(word)}</span><p>{esc(text)}</p></div>')
    h.append(f'</div><p class="note">{esc(META["confidence_note"])}</p></section>')
    h.append('<section class="standard"><h2>What every case does</h2><ol>' +
             "".join(f"<li>{esc(s)}</li>" for s in META["standard"]) + '</ol></section>')
    h.append(f'<footer class="foot"><p>Each case page carries the full report with its figures, code, data and notes.</p>'
             f'<p>Raw downloads and files over 2 MB are kept out of this site; each case\'s working-files page lists them.'
             + (' Copies of sources still in copyright are not republished; <a href="sources-left-out/">a list</a> says where each came from.' if LEFT_OUT else '') + '</p></footer>')
    h.append(tail())
    return "\n".join(h)


# ----------------------------------------------------------------------------- main
def main():
    if not DRY:
        if SITE.exists(): shutil.rmtree(SITE)
        (SITE / "assets").mkdir(parents=True)
        shutil.copy2(ROOT / "templates" / "site.css", SITE / "assets" / "site.css")
        thumbs = ROOT / "templates" / "thumbs"
        if thumbs.is_dir():
            (SITE / "assets" / "thumbs").mkdir()
            for p in sorted(thumbs.glob("*.png")): shutil.copy2(p, SITE / "assets" / "thumbs" / p.name)
    stats = {}
    for case in visible_cases():
        slug = case["slug"]; out = SITE / slug
        if not DRY: out.mkdir(parents=True, exist_ok=True)
        refs = []
        if case["status"] == "delivered":
            refs = copy_report(case, out)
            # another report kept in the case folder (an independent check, say) is served under the case as <out>/
            for extra in case.get("extra_reports", []):
                refs += copy_report(case, out / extra["out"], src_rel=extra["src"], kind=extra.get("kind", "Independent check"), up=1)
        inc, exc = mirror_files(case, out)
        stats[slug] = {"n": len(inc), "bytes": sum(s for _, s in inc), "excluded": len(exc), "excluded_bytes": sum(s for _, s, _ in exc)}
        print(f"{slug:24s} report refs={len(refs):2d}  mirrored {len(inc):4d} files {fmt_size(stats[slug]['bytes']):>8s}"
              f"  repo-only {len(exc):3d} files {fmt_size(stats[slug]['excluded_bytes']):>8s}")
        if not DRY:
            (out / "index.html").write_text(case_page(case, inc, exc, refs), encoding="utf-8")
            if case["status"] == "delivered" or inc:
                (out / "files").mkdir(parents=True, exist_ok=True)
                (out / "files" / "index.html").write_text(files_page(case, inc, exc), encoding="utf-8")
    if not DRY:
        (SITE / "index.html").write_text(index_page(stats), encoding="utf-8")
        if LEFT_OUT:
            (SITE / "sources-left-out").mkdir(parents=True, exist_ok=True)
            (SITE / "sources-left-out" / "index.html").write_text(left_out_page(), encoding="utf-8")
        scoreboard = [{k: c.get(k) for k in ("slug", "title", "question", "status", "verdict", "confidence", "confidence_label",
                                              "standing", "split", "new", "confirms_prior", "change", "overturn", "fell_short", "story", "mystery", "judged")}
                      for c in visible_cases()]
        (SITE / "cases.json").write_text(json.dumps({"date": DATE, "cases": scoreboard}, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum(v["bytes"] for v in stats.values()); n = sum(v["n"] for v in stats.values())
    print(f"site mirror total: {n} files, {fmt_size(tot)}")


if __name__ == "__main__":
    main()
