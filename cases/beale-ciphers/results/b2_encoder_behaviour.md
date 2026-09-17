# Cipher 2 encoder behaviour

Corrected cipher: 763 numbers, 181 distinct (results/b2_corrected_cipher.txt). Key = pamphlet numbering as resolved by the cipher, 95=unalienable, 811=y, 1005=x.

| letter | uses | distinct nos. | homophones in key | first word (n) | uses of first word | most used n (count, rank) | mean rank | mean norm. rank | top-3 share | max n used |
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
| x | 4 | 1 | 1 | have (1005) | 4 | 1005 (4, r1) | 1.0 | 0.50 | 1.00 | 1005 |
| y | 9 | 1 | 1 | fundamentally (811) | 9 | 811 (9, r1) | 1.0 | 0.50 | 1.00 | 811 |

## Global

- letters_encoded: 763
- distinct_numbers: 181
- reuse_rate_overall: 0.763
- share_of_uses_that_are_the_FIRST_word_with_that_initial: 0.169
- expected_share_first_word_if_uniform_over_homophones: 0.05
- mean_normalised_rank_(0.5_if_uniform): 0.123
- se_mean_normalised_rank: 0.0054
- share_uses_n_le_100: 0.535
- share_uses_n_le_250: 0.81
- share_uses_n_le_500: 0.904
- share_uses_n_gt_816: 0.005
- largest_number_other_than_1005: 811
- share_of_key_words_n_le_100: 0.076
- share_of_key_words_n_le_250: 0.191
- rank_histogram: {'rank1': 129, 'rank2': 114, 'rank3': 108, 'rank4-5': 106, 'rank6-10': 191, 'rank>10': 115}
- uses_that_repeat_a_number_seen_within_previous_10_numbers: 36
- normalised_rank_quartile_shares: [0.828, 0.118, 0.054, 0.0]
- ks_test_normalised_rank_vs_uniform: {'D': 0.6142, 'p': 2.6763569615073843e-277}
- doubled letters in the message: 19; same number used for both: 0

## Corrections applied to the printed cipher

- {"position": 223, "number": 84, "read_as": 85, "letter": "e", "word": "equal", "kind": "adjacent number"}
- {"position": 531, "number": 53, "read_as": 54, "letter": "t", "word": "to", "kind": "adjacent number"}
- {"position": 571, "number": 108, "read_as": [10, 8], "letters": "ni", "words": ["necessary", "it"]}
- {"position": 666, "number": 440, "read_as": 40, "letter": "w", "word": "which", "kind": "dropped digit"}
- {"position": 701, "number": 84, "read_as": 85, "letter": "e", "word": "equal", "kind": "adjacent number"}
- {"position": 722, "number": 96, "read_as": 95, "letter": "u", "word": "unalienable", "kind": "adjacent number"}
