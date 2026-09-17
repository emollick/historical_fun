# Hay Civil-War prose corpus (register-matched known texts) - notes

Output: `../hay_warprose.jsonl` (56 records, fields id/author/source/title/year/kind/period/word_count/text). Script: `build.py` (deterministic; rerun with `python3 build.py`).
Rules followed: no letters/diary, nothing after 1865, public-domain sources only.

## 1. "Ellsworth" - The Atlantic Monthly, vol. 8, no. 45 (July 1861), pp. 119-125. Unsigned.

Source: Project Gutenberg ebook #11154, "The Atlantic Monthly, Volume 08, No. 45, July, 1861" (Various).
- Search URL: https://www.gutenberg.org/ebooks/search/?query=Atlantic+Monthly+July+1861 (saved `gutenberg_search_atlantic_july1861.html`)
- Text URL: https://www.gutenberg.org/cache/epub/11154/pg11154.txt (saved `gutenberg_pg11154_atlantic_v08n45_july1861.txt`, 520,613 bytes, whole issue)
- The essay occupies lines 7748-8166 of that file (heading "ELLSWORTH." through "...why Ellsworth died."), between the poem ending "The fruits and flowers are kin." and "REVIEWS AND LITERARY NOTICES." Saved as `raw_ellsworth_gutenberg_pg11154_lines7748-8166.txt`.
- Cutting: heading line removed; the single footnote ("[Footnote A: Arthur F. Devereux, Esq., now in command of the Salem Zouaves ...]") and its "[A]" marker removed; Gutenberg italics underscores removed; Gutenberg "--" converted to a closed em-dash; line breaks inside paragraphs joined (the Gutenberg transcription carries no end-of-line hyphenation, so nothing needed rejoining); the two Tennyson verse quotations (indented lines) are kept inside the paragraph that introduces them, with " / " marking verse line breaks. The Gutenberg text has no running heads or page numbers. Spelling and punctuation otherwise untouched ("Bunker's Hill", "to-day", "systematizing").
- Clean text: `clean_ellsworth.txt` - 37 paragraphs, 4,099 words -> 22 pieces of 129-247 words (ids hay_ellsworth_01..22).
- Attribution: the magazine's own cumulative index, The Atlantic Monthly Index, vols. 1-88 (1857-1901) (archive.org item sim_atlantic_1857-1901_1-88_index; https://archive.org/download/sim_atlantic_1857-1901_1-88_index/sim_atlantic_1857-1901_1-88_index_djvu.txt, saved `archive_sim_atlantic_1857-1901_index_djvu.txt`) lists "Ellsworth, J. Hay ... 8 119" and, under "Hay, John", "... 8 119". Thayer, Life and Letters of John Hay (1915), vol. 1 (archive.org lifelettersofjoh01thayuoft, saved `archive_lifelettersofjoh01thayuoft_djvu.txt`) documents Hay's friendship with Ellsworth in Springfield and Washington; Burlingame (At Lincoln's Side, 2000; Lincoln's Journalist, 2006) also credits the piece to Hay. Internal evidence: first-person recollections ("He told me once ...", "a memorandum, which lies before me").
- First two sentences: "The beginnings of great periods have often been marked and made memorable by striking events. Out of the cloud that hangs around the vague inceptions of revolutions, a startling incident will sometimes flash like lightning, to show that the warring elements have begun their work."

## 2. "Colonel Baker" - Harper's New Monthly Magazine, vol. 24, no. 139 (December 1861), pp. 103-110. Unsigned.

Sources tried:
- Cornell Making of America (https://ebooks.library.cornell.edu/cgi/t/text/text-idx?c=harp;idno=harp0024-1): the page says Harper's moved to HathiTrust in 2018 (saved `cornell_moa_harp0024-1_index.html`). HathiTrust catalog (https://catalog.hathitrust.org/Record/008919716) answered HTTP 403 - not retried.
- archive.org search (`archive_search_harpers24.json`). Two OCR texts downloaded:
  a) https://archive.org/download/sim_harpers-magazine_1861-12_24_139/sim_harpers-magazine_1861-12_24_139_djvu.txt (the December 1861 issue; saved `archive_sim_harpers-magazine_1861-12_24_139_djvu.txt`; essay at lines 16734-18195, saved `raw_baker_archive_sim_harpers_1861-12_lines16734-18195.txt`). In this scan the right-hand column of several pages is clipped at the margin (p. 104: "a town of less / culture ... ster / ling ... som / time"), so it served only to cross-check doubtful words.
  b) https://archive.org/download/harpersnew24harper/harpersnew24harper_djvu.txt (bound vol. 24, Dec. 1861-May 1862, BYU-Idaho copy; saved `archive_harpersnew24harper_djvu.txt`, 5.2 MB; essay at lines 14098-15075, saved with context as `raw_baker_archive_harpersnew24harper_lines14043-15030.txt`). This is the base text.
- Cutting (build.py, `clean_baker` / `join_baker`): text taken from "RIVERS form no less striking ..." (foot of p. 102) to '... seeks to apologize."' (p. 110). Removed: running heads "COLONEL BAKER." / "HARPER'S NEW MONTHLY MAGAZINE.", bare page numbers 103-110, and the signature line "Vol. XXIV.- No. 139.- II" (p. 105). A blank-line gap in the OCR was treated as a paragraph break only when the previous line ends a sentence and the next begins with a capital; one case patched by hand (the p. 108/109 break falls inside the quotation "Lower, boys! Steady there! Keep cool ..."). End-of-line hyphens rejoined (about 190), except compounds broken at their own hyphen, kept as printed: Wheel-Horse, red-hot, half-estranged, recruiting-officer, pro-slavery (pre-eminently and Brigadier-General were broken at a later hyphen and come out right). Harper's thin spaces before ; : ! ? removed; quotation marks OCR'd as `" word "` closed up (odd/even alternation within a paragraph); em-dashes closed up as printed. Spelling untouched ("intrust", "manoeuvre", "gayly", "M'Dougal", "reconnoissance", "Korner" as OCR'd without umlaut).
- OCR corrections applied (each cross-checked against the December-issue OCR, which has the correct reading): o^|hnies -> of armies; republic-were -> republic were; settle^ -> settled; s;iw -> saw; "1 835" -> 1835; "w hen" -> when; "1 844" -> 1844; ".an" -> an; Keniucky -> Kentucky; towrn -> town; "M 'Dougal" -> M'Dougal; be^un -> begun; ruffinnism -> ruffianism; "tin; Gulf" -> the Gulf; "look his life" -> took his life; "Par more" -> Far more; "Prom all" -> From all; ithe -> the; "you sec" -> you see; "Pie went" -> He went; "di imposition" -> disposition; "awa}r" -> away; "Edwards's Perry" / "Eerry" -> Edwards's Ferry; "dying lire" -> dying fire; ''Good friend -> "Good friend.
- Clean text: `clean_baker.txt` - 37 paragraphs, 6,910 words -> 34 pieces of 139-252 words (ids hay_baker_01..34).
- Attribution: the magazine's own cumulative index, Harper's New Monthly Magazine, Index to vols. 1-70 (1850-1885) (archive.org item sim_harpers-magazine_1850-1885_1-70_cumulative-index; https://archive.org/download/sim_harpers-magazine_1850-1885_1-70_cumulative-index/sim_harpers-magazine_1850-1885_1-70_cumulative-index_djvu.txt, saved `archive_sim_harpers_1850-1885_index_djvu.txt`) lists "Baker, Edward Dickinson, John Hay ...... xxiv. 103" and the same article under "Hay, John." Thayer vol. 1, p. 122, quotes Hay's diary on Baker's death but does not cite the article; Burlingame (At Lincoln's Side, 2000, introduction) and Dennett (John Hay: From Poetry to Politics, 1933) credit it to Hay. Internal evidence: Springfield first-person voice ("of which I have been speaking"), "M. Hay" (Milton Hay, John Hay's uncle) named among the Springfield bar, and "A lady - who in her high position is still gracefully mindful of early friendships" (Mrs. Lincoln).
- First two sentences: "RIVERS form no less striking features in the pictures of history than in the face of nature. When dignified by the passage of armies, their course runs broadening through fame."

## 3. Other 1861-1865 Hay prose - not obtained

- Chronicling America (chroniclingamerica.loc.gov) answered HTTP 503 to title searches (`chronam_titles_missouri_republican.json`, `chronam_newspapers_missouri.json` hold the error pages). The loc.gov API (https://www.loc.gov/collections/chronicling-america/?fa=location_state:missouri&dates=1861/1864&fo=json, saved `locgov_chronam_missouri_facets.json`) shows the only Missouri titles digitized for 1861-1864 are Hermanner Volksblatt, Glasgow Weekly Times, Soldier's Letter, Mexico Weekly Ledger and The Palladium: the Daily Missouri Republican is not in Chronicling America, so Hay's "Ecarte" columns could not be taken from a free archive. Burlingame's Lincoln's Journalist (in copyright) was not used. No other free 1861-1865 Hay prose was located within the time budget.

## Segmentation

`pack()` in build.py accumulates whole paragraphs; a piece closes at a paragraph end once it holds >= 130 words, and if the next sentence would push a piece past 250 words the piece closes at that sentence boundary (so some pieces begin or end mid-paragraph, never mid-sentence). Paragraph breaks inside a piece are kept as blank lines. word_count = whitespace tokens. Every piece was checked to begin with a capital or quotation mark and end with terminal punctuation.

## Pieces to treat with care (quoted matter that is not Hay's own prose)

Both essays quote other people's words at length (Tennyson's Idylls; Ellsworth's militia memorandum and letters; Baker's Broderick eulogy, Union Square speech and Senate reply to Breckinridge). Pieces with more than a quarter of their words inside quotation marks:
- hay_ellsworth_07: 241 words, ~41% inside quotation marks
- hay_ellsworth_09: 245 words, ~39% inside quotation marks
- hay_ellsworth_15: 159 words, ~37% inside quotation marks
- hay_ellsworth_16: 147 words, ~65% inside quotation marks
- hay_ellsworth_18: 202 words, ~51% inside quotation marks
- hay_ellsworth_19: 208 words, ~38% inside quotation marks
- hay_ellsworth_21: 231 words, ~56% inside quotation marks
- hay_baker_06: 231 words, ~34% inside quotation marks
- hay_baker_09: 231 words, ~40% inside quotation marks
- hay_baker_18: 213 words, ~70% inside quotation marks
- hay_baker_19: 139 words, ~57% inside quotation marks
- hay_baker_20: 234 words, ~44% inside quotation marks
- hay_baker_24: 200 words, ~87% inside quotation marks
- hay_baker_25: 147 words, ~66% inside quotation marks
- hay_baker_27: 247 words, ~85% inside quotation marks
- hay_baker_34: 252 words, ~51% inside quotation marks
(Heuristic: words between paired straight quotation marks, plus the tail after an unpaired opening quote, so a piece with an odd number of quote marks can be over-counted; check the text before excluding a piece.) The attribution of the two essays is not in doubt; only these pieces are register-mixed. No piece has an uncertain attribution.
