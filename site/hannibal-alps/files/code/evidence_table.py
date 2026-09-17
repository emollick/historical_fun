"""Hannibal's pass: the evidence table (judgements argued in the report; edit and re-run evidence_model.py).

Scale: each cell is P(evidence | candidate) on a relative scale in which the best-fitting candidate sits near 1.0
and a candidate the item nearly excludes sits near 0.05. Written as (low, high) ranges.
"""
CANDS = ['Traversette', 'Clapier', 'Mont-Cenis', 'Montgenevre', 'Larche', 'Petit-St-Bernard', 'Grand-St-Bernard', 'Other col']
SHORT = {'Traversette': 'Traversette', 'Clapier': 'Clapier', 'Mont-Cenis': 'Mont-Cenis', 'Montgenevre': 'Montgenèvre',
         'Larche': 'Larche', 'Petit-St-Bernard': 'Petit St B.', 'Grand-St-Bernard': 'Grand St B.', 'Other col': 'Other col'}

# Prior. The six named cols are the ones the literature has proposed for two centuries; the Grand-Saint-Bernard is
# kept because it was the ancient "common belief" (Livy 21.38.6); "Other col" covers Agnel, the Autaret/Arnas group,
# the Echelle, Bousson, the Seigne and any col nobody has argued for.
PRIOR = {'Traversette': 0.14, 'Clapier': 0.14, 'Mont-Cenis': 0.14, 'Montgenevre': 0.14, 'Larche': 0.12,
         'Petit-St-Bernard': 0.12, 'Grand-St-Bernard': 0.06, 'Other col': 0.14}

T, C, M, G, L, P, B, O = CANDS

EVIDENCE = {
 # ---- Family P: the Polybian narrative (Livy repeats it) ----
 'P1 The Island: four days beyond a crossing that is itself four days from the sea, at a confluence with a second river (mss Skaras/Skoras; Sarar/Arar), shaped like the Delta, with the Allobroges next to it': {
   T: (0.25, 0.6), C: (0.7, 1.0), M: (0.7, 1.0), G: (0.25, 0.6), L: (0.25, 0.6), P: (0.7, 1.0), B: (0.6, 1.0), O: (0.4, 0.9)},
 'P2 Then 800 stades in ten days along the river through flat country, escorted through the Allobroges, to the foot of the ascent': {
   T: (0.3, 0.6), C: (0.8, 1.0), M: (0.8, 1.0), G: (0.3, 0.6), L: (0.3, 0.6), P: (0.7, 1.0), B: (0.05, 0.15), O: (0.4, 0.9)},
 'P3 The first fight is with the Allobroges, at the first defile of the ascent, with their town close by': {
   T: (0.15, 0.5), C: (0.8, 1.0), M: (0.8, 1.0), G: (0.15, 0.5), L: (0.15, 0.5), P: (0.8, 1.0), B: (0.4, 0.8), O: (0.3, 0.8)},
 'P4 Nine days from the foot of the ascent to the summit, with a battle, a captured town, a halt, a second ambush and a night in a gorge': {
   T: (0.6, 1.0), C: (0.8, 1.0), M: (0.8, 1.0), G: (0.6, 1.0), L: (0.6, 1.0), P: (0.8, 1.0), B: (0.5, 1.0), O: (0.5, 1.0)},
 'P5 The plains of the Po are pointed out from the summit camp (Polybius) or from a promontory on the first descent morning (Livy)': {
   T: (0.8, 1.0), C: (0.45, 0.85), M: (0.1, 0.3), G: (0.05, 0.2), L: (0.05, 0.2), P: (0.05, 0.2), B: (0.05, 0.2), O: (0.1, 0.5)},
 'P6 Old snow from the previous winter lies under the new snow on the descent, at the setting of the Pleiades (29 Oct to 9 Nov)': {
   T: (0.8, 1.0), C: (0.25, 0.7), M: (0.1, 0.35), G: (0.03, 0.2), L: (0.05, 0.25), P: (0.1, 0.35), B: (0.25, 0.7), O: (0.2, 0.9)},
 'P7 The descent is narrow and steeper than the ascent, a cliff-path is broken away for 1.5 stades, and the plain is reached three days below the cliffs': {
   T: (0.8, 1.0), C: (0.8, 1.0), M: (0.4, 0.8), G: (0.15, 0.4), L: (0.1, 0.35), P: (0.1, 0.35), B: (0.5, 0.9), O: (0.3, 0.9)},
 'P8 He comes down among the Taurini and by "the pass through the Taurini" (Polybius 3.60.8, 34.10.18; Livy 21.38.5-7), not among the Salassi': {
   T: (0.4, 0.75), C: (0.9, 1.0), M: (0.9, 1.0), G: (0.9, 1.0), L: (0.3, 0.65), P: (0.05, 0.2), B: (0.05, 0.2), O: (0.3, 0.9)},
 'P9 The crossing itself is "about 1,200 stades" (3.39.10) and takes fifteen days': {
   T: (0.7, 1.0), C: (0.4, 0.85), M: (0.4, 0.85), G: (0.7, 1.0), L: (0.7, 1.0), P: (0.5, 0.9), B: (0.3, 0.7), O: (0.4, 0.9)},
 # ---- Family L: Livy's own geography ----
 'L1 Livy: from the Island left into the Tricastini, along the Vocontii into the Tricorii, across the Druentia, then a mostly level road to the Alps': {
   T: (0.7, 1.0), C: (0.3, 0.6), M: (0.3, 0.6), G: (0.7, 1.0), L: (0.7, 1.0), P: (0.3, 0.6), B: (0.2, 0.5), O: (0.4, 0.9)},
 # ---- Family T: the other testimonia ----
 'T2 Varro lists Hannibal\'s pass between the coast road and Pompey\'s; Pompey says his own route was "other than Hannibal\'s"': {
   T: (0.7, 1.0), C: (0.35, 0.8), M: (0.35, 0.8), G: (0.15, 0.45), L: (0.7, 1.0), P: (0.15, 0.5), B: (0.2, 0.6), O: (0.5, 1.0)},
 'T3 The Roman tradition Livy rejects: Coelius\'s Cremonis iugum, the popular Poeninus, Nepos\'s saltus Graius': {
   T: (0.4, 0.8), C: (0.4, 0.8), M: (0.4, 0.8), G: (0.4, 0.8), L: (0.4, 0.8), P: (0.7, 1.0), B: (0.6, 1.0), O: (0.4, 0.8)},
 # ---- Family G: physical evidence ----
 'G1 The Traversette mire and rockfall (Mahaney and colleagues 2010-2026)': {
   T: (1.0, 1.0), C: (0.75, 1.0), M: (0.75, 1.0), G: (0.75, 1.0), L: (0.75, 1.0), P: (0.75, 1.0), B: (0.75, 1.0), O: (0.75, 1.0)},
 # ---- Family F: practicability ----
 'F1 Practicable in early November for 30,000 men, thousands of animals and 37 elephants, and known as a route (Polybius 3.48.6: Gallic armies had crossed before)': {
   T: (0.2, 0.6), C: (0.5, 0.9), M: (0.9, 1.0), G: (0.9, 1.0), L: (0.9, 1.0), P: (0.9, 1.0), B: (0.7, 1.0), O: (0.3, 0.9)},
}

FAMILIES = {}
for k in EVIDENCE:
    FAMILIES[k] = {'P': 'Polybius', 'L': 'Livy', 'T': 'Testimonia', 'G': 'Physical', 'F': 'Feasibility'}[k[0]]

NEUTRAL = {c: (0.8, 1.0) for c in CANDS}
SCENARIOS = {
 'de Beer\'s Island': {'override': {k: NEUTRAL for k in EVIDENCE if k[:2] in ('P1', 'P2', 'P3')},
                       'note': 'the Island is the Aygues and "Allobroges" is used loosely, so P1-P3 do not discriminate'},
 'view is a topos': {'override': {k: NEUTRAL for k in EVIDENCE if k[:2] == 'P5'}, 'note': 'the summit view is rhetoric, not observation'},
 'snow is a generalisation': {'override': {k: NEUTRAL for k in EVIDENCE if k[:2] == 'P6'}, 'note': 'the old snow is a stock detail, not evidence for the col\'s height'},
 'Livy\'s Druentia trusted': {'override': {k: {T: (0.9, 1.0), C: (0.1, 0.3), M: (0.1, 0.3), G: (0.9, 1.0), L: (0.9, 1.0), P: (0.1, 0.3), B: (0.05, 0.2), O: (0.4, 0.9)} for k in EVIDENCE if k[:2] == 'L1'},
                              'note': 'Livy\'s Durance itinerary is taken as reliable'},
 'numbers distrusted': {'override': {k: NEUTRAL for k in EVIDENCE if k[:2] in ('P4', 'P9')}, 'note': 'the day-counts and stades are not held against any route'},
 'Mahaney credited': {'override': {k: {T: (1.0, 1.0), C: (0.2, 0.4), M: (0.2, 0.4), G: (0.2, 0.4), L: (0.2, 0.4), P: (0.2, 0.4), B: (0.2, 0.4), O: (0.2, 0.4)} for k in EVIDENCE if k[:2] == 'G1'},
                      'note': 'the mire is accepted as a dated Punic army deposit'},
 'Traversette practicable': {'override': {k: {T: (0.8, 1.0), C: (0.5, 0.9), M: (0.9, 1.0), G: (0.9, 1.0), L: (0.9, 1.0), P: (0.9, 1.0), B: (0.7, 1.0), O: (0.3, 0.9)} for k in EVIDENCE if k[:2] == 'F1'},
                             'note': 'the height and headwall of the Traversette are not held against it'},
}
NOTES = 'Cells are the report author\'s judgements; see the report section "The evidence model" for the argument behind each.'
