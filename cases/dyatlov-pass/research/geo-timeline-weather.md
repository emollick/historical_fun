# Dyatlov Pass: geospatial, astronomical and meteorological checks

> **Note on the DEM's scale.** The slope numbers below come from a 30 m radar DEM and measure the *average* ground slope over 60–300 m windows. They bound the average (15–16° at the cairn-marked tent position; the 2021 paper's "~23° ± 2°" average is not supported; the 2022 follow-up's "around 20°" is compatible within the grid's smoothing and the tent-position uncertainty). They say nothing about the 4–6 m ground steps on which the Gaume–Puzrin weak layer is placed: Puzrin & Gaume 2022 (Commun. Earth Environ. 3:63, Fig. 2, drone photogrammetry of September 2021 at 9 cm) report steps "exceeding 28 degrees, and many slopes even steeper than 30 degrees", continuous above the candidate tent locations. Any sentence below that reads the DEM as evidence *against* the model's local step should be read with that limit.


*All numbers come from the scripts in `code/geo/` (outputs in `code/geo/out/`) or from the cited documents; nothing is quoted from memory. Reproduce with `sh code/geo/run_all.sh`.*

## 0. Headline results

1. **Slope at the tent (Copernicus GLO-30, 30 m DEM): 15–16°** at the best-supported tent site (TL 18.10), on every window from 60 m to 300 m (Horn 3×3 15.4°, plane fits r = 50/100/150 m: 15.3/15.6/15.6°, ±1.1° random error). The alternative sites are no steeper: prosecutors' 2019 position 16–17°, Borzenkov's GPS point 17°, the sculpture 17–19.5°. The 200 m directly upslope (fall line, bearing 265°) rises at 17° (0–100 m) and 14° (100–200 m), with no 25-m segment steeper than 19.6°; the steepest single DEM pixel within 300 m above the tent is 22.7°, ~280 m SSW. A 28–30° slope sustained over ≥ 60 m does **not** exist above TL 18.10 in the DEM; a 28–30° *step a few metres high* (what Gaume & Puzrin actually model, α = 28° from Buyanov's field estimate of 25–30°) is below the DEM's resolution and can be neither confirmed nor excluded.
2. **1959 eyewitness slope figures** bracket the DEM value: Sogrin/Akselrod party who climbed to the tent site on 4 March: **15–18°** (sheet 334); Brusnitsyn: **20–25°**, "reaches 20°" (sheets 366, 369); Tempalov's tent-site protocol: **30°** (sheet 2, in a protocol that also puts the tent "300 m from the top", against 764 m on the map); Maslennikov's notebook sketch: 15° above the tent over 250–300 m, then 25° (100 m), 20°, 35° (100 m) below. The often-quoted "~23° ± 2°" (Gaume & Puzrin, citing Buyanov & Slobtsov) is not the DEM slope at any candidate tent site.
3. **Darkness**: sunset 17:03, civil dusk 17:54, nautical dusk 18:49, astronomical dusk 19:40 (local, UTC+5); the tent site itself lost direct sun behind Kholat Syakhl at ~14:40. Waning crescent moon (44 % → 33 % lit) rose only at 04:15 on 2 Feb and reached 7° altitude by 06:00; new moon 8 Feb 00:22 local. From ~19:40 to ~04:15 the slope was moonless; Burmantovo reported overcast/cloudy until midnight, clearing by 03:00. Civil dawn 08:35, sunrise 09:26 on 2 Feb.
4. **Station weather (NOAA GHCN-Daily, Russian archive)**: a mild spell 28 Jan–1 Feb (daily maxima −4 to −7 °C at Ivdel/Nyaksimvol/Troitsko-Pechorsk), a **sharp cooling on the night of 1–2 Feb** (Ivdel TMIN −11.2 → −20.3 °C; Nyaksimvol −13.9 → −30.8; Troitsko-Pechorsk −15.6 → −20.7; Pechora −23.1 → −35.1), then a severe cold snap 4–5 Feb (−32 to −40 °C). Maslennikov's Burmantovo sheet times the cold-front passage there to 23:00–00:00 (−13 °C at 21:00, −5 at 23:00 with the wind veering W, −15 at 00:00 NW, −21 at 03:00 clear). Station winds were light (1–5 m/s at Burmantovo; "10–14 m/s gusty" at Ivdel airfield); the pass itself is reported at 15–20 m/s "usually" and up to 25–36 m/s (sheets 39, 93, 169, 175).
5. **Distances**: tent (TL 18.10) → cedar 1 550 m horizontal (bearing 62°), 256 m drop, mean 9.4°; case file says 1 500 m. Kolmogorova lies 654 m from the cedar / 897 m from the tent, 184 m below it, within 13 m of the straight line; Slobodin 503 m, Dyatlov 323 m from the cedar (case file: 630/480/300). Descent time for the 1.55 km without boots at night: ~35–85 min (wind crust for the first ~850 m, then 1–2 m of loose snow).

## 1. Coordinates

Full table with every source: `code/geo/data/coordinates.csv`. Datum WGS84 (Google Maps / OSM / GPS). Local metric grid centred on TL 18.10.

| feature | lat N | lon E | source | note |
|---|---|---|---|---|
| **Tent, TL 18.10** ("true TL" of the Konstantinov–Voskoboynikov–Kozyrev–Koshkin group, 2012; refined on site 2019/2023) | 61.758561 | 59.429436 | dyatlovpass.com/tent-location (Konstantinov, 9 Oct 2024): 61°45′30.82″N 59°25′45.97″E | claimed accuracy 1–2 m from bearing lines through landmark stones in 1959 photos |
| Tent, TL 18.10 on-site GPS | 61.758528 | 59.429417 | same article: "65°[sic] 45′30.7″N 59°25′45.9″E" | 3 m from the office value |
| Tent, dyatlovpass.com map placemark "Tent" | 61.7585389 | 59.4294268 | Google My Maps KML export | "three independent Russian researchers agree… marked with a cairn and metal pin"; **used as the reference tent site below** |
| Tent, Prosecutor's Office 2019–20 (±50 m declared) | 61.7595562 | 59.4299706 | KML placemark "Tent (prosecutors)" | 117 m N of TL 18.10 (Konstantinov: 115 m) |
| Tent, Borzenkov GPS reading 2009 (TL "VAB") | 61.759033 | 59.429417 | article, deciphered as 61°45.542′N 59°25.765′E, H = 903.7 m | 55 m N of TL 18.10; Konstantinov notes the reading does not match the spot Borzenkov marked in his photo (170 m away) |
| Sharavin's cairns 2001 / Buyanov's pyramid | — | — | article | no coordinates published; ~130 m from TL 18.10 (direction not stated), downslope, with Buyanov's own ±50 m error circle |
| Semyashkin 2010 marker (as printed) | 61.757383 | 59.437750 | article: "N 61.45.443; E 59.26.265" | read as 61°45.443′N 59°26.265′E this is 456 m E of the others and contradicts the text ("30–40 m from Buyanov's, 50 m from Borzenkov's"); treated as a transcription/datum error, not used |
| "New monument" sculpture | 61.7589433 | 59.4286827 | KML | 60 m NW of TL 18.10 |
| **Cedar** (fire; Doroshenko, Krivonischenko) | 61.7650062 | 59.4554272 | KML "The cedar tree" (bodies 61.7650076/59.4554141 and 61.7650092/59.4553966) | |
| Ravine bodies (Dubinina, Thibeaux-Brignolle, Zolotaryov, Kolevatov) | 61.7650727 / .7650511 / .7650460 / .7650358 | 59.4539013 / .4539523 / .4539121 / .4539497 | KML | 79 m W of the cedar |
| Den / flooring (настил) | 61.765051 | 59.453929 | mean of the four ravine placemarks | no separate published coordinate; the den protocol (sheets 341–343) puts the flooring 6 m up the creek from the bodies, 2.5–3 m deep → ±10 m |
| Dyatlov | 61.7635133 | 59.4501804 | KML | 322 m from cedar |
| Slobodin | 61.7626626 | 59.4472703 | KML | 503 m from cedar |
| Kolmogorova | 61.7621755 | 59.4445806 | KML | 652 m from cedar |
| Labaz (cache) / 31 Jan camp | 61.7466967 | 59.4494443 | KML "Jan 31 Camp & Cache site" | 402 m from the searchers' 1959 camp (radiogram: 400 m) |
| Kholat Syakhl summit | 61.7545756 | 59.4177103 | KML "Kholat Syakhl 1079" | DEM maximum 1 096.0 m at 61.75444 N 59.41778 E, 15 m away; modern map height 1 096.7 m, 1959 map 1 079 m |
| Kholat Syakhl (ru.wikipedia infobox) | 61.755000 | 59.422500 | 61°45′18″N 59°25′21″E | 250 m E of the summit pixel; generic |
| **Pass memorial** (plaques on the outlier rock) | 61.7548411 | 59.4630442 | OSM node 8152230817, historic=memorial "Перевал Дятлова" (saddle node 3678862645 at 61.7550437 59.4629146) | 1 816 m from the tent at bearing 103°; ru.wikipedia "Перевал Дятлова" 61°45′17″N 59°27′46″E is 15 m away |
| "Dyatlov Pass incident" (en.wikipedia infobox) | 61.754444 | 59.445000 | 61°45′16″N 59°26′42″E | a generic point 937 m SE of the tent, not a feature |
| 1959 helipad; searchers' camp | 61.7549781 / 61.7431330 | 59.4388246 / 59.4507000 | KML | |

**Disagreements.** The tent has three surviving candidate positions ~55–120 m apart on the same slope (TL 18.10, the prosecutors' point 117 m to the N, Borzenkov's GPS point 55 m N), plus Buyanov's/Sharavin's position ~130 m away without published coordinates; the sculpture is 60 m NW. All of them lie on the same 15–19° terrain (Section 2), so the slope conclusions do not depend on which one is right. The summit is 764 m from the tent, not "300 m" (sheet 2) nor "100–150 m" (Chernyshev, sheet 89); Maslennikov's "150 m from the spur ridge (900 m)" (sheet 70) fits the DEM shoulder 150–250 m WNW of the tent.

**Consistency check with Maslennikov's compass azimuths** (loose sheet in notebook 2, `raw/maslennikov/…azimuths-from-the-tent.jpg`): from the tent, "40° to the creek" and "90° to the rock" (magnetic). IGRF-13 declination at the tent for Feb 1959 is +17.5° E (ppigrf), giving 57.5° and 107.5° true; the placemark bearings are 61–62° (cedar / ravine) and 103° (memorial outlier rock). Agreement within 5° supports both the tent placemark and the identification of the rock.

**Case-file distances** (sheets 384–387, Ivanov's resolution; sheets 3–6 scene protocol; sheets 62–75 Maslennikov; Maslennikov's measurement scheme, notebook 2 scan 51):

| pair | case file | map placemarks |
|---|---|---|
| tent → fire/cedar | 1 500 m (Ivanov, sheet 386; Maslennikov scheme) | 1 545 m sphere / 1 551 m ellipsoid (TL 18.10); 1 475 m from the prosecutors' point; 1 566 m from the sculpture |
| fire → Dyatlov | 300 m (Ivanov; Maslennikov sheet 62–75) / 400 m (scene protocol, sheet 4) | 322 m |
| Dyatlov → Slobodin | 180 m (Ivanov) | 180 m |
| Slobodin → Kolmogorova | 150 m (Ivanov); Maslennikov: Kolmogorova 350 m from Dyatlov; scene protocol: 500 m from Dyatlov | 152 m |
| fire → ravine bodies | 75 m (Ivanov) / 70 m (Maslennikov scheme) / 50 m (den protocol) | 79 m |
| tent → 3rd stone ridge (flashlight) | 450 m (Maslennikov scheme; radiogram sheet 191: flashlight 450 m below the tent; Atmanaki sheet 220: "100 m below the tent") | — |
| tent → "start of the snow zone" | ~850 m (Maslennikov scheme) | — |
| tracks visible below the tent | up to 500 m (sheet 386) / ~1 km (sheet 160) / 50 m only (Tempalov, sheet 312) | — |
| labaz → searchers' camp | 400 m (radiogram 2 Mar) | 402 m |

The placemarks for Dyatlov, Slobodin and Kolmogorova evidently were laid out at Ivanov's distances along the tent–cedar line (they reproduce 180/150 m exactly), so they are not independent evidence; the cedar and tent placemarks are independent and reproduce the 1 500 m within 3 %.

## 2. DEM slope analysis

**Data.** Copernicus DEM GLO-30, tile N61 E059 (AWS public bucket, md5 in README). Grid 1″ × 2″ at this latitude = **31.0 m N–S × 29.3 m E–W**; heights in metres above EGM2008; it is a TanDEM-X surface model (2011–15). Spec: absolute vertical < 4 m LE90, relative vertical < 2 m LE90 for slopes < 20 %, horizontal < 6 m CE90. Sanity checks: summit pixel 1 096.0 m vs 1 096.7 m on modern Russian maps; tent 899 m vs Borzenkov's GPS altitude 903.7 m. Cross-check with the AWS "terrarium" tiles (coarser global source north of 60° N): −12 m mean offset along the profile, 14.5° fall-line slope over 60 m at the tent — consistent.

Figures: `code/geo/out/map_dem.png` (hillshade, 20 m contours, all sites) and `code/geo/out/profile_tent_cedar.png`.

### 2.1 Slope and aspect at the candidate tent sites (`out/slopes_at_sites.csv`)

Windows: Horn 3×3 = central differences spanning ~60 m at the nearest pixel (the closest thing to a "30 m" estimate a 30 m DEM can give); least-squares planes through all pixel centres within radius r (r = 30 m contains only 2–4 pixels → not fitted; r = 50 m ≈ 9 pixels ≈ "100 m window"; r = 100 m ≈ 35; r = 150 m ≈ 80). Aspect = downhill compass direction. "MC sd" = standard deviation over 200 realisations of N(0, 1.5 m) random height noise.

| site | z (m) | Horn 3×3 (≈60 m) | plane r = 50 m | plane r = 100 m | plane r = 150 m | MC sd Horn / r50 / r100 |
|---|---|---|---|---|---|---|
| Tent TL 18.10 (placemark) | 899 | 15.4° / aspect 83° | 15.3° / 83° | 15.6° / 85° | 15.6° / 84° | 1.2 / 1.1 / 0.3° |
| Tent TL 18.10 (office coords) | 899 | 15.4° | 15.3° | 15.6° | 15.6° | 1.1 / 1.1 / 0.3° |
| Tent, prosecutors 2019 | 886 | 16.2° / 77° | 16.4° / 77° | 17.0° / 81° | 16.4° / 81° | 1.2 / 1.3 / 0.3° |
| Tent, Borzenkov GPS 2009 | 898 | 17.7° / 86° | 16.9° / 86° | 17.1° / 86° | 15.9° / 84° | 1.1 / 1.3 / 0.3° |
| Sculpture | 912 | 19.5° / 91° | 19.3° / 93° | 17.1° / 89° | 15.8° / 84° | 1.0 / 0.9 / 0.3° |
| Kolmogorova | 715 | 10.2° / 60° | 10.1° | 9.6° | 9.6° | |
| Slobodin | 689 | 9.6° / 58° | 10.2° | 9.8° | 9.3° | |
| Dyatlov | 665 | 9.0° / 6° | 10.8° | 9.7° | 9.2° | |
| Cedar | 643 | 9.5° / 337° | 9.6° | 10.5° | 10.3° | |
| Den / ravine | 636 | 13.8° / 347° | 13.4° | 10.1° | 8.6° | |
| Summit (DEM max) | 1 096 | 0.6° | 0.6° | 0.5° | 0.8° | |

Steepest single pixel (Horn) within 300 m above the tent: **22.7°** at (−87 m E, −271 m N), i.e. ~280 m SSW on the flank toward the summit. Steepest pixel in the 200 m-wide descent corridor tent → cedar: 21.1°, in the first pixels of the corridor beside the tent (within 100 m of it, toward the sculpture); corridor mean 11.3° (330 pixels).

### 2.2 Profile directly upslope of the tent (`out/profile_upslope.csv`)

"Fall line" = uphill direction of the r = 100 m plane at the tent (bearing 265°); "toward summit" = bearing 233°. Gradients are centred differences over 25 / 50 / 100 m (positive = rising).

| up (m) | fall line elev (m) | grad25 | grad50 | grad100 | toward-summit elev (m) | grad25 | grad100 |
|---|---|---|---|---|---|---|---|
| 0 | 898.9 | 15.3 | 15.1 | 15.3 | 898.9 | 14.1 | 13.1 |
| 25 | 906.3 | 16.7 | 16.8 | 16.0 | 905.2 | 12.9 | 13.4 |
| 50 | 914.1 | 17.1 | 16.9 | 17.1 | 911.1 | 13.8 | 13.9 |
| 75 | 921.5 | 16.3 | 17.3 | 17.8 | 917.1 | 13.9 | 14.6 |
| 100 | 929.6 | **19.6** | 18.8 | 18.1 | 923.7 | 15.7 | 15.2 |
| 125 | 938.5 | 19.3 | 18.9 | 16.9 | 931.3 | 16.8 | 15.6 |
| 150 | 946.7 | 14.5 | 15.1 | 14.2 | 938.3 | 15.4 | 14.9 |
| 175 | 951.9 | 9.4 | 9.3 | 10.9 | 945.0 | 13.6 | 14.3 |
| 200 | 954.9 | 6.5 | 6.7 | 8.1 | 950.4 | 12.5 | 14.9 |
| 250 | 960.9 | 7.5 | 6.9 | 6.2 | 964.9 | 18.7 | 17.3 |
| 300 | 965.7 | 2.4 | 2.9 | 3.4 | 981.5 | 18.0 | 17.4 |

Segment means: fall line 0–100 m **17.1°**, 100–200 m **14.2°**, 0–200 m 15.6°, 200–300 m 6.2° (the shoulder/plateau; the tent is 56 m below it). Toward the summit: 13.9°, 14.9°, then 17.3° for 200–300 m; the mean gradient tent → summit (764 m, +197 m) is 14.4°, matching the "run-out angle of about 16°" in the Gaume & Puzrin supplement.

### 2.3 Profile tent → cedar (`out/profile_tent_cedar.csv`, every 25 m; excerpt)

| distance (m) | elev (m) | grad over 25 m | over 100 m | note |
|---|---|---|---|---|
| 0 | 898.9 | 14.8° | 13.9° | tent |
| 100 | 876.3 | 11.7° | 13.1° | |
| 150 | 863.9 | **16.1°** (max on the line) | 14.3° | |
| 250 | 839.0 | 14.1° | 13.5° | |
| 300 | 826.7 | 11.1° | 11.5° | slope eases |
| 450 | 801.0 | 9.9° | 10.2° | flashlight ~450 m (sheet 191) |
| 500 | 791.8 | 11.5° | 11.1° | |
| 850 | 723 | ~10° | ~10° | "start of the snow zone" (Maslennikov scheme) |
| 897 | 715 | 9.6° | 9.8° | Kolmogorova |
| 1 048 | 689 | 9.9° | 9.6° | Slobodin |
| 1 228 | 665 | 3.9° | 5.9° | Dyatlov (slope flattens below ~1 200 m) |
| 1 483 | 636 | 5.7° | 4.0° | den / ravine (41 m left of the line) |
| 1 551 | 643.4 | 0.7° | 0.8° | cedar |

Mean slope of the whole descent: 256 m / 1 551 m = **9.4°**; first 500 m 12.1°, 500–1 000 m 10.7°, last 550 m 5.6°. No 25-m segment of the descent exceeds 16.1°; no 100-m segment exceeds 14.4°.

### 2.4 Uncertainty statement

* **Random error.** With 1.5 m pixel noise the 60-m Horn slope at the tent has sd 1.2°, the 100-m plane 1.1°, the 200-m plane 0.3°. Horizontal positioning (< 6 m for the DEM; 1–5 m for TL 18.10; 50 m for the prosecutors' point) moves the estimate by < 1° because the slope field is smooth here (15–17° everywhere within 150 m).
* **Resolution (systematic).** A 30-m grid measures the terrain smoothed over ~60–90 m. The "4–6 m high steps" that Gaume & Puzrin (Fig. 1c, SF2, citing Buyanov & Slobtsov) place on this slope, if 10–20 m long, are 15–30° features that contribute at most 4–6 m of relief inside one pixel: they are averaged into the 15–16° regional value and **cannot be resolved**. The DEM therefore (i) rules out a 28–30° slope sustained over ≥ 60–100 m anywhere within 300 m above any candidate tent site, and (ii) says nothing about a 28–30° step shorter than ~15 m. The same applies to the "22–23°" figure: it is not the terrain slope at TL 18.10 at any scale from 60 m to 300 m; it occurs only in isolated pixels ~280 m SSW (22.7°).
* **Surface vs terrain.** Above the treeline (tent to ~1 000 m along the profile) the DSM is the ground. In the forest around the cedar the DSM includes canopy, so the cedar elevation (643 m) may be biased high by up to ~10 m and the true drop is 255–265 m; irrelevant for the slope at the tent.
* **Snow.** The DEM is snow-free (summer TanDEM-X). In February 1959 the slope carried 0.8–1.5 m of wind-packed snow (Karelin: probe went in 80–100 cm near the tent; Brusnitsyn sheet 366: "up to 1.5 m"), which smooths steps further; the searchers' angle estimates were of the snow surface.

### 2.5 Comparison with the 1959 measurements and the avalanche literature

| source | figure | comment |
|---|---|---|
| Tempalov, tent-site protocol 28 Feb 1959 (sheet 2) | "300 m from the top of 1079 on a slope of 30°" | eyeball; the same sentence has the summit distance wrong by ×2.5 (764 m) and the drainage wrong (Auspiya instead of Lozva) |
| Sogrin, sheet 334 (party with Akselrod, Korolyov and 3 Muscovites at the tent site, 4 March) | "The slope on which the tent stood is not dangerous. The steepness of the slope is 15–18°" | matches the DEM (15–17° at all candidates) |
| Brusnitsyn, sheets 366, 369 | "approx. 20–25°"; "at the tent, where the steepness of the slope reaches 20°"; first stone ridge "nearly horizontal (up to 5°)"; snow depth up to 1.5 m | 20° is within reach of the DEM at the 60-m scale if the tent stood 50–100 m further up or NW (sculpture 19.5°); 25° is not |
| Maslennikov, notebook 2 scan 53 (cross-section sketch) | above the tent 15° over 250–300 m; below: 25° (100 m), 20°, 35° (100 m), then stone ridges | the 15° above matches the DEM's 14–17°; the 25°/35° segments below do not exist at the 25-m scale (max 16.1°); read as a schematic of the stepped micro-relief |
| Chernyshev, sheet 90 | "uneven lowering traversed by several stone ridges running parallel" | the ridges at 200–450 m below the tent (Maslennikov scheme) sit where the DEM slope eases from 14° to 10° |
| Gaume & Puzrin 2021, main text | "relatively mild slope (~23° ± 2°)"; "ground surface … steeper (up to 30°) than the average snow slope"; model α = 28°, "21.6° slope at the cut" | source of both numbers is Buyanov & Slobtsov (2014/2017); SI Note 6: "the planar weak layer was parallel to the steep slope of the local step (hillock), whose inclination was estimated in the range of 25°–30°"; SI Note 2: "run-out angle from the top of the slope to the tent … around 16°" (DEM: 14.4°) |
| This study, Copernicus GLO-30 | 15–16° at TL 18.10 (60–300 m); 17° for the first 100 m up the fall line; 22.7° max pixel within 300 m above; shoulder (6°) at 200–300 m up | |

**Reading.** The DEM supports the 1959 "15–18°" measurement and the paper's own "run-out angle ~16°", and it contradicts the "~23°" *average* that the paper takes as the starting point. The paper's mechanism does not need a 28° slope at DEM scale — it needs a buried weak layer parallel to a local 25–30° step a few metres high immediately above the cut, loaded by wind-blown snow accumulating below a shoulder. The DEM confirms the shoulder (slope drops to ~6° at 200–300 m up the fall line, 55–65 m above the tent) and a 17–19° stretch just above the tent, but cannot test the step. Whether such a step existed under 1–1.5 m of wind-packed snow at TL 18.10 rests entirely on the 1959 photographs and Buyanov's field interpretation, not on topography measurable today; note that Konstantinov (2024) reports rounded, aligned stones indicating past avalanches above Buyanov's TL but "no such evidence" above TL 18.10.

## 3. Astronomy (`out/astro_tables.md`; PyEphem 4.2.1, cross-checked with an independent NOAA solar-position implementation to 0.1°)

Time zone: Sverdlovsk oblast in 1959 was UTC+5 (Moscow decree time +2 h; tzdata `Asia/Yekaterinburg` = +05 from 21 June 1930 to 31 March 1991; asserted in `astro.py`). Site 61.7585 N 59.4294 E, 899 m.

| date | astr. dawn | naut. dawn | civil dawn | sunrise | solar noon | sunset | civil dusk | naut. dusk | astr. dusk | day length |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Feb 1959 | 06:52 | 07:43 | 08:37 | 09:28 | 13:15 | 17:03 | 17:54 | 18:49 | 19:40 | 7.58 h |
| 2 Feb 1959 | 06:50 | 07:41 | 08:35 | 09:26 | 13:15 | 17:06 | 17:57 | 18:51 | 19:42 | 7.67 h |
| 26 Feb 1959 | 05:49 | 06:41 | 07:32 | 08:16 | 13:15 | 18:15 | 19:00 | 19:50 | 20:42 | 9.97 h |
| 5 Mar 1959 | 05:27 | 06:20 | 07:10 | 07:54 | 13:14 | 18:34 | 19:18 | 20:09 | 21:02 | 10.66 h |

| date | moonrise | moonset | illuminated (noon) | phase context |
|---|---|---|---|---|
| 1 Feb | 02:52 | 11:27 | 44 % | waning crescent; last full moon 25 Jan 00:32 |
| 2 Feb | 04:15 | 11:59 | 33 % | **new moon 8 Feb 00:22 local (7 Feb 19:22 UTC)** — confirms the "~8 Feb" table value |
| 26 Feb | 23:06 | 08:50 | 89 % | waning gibbous (full 23 Feb 13:53) |
| 5 Mar | 05:58 | 13:46 | 18 % | waning crescent (new 9 Mar 15:51) |

Sun/moon altitude at the hours of interest (local): 1 Feb 15:00 sun +8.3° (az 205°); 17:00 −0.5°; 18:00 −6.5° (nautical twilight begins); 19:00 −13.3°; 21:00 −27° (night); 2 Feb 01:00 −45°; 03:00 −42°; 05:00 −31°, moon +2.9°; 06:00 sun −24°, moon +6.9° (36 % lit, SE); 08:00 sun −9.9° (nautical twilight); 09:00 −3.4° (civil twilight).

**Terrain horizon** (`out/horizon.md`): from the tent the skyline toward S–W–NW stands 13–17° high (Kholat Syakhl), toward N–E–SE it is at or below 0°. The sun therefore disappeared behind the mountain at **14:40** on 1 Feb (and 2 Feb), 2 h 20 min before the flat-horizon sunset, and first cleared the terrain at 08:46. Ivanov's "tent pitched around 17:00" (sheet 385) was inferred from the exposure of the last frames; the tent site was already in mountain shadow from mid-afternoon, so those frames could be earlier than 17:00 — a point for whoever works on the photo timeline.

**Darkness timeline, night 1–2 Feb.** Full night (sun < −18°) from 19:40 to 06:50. No moon at all between sunset and 04:15; after that a 33 % crescent no higher than 7–11° in the SE. With Burmantovo overcast/cloudy until at least 00:00 and clear at 03:00, the slope was effectively pitch-dark until ~03:00 and only starlit (plus a low crescent after 04:15) thereafter; snow cover would give some contrast under a clear sky. Any descent, fire-lighting and return between ~19:00 and ~04:00 was done without moonlight; a Chinese flashlight was found on the tent roof (Maslennikov notebook 2, scan 27) and a lit one 450 m below the tent (sheet 191). On 26 Feb (tent found) the searchers had daylight to 18:15 and an 89 % moon from 23:06; on 5 Mar (Slobodin found) daylight to 18:34.

## 4. Weather

### 4.1 Station data, NOAA GHCN-Daily (`out/ghcn_daily_1959.csv`; source flag `r` = All-Russian Research Institute of Hydrometeorological Information – World Data Centre)

Nearest stations with 1959 data: Ivdel (RSM00023921, 60.683 N 60.450 E, 93 m; 131 km SSE of the tent), Nyaksimvol (RSM00023724, 62.430 N 60.869 E, 51 m; 106 km NE), Troitsko-Pechorsk (RSM00023711; 197 km NW), Cherdyn (RSM00023914; 217 km SW), Pechora (RSM00023418; 391 km N), Serov (RSM00028044; TAVG only). **Burmantovo has no GHCN-Daily record** (GHCN's 23904 is Koigorodok); Vizhay none. ERA5/20CR were not attempted (no small open subset). Values °C (TMAX / TMIN / TAVG), precipitation mm in brackets; a date's TMIN is the preceding night (the Burmantovo sheet below confirms this reading for 1–2 Feb).

| date | Ivdel | Nyaksimvol | Troitsko-Pechorsk | Cherdyn | Pechora |
|---|---|---|---|---|---|
| 28 Jan | −4.7 / −20.4 / −11.8 | −6.5 / −9.1 / −8.2 | −6.5 / −11.3 / −9.2 (2.8) | −6.2 / −9.9 / −8.4 (0.9) | −6.7 / −13.4 / −10.6 (2.5) |
| 29 Jan | −6.4 / −17.9 / −9.4 | −8.1 / −26.3 / −16.8 | −5.6 / −13.3 / −9.6 (1.6) | −6.6 / −9.9 / −7.8 (0.8) | −12.6 / −18.4 / −15.1 (1.0) |
| 30 Jan | −5.7 / −22.4 / −13.2 | −14.4 / −27.4 / −19.6 (0.1) | −6.4 / −24.6 / −18.8 (0.1) | −8.1 / −19.0 / −12.8 (1.2) | −17.7 / −31.5 / −26.2 (1.5) |
| 31 Jan | −5.5 / −22.3 / −9.4 | −5.0 / −20.1 / −10.3 (0.5) | −4.6 / −19.1 / −7.7 (2.4) | −7.0 / −18.6 / −9.7 (1.4) | −4.4 / −21.7 / −10.2 (6.9) |
| **1 Feb** | **−4.7 / −11.2 / −7.5** | **−4.5 / −13.9 / −9.4** (0.2) | −4.5 / −15.6 / −9.6 | −6.4 / −9.2 / −7.4 (0.5) | −5.2 / −23.1 / −17.3 (1.8) |
| **2 Feb** | **−9.7 / −20.3 / −13.6** | **−13.1 / −30.8 / −19.7** (1.0) | −8.7 / −20.7 / −14.2 (0.6) | −8.6 / −16.7 / −12.8 (0.2) | −18.2 / −35.1 / −24.6 (1.9) |
| 3 Feb | −8.8 / −17.3 / −11.1 | −8.3 / −18.3 / −12.8 (1.4) | −9.0 / −19.0 / −12.5 (3.4) | −9.2 / −12.4 / −10.7 (1.8) | −11.5 / −29.9 / −19.9 (3.2) |
| 4 Feb | −10.7 / −32.3 / −23.4 (0.2) | −17.2 / −33.8 / −29.0 (0.1) | −18.4 / −35.5 / −31.2 | −10.0 / −27.8 / −22.8 (0.6) | −29.9 / −40.7 / −35.8 |
| 5 Feb | −25.7 / −36.1 / −31.6 | −30.3 / −39.9 / −35.0 | −18.2 / −34.6 / −24.8 (0.1) | −18.8 / −30.4 / −23.8 | −18.5 / −34.9 / −24.4 |

Search period (full table in `out/weather_tables.md`): 24–28 Feb Ivdel maxima −4 to −10, minima −20 to −27 °C; 1 Mar −1.2 / −21.1; a thaw 2–10 Mar (Ivdel maxima +3 to +8 °C, minima −3 to −16; Nyaksimvol similar) — the "thaw when the slopes of the pass were covered with ice crust" of Atmanaki's testimony (sheet 220) and the radiogram "air temperature minus 7" (sheet 197, 10 Mar). Snow depth (SNWD) is not reported by these stations for 1959.

### 4.2 Burmantovo, 1 Feb 1959 — loose sheet in Maslennikov's notebook 2 (read from the scan; `raw/maslennikov/…Burmantovo-weather-report.jpg`)

| local time | sky | wind | m/s | °C |
|---|---|---|---|---|
| 15:00 | overcast | N | 5 | −8 |
| 18:00 | cloudy | N | 1 | −10 |
| 19:00 | cloudy | N | 3 | −11 |
| 21:00 | cloudy | N | 1 | −13 |
| 23:00 | cloudy | W | 1 | −5 |
| 00:00 | cloudy | NW | 3 | −15 |
| 03:00 | clear | W | 3 | −21 |

(dyatlovpass.com's converted table agrees except at 00:00, where it prints −5 °F = −20.6 °C for the sheet's −15 °C.) The warm blip at 23:00 with the wind veering to W, then −15 °C with NW wind at 00:00 and −21 °C under clear sky at 03:00, is a cold-front passage at Burmantovo between 23:00 and 00:00; the pass lies 78 km NW of Burmantovo, so if the front moved from the NW as the wind shift suggests it crossed the pass some hours earlier in the evening. The station minima for the night (Ivdel −20.3, Nyaksimvol −30.8 in its cold-pooling lowland) and the Burmantovo −21 °C at 03:00 bracket the lowland air at −20 to −25 °C by the early hours; at 900 m in a NW flow with the sky clearing, **−20 to −26 °C at the tent by 03:00** is my central estimate (Ivanov's "of the order of −25 to −30 °C", sheet 385, and Pigoltsina's −28.7 °C at 03:00 are at the cold end), having been only about **−10 to −15 °C when the tent was pitched and during the evening** (Burmantovo −8 to −13 °C from 15:00 to 21:00 at 180 m; Brusnitsyn's "−15 °C this evening", sheet 369).

### 4.3 Weather statements in the case file and notebooks (checked against the transcriptions in `raw/`)

| where | statement |
|---|---|
| Ivanov's resolution, sheet 385 | "strong wind that is usual in this area, and a low temperature of the order of 25–30 °C" [below zero]; ascent begun at 15:00; tent pitched ~17:00 |
| Search organisation report, sheet 39 | "strong winds constantly blow on the investigated slopes and along the valley, usually at a speed of 15–20 m/s, often reaching up to 36 m/s and more (according to weather service)"; blizzards reduce visibility to 3–5 m |
| Chernyshev, sheet 93 | "very unstable, frequent winds that blow with hurricane force… only two quiet days in 12… usually the power of the wind on the pass exceeds 15–20 m/s" |
| Radiogram 27 Feb, sheet 146/152/153 | bodies "thrown out of the tent by a hurricane… direction of the hurricane was northeast-east"; "request the weather report between January 30 and February 2, position and placing of the bodies is indicative of a hurricane"; 27 Feb "now is calm, visibility over 10 km" |
| Radiogram 1 Mar, sheet 169 | "sudden deterioration of the weather… snow is 1–2 m deep… the wind reached 30 meters, there is no visibility" |
| Radiogram 3 Mar, sheet 175; notebook 2 scan 18–19 | "Blizzard with snow lasted all day. Wind on the pass is up to 25 meters, visibility 5–8"; 3 Mar morning "overcast, wind west, down 2, in the mountains 8–10 m/s, temp −5°" |
| Radiogram 4 Mar, sheet 179 | "The weather is very good" (searches 10:30–18:00) |
| Radiogram 5 Mar, sheet 184 | "windy again, the wind swept 15 meters, bad visibility" (day Slobodin was found) |
| Notebook 2 scan 31 (Pavlov's reply, 4 Mar) | "Weather February 1 in Ivdel was temperature 17, northwest wind 14 meter per second" (sign/hour unstated; GHCN Ivdel 1 Feb −4.7/−11.2, 2 Feb −20.3) |
| Notebook 2 scan 35–36 | "Weather around the airport [Ivdel] on 1 February the temperature is minus 8–9, wind 10–14 m/s gusty"; forecast 3–5 Mar "t = −12, wind 5–6 m" |
| Maslennikov, sheet 73; Dyatlov's diary 31 Jan | on the pass 31 Jan "wind… similar to the air draft created by a taking-off airplane"; group retreated to the forest |
| Lebedev, sheet 315; Slobtsov, sheet 298 | "in the night in which the disaster allegedly happened there was a terrible blizzard" (an inference from the tracks); snow on the tent 15–20 cm, hard-packed |
| Karelin (2019 interview, dyatlovpass.com) | probe went 80–100 cm into the snow near the tent; stones on the NE spur "slightly powdered with snow" |
| Pigoltsina 2019 microclimatic expertise (Voeikov MGO; reported by KP) | at the tent: 17:00 −16.4 °C / 9.8 m/s; 19:00 −17.9 / 9.2; 21:00 −19.1 / 9.0 (wind chill −31.8); 23:00 −22.5 / 9.4 (−36.5); 01:00 −26.0 / 10.2 (−41.6); 03:00 −28.7 / 11.3 (−45.9); 05:00 −30.6 / 12.1 (−48.9); 07:00 −31.7 / 12.4 (−50.5); at the cedar 1–2 °C warmer and 1.5–3 m/s calmer; NW flow, tent in a wind shadow; "it snowed continuously 31 Jan–1 Feb"; snow "up to 250 cm 50 m above the tent" (disputed by Karelin) |

The Pigoltsina wind-chill values are exactly the JAG/TI formula applied to her temperature/wind pairs (checked: −19.1 °C, 9.0 m/s → −31.8). Her temperatures run 5–8 °C colder than my station-based estimate for the evening (−16 °C at 17:00 vs Burmantovo −8 to −10 °C at 180 m with a 3–4 °C lapse to 900 m) and are at the cold end for 03:00; the GHCN precipitation supports light snow with the front on 2–3 Feb at the northern stations (Nyaksimvol 1.0/1.4 mm, Troitsko-Pechorsk 0.6/3.4 mm, Pechora 6.9 mm on 31 Jan) and none at Ivdel.

### 4.4 Wind chill, JAG/TI 2001 (`out/windchill_table.csv`; 10-m wind)

| air °C \ wind | 2 m/s | 5 | 8 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|---|
| −10 | −14 | −17 | −19 | −20 | −22 | −23 | −25 | −26 |
| −15 | −20 | −24 | −26 | −27 | −29 | −31 | −32 | −33 |
| −20 | −26 | −30 | −32 | −34 | −36 | −38 | −39 | −40 |
| −25 | −32 | −36 | −39 | −40 | −43 | −45 | −46 | −47 |
| −30 | −37 | −42 | −45 | −47 | −50 | −52 | −53 | −55 |

Exposed skin freezes in < 30 min below about −28, < 10 min below about −40, < 5 min below about −48 (Environment Canada thresholds; Osczevski & Bluestein 2005). For the plausible evening (−12 ± 3 °C, 8–15 m/s) the wind chill was −22 to −29; for the small hours (−23 ± 3 °C, 8–15 m/s) −34 to −43; with the 20–25 m/s "usual" pass winds and −25 °C, −45 to −46. Wind chill quantifies facial heat loss for a clothed, walking adult; it is not a survival-time index for people in socks and shirts.

## 5. Distances and walking (`out/walking.md`, `out/distances.csv`)

Tent → cedar: 1 551 m horizontal, 899 → 643 m, drop 256 m, mean 9.4°, bearing 62°. The three slope bodies lie within 31 m of the straight line (offsets 13, 31, 18 m, all to the right/south looking down). Surface: wind-packed crust on the open slope — footprints preserved as raised columns 500 m–1 km below the tent (sheets 160, 386), "walking a normal step" (Tempalov, sheet 312) — then loose snow 1–2 m+ deep from the forest edge (sheets 169–170; Maslennikov's "start of the snow zone" ~850 m below the tent at ~723 m elevation).

| segment | length | drop | surface | speed | time |
|---|---|---|---|---|---|
| tent → start of deep snow | 850 m | 176 m | wind crust, 10–16°, dark | 2–4 km/h | 13–25 min |
| deep-snow zone → cedar | 700 m | 80 m | loose snow 1–2 m, birch scrub/forest edge | 0.7–2 km/h | 21–60 min |
| total | 1 551 m | 256 m | | | **34–86 min** |

Speed basis: terrain coefficients for snow rise with footprint depth (Soule & Goldman 1972; Pandolf, Givoni & Goldman 1977: ≈1.3 + 0.08 per cm of depth, i.e. 2–3× the energy cost of trail walking at 20–30 cm and 4–5× at 40 cm), giving sustained speeds of 1–2 km/h in unbroken knee-deep snow and < 1 km/h waist-deep; on crust 3–4 km/h is normal even in socks. So the fire under the cedar cannot have been lit less than ~30 min after the group left the tent, and stragglers could have taken over an hour.

Return attempt:

| body | from cedar | from tent | elev | climbed from cedar | still to climb | still to walk |
|---|---|---|---|---|---|---|
| Dyatlov | 323 m | 1 228 m | 665 m | 22 m | 234 m | 323 m |
| Slobodin | 503 m | 1 048 m | 689 m | 46 m | 210 m | 503 m |
| Kolmogorova | 654 m | 897 m | 715 m | 72 m | 184 m | 654 m |

Kolmogorova's position (630 m from the fire in the case file; 654 m on the map) is on the tent–cedar line to within 13 m, on the open crust where the slope is ~10°, head toward the tent, in a pose read in 1959 as climbing (sheets 4–5). She had covered 42 % of the horizontal distance and 28 % of the climb; at 1–2 km/h uphill that is 20–40 min from the cedar. Dyatlov (323 m) and Slobodin (503 m) are spaced 150–180 m apart on the same line, the expected pattern of three people leaving the cedar for the tent at different times or speeds and stopping where they fell; the positions alone cannot distinguish a return from a straggling descent, but the body orientations do, and the return interpretation is consistent with everything measurable here. The stopped watches (5:31, 8:14, 8:39, 8:45) are not death times: a wound Pobeda runs ~36 h and cold can stop it sooner.

## 6. What the numbers say

**Avalanche model slope requirement.** Gaume & Puzrin's delayed-slab model uses α = 28° for the weak layer and a slab only ~5 m long above the cut, on a "local step"; the paper's "~23° average slope" and "up to 30°" both come from Buyanov's field interpretation, not from a survey. Modern open topography gives 15–16° at TL 18.10 (17° for the first 100 m up the fall line, 22.7° in the steepest pixel within 300 m above), 16–19° at the other candidates, and a shoulder 55–65 m above the tent where the slope drops to ~6° — i.e. the 1959 "15–18°" measurement is confirmed, the "23°" average is not, and the 28–30° figure can only be a micro-step under the snow that a 30-m DEM cannot see. The model is therefore not refuted by the DEM, but it is unsupported by it: its steep-step premise rests on the 1959 photographs and on which of the tent sites is right (Konstantinov reports avalanche-worked stones above Buyanov's TL but not above TL 18.10). At the DEM slope (15–17°) a slab release needs a weak-layer friction angle well below 20°, which the paper allows (it cites 15° for very cold snow); the decisive quantity is the local step, which no one has measured.

**Survival timeline.** The evening was moonless, in mountain shadow from 14:40 and fully dark from ~19:40, with the tent at roughly −10 to −15 °C and a 8–15 m/s NW wind (wind chill −22 to −29) when it was pitched and abandoned; the cold front then took the lowland to −20 °C (Ivdel), −21 °C (Burmantovo, 03:00) and −31 °C (Nyaksimvol) by the early hours, i.e. about −20 to −26 °C at the tent with wind chill −34 to −45. The 1.55 km descent to the cedar took 35–85 min; the return attempt by three people stalled 320–650 m from the cedar (35–55 % of the way back, 20–40 min of uphill walking) with 180–230 m still to climb; the four in the ravine were 75 m from the fire in the only sheltered, forested spot. Nothing in the geometry requires more than a few hours for the whole sequence, and the deepening cold after midnight (rather than a blizzard: station winds were light, the searchers' "hurricane" is an inference from the bodies) is enough to make the return fatal in the clothing described. What the numbers do not settle: when the group left the tent (Ivanov's ~17:00 pitching time is itself an exposure-based inference made less secure by the 14:40 terrain sunset) and whether the ravine four died of cold or injuries — that belongs to the forensic notes.

## 7. Files

* Report: `research/geo-timeline-weather.md` (this file).
* Code and data: `code/geo/` — `README.md`, `run_all.sh`, `geo_common.py`, `dem_slope.py`, `astro.py`, `weather.py`, `walking.py`, `horizon.py`; `data/coordinates.csv`; outputs in `code/geo/out/` (`slopes_at_sites.csv`, `profile_tent_cedar.csv`, `profile_upslope.csv`, `dem_summary.json/.md`, `map_dem.png`, `profile_tent_cedar.png`, `astro_tables.md/.json`, `ghcn_daily_1959.csv`, `weather_tables.md`, `windchill_table.csv`, `distances.csv`, `walking.md`, `horizon.csv/.md`); raw downloads (57 MB) in `code/geo/raw/`.
