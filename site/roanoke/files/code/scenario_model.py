"""
Scenario ledger for the fate of the 1587 Roanoke colonists.

Question modelled
  Where was the PRINCIPAL SEAT of the main body of the colonists in the years after they
  left Roanoke Island (roughly 1588 to 1607)?

Outcomes (exclusive for the main body; parties elsewhere are handled by the separate findings)
  H1  Croatoan: the main body stayed on Hatteras until absorbed or dead
  H2  Albemarle mainland: the main body moved on to the head of Albemarle Sound, the Chowan mouth
      and the Roanoke River country (a Croatoan stage first is compatible), and dispersed there
  H3  Chesapeake: the main body went north to the Chesepian towns (Quinn's thesis)
  H4  Sea: the main body tried to sail home in the pinnace and boats and was lost
  H5  Other: the Pamlico, Tar or Neuse interior; annihilation on or near Roanoke; anything else

The evidence is grouped into CLUSTERS. Items inside a cluster share a source or a channel
(everything Jamestown heard in 1607 to 1608 came through three Powhatan informants in two
months; the slaughter and the survivor stories of 1609 to 1625 are one London informant's
report told three times), so each cluster carries ONE judgement of P(cluster | outcome).
Multiplying twenty "independent" items would overstate the case and this ledger does not.

Numbers are judgements, not measurements. Their job is to make the weighing explicit and to
show how far the verdict moves when a judgement is changed. A final 15% mixture with a flat
distribution stands in for unknown unknowns (a lost relation, a misread legend, an unpublished
site) and keeps the ledger from asserting more certainty than a hearsay case can carry.

Run: python3 code/scenario_model.py   -> data/model_results.json, data/tokens.json
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = ["H1", "H2", "H3", "H4", "H5"]
LABEL = {"H1": "Croatoan (Hatteras)", "H2": "Albemarle mainland (Chowan)", "H3": "Chesapeake",
         "H4": "Sea", "H5": "Other"}
PRIOR = {"H1": 0.20, "H2": 0.28, "H3": 0.20, "H4": 0.10, "H5": 0.22}
# Prior: the colony had to leave Roanoke (a bad harbour, hostile neighbours, no supply). The
# Croatoans were its only friends but had "but little" corn for themselves (Hakluyt 1600 III
# p. 282) and Lane had used the island only as a lookout station; the mainland to the west was
# known from Lane's 1586 voyage and was where Lane had planned to go; the Chesapeake was the seat
# Ralegh had ordered but 130 miles off by Lane's reckoning and inside Powhatan's reach; a sea
# crossing in a pinnace with families and no pilot was the least likely choice.

CLUSTERS = [
    ("C1  The plan: 'remoue 50 miles further vp into the maine presently' (White, Aug 1587); the "
     "fort symbol hidden under the patch at the Chowan mouth on White's 1585-86 map; Lane's 1586 "
     "plan to move by way of the Chowan",
     {"H1": 0.30, "H2": 0.90, "H3": 0.25, "H4": 0.30, "H5": 0.40},
     "This is the only destination the colonists stated. 'The maine' excludes the banks; 50 miles in any "
     "reckoning stays inside the Albemarle basin and does not reach the Chesapeake."),
    ("C2  The departure: CROATOAN carved without a cross, houses taken down, a palisade built, "
     "boats and light guns gone, heavy iron left (White, Aug 1590)",
     {"H1": 0.90, "H2": 0.50, "H3": 0.35, "H4": 0.50, "H5": 0.40},
     "The code names Croatoan as the seat when the word was cut. Under H2 or H3 the carving needs "
     "a Croatoan stage or a party left there, which the code allowed for but did not say."),
    ("C3  Silence at sea: the Spaniards found the harbour empty in July 1588; no vessel of the "
     "colony was ever reported in English or Spanish records, which noted every English sail in "
     "the Indies; the 1602-03 searches never reached the island",
     {"H1": 0.85, "H2": 0.85, "H3": 0.85, "H4": 0.35, "H5": 0.75},
     "This cluster bears mainly on H4: a pinnace that sailed for England or the Indies and left no trace in "
     "either nation's records most likely sank, which is possible but lowers the weight given to H4."),
    ("C4  Jamestown 1607-08: Opechancanough, Powhatan and the Paspahegh weroance report clothed men "
     "at Ocanahonan and Panawicke to the south; the chart's '4 men clothed that came from Roonock "
     "to Ocanahowan'; the Council in 1609: search south, 'more probable then towards the north'",
     {"H1": 0.35, "H2": 0.80, "H3": 0.35, "H4": 0.35, "H5": 0.45},
     "Three informants in two months all pointed inland to the south-west, and none to the banks or the bay. The small number reported fits stragglers under any outcome, which limits the "
     "weight."),
    ("C5  The London informant 1609-12: Powhatan slaughtered the first planted 'vppon the first "
     "arrivall of our Colonie' after they had lived 'twenty and od yeares ... intermixt with those "
     "salvages, and were out of his territory'; survivors fled up the Chowan to a copper-working "
     "weroance who was Powhatan's enemy (Council May 1609; Strachey); Purchas's confession note 1625",
     {"H1": 0.40, "H2": 0.70, "H3": 0.40, "H4": 0.20, "H5": 0.40},
     "This is one channel, recorded three times. Its geography (outside Powhatan's territory, up the Chowan, "
     "copper country to the west) fits H2 and fits H3 only if the Council and Strachey misplaced "
     "the victims. The objects in Purchas's note could have been picked up on Roanoke Island."),
    ("C6  The 1609 searches: Sicklemore at Chowanoke 'found little hope and lesse certainetie'; "
     "Powell and Todkill among the Mangoags heard 'they were all dead'",
     {"H1": 0.70, "H2": 0.45, "H3": 0.70, "H4": 0.75, "H5": 0.65},
     "These are the only field reports, and both are second-hand and negative. If a hundred English had lived twenty "
     "years at the Chowan mouth the Chowanokes should have known more than 'little hope'; H2 is marked down for this."),
    ("C7  The Chesapeake case: Powhatan destroyed the Chesepians for a prophecy 'not many yeares "
     "since' (Strachey p. 101); the boy with yellow hair that George Percy, one of the first Jamestown settlers, saw on the James in 1607",
     {"H1": 0.50, "H2": 0.50, "H3": 0.80, "H4": 0.50, "H5": 0.50},
     "The destruction is a fact of Strachey's text; its link to the colonists is an inference the "
     "text does not make. The boy has other explanations (the Spanish Jesuit mission of 1570-72 on the Chesapeake, Lane's men 1585-86)."),
    ("C8  Hatteras tradition: Lawson 1709, ancestors 'white People, and could talk in a Book', grey "
     "eyes, 'Affinity to the English'; Beverley 1705 'remov'd to Croatan'",
     {"H1": 0.85, "H2": 0.55, "H3": 0.40, "H4": 0.40, "H5": 0.45},
     "The tradition is independent of the Jamestown reports and comes from the Indians' side; but it was recorded 120 years after the event, concerns a community of sixteen men, and comes from a coast where shipwrecked sailors are another possible source of white ancestors."),
    ("C9  Bertie archaeology: English kitchen ceramics of c.1586-1650 types and a few fittings at "
     "two spots on Salmon Creek beside a Native town; no structure, burial or sealed deposit; "
     "no peer-reviewed report",
     {"H1": 0.35, "H2": 0.55, "H3": 0.35, "H4": 0.30, "H5": 0.40},
     "The footprint is where H2 predicts one and is small, which a plough zone and a dispersed "
     "settlement could explain; Lane's men in 1586 or Jamestown-era traders could also explain it."),
    ("C10 Hatteras archaeology: European objects of 16th-century type mostly in 17th-century "
     "contexts; the hammerscale of 2024 with claimed 1580s dates, unpublished",
     {"H1": 0.65, "H2": 0.50, "H3": 0.40, "H4": 0.45, "H5": 0.45},
     "A smithing floor of the 1580s on Croatoan would fit H1 best and a Croatoan stage under H2 "
     "well; everything turns on the date, which is not yet in print."),
    ("C11 Chesapeake archaeology: no sixteenth-century European material at the one fully "
     "reported Chesepian site (Great Neck, Hodges 1998); few sites dug",
     {"H1": 0.70, "H2": 0.70, "H3": 0.45, "H4": 0.70, "H5": 0.70},
     "This is weak evidence: a colony of a hundred for twenty years should have left something, but almost nothing has been excavated."),
]

MIX = 0.15   # unknown-unknowns mixture weight

def normalise(d):
    z = sum(d.values()); return {k: v / z for k, v in d.items()}

def posterior(prior, clusters, skip=(), soften=None):
    post = dict(prior)
    for i, (label, lik, _) in enumerate(clusters):
        if i in skip: continue
        for h in H:
            p = lik[h]
            if soften is not None and i in soften[0]:
                p = p ** soften[1]
            post[h] *= p
    return normalise(post)

def robust(p, w=MIX):
    flat = {h: 1 / len(H) for h in H}
    return {h: (1 - w) * p[h] + w * flat[h] for h in H}

def fmt(p):
    return "  ".join(f"{h} {100*p[h]:5.1f}" for h in H)

# ---------- separate findings (judgements, not multiplied into the ledger) ----------
FINDINGS = [
    ("A", "Some of the colonists went to Croatoan after August 1587 (the carving names it as their seat; arrival is inferred)",
     80, 65, 90,
     "The carved name, under the code White records, names Croatoan as the place where the planters were or meant "
     "to be seated, without the mark of distress (Hakluyt 1600 III, pp. 292 to 293); Manteo's kin had received "
     "Stafford there in July 1587, fifty miles of sheltered water away; Lawson's Hatteras tradition of 1709; "
     "sixteenth-century objects at Cape Creek in unpublished contexts. Against: White never landed there and no "
     "witness records finding them on the island; the sign could name where news of them was to be had; "
     "Lawson's white ancestors have other candidates."),
    ("B", "The colony divided into more than one group at some point",
     75, 60, 85,
     "White's own text names two destinations; Lane had dispersed his colony to eat; every Jamestown report counts a handful, never a hundred; and the two archaeological footprints lie fifty miles apart. "
     "No source states a division."),
    ("C", "Some colonists were killed by Powhatan's people, about 1607",
     45, 30, 60,
     "The killing is stated early (May 1609) and repeatedly, with a date and a place outside Powhatan's territory; but it comes through one channel, it served a Company doctrine that justified seizing priests, and the 'confession' is a 1625 margin note. Smith, who spoke with Powhatan, never wrote it."),
    ("D", "Descendants of colonists lived among the Hatteras Indians in 1709",
     60, 45, 75,
     "Lawson's testimony from the Hatteras themselves is independent and specific; castaways and Lane's "
     "men are alternative sources of 'white ancestors'; sixteen fighting men is a small community."),
    ("E", "Some colonists tried to sail home",
     10, 5, 20,
     "The boats were gone in 1590 and Grenville's men had left the same coast by boat in 1586; against, "
     "no pilot, families, and no trace in any record of either nation."),
    ("F", "The first Dare Stone is a sixteenth-century inscription",
     20, 15, 25,
     "Section 7 gives the grounds: the finder could not be traced; a stone relic was hawked and a bogus relic had been proposed at Manteo that summer; the text borrows from the printed narratives and departs from the spelling habits of the period corpus; and no test has ever been run on the stone."),
]

if __name__ == "__main__":
    raw = posterior(PRIOR, CLUSTERS)
    rep = robust(raw)
    print("Prior            ", fmt(PRIOR))
    print("Raw posterior    ", fmt(raw))
    print(f"Reported ({int(MIX*100)}% mix)", fmt(rep))
    cases = []
    cases.append(("Reported", rep))
    cases.append(("Flat prior", robust(posterior({h: 0.2 for h in H}, CLUSTERS))))
    cases.append(("No mixture (raw ledger)", raw))
    for i, c in enumerate(CLUSTERS):
        cases.append((f"Drop {c[0][:3].strip()}", robust(posterior(PRIOR, CLUSTERS, skip=(i,)))))
    cases.append(("Jamestown clusters C4 and C5 counted as one (half weight each)",
                  robust(posterior(PRIOR, CLUSTERS, soften=((3, 4), 0.5)))))
    cases.append(("Croatoan-friendly: halve the strength of C1, C4, C5, C9",
                  robust(posterior(PRIOR, CLUSTERS, soften=((0, 3, 4, 8), 0.5)))))
    cases.append(("Chesapeake-friendly: halve the strength of C1, C4, C5, C11",
                  robust(posterior(PRIOR, CLUSTERS, soften=((0, 3, 4, 10), 0.5)))))
    cases.append(("Sea-friendly: halve the strength of C3 and C5",
                  robust(posterior(PRIOR, CLUSTERS, soften=((2, 4), 0.5)))))
    cases.append(("Everything halved (every likelihood ratio pulled toward 1)",
                  robust(posterior(PRIOR, CLUSTERS, soften=(tuple(range(len(CLUSTERS))), 0.5)))))
    cases.append(("Mixture 30% instead of 15%", robust(raw, 0.30)))
    print()
    for name, p in cases:
        print(f"{name:<68} {fmt(p)}")
    lo = {h: min(100*p[h] for _, p in cases) for h in H}
    hi = {h: max(100*p[h] for _, p in cases) for h in H}
    print()
    print("Range across cases:", "  ".join(f"{h} {lo[h]:.0f}-{hi[h]:.0f}" for h in H))

    # ---------- outputs ----------
    order = sorted(H, key=lambda h: -rep[h])
    headline = [{"label": LABEL[h], "p": round(100*rep[h], 1), "lo": round(lo[h]), "hi": round(hi[h]),
                 "lead": h == order[0], "copper": h == "H1"} for h in order]
    findings = [{"id": i, "claim": c, "p": p, "lo": l, "hi": u, "basis": b} for i, c, p, l, u, b in FINDINGS]
    results = {"question": "principal seat of the main body, c. 1588-1607", "prior": PRIOR, "mix": MIX,
               "raw": raw, "reported": rep, "cases": [{"name": n, "p": p} for n, p in cases],
               "lo": lo, "hi": hi, "headline": headline, "findings": findings, "model_section": 6,
               "clusters": [{"label": l, "lik": k, "note": n} for l, k, n in CLUSTERS]}
    json.dump(results, open(os.path.join(ROOT, "data", "model_results.json"), "w"), indent=1)

    def pct(x): return f"{round(x)}"
    tok = {}
    for h in H:
        key = {"H1": "CROATOAN", "H2": "ALBEMARLE", "H3": "CHESAPEAKE", "H4": "SEA", "H5": "OTHER"}[h]
        tok["P_" + key] = pct(100*rep[h]); tok["LO_" + key] = pct(lo[h]); tok["HI_" + key] = pct(hi[h])
        tok["RAW_" + key] = pct(100*raw[h]); tok["PRIOR_" + key] = pct(100*PRIOR[h])
    for i, c, p, l, u, b in FINDINGS:
        tok[f"F{i}_P"] = str(p); tok[f"F{i}_LO"] = str(l); tok[f"F{i}_HI"] = str(u)
    tok["MIX"] = str(int(MIX*100))
    # ledger table rows
    HNAME = {"1": "the Croatoan reading", "2": "the mainland reading", "3": "the Chesapeake reading",
             "4": "the sea reading", "5": "the other reading"}
    def hname(t):
        import re as _re
        return _re.sub(r"\bH([1-5])\b", lambda m: HNAME[m.group(1)], t)
    rows = []
    for l, k, n in CLUSTERS:
        cid, text = l[:3].strip(), l[4:].strip()
        rows.append("<tr><td><strong>" + cid + "</strong> " + text + "</td>" +
                    "".join(f'<td class="num">{k[h]:.2f}</td>' for h in H) + f"<td>{hname(n)}</td></tr>")
    tok["LEDGER_ROWS"] = "\n".join(rows)
    srows = []
    for name, p in cases:
        srows.append(f"<tr><td>{name}</td>" + "".join(f'<td class="num">{100*p[h]:.0f}</td>' for h in H) + "</tr>")
    tok["SENS_ROWS"] = "\n".join(srows)
    frows = []
    for i, c, p, l, u, b in FINDINGS:
        frows.append(f'<tr><td><strong>{i}</strong> {c}</td><td class="num">{p}</td><td class="num">{l} to {u}</td><td>{b}</td></tr>')
    tok["FINDINGS_ROWS"] = "\n".join(frows)
    tok["BUILD_DATE"] = datetime.date.today().strftime("%d %B %Y").lstrip("0")
    # keep any tokens other scripts may have written
    tokpath = os.path.join(ROOT, "data", "tokens.json")
    old = json.load(open(tokpath)) if os.path.exists(tokpath) else {}
    old.update(tok)
    json.dump(old, open(tokpath, "w"), indent=1)
    print("\nwrote data/model_results.json and data/tokens.json")
