# Cipher 2, the pamphlet's key, and the Gillogly strings — cryptanalysis notes

Line of inquiry: cryptanalysis (B2 decode / encoder errors / Gillogly strings).
Code: `code/b2_key.py`, `code/b2_decode.py`, `code/b2_encoder_behaviour.py`, `code/gillogly_strings.py`,
`code/gillogly_multi_runs.py`, `code/transcription_check.py`, `code/render_tables.py` (all runnable from the case
folder as `python3 code/<script>.py`; fixed seeds). Machine-readable results in `results/`.

## 0. Findings that bear on the verdict

1. **The pamphlet's printed word-numbering is the cipher-2 encoder's numbering.** Decoding B2 with the numbering
   implied by the pamphlet's own parenthetical numbers gives the printed message at **740 of 762** positions. The 22
   failures are not miscounts: 9 × `811` (needed `y`, printed word "fundamentally"), 4 × `1005` (needed `x`, "have"),
   3 × `95` (needed `u`, printed "inalienable" — the encoder's copy read "unalienable") and 6 isolated slips
   (`84→85` twice, `53→54`, `108→10 8`, `440→40`, `96→95`). Every other number decodes correctly — including 138 of the 152 uses of numbers ≥ 250, i.e.
   the part of the key where the printed count is wrong (the other 14 are the 811s, the 1005s and the 440 slip). By contrast a straight count of the pamphlet's own text gets
   **161** letters wrong (21.1 %), the NARA text 139 (18.2 %), Gillogly's Table I 140.
2. **The encoder's miscounts, recovered from the cipher alone, are exactly the five anomalies printed in the pamphlet.**
   A dynamic programme that fits a piecewise-constant offset between cipher numbers and a straight word count (no
   knowledge of the printed markers) finds offsets 0 / +1 / +11 / +10 / +11 / +12 with changes located between numbers
   241–246, 466–485, 505–511, 620–643 and 666–807. The pamphlet prints 11 words between (240) and (250), the label (480)
   twice, 9 words between (500) and (510), 11 between (630) and (640) and 11 between (670) and (680): offsets −1, −11,
   −10, −11, −12 at exactly those places. Two independent counters do not make the same five slips, one of them a whole
   skipped line of ten words. Either the pamphlet's author copied the numbering from the encoder's key, or he
   reverse-engineered the encoder's slips from the cipher and printed them silently as if they were a plain count.
3. **The printed key is nevertheless not self-sufficient, and the pamphlet does not say so.** A reader who does what
   the pamphlet says ("comparing the foregoing numbers with the ... initial letters of the consecutive words") obtains
   "foir miles", "ehcavation", "sih feet", "countf", "jointlf", "thirtf" ... : no word of the Declaration begins with
   x or y, and the printed text has "inalienable". The pamphlet numbers 811–816 word by word — "fundamentally (811) the
   (812) powers (813) of (814) our (815) governments (816)" — and then stops; 811 is the largest number the cipher uses
   apart from `1005`, and it is the number the encoder used for **y**. The author thus printed the key exactly as far as
   the cipher needed it, and the printed plaintext silently supplies the letters the printed key cannot produce
   (Love's "convenient clairvoyance").
4. **Typesetting evidence that the numbers and the text come from different copies.** The numbering counts "mean time"
   as two words (9 printed words carry a step of 10 at (510)) although the pamphlet prints "meantime"; the numbering
   is consistent with "unalienable" at 95 although the pamphlet prints "inalienable". The numbered key was therefore
   not produced by counting the typeset text; the every-tenth-word numbers were transferred from a numbered copy — the
   encoder's working key, or a copy of it.
5. **Cipher 1 under the encoder's key.** With the key that actually decodes B2 (pamphlet numbering, u/x/y as used),
   Gillogly's string at B1 positions 188–207 reads **`ABCDEFGHIIJKLMMNOHPP`**: 17 exact consecutive alphabetic letters,
   not 14. Gillogly's "off-by-one error" at 195 is an artefact of the standard DOI count (the pamphlet's extra "a" at
   155 makes 195 = "changed" = C); only 301→302 (H→O) remains as a slip. Two further alphabetic runs of 11 letters
   appear that are invisible with a standard DOI: positions 44–54 `AAABBCDEFFI` and 84–94 `ABBBCCCCDDE`; they depend
   on numbers (200, 211, 225, 251, 284, 485, 486) that lie in the miscounted ranges. Whoever wrote B1's alphabetic runs
   used the same miscounted key as B2's encoder. (This is the "greater statistical anomaly" King 1993 reports from a
   reconstructed B2 key; we could only read King's abstract.)
6. **How improbable by chance.** Exact Markov-chain calculation for 520 i.i.d. letters with the DOI's initial-letter
   frequencies: P(some non-decreasing run ≥ 14) = 7.2 × 10⁻⁶, ≥ 17: 4.9 × 10⁻⁸; for Gillogly's stricter "+0/+1" model
   (each letter equal to or the successor of the previous) ≥ 14: 6.3 × 10⁻⁸, ≥ 17: 4.0 × 10⁻¹⁰. Gillogly's 1/13¹³
   arithmetic (equiprobable letters) is reproduced (1.2 × 10⁻¹² for n = 520), but the skewed DOI distribution makes his
   14-letter sequence ~20 000 times more likely than that — still negligible. Shuffling B1's own numbers 10⁶ times (or drawing uniform numbers 1..1322) yields a non-decreasing run ≥ 14 in
   4–7 cases per million, and a run ≥ 17 — or a "+0/+1" run ≥ 14 — in none (< 3 × 10⁻⁶); with one off-by-one
   substitution allowed, the 20-letter `ABCDEFGHIIJKLMMNOOPP` was never matched in 2 × 10⁵ shuffles (< 1.5 × 10⁻⁵).
   Three non-decreasing runs ≥ 10 in one sequence (observed under the pamphlet key) never occurred in 200 000
   shuffles (never more than one; < 1.5 × 10⁻⁵).
   Cipher 3 shows nothing of the kind (longest run 7; a random sequence of that length typically has 6–7).
7. **"Lazy hoaxer" signature.** Of the 20 numbers of the string, 6 are the *first* word of the Declaration with that
   initial (human 6, just 120, King 305, laws 42, mankind 58, people 13); 11 of 20 are among the first three. Expected
   under uniform choice among homophones: 0.76 (P(≥ 6) = 2.7 × 10⁻⁵); expected from B1's own numbers (9.0 % of B1's
   in-range numbers are first occurrences): 1.8 (hypergeometric P(≥ 6) = 0.006). The string's mean normalised
   homophone rank is 0.10 — the same habit as the B2 encoder (0.12), lower than B1 overall (0.19), far from 0.5.
   B1 as a whole shares B2's preference for small numbers (44 % of B1 numbers ≤ 100, B2 54 %, key 7.6 %).
8. **Transcription.** The pamphlet prints **762** numbers in cipher 2 (Wikisource, Love/Remington), not 763; 763 arises
   only after the `108 → 10, 8` correction (unmuseum applies it silently). Our `cipher2.txt` carried a spurious leading
   "2" (parser swept up the "2" of 'marked "2,"'); fixed, parser patched, README noted. Gillogly's Table II (as
   transmitted) differs from the pamphlet at five B1 positions; the scan supports our readings at all five. Gillogly's
   statement that B1 "contains 495 numbers" is wrong — his own Tables II and III have 520 entries.

## 1. Transcription cross-checks (Task 5)

Sources compared with `data/primary/cipher{1,2,3}.txt` (parsed from the validated Wikisource transcription of the
Library of Congress copy): Gillogly 1980 Table II (B1); George Love's copy of B2 "from Remington"; unmuseum.org's
transcription (B1, B2, B3; Wayback capture). Script: `code/transcription_check.py` → `results/transcription_check.json`.

| cipher | source | their count | ours | differences (position: ours vs theirs) | scan / verdict |
|---|---|---|---|---|---|
| B1 | Gillogly Table II | 520 | 520 | 260: 324 vs 320; 263: 64 vs 68; 417: 39 vs 36; 462: 868 vs 858; 489: 428 vs 328 | scan p. 21 (sources/scans/) reads 324, 64, 39, 868, 428 = ours; Gillogly's copy (or its 2000 HTML/OCR conversion, which also has "20l", "l01") is wrong at all five |
| B1 | unmuseum | 520 | 520 | none | — |
| B2 | Love/Remington | 762 | 762 | 629: 138 vs 188 (Love himself flags 188 as a typo for 138) | Wikisource and unmuseum read 138 |
| B2 | unmuseum | 763 | 762 | 571: 108 vs "10, 8"; 666: 440 vs 40 | unmuseum silently applies the two standard corrections |
| B3 | unmuseum | 618 | 618 | 92: 154 vs 151 | Wikisource reads 154 (Wikipedia's editors note the same unmuseum error) |

Net: our B1 and B3 agree with the independent unmuseum transcription number for number; our B2 agrees with
Love/Remington except at the one place Love marks as Remington's typo. The four B1 letters that differ between our
decode and Gillogly's Table III (positions 260, 417, 462, 489) are all outside the alphabetic strings.

## 2. The key: the Declaration as the pamphlet prints and numbers it (Task 1)

**Tokenisation.** A word is a maximal run of letters with internal apostrophes ("nature's" = 1 word). Hyphens and
dashes split words: "self-evident" = 2, "fellow-citizens" = 2, "war—in" = 2. This is the pamphlet's own convention
(it prints "self-evident, that (80)", which only works if self/evident are 78/79) and Gillogly's (Table I, 78–80 = S E T).
"&c." does not occur. Alternative hyphen-joined count also produced (`results/key_straight_pamphlet_text.csv`).

Word counts: pamphlet text 1 324 (hyphen-split; 1 322 hyphen-joined); NARA transcript 1 322; Gillogly Table I 1 322.

**(a) Straight count** of the printed text: `results/key_straight_pamphlet_text.csv`.
**(b) Pamphlet numbering** (`results/key_pamphlet_numbering.csv`): the word before "(N)" is N; inside a segment the
words are numbered forward from the previous label and, alternatively, backward from the next label — the two agree
except inside the five anomalous segments, where the cipher decides (section 3). The five anomalies
(`results/pamphlet_numbering_anomalies.json`):

| labels | printed words between them | step | words |
|---|---|---|---|
| (240)…(250) | 11 | 10 | invariably the same object evinces a design to reduce them under |
| (480)…(480) | 10 | 0 | he has refused for a long time after such dissolutions — a whole line numbered as if absent |
| (500)…(510) | 9 | 10 | for their exercise the state remaining in the meantime — "mean time" counted as two words |
| (630)…(640) | 11 | 10 | of peace standing armies without the consent of our legislature he |
| (670)…(680) | 11 | 10 | unacknowledged by our laws giving his assent to their acts of |

Resulting offsets between the pamphlet's number n and the position of the same word in other counts:

| pamphlet numbers n | straight position in pamphlet text | NARA position | note |
|---|---|---|---|
| 1–154 | n | n | |
| 155 ("a") | 155 | — | the pamphlet's extra "a" ("institute a new government") |
| 156–249 | n | n − 1 | |
| 250–480 | n + 1 | n | from "under (250)"; second "(480)" = "dissolutions" |
| 481–508 | n + 11 | n + 10 | from "to cause others" |
| 509, 510 | (printed "meantime" carries 510) | 519, 520 ("mean", "time") | |
| 511–639 | n + 10 | n + 10 | |
| 640–679 | n + 11 | n + 11 | |
| 680–816 | n + 12 | n + 12 | "valuable" = 807 (straight 819), "fundamentally" = 811 (823) |
| > 816 | continued forward: n + 12 | (NARA drifts by the wording differences below) | the pamphlet stops numbering |

**Wording, pamphlet vs NARA** (`results/doi_pamphlet_vs_nara_wording.csv`): 28 differences. Those that change an
initial letter: 95 inalienable/unalienable (I/U), 210 now/more (N/M), 549 of/for (O/F), 653 offered/affected (O/A),
825 powers/forms (P/F). Those that change the count: extra "a" (155), "meantime" for "mean time" (520), "and" for "&"
(909), extra "made" (1070), missing "of" before "consanguinity" (1138), extra "the" (1200). The rest are spelling or
same-initial substitutions (their/these 111, when/whenever 129, shown/shewn, their/the 415, depositary/depository,
danger/dangers, endeavored, migration/migrations, harass, legislature/legislatures, neighboring, in/into 808,
complete/compleat, endeavored 970, attention/attentions, british/brittish, connection/connections). Love's statement
that the pamphlet's Declaration matches the standard text except for "inalienable", the spurious "a" and one late "of"
is therefore incomplete.

**Gillogly's Table I** (`results/key_comparison_vs_gillogly_table1.csv`, `results/key_comparison_summary.json`) is the
NARA text counted with "mean time" as one word (his numbers 520–908 are one less than NARA's for the same word) and
"&" counted as a word "and" (agreement resumes at 909), with `994 = X` where the text has "sexes" (i.e. his key had
already been doctored for the x), and isolated differences at 920 (I for "the"), 1300 (I for "a"), 1308 (M for
"Providence") that look like transcription errors. Against the pamphlet numbering, Gillogly's initials agree for
1–94 and 96–154; from 155 to 250 the pamphlet is one word ahead (the extra "a"); from 251 to 470 they agree again;
from 481 on the pamphlet is 10–12 words behind (table above). So the two keys used in the literature (Hammer/Gillogly:
a standard DOI; Love/Mateer/this note: the pamphlet's numbering) differ for 22 distinct B2 numbers between 156 and 250
(68 uses) and for every number above 480 (77 uses).

## 3. Decoding cipher 2 (Task 2)

Script `code/b2_decode.py`. The decoded stream (762 letters) is aligned to the consensus reading of the message
(763 letters, since the printed "108" stands for "10, 8") by Needleman–Wunsch; every position whose key letter is
not the aligned letter is listed (`results/b2_disagreements_<key>.csv`).

| key | correct | wrong | wrong % |
|---|---|---|---|
| pamphlet numbering, anomalous gaps resolved by the cipher | 740 | 22 | 2.9 |
| pamphlet numbering, forward (or backward) count inside gaps | 735 | 27 | 3.5 |
| straight count of the pamphlet's printed text | 601 | 161 | 21.1 |
| NARA transcript, straight count | 623 | 139 | 18.2 |
| Gillogly 1980 Table I | 622 | 140 | 18.4 |

**The 22 disagreements under the pamphlet numbering** (position in the 762-number cipher; expected letter from the message):

| pos | number | key word (letter) | needed | plaintext context | class |
|---|---|---|---|---|---|
| 25, 149, 268, 364, 441, 563, 609, 714, 742 | 811 | fundamentally (f) | y | count**y**, jointl**y**, thirt**y**, twent**y**, eight**y**, securel**y**, roughl**y**, localit**y**, difficult**y** | systematic: no y-initial word exists; 811 used as y (last letter of "fundamentally") |
| 65, 83, 485, 703 | 1005 | have (h) | x | e**x**cavation, si**x**, e**x**change, e**x**act | systematic: no x-initial word; 1005 is beyond the printed numbering and is not an x-containing word under any count (sexes = 983/995, extend = 1063/1075) |
| 42, 292, 559 | 95 | inalienable (i) | u | fo**u**r, po**u**nds, sec**u**rely | systematic: encoder's copy read "unalienable" (NARA); the 96→95 slip at 722 also needs u |
| 223, 701 | 84 | created (c) | e | consist**e**d, th**e** exact | slip: 85 = equal |
| 531 | 53 | respect (r) | t | **t**housand | slip: 54 = to |
| 571 | 108 | that (t) | n i | packed i**n i**ron | slip: "10, 8" (necessary, it) printed as 108 |
| 666 | 440 | uncomfortable (u) | w | **w**ith others | slip: 40 = which (dropped digit) |
| 722 | 96 | rights (r) | u | va**u**lt | slip: 95 = unalienable |

The six slips are exactly the six "errors" listed on Wikipedia; all are adjacent-number or typesetting errors, none is a
miscount. Wikipedia's blockquote "packed in clay pots" is wrong: 2 10 8 220 106 353 = i n i r o n.

**Resolution of the anomalous gaps by the cipher** (`b2_decode_summary.json: ambiguous_gap_numbers`): 241 = invariably
(i, forward count), 246 = design (d, backward), 248 = reduce (r, backward), 250 = under (u), 485 = be (b, backward),
486 = elected (e, backward), 505 = state (s, forward), 511 = exposed. Hence the skipped word of the (240)–(250) segment
is one of "the same object evinces a" (Wikipedia's "probably a" is one of five possibilities); the whole line
"he has refused … dissolutions" is bracketed by 466 (houses, +1) and 485 (be, +11), no number 467–484 being used; the
"mean time" extra count lies between 505 and 511.

**Offset segmentation recovered from the cipher alone** (`b2_decode_summary.json: offset_segmentation`; DP over the
181 distinct numbers with a penalty λ per offset change and one unit per unexplained use):

| cipher numbers | encoder's number n = straight word | pamphlet label offset |
|---|---|---|
| 1–241 | n | 0 |
| 246–466 | n + 1 | −1 from (250) |
| 485–505 | n + 11 | −11 from second (480) |
| 511–620 | n + 10 | −10 from (510) |
| 643–666 | n + 11 | −11 from (640) |
| 807–1005 | n + 12 | −12 from (680) |

Unexplained by any constant offset: 95 (u), 108, 440, 811 (y), 1005 (x) — plus the minority uses 84→e, 53→t, 96→u.
The six segments are found for λ = 1, 2, 3; at λ = 5 the short 485–505 segment is absorbed, at λ ≥ 8 four segments
remain. Numbers ≥ 250 (152 uses, 53 distinct, 20.0 % of the cipher) decode differently under the pamphlet numbering
than under a straight count; Love's "at least 134 (19.9 %)" is the same phenomenon counted slightly differently.

**Printed plaintext versus the message the cipher spells** (`results/b2_printed_vs_decoded_plaintext.csv`): the
pamphlet's "translation" has 732 letters + 15 digits, not a letter-for-letter transcript. Differences: "3" for three;
"one thousand" for ten hundred; "three thousand" for thirty; "November, 1819" for nov eighteen nineteen;
"December, 1821" for dec eighteen twenty one; "pounds of silver" inserted after eighty-eight; "for silver" inserted
after exchange; "$13,000" for thirteen thousand dollars; "1" for one (Buford's/bufords is only an apostrophe). Nine
substantive differences, as Wikipedia says; all are editorial.

**Was the printed key "fixed up"?** Yes in the sense that matters: the numbers printed every ten words are the
encoder's numbers, not a count of the printed text — five slips, including a skipped line, reproduced exactly, and
the cipher decodes at 740/762 with them versus 601/762 with an honest count of the very same printed text. It was not
fixed up completely: u, x, y and six slips are left to the reader, and the pamphlet's narrative does not mention that
the "consecutive words" must be counted with the errors. What each reading implies:
* If the pamphlet's author solved B2 without the key (as the narrative says), he had to discover the miscounts
  himself — feasible, since the message is redundant — but he then printed the miscounted numbering as if it were a
  plain count, said nothing about it, and typeset a Declaration text ("inalienable", "meantime") that his own numbers
  do not fit. That is a strange thing for a solver to do and an unremarkable thing for someone copying numbers from
  the encoder's working key.
* If the author had the encoder's key, the narrative's central claim (the key never arrived; the Declaration was
  found by trial) is false; and since B2 was written with that key, the simplest account is that the author wrote
  B2 — Love's conclusion, and (from the abstract) Mateer's. Section 5 adds that B1's alphabetic runs were written
  with the same miscounted key.

**Literature checks.** Wikipedia's five "modifications" and six errors: confirmed. Hammer's "23 errors" (known to us
only through Gillogly's sentence "Hammer noted 23 examples where the person who encrypted B2 made errors of this type
[choosing an adjacent number]"): with a standard DOI, the 22 distinct numbers used in 156–250 (68 uses) are each off by
one word, and with the pamphlet numbering there are exactly 22 wrong letters; we cannot see Hammer's list, so we only
note that both counts land near 23. Gillogly: "495 numbers" is wrong (520). Love: the three-point textual comparison
is incomplete (28 differences); his main claim ("No. 2 works if, and only if, the pamphlet Declaration word counts are
used") is confirmed quantitatively.

## 4. Behaviour of the cipher-2 encoder (Task 3)

Script `code/b2_encoder_behaviour.py`; corrected cipher (six slips repaired, 763 numbers, one per letter) in
`results/b2_corrected_cipher.txt`; full tables in `results/b2_encoder_behaviour.{json,md}`. Key = pamphlet numbering
as resolved, 95 = unalienable, 811 = y, 1005 = x. Rank = position of the chosen word among all key words with that
initial (rank 1 = first such word in the Declaration); normalised rank = (rank − ½)/H, 0.5 for uniform choice.

| letter | uses | distinct nos. | homophones | first word (n) | uses of first word | most used n (count, rank) | mean rank | mean norm. rank | top-3 share | max n |
|---|---|---|---|---|---|---|---|---|---|---|
| a | 43 | 15 | 166 | another (24) | 4 | 150 (6, r18) | 11.3 | 0.07 | 0.35 | 284 |
| b | 11 | 7 | 48 | becomes (9) | 1 | 77 (4, r3) | 4.7 | 0.09 | 0.64 | 485 |
| c | 17 | 7 | 52 | course (4) | 3 | 84 (5, r4) | 3.9 | 0.07 | 0.59 | 200 |
| d | 49 | 11 | 37 | dissolve (15) | 8 | 63 (11, r3) | 4.8 | 0.12 | 0.59 | 582 |
| e | 105 | 14 | 36 | events (7) | 15 | 7 (15, r1) | 7.1 | 0.18 | 0.41 | 620 |
| f | 21 | 8 | 61 | for (11) | 1 | 122 (6, r2) | 5.3 | 0.08 | 0.67 | 666 |
| g | 15 | 4 | 19 | god (48) | 6 | 48 (6, r1) | 2.9 | 0.13 | 0.93 | 270 |
| h | 37 | 8 | 78 | human (6) | 4 | 20 (9, r2) | 4.6 | 0.05 | 0.65 | 466 |
| i | 55 | 12 | 68 | in (2) | 7 | 140 (15, r6) | 6.0 | 0.08 | 0.62 | 647 |
| j | 2 | 2 | 10 | just (120) | 1 | 120 (1, r1) | 2.5 | 0.20 | 1.00 | 581 |
| k | 1 | 1 | 4 | king (305) | 1 | 305 (1, r1) | 1.0 | 0.12 | 1.00 | 305 |
| l | 32 | 10 | 32 | laws (42) | 5 | 102 (7, r3) | 5.4 | 0.15 | 0.56 | 420 |
| m | 6 | 4 | 29 | mankind (58) | 1 | 117 (2, r3) | 3.2 | 0.09 | 0.83 | 208 |
| n | 69 | 8 | 20 | necessary (10) | 13 | 10 (13, r1) | 5.7 | 0.26 | 0.56 | 607 |
| o | 63 | 12 | 144 | of (5) | 4 | 106 (15, r8) | 6.5 | 0.04 | 0.49 | 302 |
| p | 12 | 4 | 61 | people (13) | 0 | 30 (5, r3) | 3.6 | 0.05 | 0.92 | 121 |
| r | 38 | 7 | 42 | respect (53) | 8 | 53 (8, r1) | 3.9 | 0.08 | 0.60 | 344 |
| s | 48 | 12 | 63 | separate (35) | 6 | 110 (11, r6) | 8.3 | 0.12 | 0.54 | 600 |
| t | 70 | 18 | 251 | the (3) | 5 | 16 (9, r3) | 12.8 | 0.05 | 0.31 | 643 |
| u | 25 | 8 | 28 | unalienable (95) | 4 | 250 (6, r3) | 3.6 | 0.11 | 0.60 | 440 |
| v | 18 | 1 | 2 | valuable (807) | 18 | 807 (18, r1) | 1.0 | 0.25 | 1.00 | 807 |
| w | 13 | 6 | 58 | when (1) | 1 | 40 (5, r4) | 4.6 | 0.07 | 0.69 | 290 |
| x | 4 | 1 | — | (1005) | 4 | 1005 | — | — | 1.00 | 1005 |
| y | 9 | 1 | — | (811) | 9 | 811 | — | — | 1.00 | 811 |

Global: 763 letters, 181 distinct numbers, reuse rate 0.76; mean normalised rank **0.123 ± 0.005** (uniform: 0.5;
Kolmogorov–Smirnov D = 0.61, p ≈ 10⁻²⁷⁷); 82.8 % of choices lie in the first quarter of the homophone list, 0 % in the
last quarter; rank histogram 1: 129, 2: 114, 3: 108, 4–5: 106, 6–10: 191, > 10: 115. Only **16.9 %** of uses are the
first word with that initial (uniform expectation 5 %): the encoder worked from the front of the numbered
Declaration but did not fixate on the first occurrence; the most-used number for a letter is typically rank 1–3, and
no number above 811 is used except the x. 53.5 % of uses are numbers ≤ 100 (7.6 % of key words), 81 % ≤ 250, 90 % ≤ 500.
The 19 doubled letters of the message (ee, ll, nn, tt, dd, ss, ff) **never** reuse the same number; 36 of 763 uses
repeat a number seen within the previous ten. v is always 807 (2 homophones), x always 1005, y always 811.

## 5. The Gillogly strings (Task 4)

Scripts `code/gillogly_strings.py` (seed 20260914; 10⁶ exact-letter simulations, 2 × 10⁵ for the substitution
statistics) and `code/gillogly_multi_runs.py`; results `results/gillogly_strings.json`, `results/gillogly_runs.csv`,
`results/b1_b3_decodes.csv`, `results/gillogly_multi_runs.json`, tables `results/gillogly_pvalues.md`.

**Reproduction.** Decoding Gillogly's own Table II with his Table I reproduces his Table III letter for letter (0 of
520 mismatches; his "20l"/"l01" read as 201/101). With our B1 numbers, 4 letters differ (positions 260, 417, 462,
489; section 1). The string `ABFDEFGHIIJKLMMNOHPP` sits at positions 188–207 (numbers 147 436 195 320 37 122 113 6 140
8 120 305 42 58 461 44 106 301 13 408). Off-by-one claims: under Gillogly's/NARA's count 194 = C (changed), 195 = F
(for), 301 = H (history), 302 = O (of) — as he says. Under the pamphlet numbering 194 = B (be), **195 = C (changed)**,
301 = H, 302 = O. Keys: Gillogly 1 322 words, NARA 1 322, pamphlet numbering 1 312, pamphlet straight 1 324; B1 has 10
numbers above 1 322 (1431 1496 1629 1701 1706 1780 1817 2018 2160 2906) and 1317, which is beyond the pamphlet key.

**Alphabetic runs** (non-decreasing, exact letters; "+0/+1" = each letter equal to or the successor of the previous):

| cipher / key | longest non-decr. | longest +0/+1 | runs ≥ 8 | runs ≥ 5 | with ≤ 1 substitution (n ± 1) | with ≤ 2 substitutions |
|---|---|---|---|---|---|---|
| B1 / Gillogly Table I | 14 `DEFGHIIJKLMMNO` (191–204) | 14 | 1 | 13 | 17 `ABCDEFGHIIJKLMMNO` (195→194) | 20 `ABCDEFGHIIJKLMMNOOPP` |
| B1 / NARA | 14 | 14 | 1 | 11 | 17 | 20 |
| B1 / pamphlet (encoder's) key | **17** `ABCDEFGHIIJKLMMNO` (188–204) | 17 | **3** (44–54 `AAABBCDEFFI`, 84–94 `ABBBCCCCDDE`, 188–204) | 9 | 20 `ABCDEFGHIIJKLMMNOOPP` (301→302) | 22 |
| B1 / pamphlet straight count | 8 `EFGHIIJP` | 7 | 1 | 6 | 10 | 14 |
| B3 / any of the keys | 7 `ACCSTTT` (150–156) | 4 | 0 | 10–13 | 8 | 9 |

Under a straight count of the pamphlet's printed text (no miscounts) the string collapses to 8 letters: the runs live
specifically in the miscounted numbering, not in the Declaration as such. Under Gillogly's key the same positions read
`AAABWCTLTFI` (231, 211, 486 and 225 change meaning) and `AABBCCACDDE` (485 and 200 change meaning), i.e. the two
extra runs are broken by exactly the numbers whose meaning the pamphlet's miscounts change.

**Probability tables** (generated by `code/render_tables.py` into `results/gillogly_pvalues.md`).

Simulations: 1,000,000 exact-letter shuffles/draws, 200,000 for the substitution statistics; seed 20260914.

#### (i) i.i.d. letters drawn from the DOI-initial distribution: exact probabilities (n = 520)

| key (letter distribution) | statistic | L=10 | L=12 | L=14 | L=17 | L=20 |
|---|---|---|---|---|---|---|
| gillogly_table1 | nondecreasing, no breaks | 4.54e-03 | 1.85e-04 | 7.18e-06 | 5.27e-08 | 3.79e-10 |
| gillogly_table1 | nondecreasing, with B1 break fraction 0.019 | 3.76e-03 | 1.47e-04 | 5.50e-06 | 3.81e-08 | 2.58e-10 |
| gillogly_table1 | step01, no breaks | 4.68e-05 | 1.71e-06 | 6.31e-08 | 4.49e-10 | 3.20e-12 |
| gillogly_table1 | step01, with B1 break fraction 0.019 | 3.87e-05 | 1.36e-06 | 4.83e-08 | 3.24e-10 | 2.18e-12 |
| pamphlet_encoder_key | nondecreasing, no breaks | 4.43e-03 | 1.79e-04 | 6.85e-06 | 4.91e-08 | 3.45e-10 |
| pamphlet_encoder_key | nondecreasing, with B1 break fraction 0.021 | 3.60e-03 | 1.39e-04 | 5.10e-06 | 3.43e-08 | 2.26e-10 |
| pamphlet_encoder_key | step01, no breaks | 4.40e-05 | 1.58e-06 | 5.73e-08 | 3.98e-10 | 2.76e-12 |
| pamphlet_encoder_key | step01, with B1 break fraction 0.021 | 3.57e-05 | 1.23e-06 | 4.27e-08 | 2.78e-10 | 1.81e-12 |

Uniform-26-letter model (Gillogly's arithmetic): P(+0/+1 run >= 14 in 520) = 1.16e-12, >= 17: 4.85e-16, >= 20: 2.01e-19; non-decreasing >= 14: 1.06e-07; Gillogly's 495/13^13 = 1.63e-12.

Expected number of maximal non-decreasing runs of length >= L (i.i.d. DOI letters, Gillogly distribution): L>=5: 9.9, L>=8: 0.129, L>=10: 0.0057, L>=12: 0.000231, L>=14: 8.92e-06, L>=17: 6.53e-08

#### Monte-Carlo p-values for B1 (P of a run at least as long as observed; MC standard error; count/N)

| null model | key | statistic | observed | P(>= observed) | P(>= 14) | P(>= 17) | P(>= 20) |
|---|---|---|---|---|---|---|---|
| (i) i.i.d. letters (B1 breaks) | gillogly_table1 | nondecreasing | 14 | 8.00e-06 ± 2.8e-06 (8/1,000,000) | 8.00e-06 ± 2.8e-06 (8/1,000,000) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (i) i.i.d. letters (B1 breaks) | gillogly_table1 | step01 | 14 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (i) i.i.d. letters (B1 breaks) | pamphlet_encoder_key | nondecreasing | 17 | 0/1,000,000 (<3.0e-06) | 4.00e-06 ± 2.0e-06 (4/1,000,000) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (i) i.i.d. letters (B1 breaks) | pamphlet_encoder_key | step01 | 17 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (ii) permutation of B1 numbers | gillogly_table1 | S1_longest_nondecreasing_exact | 14 | 4.00e-06 ± 2.0e-06 (4/1,000,000) | 4.00e-06 ± 2.0e-06 (4/1,000,000) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (ii) permutation of B1 numbers | gillogly_table1 | S2_longest_step01_exact | 14 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (ii) permutation of B1 numbers | gillogly_table1 | S3_nondecreasing_le2_subs | 20 | 0/200,000 (<1.5e-05) | 8.55e-04 ± 6.5e-05 (171/200,000) | 1.50e-05 ± 8.7e-06 (3/200,000) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | gillogly_table1 | S4_nondecreasing_unlimited_subs | 22 | 5.81e-03 ± 1.7e-04 (1163/200,000) | 5.49e-01 ± 1.1e-03 (109871/200,000) | 1.19e-01 ± 7.2e-04 (23806/200,000) | 1.99e-02 ± 3.1e-04 (3990/200,000) |
| (ii) permutation of B1 numbers | gillogly_table1 | S5_step01_le2_subs | 20 | 0/200,000 (<1.5e-05) | 1.50e-05 ± 8.7e-06 (3/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | gillogly_table1 | S6_nondecreasing_le1_sub | 17 | 0/200,000 (<1.5e-05) | 7.50e-05 ± 1.9e-05 (15/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | gillogly_table1 | S7_step01_le1_sub | 17 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S1_longest_nondecreasing_exact | 17 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S2_longest_step01_exact | 17 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S3_nondecreasing_le2_subs | 22 | 0/200,000 (<1.5e-05) | 7.95e-04 ± 6.3e-05 (159/200,000) | 1.50e-05 ± 8.7e-06 (3/200,000) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S4_nondecreasing_unlimited_subs | 22 | 4.42e-03 ± 1.5e-04 (884/200,000) | 4.96e-01 ± 1.1e-03 (99289/200,000) | 9.82e-02 ± 6.7e-04 (19648/200,000) | 1.49e-02 ± 2.7e-04 (2982/200,000) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S5_step01_le2_subs | 21 | 0/200,000 (<1.5e-05) | 1.50e-05 ± 8.7e-06 (3/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S6_nondecreasing_le1_sub | 20 | 0/200,000 (<1.5e-05) | 6.00e-05 ± 1.7e-05 (12/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (ii) permutation of B1 numbers | pamphlet_encoder_key | S7_step01_le1_sub | 20 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | gillogly_table1 | S1_longest_nondecreasing_exact | 14 | 7.00e-06 ± 2.6e-06 (7/1,000,000) | 7.00e-06 ± 2.6e-06 (7/1,000,000) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (iii) uniform numbers 1..key | gillogly_table1 | S2_longest_step01_exact | 14 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (iii) uniform numbers 1..key | gillogly_table1 | S3_nondecreasing_le2_subs | 20 | 0/200,000 (<1.5e-05) | 1.36e-03 ± 8.2e-05 (272/200,000) | 2.00e-05 ± 1.0e-05 (4/200,000) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | gillogly_table1 | S4_nondecreasing_unlimited_subs | 22 | 2.71e-03 ± 1.2e-04 (542/200,000) | 4.67e-01 ± 1.1e-03 (93387/200,000) | 7.76e-02 ± 6.0e-04 (15512/200,000) | 1.01e-02 ± 2.2e-04 (2020/200,000) |
| (iii) uniform numbers 1..key | gillogly_table1 | S5_step01_le2_subs | 20 | 0/200,000 (<1.5e-05) | 1.00e-05 ± 7.1e-06 (2/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | gillogly_table1 | S6_nondecreasing_le1_sub | 17 | 0/200,000 (<1.5e-05) | 1.40e-04 ± 2.6e-05 (28/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | gillogly_table1 | S7_step01_le1_sub | 17 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S1_longest_nondecreasing_exact | 17 | 0/1,000,000 (<3.0e-06) | 7.00e-06 ± 2.6e-06 (7/1,000,000) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S2_longest_step01_exact | 17 | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) | 0/1,000,000 (<3.0e-06) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S3_nondecreasing_le2_subs | 22 | 0/200,000 (<1.5e-05) | 1.29e-03 ± 8.0e-05 (259/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S4_nondecreasing_unlimited_subs | 22 | 2.17e-03 ± 1.0e-04 (435/200,000) | 4.49e-01 ± 1.1e-03 (89885/200,000) | 7.14e-02 ± 5.8e-04 (14289/200,000) | 9.35e-03 ± 2.2e-04 (1870/200,000) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S5_step01_le2_subs | 21 | 0/200,000 (<1.5e-05) | 2.00e-05 ± 1.0e-05 (4/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S6_nondecreasing_le1_sub | 20 | 0/200,000 (<1.5e-05) | 1.25e-04 ± 2.5e-05 (25/200,000) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| (iii) uniform numbers 1..key | pamphlet_encoder_key | S7_step01_le1_sub | 20 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |

#### Number of long runs in B1 (supplement, code/gillogly_multi_runs.py; 200,000 simulations)

| key | relation | L | observed # runs >= L | P(>= observed), permutation | P(>= observed), uniform numbers |
|---|---|---|---|---|---|
| gillogly_table1 | nondecreasing | 8 | 1 | 8.05e-02 ± 6.1e-04 (16091/200,000) | 9.70e-02 ± 6.6e-04 (19406/200,000) |
| gillogly_table1 | nondecreasing | 10 | 1 | 3.31e-03 ± 1.3e-04 (661/200,000) | 4.49e-03 ± 1.5e-04 (897/200,000) |
| gillogly_table1 | nondecreasing | 11 | 1 | 5.40e-04 ± 5.2e-05 (108/200,000) | 8.90e-04 ± 6.7e-05 (178/200,000) |
| gillogly_table1 | step01 | 8 | 1 | 6.85e-04 ± 5.9e-05 (137/200,000) | 1.48e-03 ± 8.6e-05 (297/200,000) |
| gillogly_table1 | step01 | 10 | 1 | 2.50e-05 ± 1.1e-05 (5/200,000) | 5.50e-05 ± 1.7e-05 (11/200,000) |
| pamphlet_encoder_key | nondecreasing | 8 | 3 | 5.00e-05 ± 1.6e-05 (10/200,000) | 1.60e-04 ± 2.8e-05 (32/200,000) |
| pamphlet_encoder_key | nondecreasing | 10 | 3 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| pamphlet_encoder_key | nondecreasing | 11 | 3 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| pamphlet_encoder_key | step01 | 8 | 3 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |
| pamphlet_encoder_key | step01 | 10 | 3 | 0/200,000 (<1.5e-05) | 0/200,000 (<1.5e-05) |

**Gillogly's arithmetic.** His model (26 equiprobable letters, each next letter equal to or one after the previous)
gives 495/13¹³ = 1.6 × 10⁻¹²; the exact value for n = 520 is 1.2 × 10⁻¹². With the real initial-letter frequencies of
the Declaration (T 19 %, A 12 %, O 11 %, …) the same "+0/+1" 14-run has probability 6.3 × 10⁻⁸ (2 × 10⁴ times larger —
the unevenness does not "offset" as he supposed, it helps), and the looser non-decreasing 14-run 7.2 × 10⁻⁶. His
qualitative conclusion survives by a wide margin: the 17-letter exact run under the encoder's key is at 5 × 10⁻⁸
(non-decreasing) or 4 × 10⁻¹⁰ (+0/+1), and three runs ≥ 10 in one 520-letter sequence never occurred in 2 × 10⁵
shuffles.

**Lazy-hoaxer ranks** (pamphlet key; Gillogly's key gives the same ranks except 195):

| pos | n | letter | word | rank / homophones | first word with this initial |
|---|---|---|---|---|---|
| 188 | 147 | A | alter | 17 / 166 | another (24) |
| 189 | 436 | B | bodies | 13 / 48 | becomes (9) |
| 190 | 195 | C | changed | 8 / 52 | course (4) |
| 191 | 320 | D | direct | 12 / 37 | dissolve (15) |
| 192 | 37 | E | equal | 3 / 36 | events (7) |
| 193 | 122 | F | from | 2 / 61 | for (11) |
| 194 | 113 | G | governments | 2 / 19 | god (48) |
| 195 | 6 | H | human | **1** / 78 | |
| 196 | 140 | I | is | 6 / 68 | in (2) |
| 197 | 8 | I | it | 2 / 68 | |
| 198 | 120 | J | just | **1** / 10 | |
| 199 | 305 | K | king | **1** / 4 | |
| 200 | 42 | L | laws | **1** / 32 | |
| 201 | 58 | M | mankind | **1** / 29 | |
| 202 | 461 | M | measures | 7 / 29 | |
| 203 | 44 | N | nature | 2 / 20 | necessary (10) |
| 204 | 106 | O | of | 8 / 144 | of (5) |
| 205 | 301 | H | history | 8 / 78 | (302 = of, O) |
| 206 | 13 | P | people | **1** / 61 | |
| 207 | 408 | P | people | 19 / 61 | |

6 of 20 first occurrences (uniform expectation 0.76; P(≥ 6) = 2.7 × 10⁻⁵), 11 of 20 within the first three; mean
normalised rank 0.103. Reference points: B2 encoder 0.123 (16.9 % first occurrences); all 509 in-range B1 numbers
0.186 (9.0 % first occurrences; P(≥ 6 of 20) = 0.006 hypergeometric; P(mean ≤ 0.103 for a random 20-subset) = 0.023);
uniform choice 0.5. The person who wrote the run picked, for each successive letter, a word from the front of the
numbered Declaration — the B2 encoder's habit, slightly exaggerated.

## 6. What is new versus Hammer 1979 / Gillogly 1980 / King 1993 / Mateer 2013 / Love

Confirms: Gillogly's Table III and string (reproduced exactly); the five "modifications" and six errors listed on
Wikipedia; Love's claim that B2 works if and only if the pamphlet's word counts are used; King's abstract claim that the
reconstructed B2 key reveals greater anomalies in B1 than Gillogly reported; Mateer's abstract conclusion (hoax). Goes
beyond them, as far as we can tell from what is accessible: (1) the encoder's offsets are recovered algorithmically
from the cipher alone and shown to coincide segment by segment with the pamphlet's printed anomalies, with the
within-segment ambiguities resolved by the cipher (which word was skipped is not determinable, contrary to Wikipedia's
"probably a"); (2) the typesetting argument (numbering counts "mean time" as two words and needs "unalienable"; the
print has "meantime" and "inalienable"), which shows the numbers were transferred from a copy other than the typeset
one; (3) the exact (Markov-chain) probabilities for the real letter distribution under both run definitions, and
permutation tests preserving B1's number multiset, with and without off-by-one substitutions, in place of Gillogly's
equiprobable back-of-envelope; (4) the specific statement that the 195 "error" disappears under the encoder's key
(17 exact letters), that two more 11-letter runs appear, and a test of the number of long runs; (5) the homophone-rank
("lazy hoaxer") test and its comparison with the B2 encoder's habits and with B1's own numbers; (6) quantification of
the B2 encoder's habits (first-quartile preference 83 %, first-occurrence share 17 %, no number reused on doubled
letters); (7) the 762-number count of the printed B2 and the corrected reading of Gillogly's B1 count (520, not 495).
Hammer 1979 is inaccessible to us (paywalled; only its title, DOI and Gillogly's paraphrase), so overlap with (6) cannot
be excluded; King 1993 likewise may already contain (4).

## 7. Caveats

* Full texts of Hammer 1979, King 1993 and Mateer 2013 could not be obtained (Taylor & Francis pages are behind a
  Cloudflare challenge from this environment); only abstracts (OpenAlex) and Gillogly's paraphrase were used.
* Gillogly's paper is a 2000 HTML conversion with OCR noise ("20l", "l01", "4l1"); its Table II is the copy we compared, so
  its five B1 discrepancies may be the conversion's rather than Gillogly's.
* The "message the cipher spells" is the consensus reading; all 763 letters are verified by the decode except the 22
  listed disagreements, which are exactly the u/x/y and slip positions, so no circularity beyond those.
* The encoder's numbering above 816 is unknown; the x = 1005 remains unexplained under every count we tried.
* Null models are i.i.d./permutation models; a genuine book-cipher of English text would have letter dependencies, but
  none that produce alphabetically ordered runs. The "unlimited substitutions" statistic (S4) is reported only to show how
  permissive it is (P ≈ 0.005 even for the observed 22).
* Tokenisation choices (hyphen split) follow the pamphlet's own numbering convention; alternatives are in the CSVs.
* Scan verification used the 1280-px Commons rendering of the LoC copy; "39" at position 417 is 3-or-8 in that
  rendering (never "36"); Wikisource's validated reading is 39.

## 8. Methods and reproducibility

`beale_common.py` holds the loaders and the two numberings. `b2_key.py` builds the keys and comparisons
(`results/key_*.csv`, `results/doi_pamphlet_vs_nara_wording.csv`, `results/pamphlet_numbering_anomalies.json`).
`b2_decode.py` decodes under each key, aligns with Needleman–Wunsch (match +2, mismatch −1, gap −2), resolves the
gaps, fits the offset segmentation (offsets −15..+15, λ ∈ {1,2,3,5,8,12}), and writes `results/b2_decode_summary.json`.
`b2_encoder_behaviour.py` repairs the slips and computes the rank statistics. `gillogly_strings.py` computes runs (exact
and with ≤ k substitutions by dynamic programming), exact run probabilities by a Markov chain on (last letter, run
length), and the Monte-Carlo nulls (numpy `default_rng(20260914)`); `gillogly_multi_runs.py` (seed 20260915) the
number-of-runs test; `render_tables.py` the tables above. Runtime: a few seconds for everything except the Monte Carlo
(≈ 40 min at the default sizes; `NSIM=20000 NSIM_SUB=5000` for a 40 s check).

## 9. Sources

* The Beale Papers (1885), Library of Congress copy, Wikisource transcription (validated pages): https://en.wikisource.org/wiki/The_Beale_Papers ; pages https://en.wikisource.org/wiki/Page:Beale_Papers.djvu/17 to /22 (Declaration pp. 17–20, cipher 2 and its "translation" pp. 20–21, cipher 1 p. 21, cipher 3 p. 22). Scan: https://commons.wikimedia.org/wiki/File:Beale_Papers.djvu (page 21 rendering saved as `sources/scans/beale_papers_djvu_page21_1280px.jpg`).
* J. J. Gillogly, "The Beale Cipher: A Dissenting Opinion", Cryptologia 4(2):116–119, April 1980, doi:10.1080/0161-118091854979; text used: https://web.archive.org/web/20060126085231/http://members.fortunecity.com/jpeschel/gillog3.htm (`sources/gillogly_1980_plain.txt`).
* C. Hammer, "How did TJB encode B2?", Cryptologia 3(1):9–15, 1979, doi:10.1080/0161-117991853747 (not accessible; cited through Gillogly 1980).
* J. C. King, "A reconstruction of the key to Beale cipher number two", Cryptologia 17(3):305–317, 1993, doi:10.1080/0161-119391867971; abstract via https://api.openalex.org/works/doi:10.1080/0161-119391867971
* T. D. Mateer, "Cryptanalysis of Beale Cipher Number Two", Cryptologia 37(3):215–232, 2013, doi:10.1080/01611194.2013.798517; abstract via https://api.openalex.org/works/doi:10.1080/01611194.2013.798517 ("...the author concludes that the Beale ciphers are likely a hoax").
* G. Love, "The Beale Ciphers" (myoutbox.net), https://web.archive.org/web/20060420134206/http://www.myoutbox.net/blove.htm (`sources/love_plain.txt`; includes his copy of B2 from E. E. Remington and his annotated pamphlet Declaration).
* unmuseum.org, "The Beale Papers" transcription: https://web.archive.org/web/2019/http://www.unmuseum.org/bealepap.htm (`sources/unmuseum_bealepap_wayback_plain.txt`).
* National Archives, "Declaration of Independence: A Transcription": https://www.archives.gov/founding-docs/declaration-transcript (`sources/nara_doi_plain.txt`).
* Wikipedia, "Beale ciphers" (wikitext, secondary): https://en.wikipedia.org/wiki/Beale_ciphers (`sources/wikipedia_beale_ciphers.txt`).
* DOIs resolved through https://api.crossref.org/works?query.bibliographic=... (Crossref).

## 10. King 1993 in the Internet Archive's full-text fragments

The central cryptanalytic observations were already in print. King's paper (Cryptologia 17:3, July 1993, pp. 305-317)
is paywalled and the Internet Archive's copy of the issue (sim_cryptologia_1993-07_17_3) is access-restricted, but its
full-text search returns fragments that settle the attribution:

* King reconstructed the encoder's key ("DOI-K") from the B2 decryption, with a Table 1 of word renumberings whose
  segments are ours (1-154 not renumbered; 155-157 undeterminable; 158-241 -> 157-240; 242-245 undeterminable; 467-484
  unused; 485-505 ...), a Table 4 of the seven B2 errors (positions 223, 531, 701, 722 corrected by the adjacent symbol;
  666: 440 for 40; 811 = y, 1005 = x, 95 = U), and a Table 5 of B1 anomalies under DOI-K versus Gillogly's DOI-P:
  AAABBCDEFF at 44, ABBBCCCCDDE at 84, BCDDE at 113, ABCDEFGHIIJKLMMNOHPP at 188. He notes Gillogly's 302-for-301
  correction and that the 1885 pamphlet's ciphers differ from later published versions.
* King credits earlier renumberings to Matyas (1979, after a copy of the pamphlet was found), Holst (1987, "Seven Simple
  Changes in the DOI ..."), Hammer (1979, concerning Hart's decryption) and notes that Hill (1989, unpublished)
  "discovered independently the same longer anomalous strings".
* King's reading of the strings: "it seems clear that these strings were purposely encrypted by someone"; three
  explanations: a hoax (Gillogly, Holst), alterations by the pamphlet's author "to flush out the keytext without giving
  away the entire solution", or the DOI being the true keytext with more to strip; "one would hope that such an elaborate
  hoax would be revealed by something more interesting".

Consequences for section 6 ("What is new"): items (1) in part, (4) and (7) are replications of King 1993 (and of Hill),
not additions. What survives as additions, as far as the fragments show: the offsets fitted algorithmically
from the cipher and matched to the pamphlet's printed parenthetical numbers; the typesetting argument ("mean time" /
"unalienable"); the observation that the numbering stops at 816; the exact Markov-chain probabilities, permutation and
run-count tests; the homophone-rank test; the quantification of the encoder's habits (overlap with Hammer 1979 and
Mateer 2013 cannot be excluded). Section 6 should be read with this correction; the report carries this attribution.

Consequence for the verdict: the improbability of the strings establishes that they were written deliberately from the
numbered Declaration; it does not by itself establish the whole hoax narrative, identify the author, or exclude a
further layer of encoding (King's third explanation). Those rest on the other lines of evidence and on judgement.

## 11. What King's fragments say about Matyas, Holst and Hill

King's fragments (saved as raw archive.org full-text search responses under sources/papers/king_1993_fragments/) say
"Neither Matyas nor Holst reported attempted decryptions of B1" and
"Gillogly [8] and Holst [18] see the strings as evidence of a hoax". So the three longer strings under the
reconstructed key are King's (1993), found independently by Hill (1989, unpublished); Holst (1987) reconstructed the
key and read Gillogly's string as evidence of a hoax but reported no decryption of cipher 1. Also verified from the
fragments: "The ciphers analyzed in this paper are from the 1885 pamphlet. These versions of the ciphers differ ..."
(versions_ciphers.json) and "It is known that Beale misnumbered his keytext in several places" (misnumbered.json).

The report's verdict panel states the printed-key finding as what counting establishes (the printed key and
instructions cannot produce the printed translation; the numbering matches the encoder's count at each of his five
miscounts) and treats "the narrator had the encoder's key" as the simpler reading, a judgement, with the
reconstructed-by-a-solver alternative possible in principle (section 6 of the report). Its scoreboard weight is
"strong".
