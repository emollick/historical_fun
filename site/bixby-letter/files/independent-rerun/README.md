# A second implementation of the Bixby letter n-gram tracing tests

The Bixby letter is the condolence Abraham Lincoln signed on 21 November 1864 to Lydia Bixby of Boston, who was reported to have lost five sons in the war. No manuscript survives, and since the 1920s some have held that his secretary John Hay wrote it. In 2019 a team of forensic linguists led by Jack Grieve tested the question with n-gram tracing, a method that asks which of two writers' known works contains more of the letter's short strings of letters and words, and attributed the letter to Hay. The report *The Bixby Letter* (https://historical-mysteries.netlify.app/bixby-letter/report), whose files sit one folder up from this one, reran that study and then tested the method on prose Lincoln is known to have written in the letter's own years and register. Under the study's design, 30 of 63 such pieces were attributed to Hay.

This folder is a second, independent implementation of the same tests, written from the published paper without sight of the first implementation's code, run on the same texts and then on texts chosen afresh. The published page for it is `report.html` (https://historical-mysteries.netlify.app/bixby-letter/rerun/). The question is whether the tests reproduce, not who wrote the letter.

## Verdict on reproduction

1. **Test 1, the attribution to Hay: reproduces.** With a fresh implementation of n-gram tracing written from the paper's description, and with candidate pools rebuilt from the first implementation's corpus files under the paper's design (Lincoln before 18 May 1860 against everything by Hay), the letter goes to Hay at all 17 n-gram lengths the paper used (word 1 to 3, character 3 to 16), by margins of 0.002 (character 3) to 0.145 (word 2). The paper reports the same 17 to Hay; the first implementation reports the same. Word 4 goes to Hay and word 5 to Lincoln on the single phrase "may be found in the", exactly as the paper reports.
2. **Test 2, the paper's validation on known writings: reproduces in outline, with more errors.** Leave-one-out attribution of all 1,397 pool texts (505 Lincoln, 892 Hay) gives F1 of 0.96 to 0.99 for both men at character 4 to 10, peaking at 7 and 8 characters, falling at longer lengths, with 1- and 2-character n-grams useless, which is the pattern of the paper's Tables 3 and 4. The majority of the character 4-to-10 analyses is right for 1,380 of 1,397 texts (98.8 percent); the paper reports 100 percent of 1,662. The 17 misses are concentrated in texts outside the two men's business prose: an 1842 eulogy, a temperance address, a letter to Mary Lincoln, verse, a reporter's third-person accounts, a signed appraisal.
3. **Test 3, the first implementation's register-matched pieces under the paper's design: reproduces in direction, at a lower rate.** Of its 63 Lincoln pieces, 19 (30 percent) go to Hay by the character 4-to-10 vote under the paper's sample rule with 50 random sequences, and 15 plus one tie (25 percent) under the first implementation's own rule (samples of 0.95 times the smaller pool, 10 sequences). The first implementation reports 30 of 63 (48 percent). Of the 57 Hay pieces, 2 go to Lincoln (the first implementation: 1). The Gettysburg Address and the Ellsworth letter go to Hay in both implementations; the McCullough letter goes to Lincoln here (4 votes to 3) and to Hay there. Accuracy on the Lincoln pieces at character 4, 5 and 6 is 0.29, 0.25 and 0.44 (the first implementation: 21 to 38 percent). The gap between 19 and 30 is in the Lincoln pool: with the 83,000 words of Lincoln's 1858 campaign speeches restored to the pool here, this implementation's own code sends 27 of 63 to Hay (see Test 3 below).
4. **Test 4, independently chosen texts.** On 97 pieces cut from 38 Lincoln documents of 1861 to 1865 chosen for this implementation, the paper's design sends 27 (28 percent) to Hay by the character vote; Hay's two 1861 essays are right for 72 of 76 pieces. With period-matched pools built from these documents and every piece tested with its whole parent document left out, Lincoln is right for 96 of 97 pieces and Hay's essays for 69 of 76. Under those pools the letter splits, 5 lengths to 2 for Lincoln on the character 4-to-10 vote and 9 to 8 for Hay across all 17, and the four letters Hay is known to have drafted for Lincoln's signature all go to Lincoln, so that split is evidence for neither man.

The paper's design misattributes Lincoln's elevated war-time prose at a rate well above its 2.6 percent error on his ordinary pre-1860 texts. The rate depends on what is in the Lincoln pool: 25, 28, 30 and 43 percent in four runs here (the last with the 1858 speeches restored), 48 percent in the first implementation. The higher figures alone might suggest that the 2019 attribution fails validation on known texts. The numbers support only this: the attribution reproduces, and its validation does not transfer to texts of the letter's period and register, where the design misattributes between a quarter and a half of Lincoln's known pieces. None of the results is evidence that Lincoln wrote the letter.

## What was read, and what was not

- Jack Grieve, Emily Chiang, Isobelle Clarke, Hannah Gideon, Annina Heini, Andrea Nini and Emily Waibel, "Attributing the Bixby Letter using n-gram tracing", Digital Scholarship in the Humanities 34(3), 2019, pp. 493-512, doi 10.1093/llc/fqy042, read in full in the author-accepted manuscript (University of Birmingham repository, https://pure-oai.bham.ac.uk/ws/files/53402456/Bixby_PREPRINT.pdf, 39 pages). The version of record at academic.oup.com answered HTTP 403 and was not read.
- The 2016 Aston seminar slides (Grieve and nine co-authors, "Attributing the Bixby Letter: A case of historical disputed authorship", LSS Seminar Series, 13 April 2016; https://www.dropbox.com/s/98mb706q9adst8t/LSS_BIXBY.pdf?dl=1, 69 slides) and the 2017 Corpus Linguistics slides and abstract (26 July 2017; https://www.dropbox.com/s/n38pa5ia716rol2/CL_BIXBY.pdf?dl=1; https://www.birmingham.ac.uk/Documents/college-artslaw/corpus/conference-archives/2017/general/paper200.pdf), both linked from https://sites.google.com/view/grievejw/presentations. Notes with page references: `notes/paper_notes.md`.
- From the first implementation, one folder up: its `README.md`, `report.html` and the sections `report_sections/sec_stylometry.html`, `sec_new.html`, `sec_top.html`; `corpus/README.md`; `corpus/hay_warprose/notes.md`; the data files `corpus/lincoln_basler.jsonl`, `corpus/hay.jsonl`, `corpus/hay_warprose.jsonl` (inspected, not used), `corpus/hay_warprose/clean_baker.txt` and `clean_ellsworth.txt` (used only to check this implementation's own extractions), `analysis/lapsley.jsonl`, `analysis/register.json` (the 63 plus 57 pieces), `analysis/specials.json` (the letter and the special texts), and its published report. Not opened: any `.py` file in its `analysis/` or `corpus/scripts/`, its `corpus/hay_warprose/build.py`, and its `analysis/results*` and `analysis/logs` folders.

## What was reimplemented

`code/ngt.py` is n-gram tracing written from the paper's section 3 (preprint pp. 11-14), sections 5 and 6:

- n-gram types of one level and length are extracted from the questioned text; word n-grams ignore case and punctuation, character n-grams are case-insensitive and keep punctuation and spaces; no n-gram spans a sentence.
- for each candidate a random sequence of texts is taken until its words reach the size of the smaller candidate's writing sample (paper p. 12: "roughly equal in length to the total number of words in the possible author writing sample with the fewest words"); the smaller sample is therefore used whole, as the paper's Gettysburg demonstration uses the whole Hay corpus;
- the score is the overlap coefficient, the share of the questioned text's n-gram types that occur at least once in the sample; scores are averaged over the random sequences (50 for the letter and the register pieces, 10 for the validation, as in the paper); the larger average wins; a tie is wrong for both authors;
- majority rules as in the paper: at least 4 of the 7 character 4-to-10 analyses; at least 2 of the 3 word 1-to-3 analyses.

Choices the paper leaves open, decided here: sentences end at . ! or ? followed by white space, except after common abbreviations and single initials; a word is a run of letters and digits with internal apostrophes; a text left out of its own author's sample is replaced by the next text in the random order so the sample keeps its size; the option `frac` scales the sample size (1.0 by default; 0.95 reproduces the first implementation's rule). The implementation checks, per n-gram, the first and second random-order positions of the texts containing it, so that leave-one-out over all pool texts runs in minutes (`code/run_tests.py loo`, about four minutes on four cores).

## The pools (paper's design, rebuilt here)

| Pool | Texts | Words | Built from |
|---|---|---|---|
| Lincoln before 18 May 1860 | 505 | 192,404 | Basler, Collected Works, vol. I (363 items kept of 410; dropped: documents only signed by Lincoln, DS/ES/LS, and items in another hand) plus Lapsley's 1905 edition for 1849 to 17 May 1860 (142 items; the two volumes of 1858 campaign speeches and debates with Douglas left out by default, see Test 3; datelines, addresses and signatures stripped) |
| Hay, everything | 892 | 499,867 | every item of the first implementation's `hay.jsonl` of at least 5 words: 1908 Letters and Diary, Thayer's letters, Addresses, the McKinley address, Castilian Days, The Bread-Winners, verse |
| Lincoln before 18 May 1860, 1858 speeches restored (`pools_debates.json`) | 521 | 275,806 | as above plus the 17 substantive items of Lapsley vols 3 and 4 (Lincoln's 1858 speeches and his side of the debates; a letter by Douglas, a section title and Douglas's questions dropped) |

The paper's own pools were 1,085 Lincoln texts (400,747 words, from Basler vols I to IV on the University of Michigan site, which answered HTTP 403) and 577 Hay texts (261,126 words, from Thayer's Life and Letters and four Gutenberg texts). The first implementation's were 580 and 891 texts (243,000 and 495,000 words), with the 1858 speeches in. So the Lincoln side here is half the paper's and a fifth smaller than the first implementation's, and the Hay side is twice the paper's. The full list of kept and dropped documents is `data/pools_manifest.csv` (and `pools_manifest_debates.csv` for the enlarged pool).

## Test 1: the letter

Paper's design, 50 random sequences, sample size 192,404 words (the whole Lincoln pool against random Hay samples). Margin is Lincoln's overlap minus Hay's.

| Type | Types in letter | Lincoln | Hay | Margin | Winner |
|---|---|---|---|---|---|
| word 1 | 86 | 0.895 | 0.961 | -0.065 | Hay |
| word 2 | 128 | 0.461 | 0.606 | -0.145 | Hay |
| word 3 | 128 | 0.133 | 0.180 | -0.047 | Hay |
| char 3 | 461 | 0.998 | 1.000 | -0.002 | Hay |
| char 4 | 582 | 0.983 | 0.996 | -0.014 | Hay |
| char 5 | 642 | 0.941 | 0.980 | -0.040 | Hay |
| char 6 | 677 | 0.855 | 0.934 | -0.078 | Hay |
| char 7 | 695 | 0.745 | 0.837 | -0.091 | Hay |
| char 8 | 702 | 0.625 | 0.711 | -0.086 | Hay |
| char 9 | 703 | 0.485 | 0.576 | -0.091 | Hay |
| char 10 | 700 | 0.353 | 0.453 | -0.100 | Hay |
| char 11 | 695 | 0.250 | 0.335 | -0.084 | Hay |
| char 12 | 690 | 0.165 | 0.234 | -0.068 | Hay |
| char 13 | 685 | 0.102 | 0.164 | -0.062 | Hay |
| char 14 | 680 | 0.071 | 0.117 | -0.047 | Hay |
| char 15 | 675 | 0.046 | 0.084 | -0.038 | Hay |
| char 16 | 670 | 0.033 | 0.062 | -0.029 | Hay |

Word 4: Hay (0.016 against 0.036). Word 5: Lincoln (0.0085 against 0.0056), the paper's "may be found in the". Character 1 and 2: ties at 100 percent. Character 17 to 20: Hay. The first implementation's report gives the same 17 to Hay, character 3 by 0.00004, the rest by 0.01 to 0.14, with 0.04 to 0.10 at character 5 to 12 and 0.14 at word 2; this implementation's margins are 0.04 to 0.10 at character 5 to 12 and 0.145 at word 2. The same 17 go to Hay under the first implementation's 0.95 rule with 10 sequences (`results/summary_frac095_nseq10.txt`). Under the enlarged pool with the 1858 speeches, the letter goes to Hay by the character vote 7 to 0 and at 16 of the 17 lengths with one tie (`results/summary_debates.txt`).

## Test 2: leave-one-out validation

All 1,397 pool texts, each attributed against the pools with itself removed; 10 random sequences per candidate; 25 n-gram types. F1 for Hay and Lincoln, this implementation against the paper's Tables 3 and 4:

| Type | Hay F1 here | Hay F1 paper | Lincoln F1 here | Lincoln F1 paper | Accuracy here | Accuracy paper |
|---|---|---|---|---|---|---|
| word 1 | 0.97 | 0.93 | 0.95 | 0.95 | 0.96 | 0.94 |
| word 2 | 0.98 | 0.94 | 0.97 | 0.97 | 0.98 | 0.96 |
| word 3 | 0.97 | 0.91 | 0.94 | 0.95 | 0.95 | 0.93 |
| word 4 | 0.92 | 0.80 | 0.87 | 0.92 | 0.89 | 0.85 |
| word 5 | 0.85 | 0.55 | 0.77 | 0.85 | 0.76 | 0.68 |
| char 1 | 0.17 | 0.59 | 0.10 | 0.21 | 0.08 | 0.23 |
| char 2 | 0.66 | 0.74 | 0.73 | 0.70 | 0.58 | 0.58 |
| char 3 | 0.95 | 0.89 | 0.94 | 0.88 | 0.93 | 0.85 |
| char 4 | 0.98 | 0.94 | 0.96 | 0.96 | 0.97 | 0.95 |
| char 5 | 0.98 | 0.95 | 0.96 | 0.97 | 0.97 | 0.96 |
| char 6 | 0.98 | 0.96 | 0.97 | 0.97 | 0.98 | 0.97 |
| char 7 | 0.99 | 0.96 | 0.98 | 0.98 | 0.98 | 0.98 |
| char 8 | 0.99 | 0.96 | 0.98 | 0.98 | 0.99 | 0.98 |
| char 9 | 0.99 | 0.96 | 0.97 | 0.98 | 0.98 | 0.97 |
| char 10 | 0.98 | 0.95 | 0.97 | 0.97 | 0.97 | 0.97 |
| char 12 | 0.97 | 0.93 | 0.95 | 0.96 | 0.96 | 0.96 |
| char 16 | 0.94 | 0.86 | 0.90 | 0.94 | 0.92 | 0.91 |
| char 20 | 0.89 | 0.71 | 0.84 | 0.90 | 0.85 | 0.80 |

Majority votes: character 4 to 10, Hay recall 0.996 and precision 0.986 (F1 0.99), Lincoln recall 0.974 and precision 0.992 (F1 0.98), 17 texts wrong of 1,397 (the paper: all 1,662 right); word 1 to 3, Hay F1 0.99, Lincoln F1 0.98, 25 wrong (the paper: F1 at or above 0.95). The 13 Lincoln texts the character vote gets wrong: an 1830 appraisal signed with others, a reporter's third-person account of an 1836 speech, a 70-word note (1839), the Eulogy on Benjamin Ferguson (1842), the Temperance Address (1842, with its printed header), two letters to Andrew Johnston about poetry (1846) and the verse "The Bear Hunt", a 617-word letter to Mary Todd Lincoln (1848), a letter to John D. Johnston (1851), the reported argument in the Rock Island Bridge case (1857), a 109-word letter (1858), and the verse "To Linnie" (1858). The 4 Hay texts: a 27-word note (1889) and three official letters to senators (1900 to 1905). The paper's authors cleaned their corpus by hand and removed doubtful documents, which would remove several of these. Full per-text margins: `results/test2_loo_margins.csv`.

## Test 3: the first implementation's register-matched pieces

The 63 Lincoln pieces (about 150 words each, from 30 documents of 1861 to 1865) and 57 Hay pieces (22 from "Ellsworth", 34 from "Colonel Baker", the 55-word condolence of 1864), taken as given from the first implementation's `register.json` (copied here as `data/bixby_report_register.json`), attributed under the paper's design. None of their parents is in a pool.

| Run | Lincoln pieces to Hay, char 4-10 vote | Lincoln pieces to Hay, all 17 | Hay pieces to Lincoln, char 4-10 |
|---|---|---|---|
| This implementation, paper's sample rule, 50 sequences | 19 of 63 (30%) | 7 of 63 (11%) | 2 of 57 |
| This implementation, the first implementation's 0.95 rule, 10 sequences | 15 of 63 plus 1 tie (25%) | 7 of 63 | 2 of 57 |
| This implementation, 1858 speeches restored to the Lincoln pool, paper's rule, 50 sequences | 27 of 63 (43%) | 11 of 63 | 2 of 57 |
| The first implementation, its own code | 30 of 63 (48%) | not reported | 1 of 57 |

Per-length accuracy on the Lincoln pieces here (default pool): character 4, 5, 6: 0.29, 0.25, 0.44; character 7 to 10: 0.67, 0.78, 0.89, 0.89; character 11 to 16: 0.87 to 0.90; word 1 to 3: 0.51, 0.87, 0.90. The first implementation reports 21 to 38 percent at character 4 to 6 and recovery at long lengths, which this run confirms. The pieces wrong here include both Gettysburg pieces (2 votes to 5 each), both Ellsworth pieces (0 to 7 and 2 to 5), two Second Inaugural pieces, the Baltimore Sanitary Fair address, the Methodists reply, Bullitt, McClellan, Schurz, Grant of August 1863, Hackett, Weed (`results/test3_pieces.csv` lists every piece with its 25 margins). The McCullough letter goes to Lincoln here, 4 to 3. The two Hay pieces wrong are Baker pieces 6 and 7.

The cause of the gap between 19 and 30. *The Bixby Letter*, section 4, ran each implementation's code on the other's pool and traces the gap to the Lincoln pool; the code is not the cause. The first implementation keeps 19 items from Lapsley's third and fourth volumes, 83,000 words of Lincoln's speeches in the 1858 Senate campaign and his side of the seven debates with Stephen A. Douglas, which this implementation had left out because Lapsley prints a letter of Douglas's and his questions among them. By that report's figures, its code on this implementation's pool gives 19 of 63 and this implementation's code on its pool gives 26. The mechanism it describes is the sample rule: adding the speeches enlarges both candidates' samples by the same 84,000 words, and the extra words of Hay's mixed prose cover more of a condolence letter's strings than the extra words of Lincoln's stump oratory do. Checked here: restoring those items to the Lincoln pool (`KEEP_DEBATES=1 python3 build_pools.py`, 521 texts, 275,806 words) and rerunning with this implementation's own code sends 27 of the 63 pieces to Hay under the paper's rule with 50 sequences, so the pool difference accounts for the gap (`results/summary_debates.txt`, `results/test1_test3_letter_register_debates.json`).

## Test 4: this implementation's own texts

Lincoln: 38 documents of 1861 to 1865 chosen here for register (condolence, ceremony, personal and elevated public prose), cut into 97 pieces of about 145 words at sentence boundaries, at most five pieces per document, head or tail only for long state papers; 19 of the 38 documents are also among the first implementation's 30 (Lincoln left few texts in this register), 19 are not (Independence Hall, the First Inaugural's close, the 1862 message's close, Manchester, Corning, Conkling, the Philadelphia fair, the 166th Ohio, the Baltimore Bible reply, the last public address, among others). Hay: "Ellsworth" (Atlantic, July 1861) cut afresh from Gutenberg 11154 (identical to the first implementation's text, 4,136 tokens) and "Colonel Baker" (Harper's, December 1861) cut afresh from the archive.org OCR of vol. 24 (6,975 tokens against the first implementation's 6,982, nine differences, all hyphenated compounds and one OCR fault); 76 pieces; his 55-word condolence of 1864; and, as a period-matched but not register-matched set, all 110 letters and diary entries of 1861 to 1865 of at least 100 words in the 1908 edition, 185 pieces. Every document is listed with its source in `data/test4_sources.csv`; the downloaded source texts are in `data/downloads/`.

| Design | Lincoln pieces wrong (char 4-10) | Hay essay pieces wrong | Hay letters and diary pieces wrong |
|---|---|---|---|
| A: paper's pools (pre-1860 Lincoln, all Hay) | 27 of 97 (28%); 11 of 97 by all 17 | 4 of 76 (5%) | 1 of 185 (1%) |
| B: period-matched pools, parent document left out (Lincoln 38 docs, 14,168 words; Hay 113 docs, 38,506 words) | 1 of 97 (1%) | 7 of 76 (9%) | 8 of 185 (4%) |
| B2: as B with the Hay side restricted to the essays and the condolence (11,166 words) | 2 of 97 (2%) | 7 of 76 (9%) | not tested |

Under design A the Lincoln documents with pieces wrong are the Springfield farewell, the Ellsworth letter (both pieces), Manchester (3 of 4), the Philadelphia fair (3 of 3), the 166th Ohio (2 of 2), the Baltimore fair (2 of 5), the Second Inaugural (2 of 5), Conkling (2 of 5), Gettysburg (1 of 2), Hodges, the Methodists, Hackett, the First Inaugural's close, Schurz, the election-night serenade, the Maryland committee, the January 1865 committee, and the last address (1 each). Under designs B and B2 the letter splits (B: 5 lengths to 2 for Lincoln at character 4 to 10, 9 to 8 for Hay over all 17; B2: 4 to 3 and 10 to 7), Hay's own condolence goes to Lincoln, and the four letters Hay drafted for Lincoln's signature (Boker 1863, Charles Butler 1864, Driggs and Garrison 1865) go to Lincoln 7 to 0, 7 to 0, 6 to 1 and 7 to 0. Under design A the same four go Hay, Hay, Lincoln, Lincoln, and the condolence goes to Hay 7 to 0.

## What each result does and does not show

- Test 1 shows that the paper's attribution is a stable property of its design: the same result is obtained with a fresh implementation, with a Lincoln pool half the paper's size drawn partly from a different edition, and with a Hay corpus assembled from different books. It does not show that the design gives correct attributions for texts of the letter's kind.
- Test 2 shows that the method separates the two men's ordinary writings about as well as the paper says, and that its residual errors fall on Lincoln's verse, eulogy, temperance oratory and private letters, which is the same direction as the register effect.
- Tests 3 and 4 show that the design's accuracy on Lincoln's elevated prose of 1861 to 1865 is far below its accuracy on his ordinary texts, and that the loss is confined to short character n-grams. They do not fix the size of the effect: 25 to 30 percent on the first implementation's pieces with the default pool, 43 percent with the 1858 speeches restored, 28 percent on pieces chosen independently, 48 percent in the first implementation's run. The composition of the Lincoln pool moves it. The method stays right for at least half of these pieces and for 89 percent of the all-17 votes, so "fails validation" would overstate what the numbers show.
- Design B shows that period-matched pools separate the two men in this register too, on very small pools. It does not turn the letter's split under those pools into evidence for Lincoln: the method under those pools also calls Hay's known writing for Lincoln's signature "Lincoln", as the first implementation found for its own-hand design.
- The study's authors had noted the register problem themselves (2016 slides, slide 15: "we have not looked at detail at the effect of ... register variation"; slide 54: "We also need to test sensitivity to register variation"). The first implementation was the first to test it; this run finds the same effect at a lower rate.

## Limits of this check

- The paper's own corpora were not obtainable (quod.lib.umich.edu answered HTTP 403; Basler vols II, III, V and VI are not in the first implementation's files). The Lincoln pool here is 192,000 words against the paper's 401,000, and 106,000 of those words are Lapsley's printed text rather than Basler's manuscript-based text. The Hay corpus differs from the paper's in source and size. So Tests 1 and 2 reproduce the paper's result on a reconstruction of its design, not on its data.
- Only the accepted manuscript was read; the published version could not be downloaded.
- Tokenisation and sentence splitting are this implementation's own; the paper does not specify them. The letter counts 138 words here against the paper's 139.
- The first implementation's 63 and 57 pieces were used as given; their selection, cutting and OCR were not checked beyond the two essays.
- Test 4's Lincoln texts overlap the first implementation's by 19 documents; a fully disjoint set does not exist for this register.
- Design B's pools are small (14,000 and 38,000 words), so its long-n-gram overlaps are near zero and its votes rest on characters 4 to 10.
- The first implementation's code was not read here. The cause of the gap between its 30 of 63 and the 19 of 63 here is its finding, checked here only by the run with the enlarged pool.

## Files

- `report.html`: the published page (https://historical-mysteries.netlify.app/bixby-letter/rerun/), generated by `code/make_report.py` from the numbers in this README and the result files.
- `code/ngt.py` the implementation; `code/build_pools.py` the pools (`KEEP_DEBATES=1` for the enlarged Lincoln pool); `code/run_tests.py` Tests 1 to 3 (`letter`, `loo`, `summary`; options `--nseq`, `--frac`, `--tag`, `--pools`); `code/test4_build.py` and `code/test4_run.py` Test 4; `code/export_tables.py` the CSV tables; `code/make_report.py` the page.
- `data/pools.json`, `data/pools_manifest.csv` (every candidate document, kept or dropped and why); `data/pools_debates.json`, `data/pools_manifest_debates.csv` (the enlarged Lincoln pool); `data/bixby_report_register.json` and `data/bixby_report_specials.json` (copies of the first implementation's `register.json` and `specials.json`); `data/test4_docs.json`, `data/test4_pieces.json`, `data/test4_sources.csv`; `data/downloads/` (the Project Gutenberg and archive.org texts Test 4 was cut from).
- `results/summary.txt`, `results/summary_frac095_nseq10.txt`, `results/summary_debates.txt`, `results/test4_summary.txt`; per-text tables `results/test1_letter_by_type.csv`, `results/test2_loo_margins.csv`, `results/test3_pieces.csv`, `results/test4_pieces_design{A,B,B2}.csv`; raw JSON under `results/`.
- `notes/paper_notes.md` reading notes on the paper and the two slide decks.
- Reproduce: `cd code; python3 build_pools.py; python3 run_tests.py letter --nseq 50 --workers 4; python3 run_tests.py loo --workers 3; python3 run_tests.py summary; python3 test4_build.py; python3 test4_run.py all; python3 export_tables.py; python3 make_report.py`. For the enlarged pool: `KEEP_DEBATES=1 python3 build_pools.py; python3 run_tests.py letter --nseq 50 --workers 4 --pools pools_debates.json --tag _debates; python3 run_tests.py summary --tag _debates`. Python 3.11 with numpy. Seeds are fixed.
