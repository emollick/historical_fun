# Calibration of the anachronism count (Google Books en-US-2019, smoothing 0)

Content-word types (function words, proper nouns, <3 letters excluded). "ratio" = mean relative frequency 1780-1821 / mean 1850-1900. "strong" = ratio < 0.05 with a 1850-1900 frequency above 3e-8 (i.e. words that were common later but essentially unattested before 1822).

| text | content types | % absent pre-1822 | % pre-1822 freq < 1e-7 | % ratio < 0.1 | % ratio < 0.25 | % strong | strong examples |
|---|---|---|---|---|---|---|---|
| biddle | 669 | 0.1 | 1.8 | 0.1 | 1.2 | 0.00 |  |
| ejames | 848 | 2.9 | 4.7 | 0.5 | 2.8 | 0.00 |  |
| flint | 787 | 0.5 | 1.1 | 0.1 | 1.0 | 0.00 |  |
| gregg | 896 | 0.6 | 3.1 | 0.3 | 3.5 | 0.22 | ranchero, vaqueros |
| hall | 866 | 0.9 | 1.5 | 0.0 | 2.0 | 0.00 |  |
| irving | 821 | 0.4 | 3.0 | 0.4 | 3.2 | 0.00 |  |
| jackson | 551 | 0.9 | 3.1 | 0.4 | 1.3 | 0.00 |  |
| jefferson | 737 | 0.1 | 1.9 | 0.3 | 0.9 | 0.14 | egoism |
| jqadams | 681 | 0.4 | 1.3 | 0.0 | 0.6 | 0.00 |  |
| paulding | 850 | 1.4 | 2.2 | 0.0 | 1.3 | 0.00 |  |
| pike | 604 | 0.3 | 0.5 | 0.2 | 1.3 | 0.00 |  |
| randolph | 695 | 1.4 | 0.9 | 0.0 | 0.4 | 0.00 |  |
| letters | 708 | 0.1 | 1.0 | 0.8 | 3.4 | 0.28 | stampeding, grizzlies |
| narrative | 960 | 0.5 | 0.5 | 0.2 | 1.5 | 0.00 |  |

ratio_lt_0_1: genuine 1805-1843 controls mean 0.19% (sd 0.16, n=12, max 0.47%); Beale letters 0.85% -> z = +4.1; controls above the letters' value: 0/12

ratio_lt_0_25: genuine 1805-1843 controls mean 1.62% (sd 0.96, n=12, max 3.46%); Beale letters 3.39% -> z = +1.8; controls above the letters' value: 1/12

strong: genuine 1805-1843 controls mean 0.03% (sd 0.07, n=12, max 0.22%); Beale letters 0.28% -> z = +3.6; controls above the letters' value: 0/12

rare_pre1822_lt1e7: genuine 1805-1843 controls mean 2.10% (sd 1.15, n=12, max 4.72%); Beale letters 0.99% -> z = -1.0; controls above the letters' value: 10/12
