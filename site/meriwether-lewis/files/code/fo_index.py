#!/usr/bin/env python3
"""Build an index (id -> title) of Founders Online documents via Wayback captures.
Usage: python3 fo_index.py <series-prefix> <start> <end> <outfile>
  e.g. python3 fo_index.py Jefferson/03-01-02 470 560 ../data/fo_index_ret1.tsv
"""
import sys, re, time, urllib.request
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
pre, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
seen = set()
try:
    for line in open(out, encoding="utf-8"):
        seen.add(line.split("\t")[0])
except FileNotFoundError:
    pass
f = open(out, "a", encoding="utf-8")
for n in range(a, b + 1):
    doc = f"{pre}-{n:04d}"
    if doc in seen:
        continue
    url = "https://web.archive.org/web/2024/https://founders.archives.gov/documents/" + doc
    title = ""
    for t in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
            m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no title)"
            break
        except Exception as e:
            title = "ERR " + str(e)[:60]
            time.sleep(3 * (t + 1))
    f.write(f"{doc}\t{title}\n"); f.flush()
    time.sleep(0.7)
print("done", out)
