#!/usr/bin/env python3
"""Probe Founders Online ids (via Wayback) at intervals to map id -> date. Usage: fo_probe.py out.tsv prefix start end step [prefix start end step ...]"""
import sys, re, time, urllib.request
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
out = sys.argv[1]; args = sys.argv[2:]
seen=set()
try:
    for line in open(out, encoding='utf-8'): seen.add(line.split('\t')[0])
except FileNotFoundError: pass
f = open(out, 'a', encoding='utf-8')
while args:
    pre, a, b, step = args[0], int(args[1]), int(args[2]), int(args[3]); args = args[4:]
    for n in range(a, b+1, step):
        doc = f"{pre}-{n:04d}"
        if doc in seen: continue
        url = "https://web.archive.org/web/2024/https://founders.archives.gov/documents/" + doc
        title = ''
        for t in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                html = urllib.request.urlopen(req, timeout=60).read().decode('utf-8','ignore')
                m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
                title = re.sub(r"\s+", " ", m.group(1)).strip() if m else '(no title)'
                break
            except Exception as e:
                title = 'ERR ' + str(e)[:60]; time.sleep(5*(t+1))
        f.write(f"{doc}\t{title}\n"); f.flush(); time.sleep(2.5)
print('done')
