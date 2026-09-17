#!/usr/bin/env python3
"""Query KB SRU and print compact result list. Usage: sru.py '<cql query>' [collection] [max] [start]"""
import sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET, ssl, os
q = sys.argv[1]
coll = sys.argv[2] if len(sys.argv) > 2 else "DDD_artikel"
mx = sys.argv[3] if len(sys.argv) > 3 else "50"
start = sys.argv[4] if len(sys.argv) > 4 else "1"
url = ("https://jsru.kb.nl/sru/sru?query=" + urllib.parse.quote(q) +
       "&operation=searchRetrieve&x-collection=" + coll + "&maximumRecords=" + mx +
       "&startRecord=" + start + "&recordSchema=ddd")
ctx = ssl.create_default_context()
proxy = os.environ.get("HTTPS_PROXY")
handlers = [urllib.request.HTTPSHandler(context=ctx)]
if proxy:
    handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
opener = urllib.request.build_opener(*handlers)
data = opener.open(url, timeout=120).read()
ns = {"srw": "http://www.loc.gov/zing/srw/", "dc": "http://purl.org/dc/elements/1.1/", "ddd": "http://www.kb.nl/ddd"}
root = ET.fromstring(data)
n = root.findtext("srw:numberOfRecords", namespaces=ns)
diag = root.find(".//{http://www.loc.gov/zing/srw/diagnostic/}message")
print("QUERY:", q, "| collection:", coll, "| numberOfRecords:", n, ("| DIAG: " + diag.text) if diag is not None else "")
for rec in root.findall(".//srw:record", ns):
    d = rec.find(".//srw:recordData", ns)
    date = (d.findtext("dc:date", namespaces=ns) or "")[:10]
    title = (d.findtext("dc:title", namespaces=ns) or "").strip().replace("\n", " ")
    paper = (d.findtext("ddd:papertitle", namespaces=ns) or "").strip()
    ident = (d.findtext("dc:identifier", namespaces=ns) or "").strip()
    key = (d.findtext("ddd:metadataKey", namespaces=ns) or "").strip()
    page = (d.findtext("ddd:page", namespaces=ns) or "").strip()
    src = (d.findtext("dc:source", namespaces=ns) or "").strip()
    print(f"{date} | {paper} | p{page} | {key} | {title[:90]} | {src[:40]}")
