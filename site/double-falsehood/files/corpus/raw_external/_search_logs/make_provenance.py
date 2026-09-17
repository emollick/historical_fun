#!/usr/bin/env python3
import os, re, json, glob, datetime
from wordfreq import zipf_frequency as Z
BASE=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
WORD=re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
def quality(path):
    t=open(path,encoding='utf-8',errors='replace').read()
    good=n=0
    for l in t.split('\n'):
        toks=[w.lower() for w in WORD.findall(l) if len(w)>1]
        if len(toks)<4: continue
        n+=1
        sc=sum(1 for w in toks if Z(w,'en')>=3.0)/len(toks)
        if sc>=0.6: good+=1
    return (good/n if n else 0), len(WORD.findall(t))
def iameta(slug, ident):
    p=f"{BASE}/{slug}/{ident}.ia_metadata.json"
    return json.load(open(p)) if os.path.exists(p) else {}
def ia_src(slug, ident, note=""):
    m=iameta(slug,ident)
    raw=[os.path.basename(x) for x in glob.glob(f"{BASE}/{slug}/{ident}_djvu.txt")]
    return {"kind":"archive.org","id":ident,"url":f"https://archive.org/details/{ident}",
            "title":m.get('title',''),"date":m.get('date',''),"images":m.get('imagecount',''),
            "ocr":m.get('ocr','(not stated in metadata; djvu.txt present)'),"source":m.get('source') or m.get('contributor') or '',
            "publisher":m.get('publisher',''),"raw":raw,"note":note}
ITEMS=[
# ---------------- PRIORITY 1 ----------------
dict(slug="persian_princess_1715",prio=1,title="The Persian Princess: or, the Royal Villain. A tragedy",author="Lewis Theobald",
 edition="London: printed for Jonas Browne, 1715 (imprint legible in the OCR). FIRST (and only 18th-c.) edition; acted at Drury Lane 1708.",
 sources=[ia_src("persian_princess_1715","bim_eighteenth-century_the-persian-princess-or_theobald-mr-lewis_1715","British Library copy on 'The Eighteenth Century' microfilm (reel IA40312806-81); OCR = tesseract 5.3 run by IA.")],
 clean=[("persian_princess_1715.clean.txt","full volume: dedication, preface, prologue, dramatis personae, five acts, epilogue")],
 complete="All 85 microfilm frames present in the OCR; front matter, five acts and epilogue all present. Microfilm target frames produce noise at start/end (trimmed).",
 notes="Quality is the weakest of the Theobald plays obtained (many broken lines in the preface/prologue frames); the dramatic verse itself is mostly legible."),
dict(slug="perfidious_brother_1715",prio=1,title="The Perfidious Brother. A tragedy: as it is acted at the New Theatre in Little Lincolns-Inn-Fields. By Mr. Theobald",author="Lewis Theobald (revising a draft by Henry Mestayer)",
 edition="London: printed for Jonas Browne, 1715 (imprint per ESTC; not legible in this OCR). FIRST edition of Theobald's version. Archive.org/ESTC catalogue it under Mestayer, Henry as creator; the title page says 'By Mr. Theobald'.",
 sources=[ia_src("perfidious_brother_1715","bim_eighteenth-century_the-perfidious-brother-_mestayer-henry_1715","BL 'Eighteenth Century' microfilm reel IA40312802-38; tesseract OCR.")],
 clean=[("perfidious_brother_1715.clean.txt","full volume incl. Theobald's preface defending his authorship, prologue, five acts, epilogue")],
 complete="69 frames; complete.",
 notes="Compare mestayer_perfidious_brother_1720 (Mestayer's own text, 'Dedicated to Mr. Theobald', 1720) which was also downloaded for contrast."),
dict(slug="richard_ii_1720",prio=1,title="The Tragedy of King Richard the II. As it is acted at the Theatre in Lincoln's-Inn-Fields. Alter'd from Shakespear, by Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for G. Strahan, W. Mears, T. Meighan, B. Barker; sold by J. Morphew, 1720. Only early edition.",
 sources=[],clean=[],
 complete="NOT OBTAINED.",
 notes="""Not on archive.org (searched titles 'king richard'/'tragedy of king richard'/'richard the ii'/'richard' 1719-1721, creator Theobald, creator Shakespeare 1700-1740; only Cornmarket facsimiles of OTHER plays and Shakespeare's own Richard II found).
Not in HathiTrust: the complete HathiTrust inventory file hathi_full_20260901.txt.gz (1.22 GB) was streamed and grepped for 'theobald', 'richard the ii', etc.; no 1720 Richard II record exists (HathiTrust holds only Theobald's Raleigh 1719, Shakespeare Restored 1726 and the Shakespeare editions).
Google Books: a record exists only for the Cornmarket Press 1969 facsimile (id DJwIAQAAIAAJ, 'No eBook available'); Google Books search/API/text views are blocked from here (HTTP 403 'automated queries' / 429 quota), so no Google-digitised original could be checked.
Chadwyck-Healey English Verse Drama has a TEI text (UVA mirror: https://xtf.lib.virginia.edu/xtf/view?docId=chadwyck_evd/uvaGenText/tei/chevd_V2.0347.xml) but it sits behind an AWS-WAF JavaScript challenge / licence wall - not attempted further. Yale digital-collections records 10000563 / 10000056 (same WAF block). Folger catalog record 181610 (HTTP 403).
ECCO (Gale) has the page images + OCR (ESTC T-number in ECCO); not accessible here. archive.org lending-library Cornmarket facsimiles have their OCR restricted (HTTP 401 on djvu.txt), as seen for The Comical Gallant."""),
dict(slug="orestes_1731",prio=1,title="Orestes: a dramatic opera. As it is acted at the Theatre-Royal in Lincoln's-Inn-Fields. Written by Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for J. Watts, 1731 (imprint per ESTC; not legible in this OCR). FIRST (only) edition.",
 sources=[ia_src("orestes_1731","bim_eighteenth-century_orestes-a-dramatic-oper_theobald-mr-lewis_1731","BL microfilm reel IA40313305-54; tesseract OCR.")],
 clean=[("orestes_1731.clean.txt","full volume: dedication, prologue, five acts with the sung parts, epilogue")],
 complete="90 frames; complete.",notes=""),
dict(slug="fatal_secret_1735",prio=1,title="The Fatal Secret. A tragedy. As it is acted at the Theatre-Royal, in Covent-Garden. By Mr. Theobald",author="Lewis Theobald (adapted from Webster, The Duchess of Malfi)",
 edition="London: printed for J. Watts, 1735. FIRST (only) edition; acted 1733.",
 sources=[ia_src("fatal_secret_1735","bim_eighteenth-century_the-fatal-secret-a-trag_theobald-mr_1735","BL microfilm reel IA40313615-52; tesseract OCR - UNUSABLE, see notes.")],
 clean=[("fatal_secret_1735.clean_UNUSABLE.txt","cleaner output kept only for the record; ~92% of lines are gibberish")],
 complete="73 frames are present as images, but the OCR text is garbage for almost the whole play: only ~16 of 193 25-line blocks are legible English (none of the play's character names - Bosola, Antonio, Ferdinand, the Duchess - are recoverable by grep). The microfilm frames appear to have been photographed rotated/inverted, so IA's tesseract pass produced mirror-nonsense such as '2ajquuojzrajun 441 31 f op Baq oz ayBnc'.",
 notes="""No re-OCR of the page images was attempted. The page images (PDF) are at https://archive.org/download/bim_eighteenth-century_the-fatal-secret-a-trag_theobald-mr_1735 should anyone want to OCR them with rotation correction.
No other digitised copy located: no HathiTrust record (full inventory grep), no second archive.org copy (title/creator/date searches), Google Books not reachable from here. ECCO holds the BL copy."""),
dict(slug="happy_captive_1741",prio=1,title="The Happy Captive, an English opera. With an interlude, in two comick scenes, betwixt Signor Capoccio ... and Signora Dorinna",author="Lewis Theobald",
 edition="London: printed for J. Watts, 1741 (per ESTC). FIRST (only) edition.",
 sources=[ia_src("happy_captive_1741","bim_eighteenth-century_the-happy-captive-an-en_theobald-mr_1741","BL microfilm reel IA40313615-83; tesseract OCR.")],
 clean=[("happy_captive_1741.clean.txt","full volume: dedication, three acts of the opera with the comic interlude")],
 complete="48 frames; complete (short opera libretto, c. 7,000 words).",notes="OCR noisier than average (many junk lines removed); sung verse mostly legible."),
# ---------------- PRIORITY 2 ----------------
dict(slug="electra_1714",prio=2,title="Electra: a tragedy. Translated from Sophocles, with notes. By Mr. Theobald",author="Lewis Theobald (tr. Sophocles)",
 edition="FIRST edition year, two distinct 1714 printings obtained: copy A 'printed for Bernard Lintott at the Cross-Keys' with Theobald's name and notes; copy B ('Electra, a tragedy. Translated from the Greek of Sophocles') is a separate 1714 printing 'printed for J. Watts, and sold by W. Lewis', shorter and without the notes.",
 sources=[ia_src("electra_1714","bim_eighteenth-century_electra-a-tragedy-tran_sophocles_1714","copy A, 95 frames; reel IA40313515-70"),ia_src("electra_1714","bim_eighteenth-century_electra-a-tragedy-tran_sophocles_1714_0","copy B, 83 frames; reel IA40313517-47")],
 clean=[("electra_1714_copyA.clean.txt","with notes"),("electra_1714_copyB.clean.txt","without notes")],
 complete="Both complete.",notes="Later acting editions (1777 Bell, 1780) also exist on archive.org: electratragedy00soph, electratragedyas00sophuoft, bim_..._sophocles_1777, bim_..._sophocles_1780 (not downloaded)."),
dict(slug="oedipus_1715",prio=2,title="Oedipus, King of Thebes: a tragedy. Translated from Sophocles, with notes. By Mr. Theobald",author="Lewis Theobald (tr. Sophocles)",
 edition="London: printed for Bernard Lintott, 1715. FIRST edition.",
 sources=[ia_src("oedipus_1715","bim_eighteenth-century_oedipus-king-of-thebes_sophocles_1715","reel IA40313517-21; 95 frames")],
 clean=[("oedipus_1715.clean.txt","full volume with Theobald's notes")],complete="Complete.",notes=""),
dict(slug="plutus_1715",prio=2,title="Plutus: or, the World's Idol. A comedy. Translated from the Greek of Aristophanes. By Mr. Theobald",author="Lewis Theobald (tr. Aristophanes)",
 edition="London: printed for Jonas Brown, 1715. FIRST edition (prose translation with notes).",
 sources=[ia_src("plutus_1715","bim_eighteenth-century_plutus-or-the-worlds-_aristophanes_1715","reel IA40313617-34; 82 frames")],
 clean=[("plutus_1715.clean.txt","full volume")],complete="Complete.",notes=""),
dict(slug="clouds_1715",prio=2,title="The Clouds. A comedy. Translated from the Greek of Aristophanes. By Mr. Theobald",author="Lewis Theobald (tr. Aristophanes)",
 edition="London: printed for Jonas Brown, 1715. FIRST edition (prose translation with notes).",
 sources=[ia_src("clouds_1715","bim_eighteenth-century_the-clouds-a-comedy-tr_aristophanes_1715","reel IA40313617-34; 82 frames")],
 clean=[("clouds_1715.clean.txt","full volume")],complete="Complete.",notes=""),
dict(slug="cave_of_poverty_1715",prio=2,title="The Cave of Poverty, a poem. Written in imitation of Shakespeare. By Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for Jonas Browne, sold by J. Roberts, 1715. FIRST (only) edition. Two copies obtained.",
 sources=[ia_src("cave_of_poverty_1715","bim_eighteenth-century_the-cave-of-poverty-a-p_theobald-mr-lewis_1715","copy A: BL microfilm reel IA40313312-05; 57 frames"),ia_src("cave_of_poverty_1715","bib_fict_4103198","copy B: Johns Hopkins University (Sheridan Libraries) digitisation, 70 images incl. blanks; tesseract OCR")],
 clean=[("cave_of_poverty_1715_copyA.clean.txt","BL microfilm copy"),("cave_of_poverty_1715_copyB_JHU.clean.txt","JHU copy - fewer noise lines, better for the preface")],
 complete="Complete (preface + poem in six-line stanzas). A third copy exists: bim_eighteenth-century_the-cave-of-poverty-a-p_theobald-mr-lewis_1715_0.",notes=""),
dict(slug="mausoleum_1714",prio=2,title="The Mausoleum. A poem. Sacred to the memory of Her late Majesty Queen Anne. Written by Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for Jonas Browne, 1714 (per ESTC; imprint not legible in this OCR). FIRST (only) edition.",
 sources=[ia_src("mausoleum_1714","bim_eighteenth-century_the-mausoleum-a-poem-s_theobald-mr_1714","reel IA40313615-52; 30 frames")],
 clean=[("mausoleum_1714.clean.txt","short poem, c. 1,700 words")],complete="Complete.",notes="OCR quality mediocre (0.86 good lines)."),
dict(slug="pindarick_ode_union_1707",prio=2,title="A Pindarick Ode on the Union. Written by Lew. Theobald, Gent.",author="Lewis Theobald",
 edition="London: printed for T. C. and sold by J. Morphew, 1707 (imprint legible in OCR). FIRST edition - Theobald's earliest publication.",
 sources=[ia_src("pindarick_ode_union_1707","bim_eighteenth-century_a-pindarick-ode-on-the-u_theobald-mr-lewis_1707","reel IA40316213-42; 12 frames")],
 clean=[("pindarick_ode_union_1707.clean.txt","complete ode")],complete="Complete.",notes="No other separately printed Pindaric odes by Theobald were found on archive.org/HathiTrust; the 1732 Epistle to Orrery (verse) was added instead."),
dict(slug="shakespeare_restored_1726",prio=2,title="Shakespeare Restored: or, a specimen of the many errors, as well committed, as unamended, by Mr. Pope in his late edition of this poet ... By Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for R. Francklin, J. Woodman and D. Lyon, C. Davis, 1726. FIRST edition (the only 18th-c. edition).",
 sources=[ia_src("shakespeare_restored_1726","bim_eighteenth-century_shakespeare-restored-or_theobald-mr-lewis_1726","reel IA40313515-17; 209 frames")],
 clean=[("shakespeare_restored_1726.clean.txt","whole volume c. 72,500 words")],
 complete="Complete. A second archive.org copy exists (bim_eighteenth-century_shakespeare-restored-or_theobald-lewis_1726) and HathiTrust has nyp.33433003253071 (pd).",notes="Mixed content: Theobald's prose argument plus long quotations from Shakespeare - quotations should be filtered before stylometric use."),
dict(slug="preface_works_of_shakespeare_1733",prio=2,title="Theobald's Dedication (to John, Earl of Orrery) and Preface to The Works of Shakespeare, in seven volumes (1733)",author="Lewis Theobald",
 edition="London: printed for A. Bettesworth and C. Hitch, J. Tonson, F. Clay, W. Feales, and R. Wellington, 1733 (issued January 1734). FIRST edition of Theobald's edition; the Preface was abridged in the 1740 second edition and later reprints.",
 sources=[{"kind":"gutenberg","id":"16346","url":"https://www.gutenberg.org/ebooks/16346","title":"Preface to the Works of Shakespeare (1734) - Augustan Reprint Society no. 20 (1949), ed. Hugh G. Dick; reproduces the ORIGINAL 1733 preface from the University of Michigan copy","date":"1949/2005","images":"","ocr":"human-proofread transcription (Distributed Proofreaders)","source":"Project Gutenberg (downloaded via archive.org mirror prefacetothework16346gut)","publisher":"","raw":["gutenberg_16346-0.txt"],"note":"clean transcription; the extracted file omits Dick's introduction and the ARS boilerplate"},
          ia_src("preface_works_of_shakespeare_1733","worksofshakespe01shak","Boston Public Library copy of vol. 1 (1733); ABBYY FineReader OCR; 652 images. Only the dedication + preface (lines 125-3384 of the OCR) were extracted.")],
 clean=[("theobald_1733_preface.gutenberg_transcription.txt","PREFERRED: clean transcription of the 1733 Preface (c. 15,800 words), title-page to end of preface"),("theobald_1733_dedication_and_preface.ocr.clean.txt","OCR of the same preface PLUS the Dedication to Lord Orrery, from the BPL copy of vol. 1")],
 complete="Complete.",notes="Other 1733 copies on archive.org: worksofshakespea001shak (BPL), worksshakespear03unkngoog/07unkngoog (Google scans); HathiTrust hvd.32044082535436 etc. Wikisource also has the abridged Preface as reprinted in Johnson-Steevens 1778 (not the 1733 text)."),
dict(slug="harlequin_sorcerer_1725",prio=2,title="A dramatick entertainment, call'd Harlequin a Sorcerer: with the loves of Pluto and Proserpine. As perform'd at the Theatre Royal in Lincoln's-Inn-Fields",author="Lewis Theobald (words); music by J. E. Galliard",
 edition="London: printed and sold by T. Wood, 1725 (per ESTC). FIRST edition (sung parts only, as printed).",
 sources=[ia_src("harlequin_sorcerer_1725","bim_eighteenth-century_a-dramatick-entertainmen_theobald-mr-lewis_1725","reel IA40310313-90; 23 frames")],
 clean=[("harlequin_sorcerer_1725.clean.txt","c. 1,700 words of sung verse")],complete="Complete.",notes="A 1753 Covent Garden edition is on archive.org as harlequinsorcer00lewgoog (Google scan) - not downloaded."),
dict(slug="rape_of_proserpine_1727",prio=2,title="The Rape of Proserpine: as it is acted at the Theatre-Royal in Lincoln's-Inn-Fields. Written by Mr. Theobald. And set to musick by Mr. Galliard",author="Lewis Theobald",
 edition="London: printed for T. Wood, 1727 (per ESTC). FIRST edition.",
 sources=[ia_src("rape_of_proserpine_1727","bim_eighteenth-century_the-rape-of-proserpine-_theobald-mr-lewis_1727","reel IA40313307-78; 26 frames")],
 clean=[("rape_of_proserpine_1727.clean.txt","c. 2,900 words")],complete="Complete.",notes="1731 edition also on archive.org (bim_eighteenth-century_the-rape-of-proserpine-_theobald-mr-lewis_1731)."),
dict(slug="perseus_and_andromeda_1730",prio=2,title="Perseus and Andromeda. As it is performed at the Theatre Royal in Lincoln's-Inn-Fields. Adorn'd with copper-plates",author="Lewis Theobald (attributed; Lincoln's-Inn-Fields version)",
 edition="London: printed and sold by Tho. Wood in Little Britain, 1730 (imprint legible). FIRST edition; two copies obtained. (5th ed. 1731 also on archive.org.)",
 sources=[ia_src("perseus_and_andromeda_1730","bim_eighteenth-century_perseus-and-andromeda-a_theobald-mr-lewis_1730","copy A: BL microfilm, 27 frames"),ia_src("perseus_and_andromeda_1730","perseusandromeda00theo","copy B: Rice University (Fondren) scan, 46 images incl. plates")],
 clean=[("perseus_and_andromeda_1730_copyA.clean.txt",""),("perseus_and_andromeda_1730_copyB_Rice.clean.txt","cleaner copy")],complete="Complete.",notes=""),
dict(slug="orpheus_and_eurydice_1740",prio=2,title="Orpheus and Eurydice. An opera. As it is performed at the Theatre Royal in Covent Garden. Set to musick by John-Frederick Lampe",author="Lewis Theobald",
 edition="London: printed for J. Watts (per ESTC), 1739 [i.e. Feb. 1740 N.S.] and 1740. Both the 1739-dated first edition and the 1740 edition obtained.",
 sources=[ia_src("orpheus_and_eurydice_1740","bim_eighteenth-century_orpheus-and-eurydice-an_theobald-mr-lewis_1739","1739-dated edition, 29 frames"),ia_src("orpheus_and_eurydice_1740","bim_eighteenth-century_orpheus-and-eurydice-an_theobald-mr-lewis_1740","1740 edition, 21 frames")],
 clean=[("orpheus_and_eurydice_1739.clean.txt",""),("orpheus_and_eurydice_1740.clean.txt","")],complete="Complete.",notes="1777 edition also on archive.org."),
dict(slug="decius_and_paulina_1719",prio=2,title="Decius and Paulina, a masque, to which are added, the other musical entertainments, as perform'd at the Theatre in Lincoln's-Inn-Fields, in the dramatic opera of Circe. Written by Mr. Theobald, and set to musick by Mr. Galliard",author="Lewis Theobald",
 edition="London: printed for Jonas Brown, 1719 (per ESTC). FIRST edition (the masque was performed in 1718 within Circe).",
 sources=[ia_src("decius_and_paulina_1719","bim_eighteenth-century_decius-and-paulina-a-ma_theobald-mr_1719","reel IA40313615-83; 29 frames")],
 clean=[("decius_and_paulina_1719.clean.txt","c. 1,650 words")],complete="Complete but very noisy microfilm (about half the OCR lines were junk and removed).",notes=""),
dict(slug="pan_and_syrinx_1718",prio=2,title="Pan and Syrinx: an opera of one act, as it is perform'd at the Theatre in Lincoln's-Inn-Fields. Written by Mr. Theobald, and set to musick by Mr. Galliard",author="Lewis Theobald",
 edition="London: printed for W. Mears, J. Browne and others, 1718 (imprint legible). FIRST edition.",
 sources=[ia_src("pan_and_syrinx_1718","bim_eighteenth-century_pan-and-syrinx-an-opera_theobald-mr-lewis_1718","21 frames")],
 clean=[("pan_and_syrinx_1718.clean.txt","c. 1,800 words")],complete="Complete.",notes=""),
dict(slug="apollo_and_daphne_1726",prio=2,title="Vocal parts of an entertainment, called Apollo and Daphne: or, the burgo-master trick'd. As perform'd at the Theatre Royal in Lincoln's-Inn-Fields",author="attributed to Lewis Theobald",
 edition="London: printed for T. Wood, and sold at the Theatre Royal, 1726. FIRST edition. (Bonus item; attribution to Theobald follows ESTC/archive.org.)",
 sources=[ia_src("apollo_and_daphne_1726","bim_eighteenth-century_vocal-parts-of-an-entert_theobald-mr-lewis_1726","21 frames")],
 clean=[("apollo_and_daphne_1726.clean.txt","c. 1,100 words")],complete="Complete.",notes="1731 and 1734 editions also on archive.org."),
dict(slug="epistle_to_orrery_1732",prio=2,title="An Epistle humbly addressed to the Right Honourable John, Earl of Orrery. By L. Theobald",author="Lewis Theobald",
 edition="London: printed for W. Mears at the Lamb in the Old-Baily, 1732. FIRST edition (verse epistle). Bonus item.",
 sources=[ia_src("epistle_to_orrery_1732","bim_eighteenth-century_an-epistle-humbly-addres_theobald-mr-lewis_1732","10 frames")],
 clean=[("epistle_to_orrery_1732.clean.txt","c. 1,100 words")],complete="Complete.",notes=""),
dict(slug="censor_1717",prio=2,title="The Censor (essay periodical), Vols. I-III, second (collected) edition",author="Lewis Theobald",
 edition="London: printed for Jonas Browne, 1717 (collected edition of the 96 numbers, 11 Apr.-17 Jun. 1715 and 1 Jan.-1 Jun. 1717). This IS the 1717 collected edition asked for (title pages read 'The Censor. Vol. I/II/III ... 1717').",
 sources=[ia_src("censor_1717","sim_censor_the-censor_april-11-june-17-1715_1_1-30","Vol. I (nos. 1-30); microfilm reel IA40607326-21; tesseract OCR"),ia_src("censor_1717","sim_censor_the-censor_january-01-march-16-1717_2_31-63","Vol. II (nos. 31-63)"),ia_src("censor_1717","sim_censor_the-censor_march-19-june-01-1717_3_64-96","Vol. III (nos. 64-96)")],
 clean=[("censor_vol1_nos1-30.clean.txt",""),("censor_vol2_nos31-63.clean.txt",""),("censor_vol3_nos64-96.clean.txt","")],
 complete="All three volumes complete (c. 130,000 words).",notes="This OCR rendered long-s as 'f' rather than 'ſ', so several thousand automatic f->s corrections were applied; residual 'f' forms remain in ambiguous words."),
dict(slug="merlin_1734",prio=2,title="The Vocal Parts of an Entertainment, call'd Merlin; or, the Devil of Stone-Henge ... with a succinct account of Stone-Henge and Merlin",author="Lewis Theobald",
 edition="London: printed for J. Watts, 1734. Only edition.",sources=[],clean=[],complete="NOT OBTAINED.",
 notes="Not on archive.org (title searches 'merlin' 1730-45, 'vocal parts', 'stone-henge'/'stonehenge'); not in the HathiTrust inventory; Google Books unreachable from here. Known to exist in ECCO (Gale) - the ECCO print-on-demand reprint ISBN 9781171448617 confirms it."),
dict(slug="antiochus_and_stratonice_1717",prio=2,title="The History of the Loves of Antiochus and Stratonice: in which are interspers'd some accounts relating to Greece and Syria. By Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for Jonas Browne, 1717 (per ESTC). FIRST edition (prose romance). Bonus item.",
 sources=[ia_src("antiochus_and_stratonice_1717","bim_eighteenth-century_the-history-of-the-loves_theobald-mr-lewis_1717","317 frames")],
 clean=[("antiochus_and_stratonice_1717.clean.txt","c. 64,000 words of prose")],complete="Complete.",notes=""),
dict(slug="memoirs_of_raleigh_1719",prio=2,title="Memoirs of Sir Walter Raleigh; his life, his military and naval exploits, his preferments and death ... Written by Mr. Theobald",author="Lewis Theobald",
 edition="London: printed for W. Mears, 1719. FIRST edition (prose). Bonus item.",
 sources=[ia_src("memoirs_of_raleigh_1719","bim_eighteenth-century_memoirs-of-sir-walter-ra_theobald-mr-lewis_1719","")],
 clean=[("memoirs_of_raleigh_1719.clean.txt","c. 10,500 words")],complete="Complete.",notes="Also on archive.org as memoirssirwalte00theogoog (Google scan) and HathiTrust mdp.39015063625019."),
dict(slug="life_of_cato_1713",prio=2,title="The Life and Character of Marcus Portius Cato Uticensis: collected from the best ancient Greek and Latin authors; and designed for the readers of Cato, a tragedy",author="attributed to Lewis Theobald",
 edition="London: printed for Bernard Lintott, 1713. FIRST edition (prose). Bonus item.",
 sources=[ia_src("life_of_cato_1713","lifeofcharactero00theo","Rice University (Fondren) scan; ABBYY OCR (long-s rendered as 'f')")],
 clean=[("life_of_cato_1713.clean.txt","c. 9,000 words")],complete="Complete.",notes="Wikisource has a transcription index for this pamphlet (Index:The life of and character of Marcus Portius Cato Uticensis - Theobald (1713).djvu); see any wikisource_* file in this folder if it was retrievable."),
dict(slug="mestayer_perfidious_brother_1720",prio=2,title="The Perfidious Brother, a tragedy. As it was acted at the New Theatre in Little Lincolns-Inn-Fields. Dedicated to Mr. Theobald",author="Henry Mestayer",
 edition="London, 1720. Mestayer's own version of the play Theobald had reworked in 1715 (with a dedication attacking Theobald). Calibration/contrast item, not by Theobald.",
 sources=[ia_src("mestayer_perfidious_brother_1720","bim_eighteenth-century_the-perfidious-brother-_mestayer-henry_1720","62 frames")],
 clean=[("mestayer_perfidious_brother_1720.clean.txt","")],complete="Complete.",notes=""),
# ---------------- PRIORITY 3 ----------------
dict(slug="cibber_love_makes_a_man_1701",prio=3,title="Love makes a Man: or, the Fop's Fortune. A comedy ... Written by C. Cibber",author="Colley Cibber (from Fletcher's The Custom of the Country and The Elder Brother)",
 edition="Copy B (..._1701_0, 64 frames, 'by His Majesty's servants', printed for Richard Parker et al., 1701) = FIRST edition. Copy A (..._1701, 82 frames, 'by Her Majesty's servants') is catalogued as 1701 but the Queen's-servants wording means it is a reprint of 1702-1714.",
 sources=[ia_src("cibber_love_makes_a_man_1701","bim_eighteenth-century_love-makes-a-man-or-th_cibber-colley_1701_0","copy B = 1701 first edition"),ia_src("cibber_love_makes_a_man_1701","bim_eighteenth-century_love-makes-a-man-or-th_cibber-colley_1701","copy A = later (1702-14) edition, catalogued 1701")],
 clean=[("cibber_love_makes_a_man_1701_copyB_1701_0.clean.txt","PREFERRED (first edition)"),("cibber_love_makes_a_man_1701_copyA_1701.clean.txt","later edition")],complete="Both complete.",notes=""),
dict(slug="farquhar_inconstant_1702",prio=3,title="The Inconstant: or, the Way to Win Him. A comedy ... Written by Mr. George Farquhar",author="George Farquhar (from Fletcher's The Wild-Goose Chase)",
 edition="London, 1702. FIRST edition.",
 sources=[ia_src("farquhar_inconstant_1702","bim_eighteenth-century_the-inconstant-or-the-_farquhar-george_1702","")],
 clean=[("farquhar_inconstant_1702.clean.txt","")],complete="Complete.",notes="Many later editions on archive.org (1718, 1727, 1728 ...)."),
dict(slug="cibber_richard_iii_1700",prio=3,title="The Tragical History of King Richard III. As it is acted at the Theatre Royal, by His Majesty's Servants. Alter'd from Shakespear by C. Cibber",author="Colley Cibber",
 edition="London: printed for B. Lintott at the Middle Temple-Gate, 1700 (imprint legible). FIRST edition (archive.org 'Early English Books 1641-1700' microfilm set; catalogued under Shakespeare).",
 sources=[ia_src("cibber_richard_iii_1700","bim_early-english-books-1641-1700_the-tragical-history-of-_shakespeare-william_1700","67 frames; reel IA40313704-45")],
 clean=[("cibber_richard_iii_1700.clean.txt","")],complete="Complete.",notes="Later editions 1718-1790 also on archive.org."),
dict(slug="granville_jew_of_venice_1701",prio=3,title="The Jew of Venice. A comedy. As it is acted at the Theatre in Little-Lincolns-Inn-Fields, by His Majesty's servants",author="George Granville, Baron Lansdowne (from The Merchant of Venice)",
 edition="London, 1701. FIRST edition.",
 sources=[ia_src("granville_jew_of_venice_1701","bim_eighteenth-century_the-jew-of-venice-a-com_lansdowne-george-granvi_1701","")],
 clean=[("granville_jew_of_venice_1701.clean.txt","")],complete="Complete (includes the masque Peleus and Thetis if printed with it; a separate 1701 masque printing also exists on archive.org).",notes="1711 edition and 1713/1732 collected editions also on archive.org."),
dict(slug="dennis_comical_gallant_1702",prio=3,title="The Comical Gallant: or the Amours of Sir John Falstaffe. A comedy ... By Mr. Dennis",author="John Dennis (from The Merry Wives of Windsor)",
 edition="London: printed and sold by A. Baldwin, 1702. Only edition.",
 sources=[{"kind":"hathitrust (extracted features only)","id":"pst.000005278602","url":"https://babel.hathitrust.org/cgi/pt?id=pst.000005278602","title":"The comical gallant ... (HathiTrust record 012293067, OCLC 317069827; Penn State copy; rights 'pd')","date":"1702 [in fact the 1969 Cornmarket facsimile - the page tokens include 'PUBLISHED 1969', 'NORWICH', 'SBN']","images":"82","ocr":"HathiTrust OCR exists but page text is unreachable (Cloudflare); only the HTRC Extracted-Features bag-of-words per page was obtainable","source":"HTRC EF API https://data.htrc.illinois.edu/ef-api/volumes/pst.000005278602","publisher":"","raw":["htrc_ef_pst.000005278602.json"],"note":"per-page token/POS counts (43,591 body tokens over 82 pages); word ORDER is not recoverable"}],
 clean=[],complete="FULL TEXT NOT OBTAINED. archive.org has only the 1969 Cornmarket facsimile as a lending-library item (comicalgallant170000shak) whose OCR download is restricted (HTTP 401). Google Books c5wIAQAAIAAJ = same facsimile, no eBook.",
 notes="The HTRC extracted-features JSON gives page-level word counts (with POS tags) - usable for frequency-based stylometry only."),
dict(slug="burnaby_love_betrayd_1703",prio=3,title="Love Betray'd; or, the Agreable Disapointment. A comedy. As it was acted at the Theatre in Lincolns-Inn-Fields",author="William Burnaby (from Twelfth Night)",
 edition="London, 1703. FIRST edition.",
 sources=[ia_src("burnaby_love_betrayd_1703","bim_eighteenth-century_love-betrayd-or-the-a_burnaby-william_1703","")],
 clean=[("burnaby_love_betrayd_1703.clean.txt","")],complete="Complete but noisy microfilm (c. 1,300 junk lines removed).",notes=""),
dict(slug="hill_henry_v_1723",prio=3,title="King Henry the Fifth: or, the Conquest of France, by the English. A tragedy. As it is acted at the Theatre-Royal in Drury-Lane, by His Majesty's servants",author="Aaron Hill",
 edition="London: printed for W. Chetwood, 1723 (imprint legible). FIRST edition.",
 sources=[ia_src("hill_henry_v_1723","bim_eighteenth-century_king-henry-the-fifth-or_hill-aaron_1723","")],
 clean=[("hill_henry_v_1723.clean.txt","")],complete="Complete.",notes="1724 and 1765 editions also on archive.org."),
dict(slug="sheffield_julius_caesar_1723",prio=3,title="The Tragedy of Julius Caesar, altered; with a prologue and chorus [and] The Tragedy of Marcus Brutus - in The Works of John Sheffield, Earl of Mulgrave, Marquis of Normanby, and Duke of Buckingham, vol. I",author="John Sheffield, Duke of Buckingham",
 edition="London: printed for John Barber, 1723 (first collected Works, posthumous; the two tragedies were first printed here). Vol. II (prose) also downloaded but not extracted.",
 sources=[ia_src("sheffield_julius_caesar_1723","bim_eighteenth-century_the-works-of-john-sheffi_buckingham-john-sheffie_1723_1","Vol. I, 471 frames; plays at OCR lines 11749-24327"),ia_src("sheffield_julius_caesar_1723","bim_eighteenth-century_the-works-of-john-sheffi_buckingham-john-sheffie_1723_2","Vol. II (prose; not extracted)")],
 clean=[("sheffield_julius_caesar_1723.clean.txt","Julius Caesar altered, with prologue and the choruses"),("sheffield_marcus_brutus_1723.clean.txt","Marcus Brutus (Sheffield's sequel play) - bonus")],
 complete="Both plays complete.",notes="The 1729 Works (worksjohnsheffi01buckgoog) and 1752 Poems on Several Occasions (poemsonseveraloc00buck) also contain both plays. Note that two of the choruses in Marcus Brutus ('Two Chorus's to the Tragedy of Brutus') are by Alexander Pope, not Sheffield; the Julius Caesar choruses are Sheffield's own."),
dict(slug="motteux_don_quixote_1700",prio=3,title="The History of the Renown'd Don Quixote de la Mancha ... Translated from the original by several hands: and publish'd by Peter Motteux - Part I, Book III ch. IX to Book IV ch. IX (= Cervantes Part I chs. 23-36, the Cardenio/Dorotea/Fernando story)",author="Peter Motteux (ed./tr.) et al.",
 edition="London: printed for Sam. Buckley at the Dolphin, 1700-1703 (imprint legible; FIRST edition; the archive.org item, catalogued '1700', contains the whole set incl. Part II). Motteux keeps Cervantes' four 'Books' of Part I, so the extracted chapters are numbered Book III ch. IX-XIII and Book IV ch. I-IX.",
 sources=[ia_src("motteux_don_quixote_1700","bim_early-english-books-1641-1700_the-history-of-the-renow_cervantes-miguel-de_1700","1412 frames; reel IA40313713-33; tesseract OCR; extracted OCR lines 17046-30428")],
 clean=[("motteux_dq_partI_ch23-36_cardenio.clean.txt","c. 71,000 words: from 'What befel the Renown'd Don Quixote in the Sierra Morena' (Book III ch. IX = orig. 23) to the end of Book IV ch. IX (orig. 36), i.e. up to the head of 'The History of the famous Princess Micomicona continu'd' (orig. 37)")],
 complete="Extract complete; includes the interpolated Novel of the Curious Impertinent (chs. 33-35).",notes="A 1705-06 second-edition set (4 vols) is also on archive.org (bim_eighteenth-century_the-history-of-the-renow_cervantes-saavedra-migu_1705-06-01_1..4)."),
dict(slug="phillips_don_quixote_1687",prio=3,title="The History of the most Renowned Don Quixote of Mancha: and his trusty squire Sancho Pancha, now made English according to the humour of our modern language ... by J. P. [John Phillips] - Part I chs. 23-36",author="John Phillips (tr.)",
 edition="London: printed by Thomas Hodgkin, and sold by William Whitwood, 1687 (imprint legible). FIRST (only) edition, folio. Two archive.org copies exist; both downloaded (copy _1687 used for the extract).",
 sources=[ia_src("phillips_don_quixote_1687","bim_early-english-books-1641-1700_the-history-of-the-most-_cervantes-miguel-de_1687","647 frames; reel IA40310608-90; extracted OCR lines 11701-21199"),ia_src("phillips_don_quixote_1687","bim_early-english-books-1641-1700_the-history-of-the-most-_cervantes-miguel-de_1687_0","second copy (reel IA40313017-16), whole-book OCR kept, not extracted")],
 clean=[("phillips_dq_partI_ch23-36_cardenio.clean.txt","c. 70,500 words: from the flight into the 'Black Mountain' (Sierra Morena; Phillips Book III ch. IX = orig. 23; the chapter heading itself was lost by the OCR) to the end of Book IV ch. IX (orig. 36), stopping before 'The Continuation of the History of the Famous Princess of Micomicon' (orig. 37)")],
 complete="Extract complete.",notes="Folio double-column layout; OCR column order is occasionally scrambled at page breaks."),
]
# ---------- write PROVENANCE.md ----------
def q_str(path):
    if not os.path.exists(path): return "(file missing)"
    g,w=quality(path); return f"{w:,} words; {g*100:.0f}% of text lines pass a dictionary check"
index_rows=[]
for it in ITEMS:
    d=f"{BASE}/{it['slug']}"; os.makedirs(d,exist_ok=True)
    L=[f"# {it['title']}", "", f"**Slug:** `{it['slug']}`  ", f"**Priority:** {it['prio']}  ", f"**Author:** {it['author']}  ", f"**Edition / date:** {it['edition']}", "", "## Sources"]
    if not it['sources']: L.append("_None obtained._")
    for s in it['sources']:
        L+= [f"- **{s['kind']}** `{s['id']}` - {s['url']}",
             f"  - catalogue title: {s['title']}",
             f"  - date field: {s['date']}; images/frames: {s['images']}; OCR engine: {s['ocr']}",
             f"  - digitised from / contributor: {s['source']}" + (f"; publisher: {s['publisher']}" if s.get('publisher') else ""),
             f"  - raw file(s) saved here (exactly as downloaded): " + (", ".join('`'+r+'`' for r in s['raw']) if s['raw'] else "(none)"),
             (f"  - note: {s['note']}" if s['note'] else "")]
    L+=["", "## Cleaned text(s)"]
    if not it['clean']: L.append("_None._")
    for f,note in it['clean']:
        L.append(f"- `{f}` - {note+'; ' if note else ''}{q_str(f'{d}/{f}')}")
    L+=["", "## Completeness", it['complete'], "", "## OCR quality / notes",
        "Cleaning: IA djvu.txt was normalised (ſ->s), microfilm target frames and junk lines trimmed, page numbers/signatures/running heads dropped, end-of-line hyphenation joined, and a CONSERVATIVE long-s correction applied (words with 'f' that are not in a modern frequency list are replaced by their 's' variant when that variant is common; a short override list covers so/she/sir/see/such/some...). Ambiguous real words (fame/same, fell/sell, fold/sold, found/sound, foul/soul, fit/sit ...) were left unchanged. Statistics of every change are in the `*.cleanstats.json` beside each cleaned file. Expect residual OCR noise; the '% of lines pass a dictionary check' figure above is a rough legibility score (modern-English word list; 18th-c. spellings count against it)." if it['clean'] else "",
        it['notes']]
    open(f"{d}/PROVENANCE.md","w",encoding='utf-8').write("\n".join(x for x in L if x is not None)+"\n")
    status = "FOUND" if it['clean'] else ("PARTIAL/UNUSABLE" if it['sources'] else "NOT FOUND")
    if it['slug']=='fatal_secret_1735': status="OCR UNUSABLE (images only)"
    if it['slug']=='dennis_comical_gallant_1702': status="NOT FOUND (bag-of-words only)"
    best=""
    if it['clean']:
        best=", ".join(f"`{f}`" for f,_ in it['clean'][:2]) + (" ..." if len(it['clean'])>2 else "")
    index_rows.append((it['prio'],it['slug'],it['title'].split(' - ')[0][:95],status,best))
# ---------- INDEX.md ----------
I=["# raw_external corpus index - Lewis Theobald and Restoration/18th-century adaptations", "",
   "Each sub-folder holds (a) the raw OCR/transcription exactly as downloaded (`*_djvu.txt`, `gutenberg_*.txt`, `*.ia_metadata.json`), (b) cleaned UTF-8 text(s) (`*.clean.txt`, with `*.cleanstats.json`), and (c) `PROVENANCE.md`.",
   "", "## Summary table", "", "| Pri | slug | work | status | cleaned file(s) |", "|---|---|---|---|---|"]
for r in sorted(index_rows): I.append(f"| {r[0]} | `{r[1]}` | {r[2]} | **{r[3]}** | {r[4]} |")
I+=["", "## Not found / not obtainable (details in each PROVENANCE.md)", "",
"- **Priority 1 - `richard_ii_1720`** (Theobald, *The Tragedy of King Richard the II*, 1720): no digitised copy with accessible text anywhere reachable. Not on archive.org; not in HathiTrust's complete inventory (hathi_full_20260901); Google Books has only the 1969 Cornmarket facsimile record (no eBook) and Google is blocked from here; Chadwyck-Healey English Verse Drama (UVA XTF) and Yale digital collections sit behind an AWS-WAF JavaScript challenge; ECCO (Gale) is paywalled. archive.org lending-library Cornmarket facsimiles keep their OCR behind HTTP 401.",
"- **Priority 1 - `fatal_secret_1735`**: the only digitised copy found (archive.org BL microfilm) has UNUSABLE OCR - the frames were filmed rotated, so tesseract emitted mirror-gibberish for ~92% of lines. Page images exist (PDF on archive.org); no re-OCR was attempted. No HathiTrust or second archive.org copy exists.",
"- **Priority 2 - `merlin_1734`** (*Merlin; or, the Devil of Stone-Henge*): not on archive.org, not in HathiTrust; exists in ECCO only (Google Books unverifiable from here).",
"- **Priority 3 - `dennis_comical_gallant_1702`**: full text not obtainable (archive.org copy restricted; HathiTrust page text behind Cloudflare). The HTRC Extracted-Features bag-of-words for HathiTrust pst.000005278602 was saved as a frequency-only fallback (note: that copy is itself the 1969 facsimile).",
"", "## Where I looked (and what was reachable)", "",
"- **archive.org** (`advancedsearch.php`, `metadata/`, `download/<id>/<id>_djvu.txt`): fully reachable. Queries run: `creator:(Theobald, Lewis)` (118 hits, both pages), `creator:(Theobald) AND mediatype:texts`, and title searches for every listed work (perfidious brother; king richard / tragedy of king richard / richard the ii / richard 1719-1721 / richard + creator Shakespeare 1700-1740; fatal secret; happy captive; orestes; oedipus king of thebes; plutus + aristophanes; clouds + aristophanes; mausoleum 1700-99; censor 1710-99 and `identifier:sim_censor_the-censor*`; merlin 1730-45 / merlin + stone-henge; vocal parts 1725-45; stone-henge/stonehenge 1700-99; decius and paulina; electra + sophocles/theobald; pindarick/pindaric/ode + theobald; naufragium britannicum; love makes a man; the inconstant + farquhar; richard III + cibber; tragical history of king richard 1700-30; jew of venice; comical gallant / amours of sir john; love betray'd / burnaby 1700-10; henry the fifth + hill; julius caesar + buckingham/sheffield; marcus brutus; works + creator buckingham 1720-30; don quixote + motteux, don quixote 1680-1712; publisher:cornmarket). The 'bim_eighteenth-century' and 'bim_early-english-books-1641-1700' items are British Library microfilm scans (the same microfilm ECCO/EEBO were made from) with tesseract OCR.",
"- **HathiTrust**: catalog and babel (page text) are behind a Cloudflare JavaScript challenge (HTTP 403 for curl and for a web fetch). Reachable: the Bib API (`catalog.hathitrust.org/api/volumes/brief/...`) and the full inventory `hathi_full_20260901.txt.gz` (streamed and grepped; 141 relevant rows saved to `_search_logs/hathitrust_inventory_hits_2026-09-01.tsv`). HathiTrust holds no 18th-c. Theobald play at all - only Raleigh 1719 (mdp.39015063625019), Shakespeare Restored 1726 (nyp.33433003253071), the Shakespeare editions, and Dennis's Comical Gallant (pst.000005278602). The HTRC Extracted-Features API (`data.htrc.illinois.edu/ef-api`) is reachable.",
"- **Google Books**: `googleapis.com/books/v1` returns 429 (daily quota exhausted for this egress), `books.google.com` returns 403 'automated queries'; the older `google.com/books/feeds` endpoint returns 500. Web-search snippets located only the Cornmarket facsimile records (DJwIAQAAIAAJ Richard II; c5wIAQAAIAAJ Comical Gallant).",
"- **Project Gutenberg**: only Theobald item is #16346 (the 1733 Preface, ARS reprint) - obtained. **Wikisource**: has Double Falshood (transcribed), the abridged 1778 Preface, and an index for the 1713 Life of Cato; API rate-limited (429). **Oxford Text Archive** (ECCO-TCP host): 504 gateway time-out. **Michigan quod.lib.umich.edu** (ECCO-TCP/EEBO-TCP): Cloudflare challenge. **UVA XTF (Chadwyck-Healey EVD)** and **Yale collections**: AWS WAF challenge (HTTP 202, empty). **WorldCat**: HTTP 429. **Gallica SRU**: reachable, no hits for Theobald/Stone-Henge/Fatal Secret. **MDZ (Munich)**: JavaScript-only UI, no open search API found. **Folger catalog**: 403.",
"", "## Extras obtained", "",
"Pan and Syrinx 1718, Apollo and Daphne 1726 (attrib.), Epistle to Orrery 1732 (verse), Antiochus and Stratonice 1717 (prose romance), Memoirs of Raleigh 1719 (prose), Life of Cato 1713 (prose, attrib.), Mestayer's Perfidious Brother 1720 (contrast text), Sheffield's Marcus Brutus 1723, second copies of Electra, Cave of Poverty, Perseus and Andromeda, Orpheus and Eurydice (1739 + 1740), Love Makes a Man, Phillips's Don Quixote. Theobald's own *Double Falshood* is NOT included here (assumed already in hand) but archive.org copies are: doublefalshoodor00shak (1728, 1st ed.), bib_fict_4103197_1 (1728 2nd ed., JHU), bim_eighteenth-century_double-falshood-or-the_theobald-mr-lewis_1728 / _1767 / _1769, doublefalshoodo00conggoog, cu31924013363894 (1920 reprint); Wikisource also has a transcription.",
"", "## Cleaning method (applies to every `*.clean.txt`)", "",
"`clean_ocr.py` (copy kept in `_search_logs/`): NFC-normalise; ſ->s; trim microfilm target frames / library plates at both ends; drop IA boilerplate, page-number and signature lines, junk lines (<2 letters, or short lines that are mostly symbols), and repeated running heads (per-item regex); join end-of-line hyphenation when the next line starts lower-case; collapse double spaces; conservative long-s correction using the `wordfreq` English list (replace an 'f' word only if it is itself rare (zipf<3) and an s-variant is common (zipf>=3 and >=1 point higher), plus a fixed override list for so/she/sir/see/sun/save/sin/send/slay/should/shall/such/some/since/say/said/side/son/sea/sense/speak... ; ambiguous common words left alone). Nothing else was altered: 18th-century spelling, capitalisation and italics-driven OCR errors remain. Word counts and per-file change logs are in `*.cleanstats.json`. The raw OCR is always kept alongside.",
"", "## Caveats for stylometry", "",
"- Translations (Electra, Oedipus, Plutus, Clouds) carry Theobald's verse/prose style but constrained by the source; Shakespeare Restored quotes Shakespeare at length; the pantomime librettos are short sung verse.",
"- Perfidious Brother 1715 is Theobald's rewriting of Mestayer's draft; Sheffield's Julius Caesar retains much Shakespeare; Cibber's Richard III, Granville's Jew of Venice, Hill's Henry V likewise retain Shakespearean lines - filter shared passages before using them as pure author profiles.",
"- OCR legibility scores are in each PROVENANCE.md; the weakest usable texts are Persian Princess (0.88), Happy Captive (0.87), Mausoleum (0.86), Decius and Paulina and Love Betray'd (noisy microfilm)."]
open(f"{BASE}/INDEX.md","w",encoding='utf-8').write("\n".join(I)+"\n")
print("wrote INDEX.md and", len(ITEMS), "PROVENANCE.md files")
