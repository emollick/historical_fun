#!/usr/bin/env python3
"""Build database_catalogue.csv for Legio IX Hispana from the raw EDH / EDCS downloads.

Inputs (all under raw/):
  edh_candidates_union.json, edh_records/HD*.{json,xml,html}, edh_rows_draft.json
  edcs_decoded_all.json (decoded monuments), edcs_candidates.json
Manual curation (person / rank / notes / include flag) is in CUR below, keyed by database id.
"""
import csv, json, re, html, os
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
NS = {'t': 'http://www.tei-c.org/ns/1.0'}

# ----------------------------------------------------------------------------
# Curation. include: 'yes' | 'flag' (attribution to IX Hispana uncertain / earlier
# cognomen / fragmentary) | 'no' (excluded, kept in CSV as a documented rejection)
# ----------------------------------------------------------------------------
CUR = {
 # ---------------- EDCS: Italy / Gaul / Balkans, Augustan-Julio-Claudian ----------------
 'EDCS-01401118': dict(person='C. Aninius, Lemonia, Bononia', rank='miles leg. VIIII (stip. XXII)', include='yes', notes='Aquileia group; no cognomen of legion given. Not in EDH.'),
 'EDCS-01401119': dict(person='Sex. Betutius Sex. f. Vol. Vianna(?), Vienna', rank='signifer leg. VIIII, veteranus', include='yes', notes='= EDH HD003697 (AE 1988, 583). No legion cognomen.'),
 'EDCS-01600184': dict(person='T. Cassius T. f. Firmus', rank='centurio leg. VIIII Hisp(anae); IIIIvir i.d.', include='yes', notes='Aquileia. Not in EDH.'),
 'EDCS-01600189': dict(person='C. Fabius C. f. Pub. Verona', rank='miles leg. VIIII Hispanae', include='yes', notes='CIL V 911; cited by livius.org as evidence for the legion in the Aquileia/Pannonia area under Augustus. Not in EDH.'),
 'EDCS-01600224': dict(person='Q. Vettidius Q. f. Cla. Beria', rank='miles leg. VIIII (stip. VIII)', include='yes', notes='Aquileia; no legion cognomen. Not in EDH.'),
 'EDCS-04200484': dict(person='L. Vinusius L. f.', rank='veteranus leg. VIIII Triumphalis', include='flag', notes='ILS 2240. Cognomen "Triumphalis": earlier (triumviral) title of a ninth legion; identity with the later IX Hispana is the usual assumption (Ritterling; Keppie) but not certain.'),
 'EDCS-04201559': dict(person='L. Mestrius C. f. Rom.', rank='(miles/veteranus) leg. IX', include='flag', notes='Ateste veteran colony (Augustan); legion IX without cognomen.'),
 'EDCS-04203381': dict(person='P. Cornelius Lentulus Scipio (cos. suff. AD 24)', rank='legatus Ti. Caesaris Aug. leg. VIIII Hispanae', include='yes', notes='ILS 940. Commander of the legion in Africa against Tacfarinas, AD 22-24 (Tac. Ann. 3.74). Not in EDH.'),
 'EDCS-04400181': dict(person='M. Moranus M. f. Rufus (brother of Moranus, miles leg. XI)', rank='optio leg. VIIII', include='yes', notes='InscrIt X 2, 252; the Porec/Parentium "tombstone of Moranus" cited by livius.org. Not in EDH.'),
 'EDCS-05100371': dict(person='C. Alebo Castici f.', rank='veteranus leg. VIIII', include='flag', notes='EDCS dates 50-1 BC: could be the Caesarian/triumviral Ninth rather than the imperial IX Hispana.'),
 'EDCS-05100973': dict(person='Albucius Vindilli f.', rank='veteranus miles leg. VIIII', include='yes', notes='CIL V 5818; no legion cognomen. Not in EDH.'),
 'EDCS-05400409': dict(person='M. Cocceius M. f. Pol. Severus', rank='primus pilus leg. VIIII Hispanae; praefectus leg. X Geminae', include='yes', notes='CIL V 7159. Praefectus (castrorum) of X Gemina implies a date c. AD 70-120 (X Gemina at Nijmegen until c. 104). Not in EDH.'),
 'EDCS-05400693': dict(person='M. Vibius Q. f. Pom.', rank='veteranus leg. IX Hispaniensis', include='yes', notes='= EDH HD003587 (AE 1987, 414). Augustan form "Hispaniensis".'),
 'EDCS-05400745': dict(person='L. Coelius Q. f.', rank='miles leg. VIIII, signifer; donatus phaleris torquibus armillis', include='flag', notes='ILS 2337. EDCS dates 50-1 BC: possibly the Caesarian/triumviral Ninth.'),
 'EDCS-08100002': dict(person='Sex. Aemilius Sex. f. Pom.', rank='(miles/veteranus) leg. VIIII', include='yes', notes='AE 1998, 522; no legion cognomen. Not in EDH.'),
 'EDCS-08400837': dict(person='C. Kafatius C. f. Ani. Capito', rank='veteranus leg. VIIII', include='yes', notes='CIL XII 260 = ILN Frejus 115; Forum Iulii veteran. Not in EDH.'),
 'EDCS-08400838': dict(person='[.] Iulius C. f.', rank='primus pilus leg. VIIII Hispanae; IIvir coloniae', include='yes', notes='CIL XII 261 = ILN Frejus 19. Not in EDH.'),
 'EDCS-08600717': dict(person='T. Crispius', rank='miles leg. IX', include='yes', notes='= EDH HD049599 (AE 1997, 1023).'),
 'EDCS-09201053': dict(person='[.] Blandius C. f. Vol. Latinus', rank='centurio leg. I Italicae, II Augustae, VIIII Hispanae, XX [V.V.]; donis donatus', include='yes', notes='CIL XII 2601 (Geneva). Post-66 (leg. I Italica). Not in EDH.'),
 'EDCS-09400433': dict(person='T. Aponius P. f. Ani.', rank='signifer leg. IX Hispaniensis, veteranus; donatus torquibus armillis phaleris', include='yes', notes='= EDH HD009867 (AE 1975, 446). Augustan form "Hispaniensis".'),
 'EDCS-11700356': dict(person='C. Novellius Q. f. Ani.', rank='veteranus leg. VIIII', include='yes', notes='= EDH HD004335 (AE 1979, 397).'),
 'EDCS-14805723': dict(person='C. Octavius P. f. Pub. Pastor, Verona', rank='signifer leg. VIIII; deductus Reate ab divo Aug. Vespasiano', include='yes', notes='CIL IX 4685. Veteran colonist settled at Reate by Vespasian (so discharged c. 70-79). Not in EDH.'),
 'EDCS-14805727': dict(person='L. Valerius Valens', rank='veteranus leg. VIIII; deductus Reate a divo Aug. Vespasiano', include='yes', notes='CIL IX 4689. Not in EDH.'),
 'EDCS-19700321': dict(person='M. Valerius M. f. Ani. Saturninus, Forum Iulii', rank='miles leg. VIIII Hispanae, centuria Antoni Kari (militavit XVII)', include='yes', notes='CIL VI 3639 (Rome). Not in EDH.'),
 'EDCS-19800432': dict(person='C. Fulvius [...]us (RE Fulvius 11)', rank='tribunus militum leg. IX Hisp(anae); later proconsul etc.', include='yes', notes='CIL VI 3675 = ILS 3783, votive to Concordia for Tiberius; EDCS dates AD 31. Not in EDH.'),
 'EDCS-22000190': dict(person='[...]ius Q. f. Pom.', rank='tribunus militum leg. VIIII; quaestor pro praetore; tribunus plebis', include='yes', notes='CIL XI 1838 (Arretium), Tiberian per EDCS. No legion cognomen. Not in EDH.'),
 'EDCS-22300276': dict(person='[.] C. f. Vol. [...] (with [.] Horatius Priscus)', rank='primus pilus leg. VIIII Hispanae', include='yes', notes='CIL XI 3112 (Falerii), amphitheatre builder. Not in EDH.'),
 'EDCS-22900976': dict(person='anonymous', rank='[...] leg. VIIII [...]; donatus hasta (fragmentary career)', include='flag', notes='CIL XI 5037 (Mevania); fragment also names a leg. [...] Gemina Pia [Fidelis]. Not in EDH.'),
 'EDCS-22901114': dict(person='[...] Proculus', rank='tribunus militum legionum IX et XXI', include='yes', notes='CIL XI 5173 (Vettona), Augustan senatorial career; legion IX without cognomen. Not in EDH.'),
 'EDCS-31200128': dict(person='M. Aemilius M. f. Pob. Soteria(?), eques, domo Osca', rank='veteranus leg. VIIII Hispaniensis; donatus torquibus armillis phaleris ab Imperatore', include='yes', notes='ILS 2321 (Cales). Not in EDH.'),
 'EDCS-08200279': dict(person='L. Aquillius C. f. Pom. Florus Turcianus Gallus', rank='tribunus militum leg. VIIII Macedonicae', include='flag', notes='= EDH HD026601 (Corinth). "IX Macedonica" = Augustan-period cognomen of a ninth legion, usually identified with the later IX Hispana (Ritterling; Keppie); flagged.'),
 'EDCS-27000426': dict(person='L. Aquillius C. f. Pom. Florus Turcianus Gallus', rank='tribunus militum leg. VIIII Macedonicae', include='flag', notes='= EDH HD056334 (Athens, CIL III 551 = ILS 928). Same man/cognomen issue as EDCS-08200279.'),
 'EDCS-16201101': dict(person='Q. Paesidius C. f. Aem. Macedo', rank='primus pilus leg. IX Hispanae; praef. castrorum leg. IIII Scythicae; trib. mil. leg. eiusdem; augur; flamen Neronis', include='yes', notes='= EDH HD026035 (Dyrrachium), Neronian.'),
 # ---------------- Britain ----------------
 'EDCS-07800503': dict(person='Q. Cornelius Q. f. Cla.', rank='eques leg. VIIII, centuria Cassi Martialis (aged 40, stip. 19)', include='yes', notes='= EDH HD021172 (RIB 254, Lincoln).'),
 'EDCS-07800504': dict(person='C. Saufeius C. f. Fab., Heraclea', rank='miles leg. VIIII (aged 40, stip. 22)', include='yes', notes='= EDH HD069558 (RIB 255 = ILS 2255, Lincoln); livius.org "tombstone of Gaius Saufeius".'),
 'EDCS-07800505': dict(person='L. Sempronius Flavinus, Hispanus, Gal., Clunia', rank='miles leg. VIIII, centuria Babudi Severi (aerum VII, aged 30)', include='yes', notes='= EDH HD069559 (RIB 256, Lincoln).'),
 'EDCS-07800506': dict(person='C. Valerius C. f. Maec.', rank='miles leg. IX, signifer, centuria Hospitis (aged 35, stip. 14)', include='yes', notes='= EDH HD020249 (RIB 257, Lincoln).'),
 'EDCS-07800509': dict(person='[...]rcu[...]s M. f. Cam., Pisaurum', rank='miles leg. VIIII', include='yes', notes='= EDH HD069562 (RIB 260, Lincoln).'),
 'EDCS-07800942': dict(person='L. Celerinius Vitalis', rank='cornicularius leg. VIIII Hispanae', include='yes', notes='= EDH HD069924 (RIB 659, York; altar to Silvanus).'),
 'EDCS-07800948': dict(person='Imp. Caesar Nerva Traianus Aug. (trib. pot. XII, cos. V)', rank='building inscription: porta per leg. VIIII Hisp. facta', include='yes', notes='= EDH HD069928 (RIB 665 = CIL VII 241, York fortress gate, AD 107/108). Latest securely dated attestation in Britain.'),
 'EDCS-07800964': dict(person='L. Duccius L. f. Vol. Rufinus, Vienna', rank='signifer leg. VIIII (aged 28)', include='yes', notes='= EDH HD069936 (RIB 673, York).'),
 'EDCS-07800971': dict(person='C. [...]us C. f. Cla. [...], Novaria', rank='[miles?] leg. IX Hispanae', include='yes', notes='= EDH HD069942 (RIB 680, York).'),
 'EDCS-11800710': dict(person='Tit[...] Pines', rank='centurio leg. VIIII', include='yes', notes='RIB 3047 = AE 1965, 213 (Godmanstone, Dorset; altar to IOM). Not in EDH.'),
 'EDCS-15100031': dict(person='anonymous', rank='imaginifer leg. IX (graffito)', include='yes', notes='= EDH HD027675 (AE 1949, 103, London). Same object as EDCS-51700627 (RIB II 2501.7).'),
 'EDCS-51700627': dict(person='anonymous', rank='imaginifer leg. IX (graffito)', include='yes', notes='RIB II 2501.7 (London); duplicate entry of EDCS-15100031 / AE 1949, 103.'),
 'EDCS-44500013': dict(person='[Na]evianus', rank='[miles?] leg. VIIII', include='yes', notes='= EDH HD073328 (RIB 3042, Hayling Island; votive fragment).'),
 'EDCS-03300636': dict(person='-', rank='stamp/graffito LEG VIIII', include='yes', notes='= EDH HD050845 (AE 1995, 1010, Corbridge).'),
 'EDCS-15000024': dict(person='-', rank='tile stamp LEG IX HISP', include='yes', notes='= EDH HD021832 (AE 1950, 124, Lincoln?; = RIB II 2462.9(i) per EDH comment).'),
 'EDCS-09400491': dict(person='-', rank='tile stamp LEG IX HISP', include='yes', notes='= EDH HD007055 (AE 1975, 558a, York).'),
 'EDCS-09400492': dict(person='-', rank='tile stamp LEG IX HISP', include='yes', notes='AE 1975, 558b (York); EDH HD007055 covers 558b-c.'),
 'EDCS-09400493': dict(person='-', rank='tile stamp LEG IX HISP', include='yes', notes='AE 1975, 558c (York).'),
 'EDCS-49601850': dict(person='-', rank='tile stamp "LEG IX VIC(trix)"', include='no', notes='RIB II 2462.17* (asterisk = falsum/misread); excluded.'),
 # ---------------- Germania inferior / Belgica ----------------
 'EDCS-09301104': dict(person='-', rank='tile stamp LEG VIIII HISP', include='yes', notes='= EDH HD020257 (AE 1977, 541, Nijmegen). EDCS holds a single entry for the Nijmegen stamp series.'),
 'EDCS-03000651': dict(person='-', rank='silvered bronze phalera pendant inscribed LEG HISP IX', include='yes', notes='= EDH HD050314 (AE 1996, 1107; ZPE 111, 281; Nijmegen/Ewijk). EDCS/EDH date 121-130.'),
 'EDCS-10700516': dict(person='L. Latinius L. f. Pub. Macer, Verona', rank='primus pilus leg. VIIII Hispanae; praefectus castrorum', include='yes', notes='= EDH HD014357 (AE 1968, 323, Aachen; altar to Apollo).'),
 'EDCS-10601003': dict(person='anonymous flamen Augusti, flamen Leni Martis', rank='praef. coh. II Hispanorum eq.; tribunus militum leg. VIIII Hispanae; praef. eq. alae Aug. Vocontiorum', include='yes', notes='= EDH HD011186 (CIL XIII 4030, Mersch).'),
 # ---------------- Rome / Italy: officers, 2nd c. ----------------
 'EDCS-01000406': dict(person='anonymous eques', rank='[trib. mil.?] leg. IX Hispanae; procurator prov. [...] et provinciae novae Arabiae', include='yes', notes='= EDH HD013966 (CIL VI 41280 = AE 1967, 20). EDH dates 106-161, commentary: "zwischen 106 (Einrichtung der Provinz Arabia) u. 161 (Zerstoerung der legio IX Hispana)".'),
 'EDCS-05801602': dict(person='L. Roscius M. f. Qui. Aelianus Maecius Celer (cos. suff. 100)', rank='tribunus militum leg. IX Hispanae, vexillariorum eiusdem in expeditione Germanica (AD 83); donatus dona militaria', include='yes', notes='= EDH HD030763 (CIL XIV 3612 = ILS 1025, Tibur).'),
 'EDCS-17800486': dict(person='L. Aemilius L. f. Cam. Karus (cos. suff. c. 144)', rank='tribunus militum leg. VIII Aug.; tribunus militum leg. VIIII Hispanae; later leg. leg. XXX U.V., governor of Arabia (142/3), Cappadocia', include='yes', notes='CIL VI 1333 = ILS 1077 (Rome). Tribunate of IX Hispana c. 120s; key to the "legion survived Hadrian" argument (livius.org, Wikipedia). Not in EDH.'),
 'EDCS-19700276': dict(person='Ti. Claudius Ti. f. Gal. Vitalis', rank='centurio: leg. V Mac., I Ital., I Minervia (bellum Dacicum), XX Vict., IX Hisp., VII Cl. P.F.; princeps posterior coh. II (died aged 41)', include='yes', notes='CIL VI 3584 = ILS 2656 (Rome). Transfer XX V.V. -> IX Hisp. -> VII Claudia after the Dacian wars. Not in EDH.'),
 'EDCS-20600417': dict(person='L. Burbuleius L. f. Qui. Optatus Ligarianus (cos. suff. c. 135)', rank='tribunus laticlavius leg. IX Hispanae', include='yes', notes='CIL X 6006 = ILS 1066 (Minturnae). Not in EDH.'),
 'EDCS-23000342': dict(person='Q. Camurius [.] f. Lem. Numisius Iunior (cos. 161)', rank='tribunus militum leg. VIIII Hispanae; later leg. Aug. leg. [...] and leg. VI Victricis', include='yes', notes='CIL XI 5670 (Attidium). Tribunate placed in the 130s by some (Birley), used for a post-Hadrianic survival of the legion; EDCS dates the stone 151-161. Not in EDH.'),
 'EDCS-16300271': dict(person='L. Decrius L. f. Serg. Longinus', rank='praef. fabrum; centurio leg. II Aug., VII Gem. (bis), XXII Deiot.; primus pilus leg. eiusdem; praefectus castrorum leg. VIIII Hispanae', include='yes', notes='= EDH HD027393 (AE 1913, 215, Agnano). Career pairs the two "lost" legions XXII Deiotariana and IX Hispana.'),
 'EDCS-37900019': dict(person='anonymous senator', rank='Xvir stlit. iud.; tribunus [mil.] leg. VIIII Hispanae; [...] legionis eiusdem', include='yes', notes='EE IX 612 (Lanuvium). Not in EDH.'),
 'EDCS-11500706': dict(person='Aelius Asclepiades, natione Cilix', rank='miles leg. IX (vixit 42, militavit 8)', include='flag', notes='CIL X 1769 (Naples). Legion IX without cognomen, Cilician recruit, Hadrianic/Antonine name: cited (Keppie 1989) as possible evidence for IX Hispana in the East; attribution uncertain. Not in EDH.'),
 'EDCS-19000504': dict(person='-', rank='"Nomina legionum": list of the 33 legions (Severan, after 197)', include='yes', notes='CIL VI 3492a = ILS 2288 (Rome, column); IX Hispana ABSENT from the list. Not in EDH.'),
 'EDCS-76900071': dict(person='-', rank='"Nomina legionum": list of the 33 legions (Severan, after 197)', include='yes', notes='CIL VI 3492b = ILS 2288 (Rome, second column, identical list); IX Hispana ABSENT. Not in EDH.'),
 # ---------------- Provinces: East / Africa / Danube / Spain ----------------
 'EDCS-16100418': dict(person='L. Servaeus Sabinus', rank='centurio leg. VIIII Hispanae, III Augustae, VI Victricis', include='yes', notes='= EDH HD025791 (AE 1930, 109, Savatra).'),
 'EDCS-16201163': dict(person='C. Caristanius C. f. Serg. Fronto (cos. suff. 90)', rank='legatus Imp. divi Vespasiani leg. IX Hispanae in Britannia (c. 76-79)', include='yes', notes='= EDH HD021539 (ILS 9485 = AE 1914, 262, Antioch in Pisidia).'),
 'EDCS-31800129': dict(person='C. Caristanius Fronto', rank='legatus [Imp. divi Vespasiani] leg. IX His[panae in Bri]tanni[a]', include='yes', notes='IK 67, 174 (Antioch in Pisidia), second copy of the Caristanius cursus. Not in EDH.'),
 'EDCS-16300627': dict(person='C. Velius Salvi f. Rufus', rank='primus pilus leg. XII Fulm.; praefectus vexillariorum legionum VIIII (I Adi., II Adi., II Aug., VIII Aug., VIIII Hisp., XIIII Gem., XX Vic., XXI Rapax)', include='yes', notes='= EDH HD031653 (ILS 9200 = IGLS VI 2796, Heliopolis). Vexillation of IX Hispana in a Domitianic war (83 or 89).'),
 'EDCS-21200156': dict(person='T. Aninius L. f. Pap. Sextius Florentinus', rank='legatus leg. VIIII Hispanae; proconsul Narbonensis; leg. Aug. pr. pr. prov. Arabiae (127)', include='yes', notes='CIL III 87 = IGLS XXI/4, 51 (Petra tomb). Legionary command c. 120-125; undated in EDCS. Not in EDH.'),
 'EDCS-13001586': dict(person='L. Stei[us?] [...] Hor.', rank='[tribunus militum l]eg. VIIII Hispan[ae]; ad census accipiendos provinciae [...]; [... di]vi Traiani; proconsul', include='yes', notes='CIL VIII 5355 = ILAlg I 282 (Calama). "divi Traiani" -> Hadrianic or later; undated in EDCS. Not in EDH.'),
 'EDCS-20800611': dict(person='L. Novius Crispinus Martialis Saturninus (cos. 150)', rank='tribunus militum leg. VIIII Hispanae (early in career)', include='yes', notes='= EDH HD031258 (CIL VIII 2747 = ILS 1070, Lambaesis).'),
 'EDCS-24800728': dict(person='L. Novius Crispinus Martialis Saturninus (cos. 150)', rank='tribunus militum leg. VIIII Hispanae', include='yes', notes='= EDH HD031261 (CIL VIII 18273, Lambaesis), second copy.'),
 'EDCS-29100179': dict(person='L. Valerius L. f. Proclus (died aged 75)', rank='centurio leg. V Mac. (donatus bello Dacico), I Ital., XI Cl., XX V.V., VIIII Hisp.; missus honesta missione', include='yes', notes='= EDH HD042822 (CIL III 12411 = ILS 2666b = ILBulg 432, Nedan/Nicopolis ad Istrum). Last post in IX Hispana after the Dacian wars.'),
 'EDCS-22400382': dict(person='[.] Quirina Qui[ntillus?], [P]isonis f.', rank='[miles?] leg. IX His(panae)', include='flag', notes='ERPLeon 401 = HEp 1999, 405 (Cremenes, Leon); heavily restored, reading uncertain. Not in EDH.'),
 'EDCS-44800120': dict(person='[...]lius Elaesi f. (aged 25)', rank='miles leg. nonae Hispanae (aerorum [...])', include='yes', notes='IRPPalencia 101 = CIRPBurgos 46 (Castrecias/Rebolledo de la Torre, Burgos); same stone as EDCS-74300002.'),
 'EDCS-74300002': dict(person='[...]lius Elaesus', rank='miles leg. nonae Hispanae', include='yes', notes='HAnt 1996, 91; duplicate entry of EDCS-44800120.'),
 'EDCS-34900247': dict(person='(garbled)', rank='(garbled: "leg viiii")', include='no', notes='AE 1984, 556 (Corporales, Leon): dedication pro salute M. Aureli Antonini et L. Veri (161-169) in a corrupt transcription; "leg viiii" is almost certainly a misreading (leg. VII G.?); excluded.'),
 'EDCS-68000006': dict(person='-', rank='object inscribed IX HISP XI', include='flag', notes='Unprovenanced (Hirsch auction 317, 591); EDCS "Provincia incerta".'),
 'EDCS-70500019': dict(person='-', rank='object inscribed IX / HISP / IX', include='flag', notes='Unprovenanced (TimeLine Auctions 2016); EDCS "Provincia incerta".'),
 'EDCS-78400190': dict(person='C. Fabius C. f. Pub. Verona', rank='miles leg. VIIII Hisp(anae)', include='flag', notes='CIL V *422 (Verona, "falsae vel alienae"): duplicate record of the Aquileia stone CIL V 911 = EDCS-01600189; counted once.'),
 'EDCS-84100016': dict(person='Vo[...] (immunis)', rank='immunis leg. IX (graffito on object)', include='flag', notes='AE 2020, 932 = AEA 2020/21, 31 (Lentia/Linz, Noricum). Recently published graffito naming an immunis of leg. IX without cognomen; undated in EDCS; attribution to IX Hispana plausible (no other imperial ninth legion) but unverified. Not in EDH.'),
 # ---------------- excluded EDCS hits ----------------
 'EDCS-12201569': dict(person='Iunia L. f. Hispaniensis', rank='-', include='no', notes='Personal cognomen Hispaniensis; not the legion.'),
 'EDCS-20800051': dict(person='C. Furius C. f. Aem. Gallus', rank='praefectus levis armaturae [...] Hispaniensis', include='no', notes='Auxiliary command, not leg. IX.'),
 'EDCS-03300728': dict(person='T. Varius Clemens', rank='praefectus auxiliis Hispaniensibus', include='no', notes='= EDH HD050953 (Celeia); auxilia, not the legion.'),
 'EDCS-17700479': dict(person='-', rank='-', include='no', notes='"diebus VIIII h(ic) s(itus)" - false hit.'),
}

# EDH-side curation for records whose EDCS twin is above: reuse via concordance
EDH2EDCS = {
 'HD003587':'EDCS-05400693','HD003697':'EDCS-01401119','HD004335':'EDCS-11700356','HD007055':'EDCS-09400491','HD009867':'EDCS-09400433',
 'HD011186':'EDCS-10601003','HD013966':'EDCS-01000406','HD014357':'EDCS-10700516','HD020249':'EDCS-07800506','HD020257':'EDCS-09301104',
 'HD021172':'EDCS-07800503','HD021539':'EDCS-16201163','HD021832':'EDCS-15000024','HD025791':'EDCS-16100418','HD026035':'EDCS-16201101',
 'HD026601':'EDCS-08200279','HD027393':'EDCS-16300271','HD027675':'EDCS-15100031','HD030763':'EDCS-05801602','HD031258':'EDCS-20800611',
 'HD031261':'EDCS-24800728','HD031653':'EDCS-16300627','HD042822':'EDCS-29100179','HD049599':'EDCS-08600717','HD050314':'EDCS-03000651',
 'HD050845':'EDCS-03300636','HD050953':'EDCS-03300728','HD056334':'EDCS-27000426','HD069558':'EDCS-07800504','HD069559':'EDCS-07800505',
 'HD069562':'EDCS-07800509','HD069924':'EDCS-07800942','HD069928':'EDCS-07800948','HD069936':'EDCS-07800964','HD069942':'EDCS-07800971',
 'HD073328':'EDCS-44500013',
}
CUR_EDH_ONLY = {
 'HD003700': dict(person='L. Viennius L. [f.] Ani. Verus, Forum Iulii', rank='miles leg. VIIII(?)', include='yes', notes='AE 1988, 584 (Aquileia); not retrieved from EDCS by the text searches.'),
}

def tile_stamp_default(edcs_id, text, cites):
    """Generic curation for the RIB II 2462 / CIL VII 1224 stamp series."""
    return dict(person='-', rank='tile stamp ' + re.sub(r'[()]', '', text).strip(), include='yes',
                notes='Stamped tile (' + cites.split(';')[0].strip() + '); undated in EDCS. Not in EDH (EDH holds only AE-published stamps).')

def clean(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()

rows = []

# ---------------------------------------------------------------- EDH rows
edh = json.load(open(os.path.join(RAW, 'edh_candidates_union.json')))
for hd in sorted(edh):
    j = json.load(open(os.path.join(RAW, 'edh_records', hd + '.json')))['items'][0]
    x = ET.parse(os.path.join(RAW, 'edh_records', hd + '.xml')).getroot()
    def pn(t):
        e = x.find(f'.//t:placeName[@type="{t}"]', NS)
        return clean(e.text) if e is not None and e.text else ''
    nb = na = ''; dtxt = ''
    for e in x.findall('.//t:origDate', NS):
        if e.get('notBefore-custom') or e.get('notAfter-custom'):
            nb = (e.get('notBefore-custom') or '').lstrip('0') or nb
            na = (e.get('notAfter-custom') or '').lstrip('0') or na
            dtxt = clean(e.text)
    # EDH JSON sometimes swaps not_before/not_after; XML is authoritative. Fallback to JSON if XML empty.
    if not nb and not na:
        vals = [v for v in (j.get('not_before'), j.get('not_after')) if v]
        if vals:
            vals = sorted(int(v) for v in vals); nb, na = str(vals[0]), str(vals[-1])
    comm = clean(j.get('commentary'))
    basis = 'EDH dating field' + (' (' + dtxt + ')' if dtxt else '')
    if re.search(r'Datierung|Zeit|Jh\.', comm):
        basis += '; EDH commentary: ' + comm[:300]
    key = EDH2EDCS.get(hd)
    cur = CUR.get(key) if key else CUR_EDH_ONLY.get(hd)
    if cur is None:
        cur = dict(person='?', rank='?', include='?', notes='')
    notes = cur['notes']
    if key:
        notes = f'Concordance EDCS {key}. ' + notes
    rows.append(dict(source_db='EDH', db_id=hd, url=f'https://edh.ub.uni-heidelberg.de/edh/inschrift/{hd}',
        publication_refs=clean(j.get('literature')), province=pn('province'), findspot_modern=pn('modern'), findspot_ancient=pn('ancient'),
        type=clean(j.get('type_of_inscription')) + ((' / ' + clean(j.get('type_of_monument'))) if j.get('type_of_monument') else ''),
        text=clean(j.get('transcription')), date_from=nb, date_to=na, date_basis_if_stated=basis,
        person=cur['person'], rank=cur['rank'], include=cur['include'], notes=notes))

# ---------------------------------------------------------------- EDCS rows
cands = json.load(open(os.path.join(RAW, 'edcs_candidates.json')))
for r in cands:
    eid = r['id']
    text = ' || '.join(clean(t) for t in r['texts'])
    d = r['dates'][0] if r['dates'] else [None, None]
    dfrom = '' if d is None or d[0] is None else str(d[0])
    dto = '' if d is None or d[1] is None else str(d[1])
    cur = CUR.get(eid)
    if cur is None:
        if re.search(r'RIB 02 04, 02462|CIL 07 01224', r['cites']):
            cur = tile_stamp_default(eid, r['texts'][0], r['cites'])
        else:
            cur = dict(person='?', rank='?', include='?', notes='UNCURATED')
    cats = '; '.join(sorted(set(c for cl in r['cats'] for c in cl))) if r['cats'] else ''
    rows.append(dict(source_db='EDCS', db_id=eid, url=f'https://edcs.hist.uzh.ch/monument/{eid}',
        publication_refs=r['cites'], province=r['province'], findspot_modern=r['place'], findspot_ancient='',
        type=cats + ((' / material: ' + r['material']) if r['material'] else ''),
        text=text, date_from=dfrom, date_to=dto,
        date_basis_if_stated=('EDCS dating field (no criteria stated)' if (dfrom or dto) else 'EDCS: undated'),
        person=cur['person'], rank=cur['rank'], include=cur['include'], notes=cur['notes']))

cols = ['source_db','db_id','url','publication_refs','province','findspot_modern','findspot_ancient','type','text','date_from','date_to','date_basis_if_stated','person','rank','include','notes']
out = os.path.join(BASE, 'database_catalogue.csv')
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)
print('rows', len(rows), '->', out)
unc = [r['db_id'] for r in rows if r['include'] == '?']
print('uncurated:', unc)
