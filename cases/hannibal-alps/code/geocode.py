#!/usr/bin/env python3
"""Geocode the place names used by the Hannibal route model with Nominatim (OSM).

Policy: one request per second, an identifying User-Agent, results cached in
data/geocode_cache.json so the run is reproducible and re-runs do not hit the
service.  Output: data/places.json = {key: {lat, lon, name, query, source,
osm_type, osm_id, display_name}}.  Places with a MANUAL entry are written with
source "manual" (used only where Nominatim returns nothing usable or where a
valley-floor point rather than a village centre is wanted; each manual point is
checked against the DEM by routes.py).

Usage: python3 geocode.py            (uses cache; fetches only what is missing)
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CACHE = os.path.join(DATA, "geocode_cache.json")
OUT = os.path.join(DATA, "places.json")
UA = "hannibal-alps-terrain-model/1.0 (historical research; python urllib)"

# key: (query, preferred OSM class/type hint or None)
PLACES = {
    # --- lower Rhone / crossing options
    "Fourques": ("Fourques, Gard, France", "town"),
    "Beaucaire": ("Beaucaire, Gard, France", "town"),
    "Tarascon": ("Tarascon, Bouches-du-Rhone, France", "town"),
    "Avignon": ("Avignon, Vaucluse, France", "city"),
    "Roquemaure": ("Roquemaure, Gard, France", "town"),
    "Orange": ("Orange, Vaucluse, France", "city"),
    "Caderousse": ("Caderousse, Vaucluse, France", "town"),
    "Bollene": ("Bollene, Vaucluse, France", "town"),
    "Pierrelatte": ("Pierrelatte, Drome, France", "town"),
    "Montelimar": ("Montelimar, Drome, France", "city"),
    "Loriol": ("Loriol-sur-Drome, Drome, France", "town"),
    "Valence": ("Valence, Drome, France", "city"),
    "Lyon": ("Lyon, France", "city"),
    "Vienne": ("Vienne, Isere, France", "city"),
    # --- Isere / Gresivaudan / Combe de Savoie / Maurienne (R1, R2)
    "Romans": ("Romans-sur-Isere, Drome, France", "town"),
    "Saint-Marcellin": ("Saint-Marcellin, Isere, France", "town"),
    "Tullins": ("Tullins, Isere, France", "town"),
    "Voreppe": ("Voreppe, Isere, France", "town"),
    "Grenoble": ("Grenoble, France", "city"),
    "Pontcharra": ("Pontcharra, Isere, France", "town"),
    "Montmelian": ("Montmelian, Savoie, France", "town"),
    "Aiguebelle": ("Aiguebelle, Savoie, France", "village"),
    "La Chambre": ("La Chambre, Savoie, France", "village"),
    "Saint-Jean-de-Maurienne": ("Saint-Jean-de-Maurienne, Savoie, France", "town"),
    "Saint-Michel-de-Maurienne": ("Saint-Michel-de-Maurienne, Savoie, France", "town"),
    "Modane": ("Modane, Savoie, France", "town"),
    "Bramans": ("Bramans, Savoie, France", "village"),
    "Termignon": ("Termignon, Savoie, France", "village"),
    "Lanslebourg": ("Lanslebourg-Mont-Cenis, Savoie, France", "village"),
    "Col du Mont-Cenis": ("Col du Mont Cenis", "mountain_pass"),
    "Col du Petit Mont-Cenis": ("Col du Petit Mont Cenis", "mountain_pass"),
    "Le Planay (Bramans)": ("Le Planay, Bramans, Savoie, France", None),
    "Lac Savine": ("Lac Savine, Savoie", None),
    "Col Clapier": ("Col Clapier", "mountain_pass"),
    "Giaglione": ("Giaglione, Torino, Italia", "village"),
    "Susa": ("Susa, Torino, Italia", "town"),
    "Bussoleno": ("Bussoleno, Torino, Italia", "town"),
    "Sant'Ambrogio di Torino": ("Sant'Ambrogio di Torino, Torino, Italia", "town"),
    "Avigliana": ("Avigliana, Torino, Italia", "town"),
    "Rivoli": ("Rivoli, Torino, Italia", "town"),
    "Turin": ("Torino, Italia", "city"),
    # --- Tarentaise / Petit-Saint-Bernard (R3)
    "Albertville": ("Albertville, Savoie, France", "town"),
    "Moutiers": ("Moutiers, Savoie, France", "town"),
    "Aime": ("Aime-la-Plagne, Savoie, France", "town"),
    "Bourg-Saint-Maurice": ("Bourg-Saint-Maurice, Savoie, France", "town"),
    "Seez": ("Seez, Savoie, France", "village"),
    "Col du Petit-Saint-Bernard": ("Col du Petit-Saint-Bernard", "mountain_pass"),
    "La Thuile": ("La Thuile, Aosta, Italia", "village"),
    "Pre-Saint-Didier": ("Pre-Saint-Didier, Aosta, Italia", "village"),
    "Morgex": ("Morgex, Aosta, Italia", "village"),
    "Aosta": ("Aosta, Italia", "city"),
    "Chatillon (Aosta)": ("Chatillon, Valle d'Aosta, Italia", "town"),
    "Pont-Saint-Martin": ("Pont-Saint-Martin, Aosta, Italia", "town"),
    "Ivrea": ("Ivrea, Torino, Italia", "town"),
    "Chivasso": ("Chivasso, Torino, Italia", "town"),
    "Vercelli": ("Vercelli, Italia", "city"),
    "Novara": ("Novara, Italia", "city"),
    "Milan": ("Milano, Italia", "city"),
    # --- Durance (R4, R5, R6)
    "Cavaillon": ("Cavaillon, Vaucluse, France", "town"),
    "Pertuis": ("Pertuis, Vaucluse, France", "town"),
    "Manosque": ("Manosque, Alpes-de-Haute-Provence, France", "town"),
    "Sisteron": ("Sisteron, Alpes-de-Haute-Provence, France", "town"),
    "Tallard": ("Tallard, Hautes-Alpes, France", "town"),
    "Gap": ("Gap, Hautes-Alpes, France", "city"),
    "Chorges": ("Chorges, Hautes-Alpes, France", "village"),
    "Savines-le-Lac": ("Savines-le-Lac, Hautes-Alpes, France", "village"),
    "Embrun": ("Embrun, Hautes-Alpes, France", "town"),
    "Guillestre": ("Guillestre, Hautes-Alpes, France", "town"),
    "L'Argentiere-la-Bessee": ("L'Argentiere-la-Bessee, Hautes-Alpes, France", "town"),
    "Briancon": ("Briancon, Hautes-Alpes, France", "town"),
    "Col de Montgenevre": ("Col de Montgenevre", "mountain_pass"),
    "Claviere": ("Claviere, Torino, Italia", "village"),
    "Cesana Torinese": ("Cesana Torinese, Torino, Italia", "village"),
    "Oulx": ("Oulx, Torino, Italia", "town"),
    "Exilles": ("Exilles, Torino, Italia", "village"),
    # --- Drome / Cabre / Grimone approach (Livy - de Beer)
    "Crest": ("Crest, Drome, France", "town"),
    "Saillans": ("Saillans, Drome, France", "village"),
    "Die": ("Die, Drome, France", "town"),
    "Luc-en-Diois": ("Luc-en-Diois, Drome, France", "village"),
    "Col de Cabre": ("Col de Cabre, Drome", "mountain_pass"),
    "Col de Grimone": ("Col de Grimone", "mountain_pass"),
    "La Beaume": ("La Beaume, Hautes-Alpes, France", "village"),
    "Aspres-sur-Buech": ("Aspres-sur-Buech, Hautes-Alpes, France", "village"),
    "Veynes": ("Veynes, Hautes-Alpes, France", "town"),
    # --- Guil / Traversette (R5)
    "Chateau-Ville-Vieille": ("Chateau-Ville-Vieille, Hautes-Alpes, France", "village"),
    "Aiguilles": ("Aiguilles, Hautes-Alpes, France", "village"),
    "Abries": ("Abries, Hautes-Alpes, France", "village"),
    "Ristolas": ("Ristolas, Hautes-Alpes, France", "village"),
    "L'Echalp": ("L'Echalp, Ristolas, Hautes-Alpes", None),
    "Refuge du Viso": ("Refuge du Viso, Ristolas", None),
    "Col de la Traversette": ("Col de la Traversette", "mountain_pass"),
    "Pian del Re": ("Pian del Re, Crissolo", None),
    "Crissolo": ("Crissolo, Cuneo, Italia", "village"),
    "Paesana": ("Paesana, Cuneo, Italia", "village"),
    "Saluzzo": ("Saluzzo, Cuneo, Italia", "town"),
    "Carmagnola": ("Carmagnola, Torino, Italia", "town"),
    "Col Agnel": ("Col Agnel", "mountain_pass"),
    "Col de la Croix (Croce)": ("Colle della Croce, Cuneo", "mountain_pass"),
    # --- Ubaye / Larche (R6)
    "Le Lauzet-Ubaye": ("Le Lauzet-Ubaye, Alpes-de-Haute-Provence, France", "village"),
    "Barcelonnette": ("Barcelonnette, Alpes-de-Haute-Provence, France", "town"),
    "Jausiers": ("Jausiers, Alpes-de-Haute-Provence, France", "village"),
    "Larche": ("Larche, Alpes-de-Haute-Provence, France", "village"),
    "Col de Larche": ("Col de Larche", "mountain_pass"),
    "Col de Vars": ("Col de Vars", "mountain_pass"),
    "Argentera": ("Argentera, Cuneo, Italia", "village"),
    "Pietraporzio": ("Pietraporzio, Cuneo, Italia", "village"),
    "Vinadio": ("Vinadio, Cuneo, Italia", "village"),
    "Demonte": ("Demonte, Cuneo, Italia", "village"),
    "Borgo San Dalmazzo": ("Borgo San Dalmazzo, Cuneo, Italia", "town"),
    "Cuneo": ("Cuneo, Italia", "city"),
    "Savigliano": ("Savigliano, Cuneo, Italia", "town"),
    # --- Grand-Saint-Bernard (R7)
    "Bourgoin-Jallieu": ("Bourgoin-Jallieu, Isere, France", "town"),
    "Chambery": ("Chambery, Savoie, France", "city"),
    "Annecy": ("Annecy, Haute-Savoie, France", "city"),
    "Geneva": ("Geneve, Suisse", "city"),
    "Villeneuve (Vaud)": ("Villeneuve, Vaud, Suisse", "town"),
    "Saint-Maurice (Valais)": ("Saint-Maurice, Valais, Suisse", "town"),
    "Martigny": ("Martigny, Valais, Suisse", "town"),
    "Orsieres": ("Orsieres, Valais, Suisse", "village"),
    "Bourg-Saint-Pierre": ("Bourg-Saint-Pierre, Valais, Suisse", "village"),
    "Col du Grand-Saint-Bernard": ("Col du Grand-Saint-Bernard", "mountain_pass"),
    "Saint-Rhemy-en-Bosses": ("Saint-Rhemy-en-Bosses, Aosta, Italia", "village"),
    "Etroubles": ("Etroubles, Aosta, Italia", "village"),
}


def nominatim(query):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": query, "format": "json", "limit": 5, "addressdetails": 0}
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def pick(results, hint):
    if not results:
        return None
    if hint:
        for r in results:
            if r.get("type") == hint or r.get("addresstype") == hint or r.get("class") == hint:
                return r
        # a saddle is as good as a mountain_pass
        if hint == "mountain_pass":
            for r in results:
                if r.get("type") in ("saddle", "mountain_pass") or r.get("class") == "mountain_pass":
                    return r
    return results[0]


def main():
    os.makedirs(DATA, exist_ok=True)
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            cache = json.load(f)
    places = {}
    for key, (query, hint) in PLACES.items():
        if query not in cache:
            try:
                cache[query] = nominatim(query)
            except Exception as e:  # noqa: BLE001
                print("FAILED", key, query, e, file=sys.stderr)
                cache[query] = []
            time.sleep(1.05)
            with open(CACHE, "w") as f:
                json.dump(cache, f, indent=1)
        r = pick(cache[query], hint)
        if r is None:
            print("NO RESULT", key, query, file=sys.stderr)
            continue
        places[key] = {
            "lat": float(r["lat"]),
            "lon": float(r["lon"]),
            "name": key,
            "query": query,
            "source": "Nominatim/OSM %s/%s (%s)" % (r.get("osm_type"), r.get("osm_id"), r.get("type")),
            "osm_type": r.get("osm_type"),
            "osm_id": r.get("osm_id"),
            "display_name": r.get("display_name"),
        }
        print("%-28s %9.5f %9.5f  %s" % (key, places[key]["lat"], places[key]["lon"], r.get("display_name", "")[:70]))
    with open(OUT, "w") as f:
        json.dump(places, f, indent=1, ensure_ascii=False)
    print("wrote", OUT, len(places), "places")


if __name__ == "__main__":
    main()
