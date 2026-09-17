# H — masque-de-fer.com: transcriptions of the original documents, compared with the printed editions

Harvest date: 2026-09-14. Site: http://www.masque-de-fer.com/ (plain HTTP; HTTPS fails through the proxy). Crawl: seeds = home page, /ressources/, and the WordPress sitemap (wp-sitemap.xml: 13 posts, 33 pages, 3 categories, 1 author); every internal link followed, 1 s between requests. Result: 52 pages fetched, HTTP 200 on all of them, no page failed to load, queue empty (the site has no further internal pages). Eleven document images (the site's facsimiles) were also downloaded.

Files:
- HTML and cleaned text of every page: `sources/masque-de-fer.com/<slug>.html` and `<slug>.txt` (each .txt starts with SOURCE / FETCHED / TITLE lines). Slugs are the WordPress slugs; structural pages use `category__media`, `author__claudedabos`, `page__2`, etc. The page `/presentation/` is `presentation-2` because the 2016 post of the same slug took `presentation`.
- Manifest (url, status, slug, title, bytes): `sources/masque-de-fer.com/_manifest.tsv`.
- Facsimiles: `sources/masque-de-fer.com/images/` — 1673_03_29.jpg, 1679_08_18.jpg, 1679_09_13.jpg, 1680_03_12.jpg, 1680_04_08_p1.jpg … p5.jpg, 1687_04_18.jpg, 1687_09_04.jpg.
- Printed editions used for comparison (OCR files in `sources/`): delort1825_histoire_homme_masque_de_fer.txt, delort1829_detention_philosophes_vol1.txt, iung1873_verite_masque_de_fer.txt, loiseleur1882_trois_enigmes_historiques.txt, topin1883_homme_au_masque_de_fer.txt, lair1890_nicolas_foucquet_vol2.txt, funckbrentano1901_legendes_et_archives_bastille.txt, laloy1913_masque_de_fer_lacloche_prignani_marsilly.txt, ravaisson1866_archives_bastille_t3.txt, ravaisson_archives_bastille_vol08_1675-1686.txt, ravaisson_archives_bastille_vol09_1687-1692.txt. The OCR text has double spaces between words and frequent character errors; quotations below are cleaned of double spaces only. Line numbers refer to those files.

Conventions: text inside « » or in the blocks headed "Transcription (site)" is copied from the site character for character (typographic apostrophes, guillemets, the site's own "(sic)" and "(1)" marks, its typing errors such as "vostœ" and "4chargé"). "Site commentary" summarises the site author's remarks and is his opinion. "My reading of the facsimile" is my own transcription of the site's image and is labelled as such every time.

---

## 1. Who runs the site and what it claims about its sources

- Title tag: "Le Masque de fer – Une enquête historique de Claude Dabos". WordPress site; single author account "claudedabos"; footer "Fièrement propulsé par WordPress". The pages carry reader comments (35 on /presentation/), which are not the author's text.
- Author page (/qui-suis-je/): Claude Dabos, born 15 June 1935 at Villeneuve-sur-Lot; studies at Vic-Bigorre, La Seyne and Cannes (1941-1953); military service and musical studies at Versailles (1954-1957); orchestral musician, mainly at Cannes (1958-2002); deputy director and professor at the Conservatoire de musique de Cannes (1980-2002). Publications and appearances listed by him: Le Parisien, 24 August 2000; lectures for the Cercle d'Histoire et Archéologie Mouginois (12 January 2004) and the Amis des Archives de Cannes (31 January 2004); Nice-Matin interview 14 March 2004; article in the Annales de la Società Storica Pinerolese, 2 May 2005; Nice-Matin 4 September 2005; talk at the Lycée Carnot de Cannes 3 October 2005; France Inter, "Histoires possibles et impossibles", 20 November 2005; Top Secret hors-série n°3 (December 2006-January 2007), titled elsewhere on the site "Le grand secret du Masque de fer"; Secrets d'histoire (Stéphane Bern), 2 March 2008; "2012 : Analyse de ma thèse par Jean-Christian Petitfils dans Le Masque de fer : entre histoire et légende"; lecture at Mandelieu 28 December 2012; RMC Découverte documentary 19 December 2016. Later posts add lectures on "L'énigme du Masque de fer et de Rennes-le-Château" (14 September 2021) and at Rennes-les-Bains (2026), and a book: "Le Masque de fer – Mon enquête", 464 pages, dated 18 June 2026, 19,99 €, sold on Amazon (/mon-livre/).
- He is not a professional historian; the site calls him "le chercheur Claude Dabos" and "le propriétaire de ce site". The "Présentation" page states the site's purpose: a chronology of "faits et documents dont on dispose de nos jours, y compris certains non dévoilés jusqu'ici", plus "le synopsis de ma thèse".
- Claims about sources. The "Enigme" page: « Au cours de mes années de recherches dans les Archives nationales, La découverte de documents longtemps ignorés des chercheurs, et d'ailleurs inédits, allait me permettre de trancher. » The 13 September 1679 commentary: « J'ai recherché en vain aux Archives nationales la réponse de Saint-Mars. Ce faisant, j'ai découvert en revanche une lettre [12 mars 1680] dont on est en droit de se demander comment il est possible que, bien que la connaissant, les spécialistes de cette énigme la laissent ignorer au public depuis un siècle ». The 12 March 1680 commentary: « Depuis 1825, date où Joseph Delort l'a publiée dans sa Détention des Philosophes et gens de lettres, cette lettre est restée ignorée du public mais non des spécialistes de l'énigme » (Delort's Détention des philosophes is dated 1829; the letter is in it, vol. 1 p. 316, see §3). The blog post of 26 March 2025: « Voir l'original de la lettre du 8 avril 1680 » and « Voir l'original de la lettre du 12 mars 1680 » link to the facsimiles.
- What the site actually provides, by class of source:
  1. Photographs of the originals plus a transcription for five Louvois letters in Archives Nationales K120 (nos 132, 275, 277, 299, 302). These are the only items where the reader can check the site's reading against the manuscript.
  2. Text only, with a Vincennes reference, for three letters: "Service Historique de l'Armée de Terre (Vincennes) – série A1 Vol.654 p.232" (12 May 1681), "Série A1, vol.675 p.36" (2 March 1682), "Série A1, vol.686, p.216" (11 March 1682). The wording of these three is modernised and, as §3 shows, close to the printed editions.
  3. Text copied from a printed edition and modernised for the Saint-Mars letters of 14 January 1673, February-March 1673, 18 December 1675 and Lauzun's letter of 27 January 1680: the source line is "Archives de la Bastille – recueillies par François Ravaisson"; the 3 December 1675 Louvois letter in a commentary is sourced "(Source Gallica – BNF)".
  4. One manuscript reproduced as an image without any transcription (18 April 1687, "Voyage à Gènes", Médiathèque de Nîmes) and one manuscript gazette page reproduced with transcription (4 September 1687, Bibliothèque Sainte-Geneviève).
- The site is an advocacy site for the thesis that the prisoner was Nicolas Fouquet (see §4). Its transcriptions and its commentary are interleaved on every page; they are separated below.

---

## 2. Documents transcribed on the site (the fourteen "Ressources" pages)

### 2.1 — 14 January 1673, Saint-Mars to Louvois
- URL: /ressources/lettre-du-14-janvier-1673-de-saint-mars-a-louvois/ (file lettre-du-14-janvier-1673-de-saint-mars-a-louvois.txt)
- Reference given: "Archives de la Bastille – recueillies par François Ravaisson" (no volume or page). No facsimile.
- Transcription (site):

Monseigneur, par celle qu’il a plu de me faire l’honneur de m’écrire le 4 du courant (janvier 1673), vous me commandez que lorsque je retomberai sur les choses que M. Fouquet m’a dites concernant le bien et intérêt du roi, que je lui propose de me les dire pour les mander. Comme il me donne lieu de cela toutes les fois que je lui parle, il me demandait si je ne vous ai rien fait savoir de tout ce qu’il m’a dit, je le fis voir devant hier au soir, où nous vînmes à parler des inventions dont les gens d’esprit se servaient pour avoir de la finance ; il me dit qu’il n’était pas mal propre à cela et qu’il trouvé des expédients pour en avoir où d’autres personnes seraient demeurés court.

Après force choses, il me dit : « Comme je me vois tout moribond, je charge votre honneur et la fidélité que vous avez pour le Roi de faire savoir à M. le marquis de Louvois comme je m’occupe depuis longtemps à examiner les services les plus considérables qu’on pourrait rendre à S. M. et que Dieu m’a donné des lumières d’affaires si grandes et de desseins si importants, si faciles et si glorieux, que je lui ferais un sensible déplaisir qu’elles fussent perdues sans qu’on en eût connaissance. »

Sur ce je pris la parole et lui dis qu’il ne tiendrait qu’à lui que le Roy ne sût ses grands desseins et bonnes intentions, et qu’assurément s’il les reconnaissait tels qu’il dit que S.M. adoucirait ses peines ; il m’a fait excuse de ce qu’il ne pouvait pas me confier son secret, disant que j’aurais peine à entendre des choses qui ne sont que de la portée d’un ministre versé à la connaissance de toutes sortes d’affaires.

De la manière qu’il me parut être sincère et véritable en tout ce qu’il disait je lui offris du papier et de l’encre pour qu’il me donnât par écrit les choses importantes qu’il dit savoir pour le profit du Roi ; mais il me dit franchement qu’il ne pouvait me déclarer le détail de ses pensées pour vous les mander, non pas par aucune raison de son intérêt et bien moins par manque de confiance en vous, mais par la nature des affaires que je n’entends pas ; il a conclu son discours en me disant que si vous lui vouliez faire l’honneur de lui promettre votre protection, qu’il fera tout ce que vous voudrez et comme vous le voudrez, mais il m’a fait assez connaître qu’il ne voudrait point que personne que le Roi et vous eussent connaissance et que l’affaire doit être secrète ; il m’a dit cent mille autres paroles, mais voilà, Monseigneur, tout ce que j’en ai pu retenir ; il ne manquera pas de me parler incessamment de cela, mais comme vous ne me commandez pas de me charger d’aucune chose, je l’écouterai sans lui répondre que très peu de choses, comme m’étant indifférent.

Pour vous parler à fond de cette affaire ici, enfin de ne plus vous en rompre la tête, je prends la liberté, Monseigneur, de vous dire mes petites pensées : l’une est que je crois que M. Foucquet dirait mieux la chose à un homme entendu et versé dans les affaires qu’à moi qui n’y entends rien du tout, mais auparavant de tout déclarer, il serait bien aise que vous lui promissiez votre protection et assistance ; pour cet effet, si vous lui vouliez envoyer M. Nallot qui est homme habile et entendu, je m’assure qu’il lui dirait toutes ses pensées devant moi, et que vous seriez content de son voyage et du rapport qu’il vous ferait de toutes choses ; d’autre côté je ne fais point de doute que si vous lui faîtes la moindre honnêteté pour qu’il vous donne tout par écrit, et que vous me commandiez de lui donner du papier par compte pour le laisser écrire plus commodément, je crois qu’il vous ferait un détail fort fidèle de tout son secret et de ses pensées. En faisant cela de bonne grâce comme il le fera sans doute, il vous prierait en même temps de forces choses pour ses intérêts et son élargissement…

- What it establishes: in January 1673 Fouquet told Saint-Mars that he held matters of great consequence for the King's service and wanted Louvois's protection before disclosing them; Saint-Mars proposed sending Nallot or letting Fouquet write. Elsewhere on the site (les-secrets-de-nicolas-fouquet) the same letter is dated "21 janvier 1673" and sourced "Ravaisson, Archives de la Bastille, Tome 3, p 123, 1880".
- Site commentary (opinion): after six years of harsh confinement Fouquet tries "le tout pour le tout" by offering the King a secret in exchange for his release.

### 2.2 — February and March 1673, Saint-Mars to Louvois (two extracts)
- URL: /ressources/lettres-de-fevrier-et-mars-1673/
- Reference given: "(Archives de la Bastille – recueillies par François Ravaisson)". No facsimile.
- Transcription (site):

Saint-Mars à Louvois – février 1673
« (…) Pour M. Fouquet, il se porte maintenant assez bien. Il me demande souvent si je n’ai pas reçu de réponse de vous, de ce que je vous ai mandé touchant lui. Il me dit toujours que ce sont des choses de si grande importance que je serais blâmé un jour de ne pas vous en avoir mandé l’importance. De la manière que je I ‘écoute quand il me parle de cela et les réponses que je lui fais la dessus, lui font croire que je ne me donne pas l’honneur de vous rendre compte de tout ce qu’il me dit. Il m’assure fort que vous serez, Monseigneur, très aise de savoir les avis qu’il a à vous donner, et qui sont de très grande conséquence pour le bien du service du Roi, et très glorieux pour vous. »

Saint-Mars à Louvois – mars 1673
« M. Fouquet se dit toujours avoir de grandes pensées pour votre gloire, et pour ce que j’ai eu l’honneur de vous mander par le courrier que je vous ai envoyé à sa persuasion, je crains fort Monseigneur que vous ne l’ayez pas approuvé, mais je ne l’ai fait que sur ce qu’il m’a dit qu’il n’y allait pas moins que du bien de l’Etat. Si j’ai fait quelque faute je supplie très humblement de me le pardonner, puisque je n’en ai pas eu l’intention. »

- What it establishes: Fouquet pressed Saint-Mars in February and March 1673 for Louvois's answer, and Saint-Mars sent a courier at Fouquet's urging.
- Site commentary (opinion): Louvois then ordered paper and ink to be given to Fouquet, who wrote two memoirs sent by extraordinary courier; the 29 March letter is the answer.

### 2.3 — 29 March 1673, Louvois to Saint-Mars
- URL: /ressources/lettre-du-29-mars-1673/
- Reference given: "Archives Nationales K120 N°132". Facsimile: images/1673_03_29.jpg (caption "Archives Nationales K120 N°132").
- Transcription (site), line breaks as on the site:

A St-Germain ce 29 mars 1673
J’ay receu vtre lettre du 15 de ce mois, et
j ay leu fort exactement les papiers escrits
de la main de Mo,s. foucquet, apres
avoir considéré qu’yl ny marquoit pas
ce quyl dit estre si important au service
du Roy, ce qui pourroit luy procurer
quelque soulagement dans sa peine,
je n’ay pas jugé a propos de presenter
mémoire(s) a sa Ma té. vous le luy
direz, et aussi t0St que vous luy en
aurez fait voir quelques feuilles
vous les jetterez au feu en sa presence
M Louvois

- My reading of the facsimile (for the doubtful words only): the manuscript has "presenter ses memoires a sa ma.té" and "et qui pourroit luy procurer"; the site's "mémoire(s)" and "ce qui pourroit" are its own readings. The conclusion page quotes the same letter as "présenter son mémoire".
- What it establishes: Louvois read Fouquet's papers, did not submit them to the King, and ordered Saint-Mars to show Fouquet some leaves and burn them in his presence.
- Site commentary (opinion): Louvois, "maître après Dieu (ou le Diable) du donjon", is determined that Fouquet will not leave Pignerol alive.

### 2.4 — 18 December 1675, Saint-Mars to Louvois (extract)
- URL: /ressources/lettre-du-18-decembre-1675/
- Reference given: "Archives de la Bastille – recueillies par François Ravaisson". No facsimile.
- Transcription (site):

« Je vous avouerai, Monseigneur, que M. Fouquet m ‘a pris par mon faible, en me faisant entendre les grands services qu’il pouvait rendre au Roi et à vous, s’il avait la liberté de pouvoir Mme sa femme, ou quelqu’un de ces deux messieurs que je me suis donné l’honneur de vous mander. Mais puisque S M ne désire point se servir de ces expédients, cela finira puisque je leur ai dit une fois pour toutes, que je n’oserais entretenir de telles choses sans votre permission.
(…)
Si je suis assez heureux pour que ma conduite vous agrée, je continuerai toute ma vie volontiers, pourvu que vous me fassiez la grâce de me faire entendre que mes petits services ne vous désagréeront point dans ce poste ici. Car pour le service du roi seulement je ne fais point de doute que tout autre que moi ne fit encore mieux que je n’ai fait depuis quatorze années que je fais ce métier ici, tant sous défunt M. d’Artagnan qu’ici où je suis depuis onze années. Comme ce temps-là m’a empêché d’avancer dans les armées, ainsi qu’a fait tout ce qui était moins en passe que moi, je vous demande en grâce Monseigneur, de me donner quelque honneur ou la permission de me faire casser la tête aux armées, où j’ai toujours servi depuis l’âge de douze ans. Je ne demande ni de biens ni de revenus mais seulement un peu d’honneur, où que vous me disiez que mes services vous agréent ici. En ce cas je ne vous demanderai jamais de ma vie de sortir d’ici, ni aucune autre chose, et je m’estimerai trop heureux de me sacrifier de toute manière pour vous plaire et de pouvoir me dire votre créature très respectueuses et très soumise; »

- The commentary also quotes Louvois's reply "du 3 décembre 1675" (source "(Source Gallica – BNF)"): « J’ai reçu avec votre lettre du 23 du mois passé, les papiers qui y étaient joints. J’ai lu ce qui était écrit dans le billet séparé de votre lettre. Ce qu’il contient n’est pas une chose qui mérite de réponse le Roi ne désirant point se servir des expédients qui y sont marqués. Vous pouvez néanmoins dire à celui qui vous a parlé que vous n’osez m’écrire de pareilles choses, cependant je vous prie de ne pas laisser de m’avertir de tout ce qu’il vous dira. »
- What it establishes: in November-December 1675 Saint-Mars relayed Fouquet's renewed offer (a visit from Mme Fouquet or a trusted person), the King declined, and Saint-Mars asked Louvois for some honour or a return to the army.
- Site commentary (opinion): Saint-Mars was humiliated by the reply and vexed.

### 2.5 — 18 August 1679, Louvois to Saint-Mars
- URL: /ressources/lettre-du-18-aout-1679/
- Reference given: "Archives Nationales K120 N°275". Facsimile: images/1679_08_18.jpg.
- Transcription (site), line breaks as on the site:

ARCHIVES NATIONALES
K120 N0275
A St Germain ce 18 août
1679
J’ay receu vostre lettre du 9 de ce mois,
Puisque vous avez quelque chose à me
Faire sçavoir que vous ne pouvez pas confier
a une lettre, vous pouvez envoyer icy le sr
de Blainvilliers pour m’en rendre
compte.
Lorsque Mad.e Foucquet et Mr le Comte
de Vaux retourneront à Pignerol, Sa Ma té
trouve bon que vous leur laissiez la liberté
de voir Mons. Foucquet comme auparavant
M LOUVOIS

- What it establishes: on 9 August 1679 Saint-Mars had something he would not put in a letter; Louvois authorised him to send Blainvilliers to report orally; Mme Fouquet and the comte de Vaux were to keep their access to Fouquet.
- Site commentary (opinion): an event of unknown nature occurred in August 1679; Blainvilliers returned in January with a 15,000-livre gratification for Saint-Mars.

### 2.6 — 13 September 1679, Louvois to Saint-Mars
- URL: /ressources/lettre-du-13-septembre-1679/
- Reference given: "Archives Nationales K120 N°277". Facsimile: images/1679_09_13.jpg. The image carries a caption added by the site: "Lettre de Louvois du 19 septembre 1679 / « Cependant je vous prie de me mander des nouvelles de la santé d'Eustache Dangers »"; the thesis page also calls it "Lettre de Louvois à Saint-Mars du 19 septembre 1679". The manuscript header reads "A Paris ce 13e Septembre 1679" (my reading of the facsimile agrees with the page title, 13).
- Transcription (site), line breaks as on the site:

ARCHIVES NATIONALES
K120 N0277
A Paris le 13E Septembre
1679
Vostre lettre du 2E de ce mois m’a esté
Rendue par le Sr de Blainvilliers avec
celles qui y estoient jointes que Messrs
foucquet et de Lauzun vous ont remises
j’auray soin de les faire tenoir à leurs
adresses, et de vous en envoyer les
responses ; cependant je vous prie
de me mander des nouvelles de la
senté d Eustache dangers ; et de
ce qui se passera parmy vos
prisonniers
M LOUVOIS
Je vous priue de faire tenir à mr le marquis
De Pianesse la lettre cy jointe

- My reading of the facsimile: "santé d'Eustache Dangers" — the final s is visible; the name is written as one word after the elided "d'", not "d'Angers".
- What it establishes: Louvois asked for news of Eustache Danger's health in September 1679, after Blainvilliers's oral report.
- Site commentary (opinion): Danger had suffered a serious health problem; the author says he searched the Archives nationales in vain for Saint-Mars's answer and found instead the 12 March 1680 letter.

### 2.7 — 27 January 1680, Lauzun to Louvois (extract)
- URL: /ressources/lettre-du-27-janvier-1680/
- Reference given: "(Archives de la Bastille – recueillies par François Ravaisson)". No facsimile. The page les-secrets-de-nicolas-fouquet quotes the same letter as "Une lettre de Lauzun à Louvois du 26 janvier 1680" with slightly different wording.
- Transcription (site):

« Le 27 janvier 1680. Je vous proteste que je n’ai pas plus d’impatience de sortir de prison que je n’en ai que vous soyez promptement informé ce que j’ai à vous faire savoir mais il faut de nécessité que ce soit de bouche et que vous seul en soyez informé, sans que personne en puisse avoir connaissance. Il est de votre intérêt que cela se passe de la sorte ; (…) Je vous demande seulement que je puisse vous faire parler sans qu’on le puisse savoir par quelque personne en qui je prenne entière confiance. J’en aurai bien à ma soeur de Nogent et à mon frère le chevalier mais il me faut singulièrement Barail, lui seul le peut bien faire et il vous est important que ce soit lui, et je vous prie, monsieur, de vous y comporter avec affection et de vous faire une affaire de me l’envoyer car cela vous est de toute manière d’une conséquence au dessus de tout ce que vous avez pu imaginer. Je ne puis m’expliquer d’avantage et j’attends avec la dernière impatience que vous m’en donniez les moyens et que par là je me trouve en état de recevoir les marques de votre amitié. »

- What it establishes: in late January 1680 Lauzun asked Louvois to send Barail so that he could communicate something orally that concerned Louvois's own interest.
- Site commentary (opinion): after a quarrel with Fouquet over Fouquet's daughter, Lauzun denounced the secret passage and dangled Fouquet's "grand secret" before Louvois.

### 2.8 — 12 March 1680, Louvois to Saint-Mars
- URL: /ressources/lettre-du-12-mars-1680/
- Reference given: "Archives Nationales K120 N°299". Facsimile: images/1680_03_12.jpg.
- Transcription (site, ressources page), line breaks as on the site; the garbled characters are the site's:

A Soissons ce 12 e mars 1680
J’ay receu vostœ lettre du 24 du
mois passé avec le mémoll?
qui y estoit joint escrlt de vostœ
main du contenu auquel je vous
prie de ne point dire a mr de
Lauzun que vous m ‘ayez fait
part,
L’intention du Roy n ‘est point
que vous payez a mons.r foucquet
les gages de celuy de ses vallets
qui est mort
M LOUVOIS

- Second transcription of the same letter on the page la-these-nicolas-fouquet:

« A Soissons ce 12e mars 1680
J’ay receu vostre lettre du 24e du
mois passé avec le memoire
qui y estoit escrit de vostre
main du contenu auquel je vous
prie de ne point dire a Mr de
Lauzun que vous m’ayez fait
part,
L’intention du Roy n’est point
que vous payez a mons. foucquet
les gages de celuy de ses vallets
qui est mort,
M Louvois »

- My reading of the facsimile: "avec le memoire qui y estoit joint escrit de vostre main du contenu auquel … que vous payiz a mons.r foucquet les gages de celuy de ses valletz qui est mort". The word "joint" is in the manuscript (the thesis-page version drops it).
- What it establishes: on 12 March 1680 the King refused to pay Fouquet the wages of "that one of his valets who is dead"; one of Fouquet's valets had died before 24 February 1680.
- Site commentary (opinion): the letter "est la condamnation de la thèse Eustache Danger-masque de fer", because it proves there could not have been two living valets on 8 April 1680; the author says he gave a copy to Stéphane Bern's staff before the 2008 broadcast.

### 2.9 — 8 April 1680, Louvois to Saint-Mars (five pages)
- URL: /ressources/lettre-du-8-avril-1680/
- Reference given: "Archives Nationales K120 n°302 – p1" … "– p5". Facsimiles: images/1680_04_08_p1.jpg to p5.jpg. The site's images of p. 1 show, in the margin, "8 Avril 1680", "K.120 n° 302" and the header "A St Germain en laye le 8e Avril 1680".
- Transcription (site), page by page, exactly as on the site (its "(sic)", "./." and typing errors included):

Page 1 (Archives Nationales K120 n°302 – p1)
A St Germain en laye le 8 avril 1680

Le Roi a appris par la lettre que vous m’avez escrite le 23e du mois passé, la mort de Monsieur Fouquet, et le jugement que vous faite que Monsieur de Lauzun sait la plupart des choses importantes dont Monsieur Fouquet avait connaissance, et que le nommé la Rivière ne les ignore pas ./. Surquoy Sa Majesté m’a commandé de vous faire savoir qu’après que vous aurez fait reboucher le trou par lequel Mess Fouquet et de Lauzun ont communiqué a votre insu , et cela retabli si solidement qu’on ne puisse plus travailler en cet endroit, et que vous aurez aussi fait défaire le degré qui communique de la chambre de feu Mons Fouquet a celle que vous aviez fait accommoder pour Melle sa fille, I’Intention de Sa Majesté est que vous logiez Monsieur de Lauzun dans la chambre de feu Mons. Fouquet, et fassiez de si fréquentes visites dans la dite chambre, même en en faisant remuer tous les meubles, que Monsieur de Lauzun ne puisse point faire travailler en aucun endroit de son logement que vous ne vous en aperceviez ./.

Que vous persuadiez a Monsieur de Lauzun que les nommés Eustache d’Angers (sic), et ledit la Rivière, ont été mis en liberté, et que vous en parliez de mesme

Page 2 (Archives Nationales K120 n°302 – p2)
« à tous ceux qui pourraient vous en demander des nouvelles, que cependant vous les renfermiez tous deux dans une chambre ou vous puissiez répondre a Sa maj qu’ils n’auront communication avec qui que ce soit de vive voix ni par escrit et que Monsieur de Lauzun ne pourra point s’apercevoir qu’ils y sont renfermés ./.

Vous avez eu tort de souffrir que Monsieur de Vaux ait emporté les papiers et les vers de Monsieur son père et vous deviez faire enfermer cela dans son appartement pour en être usé ainsi que Sa Majesté en ordonnerait ./.

Vous pouvez disposer des meubles appartenant à Sa Majesté et qui ont servi à Monsieur Fouquet comme vous I’estimerez a propos ./.

Lorsque Sa Majesté envoya Monsieur de Lauzun a Pignerol elle fit un fond nouveau pour son entretiennement, vous trouverez cy joint I’estat de celuy qui sera fait a l’advenir tant pour la subsistance, que pour I’entretlennement de votre compagnie.

A l esgard des autres prisonniers dont vous estes 4chargé, Sa Majesté vous en fera payer la subsistance a raison de quatre livres pour chacun par jour, et en m’en envoyant un estat tous les trois mois je prendrai les ordres de Sa Majesté pour pourvoir »

Page 3 (Archives Nationales K120 n°302 – p3)
« à votre remboursement sur ce pied-la Le Roi a permis à Monsieur le Chancelier de Lauzun d’aller demeurer quelque temps auprès de Monsieur son frère, Sa Majesté ne veut point que vous le laissiez entrer armé dans le Donjon, ny que vous souffriez qu’il y mange ; et pour vous expliquer plus particulièrement la conduite que vous devez tenir a cet égard, je vous dirai que vous pouvez permettre qu’il entre dans l’appartement de Monsieur son frère les matins a huit heures, a condition d’en sortir à onze avant midi ; l’y laisser rentrer a deux heures après midi, a condition aussi d’en sortir a six heures du soir en hiver, et a sept en été, que tant qu’ils voudront demeurer seuls ensemble dans son appartement vous pouvez les y laisser mais que s’il désire se promener dans les lieux qui lui sont pemiss par les précédents ordres de Sa Maj , vous ne devez pas souffrir qu’il sorte sans que vous y soyez, ou deux de vos Lieutenants, vous faisant et eux aussi accompagner si bien qu’il ne puisse rien entreprendre pour se sauver. Et comme Mons. le chancelier de Lauzun »

Page 4 (Archives Nationales K120 n°302 – p4)
« pourrait porter a son frère soit des armes, soit des Instruments propres a lui donner lieu de se sauver, ou d’avoir des communications que vous ne connaîtriez point, il sera de vos soins et de votre vigilance de faire pendant les promenades que fera Monsieur de Lauzun et même pendant la nuit de temps en temps, de telles visites, qu’il ne puisse rien cacher dans sa chambre dont vous n’ayez connaissance ny entreprendre sur les murailles, grilles, ou portes de ses appartements, que vous ne vous en aperceviez. Au reste vous devez être persuadé que Sa Majesté vous donnera des marques de la satisfaction quelle a de vos services, dans les occasions qui se pourront présenter, de quoi je prendrai soin de le faire souvent avec beaucoup de plaisir.

J’ajoute ce mot pour vous dire que vous ne devez entrer en aucun discours, ni confidence, avec Monsieur de Lauzun, sur ce qu’il peut avoir »

Page 5 (Archives Nationales K120 n°302 – p5)
« appris de Monsieur Fouquet, et plus vous le trouverez souple et complaisant pour vous, plus vous devrez renouveler vos soins pour sa garde, parce que homme au monde n’est plus capable de dissimulation que lui.

M. Louvois »

- A second, older-spelling version of the key sentence is given on the page la-these-eustache-danger: « Que vous persuadiez à Mons. de Lauzun que les nommés Eustache d’Angers, et ledit la Rivière, ont esté mis en liberté, et que vous en parliez de mesme à tous ceux qui pourroient vous en demander des nouvelles que cependant que vous les renfermiez tous deux dans une chambre ou vous pourriez respondre à Sa Majesté qu’ils n’auront de communication avec qui que ce soit de vive voix ny par escrit et que Mons. de Lauzun ne pourra point s’apercevoir qu’yls y sont renfermés. ./. » A third, shortened version is on the page le-8-avril-1680.
- My reading of the facsimile of p. 1, last lines: "Que vous persuadiez a Mons.r de Lauzun que les nommez Eustache d'Angers, et led. la Riviere, ont esté mis en liberté, et que vous en parliez de mesme". "d'Angers" is unambiguous in the manuscript; the site's "(sic)" marks this spelling.
- What it establishes: the King had been told of Fouquet's death by Saint-Mars's letter of 23 March 1680; Lauzun was to be made to believe that Eustache d'Angers and La Rivière had been freed while both were shut up incommunicado; the rest of the letter concerns Lauzun's brother, the furniture, the subsistence money and Lauzun's guard.
- Site commentary (opinion): the letter is "en quelque sorte l'acte de décès de Fouquet et l'acte de naissance de l'homme au Masque de fer"; the author finds it strange that a man who had died a month earlier (his reading of 12 March 1680) is ordered to be locked up, and that Danger is not named in the first paragraph although Lauzun and La Rivière are.

### 2.10 — 12 May 1681, Louvois to Saint-Mars
- URL: /ressources/lettre-du-12-mai-1681/
- Reference given: "(Service Historique de l’Armée de Terre (Vincennes) – série A1 Vol.654 p.232)". No facsimile.
- Transcription (site):

« J’ai lu votre lettre du 3 de ce mois, par laquelle Sa Majesté ayant connu l’extrême répugnance que vous avez à accepter le commandement de la citadelle de Pignerol, a trouvé bon de vous accorder le gouvernement d’Exiles, vacant par la mort de Monsieur le duc de Lesdiguières, où elle fera transporter ceux des prisonniers qui sont à votre garde, qu’elle croira assez de conséquence pour ne pas les mettre en d’autres mains que les vôtres.
Je demande au sieur du Chaunoy d’aller visiter avec vous les bâtiments d’Exilles et d’y faire un mémoire des réparations absolument nécessaires pour le logement des deux prisonniers de la tour d’en bas qui sont je crois les seuls que Sa Majesté fera transporter à Exilles. Envoyez-moi un mémoire de tous les prisonniers dont vous êtes chargé et marquez-moi à côté ce que vous savez des raisons pour lesquelles ils sont arrêtés. A l’égard des deux de la tour d’en bas vous n’avez qu’à les marquer de ce nom, sans y mettre autre chose.
Le roi s’attend que, pendant le peu de temps que vous serez absent de la citadelle de Pignerol pour aller avec le sieur du Chaunoy à Exilles, vous mettiez un tel ordre à la garde de vos prisonniers qu’il n’en puisse mésarriver d’aucun, et qu’ils n’auront pas plus de commerce avec qui que ce soit qu’ils n’en ont eu depuis que vous en êtes chargé. »

- What it establishes: Saint-Mars was given Exilles, and the two prisoners "de la tour d'en bas" were expected to be the only ones transferred there; Louvois did not want their names written in the list of prisoners.
- Site commentary (opinion): Saint-Mars's morale had collapsed under the burden of feeding two hidden prisoners himself; Exilles was Louvois's solution.

### 2.11 — 2 March 1682, Louvois to Saint-Mars
- URL: /ressources/lettre-du-2-mars-1682/
- Reference given: "(Service Historique de l’Armée de Terre (Vincennes) – Série A1, vol.675 p.36)". No facsimile.
- Transcription (site):

« Comme il est important d’empêcher que les prisonniers qui sont à Exiles, que l’on nommait à Pignerol de la tour d’en bas n’aient aucun commerce, le Roi m’a ordonné de vous commander de les faire garder si sévèrement et de prendre de telles précautions que vous puissiez répondre à Sa Majesté qu’ils ne parleront à qui que ce soit, non seulement de dehors, mais même de la garnison d’Exiles ; je vous prie de me mander de temps en temps ce qui se passe à leur égard.
MLOUVOIS »

- The commentary also quotes, without reference, Saint-Mars to the abbé d'Estrades (« J’ai tous les ordres pour m’en aller dans cet exil-là … avec toute ma famille et les ours … ») and Louvois's reply to Saint-Mars's request of 28 December 1681 to go to Casal (« Vous ne savez ce qui vous est bon, quand vous demandez à changer le gouvernement d’Exilles contre le commandement du château de Casal qui ne vaudra que deux mille livres d’appointements. Ainsi je ne vous conseille pas d’y songer. »).
- What it establishes: the Exilles prisoners were the same men called at Pignerol "de la tour d'en bas", and they were to speak to nobody, garrison included.

### 2.12 — 11 March 1682, Saint-Mars to Louvois
- URL: /ressources/lettre-du-11-mars-1682/
- Reference given: "(Service Historique de l’Armée de Terre (Vincennes) – Série A1, vol.686, p.216)". No facsimile. The "(1)" and "(2)" and the two notes are the site's.
- Transcription (site):

« Vous me mandez, Monseigneur, qu’il est important que mes deux prisonniers n’aient aucun commerce. Depuis le commencement que Monseigneur m’a fait ce commandement-là j’al gardé ces deux prisonniers qui sont à ma garde aussi sévèrement et exactement que j’ai fait autrefois Fouquet et Lauzun, lequel ne se peut pas se vanter d’avoir donné ni reçu des nouvelles tant qu’il a été enfermé(1).
Ceux-ci peuvent entendre parler Ie monde qui passe au chemin qui est au bas de la tour où ils sont, mais eux, quand ils le voudraient, ne sauraient se faire entendre ; ils peuvent voir les personnes qui seraient sur la montagne qui est devant leurs fenêtres mais on ne saurait les voir à cause des grilles qui sont au devant de leurs chambres(2). J’ai deux sentinelles de ma compagnie nuit et jour, des deux côtés de la tour, d’une distance raisonnable, qui voient obliquement la fenêtre des prisonniers ; il leur est consigné d’entendre si personne ne leur parle et s’ils ne crient point par les fenêtres et de faire marcher les passants qui s’arrêteraient dans le chemin ou sur le penchant de la montagne. Ma chambre étant jointe à la tour, qui n’a d’autre vue que du côté de ce chemin, fait que j’entends et vois tout, et même mes deux sentinelles qui sont toujours alertes par ce moyen-là.
Pour le dedans de la tour, je l’ai fait réparer d’une manière où le prêtre qui leur dit la messe ne les peut voir à cause d’un tambour que j’ai fait mettre qui couvre leurs doubles-portes. Les domestiques qui leur portent à manger mettent ce qui est de besoin aux prisonniers sur une table qui est là et mon lieutenant le prend et le porte. Personne ne leur parle que moi, mon officier, M. Vignon le confesseur et un médecin qui est de Pragelas à six lieues d’ici, et en ma présence. Pour leur linge et autres nécessités, mêmes précautions que je faisais jadis pour mes prisonniers du passé. »
(1) Saint-Mars omet d’évoquer les rencontres clandestines entre Lauzun et Fouquet
(2) II apparait ici que chacun des prisonniers avait sa chambre.

- What it establishes: the guard arrangements at Exilles in March 1682 — two sentries, grilles, a "tambour" screening the double doors so that the priest saying mass could not see the prisoners, food passed through the lieutenant, and only Saint-Mars, his officer, the confessor Vignon and a doctor from Pragelas allowed to speak to them.
- Site commentary (opinion): the "tambour" (defined from the 1694 Académie dictionary) created a space from which priest or doctor could be heard without seeing; the author infers that a mask was imposed when anyone had to enter; he quotes Petitfils on the treasury entries "Messieurs de la tour d'en bas et un valet", "La tour d'enbas et un valet", "La tour d'aubas et son valet" and concludes "Un seul valet à chaque fois."

### 2.13 — 18 April 1687, the abbé Mauvans to Henri de Soubiran
- URL: /ressources/lettre-du-18-avril-1687/
- Reference given (image caption): "Extrait du Voyage à Gènes, campagne maritime d’avril 1687 (p.314)- Médiathèque de Nîmes – Secteur des documents anciens". The page contains NO transcription: the document is only the image images/1687_04_18.jpg (a manuscript page, twelve lines).
- My reading of the facsimile (labelled as mine; the right margin is cut, doubtful letters in square brackets):

On va faire de nouvelles fortifications a cette place nous en vimes tous les appre[ts] & on y mettra la main a l arrivée de M de St Marc, qui estoit party de la depuis quelque tams pour aller écorter ce prisonier inconu, que l on conduit avec tant de precaution, & auquel on a fait savoir [word struck out] a bonne heure que lorsqu il seroit ennuyé de la vie, il n avoit qu a dire son nom parce qu on avoit ordre de luy donner aussy tost un coup de pistolet dans la teste. On nous dit qu on alloit disposer un logemant pour ce prisonnier qui repondroit a celuy de M le Gouverneur, qu il n y auroit que luy qui le vit, qu il luy donneroit luy meme a manger, & qu il seroit presque son unique geolier & son garde.

- The only other text of this passage in the project is the Cannes médiathèque page (sources/cannes_mediatheque_masque_de_fer_star_cannoise.txt), which modernises it: « M. de St Marc [sic] est parti de là depuis quelque temps pour aller escorter ce prisonnier inconnu que l’on conduit avec tant de précautions, et auquel on a fait savoir de bonne heure que lorsqu’il serait ennuyé de la vie, il n’avait qu’à dire son nom parce qu’on avait ordre de lui donner aussitôt un coup de pistolet dans la tête. » and dates the visit "le 18 avril 1687". The site's commentary dates the landing on the island 17 April 1687 and the letter 18 April.
- What it establishes: before the prisoner arrived, an officer of the Sainte-Marguerite garrison told visitors that Saint-Mars had gone to escort an unknown prisoner who would be shot if he said his name, and that a lodging next to the governor's was being prepared for him.
- Site commentary (opinion): Saint-Mars's "propos stupéfiants" were reported by the abbé Mauvans, secretary of the expedition, in his travel journal.

### 2.14 — 4 September 1687, Nouvelles ecclésiastiques (Mgr Louis Fouquet, bishop of Agde)
- URL: /ressources/gazette-du-4-septembre-1687/
- Reference given: "Bibliothèque Ste Geneviève Paris – Réserve, Mss, vol.1477, folio 396 verso". Facsimile: images/1687_09_04.jpg (the right margin of the page is cut in the image, which is why the site prints conjectures in parentheses). The thesis page gives the reference as "(Réf. M.1427, folio 396)".
- Transcription (site):

« M. de cinq mars a transporté par ordre du Roy un prisonnier d’état de pignerol aux iles de Ste marguerite personne ne sait qui il est il y a défense de dire son nom et ordre de le (tuer) s’il l’avoit prononcé on en a conduit d’autres (à) Pignerol, et celuy sans doute de la sorte il y eut un homme qui s’y tua, celuy cy etoit enfermé dans une chaise à porteurs ayant un masque d’acier sur le visage et tout ce qu’on a pu savoir de cinq mars est que ce prisonnier etoit depuis de longues années a pignerol et que tous les gens que le public croit morts ne le sont pas »

- The thesis page quotes it in a shortened, modernised form: « M. de Saint-Mars a transporté un prisonnier d’État de Pignerol aux Iles Sainte-Marguerite. (…) Personne ne sait qui il est. (…) Il était enfermé dans une chaise à porteurs ayant un Masque d’acier sur le visage. (…) Tout ce qu’on a pu savoir de Saint-Mars et que son prisonnier était depuis de longues années à Pignerol et qu’il y a des gens que le public croit mort et qui ne le sont pas. »
- My reading of the facsimile: the visible text agrees with the site's; "masqu[e] / d'acier sur le visage" is clearly legible across the line break; the words "tuer", "à", "sa[voir]", "de[puis]", "g[ens]" fall in the cut margin.
- What it establishes: a manuscript newsletter of September 1687 reported that the prisoner moved by Saint-Mars from Pignerol to Sainte-Marguerite travelled in a sedan chair with a steel mask, that saying his name was forbidden on pain of death, and that Saint-Mars said he had been many years at Pignerol and that "people the public believes dead are not".
- Site commentary (opinion): the bishop, a Jansenist under surveillance at Issoudun, circulated the gazette "sous le manteau".

### 2.15 — Documents quoted on the "Enquête" pages (not transcribed in full; the site's references as given)

| Document | Site's quoted text (verbatim) | Site's source line |
|---|---|---|
| 19 July 1669, Louvois to Saint-Mars (les-protagonistes) | « Le roi m’ayant commandé de faire conduire à Pignerol le nommé Eustache, je vous prie de faire accommoder un cachot ou le mettre surement. Il faudra que vous portiez vous-même à ce misérable, une fois par jour, de quoi vivre toute la journée et que vous n’écoutiez jamais, sous aucun prétexte, ce qu’il voudra vous dire, le menaçant toujours de le faire mourir s’il vous ouvre la bouche pour vous parler d’autre chose que de ses nécessités. Comme ce n’est qu’un valet, il ne lui faudra pas de meubles bien considérables. » | none |
| 1669, Saint-Mars to Louvois (same page) | « Monsieur de Vauroy a remis entre mes mains Eustache Danger. Aussitôt que je l’eus mis en un lieu fort sûr, je lui dis que s’il me parlait d’autre chose que de ses nécessités, je lui mettrai mon épée dans le ventre. » | none |
| 1671, Saint-Mars on Lauzun's lodging | « Je le logerai dans les deux chambres basses qui sont au-dessous de M. Fouquet » | none |
| January 1680, Lauzun to Louvois (pignerol-de-1666-a-1680) | « Je souhaite autant être libéré que de vous informer de choses qu’il ne m’est impossible de confier par écrit. Vous n’avez jamais eu de meilleur serviteur que moi relativement à vos intérêts et à votre fortune. (…) Cela est au dessus de tout ce que vous pouvez imaginer. » | none (a third wording of the 26/27 January 1680 letter) |
| 6 February 1680, Louvois to Fouquet (comment by the author, /presentation/) | « Monsieur, j’ai appris avec bien du déplaisir la mort de Monsieur votre frère, je vous supplie d’être persuadé que je prends toute la part que je dois à la douleur que cette nouvelle vous a donnée. » | none |
| 8 and 9 April 1680, Louvois (la-these-nicolas-fouquet) | a second letter of 8 April authorising the comte de Vaux to take the body; one of 9 April authorising Saint-Mars to hand the body « aux gens de la famille Fouquet »; a bill for « le paiement des médecins et chirurgiens qui ont traité le sieur Fouquet pendant l’année 1680 et pendant la maladie dont il est mort, les remèdes et des vêtements pour les funérailles du sieur Fouquet »; Visitation register « Le 28 mars 1681, fut inhumé dans notre église messire Nicolas Fouquet » | none |
| 20 January 1687, Saint-Mars to Louvois | « La plus sûre voiture serait une chaise couverte de toile cirée de manière que personne le pût voir ni lui parler pendant la route, pas même les soldats que je choisirai pour être proches de la chaise (…) On installera près de sa cellule une chapelle pour qu’il puisse entendre la messe sans être aperçu ». Longer form on la-these-eustache-danger: « Si je mène aux îles je crois que la plus sûre voiture serait une chaise couverte de toile cirée de manière qu’il aurait assez d’air sans que personne le pût voir, ni lui parler pendant la route, pas même les soldats que je choisirai pour être proche de la chaise. » | "Joseph Delort, L’homme au masque de fer, 1838, pages 283-284" |
| 23 March 1687, Saint-Mars to Louvois | « Je vous promets de conduire ici mon prisonnier sans que personne ne le voie ni ne lui puisse parler (…) Je ne lui ferai point entendre la messe depuis son départ d’Exilles jusqu’à ce qu’il soit logé dans la prison où il y aura joignant une chapelle Je vous réponds sur mon honneur de sa sûreté entière » | "Archives de l’Armée de Terre, v 792, p.16" |
| 3 May 1687, Saint-Mars to Louvois | « Je puis vous assurer, Monseigneur, que personne au monde ne l’a vu » | "Roux-Fazillac, Recherches historiques et critiques sur l’homme au masque de fer, [1800], p.116" |
| January 1688, Saint-Mars to Louvois | « J’ai mis le prisonnier dans l’une des deux nouvelles prisons que j’ai fait faire suivant vos ordres. Elles sont grandes, belles et claires, et pour leur bonté je ne crois pas qu’il y en ait de plus fortes et de plus assurées dans l’Europe. » | "Champollion-Figeac, Documents historiques inédits, Paris, 1847, Tome3, p.645" |
| 1691, Barbezieux to Saint-Mars | « Lorsque vous aurez quelque chose à me mander du prisonnier qui est sous votre garde depuis vingt ans, je vous prie d’user des mêmes précautions que vous faisiez avec M. de Louvois. » | none |
| 20 March 1694, Barbezieux to Saint-Mars | « Comme vous savez que les prisonniers qui arrivent sont, au moins l’un, de plus de conséquence que ceux qui sont présentement sur l’île, vous les mettrez dans les prisons les plus sûres. » | none |
| 18 September 1698 and 19 November 1703, Du Junca's registers; Saint-Paul burial register | « Du jeudi 18 de septembre à trois heures de l’après-midi Monsieur de Saint-Mars, gouverneur du château de la Bastille, est arrivé pour sa première entrée venant de son gouvernement des Iles Sainte-Marguerite et Honorat, ayant avec lui dans sa litière un ancien prisonnier qu’il avait à Pignerol lequel il fait tenir toujours masqué dont le nom ne se dit pas … » ; « Du même jour lundi 19 de novembre 1703 : le prisonnier inconnu toujours masqué d’un masque de velours noir, que Monsieur de Saint-Mars gouverneur gardait depuis longtemps, lequel s’étant trouvé hier un peu mal en sortant de la messe il est mort ce jour d’hui vers les dix heures du soir. Sans avoir eu une grande maladie. » ; « MARCHIALI » « 45 ans environ » | none (post masque-de-velours-et-masque-de-fer) |
| Later testimonies used for the "portrait-robot" | Saint-Foix (Essais historiques, 1777) on fine linen; Papon (Histoire de Provence, t. 4, 1780) on the shirt and the servant from Mougins; Lagrange-Chancel (Année littéraire, 1768) on silver plate; abbé Dubos to Voltaire, 3 December 1738 (Besterman, t. 89); Voltaire, Siècle de Louis XIV 1752 and Supplément 1753 (Chamillart "un homme qui avait tous les secrets de M. Fouquet"); Formanoir de Palteau, June 1768 ("La Tour") | as listed on la-these-nicolas-fouquet |
| Briançon consuls' accounts, 1687 (author's reply in the comments of /presentation/) | « Le 18 avril la compagnie de Saint-Mars ayant séjourné, 18 et 19 avril, avec 1 capitaine, 2 lieutenants, 2 sergents et 43 soldats, avons payé 362 rations tant pour les hommes que pour les chevaux » | "Article 83 des comptes des consuls de 1687, série EE156" |
| Louis Fouquet to Nicolas Fouquet, 17 April 1656; Fouquet's Défenses (1663) | Poussin passage (« des avantages que les rois auraient grand peine à tirer de lui … ») ; « Demeurons dans le silence et le respect, ne disons pas au public ce que je serais consolé si je pouvais avoir l’honneur de dire à Sa Majesté, en secret, comme le plus important de tous, et qu’il saura peut-être trop tard. » | "De Lépinois, Lettres de Louis Fouquet à son frère Nicolas, page 269 et suivantes"; "Nicolas Fouquet, Mémoires de Défense, 1663" |

---

## 3. The site's readings compared with the printed editions (1825-1913)

### 3.1 The prisoner's name

| Document | Site's reading | Facsimile (my reading) | Delort 1829 | Iung 1873 | Lair 1890 | Laloy 1913 | Topin 1883 / Funck-Brentano 1901 / Loiseleur 1882 |
|---|---|---|---|---|---|---|---|
| 13 Sept. 1679 (AN K120 n°277) | « senté d Eustache dangers » (page); "Eustache Dangers" (image caption) | "santé d'Eustache Dangers" (final s visible) | not printed | not found | not found | « des nouvelles de la santé d'Eustache Danger » (l. 4120-4123) | not found |
| 12 March 1680 (AN K120 n°299) | « celuy de ses vallets qui est mort » (no name) | "celuy de ses valletz qui est mort" | « les gages de celuy de ses valets qui est mort » (l. 12440-12442, letter headed "Soissons, ce 12 mars 1680") | not printed | not printed | not printed | not printed |
| 8 April 1680 (AN K120 n°302) | « Eustache d’Angers (sic), et ledit la Rivière » | "les nommez Eustache d'Angers, et led. la Riviere" | « les nommés Eustache d'Angers, et le dit la Rivière » (l. 12526-12527) | « le nommé Eustache Dauger et ledit La Rivière » (l. 9500-9503) | « les nommés Eustache Danger et ledit La Rivière » (l. 21521-21523) | « les nommés Eustache d' Angers et le dit La Rivière » (l. 4232-4234); second citation « les nommés Eustache d'Augers et La Rivière » (l. 4961-4962) | Topin and Funck-Brentano do not quote the sentence (Topin writes "Eustache d'Auger", l. 2795; Funck-Brentano "Dauger", l. 5457); Loiseleur not found |

Raw counts of spellings in each OCR file (case-insensitive except "Danger", which is case-sensitive to avoid "danger/dangereux"; running heads and indexes included): Iung Dauger 21, Danger 27, d'Angers 4; Lair Dauger 13, Danger 29, d'Auger 1, d'Angers 12; Laloy Dauger 55, Danger 35, d'Auger 5, d'Angers 1; Topin d'Auger 4, Danger 1; Funck-Brentano Dauger 4, Danger 3; Delort 1829 Danger 1, d'Auger 1, d'Angers 2; Loiseleur d'Auger 2, d'Angers 1; Delort 1825 none; Ravaisson vol. 7 d'Angers 26, vol. 8 d'Angers 8 and Dauger 1, vol. 9 d'Angers 32.

Result on the name: the two originals reproduced by the site read "Dangers" (1679) and "d'Angers" (1680). Delort 1829 and Laloy (first citation) print the 1680 form as in the manuscript; Iung normalised it to "Dauger" and Lair to "Danger"; Laloy's second citation ("d'Augers") is a variant of his own. The site's commentary uses "Danger" and states that the spelling fluctuates ("Dauger, Danger, Dangers, d'Angers").

### 3.2 Dates

| Document | Site | Printed editions |
|---|---|---|
| 14 Jan. 1673 | "14 janvier 1673" (page title); "21 janvier 1673" on les-secrets-de-nicolas-fouquet | Ravaisson t. III (l. 7062-7078): the letter follows one closing "A Pignerol, ce 1? janvier 1673" (OCR illegible) under "Le même au même"; Lair II quotes it (l. 20103-20109) |
| 29 March 1673 | "A St-Germain ce 29 mars 1673" | Delort 1829 "Saint-Germain, ce 29 mars 1673" (l. 8612-8626) |
| 3 Dec. 1675 (Louvois, in commentary) | "3 décembre 1675" | Ravaisson t. III "A Versailles, le 2 décembre 1675" (l. 8976); Saint-Mars's reply refers to "celle … du 2 du courant" (l. 8988) |
| 18 Aug. 1679 | "A St Germain ce 18 août 1679" | Delort 1829 prints the letter (l. 11839-11847), header not captured in the OCR excerpt |
| 13 Sept. 1679 | "A Paris le 13E Septembre 1679" (page); "19 septembre 1679" (image caption and thesis page) | Laloy "le 13 septembre" (l. 4120) |
| 27 Jan. 1680 | "27 janvier 1680" (page); "26 janvier 1680" (secrets page) | not located in the OCR of Ravaisson t. III or vol. 8 (searched "impatience de sortir", "singulièrement Barail", "de bouche") |
| 12 March 1680 | "A Soissons ce 12 e mars 1680" | Delort 1829 "Soissons, ce 12 mars 1680" (OCR "IX uiar» x68o", l. 12425) |
| 8 April 1680 | "A St Germain en laye le 8 avril 1680" (facsimile "8e Avril") | Delort 1829 "Saint-Germain en Laye, le 8 avril 1680" (l. 12495); Iung "le 8 avril 1680" (l. 9501); Laloy "lettre du 8 avril 1680" (l. 4960); Iung's footnote gives his source as "P. 524, V. 681. Mss. Dépôt de la guerre" (l. 9507), i.e. the War Depot copy, not AN K120 |
| 12 May 1681 | "votre lettre du 3 de ce mois"; letter of 12 May | Iung (l. 18700 "le 12"), Laloy (l. 4845), Loiseleur (l. 10265 "Au mois de mai 1681") agree |
| 2 March 1682 | 2 March 1682, "Série A1, vol.675 p.36" | Iung's footnote "p. 36, V. 675, Mss. Dépôt de la guerre" (l. 7989) is the same reference |
| 11 March 1682 | 11 March 1682 | Laloy "Saint-Mars à Louvois, 11 mars 1682" (l. 5118); Delort 1825 prints it with its opening "J'ai reçu celle qu'il vous a plû me faire l'honneur de m'écrire le 27 du passé" (l. 10205-10206), which the site omits |
| 18 April 1687 | letter of 18 April; landing on 17 April | not in any of the editions (no hit for Mauvans, Soubiran, Mazaugues, "Voyage à Gènes") |
| 4 Sept. 1687 | 4 September 1687 | not in any of the editions (see 3.7) |
| Arrival on Sainte-Marguerite | "30 avril 1687" (lile-sainte-marguerite, /presentation/ comments); "le 28 mars 1687" (un-blog-pour-debattre) — an internal inconsistency of the site | Iung l. 19280 (Saint-Mars: "le 30 du mois passé") |

### 3.3 "les deux prisonniers de la tour d'en bas" (12 May 1681)

- Site: « pour le logement des deux prisonniers de la tour d’en bas qui sont je crois les seuls que Sa Majesté fera transporter à Exilles. … A l’égard des deux de la tour d’en bas vous n’avez qu’à les marquer de ce nom, sans y mettre autre chose. »
- Iung (l. 3942-3946, p. 77, and l. 18710-18723, p. 397): « Je demande au sieur du Chaunoy d'aller visiter avec vous les bâtiments d'Exilés, et d'y faire un mémoire des réparations absolument nécessaires pour le logement des deux prisonniers de la Tour d'en bas, qui sont, je crois, les seuls que Sa Majesté fera transférer à Exiles. Envoyez-moi un mémoire de tous les prisonniers dont vous êtes chargé, et marquez-moi à côté ce que vous saurez des raisons pour lesquelles ils sont arrêtés. A l'égard des deux de la Tour d'en bas, vous n'avez qu'à les marquer de ce nom, sans y mettre autre chose. » (the p. 397 citation has "Je mande au sieur Duchaunoy" and "ce que vous saurez"; the p. 77 citation "Je demande au sieur du Chaunoy"). Iung opens the letter « J'ai lu au Roi votre lettre du 3 de ce mois ».
- Laloy (l. 4845-4875): same text as Iung p. 77 ("Je demande au sieur du Chaunoy", "transférer à Exiles", "ce que vous savez"), opening « lu au roi votre lettre du 3 de ce mois », and « ceux de vos prisonniers qui sont à votre garde ».
- Loiseleur (l. 10271-10285): « pour le logement des deux prisonniers de la tour d'en bas, qui, dit-il, sont, je crois, les seuls que Sa Majesté fera transférer à Exiles » and « A l'égard des deux de la tour d'en bas, vous n'aurez qu'à les marquer de ce nom, sans y mettre autre chose. »
- Topin (l. 12360-12363): quotes only « les deux prisonniers de la tour d'en bas » and holds them to be Matthioli and the Jacobin.
- Differences of reading: site "transporter à Exilles" against "transférer à Exiles" in Iung, Laloy and Loiseleur; site "J'ai lu votre lettre" against "J'ai lu au Roi votre lettre" (Iung, Laloy); "vous n'avez qu'à" (site, Iung, Laloy) against "vous n'aurez qu'à" (Loiseleur); "ce que vous savez" (site, Laloy, Iung p. 77) against "ce que vous saurez" (Iung p. 397). The phrase "les deux prisonniers de la tour d'en bas" itself is identical in all of them.

### 3.4 The 8 April 1680 sentence about Lauzun

- Site (ressources page, modernised): « Que vous persuadiez a Monsieur de Lauzun que les nommés Eustache d’Angers (sic), et ledit la Rivière, ont été mis en liberté, et que vous en parliez de mesme à tous ceux qui pourraient vous en demander des nouvelles, que cependant vous les renfermiez tous deux dans une chambre ou vous puissiez répondre a Sa maj qu’ils n’auront communication avec qui que ce soit de vive voix ni par escrit et que Monsieur de Lauzun ne pourra point s’apercevoir qu’ils y sont renfermés ./. »
- Site (thesis page, old spelling): see §2.9 ("ont esté mis en liberté … que cependant que vous les renfermiez … ou vous pourriez respondre … qu’ils n’auront de communication … qu’yls y sont renfermés").
- Delort 1829 (l. 12526-12535): « Que vous persuadiez à monsieur de Lauzun, que les nommés Eustache d'Angers, et le dit la Rivière, ont été mis en liberté, et que vous en parliez de mèsme à tous ceux qui pourroyent vous en demander des nouvelles; que cependant vous les renfermiez tous deux dans une chambre, ou vous puissiez réspondre à Sa Majesté qu'ils n'auront communication avec qui que ce soit, de vive voix, n'y par éscrit, et que monsieur de Lauzun ne pourra point s'apperçevoir qu'ils y sont renfermez. »
- Iung (l. 9500-9505): « Persuadez à Lauzun, dit Louvois à Saint-Mars, le 8 avril 1680, que le nommé Eustache Dauger et ledit La Rivière ont été mis en liberté ; il faut que vous en parliez de même à tous ceux qui pourraient vous en demander des nouvelles, que cependant vous les renfermiez tous deux dans une chambre » — Iung turns the subordinate clause into an imperative, writes "le nommé" in the singular, inserts "il faut que", and spells "Dauger".
- Lair (l. 21521-21530): « que vous persuadiez à M. de Lauzun que les nommés Eustache Danger et ledit La Rivière ont été mis en liberté et que vous en parliez de mesme à tous ceux qui pourroyent vous en demander des nouvelles: que, cependant, vous les renfermiez tous deux dans une chambre où vous puissiez respondre à Sa Majesté qu'ils n'auront communication avec qui que ce soit, de vive voix, ny par escrit, et que M. de Lauzun ne pourra point s'appercevoir qu'ils y sont renfermés ».
- Laloy (l. 4232-4241): « que vous persuadiez à M. de Lauzun que les nommés Eustache d' Angers et le dit La Rivière ont été mis en liberté, et que vous parliez de même à tous ceux qui pourraient vous en demander des nouvelles ; que cependant vous les renfermiez tous deux dans une chambre où vous puissiez répondre à Sa Majesté qu'ils n'auront aucune communication avec qui que ce soit, de vive voix ni par écrit, et que M. de Lauzun ne pourra point s'apercevoir qu'ils y sont renfermés » ("aucune communication" is Laloy's addition); second citation (l. 4961-4967): « Persuadez à M. de Lauzun que les nommés Eustache d'Augers et La Rivière ont été mis en liberté et parlez de même à tous ceux qui pourraient vous demander des nouvelles, et cependant renfermez-les dans une chambre où vous puissiez répondre à Sa Majesté qu'ils n'auront communication avec qui que ce soit ».
- Topin and Funck-Brentano paraphrase without quoting the sentence.
- Result: the manuscript wording is "les nommez Eustache d'Angers, et led. la Riviere, ont esté mis en liberté". Delort 1829, Lair and Laloy (first citation) keep the construction; Iung's and Laloy's second citations rewrite it as an order, which is a difference of syntax, not of substance. The only substantive variants are the spelling of the name (3.1) and Laloy's "aucune communication".

### 3.5 The 11 March 1682 letter (Exilles)

Site text is in §2.12. Printed versions: Delort 1825 (l. 10205-10262, pp. 282-284 of the 1825 book), Iung (l. 7985-8016, p. 165, and a second citation l. 18928-18936), Laloy (l. 5118-5157, pp. 142-143). Differences:
- Opening: Delort 1825 begins « J'ai reçu celle qu'il vous a plû me faire l'honneur de m'écrire le 27 du passé, par laquelle vous me mandez, Monseigneur, qu'il est important que mes deux prisonniers n'aient aucun commerce »; Iung (l. 7939-7942) prints the same opening (« J'ai reçu celle qu'il vous a plu me faire l'honneur de m'écrire le 27 du passé, par laquelle vous me mandez, Monseigneur … ») and explains that Saint-Mars was answering both the 2 March letter and « une autre du 27 février »; the site begins « Vous me mandez, Monseigneur, qu’il est important que mes deux prisonniers n’aient aucun commerce », dropping the date reference. (The 2 March 1682 letter the site prints answers to a Saint-Mars letter; Delort's "27 du passé" would be 27 February; the site does not discuss this.)
- « Fouquet et Lauzun, lequel ne se peut pas se vanter » (site) / « MM. Foucquet et Lauzun, lequel ne se peut pas vanter » (Delort 1825) / « MM. Foucquet et Lauzun, lequel ne peut se vanter » (Laloy).
- « le monde qui passe au chemin qui est au bas de la tour » (site, Delort 1825) / « le monde qui est en bas de la tour » (Laloy).
- « d’entendre si personne ne leur parle et s’ils ne crient point par les fenêtres » (site) / « d'entendre si personne ne leur parle, et s'ils ne crient point par leurs fenêtres » (Delort 1825) / « d'entendre que personne ne leur parle, et qu'ils ne crient point par leurs fenêtres » (Laloy).
- « je l’ai fait réparer … un tambour que j’ai fait mettre » (site) / « réparer … fait mettre » (Iung p. 165) / « séparer … fait faire » (Delort 1825; Iung second citation) / « réparer … fait faire » (Laloy).
- « M. Vignon le confesseur » (site) / « M. Vigneron le confesseur » (Iung) / « M. Vigneron (le confesseur) » (Delort 1825) / « M. Vigneron (curé d'Exilés, leur confesseur) » (Laloy). All three editions read Vigneron.
- « mêmes précautions que je faisais jadis pour mes prisonniers du passé » (site) / « que je faisois pour mes prisonniers du passé » (Iung) / « que je faisais pour mes prisonniers du passé » (Laloy): "jadis" is the site's.
- The site's footnote "(2) Il apparait ici que chacun des prisonniers avait sa chambre" rests on "leurs chambres", which all versions have.

### 3.6 The 18 April 1687 letter (Mauvans)

Not in Delort, Iung, Loiseleur, Topin, Lair, Funck-Brentano or Laloy (no hit for Mauvans, Soubiran, Mazaugues, "Voyage à Gènes", "écorter/escorter ce prisonnier"). The site gives no transcription; the only texts are my reading of the facsimile (§2.13) and the Cannes médiathèque page's modernised extract, which agree on the substance ("St Marc", "prisonnier inconnu … conduit avec tant de précautions", the pistol shot if he says his name). The Cannes page reads "de bonne heure" where the manuscript, as I read it, has "a bonne heure".

### 3.7 The Nouvelles ecclésiastiques of 4 September 1687 (steel mask)

- None of the 1825-1913 editions in the sources folder prints this gazette: "masque d'acier" in Iung (l. 2554), Lair (l. 23860, 24070), Laloy (l. 6635), Topin (l. 686) and Delort 1825 (l. 1958) refers only to Voltaire's "masque dont la mentonnière avait des ressorts d'acier"; "Issoudun", "Nouvelles ecclésiastiques" and "Sainte-Geneviève" give no relevant hit (Iung l. 21063 mentions Louis Fouquet's exile to Issoudun only in a biographical note).
- Later texts in the project that quote it: Petitfils 2004 snippets ("chaise à porteurs, ayant un masque d'acier sur le visage, et tout ce qu'on a pu savoir", p. 104); the Pinerolo 1991 colloquium snippets ("il y eut un homme qui s'y tua: celui-ci était enfermé dans une chaise a porteur ayant un masque d'acier sur le visage"); the French Wikipedia extract, modernised: « Monsieur de Saint-Mars a transporté, par ordre du Roi, un prisonnier d'État de Pignerol aux îles Sainte-Marguerite. Personne ne sait qui il est ; il y a défense de dire son nom et ordre de le tuer s'il le prononce. Il était enfermé dans une chaise à porteurs, ayant un masque d'acier sur le visage et tout ce qu'on a pu savoir de Saint-Mars était que ce prisonnier était depuis de longues années à Pignerol et que tous les gens que le public croient [sic] morts ne le sont pas ».
- Differences: the site keeps the manuscript's "cinq mars" for Saint-Mars, "s'il l'avoit prononcé" (Wikipedia: "s'il le prononce"), and the clause « on en a conduit d'autres (à) Pignerol, et celuy sans doute de la sorte il y eut un homme qui s'y tua », which the Wikipedia version omits and the colloquium version keeps. The words "tuer" and "à" are conjectures marked as such by the site; the facsimile is cut at the right margin. The site's two shelf-marks disagree (Réserve, Mss, vol. 1477, f. 396 v° on the ressources page; "M.1427, folio 396" on the thesis page).

### 3.8 The other letters

- 29 March 1673: Delort 1829 (l. 8618-8626) « J'ay reçeu vostre lettre du 15 de ce mois, et j'ay leu fort exactement les papiers éscrits de la main de monsieur Foucquet. Après avoir considéré qu'il n'y marquoit pas ce qu'il dit êstre si important au service du Roy, et qui pouvoit luy procurer quelque soulagement dans sa peine, je n'ay pas jugé à propos de présenter ses mémoires à Sa Majesté ; vous le luy direz, et aussitôst que vous luy en aurez fait voir quelques feuilles, vous les jetterez au feu en sa présence. » Site: "ce qui pourroit luy procurer" and "presenter mémoire(s)". The facsimile reads "ses memoires" and "et qui pourroit"; Delort is right on "ses mémoires", the site on "pourroit".
- 12 March 1680: Delort 1829 (l. 12435-12442) « J ay reçeu vostre lettre du 24 du mois passé avec le mémoire qui y éstoit joint, éscrit de votre main, du contenu duquel je vous prie de ne point dire à monsieur de Lauzun, que vous m'ayez fait part. L'intention du Roy n'est point que vous payez à monsieur Foucquet les gages de celuy de ses valets qui est mort. » Site: "du contenu auquel" (the facsimile reads "auquel"), "vallets" (facsimile "valletz"). Not printed by Iung, Lair, Topin, Funck-Brentano or Laloy: the site's claim that the letter was known to specialists but not published since Delort is consistent with these OCR files.
- 18 August 1679: Delort 1829 (l. 11839-11847) « J'ay reçeu vostre lettre du 9 de ce mois. Puisque vous avez quelque chose à me faire sçavoir que vous ne pouvez pas confier à une lettre, vous pouvez envoyer icy le sieur de Blainvilliers pour m'en rendre compte. Lorsque madame Foucquet et M. le comte de Vaux retourneront à Pignerol, Sa Majesté trouve bon que vous leur laissiez la liberté de voir monsieur Fouc[quet] … » Same text as the site apart from spelling; the site adds nothing.
- 13 September 1679: Laloy alone quotes the last sentence (« Je vous prie de me mander des nouvelles de la santé d'Eustache Danger et de ce qui se passera parmi vos prisonniers »); the site gives the whole letter, including the Blainvilliers passage and the postscript about the marquis de Pianesse.
- 14 January 1673: Ravaisson t. III (l. 7062-7112) « je le fus voir devant hier au soir … il me dit ensuite qu'il n'était pas mal propre à cela, et qu'il avait trouvé des expédients pour en avoir où d'autres personnes seraient demeurées court … Comme je me vois tout moribond … que Dieu lui a donné des lumières d'affaires si grandes … versé en la connaissance de toutes natures d'affaires … il m'a bien dit cent mille autres paroles ». Site: "je le fis voir", "et qu'il trouvé des expédients", "que Dieu m'a donné des lumières", "versé à la connaissance de toutes sortes d'affaires", "il m'a dit cent mille autres paroles". Lair (l. 20105-20106) reads « Comme je me sens tout moribond ». The site's "Dieu m'a donné" (first person, inside Fouquet's reported speech) against Ravaisson's "Dieu lui a donné" is the one difference that changes the sense; the conclusion page repeats "Dieu m'a donné".
- February 1673: Ravaisson t. III (l. 7374-7383) « il me demande souvent si je n'ai point reçu de réponse de vous, Monseigneur, de ce que je vous ai mandé touchant lui ; il me dit toujours que ce sont des affaires de si grande importance que je serais blâmé un jour de ne vous en avoir pas mandé l'importance … et qui sont de très-grande conséquence pour le bien du service du Roi, et très-glorieux pour vous. » Site: "si je n'ai pas reçu", "des choses de si grande importance", "de ne pas vous en avoir mandé". The March 1673 extract was not located in the OCR.
- 18 December 1675: Ravaisson t. III (l. 8998-9004) « M. Foucquet m'a pris par mon faible, en me faisant entendre les grands services qu'il pouvait rendre au Roi et à vous, s'il avait la liberté de pouvoir voir madame sa femme ou quelqu'un de ces deux messieurs que je me suis donné l'honneur de vous mander. Mais puisque S. M. ne désire point se servir de ces expédients, cela finira là, puisque je leur ai dit, une fois pour toutes, que je n'oserais vous entretenir de telles choses sans permission. » Site drops "voir" ("de pouvoir Mme sa femme"), "là", and "vous", and adds "votre" before "permission". The site's Louvois letter "du 3 décembre 1675" is dated 2 December in Ravaisson.
- 2 March 1682: Iung (l. 7930-7933) « … les prisonniers qui sont à Exiles, que l'on nommoit à Pignerol de la Tour d'en bas, n'aient aucun commerce, le Roi m'a ordonné de vous commander de les faire garder si sévèrement et de prendre de telles précautions, que vous puissiez répondre à … »; Laloy (l. 5108-5111) « que l'on nommait à Pignerol de la Tour d'en bas, n'aient aucun commerce, le Roi m'a ordonné de vous commander de les faire garder si sévèrement et de prendre … ». The site's text agrees except for the last words: Iung « ce qui se passera à leur égard » (l. 7936-7937), site « ce qui se passe à leur égard ». Iung's footnote to this letter cites the same Vincennes reference (vol. 675, p. 36).
- 20 January 1687 (quoted on the enquête pages): Iung (l. 741-746, 19162-19168), Laloy (l. 5349-5355), Delort 1825 (l. 10318-10322): « Si je le mène aux îles, je crois que la plus sûre voiture seroit une chaise couverte de toile cirée, de manière qu'il auroit assez d'air, sans que personne le pût voir ni lui parler pendant la route, pas même les soldats que je choisirois pour être proche de la chaise, qui seroit moins embarrassante qu'une litière [qui peut souvent se rompre] ». The site's short version on la-these-nicolas-fouquet adds a sentence on a chapel next to the cell that is not in these printed texts of the 20 January letter; its longer version on la-these-eustache-danger matches them. The site's source "Joseph Delort, L'homme au masque de fer, 1838, pages 283-284" corresponds to Delort's 1825 Histoire de l'homme au masque de fer (OCR page marks "(284)" near l. 10363).
- 23 March 1687: Iung (l. 19252-19258) « je me remettrai en marche avec mon prisonnier, que je vous promets de conduire ici en toute sûreté sans que personne le voie ni lui puisse parler. Je ne lui ferai point entendre la messe depuis son départ d'Exiles jusqu'à ce qu'il soit logé dans la prison qu'on lui prépare ici, où il y aura joignant une chapelle. Je vous réponds sur mon honneur de la sûreté entière de mon prisonnier » ; Delort 1825 (l. 10365-10370) same ending. The site's "de sa sûreté entière" and "sans que personne ne le voie ni ne lui puisse parler" are paraphrases.
- 3 May 1687: Iung (l. 19280-19286) « Je n'ai resté que douze jours en chemin, à cause que mon prisonnier étoit malade, à ce qu'il disoit n'avoir pas autant d'air qu'il l'auroit souhaité; je puis vous assurer, Monseigneur, que personne au monde ne l'a vu, et que la manière dont je l'ai gardé et conduit pendant toute ma route fait que chacun cherche à deviner qui peut être mon prisonnier »; Delort 1825 (l. 10383-10389) and Loiseleur (l. 10705-10708, 12703-12707) same. The site quotes only « Je puis vous assurer, Monseigneur, que personne au monde ne l’a vu ».

---

## 4. The site author's conclusions (his opinion, not a document)

Stated on the pages conclusion, qui-est-le-masque-de-fer, la-these-nicolas-fouquet, les-secrets-de-nicolas-fouquet, un-blog-pour-debattre and masque-de-velours-et-masque-de-fer. In plain terms:

- Identity. The man in the mask was Nicolas Fouquet, not the valet Eustache Danger. The author's chain of reasoning: the 12 March 1680 letter shows that one of Fouquet's two valets was already dead before 8 April 1680; the author identifies the dead valet as Danger, because Louvois had asked after Danger's health in September 1679 and because La Rivière is still mentioned on 8 April 1680; the "two prisoners of the tour d'en bas" of 8 April 1680 were therefore Fouquet and La Rivière, and the name "Eustache d'Angers" in that letter is a disguise for Fouquet, whose family came from Angers ("Nicolas Fouquet était originaire de la ville d'Angers. L'un de ses ancêtres en a même été l'échevin !"). The death of Fouquet announced in the 8 April 1680 letter is, in his view, a fiction invented by Louvois; the other documents of April 1680 (permission to remove the body, the medical bill, the Visitation burial entry of 28 March 1681) are, in his view, either fabricated by Louvois or unsupported by any independent letter. The treasury entries "Messieurs de la tour d'en bas et un valet", "La Tour d'aubas et son valet" (as quoted by Petitfils) are taken as showing one master and one valet. Later testimony (steel mask, sedan chair, silver plate, fine linen, the search for a servant, Chamillart's "un homme qui avait tous les secrets de M. Fouquet") is assembled into a "portrait-robot" that, he says, fits only Fouquet.
- Reason for the secrecy. Louvois (and, before him, his father Le Tellier) hated and feared Fouquet; Fouquet held a secret of great importance that he tried to trade for his freedom in 1673 and 1675, and the King, influenced by Mme de Montespan after her meeting with the Fouquet family at Bourbon in 1677, was moving towards releasing him; Lauzun's denunciation of January 1680 revealed to Louvois that Fouquet had confided "des choses au-dessus de tout ce qu'il pouvait imaginer"; Louvois therefore announced a false death and buried Fouquet in the "tour d'en bas" under Saint-Mars's sole care. The mask was needed because the soldiers of Saint-Mars's company had seen Fouquet walking in the citadel of Pignerol in 1679 and would have recognised him. The nature of the secret is left open ("Ceci est une autre histoire"); the author's lectures link it to Rennes-le-Château and the Poussin letter of 1656.
- Later fate. Fouquet, in his reconstruction, died on Sainte-Marguerite between 1691 (Barbezieux's letter about "le prisonnier qui est sous votre garde depuis vingt ans") and March 1694 (Barbezieux calling one of the arriving prisoners "de plus de conséquence que ceux qui sont présentement sur l'île"). The masked prisoner taken to the Bastille in 1698 and buried as "Marchiali, 45 ans environ" in 1703 was Matthioli, deliberately displayed by Barbezieux to make posterity confuse him with the prisoner of 1687.
- Degree of certainty claimed: « Je sais maintenant avec une quasi-certitude – il n'y a presque jamais de certitude absolue dans aucun domaine – qui était le Masque de fer » (enigme page); the Bastille reconstruction is presented as "une hypothèse, mais c'est celle qui me paraît la plus plausible".
- The site records Petitfils's response: an analysis titled "Fouquet de nouveau" in a re-edition of Le Masque de fer entre histoire et légende (the site gives the year as "1911", an evident slip for 2011), concluding « Non, il n'y a pas de sursis pour la thèse Fouquet », and calling the thesis "un fantôme aux formes imprécises qui revient périodiquement".

---

## 5. Internal inconsistencies and cautions for using the site

1. Dates given differently on different pages: 13 vs 19 September 1679; 14 vs 21 January 1673; 26 vs 27 January 1680; 3 December 1675 (Ravaisson: 2 December); arrival on the island 30 April vs 28 March 1687.
2. Two different transcriptions of the 12 March 1680 letter (the ressources page has garbled characters "vostœ", "mémoll?", "escrlt" and keeps "joint"; the thesis page is clean but drops "joint").
3. "mémoire(s)" (29 March 1673) where the facsimile reads "ses memoires"; "son mémoire" on the conclusion page.
4. "Dieu m'a donné des lumières" (14 January 1673) where Ravaisson reads "Dieu lui a donné".
5. Bibliographic slips: Delort's Détention des philosophes dated 1825 (it is 1829); "Joseph Delort, L'homme au masque de fer, 1838" (Delort's book is 1825); Petitfils's re-edition dated "1911"; two shelf-marks for the gazette (vol. 1477 f. 396 v° / M.1427 f. 396).
6. The letters sourced "Archives de la Bastille – recueillies par François Ravaisson" are modernised copies of a printed edition, not readings of originals; only the five K120 letters and the gazette are checkable against the site's own facsimiles, and those facsimiles support the site's readings of the name ("Dangers" 1679, "d'Angers" 1680).
7. The 18 April 1687 document has no transcription on the site at all; §2.13 gives mine.

## 6. Pages harvested (52) and status

All 52 URLs returned HTTP 200; none failed. Pages: index, page__2, ressources, the 14 ressources pages listed in §2, enigme, les-theses-actuelles, enquete, les-protagonistes-de-laffaire, pignerol-de-1666-a-1680, le-8-avril-1680, exilles-de-1681-a-1687, lile-sainte-marguerite, qui-est-le-masque-de-fer, la-these-eustache-danger, la-these-nicolas-fouquet, les-secrets-de-nicolas-fouquet, conclusion, presentation-2 (/presentation/, with 35 reader comments), qui-suis-je, mon-livre, contact; posts presentation, le-parisien, nice-matin-mars-2004, nice-matin-4-septembre-2005, nice-matin-22-septembre-2024, diaporama-masque-de-fer, conference-masque-de-fer-rennes-le-chateau-2021, un-blog-pour-debattre, parcours-historique-a-vaux-le-vicomte, fouquet-une-these-bien-vivace, masque-de-velours-et-masque-de-fer, conference-a-rennes-les-bains, le-masque-de-fer-mon-enquete; category__media, category__general, category__article, author__claudedabos, author__claudedabos__page__2. The press pages (Le Parisien 2000, Nice-Matin 2004 and 2005, the 2021 lecture, the diaporama) contain only images or embedded media and no text beyond their titles.
