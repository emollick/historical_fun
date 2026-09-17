# Source captures for the historical-records check (Beale Papers)

All captures were made on **2026-09-14**.
Every file listed here was actually read; nothing in `notes/historical_records.md` rests on a source that is not either
in this folder, in `sources/` (Wikisource pamphlet transcription, Wikipedia wikitext, Gillogly 1980) or explicitly marked
"not accessible" in the notes.

Folder layout

| Folder | Contents |
|---|---|
| `chronicling_america/ocr/` | Full-page OCR text of newspaper pages from the Library of Congress *Chronicling America* collection (PRIMARY sources). File name = `{LCCN}_{YYYY-MM-DD}_ed{edition}_sp{page}.txt`. The page image is at `https://www.loc.gov/resource/{LCCN}/{YYYY-MM-DD}/ed-{edition}/?sp={page}`; the OCR came from the `fulltext_file` link in `https://www.loc.gov/resource/{LCCN}/{date}/ed-{n}/?sp={page}&st=text&fo=json`. OCR is raw (uncorrected); quotations in the notes were checked against the text and, where the OCR is garbled, against the page image at the URL. |
| `chronicling_america/searches/` | Condensed hit lists (date, title, state, page URL) for each search run against the collection API. The raw API responses (1-4 MB each) were not kept; the `query_url` field in each file reproduces the search. |
| `books/` | Public-domain book texts downloaded from archive.org (`/download/{id}/{id}_djvu.txt`). |
| `nsa_foia/` | NSA FOIA releases on the Beale Papers (mirrored by The Black Vault; the same documents are on media.defense.gov) and W. F. Friedman's 1949 letters (archive.org copy of NSA REF ID A69983). |
| `papers/` | Open-access papers/PDFs read in full. |
| `metadata/` | Bibliographic metadata JSON (Semantic Scholar Graph API) for paywalled journal articles; API probe of the loc.gov endpoint. |

LCCN key: sn85027015 = The Virginian (Lynchburg, Va.) 1822-1829; sn84024649 = Lynchburg Virginian 1829-185?;
sn86071868 = The Roanoke Times 1890-1895; sn84024735 / sn84024736 / sn83026170 / sn84024014 = Richmond Enquirer and
Alexandria Gazette runs; sn84024738 = The Daily Dispatch (Richmond); sn84024656 = Richmond Daily Whig. Other LCCNs are
out-of-state papers that were false positives for "Beale" (listed in the appendix).

## A. Key newspaper pages (PRIMARY)

| File | Newspaper, date, page | URL | What it shows |
|---|---|---|---|
| `chronicling_america/ocr/sn85027015_1823-09-08_ed1_sp3.txt` | The Virginian (Lynchburg), 8 Sep 1823, p. 3 | https://www.loc.gov/resource/sn85027015/1823-09-08/ed-1/?sp=3 | Music teacher's notice: he "may be seen at his room at Mr. Robert Morris's" - Morriss taking lodgers in Sept 1823, before he had the Washington. |
| `chronicling_america/ocr/sn85027015_1823-09-30_ed1_sp4.txt` | The Virginian, 30 Sep 1823, p. 4 | https://www.loc.gov/resource/sn85027015/1823-09-30/ed-1/?sp=4 | **Earliest record of Morriss and the Washington.** Notice dated "Sept. 20" [1823] under the heading "Washington Tavern" (OCR garbled): Robert Morriss "has rented the house known by the above name, situated on Third street, at the corner immediately above Messrs David & William Kyle's, lately occupied by Mr. Henry Moorman [OCR reads 'Drury'] and that he will be prepared by the first of October, to accommodate BOARDERS, and TRANSIENT CUSTOMERS. From his long experience in this business ... He returns thanks to his friends for the liberal encouragement which he has already received in his line of business". |
| `chronicling_america/ocr/sn85027015_1823-10-10_ed1_sp4.txt` | The Virginian, 10 Oct 1823, p. 4 | https://www.loc.gov/resource/sn85027015/1823-10-10/ed-1/?sp=4 | Revised notice dated "October 7": "WASHINGTON [HOTEL] ... he has rented the house known by the above name, situated on Third street, at the corner immediately above Messrs. David & William Kyle's, lately occupied by Mr. Henry Moorman and he is now prepared to accommodate BOARDERS and TRANSIENT CUSTOMERS ... ROBERT MORRISS. N.B. I have a large yard, in which droves of horses can be accommodated. R. M." Same notice repeated 14 Oct p4, 17 Oct p4, 24 Oct p4, 21 Nov p1, 9 Dec p1 (files with those dates). |
| `chronicling_america/ocr/sn85027015_1823-10-14_ed1_sp4.txt`, `..._1823-10-24_ed1_sp4.txt` | The Virginian, 14 and 24 Oct 1823, p. 4 | https://www.loc.gov/resource/sn85027015/1823-10-14/ed-1/?sp=4 | Deposition notice dated Sept. 26, 1823: depositions to be taken 27 Oct 1823 "at the tavern-house of Robert Morriss, in the town of Lynchburg". |
| `chronicling_america/ocr/sn85027015_1823-12-09_ed1_sp1.txt`, `..._1823-12-12_ed1_sp4.txt` | The Virginian, 9 and 12 Dec 1823 | https://www.loc.gov/resource/sn85027015/1823-12-12/ed-1/?sp=4 | Notice (dated Dec. 5) of depositions to be taken 15 Jan 1824 "at Robert Morriss's tavern, in the town of Lynchburg". The 9 Dec p1 file also carries the Washington notice. |
| `chronicling_america/ocr/sn85027015_1825-04-14_ed1_sp4.txt`, `..._1825-04-18_ed1_sp4.txt`, `..._1825-05-26_ed1_sp4.txt` | The Virginian, Apr-May 1825, p. 4 | https://www.loc.gov/resource/sn85027015/1825-04-14/ed-1/?sp=4 | Depositions "at the tavern of Robert Morriss, in the town of Lynchburg" (May 1825). |
| `chronicling_america/ocr/sn85027015_1825-06-23_ed1_sp4.txt` | The Virginian, 23 Jun 1825, p. 4 | https://www.loc.gov/resource/sn85027015/1825-06-23/ed-1/?sp=4 | "Subscribers to Lucas' Atlas are requested to call at the Washington Hotel, and take them away. ROB. MORRISS. June 6, 1825." (also in the 13, 16, 30 Jun and Jul 1825 files). |
| `chronicling_america/ocr/sn85027015_1826-03-23_ed1_sp4.txt` ... `..._1826-04-27_ed1_sp4.txt` | The Virginian, 23 Mar - 27 Apr 1826, p. 4 | https://www.loc.gov/resource/sn85027015/1826-04-27/ed-1/?sp=4 | "FRANKLIN HOTEL. The Subscriber has removed from the Washington, which he has occupied for more than two years past, to the Franklin Hotel. He returns thanks to the public for the patronage he has received during his residence at the Washington ... ROBERT MORRISS. Dec. 30." [1825]. |
| `chronicling_america/ocr/sn85027015_1826-01-26_ed1_sp1.txt` (and Feb-May 1826 p4 files) | The Virginian, 26 Jan 1826, p. 1 | https://www.loc.gov/resource/sn85027015/1826-01-26/ed-1/?sp=1 | Bedstead-fastening advertisement: the model "may be seen at Mr. Morriss' Franklin Hotel"; the patentee "has sold to Mr. Robert Morriss, of this place, the exclusive right" for adjoining counties. Morriss at the Franklin by January 1826. |
| `chronicling_america/ocr/sn84024649_1829-10-05_ed1_sp4.txt` | Lynchburg Virginian, 5 Oct 1829, p. 4 | https://www.loc.gov/resource/sn84024649/1829-10-05/ed-1/?sp=4 | "WASHINGTON HOTEL. The subscriber respectfully informs the public, that he has extended his lease on the Washington Hotel ... JAS. C. MOORMAN. Sept. 24." Tariff: breakfast 25 c., dinner 37 1/2, supper 25, lodging 12 1/2, horses per day 62 1/2, per month $8, board per year $133.33. Shows the Washington was a leased house kept by a Moorman before (1823) and after (1829) Morriss. |
| `chronicling_america/ocr/sn86071868_1893-01-20_ed1_sp1.txt` | The Roanoke Times, 20 Jan 1893, p. 1 | https://www.loc.gov/resource/sn86071868/1893-01-20/ed-1/?sp=1 | Article "WHERE IS THIS GOLD AND SILVER. Treasure Buried in Bedford County Years Ago." Full retelling of the pamphlet (Morriss, Washington Hotel 1820, St. Louis letter of 9 May 1822, 1817 party of thirty, decoded paper No. 2 with the 1,014/3,812 and 1,907/1,288 lb figures and $13,000 jewels), ending: "The facts in the matter have been given to the public by a friend of Morriss, who learned them in 1863, and have been published in pamphlet form. The inhabitants of Bedford county have hunted for this treasure but so far in vain." Earliest press notice of the pamphlet found in Chronicling America. |
| `chronicling_america/ocr/sn84024738_1861-05-23_ed1_sp2.txt`, `..._05-24...`, `..._05-29...`, `sn84024735_1861-06-18_ed1_sp3.txt`, `sn84024656_1861-06-18_ed1_sp2.txt` | Richmond Daily Dispatch, Enquirer, Whig, May-June 1861 | https://www.loc.gov/resource/sn84024738/1861-05-23/ed-1/?sp=2 | Negative check for a Sarah Morriss death notice in May-June 1861 (the pamphlet implies she died in 1861): the only Morrisses are Richard H., Robert F. and Charles Y. Morriss of Richmond. |
| `chronicling_america/ocr/sn84024735_1820-08-*`, `sn84024735_1821-12-06_ed1_sp2.txt`, `sn84024736_1815-*`, `sn84024014_1815-12-*`, `sn83026170_1819-01-07_ed1_sp2.txt` | Richmond Enquirer 1815-1821, Alexandria Gazette 1815-1819 | e.g. https://www.loc.gov/resource/sn84024735/1821-12-06/ed-1/?sp=2 | Hits for "Washington Hotel" / "Beale" 1815-1821: all refer to other establishments (Washington Hotel in Richmond/Alexandria) or other Beales; no Lynchburg Washington Hotel and no Thomas J. Beale. |

## B. Condensed search captures (`chronicling_america/searches/*_hits.json`)

| File | Query (see `query_url` inside) | Hits | Result |
|---|---|---|---|
| `loc_ca_washington_hotel_va_hits.json` | phrase "washington hotel", Virginia titles, 1815-1830 | 159 | Lynchburg hits begin 1825 (Morriss, Lucas' Atlas) and 1829 (Moorman); earlier hits are Richmond/Alexandria houses. |
| `loc_ca_lynchburg_hotel_1818_1823_hits.json` | lynchburg + washington + hotel, 1818-1823 | 431 | No Lynchburg "Washington Hotel" before Morriss's own notices of Sept-Oct 1823 (Lynchburg has no digitised paper before Aug 1822). |
| `loc_ca_virginian_washington_1822_23_hits.json` | washington + tavern, Lynchburg, Aug 1822 - Oct 1823 | 61 | Located the 30 Sep 1823 notice. |
| `loc_ca_henry_moorman_1818_1824_hits.json` | phrase "henry moorman", 1815-1826 | 11 | The 1823 Morriss notices (prior occupant Henry Moorman); no notice by Moorman himself about the Washington. |
| `loc_ca_moorman_va_1818_1824_hits.json` | moorman + hotel, Virginia, 1818-1824 | 79 | Nothing on who kept the Washington in 1820. |
| `loc_ca_morriss_va_hits.json` | morriss, Virginia, 1815-1830 | 219 | Source of the Morriss tavern / Franklin Hotel pages above. |
| `loc_ca_robert_morriss_1863_hits.json` | phrase "robert morriss", Dec 1862 - Mar 1863 | 0 | Lynchburg Virginian for 1863 is not in Chronicling America; death notice not retrievable here. |
| `loc_ca_morriss_va_1861_hits.json`, `loc_ca_morriss_va_1865_hits.json` | morriss, Virginia, May-Jun 1861 / May-Jun 1865 | 5 / 0 | No Sarah Morriss notice. |
| `loc_ca_thomas_beall_mo_hits.json`, `loc_ca_beall_mo_1819_1822_any_hits.json`, `loc_ca_morriss_mo_1830_1834_hits.json`, `loc_ca_titles_missouri_1820_hits.json`, `loc_ca_titles_stlouis_hits.json` | Missouri titles and Beall/Morriss searches 1818-1834 | 0 / 0 / 0 / 98 titles / 0 | Chronicling America has no Missouri newspaper pages for 1817-1834 relevant here (Missouri Intelligencer, Missouri Gazette, St. Louis Beacon are not digitised there). |
| `loc_ca_beale_papers_1885_hits.json`, `loc_ca_beale_papers_1885_1900_hits.json` | phrase "beale papers", 1885-1890 / 1885-1900 | 1 / 1 | The single hit is the Roanoke Times of 20 Jan 1893. |
| `loc_ca_beale_treasure_bedford_1885_1900_hits.json`, `loc_ca_beale_cipher_bedford_1885_1915_hits.json`, `loc_ca_beale_treasure_lynchburg_1885_1915_hits.json`, `loc_ca_beale_morriss_1885_1915_hits.json` | beale + treasure/cipher + bedford/lynchburg/morriss, 1885-1915 | 180 / 36 / 195 / 227 | Every Virginia hit for 1885-1899 (and a sample of out-of-state hits) was fetched and read (appendix): all are other Beales except the Roanoke Times article. No 1885-1892 notice of the pamphlet, its sale, or a printing-house fire. |
| `loc_ca_lynchburg_titles_hits.json`, `loc_ca_titles_lynchburg_hits.json` | title lists | - | Lynchburg titles in Chronicling America: Lynchburg Star 1805-181? (few issues), The Virginian 1822-1829, Lynchburg Virginian 1829-185?, Lynchburg Daily Virginian 1852-1861. Nothing for 1819-1821, 1862-1865 or 1885-1890. |

## C. Books (archive.org, public domain; SECONDARY unless noted)

| File | Work | URL | What it shows |
|---|---|---|---|
| `books/sketchesrecollec00cabe.txt` | Mrs. M. Cabell, *Sketches and Recollections of Lynchburg, by the Oldest Inhabitant* (Richmond, 1858) | https://archive.org/details/sketchesrecollec00cabe | pp. 239-241 "ROBERT MORRISS": in 1820 ("thirty-eight years since") Morriss owned "the large dwelling opposite the residence of Dr. Robert Early" and "was a man of wealth"; after "a sudden reverse" he and his wife "there established a house for receiving boarders"; "In the year 1824, Mr. Morriss took possession of the Washington House ... then he moved to the Franklin Hotel"; couple still living in 1858. p. 185: Masonic ball Dec 1827 at the Franklin Hotel supplied by Mrs. Robert Morriss. p. 192: house "formerly occupied by Robert Morriss, Esq." taken by another family in autumn 1827. p. 196: his former house "was, in 1823, the residence of Mrs. Brown, of Amherst". p. 297: Franklin Hotel leased by Morriss after Mr. Hoyle; now (1858) the "Norvelle House". Contemporary recollection, written 1858. |
| `books/lynchburgitspeop00chri.txt` | W. A. Christian, *Lynchburg and Its People* (Lynchburg, 1900) | https://archive.org/details/lynchburgitspeop00chri | 1813: "Robert Morris" on the committee to build the new market house; Jan 1819: "Robert Morris, Treasurer of Lynchburg Toll Bridge Company, declared a dividend of two per cent"; 1842: Universalist church lot "just back of Morriss' hotel"; 1865-68 mentions of the "Washington House"/"Washington Hotel"; the "Arlington" hotel from 1877 and the "Norvell-Arlington". |
| `books/commerceofprair01greg.txt` | Josiah Gregg, *Commerce of the Prairies*, vol. 1 (New York, 1844; this scan is a later printing with the 1844 preface) | https://archive.org/details/commerceofprair01greg | Ch. I pp. 17-22: Pursley 1805, La Lande 1804, McKnight-Beard-Chambers 1812 "seized as spies, their goods and chattels confiscated, and themselves thrown into the calabozos of Chihuahua ... nine years"; Glenn and Becknell 1821; "First Introduction of wheeled Vehicles" (Becknell's second journey, 1822). |
| `books/americanfurtrade00chit_0.txt` | H. M. Chittenden, *The American Fur Trade of the Far West* (New York, 1902), vol. 2 | https://archive.org/details/americanfurtrade00chit_0 | Part IV ch. XXVIII "The Santa Fe Trade", pp. 496-501: McKnight-Baird-Chambers 1812 (nine years in prison); Chouteau and De Munn 1815-17 (ordered out, arrested 24 May 1817, forty-eight days' imprisonment, all property confiscated, ~$30,000 claim; Missouri Gazette 13 Sept 1817 quoted); D. Meriwether taken prisoner 1819; "The period of Spanish dominion in New Mexico, which terminated in 1821, was thus marked by total failure on the part of American traders to gain any foothold in the Santa Fe trade". Chapter synopsis lists "First wagons on the Santa Fe Trail" after Becknell's second journey (1822). |
| `books/americanfurtrade01chit.txt` | Chittenden, vol. 1 | https://archive.org/details/americanfurtrade01chit | Context on St. Louis and the 1819-20 Yellowstone expedition; no Beale material. |
| `books/genealogyofbeale00hodg.txt` | [Hodges], *Genealogy of the Beale Family, 1399-1956* | https://archive.org/details/genealogyofbeale00hodg | pp. 93-94 (entry E2): Thomas Beale, merchant, clerk in the Alexandria china store of his brothers John and Charles Beale; engaged to "Miss Judy Hancock of Fincastle"; fought a duel with "a Mr. Risk" (Beale uninjured); fled to New Orleans "until he heard of Risk's recovery", went to Europe, "returned & died in New Orleans where he had married a French lady, Celeste Grandpierre"; children Celeste, Octavia, James. No dates given. Charles Beale (E4) b. 1771 d. 1842, delegate 1804-07, state senator 1830-34. Family genealogy, undocumented. |

## D. NSA FOIA releases (SECONDARY, but they quote/describe primary records)

| File | Document | URL | What it shows |
|---|---|---|---|
| `nsa_foia/doc656726.pdf` / `.txt` | Carl Nelson [Jr.], "BCSC Report, 15 April 1972" (Beale Cypher Study Committee), in NSA FOIA release DOCID 656726 | https://documents.theblackvault.com/documents/nsa/bealepapers/doc656726.pdf (also https://media.defense.gov/2021/Jul/15/2002763571/-1/-1/0/DOC656726.PDF) | Newspaper research: Columbia (Mo.) Herald-Statesman, Missouri Intelligencer (Franklin, Mo.), Illinois Intelligencer (Kaskaskia), Illinois Emigrant/Gazette (Shawneetown), Richmond Enquirer (Jan-Jul 1817, Jan-Mar 1820) - "NO BEALE PARTY ITEMS WERE FOUND", except a letter held at the Franklin (Mo.) post office for "THOMAS BEALL" in the 1 April 1820 Missouri Intelligencer (confirmed with the Missouri Historical Society; not in later lists). Spanish Archives of New Mexico (LoC microfilm rolls 18-22, 1815-1821): "NO BEALE PARTY REFERENCES WERE FOUND"; notes Roll 18 fr. 862 (Nov 1817; year digit unclear in the OCR) travel regulations for visitors and Roll 19 fr. 441 (11 Nov 1818) instructions on passports. Also: Richmond post office letter for "Reuben Beale" (11 Mar 1817); Charles Beale of Botetourt on the Washington Monument commission (9 May 1817); Norborne B. Beall, Louisville 1819. |
| `nsa_foia/doc656779.pdf` / `.txt` | George L. Hart, Sr., "The Beale Papers ... in an attempt to bring up to date all that is known and surmised about the subject", 1964 (the "Hart Papers"), NSA FOIA DOCID 656779 | https://documents.theblackvault.com/documents/nsa/bealepapers/doc656779.pdf | Clayton Hart learned of the ciphers in summer 1897 from N. H. Hazlewood of Montvale (formerly Buford); digging from 1898. "The manuscript ... was prepared by James B. Ward, of Campbell County, Virginia, contiguous to Lynchburg, in the year 1885. It was printed in pamphlet form by the Virginian Job Print, Lynchburg, Va. However, Clayton was informed by Ward that all but a few copies had been destroyed by fire, which broke out in the printing plant before a plan of distribution and sale at 50c a copy had been made and carried out. About the year 1903 Clayton visited Mr. Ward, who then was at an advanced age. He confirmed all that is contained in the pamphlet; and his son, then U.S. Mail transfer clerk at the union station, Lynchburg, added his own confirmation". Hart: "we secured confirmation as to the Washington Hotel, and its proprietor, Mr. Morriss, during the period 1819 to 1862" (no source given). Hart's doubt: "I have wondered if Ward might have written his manuscript based upon some figures he found, or made up; and yet, we have the word of Ward, his son, and friends to the contrary. Inquiry among some aged neighbors of Ward showed the high respect they had for him, and brought forth the statement that Ward would never practice deception." Reprints the pamphlet text. |
| `nsa_foia/doc656729.pdf` / `.txt` | Miscellaneous NSA release on the Beale Papers (DOCID 656729) | https://documents.theblackvault.com/documents/nsa/bealepapers/doc656729.pdf | Correspondence and notes; used only for context. |
| `nsa_foia/friedman_letters_percy_1949_A69983.txt` | W. F. Friedman, letters to Alfred Percy (15 Aug 1949) and Martha Rivers Adams (16 Jun 1949), NSA REF ID A69983 | https://archive.org/details/41733399077263 | Friedman "do[es] not intend by any means to drop the study which I initiated on [The Beale Papers] sometime ago" (1949). Documents his interest; no findings. |

## E. Papers and metadata

| File | Item | URL | What it shows |
|---|---|---|---|
| `papers/wase2020.pdf` / `.txt` | Viktor Wase, "The Role of Base 10 in the Beale Papers", *Proceedings of the 3rd International Conference on Historical Cryptology (HistoCrypt 2020)*, Linköping Electronic Conference Proceedings 171, pp. 153-157 | https://ep.liu.se/ecp/171/019/ecp2020_171_019.pdf | Discrete KS tests on last digits (base 10 p-values 0.4%, 0.02%, 0.4% for B1, B2, B3), leading digits vs Benford (0.043%, 3.1%, 0.004%), repeated in bases coprime to 10; B1 and B3 behave differently in base 10 than in other bases, B2 does not; "One can, with a greater certainty than before, declare the Beale Papers to be frauds." Also summarises Chan 2008 (St. Louis Beacon, Aug 1832, letter held for "Robert Morriss") and Hammer's 1970 NSA-conference paper (released 2001). |
| `papers/schmeh_mtc3.pdf` / `.txt` | Klaus Schmeh, "The Beale Ciphers" (MysteryTwister challenge sheet, 2010 file) | https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-04-beale-en.pdf | Statement of the problem and the two unsolved cipher texts; no historical findings. |
| `metadata/10.1145_362452.362461.json` | Semantic Scholar record: C. Hammer, "Signature simulation and certain cryptographic codes", *Communications of the ACM* 14(1), 1971 | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/362452.362461 | Bibliographic data only (paper paywalled). |
| `metadata/10.1080_0161-118091854979.json` | J. Gillogly, "The Beale Cipher: a Dissenting Opinion", *Cryptologia* 4(2), 1980 | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/0161-118091854979 | Bibliographic data; full text is in `sources/gillogly_1980_plain.txt`. |
| `metadata/10.1080_0161-118891863007.json` | L. Kruh, "The Beale Cipher as a Bamboozlement - Part II", *Cryptologia* 12(4):241-246, 1988 | (as above, DOI 10.1080/0161-118891863007) | Bibliographic data only. Part I: Kruh, "A Basic Probe of the Beale Cipher as a Bamboozlement", *Cryptologia* 6(4):378-382, Oct 1982, DOI 10.1080/0161-118291857190 (Crossref, 2026-09-14). Hammer, "How did TJB encode B2?", *Cryptologia* 3(1):9-15, Jan 1979, DOI 10.1080/0161-117991853747 (Crossref). |
| `metadata/10.1080_01611190701577759.json` | W.-S. Chan, "Key Enclosed: Examining the Evidence for the Missing Key Letter of the Beale Cipher", *Cryptologia* 32(1), 2008 | (DOI as in file name) | Bibliographic data only. |
| `metadata/10.1080_01611194.2013.798517.json` | T. D. Mateer, "Cryptanalysis of Beale Cipher Number Two", *Cryptologia* 37(3), 2013 | (DOI as in file name) | Bibliographic data only. |
| `metadata/10.1080_01611194.2018.1550691.json` | J. Dooley, "The Beale ciphers in fiction", *Cryptologia* 43(4), 2019 | (DOI as in file name) | Abstract. |
| `metadata/10.1080_01611194.2020.1821409.json` | V. Wase, "Benford's law in the Beale ciphers", *Cryptologia* 45(3), 2021 | (DOI as in file name) | Abstract. |
| `metadata/10.1080_01611194.2022.2116614.json` | L. Campanelli, "A statistical cryptanalysis of the Beale ciphers", *Cryptologia* 47(5), 2023 | (DOI as in file name) | Abstract (epsilon-Benford, epsilon about 0.15 for B2). |
| `metadata/search_*.json` | Semantic Scholar title searches for Hammer 1979, Kruh 1982, Nickell 1982 and a 2026 "reproducible re-examination" paper | https://api.semanticscholar.org/graph/v1/paper/search?query=... | Empty results (API returned nothing for these titles). |
| `metadata/loc_api_probe.json` | Probe of the loc.gov Chronicling America JSON endpoint | https://www.loc.gov/collections/chronicling-america/?fo=json | Confirms field names used by the search scripts. |

Web pages consulted but not captured as files (secondary; quoted in the notes only where stated):
Cipher Mysteries, "The two Thomas Beales..." (N. Pelling, 23 May 2015) https://ciphermysteries.com/2015/05/23/the-two-thomas-beales ;
TreasureNet thread "Robert Morriss - 1863..." https://www.treasurenet.com/threads/robert-morriss-1863.312580/ (transcription of the Lynchburg Virginian death notice of 8 Jan 1863) and "The Robert and Sarah Morriss Story" https://www.treasurenet.com/threads/the-robert-and-sarah-morriss-story.520583/ ;
Mental Floss, "The Quest to Break America's Most Mysterious Code" https://www.mentalfloss.com/article/540277/beale-ciphers-buried-treasure .

## F. Not accessible from this environment (see notes for the best secondary pointer in each case)

JSTOR (Nickell 1982, stable/4248566: JavaScript challenge page); Taylor & Francis full texts (Hammer 1979, Kruh 1982/1988, Chan 2008, Mateer 2013, Wase 2021, Campanelli 2023: 403); ACM DL (Hammer 1971: 403); archive.org lending-only books (Poundstone 1993 *Biggest Secrets*, Innis 1973 *Gold in the Blue Ridge*, Matyas 2011, Bauer 2017: 401/"item not available"); nsa.gov Beale Papers page (Access Denied; Black Vault / media.defense.gov mirrors used instead); virginiachronicle.com and babel.hathitrust.org (Cloudflare challenge); findagrave.com (403); Ancestry census indexes (subscription); angelfire.com and unmuseum.org (blocked by proxy policy); researchgate.net (403); Georgia Southern digitalcommons PDF (returned HTML); Popular Mechanics and web.archive.org (fetch failed); Viemeister 1987/1997 (not online); U.S. Copyright Office record books for 1885 (not online); New Orleans probate records for Thomas Beale (not online).

## Appendix: every OCR page in `chronicling_america/ocr/` (all read; "-" = no relevant content, i.e. other persons named Beale/Morriss or other Washington Hotels)

| File | Newspaper | Page URL | Relevant? |
|---|---|---|---|
| `sn78000873_1892-10-27_ed1_sp1.txt` | the republican journal (belfast, me.) 1829-current | https://www.loc.gov/resource/sn78000873/1892-10-27/ed-1/?sp=1 | - |
| `sn82014248_1885-06-08_ed1_sp1.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1885-06-08/ed-1/?sp=1 | - |
| `sn82014248_1889-08-23_ed1_sp2.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1889-08-23/ed-1/?sp=2 | - |
| `sn82014248_1889-10-23_ed1_sp1.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1889-10-23/ed-1/?sp=1 | - |
| `sn82014248_1895-10-30_ed1_sp6.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1895-10-30/ed-1/?sp=6 | - |
| `sn82014248_1896-02-14_ed1_sp2.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1896-02-14/ed-1/?sp=2 | - |
| `sn82014248_1899-06-20_ed1_sp3.txt` | daily kennebec journal (augusta, me.) 1870-1975 [microfilm reel] | https://www.loc.gov/resource/sn82014248/1899-06-20/ed-1/?sp=3 | - |
| `sn82014381_1885-03-16_ed1_sp3.txt` | sacramento daily record-union (sacramento [calif.]) 1875-1891 | https://www.loc.gov/resource/sn82014381/1885-03-16/ed-1/?sp=3 | - |
| `sn82014381_1885-04-02_ed1_sp3.txt` | sacramento daily record-union (sacramento [calif.]) 1875-1891 | https://www.loc.gov/resource/sn82014381/1885-04-02/ed-1/?sp=3 | - |
| `sn82014381_1885-06-30_ed1_sp1.txt` | sacramento daily record-union (sacramento [calif.]) 1875-1891 | https://www.loc.gov/resource/sn82014381/1885-06-30/ed-1/?sp=1 | - |
| `sn82015137_1886-10-04_ed1_sp8.txt` | savannah morning news (savannah) 1868-1887 | https://www.loc.gov/resource/sn82015137/1886-10-04/ed-1/?sp=8 | - |
| `sn82016187_1886-08-26_ed1_sp1.txt` | the national tribune (washington, d.c.) 1877-1917 | https://www.loc.gov/resource/sn82016187/1886-08-26/ed-1/?sp=1 | - |
| `sn82016187_1890-09-11_ed1_sp6.txt` | the national tribune (washington, d.c.) 1877-1917 | https://www.loc.gov/resource/sn82016187/1890-09-11/ed-1/?sp=6 | - |
| `sn82016187_1894-10-04_ed1_sp6.txt` | the national tribune (washington, d.c.) 1877-1917 | https://www.loc.gov/resource/sn82016187/1894-10-04/ed-1/?sp=6 | - |
| `sn83016025_1886-01-05_ed1_sp1.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1886-01-05/ed-1/?sp=1 | - |
| `sn83016025_1890-10-25_ed1_sp3.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1890-10-25/ed-1/?sp=3 | - |
| `sn83016025_1892-03-08_ed1_sp7.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1892-03-08/ed-1/?sp=7 | - |
| `sn83016025_1894-09-18_ed1_sp8.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1894-09-18/ed-1/?sp=8 | - |
| `sn83016025_1897-06-15_ed1_sp5.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1897-06-15/ed-1/?sp=5 | - |
| `sn83016025_1897-06-24_ed1_sp2.txt` | the portland daily press (portland, me.) 1862-1921 | https://www.loc.gov/resource/sn83016025/1897-06-24/ed-1/?sp=2 | - |
| `sn83016107_1890-03-28_ed1_sp2.txt` | the aegis & intelligencer (bel air, md.) 1864-1923 | https://www.loc.gov/resource/sn83016107/1890-03-28/ed-1/?sp=2 | - |
| `sn83026170_1819-01-07_ed1_sp2.txt` | alexandria gazette & daily advertiser (alexandria [va.]) 1817-1822 | https://www.loc.gov/resource/sn83026170/1819-01-07/ed-1/?sp=2 | - |
| `sn83030180_1897-05-06_ed1_sp11.txt` | new york journal and advertiser (new york [n.y.]) 1897-1901 | https://www.loc.gov/resource/sn83030180/1897-05-06/ed-1/?sp=11 | - |
| `sn83030180_1897-05-16_ed1_sp53.txt` | new york journal and advertiser (new york [n.y.]) 1897-1901 | https://www.loc.gov/resource/sn83030180/1897-05-16/ed-1/?sp=53 | - |
| `sn83030193_1888-05-03_ed3_sp2.txt` | the evening world (new york, n.y.) 1887-1931 | https://www.loc.gov/resource/sn83030193/1888-05-03/ed-3/?sp=2 | - |
| `sn83030214_1891-02-24_ed1_sp2.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1891-02-24/ed-1/?sp=2 | - |
| `sn83030214_1891-06-27_ed1_sp11.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1891-06-27/ed-1/?sp=11 | - |
| `sn83030214_1895-07-15_ed1_sp4.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1895-07-15/ed-1/?sp=4 | - |
| `sn83030214_1897-05-16_ed1_sp5.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1897-05-16/ed-1/?sp=5 | - |
| `sn83030214_1900-04-11_ed1_sp3.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1900-04-11/ed-1/?sp=3 | - |
| `sn83030214_1900-04-25_ed1_sp7.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1900-04-25/ed-1/?sp=7 | - |
| `sn83030214_1901-08-14_ed1_sp4.txt` | new-york tribune (new york [n.y.]) 1866-1924 | https://www.loc.gov/resource/sn83030214/1901-08-14/ed-1/?sp=4 | - |
| `sn83030272_1888-08-11_ed1_sp3.txt` | the sun (new york [n.y.]) 1833-1916 | https://www.loc.gov/resource/sn83030272/1888-08-11/ed-1/?sp=3 | - |
| `sn83045160_1885-02-01_ed1_sp4.txt` | memphis daily appeal (memphis, tenn.) 1847-1886 | https://www.loc.gov/resource/sn83045160/1885-02-01/ed-1/?sp=4 | - |
| `sn83045160_1885-08-07_ed1_sp2.txt` | memphis daily appeal (memphis, tenn.) 1847-1886 | https://www.loc.gov/resource/sn83045160/1885-08-07/ed-1/?sp=2 | - |
| `sn83045160_1885-09-16_ed1_sp1.txt` | memphis daily appeal (memphis, tenn.) 1847-1886 | https://www.loc.gov/resource/sn83045160/1885-09-16/ed-1/?sp=1 | - |
| `sn83045160_1885-09-16_ed1_sp4.txt` | memphis daily appeal (memphis, tenn.) 1847-1886 | https://www.loc.gov/resource/sn83045160/1885-09-16/ed-1/?sp=4 | - |
| `sn83045160_1885-10-14_ed1_sp4.txt` | memphis daily appeal (memphis, tenn.) 1847-1886 | https://www.loc.gov/resource/sn83045160/1885-10-14/ed-1/?sp=4 | - |
| `sn83045462_1887-07-05_ed1_sp1.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1887-07-05/ed-1/?sp=1 | - |
| `sn83045462_1889-08-03_ed1_sp9.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1889-08-03/ed-1/?sp=9 | - |
| `sn83045462_1890-07-07_ed1_sp2.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1890-07-07/ed-1/?sp=2 | - |
| `sn83045462_1894-06-25_ed1_sp11.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1894-06-25/ed-1/?sp=11 | - |
| `sn83045462_1894-11-15_ed1_sp2.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1894-11-15/ed-1/?sp=2 | - |
| `sn83045462_1895-11-01_ed1_sp10.txt` | evening star (washington, d.c.) 1854-1972 | https://www.loc.gov/resource/sn83045462/1895-11-01/ed-1/?sp=10 | - |
| `sn84020630_1901-01-23_ed1_sp3.txt` | santa fe new mexican (santa fe, n.m.) 1898-1951 | https://www.loc.gov/resource/sn84020630/1901-01-23/ed-1/?sp=3 | - |
| `sn84022060_1899-06-13_ed1_sp3.txt` | the silver state (unionville, nev.) 1870-1903 | https://www.loc.gov/resource/sn84022060/1899-06-13/ed-1/?sp=3 | - |
| `sn84022060_1899-06-16_ed1_sp3.txt` | the silver state (unionville, nev.) 1870-1903 | https://www.loc.gov/resource/sn84022060/1899-06-16/ed-1/?sp=3 | - |
| `sn84022770_1896-02-28_ed1_sp4.txt` | washington standard (olympia, wash. territory) 1860-1921 | https://www.loc.gov/resource/sn84022770/1896-02-28/ed-1/?sp=4 | - |
| `sn84022770_1896-03-27_ed1_sp4.txt` | washington standard (olympia, wash. territory) 1860-1921 | https://www.loc.gov/resource/sn84022770/1896-03-27/ed-1/?sp=4 | - |
| `sn84022770_1896-04-10_ed1_sp4.txt` | washington standard (olympia, wash. territory) 1860-1921 | https://www.loc.gov/resource/sn84022770/1896-04-10/ed-1/?sp=4 | - |
| `sn84022770_1896-05-01_ed1_sp4.txt` | washington standard (olympia, wash. territory) 1860-1921 | https://www.loc.gov/resource/sn84022770/1896-05-01/ed-1/?sp=4 | - |
| `sn84024014_1815-12-15_ed1_sp3.txt` | alexandria gazette, commercial and political (alexandria [va.]) 1812-1817 | https://www.loc.gov/resource/sn84024014/1815-12-15/ed-1/?sp=3 | - |
| `sn84024014_1815-12-18_ed1_sp2.txt` | alexandria gazette, commercial and political (alexandria [va.]) 1812-1817 | https://www.loc.gov/resource/sn84024014/1815-12-18/ed-1/?sp=2 | - |
| `sn84024014_1815-12-20_ed1_sp1.txt` | alexandria gazette, commercial and political (alexandria [va.]) 1812-1817 | https://www.loc.gov/resource/sn84024014/1815-12-20/ed-1/?sp=1 | - |
| `sn84024448_1886-03-17_ed1_sp5.txt` | the memphis appeal (memphis, tenn.) 1886-1890 | https://www.loc.gov/resource/sn84024448/1886-03-17/ed-1/?sp=5 | - |
| `sn84024546_1889-06-27_ed1_sp4.txt` | pittsburg dispatch (pittsburg [pa.]) 1880-1923 | https://www.loc.gov/resource/sn84024546/1889-06-27/ed-1/?sp=4 | - |
| `sn84024546_1890-05-29_ed1_sp12.txt` | pittsburg dispatch (pittsburg [pa.]) 1880-1923 | https://www.loc.gov/resource/sn84024546/1890-05-29/ed-1/?sp=12 | - |
| `sn84024546_1891-08-09_ed1_sp12.txt` | pittsburg dispatch (pittsburg [pa.]) 1880-1923 | https://www.loc.gov/resource/sn84024546/1891-08-09/ed-1/?sp=12 | - |
| `sn84024649_1829-09-07_ed1_sp3.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-09-07/ed-1/?sp=3 | - |
| `sn84024649_1829-10-05_ed1_sp4.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-05/ed-1/?sp=4 | Jas. C. Moorman extends lease on the Washington Hotel |
| `sn84024649_1829-10-08_ed1_sp4.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-08/ed-1/?sp=4 | - |
| `sn84024649_1829-10-19_ed1_sp1.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-19/ed-1/?sp=1 | - |
| `sn84024649_1829-10-19_ed1_sp3.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-19/ed-1/?sp=3 | - |
| `sn84024649_1829-10-22_ed1_sp1.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-22/ed-1/?sp=1 | - |
| `sn84024649_1829-10-29_ed1_sp4.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-10-29/ed-1/?sp=4 | - |
| `sn84024649_1829-11-02_ed1_sp4.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-11-02/ed-1/?sp=4 | - |
| `sn84024649_1829-11-12_ed1_sp3.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-11-12/ed-1/?sp=3 | - |
| `sn84024649_1829-11-16_ed1_sp4.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1829-11-16/ed-1/?sp=4 | - |
| `sn84024649_1830-01-07_ed1_sp3.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1830-01-07/ed-1/?sp=3 | - |
| `sn84024649_1830-12-27_ed1_sp3.txt` | lynchburg virginian (lynchburg [va.]) 1829-185? | https://www.loc.gov/resource/sn84024649/1830-12-27/ed-1/?sp=3 | - |
| `sn84024656_1861-06-18_ed1_sp2.txt` | richmond daily whig (richmond, va.) 1842-1861 | https://www.loc.gov/resource/sn84024656/1861-06-18/ed-1/?sp=2 | - |
| `sn84024707_1893-04-06_ed1_sp2.txt` | the valley virginian (staunton, va.) 1865-1895 | https://www.loc.gov/resource/sn84024707/1893-04-06/ed-1/?sp=2 | - |
| `sn84024718_1887-04-06_ed1_sp2.txt` | staunton spectator (staunton, va.) 1849-1896 | https://www.loc.gov/resource/sn84024718/1887-04-06/ed-1/?sp=2 | - |
| `sn84024735_1820-08-04_ed1_sp1.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1820-08-04/ed-1/?sp=1 | - |
| `sn84024735_1820-08-08_ed1_sp1.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1820-08-08/ed-1/?sp=1 | - |
| `sn84024735_1820-08-15_ed1_sp4.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1820-08-15/ed-1/?sp=4 | - |
| `sn84024735_1820-08-22_ed1_sp1.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1820-08-22/ed-1/?sp=1 | - |
| `sn84024735_1820-08-25_ed1_sp1.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1820-08-25/ed-1/?sp=1 | - |
| `sn84024735_1821-12-06_ed1_sp2.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1821-12-06/ed-1/?sp=2 | - |
| `sn84024735_1861-06-18_ed1_sp3.txt` | richmond enquirer (richmond, va.) 1815-1867 | https://www.loc.gov/resource/sn84024735/1861-06-18/ed-1/?sp=3 | - |
| `sn84024736_1815-01-07_ed1_sp2.txt` | the enquirer (richmond, va.) 1804-1815 | https://www.loc.gov/resource/sn84024736/1815-01-07/ed-1/?sp=2 | - |
| `sn84024736_1815-05-13_ed1_sp3.txt` | the enquirer (richmond, va.) 1804-1815 | https://www.loc.gov/resource/sn84024736/1815-05-13/ed-1/?sp=3 | - |
| `sn84024736_1815-05-20_ed1_sp2.txt` | the enquirer (richmond, va.) 1804-1815 | https://www.loc.gov/resource/sn84024736/1815-05-20/ed-1/?sp=2 | - |
| `sn84024738_1861-05-23_ed1_sp2.txt` | the daily dispatch (richmond [va.]) 1850-1884 | https://www.loc.gov/resource/sn84024738/1861-05-23/ed-1/?sp=2 | negative check (Sarah Morriss) |
| `sn84024738_1861-05-24_ed1_sp2.txt` | the daily dispatch (richmond [va.]) 1850-1884 | https://www.loc.gov/resource/sn84024738/1861-05-24/ed-1/?sp=2 | negative check (Sarah Morriss) |
| `sn84024738_1861-05-29_ed1_sp2.txt` | the daily dispatch (richmond [va.]) 1850-1884 | https://www.loc.gov/resource/sn84024738/1861-05-29/ed-1/?sp=2 | negative check (Sarah Morriss) |
| `sn84024828_1893-09-23_ed1_sp3.txt` | mohave county miner (mineral park, a.t. [ariz.]) 1882-1918 | https://www.loc.gov/resource/sn84024828/1893-09-23/ed-1/?sp=3 | - |
| `sn84025968_1892-08-28_ed1_sp4.txt` | los angeles herald (los angeles [calif.]) 1890-1893 | https://www.loc.gov/resource/sn84025968/1892-08-28/ed-1/?sp=4 | - |
| `sn84026784_1886-08-05_ed1_sp3.txt` | virginia free press (charlestown, va. [w. va.]) 1832-1916 | https://www.loc.gov/resource/sn84026784/1886-08-05/ed-1/?sp=3 | - |
| `sn84026784_1894-03-21_ed1_sp2.txt` | virginia free press (charlestown, va. [w. va.]) 1832-1916 | https://www.loc.gov/resource/sn84026784/1894-03-21/ed-1/?sp=2 | - |
| `sn84026788_1902-08-26_ed1_sp3.txt` | spirit of jefferson (charles town, va. [w. va.]) 1844-1948 | https://www.loc.gov/resource/sn84026788/1902-08-26/ed-1/?sp=3 | - |
| `sn84026817_1900-03-07_ed1_sp3.txt` | the weekly register (point pleasant, va. [w. va.]) 1862-1909 | https://www.loc.gov/resource/sn84026817/1900-03-07/ed-1/?sp=3 | - |
| `sn84036034_1888-11-03_ed1_sp4.txt` | butte semi-weekly miner (butte, mont.) 1886-1890 | https://www.loc.gov/resource/sn84036034/1888-11-03/ed-1/?sp=4 | - |
| `sn84037217_1895-10-10_ed1_sp3.txt` | greenbrier independent (lewisburg, va. [w. va.]) 1859-1980 | https://www.loc.gov/resource/sn84037217/1895-10-10/ed-1/?sp=3 | - |
| `sn84038560_1889-06-03_ed1_sp2.txt` | weekly courier-journal (louisville [ky.]) 1874-1917 | https://www.loc.gov/resource/sn84038560/1889-06-03/ed-1/?sp=2 | - |
| `sn84038560_1896-08-03_ed1_sp8.txt` | weekly courier-journal (louisville [ky.]) 1874-1917 | https://www.loc.gov/resource/sn84038560/1896-08-03/ed-1/?sp=8 | - |
| `sn85025007_1894-11-12_ed1_sp3.txt` | alexandria gazette (alexandria, d.c.) 1834-1974 | https://www.loc.gov/resource/sn85025007/1894-11-12/ed-1/?sp=3 | - |
| `sn85025007_1894-11-14_ed1_sp2.txt` | alexandria gazette (alexandria, d.c.) 1834-1974 | https://www.loc.gov/resource/sn85025007/1894-11-14/ed-1/?sp=2 | - |
| `sn85025007_1897-12-28_ed1_sp3.txt` | alexandria gazette (alexandria, d.c.) 1834-1974 | https://www.loc.gov/resource/sn85025007/1897-12-28/ed-1/?sp=3 | - |
| `sn85025715_1897-01-29_ed1_sp6.txt` | the norfolk virginian (norfolk, va.) 186?-189? | https://www.loc.gov/resource/sn85025715/1897-01-29/ed-1/?sp=6 | - |
| `sn85026941_1892-07-08_ed1_sp3.txt` | shenandoah herald (woodstock, va.) 1865-1974 | https://www.loc.gov/resource/sn85026941/1892-07-08/ed-1/?sp=3 | - |
| `sn85027015_1822-08-06_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-08-06/ed-1/?sp=4 | - |
| `sn85027015_1822-08-09_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-08-09/ed-1/?sp=4 | - |
| `sn85027015_1822-08-20_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-08-20/ed-1/?sp=4 | - |
| `sn85027015_1822-09-06_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-09-06/ed-1/?sp=4 | - |
| `sn85027015_1822-09-20_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-09-20/ed-1/?sp=3 | - |
| `sn85027015_1822-09-20_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-09-20/ed-1/?sp=4 | - |
| `sn85027015_1822-10-01_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-10-01/ed-1/?sp=4 | - |
| `sn85027015_1822-10-08_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-10-08/ed-1/?sp=1 | - |
| `sn85027015_1822-11-01_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-11-01/ed-1/?sp=4 | - |
| `sn85027015_1822-11-29_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-11-29/ed-1/?sp=3 | - |
| `sn85027015_1822-12-13_ed1_sp2.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1822-12-13/ed-1/?sp=2 | - |
| `sn85027015_1823-01-07_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-01-07/ed-1/?sp=3 | - |
| `sn85027015_1823-01-10_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-01-10/ed-1/?sp=3 | - |
| `sn85027015_1823-01-21_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-01-21/ed-1/?sp=3 | - |
| `sn85027015_1823-01-31_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-01-31/ed-1/?sp=3 | - |
| `sn85027015_1823-02-18_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-02-18/ed-1/?sp=4 | - |
| `sn85027015_1823-02-21_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-02-21/ed-1/?sp=4 | - |
| `sn85027015_1823-02-25_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-02-25/ed-1/?sp=4 | - |
| `sn85027015_1823-02-28_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-02-28/ed-1/?sp=4 | - |
| `sn85027015_1823-03-04_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-03-04/ed-1/?sp=4 | - |
| `sn85027015_1823-03-21_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-03-21/ed-1/?sp=3 | - |
| `sn85027015_1823-03-28_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-03-28/ed-1/?sp=3 | - |
| `sn85027015_1823-04-04_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-04-04/ed-1/?sp=3 | - |
| `sn85027015_1823-04-18_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-04-18/ed-1/?sp=3 | - |
| `sn85027015_1823-05-02_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-02/ed-1/?sp=4 | - |
| `sn85027015_1823-05-09_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-09/ed-1/?sp=4 | - |
| `sn85027015_1823-05-13_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-13/ed-1/?sp=4 | - |
| `sn85027015_1823-05-16_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-16/ed-1/?sp=4 | - |
| `sn85027015_1823-05-23_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-23/ed-1/?sp=4 | - |
| `sn85027015_1823-05-30_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-05-30/ed-1/?sp=4 | - |
| `sn85027015_1823-06-06_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-06-06/ed-1/?sp=1 | - |
| `sn85027015_1823-06-13_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-06-13/ed-1/?sp=3 | - |
| `sn85027015_1823-08-05_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-08-05/ed-1/?sp=4 | - |
| `sn85027015_1823-08-08_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-08-08/ed-1/?sp=3 | - |
| `sn85027015_1823-08-08_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-08-08/ed-1/?sp=4 | - |
| `sn85027015_1823-08-12_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-08-12/ed-1/?sp=4 | - |
| `sn85027015_1823-08-19_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-08-19/ed-1/?sp=4 | - |
| `sn85027015_1823-09-02_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-02/ed-1/?sp=4 | - |
| `sn85027015_1823-09-05_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-05/ed-1/?sp=4 | - |
| `sn85027015_1823-09-08_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-08/ed-1/?sp=1 | - |
| `sn85027015_1823-09-08_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-08/ed-1/?sp=3 | Morriss lodgings Sept 1823 |
| `sn85027015_1823-09-08_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-08/ed-1/?sp=4 | - |
| `sn85027015_1823-09-12_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-12/ed-1/?sp=4 | - |
| `sn85027015_1823-09-16_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-16/ed-1/?sp=4 | - |
| `sn85027015_1823-09-30_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-09-30/ed-1/?sp=4 | Washington notice dated Sept 20, 1823 |
| `sn85027015_1823-10-07_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-07/ed-1/?sp=1 | - |
| `sn85027015_1823-10-10_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-10/ed-1/?sp=4 | Washington notice dated Oct 7, 1823 |
| `sn85027015_1823-10-14_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-14/ed-1/?sp=4 | Washington notice; tavern-house of Robert Morriss |
| `sn85027015_1823-10-17_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-17/ed-1/?sp=3 | - |
| `sn85027015_1823-10-17_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-17/ed-1/?sp=4 | Washington notice |
| `sn85027015_1823-10-24_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-24/ed-1/?sp=1 | - |
| `sn85027015_1823-10-24_ed1_sp3.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-24/ed-1/?sp=3 | - |
| `sn85027015_1823-10-24_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-10-24/ed-1/?sp=4 | Washington notice; tavern-house of Robert Morriss |
| `sn85027015_1823-11-14_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-14/ed-1/?sp=1 | - |
| `sn85027015_1823-11-18_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-18/ed-1/?sp=1 | - |
| `sn85027015_1823-11-18_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-18/ed-1/?sp=4 | - |
| `sn85027015_1823-11-21_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-21/ed-1/?sp=1 | Washington notice |
| `sn85027015_1823-11-21_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-21/ed-1/?sp=4 | - |
| `sn85027015_1823-11-25_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-25/ed-1/?sp=4 | - |
| `sn85027015_1823-11-28_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-11-28/ed-1/?sp=4 | - |
| `sn85027015_1823-12-02_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-12-02/ed-1/?sp=4 | - |
| `sn85027015_1823-12-05_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-12-05/ed-1/?sp=4 | - |
| `sn85027015_1823-12-09_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-12-09/ed-1/?sp=1 | Washington notice; Morriss tavern |
| `sn85027015_1823-12-09_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-12-09/ed-1/?sp=4 | - |
| `sn85027015_1823-12-12_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1823-12-12/ed-1/?sp=4 | Morriss tavern |
| `sn85027015_1824-10-15_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1824-10-15/ed-1/?sp=1 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1825-03-29_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-03-29/ed-1/?sp=4 | - |
| `sn85027015_1825-04-14_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-04-14/ed-1/?sp=4 | tavern of Robert Morriss |
| `sn85027015_1825-04-18_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-04-18/ed-1/?sp=4 | tavern of Robert Morriss |
| `sn85027015_1825-05-26_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-05-26/ed-1/?sp=4 | tavern-house of Robert Morriss |
| `sn85027015_1825-06-13_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-13/ed-1/?sp=1 | - |
| `sn85027015_1825-06-13_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-13/ed-1/?sp=4 | - |
| `sn85027015_1825-06-16_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-16/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1825-06-23_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-23/ed-1/?sp=1 | - |
| `sn85027015_1825-06-23_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-23/ed-1/?sp=4 | Morriss at the Washington Hotel, June 1825 |
| `sn85027015_1825-06-30_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-06-30/ed-1/?sp=1 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1825-07-07_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-07-07/ed-1/?sp=1 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1825-07-11_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-07-11/ed-1/?sp=1 | - |
| `sn85027015_1825-07-14_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1825-07-14/ed-1/?sp=1 | - |
| `sn85027015_1826-01-26_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-01-26/ed-1/?sp=1 | Mr. Morriss' Franklin Hotel |
| `sn85027015_1826-02-13_ed1_sp1.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-02-13/ed-1/?sp=1 | - |
| `sn85027015_1826-02-13_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-02-13/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-03-23_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-03-23/ed-1/?sp=4 | Removal from the Washington to the Franklin (dated Dec 30, 1825) |
| `sn85027015_1826-04-03_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-03/ed-1/?sp=4 | - |
| `sn85027015_1826-04-06_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-06/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-04-13_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-13/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-04-17_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-17/ed-1/?sp=4 | - |
| `sn85027015_1826-04-20_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-20/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-04-24_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-24/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-04-27_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-04-27/ed-1/?sp=4 | Removal notice (dated Dec 30, 1825) |
| `sn85027015_1826-05-08_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-05-08/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85027015_1826-05-11_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-05-11/ed-1/?sp=4 | - |
| `sn85027015_1826-05-22_ed1_sp4.txt` | the virginian (lynchburg [va.]) 1822-1829 | https://www.loc.gov/resource/sn85027015/1826-05-22/ed-1/?sp=4 | Morriss / Franklin Hotel / Washington mention (1826 adverts etc.) |
| `sn85033255_1896-04-23_ed1_sp2.txt` | river falls journal (river falls, pierce county, wis.) 1872-2019 | https://www.loc.gov/resource/sn85033255/1896-04-23/ed-1/?sp=2 | - |
| `sn85034375_1902-03-15_ed1_sp8.txt` | the grenada sentinel (grenada, miss.) 1868-1955 | https://www.loc.gov/resource/sn85034375/1902-03-15/ed-1/?sp=8 | - |
| `sn85034438_1891-05-07_ed1_sp6.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1891-05-07/ed-1/?sp=6 | - |
| `sn85034438_1892-05-01_ed1_sp7.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1892-05-01/ed-1/?sp=7 | - |
| `sn85034438_1892-07-31_ed1_sp8.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1892-07-31/ed-1/?sp=8 | - |
| `sn85034438_1892-11-06_ed1_sp8.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1892-11-06/ed-1/?sp=8 | - |
| `sn85034438_1893-01-10_ed1_sp2.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1893-01-10/ed-1/?sp=2 | - |
| `sn85034438_1895-02-06_ed1_sp6.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1895-02-06/ed-1/?sp=6 | - |
| `sn85034438_1895-03-15_ed1_sp4.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1895-03-15/ed-1/?sp=4 | - |
| `sn85034438_1896-06-30_ed1_sp15.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1896-06-30/ed-1/?sp=15 | - |
| `sn85034438_1896-06-30_ed1_sp21.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1896-06-30/ed-1/?sp=21 | - |
| `sn85034438_1896-11-17_ed1_sp5.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1896-11-17/ed-1/?sp=5 | - |
| `sn85034438_1899-02-15_ed1_sp3.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1899-02-15/ed-1/?sp=3 | - |
| `sn85034438_1899-09-20_ed1_sp3.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1899-09-20/ed-1/?sp=3 | - |
| `sn85034438_1899-12-17_ed1_sp17.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1899-12-17/ed-1/?sp=17 | - |
| `sn85034438_1901-11-15_ed1_sp6.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1901-11-15/ed-1/?sp=6 | - |
| `sn85034438_1902-09-16_ed1_sp8.txt` | the times (richmond, va.) 1890-1903 | https://www.loc.gov/resource/sn85034438/1902-09-16/ed-1/?sp=8 | - |
| `sn85035524_1889-06-08_ed1_sp1.txt` | the penn's grove record (penn's grove, salem co., n.j.) 1878-???? | https://www.loc.gov/resource/sn85035524/1889-06-08/ed-1/?sp=1 | - |
| `sn85038614_1885-04-22_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1885-04-22/ed-1/?sp=1 | - |
| `sn85038614_1889-04-03_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1889-04-03/ed-1/?sp=3 | - |
| `sn85038614_1889-12-13_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1889-12-13/ed-1/?sp=1 | - |
| `sn85038614_1890-11-13_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1890-11-13/ed-1/?sp=3 | - |
| `sn85038614_1891-11-15_ed1_sp9.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1891-11-15/ed-1/?sp=9 | - |
| `sn85038614_1893-04-30_ed1_sp2.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1893-04-30/ed-1/?sp=2 | - |
| `sn85038614_1893-12-29_ed1_sp4.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1893-12-29/ed-1/?sp=4 | - |
| `sn85038614_1894-01-28_ed1_sp8.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1894-01-28/ed-1/?sp=8 | - |
| `sn85038614_1894-05-01_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1894-05-01/ed-1/?sp=1 | - |
| `sn85038614_1894-09-11_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1894-09-11/ed-1/?sp=1 | - |
| `sn85038614_1895-04-07_ed1_sp16.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1895-04-07/ed-1/?sp=16 | - |
| `sn85038614_1895-04-14_ed1_sp16.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1895-04-14/ed-1/?sp=16 | - |
| `sn85038614_1895-08-18_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1895-08-18/ed-1/?sp=3 | - |
| `sn85038614_1895-09-19_ed1_sp5.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1895-09-19/ed-1/?sp=5 | - |
| `sn85038614_1896-06-21_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1896-06-21/ed-1/?sp=1 | - |
| `sn85038614_1896-06-21_ed1_sp7.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1896-06-21/ed-1/?sp=7 | - |
| `sn85038614_1896-07-02_ed1_sp1.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1896-07-02/ed-1/?sp=1 | - |
| `sn85038614_1896-12-02_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1896-12-02/ed-1/?sp=3 | - |
| `sn85038614_1899-01-25_ed1_sp2.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1899-01-25/ed-1/?sp=2 | - |
| `sn85038614_1899-04-20_ed1_sp4.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1899-04-20/ed-1/?sp=4 | - |
| `sn85038614_1899-07-30_ed1_sp7.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1899-07-30/ed-1/?sp=7 | - |
| `sn85038614_1899-11-19_ed1_sp14.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1899-11-19/ed-1/?sp=14 | - |
| `sn85038614_1899-12-31_ed1_sp20.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1899-12-31/ed-1/?sp=20 | - |
| `sn85038614_1901-04-12_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1901-04-12/ed-1/?sp=3 | - |
| `sn85038614_1901-05-08_ed1_sp3.txt` | richmond dispatch (richmond, va.) 1884-1903 | https://www.loc.gov/resource/sn85038614/1901-05-08/ed-1/?sp=3 | - |
| `sn85042354_1891-08-04_ed1_sp2.txt` | evening journal (wilmington, del.) 1888-1932 | https://www.loc.gov/resource/sn85042354/1891-08-04/ed-1/?sp=2 | - |
| `sn85042354_1894-09-29_ed1_sp1.txt` | evening journal (wilmington, del.) 1888-1932 | https://www.loc.gov/resource/sn85042354/1894-09-29/ed-1/?sp=1 | - |
| `sn85042460_1887-07-25_ed1_sp8.txt` | los angeles daily herald (los angeles [calif.]) 1884-1890 [microfilm reel] | https://www.loc.gov/resource/sn85042460/1887-07-25/ed-1/?sp=8 | - |
| `sn85042460_1887-08-06_ed1_sp13.txt` | los angeles daily herald (los angeles [calif.]) 1884-1890 [microfilm reel] | https://www.loc.gov/resource/sn85042460/1887-08-06/ed-1/?sp=13 | - |
| `sn85047084_1886-07-21_ed1_sp1.txt` | the pacific commercial advertiser (honolulu, hawaiian islands) 1885-1921 | https://www.loc.gov/resource/sn85047084/1886-07-21/ed-1/?sp=1 | - |
| `sn85047084_1887-04-14_ed1_sp2.txt` | the pacific commercial advertiser (honolulu, hawaiian islands) 1885-1921 | https://www.loc.gov/resource/sn85047084/1887-04-14/ed-1/?sp=2 | - |
| `sn85054468_1899-04-05_ed1_sp6.txt` | the times (washington [d.c.]) 1897-1901 | https://www.loc.gov/resource/sn85054468/1899-04-05/ed-1/?sp=6 | - |
| `sn85066387_1895-05-03_ed1_sp10.txt` | the san francisco call (san francisco [calif.]) 1895-1913 | https://www.loc.gov/resource/sn85066387/1895-05-03/ed-1/?sp=10 | - |
| `sn86053634_1885-01-07_ed1_sp2.txt` | juniata sentinel and republican (mifflintown, juniata county, pa.) 1873-1955 | https://www.loc.gov/resource/sn86053634/1885-01-07/ed-1/?sp=2 | - |
| `sn86053634_1886-09-01_ed1_sp3.txt` | juniata sentinel and republican (mifflintown, juniata county, pa.) 1873-1955 | https://www.loc.gov/resource/sn86053634/1886-09-01/ed-1/?sp=3 | - |
| `sn86053634_1889-03-06_ed1_sp2.txt` | juniata sentinel and republican (mifflintown, juniata county, pa.) 1873-1955 | https://www.loc.gov/resource/sn86053634/1889-03-06/ed-1/?sp=2 | - |
| `sn86053634_1896-02-26_ed1_sp2.txt` | juniata sentinel and republican (mifflintown, juniata county, pa.) 1873-1955 | https://www.loc.gov/resource/sn86053634/1896-02-26/ed-1/?sp=2 | - |
| `sn86069395_1902-08-01_ed1_sp5.txt` | hopkinsville kentuckian (hopkinsville, ky.) 1889-1918 | https://www.loc.gov/resource/sn86069395/1902-08-01/ed-1/?sp=5 | - |
| `sn86071779_1899-09-16_ed1_sp6.txt` | virginian-pilot (norfolk, va.) 1898-1911 | https://www.loc.gov/resource/sn86071779/1899-09-16/ed-1/?sp=6 | - |
| `sn86071854_1889-09-10_ed1_sp1.txt` | the daily times (richmond, va.) 1886-1889 | https://www.loc.gov/resource/sn86071854/1889-09-10/ed-1/?sp=1 | - |
| `sn86071868_1892-10-02_ed1_sp5.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1892-10-02/ed-1/?sp=5 | - |
| `sn86071868_1893-01-07_ed1_sp2.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1893-01-07/ed-1/?sp=2 | - |
| `sn86071868_1893-01-20_ed1_sp1.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1893-01-20/ed-1/?sp=1 | Beale treasure article |
| `sn86071868_1893-06-01_ed1_sp5.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1893-06-01/ed-1/?sp=5 | - |
| `sn86071868_1893-08-12_ed1_sp2.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1893-08-12/ed-1/?sp=2 | - |
| `sn86071868_1893-11-14_ed1_sp1.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1893-11-14/ed-1/?sp=1 | - |
| `sn86071868_1894-09-12_ed1_sp2.txt` | the roanoke times (roanoke, va.) 1890-1895 | https://www.loc.gov/resource/sn86071868/1894-09-12/ed-1/?sp=2 | - |
| `sn86072173_1889-09-25_ed1_sp1.txt` | the cheyenne daily leader (cheyenne, wyo.) 1887-1895 | https://www.loc.gov/resource/sn86072173/1889-09-25/ed-1/?sp=1 | - |
| `sn86092182_1889-05-25_ed1_sp2.txt` | the new dominion (morgantown, w. va.) 1876-1904 | https://www.loc.gov/resource/sn86092182/1889-05-25/ed-1/?sp=2 | - |
| `sn86092282_1894-10-24_ed1_sp1.txt` | randolph enterprise (beverly, w. va.) 1874-1956 | https://www.loc.gov/resource/sn86092282/1894-10-24/ed-1/?sp=1 | - |
| `sn87060165_1899-08-01_ed1_sp4.txt` | the free lance (fredericksburg, va.) 1885-1926 | https://www.loc.gov/resource/sn87060165/1899-08-01/ed-1/?sp=4 | - |
| `sn87060165_1899-08-26_ed1_sp4.txt` | the free lance (fredericksburg, va.) 1885-1926 | https://www.loc.gov/resource/sn87060165/1899-08-26/ed-1/?sp=4 | - |
| `sn87060165_1900-05-17_ed1_sp1.txt` | the free lance (fredericksburg, va.) 1885-1926 | https://www.loc.gov/resource/sn87060165/1900-05-17/ed-1/?sp=1 | - |
| `sn87068079_1899-08-17_ed1_sp1.txt` | gloucester county democrat (woodbury, n.j.) 1878-1932 | https://www.loc.gov/resource/sn87068079/1899-08-17/ed-1/?sp=1 | - |
| `sn87076917_1887-12-31_ed1_sp1.txt` | springfield daily republic (springfield, o. [ohio]) 1887-1888 | https://www.loc.gov/resource/sn87076917/1887-12-31/ed-1/?sp=1 | - |
| `sn87078000_1892-09-15_ed1_sp3.txt` | the evening herald (shenandoah, pa.) 1891-1966 | https://www.loc.gov/resource/sn87078000/1892-09-15/ed-1/?sp=3 | - |
| `sn88076998_1891-03-06_ed1_sp2.txt` | griggs courier (cooperstown, griggs co., dak. [n.d.]) 1885-1902 | https://www.loc.gov/resource/sn88076998/1891-03-06/ed-1/?sp=2 | - |
| `sn89053987_1891-11-11_ed1_sp6.txt` | the central presbyterian (richmond, va.) 1856-1908 | https://www.loc.gov/resource/sn89053987/1891-11-11/ed-1/?sp=6 | - |
| `sn91070630_1893-04-18_ed1_sp5.txt` | the providence news (providence [r.i.]) 1891-1906 | https://www.loc.gov/resource/sn91070630/1893-04-18/ed-1/?sp=5 | - |
| `sn91070630_1893-10-09_ed1_sp2.txt` | the providence news (providence [r.i.]) 1891-1906 | https://www.loc.gov/resource/sn91070630/1893-10-09/ed-1/?sp=2 | - |
| `sn91070630_1901-05-23_ed1_sp2.txt` | the providence news (providence [r.i.]) 1891-1906 | https://www.loc.gov/resource/sn91070630/1901-05-23/ed-1/?sp=2 | - |
| `sn92051487_1901-06-21_ed1_sp3.txt` | the newtown bee (newtown, conn.) 1877-current | https://www.loc.gov/resource/sn92051487/1901-06-21/ed-1/?sp=3 | - |
| `sn94052989_1890-08-04_ed1_sp1.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1890-08-04/ed-1/?sp=1 | - |
| `sn94052989_1891-01-25_ed1_sp3.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1891-01-25/ed-1/?sp=3 | - |
| `sn94052989_1891-04-03_ed1_sp8.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1891-04-03/ed-1/?sp=8 | - |
| `sn94052989_1891-08-10_ed1_sp3.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1891-08-10/ed-1/?sp=3 | - |
| `sn94052989_1891-11-26_ed1_sp6.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1891-11-26/ed-1/?sp=6 | - |
| `sn94052989_1892-07-15_ed1_sp7.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1892-07-15/ed-1/?sp=7 | - |
| `sn94052989_1892-09-01_ed1_sp3.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1892-09-01/ed-1/?sp=3 | - |
| `sn94052989_1892-11-18_ed1_sp6.txt` | the morning call (san francisco [calif.]) 1878-1895 | https://www.loc.gov/resource/sn94052989/1892-11-18/ed-1/?sp=6 | - |
| `sn97065762_1889-06-22_ed1_sp7.txt` | custer chronicle (custer city, black hills, d.t. [s.d.]) 1880-1890 | https://www.loc.gov/resource/sn97065762/1889-06-22/ed-1/?sp=7 | - |
| `sn98062948_1891-03-05_ed1_sp2.txt` | hand county press (miller, dakota [s.d.]) 1882-1893 | https://www.loc.gov/resource/sn98062948/1891-03-05/ed-1/?sp=2 | - |
