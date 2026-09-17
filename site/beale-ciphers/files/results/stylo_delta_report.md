# Stylometric distances: Beale letters vs. the 1885 narrative, calibrated on control authors

Control corpus: 115 samples from 27 authors (see data/controls/manifest.csv). Z-scores computed on control samples only. Distances: Burrows Delta = mean |z-difference|; Cosine Delta = cosine distance between z-vectors.


## burrows_delta_100mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.50 (n=115). Same-author pairs: mean 0.874 (sd 0.153, n=203); different-author pairs: mean 1.057 (sd 0.154, n=6352). Cross-genre (letters vs other) different-author mean 1.076 (n=2688); cross-genre same-author mean 0.976 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.774 | -1.84 | 1.8 | 24.1 | 0.018 | 4.79 |
| beale_letters_2000 vs narrative_2000 | 0.957 | -0.65 | 27.8 | 72.9 | 0.278 | 0.83 |
| beale_letter1 vs narrative_2000 | 0.942 | -0.75 | 24.3 | 70.9 | 0.243 | 0.94 |
| beale_letters vs narrative_A | 0.941 | -0.75 | 24.2 | 70.9 | 0.242 | 0.95 |
| beale_letters vs narrative_B | 0.907 | -0.97 | 17.5 | 62.6 | 0.175 | 1.26 |
| narrative_A vs narrative_B | 0.861 | -1.27 | 9.5 | 48.8 | 0.095 | 1.84 |
| morriss vs narrative | 0.876 | -1.17 | 11.9 | 52.7 | 0.119 | 1.61 |
| morriss vs beale_letters | 1.044 | -0.08 | 49.1 | 85.2 | 0.491 | 0.50 |
| beale_b2 vs narrative | 1.531 | +3.09 | 99.7 | 100.0 | 0.997 | 0.00 |
| beale_b2 vs beale_letters | 1.523 | +3.04 | 99.7 | 100.0 | 0.997 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.275 (95% interval 0.194-0.355).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.774, z=-2.53), jefferson_2 (0.812, z=-2.22), jackson_3 (0.867, z=-1.77), cooke_lee_1 (0.886, z=-1.62), davis_1 (0.889, z=-1.60)
- **narrative**: cooke_lee_1 (0.727, z=-2.02), jefferson_1 (0.748, z=-1.86), davis_1 (0.758, z=-1.79), jefferson_2 (0.758, z=-1.79), cooke_2 (0.772, z=-1.68)
- **morriss**: narrative (0.876, z=-3.31), narrative_A (0.941, z=-2.68), narrative_2000 (0.944, z=-2.65), narrative_B (0.990, z=-2.20), jackson_4 (1.004, z=-2.07)
- **beale_letter1**: jefferson_2 (0.833, z=-2.21), narrative (0.834, z=-2.21), pattie_1 (0.900, z=-1.65), shsp_4 (0.921, z=-1.48), davis_1 (0.926, z=-1.44)
- **poe_goldbug_1**: bagby_4 (0.814, z=-2.59), randolph_4 (0.875, z=-2.15), poe_goldbug_2 (0.907, z=-1.92), twain_letters_1 (0.948, z=-1.63), cable_4 (0.971, z=-1.47)
- **poe_letters_1**: pattie_4 (0.906, z=-2.18), narrative (0.912, z=-2.13), jefferson_1 (0.968, z=-1.73), narrative_B (0.969, z=-1.72), paulding_3 (0.972, z=-1.70)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.924, jefferson 0.936, jackson 0.943, davis 0.982, paulding 0.994, flint 0.997
- **beale_letters_2000**: NARRATIVE(1885) 0.978, jefferson 0.990, davis 1.013, irving 1.019, flint 1.036, paulding 1.038
- **narrative**: BEALE LETTERS 0.774, paulding 0.884, jqadams 0.887, davis 0.897, jefferson 0.901, jackson 0.909
- **morriss**: NARRATIVE(1885) 0.966, jackson 1.115, jqadams 1.140, eggleston 1.149, paulding 1.161, lee 1.165

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.74 (n=108).
- beale_letters: mean distance to 1805-1846 samples 1.053, to 1858-1900 samples 1.117 -> looks EARLY (diff +0.064)
- beale_letters_2000: mean distance to 1805-1846 samples 1.091, to 1858-1900 samples 1.142 -> looks EARLY (diff +0.051)
- beale_letter1: mean distance to 1805-1846 samples 1.070, to 1858-1900 samples 1.126 -> looks EARLY (diff +0.056)
- narrative: mean distance to 1805-1846 samples 1.002, to 1858-1900 samples 0.992 -> looks LATE (diff -0.010)
- morriss: mean distance to 1805-1846 samples 1.220, to 1858-1900 samples 1.213 -> looks LATE (diff -0.007)

## cosine_delta_100mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.58 (n=115). Same-author pairs: mean 0.731 (sd 0.190, n=203); different-author pairs: mean 1.017 (sd 0.158, n=6352). Cross-genre (letters vs other) different-author mean 1.039 (n=2688); cross-genre same-author mean 0.762 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.655 | -2.29 | 2.0 | 35.5 | 0.020 | 6.48 |
| beale_letters_2000 vs narrative_2000 | 0.741 | -1.75 | 5.3 | 50.7 | 0.053 | 3.62 |
| beale_letter1 vs narrative_2000 | 0.745 | -1.72 | 5.4 | 51.2 | 0.054 | 3.51 |
| beale_letters vs narrative_A | 0.747 | -1.71 | 5.5 | 51.2 | 0.055 | 3.48 |
| beale_letters vs narrative_B | 0.682 | -2.12 | 2.6 | 37.9 | 0.026 | 5.30 |
| narrative_A vs narrative_B | 0.621 | -2.50 | 1.2 | 29.6 | 0.012 | 8.50 |
| morriss vs narrative | 0.584 | -2.73 | 0.7 | 22.7 | 0.007 | 13.56 |
| morriss vs beale_letters | 0.767 | -1.58 | 6.5 | 54.2 | 0.065 | 2.92 |
| beale_b2 vs narrative | 1.099 | +0.51 | 68.0 | 97.5 | 0.680 | 0.17 |
| beale_b2 vs beale_letters | 0.956 | -0.38 | 32.8 | 88.2 | 0.328 | 0.49 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.052 (95% interval 0.037-0.071).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: jackson_2 (0.644, z=-2.38), narrative (0.655, z=-2.31), jefferson_2 (0.660, z=-2.27), jefferson_4 (0.663, z=-2.25), narrative_B (0.682, z=-2.13)
- **narrative**: morriss (0.584, z=-2.37), beale_letters (0.655, z=-1.97), poe_letters_1 (0.674, z=-1.87), cabell_2 (0.681, z=-1.83), cooke_lee_4 (0.689, z=-1.78)
- **morriss**: narrative (0.584, z=-3.34), narrative_A (0.613, z=-3.11), narrative_2000 (0.615, z=-3.09), eggleston_3 (0.688, z=-2.51), narrative_B (0.695, z=-2.45)
- **beale_letter1**: narrative (0.699, z=-2.21), jefferson_2 (0.702, z=-2.19), jefferson_4 (0.707, z=-2.15), morriss (0.743, z=-1.89), narrative_A (0.744, z=-1.88)
- **poe_goldbug_1**: bagby_4 (0.476, z=-2.80), cable_4 (0.601, z=-2.16), twain_letters_1 (0.628, z=-2.02), randolph_4 (0.650, z=-1.90), twain_letters_4 (0.661, z=-1.85)
- **poe_letters_1**: pattie_4 (0.589, z=-2.20), twain_letters_4 (0.637, z=-1.95), lee_3 (0.638, z=-1.94), poe_goldbug_2 (0.639, z=-1.94), randolph_1 (0.642, z=-1.92)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.714, jefferson 0.760, jackson 0.764, randolph 0.840, gregg 0.899, pattie 0.902
- **beale_letters_2000**: NARRATIVE(1885) 0.762, jefferson 0.813, pattie 0.830, jackson 0.872, flint 0.892, gregg 0.899
- **narrative**: BEALE LETTERS 0.655, jackson 0.808, poe 0.809, lee 0.822, jqadams 0.836, eggleston 0.843
- **morriss**: NARRATIVE(1885) 0.654, jackson 0.810, lee 0.849, eggleston 0.882, jqadams 0.892, randolph 0.947

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.76 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.951, to 1858-1900 samples 1.053 -> looks EARLY (diff +0.102)
- beale_letters_2000: mean distance to 1805-1846 samples 0.947, to 1858-1900 samples 1.051 -> looks EARLY (diff +0.104)
- beale_letter1: mean distance to 1805-1846 samples 0.946, to 1858-1900 samples 1.054 -> looks EARLY (diff +0.108)
- narrative: mean distance to 1805-1846 samples 1.028, to 1858-1900 samples 0.985 -> looks LATE (diff -0.043)
- morriss: mean distance to 1805-1846 samples 1.005, to 1858-1900 samples 0.994 -> looks LATE (diff -0.011)

## burrows_delta_150mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.56 (n=115). Same-author pairs: mean 0.871 (sd 0.134, n=203); different-author pairs: mean 1.034 (sd 0.134, n=6352). Cross-genre (letters vs other) different-author mean 1.052 (n=2688); cross-genre same-author mean 0.988 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.741 | -2.19 | 0.5 | 16.3 | 0.005 | 11.01 |
| beale_letters_2000 vs narrative_2000 | 0.888 | -1.09 | 14.1 | 57.6 | 0.141 | 1.54 |
| beale_letter1 vs narrative_2000 | 0.871 | -1.21 | 10.7 | 48.8 | 0.107 | 1.75 |
| beale_letters vs narrative_A | 0.872 | -1.21 | 10.8 | 48.8 | 0.108 | 1.75 |
| beale_letters vs narrative_B | 0.865 | -1.26 | 9.5 | 47.3 | 0.095 | 1.85 |
| narrative_A vs narrative_B | 0.784 | -1.87 | 1.4 | 23.6 | 0.014 | 5.06 |
| morriss vs narrative | 0.908 | -0.94 | 18.3 | 65.0 | 0.183 | 1.29 |
| morriss vs beale_letters | 1.027 | -0.05 | 50.5 | 88.2 | 0.505 | 0.46 |
| beale_b2 vs narrative | 1.344 | +2.32 | 98.3 | 100.0 | 0.983 | 0.04 |
| beale_b2 vs beale_letters | 1.351 | +2.37 | 98.4 | 100.0 | 0.984 | 0.03 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.138 (95% interval 0.085-0.200).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.741, z=-2.93), jefferson_2 (0.835, z=-1.99), narrative_B (0.865, z=-1.70), narrative_2000 (0.871, z=-1.63), narrative_A (0.872, z=-1.63)
- **narrative**: jefferson_1 (0.728, z=-2.01), cooke_lee_1 (0.740, z=-1.90), beale_letters (0.741, z=-1.89), jefferson_2 (0.757, z=-1.75), cabell_1 (0.760, z=-1.72)
- **morriss**: narrative (0.908, z=-3.74), narrative_A (0.967, z=-3.08), narrative_2000 (0.968, z=-3.06), narrative_B (0.981, z=-2.92), beale_letter1 (1.020, z=-2.46)
- **beale_letter1**: narrative (0.796, z=-2.41), jefferson_2 (0.855, z=-1.82), ejames_2 (0.866, z=-1.70), narrative_A (0.870, z=-1.67), narrative_2000 (0.871, z=-1.65)
- **poe_goldbug_1**: poe_goldbug_2 (0.882, z=-2.20), bagby_4 (0.889, z=-2.14), cable_4 (0.894, z=-2.10), randolph_4 (0.925, z=-1.82), twain_letters_1 (0.932, z=-1.76)
- **poe_letters_1**: narrative (0.917, z=-2.45), lee_3 (0.950, z=-2.20), pattie_4 (0.959, z=-2.13), jefferson_1 (0.982, z=-1.96), narrative_B (0.993, z=-1.87)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.868, jackson 0.919, jefferson 0.929, tjames 0.945, davis 0.976, shsp 0.980
- **beale_letters_2000**: NARRATIVE(1885) 0.917, tjames 0.960, jefferson 0.972, irving 0.979, davis 0.985, shsp 0.987
- **narrative**: BEALE LETTERS 0.741, cabell 0.825, jqadams 0.852, jefferson 0.859, jackson 0.873, hall 0.892
- **morriss**: NARRATIVE(1885) 0.974, jackson 1.143, jqadams 1.159, cabell 1.180, eggleston 1.186, shsp 1.187

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.73 (n=108).
- beale_letters: mean distance to 1805-1846 samples 1.005, to 1858-1900 samples 1.064 -> looks EARLY (diff +0.059)
- beale_letters_2000: mean distance to 1805-1846 samples 1.029, to 1858-1900 samples 1.083 -> looks EARLY (diff +0.054)
- beale_letter1: mean distance to 1805-1846 samples 1.008, to 1858-1900 samples 1.064 -> looks EARLY (diff +0.056)
- narrative: mean distance to 1805-1846 samples 0.963, to 1858-1900 samples 0.947 -> looks LATE (diff -0.016)
- morriss: mean distance to 1805-1846 samples 1.238, to 1858-1900 samples 1.232 -> looks LATE (diff -0.007)

## cosine_delta_150mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.59 (n=115). Same-author pairs: mean 0.758 (sd 0.168, n=203); different-author pairs: mean 1.016 (sd 0.137, n=6352). Cross-genre (letters vs other) different-author mean 1.035 (n=2688); cross-genre same-author mean 0.817 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.673 | -2.51 | 1.4 | 32.0 | 0.014 | 8.95 |
| beale_letters_2000 vs narrative_2000 | 0.747 | -1.97 | 3.7 | 45.8 | 0.037 | 4.89 |
| beale_letter1 vs narrative_2000 | 0.745 | -1.98 | 3.6 | 45.8 | 0.036 | 4.99 |
| beale_letters vs narrative_A | 0.723 | -2.14 | 2.8 | 40.9 | 0.028 | 5.92 |
| beale_letters vs narrative_B | 0.733 | -2.07 | 3.1 | 41.4 | 0.031 | 5.51 |
| narrative_A vs narrative_B | 0.615 | -2.93 | 0.7 | 20.2 | 0.007 | 17.62 |
| morriss vs narrative | 0.620 | -2.89 | 0.7 | 21.2 | 0.007 | 17.01 |
| morriss vs beale_letters | 0.749 | -1.95 | 3.7 | 47.3 | 0.037 | 4.79 |
| beale_b2 vs narrative | 1.078 | +0.45 | 65.8 | 97.5 | 0.658 | 0.16 |
| beale_b2 vs beale_letters | 0.974 | -0.31 | 35.2 | 89.7 | 0.352 | 0.46 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.037 (95% interval 0.023-0.055).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.673, z=-2.98), narrative_A (0.723, z=-2.52), narrative_2000 (0.724, z=-2.51), jackson_2 (0.728, z=-2.48), narrative_B (0.733, z=-2.43)
- **narrative**: morriss (0.620, z=-2.45), poe_letters_1 (0.650, z=-2.25), cabell_2 (0.658, z=-2.20), beale_letters (0.673, z=-2.10), eggleston_3 (0.723, z=-1.78)
- **morriss**: narrative (0.620, z=-3.50), narrative_A (0.662, z=-3.12), narrative_2000 (0.664, z=-3.10), narrative_B (0.706, z=-2.71), eggleston_3 (0.747, z=-2.33)
- **beale_letter1**: narrative (0.730, z=-2.61), narrative_A (0.744, z=-2.47), narrative_2000 (0.745, z=-2.46), morriss (0.775, z=-2.17), poe_goldbug_2 (0.783, z=-2.09)
- **poe_goldbug_1**: bagby_4 (0.589, z=-2.47), cable_4 (0.607, z=-2.37), twain_letters_1 (0.658, z=-2.07), poe_letters_1 (0.678, z=-1.96), twain_letters_4 (0.678, z=-1.96)
- **poe_letters_1**: lee_3 (0.576, z=-2.45), twain_letters_4 (0.582, z=-2.42), pattie_4 (0.638, z=-2.11), narrative (0.650, z=-2.04), randolph_1 (0.663, z=-1.97)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.728, jackson 0.824, jefferson 0.847, gregg 0.898, randolph 0.909, tjames 0.923
- **beale_letters_2000**: NARRATIVE(1885) 0.789, jefferson 0.885, tjames 0.887, gregg 0.889, pattie 0.889, flint 0.911
- **narrative**: BEALE LETTERS 0.673, cabell 0.793, lee 0.839, jackson 0.839, poe 0.839, jqadams 0.862
- **morriss**: NARRATIVE(1885) 0.684, jackson 0.864, eggleston 0.906, randolph 0.908, jqadams 0.917, lee 0.919

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.73 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.953, to 1858-1900 samples 1.047 -> looks EARLY (diff +0.094)
- beale_letters_2000: mean distance to 1805-1846 samples 0.949, to 1858-1900 samples 1.046 -> looks EARLY (diff +0.097)
- beale_letter1: mean distance to 1805-1846 samples 0.949, to 1858-1900 samples 1.048 -> looks EARLY (diff +0.099)
- narrative: mean distance to 1805-1846 samples 1.029, to 1858-1900 samples 0.978 -> looks LATE (diff -0.050)
- morriss: mean distance to 1805-1846 samples 1.003, to 1858-1900 samples 0.996 -> looks LATE (diff -0.007)

## burrows_delta_200mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.60 (n=115). Same-author pairs: mean 0.854 (sd 0.115, n=203); different-author pairs: mean 1.006 (sd 0.118, n=6352). Cross-genre (letters vs other) different-author mean 1.017 (n=2688); cross-genre same-author mean 0.956 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.683 | -2.75 | 0.0 | 7.4 | 0.000 | 94.01 |
| beale_letters_2000 vs narrative_2000 | 0.828 | -1.52 | 5.3 | 42.4 | 0.053 | 2.71 |
| beale_letter1 vs narrative_2000 | 0.816 | -1.62 | 3.8 | 37.9 | 0.038 | 3.23 |
| beale_letters vs narrative_A | 0.811 | -1.66 | 3.4 | 36.9 | 0.034 | 3.52 |
| beale_letters vs narrative_B | 0.804 | -1.72 | 2.6 | 35.0 | 0.026 | 3.94 |
| narrative_A vs narrative_B | 0.750 | -2.18 | 0.5 | 16.7 | 0.005 | 10.21 |
| morriss vs narrative | 0.910 | -0.82 | 21.2 | 70.0 | 0.212 | 1.12 |
| morriss vs beale_letters | 1.013 | +0.06 | 55.1 | 90.6 | 0.551 | 0.34 |
| beale_b2 vs narrative | 1.366 | +3.06 | 99.7 | 100.0 | 0.997 | 0.00 |
| beale_b2 vs beale_letters | 1.377 | +3.15 | 99.7 | 100.0 | 0.997 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.052 (95% interval 0.026-0.076).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.683, z=-3.46), jefferson_2 (0.790, z=-2.26), narrative_B (0.804, z=-2.11), narrative_2000 (0.806, z=-2.10), narrative_A (0.811, z=-2.04)
- **narrative**: beale_letters (0.683, z=-2.49), jefferson_1 (0.730, z=-2.01), beale_letter1 (0.745, z=-1.86), pollock_3 (0.760, z=-1.70), jackson_3 (0.766, z=-1.64)
- **morriss**: narrative (0.910, z=-4.31), narrative_2000 (0.942, z=-3.90), narrative_A (0.944, z=-3.86), narrative_B (0.989, z=-3.28), beale_letter1 (1.008, z=-3.04)
- **beale_letter1**: narrative (0.745, z=-2.83), narrative_2000 (0.816, z=-2.05), narrative_A (0.820, z=-2.01), jefferson_2 (0.821, z=-1.99), ejames_2 (0.822, z=-1.99)
- **poe_goldbug_1**: cable_4 (0.808, z=-2.51), poe_goldbug_2 (0.808, z=-2.51), bagby_4 (0.849, z=-2.10), twain_letters_4 (0.869, z=-1.89), twain_letters_1 (0.889, z=-1.68)
- **poe_letters_1**: narrative (0.903, z=-2.35), jefferson_1 (0.960, z=-1.85), narrative_B (0.973, z=-1.73), randolph_1 (0.978, z=-1.69), lee_3 (0.981, z=-1.66)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.808, jackson 0.890, jefferson 0.894, davis 0.903, tjames 0.918, gregg 0.940
- **beale_letters_2000**: NARRATIVE(1885) 0.859, davis 0.928, tjames 0.934, jefferson 0.939, irving 0.943, gregg 0.955
- **narrative**: BEALE LETTERS 0.683, jackson 0.840, jefferson 0.840, davis 0.842, jqadams 0.848, cabell 0.859
- **morriss**: NARRATIVE(1885) 0.967, jackson 1.160, jqadams 1.183, eggleston 1.193, cooke 1.201, davis 1.206

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.72 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.965, to 1858-1900 samples 1.023 -> looks EARLY (diff +0.058)
- beale_letters_2000: mean distance to 1805-1846 samples 0.994, to 1858-1900 samples 1.050 -> looks EARLY (diff +0.056)
- beale_letter1: mean distance to 1805-1846 samples 0.973, to 1858-1900 samples 1.030 -> looks EARLY (diff +0.057)
- narrative: mean distance to 1805-1846 samples 0.925, to 1858-1900 samples 0.929 -> looks EARLY (diff +0.004)
- morriss: mean distance to 1805-1846 samples 1.240, to 1858-1900 samples 1.247 -> looks EARLY (diff +0.006)

## cosine_delta_200mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.63 (n=115). Same-author pairs: mean 0.771 (sd 0.157, n=203); different-author pairs: mean 1.016 (sd 0.120, n=6352). Cross-genre (letters vs other) different-author mean 1.031 (n=2688); cross-genre same-author mean 0.824 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.611 | -3.38 | 0.3 | 15.3 | 0.003 | 24.88 |
| beale_letters_2000 vs narrative_2000 | 0.691 | -2.71 | 1.0 | 31.0 | 0.010 | 13.11 |
| beale_letter1 vs narrative_2000 | 0.694 | -2.69 | 1.1 | 31.5 | 0.011 | 12.76 |
| beale_letters vs narrative_A | 0.674 | -2.86 | 0.8 | 26.6 | 0.008 | 15.66 |
| beale_letters vs narrative_B | 0.675 | -2.84 | 0.9 | 26.6 | 0.009 | 15.43 |
| narrative_A vs narrative_B | 0.597 | -3.50 | 0.3 | 14.3 | 0.003 | 26.19 |
| morriss vs narrative | 0.544 | -3.94 | 0.1 | 9.9 | 0.001 | 79.94 |
| morriss vs beale_letters | 0.666 | -2.92 | 0.7 | 24.6 | 0.007 | 16.55 |
| beale_b2 vs narrative | 1.099 | +0.70 | 75.0 | 100.0 | 0.750 | 0.13 |
| beale_b2 vs beale_letters | 1.019 | +0.02 | 47.8 | 94.1 | 0.478 | 0.26 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.010 (95% interval 0.004-0.019).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.611, z=-4.06), morriss (0.666, z=-3.48), narrative_2000 (0.669, z=-3.45), narrative_A (0.674, z=-3.41), narrative_B (0.675, z=-3.39)
- **narrative**: morriss (0.544, z=-3.87), beale_letters (0.611, z=-3.30), beale_letter1 (0.672, z=-2.78), beale_letters_2000 (0.681, z=-2.71), poe_letters_1 (0.710, z=-2.46)
- **morriss**: narrative (0.544, z=-4.97), narrative_2000 (0.586, z=-4.52), narrative_A (0.600, z=-4.37), narrative_B (0.636, z=-3.97), beale_letters_2000 (0.653, z=-3.79)
- **beale_letter1**: morriss (0.670, z=-3.54), narrative (0.672, z=-3.52), narrative_2000 (0.694, z=-3.28), narrative_A (0.701, z=-3.20), narrative_B (0.749, z=-2.69)
- **poe_goldbug_1**: bagby_4 (0.630, z=-2.52), cable_4 (0.636, z=-2.48), twain_letters_4 (0.686, z=-2.15), twain_letters_1 (0.690, z=-2.12), randolph_2 (0.709, z=-2.00)
- **poe_letters_1**: twain_letters_4 (0.653, z=-2.40), lee_3 (0.693, z=-2.13), randolph_1 (0.697, z=-2.10), lee_1 (0.702, z=-2.07), randolph_2 (0.705, z=-2.05)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.674, jefferson 0.863, jackson 0.869, randolph 0.894, gregg 0.898, poe 0.914
- **beale_letters_2000**: NARRATIVE(1885) 0.732, jefferson 0.890, gregg 0.893, pattie 0.895, tjames 0.901, ejames 0.928
- **narrative**: BEALE LETTERS 0.611, poe 0.849, lee 0.858, cabell 0.859, jackson 0.874, eggleston 0.893
- **morriss**: NARRATIVE(1885) 0.618, randolph 0.885, jackson 0.919, eggleston 0.920, poe 0.941, lee 0.943

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.79 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.956, to 1858-1900 samples 1.044 -> looks EARLY (diff +0.088)
- beale_letters_2000: mean distance to 1805-1846 samples 0.954, to 1858-1900 samples 1.044 -> looks EARLY (diff +0.091)
- beale_letter1: mean distance to 1805-1846 samples 0.953, to 1858-1900 samples 1.045 -> looks EARLY (diff +0.091)
- narrative: mean distance to 1805-1846 samples 1.014, to 1858-1900 samples 0.991 -> looks LATE (diff -0.024)
- morriss: mean distance to 1805-1846 samples 0.998, to 1858-1900 samples 1.003 -> looks EARLY (diff +0.004)

## burrows_delta_300mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.69 (n=115). Same-author pairs: mean 0.821 (sd 0.101, n=203); different-author pairs: mean 0.958 (sd 0.104, n=6352). Cross-genre (letters vs other) different-author mean 0.964 (n=2688); cross-genre same-author mean 0.926 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.638 | -3.06 | 0.0 | 3.9 | 0.000 | 284.08 |
| beale_letters_2000 vs narrative_2000 | 0.799 | -1.52 | 4.9 | 43.3 | 0.049 | 2.70 |
| beale_letter1 vs narrative_2000 | 0.785 | -1.65 | 3.4 | 35.5 | 0.034 | 3.44 |
| beale_letters vs narrative_A | 0.785 | -1.66 | 3.3 | 35.5 | 0.033 | 3.48 |
| beale_letters vs narrative_B | 0.709 | -2.38 | 0.2 | 14.3 | 0.002 | 19.96 |
| narrative_A vs narrative_B | 0.741 | -2.08 | 0.7 | 21.2 | 0.007 | 9.13 |
| morriss vs narrative | 0.862 | -0.92 | 18.4 | 64.0 | 0.184 | 1.20 |
| morriss vs beale_letters | 0.961 | +0.03 | 54.1 | 90.6 | 0.541 | 0.38 |
| beale_b2 vs narrative | 1.196 | +2.28 | 98.1 | 100.0 | 0.981 | 0.00 |
| beale_b2 vs beale_letters | 1.225 | +2.56 | 98.9 | 100.0 | 0.989 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.049 (95% interval 0.023-0.073).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.638, z=-3.73), narrative_B (0.709, z=-2.85), jefferson_2 (0.733, z=-2.56), narrative_2000 (0.780, z=-1.98), narrative_A (0.785, z=-1.92)
- **narrative**: beale_letters (0.638, z=-2.69), beale_letter1 (0.681, z=-2.22), beale_letters_2000 (0.702, z=-1.99), jackson_3 (0.732, z=-1.66), pollock_3 (0.736, z=-1.62)
- **morriss**: narrative (0.862, z=-4.40), narrative_2000 (0.913, z=-3.70), narrative_A (0.915, z=-3.66), narrative_B (0.922, z=-3.57), beale_letters (0.961, z=-3.03)
- **beale_letter1**: narrative (0.681, z=-3.25), narrative_B (0.750, z=-2.39), jefferson_2 (0.755, z=-2.32), gregg_1 (0.778, z=-2.03), narrative_2000 (0.785, z=-1.94)
- **poe_goldbug_1**: poe_goldbug_2 (0.788, z=-1.98), bagby_4 (0.793, z=-1.92), cable_4 (0.799, z=-1.85), cable_1 (0.813, z=-1.68), bagby_2 (0.823, z=-1.57)
- **poe_letters_1**: narrative (0.835, z=-2.29), pattie_4 (0.876, z=-1.89), jackson_3 (0.879, z=-1.85), narrative_B (0.883, z=-1.81), jefferson_2 (0.894, z=-1.71)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.747, jefferson 0.836, jackson 0.841, davis 0.872, paulding 0.878, gregg 0.880
- **beale_letters_2000**: NARRATIVE(1885) 0.788, jefferson 0.863, davis 0.886, gregg 0.888, shsp 0.896, hall 0.896
- **narrative**: BEALE LETTERS 0.638, jefferson 0.792, jackson 0.800, jqadams 0.800, paulding 0.815, cabell 0.818
- **morriss**: NARRATIVE(1885) 0.919, jackson 1.082, jqadams 1.114, flint 1.123, eggleston 1.136, paulding 1.147

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.77 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.919, to 1858-1900 samples 0.961 -> looks EARLY (diff +0.042)
- beale_letters_2000: mean distance to 1805-1846 samples 0.935, to 1858-1900 samples 0.974 -> looks EARLY (diff +0.039)
- beale_letter1: mean distance to 1805-1846 samples 0.918, to 1858-1900 samples 0.961 -> looks EARLY (diff +0.042)
- narrative: mean distance to 1805-1846 samples 0.882, to 1858-1900 samples 0.889 -> looks EARLY (diff +0.007)
- morriss: mean distance to 1805-1846 samples 1.174, to 1858-1900 samples 1.188 -> looks EARLY (diff +0.015)

## cosine_delta_300mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.63 (n=115). Same-author pairs: mean 0.792 (sd 0.145, n=203); different-author pairs: mean 1.015 (sd 0.103, n=6352). Cross-genre (letters vs other) different-author mean 1.028 (n=2688); cross-genre same-author mean 0.843 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.580 | -4.24 | 0.0 | 10.3 | 0.000 | 73.33 |
| beale_letters_2000 vs narrative_2000 | 0.729 | -2.79 | 1.0 | 31.0 | 0.010 | 10.55 |
| beale_letter1 vs narrative_2000 | 0.728 | -2.80 | 1.0 | 30.5 | 0.010 | 10.67 |
| beale_letters vs narrative_A | 0.717 | -2.91 | 0.8 | 29.1 | 0.008 | 13.17 |
| beale_letters vs narrative_B | 0.590 | -4.14 | 0.0 | 11.3 | 0.000 | 50.19 |
| narrative_A vs narrative_B | 0.651 | -3.55 | 0.3 | 15.8 | 0.003 | 24.53 |
| morriss vs narrative | 0.585 | -4.20 | 0.0 | 10.3 | 0.000 | 61.11 |
| morriss vs beale_letters | 0.690 | -3.17 | 0.6 | 24.6 | 0.006 | 23.51 |
| beale_b2 vs narrative | 0.947 | -0.67 | 22.6 | 84.7 | 0.226 | 0.72 |
| beale_b2 vs beale_letters | 0.973 | -0.41 | 30.3 | 91.1 | 0.303 | 0.46 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.010 (95% interval 0.004-0.018).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.580, z=-4.96), narrative_B (0.590, z=-4.85), morriss (0.690, z=-3.66), narrative_2000 (0.714, z=-3.38), narrative_A (0.717, z=-3.34)
- **narrative**: beale_letters (0.580, z=-3.92), morriss (0.585, z=-3.88), beale_letter1 (0.628, z=-3.47), beale_letters_2000 (0.647, z=-3.30), poe_letters_1 (0.734, z=-2.48)
- **morriss**: narrative (0.585, z=-5.22), narrative_2000 (0.654, z=-4.35), narrative_B (0.655, z=-4.34), narrative_A (0.663, z=-4.24), beale_letters (0.690, z=-3.89)
- **beale_letter1**: narrative (0.628, z=-4.88), narrative_B (0.653, z=-4.54), morriss (0.698, z=-3.96), narrative_2000 (0.728, z=-3.56), narrative_A (0.733, z=-3.49)
- **poe_goldbug_1**: bagby_4 (0.681, z=-2.65), cable_4 (0.738, z=-2.19), cable_2 (0.748, z=-2.11), poe_letters_1 (0.767, z=-1.96), randolph_2 (0.771, z=-1.93)
- **poe_letters_1**: twain_letters_4 (0.691, z=-2.49), lee_1 (0.710, z=-2.34), narrative_B (0.731, z=-2.18), narrative (0.734, z=-2.15), randolph_1 (0.752, z=-2.01)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.653, jefferson 0.863, jackson 0.870, randolph 0.913, poe 0.918, gregg 0.919
- **beale_letters_2000**: NARRATIVE(1885) 0.709, jefferson 0.894, gregg 0.915, pattie 0.927, poe 0.952, tjames 0.955
- **narrative**: BEALE LETTERS 0.580, poe 0.863, lee 0.866, jackson 0.869, eggleston 0.887, cabell 0.889
- **morriss**: NARRATIVE(1885) 0.659, randolph 0.903, jackson 0.908, eggleston 0.919, poe 0.934, lee 0.946

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.78 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.971, to 1858-1900 samples 1.029 -> looks EARLY (diff +0.058)
- beale_letters_2000: mean distance to 1805-1846 samples 0.973, to 1858-1900 samples 1.024 -> looks EARLY (diff +0.051)
- beale_letter1: mean distance to 1805-1846 samples 0.971, to 1858-1900 samples 1.026 -> looks EARLY (diff +0.055)
- narrative: mean distance to 1805-1846 samples 1.006, to 1858-1900 samples 0.994 -> looks LATE (diff -0.012)
- morriss: mean distance to 1805-1846 samples 0.994, to 1858-1900 samples 1.006 -> looks EARLY (diff +0.011)

## burrows_delta_500mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.65 (n=115). Same-author pairs: mean 0.773 (sd 0.085, n=203); different-author pairs: mean 0.889 (sd 0.086, n=6352). Cross-genre (letters vs other) different-author mean 0.892 (n=2688); cross-genre same-author mean 0.830 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.604 | -3.30 | 0.0 | 2.5 | 0.000 | 342.74 |
| beale_letters_2000 vs narrative_2000 | 0.753 | -1.57 | 3.7 | 39.9 | 0.037 | 3.55 |
| beale_letter1 vs narrative_2000 | 0.735 | -1.78 | 1.9 | 30.5 | 0.019 | 5.12 |
| beale_letters vs narrative_A | 0.720 | -1.96 | 1.0 | 26.6 | 0.010 | 7.43 |
| beale_letters vs narrative_B | 0.680 | -2.42 | 0.2 | 13.3 | 0.002 | 25.42 |
| narrative_A vs narrative_B | 0.705 | -2.13 | 0.5 | 20.7 | 0.005 | 11.69 |
| morriss vs narrative | 0.799 | -1.04 | 13.6 | 64.5 | 0.136 | 1.34 |
| morriss vs beale_letters | 0.829 | -0.70 | 24.4 | 74.4 | 0.244 | 0.85 |
| beale_b2 vs narrative | 1.175 | +3.31 | 99.4 | 100.0 | 0.994 | 0.01 |
| beale_b2 vs beale_letters | 1.185 | +3.43 | 99.4 | 100.0 | 0.994 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.037 (95% interval 0.014-0.058).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.604, z=-3.86), narrative_B (0.680, z=-2.71), narrative_2000 (0.718, z=-2.14), narrative_A (0.720, z=-2.10), jefferson_2 (0.749, z=-1.66)
- **narrative**: beale_letters (0.604, z=-3.21), beale_letter1 (0.653, z=-2.55), beale_letters_2000 (0.678, z=-2.21), bagby_1 (0.722, z=-1.61), jqadams_2 (0.723, z=-1.60)
- **morriss**: narrative (0.799, z=-3.81), beale_letters (0.829, z=-3.28), beale_letter1 (0.835, z=-3.17), narrative_B (0.838, z=-3.12), beale_letters_2000 (0.839, z=-3.10)
- **beale_letter1**: narrative (0.653, z=-3.10), narrative_B (0.717, z=-2.14), narrative_2000 (0.735, z=-1.86), narrative_A (0.737, z=-1.83), gregg_2 (0.751, z=-1.62)
- **poe_goldbug_1**: bagby_2 (0.740, z=-1.95), cable_4 (0.750, z=-1.81), bagby_4 (0.759, z=-1.69), twain_letters_1 (0.767, z=-1.59), twain_letters_4 (0.771, z=-1.53)
- **poe_letters_1**: narrative (0.795, z=-2.01), bagby_1 (0.817, z=-1.73), jefferson_1 (0.827, z=-1.60), jefferson_2 (0.829, z=-1.58), twain_letters_4 (0.830, z=-1.56)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.700, davis 0.798, jackson 0.799, hall 0.807, jqadams 0.809, jefferson 0.810
- **beale_letters_2000**: NARRATIVE(1885) 0.745, davis 0.799, gregg 0.809, hall 0.810, jqadams 0.810, tjames 0.815
- **narrative**: BEALE LETTERS 0.604, jqadams 0.767, davis 0.779, hall 0.781, eggleston 0.783, jefferson 0.784
- **morriss**: NARRATIVE(1885) 0.841, jqadams 0.956, eggleston 0.965, jackson 0.971, hall 0.979, bagby 0.983

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.74 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.842, to 1858-1900 samples 0.876 -> looks EARLY (diff +0.034)
- beale_letters_2000: mean distance to 1805-1846 samples 0.848, to 1858-1900 samples 0.882 -> looks EARLY (diff +0.034)
- beale_letter1: mean distance to 1805-1846 samples 0.841, to 1858-1900 samples 0.876 -> looks EARLY (diff +0.036)
- narrative: mean distance to 1805-1846 samples 0.838, to 1858-1900 samples 0.846 -> looks EARLY (diff +0.008)
- morriss: mean distance to 1805-1846 samples 1.009, to 1858-1900 samples 1.018 -> looks EARLY (diff +0.009)

## cosine_delta_500mfw

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.68 (n=115). Same-author pairs: mean 0.821 (sd 0.129, n=203); different-author pairs: mean 1.015 (sd 0.083, n=6352). Cross-genre (letters vs other) different-author mean 1.024 (n=2688); cross-genre same-author mean 0.881 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.622 | -4.74 | 0.0 | 7.9 | 0.000 | 304.94 |
| beale_letters_2000 vs narrative_2000 | 0.805 | -2.53 | 1.9 | 37.4 | 0.019 | 8.52 |
| beale_letter1 vs narrative_2000 | 0.776 | -2.88 | 1.1 | 31.5 | 0.011 | 10.99 |
| beale_letters vs narrative_A | 0.737 | -3.36 | 0.6 | 25.6 | 0.006 | 18.41 |
| beale_letters vs narrative_B | 0.651 | -4.39 | 0.1 | 11.8 | 0.001 | 56.03 |
| narrative_A vs narrative_B | 0.671 | -4.15 | 0.1 | 13.8 | 0.001 | 37.71 |
| morriss vs narrative | 0.702 | -3.78 | 0.3 | 18.2 | 0.003 | 28.80 |
| morriss vs beale_letters | 0.730 | -3.43 | 0.5 | 23.6 | 0.005 | 19.59 |
| beale_b2 vs narrative | 0.935 | -0.96 | 15.3 | 80.3 | 0.153 | 1.07 |
| beale_b2 vs beale_letters | 0.974 | -0.49 | 27.0 | 89.7 | 0.270 | 0.52 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.019 (95% interval 0.011-0.030).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.622, z=-5.47), narrative_B (0.651, z=-5.06), morriss (0.730, z=-3.90), narrative_2000 (0.733, z=-3.86), narrative_A (0.737, z=-3.81)
- **narrative**: beale_letters (0.622, z=-4.40), beale_letter1 (0.676, z=-3.77), morriss (0.702, z=-3.47), beale_letters_2000 (0.715, z=-3.31), jackson_3 (0.786, z=-2.48)
- **morriss**: narrative (0.702, z=-5.13), beale_letters_2000 (0.723, z=-4.77), beale_letters (0.730, z=-4.63), beale_letter1 (0.735, z=-4.56), narrative_2000 (0.746, z=-4.36)
- **beale_letter1**: narrative (0.676, z=-4.89), narrative_B (0.695, z=-4.60), morriss (0.735, z=-4.00), narrative_2000 (0.776, z=-3.37), narrative_A (0.780, z=-3.31)
- **poe_goldbug_1**: randolph_2 (0.731, z=-2.87), bagby_4 (0.742, z=-2.75), cable_4 (0.760, z=-2.56), cable_2 (0.799, z=-2.16), poe_letters_1 (0.818, z=-1.97)
- **poe_letters_1**: twain_letters_4 (0.759, z=-2.51), randolph_1 (0.774, z=-2.35), jackson_2 (0.775, z=-2.34), lee_1 (0.788, z=-2.21), lee_3 (0.793, z=-2.17)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.694, jackson 0.886, jefferson 0.921, randolph 0.930, gregg 0.942, davis 0.945
- **beale_letters_2000**: NARRATIVE(1885) 0.769, pattie 0.918, gregg 0.932, jefferson 0.934, davis 0.939, jackson 0.949
- **narrative**: BEALE LETTERS 0.622, poe 0.867, jackson 0.890, eggleston 0.893, jefferson 0.915, davis 0.926
- **morriss**: NARRATIVE(1885) 0.757, eggleston 0.916, jackson 0.943, page 0.948, randolph 0.950, lee 0.958

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.80 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.977, to 1858-1900 samples 1.022 -> looks EARLY (diff +0.045)
- beale_letters_2000: mean distance to 1805-1846 samples 0.975, to 1858-1900 samples 1.020 -> looks EARLY (diff +0.045)
- beale_letter1: mean distance to 1805-1846 samples 0.975, to 1858-1900 samples 1.021 -> looks EARLY (diff +0.047)
- narrative: mean distance to 1805-1846 samples 1.005, to 1858-1900 samples 0.997 -> looks LATE (diff -0.008)
- morriss: mean distance to 1805-1846 samples 1.000, to 1858-1900 samples 0.999 -> looks LATE (diff -0.001)

## cosine_delta_200mfw_nopronouns

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.57 (n=115). Same-author pairs: mean 0.783 (sd 0.154, n=203); different-author pairs: mean 1.016 (sd 0.113, n=6352). Cross-genre (letters vs other) different-author mean 1.027 (n=2688); cross-genre same-author mean 0.839 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.546 | -4.18 | 0.1 | 9.9 | 0.001 | 201.75 |
| beale_letters_2000 vs narrative_2000 | 0.633 | -3.40 | 0.3 | 15.3 | 0.003 | 24.38 |
| beale_letter1 vs narrative_2000 | 0.632 | -3.41 | 0.3 | 15.3 | 0.003 | 24.38 |
| beale_letters vs narrative_A | 0.620 | -3.52 | 0.2 | 14.3 | 0.002 | 24.24 |
| beale_letters vs narrative_B | 0.618 | -3.54 | 0.2 | 13.8 | 0.002 | 24.35 |
| narrative_A vs narrative_B | 0.591 | -3.77 | 0.1 | 11.8 | 0.001 | 38.96 |
| morriss vs narrative | 0.590 | -3.78 | 0.1 | 11.8 | 0.001 | 41.13 |
| morriss vs beale_letters | 0.651 | -3.24 | 0.3 | 18.7 | 0.003 | 22.16 |
| beale_b2 vs narrative | 1.070 | +0.48 | 66.5 | 98.5 | 0.665 | 0.17 |
| beale_b2 vs beale_letters | 1.009 | -0.06 | 44.3 | 92.1 | 0.443 | 0.31 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.003 (95% interval 0.001-0.007).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.546, z=-5.05), narrative_2000 (0.616, z=-4.27), narrative_B (0.618, z=-4.25), narrative_A (0.620, z=-4.22), morriss (0.651, z=-3.87)
- **narrative**: beale_letters (0.546, z=-3.88), morriss (0.590, z=-3.50), beale_letter1 (0.601, z=-3.41), beale_letters_2000 (0.613, z=-3.30), poe_letters_1 (0.694, z=-2.61)
- **morriss**: narrative (0.590, z=-4.86), beale_letters_2000 (0.617, z=-4.54), beale_letter1 (0.637, z=-4.29), narrative_2000 (0.641, z=-4.25), beale_letters (0.651, z=-4.13)
- **beale_letter1**: narrative (0.601, z=-4.67), narrative_2000 (0.632, z=-4.30), morriss (0.637, z=-4.24), narrative_A (0.639, z=-4.22), narrative_B (0.689, z=-3.63)
- **poe_goldbug_1**: bagby_4 (0.666, z=-2.66), cable_4 (0.706, z=-2.35), cable_2 (0.733, z=-2.14), twain_letters_1 (0.734, z=-2.14), randolph_2 (0.753, z=-1.99)
- **poe_letters_1**: twain_letters_4 (0.685, z=-2.51), narrative (0.694, z=-2.45), lee_3 (0.729, z=-2.17), narrative_2000 (0.732, z=-2.15), narrative_A (0.743, z=-2.07)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.619, jefferson 0.847, jackson 0.872, gregg 0.883, tjames 0.921, pattie 0.935
- **beale_letters_2000**: NARRATIVE(1885) 0.674, jefferson 0.883, gregg 0.888, tjames 0.898, pattie 0.912, jackson 0.936
- **narrative**: BEALE LETTERS 0.546, poe 0.855, cabell 0.868, lee 0.870, jackson 0.878, jefferson 0.887
- **morriss**: NARRATIVE(1885) 0.656, randolph 0.893, eggleston 0.924, tjames 0.935, jackson 0.937, pattie 0.944

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.79 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.960, to 1858-1900 samples 1.038 -> looks EARLY (diff +0.078)
- beale_letters_2000: mean distance to 1805-1846 samples 0.959, to 1858-1900 samples 1.038 -> looks EARLY (diff +0.079)
- beale_letter1: mean distance to 1805-1846 samples 0.959, to 1858-1900 samples 1.038 -> looks EARLY (diff +0.080)
- narrative: mean distance to 1805-1846 samples 1.002, to 1858-1900 samples 0.998 -> looks LATE (diff -0.004)
- morriss: mean distance to 1805-1846 samples 0.987, to 1858-1900 samples 1.010 -> looks EARLY (diff +0.022)

## cosine_delta_300mfw_nopronouns

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.60 (n=115). Same-author pairs: mean 0.806 (sd 0.139, n=203); different-author pairs: mean 1.015 (sd 0.096, n=6352). Cross-genre (letters vs other) different-author mean 1.025 (n=2688); cross-genre same-author mean 0.851 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.552 | -4.82 | 0.0 | 4.9 | 0.000 | 645.53 |
| beale_letters_2000 vs narrative_2000 | 0.699 | -3.29 | 0.5 | 22.2 | 0.005 | 24.78 |
| beale_letter1 vs narrative_2000 | 0.691 | -3.37 | 0.4 | 19.7 | 0.004 | 25.32 |
| beale_letters vs narrative_A | 0.672 | -3.56 | 0.3 | 17.7 | 0.003 | 24.48 |
| beale_letters vs narrative_B | 0.590 | -4.42 | 0.0 | 10.3 | 0.000 | 78.04 |
| narrative_A vs narrative_B | 0.648 | -3.82 | 0.1 | 12.8 | 0.001 | 27.90 |
| morriss vs narrative | 0.610 | -4.21 | 0.1 | 11.8 | 0.001 | 50.10 |
| morriss vs beale_letters | 0.653 | -3.76 | 0.2 | 14.3 | 0.002 | 26.08 |
| beale_b2 vs narrative | 0.913 | -1.06 | 13.8 | 75.9 | 0.138 | 1.31 |
| beale_b2 vs beale_letters | 0.966 | -0.51 | 27.6 | 87.7 | 0.276 | 0.56 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.005 (95% interval 0.002-0.010).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.552, z=-5.68), narrative_B (0.590, z=-5.19), morriss (0.653, z=-4.38), narrative_2000 (0.667, z=-4.21), narrative_A (0.672, z=-4.14)
- **narrative**: beale_letters (0.552, z=-4.45), beale_letter1 (0.599, z=-3.97), morriss (0.610, z=-3.86), beale_letters_2000 (0.622, z=-3.75), jackson_3 (0.759, z=-2.37)
- **morriss**: narrative (0.610, z=-5.20), beale_letters (0.653, z=-4.62), beale_letters_2000 (0.656, z=-4.59), narrative_B (0.658, z=-4.56), beale_letter1 (0.660, z=-4.53)
- **beale_letter1**: narrative (0.599, z=-5.60), narrative_B (0.644, z=-4.98), morriss (0.660, z=-4.74), narrative_2000 (0.691, z=-4.31), narrative_A (0.697, z=-4.22)
- **poe_goldbug_1**: bagby_4 (0.717, z=-2.81), cable_2 (0.766, z=-2.34), randolph_2 (0.803, z=-1.98), page_3 (0.810, z=-1.92), poe_letters_1 (0.813, z=-1.89)
- **poe_letters_1**: twain_letters_4 (0.721, z=-2.60), narrative (0.775, z=-2.11), lee_3 (0.776, z=-2.10), lee_1 (0.785, z=-2.02), narrative_2000 (0.812, z=-1.78)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.631, jefferson 0.872, jackson 0.874, gregg 0.903, poe 0.951, paulding 0.956
- **beale_letters_2000**: NARRATIVE(1885) 0.689, jefferson 0.901, gregg 0.904, eggleston 0.953, jackson 0.957, tjames 0.960
- **narrative**: BEALE LETTERS 0.552, eggleston 0.853, cabell 0.890, jackson 0.893, lee 0.899, poe 0.900
- **morriss**: NARRATIVE(1885) 0.679, randolph 0.910, jackson 0.913, eggleston 0.924, tjames 0.941, page 0.951

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.78 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.977, to 1858-1900 samples 1.020 -> looks EARLY (diff +0.043)
- beale_letters_2000: mean distance to 1805-1846 samples 0.979, to 1858-1900 samples 1.017 -> looks EARLY (diff +0.038)
- beale_letter1: mean distance to 1805-1846 samples 0.977, to 1858-1900 samples 1.018 -> looks EARLY (diff +0.041)
- narrative: mean distance to 1805-1846 samples 1.008, to 1858-1900 samples 0.990 -> looks LATE (diff -0.017)
- morriss: mean distance to 1805-1846 samples 0.989, to 1858-1900 samples 1.008 -> looks EARLY (diff +0.019)

## cosine_delta_function_words_150

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.61 (n=115). Same-author pairs: mean 0.774 (sd 0.155, n=203); different-author pairs: mean 1.016 (sd 0.129, n=6352). Cross-genre (letters vs other) different-author mean 1.034 (n=2688); cross-genre same-author mean 0.788 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.615 | -3.11 | 0.4 | 17.2 | 0.004 | 21.60 |
| beale_letters_2000 vs narrative_2000 | 0.730 | -2.22 | 2.1 | 37.9 | 0.021 | 6.60 |
| beale_letter1 vs narrative_2000 | 0.722 | -2.28 | 1.9 | 36.5 | 0.019 | 7.08 |
| beale_letters vs narrative_A | 0.728 | -2.23 | 2.0 | 37.4 | 0.020 | 6.70 |
| beale_letters vs narrative_B | 0.638 | -2.93 | 0.6 | 20.2 | 0.006 | 17.45 |
| narrative_A vs narrative_B | 0.654 | -2.81 | 0.8 | 23.6 | 0.008 | 15.44 |
| morriss vs narrative | 0.534 | -3.74 | 0.1 | 8.4 | 0.001 | 102.40 |
| morriss vs beale_letters | 0.765 | -1.95 | 3.3 | 43.8 | 0.033 | 4.77 |
| beale_b2 vs narrative | 0.950 | -0.51 | 28.9 | 85.7 | 0.289 | 0.64 |
| beale_b2 vs beale_letters | 1.011 | -0.04 | 45.7 | 94.1 | 0.457 | 0.35 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.021 (95% interval 0.011-0.034).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.615, z=-3.41), narrative_B (0.638, z=-3.20), jefferson_2 (0.680, z=-2.83), narrative_A (0.728, z=-2.41), narrative_2000 (0.729, z=-2.40)
- **narrative**: morriss (0.534, z=-3.44), beale_letters (0.615, z=-2.85), beale_letter1 (0.648, z=-2.60), poe_letters_1 (0.648, z=-2.60), beale_letters_2000 (0.683, z=-2.34)
- **morriss**: narrative (0.534, z=-5.00), narrative_B (0.600, z=-4.29), narrative_A (0.636, z=-3.91), narrative_2000 (0.637, z=-3.89), beale_letters_2000 (0.715, z=-3.05)
- **beale_letter1**: narrative (0.648, z=-3.47), narrative_B (0.701, z=-2.94), jefferson_2 (0.718, z=-2.78), narrative_A (0.721, z=-2.75), narrative_2000 (0.722, z=-2.74)
- **poe_goldbug_1**: cable_4 (0.566, z=-2.75), bagby_4 (0.574, z=-2.70), randolph_2 (0.599, z=-2.55), poe_letters_1 (0.715, z=-1.84), cable_2 (0.721, z=-1.80)
- **poe_letters_1**: narrative (0.648, z=-2.22), pattie_4 (0.651, z=-2.21), narrative_B (0.652, z=-2.20), twain_letters_4 (0.656, z=-2.17), randolph_1 (0.670, z=-2.09)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.683, jackson 0.812, jefferson 0.846, pattie 0.885, randolph 0.902, poe 0.914
- **beale_letters_2000**: NARRATIVE(1885) 0.740, pattie 0.840, jefferson 0.885, gregg 0.899, jackson 0.909, poe 0.948
- **narrative**: BEALE LETTERS 0.615, poe 0.803, lee 0.835, eggleston 0.859, paulding 0.885, jackson 0.886
- **morriss**: NARRATIVE(1885) 0.618, jackson 0.887, lee 0.901, pattie 0.935, eggleston 0.940, shsp 0.950

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.76 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.971, to 1858-1900 samples 1.036 -> looks EARLY (diff +0.066)
- beale_letters_2000: mean distance to 1805-1846 samples 0.971, to 1858-1900 samples 1.031 -> looks EARLY (diff +0.060)
- beale_letter1: mean distance to 1805-1846 samples 0.970, to 1858-1900 samples 1.034 -> looks EARLY (diff +0.064)
- narrative: mean distance to 1805-1846 samples 1.018, to 1858-1900 samples 0.998 -> looks LATE (diff -0.020)
- morriss: mean distance to 1805-1846 samples 1.004, to 1858-1900 samples 0.997 -> looks LATE (diff -0.007)

## burrows_delta_function_words_150

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.54 (n=115). Same-author pairs: mean 0.885 (sd 0.130, n=203); different-author pairs: mean 1.041 (sd 0.130, n=6352). Cross-genre (letters vs other) different-author mean 1.062 (n=2688); cross-genre same-author mean 1.006 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.771 | -2.07 | 0.9 | 18.2 | 0.009 | 7.20 |
| beale_letters_2000 vs narrative_2000 | 0.926 | -0.88 | 19.5 | 66.0 | 0.195 | 1.24 |
| beale_letter1 vs narrative_2000 | 0.911 | -0.99 | 15.7 | 63.1 | 0.157 | 1.45 |
| beale_letters vs narrative_A | 0.917 | -0.95 | 17.3 | 64.0 | 0.173 | 1.36 |
| beale_letters vs narrative_B | 0.871 | -1.30 | 8.2 | 46.3 | 0.082 | 2.27 |
| narrative_A vs narrative_B | 0.877 | -1.25 | 9.2 | 48.8 | 0.092 | 2.11 |
| morriss vs narrative | 1.006 | -0.26 | 41.8 | 84.2 | 0.418 | 0.47 |
| morriss vs beale_letters | 1.199 | +1.21 | 88.2 | 99.5 | 0.882 | 0.31 |
| beale_b2 vs narrative | 1.482 | +3.38 | 99.8 | 100.0 | 0.998 | 0.00 |
| beale_b2 vs beale_letters | 1.490 | +3.45 | 99.8 | 100.0 | 0.998 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.192 (95% interval 0.118-0.281).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.771, z=-3.17), jefferson_2 (0.848, z=-2.38), narrative_B (0.871, z=-2.14), shsp_4 (0.883, z=-2.01), jackson_3 (0.885, z=-1.99)
- **narrative**: beale_letters (0.771, z=-2.13), davis_1 (0.803, z=-1.83), cooke_lee_1 (0.807, z=-1.80), beale_letter1 (0.810, z=-1.77), paulding_3 (0.825, z=-1.62)
- **morriss**: narrative (1.006, z=-3.51), narrative_B (1.053, z=-3.00), narrative_A (1.088, z=-2.60), narrative_2000 (1.089, z=-2.59), jackson_3 (1.131, z=-2.13)
- **beale_letter1**: narrative (0.810, z=-2.82), jefferson_2 (0.862, z=-2.26), shsp_4 (0.886, z=-2.01), narrative_B (0.906, z=-1.80), narrative_A (0.911, z=-1.75)
- **poe_goldbug_1**: cable_4 (0.813, z=-2.78), bagby_4 (0.862, z=-2.35), randolph_2 (0.900, z=-2.00), cable_2 (0.925, z=-1.78), poe_goldbug_2 (0.931, z=-1.72)
- **poe_letters_1**: narrative (0.991, z=-2.26), pattie_4 (1.037, z=-1.88), bagby_1 (1.044, z=-1.82), jackson_3 (1.051, z=-1.77), narrative_B (1.061, z=-1.68)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.894, jackson 0.935, davis 0.962, tjames 0.976, paulding 1.007, shsp 1.013
- **beale_letters_2000**: NARRATIVE(1885) 0.936, davis 0.968, tjames 0.991, jackson 0.998, shsp 1.005, pattie 1.009
- **narrative**: BEALE LETTERS 0.771, paulding 0.889, jqadams 0.917, davis 0.921, jackson 0.927, cabell 0.939
- **morriss**: NARRATIVE(1885) 1.071, jackson 1.208, jqadams 1.245, shsp 1.249, cooke 1.259, lee 1.286

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.72 (n=108).
- beale_letters: mean distance to 1805-1846 samples 1.057, to 1858-1900 samples 1.096 -> looks EARLY (diff +0.040)
- beale_letters_2000: mean distance to 1805-1846 samples 1.070, to 1858-1900 samples 1.100 -> looks EARLY (diff +0.030)
- beale_letter1: mean distance to 1805-1846 samples 1.058, to 1858-1900 samples 1.092 -> looks EARLY (diff +0.035)
- narrative: mean distance to 1805-1846 samples 1.002, to 1858-1900 samples 0.992 -> looks LATE (diff -0.010)
- morriss: mean distance to 1805-1846 samples 1.328, to 1858-1900 samples 1.316 -> looks LATE (diff -0.013)

## cosine_delta_char4gram_2000

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.65 (n=115). Same-author pairs: mean 0.845 (sd 0.112, n=203); different-author pairs: mean 1.014 (sd 0.072, n=6352). Cross-genre (letters vs other) different-author mean 1.023 (n=2688); cross-genre same-author mean 0.885 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.655 | -4.96 | 0.0 | 7.9 | 0.000 | 147.12 |
| beale_letters_2000 vs narrative_2000 | 0.742 | -3.75 | 0.2 | 17.7 | 0.002 | 24.74 |
| beale_letter1 vs narrative_2000 | 0.737 | -3.83 | 0.1 | 16.7 | 0.001 | 28.63 |
| beale_letters vs narrative_A | 0.736 | -3.84 | 0.1 | 16.7 | 0.001 | 29.27 |
| beale_letters vs narrative_B | 0.711 | -4.20 | 0.1 | 12.8 | 0.001 | 84.94 |
| narrative_A vs narrative_B | 0.710 | -4.20 | 0.1 | 12.8 | 0.001 | 85.86 |
| morriss vs narrative | 0.705 | -4.27 | 0.1 | 11.8 | 0.001 | 114.88 |
| morriss vs beale_letters | 0.773 | -3.33 | 0.5 | 23.2 | 0.005 | 16.88 |
| beale_b2 vs narrative | 0.994 | -0.27 | 35.1 | 91.1 | 0.351 | 0.34 |
| beale_b2 vs beale_letters | 0.924 | -1.25 | 10.2 | 73.4 | 0.102 | 1.63 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.002 (95% interval 0.000-0.004).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.655, z=-5.14), narrative_B (0.711, z=-4.31), narrative_2000 (0.733, z=-3.99), narrative_A (0.736, z=-3.93), morriss (0.773, z=-3.38)
- **narrative**: beale_letters (0.655, z=-4.52), beale_letter1 (0.680, z=-4.19), beale_letters_2000 (0.692, z=-4.04), morriss (0.705, z=-3.86), cabell_2 (0.834, z=-2.17)
- **morriss**: narrative (0.705, z=-6.04), narrative_B (0.755, z=-5.02), narrative_2000 (0.770, z=-4.70), narrative_A (0.772, z=-4.66), beale_letters (0.773, z=-4.64)
- **beale_letter1**: narrative (0.680, z=-4.97), narrative_2000 (0.737, z=-4.09), narrative_A (0.741, z=-4.03), narrative_B (0.746, z=-3.95), morriss (0.787, z=-3.30)
- **poe_goldbug_1**: bagby_4 (0.797, z=-2.35), randolph_4 (0.798, z=-2.34), twain_letters_4 (0.808, z=-2.22), cable_2 (0.833, z=-1.95), poe_letters_1 (0.833, z=-1.95)
- **poe_letters_1**: randolph_2 (0.793, z=-2.46), randolph_1 (0.805, z=-2.33), twain_letters_4 (0.825, z=-2.11), jackson_3 (0.828, z=-2.07), lee_3 (0.829, z=-2.06)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.723, jefferson 0.911, pattie 0.924, davis 0.932, randolph 0.944, jackson 0.947
- **beale_letters_2000**: NARRATIVE(1885) 0.752, pattie 0.907, jefferson 0.923, davis 0.924, gregg 0.953, flint 0.966
- **narrative**: BEALE LETTERS 0.655, cabell 0.888, jqadams 0.897, davis 0.920, poe 0.924, eggleston 0.931
- **morriss**: NARRATIVE(1885) 0.763, jackson 0.931, lee 0.940, randolph 0.943, poe 0.954, cabell 0.957

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.78 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.979, to 1858-1900 samples 1.022 -> looks EARLY (diff +0.044)
- beale_letters_2000: mean distance to 1805-1846 samples 0.980, to 1858-1900 samples 1.019 -> looks EARLY (diff +0.039)
- beale_letter1: mean distance to 1805-1846 samples 0.980, to 1858-1900 samples 1.020 -> looks EARLY (diff +0.040)
- narrative: mean distance to 1805-1846 samples 1.006, to 1858-1900 samples 0.996 -> looks LATE (diff -0.010)
- morriss: mean distance to 1805-1846 samples 1.003, to 1858-1900 samples 0.997 -> looks LATE (diff -0.006)

## cosine_raw_char4gram_2000

Leave-one-out nearest-neighbour attribution accuracy on controls: 0.53 (n=115). Same-author pairs: mean 0.111 (sd 0.044, n=203); different-author pairs: mean 0.151 (sd 0.055, n=6352). Cross-genre (letters vs other) different-author mean 0.160 (n=2688); cross-genre same-author mean 0.151 (n=18).

| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |
|---|---|---|---|---|---|---|
| beale_letters vs narrative | 0.084 | -1.23 | 4.6 | 33.5 | 0.046 | 1.92 |
| beale_letters_2000 vs narrative_2000 | 0.110 | -0.76 | 24.6 | 53.7 | 0.246 | 1.03 |
| beale_letter1 vs narrative_2000 | 0.112 | -0.72 | 26.5 | 55.2 | 0.265 | 1.02 |
| beale_letters vs narrative_A | 0.118 | -0.61 | 31.6 | 63.1 | 0.316 | 0.99 |
| beale_letters vs narrative_B | 0.095 | -1.03 | 11.5 | 42.4 | 0.115 | 1.23 |
| narrative_A vs narrative_B | 0.096 | -1.01 | 12.0 | 42.9 | 0.120 | 1.21 |
| morriss vs narrative | 0.105 | -0.84 | 20.8 | 49.8 | 0.208 | 1.05 |
| morriss vs beale_letters | 0.157 | +0.11 | 62.7 | 84.7 | 0.627 | 0.54 |
| beale_b2 vs narrative | 0.323 | +3.15 | 98.9 | 100.0 | 0.989 | 0.00 |
| beale_b2 vs beale_letters | 0.317 | +3.04 | 98.7 | 100.0 | 0.987 | 0.00 |

Author-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = 0.246 (95% interval 0.166-0.339).

Nearest neighbours (5 closest samples; distance, z within the row over control samples):

- **beale_letters**: narrative (0.084, z=-2.02), narrative_B (0.095, z=-1.69), jefferson_2 (0.099, z=-1.60), jackson_3 (0.103, z=-1.48), flint_1 (0.103, z=-1.47)
- **narrative**: jefferson_1 (0.078, z=-1.31), cooke_lee_4 (0.080, z=-1.26), lee_2 (0.082, z=-1.21), jqadams_2 (0.083, z=-1.18), cabell_1 (0.083, z=-1.17)
- **morriss**: narrative (0.105, z=-2.47), narrative_2000 (0.112, z=-2.31), narrative_A (0.114, z=-2.27), lee_4 (0.133, z=-1.80), narrative_B (0.140, z=-1.62)
- **beale_letter1**: narrative (0.085, z=-2.03), jefferson_2 (0.100, z=-1.57), narrative_B (0.100, z=-1.56), hall_3 (0.102, z=-1.52), flint_1 (0.105, z=-1.42)
- **poe_goldbug_1**: randolph_4 (0.107, z=-1.73), bagby_4 (0.113, z=-1.56), twain_letters_2 (0.119, z=-1.41), narrative (0.120, z=-1.37), twain_letters_1 (0.122, z=-1.32)
- **poe_letters_1**: randolph_4 (0.149, z=-1.95), twain_letters_1 (0.157, z=-1.78), lee_3 (0.157, z=-1.78), randolph_2 (0.158, z=-1.77), jackson_3 (0.159, z=-1.75)

Nearest authors (mean distance to that author's control samples; the narrative is included as a candidate author for the letters):

- **beale_letters**: NARRATIVE(1885) 0.107, jackson 0.119, flint 0.123, lee 0.126, jefferson 0.128, paulding 0.129
- **beale_letters_2000**: NARRATIVE(1885) 0.107, flint 0.122, hall 0.128, pattie 0.130, paulding 0.131, irving 0.132
- **narrative**: BEALE LETTERS 0.084, paulding 0.093, jqadams 0.094, hall 0.096, cabell 0.098, eggleston 0.100
- **morriss**: NARRATIVE(1885) 0.127, lee 0.168, cabell 0.173, paulding 0.179, twain 0.184, jackson 0.184

Style-based period classification (nearest period by mean distance, author held out): accuracy on controls 0.72 (n=108).
- beale_letters: mean distance to 1805-1846 samples 0.145, to 1858-1900 samples 0.159 -> looks EARLY (diff +0.014)
- beale_letters_2000: mean distance to 1805-1846 samples 0.148, to 1858-1900 samples 0.159 -> looks EARLY (diff +0.011)
- beale_letter1: mean distance to 1805-1846 samples 0.147, to 1858-1900 samples 0.159 -> looks EARLY (diff +0.012)
- narrative: mean distance to 1805-1846 samples 0.123, to 1858-1900 samples 0.125 -> looks EARLY (diff +0.002)
- morriss: mean distance to 1805-1846 samples 0.212, to 1858-1900 samples 0.198 -> looks LATE (diff -0.013)

## Function words that make the Beale letters and the narrative alike (150 function words; z-scores vs control samples)

| word | z letters | z narrative | product |
|---|---|---|---|
| until | +2.66 | +3.57 | 9.48 |
| myself | +1.45 | +3.23 | 4.68 |
| such | +2.69 | +1.49 | 4.00 |
| may | +1.68 | +2.00 | 3.37 |
| each | +3.93 | +0.83 | 3.27 |
| will | +3.36 | +0.60 | 2.02 |
| be | +3.45 | +0.54 | 1.87 |
| might | +1.86 | +0.98 | 1.82 |
| this | +1.36 | +1.33 | 1.81 |
| on | -1.11 | -1.55 | 1.72 |
| to | +1.48 | +1.08 | 1.60 |
| once | +2.62 | +0.59 | 1.54 |
| can | +0.92 | +1.61 | 1.47 |
| my | +1.06 | +1.35 | 1.43 |
| as | +0.74 | +1.75 | 1.28 |
| all | +1.14 | +0.98 | 1.11 |
| ever | +0.55 | +1.99 | 1.10 |
| with | +0.78 | +1.16 | 0.90 |
| about | -0.98 | -0.89 | 0.87 |
| its | +0.98 | +0.82 | 0.81 |
| which | +0.81 | +0.98 | 0.80 |
| very | -0.93 | -0.82 | 0.76 |
| both | -0.86 | -0.86 | 0.74 |
| yet | -0.85 | -0.85 | 0.73 |
| down | -0.85 | -0.85 | 0.73 |

Function words where they differ most (opposite signs):

| word | z letters | z narrative | product |
|---|---|---|---|
| being | +1.39 | -0.45 | -0.63 |
| those | -1.02 | +0.63 | -0.65 |
| much | -0.97 | +0.69 | -0.67 |
| under | +1.05 | -0.66 | -0.69 |
| no | -0.66 | +1.09 | -0.72 |
| you | +2.02 | -0.51 | -1.03 |
| nor | -0.73 | +1.46 | -1.07 |
| our | +1.67 | -0.64 | -1.07 |
| could | -0.89 | +1.23 | -1.09 |
| him | -0.73 | +1.53 | -1.12 |
| his | -0.97 | +1.19 | -1.15 |
| he | -1.16 | +1.37 | -1.59 |

## Genre-matched period test (function words): mean distance of each text to letter-genre controls only

Early letters: ['flint', 'hall', 'jackson', 'jefferson', 'paulding', 'randolph']; late letters: ['lee', 'poe_letters', 'twain_letters']

- beale_letters: to early letters 0.916, to late letters 0.962 (EARLY, diff +0.046)
- beale_letters_2000: to early letters 0.954, to late letters 1.012 (EARLY, diff +0.058)
- narrative: to early letters 0.935, to late letters 0.877 (LATE, diff -0.058)
- morriss: to early letters 0.983, to late letters 0.951 (LATE, diff -0.032)
- control accuracy of this letters-only period test (author held out): 0.70 (n=33)
