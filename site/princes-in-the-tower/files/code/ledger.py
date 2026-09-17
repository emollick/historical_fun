"""
Evidence ledger for the Princes in the Tower.

Outcomes
  H1   both boys died in 1483 while in Richard III's custody (whoever did it, however)
  H2a  Edward V survived to adulthood (Richard did not)
  H2b  Richard of York survived to adulthood (Edward did not)
  H2c  both survived
  H3   something else: died in 1484-85 under Richard; died under Henry VII after Aug 1485;
       or died abroad as children without ever becoming claimants

The evidence is grouped into five CLUSTERS. Items inside a cluster are correlated (the
1483 rumour reported by Mancini, Crowland and Rochefort is largely one rumour), so each
cluster carries ONE judgement of P(cluster | outcome). Multiplying twelve "independent"
items would overstate the case; this version deliberately does not.

Numbers are judgements, not measurements. Their job is to make the weighing explicit and
to show how far the verdict moves when a judgement is changed. A final 10% mixture with a
flat distribution stands in for unknown unknowns (a misread or forged document on either
side, a lost source) and keeps the ledger from asserting more certainty than a
documentary case can carry.
"""

H = ["H1", "H2a", "H2b", "H2c", "H3"]
PRIOR = {"H1": 0.40, "H2a": 0.10, "H2b": 0.10, "H2c": 0.10, "H3": 0.30}
# Prior: every deposed English king held in custody since 1327 (Edward II, Richard II,
# Henry VI) died there within about two years; Arthur of Brittany (1203) is the precedent
# for a boy heir. That tilts toward death in custody but not to 1483 in particular, and the
# bastardy act gave Richard a reason to think he could afford to keep them alive.

CLUSTERS = [
    ("C1  1483: withdrawn from view, belief in London by Dec 1483 that they were dead (Mancini), "
     "rebels turn to Tudor and Elizabeth Woodville backs the Tudor match (Crowland, Rennes oath), "
     "Rochefort's speech (Jan 1484), the 1484 oath covering daughters only; Richard never produces them",
     {"H1": 0.85, "H2a": 0.15, "H2b": 0.15, "H2c": 0.12, "H3": 0.20},
     "The decisive cluster. A living, producible nephew was the obvious rebuttal to a rumour that "
     "was costing Richard his southern support; none came in two years."),
    ("C2  Henry VII 1485-1502: 'shedding of infants' blood' in the attainder but no bodies, no inquest, "
     "no official narrative; repeals Titulus Regius and marries Elizabeth of York",
     {"H1": 0.60, "H2a": 0.45, "H2b": 0.50, "H2c": 0.40, "H3": 0.40},
     "Weak either way. Under 'Henry the killer' (part of H3) Potter's point applies: he would have "
     "produced corpses and a story blaming Richard."),
    ("C3  The 1487 claimant: Symonds's confession, Warwick exhibited, Henry's letter to the Pope, York "
     "House Books 'Edward the vjt', Irish exchequer 'first year of Edward VI', Butler patent 'anno primo', "
     "Voorne and Mechelen accounts and Molinet ('son of Clarence') -- against the Lille receipt and Andre",
     {"H1": 0.30, "H2a": 0.03, "H2b": 0.30, "H2c": 0.03, "H3": 0.30},
     "0.30 rather than higher because the Lille receipt and Andre are a real cost to every outcome in "
     "which Edward V was not the Dublin king; 0.03 because under 'Edward V was the Dublin king' the "
     "Irish regnal year alone is close to disqualifying."),
    ("C4  'Perkin Warbeck': Setubal depositions (Apr 1496, before capture), Tournai records, 1497 "
     "confession, no recognition by anyone who had known Richard of York; against: the Gelderland "
     "narrative, Margaret's and Maximilian's recognition, the papal indult, the Dresden pledge",
     {"H1": 0.60, "H2a": 0.60, "H2b": 0.10, "H2c": 0.10, "H3": 0.60},
     "A pretender's court generates recognitions and a first-person escape story as a matter of "
     "course; the Portuguese depositions predate Henry's custody of the man and are the hard part "
     "for H2b."),
    ("C5  Traces of death: More's narrative with Thornton's finds (Forest's sons at court; Edward V's "
     "chain with Tyrell's in-laws by 1516); the 1674 bones (two juveniles, unsexed, undated)",
     {"H1": 0.35, "H2a": 0.12, "H2b": 0.12, "H2c": 0.08, "H3": 0.25},
     "Suggestive, not probative: no DNA, no date, no confession text; but two children's skeletons "
     "where More said the bodies were first laid is not nothing."),
]

def normalise(d):
    z = sum(d.values()); return {k: v / z for k, v in d.items()}

def posterior(prior, clusters, skip=None, soften=None):
    post = dict(prior)
    for i, (label, lik, _) in enumerate(clusters):
        if skip == i: continue
        for h in H:
            p = lik[h]
            if soften is not None and i in soften[0]:
                p = p ** soften[1]          # pull ratios toward 1 (exponent 0 = no evidence)
            post[h] *= p
    return normalise(post)

def robust(p, w=0.10):
    flat = {h: 1 / len(H) for h in H}
    return {h: (1 - w) * p[h] + w * flat[h] for h in H}

def show(tag, p):
    surv = p["H2a"] + p["H2b"] + p["H2c"]
    print(f"{tag:<52} H1 {p['H1']:.3f}   survived {surv:.3f} (Ed {p['H2a']:.3f}, Ric {p['H2b']:.3f}, both {p['H2c']:.3f})   H3 {p['H3']:.3f}")

if __name__ == "__main__":
    show("Prior", PRIOR)
    raw = posterior(PRIOR, CLUSTERS)
    show("Ledger posterior (raw)", raw)
    rob = robust(raw)
    show("With 10% unknown-unknowns mixture (REPORTED)", rob)
    print()
    print("Sensitivity (raw, then mixed): drop one cluster at a time")
    for i, c in enumerate(CLUSTERS):
        p = posterior(PRIOR, CLUSTERS, skip=i)
        show(f"  drop {c[0][:3]}", robust(p))
    print()
    print("Survival-friendly reading: halve the log-strength of C1, C3 and C4")
    show("  softened", robust(posterior(PRIOR, CLUSTERS, soften=((0, 2, 3), 0.5))))
    print("Flat prior (1/5 each)")
    show("  flat prior", robust(posterior({h: 0.2 for h in H}, CLUSTERS)))
    print("No mixture at all (raw ledger, flat prior)")
    show("  raw, flat prior", posterior({h: 0.2 for h in H}, CLUSTERS))
