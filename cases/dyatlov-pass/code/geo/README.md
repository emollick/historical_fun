# Dyatlov Pass – geospatial, astronomical and meteorological checks

Independent, reproducible computations behind `research/geo-timeline-weather.md`.
Nothing depends on network access once `raw/` is populated.

## Layout

| path | what |
|---|---|
| `geo_common.py` | shared helpers: WGS84 local-metric projection around the tent, haversine, bearings, loader for `data/coordinates.csv` |
| `dem_slope.py` | Copernicus GLO-30 slope/aspect at every candidate site (Horn 3×3 + least-squares plane fits of radius 30/50/100/150 m + Monte-Carlo noise), profile tent→cedar every 25 m, profiles 300 m upslope of the tent (fall line and toward the summit), map and profile figures, Mapzen "terrarium" cross-check |
| `astro.py` | sunrise/sunset, civil/nautical/astronomical twilight, moonrise/moonset, phase, sun/moon altitude at chosen hours (PyEphem 4.2.1; independent NOAA solar-position check implemented inline; time zone verified with tzdata `Asia/Yekaterinburg`) |
| `weather.py` | GHCN-Daily extraction for 6 stations, 28 Jan–5 Feb and 24 Feb–10 Mar 1959; Burmantovo 1 Feb 1959 hourly sheet from Maslennikov's notebook; JAG/TI 2001 wind-chill table |
| `horizon.py` | terrain horizon around the tent from the DEM (curvature + refraction) and the times the sun actually clears / disappears behind the terrain |
| `walking.py` | distances between all mapped points (vs. the case-file distances), tent→cedar drop, walking-time envelopes, return-attempt geometry |
| `run_all.sh` | re-runs all scripts in order (`sh run_all.sh`) |
| `data/coordinates.csv` | every coordinate used, one row per source, with the source and caveats (this is the "coordinates table with sources") |
| `out/` | all results: `slopes_at_sites.csv`, `profile_tent_cedar.csv`, `profile_upslope.csv`, `dem_summary.json/.md`, `map_dem.png`, `profile_tent_cedar.png`, `astro_tables.md/.json`, `ghcn_daily_1959.csv`, `weather_tables.md`, `windchill_table.csv`, `distances.csv`, `walking.md`, `horizon.csv`, `horizon.md` |
| `raw/` | raw downloads (≈40 MB): DEM tile, terrarium tiles, GHCN station files + station list + readme, dyatlovpass.com pages (HTML + extracted `.txt`), Google-My-Maps KML export, Nature paper + supplements, Wikipedia pages, OSM Nominatim result, Maslennikov notebook scans |

## Data sources (all open)

* **DEM**: Copernicus DEM GLO-30, tile `Copernicus_DSM_COG_10_N61_00_E059_00_DEM.tif` from the public AWS bucket
  `https://copernicus-dem-30m.s3.amazonaws.com/` (md5 `0c15753d8bd0c99d05fafaa78e819443`, 21 MB). Float32 metres above EGM2008,
  WGS84 geographic grid, 1″ (lat) × 2″ (lon) at 60–70° N = 31.0 m × 29.3 m here, `GTRasterType = PixelIsPoint`, tie point (59.0 E, 62.0 N) at raster (0,0).
  Read with `tifffile` + `imagecodecs` (floating-point predictor). It is a *surface* model (TanDEM-X 2011–2015): fine on the treeless slope, biased upward by canopy height in the forest near the cedar.
  Spec accuracy: absolute vertical < 4 m LE90, relative vertical < 2 m LE90 (slope < 20 %), horizontal < 6 m CE90.
* **Cross-check DEM**: AWS/Mapzen terrain tiles `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/14/{x}/{y}.png`, tiles x=10895–10897, y=4592–4594
  (decoded as `(R*256+G+B/256)-32768`). North of 60° N these derive from coarser global sources; used only as a sanity check.
* **Coordinates**: dyatlovpass.com Google My Maps (`mid=1ir_5s1TxKPbmckWlLdNRzfqb5ZE`, KML export in `raw/dyatlovpass-googlemap.kml`),
  A. Konstantinov's article "Determining where the Dyatlov group's tent was found in 1959" (dyatlovpass.com/tent-location, 9 Oct 2024),
  OpenStreetMap (Nominatim query "Перевал Дятлова"), en/ru Wikipedia infoboxes.
* **Case file**: dyatlovpass.com English transcriptions (sheets 2, 3–6, 36–39, 62–75, 88–93, 136–198, 209–220, 298–300, 309–312, 313–315, 316–329, 330–339, 341–343, 362–369, 384–387), Maslennikov's notebooks 1 and 2 (text + scans), the Burmantovo weather sheet, the 2019 Pigoltsina microclimate study as reported by Komsomolskaya Pravda (dyatlovpass.com/investigation-materials-2).
* **Gaume & Puzrin 2021**: Communications Earth & Environment 2:10, https://www.nature.com/articles/s43247-020-00081-8, plus Supplementary Information (`raw/nature-s43247-020-00081-8_MOESM3_ESM.pdf`) and the peer-review file.
* **Weather**: NOAA GHCN-Daily `by_station` files for RSM00023921 (Ivdel), RSM00023724 (Nyaksimvol), RSM00023711 (Troitsko-Pechorsk), RSM00023914 (Cherdyn), RSM00023418 (Pechora), RSM00028044 (Serov), RSM00023813 (Ust-Unya, precipitation only), RSM00028033 (Karpinsk, precipitation only); station list `ghcnd-stations.txt`; `readme.txt` for flags (source flag `r` = All-Russian Research Institute of Hydrometeorological Information – World Data Centre). Burmantovo has no GHCN-Daily record (WMO 23904 in GHCN is Koigorodok); ERA5/20CR were not attempted.
* **Astronomy**: PyEphem 4.2.1 (self-contained ephemerides). Time zone: tzdata `Asia/Yekaterinburg` = UTC+5 from 1930-06-21 to 1991 (Sverdlovsk decree time); asserted in `astro.py`.
* **Magnetic declination** (to compare Maslennikov's compass azimuths with true bearings): IGRF-13 via `ppigrf` → 17.5° E at the tent on 1959-02-01.

## Method notes

* Local metric grid: equirectangular about the tent with WGS84 metres-per-degree (111 442 m/° lat, 52 812 m/° lon at 61.7585° N); errors < 0.1 % over the < 5 km used.
* Slope: Horn (1981) 3×3 on the native grid (central differences spanning ~60 m); least-squares planes through all pixel centres within radius R (R = 30 m holds only 2–4 pixels and is reported as "n/a"; R = 50 m ≈ 9 pixels, R = 100 m ≈ 35, R = 150 m ≈ 80). Aspect = downhill compass direction. Monte Carlo: 200 realisations of N(0, 1.5 m) pixel noise → standard deviation of each slope estimate.
* Profiles: bilinear interpolation, samples every 25 m; "grad25/50/100" = centred difference over that base length.
* Wind chill: JAG/TI 2001 (Osczevski & Bluestein 2005), 10-m wind in km/h.

## Re-running

```
pip install numpy scipy matplotlib pillow tifffile imagecodecs ephem ppigrf
sh run_all.sh
```
