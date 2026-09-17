#!/usr/bin/env python3
"""
Likelihood-ratio model for the referent of the "Hanging Garden of Babylon".

Hypotheses (mutually exclusive):
  B  a real raised palace garden at Babylon lies behind the tradition (most
     plausibly on the terraces of Nebuchadnezzar II's North Palace; a
     Persian-period garden on the same spot also counts), however much the
     telling exaggerated it or borrowed Assyrian colour;
  N  Sennacherib's palace garden at Nineveh lies behind it (Dalley's thesis),
     relocated to Babylon by confusion in the Greek tradition;
  0  no single real structure lies behind it: a literary construct.

The evidence is grouped into seven CLUSTERS.  Items inside a cluster are
correlated (they would rise and fall together), so each cluster gets ONE
likelihood triple P(E|B), P(E|N), P(E|0); treating the thirteen underlying
items as independent would overstate the case.  All numbers are judgements, stated
so that anyone can change them and rerun:  python3 likelihood_model.py
"""
import json, sys

CLUSTERS = [
 ("C1", "Location testimony of the Greek tradition",
  ["Every Greek and Latin source that names a city puts the garden in Babylon: the Clitarchus-derived accounts "
   "(Diodorus 2.10, Curtius 5.1.31-35), Strabo 16.1.5, Berossus/Abydenus; Philo names no city, and Antipater of Sidon "
   "names Babylon only for the wall beside the gardens",
   "Greek writers from Herodotus 1.178 on distinguish Babylon from the dead city of Ninus; Xenophon saw Nineveh "
   "deserted in 401 BC (Anab. 3.4.10-12); the descriptions present a working garden in Alexander's Babylon",
   "No Neo-Assyrian text calls Nineveh 'Babylon'; the 'old Babylon' latitude datum is an 11th-century Arabic "
   "tract (Bichler-Rollinger 2005, 179-181); Sennacherib's cult transfers concern Assur, not Nineveh"],
  0.90, 0.12, 0.75),
 ("C2", "Berossus",
  ["Berossus (c. 290 BC), a Babylonian priest demonstrably using Nebuchadnezzar's inscriptions (the 'fifteen days'), "
   "places the 'hanging paradeisos' of high stone terraces in Nebuchadnezzar's new palace (Josephus, Ap. 1.141 = "
   "Ant. 10.226; Abydenus in Eusebius, PE 9.41)",
   "Nebuchadnezzar's own text on that palace describes a 'kummu of large gigunu-terraces' raised 'as high as a "
   "mountain' (RINBE 1/1 Nbk. 21 ii 33-35; Nbk. 2 viii 27-ix 2), which CAD G 70 already said 'could well have been "
   "interpreted as a hanging garden'"],
  0.80, 0.20, 0.35),
 ("C3", "The Babylonian blank",
  ["No Neo-Babylonian royal inscription mentions a garden at Babylon (RINBE 1/1, 2024: 'nor in any other extant text of "
   "Nebuchadnezzar'; the corpus's two occurrences of kiru are Nabonidus' orchards at Ur and a funerary offering)",
   "Nothing identifiable has been excavated at Babylon; Koldewey's vaulted building is a storeroom; the North Palace "
   "slopes and riverside are denuded and largely unexcavated",
   "Herodotus, Xenophon's Cyropaedia and the eyewitness Alexander stratum (Arrian; the Ephemerides in Plutarch, "
   "Alex. 76) are silent; only Clitarchus and Berossus/Abydenus carry the garden"],
  0.30, 0.95, 0.90),
 ("C4", "The Nineveh match, net of what is missing",
  ["Sennacherib documents a palace garden 'a replica of Mount Amanus', water raised from wells by a novel cast-copper "
   "installation, canals and aqueducts (RINAP 3/1 no. 17 vii 45-57; Jerwan); reliefs show an aqueduct on arches into "
   "a planted hillside (BM 124939) and a pillared walkway roofed with trees (Or. Dr. IV 77)",
   "But his detailed accounts never describe terraces, vaults or a raised substructure; the 'wonder for all peoples' "
   "is the palace (no. 17 vii 50-52); the Amanus formula is reused by Esarhaddon (RINAP 4 no. 1 vi 30-34); the "
   "relief shows a hillside and an aqueduct, not tiered vaults (Reade 2000; Bichler-Rollinger 2005)"],
  0.50, 0.70, 0.45),
 ("C5", "Builder and wife",
  ["Nebuchadnezzar for his Median wife (Berossus); 'a later Syrian king reigning at Babylon' for a Persian concubine "
   "(Clitarchus): Nebuchadnezzar's Median marriage is credible, Sennacherib's queens (Tashmetu-sharrat, Naqia) are not Median",
   "but 'Syrian' means Assyrian (Strabo 16.1.2) and fits any Sargonid who held Babylon, so the attribution itself is "
   "only mildly discriminating. Building materials (the baked brick and bitumen of Strabo and Diodorus) are "
   "not counted, because they do not discriminate: Sennacherib's own "
   "palace account has the terrace foundation bonded with bitumen under a bed of reeds (RINAP 3/1 no. 17 v 86-vi 1; "
   "no. 16 vi 19b-21a) and culverts of baked brick under the city wall (no. 16 vii 81-84), and baked brick with "
   "bitumen is attested archaeologically at Nineveh (Viggiano)."],
  0.55, 0.40, 0.50),
 ("C6", "The screws",
  ["Strabo's and Philo's kochliai versus Sennacherib's copper 'tree trunks and date palms' set over wells for "
   "bucket-drawn water (dilutu): the screw reading is conjectural (CAD A/1 and M/1; RINAP 3/1 note 49; Bagg 2000), "
   "and the Greek screw is probably Hellenistic technology (Oleson in Dalley-Oleson 2003, 14)"],
  0.45, 0.50, 0.45),
 ("C7", "A watered garden at the North Palace in Persian times",
  ["A Persian-period Babylon text lists gardeners (nukaribbu) and water-drawers (dalu) for the 'new palace' "
   "(Abraham 2004 no. 18, via Pedersen 2021, 121)"],
  0.80, 0.60, 0.60),
]

HYP = ["Babylon", "Nineveh", "No single structure"]

def posterior(clusters, prior):
    w = list(prior)
    for c in clusters:
        pb, pn, p0 = c[3], c[4], c[5]
        w[0] *= pb; w[1] *= pn; w[2] *= p0
    s = sum(w)
    return [x / s for x in w]

def fmt(p):
    return "  ".join(f"{h}: {x*100:5.1f}%" for h, x in zip(HYP, p))

def modify(clusters, changes):
    out = []
    for c in clusters:
        cid, name, items, pb, pn, p0 = c
        if cid in changes:
            pb, pn, p0 = changes[cid]
        out.append((cid, name, items, pb, pn, p0))
    return out

def main():
    flat = (1/3, 1/3, 1/3)
    base = posterior(CLUSTERS, flat)
    print("Base case (flat priors):\n  " + fmt(base))
    print("\nLikelihood ratios per cluster (N:B, 0:B):")
    for cid, name, items, pb, pn, p0 in CLUSTERS:
        print(f"  {cid} {name:48s} N/B = {pn/pb:5.2f}   0/B = {p0/pb:5.2f}")
    print("\nAlternative priors:")
    for name, pr in [("Babylon-leaning (0.45,0.20,0.35)", (0.45,0.20,0.35)),
                     ("Nineveh-leaning (0.30,0.40,0.30)", (0.30,0.40,0.30)),
                     ("Sceptic-leaning (0.30,0.20,0.50)", (0.30,0.20,0.50))]:
        print(f"  {name:36s} " + fmt(posterior(CLUSTERS, pr)))
    print("\nLeave-one-cluster-out (flat priors):")
    for i, c in enumerate(CLUSTERS):
        print(f"  without {c[0]}  " + fmt(posterior(CLUSTERS[:i] + CLUSTERS[i+1:], flat)))
    print("\nDalley-favourable world: Berossus' garden sentence an interpolation (C2 N=0.6), the screw reading accepted")
    print("(C6 B=0.30 N=0.85 0=0.30), Greek confusion granted and Nineveh not wholly abandoned (C1 N=0.35):")
    dal = modify(CLUSTERS, {"C2": (0.80, 0.60, 0.35), "C6": (0.30, 0.85, 0.30), "C1": (0.90, 0.35, 0.75)})
    print("  " + fmt(posterior(dal, flat)))
    print("\nWhat would put Nineveh ahead: additionally a Nineveh text or relief showing vaulted, tiered terraces")
    print("(C4 N=0.95) and the builder-and-wife cluster read as neutral (C5 0.5/0.5/0.5):")
    dal2 = modify(dal, {"C4": (0.50, 0.95, 0.45), "C5": (0.50, 0.50, 0.50)})
    print("  " + fmt(posterior(dal2, flat)))
    out = {"hypotheses": HYP, "base_posterior": base,
           "clusters": [dict(id=c[0], name=c[1], items=c[2], P_B=c[3], P_N=c[4], P_0=c[5]) for c in CLUSTERS],
           "dalley_favourable": posterior(dal, flat), "nineveh_ahead_scenario": posterior(dal2, flat)}
    with open(sys.argv[1] if len(sys.argv) > 1 else "likelihood_results.json", "w") as f:
        json.dump(out, f, indent=1)

if __name__ == "__main__":
    main()
