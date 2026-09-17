# Viewshed test (viewshed.py)

Target: Po plain = DEM < 400 m, east of 7.3E, north of 44.4N. Rays every 0.25 deg to 120 km; curvature + refraction k=0.13; observer 2 m.

| col | DEM height at col (m) | plain visible from col | % azimuths (col) | nearest plain from col (km) | first descent point with plain visible (km from col) | % az there | +100 m knoll: visible / % az | +300 m knoll: visible / % az | vantage scan (cells <=1.5 km, <=300 m above): n seeing plain / n scanned; best % az |
|---|---|---|---|---|---|---|---|---|---|
| Col du Mont-Cenis | 2088 | no | 0.0 | - | none within 10 km | - | no / 0.0 (2197 m, 370 m away) | yes / 0.2 (2394 m, 767 m away) | 3 / 61; best 0.5% (2383 m, 1053 m away) |
| Col Clapier | 2479 | yes | 0.6 | 79.6 | 1.00 | 4.9 | no / 0.0 (2580 m, 290 m away) | no / 0.0 (2795 m, 661 m away) | 29 / 56; best 8.1% (2712 m, 1400 m away) |
| Col du Petit Mont-Cenis | 2181 | no | 0.0 | - | none within 10 km | - | no / 0.0 (2296 m, 458 m away) | no / 0.0 (2567 m, 770 m away) | 0 / 57; best 0.0% (2456 m, 1496 m away) |
| Col du Petit-Saint-Bernard | 2189 | no | 0.0 | - | none within 10 km | - | no / 0.0 (2303 m, 404 m away) | no / 0.0 (2512 m, 1009 m away) | 0 / 89; best 0.0% (2288 m, 1489 m away) |
| Col de Montgenevre | 1853 | no | 0.0 | - | none within 10 km | - | no / 0.0 (1956 m, 387 m away) | no / 0.0 (2156 m, 1090 m away) | 0 / 91; best 0.0% (2142 m, 1253 m away) |
| Col de la Traversette | 2912 | yes | 17.3 | 25.6 | 0.25 | 11.5 | yes / 21.7 (3048 m, 220 m away) | none within 2.5 km | 14 / 18; best 25.6% (3001 m, 960 m away) |
| Col de Larche | 1996 | no | 0.0 | - | none within 10 km | - | no / 0.0 (2098 m, 420 m away) | no / 0.0 (2298 m, 847 m away) | 0 / 68; best 0.0% (2132 m, 1475 m away) |
| Col du Grand-Saint-Bernard | 2472 | no | 0.0 | - | none within 10 km | - | no / 0.0 (2576 m, 201 m away) | no / 0.0 (2780 m, 643 m away) | 0 / 57; best 0.0% (2753 m, 1419 m away) |
| Col Agnel | 2731 | no | 0.0 | - | n/a | - | no / 0.0 (2833 m, 564 m away) | no / 0.0 (3056 m, 1283 m away) | 0 / 47; best 0.0% (2736 m, 1246 m away) |
