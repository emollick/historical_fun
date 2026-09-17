#!/usr/bin/env python3
"""Turn a wbfetch.py Founders Online text dump into a sources/ file with a citation header.
Usage: fo_source.py <dump.txt> <out.md> [extra note]"""
import sys, re, datetime
dump, out = sys.argv[1], sys.argv[2]
note = sys.argv[3] if len(sys.argv) > 3 else ''
t = open(dump, encoding='utf-8').read()
cap = re.search(r'SOURCE CAPTURE: (\S+)', t).group(1)
orig = re.search(r'ORIGINAL URL: (\S+)', t).group(1)
cite = re.search(r'Cite as (.*?)\]', t, flags=re.S)
cite = re.sub(r'\s+', ' ', cite.group(1)).strip() + ']' if cite else '(citation block not captured)'
title = re.search(r'\nPermanent Link \nview \n(.*?)\n', t)
title = title.group(1).strip() if title else ''
body = t.split('\n', 3)[3] if t.count('\n') >= 3 else t
# drop leading chrome lines
body = re.sub(r'^\s*Permanent Link \nview \n', '', body)
# cut the trailing "Permanent Link What's this?" chrome but keep the index entries and citation
with open(out, 'w', encoding='utf-8') as f:
    f.write(f"# {title}\n\n")
    f.write(f"CITATION: {cite}\n")
    f.write(f"URL (original): {orig}\n")
    f.write(f"URL (fetched, Wayback Machine capture): {cap}\n")
    f.write(f"DATE FETCHED: {datetime.date.today().isoformat()}\n")
    f.write("TRANSCRIPTION: scholarly edition text (Princeton, Papers of Thomas Jefferson / Madison Papers, as published on Founders Online); text below is verbatim from the fetched page, including the editors' source note and footnotes. Superscripts are flattened by the HTML-to-text conversion (e.g. 'Oct r' = Oct^r, '11 th' = 11^th).\n")
    if note: f.write("NOTE: " + note + "\n")
    f.write("\n---- VERBATIM TEXT (Founders Online page) ----\n\n")
    f.write(body.strip() + "\n")
print('wrote', out)
