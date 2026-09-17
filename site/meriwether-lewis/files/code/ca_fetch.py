#!/usr/bin/env python3
"""Fetch OCR full text of a Chronicling America page via the loc.gov JSON API.
Usage: ca_fetch.py <resource url like https://www.loc.gov/resource/sn82014783/1809-10-31/ed-1/?sp=3> <outfile>"""
import sys, json, urllib.request, re
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':UA}), timeout=120).read()
url, out = sys.argv[1], sys.argv[2]
url = url.replace('http://','https://')
j = json.loads(get(url + ('&' if '?' in url else '?') + 'fo=json'))
ft_url = j['resource'].get('fulltext_file')
pdf = j['resource'].get('pdf')
title = j.get('item',{}).get('title') or j.get('item',{}).get('partof_title')
d = json.loads(get(ft_url))
txt = list(d.values())[0].get('full_text','')
with open(out,'w',encoding='utf-8') as f:
    f.write('PAGE: ' + url + '\nTITLE: ' + str(title) + '\nFULLTEXT: ' + ft_url + '\nPDF: ' + str(pdf) + '\n\n' + txt)
print('wrote', out, len(txt), 'chars; pdf', pdf)
