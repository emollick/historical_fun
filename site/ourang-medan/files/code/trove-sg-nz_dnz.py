#!/usr/bin/env python3
"""Query DigitalNZ public API (no key) for Papers Past records. Usage: dnz.py "text" [year] [per_page]"""
import sys, json, urllib.parse, urllib.request, os, ssl
text = sys.argv[1]
year = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] not in ("-", "") else None
per_page = int(sys.argv[3]) if len(sys.argv) > 3 else 50
params = [("text", text), ("and[primary_collection][]", "Papers Past"), ("per_page", str(per_page)),
          ("fields", "id,title,date,display_date,publisher,landing_url,source_url,fulltext,description,collection_title")]
if year:
    for y in year.split(","):
        params.append(("and[year][]", y))
url = "https://api.digitalnz.org/records.json?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
data = json.load(urllib.request.urlopen(req, timeout=60))
s = data["search"]
print(f"QUERY: {text!r} year={year} -> result_count={s['result_count']}")
for r in s["results"]:
    print(f"--- [{r.get('display_date') or r.get('date')}] {r.get('publisher')} | {r.get('title')} | {r.get('landing_url')}")
    ft = r.get("fulltext") or r.get("description") or ""
    if isinstance(ft, list): ft = " ".join(ft)
    print("    " + ft[:600].replace("\n", " "))
