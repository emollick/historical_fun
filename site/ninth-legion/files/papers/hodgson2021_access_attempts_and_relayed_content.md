# N. Hodgson, "The End of the Ninth Legion, War in Britain and the Building of Hadrian's Wall", Britannia 52 (2021), 97–118 (doi:10.1017/S0068113X21000015)

## 0. STATUS: FULL TEXT NOT OBTAINED

The article is closed access at Cambridge Core and no legitimate open copy exists in any
aggregator, repository, search engine or archive tried (full log in section 1). No
`hodgson2021_full.txt` was therefore produced.

What WAS obtained and is used below (with clear attribution):

* Hodgson's own **abstract** (verbatim, from the Cambridge Core page; section 2).
* **E. P. Graafstal, "What Happened Next? Hadrian's Wall, the expeditio Britannica and the
  Fate of the Ninth Legion", Britannia 56 (2025), 25–55, doi:10.1017/S0068113X2510038X** —
  freely downloadable PDF on Cambridge Core (no access gate; Unpaywall still lists it as
  "closed", licence = cambridge.org/core/terms). Full text extracted to
  `graafstal2025_full.txt` (31 pp., ~120k chars). It is a direct sequel to and engagement
  with Hodgson 2021: it cites Hodgson 2021 in 14 footnotes with page numbers and quotes
  him verbatim three times. This is the best available proxy for Hodgson's arguments.
* **M. Symonds, "Was Hadrian's Wall a response to a military threat?", in Roman Frontier
  Archaeology – in Britain and Beyond (Archaeopress 2022), c. pp. 316–28** — open access
  (OAPEN); excerpt in `symonds2022_excerpt.txt`. Cites Hodgson 2021: 8–10.
* Wikipedia, "Legio IX Hispana" (cites Hodgson 2021 once).

**Page-number caveat.** Graafstal 2025 and Symonds 2022 cite Hodgson 2021 by its
*FirstView* pagination (pp. 1–22), not the printed pagination (97–118). FirstView p. N
corresponds approximately to printed p. 96+N (p. 1 = 97, p. 22 = 118), but the FirstView
layout may differ slightly, so treat printed equivalents given below as approximate.

Everything in sections 3–4 is therefore *reported* content: verbatim quotations are
Hodgson's words only where marked "Hodgson, quoted by Graafstal"; everything else is
Graafstal's or Symonds's paraphrase of Hodgson, or their own argument citing him.

---

## 1. What was tried for Hodgson 2021 and what each attempt returned

| # | Source / URL | Result |
|---|---|---|
| 1 | Cambridge Core direct PDF `…/content/view/63F63650070022B9E59DE06BF18D8729/S0068113X21000015a.pdf` (browser UA) | HTTP 200 but 302-chain to the `/abs/` abstract page: `text/html`, 922 KB, "Get access" box, no article body, no `citation_pdf_url` meta. |
| 2 | Same with the slug-suffix form that works for OA articles (`…a.pdf/end-of-the-ninth-legion-….pdf`) | Redirected to the abstract page (HTML). |
| 3 | HTML full-text URL without `/abs/` | Redirected back to `/abs/…`; "Get access" x2; no full text. |
| 4 | `…/content/view/S0068113X21000015` (Crossref "similarity-checking" link) | Redirected to abstract page. |
| 5 | `/core/product/identifier/S0068113X21000015/type/journal_article` | Redirected to abstract page. |
| 6 | `…/63F63650070022B9E59DE06BF18D8729/core-reader` | Redirected to abstract page. |
| 7 | Open-access check on the page / Crossref licence | No OA badge or CC licence; Crossref licence = `cambridge.org/core/terms`; only link is `similarity-checking`. **Not open access.** |
| 8 | Unpaywall `api.unpaywall.org/v2/10.1017/S0068113X21000015` | HTTP 200: `is_oa=false`, `oa_status=closed`, `best_oa_location=null`, 0 locations. |
| 9 | Semantic Scholar graph API (paperId 3f5f003afd35dfe5c0b6266766bd16e0436dd9a1) | `isOpenAccess=false`, `openAccessPdf.url=""`. `pdfs.semanticscholar.org/3f5f/…pdf` → HTTP 202, empty body. |
| 10 | OpenAlex `works/doi:10.1017/S0068113X21000015` (W3156819257) | `is_oa=false`, `oa_status=closed`, `any_repository_has_fulltext=false`; single location = doi.org. |
| 11 | OpenAIRE `api.openaire.eu/search/publications?doi=…` | `bestaccessright=CLOSED`; one instance (doi.org); `fulltext=None`. |
| 12 | CORE website search | HTTP 403 (Cloudflare bot check). |
| 13 | CORE API v3 `search/works/?q=doi:"10.1017/S0068113X21000015"` | First HTTP 429, then HTTP 200 with `totalHits: 0`. Title searches → HTTP 500 / 429. |
| 14 | Google Scholar (exact title, then loose query) | Record found, cluster id 3775831692660079227, **no [PDF]/[HTML] badge**; "all versions" page lists no alternative version; "cited by" = 3: Perring 2022 (book), Graafstal 2025 (Britannia; free), Symonds 2022 (OAPEN; free). |
| 15 | Newcastle University ePrints `eprints.ncl.ac.uk/search_results.aspx?q=…` | "Your search returned no results" for "Ninth Legion" and "Hodgson Hadrian's Wall"; the repository is frozen pending migration to Figshare. |
| 16 | Durham Research Online | `dro.dur.ac.uk` redirects to `palimpsest.dur.ac.uk` → empty reply (curl 52); `durham-repository.worktribe.com` → HTTP 403. |
| 17 | Tyne & Wear Archives & Museums / Great North Museum site search | Both resolve to `northeastmuseums.org.uk`; no hit for the article or any PDF. |
| 18 | Arbeia Society website | HTTP 522 (origin server down). |
| 19 | ResearchGate search (browser UA) | HTTP 403. |
| 20 | Academia.edu search (browser UA) | HTTP 403. |
| 21 | Bing (3 queries incl. `filetype:pdf`) | Returned only irrelevant dictionary hits for "end" (query mangled by bot handling). |
| 22 | DuckDuckGo html / lite | 202 bot-challenge page / connection reset. |
| 23 | Brave, Mojeek, Google web | 429 / 403 / consent-JS page. |
| 24 | Wayback Machine CDX for the article URLs | 7 captures (2021-05-01 … 2025-12-05) of the abstract page only; **no capture of any PDF or content URL**. Availability API → 429. |
| 25 | Internet Archive Scholar / fatcat API | Rate-limit page (twice) / connection reset (twice). |
| 26 | Zenodo API, BASE, Lens.org | Irrelevant hits / no results / Cloudflare challenge. |
| 27 | Wikipedia "Legio IX Hispana" wikitext | Cites Hodgson 2021 only for: "some scholars have ascribed the Nijmegen evidence to a mere detachment of IX Hispana, not the whole legion." |

Not attempted on purpose: spoofing a search-engine crawler user agent to defeat the
paywall, and shadow-library sites.

---

## 2. Hodgson's abstract (verbatim, Cambridge Core)

> It is often stated that the Ninth Legion was transferred from Britain and continued to
> exist until the 130s or beyond. The evidence is reviewed, and it is concluded that:
> (1) no more than a detachment of the legion went abroad, and that only for the period
> c. 105 to c. 120; (2) there is no prosopographical or other evidence which proves that
> the legion existed after the early 120s. Given that war, heavy Roman losses and an
> interruption in the building of Hadrian's Wall are directly attested in Britain,
> probably occurring in 122 or shortly after, it is argued that it is most likely that
> the legion was defeated and disbanded in connection with those events.

Bibliographic data (Crossref): Britannia 52, pp. 97–118, published online 13 April 2021.
Symonds 2022 gives the title with lower-case "legion"; Crossref has "Legion".

---

## 3. Hodgson's arguments as reported by Graafstal 2025 and Symonds 2022

Where an item says "Hodgson 2021, N" the page is Hodgson's FirstView page as cited by
Graafstal; "G p. N" = printed page of Graafstal 2025; "S p. N" = printed page of Symonds 2022.

### (a) Conclusion on the legion's fate and date

* Hodgson's own summary (abstract): the legion "was defeated and disbanded" in connection
  with war, heavy losses and the interruption of Wall-building "probably occurring in 122
  or shortly after"; this is "most likely", not certain.
* Graafstal's characterisation (G p. 27, fn 20 = "Hodgson 2021; cf. 2017, 41"): "An
  important paper by Nick Hodgson recently published in this journal has confirmed and
  amplified Keppie's findings: Legio IX Hispana vanished from the epigraphical radar after
  the early 120s, with its last attested officers on record around 124, and no reliable
  traces left on the Continent after that date. This opens up the intriguing possibility
  that the loss of the Ninth may, after all, have happened in Britain, the legion's last
  attested base."
* G p. 27 (fn 32 = Hodgson 2021): "a coupling of the loss of the Ninth, the transfer of
  the Sixth and the expeditio Britannica remains an attractive, and economic, solution to
  a centennial conundrum — and well within the bounds of evidence, as Hodgson has recently
  demonstrated."
* G p. 26 fn 6 lists Hodgson 2021 (with Jarrett 1976, Dobson 1978, A. Birley 1997/2005/
  2014, Breeze et al. 2012, Symonds 2021) among those who put the expeditio Britannica
  "in the run-up to Hadrian's visit of 122".
* G p. 28 fn 35: "Different elements of [the scenario of a crisis after 122] have been
  proposed earlier, especially in Stevens 1966; Breeze 2003; and Hodgson 2021."
* Symonds (S p. 320): "Hodgson (2021) has rekindled the argument that much of the IX
  Hispana legion may have been annihilated in Britain, rather than being redeployed to
  Nijmegen and then destroyed in the east."
* R. Hingley, "Hadrian and the Ocean", in the same OAPEN volume, p. 257: "Nick Hodgson's
  recent re-assessment of the available information has raised the possibility that the
  Ninth was lost in Britain, indicating the potential scale of trouble early in Hadrian's
  reign (Hodgson 2021)."
* **Hodgson, quoted by Graafstal** (G p. 47, fn 204 = Hodgson 2021, 16 [≈ printed 112]):
  "'Since the 1970s', Hodgson has pointed out in his recent contribution, 'the possibility
  that the Ninth was in Britain when it ceased to exist has disappeared so thoroughly from
  the educated public consciousness that many believe its departure from the island to be
  a matter of fact.'"
* Note the difference in date: Hodgson = "122 or shortly after"; Graafstal 2025 argues for
  a trigger event "early in 123" with the Ninth's disappearance "not much before 123/4"
  (G pp. 37–38, 50).

### (b) The officers' careers (Florentinus, Karus, Crispinus, Numisius, Asclepiades)

Graafstal's section "The end of the Ninth: not much before 123/4" (G pp. 37–38) follows
Keppie and Hodgson and Birley 2005; the framing is Graafstal's, but he cites Hodgson for
the conclusion and for the treatment of the two "late" names:

* G p. 37: "After all the good work that has been done by Keppie and Hodgson, [fn 118] the
  disappearance of IX Hispana, strange as it may sound, need not occupy us very long, the
  only point being its last attested moment of existence. We are lucky to have the careers
  of three high officers serving in what appear to be the final years of the legion…"
  * L. Aninius Sextius Florentinus (legate; tomb at Petra; governor of Arabia by a papyrus
    of 2 Dec. 127; proconsul of Narbonensis 123–4 or 124–5): "'is unlikely to have left
    the legion much before 124'" (Birley 2005, 228).
  * L. Aemilius Karus (tribunus laticlavius; consul March 144 per Eck & Pangerl 2015):
    tribunate "around 124"; "there is no reason to assume a much longer interval".
  * L. Novius Crispinus Martialis Saturninus (cos. des. 149; praetorship c. 135):
    "'Crispinus can hardly have been tribune earlier than the mid-120s.'" (Birley).
* **Hodgson, quoted by Graafstal** (G pp. 37–38, fn 128 = Hodgson 2021, 6 [≈ printed
  102]): "Hodgson rightly concludes that 'the[se] careers rule out the traditional loss of
  the legion in 117–19 but are compatible with loss or disbanding at some point in the
  120s.'"
* G p. 38 (fn 129 = "Cf. Hodgson 2021, 16–17" [≈ printed 112–13]): "It is of course
  possible to conjecture that one of the officers may have had his career retarded by
  some circumstance." — i.e. Hodgson 2021, 16–17 discusses the possibility of retarded
  careers as an objection/hedge.
* G p. 37 fn 118: "On the issues of Numisius Iunior (CIL XI, 5670) and Aelius Asclepiades
  (CIL X, 1769) see Keppie 1989, 251–3 and Hodgson 2021, 18–19, respectively." So Hodgson
  2021, 18–19 [≈ printed 114–15] is where Asclepiades (the tribune of IX Hispana on the
  Puteoli inscription) is dealt with; for Numisius Iunior Graafstal relies on Keppie 1989,
  251–2 ("the consul of 161 may well have been the son of the tribune Numisius Iunior …
  who may then have served a generation before c. 140"). Hodgson's abstract ("no
  prosopographical or other evidence which proves that the legion existed after the early
  120s") implies he rejects both Numisius and Asclepiades as proof of survival, but his
  exact arguments are not recoverable from the secondary sources.

### (c) Nijmegen and the Aachen altar

* Hodgson (abstract): "no more than a detachment of the legion went abroad, and that only
  for the period c. 105 to c. 120."
* Wikipedia paraphrase: Hodgson 2021 "ascribed the Nijmegen evidence to a mere detachment
  of IX Hispana, not the whole legion."
* G p. 47 (fn 207 = "For historiography: Hodgson 2021, 3" [≈ printed 99]): "Those intent
  on writing the Ninth out of Britain usually assumed that the unit came over in full
  strength. However, the archaeology of the legionary fortress does not support the
  presence of a complete legion after c. 104. What is massively attested at Nijmegen in
  the early second century, by over a hundred tile stamps, is a VEX(illatio)
  BRIT(annica)."
* G p. 48 (fn 217 = "A. Birley 2005, 229; 2013, 132; cf. Hodgson 2021, 4" [≈ printed
  100]): "Whatever the state of deployment of IX Hispana in 117, if the crisis in Britain
  was serious enough to merit a victory issue two years later, any remaining British
  troops posted at Nijmegen would likely have been repatriated to help deal with the
  problems." — so Hodgson 2021, 4 covers the detachment's return c. 117–20 (matching his
  "c. 105 to c. 120").
* The Aachen altar: Graafstal fn 205 lists the continental evidence as "only three stamped
  rooftiles …, a mortarium stamp …, a bronze pendant inscribed LEG IX HISP … and, likely
  connected, the inscription of L. Latinius Macer, primus pilus and praefectus castrorum
  (perhaps designate: Haalebos 2000, 472) of the Ninth, found at Aachen (AE 1968, 323)."
  Graafstal (p. 47 fn 213) explains the "unexpected presence of a praefectus castrorum" by
  the detachment finishing building projects begun by X Gemina. **Hodgson's own handling
  of the Aachen altar is not quoted by any obtained source and cannot be reported.**

### (d) Engagement with Campbell 2018 and Keppie 1989

* Keppie 1989: G pp. 26–27: "In 1989 Lawrence Keppie critically reviewed the evidence for
  a continued existence of the Ninth in the east, including the new diploma, but could find
  nothing conclusive. An important paper by Nick Hodgson … has confirmed and amplified
  Keppie's findings". G p. 28 fn 33: "much work having been done already, on the Ninth by
  Keppie, on the expeditio Britannica by Breeze, Dobson and Maxfield, and on both by
  Hodgson just recently." Hodgson's position is thus presented as building on and
  extending Keppie 1989 (and Keppie 2000).
* Campbell 2018 (D. B. Campbell, The Fate of the Ninth): Graafstal cites it only as "An
  exhaustive historiography" (fn 10); Hingley 2022, p. 257 (same OAPEN volume) cites it
  for the old view: "It used to be supposed that the Ninth Legion was destroyed in
  northern Britain early in Hadrian's reign (Campbell 2018) … This idea was abandoned
  several decades ago as a result of the hint from inscriptions that members of this
  Legion served in other areas of the Empire after the early 120s." **No obtained source reports
  how Hodgson 2021 engages with Campbell 2018**; Graafstal's fn 207 places Hodgson's
  historiographical review at Hodgson 2021, 3, which is where such engagement would be
  expected, but this is unverified.

### (e) The expeditio Britannica, RIB 3364 and the building of the Wall

* Date of the expeditio = 122: S p. 318: "The details of Sabinus' career provide broad
  parameters by suggesting a date in the 120s. Of these, one year seems more likely than
  the others: 122 (Hodgson 2021: 8–10 [≈ printed 104–6]). There are two reasons for this.
  The first is that, as Anthony Birley stressed, an emperor should normally be present
  during an expeditio, and 122 is when Hadrian was in Britain. Secondly, coin issues
  assignable to 122–123 refer to an EXPED AVG, which is most likely a contraction of
  expeditio Augusti". G p. 30 fn 53 ("Cf. lastly Hodgson 2021, 8"): "In recent discussions
  of Hadrian's British expedition, the coupling of expeditio with a geographical adjective
  has come to automatically imply the participation of the emperor." G p. 33 fn 84
  ("Hodgson 2021; Symonds 2021, 56–7, both following A. Birley 2014"): "the time window
  that has recently been proposed for it" (= 122). Graafstal 2025 then argues *against*
  this automatic equation (pp. 30–32) and for c. 123–4.
* Discharges/diplomas: G p. 51 fn 234 ("RIB 2401.6. Cf. Hodgson 2021, 9–10"): "After the
  major discharge of July 122, the releasing of emeriti from the auxilia had resumed by
  mid-September 124, perhaps indicating that the greatest difficulties were over." So
  Hodgson 2021, 9–10 uses the diplomas of 17 July 122 (CIL XVI 65) and 124 (RIB 2401.6) in
  dating the crisis.
* Heavy losses: **Hodgson, quoted by Graafstal** (G p. 29, fn 42 = Hodgson 2021, 14
  [≈ printed 110]): "Hodgson may well be right that Sabinus' 3,000 men came over
  'following heavy losses'." (Pontius Sabinus, CIL X 5829 = ILS 2726: praepositus of
  3,000 legionaries of VII Gemina, VIII Augusta and XXII Primigenia.)
* Mauretanian parallel: G p. 31 fn 69: "AE 1960, 28: misso cum exer(citu) in
  exp(editionem) Maur(etanicam/iae) ab Imp(eratore) Antonino Aug(usto). For other suggested
  expansions of Maur(…): Hodgson 2021, n. 51." So Hodgson's n. 51 discusses the formula of
  the Sex. Flavius Quietus inscription as a comparandum for "missus … in expeditionem".
* RIB 3364 (T. Annius, centurion of cohors I Tungrorum, Vindolanda, "killed in the war"):
  Graafstal (p. 29, fn 51 = "RIB 3364 with A. Birley 1998") and Symonds (p. 317: "One of
  those slain soldiers was probably Titus Annius, who died 'in war' … (RIB 3364)") both use
  it alongside Fronto's "what a number [of soldiers were killed] by the Britons" and the
  Sabinus/Agrippa inscriptions as the attestation of "war, heavy Roman losses" that
  Hodgson's abstract invokes. Hodgson's specific page for RIB 3364 is not cited by either.
* The Wall: G p. 32 fn 73 ("Graafstal 2012; 2018; Breeze 2019, 87, 91; Hodgson 2021, 11
  [≈ printed 107]; Symonds 2021, 67"): "Lately, there has been increasing favour for the
  imperial visit of 122 as the likely occasion for [the 'fort decision']." G p. 36 fn 111
  ("Hodgson 2021, 11; Graafstal and Breeze 2023, 169"): "given the logistic and social
  impact of the fort decision". G p. 28 fn 35 places Hodgson 2021 with Breeze 2003
  ("Warfare in Britain and the building of Hadrian's Wall") as a precursor of the view
  that the observed breaks in construction at Birdoswald, Housesteads and milecastle 37
  reflect a security crisis — matching Hodgson's abstract: "an interruption in the
  building of Hadrian's Wall [is] directly attested". G p. 49 fn 228 notes that Hodgson
  2017, 66 (not 2021) already suggested IX Hispana may have worked on the Turf Wall.

### (f) Probabilities and hedges stated by Hodgson (as far as recoverable)

* Abstract: "it is argued that it is most likely that the legion was defeated and
  disbanded"; "probably occurring in 122 or shortly after"; "no prosopographical or other
  evidence which proves that the legion existed after the early 120s" (a negative claim
  about proof, not a positive proof of destruction).
* Hodgson 2021, 6: the careers "are compatible with loss or disbanding at some point in
  the 120s" (compatibility, not demonstration).
* Hodgson 2021, 16–17: considers the possibility of retarded careers (per Graafstal fn
  129).
* Hodgson 2021, 14: Sabinus's reinforcements came "following heavy losses" — Graafstal:
  "may well be right".
* Symonds's rendering: Hodgson "rekindled the argument that much of the IX Hispana legion
  may have been annihilated in Britain" (note "much of" and "may").
* Graafstal's overall verdict on Hodgson: the coupling of the loss of the Ninth, the
  transfer of the Sixth and the expeditio is "well within the bounds of evidence, as
  Hodgson has recently demonstrated" (G p. 27), while Graafstal himself relocates the
  crisis to early 123 and treats the whole scenario as "no more than a possibility"
  (G p. 52).
* No numerical probabilities are reported by any secondary source.

---

## 4. Second target: E. Graafstal, "What happened in the summer of A.D. 122? Hadrian on the British frontier: archaeology, epigraphy and historical agency", Britannia 49 (2018), 79–111, doi:10.1017/S0068113X1800020X

**Status: full text NOT obtained** (no `graafstal2018_full.txt`). Attempts: Cambridge Core
PDF link in both forms (`…/5ECB860CFC347781357AEB11B8C7A5C2/S0068113X1800020Xa.pdf` and with
slug suffix) and the `content/view/S0068113X1800020X` link → all redirect to the abstract
page ("Get access" x2); Unpaywall `is_oa=false/closed`; OpenAlex closed, no repository
copy; Semantic Scholar `openAccessPdf.status=CLOSED`; Google Scholar exact-title query →
no PDF version; Crossref licence = cambridge.org/core/terms.

**Abstract (verbatim, Cambridge Core):**

> In the summer of a.d. 122, Hadrian (a.d. 117–38) visited Britain as part of his first
> major journey. It is broadly accepted that the construction of Hadrian's Wall was
> inaugurated on this occasion. Following recent advances in Upper Germany where the limes
> palisade is now known to have been under construction when Hadrian visited the province,
> this paper re-examines the various strands of evidence for the early chronology of the
> Wall. It is argued that work started well before a.d. 122 and that it was in fact the
> 'fort decision' which resulted from the imperial visit. The revised sequence offers a
> fresh perspective on several classic Wall problems and prepares the ground for a new
> understanding of unique features like the milecastles and Vallum.

**What it says about the Ninth Legion and the expeditio Britannica** (as reported by
Graafstal 2025's self-citations and by Symonds 2022; page numbers are printed pages of
the 2018 article):

* The paper is about Wall chronology, not the Ninth. Graafstal 2025 fn 1: "This argued
  that the outcome of Hadrian's visit to Britain was not the plan for the Wall itself, but
  the decision to add a dozen forts to it."
* Ninth Legion: only indirectly. 2018, p. 91 raised "earlier concerns about the timely
  arrival of VI Victrix for the start of the three-legion Wall project" (G fn 20) — i.e.
  if the Wall began before 122, the third legion at work on the first stretch cannot
  easily have been the Sixth; 2018, p. 90: "There is no evidence for involvement of the
  Sixth at this stage [Wall miles 7–22]" (G fn 223); 2018, p. 91 on the cascade of
  legionary transfers (I Adiutrix to Brigetio, TRIB POT [VII]I = 124) of which the Sixth's
  move was part (G fn 136). The 2025 paper makes explicit what 2018 left implicit: the
  third legion of the first season could be IX Hispana.
* Expeditio Britannica: 2018, pp. 98–9 already discussed the "exceptions to the rule" that
  expeditio + geographical adjective implies the emperor's personal participation (G fn
  23), i.e. it questioned the automatic equation of the expeditio with the 122 visit;
  2018, pp. 101–3 used the sequence of Maryport commanders (Maenius Agrippa's cohors I
  Hispanorum) to argue for a fort decision in 122 (G fn 99, 100); 2018, n. 189 on the
  number of Maryport tribunes (G fn 116).
* Related chronology: 2018, pp. 85, 88–9 — palisade in Upper Germany begun winter 119–20
  and preparations for the Wall likewise before 122 (G fn 31, 81); pp. 94–5 — the Jarrow
  inscription (RIB 1051) and the context of c. 118 (G fn 49, 79–80); p. 80 — milestones
  and road works announcing the imperial journey (G fn 26); pp. 99–100 — a Breeze-2003-
  like sequence but with the fort decision in 122 (G fn 7). Symonds 2022 (p. 318) cites
  Graafstal 2018 for the possibility that construction started c. 121, so that "both the
  expeditio and the fort decision could potentially have followed in 122".

---

## 5. Working files

* `hodgson2021_access_attempts_and_relayed_content.md` — this file; the working copies listed below are not included in this folder.
* `graafstal2025.pdf`, `graafstal2025_full.txt` — Graafstal, Britannia 56 (2025), full text
  (freely served by Cambridge Core).
* `graafstal2025_hodgson_passages.txt` — every passage of Graafstal 2025 mentioning Hodgson,
  with PDF/printed page numbers.
* `symonds2022_excerpt.txt` — Symonds 2022 chapter (OAPEN plain text, c. pp. 316–28);
  `oapen_frontiers.txt` — the whole OA volume's text.
* `cc_abs_page.html`, `graafstal_cc.bin` — the Cambridge abstract pages for Hodgson 2021
  and Graafstal 2018 (evidence of the paywall).
* `unpaywall_*.json`, `openalex_*.json`, `s2_*.json`, `crossref_*.json`, `openaire.json`,
  `core_api*.json`, `gscholar*.html`, `gs_cluster.html`, `gs_cites.html`, `wb_cdx3.json`,
  etc. — raw responses of the attempts listed in section 1.
* `fulford2022.pdf` / `fulford2022_full.txt` — Fulford, Britannia 53 (2022), CC-BY; checked
  and found to contain nothing on the Ninth Legion (kept for completeness).
