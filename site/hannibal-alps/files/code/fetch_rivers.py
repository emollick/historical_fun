#!/usr/bin/env python3
"""Fetch simplified river centrelines (OSM waterway relations) via Nominatim for the map.

Nominatim returns the relation geometry as GeoJSON when asked with
polygon_geojson=1; polygon_threshold simplifies it (Douglas-Peucker, degrees).
One request per second, identifying User-Agent.  Output: data/rivers.json
{name: {"osm": "relation/ID", "lines": [[[lat, lon], ...], ...]}}.
Only for drawing; the route model does not use these lines.
"""
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "rivers.json")
UA = "hannibal-alps-terrain-model/1.0 (historical research; python urllib)"
RIVERS = {
    "Rhone": "Rhône river",
    "Isere": "Isère river",
    "Arc (Maurienne)": "L'Arc, Savoie",
    "Drac": "Drac river",
    "Drome": "Drôme river",
    "Durance": "Durance river",
    "Guil": "Guil river",
    "Ubaye": "Ubaye river",
    "Buech": "Buëch river",
    "Aygues": "Eygues river",
    "Dora Riparia": "Dora Riparia",
    "Dora Baltea": "Dora Baltea",
    "Po": "fiume Po",
    "Stura di Demonte": "Stura di Demonte",
    "Chisone": "Chisone",
    "Pellice": "Pellice",
    "Varaita": "Varaita",
    "Maira": "Maira torrente",
    "Tanaro": "Tanaro",
    "Sesia": "Sesia",
    "Orco": "Orco torrente",
}


def fetch(q):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "limit": 5, "polygon_geojson": 1, "polygon_threshold": 0.003})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    out = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            out = json.load(f)
    for name, q in RIVERS.items():
        if name in out:
            continue
        try:
            res = fetch(q)
        except Exception as e:  # noqa: BLE001
            print("FAILED", name, e)
            time.sleep(1.1)
            continue
        time.sleep(1.1)
        best = None
        for x in res:
            if x.get("class") == "waterway" and x.get("osm_type") == "relation":
                best = x
                break
        if best is None:
            for x in res:
                if x.get("class") == "waterway":
                    best = x
                    break
        if best is None:
            print("NO RIVER", name, [(x.get("class"), x.get("type")) for x in res])
            continue
        g = best.get("geojson", {})
        lines = []
        if g.get("type") == "LineString":
            lines = [[[c[1], c[0]] for c in g["coordinates"]]]
        elif g.get("type") == "MultiLineString":
            lines = [[[c[1], c[0]] for c in part] for part in g["coordinates"]]
        else:
            print("odd geometry", name, g.get("type"))
        out[name] = {"osm": "%s/%s" % (best.get("osm_type"), best.get("osm_id")), "display_name": best.get("display_name"), "lines": lines}
        print("%-18s %s parts=%d pts=%d" % (name, out[name]["osm"], len(lines), sum(len(l) for l in lines)))
        with open(OUT, "w") as f:
            json.dump(out, f)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
