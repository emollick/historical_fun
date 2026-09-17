# Legio IX Hispana: the last decade of the Ninth Legion

Published page: https://historical-mysteries.netlify.app/ninth-legion/report
Local copy of the same page: `report.html` (this directory).

## The mystery
Some time between December 107 and December 108 the Ninth Legion, Legio IX Hispana, a unit of about five thousand Roman soldiers, finished a gate of its fortress at York in northern England. Part of the dedication slab, carrying the emperor Trajan's titles, survives (RIB 665, in Roman Inscriptions of Britain, the corpus of every Roman inscription found in Britain). It is the last dated text that names the legion anywhere. Soon after 165 the army's legions were listed on a column in Rome (ILS 2288); the Ninth is not among them. No ancient writer records where or how it ended in the half-century between.

## Why it is a mystery, and the sides
The evidence is indirect: inscriptions of officers who served in the legion and went on to dated posts, roof tiles stamped with the legion's name, and a few sentences in later writers about wars in which Roman soldiers died. Historians have read it in four ways.
- Destroyed or disbanded in Britain. The oldest view (Theodor Mommsen, 1885); in its modern form, argued by Nick Hodgson, an archaeologist of Hadrian's Wall (Britannia 52, 2021), and explored by the Dutch archaeologist Erik Graafstal (Britannia 56, 2025), the loss falls in fighting that followed the emperor Hadrian's visit to Britain in 122.
- Left Britain for the Rhine, on the strength of three stamped tiles found at the Nijmegen fortress in the Netherlands, and lost in the Bar Kokhba war, the Jewish revolt of 132-136.
- Left Britain and lost at Elegeia in Armenia in 161, where the historian Cassius Dio records a Roman legion destroyed by the Parthians (Werner Eck, 1972; Duncan Campbell, a historian of the Roman army, leans this way).
- Quietly broken up or merged into another legion, leaving no record.

## How the case was judged
Every inscription naming the legion was collected: all 133 records from Britain, and every entry in the Heidelberg and Clauss-Slaby online databases for the rest of the empire. The careers of the three senators who served in the legion as young officers, and whose later posts are dated, were worked back to the latest year the legion must have existed, and that arithmetic was run as a simulation. The Nijmegen finds were counted against the fortress's other finds. Five pieces of evidence were then weighed against the four endings, each weight given as a range from a base reading to a sceptical one. Result: the legion certainly existed in 122 and almost certainly in 124; nothing places it outside Britain after that; Britain in c. 122-130 is the probable ending, at about 50-65% on central readings. That probability is a judgement rather than a measurement; the British ending is probable but not proven.

## Assessment (probable)
- Evidence label: Probable. The evidence clearly favours a British ending over the others but does not prove it; the percentage moves when the same evidence is weighed differently.
- Probable ending: Britain, c. 122-130, destroyed or defeated and then disbanded in the years after Hadrian's visit of 122. This is the reading argued by Nick Hodgson (Britannia 52, 2021) and explored as a possibility by Erik Graafstal (Britannia 56, 2025, 25-55), who frames it as a possibility to be examined rather than a settled identification. It is not the agreed view of the field: Campbell, A.R. Birley and Keppie hold other positions, and no published response to Hodgson exists. The page supports the Hodgson-Graafstal interpretation; it does not establish it.
- Probability of a British ending, conditional on the four hypotheses and the likelihood ranges in `model/scenario_weights_v2.py`: about 50-65% on central readings (85% at the base reading, 36% at the sceptical reading, 19% with a sceptical reading and a 15% prior); Britain ranks first in 97-100% of weightings. Alternatives on the same conditions: Bar Kokhba 132-136 c. 14-19%; Elegeia 161 c. 3-5%; elsewhere or undocumented c. 17-23%. These are judgements stated so that they can be varied and tested, rather than measured frequencies.
- Last secure date and place as a unit: York (Roman Eboracum), 10 Dec 107 to 9 Dec 108, building a fortress gate (RIB 665).
- Floor on the legion's existence from the officers' careers: c. 123/124 secure (the legion's commander T. Aninius Sextius Florentinus, CIL III 87, governor of Arabia by 2 Dec 127 after governing Narbonensis in 123/4 or 124/5; the senatorial tribune L. Aemilius Karus, ILS 1077, consul 19 March 144); probably c. 125-128, the end of the service of the senatorial tribune L. Novius Crispinus (ILS 1070), whose tribunate falls c. 124-128. This is the latest date the careers require the legion to exist, not the date it ended. Terminus ante quem: absent from the Nomina legionum (ILS 2288, after 165).
- Nijmegen: a detachment, not the legion (3 tile stamps from one die against 196 stamps of the vexillatio Britannica, the task force from the British legions; fortress 16.5 ha, structural occupation ended c. 125/130; no legion-sized base free on the Lower Rhine after 122).
- Model outputs: the officers alone require the legion to exist in 124 at 88%, in 126 at 51%, in 130 at 6% (`model/career_model.py`).
- What would change the answer: any attestation of the legion or a serving soldier dated after c. 130; proof that the tribune of the Numisius stone (CIL XI 5670) is the consul of 161; Hadrianic Nijmegen finds at legion scale; a Ninth building stone on Hadrian's Wall in a sector dated after 124.

## What is new
- New evidence: none.
- New analysis of existing evidence: a complete catalogue (all 133 RIB records; an empire-wide sweep of the Heidelberg and Clauss-Slaby databases, 245 rows, c. 195 monuments, every query recorded); the career model; the explicit ranged weighting with its sensitivity rows; the quantified Nijmegen ratio; two under-used items (CIL VI 41280 and its circular database date; CIL V 7159).
- Confirms / shifts / overturns: agrees with a position already argued (Hodgson 2021 and Graafstal 2025; Ritterling 1925 for a British setting after 120), with the detachment reading of Nijmegen (Haalebos 2000; van der Veen 2025) and with the father-son reading of Numisius (Keppie 1989). It does not shift or overturn any published position. It rules out the traditional 117-119 date, which A.R. Birley 2005 had already done.

## Where the work fell short
- Campbell's book The Fate of the Ninth (2018) could not be read (no preview, scan, review copy or journal review). His case is stated from his 2010 article, all 57 blog posts and all 25 forum posts to February 2026, read in full (`papers/campbell_case_from_accessible_texts.md`). Arguments that exist only in the book are unknown here and are not answered.
- Hodgson 2021 is closed access; read in abstract and through the citations and quotations in Graafstal 2025 and in Matthew Symonds's 2022 chapter "Was Hadrian's Wall a response to a military threat?" (`papers/hodgson2021_access_attempts_and_relayed_content.md`); his 2021 book Hadrian's Wall: Creating Division is a separate work, cited on the page for the objection that a disaster near the emperor would have been recorded. Cited by FirstView page as in Graafstal.
- Haalebos 2000 and Ritterling 1925 were reached through citation; BGU I 140 was not re-read online.
- Reports of a 2018 debate at York between Russell and Campbell could not be verified.

## Notes on references
Florentinus is CIL III 87 = 14148,10, not ILS 1057. Keppie's paper is 1989 (BAR S553), not 1996. "CIL III 14147 = ILS 2483" is not the terminus for XXII Deiotariana; BGU I 140 of 4 Aug 119 is. Crispinus' intermediate posts were iuridicus of Asturia-Callaecia, legate of I Italica and proconsul of Narbonensis.

## Files
- `report.html`: the published page.
- `data/britain_inscriptions.{json,md}`, `britain_inscriptions_full.json`: all 133 RIB records (11 stones, 116 tile stamps, 2 graffiti, 2 unassignable, 1 rejected stamp, 1 forgery).
- `data/officers.{json,md}`: 20-entry prosopographical file with Latin texts, fixed points and arithmetic.
- `data/rhineland_evidence.{json,md}`: Nijmegen, Ewijk, Aachen items with contexts, counts and the fortress chronology.
- `data/literary_sources.{json,md}`: 32 passages with original text, translation, URL and bearing (Tacitus, Fronto, SHA, Dio, Lucian, ILS 2288, 2726, 2735, RIB 1051, 3364, BGU I 140).
- `data/scholarship.{json,md}`: positions from Mommsen 1885 to Graafstal 2025, with the genealogy of the four hypotheses.
- `data/database_catalogue.{csv,md}`: empire-wide EDH + EDCS sweep (245 rows, c. 195 monuments) with every query; `legion_counts.csv/.py`: comparison legions by province and date band; `build_catalogue.py`.
- `model/career_model.py` + `career_model_results.json`: Monte Carlo (numpy, N=200,000, seed 20260914). `model/scenario_weights_v2.py` + `.json`: the ranged likelihood table, posteriors and sensitivity used on the page; `model/scenario_weights.py` + `.json`: the earlier point-value weighting, kept for comparison. `model/make_charts.py` + SVGs: the two figures. `model/build_report.py`, `template.html`, `style.css`, `build_tables.py`: the page build.
- `papers/graafstal2025_britannia56_text.txt`: text of Graafstal 2025; `papers/graafstal2025_hodgson_passages.txt`: every Hodgson citation in it; `papers/hodgson2021_access_attempts_and_relayed_content.md`; `papers/campbell_case_from_accessible_texts.md`.
