#!/usr/bin/env python3
"""Headline probability for the identity of the prisoner who died in the Bastille on 19 November 1703,
as the product of three links, with the sensitivity table printed in the report.

L1: the Bastille prisoner of 1698 is the prisoner Saint-Mars brought from Sainte-Marguerite
    (du Junca 18 Sept 1698; Barbezieux 17 June to 4 Aug 1698; Pontchartrain 3 Nov 1698).
L2: the island prisoner of 1698 is the prisoner brought from Exilles on 30 April 1687
    (Saint-Mars 3 May 1687, 8 Jan 1688; Barbezieux 13 Aug 1691; "ancien prisonnier" Jan 1696 to Aug 1698;
    against Brugnon's thesis of a death in 1693 resting on Papon 1778).
L3: the Exilles survivor of January 1687 is the valet of 1669 and not La Rivière
    (Barbezieux 13 Aug 1691 "depuis vingt ans"; 17 Nov 1697 "ce qu'a fait"; shape of the file).
Residual mass: if L2 fails, the 1698 prisoner is someone else (another Pignerol prisoner of 1694 or unknown);
if L3 fails, he is La Rivière. Mattioli is given a small fixed share of the "someone else" mass.
Usage: python3 probability.py
"""

def headline(L1=0.99, L2=0.93, L3=0.85, mattioli_share=0.4):
    valet = L1 * L2 * L3
    lariviere = L1 * L2 * (1 - L3)
    other = 1 - L1 * L2
    mattioli = other * mattioli_share
    other -= mattioli
    return {"valet_1669": valet, "la_riviere": lariviere, "mattioli": mattioli, "other": other}

def fmt(d):
    return "  ".join(f"{k} {v*100:5.1f}%" for k, v in d.items())

if __name__ == "__main__":
    print("Headline (L1=0.99, L2=0.93, L3=0.85):")
    print("  " + fmt(headline()))
    print("\nSensitivity:")
    for label, kw in [
        ("L3 = 0.95 (1691 'vingt ans' read strictly)", dict(L3=0.95)),
        ("L3 = 0.60 (1691 read as a loose round number)", dict(L3=0.60)),
        ("L3 = 0.50 (no evidence either way on the survivor)", dict(L3=0.50)),
        ("L2 = 0.85 (more weight to Brugnon's 1693 death)", dict(L2=0.85)),
        ("L2 = 0.50 (Brugnon accepted at even odds)", dict(L2=0.50)),
        ("L2 = 0.99 (Brugnon dismissed)", dict(L2=0.99)),
    ]:
        print(f"  {label:55s} " + fmt(headline(**kw)))
