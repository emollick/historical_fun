# Bixby study corpus

Built from archive.org OCR and Project Gutenberg texts. Three corpora:

| file | what | items | words |
|---|---|---|---|
| `lincoln_basler.jsonl` (+ `lincoln_basler_index.csv`) | Lincoln's own text from Basler, *Collected Works*, vols. I, IV, VII, VIII | 3,535 | 337,953 |
| `hay.jsonl` (+ `hay_index.csv`) | John Hay: 1908 letters/diary, Thayer-quoted letters, books, addresses, verse | 895 | 501,930 |
| `controls.jsonl` (+ `controls_summary.json`) | 20 control authors, cut into 150-300-word pieces | 5,055 pieces | 1,180,193 |

Other files in this directory:

* `bixby_letter_basler.txt` – the Bixby letter as parsed from Basler VIII:116-117 (OCR uncorrected).
* `bixby_letter_transcript_wikipedia.txt` – the Boston Evening Transcript text taken from the wikitext of the Wikipedia article on the letter (clean questioned-document text).
* `bixby_letter_comparison_note.txt` – token-level comparison of the two (no wording differences; only OCR errors "hare"/"f ound" and frame differences).
* `controls_raw/` – downloaded raw texts for the controls (`ia_<identifier>.txt` = `https://archive.org/download/<id>/<id>_djvu.txt`; `pg<n>.txt` = `https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt`), plus `pg_catalog.csv` and `ia_search_results.json` (archive.org advancedsearch results used to pick identifiers). Some downloaded texts were not used in the end (Seward vol. 5, Sumner memoir vol. 4, Curtis *Orations and Addresses*, Lowell vol. 2, Taylor vol. 2, Motley vol. 2, pg2944/2945/69258/7445/8222).
* `hay_raw/` – Gutenberg texts of Hay's books: pg7470 (Castilian Days), pg16321 (The Bread-Winners), pg6062 (Pike County Ballads), pg10518 (Poems).
* `scripts/parse_basler.py`, `scripts/parse_hay.py`, `scripts/build_controls.py` – the only build scripts; everything above is reproducible from them (see "Rebuild").
* `hay_warprose.jsonl` and `hay_warprose/` – **not produced by the scripts here** (built by `hay_warprose/build.py`; see `hay_warprose/notes.md`). Their own fields say 56 items / 11,009 words of Hay's 1861 prose (Atlantic, "Ellsworth" etc.). Not validated by me; do not confuse with `hay.jsonl`.

Period tags used everywhere: `pre_war` = year < 1861, `civil_war` = 1861-1865, `post_war` = year > 1865, `None` = year unknown.

---

## 1. `lincoln_basler.jsonl` – Lincoln (Basler, Collected Works)

**Sources** (archive.org OCR): `collectedworksof015581mbp` = vol. I (1824-1848), `collectedworksof015582mbp` = vol. IV (1860-1861), `collectedworksof015583mbp` = vol. VII (1863-1864), `collectedworksof015584mbp` = vol. VIII (1864-1865, incl. Appendix I and Additions). **Vols. II, III, V, VI were not available** on archive.org (only these four scans exist there), so 1849-1859 and Nov. 1861-Aug. 1863 are essentially missing (the few 1862/1853-1858 dates in the file are back-references or OCR misreads). The Nicolay & Hay 1905 *Complete Works* vols. 9-11 (`completeworksov9linc`, `completeworksofv10linc`, `completeworksofav11linc`) were downloaded but **not parsed** (time); they can be used as cross-check. Gutenberg Lapsley Lincoln (pg2653-2659) is also available for OCR cross-checks; Basler was not replaced by it.

**Fields**: `id` (basler-VOL-NNNN, in page order), `volume`, `section` (main / appendix_1 / additions), `page`, `line` (OCR line of the heading), `heading`, `heading_marker` (superscript footnote marker seen), `date` (ISO, day precision when the dateline gives it), `year`, `date_source` (dateline / carried [from the previous item] / None), `header` and `trailer` (the dateline / inside-address / signature lines that were stripped, kept for audit), `addressee` (from "To X" headings), `genre` (letter, telegram, endorsement, speech, proclamation, message, memorandum, order, other), `source_code` (Basler manuscript code from the first footnote: ALS, ADfS, ADf, AD, ADS, AES, AE, AL, LS, DS, Df, DfS, ES, Copy …), `source_kind`/`source_type` (manuscript vs printed source, how the footnote was recognised), `autograph` (True iff the code starts with "A" and the note does not say the body is in Hay's hand), `hay_hand` (True iff the source note says the document/body/draft is in John Hay's handwriting or autograph), `other_hand` (note names another hand, e.g. Nicolay, Stoddard, a clerk), `source_note` (raw text of the first footnote, up to 3,000 chars, for auditing the flags), `footnote_head`, `text`, `word_count`, `flags`.

**Parsing rules**: page markers `[N]` end a page; running heads (garbled all-caps dates) and page numbers are dropped; an item starts at a title-cased heading carrying a superscript marker (OCR'd as `1 l i I * ! x ^ ' "`), or at a two-line heading, or (pass 2) at a heading without marker between two footnote blocks (`heading_relaxed`); the item's text runs to the first footnote block (marker + manuscript code such as ALS, or a printed-source citation); if no footnote is found the text is cut at Lincoln's signature (`footnote_by_signature`) or flagged `no_footnote_found`. Standalone dateline and inside-address lines and trailing signature/addressee lines are stripped (kept in `header`/`trailer`); run-in salutations ("Dear Madam,") and closing formulas are kept; the signature token "A. LINCOLN" is removed (fuzzy OCR forms included); editorial brackets are removed (short supplied words kept unbracketed, longer bracketed editorial matter dropped); hyphenated line breaks are rejoined; OCR digit errors are fixed **only** in datelines (i/l/I→1, o/O→0, "186/5"→1865 etc.), never in the wording. Dates: day-precision from the dateline when it is in the volume's year range (I 1824-1848, IV 1860-1861, VII 1863-1864, VIII 1864-1865); out-of-range years are rejected and the previous item's date carried (`year_ocr_rejected`, `date_source=carried`). Genre: endorsement if code AES/AE/ES or heading says Endorsement; "To the Senate/House" → message; "To X" → letter, or telegram when the footnote says telegram/telegraph/cypher; speech/proclamation/memorandum/order/message by heading first word; other otherwise. Quoted third-party letters inside footnotes are excluded because everything after the first footnote marker is excluded.

**Totals**: 3,535 items, 337,953 words. By volume: I 410 items / 94,608 words; IV 1,046 / 98,974; VII 1,185 / 80,728; VIII 894 / 63,643 (main 3,471, appendix_1 54, additions 10). Genre: letter 1,616, endorsement 669, telegram 447, other 230, speech 188, order 168, message 115, memorandum 73, proclamation 29. Autograph: 2,233 True / 1,302 False. Source codes: ALS 1,213, none 835, AES 554, AD 186, Copy 182, DS 166, ADS 111, LS 65, AL 47, ADf 44, ADfS 43, AE 42, ES 29, Df 13, other 5. `hay_hand` 38 (none of them autograph=True), `other_hand` 173. Dates: dateline 2,926, carried 564, none 45; years: 1830-1850 ~ 410, 1860: 255, 1861: 795, 1863: 181, 1864: 1,371, 1865: 465 (vol. VIII now runs Sept. 1864-Apr. 1865 only). Flags: multiple_strict_footnotes 65, heading_relaxed 62, no_footnote_found 36, footnote_by_signature 22, date_out_of_sequence 1; one zero-length item (garbage OCR page).

**Validation set** (autograph=True, 1861-1865, 100-300 words): **175 items** (letter 110, telegram 29, other 12, memorandum 11, message 4, endorsement 4, order 3, speech 2).

**Known problems**: OCR noise is left as is (e.g. "hare" for "have" in the Bixby letter itself); 835 items have no source code (headings whose footnote marker/code was unreadable, items drawn from printed sources, and items cut by signature); the 1908-style page-boundary transmittal notes occasionally leak (e.g. basler-VII-0470 keeps Nicolay's "Major Eckert: Please send the above dispatch"); running heads with spaced digits ("FEBRUARY 1 8, l86l") leak into a few items; garbled signatures ("A. LiisrcoLisr") are not always stripped; `date_out_of_sequence`/`carried` dates are approximate; the vol. VIII "186/5" misreads were fixed but a few carried dates remain; the superscript markers make `heading` text end with stray characters in some items. The spot check (below) found 4/10 items with minor leakage of this kind and 0/10 with wrong item boundaries.

## 2. `hay.jsonl` – John Hay

**Sources**: `lettersofjohnhay01hayj`, `02hayj`, `03hayj` (Letters of John Hay and Extracts from Diary, 1908, privately printed, 3 vols.; letters and diary), `lifelettersofjoh01thay`, `02thay` (Thayer, Life and Letters, 1915; only letters quoted under "To Name" headers), `poetinexileearly00hayj` (A Poet in Exile: early letters, 1938 – 4 letters, italic OCR noisy), `addressesofjohnh00hayj` (Addresses, 1906; 23 of 24 addresses; the McKinley memorial address chapter is flagged as a duplicate of the pamphlet), `williammckinleym02hayj` (William McKinley memorial address, 1902), `washingtonafterw00hayj` (Washington after the War, diary notes ed. Thayer – only 3 entries could be delimited), Gutenberg pg7470 Castilian Days (11 essays), pg16321 The Bread-Winners (20 chapters, `fiction: true`), pg6062 Pike County Ballads (100 poems, `kind: verse`), pg10518 Poems (28 poems, verse).

**Fields**: `id` (hay-NNNN), `source` (letters_1908, thayer, poet_in_exile, addresses, mckinley, washington_after_war, castilian_days, bread_winners, pike_county_ballads, poems), `volume`, `line` (OCR line), `kind` (letter, diary, essay, speech, fiction, verse), `heading`, `recipient` (from the 1908 caps headings "HAY TO NICOLAY."; "C S H" resolved to Clara Stone Hay (wife)), `year`, `month`, `day`, `date` (ISO where known), `date_source` (entry date / carried / heading), `header` (the dateline/heading lines removed), `text`, `word_count`, `elisions` (count of dashed-out names replaced by the placeholder "N"), `ellipses` (count of editorial "...." removed), `flags`, `period`, `fiction`.

**Parsing rules**: 1908 volumes: an item starts at a caps heading ("HAY TO NICOLAY.", "DIARY." section entries starting "Aug. 22, 1861." / "Jan. 18."); running heads ("LETTERS OF JOHN HAY 237") and page numbers dropped; editor's footnotes (digit-led lines) dropped; the year is carried forward inside a volume (vol. 1 1860-1870, vol. 2 1870-1895, vol. 3 1896-1905) and datelines update month/day; dashed-out names ("S- 's", "Major H ,", OCR'd as a capital + spaces) are replaced by "N"; embedded Lincoln documents (Executive Mansion … A. LINCOLN.) are removed (`embedded_lincoln_removed`); salutations run into the text are kept, signatures dropped. Thayer: a letter starts at a "To Name" header followed by a dateline and stops at the next heading, chapter, third-person mention of Hay, signature, or after 12 paragraphs (`delimitation_heuristic`, `stop_*` flags) – **Thayer's own prose is never included on purpose, but the stop rule is heuristic**. Addresses: split on the printed title list (two-line titles joined); years from the address datelines (1890-1906 window). Gutenberg books: split at essay/chapter/poem titles, Gutenberg header/licence removed.

**Totals**: 895 items, 501,930 words. letters_1908: letters 472 (civil_war 34 / 13,689 w; post_war 431 / 143,134 w; pre_war 6 / 659 w; undated 1), diary 138 (civil_war 111 / 39,551 w; post_war 27 / 8,988 w); thayer letters 95 / 35,119 w (all post_war – Thayer's civil-war letters are quoted without "To X" headers and were **not** extracted); poet_in_exile 4 / 4,862 (pre_war); addresses 23 / 56,092 (3 undated); mckinley 1 / 8,094; washington_after_war 3 / 1,451; castilian_days 11 / 66,729; bread_winners 20 / 84,132 (fiction); pike_county_ballads 100 / 21,788 and poems 28 / 17,499 (verse – keep out of prose comparisons).

**Validation set** (1908 letters/diary entries dated 1861-1866, 100-300 words): **55 items** (15 letters, 40 diary entries).

**Known problems**: the 1908 edition dashes out many names (338 elisions replaced by "N"; more are missed because whitespace is collapsed before the elision rule runs, so "N" counts are an undercount) and uses editorial "…." cuts (398 removed); OCR page numbers like "g2" occasionally leak a running head ("g2 LETTERS OF JOHN HAY"); Poet in Exile is italic OCR and noisy (`ocr_italic_noisy`); Washington after the War could not be segmented into entries reliably (only 3 entries; the rest dropped); Thayer letters are heuristic (98 flagged `delimitation_heuristic`) and cover 1866-1905 only; addresses years for 3 items unknown; the 1908 diary entries in vol. 1 that lack a year were dated by carry-forward from the preceding entry. Spot check: 10/10 boundaries correct, minor leakage in 2 items.

## 3. `controls.jsonl` – control authors

One line per piece: `id` (ctrl-<surname>-NNNN), `author`, `source` (`ia:<archive.org identifier>` or `pg:<Gutenberg number>`), `title`, `url`, `kind` (letter, diary, speech, memoir, essay, history), `year`, `year_source` (dateline = carried forward from the last dateline/heading naming a year; nominal = year of the book; None = unknown), `period`, `word_count`, `text` (paragraphs separated by newlines).

**Rules**: only the named author's prose is kept – front matter, contents, editors' introductions and narrative, indexes, appendices, footnotes (digit-led blocks), running heads and page numbers are removed by the mode-specific rules in `scripts/build_controls.py` (`pg_whole`, `pg_flush`, `pg_twain`, `ocr_whole`, `ocr_letters` – documented in the script header); chapter synopses ("A -- B -- C"), bracketed editorial notes, paragraphs naming "Mr. Sumner" in the third person, verse blocks and garbled OCR paragraphs are dropped. Pieces: paragraphs (or diary entries / letter paragraphs) are accumulated until 100-300 words, closing at a paragraph boundary and at a change of year; paragraphs longer than 300 words are split at sentence ends; tail pieces under 60 words dropped. Per author at most 60,000 words, **sampled evenly across the whole source** (every k-th piece), so memoirs are not only childhood chapters; Chase and Sumner take 30,000 words from each of two sources. Piece sizes: min 82, median 243, max 376 words (339 pieces < 150 words, 97 > 300).

| author | kind | source (archive id / PG #) | years of pieces | pieces | words | pre_war / civil_war / post_war pieces |
|---|---|---|---|---|---|---|
| William H. Seward | speech | ia:sewardwilliam04sewarich (Works vol. 4, 1884: orations, speeches 1853-1861) | 1853-1860 | 266 | 59,944 | 255 / 0 / 0 (11 unknown) |
| Salmon P. Chase | diary, letter | ia:diaryandcorrespo00chasrich (AHA 1903: diary 1862, letters 1846-1863) | 1846-1863 | 213 | 51,331 | 72 / 141 / 0 |
| Gideon Welles | diary | ia:diaryofgideonwelv1well (Diary vol. 1, 1911) | 1861-1864 | 254 | 59,935 | 0 / 254 / 0 |
| Charles Sumner | speech | pg:48077 + pg:48170 (Complete Works vols. 7-8, 1900) | 1860-1862 | 257 | 59,919 | 72 / 185 / 0 |
| William O. Stoddard | memoir | ia:insidewhitehouse00stod (1890) | 1890 (nominal) | 227 | 59,927 | 0 / 0 / 227 |
| Noah Brooks | memoir | ia:washingtoninlinc00broo (1895) | 1895 (nominal) | 227 | 60,038 | 0 / 0 / 227 |
| John G. Nicolay | history | ia:outbreakofrebell00nico (1881) | 1881 (nominal) | 222 | 52,015 | 0 / 0 / 222 |
| Edward Everett | speech | ia:orationsspeeches04ever (Orations vol. 4, 1868) | 1856-1864 | 259 | 59,898 | 140 / 119 / 0 |
| Walt Whitman | diary (Specimen Days notes) | pg:8813 (Complete Prose Works) | 1860-1882 | 268 | 59,969 | 3 / 142 / 122 (1 unknown) |
| Ulysses S. Grant | memoir | pg:4367 (Personal Memoirs, 1885) | 1885 (nominal) | 276 | 59,436 | 0 / 0 / 276 |
| William T. Sherman | memoir | pg:4361 (Memoirs, 1875) | 1875 (nominal) | 252 | 60,077 | 0 / 0 / 252 |
| James Russell Lowell | letter | ia:lettersofjamesru01lowe_0 (Letters vol. 1, 1894) | 1840-1868 | 243 | 60,034 | 171 / 33 / 39 |
| Ralph Waldo Emerson | essay | pg:39827 (The Conduct of Life, 1860) | 1860 (nominal) | 268 | 60,009 | 268 / 0 / 0 |
| Frederick Douglass | memoir | pg:71893 (Life and Times, 1881/1892) | 1881 (nominal) | 258 | 60,038 | 0 / 0 / 258 |
| Horace Greeley | memoir | ia:recollectionsofb00greeuoft (1868) | 1868 (nominal) | 265 | 59,913 | 0 / 0 / 265 |
| George William Curtis | essay | pg:8108 (Literary and Social Essays; years from the contents table) | 1853-1891 | 262 | 58,573 | 130 / 30 / 102 |
| Bayard Taylor | letter | ia:lifelettersofbay00tayl (Life and Letters vol. 1, 1884) | 1840-1863 | 258 | 59,918 | 225 / 33 / 0 |
| John Lothrop Motley | letter | ia:correspondenceof01motluoft (Correspondence vol. 1, 1889) | 1832-1861 | 257 | 59,890 | 233 / 20 / 0 (4 unknown) |
| Mark Twain | letter | pg:3193 + 3194 + 3195 (Letters ed. Paine, 1917) | 1853-1885 | 247 | 59,444 | 16 / 32 / 199 |
| Henry Adams | memoir | pg:2044 (The Education, written 1905-07) | 1907 (nominal) | 276 | 59,885 | 0 / 0 / 276 |

Totals: 20 authors, 5,055 pieces, 1,180,193 words; by period: pre_war 1,585 pieces / 365,743 words, civil_war 989 / 231,067, post_war 2,465 / 579,364, unknown 16 / 4,019. Per-source notes (how cleanly each author was isolated) are in `controls_summary.json` (`sources[].note`) and in the `CONFIG` list of the script.

**Known problems**: OCR noise in the archive.org texts (Greeley's drop-caps, "1 " for "I ", cut margins on a few Motley pages); memoir text of Grant/Sherman embeds quoted orders and letters by others that cannot be separated; Seward's and Everett's headnotes by the editors are short and cannot be told from OCR, so some sentences of G. E. Baker / the Everett editor may leak; Lowell/Motley/Taylor letters are quoted inside editorial biographies – connecting sentences by the editors sometimes remain at letter ends and a few letter pieces start with the dateline run into the text; Chase's letters occasionally keep the closing formula; the Chase diary and Welles diary were revised by their authors/editors before printing (Welles in the 1870s); Sumner's years come from the speech headings, Seward's from the footnoted dates (so a piece can inherit the year of the previous item when the footnote was unreadable); Whitman's nature notes (1876-1881) and Adams (1905-07) fall outside 1850-1890; memoir years are nominal (publication) years, not the years described. Random check of 14 pieces: all were the named author's prose; 2 had minor frame leakage (a closing formula; a dateline), 1 had OCR noise.

## 4. Bixby letter

`bixby_letter_basler.txt` is the parsed text from Basler VIII:116-117 (item in `lincoln_basler.jsonl` with heading "To Mrs. Lydia Bixby"; Basler prints the Boston Transcript text, footnote: no manuscript exists). Compared with the Transcript text (`bixby_letter_transcript_wikipedia.txt`): no wording differences; the OCR has "hare" for "have" and "f ound" for "found"; frame (dateline, signature, addressee line) differs because the corpus strips those. See `bixby_letter_comparison_note.txt`.

## 5. Spot checks

Lincoln, 10 random items against the raw OCR: 0 wrong boundaries, 0 footnote text leaked into `text`; 4 items with minor leakage (a Nicolay transmittal note after a page break; a running head with spaced digits; two garbled signature lines "A. LiisrcoLisr" + "The Honourable Attorney General" not stripped). Hay, 10 random 1908 items: 10/10 boundaries correct; minor: one running head "g2 LETTERS OF JOHN HAY" leaked, one heading fragment kept ("Hay, Reformed Tribune Man."), elision placeholders under-applied. Controls: 14 random pieces, see above. Estimated error rate for the analysis: ~0 wrong attributions (text by someone else) in the Lincoln/Hay items checked, ~20-40 % of items carry a few words of frame/running-head noise.

## 6. Rebuild

```
cd corpus
python3 scripts/parse_basler.py      # reads ia/txt/collectedworksof01558[1-4]mbp.txt -> lincoln_basler.jsonl, lincoln_basler_index.csv, bixby_letter_basler.txt
python3 scripts/parse_hay.py         # reads ia/txt/{lettersofjohnhay0[123]hayj,lifelettersofjoh0[12]thay,poetinexileearly00hayj,addressesofjohnh00hayj,williammckinleym02hayj,washingtonafterw00hayj}.txt and hay_raw/pg*.txt -> hay.jsonl, hay_index.csv
python3 scripts/build_controls.py    # reads controls_raw/ -> controls.jsonl, controls_summary.json   (add --probe to print samples without writing)
```
The raw downloads were fetched with `curl` from `https://archive.org/download/<id>/<id>_djvu.txt` and `https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt` (see `controls_raw/`, `hay_raw/`; working copies of the Basler and Hay OCR downloads are not included in this folder: the two parse scripts read them from `ia/txt/` under the corpus folder, or from `$S/ia/txt/` when the environment variable `S` is set). Scripts have no dependencies beyond the Python 3.11 standard library.

## 7. Dropped / not done

* Basler vols. II, III, V, VI (not on archive.org here) – so no Lincoln text for 1849-1859 and Nov. 1861-Aug. 1863.
* Nicolay & Hay 1905 vols. 9-11: downloaded, not parsed.
* Hay: Thayer's civil-war letters (quoted without headers), most of Washington after the War, and the archive.org OCR of the books (replaced by Gutenberg) were dropped.
* Controls: Sumner's memoir/letters (Pierce, vol. 4) and Seward vol. 5, Curtis Orations, second volumes of Lowell/Taylor/Motley were downloaded but not needed once the 60k cap was reached from the first volumes.
