# Reading notes: the published method

Read in full for this rerun (all page numbers are those of the preprint PDF).

1. Jack Grieve, Emily Chiang, Isobelle Clarke, Hannah Gideon, Annina Heini,
   Andrea Nini and Emily Waibel, "Attributing the Bixby Letter using n-gram
   tracing", Digital Scholarship in the Humanities 34(3), 2019, 493-512,
   doi 10.1093/llc/fqy042. Author-accepted manuscript, University of
   Birmingham repository: https://pure-oai.bham.ac.uk/ws/files/53402456/Bixby_PREPRINT.pdf
   (39 pages; checked for eligibility 28 Sept 2018). The version of record
   at academic.oup.com is behind a paywall and was not read; the preprint
   is "pre-copyedited" and accepted 8 Aug 2018.
2. Jack Grieve, Emily Carmody, Isobelle Clarke, Mária Csemezová, Hannah
   Gideon, Cristina Greco, Annina Heini, Andrea Nini, Maria Tagtalidou and
   Emily Waibel, "Attributing the Bixby Letter: A case of historical
   disputed authorship", LSS Seminar Series, Aston University, 13 April
   2016. Slides (69 pages), linked from Grieve's presentations page
   https://sites.google.com/view/grievejw/presentations, file
   https://www.dropbox.com/s/98mb706q9adst8t/LSS_BIXBY.pdf?dl=1
3. Jack Grieve, Emily Carmody, Isobelle Clarke, Hannah Gideon, Annina
   Heini, Andrea Nini and Emily Waibel, "Attributing the Bixby Letter using
   n-gram tracing", Corpus Linguistics 2017, Birmingham, 26 July 2017.
   Slides (44 pages), https://www.dropbox.com/s/n38pa5ia716rol2/CL_BIXBY.pdf?dl=1,
   and the two-page abstract
   https://www.birmingham.ac.uk/Documents/college-artslaw/corpus/conference-archives/2017/general/paper200.pdf

## The method as the paper states it (preprint pp. 11-14)

- Unit: n-grams of words or characters. Word n-grams "ignore case and
  punctuation" and are not allowed "to span sentences" (p. 16, the
  Gettysburg example: 239 distinct 2-word types in 272 words). Character
  n-grams are "case-insensitive", include "punctuation marks and spaces",
  and again do not span sentences (p. 18).
- Step 1: extract all n-gram types of one length and level from the
  questioned text. Step 2: "a random sample of texts is analysed that is
  roughly equal in length to the total number of words in the possible
  author writing sample with the fewest words" (p. 12). Step 3: the share
  of the questioned text's n-gram types that occur at least once in each
  sample, the overlap coefficient |Q and A| / |Q| (p. 13). Step 4:
  attribute to the author with the larger share (p. 13).
- Repetition: "the analysis can be repeated for different random samples
  of texts, allowing for the average percentages of n-grams seen to be
  calculated and compared" (p. 13). The Gettysburg demonstration uses the
  whole Hay corpus (261,126 words) against random Lincoln samples of
  260,954 words; 50 random sequences for the letter (p. 27), 10 for the
  evaluation (p. 23). Cumulative traces are read "at 260,000 words".
- Ties "(often 0% or 100%)" count "as incorrect attributions for both
  authors" (p. 24).
- Majority rules: the author returned by at least 4 of the 7 analyses on
  4- to 10-character n-grams; the author returned by at least 2 of the 3
  analyses on 1- to 3-word n-grams (p. 24).

## Corpora (pp. 9-10)

- Lincoln: Basler's Collected Works from the University of Michigan site
  (quod.lib.umich.edu/l/lincoln/), 5,601 documents after removing any
  "for which we had any doubt that Lincoln was the primary author",
  cleaned of "salutations and valedictions"; then everything from 18 May
  1860 onward removed. Final corpus 1,085 texts, 400,747 words, 5 to
  17,003 words each, median 125.
- Hay: Thayer's Life and Letters vols I-II (archive.org), divided by hand
  into documents, plus Gutenberg 11392 (short stories, an anthology), 6062
  (Pike County Ballads), 16321 (The Bread-Winners), 7470 (Castilian Days).
  577 texts, 261,126 words, 9 to 8,954 words each, median 159.

## Evaluation (pp. 23-27) and result (pp. 27-29)

- Leave-one-out over all 1,662 texts; 25 n-gram types (1-5 word, 1-20
  character); 10 random sequences per author; author chosen at 260,000
  words. Table 3 (character) and Table 4 (word) give recall, precision,
  F1 and accuracy per type. Character 5- to 10-grams: F1 at or above 0.95
  for both authors; the 4- to 10-character majority "correctly identified
  the author of all 1,662 texts"; the 1- to 3-word majority reaches F1 at
  or above 0.95. Shorter texts are attributed less well (Wilcoxon,
  p < 0.001); under 100 words the 7-character recall is 0.94 (Hay) and
  0.96 (Lincoln).
- The letter: 1- to 3-word and 3- to 16-character n-grams, 17 analyses,
  all to Hay; "clear and consistent differences ... by 100,000 words for
  all word-level analyses and for all character-level analyses from 5
  characters onward". Longer character n-grams and 4-word n-grams also go
  to Hay; 5-word n-grams go to Lincoln on the single phrase "may be found
  in the" (Lincoln, 11 Jan 1837), which the authors discount.
- Table 5 lists the word n-grams of the letter used by only one man.

## What the slides add

- 2016 (LSS, Aston), slide 15: "For now we have not looked at detail at
  the effect of variation of register variation." Slide 54: "We also need
  to test sensitivity to register variation." Slide 68: "systematically
  test the method, including character- and POS-level n-grams and across
  different registers". The 2016 corpus was smaller (Hay 471 texts, about
  250,000 words; Lincoln 2,088 texts, about 350,000 words, before the
  May 1860 cut) and the evaluation then covered "around half-a-dozen
  Lincoln and Hay tests a piece". The 2016 attribution used word n-grams
  only, 25 random walks, averages every 2,000 words.
- 2017 (CL, Birmingham): the corpora and tables of the paper; "17 of the
  19 analyses attributed the Letter to Hay", 1- and 2-character analyses
  inconclusive; a closing slide says the method "appears to allow for
  cross-genre attribution".
