"""
Straight-line distances from the 1587 settlement site on Roanoke Island to the places
named in the sources and in the scenarios, for the question of what "50 miles into the
maine" (White, 1587 and 1590) could have meant.

Coordinates: Wikipedia page coordinates (fetched 14 Sep 2026 via the MediaWiki API) for
modern places; the archaeological sites are placed from their published descriptions and
carry an uncertainty of a few kilometres, which does not matter at this scale.

A "mile" in 1587 is itself uncertain. The statute mile (1,760 yd = 1.609 km) was fixed by
35 Eliz. I c. 6 (1593); a longer customary "old English mile" of roughly 2.0-2.2 km was
still in use. Both readings are tabulated.
"""
import math, csv, sys, os

ROANOKE = ("Roanoke Island, 1585-87 settlement (Fort Raleigh NHS)", 35.9386, -75.7100)

PLACES = [
    # name, lat, lon, note
    ("Dasamonquepeuc (Manns Harbor)", 35.8858, -75.7628, "mainland town opposite Roanoke; Wikipedia coord for Manns Harbor"),
    ("Port Ferdinando / Hatarask inlet (approx.)", 35.82, -75.55, "closed inlet S of Nags Head; position approximate (Quinn)"),
    ("Kenricks Mounts / Chicamacomico (Rodanthe)", 35.5933, -75.4678, "smoke seen 1590; Wikipedia coord for Rodanthe"),
    ("Croatoan: Cape Creek site 31DR1 (Buxton)", 35.2678, -75.5425, "Manteo's town; Wikipedia coord for Buxton, site within ~1 km"),
    ("Wokokon (Ocracoke)", 35.1128, -75.9758, "Wikipedia coord for Ocracoke"),
    ("Site X / Site Y, Salmon Creek (near Merry Hill)", 36.00, -76.70, "First Colony Foundation sites at the mouth of Salmon Creek; approx. from FCF descriptions"),
    ("Edenton (reported findspot region of the 1937 Dare Stone)", 36.0581, -76.6008, "Wikipedia coord"),
    ("Chowanoke, main town of the Chowanoc (near Harrellsville)", 36.28, -76.75, "approx.; site 31HF30 on the Chowan, Hertford County"),
    ("Windsor (Cashie River, Tuscarora country)", 35.9931, -76.94, "Wikipedia coord"),
    ("Weldon (Roanoke River fall line)", 36.4239, -77.6131, "Wikipedia coord; one region proposed for Ocanahowan"),
    ("Bath (Pamlico River)", 35.4703, -76.8119, "Wikipedia coord; Secotan/Pomeiooc country lies between"),
    ("Chesepian towns, Lynnhaven / Great Neck (Virginia Beach)", 36.88, -76.05, "approx.; Great Neck Point site"),
    ("Jamestown (1607)", 37.2088, -76.7794, "Historic Jamestowne"),
]

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

def bearing(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl)*math.cos(p2)
    y = math.cos(p1)*math.sin(p2) - math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def compass(b):
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return dirs[int((b + 11.25) // 22.5) % 16]

STATUTE_MILE_KM = 1.609344
OLD_MILE_KM = 2.1   # customary 'old English mile' c. 1.3 statute miles; a rough central value

rows = []
for name, lat, lon, note in PLACES:
    km = haversine_km(ROANOKE[1], ROANOKE[2], lat, lon)
    b = bearing(ROANOKE[1], ROANOKE[2], lat, lon)
    rows.append({
        "place": name, "lat": lat, "lon": lon,
        "km_straight": round(km, 1),
        "statute_miles": round(km / STATUTE_MILE_KM, 1),
        "old_miles": round(km / OLD_MILE_KM, 1),
        "bearing_deg": round(b), "compass": compass(b),
        "on_mainland": "no" if any(k in name for k in ["Croatoan", "Wokokon", "Kenricks", "Port Ferdinando"]) else "yes",
        "note": note,
    })

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "distances_from_roanoke.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

print(f"From {ROANOKE[0]} ({ROANOKE[1]}, {ROANOKE[2]})")
print(f"{'place':62s} {'km':>6s} {'stat.mi':>8s} {'old mi':>7s} {'bearing':>8s} mainland")
for r in rows:
    print(f"{r['place']:62s} {r['km_straight']:6.1f} {r['statute_miles']:8.1f} {r['old_miles']:7.1f} {r['bearing_deg']:5d} {r['compass']:>3s}  {r['on_mainland']}")
print("\n'50 miles' = %.0f km (statute) to %.0f km (old mile)" % (50*STATUTE_MILE_KM, 50*OLD_MILE_KM))
