# Legio IX Hispana — database catalogue: method, queries, filtering, gaps

Output: `database_catalogue.csv` (245 rows; columns source_db, db_id, url, publication_refs, province, findspot_modern,
findspot_ancient, type, text, date_from, date_to, date_basis_if_stated, person, rank, **include**, notes).
`include` = `yes` (names IX Hispana / leg. VIIII-IX in an imperial context), `flag` (attribution uncertain: earlier cognomen
Macedonica/Triumphalis, 1st-c.-BC "leg. VIIII", fragmentary, unprovenanced, duplicate record), `no` (documented false hit).
Rows: EDH 37 (34 yes, 2 flag, 1 no); EDCS 208 (189 yes, 13 flag, 6 no). After de-duplicating EDH/EDCS concordances and
EDCS double entries (second copies, CIL V *422, duplicate graffito/tombstone records, column b, York stamps b–c) the
catalogue represents **c. 195 distinct monuments**, of which **135 are stamped tiles / small graffiti from Britain**.
Raw API responses (working copies, not included in this folder): `raw/` (EDH: `edh_*.json`, `edh_records/HD*.{json,xml,html}`; EDCS: `edcs_search_*.json`,
`edcs_monuments/*.json`, `edcs_indexes/*.json`, `edcs_js/app.js`; cross-checks: `raw/crosscheck/`).
Build script: `build_catalogue.py` (contains the manual curation table). Comparison legions: `legion_counts.py` → `legion_counts.csv`.

## 1. EDH (Epigraphic Database Heidelberg) — public JSON API

Endpoint discovered from https://edh.ub.uni-heidelberg.de/data/api : `GET /data/api/inschrift/suche?atext1=<text>&limit=N`
(`atext1` = transcription search, automatic truncation, brackets ignored; other params: provinz, land, fo_modern, fo_antik,
dat_jahr_a/e, inschriftgattung, hd_nr). Search hits carry only id/country/findspot_modern/text/literature/type; **province,
ancient findspot and dating were taken from the per-record EpiDoc XML** `GET /edh/inschrift/HDxxxxxx/xml` (`origDate
notBefore-custom/notAfter-custom`, `placeName type=province|ancient|modern`), the per-record JSON `/edh/inschrift/HDxxxxxx/json`
(commentary, type_of_monument, literature) and the HTML page (People block). NB: the EDH JSON export swaps `not_before` /
`not_after` for many records (e.g. HD069928: not_before 108, not_after 107); the XML values were used.

Queries run (literal `atext1` values → total hits; all with `limit=2000..10000`):

| atext1 | hits | | atext1 | hits |
|---|---|---|---|---|
| VIIII Hisp | 11 | | IX Hisp | 9 |
| VIIII Hispan | 11 | | IX Hispan | 9 |
| VIIII H | 64 | | legionis VIIII | 20 |
| legionis IX | 10 | | leg VIIII / leg IX | 0 / 0 (brackets are expanded, so "leg(ionis)" = "legionis") |
| legio VIIII / legio IX | 1 / 2 | | legione(m) VIIII/IX | 1 / 0 / 0 / 0 |
| VIIII (all) | 1057 | | Hispan | 478 |
| Hispana / Hispanae | 39 / 20 | | Hispanien / VIIII Hispaniensis | 3 / 0 |
| nona / nonae Hisp | 388 / 0 | | Ἱσπαν (Greek) | 1 (coh. XIII Hispanorum) |
| name checks: Caristanio 5, Duccius 4, Scipioni 10, Aemilio Caro 1 (Arabian diploma), Triumphal 60; Sextio Florentino, Aemilio Karo, Cornelio Scipioni, Moranus, Petillio Ceriali, Caesio Nasicae, Latinio Macro, vexillationis Britannicae: 0 each | | | | |
| Britannia (for CIL VI 3492) | 64 (column not in EDH) | | Germania superior | 15 |

Union of all hit lists: 1,919 records → regex filter on bracket-stripped transcription
(`\bVIIII\s*Hisp`, `\bIX\s*Hisp`, `\bleg\w*\W+(VIIII|IX)\b`, `\bnon(a|ae)\W+Hisp`, `\bVIIII\s*H\b`, `\bIX\s*H\b`,
`Hispanien`, `Hisp\w*\s*/?\s*(IX|VIIII)\b`) → 37 candidates, all fetched in full and read by hand.
Excluded: HD050953 (auxilia Hispaniensia). Flagged: HD026601/HD056334 (leg. VIIII *Macedonica*, Augustan; identity with
IX Hispana per Ritterling/Keppie). EDH does not hold CIL VI 3492 (Rome coverage limited to AE-published texts) nor most of the
CIL-only veteran tombstones of Italy/Gaul; it has 14 British records (11 stones, 3 stamp entries).

## 2. EDCS (Clauss–Slaby)

`https://db.edcs.eu/epigr/epi.php` now redirects (301) to a new JavaScript front end at **https://edcs.hist.uzh.ch/**; the
old POST form (`p_text`, `p_belegstelle` …, `epi_ergebnis.php`) no longer exists. From `assets/app.js` the real interface is:

* `GET https://edcs.hist.uzh.ch/api/search?q=<term>[&q2=..&q3=..]&mode=<t|r per term, uppercase = negated>[&type=fs|kl]`
  → JSON array of numeric monument ids (`t` = plain substring on the resolved text with brackets removed, `r` = regex;
  `type=kl` searches the unresolved majuscule text, `fs` the original text).
* `GET https://edcs.hist.uzh.ch/data/monument/<first 3 of 8-digit id>/<8-digit id>.json` → `{d:{g:place_id, m:material,
  q:[[source_idx, vol, no]…], i:[{t:text, d:[from,to], g:[category ids]}…]}}`; decoded with
  `/data/indexes/places.json` (geo_id → place, province index), `/data/indexes/lookups.json` (provinces, categories,
  materials), `/data/indexes/sources.json` (citation abbreviations). `/data/indexes/searchable.json` (19 MB) lists every
  monument with place id and dating (used for the comparison-legion counts).
* Web URL for a record: `https://edcs.hist.uzh.ch/monument/EDCS-xxxxxxxx`.

Scripted access worked (the proxy occasionally reset connections; every request was retried with `curl --retry 6`).
Queries (literal URL → hits): see the full list in `raw/edcs_search_counts.json`; main ones:

| q | mode | hits | | q | mode | hits |
|---|---|---|---|---|---|---|
| VIIII Hisp | t | 30 | | IX Hisp | t | 131 (includes coh. IX Hispanorum) |
| VIIII H | t | 383 | | legionis VIIII / legionis IX | t | 49 / 19 |
| VIIII Hispan / IX Hispan | t | 30 / 130 | | Hispaniens / Hispanien | t | 5 / 6 |
| `leg[a-z()]* (VIIII\|IX)( \|$\|/)` | r | 201 | | `(VIIII\|IX) ?Hisp` | r | 161 |
| VIIII HISP / IX HISP / VIIII HIS / VIIII H / LEG VIIII / LEG IX | t, type=kl | 24 / 123 / 26 / 369 / 1 / 0 | | Hispana IX / nonae Hisp | t | 2 / 2 |
| XXX Ulp + XV Apol | tt | 4 (→ CIL VI 3492a/b) | | II Aug + XX Vic + XXX Ulp | ttt | 2 |
| Sextio Florentino 1, Moranus 2, Aemilio Caro 4, Lentulo Scipioni 1, Triumphal 128, vexil+Britannic 36, Ισπαν 11; Aemilio Karo, Cornelio Scipioni, Petillio Ceriali, Caesio Nasicae, Latinio Macro/Latinius Macer, Hisp IX, Hisp VIIII, Hispana VIIII, nona Hisp, Ἱσπαν, leg IX: 0 | | | | | | |

Union: 608 monuments fetched (2 retried after resets) → same regex filter (+ `Nomina legionum`) → 208 candidates, each read by
hand; a slash-tolerant re-run (`(VIIII|IX)\s*/\s*H`) added only `diebus VIIII / h(ic)` noise. Excluded (kept in the CSV as
`no`): Iunia Hispaniensis (CIL VI 20888), praef. levis armaturae Hispaniensis (CIL X 6098), T. Varius Clemens' auxilia
Hispaniensia (Celeia), "diebus VIIII h.s." (CIL VIII 986), RIB II 2462.17* "LEG IX VIC" (falsum), AE 1984, 556 Corporales
(garbled "leg viiii" in a 161–169 dedication; almost certainly not IX Hispana).

Filtering rules applied: (a) explicit `leg. VIIII/IX Hisp(ana/-iensis)`, `leg. nonae Hispanae`, `LEG HISP IX`, `Nomina
legionum` list → yes; (b) `leg. VIIII/IX` without cognomen → yes when imperial (Britain, Aquileia/Pannonian-period group,
Flavian Reate colonists, London graffito), `flag` when the database dates it to the 1st c. BC (CIL V 5218, ILS 2337), when
it is the Ateste colonist CIL V 2507, the Mevania fragment CIL XI 5037, the Naples Cilician soldier CIL X 1769, or the new
Lentia graffito AE 2020, 932; (c) `leg. VIIII Macedonica` (ILS 928; AE 1919, 1) and `leg. VIIII Triumphalis` (ILS 2240) →
flag (earlier cognomina, usually identified with the later IX Hispana); (d) cohortes/alae Hispanorum, "Hispaniensis" as
personal or auxiliary epithet, leg. VII Gemina, "VIIII h(ic)/h(oras)" → no.

## 3. Cross-checks

* **livius.org** (`/articles/legion/legio-viiii-hispana/`; the `legio-ix-hispana` slug is 404): every inscription it cites
  is in the catalogue — CIL V 911 (EDCS-01600189), the Poreč Moranus stone (EDCS-04400181), the Scalesceugh tile
  (EDCS-49600361/62), Saufeius (EDCS-07800504/HD069558), the Ewijk/Nijmegen "LEG HISP IX" phalera (EDCS-03000651/HD050314),
  Sextius Florentinus (EDCS-21200156), Aemilius Karus (EDCS-17800486), CIL VI 3492 (EDCS-19000504/76900071). The only
  livius item **not** found in either database is P. Cornelius (Lentulus) Scipio's monument at Lepcis Magna (IRT); the man
  is present through the Brixia stone CIL V 4329 = ILS 940 (EDCS-04203381).
* **Wikipedia (en, raw wikitext)**: cites only CIL VI 3492 and ILS 9485 (Caristanius Fronto, EDCS-16201163/HD021539) plus
  the Nijmegen tile stamps, phalera and the Aachen altar of L. Latinius Macer (all present). Its two "senior officers who
  lived on for decades" are Aemilius Karus and Novius Crispinus (EDCS-20800611/24800728 = HD031258/61); Camurius Numisius
  Iunior (EDCS-23000342), Burbuleius Optatus (EDCS-20600417), Ti. Claudius Vitalis (EDCS-19700276) and L. Valerius Proclus
  (EDCS-29100179/HD042822) are the other post-Trajanic careers in the catalogue.
* **Ritterling, RE XII (1925) "Legio"**: de.wikisource `RE:Legio 1` (cols 1186–1829) is an unfilled placeholder
  ("unvollständig", body "[...]"); archive.org holds RE Bd. 12–16 only as page TIFFs without OCR (`PaulyWissowa2130`), so
  cols 1664–1670 could not be read online. Not checked against the primary text; the livius article (which summarises
  Ritterling) was used instead.

## 4. What is incomplete / caveats

* EDH's own dating criteria are not exposed in any export; `date_basis_if_stated` therefore records the EDH date range
  and, where the EDH commentary discusses the date, that commentary (e.g. HD013966: "106 = creation of Arabia … 161 =
  destruction of legio IX Hispana"). EDCS gives bare year ranges with no criteria.
* EDCS holds one record for the whole Nijmegen tile-stamp series (AE 1977, 541) and does not itemise Haalebos' later
  stamps; the RIB II 2462 series (York, Malton, Aldborough, Castleford, Carlisle, Scalesceugh, Stanwix, Leicester,
  Templeborough, Hilly Wood, Winteringham, North Thoresby, Cockridge, Lanthorp) is itemised (125 EDCS rows), all undated.
* Two EDCS records are unprovenanced auction objects (`IX HISP XI`, `IX / HISP / IX`) — flagged.
* The Corporales stone (AE 1984, 556) would be the only Marcus-Aurelius-period mention if its "leg viiii" were real; the
  EDCS transcription is corrupt and it is excluded.
* EDH comparison counts for the other legions were not done (only EDCS; EDH bulk CSV `edh_data_text.csv` exists at
  /data/download but was not processed in the time available).
