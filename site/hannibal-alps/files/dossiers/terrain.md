# Terrain and route dossier: which Alpine pass fits the numbers? (Hannibal, 218 BC)

All numbers below are produced by the code in `code/` from public data; nothing in this dossier is taken from memory unless marked "(unverified)".

## README: how to re-run everything

```
cd code
pip install rasterio numpy pillow skyfield ephem        # versions used: rasterio 1.4.4, numpy 2.4.6, Pillow 12.3.0, skyfield 1.55, ephem 4.2.1
python3 download_dem.py            # 20 Copernicus GLO-90 tiles (N43-N46, E004-E008) -> dem/ in the case folder (about 95 MB; idempotent)
python3 geocode.py                 # Nominatim, 1 request/s; results cached in data/geocode_cache.json -> data/places.json
python3 fetch_rivers.py            # OSM river centrelines via Nominatim (map decoration only) -> data/rivers.json
python3 routes.py                  # least-cost valley paths, profiles, all distance tables (about 3 min, pure Python + numpy)
python3 viewshed.py                # Po-plain visibility from every col, descent point and nearby knoll (about 20 min)
curl -o de406.bsp https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de406.bsp   # 300 MB; DE421 does not cover 218 BC
python3 pleiades.py de406.bsp   # Pleiades phases 218 BC (skyfield + independent pyephem check)
python3 figures.py                 # data/map_overview.svg, data/profiles.svg, data/viewshed_panels.png
python3 report_tables.py           # regenerates the tables of this dossier -> data/terrain_tables.md
```

The DEM directory defaults to `dem/` in the case folder (`HANNIBAL_DEM_DIR` overrides it); the ephemeris path is the first argument of `pleiades.py` (`HANNIBAL_EPHEMERIS` overrides it). Network is needed only for the first three steps and for the ephemeris.

## Summary

| candidate (route) | col, map / DEM (m) | Island -> gate, km (stades @177.6) | gate -> col, km (km/day in 9 d) | col -> plain (<400 m), km (km/day in 4 d) | gate -> plain, km (stades) vs Polybius 1200 | Po plain visible from the col | old snow at the col in late Oct (modern climate) |
|---|---|---|---|---|---|---|---|
| R1 Isère-Arc-**Mont-Cenis** | 2083 / 2088 | 158 (888) to Aiguebelle | 87 (9.7) | 32 (8.0) | 119 (670) = 56 % | no; 3 of 61 cells within 1.5 km see a sliver, the best 0.5 % of azimuths | very unlikely |
| R2 Isère-Arc-Savine-**Clapier** | 2482 / 2478 | 158 (888) to Aiguebelle | 86 (9.5) | 25 (6.2) | 111 (622) = 52 % | marginal: a 2-degree sliver from the col (0.6 % of azimuths, 80 km off); 4.9 % from 1.0 km down the descent; up to 8 % from the ridge 1.4 km away | unlikely; possible in shaded hollows |
| R2b Ambin-**Petit Mont-Cenis** | 2183 / 2180 | 158 (888) | 80 (8.8) | 35 (8.6) | 114 (642) = 54 % | no | very unlikely |
| R3 Isère-Tarentaise-**Petit-Saint-Bernard** | 2188 / 2190 | 169 (950) to Albertville | 64 (7.1) | 72 (17.9) | 135 (762) = 63 % | no | very unlikely |
| R4 Durance-**Montgenèvre** | 1854 / 1851 | 161 (908) to Sisteron | 132 (14.7) | 51 (12.8) | 184 (1033) = 86 % | no | nil |
| R5 Durance-Guil-**Traversette** | 2947 / 2913 | 161 (908) to Sisteron | 139 (15.4) | 28 (7.0) | 167 (939) = 78 % | **yes: 17 % of azimuths from the col, nearest plain 26 km; from every point of the first 2.25 km of descent; 22-26 % from the knolls beside the col** | possible to likely (within 100 m of the modern snowline) |
| R6 Durance-Ubaye-**Larche** | 1991 / 2002 | 161 (908) to Sisteron | 114 (12.6) | 79 (19.8) | 193 (1084) = 90 % | no | nil |
| R7 Rhône-Geneva-Valais-**Grand-Saint-Bernard** | 2469 / 2495 | 379 (2135) to Martigny | 37 (4.1) | 52 (12.9) | 89 (498) = 42 % | no | unlikely |
| Drôme approaches (R4c, R5c, R5g; gate Crest) | as above | 91 (512) | 222-237 (25-26) | as above | 257-274 (1446-1540) = 120-128 % | as above | as above |

Pleiades, 218 BC, 45 N, Julian calendar: true morning (cosmical) setting **29 October**; first visible morning setting **4-9 November** (arcus visionis 6-11 deg; 6 Nov at the conventional 7.5 deg). Two independent computations (Skyfield + JPL DE406; PyEphem) agree to the day; Columella (AD c. 60) has the Vergiliae "begin to set at sunrise" on 20/21 Oct, "set" on 28 Oct and "set in the morning" on 8 Nov.

What discriminates: (1) only two of the candidate cols see any of the Po plain at all: the Traversette broadly (17 % of azimuths from the col, 22-26 % from the knolls beside it, and from every point of the first 2.25 km of descent) and the Clapier marginally (a 2-degree sliver 80 km away from the col itself, 5 % from 1 km down the descent, 8 % from the ridge crest 1.4 km away); every other col is closed in, and of the 47-91 cells within 1.5 km of each and up to 300 m above it not one sees any plain, except three cells above the Mont-Cenis with a 0.5 % sliver; (2) with the Isère "Island" the 800-stade march ends exactly at the Combe de Savoie / Maurienne entrance (Montmélian-Aiguebelle, 136-158 km), with the Aygues "Island" and the Durance it ends at Sisteron (161 km) and with the Drôme it ends at the foot of the Col de Cabre (Luc-en-Diois, 145 km); (3) Polybius' 1200 stades for the Alps (213-222 km) is matched only by the Durance routes from Sisteron (78-104 %) and over-matched by the Drôme-Gap approaches (120-128 %); the Isère routes from the Maurienne entrance give only 52-63 %; (4) the Traversette, Clapier, Grand-Saint-Bernard and Mont-Cenis descents all contain 500-m stretches at 50 % or steeper; Montgenèvre, Larche and Petit-Saint-Bernard never exceed 23-29 %, i.e. they have nothing a landslip could have made impassable "for about 1.5 stades" with a 1000-foot drop; (5) a 9-day ascent at 4-16 km/day is slow-but-plausible for all routes from a gate, and the 4-day descent of 25-32 km (6-8 km/day) on Clapier / Traversette / Mont-Cenis is consistent with the three lost days of road-building, whereas the Petit-Saint-Bernard (72 km) and Larche (79 km) need 18-20 km/day downhill with a wrecked army.

None of this is a verdict; the resolution and the caveats are in section 8. The numbers were set out here so that the report can argue from them.

## 1. Data

**Elevation.** Copernicus DEM GLO-90 (ESA/Airbus, 2022 release on the AWS open-data bucket `copernicus-dem-90m`), 20 one-degree tiles N43-N46 x E004-E008, 3-arc-second grid (92.6 m north-south, 65.5 m east-west at 45 N), heights in metres above EGM2008, read with rasterio into one mosaic (`code/dem.py`, bilinear interpolation across tile edges). It is a surface model (canopy and buildings included; stated vertical accuracy < 4 m LE90). Check values: Col du Mont-Cenis 2088 m (map 2083), Montgenèvre 1853 (1854), Petit-Saint-Bernard 2189 (2188), Grand-Saint-Bernard 2472 (2469), Col de Larche 1996 (1991), Col Clapier 2479 (2482), Petit Mont-Cenis 2181 (2183), Col Agnel 2731 (2744), Col de la Traversette 2912 (2947: a notch 40 m narrower than a cell is smoothed), Turin 242 m, Fourques 6 m.

**Places.** 122 place names geocoded with Nominatim (`code/geocode.py`; the raw responses are kept in `data/geocode_cache.json`, the chosen point and its OSM id in `data/places.json`). Every point was checked against the DEM. Five commune centroids that Nominatim put on hillsides were replaced by the town on the valley floor (Aime 1336 -> 666 m; Vinadio 1975 -> 922; Argentera 2234 -> 1730; Châtillon 853 -> 519; Pont-Saint-Martin 1016 -> 333), and 17 points that are not places (river crossings, confluences, valley-floor points in the Val Clarea and on the Mont-Cenis plateau, Les Échelles) were placed by hand and DEM-checked; each carries the word "manual" in its `source` field in `data/routes.json`. Fourques (opposite Arles, 43.69 N) and Beaucaire-Tarascon (43.81 N) are 14 km apart along the river and are treated as separate crossing options. "Col de la Croix" (Colle della Croce, 2299 m on the maps) could not be located: Nominatim returns nothing and the lowest DEM crossing between the Guil and Pellice basins is 2496 m at 44.806 N 7.013 E, so it was left out (it was a completeness candidate only).

**Ancient text.** Distances and day-counts are those of Polybius 3.39.9-10, 3.49.5, 3.50.1, 3.53.9, 3.54.7, 3.55.7-8 and 3.56.3 (Greek from `texts/polybius_3_greek.txt`, PerseusDL) and Livy 21.35-36 (`texts/terrain_sources/livy_21_thelatinlibrary.txt`):

- 3.39.9 ἀπὸ δὲ τῆς διαβάσεως τοῦ Ῥοδανοῦ πορευομένοις παρ' αὐτὸν τὸν ποταμὸν ὡς ἐπὶ τὰς πηγὰς ἕως πρὸς τὴν ἀναβολὴν τῶν Ἄλπεων τὴν εἰς Ἰταλίαν χίλιοι τετρακόσιοι — "from the crossing of the Rhône, going along the river towards its sources, up to the beginning of the ascent of the Alps into Italy, 1400 [stades]".
- 3.39.10 λοιπαὶ δ' αἱ τῶν Ἄλπεων ὑπερβολαί, περὶ χιλίους διακοσίους· ἃς ὑπερβαλὼν ἔμελλεν ἥξειν εἰς τὰ περὶ τὸν Πάδον πεδία τῆς Ἰταλίας — "there remain the passes of the Alps, about 1200; crossing these he would come to the plains of the Po".
- 3.49.5 ποιησάμενος ἑξῆς ἐπὶ τέτταρας ἡμέρας τὴν πορείαν ἀπὸ τῆς διαβάσεως ἧκε πρὸς τὴν καλουμένην Νῆσον — "marching four days in succession from the crossing he came to the so-called Island", 3.49.6 bounded by the Rhône and the Ἰσάρας.
- 3.50.1 ἐν ἡμέραις δέκα πορευθεὶς παρὰ τὸν ποταμὸν εἰς ὀκτακοσίους σταδίους ἤρξατο τῆς πρὸς τὰς Ἄλπεις ἀναβολῆς — "in ten days, going along the river for 800 stades, he began the ascent of the Alps".
- 3.53.9 ἐναταῖος δὲ διανύσας εἰς τὰς ὑπερβολὰς ... καὶ δύ' ἡμέρας προσέμεινε — "on the ninth day he reached the summit of the pass ... and waited two days".
- 3.54.1 διὰ τὸ συνάπτειν τὴν τῆς Πλειάδος δύσιν — "because the setting of the Pleiades was near" (snow already gathering on the heights).
- 3.54.3 ἐνδεικνύμενος αὐτοῖς τὰ περὶ τὸν Πάδον πεδία ... ἅμα δὲ καὶ τὸν τῆς Ῥώμης αὐτῆς τόπον ὑποδεικνύων — "pointing out to them the plains of the Po ... and also indicating the direction of Rome itself".
- 3.54.7 σχεδὸν ἐπὶ τρί' ἡμιστάδια τῆς ἀπορρῶγος — the broken-away path "for about three half-stades" (1.5 stades = 266-278 m); 3.55.7-8 one day to make it passable for the pack animals and horses, three days for the elephants.
- 3.55.1 ἐπὶ γὰρ τὴν προϋπάρχουσαν χιόνα καὶ διαμεμενηκυῖαν ἐκ τοῦ πρότερον χειμῶνος ἄρτι τῆς ἐπ' ἔτους πεπτωκυίας — "on top of the old snow that had remained from the previous winter, this year's had just fallen"; 3.55.9 the summits are treeless "because snow lies on them continuously summer and winter".
- 3.56.3 τὴν δὲ τῶν Ἄλπεων ὑπερβολὴν ἡμέραις δεκαπέντε — "the crossing of the Alps in fifteen days".
- Livy 21.35.6 "nivis etiam casus, occidente iam sidere Vergiliarum"; 21.35.8 "in promunturio quodam, unde longe ac late prospectus erat, ... Italiam ostentat subiectosque Alpinis montibus Circumpadanos campos"; 21.36.2 "natura locus iam ante praeceps recenti lapsu terrae in pedum mille admodum altitudinem abruptus erat" (a fall of about 1000 feet = 296 m).

Stade: 177.6 m (Attic) and 185 m (the 8-stades-to-the-mile equivalence Polybius himself invokes at 3.39.8 for the Roman-measured road) are both carried through every table.

## 2. Method

**Routes as valley-floor paths.** Each candidate is a chain of 15-25 named waypoints (valley towns and the col). Between consecutive waypoints the line is not the straight chord but a least-cost path on the DEM grid (`code/routes.py`, A* search, 16-neighbour moves) with cost = horizontal distance + 8 x |height change| (a Naismith-type penalty, 8 m of walking per metre of climb or descent; cells steeper than 70 % cost four times more; no-data cells barred). On flat ground this is the straight line (Beaucaire -> Avignon 21.0 km against 20.3 straight); in a valley it stays on the floor and refuses to cut across spurs (Aiguebelle -> La Chambre 22.2 km against 20.5). The grid path is simplified (Douglas-Peucker, 100 m) and sampled every 250 m for the profile. The brief's chord test was also run: elevation sampled every 250 m along each straight chord, any sample more than 150 m above both endpoints flagged. 9-13 chords per route fail it (worst: Grenoble -> Pontcharra, 78 samples up to 860 m above the valley; Morgex -> Aosta up to 1600 m), which is why the least-cost path, not the chord, is used for every distance (`data/chord_check.csv`).

**Zigzag correction.** Where the ground is steeper than a mule track can take, the least-cost path still climbs the fall line (it minimises length + climb, not gradient). A second length replaces every 250-m step steeper than 25 % by a traverse at 25 % (`c_zigzag25_km`, `d_zigzag25_km`). It adds 0.3-2 km to the ascents and descents and does not change any conclusion; the 1-km and 500-m gradient statistics are taken from the fall-line profile and are therefore upper bounds for the ground and not estimates of the track.

**Segments.** (a) crossing -> Island: along the left bank of the Rhône; (b) Island -> beginning of the ascent; (c) ascent start -> col (highest profile sample within 1 km of the col waypoint); (d) col -> plain, the plain being the first profile sample below 400 m in the Po basin (Sant'Antonino di Susa at 45.127 N 7.220 E for the Dora Riparia routes; Revello/Envie 44.642 N 7.367 E for the Traversette; Fossano/Centallo 44.526 N 7.603 E for Larche; Pont-Saint-Martin/Ivrea 45.717 N 7.668 E for the Aosta routes); (e) ascent start -> plain. Three definitions of the "beginning of the ascent" are reported because the choice moves segment (b) by up to 100 km: **gate** (a named mountain gate: Aiguebelle where the Maurienne closes for R1/R2, Albertville for the Tarentaise, Sisteron for the Durance, Crest for the Drôme, Martigny for the Valais), **flat10** (the end of the last 10-km stretch of level valley, mean gradient < 0.5 %, before the col: the last point after which the route climbs without respite), and **z500** (first point above 500 m). Distances to every named waypoint are tabulated (Table E, `data/waypoint_distances.csv`) so any other definition can be applied.

**Daily rates.** Polybius' counts are applied literally: 4 days for (a); 10 days for (b); 9 days for (c); 2 days at the summit; 4 days (and 3) for (d); 15 days for the Alps of which 13 are marching days, for (e). Plausible band for an army with pack animals and elephants: 12-25 km/day on the flat, less in the mountains (Engels 1978 for Alexander's army; Brunanburh model in the Brunanburh case's `code/routes.py`).

**Viewshed** (`code/viewshed.py`). Rays at 0.25 deg azimuth steps (1440 rays) to 120 km, sampled every 90 m, positions by the spherical direct geodesic, elevation bilinear; Earth curvature with standard refraction, effective height z - (1 - k) d^2 / 2R with k = 0.13; observer 2 m above the surface; a sample is visible if its elevation angle is at least the running maximum of all nearer samples on the ray. Target "Po plain": DEM below 400 m, east of 7.3 E, north of 44.4 N. Computed from each col, from every 250 m of the first 3 km of descent and every km to 10 km, from the nearest ground 100 m and 300 m higher within 2.5 km, and (vantage scan) from every third cell within 1.5 km of the col that is 0-300 m above it. Because the DEM is a surface model, modern forest can only hide plain that would otherwise be visible; it cannot create a view.

**Snow and climate.** Col heights and the bearing of the first 2 km of descent from the DEM; modern snowline and snow-onset values from fetched sources (section 5); 3rd-century-BC glacier state from Holzhauser et al. 2005 and Le Roy, Ivy-Ochs et al. 2024 (texts saved under `texts/terrain_sources/`).

**Astronomy** (`code/pleiades.py`). Alcyone (Hipparcos position and proper motion) precessed to 218 BC (IAU 2006/2000A in Skyfield), Sun from JPL DE406 (the task's DE421 stops at 1900 and cannot be used); the phase falls on the day the star is on the mathematical horizon when the Sun's true altitude is -h (arcus visionis h = 6, 7.5, 9 deg as asked, plus Schoch's 11 deg for the Pleiades and the "true" event with the Sun's upper limb on the horizon); observer 45 N 7 E; proleptic Julian calendar; Delta-T from Skyfield's long-term tables (about 3.5 h in 218 BC, which cannot move a date by more than 0.15 day). An independent PyEphem computation (its own precession and Sun) reproduces every date.

## 3. Results: distances, stades and rates

### Table A. Key results per candidate (ascent start = named gate; distances along the valley-floor path)

| route | col (map m / DEM m) | Island -> gate km (stades 177.6 / 185) | gate -> col km (climb m) | km/day over 9 d | col -> plain km | km/day over 4 d (3 d) | gate -> plain km (stades 177.6 / 185) | km/day over 13 marching d | steepest 500 m on descent (% , km from col) | plain visible from col (% azimuths) |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 Isere - Arc (Maurienne) - Col du Mont-Cenis | du Mont-Cenis 2083 / 2088 | Aiguebelle 158 (888 / 853) | 87 (+1825) | 9.7 | 32 | 8.0 (10.7) | 119 (670 / 643) | 9.2 | 53% at 13.0 km | no (0.0%) |
| R2 Isere - Arc - Ambin/Savine - Col Clapier - Val Clarea | Clapier 2482 / 2478 | Aiguebelle 158 (888 / 853) | 86 (+2209) | 9.5 | 25 | 6.2 (8.3) | 110 (622 / 597) | 8.5 | 50% at 1.0 km | yes (0.6%) |
| R2b Isere - Arc - Ambin - Col du Petit Mont-Cenis - Mont-Cenis plateau | du Petit Mont-Cenis 2183 / 2180 | Aiguebelle 158 (888 / 853) | 80 (+1842) | 8.8 | 34 | 8.6 (11.5) | 114 (642 / 616) | 8.8 | 54% at 15.2 km | no (0.0%) |
| R3 Isere - Tarentaise - Col du Petit-Saint-Bernard - Aosta - Ivrea | du Petit-Saint-Bernard 2188 / 2190 | Albertville 169 (950 / 912) | 64 (+1937) | 7.1 | 72 | 17.9 (23.9) | 135 (762 / 731) | 10.4 | 29% at 12.2 km | no (0.0%) |
| R4 Durance (direct from Avignon) - Briancon - Col de Montgenevre - Susa | de Montgenevre 1854 / 1851 | Sisteron 161 (908 / 872) | 132 (+1722) | 14.7 | 51 | 12.8 (17.1) | 184 (1033 / 992) | 14.1 | 23% at 5.0 km | no (0.0%) |
| R4c Rhone - Drome - Col de Cabre - Gap - Durance - Col de Montgenevre (Livy/de Beer approach) | de Montgenevre 1854 / 1852 | Crest 91 (512 / 492) | 222 (+2894) | 24.7 | 51 | 12.8 (17.1) | 274 (1540 / 1478) | 21.0 | 25% at 5.0 km | no (0.0%) |
| R5 Durance (direct) - Guil - Col de la Traversette - Po (Saluzzo) | de la Traversette 2947 / 2913 | Sisteron 161 (908 / 872) | 139 (+2687) | 15.4 | 28 | 7.0 (9.3) | 167 (939 / 901) | 12.8 | 51% at 0.5 km | yes (17.3%) |
| R5g Rhone - Drome - Col de Grimone - Gap - Durance - Guil - Traversette (de Beer 1955) | de la Traversette 2947 / 2924 | Crest 91 (512 / 492) | 237 (+3980) | 26.4 | 28 | 7.1 (9.4) | 266 (1495 / 1435) | 20.4 | 51% at 0.0 km | yes (17.3%) |
| R5c Rhone - Drome - Col de Cabre - Gap - Durance - Guil - Traversette | de la Traversette 2947 / 2883 | Crest 91 (512 / 492) | 228 (+3823) | 25.4 | 28 | 7.1 (9.4) | 257 (1446 / 1388) | 19.8 | 50% at 0.8 km | yes (17.3%) |
| R6 Durance (direct) - Ubaye - Col de Larche - Stura - Cuneo | de Larche 1991 / 2002 | Sisteron 161 (908 / 872) | 114 (+1601) | 12.6 | 79 | 19.8 (26.3) | 192 (1084 / 1041) | 14.8 | 23% at 4.0 km | no (0.0%) |
| R6v Durance (direct) - Guillestre - Col de Vars - Ubaye - Col de Larche - Cuneo | de Larche 1991 / 2002 | Sisteron 161 (908 / 872) | 143 (+2603) | 15.9 | 79 | 19.8 (26.3) | 222 (1251 / 1201) | 17.1 | 23% at 4.0 km | no (0.0%) |
| R7 Rhone - Lyon - Geneva - Valais - Col du Grand-Saint-Bernard - Aosta - Ivrea | du Grand-Saint-Bernard 2469 / 2495 | Martigny 379 (2135 / 2050) | 37 (+1954) | 4.1 | 52 | 12.9 (17.2) | 88 (498 / 478) | 6.8 | 54% at 1.8 km | no (0.0%) |

### Table B. Sensitivity to the definition of the 'beginning of the ascent'

| route | definition | start (m, km from Island) | b: Island->start km (stades 177.6) | c: start->col km, zigzag-corrected km, km/day/9d | e: start->plain km (stades 177.6), km/day/13d |
|---|---|---|---|---|---|
| R1 | gate:Aiguebelle | 326 m, 158 km | 158 (888) | 87, 88, 9.7 | 119 (670), 9.2 |
| R1 | flat10 | 1281 m, 236 km | 236 (1326) | 9, 10, 1.1 | 41 (232), 3.2 |
| R1 | z500 | 501 m, 187 km | 187 (1052) | 58, 59, 6.5 | 90 (507), 6.9 |
| R2 | gate:Aiguebelle | 326 m, 158 km | 158 (888) | 86, 86, 9.5 | 110 (622), 8.5 |
| R2 | flat10 | 459 m, 182 km | 182 (1028) | 61, 61, 6.8 | 86 (483), 6.6 |
| R2 | z500 | 501 m, 187 km | 187 (1052) | 56, 57, 6.3 | 82 (459), 6.3 |
| R2b | gate:Aiguebelle | 326 m, 158 km | 158 (888) | 80, 80, 8.9 | 114 (642), 8.8 |
| R2b | flat10 | 459 m, 182 km | 182 (1028) | 55, 56, 6.2 | 89 (503), 6.9 |
| R2b | z500 | 501 m, 187 km | 187 (1052) | 50, 51, 5.7 | 85 (479), 6.5 |
| R3 | gate:Albertville | 346 m, 169 km | 169 (950) | 64, 64, 7.1 | 135 (762), 10.4 |
| R3 | flat10 | 697 m, 210 km | 210 (1182) | 22, 23, 2.5 | 94 (529), 7.2 |
| R3 | z500 | 504 m, 193 km | 193 (1088) | 39, 40, 4.4 | 111 (624), 8.5 |
| R4 | gate:Sisteron | 494 m, 161 km | 161 (908) | 132, 133, 14.7 | 184 (1033), 14.1 |
| R4 | flat10 | 939 m, 267 km | 267 (1505) | 26, 27, 2.9 | 78 (436), 6.0 |
| R4 | z500 | 517 m, 146 km | 146 (819) | 148, 148, 16.5 | 199 (1122), 15.3 |
| R4c | gate:Crest | 199 m, 91 km | 91 (512) | 222, 223, 24.7 | 274 (1540), 21.0 |
| R4c | flat10 | 939 m, 287 km | 287 (1616) | 26, 26, 2.9 | 78 (436), 6.0 |
| R4c | z500 | 500 m, 140 km | 140 (790) | 173, 173, 19.3 | 224 (1263), 17.2 |
| R5 | gate:Sisteron | 494 m, 161 km | 161 (908) | 139, 139, 15.5 | 167 (939), 12.8 |
| R5 | flat10 | 875 m, 248 km | 248 (1394) | 52, 53, 5.9 | 80 (453), 6.2 |
| R5 | z500 | 517 m, 146 km | 146 (819) | 154, 155, 17.2 | 182 (1028), 14.0 |
| R5g | gate:Crest | 199 m, 91 km | 91 (512) | 237, 238, 26.5 | 266 (1495), 20.4 |
| R5g | flat10 | 870 m, 277 km | 277 (1558) | 52, 52, 5.8 | 80 (449), 6.1 |
| R5g | z500 | 509 m, 135 km | 135 (760) | 193, 194, 21.6 | 222 (1247), 17.0 |
| R5c | gate:Crest | 199 m, 91 km | 91 (512) | 228, 229, 25.5 | 257 (1446), 19.8 |
| R5c | flat10 | 871 m, 268 km | 268 (1509) | 52, 52, 5.8 | 80 (449), 6.1 |
| R5c | z500 | 500 m, 140 km | 140 (790) | 179, 180, 20.0 | 208 (1168), 16.0 |
| R6 | gate:Sisteron | 494 m, 161 km | 161 (908) | 114, 114, 12.6 | 192 (1084), 14.8 |
| R6 | flat10 | 822 m, 225 km | 225 (1267) | 50, 50, 5.5 | 129 (725), 9.9 |
| R6 | z500 | 517 m, 146 km | 146 (819) | 129, 129, 14.4 | 208 (1173), 16.0 |
| R6v | gate:Sisteron | 494 m, 161 km | 161 (908) | 143, 143, 15.9 | 222 (1251), 17.1 |
| R6v | flat10 | 1306 m, 292 km | 292 (1643) | 13, 13, 1.4 | 92 (517), 7.1 |
| R6v | z500 | 517 m, 146 km | 146 (819) | 159, 159, 17.7 | 238 (1340), 18.3 |
| R7 | gate:Martigny | 474 m, 379 km | 379 (2135) | 37, 37, 4.1 | 88 (498), 6.8 |
| R7 | flat10 | 496 m, 381 km | 381 (2145) | 35, 35, 3.9 | 87 (488), 6.7 |
| R7 | z500 | 556 m, 180 km | 180 (1014) | 236, 236, 26.3 | 288 (1620), 22.1 |

### Table C. Rhone crossing -> 'Island' (Polybius 3.49.5: four days' march)

| leg | km along valley | km straight | stades (177.6 / 185) | km/day over 4 days | band 12-25 |
|---|---|---|---|---|---|
| Fourques/Arles -> Island (ii) Aygues | 57 | 50 | 321 / 308 | 14.2 | in band |
| Beaucaire-Tarascon -> Island (ii) Aygues | 42 | 35 | 239 / 229 | 10.6 | slow |
| Roquemaure -> Island (ii) Aygues | 9 | 9 | 49 / 47 | 2.2 | slow |
| Fourques/Arles -> Island (i) Isere | 159 | 147 | 894 / 858 | 39.7 | fast |
| Beaucaire-Tarascon -> Island (i) Isere | 144 | 132 | 812 / 780 | 36.1 | fast |
| Roquemaure -> Island (i) Isere | 111 | 105 | 623 / 598 | 27.6 | fast |
| Beaucaire-Tarascon -> Drome confluence (Loriol) | 117 | 106 | 657 / 631 | 29.2 | fast |

### Table D. Where 800 stades from the Island falls (Polybius 3.50.1) and the straight-line ('crow') distances

| route | 800 st @177.6 m = 142.1 km falls at | 800 st @185 m = 148.0 km falls at | Island->gate straight km | gate->col straight km | col->plain straight km | gate->plain straight km |
|---|---|---|---|---|---|---|
| R1 | 45.532N 6.124E (274 m; nearest waypoint Montmelian at 136 km) | 45.555N 6.191E (nearest Aiguebelle at 158 km) | 129 | 56 | 29 | 85 |
| R2 | 45.532N 6.124E (274 m; nearest waypoint Montmelian at 136 km) | 45.555N 6.191E (nearest Aiguebelle at 158 km) | 129 | 64 | 24 | 85 |
| R2b | 45.532N 6.124E (274 m; nearest waypoint Montmelian at 136 km) | 45.555N 6.191E (nearest Aiguebelle at 158 km) | 129 | 57 | 29 | 85 |
| R3 | 45.532N 6.123E (273 m; nearest waypoint Montmelian at 136 km) | 45.560N 6.190E (nearest Montmelian at 136 km) | 143 | 38 | 61 | 99 |
| R4 | 44.031N 5.946E (395 m; nearest waypoint Sisteron at 161 km) | 44.082N 5.950E (nearest Sisteron at 161 km) | 97 | 102 | 45 | 144 |
| R4c | 44.634N 5.435E (520 m; nearest waypoint Luc-en-Diois at 144 km) | 44.590N 5.473E (nearest Luc-en-Diois at 144 km) | 72 | 136 | 45 | 179 |
| R5 | 44.031N 5.946E (395 m; nearest waypoint Sisteron at 161 km) | 44.082N 5.950E (nearest Sisteron at 161 km) | 97 | 106 | 25 | 123 |
| R5g | 44.691N 5.500E (571 m; nearest waypoint Die at 127 km) | 44.673N 5.559E (nearest Col de Grimone at 157 km) | 72 | 161 | 25 | 186 |
| R5c | 44.634N 5.435E (520 m; nearest waypoint Luc-en-Diois at 144 km) | 44.590N 5.473E (nearest Luc-en-Diois at 144 km) | 72 | 161 | 25 | 186 |
| R6 | 44.031N 5.946E (395 m; nearest waypoint Sisteron at 161 km) | 44.082N 5.950E (nearest Sisteron at 161 km) | 97 | 80 | 57 | 137 |
| R6v | 44.031N 5.946E (395 m; nearest waypoint Sisteron at 161 km) | 44.082N 5.950E (nearest Sisteron at 161 km) | 97 | 80 | 57 | 137 |
| R7 | 45.563N 5.399E (305 m; nearest waypoint Bourgoin-Jallieu at 132 km) | 45.561N 5.473E (nearest Bourgoin-Jallieu at 132 km) | 213 | 27 | 42 | 63 |

### Table E. Cumulative distance from the Island at named points (km; stades at 177.6 m in brackets)

- **R1**: Grenoble 91.3 (514); Montmelian 135.9 (765); Aiguebelle 157.8 (888); Saint-Jean-de-Maurienne 190.4 (1072); Modane 219.9 (1238); Lanslebourg 241.4 (1359); Col du Mont-Cenis 244.8 (1378); Susa 263.0 (1481); Turin 315.4 (1776)
- **R2**: Modane 219.9 (1238); Bramans 229.3 (1291); Le Planay (Bramans) 234.6 (1321); Lac Savine 242.2 (1364); Col Clapier 243.3 (1370); Giaglione 251.7 (1417); Susa 254.4 (1433); Turin 306.8 (1728)
- **R3**: Montmelian 135.9 (765); Albertville 168.7 (950); Moutiers 194.4 (1095); Bourg-Saint-Maurice 220.5 (1241); Col du Petit-Saint-Bernard 232.1 (1307); Aosta 274.7 (1547); Ivrea 340.9 (1919); Turin 391.4 (2204)
- **R4**: Avignon 20.7 (117); Cavaillon 43.8 (246); Manosque 115.1 (648); Sisteron 161.2 (908); Tallard 195.1 (1099); Embrun 236.4 (1331); Guillestre 254.4 (1433); L'Argentiere-la-Bessee 271.7 (1530); Briancon 286.0 (1610); Col de Montgenevre 293.7 (1654); Susa 331.0 (1864); Turin 383.4 (2159)
- **R4c**: Loriol 74.4 (419); Crest 91.1 (513); Die 127.4 (717); Luc-en-Diois 144.5 (814); Col de Cabre 161.1 (907); Gap 203.0 (1143); Tallard 214.8 (1209); Guillestre 274.1 (1543); Briancon 305.6 (1721); Col de Montgenevre 313.4 (1764); Turin 403.0 (2269)
- **R5**: Sisteron 161.2 (908); Tallard 195.1 (1099); Guillestre 254.4 (1433); Abries 283.0 (1593); Refuge du Viso 298.3 (1679); Col de la Traversette 300.0 (1689); Pian del Re 302.7 (1704); Paesana 317.3 (1787); Saluzzo 338.1 (1904); Turin 392.1 (2208)
- **R5g**: Loriol 74.4 (419); Crest 91.1 (513); Die 127.4 (717); Col de Grimone 156.8 (883); Gap 211.7 (1192); Guillestre 282.7 (1592); Col de la Traversette 328.3 (1849); Saluzzo 366.4 (2063); Turin 420.4 (2367)
- **R6**: Sisteron 161.2 (908); Tallard 195.1 (1099); Le Lauzet-Ubaye 228.2 (1285); Barcelonnette 247.4 (1393); Jausiers 255.4 (1438); Col de Larche 275.0 (1548); Vinadio 302.7 (1704); Cuneo 337.9 (1903); Savigliano 367.6 (2070); Turin 416.0 (2342)
- **R7**: Lyon 91.7 (516); Les Echelles 176.7 (995); Geneva 275.7 (1552); Martigny 379.2 (2135); Col du Grand-Saint-Bernard 416.2 (2344); Aosta 438.4 (2468); Ivrea 504.6 (2841); Turin 555.1 (3126)

### Table F. Viewshed of the Po plain (viewshed.py; plain = DEM < 400 m, east of 7.3E, north of 44.4N; 0.25 deg rays to 120 km; k = 0.13; observer 2 m)

| col | DEM height (m) | from the col: plain visible, % of azimuths, nearest plain km | first point on the descent with plain visible (km from col; % az) | +100 m knoll | +300 m knoll | vantage scan: cells <=1.5 km & <=300 m above seeing plain / scanned; best % az (height, distance) |
|---|---|---|---|---|---|---|
| Col du Mont-Cenis | 2088 | no, 0.0%, - | none within 10 km | no 0.0% (2197 m, 370 m away) | yes 0.2% (2394 m, 767 m away) | 3 / 61; best 0.5% (2383 m, 1053 m away) |
| Col Clapier | 2479 | yes, 0.6%, 80 km | 1.00 km; 4.9% | no 0.0% (2580 m, 290 m away) | no 0.0% (2795 m, 661 m away) | 29 / 56; best 8.1% (2712 m, 1400 m away) |
| Col du Petit Mont-Cenis | 2181 | no, 0.0%, - | none within 10 km | no 0.0% (2296 m, 458 m away) | no 0.0% (2567 m, 770 m away) | 0 / 57; best 0.0% (2456 m, 1496 m away) |
| Col du Petit-Saint-Bernard | 2189 | no, 0.0%, - | none within 10 km | no 0.0% (2303 m, 404 m away) | no 0.0% (2512 m, 1009 m away) | 0 / 89; best 0.0% (2288 m, 1489 m away) |
| Col de Montgenevre | 1853 | no, 0.0%, - | none within 10 km | no 0.0% (1956 m, 387 m away) | no 0.0% (2156 m, 1090 m away) | 0 / 91; best 0.0% (2142 m, 1253 m away) |
| Col de la Traversette | 2912 | yes, 17.3%, 26 km | 0.25 km; 11.5% | yes 21.7% (3048 m, 220 m away) | none within 2.5 km | 14 / 18; best 25.6% (3001 m, 960 m away) |
| Col de Larche | 1996 | no, 0.0%, - | none within 10 km | no 0.0% (2098 m, 420 m away) | no 0.0% (2298 m, 847 m away) | 0 / 68; best 0.0% (2132 m, 1475 m away) |
| Col du Grand-Saint-Bernard | 2472 | no, 0.0%, - | none within 10 km | no 0.0% (2576 m, 201 m away) | no 0.0% (2780 m, 643 m away) | 0 / 57; best 0.0% (2753 m, 1419 m away) |
| Col Agnel | 2731 | no, 0.0%, - | n/a (not on a modelled route) | no 0.0% (2833 m, 564 m away) | no 0.0% (3056 m, 1283 m away) | 0 / 47; best 0.0% (2736 m, 1246 m away) |

### Table H. Rhone crossing -> Po plain in total, against Polybius 3.39.9-10 (1400 + 1200 = 2600 stades = 462 km at 177.6 m, 481 km at 185 m)

| route | Island | crossing option | crossing->Island km | Island->plain km | total km | total stades (177.6 / 185) | % of 2600 st (177.6) |
|---|---|---|---|---|---|---|---|
| R1 | Isere | Fourques/Arles | 159 | 277 | 436 | 2453 / 2354 | 94% |
| R1 | Isere | Beaucaire-Tarascon | 144 | 277 | 421 | 2370 / 2275 | 91% |
| R1 | Isere | Roquemaure | 111 | 277 | 387 | 2181 / 2094 | 84% |
| R2 | Isere | Fourques/Arles | 159 | 268 | 427 | 2405 / 2308 | 92% |
| R2 | Isere | Beaucaire-Tarascon | 144 | 268 | 412 | 2322 / 2230 | 89% |
| R2 | Isere | Roquemaure | 111 | 268 | 379 | 2133 / 2048 | 82% |
| R2b | Isere | Fourques/Arles | 159 | 272 | 431 | 2424 / 2327 | 93% |
| R2b | Isere | Beaucaire-Tarascon | 144 | 272 | 416 | 2342 / 2248 | 90% |
| R2b | Isere | Roquemaure | 111 | 272 | 382 | 2153 / 2067 | 83% |
| R3 | Isere | Fourques/Arles | 159 | 304 | 463 | 2606 / 2502 | 100% |
| R3 | Isere | Beaucaire-Tarascon | 144 | 304 | 448 | 2524 / 2423 | 97% |
| R3 | Isere | Roquemaure | 111 | 304 | 415 | 2334 / 2241 | 90% |
| R4 | Aygues | Fourques/Arles | 57 | 345 | 402 | 2262 / 2172 | 87% |
| R4 | Aygues | Beaucaire-Tarascon | 42 | 345 | 387 | 2180 / 2093 | 84% |
| R4 | Aygues | Roquemaure | 9 | 345 | 354 | 1990 / 1911 | 77% |
| R4c | Aygues | Fourques/Arles | 57 | 364 | 421 | 2373 / 2278 | 91% |
| R4c | Aygues | Beaucaire-Tarascon | 42 | 364 | 407 | 2291 / 2199 | 88% |
| R4c | Aygues | Roquemaure | 9 | 364 | 373 | 2102 / 2018 | 81% |
| R5 | Aygues | Fourques/Arles | 57 | 328 | 385 | 2168 / 2081 | 83% |
| R5 | Aygues | Beaucaire-Tarascon | 42 | 328 | 370 | 2085 / 2002 | 80% |
| R5 | Aygues | Roquemaure | 9 | 328 | 337 | 1896 / 1820 | 73% |
| R5g | Aygues | Fourques/Arles | 57 | 356 | 413 | 2328 / 2235 | 90% |
| R5g | Aygues | Beaucaire-Tarascon | 42 | 356 | 399 | 2246 / 2156 | 86% |
| R5g | Aygues | Roquemaure | 9 | 356 | 365 | 2057 / 1974 | 79% |
| R5c | Aygues | Fourques/Arles | 57 | 348 | 405 | 2279 / 2188 | 88% |
| R5c | Aygues | Beaucaire-Tarascon | 42 | 348 | 390 | 2197 / 2109 | 84% |
| R5c | Aygues | Roquemaure | 9 | 348 | 357 | 2007 / 1927 | 77% |
| R6 | Aygues | Fourques/Arles | 57 | 354 | 411 | 2313 / 2220 | 89% |
| R6 | Aygues | Beaucaire-Tarascon | 42 | 354 | 396 | 2230 / 2141 | 86% |
| R6 | Aygues | Roquemaure | 9 | 354 | 363 | 2041 / 1959 | 79% |
| R6v | Aygues | Fourques/Arles | 57 | 384 | 440 | 2480 / 2381 | 95% |
| R6v | Aygues | Beaucaire-Tarascon | 42 | 384 | 426 | 2398 / 2302 | 92% |
| R6v | Aygues | Roquemaure | 9 | 384 | 392 | 2209 / 2120 | 85% |
| R7 | Isere | Fourques/Arles | 159 | 468 | 627 | 3528 / 3387 | 136% |
| R7 | Isere | Beaucaire-Tarascon | 144 | 468 | 612 | 3446 / 3308 | 133% |
| R7 | Isere | Roquemaure | 111 | 468 | 578 | 3256 / 3126 | 125% |

### Table G. Pleiades (Alcyone) phases in 218 BC at 45 N, proleptic Julian calendar (pleiades.py)

| event | sun -0.833 (true) | h = 6 | h = 7.5 | h = 9 | h = 11 (Schoch) | pyephem cross-check agrees |
|---|---|---|---|---|---|---|
| morning setting | 29 Oct 218 BC | 4 Nov 218 BC | 6 Nov 218 BC | 7 Nov 218 BC | 9 Nov 218 BC | yes |
| evening setting | 24 Apr 218 BC | 18 Apr 218 BC | 16 Apr 218 BC | 15 Apr 218 BC | 12 Apr 218 BC | yes |
| acronychal rising | 14 Oct 218 BC | 30 Sep 218 BC | 25 Sep 218 BC | 21 Sep 218 BC | 15 Sep 218 BC | yes |
| heliacal rising | 17 Apr 218 BC | 2 May 218 BC | 6 May 218 BC | 11 May 218 BC | 17 May 218 BC | yes |

### 3.1 Reading the tables

**The Rhône leg (Table C).** Polybius' own arithmetic makes crossing -> Island 1400 - 800 = 600 stades = 107-111 km. The valley-floor distance from Roquemaure to the Isère confluence is 111 km (623 stades; 27.6 km/day for four days) and from Beaucaire to the Drôme confluence 117 km (657 stades); from Beaucaire/Tarascon to the Isère it is 144 km (812 stades, 36 km/day), from Fourques 159 km (40 km/day). The Aygues confluence is 42 km from Beaucaire (239 stades; 10.6 km/day) and 57 km from Fourques (321 stades; 14.2 km/day). So the Isère Island fits the 600 stades only with a crossing north of Avignon (Roquemaure/Orange), the Aygues Island fits the four days only with a crossing at or south of Beaucaire and a very slow march, and the Drôme confluence fits the distance from Beaucaire but is not a river Polybius names. These are the numbers behind the old dispute; the model does not settle which river is the Skaras/Isaras.

**800 stades from the Island (Tables A, D, E).** Along the Isère, 142-148 km ends between Montmélian (136 km) and Aiguebelle (158 km): the point where the Combe de Savoie ends and the Maurienne closes, which is the "first ascent" of the Mont-Cenis and Clapier theories and equally the turn into the Tarentaise (Albertville, 169 km). From the Aygues Island down to Avignon and up the Durance, 142-148 km ends 13-19 km short of Sisteron (161 km), the gate of the Durance. From the Aygues Island up the Rhône and the Drôme, it ends at Luc-en-Diois (145 km), the foot of the Col de Cabre, or (via Grimone) between Die and the col. Every school can therefore claim the 800 stades to within 10-15 %; the figure discriminates only against the Grand-Saint-Bernard, whose "ascent" begins 379 km from the Isère.

**The Alps (Table A, B, H).** Polybius' 1200 stades (213-222 km) from the beginning of the ascent to the plain: Sisteron -> plain is 184 km by the Montgenèvre (86 %), 193 km by Larche (90 %), 167 km by the Traversette (78 %), 222 km by Vars-Larche (104 %); Aiguebelle -> plain is 111-119 km by Clapier/Mont-Cenis (52-56 %); Albertville -> plain by the Petit-Saint-Bernard 135 km (63 %); Martigny -> plain 89 km (42 %); Crest -> plain by the Drôme-Gap approaches 257-274 km (120-128 %). Taking the crossing -> plain total instead (2600 stades = 462-481 km, Table H) the best fits are Beaucaire -> Isère -> Petit-Saint-Bernard -> Ivrea (448 km, 97 %), Roquemaure -> Isère -> Mont-Cenis or Clapier (~390 km, 84 %), Beaucaire -> Aygues -> Drôme-Gap -> Traversette (398 km, 86 %) and Beaucaire -> Aygues -> Durance -> Larche (396 km, 86 %); the direct Durance-Traversette total is 370 km (80 %). In other words Polybius' two figures cannot both be satisfied by any single line: the routes that fit 1200 stades for the Alps (Durance) fail the 600 stades to the Island or the 4 days, and the routes that fit the Island (Isère) give an Alpine crossing barely half of 1200 stades. This is a property of the text, not of the terrain, and the report should say so before it uses either figure against a candidate.

**Days and rates (Table A).** Nine days from the gate to the col: 4-16 km/day for every route with a gate (R7 4.1; R3 7.1; R2b 8.8; R2 9.5; R1 9.7; R6 12.6; R4 14.7; R5 15.4), slow but not impossible for an army fighting its way up (Polybius has a battle on day 1, a captured town, a day's halt, an ambush on day 4 and a night on a bare rock: 3.50-53). The Drôme approaches need 25-26 km/day for nine days including two cols (Cabre 1180 m or Grimone 1318 m) and the whole upper Durance, which is outside the band. The four-day descent to the plain: 6-9 km/day for Clapier (25 km), Traversette (28 km), Mont-Cenis (32 km) and Petit Mont-Cenis (35 km), 13 km/day for Montgenèvre (51 km) and the Grand-Saint-Bernard (52 km), 18-20 km/day for the Petit-Saint-Bernard (72 km to Pont-Saint-Martin) and Larche (79 km to the Fossano plain). Since Polybius spends one day plus three on the broken path (3.55.7-8) and the elephants "in a bad way from hunger", a 4-day descent that has to cover 72-79 km at 18-20 km/day after those losses is hard to credit; 25-35 km is easy. If instead one lets the descent run to the first Gallic villages rather than to the 400-m plain, the difference between the short-descent cols and the long-descent cols remains, because it is the length of the confined valley below the col that differs (Val Clarea/Susa 25-32 km against the Aosta valley 72 km and the Stura 79 km).

### 3.2 Gradients and the broken path

Fall-line gradients over 1-km windows on the ascent from the gate: 39 % (R1, the direct slope above Lanslebourg; the old road did 7 % in hairpins), 26 % (R2), 27 % (R3), 24 % (R4), 34-36 % (R5, the last 1.7 km above the Refuge du Viso climb 450 m), 12-14 % (R6), 25 % (R7). Steepest 500-m window on the descent, in fall-line terms: Mont-Cenis 53 % at 13.0 km from the col (the Ramasse drop from the plateau to Novalesa, after 13 km of near-level plateau), Petit Mont-Cenis 54 % at 15 km, Clapier 50 % at 1.0 km (the Clarea headwall), Traversette 51 % at 0.5 km (the east face down to Pian del Re; 900 m lost in 2.7 km), Grand-Saint-Bernard 54 % at 1.75 km; Petit-Saint-Bernard 29 % at 12 km, Montgenèvre 23 % at 5 km, Larche 23 % at 4 km. Polybius' broken path (1.5 stades = 270 m of path, Livy's 1000-foot precipice) requires ground where a mule track hangs above a drop: at 90-m resolution such ground exists on the first kilometre below Clapier, the Traversette and the Grand-Saint-Bernard, 13-15 km below the Mont-Cenis and Petit Mont-Cenis, and does not exist on Montgenèvre, Larche or the Petit-Saint-Bernard descents. The DEM can say where a landslip could have blocked a ledge; it cannot say whether one did in 218 BC (brief, rule 5).

Cumulative climb from gate to plain (5-sample smoothing, so a lower bound): R1 1861 m, R2 2215, R2b 1929, R3 2071, R4 1793, R5 2855, R6 1797, R7 2095; the Drôme approaches add the Cabre/Grimone cols and the Buëch: R4c 2956, R5c 4011, R5g 4153 m.

## 4. Viewshed: Polybius 3.54.3 and Livy 21.35.8

Table F is the result. In words:

- **Col de la Traversette (2947 m).** The plain is in sight from the col itself over 17 % of the azimuths (a 63-degree sector from 60 to 123 deg, i.e. east-north-east to east-south-east), nearest plain cell 26 km away (the Po at Revello/Saluzzo), farthest 120 km (the Vercelli plain at the edge of the DEM), and from every 250-m point of the first 2.25 km of descent (11.5 % at 0.25 km, falling to 2 % at 2.25 km; the Pian del Re basin floor at 2.5-3 km is blind; the view reopens from 4 to 8 km). The nearest ground 100 m higher (3048 m, 220 m from the col) sees 22 %; of 18 cells within 1.5 km and up to 300 m above the col, 14 see the plain, the best 26 % (3001 m, 960 m from the col). This is the only candidate whose view matches both authors without special pleading: "pointing out the plains of the Po" from the summit, and a "promontory with a wide view" in the first hour of the descent.
- **Col Clapier (2482 m).** From the col itself only a 2-degree sliver (0.6 % of azimuths, at 111-113 deg) of plain 80 km away beyond Turin, through the Val Clarea notch; nothing from the +100 m and +300 m knolls; from the descent, 4.9 % at 1.0 km and 2 % at 1.25 km (the lip of the Clarea headwall), then nothing until 6-10 km (1 % or less). The vantage scan is more generous: 29 of 56 cells within 1.5 km and up to 300 m above the col see some plain, the best 8 % from the ridge at 2712 m, 1.4 km from the col. So the Clapier can support Livy's promontory on the descent and, with a climb, a modest view; it does not give Polybius' panorama from the summit itself.
- **Mont-Cenis (2083 m).** Nothing from the col, nothing from any of the 19 descent points to 10 km, nothing from the +100 m knoll, 0.2 % from the +300 m knoll, and of 61 cells within 1.5 km and up to 300 m above the col only 3 see any plain, the best 0.5 % of azimuths (a sliver through the Susa gap from 2383 m, 1 km from the col). The Mont-Cenis plateau is a closed basin; the famous view over the Susa valley is from the plateau's south-east rim above the Ramasse, 12 km beyond the col.
- **Petit Mont-Cenis, Montgenèvre, Larche, Petit-Saint-Bernard, Grand-Saint-Bernard, Col Agnel.** Nothing from the col, nothing within 10 km of descent, nothing from the +100 m and +300 m knolls, and the vantage scans (47-91 cells each within 1.5 km and up to 300 m above the col) find not one cell that sees any plain (Table F).

The Livy passage does not require the summit itself, only a promontory reached on the descent "prima luce" of the morning after the two-day halt; at 6-9 km/day the army's first descent morning covers 1-3 km, which is the stretch the descent-point test covers. The test is robust to the 400-m threshold (raising it to 500 m adds the Cuneo plateau and the Canavese hills but changes no "no" to a "yes" for the closed cols, whose horizons are ridges of 2500-3500 m) and to refraction (k from 0 to 0.2 moves the far horizon by a few km without opening any new sector). It is not robust to the assumption that the col point is the observer: a general with a day to spare could walk further than 1.5 km. The vantage scan should be read as "no view within an hour's walk of the col", not "no view anywhere on the massif" (`data/viewshed_output.json` has every point tested).

## 5. Snow

### 5.1 Cols, heights and the descent's exposure

| col | map height | DEM height | bearing of the first 2 km of descent (from `routes.json`) | descent side faces |
|---|---|---|---|---|
| Col de la Traversette | 2947 | 2913 | 114 deg | east-south-east (Pian del Re) |
| Col Agnel | 2744 | 2731 | (not routed) | east (Val Varaita) |
| Col Clapier | 2482 | 2478 | 106 deg | east-south-east (Val Clarea) |
| Col du Grand-Saint-Bernard | 2469 | 2495 | 192 deg | south (Saint-Rhémy) |
| Col du Petit-Saint-Bernard | 2188 | 2190 | 37 deg | north-east (La Thuile) |
| Col du Petit Mont-Cenis | 2183 | 2180 | 51 deg | north-east onto the Mont-Cenis plateau |
| Col du Mont-Cenis | 2083 | 2088 | 141 deg | south-east across the plateau, then the Ramasse |
| Col de Larche | 1991 | 2002 | 134 deg | south-east (Argentera) |
| Col de Montgenèvre | 1854 | 1851 | 69 deg | east-north-east (Clavière) |

### 5.2 Modern climatological reference points (fetched sources)

- **Regional snowline / equilibrium line.** Rabatel, Letréguilly, Dedieu & Eckert 2013, *The Cryosphere* 7, 1455-1471, doi:10.5194/tc-7-1455-2013 (open access; text in `texts/terrain_sources/rabatel_etal_2013_cryosphere_ELA_western_alps.txt`): end-of-summer snowline (= ELA) of 43 glaciers of the French western Alps 1984-2010: "the average ELA for the whole period was located at 3035 ± 120 m a.s.l."; "the difference between extreme years was as high as 460 m, with the lowest average ELA measured in 1984 (2790 ± 180 m a.s.l.), and the highest average ELA measured in 2003 (3250 ± 135 m a.s.l.)"; the ELA rose "by about 170 m" over the period; sensitivity to summer temperature "115 m °C-1". The glaciers are in the Écrins, Vanoise, Grandes Rousses, Belledonne and Mont-Blanc; the Cottian Alps have only the small Monviso glaciers (no series found), the Graian Alps are covered by the Vanoise sites.
- **Snow onset at 2500 m.** Klein, Vitasse, Rixen, Marty & Rebetez 2016, *Climatic Change* 139, 637-649, doi:10.1007/s10584-016-1806-y (PDF from the WSL repository, `texts/terrain_sources/klein_etal_2016_climatic_change_snow_onset.txt`): eleven Swiss stations 1139-2540 m, 1970-2015, snow onset = first day of the first continuous cover of 40+ days with >= 1 cm: "In autumn, the snow onset now takes place on average on 7 December at the lowest station and on 25 October at the highest station, whereas it was respectively on 22 November and 15 October in 1970"; earliest onset of the whole record 6 September 1984 at Weissfluhjoch (2540 m).
- **Snow season at 2500-2850 m.** Bender, Lehning & Fiddes 2020, *Frontiers in Earth Science* 8:100, doi:10.3389/feart.2020.00100 (open access): snow onset defined as 10 successive days with > 10 cm; reference-period season lengths 192 days at Simplon 2620 m (south-facing), 244 days at Zermatt 2750 m, 265 days at Arolla 2850 m, 267 days at Zernez 2680 m, i.e. continuous cover from about mid-October to late June at 2700-2850 m in the Swiss Alps.
- **Piedmont side.** ARPA Piemonte, *Effetti dei cambiamenti climatici sull'innevamento delle Alpi piemontesi* (technical note, webgis.arpa.piemonte.it, fetched 2026-09-14; `texts/terrain_sources/arpa_piemonte_effetti_cambiamenti_climatici_innevamento.txt`): mean annual fresh snow above 2000 m "raggiunge i 4.5 metri" in the western sector (Susa/Chisone) and "i 6 metri all'anno" in the southern sector (Cuneo); the snowfall level has risen "di circa 100 m ogni 10 anni"; above 2000 m the onset of melting conditions has moved "dall'inizio di maggio all'inizio di aprile" (west) and "dall'inizio di aprile alla prima metà di marzo" (south); the winter season with 40 cm on the ground "sempre più raramente si verifica nel mese di dicembre" at the ski-station altitudes.
- **Hautes-Alpes.** "Le climat des Hautes-Alpes" (Météo-France data 1961-1990, meteo05.sepcs.fr; `texts/terrain_sources/meteo05_climat_hautes_alpes.txt`): a "méditerranéen de montagne" climate; in the Gapençais-Durance-Buëch sector annual precipitation 750-900 mm falls "principalement en octobre-novembre et en mai"; Embrun (871 m) maximum snow on the ground 52 cm (21/03/1971), Briançon 126 cm (17/02/1978); the Embrunais keeps its snow "environ un mois" less than the Briançonnais.
- Not obtained: Durand et al. 2009 (*J. Appl. Meteor. Climatol.* 48, 2487-2512), the SAFRAN snow-cover climatology by altitude for the French Alps (AMS returns 403 through the proxy); the S2M reanalysis paper (Vernay et al. 2022, ESSD 14, 1707-1733, open) describes the dataset but gives no onset-by-altitude table in the text.

**Derived reference dates (model-informed, unverified against a southern-Alps station series):** first lasting snow at 2000 m in the Cottian/Maritime Alps: typically mid-November, range late October to December; at 2500 m: late October to mid-November (Klein 2016 gives 25 October at 2540 m in the wetter northern Swiss Alps, 15 October in 1970; the southern Alps get their autumn snow from Mediterranean returns in October-November and are drier); at 3000 m: the cover is quasi-permanent because 3000 m is at the regional ELA (3035 ± 120 m), i.e. on shaded slopes and glaciers last winter's snow does not melt out at all in an average year, and in a cool year (1984-type, ELA 2790 m) it survives 200-250 m lower.

### 5.3 Band for "old snow from the previous winter lying at the col in late October"

The test is Polybius 3.55.1: on the descent below the summit, this year's fresh snow lay on the hard old snow of the previous winter. In the modern climate old snow (firn) survives the summer only above the ELA of ~3035 m on glaciers, and in shaded hollows, avalanche cones and north faces some 200-400 m lower; the col itself is a wind-swept saddle where it survives least.

| col (m) | height relative to the 1984-2010 mean ELA | old snow at the col, late October, modern climate | same, in a climate like 1984 (ELA 2790 m) or the Iron Age Advance Period 2 (~2.1 ka) |
|---|---|---|---|
| Traversette 2947 | -90 m (within one standard deviation) | possible: the east-facing gully below the col and the shaded north side of the Pian del Re headwall hold firn in cool years; band 30-60 % | likely (the col would be above the ELA); 60-85 % |
| Agnel 2744 | -290 m | unlikely at the col; possible in shaded hollows; 10-30 % | possible; 30-50 % |
| Clapier 2482 | -550 m | unlikely; 5-15 % (avalanche deposits under the Savine/Clarea headwalls only) | possible in shade; 15-35 % |
| Grand-Saint-Bernard 2469 | -570 m | unlikely; 5-15 % | 15-35 % |
| Petit-Saint-Bernard 2188, Petit Mont-Cenis 2183, Mont-Cenis 2083 | -850 to -950 m | very unlikely; < 5 % | < 10 % |
| Larche 1991, Montgenèvre 1854 | -1050 to -1180 m | nil; < 2 % | < 5 % |

The bands are judgements from the sources above, not measurements; what would move them is a southern-Alps station series of end-of-summer snow patches at 2500-3000 m (not found) and a firmer temperature reconstruction for the late 3rd century BC (section 5.4). Two textual cautions: Polybius places the old snow on the descent below the summit, not necessarily on the col; and his 3.55.9 (perennial snow on all the summits) is a generalisation, so 3.55.1 need not be read as an eyewitness detail from the exact col.

### 5.4 Climate of the Alps around 2200 BP (fetched)

- Holzhauser, Magny & Zumbühl 2005, "Glacier and lake-level variations in west-central Europe over the last 3500 years", *The Holocene* 15(6), 789-801, doi:10.1191/0959683605hl853ra (open PDF copy; `texts/terrain_sources/holzhauser_magny_zumbuhl_2005_holocene_15_789.txt`): Great Aletsch advances at "1000-600 BC, AD 500-600, 800-900, 1100-1200 and 1300-1860", with a dendro-dated advance "around 602 BC"; "Between 200 BC and AD 50, the glacier reached today's extent or was even somewhat shorter than today"; "the period 400 BC-AD 400 appears to correspond to a major glacier recession"; "the lack of data documenting any advance of the Lower Grindelwald and Gorner glaciers from 400 BC to AD 400 may be paralleled with the long recession phase of the Great Aletsch glacier at this time"; lake levels show "two periods of pronounced lowering at 1150-800 and 250-650 BC" and a glacier minimum "culminating at c. 200 BC-AD 50".
- Le Roy, Ivy-Ochs, Nicolussi, Monegato, Reitner, Colucci, Ribolini, Spagnolo & Stoffel 2024, "Holocene glacier variations in the Alps", chapter 20 of *European Glacial Landscapes: The Holocene* (Elsevier), 367-418, doi:10.1016/B978-0-323-99712-6.00018-0 (open copy at iris.cnr.it; `texts/terrain_sources/leroy_ivyochs_etal_2024_...txt`): "renewal of glacier activity occurred during the period we herein termed the Iron Age Advance Period 1 (IAAP 1, 3.0-2.4 ka, formerly known as the Göschenen 1 advance)"; "the glacier subfossil wood record is inexplicably sparse during the second part of the first millennium BCE ... This could be partly due to cold conditions ... sustaining positive mass balance and high average glacier extent"; "Around ~2.1 ka, a body of reliable evidence indicates a prominent advance at the end of the Iron Age, the Iron Age Advance Period 2 (IAAP 2). It is dated so far at Bonnepierre, Argentière (Mont Blanc Massif, France), Upper Grindelwald and possibly also at Lower Grindelwald and Gepatsch Glaciers"; "During the Roman Warm Period (RWP, CE 1-250 ...), Alpine glaciers were significantly reduced (< 1980s), as exemplified by the Aletsch Glacier record (Holzhauser et al., 2005). However, smaller-than-present glacier extent (< CE 2000-2020) cannot be proved"; Late Iron Age and Roman artefacts at glacial passes of 2750-3300 m (Col de l'Autaret 3072 m and Colerin 3207 m in the Vanoise, Col d'Annibal 2991 m, Théodule 3295 m, Schnidejoch 2756 m) "point to their frequent use and accessibility during the RWP".
- Ivy-Ochs, Kerschner, Maisch, Christl, Kubik & Schlüchter 2009, "Latest Pleistocene and Holocene glacier variations in the European Alps", *Quaternary Science Reviews* 28, 2137-2149, doi:10.1016/j.quascirev.2009.03.009: bibliographic record confirmed through CrossRef; the text could not be obtained (Elsevier and the ZORA repository are blocked, the Wayback copy returns 401), so it is cited here only through the 2024 chapter by the same group, which restates its Göschenen I/II scheme.

Net for 218 BC: the year sits at the end of the Iron Age, after the IAAP 1 advances (peak ~2.6 ka) had waned but within a century of the IAAP 2 advance (~2.1 ka) and before the Roman recession that begins about 200 BC in the Aletsch curve. The safest statement is that the snowline in 218 BC was not higher than the 1984-2010 mean and may have been 100-250 m lower (one to two degrees of summer cooling at 115 m per degree), which moves the Traversette from "at the snowline" to "above it" and does not bring any col below 2500 m into the old-snow zone.

## 6. Astronomy: the setting of the Pleiades in 218 BC

Method in section 2 and in the docstring of `code/pleiades.py`; results in Table G and `data/pleiades_output.json`. At 45 N, proleptic Julian calendar, 218 BC (astronomical year -217):

- True morning (cosmical) setting, Alcyone on the western horizon as the Sun's upper limb rises: **29 October**.
- First visible morning setting (the star can be seen setting in the dawn): **4 November** with the Sun 6 deg below the horizon, **6 November** at 7.5 deg, **7 November** at 9 deg, **9 November** at Schoch's 11 deg for the Pleiades. This is the "δύσις" of the parapegmata.
- Evening (heliacal) setting, last evening the cluster is seen setting after sunset: 12-18 April (true 24 April); acronychal rising: 15-30 September (true 14 October); heliacal rising: 2-17 May (true 17 April).
- Alcyone's apparent place on 1 November 218 BC: RA 1.712 h, Dec +14.9 deg (it has since precessed to RA 3.79 h, Dec +24.1 deg).
- Cross-checks: PyEphem reproduces every date; Columella, *De re rustica* 11.2.77-84 (AD c. 60-65, Italy; `thelatinlibrary.com/columella/columella.rr11.shtml`, text saved as `texts/terrain_sources/columella_rr11_thelatinlibrary.txt`): "XIII et XII Kal. Nov. solis exortu Vergiliae incipiunt occidere" (20-21 Oct), "V Kal. Nov. Vergiliae occidunt, hiemat cum frigore et gelicidiis" (28 Oct), "VI Id. Nov. Vergiliae mane occidunt, significat tempestatem, hiemat" (8 Nov). The 280 years and 3 degrees of latitude between Columella and Hannibal shift the phase by about two days, so the agreement (29 Oct / 28 Oct true; 6-9 Nov / 8 Nov visible) is as good as the method allows.

So "the setting of the Pleiades was near" (3.54.1) at the summit means the last days of October or the first week of November (Julian) of 218 BC; this is the date band to combine with the snow evidence. A caution: the phrase is calendrical (Hesiod's ploughing signal), not an observation made from the col; from a col the western horizon is a ridge several degrees high and the observed disappearance would be a day or two later.

## 7. Figures

- `data/map_overview.svg` (178 KB): Copernicus GLO-90 hillshade with hypsometric tint, OSM river centrelines, the Rhône legs, routes R1-R7 with variants in distinct colours and dash patterns, the cols with map heights.
- `data/profiles.svg` (36 KB): elevation profiles of R1-R7 on a common axis (km from each route's Island), with the col (triangle), the gate (circle) and the 400-m plain point (square), and the 800-stade lines at 177.6 and 185 m.
- `data/viewshed_panels.png` (171 KB): one panel per col: plain cells (< 400 m) in yellow, those in line of sight from the col in red.
- `data/radiocarbon_curve_40cm.svg` belongs to the geoarchaeology dossier and is not part of this dossier.

## 8. Limitations

1. **Resolution.** 90 m x 65 m cells and a surface model. Good enough for "is the plain visible", "how long and how high is the valley", "is there ground steeper than 50 % on the descent"; not good enough for whether a particular ledge or its landslip existed, for a col notch narrower than a cell (the Traversette is 35 m too low in the DEM), or for tree cover, which in the viewshed can only hide, never reveal.
2. **The route line.** The least-cost path is a modern-terrain valley-floor line between hand-chosen waypoints. The lower Rhône, Isère and Durance ran in braided, marshy beds in antiquity (the Isère below Grenoble and the Durance below Sisteron especially), and the Guil (Combe du Queyras), the Arc (Maurienne narrows below Saint-Michel) and the Cenischia were unroaded gorges; an ancient track climbed above them, which adds length and climb that the model does not include. Lengths are therefore lower bounds for segments (b)-(e), probably by 5-15 %, more in the gorges. The 4 % metrication and the choice of waypoints are smaller than that.
3. **Which stade, which Island, which gate.** The stade choice moves every stade figure by 4 %; the Island choice moves the Rhône leg by 100 km; the gate choice moves segment (b) by up to 100 km (Table B). Everything is tabulated at named points so the report can apply its own definitions; the summary uses the gates most theories use.
4. **Rates.** Daily rates assume Polybius' day-counts apply to the segments as defined here; his own 1400 + 1200 do not fit any candidate simultaneously (section 3.1), so the day-counts must be read with the same tolerance.
5. **Viewshed observer.** Col points are the geocoded saddles (checked to within 40 m of map height); a crude automatic saddle search was tried and rejected because at 90 m it snaps to notches and lake basins. The vantage scan covers 1.5 km around each col at a 3-cell stride; a longer walk was not modelled.
6. **Snow bands are judgements** from modern climatology and the glacier record, with the caveats of 5.3-5.4; no southern-Alps snow-patch series was obtained.
7. **Astronomy** is exact to the day for the geometric criterion; the arcus visionis is a convention (6-11 deg), hence the 4-9 November band.

## 9. Numbers the report can cite, and where each one lives

| number | file / key |
|---|---|
| valley-floor length of every leg and segment, stades at 177.6 and 185 m, km/day for 4/9/4/13 days, straight-line lengths, climb, mean and max 1-km gradients, steepest 500-m descent window, descent bearing, chord failures | `data/routes_output.csv` (one row per route x ascent-start definition; the `gate:` rows are the summary), markdown copy `data/routes_output.md` |
| everything above plus the waypoints with sources, the simplified path, the 800-stade marks, the plain point, zigzag-corrected lengths | `data/routes.json` -> `routes[<id>]` and `rhone_legs[<leg>]` |
| cumulative distance and DEM height at every named waypoint | `data/waypoint_distances.csv` |
| 250-m profiles (distance, lat, lon, elevation) and the indices of col, gate, flat10, z500 and plain | `data/profiles.json` |
| chords that climb > 150 m above both ends (why the least-cost path was needed) | `data/chord_check.csv` |
| plain visible from col / descent points / knolls / vantage scan, fractions of azimuths, nearest and farthest plain, every point tested | `data/viewshed_output.json`, table `data/viewshed_output.md` |
| Pleiades dates for every threshold, both computations, and the Sun-altitude series | `data/pleiades_output.json` |
| geocoded coordinates and OSM ids of all 122 places | `data/places.json` (raw Nominatim replies: `data/geocode_cache.json`) |
| the tables of this dossier | `data/terrain_tables.md` (from `code/report_tables.py`) |
| modern snow and glacier sources, quoted verbatim | `texts/terrain_sources/*.txt` |

## 10. Could not access / did not verify

- Ivy-Ochs et al. 2009 (QSR): Elsevier 403, ZORA blocked by an Anubis challenge, Wayback 401; cited through Le Roy, Ivy-Ochs et al. 2024 (open).
- Durand et al. 2009 (J. Appl. Meteor. Climatol.): AMS 403 through the proxy. Klein et al. 2016 obtained from the WSL repository instead; Bender et al. 2020 open.
- Pliny, NH 18.59 (the Vergiliae date), for a second Roman parapegma check: the Latin Library page could not be located (several URL forms return 404); Columella 11.2 was used instead.
- Col de la Croix / Colle della Croce: not geocodable; no 2299-m saddle in the DEM where the maps put it; left out.
- The exact modern hairpin road lengths (Mont-Cenis, Traversette mule path) were not fetched; the zigzag-corrected length is a model, not a survey.
- All "(unverified)" or "derived" statements in section 5 are so marked.
