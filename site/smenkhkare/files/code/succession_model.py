#!/usr/bin/env python3
"""
Explicit model of the late-Amarna succession.

Run:  python3 succession_model.py
Writes: ../data/results.json, ../data/results.md, ../data/likelihood_table.json

The model is a discrete joint distribution over five questions:

  id  who bore the extended prenomen and the nomen Neferneferuaten
        Nefertiti | Meritaten | Tasherit (Neferneferuaten-tasherit) | Male (Smenkhkare renamed)
  sk  where the king Smenkhkare Djeserkheperu stands relative to that ruler
        same          one person with two name-sets
        before_coreg  a separate king, coregent of Akhenaten, dead before Akhenaten (Dodson)
        before_sole   a separate king who reigned after Akhenaten and before Neferneferuaten (Gabolde, Krauss 1978)
        after         a separate king who reigned after Neferneferuaten and before Tutankhaten (Allen 2009)
      For id = Male only sk = same is defined (that is what "Male" means).
  cg  was Neferneferuaten made coregent while Akhenaten lived   yes | no
  kv  who is the KV55 body   Akhenaten | Smenkhkare | AnotherSon (another son of Amenhotep III)
  nb  who is Nibhururiya of the Hittite Deeds   Tutankhamun | Akhenaten | Smenkhkare

Every evidence item is a function from a state to a likelihood in [0, 1], on a coarse scale:
1.0 expected under the state; 0.6-0.8 mildly unexpected; 0.3-0.5 surprising; 0.1-0.2 very
surprising; 0.0 logically excluded.  Three settings are carried for every item: base (the
report's judgement), sceptical (the reading least favourable to the female-king / Nefertiti
thesis that a named scholar defends) and generous (the reading most favourable).  The report
prints all three next to the headline.  Nothing here is a measurement; it is a bookkeeping
device that makes the judgements explicit and lets a reader change any one of them.
"""
import itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
os.makedirs(DATA, exist_ok=True)

IDS = ["Nefertiti", "Meritaten", "Tasherit", "Male"]
SKS = ["same", "before_coreg", "before_sole", "after"]
CGS = ["yes", "no"]
KVS = ["Akhenaten", "Smenkhkare", "AnotherSon"]
NBS = ["Tutankhamun", "Akhenaten", "Smenkhkare"]

def states():
    for i, s, c, k, n in itertools.product(IDS, SKS, CGS, KVS, NBS):
        if i == "Male" and s != "same":
            continue
        yield dict(id=i, sk=s, cg=c, kv=k, nb=n)

def named_model(st):
    """Label the succession models that named scholars defend."""
    i, s = st["id"], st["sk"]
    key = (i, s)
    return {
        ("Nefertiti", "before_coreg"): "N-SB-coreg  Dodson 2009/2020, Belmonte 2013, Kawai 2023",
        ("Nefertiti", "before_sole"):  "N-SB-sole   Allen 2016 (as reported), Eaton-Krauss",
        ("Nefertiti", "after"):        "N-SA        (Allen 1994 order with Nefertiti; no named champion)",
        ("Nefertiti", "same"):         "N-SI        Harris 1973-77, Samson, Reeves 2001-2023",
        ("Meritaten", "before_sole"):  "M-SB        Gabolde 1998-2015, Laboury 2002/2010",
        ("Meritaten", "before_coreg"): "M-SB-coreg  (no named champion)",
        ("Meritaten", "after"):        "M-SA        (no named champion)",
        ("Meritaten", "same"):         "M-SI        (no named champion)",
        ("Tasherit", "after"):         "T-SA        Allen 2009 (withdrawn by Allen 2016)",
        ("Tasherit", "before_coreg"):  "T-SB-coreg  (no named champion)",
        ("Tasherit", "before_sole"):   "T-SB-sole   (no named champion)",
        ("Tasherit", "same"):          "T-SI        (no named champion)",
        ("Male", "same"):              "X-SI        Krauss 1978/2007, Hornung 2006, Kemp 2016, Willeitner 2022",
    }[key]

# ---------------------------------------------------------------------------
# Evidence items.  Each returns a dict {variant: likelihood} for a given state.
# `v` picks base / sceptical / generous values from a small table.
# ---------------------------------------------------------------------------
def pick(table, key, v):
    val = table[key]
    return val[v] if isinstance(val, dict) else val

ITEMS = []
def item(code, title, depends, sources):
    def deco(fn):
        ITEMS.append(dict(code=code, title=title, depends=depends, sources=sources, fn=fn))
        return fn
    return deco

B, S, G = "base", "sceptical", "generous"

@item("E01", "Feminine grammatical forms attached to the extended-prenomen titulary",
      "id",
      "Bezel UC 1927 Ankhetkheperure (Samson, COA III 230); pectoral Carter 261p(1) ankh(t)-kheperure mer(yt)-Waenre + maat-kheru (Gabolde 2009 p. 116-117; Eaton-Krauss OLZ 98, 2003, 47); coffinette 266g Selkis line 7 akhet-en-hies (Gabolde 2009 p. 117); bracelets (Sousa et al. 2024); UC 410, NRP plaster, Munich AeS 7342 akhet-en-hies (Dietrich 2024 p. 101-102). Counter: Kemp 2016 p. 18-20, 28-29 (t may be r or n on bezels; .ti endings are second person).")
def e01(st, v):
    t = {"Nefertiti": 1, "Meritaten": 1, "Tasherit": 1, "Male": {B: 0.15, S: 0.4, G: 0.05}}
    return pick(t, st["id"], v)

@item("E02", "The nomen Neferneferuaten is Nefertiti's own cartouche name (Neferneferuaten-Nefertiti from about year 5), written with the same reversed Aten group",
      "id",
      "Harris 1973 AcOr 35; Kemp 2016 p. 22 (reversed Aten group noted, explained as scribal habit); Allen 2009 p. 12 on the daughter Neferneferuaten-tasherit.")
def e02(st, v):
    t = {"Nefertiti": 1, "Meritaten": {B: 0.4, S: 0.6, G: 0.3}, "Tasherit": {B: 0.7, S: 0.8, G: 0.6}, "Male": {B: 0.3, S: 0.5, G: 0.2}}
    return pick(t, st["id"], v)

@item("E03", "Epithets tying the ruler to Akhenaten as his beloved and to a husband: mery-Waenre, mery-Neferkheperure, akhet-en-hies 'effective for her husband'",
      "id",
      "Gabolde 1998 p. 153-157 (reading accepted by Murnane 2001, Eaton-Krauss & Krauss 2001, Hornung 2006, Dodson 2009); Kemp 2016 p. 22 reads the husband as Ankhkheperure himself; Krauss 2007 gives the epithet to a widow of Ankhkheperure.")
def e03(st, v):
    t = {"Nefertiti": 1, "Meritaten": {B: 0.6, S: 0.8, G: 0.5}, "Tasherit": {B: 0.3, S: 0.5, G: 0.2}, "Male": {B: 0.5, S: 0.7, G: 0.3}}
    return pick(t, st["id"], v)

@item("E04", "Stela UC 410 + Cairo JE 64959: the double cartouche of Neferneferuaten is cut over Nefertiti's single queenly cartouche and a king's-daughter caption",
      "id",
      "Allen JARCE 25 (1988) via Allen 2009 n. 5, 12; Krauss BSEG 13 (1989); Gabolde BSEG 14 (1990); COA III 231-233 (Samson, Fairman); Kemp 2016 p. 23-26 with Gabolde's tracing; Dietrich 2024 p. 102.")
def e04(st, v):
    t = {"Nefertiti": 1, "Meritaten": {B: 0.8, S: 1.0, G: 0.6}, "Tasherit": {B: 0.3, S: 0.5, G: 0.2}, "Male": {B: 0.5, S: 0.7, G: 0.3}}
    return pick(t, st["id"], v)

@item("E05", "Paired-ruler scenes: an adult woman in the blue crown beside a male king, both with uraeus, interacting as living rulers; the Hermopolis pillar join names Neferneferuaten and King's Daughter Ankhesenpaaten",
      "id, cg",
      "Berlin AeM 17813 and 20716 (Harris 1973; Allen 2009 figs 3-4; Dietrich 2024 p. 98); Ranefer sealing COA I pl. X.6; Hermopolis 406/VII + 777/VIII (Johnson 2020, as reported by Dietrich 2024 p. 102-104) + 826/VIIIA (Gabolde 1990; Dietrich fig. 3). Counter: Harris 1973 read the figures as king and crowned queen; Kemp 2016 p. 15 doubts coregency.")
def e05(st, v):
    ti = {"Nefertiti": 1, "Meritaten": {B: 0.9, S: 1.0, G: 0.8}, "Tasherit": {B: 0.25, S: 0.4, G: 0.15}, "Male": {B: 0.5, S: 0.7, G: 0.3}}
    tc = {"yes": 1, "no": {B: 0.35, S: 0.6, G: 0.25}}
    return pick(ti, st["id"], v) * pick(tc, st["cg"], v)

@item("E06", "Box Carter 1k: Akhenaten 'great in his lifetime', then Ankhkheperure-mery-Neferkheperure Neferneferuaten-mery-Waenre, then King's Great Wife Meritaten 'may she live', as three entries in one protocol",
      "id, sk, cg",
      "Carter cards 001k-1..4; Newberry JEA 14 (1928) 4-5; Dietrich 2024 p. 100-101; Allen 2009 p. 9-10 and n. 6; Kemp 2016 p. 13-15 (reads the box as posthumous respect to Akhenaten and as proof the king was married to Meritaten); Gabolde 1998 p. 178-179 reads Meritaten in apposition to Neferneferuaten (rejected by Murnane 2001, Eaton-Krauss & Krauss 2001, Allen 2009, Dodson 2020, Kemp 2016).")
def e06(st, v):
    i, s, c = st["id"], st["sk"], st["cg"]
    if i == "Meritaten":
        a = {B: 0.25, S: 0.4, G: 0.15}[v]
    else:
        a = 1.0   # the oddity of a female king with a 'Great Royal Wife' is scored once, in E07
    b = 1.0 if c == "yes" else {B: 0.6, S: 0.8, G: 0.5}[v]
    return a * b

@item("E07", "Tomb of Meryre II (Amarna tomb 2) and the Memphis block: King Ankhkheperure Smenkhkare Djeserkheperu with King's Great Wife Meritaten, under the Aten, in a tomb whose dated decoration ends with the year-12 durbar",
      "id, sk",
      "Davies 1905 pl. XLI after Lepsius LD III 99a; Petrie 1894 p. 29; Newberry JEA 14 (1928) 5-6 (Memphis); Kemp 2016 p. 15 (year 12 dates the event, not the carving); Allen 2009 p. 9 and 17; Dodson 2020 p. 68-71.")
def e07(st, v):
    i, s = st["id"], st["sk"]
    if i == "Male":
        return 1.0
    t = {"before_coreg": 1.0, "before_sole": 1.0, "after": {B: 0.6, S: 0.5, G: 0.7}}
    if s == "same":
        return {"Nefertiti": {B: 0.35, S: 0.25, G: 0.5}, "Meritaten": {B: 0.05, S: 0.05, G: 0.05}, "Tasherit": {B: 0.35, S: 0.25, G: 0.5}}[i][v]
    return pick(t, s, v)

@item("E08", "Calcite jar Carter 405: Akhenaten's cartouches followed by Smenkhkare's, both later erased; the only object joining the two names",
      "id, sk",
      "Carter cards 405-1/2; Loeben, Amarna Letters 3 (1994) as cited; Allen 2009 p. 9 fig. 1; Dietrich 2024 p. 102 ('at best circumstantial' for a coregency).")
def e08(st, v):
    i, s = st["id"], st["sk"]
    if i == "Male":
        return 1.0
    t = {"before_coreg": 1.0, "before_sole": 0.9, "after": {B: 0.5, S: 0.4, G: 0.6}, "same": 0.8}
    return pick(t, s, v)

@item("E09", "Complementary distribution of the names: the plain prenomen only with the nomen Smenkhkare, the extended prenomen only with the nomen Neferneferuaten, with no crossed example among hundreds of bezels and moulds",
      "id, sk",
      "Allen JARCE 25 (1988) 126; Allen 1991: 84-85; Gabolde 1998: 153-157; Harris 1992: 60-61 (all as cited by Dietrich 2024 p. 101); Petrie 1894 pl. XV; COA III bezel lists.")
def e09(st, v):
    return 1.0 if st["sk"] != "same" else {B: 0.6, S: 0.8, G: 0.5}[v]

@item("E10", "Pairi graffito TT 139: 'Year 3, III Akhet 10' of Ankhkheperure-mery-[...] Neferneferuaten-mery-[...], with Amun worshipped and a 'House of Ankhkheperure in Thebes' staffed by priests of Amun; Smenkhkare is otherwise attested only in Aten contexts",
      "sk",
      "Gardiner JEA 14 (1928) 10-11 pls V-VI; Newberry JEA 14, 3-9; Krauss in Hornung-Krauss-Warburton 2006 p. 207-208; Dodson 2020b (Fs Hawass) and Reeves 2023 (Fs Strudwick) as reported by Dietrich 2024 n. 15, 18; Dietrich n. 18 on the two theologies.")
def e10(st, v):
    s = st["sk"]
    if st["id"] == "Male":
        return {B: 0.8, S: 0.9, G: 0.7}[v]
    t = {"before_coreg": 1.0, "before_sole": 1.0, "after": {B: 0.8, S: 0.7, G: 0.85}, "same": {B: 0.8, S: 0.7, G: 0.9}}
    return pick(t, s, v)

@item("E11", "Amarna jar dockets: Akhenaten's highest year 17; a year-17 docket relabelled 'year 1' (COA III 279); years 1-3 of a successor at Amarna; 'House of Smenkhkare, [justified]' in a year 1 (no. 35); 'House of Ankhkheperure' as a separate estate (no. 36)",
      "sk",
      "Petrie 1894 p. 32-34 (Griffith); COA III (Fairman) p. 143-159, 199; Krauss 2006 p. 207-208; Allen 2009 p. 12 and n. 14; Dodson 2009 p. 31 n. 14.")
def e11(st, v):
    s = st["sk"]
    if st["id"] == "Male":
        return 1.0
    t = {"before_coreg": 1.0, "before_sole": {B: 0.9, S: 0.85, G: 0.95}, "after": 1.0, "same": 1.0}
    return pick(t, s, v)

@item("E12", "Manetho according to Josephus: Orus, then 'his daughter Akencheres, 12 years 1 month', then 'her brother Rathotis, 9 years'",
      "id",
      "Josephus, Contra Apionem 1.96-97 (Niese); Waddell 1940 fr. 50-53; Krauss 1978 p. 43-53 and Hornung-Krauss-Warburton 2006 p. 36, 207; Allen 2009 p. 18; Dodson 2020 p. 104-105, 128; Kemp 2016 p. 30 ('nothing is gained').")
def e12(st, v):
    t = {"Nefertiti": {B: 0.7, S: 1.0, G: 0.5}, "Meritaten": 1.0, "Tasherit": 1.0, "Male": {B: 0.7, S: 1.0, G: 0.6}}
    return pick(t, st["id"], v)

@item("E13", "A shabti of Nefertiti with queenly titles only (Louvre AF 9904 + Brooklyn 33.51)",
      "id",
      "Loeben MDAIK 42 (1986) 99-107 and EAO 13 (1999); Bovot EAO 13 (1999) 31-34 (two shabtis); Allen 2009 p. 16 n. 59; Dodson 2020 p. 89 (made in anticipation of death); Reeves 2015 n. 35.")
def e13(st, v):
    t = {"Nefertiti": {B: 0.6, S: 0.4, G: 0.8}, "Meritaten": 1.0, "Tasherit": 1.0, "Male": 1.0}
    return pick(t, st["id"], v)

@item("E14", "Masculine references beside the extended names: 'my lord' with a masculine article on Ranefer's door jamb; the North Riverside Palace prenomen painted with r, not t, under mer",
      "id",
      "Kemp 2016 p. 13, 20-21 (with Weatherhead's and Hilda Pendlebury's copies); Kemp & Stevens 2010 p. 119-127 (not seen).")
def e14(st, v):
    t = {"Nefertiti": {B: 0.85, S: 0.7, G: 0.95}, "Meritaten": {B: 0.85, S: 0.7, G: 0.95}, "Tasherit": {B: 0.85, S: 0.7, G: 0.95}, "Male": 1.0}
    return pick(t, st["id"], v)

@item("E15", "Age of Neferneferuaten-tasherit: fourth daughter, shown as a child at the year-12 durbar, so at most about ten years old in year 17",
      "id",
      "Davies 1905 pl. XXXVIII (six daughters); Allen 2009 p. 15-16; Dodson 2020 p. 129 on Allen's withdrawal.")
def e15(st, v):
    return {B: 0.15, S: 0.3, G: 0.1}[v] if st["id"] == "Tasherit" else 1.0

@item("E16", "Dayr Abu Hinnis graffito: Nefertiti still King's Great Wife on day 15 of a month of Akhet in year 16, about a year before Akhenaten's death",
      "id, cg",
      "Van der Perre 2012; 2014 JEgH 7, 67-108 (abstract only); Dodson 2020 p. 72-73 fig. 80; Reeves 2015 n. 32.")
def e16(st, v):
    if st["id"] == "Nefertiti" and st["cg"] == "yes":
        return {B: 0.85, S: 0.75, G: 0.9}[v]
    return 1.0

@item("E17", "A full kingly burial outfit made for the female king was left unused and re-inscribed for Tutankhamun (coffinettes, pectoral, trappings, middle coffin, mask, second shrine, statuettes)",
      "none (documentary)",
      "Gabolde 2009 p. 116-118; Reeves 2015 JAEI 7.4 and ARTP OP1; Laboury 2002; Engelbach ASAE 40 (1940); Sousa-Pieke-Bagh 2024 (Broschat); Kemp 2016 p. 26-29 (shrine endings read as second person).")
def e17(st, v):
    return 1.0

@item("E18", "Two rulers with one prenomen: Ankhkheperure is shared by the Smenkhkare name-set and the Neferneferuaten name-set, which has no parallel for two successive kings",
      "sk",
      "Harris 1973 AcOr 35 p. 5-13 (the one-person argument); Reeves 2015 ARTP OP1 n. 33; Kemp 2016 p. 15; Allen 2009 p. 12-13 and Dodson 2020 p. 79 (continuity explanations for two persons).")
def e18(st, v):
    return 1.0 if st["sk"] == "same" else {B: 0.35, S: 0.25, G: 0.5}[v]

# KV55 items
@item("K01", "Age at death of the KV55 body: six hands-on examiners give 19-26; Harris and Wente 30-35 and Hawass 2010 (CT, criteria unpublished) 35-45; Akhenaten had a daughter by about year 2 and reigned 17 years",
      "kv",
      "Elliot Smith 1912; Derry ASAE 31 (1931); Harrison JEA 52 (1966); Filer 2000; Strouhal 2010; Duhig 2010; Hawass et al. JAMA 303 (2010); Gabolde 2009 p. 12 (26-27 for Akhenaten); dossier B section 2.")
def k01(st, v):
    t = {"Akhenaten": {B: 0.2, S: 0.5, G: 0.08}, "Smenkhkare": 1.0, "AnotherSon": 1.0}
    return pick(t, st["kv"], v)

@item("K02", "Inscribed material in KV55: magic bricks of Akhenaten, Kiya's coffin re-worked with Akhenaten's epithets (cartouches later cut out), Kiya's canopic jars, Tiye's shrine, sealings of Tutankhamun; no name of Smenkhkare",
      "kv",
      "Davis 1910; Allen 2009 n. 24-26; Gabolde 2009 p. 3-6, 12-18; Dodson 2009 ch. 2 and 2020 p. 47-48; Reeves 2001 p. 81-84; dossier B section 1.")
def k02(st, v):
    t = {"Akhenaten": 1.0, "Smenkhkare": {B: 0.4, S: 0.7, G: 0.25}, "AnotherSon": {B: 0.3, S: 0.6, G: 0.15}}
    return pick(t, st["kv"], v)

@item("K03", "2010 STR pedigree (8 loci): KV55 a son of Amenhotep III and KV35EL (Tiye) and the father of Tutankhamun with KV35YL; no independent replication; Gad et al. 2020 same team",
      "kv",
      "Hawass et al. JAMA 303 (2010) 638-647; Gad et al. 2020; Lorenzen & Willerslev JAMA 2010; Marchant Nature 2011; Phizackerley 2010 (D7S820); Gabolde ENiM 6 (2013); dossier B sections 3-4.")
def k03(st, v):
    t = {"Akhenaten": 1.0, "Smenkhkare": 1.0, "AnotherSon": 1.0}
    return pick(t, st["kv"], v)

@item("K04", "Tutankhaten was 'King's Son of his body' at Amarna; if the pedigree holds, his father is the KV55 man, who must therefore have been a king",
      "kv",
      "Hermopolis talatat 56-VIIIA + 831-VIIIC (Allen 2009 fig. 5, p. 14-17; Dodson 2014 fig. 104).")
def k04(st, v):
    t = {"Akhenaten": 1.0, "Smenkhkare": 1.0, "AnotherSon": {B: 0.4, S: 0.6, G: 0.3}}
    return pick(t, st["kv"], v)

# Nibhururiya items
@item("D01", "The name: Ni-ip-hu-ru-ri-ia-as (KBo 14.12 iv 18) against Nebkheperure (Tutankhamun) and Neferkheperure (Akhenaten); EA 9 addressed to Nibhurrereya",
      "nb",
      "Güterbock JCS 10 (1956) 94-98; Miller AoF 34 (2007) 252-293 (EA 9 = Akhenaten); Bryce 1990; Federn JCS 14 (1960) 33; dossier C section 2.4.")
def d01(st, v):
    t = {"Tutankhamun": 1.0, "Akhenaten": {B: 0.6, S: 0.4, G: 0.8}, "Smenkhkare": {B: 0.1, S: 0.05, G: 0.15}}
    return pick(t, st["nb"], v)

@item("D02", "The Armaa synchronism: Horemheb acts in Syria as a non-king in years 7-9 of Mursili II (KUB 19.15 + KBo 50.24), which sits badly with a Nibhururiya who died only four years before Horemheb's accession",
      "nb",
      "Miller 2007; Devecchi & Miller 2011; contra Stempel GM 213 (2007) and Theis 2011 as cited by Dodson 2020 n. 44; Bryce 1990, Klinger 2006, Freu 2004 for Tutankhamun; dossier C sections 5-6.")
def d02(st, v):
    t = {"Tutankhamun": {B: 0.25, S: 0.6, G: 0.12}, "Akhenaten": 1.0, "Smenkhkare": 1.0}
    return pick(t, st["nb"], v)

@item("D03", "Season: the death message reached Suppiluliuma during the Carchemish campaign (late summer or autumn) and Hani came back in spring; Tutankhamun's burial flowers point to a death in winter; Akhenaten died after the year-17 vintage",
      "nb",
      "Deeds fragment 28 (Güterbock 1956 p. 94-98); floral evidence of KV62 (Hepper 1990) as used by Belmonte 2013; Fairman COA III 157-159 on docket 279; dossier C section 7.")
def d03(st, v):
    t = {"Tutankhamun": {B: 0.4, S: 0.7, G: 0.25}, "Akhenaten": 0.9, "Smenkhkare": 0.9}
    return pick(t, st["nb"], v)

@item("D04", "The widow's plea: 'my husband died, a son I have not, I will never take a servant of mine and make him my husband'; Ankhesenamun was later paired with Ay on a ring; Nefertiti and Meritaten each had daughters and a boy in the family",
      "nb",
      "Deeds fragment 28 A iii 7-15 (Güterbock 1956); Newberry JEA 18 (1932) 50 (Ay-Ankhesenamun ring); Reeves 2001 ch. 9; Allen 2009 n. 62.")
def d04(st, v):
    t = {"Tutankhamun": 1.0, "Akhenaten": {B: 0.7, S: 0.6, G: 0.8}, "Smenkhkare": 0.8}
    return pick(t, st["nb"], v)

@item("D05", "Lupakki's raid on Amka at the time of the king's death (Deeds) matches EA 170 from the Amarna archive, and the envoy Hani of the Deeds appears in EA 161, 162 and 369",
      "nb",
      "EA 170 and 161-162, 369 (Knudtzon 1915; Moran 1992 as cited); Deeds fragment 28; Miller 2007; Reeves 2001 p. 176-177; dossier C section 6.")
def d05(st, v):
    t = {"Tutankhamun": {B: 0.5, S: 0.8, G: 0.35}, "Akhenaten": 1.0, "Smenkhkare": 0.9}
    return pick(t, st["nb"], v)

@item("D06", "Hittite relative chronology: the plague prayers, the 20-year plague, and the solar omen of Mursili's year 10 (eclipse of 24 June 1312 if that is the omen)",
      "nb",
      "CTH 378.2 (Rieken's score); KUB 14.4 (omen); Belmonte 2013 p. 427-429; Dodson 2020 chronology table; dossier C section 7.")
def d06(st, v):
    t = {"Tutankhamun": {B: 0.7, S: 1.0, G: 0.5}, "Akhenaten": 1.0, "Smenkhkare": 1.0}
    return pick(t, st["nb"], v)

@item("D07", "Consistency of the plea with the Egyptian succession: a widow writes that Egypt has no king; a coregent already on the throne, or an Egyptian king who acceded after months of negotiation for a Hittite prince, fit that less well",
      "nb, cg, sk",
      "Deeds fragment 28; Reeves 2001 ch. 9 (Nefertiti seeking a consort); Allen 2009 n. 62 (no demotion implied); Gabolde 1998 p. 213-226 (Zannanza = Smenkhkare), judged 'not probable' by Hornung-Krauss-Warburton 2006 n. 73.")
def d07(st, v):
    if st["nb"] != "Akhenaten":
        return 1.0
    a = {B: 0.4, S: 0.3, G: 0.6}[v] if st["cg"] == "yes" else 1.0
    b = {B: 0.5, S: 0.4, G: 0.6}[v] if st["sk"] == "before_sole" else 1.0
    return a * b

@item("D08", "'A son he has not' against Tutankhaten's existence: if the dead king was Tutankhaten's father, the statement is false for the royal house",
      "nb, kv",
      "Deeds fragment 28 A iii 7-15 and E3 iv 1-39 (Hani's speech); Hermopolis King's Son block; JAMA 2010 pedigree.")
def d08(st, v):
    n, k = st["nb"], st["kv"]
    if n == "Tutankhamun":
        return 1.0
    if n == "Akhenaten":
        return {"Akhenaten": {B: 0.35, S: 0.5, G: 0.25}[v], "Smenkhkare": 1.0, "AnotherSon": 0.6}[k]
    return {"Akhenaten": 1.0, "Smenkhkare": {B: 0.3, S: 0.45, G: 0.2}[v], "AnotherSon": 1.0}[k]

# Hard constraints between questions
def constraint(st):
    i, s, k, n = st["id"], st["sk"], st["kv"], st["nb"]
    if i != "Male" and s == "same" and k == "Smenkhkare":
        return 0.0   # a female Smenkhkare is not the KV55 man
    if n == "Smenkhkare":
        if i != "Male" and s in ("same", "before_coreg"):
            return 0.0   # no male Smenkhkare who died as reigning king
    return 1.0

# ---------------------------------------------------------------------------
def dahamunzu(st):
    n, i = st["nb"], st["id"]
    if n == "Tutankhamun":
        return {"Ankhesenamun": 1.0}
    if n == "Smenkhkare":
        return {"Meritaten": 1.0}
    return {"Nefertiti": {"Nefertiti": 0.7, "Meritaten": 0.1, "Tasherit": 0.6, "Male": 0.7}[i],
            "Meritaten": {"Nefertiti": 0.3, "Meritaten": 0.9, "Tasherit": 0.4, "Male": 0.3}[i]}

def prior(st, kind):
    if kind == "uniform":
        return 1.0
    if kind == "literature":   # named positions weighted 2:1 against unheld combinations
        return 2.0 if "no named champion" not in named_model(st) else 1.0
    if kind == "nefertiti_sceptical":
        return {"Nefertiti": 0.15, "Meritaten": 0.35, "Tasherit": 0.15, "Male": 0.35}[st["id"]] / (0.25 if st["id"] != "Male" else 0.25)
    if kind == "one_person_half":   # sk = same weighted so that one-person models hold about half the prior
        return 3.0 if st["sk"] == "same" else 1.0
    if kind == "tut_favouring":
        return {"Tutankhamun": 0.6, "Akhenaten": 0.3, "Smenkhkare": 0.1}[st["nb"]] * 3
    raise ValueError(kind)

def run(variant=B, prior_kind="uniform", drop=None, only=None):
    post = {}
    for st in states():
        w = prior(st, prior_kind) * constraint(st)
        for it in ITEMS:
            if drop and it["code"] in drop:
                continue
            if only and it["code"] not in only:
                continue
            w *= it["fn"](st, variant)
        post[tuple(st.values())] = w
    z = sum(post.values())
    return {k: v / z for k, v in post.items()}

def marg(post, field):
    idx = ["id", "sk", "cg", "kv", "nb"].index(field)
    out = {}
    for k, p in post.items():
        out[k[idx]] = out.get(k[idx], 0) + p
    return dict(sorted(out.items(), key=lambda x: -x[1]))

def marg_model(post):
    out = {}
    for k, p in post.items():
        st = dict(zip(["id", "sk", "cg", "kv", "nb"], k))
        lab = named_model(st).split()[0]
        out[lab] = out.get(lab, 0) + p
    return dict(sorted(out.items(), key=lambda x: -x[1]))

def marg_dahamunzu(post):
    out = {}
    for k, p in post.items():
        st = dict(zip(["id", "sk", "cg", "kv", "nb"], k))
        for who, q in dahamunzu(st).items():
            out[who] = out.get(who, 0) + p * q
    return dict(sorted(out.items(), key=lambda x: -x[1]))

def summary(post):
    return dict(identity=marg(post, "id"), smenkhkare=marg(post, "sk"), coregency=marg(post, "cg"),
                kv55=marg(post, "kv"), nibhururiya=marg(post, "nb"), dahamunzu=marg_dahamunzu(post),
                models=marg_model(post),
                separate_smenkhkare=sum(p for k, p in post.items() if k[1] != "same"),
                smenkhkare_before=sum(p for k, p in post.items() if k[1] in ("before_coreg", "before_sole")),
                smenkhkare_after=sum(p for k, p in post.items() if k[1] == "after"))

def fmt(d, n=None):
    items = list(d.items())[:n] if n else d.items()
    return ", ".join(f"{k} {100*v:.0f}%" for k, v in items)

def main():
    results = {}
    base = run(B)
    results["base"] = summary(base)
    results["sceptical"] = summary(run(S))
    results["generous"] = summary(run(G))
    for pk in ["literature", "nefertiti_sceptical", "one_person_half", "tut_favouring"]:
        results["prior_" + pk] = summary(run(B, pk))
    # leave-one-out influence on the headline marginals
    loo = {}
    for it in ITEMS:
        s = summary(run(B, drop={it["code"]}))
        loo[it["code"]] = dict(title=it["title"], P_Nefertiti=s["identity"].get("Nefertiti", 0),
                               P_separate=s["separate_smenkhkare"], P_coreg=s["coregency"].get("yes", 0),
                               P_kv55_Akh=s["kv55"].get("Akhenaten", 0), P_nib_Tut=s["nibhururiya"].get("Tutankhamun", 0))
    results["leave_one_out"] = loo
    # Egyptian-only and Hittite-only views
    eg = [i["code"] for i in ITEMS if i["code"][0] == "E"]
    results["egyptian_items_only"] = summary(run(B, only=set(eg)))
    results["hittite_items_only"] = summary(run(B, only=set(i["code"] for i in ITEMS if i["code"][0] == "D")))
    results["kv55_items_only"] = summary(run(B, only=set(i["code"] for i in ITEMS if i["code"][0] in "KD")))
    # top composite states
    top = sorted(base.items(), key=lambda x: -x[1])[:12]
    results["top_states"] = [dict(zip(["id", "sk", "cg", "kv", "nb"], k)) | {"p": p, "model": named_model(dict(zip(["id", "sk", "cg", "kv", "nb"], k)))} for k, p in top]
    # likelihood table for the report
    table = []
    for it in ITEMS:
        row = dict(code=it["code"], title=it["title"], depends=it["depends"], sources=it["sources"], values={})
        # tabulate over the sub-state the item depends on
        seen = {}
        for st in states():
            key = tuple((f, st[f]) for f in ["id", "sk", "cg", "kv", "nb"] if f in it["depends"])
            if key in seen:
                continue
            seen[key] = {v: it["fn"](st, v) for v in (B, S, G)}
        row["values"] = {" ".join(f"{f}={x}" for f, x in k) or "all": vals for k, vals in seen.items()}
        table.append(row)
    json.dump(table, open(os.path.join(DATA, "likelihood_table.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(results, open(os.path.join(DATA, "results.json"), "w"), indent=1, ensure_ascii=False)

    lines = ["# Model results", ""]
    for name in ["base", "sceptical", "generous", "prior_literature", "prior_nefertiti_sceptical", "prior_one_person_half", "prior_tut_favouring", "egyptian_items_only", "hittite_items_only"]:
        s = results[name]
        lines += [f"## {name}", f"- identity: {fmt(s['identity'])}", f"- Smenkhkare: {fmt(s['smenkhkare'])} (separate person {100*s['separate_smenkhkare']:.0f}%; before {100*s['smenkhkare_before']:.0f}%, after {100*s['smenkhkare_after']:.0f}%)",
                  f"- coregency: {fmt(s['coregency'])}", f"- KV55: {fmt(s['kv55'])}", f"- Nibhururiya: {fmt(s['nibhururiya'])}", f"- Dahamunzu: {fmt(s['dahamunzu'])}", f"- models: {fmt(s['models'], 6)}", ""]
    lines += ["## leave one out (base)", "| item | P(Nefertiti) | P(separate Smenkhkare) | P(coregency) | P(KV55=Akhenaten) | P(Nib=Tut) |", "|---|---|---|---|---|---|"]
    for c, r in loo.items():
        lines.append(f"| {c} | {100*r['P_Nefertiti']:.0f} | {100*r['P_separate']:.0f} | {100*r['P_coreg']:.0f} | {100*r['P_kv55_Akh']:.0f} | {100*r['P_nib_Tut']:.0f} |")
    lines += ["", "## top composite states (base)"]
    for t in results["top_states"]:
        lines.append(f"- {100*t['p']:.1f}%  {t['id']} / Smenkhkare {t['sk']} / coregency {t['cg']} / KV55 {t['kv']} / Nibhururiya {t['nb']}  [{t['model']}]")
    open(os.path.join(DATA, "results.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
