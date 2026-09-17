# Evidence model output (Hannibal's pass)

## Point estimate (geometric midpoints) with Monte-Carlo 5–95% bands (n=20000)

| Candidate | prior | point | p05 | p50 | p95 | leads in draws |
|---|---:|---:|---:|---:|---:|---:|
| Clapier | 0.14 | 69.9% | 35.9% | 66.8% | 87.8% | 91.1% |
| Traversette | 0.14 | 19.4% | 5.2% | 18.4% | 47.5% | 8.1% |
| Mont-Cenis | 0.14 | 7.8% | 1.9% | 7.2% | 24.0% | 0.5% |
| Other col | 0.14 | 2.6% | 0.4% | 2.3% | 13.9% | 0.3% |
| Petit-St-Bernard | 0.12 | 0.1% | 0.0% | 0.1% | 0.5% | 0.0% |
| Larche | 0.12 | 0.1% | 0.0% | 0.1% | 0.5% | 0.0% |
| Montgenevre | 0.14 | 0.1% | 0.0% | 0.1% | 0.3% | 0.0% |
| Grand-St-Bernard | 0.06 | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |

## Likelihood table (point values; ranges in evidence_table.py)

| Item | Traversette | Clapier | Mont-Cenis | Montgenevre | Larche | Petit-St-Bernard | Grand-St-Bernard | Other col |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 The Island: four days beyond a crossing that is itself four days from the sea, at a confluence with a second river (mss Skaras/Skoras; Sarar/Arar), shaped like the Delta, with the Allobroges next to it | 0.39 | 0.84 | 0.84 | 0.39 | 0.39 | 0.84 | 0.77 | 0.60 |
| P2 Then 800 stades in ten days along the river through flat country, escorted through the Allobroges, to the foot of the ascent | 0.42 | 0.89 | 0.89 | 0.42 | 0.42 | 0.84 | 0.09 | 0.60 |
| P3 The first fight is with the Allobroges, at the first defile of the ascent, with their town close by | 0.27 | 0.89 | 0.89 | 0.27 | 0.27 | 0.89 | 0.57 | 0.49 |
| P4 Nine days from the foot of the ascent to the summit, with a battle, a captured town, a halt, a second ambush and a night in a gorge | 0.77 | 0.89 | 0.89 | 0.77 | 0.77 | 0.89 | 0.71 | 0.71 |
| P5 The plains of the Po are pointed out from the summit camp (Polybius) or from a promontory on the first descent morning (Livy) | 0.89 | 0.62 | 0.17 | 0.10 | 0.10 | 0.10 | 0.10 | 0.22 |
| P6 Old snow from the previous winter lies under the new snow on the descent, at the setting of the Pleiades (29 Oct to 9 Nov) | 0.89 | 0.42 | 0.19 | 0.08 | 0.11 | 0.19 | 0.42 | 0.42 |
| P7 The descent is narrow and steeper than the ascent, a cliff-path is broken away for 1.5 stades, and the plain is reached three days below the cliffs | 0.89 | 0.89 | 0.57 | 0.24 | 0.19 | 0.19 | 0.67 | 0.52 |
| P8 He comes down among the Taurini and by "the pass through the Taurini" (Polybius 3.60.8, 34.10.18; Livy 21.38.5-7), not among the Salassi | 0.55 | 0.95 | 0.95 | 0.95 | 0.44 | 0.10 | 0.10 | 0.52 |
| P9 The crossing itself is "about 1,200 stades" (3.39.10) and takes fifteen days | 0.84 | 0.58 | 0.58 | 0.84 | 0.84 | 0.67 | 0.46 | 0.60 |
| L1 Livy: from the Island left into the Tricastini, along the Vocontii into the Tricorii, across the Druentia, then a mostly level road to the Alps | 0.84 | 0.42 | 0.42 | 0.84 | 0.84 | 0.42 | 0.32 | 0.60 |
| T2 Varro lists Hannibal's pass between the coast road and Pompey's; Pompey says his own route was "other than Hannibal's" | 0.84 | 0.53 | 0.53 | 0.26 | 0.84 | 0.27 | 0.35 | 0.71 |
| T3 The Roman tradition Livy rejects: Coelius's Cremonis iugum, the popular Poeninus, Nepos's saltus Graius | 0.57 | 0.57 | 0.57 | 0.57 | 0.57 | 0.84 | 0.77 | 0.57 |
| G1 The Traversette mire and rockfall (Mahaney and colleagues 2010-2026) | 1.00 | 0.87 | 0.87 | 0.87 | 0.87 | 0.87 | 0.87 | 0.87 |
| F1 Practicable in early November for 30,000 men, thousands of animals and 37 elephants, and known as a route (Polybius 3.48.6: Gallic armies had crossed before) | 0.35 | 0.67 | 0.95 | 0.95 | 0.95 | 0.95 | 0.84 | 0.52 |

## Leave-one-out (posterior of each candidate when the item is dropped)

| Item dropped | Traversette | Clapier | Mont-Cenis | Montgenevre | Larche | Petit-St-Bernard | Grand-St-Bernard | Other col |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 The Island: four days beyond a crossing that is itself four days from the sea, at a confluence with a second river (mss Skaras/Skoras; Sarar/Arar), shaped like the Delta, with the Allobroges next to it | 33.9% | 56.5% | 6.3% | 0.1% | 0.2% | 0.1% | 0.0% | 2.9% |
| P2 Then 800 stades in ten days along the river through flat country, escorted through the Allobroges, to the foot of the ascent | 33.2% | 56.8% | 6.4% | 0.1% | 0.2% | 0.1% | 0.1% | 3.1% |
| P3 The first fight is with the Allobroges, at the first defile of the ascent, with their town close by | 43.3% | 47.8% | 5.4% | 0.1% | 0.2% | 0.1% | 0.0% | 3.2% |
| P4 Nine days from the foot of the ascent to the summit, with a battle, a captured town, a halt, a second ambush and a night in a gorge | 21.6% | 67.4% | 7.6% | 0.1% | 0.1% | 0.1% | 0.0% | 3.1% |
| P5 The plains of the Po are pointed out from the summit camp (Polybius) or from a promontory on the first descent morning (Livy) | 11.2% | 58.2% | 23.3% | 0.3% | 0.5% | 0.6% | 0.1% | 5.9% |
| P6 Old snow from the previous winter lies under the new snow on the descent, at the setting of the Pleiades (29 Oct to 9 Nov) | 9.1% | 69.9% | 17.5% | 0.4% | 0.3% | 0.2% | 0.0% | 2.5% |
| P7 The descent is narrow and steeper than the ascent, a cliff-path is broken away for 1.5 stades, and the plain is reached three days below the cliffs | 18.1% | 65.1% | 11.5% | 0.2% | 0.4% | 0.5% | 0.0% | 4.1% |
| P8 He comes down among the Taurini and by "the pass through the Taurini" (Polybius 3.60.8, 34.10.18; Livy 21.38.5-7), not among the Salassi | 28.6% | 59.5% | 6.7% | 0.1% | 0.2% | 0.9% | 0.1% | 4.0% |
| P9 The crossing itself is "about 1,200 stades" (3.39.10) and takes fifteen days | 14.4% | 74.4% | 8.3% | 0.0% | 0.1% | 0.1% | 0.0% | 2.6% |
| L1 Livy: from the Island left into the Tricastini, along the Vocontii into the Tricorii, across the Druentia, then a mostly level road to the Alps | 11.0% | 78.0% | 8.7% | 0.0% | 0.1% | 0.1% | 0.0% | 2.0% |
| T2 Varro lists Hannibal's pass between the coast road and Pompey's; Pompey says his own route was "other than Hannibal's" | 13.3% | 75.7% | 8.5% | 0.1% | 0.1% | 0.2% | 0.0% | 2.1% |
| T3 The Roman tradition Livy rejects: Coelius's Cremonis iugum, the popular Poeninus, Nepos's saltus Graius | 19.4% | 70.0% | 7.8% | 0.1% | 0.1% | 0.1% | 0.0% | 2.6% |
| G1 The Traversette mire and rockfall (Mahaney and colleagues 2010-2026) | 17.2% | 71.8% | 8.0% | 0.1% | 0.1% | 0.1% | 0.0% | 2.6% |
| F1 Practicable in early November for 30,000 men, thousands of animals and 37 elephants, and known as a route (Polybius 3.48.6: Gallic armies had crossed before) | 32.2% | 60.0% | 4.8% | 0.0% | 0.1% | 0.1% | 0.0% | 2.8% |

## Robustness variants

| Variant | Traversette | Clapier | Mont-Cenis | Montgenevre | Larche | Petit-St-Bernard | Grand-St-Bernard | Other col |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| point | 19.4% | 69.9% | 7.8% | 0.1% | 0.1% | 0.1% | 0.0% | 2.6% |
| polybius_half | 28.7% | 40.0% | 15.9% | 1.4% | 2.8% | 1.5% | 0.3% | 9.3% |
| flat_prior | 19.4% | 69.9% | 7.8% | 0.1% | 0.1% | 0.1% | 0.0% | 2.6% |
| polybius_half_flat_prior | 28.4% | 39.5% | 15.7% | 1.4% | 3.3% | 1.8% | 0.7% | 9.2% |
| collapsed_by_source | 17.3% | 14.5% | 15.5% | 12.6% | 18.0% | 7.6% | 2.3% | 12.2% |
| tempered_half | 24.4% | 46.2% | 15.5% | 1.4% | 1.6% | 1.7% | 0.4% | 8.8% |
| tempered_half_collapsed | 15.8% | 14.4% | 14.9% | 13.4% | 14.9% | 9.6% | 3.8% | 13.2% |
| scenario: de Beer's Island | 76.2% | 18.5% | 2.1% | 0.3% | 0.4% | 0.0% | 0.1% | 2.6% |
| scenario: view is a topos | 11.2% | 58.2% | 23.3% | 0.3% | 0.5% | 0.6% | 0.1% | 5.9% |
| scenario: snow is a generalisation | 9.1% | 69.9% | 17.5% | 0.4% | 0.3% | 0.2% | 0.0% | 2.5% |
| scenario: Livy's Druentia trusted | 38.9% | 50.5% | 5.7% | 0.1% | 0.2% | 0.1% | 0.0% | 4.5% |
| scenario: numbers distrusted | 16.1% | 72.3% | 8.1% | 0.1% | 0.1% | 0.1% | 0.0% | 3.3% |
| scenario: Mahaney credited | 42.4% | 50.0% | 5.6% | 0.0% | 0.1% | 0.1% | 0.0% | 1.8% |
| scenario: Traversette practicable | 38.3% | 53.5% | 6.0% | 0.1% | 0.1% | 0.1% | 0.0% | 2.0% |

## Headline run: Polybian items at half strength (shared source), others full; Monte-Carlo bands

| Candidate | point | p05 | p50 | p95 | leads in draws |
|---|---:|---:|---:|---:|---:|
| Clapier | 40.0% | 19.7% | 37.8% | 60.0% | 64.6% |
| Traversette | 28.7% | 12.6% | 26.9% | 48.2% | 28.8% |
| Mont-Cenis | 15.9% | 6.3% | 14.8% | 30.8% | 4.6% |
| Other col | 9.3% | 2.8% | 8.7% | 24.2% | 2.0% |
| Larche | 2.8% | 1.0% | 2.6% | 6.5% | 0.0% |
| Petit-St-Bernard | 1.5% | 0.5% | 1.4% | 4.0% | 0.0% |
| Montgenevre | 1.4% | 0.4% | 1.3% | 3.7% | 0.0% |
| Grand-St-Bernard | 0.3% | 0.1% | 0.3% | 0.8% | 0.0% |

### Headline run, leave-one-out

| Item dropped | Traversette | Clapier | Mont-Cenis | Montgenevre | Larche | Petit-St-Bernard | Grand-St-Bernard | Other col |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 The Island: four days beyond a crossing that is itself four days from the sea, at a confluence with a second river (mss Skaras/Skoras; Sarar/Arar), shaped like the Delta, with the Allobroges next to it | 36.0% | 34.1% | 13.6% | 1.8% | 3.6% | 1.3% | 0.3% | 9.3% |
| P2 Then 800 stades in ten days along the river through flat country, escorted through the Allobroges, to the foot of the ascent | 35.4% | 34.0% | 13.5% | 1.8% | 3.5% | 1.4% | 0.8% | 9.6% |
| P3 The first fight is with the Allobroges, at the first defile of the ascent, with their town close by | 39.9% | 30.8% | 12.2% | 2.0% | 3.9% | 1.2% | 0.3% | 9.6% |
| P4 Nine days from the foot of the ascent to the summit, with a battle, a captured town, a halt, a second ambush and a night in a gorge | 29.8% | 38.6% | 15.4% | 1.5% | 2.9% | 1.5% | 0.3% | 10.0% |
| P5 The plains of the Po are pointed out from the summit camp (Polybius) or from a promontory on the first descent morning (Livy) | 19.2% | 32.1% | 24.2% | 2.9% | 5.7% | 3.1% | 0.6% | 12.4% |
| P6 Old snow from the previous winter lies under the new snow on the descent, at the setting of the Pleiades (29 Oct to 9 Nov) | 18.9% | 38.4% | 22.9% | 3.2% | 5.3% | 2.2% | 0.3% | 8.8% |
| P7 The descent is narrow and steeper than the ascent, a cliff-path is broken away for 1.5 stades, and the plain is reached three days below the cliffs | 25.3% | 35.2% | 17.6% | 2.4% | 5.5% | 3.0% | 0.3% | 10.7% |
| P8 He comes down among the Taurini and by "the pass through the Taurini" (Polybius 3.60.8, 34.10.18; Livy 21.38.5-7), not among the Salassi | 32.2% | 34.0% | 13.6% | 1.2% | 3.5% | 4.0% | 0.8% | 10.6% |
| P9 The crossing itself is "about 1,200 stades" (3.39.10) and takes fifteen days | 25.4% | 42.4% | 16.9% | 1.3% | 2.5% | 1.5% | 0.4% | 9.7% |
| L1 Livy: from the Island left into the Tricastini, along the Vocontii into the Tricorii, across the Druentia, then a mostly level road to the Alps | 17.9% | 49.3% | 19.6% | 0.9% | 1.8% | 1.9% | 0.5% | 8.1% |
| T2 Varro lists Hannibal's pass between the coast road and Pompey's; Pompey says his own route was "other than Hannibal's" | 20.4% | 44.9% | 17.9% | 3.3% | 2.0% | 3.3% | 0.5% | 7.8% |
| T3 The Roman tradition Livy rejects: Coelius's Cremonis iugum, the popular Poeninus, Nepos's saltus Graius | 28.9% | 40.2% | 16.0% | 1.4% | 2.9% | 1.0% | 0.2% | 9.3% |
| G1 The Traversette mire and rockfall (Mahaney and colleagues 2010-2026) | 25.9% | 41.6% | 16.6% | 1.5% | 2.9% | 1.6% | 0.3% | 9.6% |
| F1 Practicable in early November for 30,000 men, thousands of animals and 37 elephants, and known as a route (Polybius 3.48.6: Gallic armies had crossed before) | 45.2% | 32.5% | 9.1% | 0.8% | 1.6% | 0.9% | 0.2% | 9.7% |

### Headline run, scenarios

| Scenario | Traversette | Clapier | Mont-Cenis | Montgenevre | Larche | Petit-St-Bernard | Grand-St-Bernard | Other col |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| de Beer's Island | 54.3% | 19.6% | 7.8% | 2.7% | 5.4% | 0.8% | 0.6% | 8.8% |
| view is a topos | 19.2% | 32.1% | 24.2% | 2.9% | 5.7% | 3.1% | 0.6% | 12.4% |
| snow is a generalisation | 18.9% | 38.4% | 22.9% | 3.2% | 5.3% | 2.2% | 0.3% | 8.8% |
| Livy's Druentia trusted | 46.4% | 23.3% | 9.3% | 2.3% | 4.6% | 0.9% | 0.1% | 13.2% |
| numbers distrusted | 26.4% | 41.0% | 16.3% | 1.3% | 2.6% | 1.5% | 0.4% | 10.5% |
| Mahaney credited | 55.2% | 25.1% | 10.0% | 0.9% | 1.8% | 1.0% | 0.2% | 5.8% |
| Traversette practicable | 51.0% | 27.5% | 10.9% | 1.0% | 1.9% | 1.1% | 0.2% | 6.4% |

## Best-case share (candidate at its high ends, rivals at their low ends)

- Traversette: 99.7%
- Clapier: 100.0%
- Mont-Cenis: 99.2%
- Montgenevre: 81.5%
- Larche: 85.6%
- Petit-St-Bernard: 82.8%
- Grand-St-Bernard: 53.6%
- Other col: 99.8%

## Factor by which a rival's total case must strengthen to tie the leader (Clapier)

- Traversette: ×3.6
- Mont-Cenis: ×8.9
- Other col: ×27.3
- Petit-St-Bernard: ×628.2
- Larche: ×752.7
- Montgenevre: ×1066.1
- Grand-St-Bernard: ×6218.4
