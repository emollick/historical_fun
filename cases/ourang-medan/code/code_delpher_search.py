#!/usr/bin/env python3
"""Reproducible Delpher (KB) SRU search used for the Ourang Medan investigation.
Usage: python3 code_delpher_search.py '"ourang medan"' [collection]
Collections: DDD_artikel (newspaper articles, default), ANP (radio bulletins).
Prints date | title | paper | OCR url for every hit, and can dump OCR text.
"""
import sys, re, html, urllib.request, urllib.parse

def sru(query, collection="DDD_artikel", start=1, max_records=50):
    url = ("https://jsru.kb.nl/sru/sru?operation=searchRetrieve&recordSchema=ddd"
           f"&x-collection={collection}&startRecord={start}&maximumRecords={max_records}"
           f"&query={urllib.parse.quote(query)}")
    with urllib.request.urlopen(url, timeout=60) as r:
        x = r.read().decode("utf-8", "replace")
    n = int(re.search(r"<srw:numberOfRecords>(\d+)", x).group(1))
    recs = []
    for m in re.finditer(r"<srw:record>(.*?)</srw:record>", x, re.S):
        r = m.group(1)
        g = lambda t: (re.search(rf"<{t}[^>]*>(.*?)</{t}>", r, re.S) or [None, ""])[1].strip()
        recs.append(dict(date=g("dc:date")[:10], title=html.unescape(g("dc:title")),
                         paper=html.unescape(g("ddd:papertitle")), ocr=g("dc:identifier")))
    return n, recs

def ocr_text(ocr_url):
    with urllib.request.urlopen(ocr_url, timeout=60) as r:
        x = r.read().decode("utf-8", "replace")
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).strip()

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else '"ourang medan"'
    coll = sys.argv[2] if len(sys.argv) > 2 else "DDD_artikel"
    n, recs = sru(q, coll)
    print(f"{n} records for {q!r} in {coll}")
    for r in sorted(recs, key=lambda r: r["date"]):
        print(f'{r["date"]} | {r["paper"][:45]} | {r["title"][:70]} | {r["ocr"]}')
