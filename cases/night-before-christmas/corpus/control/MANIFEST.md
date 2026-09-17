# Control corpus manifest — English verse c. 1780–1840

Corpus root: `corpus/control/<author-slug>/<NN>_<slug>.txt`. Every file has an eight-line header (title, author, date, source, form, lines, attribution, notes), a blank line, then the poem: one verse line per text line, blank line between stanzas, edition spelling and punctuation retained. Long poems are split into parts of ≤150 lines at stanza boundaries ("(part k of n)" in the title). The `form` field was assigned by a CMU-dictionary stress scanner (line-by-line best fit of iambic / anapestic / trochaic / dactylic templates, aggregated per poem) and spot-checked by hand on the well-known anapestic pieces; "anapestic mixed" = predominantly triple metre but with mixed line lengths or many duple lines; "ballad" = alternating iambic 4/3; "mixed" = no dominant pattern.

Word counts = alphabetic tokens (apostrophes/hyphens internal). "Anapestic lines" = verse lines in files whose form begins with "anapestic" (dactylic files are not counted).

## American authors

| author | slug | poems (files) | lines | words | anapestic lines | anapestic files | mean dict-hit |
|---|---|---:|---:|---:|---:|---:|---:|
| Samuel Woodworth | `woodworth` | 99 | 5576 | 37522 | 1418 | 30 | 0.97 |
| Fitz-Greene Halleck | `halleck` | 34 | 2943 | 20881 | 130 | 2 | 0.98 |
| Joseph Rodman Drake | `drake` | 25 | 1548 | 11358 | 36 | 3 | 0.98 |
| William Cullen Bryant | `bryant` | 67 | 4025 | 29704 | 64 | 1 | 0.98 |
| Hannah Flagg Gould | `gould` | 176 | 8088 | 58752 | 2345 | 55 | 0.98 |
| Philip Freneau | `freneau` | 323 | 19759 | 142527 | 4572 | 66 | 0.98 |
| John Trumbull | `trumbull` | 56 | 5725 | 37718 | 0 | 0 | 0.96 |
| Joel Barlow | `barlow` | 15 | 1826 | 14173 | 0 | 0 | 0.96 |
| John Pierpont | `pierpont` | 69 | 6983 | 49164 | 171 | 3 | 0.98 |
| James Kirke Paulding | `paulding` | 25 | 3303 | 25879 | 0 | 0 | 0.96 |
| Lydia Huntley Sigourney | `sigourney` | 133 | 6045 | 41428 | 208 | 4 | 0.97 |
| James Gates Percival | `percival` | 96 | 9939 | 74693 | 583 | 8 | 0.98 |
| Nathaniel Parker Willis | `willis` | 45 | 2971 | 21744 | 0 | 0 | 0.98 |
| Charles Sprague | `sprague` | 33 | 2552 | 18458 | 0 | 0 | 0.98 |
| Richard Henry Dana Sr. | `dana` | 30 | 3279 | 25372 | 0 | 0 | 0.99 |
| Anonymous (The Children's Friend, No. III, New York: William B. Gilley, 1821) | `anon_1821` | 1 | 32 | 210 | 0 | 0 | 0.98 |
| **subtotal** | | **1227** | **84594** | **609583** | **9527** | **172** | |

## British and Irish authors

| author | slug | poems (files) | lines | words | anapestic lines | anapestic files | mean dict-hit |
|---|---|---:|---:|---:|---:|---:|---:|
| William Roscoe | `roscoe` | 1 | 52 | 476 | 52 | 1 | 0.99 |
| Catherine Ann Dorset | `dorset` | 2 | 151 | 1314 | 151 | 2 | 0.96 |
| Thomas Moore | `thomas_moore` | 454 | 16372 | 119094 | 7515 | 201 | 0.97 |
| George Gordon, Lord Byron | `byron` | 118 | 3275 | 21984 | 707 | 26 | 0.98 |
| William Cowper | `cowper` | 159 | 9960 | 69111 | 501 | 16 | 0.98 |
| Robert Southey | `southey` | 79 | 5555 | 38468 | 558 | 7 | 0.97 |
| Thomas Campbell | `campbell` | 102 | 6907 | 49480 | 504 | 14 | 0.97 |
| George Colman the Younger | `colman` | 13 | 1501 | 10636 | 0 | 0 | 0.97 |
| Walter Scott | `scott` | 23 | 3157 | 20169 | 0 | 0 | 0.97 |
| Thomas Hood | `hood` | 186 | 15197 | 106167 | 3201 | 35 | 0.97 |
| Winthrop Mackworth Praed | `praed` | 102 | 7770 | 49961 | 932 | 15 | 0.98 |
| James Smith and Horace Smith | `smith_rejected_addresses` | 23 | 1676 | 11663 | 446 | 7 | 0.96 |
| Robert Bloomfield | `bloomfield` | 24 | 2970 | 20695 | 0 | 0 | 0.96 |
| Charles Wolfe | `wolfe` | 10 | 582 | 4377 | 68 | 2 | 0.98 |
| Thomas Love Peacock | `peacock` | 110 | 7288 | 48172 | 1039 | 17 | 0.96 |
| John Wolcot (Peter Pindar) | `wolcot` | 123 | 8403 | 63827 | 15 | 1 | 0.93 |
| **subtotal** | | **1529** | **90816** | **635594** | **15689** | **344** | |

**Grand total:** 2756 files, 175410 verse lines, 1245177 words; 25216 lines in 516 anapestic files.

## Form distribution (files / lines)

| form | files | lines |
|---|---:|---:|
| iambic pentameter | 834 | 67352 |
| iambic tetrameter | 586 | 38583 |
| anapestic tetrameter | 292 | 14039 |
| ballad | 235 | 11878 |
| iambic mixed | 233 | 15472 |
| mixed | 195 | 11315 |
| anapestic mixed | 161 | 8539 |
| trochaic tetrameter | 91 | 3633 |
| anapestic trimeter | 51 | 2198 |
| iambic trimeter | 42 | 1243 |
| trochaic mixed | 16 | 493 |
| anapestic dimeter | 12 | 440 |
| dactylic mixed | 5 | 120 |
| dactylic tetrameter | 3 | 105 |

## Provenance

- **Samuel Woodworth** (`woodworth`): https://archive.org/details/poemsodessongs00woodrich (The Poems, Odes, Songs, and Other Metrical Effusions of Samuel Woodworth, New York: Abraham Asten and Matthias Lopez, 1818; OCR text); https://archive.org/details/poetis00wood (The Poetical Works of Samuel Woodworth, ed. by his son, New York: Scribner, 1861; OCR text)
- **Fitz-Greene Halleck** (`halleck`): https://www.gutenberg.org/ebooks/34762 (Fanny, with Other Poems, New York: Harper, 1839); https://archive.org/details/alnwickcastlewit15hall (Alnwick Castle, with Other Poems, New York: G. & C. Carvill, 1827; OCR text)
- **Joseph Rodman Drake** (`drake`): https://www.gutenberg.org/ebooks/317 (The Culprit Fay, and Other Poems, New York: George Dearborn, 1835)
- **William Cullen Bryant** (`bryant`): https://www.gutenberg.org/ebooks/16341 (Poems by William Cullen Bryant, authorized edition, Dessau: Katz Brothers, 1854; "Poems" section = poems of 1814-1832)
- **Hannah Flagg Gould** (`gould`): https://archive.org/details/hammahflagg00goulrich (Poems, 2nd ed. with additions, Boston: Hilliard, Gray, 1833; OCR text); https://archive.org/details/poems09goulgoog (Poems, vol. II, Boston: Hilliard, Gray, 1836; OCR text)
- **Philip Freneau** (`freneau`): https://www.gutenberg.org/ebooks/38529 (The Poems of Philip Freneau, ed. F. L. Pattee, Princeton, 1902-07, vol. 2, poems of 1780-1791); https://www.gutenberg.org/ebooks/39909 (The Poems of Philip Freneau, ed. F. L. Pattee, Princeton, 1902-07, vol. 3, poems of 1791-1815)
- **John Trumbull** (`trumbull`): https://archive.org/details/poeticalworksofj0001trum (The Poetical Works of John Trumbull, Hartford, 1820, vol. I; OCR text); https://archive.org/details/poeticalworksofj0002trum (The Poetical Works of John Trumbull, Hartford, 1820, vol. II; OCR text)
- **Joel Barlow** (`barlow`): https://archive.org/details/hastypuddingpoem00barl (The Hasty-Pudding: A Poem in Three Cantos, New York: W. H. Graham, 1847; first pub. 1796; OCR text); https://www.gutenberg.org/ebooks/8683 (The Columbiad: A Poem, Philadelphia, 1807)
- **John Pierpont** (`pierpont`): https://archive.org/details/airspal00pier (Airs of Palestine, and Other Poems, Boston: James Munroe, 1840; OCR text)
- **James Kirke Paulding** (`paulding`): https://archive.org/details/backwoodsmanpoem00paul (The Backwoodsman: A Poem, Philadelphia: M. Thomas, 1818; OCR text)
- **Lydia Huntley Sigourney** (`sigourney`): https://archive.org/details/poems00sigo (Poems, Philadelphia: Key & Biddle, 1834; OCR text)
- **James Gates Percival** (`percival`): https://archive.org/details/poems00perc (Poems, New York: Charles Wiley, 1823; OCR text)
- **Nathaniel Parker Willis** (`willis`): https://archive.org/details/melanieotherpoem00willuoft (Melanie, and Other Poems, ed. Barry Cornwall, London: Saunders and Otley, 1835; OCR text)
- **Charles Sprague** (`sprague`): https://www.gutenberg.org/ebooks/22626 (An Ode pronounced before the Inhabitants of Boston, September 17, 1830); https://archive.org/details/writingsofcharles00sprarich (Writings of Charles Sprague, now first collected, New York, 1841; OCR text)
- **Richard Henry Dana Sr.** (`dana`): https://archive.org/details/poemsprosewritin00dana (Poems and Prose Writings, Boston: Russell, Odiorne, 1833; OCR text)
- **Anonymous (The Children's Friend, No. III, New York: William B. Gilley, 1821)** (`anon_1821`): https://en.wikipedia.org/wiki/Old_Santeclaus_with_Much_Delight (transcription of The Children's Friend, Number III, 1821)
- **William Roscoe** (`roscoe`): https://www.gutenberg.org/ebooks/23665 (The Butterfly's Ball and the Grasshopper's Feast, in the 1854 Grant and Griffith reprint; first pub. 1807)
- **Catherine Ann Dorset** (`dorset`): https://www.gutenberg.org/ebooks/23665 (The Peacock "At Home", 23rd ed., London: Grant and Griffith, 1854; first pub. 1807)
- **Thomas Moore** (`thomas_moore`): https://www.gutenberg.org/ebooks/8187 (The Complete Poems of Sir Thomas Moore, collected by himself, ed. W. M. Rossetti)
- **George Gordon, Lord Byron** (`byron`): https://www.gutenberg.org/ebooks/21811 (The Works of Lord Byron, Poetry vol. III, ed. E. H. Coleridge, London: John Murray, 1900); https://www.gutenberg.org/ebooks/27577 (The Works of Lord Byron, Poetry vol. VII, ed. E. H. Coleridge, London: John Murray, 1904)
- **William Cowper** (`cowper`): https://www.gutenberg.org/ebooks/3698 (The Task, and Other Poems, Cassell National Library ed.); https://www.gutenberg.org/ebooks/47790 (The Works of William Cowper, ed. T. S. Grimshawe, London, 1849; shorter poems)
- **Robert Southey** (`southey`): https://www.gutenberg.org/ebooks/8212 (Poems, Bristol: Cottle, 1797); https://www.gutenberg.org/ebooks/8639 (Poems, vol. II, Bristol: Biggs and Cottle, 1799); Wikisource (see per-file source lines)
- **Thomas Campbell** (`campbell`): https://www.gutenberg.org/ebooks/59788 (The Poetical Works of Thomas Campbell, reprinted from the early editions, London: Griffith Farran, n.d. [c. 1890])
- **George Colman the Younger** (`colman`): https://www.gutenberg.org/ebooks/25426 (Broad Grins, 8th ed., London: Bohn, 1839; first pub. 1802, incorporating My Night-gown and Slippers, 1797)
- **Walter Scott** (`scott`): https://www.gutenberg.org/ebooks/3011 (The Lady of the Lake, ed. W. J. Rolfe, Boston, 1883; first pub. 1810)
- **Thomas Hood** (`hood`): https://www.gutenberg.org/ebooks/15652 (The Poetical Works of Thomas Hood, ed. W. M. Rossetti, New York: A. L. Burt)
- **Winthrop Mackworth Praed** (`praed`): https://www.gutenberg.org/ebooks/71008 (The Poems of Winthrop Mackworth Praed [selected], ed. Frederick Cooper, London: Walter Scott)
- **James Smith and Horace Smith** (`smith_rejected_addresses`): https://www.gutenberg.org/ebooks/3769 (Rejected Addresses; or, The New Theatrum Poetarum, 1812; 22nd ed.)
- **Robert Bloomfield** (`bloomfield`): https://www.gutenberg.org/ebooks/9092 (The Farmer's Boy: A Rural Poem, 3rd ed., London, 1800); https://www.gutenberg.org/ebooks/9047 (The Banks of Wye: A Poem, London, 1811)
- **Charles Wolfe** (`wolfe`): https://archive.org/details/remainsoflaterev00wolfrich (Remains of the late Rev. Charles Wolfe, 3rd ed., London, 1827; OCR text)
- **Thomas Love Peacock** (`peacock`): https://archive.org/details/worksofthomaslov03peacuoft (The Works of Thomas Love Peacock, ed. Henry Cole, London: Bentley, 1875, vol. III: Poetry; OCR text)
- **John Wolcot (Peter Pindar)** (`wolcot`): https://archive.org/details/worksofpeterpind01wolcuoft (The Works of Peter Pindar, Esq., London, 1797, vol. I; OCR text)

## Problems, exclusions and caveats

**Authors / texts not obtained**
- **James Hogg** — skipped. The only machine-readable editions reachable (archive.org OCR of *The Mountain Bard* and the 1838 *Poetical Works*) scored 0.91–0.92 dictionary-hit and are heavily Scots-dialect; automated cleaning could not separate OCR damage from dialect, so nothing was included rather than risk mislabelled metre.
- **Samuel Woodworth, "The Hunters of Kentucky"** — not in the 1861 *Poetical Works* used for Woodworth (only "The Old Oaken Bucket" was taken from the 1818 *Poems*); not found as clean text elsewhere.
- **Halleck/Drake "Croaker" pieces** — jointly written; excluded by design (attribution not single-author).
- **Hannah F. Gould's later volumes (1846–1850s)** — outside the period; not used.
- **Google Books and HathiTrust** return 403 through the proxy, so several first editions could only be represented by Gutenberg or archive.org copies (see Provenance).
- **Southey**: the archive.org *Minor Poems* download failed; "The Cataract of Lodore", "The Old Man's Comforts", "The Well of St. Keyne", "Bishop Bruno", "The Inchcape Rock", "God's Judgment on a Wicked Bishop" and "The Battle of Blenheim" were taken from Wikisource (URL in each file); the rest from Gutenberg 8212 (Poems, 1797) and 8639.

**Texts excluded (and why)**
- Translations and imitations from other languages (Freneau, Campbell "Translations", Peacock's Italian-comedy translation and Latin epitaph pieces, Moore's Anacreon), plays and blank-verse drama (Freneau), Latin/French/Italian poems, bibliographic apparatus, prose "arguments", footnotes and editorial notes.
- Hood: titles first published after 1840 excluded; the Reynolds pieces in *Odes and Addresses to Great People* (e.g. Mrs Fry) excluded. Hood's dates are approximate (by volume). The deliberately archaic "The Carelesse Nurse Mayd" is retained (flagged: dictionary-hit 0.73).
- Peacock: "Newark Abbey" (1842) excluded; Paper Money Lyrics parodies of Southey ("Proœmium of an Epic") and Wordsworth ("A Mood of My Own Mind") are flagged as parodies in `notes`; OCR-garbled titles were reconstructed where the raw scan allowed (e.g. "A Border Ballad", "Pan in Town", "Clonar and Tlamin"); "Fiolfab King of Nokway" = *Fiolfar, King of Norway*; one 20-line untitled continuation fragment is kept under an explicit "Untitled (continuation …)" title.
- Rejected Addresses (James & Horace Smith): every piece is a parody; the target is named in `notes` ("Drury-Lane Hustings" parodies a halfpenny comic-song, no single author).
- Colman's *Broad Grins* is iambic (not anapestic) and is labelled so; Roscoe and Dorset each contribute a single poem, as intended.
- Anonymous "Old Santeclaus" (1821): a single 32-line file, iambic tetrameter.

**OCR-derived authors (archive.org)** — Woodworth, Gould, Trumbull, Pierpont, Paulding, Sigourney, Percival, Willis, Sprague, Dana, Barlow, Wolfe, Peacock, Wolcot, and part of Halleck. Stanza breaks are approximate; running heads, page numbers, footnotes and headnotes were removed heuristically; lines the parser had dropped because they begin with OCR quote marks (`*`), "0"/"1" for O/I or parentheses (about 250 lines, mostly quoted-speech stanza openers) were restored from the raw scans in a final pass; a few dozen unrecoverable garbled lines (dictionary-hit < 25 %) were deleted. Dialogue poems that the parser had split at speaker labels were re-merged with labels removed (Campbell "Lochiel's Warning", Southey's Botany-Bay Eclogues, Peacock "Pan in Town", Wolcot "Bozzy and Piozzi" and "Peter's Prophecy").

**Wolcot (Peter Pindar)** — only the 1797 *Works* vol. I OCR (long-s typography) was obtainable. Long-s was repaired automatically (dictionary-hit 0.84 → 0.93) but residual noise remains (garbled drop-caps, f/s ambiguities such as "fame/same"); the prose "Arguments" printed before each ode were removed; the *Lousiad* canto numbering was reconstructed from running heads; several titles are reconstructed or generic ("Farewell Odes for 1786 (untitled section)"). Treat Wolcot as a low-weight calibration author.

**Form labels** are automatic (CMU-dictionary stress scanner) and were hand-checked on the anchor pieces: "The Destruction of Sennacherib", "Lochiel's Warning", "The Poplar Field", "The Old Oaken Bucket", "Drury-Lane Hustings", Southey's "John, Samuel, & Richard" = anapestic tetrameter; "The Old Man's Comforts" = anapestic mixed; "Old Santeclaus" = iambic tetrameter. Dactylic files are labelled separately and not counted as anapestic; "mixed" files may contain some anapestic lines. Byron's *Hebrew Melodies* (incl. Sennacherib) are in `byron/` files 39–66.

**Other notes** — File numbering has gaps where fragments were merged or deleted. `attribution: certain` follows the collected editions used (Byron's minor "Jeux d'esprit" and Moore's newspaper squibs as attributed by their editors). Dates are the composition/publication year where the edition gives one, otherwise "c." ranges by volume.

