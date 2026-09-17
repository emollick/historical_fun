"""
Explicit scenario weighting for the end of Legio IX Hispana.

Four hypotheses:
  H1  ended in Britain c. 120-128 (destroyed, or defeated and disbanded)
  H2  survived, left Britain c. 120-125, lost in the Bar Kokhba war 132-136 (or disbanded after it)
  H3  survived to 161, destroyed at Elegeia (Dio 71.2)
  H4  other: an undocumented loss or disbandment elsewhere, 125-165

Each evidence item carries a likelihood P(evidence | H), entered as a number relative
to H1 = 1.0 where convenient. These are judgments, argued in the report; the point of
writing them down is that a reader can change any one of them and rerun the file.
"""
import itertools, json

priors = {"H1": 0.30, "H2": 0.30, "H3": 0.25, "H4": 0.15}

evidence = {
 # name: (H1, H2, H3, H4, note)
 "E1 officers: securely dated service ends c. 123-128; none secure after c. 130":
     (1.00, 0.35, 0.08, 0.30, "silence of 6 years (H2) vs 30+ years (H3) at the attested rate of c. 1 senatorial officer per 3 years, softened for randomness; Numisius identity given 35% weight favours H3 slightly"),
 "E2 no base and no trace outside Britain after c. 122 (Nijmegen small units, abandoned c. 125/130; Rhine reduced to two legions; no eastern inscription; absent from expeditio Iudaica records)":
     (1.00, 0.20, 0.10, 0.50, "a legion that left Britain needed a fortress for 122-133 (H2) or 122-161 (H3); none is available or attested"),
 "E3 VI Victrix arrives c. 122-124 as the only new legion; 3,000 legionaries plus a Spanish levy in 123 (expeditio Britannica)":
     (1.00, 0.50, 0.50, 0.60, "a one-for-one replacement plus emergency reinforcement fits losses better than a routine swap"),
 "E4 heavy losses in Britain under Hadrian attested (Fronto; SHA Hadr. 5.2; RIB 3364; hoard horizon 118-123; halted Wall building c. 123)":
     (1.00, 0.70, 0.70, 0.70, "a British war is attested whatever became of the Ninth; it merely supplies the occasion for H1"),
 "E5 Dio 71.2 records a legion annihilated at Elegeia in 161":
     (1.00, 1.00, 2.00, 1.00, "the record exists under every hypothesis; it mildly favours H3 because some legion must fit it, and only IX and XXII vanish"),
 "E6 no centurial stone of the Ninth on Hadrian's Wall":
     (0.50, 1.00, 1.00, 1.00, "expected if the legion left before 122; under H1 the Ninth would have worked one season at most, and the third legion of the earliest sector is unnamed anyway"),
}

def posterior(priors, evidence, drop=None, scale=None):
    post = {}
    for h, i in zip(["H1","H2","H3","H4"], range(4)):
        p = priors[h]
        for name, vals in evidence.items():
            if drop and name.startswith(drop): continue
            v = vals[i]
            if scale and h in scale and not name.startswith("E5"): v = min(1.0, v * scale[h]) if v < 1 else v
            p *= v
        post[h] = p
    z = sum(post.values())
    return {h: round(v / z, 3) for h, v in post.items()}

if __name__ == "__main__":
    base = posterior(priors, evidence)
    print("Base posterior:", base)
    out = {"priors": priors, "evidence": {k: {"H1": v[0], "H2": v[1], "H3": v[2], "H4": v[3], "note": v[4]} for k, v in evidence.items()}, "posterior": base, "sensitivity": {}}
    # sensitivity: drop each evidence item
    for name in evidence:
        r = posterior(priors, evidence, drop=name[:2])
        out["sensitivity"]["without " + name[:2]] = r
        print("without", name[:2], r)
    # sceptic: double every sub-unity likelihood for H2, H3, H4
    r = posterior(priors, evidence, scale={"H2": 2.0, "H3": 2.0, "H4": 2.0})
    out["sensitivity"]["sceptic: H2-H4 likelihoods doubled"] = r
    print("sceptic (H2-H4 likelihoods doubled):", r)
    r = posterior({"H1": 0.15, "H2": 0.35, "H3": 0.35, "H4": 0.15}, evidence, scale={"H2": 2.0, "H3": 2.0, "H4": 2.0})
    out["sensitivity"]["sceptic prior (H1 15%) and doubled"] = r
    print("sceptic prior + doubled:", r)
    json.dump(out, open("scenario_weights.json", "w"), indent=1)
