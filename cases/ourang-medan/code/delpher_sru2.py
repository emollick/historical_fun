#!/usr/bin/env python3
"""Query KB SRU, page through up to N records, filter by year range client-side.
Usage: sru2.py '<cql>' [y1] [y2] [maxtotal]"""
import sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET, ssl, os
q = sys.argv[1]
y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
y2 = int(sys.argv[3]) if len(sys.argv) > 3 else 9999
cap = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
ctx = ssl.create_default_context()
proxy = os.environ.get("HTTPS_PROXY")
handlers = [urllib.request.HTTPSHandler(context=ctx)]
if proxy: handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
opener = urllib.request.build_opener(*handlers)
ns = {"srw": "http://www.loc.gov/zing/srw/", "dc": "http://purl.org/dc/elements/1.1/", "ddd": "http://www.kb.nl/ddd"}
start, total, shown = 1, None, 0
while True:
    url = ("https://jsru.kb.nl/sru/sru?query=" + urllib.parse.quote(q) + "&operation=searchRetrieve&x-collection=DDD_artikel&maximumRecords=50&startRecord=" + str(start) + "&recordSchema=ddd")
    root = ET.fromstring(opener.open(url, timeout=180).read())
    if total is None:
        total = int(root.findtext("srw:numberOfRecords", namespaces=ns) or 0)
        print(f"QUERY: {q} | total {total} | showing years {y1}-{y2}" + (f" (capped at {cap})" if total > cap else ""))
    recs = root.findall(".//srw:record", ns)
    if not recs: break
    for rec in recs:
        d = rec.find(".//srw:recordData", ns)
        date = (d.findtext("dc:date", namespaces=ns) or "")[:10]
        try: yr = int(date[:4])
        except: yr = 0
        if y1 <= yr <= y2:
            shown += 1
            print(f"  {date} | {(d.findtext('ddd:papertitle', namespaces=ns) or '').strip()[:60]} | p{(d.findtext('ddd:page', namespaces=ns) or '').strip()} | {(d.findtext('ddd:metadataKey', namespaces=ns) or '').strip()} | {(d.findtext('dc:title', namespaces=ns) or '').strip().replace(chr(10),' ')[:90]}")
    start += 50
    if start > total or start > cap: break
print(f"  -> {shown} in range")
