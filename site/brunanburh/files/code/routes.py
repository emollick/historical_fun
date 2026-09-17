#!/usr/bin/env python3
"""Brunanburh 937: route-length and time-budget model.

Pure-python (no dependencies). Computes great-circle lengths of coast-hugging
sea routes and Roman-road land routes from the known start points of the three
coalition contingents (Dublin fleet, Scots of Alba, Cumbrians of Strathclyde)
and of Aethelstan's West Saxon/Mercian host, to each candidate battlefield.

Coordinates are decimal degrees (WGS84), read from Ordnance Survey / OpenStreetMap
for modern places; waypoint paths are approximations of coast-hugging sailing
routes (headland to headland) and of the Roman road network (fort to fort).
Distances are therefore lower bounds for real journeys (they ignore tacking,
weather, tides, river meanders and detours). Speeds used:

  Sea:  Viking-age replica trials give 4-6 knots average under sail in fair wind
        (Sea Stallion from Glendalough, Roskilde-Dublin 2007: ~5.5 kn average
        over the open-sea legs; Ottar 2004; see Englert & Ossowski 2009, and
        Crumlin-Pedersen 1997). A fleet of hundreds of ships, coasting by day and
        anchoring or beaching at night, is modelled at 40-70 nautical miles per
        day; continuous sailing at 5 kn gives 120 nmi/day as an upper bound.
  Land: pre-modern armies with baggage: 15-25 km/day (Engels 1978 on Alexander's
        army; Haldon 1999; Bachrach on Carolingian marches); forced march up to
        35 km/day for short periods.

Run: python3 routes.py  -> prints tables and writes routes_output.csv
"""
import math, csv, sys

R_KM = 6371.0088
NMI = 1.852  # km per nautical mile

def hav(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = p2 - p1
    dl = math.radians(lo2 - lo1)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R_KM*math.asin(math.sqrt(h))

def path_len(pts):
    return sum(hav(pts[i], pts[i+1]) for i in range(len(pts)-1))

# ---------------------------------------------------------------- places
P = {
 # start points
 'Dublin (Liffey mouth)':      (53.345, -6.20),
 'Scone / Forteviot (Alba royal centre)': (56.40, -3.45),
 'Govan / Dumbarton (Strathclyde)': (55.90, -4.45),
 'Winchester':                 (51.063, -1.308),
 'Tamworth':                   (52.634, -1.695),
 # candidate battlefields
 'Bromborough (Wirral)':       (53.343, -2.987),
 'Brinsworth / Tinsley (Rotherham)': (53.408, -1.383),
 'Wentbridge / Went valley (Doncaster N)': (53.636, -1.267),
 'Burnswark (Dumfriesshire)':  (55.108, -3.254),
 'Lanchester (Co. Durham)':    (54.822, -1.740),
 'Burnley (River Brun)':       (53.789, -2.248),
 # landing places
 'Mersey mouth (New Brighton)': (53.44, -3.03),
 'Dee estuary (Hilbre / West Kirby)': (53.38, -3.22),
 'Ribble mouth':               (53.73, -3.05),
 'Solway (Annan mouth)':       (54.97, -3.27),
 'Tyne mouth':                 (55.01, -1.40),
 'Wear mouth (Sunderland)':    (54.92, -1.36),
 'Humber mouth (Spurn Head)':  (53.58, 0.11),
 'Humber head (Airmyn, Ouse/Aire)': (53.72, -0.90),
 # towns
 'Chester':                    (53.19, -2.89),
 'York':                       (53.96, -1.08),
 'Carlisle':                   (54.89, -2.94),
 'Doncaster':                  (53.52, -1.13),
}

# coast-hugging sea waypoints (headland to headland)
SEA = {
 'Dublin -> Mersey/Dee (direct Irish Sea crossing)': [
    P['Dublin (Liffey mouth)'], (53.37, -6.04), (53.42, -3.30), P['Dee estuary (Hilbre / West Kirby)']],
 'Dublin -> Ribble mouth': [
    P['Dublin (Liffey mouth)'], (53.37, -6.04), (53.72, -3.40), P['Ribble mouth']],
 'Dublin -> Solway (Annan) via Isle of Man': [
    P['Dublin (Liffey mouth)'], (53.37, -6.04), (54.10, -4.75), (54.42, -4.36), (54.75, -3.75), P['Solway (Annan mouth)']],
 'Dublin -> Humber, NORTH-ABOUT (Minch, Cape Wrath, Pentland Firth, east coast)': [
    P['Dublin (Liffey mouth)'], (53.37, -6.04), (54.20, -5.50), (54.90, -5.40), (55.25, -5.85), (55.70, -6.55),
    (56.35, -7.10), (56.85, -6.90), (57.45, -6.85), (58.05, -5.90), (58.65, -5.05), (58.70, -3.40),
    (58.64, -3.00), (58.15, -3.30), (57.72, -1.95), (57.47, -1.75), (57.15, -2.00), (56.70, -2.40),
    (56.28, -2.55), (55.92, -2.10), (55.62, -1.60), (55.01, -1.35), (54.50, -0.55), (54.12, -0.05),
    P['Humber mouth (Spurn Head)']],
 'Dublin -> Humber, SOUTH-ABOUT (Land\'s End, Channel, Dover, East Anglia)': [
    P['Dublin (Liffey mouth)'], (52.97, -5.95), (52.20, -6.15), (51.90, -5.35), (51.15, -4.75), (50.05, -5.75),
    (49.95, -5.15), (50.20, -3.60), (50.50, -2.40), (50.55, -1.25), (50.72, 0.25), (51.12, 1.40),
    (51.38, 1.48), (52.08, 1.62), (52.62, 1.78), (52.95, 1.30), (52.98, 0.45), (53.15, 0.38),
    P['Humber mouth (Spurn Head)']],
 'Dublin -> Tyne mouth, NORTH-ABOUT': [
    P['Dublin (Liffey mouth)'], (53.37, -6.04), (54.20, -5.50), (54.90, -5.40), (55.25, -5.85), (55.70, -6.55),
    (56.35, -7.10), (56.85, -6.90), (57.45, -6.85), (58.05, -5.90), (58.65, -5.05), (58.70, -3.40),
    (58.64, -3.00), (58.15, -3.30), (57.72, -1.95), (57.47, -1.75), (57.15, -2.00), (56.70, -2.40),
    (56.28, -2.55), (55.92, -2.10), (55.62, -1.60), P['Tyne mouth']],
 'Humber mouth -> Airmyn (head of Humber, Ouse/Aire junction), river leg': [
    P['Humber mouth (Spurn Head)'], (53.63, -0.25), (53.72, -0.60), P['Humber head (Airmyn, Ouse/Aire)']],
}

# Roman-road land waypoints (fort to fort)
DERE_STREET_TO_YORK = [P['Scone / Forteviot (Alba royal centre)'], (56.12, -3.94), (55.99, -3.86), (55.94, -3.06),
    (55.60, -2.69), (55.28, -2.31), (54.97, -2.02), (54.82, -1.74), (54.67, -1.68), (54.38, -1.63), (54.09, -1.38), P['York']]
WEST_ROAD_TO_CHESTER = [P['Scone / Forteviot (Alba royal centre)'], (56.12, -3.94), (55.71, -3.62), (55.47, -3.66),
    (55.108, -3.254), P['Carlisle'], (54.65, -2.72), (54.40, -2.60), (54.05, -2.80), (53.81, -2.53), (53.55, -2.63),
    (53.39, -2.58), P['Chester']]
STRATHCLYDE_TO_CARLISLE = [P['Govan / Dumbarton (Strathclyde)'], (55.71, -3.62), (55.47, -3.66), (55.108, -3.254), P['Carlisle']]

LAND = {
 'Alba (Scone) -> Bromborough, west road via Carlisle, Lancaster, Chester': WEST_ROAD_TO_CHESTER + [P['Bromborough (Wirral)']],
 'Alba (Scone) -> Burnswark, via Clydesdale/Annandale': [P['Scone / Forteviot (Alba royal centre)'], (56.12, -3.94), (55.71, -3.62), (55.47, -3.66), P['Burnswark (Dumfriesshire)']],
 'Alba (Scone) -> Lanchester, Dere Street': DERE_STREET_TO_YORK[:8],
 'Alba (Scone) -> Wentbridge, Dere Street via York': DERE_STREET_TO_YORK + [(53.88, -1.26), (53.72, -1.36), P['Wentbridge / Went valley (Doncaster N)']],
 'Alba (Scone) -> Brinsworth, Dere Street via York and Doncaster': DERE_STREET_TO_YORK + [(53.88, -1.26), (53.72, -1.36), (53.636, -1.267), P['Doncaster'], P['Brinsworth / Tinsley (Rotherham)']],
 'Alba (Scone) -> Burnley, west road via Carlisle, Ribchester': WEST_ROAD_TO_CHESTER[:10] + [P['Burnley (River Brun)']],
 'Strathclyde (Govan) -> Bromborough via Carlisle, Lancaster, Chester': STRATHCLYDE_TO_CARLISLE + WEST_ROAD_TO_CHESTER[6:] + [P['Bromborough (Wirral)']],
 'Strathclyde (Govan) -> Burnswark': STRATHCLYDE_TO_CARLISLE[:4],
 'Strathclyde (Govan) -> Brinsworth via Carlisle, Stainmore, Catterick, York': STRATHCLYDE_TO_CARLISLE + [(54.60, -2.20), (54.50, -1.90), (54.38, -1.63), (54.09, -1.38), P['York'], (53.88, -1.26), (53.72, -1.36), (53.636, -1.267), P['Doncaster'], P['Brinsworth / Tinsley (Rotherham)']],
 'Winchester -> Bromborough via Watling Street and Chester': [P['Winchester'], (51.75, -1.26), (52.13, -0.99), (52.66, -1.83), (52.72, -2.55), (52.83, -2.75), P['Chester'], P['Bromborough (Wirral)']],
 'Winchester -> Brinsworth via Fosse Way / Ryknild Street': [P['Winchester'], (51.75, -1.26), (52.13, -0.99), (52.63, -1.32), (52.95, -1.16), (53.23, -1.45), P['Brinsworth / Tinsley (Rotherham)']],
 'Winchester -> Wentbridge via Ermine Street and Lincoln': [P['Winchester'], (51.51, -0.09), (52.24, -0.27), (52.77, -0.38), (53.23, -0.54), (53.52, -1.13), P['Wentbridge / Went valley (Doncaster N)']],
 'Winchester -> Lanchester via York and Dere Street': [P['Winchester'], (51.51, -0.09), (52.24, -0.27), (52.77, -0.38), (53.23, -0.54), (53.52, -1.13), P['York'], (54.09, -1.38), (54.38, -1.63), (54.67, -1.68), P['Lanchester (Co. Durham)']],
 'Winchester -> Burnswark via Chester, Lancaster, Carlisle': [P['Winchester'], (51.75, -1.26), (52.13, -0.99), (52.66, -1.83), (52.72, -2.55), (52.83, -2.75), P['Chester'], (53.39, -2.58), (53.55, -2.63), (53.81, -2.53), (54.05, -2.80), (54.40, -2.60), (54.65, -2.72), P['Carlisle'], P['Burnswark (Dumfriesshire)']],
 # landing to battlefield (fleet contingent on foot)
 'Dee estuary landing -> Bromborough': [P['Dee estuary (Hilbre / West Kirby)'], P['Bromborough (Wirral)']],
 'Airmyn (Humber head) -> Wentbridge': [P['Humber head (Airmyn, Ouse/Aire)'], (53.70, -1.05), P['Wentbridge / Went valley (Doncaster N)']],
 'Airmyn (Humber head) -> Brinsworth': [P['Humber head (Airmyn, Ouse/Aire)'], P['Doncaster'], P['Brinsworth / Tinsley (Rotherham)']],
 'Annan mouth -> Burnswark': [P['Solway (Annan mouth)'], P['Burnswark (Dumfriesshire)']],
 'Tyne mouth -> Lanchester': [P['Tyne mouth'], (54.97, -1.62), P['Lanchester (Co. Durham)']],
 'Ribble mouth -> Burnley': [P['Ribble mouth'], (53.76, -2.70), (53.81, -2.53), P['Burnley (River Brun)']],
}

rows = []
print("SEA ROUTES (coast-hugging great-circle legs; lower bounds)")
print(f"{'route':78s} {'km':>7s} {'nmi':>7s} {'days@40nmi':>11s} {'days@70nmi':>11s} {'days@120nmi':>12s}")
for name, pts in SEA.items():
    km = path_len(pts); nmi = km/NMI
    print(f"{name:78s} {km:7.0f} {nmi:7.0f} {nmi/40:11.1f} {nmi/70:11.1f} {nmi/120:12.1f}")
    rows.append(('sea', name, round(km), round(nmi), round(nmi/40,1), round(nmi/70,1), round(nmi/120,1)))
print()
print("LAND ROUTES (Roman roads, fort to fort; lower bounds)")
print(f"{'route':78s} {'km':>7s} {'days@15km':>10s} {'days@20km':>10s} {'days@25km':>10s}")
for name, pts in LAND.items():
    km = path_len(pts)
    print(f"{name:78s} {km:7.0f} {km/15:10.1f} {km/20:10.1f} {km/25:10.1f}")
    rows.append(('land', name, round(km), '', round(km/15,1), round(km/20,1), round(km/25,1)))

with open(sys.argv[1] if len(sys.argv) > 1 else 'routes_output.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['mode','route','km','nmi','days_slow','days_mid','days_fast'])
    w.writerows(rows)
