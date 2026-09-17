#!/usr/bin/env python3
"""Fetch OCR text of a KB article. Usage: ocr.py <metadataKey e.g. ddd:010862872:mpeg21:a0050>"""
import sys, urllib.request, xml.etree.ElementTree as ET, ssl, os, re, html
key = sys.argv[1]
url = "https://resolver.kb.nl/resolve?urn=" + key + ":ocr"
ctx = ssl.create_default_context()
proxy = os.environ.get("HTTPS_PROXY")
handlers = [urllib.request.HTTPSHandler(context=ctx)]
if proxy:
    handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
opener = urllib.request.build_opener(*handlers)
data = opener.open(url, timeout=120).read().decode("utf-8", "replace")
# try XML parse
try:
    root = ET.fromstring(data.encode("utf-8"))
    parts = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag in ("title", "p") and el.text:
            parts.append(("## " if tag == "title" else "") + " ".join(el.text.split()))
    txt = "\n\n".join(parts)
except Exception as e:
    txt = re.sub(r"<[^>]+>", "\n", data)
    txt = html.unescape(txt)
print("DELPHER URL: https://www.delpher.nl/nl/kranten/view?identifier=" + key)
print("RESOLVER: " + url)
print()
print(txt)
