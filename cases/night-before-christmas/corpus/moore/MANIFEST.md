# Clement Clarke Moore verse corpus — MANIFEST

Machine-readable corpus of Moore's verse for the stylometric study of "A Visit from St. Nicholas". Built from the 1844 *Poems* (New York: Bartlett & Welford), proofread page by page against the archive.org scan, plus the earlier witnesses of three poems in Hoffman's *New-York Book of Poetry* (1837) and the four texts of the *Visit* in `../visit/`.

## Layout and conventions

* `NN_slug.txt` — one file per poem, NN = order in the 1844 book (the four items in the book that are not by Moore keep their NN but live in `not_moore/`, so the numbering has gaps at 14, 20, 22, 36).
* `not_moore/` — pieces printed in *Poems* (1844) but written by others (William Bard, Philip Hone, Moore's late wife); header `attribution: not Moore (<author>)`. Excluded from all Moore totals.
* `hoffman_1837/` — the three Moore poems that Hoffman printed in 1837 besides the *Visit*; earlier witnesses of poems 02, 17 and 19. Duplicates of 1844 texts: use for variant study only, never add them to the totals.
* `preface_1844.txt` — Moore's prose preface (dedication 'My dear children') and the title-page epigraph.
* `../visit/` — the *Visit* in its 1823, 1837 and 1844 forms (plus the 1830 broadside as an extra witness) and `visit_collation.md`.
* Every file starts with an eight-field header (`title, author, date, source, form, lines, attribution, notes`), then a blank line, then the text: one verse line per line, a blank line between stanzas or verse paragraphs as printed (see 'Stanza and paragraph breaks at page ends' in section F), no line numbers, running heads, catchwords or footnotes (footnote text is quoted in `notes`). The section headings of *A Trip to Saratoga* (`PART SECOND.` … `PART SIX.`, spelled as the book spells them; `PART FIRST.` belongs to the poem's heading) are kept as lines but are **not** counted in `lines` or in the word counts.
* Spelling and punctuation follow the 1844 print, including its elisions ('twas, e'er, look'd) and its printer's errors (listed below). Modernized only in representation: straight ASCII quotation marks and apostrophes; em dash U+2014 set closed (no spaces); end-of-line hyphenation rejoined; italics, small capitals, indentation and ornaments are not represented (they are noted in `notes` when they matter, e.g. small-capital 'St. Nicholas').
* `lines` = number of non-blank verse lines; word counts = whitespace-separated tokens of those lines (hyphenated compounds count as one word, 'St.' as one word).

## A. Moore's poems in *Poems* (1844)

| NN | file | title | form | lines | words | pp. 1844 | tone |
|---|---|---|---|---|---|---|---|
| 01 | `01_a_trip_to_saratoga.txt` | A Trip to Saratoga | iambic pentameter quatrains (abab) | 864 | 6804 | 15-64 | Comic-serious narrative (six parts) |
| 02 | `02_to_my_children_with_my_portrait.txt` | To My Children, after Having My Portrait Taken for Them | iambic pentameter quatrains (abab) | 48 | 361 | 65-68 | Serious |
| 03 | `03_to_the_fashionable_part_of_my_young_countrywomen.txt` | Lines Addressed, Many Years Ago, to the Fashionable Part of My Young Countrywomen | iambic pentameter couplets | 76 | 578 | 69-73 | Satirical-moral |
| 04 | `04_the_mischievous_muse.txt` | The Mischievous Muse | iambic tetrameter/trimeter quatrains (ballad measure, abcb) | 84 | 460 | 74-79 | Light |
| 05 | `05_lines_written_after_a_snow_storm.txt` | Lines Written after a Snow-Storm | iambic tetrameter/trimeter quatrains (common measure, abab) | 32 | 186 | 80-82 | Serious-tender |
| 06 | `06_to_young_ladies_who_attended_philosophical_lectures.txt` | Lines Addressed to the Young Ladies Who Attended Mr. Chilton's Lectures in Natural Philosophy, Anno 1804-5 | iambic pentameter couplets | 75 | 590 | 83-87 | Satirical-moral |
| 07 | `07_on_seeing_my_name_written_in_the_sand.txt` | Lines on Seeing My Name Written by a Young Lady in the Sand of the Sea-Shore | iambic tetrameter/trimeter quatrains (common measure, abab) | 8 | 43 | 88-88 | Light |
| 08 | `08_on_cowper_the_poet.txt` | Lines on Cowper the Poet, Written after Reading the Life of Him by Hayley | iambic pentameter couplets | 36 | 271 | 89-91 | Serious |
| 09 | `09_to_petrosa.txt` | To Petrosa | iambic tetrameter quatrains (abab) | 32 | 200 | 92-94 | Comic |
| 10 | `10_translation_of_an_ode_of_metastasio.txt` | Translation of Metastasio's Ode to Nice | iambic tetrameter/trimeter 8-line stanzas (abbcaddc) | 104 | 626 | 95-100 |  |
| 11 | `11_a_song.txt` | A Song, Written to Italian Music | mixed (song; mainly iambic trimeter with tetrameter lines) | 23 | 119 | 101-102 |  |
| 12 | `12_old_dobbin.txt` | Old Dobbin | iambic tetrameter triplets with refrain ('Old Dobbin.') | 28 | 152 | 103-104 | Comic |
| 13 | `13_apology_for_not_accepting_an_invitation_to_a_ball.txt` | Lines Addressed to a Lady, as an Apology for Not Accepting Her Invitation to a Ball | iambic pentameter couplets | 70 | 545 | 105-108 | Light |
| 15 | `15_translation_of_a_chorus_in_aeschylus.txt` | Translation of One of the Choruses in the Prometheus of Aeschylus | iambic tetrameter couplets | 34 | 216 | 111-113 |  |
| 16 | `16_lines_accompanying_some_balls_sent_to_a_fragment_fair.txt` | Lines Accompanying Some Balls Made for a Fragment Fair, at the Request of a Young Lady | iambic tetrameter/trimeter sestets (aabccb) | 54 | 334 | 114-117 | Light-moral |
| 17 | `17_to_a_lady.txt` | To a Lady | iambic tetrameter/trimeter sestets (aabccb) | 90 | 541 | 118-123 | Serious |
| 18 | `18_a_visit_from_st_nicholas.txt` | A Visit from St. Nicholas | anapestic tetrameter couplets | 56 | 540 | 124-127 | Light |
| 19 | `19_from_a_husband_to_his_wife.txt` | From a Husband to His Wife | iambic tetrameter quatrains (abab) | 72 | 460 | 128-132 | Serious |
| 21 | `21_lines_accompanying_a_bunch_of_flowers.txt` | Lines Sent with a Bunch of Flowers to a Friend—March, 1842 | iambic tetrameter quatrains (abab) | 24 | 150 | 135-136 | Light |
| 23 | `23_lines_written_after_a_season_of_yellow_fever.txt` | Lines Addressed to the Fashionable People of New York, upon Their Return to the City, after the Disappearance of the Yellow Fever in the Autumn of —— | iambic pentameter couplets | 152 | 1143 | 139-147 |  |
| 24 | `24_to_the_nymphs_of_mount_harmony.txt` | To the Nymphs of Mount Harmony | iambic tetrameter couplets | 96 | 588 | 148-153 | Light-serious |
| 25 | `25_to_a_young_lady_on_her_birth_day.txt` | To a Young Lady, on Her Birth-day | iambic tetrameter/trimeter quatrains (common measure, abcb) | 32 | 176 | 154-156 | Serious |
| 26 | `26_on_receiving_a_caricature_cast_of_paganini.txt` | Lines on Receiving from a Friend a Caricature Cast of Paganini | iambic pentameter couplets | 28 | 212 | 157-158 | Light |
| 27 | `27_the_organist.txt` | The Organist | iambic pentameter/tetrameter alternating quatrains (abab) | 84 | 584 | 159-164 | Light-serious |
| 28 | `28_the_pig_and_the_rooster.txt` | The Pig and the Rooster | anapestic tetrameter couplets | 86 | 781 | 165-169 | Comic |
| 29 | `29_lines_for_valentines_day.txt` | Lines for Valentine's Day, to a Lady Remarkable for Her Vocal Powers | iambic tetrameter/trimeter quatrains (common measure, abab) | 52 | 285 | 170-173 | Light |
| 30 | `30_the_wine_drinker.txt` | The Wine Drinker | iambic tetrameter couplets | 172 | 1069 | 174-182 | Comic-serious |
| 31 | `31_the_water_drinker.txt` | The Water Drinker | iambic tetrameter couplets (with a few longer and shorter lines) | 181 | 1130 | 183-192 |  |
| 32 | `32_lines_sent_to_a_young_lady_with_a_pair_of_gloves.txt` | Lines Sent to a Young Lady, with a Pair of Gloves | iambic tetrameter/trimeter sestets (aabccb) | 24 | 140 | 193-194 | Light |
| 33 | `33_farewell.txt` | Farewell | iambic pentameter couplets | 42 | 320 | 195-197 | Light-serious |
| 34 | `34_lines_on_the_sisters_of_charity.txt` | Lines on the Sisters of Charity | iambic pentameter quatrains (abab) | 80 | 615 | 198-203 | Serious |
| 35 | `35_to_my_daughter_on_her_marriage.txt` | To My Daughter, on Her Marriage—1836 | iambic pentameter quatrains (abab) | 72 | 572 | 204-208 | Serious |
| 37 | `37_to_southey.txt` | To Southey | iambic pentameter couplets | 96 | 743 | 212-216 | Serious |
| | **total (33 poems)** | | | **3007** | **21534** | | |

## B. Metrical breakdown (Moore poems only, by the `form` label; scansion by judgment of the dominant line)

| form | poems (NN) | lines | share |
|---|---|---|---|
| iambic pentameter quatrains (abab) | 01, 02, 34, 35 | 1064 | 35.4% |
| iambic pentameter couplets | 03, 06, 08, 13, 23, 26, 33, 37 | 575 | 19.1% |
| iambic tetrameter couplets | 15, 24, 30 | 302 | 10.0% |
| iambic tetrameter couplets (with a few longer and shorter lines) | 31 | 181 | 6.0% |
| iambic tetrameter/trimeter sestets (aabccb) | 16, 17, 32 | 168 | 5.6% |
| anapestic tetrameter couplets | 18, 28 | 142 | 4.7% |
| iambic tetrameter quatrains (abab) | 09, 19, 21 | 128 | 4.3% |
| iambic tetrameter/trimeter 8-line stanzas (abbcaddc) | 10 | 104 | 3.5% |
| iambic tetrameter/trimeter quatrains (common measure, abab) | 05, 07, 29 | 92 | 3.1% |
| iambic tetrameter/trimeter quatrains (ballad measure, abcb) | 04 | 84 | 2.8% |
| iambic pentameter/tetrameter alternating quatrains (abab) | 27 | 84 | 2.8% |
| iambic tetrameter/trimeter quatrains (common measure, abcb) | 25 | 32 | 1.1% |
| iambic tetrameter triplets with refrain ('Old Dobbin.') | 12 | 28 | 0.9% |
| mixed (song; mainly iambic trimeter with tetrameter lines) | 11 | 23 | 0.8% |

**Anapestic tetrameter couplets: 142 lines (4.7%)** — only two poems: *A Visit from St. Nicholas* (18, 56 lines) and *The Pig and the Rooster* (28, 86 lines). **Iambic: 2842 lines (94.5%)**; mixed/song: 23 lines. Pentameter (couplets or quatrains) accounts for 1723 lines, tetrameter-based forms for 1284 lines.

## C. Items in the 1844 book not by Moore (`not_moore/`, excluded from totals)

| NN | file | title | author (per the book/preface) | form | lines | words | pp. |
|---|---|---|---|---|---|---|---|
| 14 | `not_moore/14_answer_to_the_preceding_by_mr_bard.txt` | Answer to the Preceding, by Mr. Wm. Bard | William Bard | iambic tetrameter/trimeter sestets (aabccb) | 24 | 143 | 109-110 |
| 20 | `not_moore/20_lines_by_my_late_wife_in_an_album.txt` | Lines by My Late Wife, on Being Requested to Write in an Album | Catharine Elizabeth Taylor Moore (Moore's wife, d. 1830) | iambic tetrameter/trimeter quatrains (common measure, abcb) | 20 | 113 | 133-134 |
| 22 | `not_moore/22_answer_to_the_preceding_by_mr_hone.txt` | Answer to the Preceding, by Mr. P. Hone | Philip Hone | iambic tetrameter quatrains with closing pentameter couplet | 14 | 88 | 137-138 |
| 36 | `not_moore/36_lines_to_the_memory_of_miss_susan_moore.txt` | Lines to the Memory of Miss Susan Moore, Written by My Late Wife | Catharine Elizabeth Taylor Moore (Moore's wife, d. 1830) | mixed (pentameter couplets with tetrameter quatrains) | 30 | 208 | 209-211 |
| | **total** | | | | **88** | **552** | |

## D. Earlier witnesses in Hoffman, *The New-York Book of Poetry* (1837) (`hoffman_1837/`, duplicates — not added to totals)

| file | title (1837) | 1844 counterpart | form | lines | words | pp. 1837 |
|---|---|---|---|---|---|---|
| `hoffman_1837/1837_p211_to_a_lady.txt` | To a Lady | `17_to_a_lady.txt` | iambic tetrameter/trimeter sestets (aabccb) | 78 | 469 | 211-213 |
| `hoffman_1837/1837_p215_from_a_father_to_his_children.txt` | From a Father to His Children, after Having Had His Portrait Taken for Them | `02_to_my_children_with_my_portrait.txt` | iambic pentameter quatrains (abab) | 48 | 361 | 215-216 |
| `hoffman_1837/1837_p221_from_a_husband_to_his_wife.txt` | From a Husband to His Wife | `19_from_a_husband_to_his_wife.txt` | iambic tetrameter quatrains (abab) | 72 | 460 | 221-224 |
| | **total** | | | **198** | **1290** | |

The 1837 *To a Lady* (78 lines, dated 1804) lacks two stanzas that 1844 adds; the other two are the same length as in 1844 with only spelling/punctuation differences (details in each file's `notes`). Hoffman's *Visit* (pp. 217-219) is in `../visit/visit_1837_hoffman.txt`.

## E. Preface and the *Visit* files

| file | content | lines | words |
|---|---|---|---|
| `preface_1844.txt` | Moore's prose preface, March 1844, plus title-page epigraph (prose; 7 paragraphs) | n/a | 663 |
| `../visit/visit_1823_troy_sentinel.txt` | Account of a Visit from St. Nicholas — 23 December 1823 (first printing, anonymous) | 56 | 540 |
| `../visit/visit_1830_broadside.txt` | Account of a Visit from St. Nicholas, or Santa Claus — c. 1830 (undated broadside reprint of the Troy Sentinel text; extra witness, not one of the three required) | 56 | 537 |
| `../visit/visit_1837_hoffman.txt` | A Visit from St. Nicholas — 1837 (first attributed printing) | 56 | 539 |
| `../visit/visit_1844_poems.txt` | A Visit from St. Nicholas — 1844 (first printing under Moore's own name, in his Poems) | 56 | 540 |
| `../visit/visit_collation.md` | line-by-line collation 1823/1837/1844 with 1830, 1840 and holograph appendices | | |

**Corpus totals for the authorship test: Moore, 33 poems, 3007 lines, 21534 words** (the 1844 *Visit* is included in these totals as poem 18; subtract 56 lines / 540 words for a Moore corpus without the disputed poem: 2951 lines, 20994 words).

## F. OCR quality and known problems

* **Base text.** archive.org OCR (`_djvu.txt` / `_djvu.xml`) of the primary scan `poemsmoor00moorrich` (244 leaves; text pages pp. 15-216 = leaves n25-n236). The second scan `poems00moor` (Library of Congress copy) was OCR-aligned to it and used only as a tiebreaker; its OCR is noisier.
* **Proofreading.** Every one of the 202 text pages (and the title page and preface) was compared with the page image (1000-px JPEG, cropped to the text block); 167 corrections were logged and applied by script (the log is not included in this folder). Typical fixes: `tbe`→`the`, `aud`→`and`, `1`/`l`, `I`/`!`, dropped or doubled apostrophes and quotation marks, misread punctuation (`•`→`;`, `,`↔`.`), dropped small-capital first words, rejoined end-of-line hyphenation, stray running heads, catchwords and 'THE END.'.
* **Residual risk.** Punctuation in faint or broken type (comma vs. period, semicolon vs. colon) is the least certain class; two letters are physically damaged in the scan and were read from context: 'control' (p. 121, poem 17) and 'weight' (p. 141, poem 23).
* **Printer's errors kept as printed** (searchable, so they can be normalized if wanted): 'unsconcious', 'misfortue', 'autumal', 'the the', "the' azure", 'faries', 'balmly', 'sprighliest', 'bowlfull', 'extacy', 'wo', 'chrystal'; also the book's own inconsistencies of spelling (honor/honour, portray, moulder'd).
* **Quotation marks as printed.** In *A Trip to Saratoga* (01) quotation marks are re-opened at paragraph starts and not always closed (unbalanced at lines 308, 319, 424, 513-514, 985 of the file); in poem 06 the final quotation is never closed. Left as in the book. The 1837 *To a Lady* has an opening quotation mark at the start of every line of its last three stanzas (restored from the scan; Gutenberg had normalized them).
* **Stanza and paragraph breaks at page ends.** The page-level stanza detection had produced a blank line at every one of the 159 page boundaries inside poems. Each was checked: in the regular stanzaic poems (quatrains, sestets, 8-line stanzas) a page-end break is kept only where it falls on the stanza grid — the compositor splits stanzas across pages without any gap (e.g. pp. 119, 201-202); in the continuous poems (couplets, and the verse paragraphs of *A Trip to Saratoga*) a page-end break is kept only where the page's last line ends a sentence and, in addition, a section heading follows, or the page was set short (the compositor's practice at paragraph ends in *Saratoga*), or the sense clearly turns; a full page whose sentence simply runs on is joined. Result: 101 spurious blanks removed, 58 breaks kept (25 by stanza grid, 4 before section headings, 29 by judgment: poem 01 pp. 15, 19, 23, 24, 25, 26, 27, 29, 33, 34, 38, 43, 44, 45, 46, 48, 51, 57, 58, 59; poem 06 pp. 84; poem 08 pp. 90; poem 15 pp. 112; poem 22 pp. 137; poem 23 pp. 146; poem 28 pp. 167; poem 36 pp. 209, 210; poem 37 pp. 214). Because this book marks paragraphs by extra leading only, a paragraph break that coincides with a full page end leaves no physical trace, so paragraph breaks in the continuous poems may be slightly under-represented. Line and word counts are unaffected. *A Trip to Saratoga* is in abab quatrains printed as verse paragraphs (4-52 lines), with occasional six-line ababab stanzas (e.g. ll. 173-178, 459-464).
* **Not represented:** italics, small capitals, indentation patterns, section rules, page breaks and running heads; engraved plates (unnumbered leaves before pp. 15, 49, 51, 89, 125, 213) carry no text.
* **Footnotes** occur in poems 01, 03, 04, 15 and 31; their text is quoted in the `notes` field and the footnote markers are removed from the verse.
* **Table-of-contents errors in the book:** the 1844 contents page gives *Old Dobbin* as p. 104; it begins on p. 103 (*A Song* is pp. 101-102). Page ranges in the headers are from the pages themselves.
* **Hoffman 1837 texts** are from the Distributed Proofreaders transcription (Project Gutenberg #42769) checked against the archive.org scan `newyorkbkpoet00fennrich`; Gutenberg's `--` is rendered as an em dash and its `_italics_` markers removed.
* **Visit texts:** 1823 from the validated Wikisource transcription proofread against the Commons scan of the newspaper (turnover lines rejoined); 1837 from Gutenberg checked against the scan; 1844 from the 1844 scan; 1830 broadside from the validated Wikisource transcription (spot-checked against the Commons image). See `../visit/visit_collation.md`.

## G. Provenance (all sources used)

* Primary scan of *Poems* (1844): https://archive.org/details/poemsmoor00moorrich — OCR text https://archive.org/download/poemsmoor00moorrich/poemsmoor00moorrich_djvu.txt, word-coordinate XML `..._djvu.xml`, `..._page_numbers.json`, page images `https://archive.org/download/poemsmoor00moorrich/page/n{N}_w1000.jpg` (N = leaf − 1).
* Second scan of *Poems* (1844): https://archive.org/details/poems00moor (used only to adjudicate doubtful OCR readings).
* Wikisource, *Poems* (1844): https://en.wikisource.org/wiki/Index:Poems_(Clement_C._Moore).djvu — pagelist (position of the plates) and the proofread preface pages; not used as the text base for the poems (at the time of use only 31 of its 244 pages were proofread or validated, 25 were raw OCR and the rest not created).
* Hoffman, *The New-York Book of Poetry* (1837): scan https://archive.org/details/newyorkbkpoet00fennrich (page images `page/n{N}_w1000.jpg`); transcription Project Gutenberg #42769, https://www.gutenberg.org/ebooks/42769 (mirror https://archive.org/details/thenewyorkbookof42769gut).
* *Troy Sentinel*, 23 Dec. 1823: Wikisource https://en.wikisource.org/wiki/Page:A_Visit_From_St_Nicholas_-_Troy_Sentinel.png and https://en.wikisource.org/wiki/Troy_Sentinel/1823/12/23/Account_of_a_Visit_from_St._Nicholas; scan https://commons.wikimedia.org/wiki/File:A_Visit_From_St_Nicholas_-_Troy_Sentinel.png.
* 1830 broadside: Wikisource https://en.wikisource.org/wiki/Page:Visit_From_St_Nicholas_-_Broadside.jpg; image https://commons.wikimedia.org/wiki/File:Visit_From_St_Nicholas_-_Broadside.jpg.
* Bryant, *Selections from the American Poets* (New York: Harper, 1840), pp. 285-286: Wikisource https://en.wikisource.org/wiki/Selections_from_the_American_Poets/A_Visit_from_St._Nicholas, transcluding the proofread pages https://en.wikisource.org/wiki/Page:Selections_from_the_American_poets_(IA_selectamerpoet00bryarich).pdf/289 and /290 (scan https://archive.org/details/selectamerpoet00bryarich).
* NYHS holograph (first page): https://commons.wikimedia.org/wiki/File:A_Visit_From_St._Nicholas,_by_Clement_C_Moore.jpg.
* Background only: https://en.wikipedia.org/wiki/A_Visit_from_St._Nicholas, https://en.wikisource.org/wiki/A_Visit_from_St._Nicholas, https://en.wikisource.org/wiki/Author:Clement_Clarke_Moore.
* Access notes: archive.org fetched directly; Commons originals were rate-limited (HTTP 429) and were fetched through the Wayback Machine (`https://web.archive.org/web/2024id_/<url>`); Google Books / HathiTrust were not needed.

## H. Other Moore verse outside the 1844 book and items not recovered

* **Nothing from the 1844 book is missing:** all 37 items are extracted (33 Moore, 4 not Moore).
* **1806 volume (lead, not extracted):** *A New Translation with Notes, of the Third Satire of Juvenal. To which are added, Miscellaneous Poems, Original and Translated* (New-York: E. Sargeant, 1806), by Moore and John Duer, https://archive.org/details/thirdsatirejuvenal00nonerich. Its table of contents shows early versions of several 1844 poems (lines to Petrosa, to the memory of Cowper, to the fashionable part of my young countrywomen, to the young ladies who attended Mr. Chilton's lectures, a chorus from Aeschylus, lines addressed to Miss *****) and other pieces (Anacreon, Tyrtaeus, Tasso, Petrarch sonnets, 'To William Cobbett', 'Triumph of Woman') that are not individually signed, so the Moore/Duer attribution of the extra pieces is not secure. The OCR of this long-s print is poor; recovering it would need image proofreading of c. 60 pages. Recorded here as a lead only.
* Wikisource's author page lists only the *Visit* and 'Lines to Southey', both already in the corpus. No other verse by Moore was found in a reliable transcription with secure attribution, so no further items were added.
