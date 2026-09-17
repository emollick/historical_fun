#!/usr/bin/env python3
"""Query KB SRU DTS_document (magazines) and print compact list. Usage: sru_dts.py '<cql>' [max] [start]"""
import sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET, ssl, os
q = sys.argv[1]; mx = sys.argv[2] if len(sys.argv) > 2 else "50"; start = sys.argv[3] if len(sys.argv) > 3 else "1"
url = ("https://jsru.kb.nl/sru/sru?query=" + urllib.parse.quote(q) + "&operation=searchRetrieve&x-collection=DTS_document&maximumRecords=" + mx + "&startRecord=" + start + "&recordSchema=dcx")
ctx = ssl.create_default_context()
proxy = os.environ.get("HTTPS_PROXY")
handlers = [urllib.request.HTTPSHandler(context=ctx)]
if proxy: handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
data = urllib.request.build_opener(*handlers).open(url, timeout=120).read()
ns = {"srw": "http://www.loc.gov/zing/srw/", "dc": "http://purl.org/dc/elements/1.1/", "dcx": "http://krait.kb.nl/coop/tel/handbook/telterms.html", "dcterms": "http://purl.org/dc/terms/"}
root = ET.fromstring(data)
print("QUERY:", q, "| DTS_document | numberOfRecords:", root.findtext("srw:numberOfRecords", namespaces=ns))
for rec in root.findall(".//srw:record", ns):
    d = rec.find(".//srw:recordData", ns)
    print(" ", (d.findtext("dc:date", namespaces=ns) or ""), "|", (d.findtext("dc:title", namespaces=ns) or "").strip()[:60], "|", (d.findtext("dcx:recordIdentifier", namespaces=ns) or ""), "|", (d.findtext("dc:identifier", namespaces=ns) or ""), "| vol", (d.findtext("dcx:volumeNumber", namespaces=ns) or ""), "| ext", (d.findtext("dcterms:extent", namespaces=ns) or ""))
