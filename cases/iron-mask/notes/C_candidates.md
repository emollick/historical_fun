# C. Candidates for the masked prisoner: dossier

Residual probabilities are provisional.

## 0. Scope, fixed points, sources, conventions

### 0.1 Fixed points used

- (a) arrested in the Dunkirk/Calais area in late July 1669; delivered to Saint-Mars at Pignerol on or about 24 August 1669 by Captain de Vauroy; described by Louvois as "un valet".
- (b) allowed in 1675 to serve Nicolas Fouquet as a valet.
- (c) shut up with Fouquet's valet La Rivière after Fouquet's death (March 1680) as "the two prisoners of the lower tower".
- (d) taken by Saint-Mars to Exilles in 1681.
- (e) the survivor of the two, taken to the île Sainte-Marguerite in spring 1687 after the other died in January 1687.
- (f) taken by Saint-Mars to the Bastille in September 1698 as "un ancien prisonnier qu'il avait à Pignerol".
- (g) died 19 November 1703, buried 20 November as "Marchioly", "âgé de quarante-cinq ans ou environ".

Each candidate is tested against these. A candidate who is documented alive and free, or in another prison, at the date of any fixed point, fails that point. The age at (g) is a weak test, since the register age is a figure supplied by the Bastille staff (see section 17); it is reported for every candidate but never treated as decisive on its own.

### 0.2 Sources used and how they are cited

Local OCR files in `sources/` (short forms used below):

- Delort 1825 = J. Delort, *Histoire de l'homme au masque de fer* (Paris, 1825) — `delort1825_histoire_homme_masque_de_fer.txt`. Page numbers as printed "(43)" etc. in the OCR.
- Ellis 1826 = G. A. Ellis, *The True History of the State Prisoner commonly called the Iron Mask* (London, 1826) — `ellis1826_true_history_state_prisoner.txt` (re-downloaded; the file of that name previously in the folder was an Internet Archive "Page Not Found" page).
- Iung 1873 = Th. Iung, *La Vérité sur le Masque de fer* (Paris, 1873) — `iung1873_verite_masque_de_fer.txt`.
- Topin 1883 = M. Topin, *L'Homme au masque de fer*, 6th ed. (Paris, 1883) — `topin1883_homme_au_masque_de_fer.txt`; Topin 1870 = English translation (London, 1870).
- Loiseleur 1882 = J. Loiseleur, *Trois énigmes historiques* (Paris, 1882) — `loiseleur1882_trois_enigmes_historiques.txt` (downloaded, archive.org `troisnigmeshist00loisgoog`).
- Lair 1890 = J. Lair, *Nicolas Foucquet*, t. II (Paris, 1890) — `lair1890_nicolas_foucquet_vol2.txt`.
- Funck-Brentano 1901 = F. Funck-Brentano, *Légendes et archives de la Bastille*, ed. of 1901 — `funckbrentano1901_legendes_et_archives_bastille.txt`.
- Lang 1903 = A. Lang, *The Valet's Tragedy and Other Studies* (London, 1903), Project Gutenberg #2073 — `lang1903_valets_tragedy.txt` (no page numbers; cited by chapter and section).
- Barnes 1908 = A. S. Barnes, *The Man of the Mask* (London, 1908) — `barnes1908_man_of_the_mask.txt` (downloaded, `manofmaskstudyin00barnuoft`).
- Laloy 1913 = E. Laloy, *Le Masque de fer: Jacques Stuart de la Cloche, l'abbé Prignani, Roux de Marsilly* (Paris, 1913) — `laloy1913_masque_de_fer_lacloche_prignani_marsilly.txt`.
- Ravaisson X = F. Ravaisson, *Archives de la Bastille*, t. X (Paris, Durand et Pedone-Lauriel, 1879) — `ravaisson_archives_bastille_vol10_1693-1702.txt`.
- Dangeau III = *Journal du marquis de Dangeau*, ed. Soulié, Dussieux et al., t. III (Paris, Firmin Didot, 1854) — `dangeau_journal_vol03.txt` (downloaded, `journaldumarquis03dang`).
- Mongrédien 1953 = G. Mongrédien, "Le problème du Masque de fer", *XVIIe siècle*, no. 17-18 (15 April 1953), pp. 55-58 — `mongredien1953_xviie_siecle_17-18.txt` (downloaded, archive.org `xviie-siecle_1953_17-18`).
- La Grange 1876 = *Registre de La Grange (1658-1685)* (Paris, 1876) — `lagrange1876_registre_1658-1685.txt`; Beffara 1821 = L.-F. Beffara, *Dissertation sur J.-B. Poquelin-Molière* (Paris, 1821) — `beffara1821_dissertation_moliere.txt`.
- Saint-Mihiel 1790, Taulès 1825, the 1789 pamphlet, Parsons 1893 (*Some Lies and Errors of History*, downloaded), Hopkins 1901: consulted for attributions only.

Online sources (URL given at the point of use): Batiffol's review of Bazeries-Burgaud in *Bibliothèque de l'École des chartes* 55 (1894) on Persée; Noone's *The Man Behind the Iron Mask* (chapters 11-13, full text on erenow.org, page numbers not available); Madry 2016 (earlymodernfrance.org); UCSB press release on Sonnino 2016; Publishers Weekly on Wilkinson 2021; OpenLibrary "search inside" snippets from Petitfils 2003/2004, Noone 1994, Thompson 1987, Pagnol 1973, Vergé-Franceschi 2009, Macdonald 2005; French and English Wikipedia raw text used only as pointers to proposers, dates and bibliographic references.

### 0.3 Access failures (reported, not routed around)

- Gallica: every request (SRU and `.texteBrut`) returns an "altcha" JavaScript security-check page ("Gallica | Vérification de sécurité"); no Gallica text could be retrieved. This blocked Bazeries and Burgaud 1893, Mongrédien 1952 (`bpt6k3357084j`) and Loquin 1898.
- Bazeries and Burgaud, *Le Masque de fer, révélation de la correspondance chiffrée de Louis XIV* (Paris, Firmin-Didot, 1893, 302 pp.) is not on archive.org under any search tried; Google Books API returned an empty result; HathiTrust returns 403 through the proxy. The deciphered text is therefore taken from Batiffol's contemporary review and from Laloy 1913, pp. 155-156, both of which quote it.
- Internet Archive lending items (Petitfils, Noone, Thompson, Furneaux, Macdonald, Pagnol, Bartoli, Vergé-Franceschi, Sonnino): OCR download returns 403 "Item not available"; the IA full-text "inside.php" endpoint returns 403. Only OpenLibrary snippet search worked (short highlighted fragments without page numbers).
- Persée: the review page shows only p. 359 of Batiffol's review; the PDF endpoint returns 403; the second page (p. 360, containing his archival reference "Cabinet des titres, pièces originales, t. 1612, dossier Labbé de Bulonde") could not be read beyond the first words.
- History Today (Macdonald 2005 article) returns 403.
- Duvivier 1932 could not be read; his positions are taken from Mongrédien 1953 (which summarises Duvivier) and from Mongrédien 1952. Mongrédien 1952 (*Le Masque de fer*, Hachette) was not readable in full: Gallica ContentSearch snippets of it with printed page numbers (`sources/mongredien_1952_snippets.md`, Gallica ark bpt6k3357084j) and Gallica snippets of Petitfils 2004 (`sources/petitfils_2004_snippets.md`) are in the folder; page references below marked "Mongrédien 1952, p. …" come from those snippets, which the service cuts mid-sentence.
- Pinard, *Chronologie historique-militaire*: only tome I is on archive.org; the volume with Bulonde's notice was not found.

### 0.4 Conventions

"Document" = a contemporary record quoted or precisely cited by a named edition. "Inference" = a conclusion drawn from documents. Quotations keep the spelling of the edition cited; OCR line-break hyphenation removed. Page numbers of the local OCR files were read from the running heads in the OCR and may be off by one where the running head was garbled.

---

## 1. Eustache Dauger / Danger, the valet (consensus identification) — brief

Who this man was is covered in dossier E. Summary of the position only.

Documents (the fixed points, all in the Louvois–Saint-Mars–Barbezieux correspondence, Archives de la Guerre, printed in Delort 1825, Iung 1873, Lair 1890, Laloy 1913): the 19 July 1669 order to prepare a cell for "le nommé Eustache Dauger" with the remark that he is only a valet; arrival 24 August 1669; permission of 30 January 1675 to serve Fouquet; order of 8 April 1680 shutting him and La Rivière in the lower tower; the Exilles transfer of 1681; the death of one of the two in January 1687 (Iung 1873, pp. 340-341 and 404-405); the letter of Barbezieux of 13 August 1691, "Lorsque vous aurez quelque chose à me mander du prisonnier qui est sous votre garde depuis vingt ans, je vous prie d'user des mêmes précautions que vous faisiez quand vous les donniez à M. de Louvois" (Iung 1873, early chapter, OCR line 786; Laloy 1913, pp. 152-153; Lang 1903, ch. I §2); du Junca's entries of 18 September 1698 and 19 November 1703 (Funck-Brentano 1901, pp. 86-88).

Inference accepted by Lair 1890, Lang 1903, Laloy 1913, Mongrédien 1952, Petitfils 1970/2003, Noone 1988, Sonnino 2016, Wilkinson 2021: the 1703 prisoner is the man of 1669, whatever his real name. The chain (a)-(g) is continuous only if the survivor of January 1687 was Dauger and not La Rivière (see section 4).

Hypotheses on who the valet was (all compatible with the fixed points, since they concern the same man):

- Lang 1903, ch. I "The Valet's Tragedy": Dauger was "Martin", the valet left in London by the Huguenot conspirator Roux de Marsilly (executed Paris, June 1669); "Martin must be Dauger" (Lang 1903, ch. I §2). Lang is the origin of the "Martin" identification, not of the Cavoye one.
- Duvivier 1932: Eustache Dauger de Cavoye (refuted, section 2).
- Laloy 1931: an "Eustache Daugé" of a family of royal household officers (pointer: en.wikipedia list of candidates, row 1931; not checked).
- Petitfils 2003: a valet used by Madame (Henrietta of England) to carry letters in the secret negotiation of the Treaty of Dover, who had seen too much (summarised in Noone, ch. 12, revised ed.).
- Sonnino 1991/2016: a valet of the treasurer of the late Cardinal Mazarin — Antoine-Hercule Picon, Colbert's associate in the management of Mazarin's fortune, in whose service Sonnino places Dauger from about 1643 (Julius R. Ruff's review, *H-France Review* 16, November 2016, no. 258, pp. 1-2, https://h-france.net/vol16reviews/vol16no258Ruff.pdf, local copy `sources/ruff2016_hfrance_review_sonnino.txt`) — who knew that Mazarin had misappropriated money belonging to Charles I and Henrietta Maria and "blabbed at the wrong time" in 1669, when Louis XIV was courting Charles II (UCSB press release, 29 April 2016, https://www.history.ucsb.edu/2016/04/29/professor-sonnino-solves-17th-century-case-man-iron-mask/; the 1991 article is "On the Trail of the Iron Mask: The Candidacy of Claude Imbert", *Proceedings of the Western Society for French History* 19, pages given variously as 99-108 and 261-272 in secondary references; not read).
- Macdonald 2005: "Martin, Etienne alias Eustache Danger/Dauger: fixer, poisoner, valet" (index entry, OpenLibrary snippet of the 2005 edition); Macdonald's headline candidate is however d'Artagnan (section 16).
- Vergé-Franceschi 2009: a valet of the duc de Beaufort, arrested after Beaufort's disappearance at Candia (as summarised in Madry 2016; the book itself not read).
- Madry 2016: Louvois's "un valet" is a pun on the playing-card Jack (Hogier le Danois) and on Louvois's rival Louis d'Auger de Cavoye; Madry 2024 (*Second Son*, Locate Press): the prisoner was a secret younger brother of Philippe d'Orléans (pointer: en.wikipedia list, row 2024; not read).
- Noone 1988/1994/2003 (ch. 13, "The Valet in the Face-Saving Mask"): the prisoner was the valet Eustache; the mask and the mystery were Saint-Mars's own invention to save face after he lost Fouquet (d. 1680) and Lauzun (freed 1681), and "as governor of the Bastille he kept up that pretence and saw the image he had invented for the prisoner outlive the prisoner's death" (Noone, ch. 13, https://erenow.org/biographies/the-man-behind-the-iron-mask/13.php). Noone treats the man's identity beyond "a valet" as unrecoverable on present evidence and, in the revised edition, endorses Petitfils's Dover hypothesis as the most plausible. I did not find the phrase "stand-in" in chapters 11-13; the sense of his argument is that an insignificant valet was made to stand in, in Saint-Mars's staging, for a prisoner of consequence.
- Wilkinson 2021 (*The Man in the Iron Mask: The True Story of Europe's Most Famous Prisoner*, Pegasus, July 2021, 352 pp.): concludes he was "only a valet"; Publishers Weekly (review dated 19 April 2021, https://www.publishersweekly.com/9781643137421) summarises her conclusion as "a valet of Louvois's who had somehow betrayed him".

Age: Lang 1903, ch. I §4: "Dauger cannot have been under fifty-three" in 1703.

Assessment: passes (a)-(g) by construction; the only weak link is (e). Residual probability that the 1703 prisoner is the 1669 valet: about 85%.

---

## 2. Eustache Dauger de Cavoye

Proponents: Maurice Duvivier, *Le Masque de fer* (Paris, Armand Colin, 1932) — the first to identify the prisoner with this man, whom he also connected with the Affair of the Poisons (Mongrédien 1953, p. 55, summarising Duvivier; Mongrédien 1952, p. 217, adds that Duvivier "tient pour assuré que Foucquet, à la veille de sa libération, fut empoisonné à Pignerol, que Dauger fut l'artisan de ce crime" — Gallica snippet); Rupert Furneaux, *The Man Behind the Mask* (London, Cassell, 1954), who made him a bastard of Louis XIII and Marie de Sérignan; Marie-Madeleine Mast (1974) and Harry Thompson, *The Man in the Iron Mask: A Historical Detective Investigation* (London, Weidenfeld and Nicolson, 1987), who made him a son of Anne of Austria and François de Cavoye (en.wikipedia list, rows 1954 and 1974; Thompson snippet on OpenLibrary). Andrew Lang did not propose Cavoye; his 1903 candidate for the valet's identity was Roux de Marsilly's servant Martin (section 1).

Documented life (Mongrédien 1953, pp. 55-58; Noone 1988, ch. 11, quoting the baptismal certificate):

- Born 30 August 1637, baptised 18 February 1639 at Saint-Eustache, son of François Dauger (d'Oger), sieur de Cavoye, captain of Richelieu's guards, and Marie de Sérignan (Noone, ch. 11, opening sentence, quoting the certificate).
- Lieutenant in the Guards; one of the participants in the "débauche de Roissy" (Easter 1659) with Bussy-Rabutin and the abbé Le Camus; duels; killed a page; disinherited by his mother's will of 6 May 1664 in favour of his younger brother Louis; deed of 15 August 1665 ceding the family fiefs to Louis for a life annuity of 1,400 livres; settlement of accounts between the brothers 8 January 1668 (Mongrédien 1953, pp. 55-56 and n. 4, citing Duvivier pp. 157-162 and 327-330).
- Louis de Cavoye was arrested 5 July 1668 (Huguet, *Le marquis de Cavoye*, 1920, pp. 224-225, as cited by Mongrédien); "Eustache dut être mis à Saint-Lazare peu de jours après" (Mongrédien 1953, p. 56 n. 4).
- Letter of 20 June 1678 to his sister the marquise de Fabrègues (Louise-Henriette de Cavoye, widow since December 1674 of François-Antoine de Sarret, marquis de Fabrègues et de Coussergues; d. 1696), from the Sarret de Coussergues family archives, first printed in Mongrédien 1953, pp. 56-57. Decisive sentence: « Si vous scaviez ce que ie souffre, ie ne doute nullement que vous ne fissiez vos derniés efforts pour me tirer de la cruelle persécution et captivittée où ie suis détenu depuis plus de dix ans par la tirannie de M. de Cavoy mon frère sous de feaux prétextes ... » Signed « d'Eustache de Cavoy, ce vingtieme de juing mil six cens soissante et d(ix) huit », addressed « À Madame la marquise de Fabrègues à Paris ». Translation: "If you knew what I suffer, I have no doubt you would make your utmost efforts to draw me out of the cruel persecution and captivity in which I have been held for more than ten years by the tyranny of M. de Cavoye my brother, on false pretexts."
- Letter of Louis XIV to the superior of Saint-Lazare, 17 August 1678, found by Stanislas Brugnon in the register of the King's orders at the Archives nationales (Noone, ch. 11; en.wikipedia "Man in the Iron Mask", note "stlazare", citing Noone). Not seen by me.
- Undated petition to the King, from the same archives, printed in Mongrédien 1953, pp. 57-58. Decisive sentence: « Cavoy qui est destenu dans les prisons de St Lazare par une lettre de cachet de Vostre Majesté depuis unze ans et demy la supplie très humblement de luy faire la grace d'escoutter ses justes plaintes contre le sieur de Cavoy, son frère ... » Translation: "Cavoye, who has been held in the prisons of Saint-Lazare by a lettre de cachet of Your Majesty for eleven and a half years, most humbly begs her to hear his just complaints against the sieur de Cavoye, his brother." Eleven and a half years from mid-1668 places the petition around the end of 1679 or the beginning of 1680; Mongrédien: "dix-huit mois plus tard, le malheureux Eustache était toujours à Saint-Lazare" (p. 57).
- Funeral ode on Cavoye by the comte de Brienne, a fellow inmate of Saint-Lazare, in a verse notebook completed by Brienne in February 1689; published by Antoine Adam in the *Revue d'Histoire de la Philosophie* (1938) (Noone, ch. 11). Thompson quotes its opening as "Here in this coffin at Saint-Lazare lies Cavoye" (OpenLibrary snippet of Thompson 1987). Not seen by me.
- Death: "sometime between 1680 and 1689" at Saint-Lazare (Noone, ch. 11). Mongrédien 1953, p. 58: « J'ignore si Eustache Dauger de Cavoye sortit de la prison de Saint-Lazare où, entré en 1668, il était encore en 1680. » No burial record has been produced by anyone I read.

Who first published the refutation: Georges Mongrédien, "Le problème du Masque de fer", *XVIIe siècle* (Bulletin de la Société d'étude du XVIIe siècle), no. 17-18, 15 April 1953, pp. 55-58, printing the two letters obtained from the baronne de Sarret de Coussergues and her daughters. Mongrédien had already rejected Duvivier on internal grounds in *Le Masque de fer* (Paris, Hachette, 1952), pp. 211-219 (his own reference, 1953, p. 56 n. 1, where he gives the date as 1951). The Brienne ode (Adam 1938) predates this but was not applied to the question until later (Noone).

Fixed points: fails (a) — held at Saint-Lazare, Paris, from 1668 to at least 1680, while the prisoner was at Pignerol from August 1669; fails (b), (c) for the same reason; fails (g) on age (66 in 1703, not "45 ou environ"). Louvois's "valet" also tells against a lieutenant of the Guards.

Best counter-argument by proponents (as reported by Noone, ch. 11): "die-hard supporters of the Cavoye theory have done their utmost to invalidate them, claiming that Brienne's poem must have been a forgery and that Cavoye's letters must have been written not from Saint-Lazare but from Pignerol." The petition itself names "les prisons de St Lazare"; a prisoner at Pignerol, forbidden to write, could not have addressed a petition to the King naming a Paris prison. Thompson's variant (the Mask as a royal bastard hidden under the Cavoye name) inherits the same documentary problem.

Assessment: refuted by documents. Residual probability: under 0.5%.

---

## 3. Count Ercole Antonio Mattioli

Proponents: Baron de Heiss (1770); Pierre Roux-Fazillac, *Recherches historiques et critiques sur l'homme au masque de fer* (1801); Delort 1825; Ellis 1826 (an English digest of Delort's documents); Topin 1869 (*Le Correspondant*) and 1870/1883; Funck-Brentano, *Revue historique* 56 (1894) and *Légendes et archives de la Bastille* (1898; ed. 1901 used). Loiseleur was an opponent, not a proponent. In *Trois énigmes historiques* (1882), pp. 319-322, he recapitulates his polemic with Topin (*Revue contemporaine*, 16 December 1869 and 13 February 1870), argues that "le vrai Masque de fer n'avait pas de valet" and that Mattioli died between 20 March and 10 May 1694, and concludes "qu'il y a eu plusieurs masques de fer, et que le dernier en date, celui qui mourut en 1703, hérita ... de toutes les particularités propres à ses prédécesseurs" (p. 318). Iung 1873 was also anti-Mattioli.

Documented life:

- Born 1 December 1640, son of Valerio Mattioli and Girolama Maggi, of Bologna; married 13 January 1661 (Ellis 1826, p. 3, from Bolognese sources).
- Secretary of state of the Duke of Mantua; negotiated the secret cession of Casale to Louis XIV and betrayed it; lured to a meeting near Turin and arrested 2 May 1679 by Catinat (Delort 1825, pp. 43-44, citing Catinat's letter to Louvois of 3 May 1679 written under the alias "Richemont"); imprisoned at Pignerol under the false name "Lestang" (Delort, p. 43).
- His valet was sent to Pignerol with his clothes and papers by the abbé d'Estrades (Delort, p. 44, citing Catinat 6 May 1679; Catinat's letter printed pp. 215-216: « M. l'abbé d'Estrades ... a trouvé moyen d'envoyer à Pignerol le valet du sieur de Lestang avec ses hardes et tous ses papiers »).
- 1680: put in the lower tower with the mad Jacobin monk, allowed confession once a year (Delort, p. 47).
- 1681: left at Pignerol when Saint-Mars took "the two prisoners of the lower tower" to Exilles; Louvois's letters of 1681 distinguish the two Exilles prisoners from Mattioli (Lang 1903, ch. I §2: "In 1681 Louvois had thought Dauger and La Rivière more important than Mattioli").
- December 1693: he and his valet caught trying to smuggle out letters written on the linings of their pockets (Barbezieux to Saint-Mars 27 December 1693, per Lang ch. I §2 and Laloy p. 160).
- March 1694: Barbezieux orders Laprade (20 March 1694) to take his three Pignerol prisoners one by one to Sainte-Marguerite; Barbezieux to Saint-Mars 26 February 1694: they are "of more consequence, one of them at least, than the prisoners on the island" (Lang, ch. I §2).
- Death: Barbezieux to Saint-Mars, 10 May 1694 (Archives de la Guerre, vol. 1391, p. 188, per Iung 1873, p. 91; also Laloy 1913, p. 160): « J'ai reçu la lettre que vous avez pris la peine de m'écrire le 29 du mois passé; vous pouvez, suivant que vous le proposez, faire mettre dans la prison voûtée le valet du prisonnier qui est mort, observant de le faire garder aussi bien que les autres, sans communication de vive voix, ni par écrit, avec qui que ce soit. » Translation: "you may, as you propose, have the valet of the prisoner who has died put in the vaulted prison, taking care to have him guarded as well as the others, without communication by word or in writing with anyone." Saint-Mars's letter of 29 April 1694 is not printed in any source I saw. Laloy, p. 160: "seul Matthioly avait un valet"; "C'est là la dernière mention de Matthioly et de son valet dans les documents connus." Petitfils dates the death 28 April 1694 and the valet ("Rousseau") to December 1699 (en.wikipedia "Man in the Iron Mask", citing Petitfils 2004, p. 261 — pointer only).

The two sides on the 1694 death:

- For Mattioli's death in April 1694 (Iung, Loiseleur, Lair, Lang, Laloy, Mongrédien, Petitfils, Noone): only Mattioli among the prisoners transferred in 1694 had a valet; Saint-Mars's letter of 6 January 1696 shows that no prisoner on the island then had a valet (each collected his own dishes); the name Mattioli, "freely used before", never recurs after December 1693 (Lang, ch. I §2; Laloy pp. 160-163; Loiseleur pp. 320-321 n.).
- Against (Funck-Brentano 1901, pp. 110-120; quoted by Laloy pp. 160-161): it is "pas certain que Matthioly ait eu un valet aux îles Sainte-Marguerite comme il en avait un à Pignerol"; after the December 1693 complaints master and valet may have been separated; other prisoners had valets (Funck-Brentano cited Fouquet and Lauzun — but they were at Pignerol, not the islands, as Lang points out); the Protestant preacher Malzac might be the dead man (Lang: Malzac was dead by March 1693, on Iung's own showing, pp. 269-270). Funck-Brentano's positive case: "mon ancien prisonnier" in Saint-Mars's letters of 1696-98 means "my erstwhile prisoner, restored to me" (Mattioli); du Junca's "un ancien prisonnier qu'il avait à Pignerol"; Barbezieux 17 November 1697, "sans vous expliquer à qui que ce soit de ce qu'a fait votre ancien prisonnier"; and above all the burial name: « C'est le nom même de l'ancien secrétaire du duc de Mantoue qui y est tracé : "Marchioly". Il faut considérer : que "Marchioly" doit être prononcé à l'italienne "Markioly" ; que Saint-Mars ... écrit presque toujours dans sa correspondance ... non "Mattioli", mais "Martioly" » (Funck-Brentano 1901, pp. 119-120). He calls the demonstration "d'une rigueur mathématique" (p. 119).

Fixed points: fails (a) (arrested 2 May 1679 near Turin, not July 1669 near Dunkirk; free and in Mantuan service in 1669), (b), (c) (he was with the Jacobin, not with La Rivière), (d) (stayed at Pignerol 1681-1694), (e) (not at Sainte-Marguerite in 1687); passes (f) only on the loose reading of "ancien prisonnier qu'il avait à Pignerol"; (g): age 62, not 45, but the name "Marchioly" is his strongest point (section 17). If the 1694 reading is right he also fails (f) and (g) outright.

Best counter-argument: the name on the register, and the objection that a mere valet would not have been guarded for 34 years. The reply of the anti-Mattioli side is that the chain (a)-(e) is documented for the 1669 prisoner and that Saint-Mars never took Mattioli anywhere in 1681 or 1687.

Assessment: the only candidate other than the valet who ever came under Saint-Mars's hand, and the only one whose name resembles the burial name. Residual probability: about 3-4%, resting entirely on the possibility that the "prisoner who died" in April 1694 was not Mattioli and that "ancien prisonnier" in 1697-98 means him.

---

## 4. La Rivière, Fouquet's valet

Proponent: no author I consulted presents La Rivière as the 1703 prisoner in so many words; the candidacy is implicit in every account, since the Exilles pair (Dauger, La Rivière) lost one member in January 1687 and the documents do not name the dead man.

Documented life: valet of Fouquet at Pignerol (with another valet, Champagne, who died in 1674); Louvois's permission of 30 January 1675 for Dauger to serve Fouquet "when La Rivière is unavailable"; Louvois to Fouquet, 23 November 1678, asking whether Dauger had spoken in front of La Rivière about what he had been employed to do before Pignerol; after Fouquet's death (23 March 1680) Louvois on 8 April 1680 ordered the two shut up together (fixed point c; pointers en.wikipedia "Man in the Iron Mask", citing Mongrédien 1961, pp. 188-193). At Exilles: June 1685, La Rivière asked leave to make his will (pointer: Mongrédien 1961, p. 112, via en.wikipedia). Louvois to Saint-Mars, 9 October 1686 (Iung 1873, p. 340; printed again at p. 404 with the date "9 janvier 1686", evidently a misprint): « vous auriez dû me nommer quel est celui de vos prisonniers qui est devenu hydropique »; Louvois, 3 November 1686 (Iung, pp. 340-341, 404): « Il est juste de faire confesser celui de vos deux prisonniers qui devient hydropique, lorsque vous verrez apparence d'une prochaine mort. Jusque-là, il ne faut pas que lui ou son camarade aient aucune communication. » Saint-Mars reported the death on 5 January 1687; Louvois acknowledged it on 13 January: « J'ai reçu votre lettre du 5 de ce mois, par laquelle j'apprends la mort d'un de vos prisonniers » (Iung, p. 404). Iung himself (pp. 340-341) wrongly took the dead man for the Jacobin monk; the Jacobin was left at Pignerol in 1681 and died there in January 1694 (Noone, ch. 13 n. 4; Petitfils 2004, p. 74 via en.wikipedia).

Which of the two died? Documents bearing on it: Louvois's letters of 1686 do not name the sick man; Barbezieux's letter of 13 August 1691 calls the surviving prisoner "le prisonnier qui est sous votre garde depuis vingt ans" (Iung, OCR line 786; Laloy pp. 152-153; Lang ch. I §2). Inference: the 1669 prisoner had been under Saint-Mars for 22 years in 1691; La Rivière had been a state prisoner only since April 1680 (11 years), though he had lived inside Saint-Mars's prison as Fouquet's servant since 1665 (26 years). "Depuis vingt ans" fits Dauger better but does not exclude La Rivière absolutely, and Laloy notes (pp. 152-153) that Barbezieux probably copied the phrase from a letter of Saint-Mars. The modern consensus (Mongrédien 1961, pp. 113-115; Noone, ch. 13; Petitfils) that the dropsical prisoner was La Rivière rests on the 1685 will request and on the sequence of the letters, not on any letter naming him. Mongrédien 1952, p. 200, states the conclusion of his study as "l'identification des deux prisonniers emmenés à Exiles par Saint-Mars, Dauger et La Rivière, et des deux décédés de 1687 et de 1694, La Rivière et le [snippet cut; the 1694 dead man is the Jacobin monk in his system]" ("the identification of the two prisoners taken to Exilles by Saint-Mars, Dauger and La Rivière, and of the two who died in 1687 and 1694, La Rivière and the …"; Gallica ContentSearch snippet, `sources/mongredien_1952_snippets.md`). This is inference from the 1691 "vingt ans" letter, not a document naming the dead man.

Fixed points: passes (b) trivially (he was Fouquet's valet), (c), (d); fails (a) (he was at Pignerol with Fouquet from 1665, not arrested at Dunkirk in 1669; Louvois's 1669 letters concern another man); (e) only if he survived, which the 1691 "vingt ans" letter makes unlikely; (g) age unknown.

Assessment: the one alternative that would leave every later document intact while changing the man. Residual probability: about 5%, to be revised after checking whether Mongrédien 1961 or Petitfils cite a document naming the sick prisoner in 1686-87.

---

## 5. Lieutenant-général Vivien Labbé (L'Abbé) de Bulonde

Proponents: Émile Burgaud and commandant Étienne Bazeries, *Le Masque de fer, révélation de la correspondance chiffrée de Louis XIV. Étude appuyée de documents inédits des Archives du dépôt de la guerre* (Paris, Firmin-Didot, 1893, in-18, 302 pp.; bibliographic data from Batiffol's review).

Documented life: born c. 1637 at Fontaine-le-Dun (Seine-Maritime); brigadier 12 March 1675; lieutenant-général 24 August 1688; died 1709 (fr.wikipedia "Vivien l'Abbé de Bulonde", citing Mongrédien 1952, pp. 202-204, 253, and *Biographie des hommes illustres de la noblesse française*, 1864, pp. 29 ff.; neither checked by me; Pinard's *Chronologie* volume with his notice was not found). Under Catinat he commanded the siege of Coni (Cuneo) in June 1691 and lifted it on 29 June 1691 on news that Prince Eugene was coming with 4,000 horse (Dangeau III, p. 357, entry of Sunday 8 July 1691). Dangeau III, p. 357, Tuesday 10 July 1691: « Le roi a envoyé ordre à M. de Catinat de faire arrêter M. de Bulonde, et de l'envoyer dans la citadelle de Pignerol. » Dangeau III, p. 441, Tuesday 11 December 1691: « Le roi a envoyé ordre qu'on remît M. de Bulonde en liberté; il avoit toujours été en prison depuis la levée du siège de Coni. » Translation: "The King has sent an order that M. de Bulonde be set at liberty; he had been in prison ever since the raising of the siege of Coni."

The deciphered letter (Louvois to Catinat, 8 July 1691, in the Great Cipher of the Rossignols, broken by Bazeries), as quoted by Batiffol from the book (*Bibliothèque de l'École des chartes* 55 (1894), p. 359, https://www.persee.fr/doc/bec_0373-6237_1894_num_55_1_447793_t1_0359_0000_2) and by Laloy 1913, p. 155: « Sa Majesté désire que vous fassiez arrester monsieur de Bulonde et le fassiez conduire à la citadelle de Pignerol, où Sa Majesté veut qu'il soit gardé enfermé pendant la nuit dans une chambre de laditte citadelle, et, le jour, ayant la liberté de se promener sur les remparts avec [un] 330. » Batiffol: « et ici le chiffre 330, qui ne se retrouve nulle part ailleurs, et dont on ne peut imaginer le sens que par hypothèse. M. Burgaud a voulu lire "avec un masque"; un autre lirait avec autant d'autorité toute autre chose et voilà la base sur laquelle MM. Burgaud et Bazeries ont fait reposer leur thèse ... Ils n'ont pas d'autre preuve. » Laloy, p. 155: « D'après MM. Burgaud et Bazeries, il n'y a pas pour le groupe 330 d'autre traduction possible que masque. Il est plus rationnel de dire que bien d'autres conviendraient ... la clef étant perdue et ce groupe n'étant employé qu'une fois dans la correspondance. » Modern accounts add that Bazeries read the following group 309 as a full stop, giving "avec un masque." (fr.wikipedia; not verifiable without the book).

Refutation: Batiffol 1894, p. 359: « Il faut, pour que Bulonde soit le masque de fer, qu'il meure le 19 novembre 1703. C'est ce qu'affirment les auteurs. Ils n'ont pas consulté le dossier Labbé de Bulonde du Cabinet des titres de la Bibliothèque nationale. Ils y auraient vu au tome 1612 des pièces originales, dos[sier ...] » (p. 360 not retrievable). Geoffroy de Grandmaison, *L'Univers*, 9 January 1895: two receipts signed by Bulonde, one in 1699, "date où l'homme au masque était à la Bastille dans un isolement rigoureux; l'autre, en 1705, alors que le prisonnier masqué était mort depuis deux ans" (Funck-Brentano 1901, p. 111; Laloy p. 156; Barnes 1908, p. 37 and n. 1 — Barnes's "at liberty in Paris as early as 1675" is a misprint for the 1690s). Burgaud himself cited Pinard's statement that Bulonde was free in 1692 and alive in 1708 but declined to believe it (Laloy, p. 156).

Fixed points: fails (a)-(e) (a serving general, arrested only in July 1691); fails (f) (in 1691 Saint-Mars was at Sainte-Marguerite and Bulonde at Pignerol under Villebois; released 11 December 1691); fails (g) (alive 1699, 1705; d. 1709; age 66 in 1703). Passes none.

Best counter-argument of the proponents: that Pinard was wrong and that the release order was a fiction. The 1699 and 1705 receipts answer it.

Assessment: residual probability under 0.5% (the only surviving interest of the book is the cipher work).

---

## 6. Nicolas Fouquet himself

Proponents: the anonymous pamphlet *L'Homme au masque de fer dévoilé* (1789), which prints a supposed Bastille card "Foucquet arrivant des Isles Sainte-Marguerite avec un masque de fer" (local file `pamphlet1789_...txt`, pp. 2-3); Paul Lacroix, *L'Homme au masque de fer* (Brussels, H. Dumont, 1836); Pierre-Jacques Arrèse, *Le Masque de fer. L'énigme enfin résolue* (Paris, Laffont, 1970), who argued from the absence of a published death certificate that Fouquet's death was staged and that he reappeared masked at Sainte-Marguerite in 1687 (fr.wikipedia "Homme au masque de fer", section on Arrèse). Roger Macdonald (2005) did not make Fouquet the Mask; his candidate is d'Artagnan (section 16), with Fouquet as one of the "two secret prisoners" of Pignerol in the ordinary sense.

Documented death: Lair 1890, II, p. 472: « Le 23 mars 1680, une sorte d'apoplexie emporta subitement Nicolas Foucquet. » Louvois to Saint-Mars, 9 April 1680 (Arch. nat. K 120, 203; Delort, *Détention*, I, p. 321, as cited by Lair II, p. 473 n.): Saint-Mars authorised « à remettre aux gens de Mme Foucquet le corps de feu Monsieur son mari, pour le faire transporter où bon lui semblera ». The coffin was first deposited "dans un couvent de l'église de Sainte-Claire" at Pignerol; when Fouquet's mother Marie de Maupeou died within the year, mother and son were buried together in the family chapel of the Visitation Sainte-Marie, rue Saint-Antoine, Paris; the convent register records: « Le 28 mars 1681, fut inhumé dans notre église, en la chapelle de Saint-François de Sales, messire Nicolas Foucquet ... » (Lair II, pp. 473-474). Mme de Sévigné's letter on leaving the body at Pignerol is quoted by Lair, p. 473. Louvois's letter of 8 April 1680 about the hole found between Fouquet's and Lauzun's rooms and the two valets (fixed point c) presupposes the death.

Fixed points: fails (a) (Fouquet, arrested 1661, was at Pignerol from January 1665 — he cannot be the valet delivered by Vauroy in 1669), (b) (cannot be his own valet), (c) (the two prisoners of the lower tower are shut up because of his death), (g) (born 27 January 1615: 88 in 1703). Arrèse's version sidesteps (a)-(c) by making the Mask a second prisoner substituted after 1680, which leaves the 1681 and 1687 documents ("the two prisoners of the lower tower", "vingt ans" in 1691) unexplained.

Best counter-argument: no parish death certificate for Fouquet at Pignerol has been published. Reply: the transport authorisation, the family reburial and the convent register are contemporary records of the corpse.

Assessment: residual probability under 0.5%.

---

## 7. James Scott, Duke of Monmouth

Proponent: Germain-François Poullain de Saint-Foix, *Réponse au P. Griffet* (1768), who argued that a substitute was beheaded in Monmouth's place (Topin 1883, pp. 109-115; Laloy 1913, p. 195: "Sainte-Foix (1768) lança l'hypothèse que le Masque de fer aurait été Monmouth").

Documented facts: born 9 April 1649; led the rebellion of June 1685; executed on Tower Hill 15 July 1685. Topin 1883, pp. 109-115, "Preuves irréfragables qui établissent la mort de Monmouth en 1685", cites the dispatches of Barrillon, Louis XIV's ambassador (Archives des affaires étrangères, Angleterre 155, dispatches of 23 and 28 June, 12, 19, 25 and 26 July 1685) and the printed accounts of the scaffold, including the executioner's botched strokes (p. 115). Topin, p. 113: « Monmouth est mort sur l'échafaud le 15 juillet 1685. Des dépêches authentiques en fournissent la preuve, signées de l'ambassadeur de Louis XIV. »

Fixed points: fails (a)-(d) (a free man in England, Holland and France 1669-1685), (e) only if a substitution is accepted, (g) (54 in 1703). Passes none.

Best counter-argument: Saint-Foix's substitution and Louis XIV's interest in the Stuart succession (Topin, pp. 111-112). No document supports it.

Assessment: residual probability effectively zero.

---

## 8. Louis de Bourbon, comte de Vermandois

Proponents: the anonymous *Mémoires secrets pour servir à l'histoire de Perse* (1745), discussed by Griffet (1769), who devoted most attention to this hypothesis (Laloy 1913, p. 195; en.wikipedia list, row 1745).

Documented death (Topin 1883, pp. 82-87, quoting the Archives de la Guerre): fell ill at Courtrai on 6 November 1683 during the siege operations (letter of the maréchal d'Humières to Louvois, "Du camp de Courtray, 7 novembre 1683 — M. de Vermandois a un peu de fièvre ..."); further letters of d'Humières (8, 12, 14 November) and Boufflers (13, 15, 16 November); communion on 16 November; « Le 18 novembre, le fils de la Vallière mourait d'une fièvre maligne, entouré du maréchal d'Humières ..., du marquis de Montchevreuil et du lieutenant général Boufflers » (p. 86); Boufflers to Louvois, 19 November 1683: « après la funeste destinée de M. l'admiral » (p. 86 n.); Mme de Maintenon to Mme de Brinon, 15 November 1683; the body was taken to Arras and buried there (p. 82: « le transport de ses dépouilles à Arras, où il a été enterré »). (The OCR of Topin prints several of these dates as "1685"; the year is 1683.)

Fixed points: fails (a) (born 2 October 1667: aged one in 1669), (b)-(d), (e) (dead at Courtrai in 1683, four years before the transfer), (g) (would have been 36). Passes none.

Best counter-argument: the 1745 story that the prince had struck the Dauphin and was hidden. Contradicted by the sick-bed letters of two generals.

Assessment: zero.

---

## 9. François de Vendôme, duc de Beaufort

Proponents: François-Joseph de Lagrange-Chancel, letter to Fréron in *L'Année littéraire* (1759); the rumour was current at Sainte-Marguerite in Saint-Mars's own time; modern revivals by Jean-Paul Desprat (*Le Secret des Bourbons*, 1991) and Hubert Monteilhet (*Au royaume des ombres*, 2003), who suppose Beaufort captured at Candia and sold by the Turks to Louis XIV (fr.wikipedia "Homme au masque de fer", pointer).

Documents: Beaufort, born 16 January 1616, commanded the French expedition to Candia; in the sortie of the night of 24-25 June 1669 the explosion of a powder magazine caused a rout in which he disappeared and was never found (Topin 1883, ch. X, pp. 126-150, "Certitude de la mort de Beaufort", using the report of the intendant Brodart to Colbert, "à la rade de Candie, à bord de la Princesse, le 27 juin 1669", papiers Colbert 155 bis, Bibliothèque nationale). Saint-Mars to Louvois, 8 January 1688, from Sainte-Marguerite: « Dans toute cette province, on dit que le mien est M. de Beaufort, et d'autres disent que c'est le fils de feu Cromwell » (Laloy 1913, p. 152). Translation: "Throughout this province they say that mine is M. de Beaufort, and others say that he is the son of the late Cromwell." A letter attributed to Louis Fouquet (1687) hints that "all the people that one believes dead are not" (en.wikipedia list, row 1687, citing the *Nouvelles ecclésiastiques*; not checked).

Timing against (a): Louvois's order of 19 July 1669 and the arrest near Dunkirk about 28 July 1669 come thirty-three days after the disappearance at Candia, on the opposite side of Europe; the prisoner was already at Pignerol on 24 August. A captured admiral would have had to be shipped from Crete to the Channel in a month and then described by Louvois as "un valet". Beaufort was 53 in 1669 and would have been 87 in 1703.

Fixed points: fails (a) on timing and description, (b) (a grandson of Henri IV serving as Fouquet's valet), (g). Passes none.

Best counter-argument: the body was never found, and Saint-Mars's own soldiers believed it. Saint-Mars had reported in 1670 that he told tall tales to those who asked (en.wikipedia list, row 1670, citing his letter of 12 April 1670; dossier A, E16).

Assessment: under 0.5%.

---

## 10. A twin or elder brother of Louis XIV

Proponents: Voltaire, *Le Siècle de Louis XIV* (1751) for the story, and the *Questions sur l'Encyclopédie* (1771) for the hint that the prisoner was an elder, illegitimate brother of the King; Michel de Cubières (1789) and the abbé Soulavie, *Mémoires du maréchal duc de Richelieu* (1790), for the twin; Saint-Mihiel, *Le Véritable Homme dit au Masque de fer* (1790), for a son of Anne of Austria and Mazarin (local file: "un fils d'Anne d'Autriche et du Cardinal Mazarin"; his table of contents includes "D'un prétendu frère aîné de Louis XIV"); Charpentier and Manuel, *La Bastille dévoilée* (1790), for a son of the Queen and the Duke of Buckingham born in 1626 (en.wikipedia list, row 1790); Dumas, *Le Vicomte de Bragelonne* (1847-50); Marcel Pagnol, *Le Masque de fer* (1965), reworked as *Le Secret du Masque de fer* (1973) (fr.wikipedia bibliography).

Documented birth: Topin 1883, pp. 58-59, from Chavigny's letter to Richelieu of 6 September 1638, Louis XIII's dispatch to Bellièvre of 9 September 1638 and Dumont's *Corps diplomatique*: on 5 September 1638 at Saint-Germain the King was present from five in the morning; at six arrived Gaston d'Orléans, the princesse de Condé, Mme de Vendôme, the chancellor Séguier, Mme de Lansac, Mmes de Senecey and de la Flotte; the bishops of Lisieux, Meaux and Beauvais said mass at an altar behind the Queen's pavilion; in the next room the dames de la Ville-aux-Clercs, de Liancourt, de Mortemart, the princesse de Guéméné, the duchesses de la Trémouille and de Bouillon, the dukes of Vendôme, Chevreuse and Montbazon, the sieurs de Souvré, de Liancourt, de Mortemart, de la Ville-aux-Clercs, de Brion and de Chavigny, the archbishop of Bourges, the bishops of Metz, Châlons, Dardanie and Le Mans, "enfin une foule énorme qui envahit de bonne heure et remplit bientôt tout le palais"; « À onze heures précises du matin, Anne d'Autriche met au monde un enfant dont la sage-femme fait aussitôt constater le sexe par les princes de la famille royale » (pp. 58-59). Richelieu was absent at Saint-Quentin (p. 62 n.). Topin's argument (pp. 60-63): a second delivery either followed at once before the same witnesses or was foreseen and could not have been hidden from the crowd in the room.

Pagnol's version (fr.wikipedia, sections on Pagnol; his 1973 book snippet on OpenLibrary): the twin was born second, in the evening, hidden, raised abroad, became "James de la Cloche", joined the Roux de Marsilly conspiracy and was arrested at Calais in 1669 under the name Eustache Dauger; the register age is a deliberate falsehood. Pagnol accepted that the prisoner was not Cavoye once Mongrédien's letters appeared ("Enfin, en 1952, l'ouvrage de Georges Mongrédien ... le véritable Eustache Dauger est mort dans la prison Saint-Lazare" — OpenLibrary snippet of Pagnol 1973).

Fixed points: passes (a)-(f) only by identifying the twin with the valet and treating "un valet" as a cover; fails (g) on age (65); no contemporary document mentions a second child, and the witnesses in the room exclude a concealed birth.

Best counter-argument: Pagnol's reading of the birth-chamber sources (that the court had left by evening) and the secrecy of the prisoner's treatment. No document.

Assessment: about 0.5%.

---

## 11. James de la Cloche

Proponents: Edith Carey (1904, Jersey tradition; Barnes's frontispiece shows Trinity Manor, Jersey, "home of Marguerite Carteret, the first love ... of Charles II"); Arthur Stapylton Barnes, *The Man of the Mask* (1908), identifying de la Cloche with the abbé Prignani and with the Mask; Pagnol (section 10).

Documents (Laloy 1913, pp. 24-40, from the Jesuit archives, the letters of "Charles II" to Father Oliva and the Record Office): a "Jacques de la Cloche", claiming to be Charles II's natural son by a Jersey lady, entered the Jesuit novitiate of Sant'Andrea al Quirinale in Rome in April 1668 with letters purporting to come from Charles II (Lang later showed the letters to be forgeries: "The Master Hoaxer", *Fortnightly Review*, vol. 86, cited Laloy p. 40); he left Rome in late 1668 with money from Oliva. In Naples a "James Stuart" or "Don Giacomo Stuardo" married Teresa Corona on 19 February 1669, was arrested as an impostor, released, fell ill and made a will "à Naples, malade et au lit" claiming the principality of Wales or Monmouth for his unborn child (Laloy pp. 35-36, from Armanni's letters, Macerata 1674, and Kent's dispatches); he died in August 1669 and was buried in S. Francesco di Paola outside the Porta Capuana, "car il mourut catholique romain", leaving 400 £ for a tombstone (Kent's report, Laloy p. 36; the church and its registers were destroyed in 1806, p. 36 n. 1); a posthumous son was baptised 10 December 1669 (p. 37). Whether the Naples adventurer and the Roman novice were the same man was disputed (Acton: two men; Brady 1890 and Lang, after seeing Armanni's letter: one man; Laloy pp. 38-40).

Fixed points: if the novice is the Naples Stuart, he died in Naples in August 1669 while the prisoner was being taken to Pignerol: fails (a)-(g). If they are two men, the novice vanishes from all records in late 1668 and nothing connects him with Dunkirk or a valet: no fixed point passed on evidence. Age: unknown, probably born c. 1644-47 (57-59 in 1703).

Best counter-argument (Barnes): the novice was sent to England in the Dover negotiation and returned to France as "Prignani". See section 12.

Assessment: effectively zero.

---

## 12. The abbé Prignani (Pregnani)

Proponent: Barnes 1908, first edition, "adoptant l'hypothèse de lord Acton et voyant dans le Jacques Stuart de Naples un personnage différent du novice de St. Andrea, avait exprimé l'opinion que l'abbé Prignani et ce novice devaient ne faire qu'un" (Laloy 1913, p. 95).

Documents (Laloy 1913, pp. 95-102, from the Affaires étrangères and the archives of Seine-Inférieure): Giuseppe Prignani, a Neapolitan abbé and astrologer, was sent to London in February 1669 and returned to Paris in early July 1669; he held the abbey of Beaubec in Normandy, which fell vacant by his resignation (p. 105); from February 1675 he was in Rome plotting a rising in Naples against Spain, borrowing from the cardinal d'Estrées; in May 1677 the Spanish ambassador said the Viceroy of Naples had men in Rome to seize or kill him; on 26 October 1677 the duc d'Estrées again solicited money for him, "dans une très grande nécessité"; on 21 December 1677 Prignani asked to defer his journey to France because of the season and "son indisposition"; « Il ne semble pas qu'il soit revenu dans notre pays, car il mourut à Rome à la fin de 1678 ou au commencement de 1679 (arch. Seine-Inf., G. 6139, f° 85) » (Laloy, p. 101). The memoirs of Primi Visconti also record his death in Rome in 1679 (pointer: en.wikipedia "James de la Cloche"; not checked).

Fixed points: fails (a)-(c) (free in Paris in July 1669 and in Rome 1675-78, while the prisoner was at Pignerol), (d)-(g) (dead by early 1679). Passes none.

Best counter-argument: none that survives the 1675-78 Roman correspondence.

Assessment: zero.

---

## 13. Nabo, the black page of Queen Marie-Thérèse

Proponent: Pierre-Marie Dijol, *Nabo ou le Masque de fer* (Paris, France-Empire, 1978, 266 pp.) (fr.wikipedia bibliography). Thesis: the Queen's black daughter, the "Mauresse de Moret" (Louise-Marie-Thérèse, Benedictine nun, d. 1732), was fathered by the dwarf page Nabo, who was removed from court and became the masked prisoner.

Documents: none produced for Nabo's fate. The existence of a black nun at Moret who claimed royal birth is documented in eighteenth-century memoirs (Saint-Simon, the princesse Palatine); the paternity is court gossip. No record places a black page near Dunkirk in July 1669 or in Saint-Mars's letters; the only description of the prisoner's person, in du Junca's entries and in later Bastille recollections, mentions nothing of the kind.

Fixed points: no fixed point is documented for him; (a) is asserted only by identifying the "valet" with a page. Age unknown.

Best counter-argument: "un valet" is compatible with a page, and the mask would hide a face that would identify the man at once. This cuts both ways: every warder, surgeon and confessor saw the face, and none remarked on it.

Assessment: effectively zero.

---

## 14. Molière

Proponents: Anatole Loquin (under the pseudonym "Ubalde"), *Le Secret du masque de fer: étude sur les dernières années de la vie de J.-B. Poquelin de Molière (1664-1703)* (Bordeaux, Féret; Orléans, Herluison, 1883); Loquin, *Molière à Bordeaux vers 1647 et en 1656, avec des considérations nouvelles sur ses fins dernières à Paris en 1673 ... ou peut-être en 1703* (Actes de l'Académie de Bordeaux, 1898; archive.org `molirebordea01loqu`, `molirebordea02loqu`); Loquin, *Un secret d'État sous Louis XIV et Louis XV: le prisonnier masqué de la Bastille, son histoire authentique* (Paris, 1900); Marcel Diamant-Berger, *C'était l'homme au masque de fer* (Paris, JF Éditions, 1971). Loquin's main argument was that the first biography of Molière (Grimarest, 1705) appeared two years after the Mask's death and that Molière was removed at the Jesuits' instance for *Tartuffe* (fr.wikipedia, section on Loquin).

Documents:

- Activity in 1669 (La Grange 1876, pp. 107-108, register entries): the troupe played in Paris through July 1669 (*Les Fâcheux*, *L'École des maris*, *George Dandin*), went "à Saint-Germain par ordre du Roy" on Saturday 3 August 1669 to play *L'Avare* and *Tartuffe*, returned 5 August; played *Tartuffe* on 9, 11, 13 August; « Mercredy 21 [août 1669] ... Ce mesme jour, le Père de M. de Molière est mort »; Saint-Germain again 23 August-1 September (*La Princesse d'Élide* four times); « Mardy 17 [septembre 1669]. La Troupe est partie pour aller à Chambord. On y a joué, entre plusieurs comédies, le Pourceaugnac pour la première fois. Le retour a esté le Dimanche 20 Octobre. » Molière created the title role of *Monsieur de Pourceaugnac* at Chambord.
- Death (La Grange 1876, p. 140, entry of Friday 17 February 1673): « Ce mesme jour, aprez la comédie, sur les 10 heures du soir, Monsieur de Molière mourut dans la maison, rue de Richelieu, ayant joué le rôle dudit Malade imaginaire, fort incommodé d'un rhume et fluxion sur la poitrine qui lui causait une grande toux, de sorte que, dans les grands efforts qu'il fit pour cracher, il se rompit une veine dans le corps et ne vécut pas demi-heure ou trois quarts d'heure, depuis ladite veine rompue. »
- Burial (register of Saint-Eustache, transcribed by Beffara 1821, p. 16): « Le mardi 21e février 1673, défunt Jean-Baptiste Poquelin de Molière, tapissier-valet-de-chambre ordinaire du roi, demeurant rue de Richelieu, proche l'Académie des Peintres, décédé le 17 du présent mois, a été inhumé dans le cimetière de Saint-Joseph. » Beffara notes that the entry carries no witnesses' signatures and is followed by two or three blank lines (p. 16) — the detail Loquin exploited.

Fixed points: fails (a) (in Paris and at Chambord, on stage, in August-October 1669 while the prisoner was at Pignerol), (b)-(d) (alive and performing in Paris until 17 February 1673), (g) (born 15 January 1622: 81 in 1703). Passes none.

Best counter-argument: the night burial without witnesses' signatures and the absence of any autopsy. Against it stand La Grange's register, the widow's petition to the archbishop, and the three-year gap between the arrest of the prisoner (1669) and Molière's death (1673).

Assessment: zero.

---

## 15. Avedick, Armenian patriarch of Constantinople

Proponent: the chevalier Pierre de Taulès, *L'Homme au masque de fer, mémoire historique où l'on réfute les différentes opinions relatives à ce personnage mystérieux et où l'on démontre que ce prisonnier fut une victime des Jésuites* (Paris, 1825, posthumous; local file, title page).

Documents (Topin 1883, pp. 168-170 and 197-199, from the Affaires étrangères and Depping's *Correspondance administrative*): « Avedick avait été déposé le 25 février 1706. Deux mois après on le transportait en exil. Le 20 avril, il quittait Constantinople » (p. 168); seized at Chios by the French vice-consul on the ambassador Ferriol's orders, shipped to Marseille and handed to the intendant des galères Montmor (pp. 169-170); Mont-Saint-Michel, then the Bastille; abjured on 22 September 1710 before Cardinal de Noailles, was ordained priest at Notre-Dame and released (p. 197); « Dix mois après être sorti de la Bastille, le 21 juillet 1711, il mourut » (p. 198; the OCR reads "1714", the footnote gives the Saint-Sulpice burial extract delivered 14 August 1711); buried in the Saint-Sulpice cemetery (p. 198 n.). Taulès knew the 1706 dispatches and tried to discount du Junca's dates (Topin, pp. 175-176).

Fixed points: fails all seven: still patriarch at Constantinople in February 1706, more than two years after the prisoner's burial. Age (born c. 1657: 46 in 1703) is the only fit, and it is a coincidence.

Assessment: zero.

---

## 16. Other named candidates

### 16.1 Henri II de Lorraine, duc de Guise (Camille Bartoli)

Bartoli, *Henri II de Guise, l'homme au masque de fer — sa vie et son secret* (Tac Motifs, 1977); *J'ai découvert l'inconcevable secret du Masque de fer* (A. Lefeuvre, 1978); *La fin du black-out: Henri II de Guise, l'homme au masque de fer* (Éditions Clémentine, 3 September 2012) (fr.wikipedia bibliography; publisher pages). Thesis: Guise as pretender of a secret Carolingian-restoration group. Documented: born 4 April 1614, died in Paris 2 June 1664 (standard biographical dates; en.wikipedia list, row 1978; I did not verify the death in a primary source). Fails (a)-(g) (dead five years before the arrest; would have been 89). Zero.

### 16.2 "The son of Cromwell"

Not a scholar's proposal but a garrison rumour reported by Saint-Mars himself on 8 January 1688 (« le fils de feu Cromwell », Laloy p. 152). Richard Cromwell (1626-1712) died at Cheshunt; Henry Cromwell died 1674 at Wicken (en.wikipedia list, rows 1688). Zero.

### 16.3 Lagrange-Chancel (1759)

Proposed Beaufort (section 9), on the basis of what he claimed to have heard at Sainte-Marguerite while a prisoner there in 1719-22.

### 16.4 Sébastien de Penancoët de Kéroualze (François Ravaisson, 1879)

Ravaisson X (1879), Avertissement, pp. xx-xxiii, dated 31 January 1879: an ensign of Beaufort's guards, lieutenant of the flagship at Candia in 1669, brother of Louise de Kéroualle, duchess of Portsmouth. Laffilard's naval register has him "tué sur le Monarque en 1671" (altered from 1670), while a family genealogy says "il mourut au retour de cette expédition, sans alliance" (p. xx). Ravaisson's reasoning: the discrepancy hides a secret; "M. de Keroualze aura été pris avec l'amiral" and was the officer charged with negotiating Beaufort's exchange, then buried alive at Pignerol; Saint-Mars's contempt fits "un domestique de la maison de Vendôme"; a sailor speaks languages and plays the guitar; on the age: « Or, M. de Keroualze, âgé de vingt-deux ans en 1669, aurait eu cinquante-cinq ans en 1703 ; serait-il extravagant de penser que les officiers du château ont rajeuni le défunt, ou que le bon prêtre avait entendu quarante-cinq au lieu de cinquante-cinq ans. Si le curé a écrit Marchiali ..., à la Bastille M. Du Junca a écrit Marchiel, ne serait-ce pas un nom bas-breton mal orthographié, peut-être Marcel ou bien Marecal, c'est-à-dire Maréchal » (p. xxiii). Ravaisson himself: « Nous n'osons affirmer qu'on doive désormais appeler l'homme au masque de fer M. de Keroualze » (p. xxiii). Fails (a) on the same timing as Beaufort (Candia 25 June — Dunkirk 28 July 1669) and on "valet"; the naval register records him killed at sea. Residual probability about 0.1%.

### 16.5 "Louis de Oldendorf" / the "gentilhomme lorrain" (Théodore Iung, 1873)

Iung 1873, chapter XXII (pp. 374-382 and following): a horseman arrested in the night of 28-29 March 1673 at a ford of the Somme near Péronne, who "prétendit s'appeler Louis de Oldendorf" of Nijmegen, taken to the Bastille, interrogated by Louvois in person; Louvois to Méthelet, 7 April 1673: « L'on a arrêté depuis quelques jours, à Péronne, un homme appelé Louis de Oldendorf, qui se dit de la ville de Nimègue » (p. 374); Iung makes him the Lorraine ex-cavalry captain who used the aliases chevalier de Kiffenbach and chevalier des Harmoises, head of a poisoning plot against Louis XIV, and identifies him with "l'homme que vous savez" of the Bastille letters, with the prisoner sent to Pignerol in 1674, and with "de Marchiel" on the register. Laloy 1913, pp. 122-128: « Il n'est donc pas prouvé que Louis de Oldendorf ait jamais été enfermé à Pignerol et il est sûr qu'il n'y était pas en 1681. Ce n'est donc pas lui qui a été le prisonnier "toujours masqué d'un masque de velours noir" qui est mort le 19 nov. 1703 » (p. 127); the 1674 prisoner was the Jacobin monk. Loiseleur 1882, p. 321: Iung "ne parvenait point à établir de liaison évidente entre l'affaire des empoisonneurs et le drame du Masque". Fails (a) (arrested 1673, not 1669), (b)-(e). Residual probability about 0.2%.

### 16.6 Others recorded in the literature (pointers only, from the en.wikipedia list of candidates and fr.wikipedia bibliography; none of these books read)

- Jules Loiseleur (1867): a prisoner "Guibert" brought to Pignerol by Catinat — in *Trois énigmes* (1882), p. 244 n., Loiseleur himself explains that "Guibert" was Catinat's own alias in 1681, later "Richemont".
- Anonymous, *Journal de Mâcon* (1869): the chevalier de Rohan (beheaded at the Bastille 27 November 1674).
- Domenico Carutti (1893): the Dominican monk "Lapierre" (died Pignerol January 1694). Fernand Bournon (1893): a son of a great family. Maurice Boutry (1899): various royal bastards of eighteenth-century rumour.
- Franz Scheichl (1914): Jacques Bretel de Grémonville (d. 29 November 1686 at Lyre abbey).
- Émile Laloy (1931): "Eustache Daugé". Pierre Vernadeau (1934): Marc de Jarrige de la Morelhie (d. 14 December 1680).
- Hugh Ross Williamson (1955, after Lord Quickswood): Louis XIV's illegitimate father.
- Roger Macdonald, *The Man in the Iron Mask* (London, Constable; New York, Carroll & Graf, 2005): d'Artagnan, supposedly not killed at Maastricht on 25 June 1673 but imprisoned at Pignerol, with the "two secret prisoners" being Étienne Martin alias Eustache Danger and d'Artagnan; fr.wikipedia summarises the argument from Courtilz de Sandras's *Mémoires de M. d'Artagnan* (Courtilz being at the Bastille 1702-11). Fails (a)-(c) (d'Artagnan arrested Fouquet in 1661 and commanded the musketeers until 1673) and (g) (born c. 1611-15: about 90 in 1703).
- Sarah B. Madry, *Second Son: Man in the Iron Mask* (Locate Press, 2024): a secret younger brother of Philippe d'Orléans with a facial defect, placed with caretakers as "Eustache Dauger" (search-result summary; not read).
- Michel-Vital Le Bossé, *Le Masque de fer: c'est la faute à Voltaire* (1991): not read; position unknown to me.
- "The Arwenack": I found no candidate of this name in any source consulted (Arwenack is the Killigrew seat at Falmouth; no Killigrew was ever proposed as the Mask so far as I can find). "The Duke of Buckingham's son" is the Charpentier-Manuel hypothesis of 1790 (section 10).

---

## 17. The name "Marchioly" / "Marchiali" / "Marchiel"

Documents (Funck-Brentano 1901, pp. 87-89):

- Du Junca's register of exits, 19 November 1703: « le prisonnier inconnu, toujours masqué d'un masque de velours noir, que M. de Saint-Mars, gouverneur, a mené avec lui en venant des îles Sainte-Marguerite, qu'il gardait depuis longtemps, lequel s'étant trouvé un peu mal hier en sortant de la messe, il est mort ce jourd'hui, sur les dix heures du soir, sans avoir eu une grande maladie ... Et ce prisonnier inconnu, gardé depuis si longtemps, a été enterré le mardi, à quatre heures de l'après-midi, 20e novembre, dans le cimetière Saint-Paul, notre paroisse; sur le registre mortuel on a donné un nom aussi inconnu. » In the margin: « J'ai appris depuis qu'on l'avait nommé sur le registre M. de Marchiel, qu'on a payé 40 livres d'enterrement. » (Bibliothèque de l'Arsenal, mss. 5133-5134; Funck-Brentano prints the text with modernised spelling and a facsimile.)
- Register of Saint-Paul: « Le 19e (1703), Marchioly, âgé de quarante-cinq ans, ou environ, est décédé dans la Bastille, duquel le corps a été inhumé dans le cimetière de Saint-Paul, sa paroisse, le 20e du présent, en présence de M. Rosage (sic), majeur de la Bastille, et de M. Reglhe (sic) chirurgien majeur de la Bastille, qui ont signé. — Signé : Rosarges, Reilhe. » The original was in the Archives de la Ville de Paris and burned in 1871; the facsimile survives in Topin's English translation (Vizetelly, London, 1870) and in the 5th French edition (1878) (Funck-Brentano, p. 89 n. 1). Griffet (1769) first printed both extracts and read "Marchiali" (Laloy, p. 195).

Interpretations:

- Funck-Brentano (pp. 119-120): the name is Mattioli's, pronounced "Markioly" in Italian; Saint-Mars habitually wrote "Martioly"; the major's own name is more deformed ("Rosage" for Rosarges) than the prisoner's.
- Iung (1873): reads du Junca's "Marchiel" as the true name of a Lorraine family "Marcheuille" (Laloy, pp. 127-128, who replies that du Junca only repeated what the priest had been told, and that "si l'on s'arrête à des similitudes de nom, on est fatalement conduit sur la piste Matthioly").
- Ravaisson (1879): a Breton name misspelt, "Marcel" or "Maréchal" (section 16.4).
- Barnes (1908): "They buried him under the name of Marchioly, giving him no doubt a false name, as the law required" (OpenLibrary snippet; Barnes holds "that his name, whatever it may have been, was not Marchioly or anything the least like it").
- Lang, Laloy, Mongrédien, Petitfils: a false name chosen by Saint-Mars, whether as a leak of Mattioli's name or, more probably, as a deliberate red herring ("Marchioly ... d'aucuns liront Marchialy", Petitfils 2003, OpenLibrary snippet); Petitfils, like Funck-Brentano, notes the Italian pronunciation.
- Later speculation (Marriott, *Bad History*): a garbling of "Marsilly", on Lang's Martin hypothesis. No document supports it.

The age "quarante-cinq ans ou environ": supplied by Rosarges and Reilhe, who had known the prisoner five years; it fits none of the serious candidates (the valet at least 53 by Lang's reckoning; Mattioli 62; Cavoye and Bulonde 66). Ravaisson's suggestion that the staff "rajeuni le défunt" or the priest misheard is as good as any; the figure cannot discriminate between candidates.

---

## 18. Candidates proposed after 2000 (with proposer and date)

- Jean-Christian Petitfils, *Le Masque de fer: entre histoire et légende* (Paris, Perrin, 2003; revised 2004): the valet Eustache Danger, probably a courier in the Dover negotiation (section 1). Reviewed in *Dix-huitième siècle* 37 (2005) (Persée, pointer).
- Hubert Monteilhet, *Au royaume des ombres* (2003): Beaufort (section 9).
- John Noone, *The Man Behind the Iron Mask*, new edition (Sutton, 2003): as section 1; his own theory is of Saint-Mars's "face-saving mask", not of a new person.
- Roger Macdonald, *The Man in the Iron Mask* (2005): d'Artagnan (section 16.6), with Eustache Danger = Étienne Martin as the second secret prisoner.
- Michel Vergé-Franceschi, *Le Masque de fer enfin démasqué* (Paris, Fayard, 2009, 476 pp.): the prisoner as a valet of the duc de Beaufort (per Madry 2016; the book's own conclusion not read; its snippets show him surveying "Cromwell et Beaufort ... pistes à retenir").
- Camille Bartoli, *La fin du black-out* (2012): Henri II de Guise (section 16.1).
- Paul Sonnino, *The Search for the Man in the Iron Mask: A Historical Detective Story* (Lanham, Rowman & Littlefield, 2016, xiv-252 pp.): Dauger as valet of Antoine-Hercule Picon, manager of the late Mazarin's fortune (Ruff, *H-France Review* 16 (2016), no. 258; section 1).
- Sarah Madry, "The Valet: The Marquis de Louvois's Invited Guest in the Mystery of the Man in the Iron Mask", *Cahiers du dix-septième* 17 (2016), pp. 1-27 (https://earlymodernfrance.org/journal/2016-volume-xvii/): "un valet" as a pun; it concerns Louvois's word "valet", not Fouquet's servant.
- Josephine Wilkinson, *The Man in the Iron Mask: The True Story of Europe's Most Famous Prisoner* (Pegasus, 2021): "only a valet" (section 1).
- Sarah B. Madry, *Second Son* (2024): a secret brother of Philippe d'Orléans (section 16.6).

None of these proposes a new documented person who can be tested against the fixed points except Macdonald (d'Artagnan, fails) and Bartoli (Guise, fails); the rest are hypotheses about the identity of the valet of 1669.

---

## 19. Summary table

Fixed points: a = 1669 arrest/delivery as "un valet"; b = 1675 service to Fouquet; c = 1680 lower tower with La Rivière; d = 1681 Exilles; e = 1687 survivor to Sainte-Marguerite; f = 1698 Bastille as "ancien prisonnier de Pignerol"; g = 19 Nov 1703 death, "Marchioly", "45 ans ou environ". "Passed" means not contradicted by documents (for the valet, passed by construction). Probabilities are rough and provisional.

| Candidate | Principal proponents (work, year) | Fixed points passed | Fixed points failed | Decisive document | Residual probability |
|---|---|---|---|---|---|
| Eustache Dauger/Danger, valet (whoever he was) | Lair 1890; Lang 1903; Laloy 1913; Mongrédien 1952; Petitfils 1970/2003; Noone 1988; Sonnino 2016; Wilkinson 2021 | a-g (e depends on the 1687 survivor) | none; g only on age (≥53) | Louvois 19 Jul 1669; Barbezieux 13 Aug 1691 "depuis vingt ans"; du Junca 1698/1703 | ~85% |
| La Rivière, Fouquet's valet | none explicit; implicit alternative for the 1687 survivor | b, c, d | a; e (probably); g age unknown | Barbezieux 13 Aug 1691 "depuis vingt ans" (Iung; Laloy pp. 152-153) | ~5% |
| Ercole Antonio Mattioli | Heiss 1770; Roux-Fazillac 1801; Delort 1825; Ellis 1826; Topin 1869/1883; Funck-Brentano 1894/1898 | f (loose reading); name at g | a, b, c, d, e; g age 62; probably dead Apr 1694 | Barbezieux 10 May 1694 "le valet du prisonnier qui est mort" (Iung p. 91; Laloy p. 160); Louvois 1681 letters | ~3-4% |
| Eustache Dauger de Cavoye | Duvivier 1932; Furneaux 1954; Mast 1974; Thompson 1987 | none | a, b, c, (d, e); g age 66 | Letters of 20 Jun 1678 and c. 1679/80 from Saint-Lazare (Mongrédien, *XVIIe siècle* 17-18, 1953, pp. 55-58); Louis XIV 17 Aug 1678; Brienne's ode (by 1689) | <0.5% |
| Vivien Labbé de Bulonde | Bazeries & Burgaud 1893 | none | a-g | Dangeau III p. 441 (11 Dec 1691 release); Grandmaison receipts 1699, 1705 (*L'Univers* 9 Jan 1895; Funck-Brentano p. 111); Batiffol BEC 1894 | <0.5% |
| Nicolas Fouquet | 1789 pamphlet; Lacroix 1836; Arrèse 1970 (not Macdonald) | none | a, b, c, g (age 88) | Lair II pp. 472-474: death 23 Mar 1680; Louvois 9 Apr 1680; Visitation register 28 Mar 1681 | <0.5% |
| Duke of Monmouth | Saint-Foix 1768 | none | a-e, g (54) | Barrillon's dispatches Jun-Jul 1685 (AAE Angleterre 155; Topin pp. 109-115) | ~0 |
| Comte de Vermandois | anon. 1745; discussed Griffet 1769 | none | a (aged 1 in 1669), b-e, g (36) | d'Humières/Boufflers letters 7-19 Nov 1683 (Topin pp. 83-87); burial at Arras | 0 |
| Duc de Beaufort | Lagrange-Chancel 1759; Desprat 1991; Monteilhet 2003 | none | a (Candia 25 Jun 1669 vs Dunkirk 28 Jul 1669; "valet"), b, g (87) | Brodart report 27 Jun 1669 (Topin ch. X); Saint-Mars 8 Jan 1688 reporting the rumour | <0.5% |
| Twin/elder brother of Louis XIV | Voltaire 1751/1771; Soulavie 1790; Saint-Mihiel 1790; Dumas; Pagnol 1965/1973 | a-f only by identification with the valet | g (65); no document; birth witnesses | Chavigny 6 Sep 1638; Louis XIII 9 Sep 1638 (Topin pp. 58-59) | ~0.5% |
| James de la Cloche | Carey 1904; Barnes 1908; Pagnol | none | a-g if = Naples Stuart (d. Aug 1669) | Kent's dispatches and the Naples will (Laloy pp. 35-37) | ~0 |
| Abbé Prignani | Barnes 1908 | none | a-g (free in Rome 1675-78; d. 1678/79) | arch. Seine-Inf. G 6139 f° 85 (Laloy p. 101) | 0 |
| Nabo, the Queen's page | Dijol 1978 | none documented | a (no document), g unknown | none exists | ~0 |
| Molière | Loquin 1883/1898/1900; Diamant-Berger 1971 | none | a-d, g (81) | La Grange register 1669 and 17 Feb 1673 (1876 ed. pp. 107-108, 140); Saint-Eustache burial 21 Feb 1673 (Beffara 1821 p. 16) | 0 |
| Avedick | Taulès 1825 | none | a-g (in Constantinople until Apr 1706) | Topin pp. 168-170, 197-199 | 0 |
| Henri II de Guise | Bartoli 1977/1978/2012 | none | a-g (d. 2 Jun 1664) | standard death date (not verified in a primary source) | 0 |
| "Son of Cromwell" | garrison rumour, Saint-Mars 8 Jan 1688 | none | a-g | Saint-Mars 8 Jan 1688 (Laloy p. 152) | 0 |
| Kéroualze | Ravaisson 1879 | none | a (timing, "valet"); g (56) | Laffilard's register "tué sur le Monarque" (Ravaisson X pp. xx-xxiii) | ~0.1% |
| Louis de Oldendorf | Iung 1873 | none | a (arrested Mar 1673), b-e | Louvois 7 Apr 1673 (Iung p. 374); Laloy pp. 122-127 | ~0.2% |
| d'Artagnan | Macdonald 2005 | none | a-c, g (~90) | his career 1661-1673 | ~0 |

---

## 20. What I could not find

- Any author who names La Rivière outright as the 1703 prisoner.
- The text of Bazeries and Burgaud 1893 (Gallica blocked; not on archive.org); Batiffol's p. 360; Bulonde's death record (1709 per Mongrédien 1952, unverified).
- Duvivier 1932 (unread) and Mongrédien 1952 (read only in Gallica ContentSearch snippets, `sources/mongredien_1952_snippets.md`); the Brienne ode (Adam 1938) and Louis XIV's letter of 17 August 1678 in the original.
- A primary source for Henri II de Guise's death (2 June 1664) and for Beaufort's funeral honours of 1670.
- Any candidate called "the Arwenack".
- Saint-Mars's own letter of 29 April 1694 announcing the death of "the prisoner with a valet".
- The exact page range of Sonnino's 1991 article (given as 99-108 and as 261-272 in different secondary references).
