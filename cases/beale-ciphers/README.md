# The Beale ciphers

Working files for one question: are the three pages of numbers printed in the 1885 Lynchburg pamphlet *The Beale Papers*
genuine ciphers or a hoax? The published page is https://historical-mysteries.netlify.app/beale-ciphers/report ;
report.html in this folder is the same page.

## What is in this folder
- data/primary/   Texts parsed from the 1885 pamphlet (Wikisource transcription of the Library of Congress copy,
                  Page:Beale Papers.djvu/1-23): the three ciphers, the Declaration of Independence exactly as the pamphlet
                  prints and numbers it, the printed decipherment of cipher 2, the three "Beale" letters, Morriss's quoted
                  statement, and the anonymous author's narrative.
- sources/        Raw source captures (Wikisource pages, Gillogly 1980 via the Wayback Machine, Wikipedia wikitext, the
                  National Archives Declaration transcript, newspaper page OCR, the archive.org full-text search responses
                  for King 1993 under sources/papers/king_1993_fragments/) and the parser (parse_pamphlet.py).
- sources/scans/  Scan of pamphlet p. 21 (Commons rendering of the LoC copy) with crops used to check cipher-1 readings.
- code/           Analysis code (Python 3, numpy and scipy). Each script runs on its own. make_report_figures.py draws the
                  two figures and the table on the page.
- results/        Machine-readable outputs of every analysis, and the page's two figures and its table as SVG: figure1_offsets.svg,
                  table1_alphabet_strip.svg, figure2_histograms.svg.
- notes/          Working notes with citations, one file per line of inquiry.
- report.html     The published page.

Data note: data/primary/cipher2.txt originally began with a spurious "2" (the parser swept up the
"2," of 'marked "2,"' before the cipher block). The pamphlet prints 762 numbers in cipher 2 (763 after the standard
"108 -> 10, 8" correction). The file and sources/parse_pamphlet.py were fixed, and everything in results/ was computed
from the corrected file.

## Summary for the site
The story. In 1885 a pamphlet was printed in Lynchburg, a town in central Virginia, under the title The Beale Papers.
Its author, who gives no name, says that in 1820 and again in 1822 a stranger called Thomas J. Beale stayed at the
Washington Hotel, kept by the merchant Robert Morriss, and left with Morriss a locked iron box. Opened in 1845, the box
held three pages of numbers and letters telling of thirty Virginians who found gold and silver north of Santa Fe in
1817 and buried it in Bedford County, Virginia. Morriss passed the papers to the author in 1862. Numbering the words
of the Declaration of Independence, the author read the second page (cipher 2): it describes the treasure. Ciphers 1
and 3 have never been read.

Why it is still argued. Cipher 2 is a real cipher with a real message, and no record of Beale, his party or the box
has ever been found. Those who believe the story point to that message and to computer analyses (Carl Hammer, a
computer scientist, 1971) showing that the unread pages are not random numbers. The sceptics' case was made in print by
the cryptanalyst Jim Gillogly (1980: cipher 1 contains the alphabet in order), the investigator Joe Nickell (1982:
Morriss did not keep the hotel before 1823, and the letters and the narrative read like one hand) and the cryptanalyst
John C. King (1993: the exact numbering of the Declaration that decodes cipher 2, and longer alphabetical runs in
cipher 1 under it).

How the case was judged. From the pamphlet's own text: decode cipher 2 with the pamphlet's printed numbering and see
where that numbering goes wrong (it reproduces the encoder's own five miscounts); compute exactly how likely the
alphabet in cipher 1 is by chance; compare the three ciphers as sequences of numbers; measure the letters and the
narrative against 115 samples by 27 American authors; date the letters' vocabulary; and check the story's dates against
the Lynchburg newspapers and the archives of Spanish New Mexico.

Verdict: a hoax, as a composite judgement, about 95 percent. The figure is a judgement rather than a measurement.

Evidence: strong. The evidence leaves little room for another answer. The verdict is still a reading of the documents,
and a new document could change it.

Framing: a replication and extension of the case made in print by the cryptanalysts Gillogly (1980), Matyas (1979),
Holst (1987), Hill (1989) and King (1993), with statistical, stylistic and archival checks added. Not a first discovery
that the ciphers are suspicious.

Confidence by claim:
1. The three alphabetical strings in cipher 1 are deliberate, not chance: beyond reasonable doubt under the models
   tested (P = 4.9e-8 by exact calculation under the most generous model; 0 in 10^6 shuffles of the cipher's own
   numbers). The passage was found by Gillogly (1980); the longer strings under the reconstructed key were reported by
   King (1993) and found independently by Hill (1989).
2. Cipher 1 as printed is not an ordinary book-cipher encipherment: about 99 percent, a judgement. King's "further
   layer" alternative cannot be excluded by statistics, and nothing supports it.
3. The pamphlet's printed key and instructions cannot produce its printed translation, and its numbering matches the
   cipher-2 encoder's count at each of his five miscounts: established by counting, reproducible from the pamphlet's
   text. Whether the narrator had the encoder's key (the simpler reading) or reconstructed the miscounts himself
   (possible in principle) is a judgement.
4. The story is a fiction: about 95 percent, a composite judgement (claims 1 to 3 plus the Morriss hotel dates, the
   Santa Fe record and the language of the letters).
5. The narrator wrote the "Beale" letters: about 90 percent, a judgement. Length-matched likelihood ratios run from
   3 to 25 depending on the measure (2.7 for Burrows Delta, 6.6 for function words, 25 for cosine Delta without
   pronouns and for character 4-grams; the measures are explained in section 4 of the report), which is 73
   to 96 percent with even prior odds; the reflexive-pronoun habit (letters and narrative at six to ten times the
   control rate; one of 115 control samples reaches the lower rate) adds to that.
6. The narrator was J. B. Ward: not established.

What moves the figure: the composite moves with the reading of the printed key (if the narrator reconstructed the
miscounts himself, claim 3 no longer bears on the story and the verdict rests on the alphabet in cipher 1, the Morriss
dates and the Santa Fe record); with the stylometric measure chosen (Burrows Delta alone gives about 73 percent for
common authorship); and with the prior odds, which are a judgement. A reading of cipher 1 that survived the section 3
tests would overturn the verdict on the ciphers.

What is added. New analysis of evidence already in print: the encoder's offsets fitted from the cipher alone and
matched to the pamphlet's printed numbers; the "meantime / inalienable" typesetting argument; the numbering that stops at
816; exact Markov-chain probabilities, permutation and run-count tests, the homophone-rank test; the cipher-2 encoder
model and cipher 3's serial structure; the capacity bound with real Virginia names; calibrated stylometry with likelihood
ratios; the calibrated late-vocabulary density; corrected attestation dates for "stampede" and "improvise". Documents
that Wikipedia and Poundstone's Biggest Secrets (as Wikipedia cites it) do not use: Morriss's own notices in The
Virginian (a notice dated 20 September 1823, printed on 30 September, that he has rented the Washington Hotel to open on
1 October; a removal notice dated 30 December 1825, printed from March 1826), where those accounts had only "not until at
least 1823"; the 1823 Austin Papers "stampeded"; the January 1847 newspaper
uses of "objective point"; the Roanoke Times retelling of 20 January 1893; Nelson's 1972 archive search and Hart's 1964
memoir in the NSA FOIA release. None of this is new primary evidence about Beale himself; it documents the pamphlet's
errors and the words' histories.

How it stands to earlier views: confirms. The verdict agrees with the hoax reading argued in print by the cryptanalysts
Jim Gillogly (1980), John C. King (1993) and Todd Mateer (2013), the investigator Joe Nickell (1982) and the cryptologic
historian Louis Kruh (1982, 1988). That position is not unanimous: the computer scientist Carl Hammer (1971, 1979) and
the Beale Cypher Association, a society of enthusiasts, held the unsolved ciphers to be genuine, and popular accounts treat them as an unsolved
treasure puzzle. The page does not show that the hoax reading is a settled position, only that it is the position of
the cryptanalysts who worked on the ciphers in print.

What could not be checked: King 1993 was read only in fragments (the archive.org full-text search responses are saved
under sources/papers/king_1993_fragments/); Matyas 1979, Holst 1987, Hill 1989, Hammer 1979, Nickell 1982, Kruh
1982/1988, Poundstone 1993 (known through Wikipedia's summary and the Internet Archive's full-text index) and Mateer 2013
were not read; Nickell's findings are known only through Wikipedia's summary; the Lynchburg papers of 1819 to 1821, 1862
to 1865 and 1885 to 1892 are not digitised (the Library of Congress collection holds Lynchburg papers only from 1822 to
the 1850s), so silence there is untested; the
January 1847 "objective point" attestations were not re-verified from the page images; the stylometric likelihood ratio
depends on the measure (3 to 25; 2.7 for Burrows Delta) and on the prior odds; the 95 percent is a judgement.

Figures: the two figures and the table on the page were made for it by code/make_report_figures.py and are saved in
results/ as figure1_offsets.svg, table1_alphabet_strip.svg and figure2_histograms.svg. Figure 1 is drawn from
data/primary/cipher2.txt and data/primary/doi_pamphlet_as_printed.txt; the fitted offsets are in
results/b2_decode_summary.json and the five printed miscounts in results/pamphlet_numbering_anomalies.json. Its points
are the 178 distinct numbers that cipher 2 uses apart from 95, 811 and 1005, each plotted once: cipher 2 has 762
numbers, 181 of them distinct, and those three stand for single letters (u, y, x) rather than for words of the count.
Table 1 (the alphabet inside cipher 1, positions 184 to 210) is drawn from data/primary/cipher1.txt and the same
Declaration file, decoded with the numbering of section 1 of the report; the decodes are in results/gillogly_strings.json.
Figure 2 (the histograms) is drawn from data/primary/cipher1.txt,
cipher2.txt and cipher3.txt: each bar counts the numbers of one cipher that fall in a range of fifty, the ranges
stopping at 1,050 (the first multiple of fifty above 1005, cipher 2's largest number), and one final bar holds every
number above 1,050, which is 18 numbers in cipher 1 (17 distinct values, ten of them above the Declaration's 1,322
words, the largest 2,906) and none in ciphers 2 and 3. No image on the page is reproduced from elsewhere.
