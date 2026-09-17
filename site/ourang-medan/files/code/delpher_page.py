#!/usr/bin/env python3
"""Download a KB page image (JP2) + ALTO; save reduced JPEG and optionally crops around search strings.
Usage: page.py <page_urn> <outprefix> [search terms...]"""
import sys, subprocess, os, re, xml.etree.ElementTree as ET
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
urn, out = sys.argv[1], sys.argv[2]
terms = [t.lower() for t in sys.argv[3:]]
jp2 = out + ".jp2"; alto = out + ".alto.xml"
if not os.path.exists(jp2) or os.path.getsize(jp2) < 1000:
    subprocess.run(["curl", "-sSL", "-o", jp2, f"https://resolver.kb.nl/resolve?urn={urn}:image"], check=True)
if not os.path.exists(alto) or os.path.getsize(alto) < 1000:
    subprocess.run(["curl", "-sSL", "-o", alto, f"https://resolver.kb.nl/resolve?urn={urn}:alto"], check=True)
im = Image.open(jp2); W, H = im.size
print("image size", W, H)
# reduced overview
ov = im.copy(); ov.thumbnail((2000, 2000)); ov.convert("L").save(out + "_overview.jpg", quality=80)
# ALTO hits
try:
    root = ET.parse(alto).getroot()
except Exception as e:
    print("ALTO parse error", e); sys.exit()
hits = []
pw = None
for el in root.iter():
    tag = el.tag.split('}')[-1]
    if tag == "Page":
        pw = (int(float(el.get("WIDTH", 0))), int(float(el.get("HEIGHT", 0))))
    if tag == "String":
        c = (el.get("CONTENT") or "").lower()
        for t in terms:
            if t in c:
                hits.append((t, el.get("CONTENT"), int(float(el.get("HPOS"))), int(float(el.get("VPOS")))))
print("ALTO page size", pw, "image size", (W, H))
sx = W / pw[0] if pw and pw[0] else 1.0; sy = H / pw[1] if pw and pw[1] else 1.0
for h in hits:
    print("HIT", h)
# crops: cluster hits
import math
done = []
for i, (t, c, x, y) in enumerate(hits):
    X, Y = int(x * sx), int(y * sy)
    if any(abs(X - dx) < 900 and abs(Y - dy) < 1500 for dx, dy in done):
        continue
    done.append((X, Y))
    box = (max(0, X - 700), max(0, Y - 500), min(W, X + 1100), min(H, Y + 2500))
    cr = im.crop(box); cr.thumbnail((1800, 3000)); cr.convert("L").save(f"{out}_crop{len(done)}.jpg", quality=85)
    print("crop", len(done), box)
