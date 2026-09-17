# Generates frags/rivals.html: the fact x explanation matrix plus the prose around it.
import html
COLS = [("A","Gaume–Puzrin 2021: delayed wind slab at the tent"),
        ("B","Prosecutors' check 2020: slab at ~21:00, ravine bank collapse"),
        ("C","Buyanov 2011: snow board at the tent, the three crushed there"),
        ("D","Katabatic wind, Holmgren 2019"),
        ("E","Infrasound, Eichar 2013"),
        ("F","Military, rocket or toxic release"),
        ("G","Mansi attack or sacred-mountain retribution"),
        ("H","KGB or criminal, Rakitin 2013"),
        ("V","This finding: snow on the tent, cold, ravine collapse")]
# (fact, sheets, scores A..H,V)  E explains/requires  N neutral  C contradicts  P partial / explained away / unmodelled
ROWS = [
("Tent cut open from inside: three knife cuts in the downhill wall plus wind tears", "303–304 (Churkina)", "EEEEEENNE"),
("Tent still standing on its skis; entrance pole and most guy lines intact; buried under 15–20 cm of hard snow; spare skis and ski poles upright beside it", "298–299, 214, 365", "EEECNNNNE"),
("Dyatlov's flashlight lying on the canvas on 5–10 cm of snow with none on top", "299, 70, 310", "PPPENNNNP"),
("No avalanche debris, crown or run-out seen on 26–28 February; the searchers walked and dug on the slope", "298–300, 214–215, 62–75", "PPPEEEEEP"),
("Eight or nine tracks at a normal pace, close together, in a line, for 500–800 m, in socks or barefoot, preserved as raised columns", "312, 91, 215, 292, 386", "EEECCNNEE"),
("Tracks start 15–40 m below the tent in two groups that merge lower down", "215, 315", "NNENNNNNE"),
("No tracks of other people or animals except one dog; no signs of a struggle", "386–387, 91, 71, 177", "EEEEEECCE"),
("Slippers, caps and small items 0.5–15 m downwind of the tent; ice axe by the entrance; a second flashlight, switched on, on the slope below", "299, 70, 215, 191", "EEEEEENNE"),
("Fire under the cedar burned 1.5–2 h; dry branches broken off to 4–5 m; young firs cut", "68, 92, 218–219, 330–339", "EEEEEENNE"),
("Doroshenko and Krivonischenko in underwear by the fire; Krivonischenko's shin burn; their clothes cut off after death and carried to the den", "104–119, 341–343, 386", "EEEEEENNE"),
("Dyatlov, Slobodin and Kolmogorova on the straight line from the fire to the tent, heads toward the tent, 300, 480 and 630 m from the fire", "69–72, 386", "EEEEENNNE"),
("The slope three died of cold; Slobodin's 6 cm skull crack and the ice under him; no alcohol in any of the five March autopsies", "95–103, 120–134, 322", "EEEEEENNE"),
("Den: a floor of 14 fir tops and a birch at 2.5–3 m depth, clothes laid on it, nobody on it; the bodies 6 m downstream in the stream under 2–2.5 m of snow", "341–343", "NENENNNNP"),
("Ravine injuries: bilateral rib fractures on two lines, haemorrhage into the heart, a depressed temporal fracture, all without skin damage; «большая сила»; Thibeaux could only be carried; Dubinina lived 10–20 min", "349–357, 381–383", "PECPCECCP"),
("Kolevatov uninjured, died of cold beside the three injured", "345–348", "EEEEENNNE"),
("Clothing redistributed: Zolotaryov and Thibeaux best dressed with footwear; Dubinina in Krivonischenko's trousers; Zolotaryov in her jacket and cap", "341–343, 386", "EEEEEENNE"),
("Watches stopped at 5:31 (Dyatlov), 8:45 (Slobodin), 8:14 and 8:39 (Thibeaux)", "386, 341", "NNNNNNNNN"),
("Beta contamination on three garments, 5,000–9,900 decays per minute per 150 cm², halved by washing; organs at the natural potassium-40 level", "371–377", "NEENNPNEN"),
("Post-mortem soft-tissue loss on the ravine bodies after three months in the stream: Dubinina's tongue and eyes, Zolotaryov's eyes, Kolevatov's brows", "357, 351, 348", "NNNNNNNNE"),
("Fireballs documented for 17 February and 31 March, none for 1–2 February", "344, 264–267, 290–292, 209–220, 378–380", "NNENNCNNE"),
("Food cache intact on 2 March; money, documents and cameras present; no weapons carried", "8–10, 11–20, 387", "EEEEEENCE"),
("Diaries end on 31 January with no conflict, fear or strangers; the last frames show the tent being pitched in wind at dusk", "21–28; the films", "EEEEENNNE"),
("Stove packed in its case with the pipes inside; a log for it outside; no fire in the tent", "314", "EEEEENNNE"),
("Cameras: four in the tent and one on Zolotaryov's body with a ruined film; a roll of film 15 m below the tent", "11–20, 215", "NNNNNNNPN"),
("Weather: −25 to −30 °C with strong wind in the resolution; the Burmantovo readings fall from −8 to −21 °C between 15:00 and 03:00; the 2020 microclimate expertise gives NW 8 m/s gusting to 30", "385; Maslennikov's notebook; Pigoltsina 2020", "EEEEENNNE"),
("Mansi: alibis, mutual knowledge of every household within 100 km, friendliness; the sacred place is in the upper Vizhay and open to Russians; Mansi were the searchers' guides", "82–87, 223–232, 261–262, 387", "NNNNNNCNN"),
("Slope at the tent: 30° in the 1959 protocol; 15–18° (Sogrin) and 20–25° (Brusnitsyn) from witnesses; 21° at one point in 2019; 15–16° average on a 30 m model that cannot see steps; on the 9 cm drone model of 2021 an average of about 20° with 4–6 m steps over 28–30° above the candidate positions", "3–6, 316–329, 365; Puzrin and Gaume 2022", "EEENNNNNE"),
("Zolotaryov's skeleton, exhumed 12 April 2018: rib fractures as in the 1959 act (posterior rather than mid-axillary line); three right scapula fractures the act missed; front-to-back compression of a supine chest by a surface wider than the ribcage, «большая тяжёлая масса, скорее всего снег»; blast wave excluded; place not determinable from bone", "Nikitin, KP 26 Apr 2018; MK 28 Feb 2019", "EEEECPCCE"),
]
CLS = {"E":"ex","N":"ne","C":"co","P":"pa"}
out = []
out.append('<h2 id="rivals">Every explanation against every fact</h2>')
out.append('<div class="prose"><p>Twenty-eight documented facts, each with its source, are scored below against the eight published explanations and against this finding. The eight are: A, the delayed wind slab of Gaume and Puzrin (2021); B, the prosecutors\' review of 2019–20, which ended with a slab at about 21:00 and a collapse of the ravine bank; C, the version of Evgeny Buyanov, a St Petersburg engineer and mountaineer (2011), a snow slab at the tent that crushed three of them there; D, a katabatic wind, a violent fall wind off the mountain, proposed by the Swedish archaeologist Richard Holmgren (2019); E, infrasound, low-frequency sound off the summit inducing panic, from the American writer Donnie Eichar\'s 2013 book Dead Mountain; F, a military test, rocket or toxic release; G, an attack by Mansi hunters or a sacred-mountain retribution; H, a KGB operation or a criminal attack, from the pseudonymous Russian author Alexei Rakitin (2013). A green cell means the explanation requires or accounts for the fact; grey means it does not address it; amber means it accounts for the fact only by assumption, or leaves it unmodelled; red means the fact contradicts it, with the reason given under the table. The three slab versions are kept apart because they put the fatal injuries in different places.</p></div>')
out.append('<div class="legend"><span><span class="cell ex">E</span> explains or requires</span><span><span class="cell ne">N</span> does not address</span><span><span class="cell pa">P</span> partial, assumed or unmodelled</span><span><span class="cell co">C</span> contradicted</span></div>')
out.append('<div class="tablewrap"><table class="matrix"><thead><tr><th>#</th><th>Documented fact</th><th>Sheets</th>' + ''.join(f'<th title="{html.escape(t)}">{k}</th>' for k,t in COLS) + '</tr></thead><tbody>')
for i,(fact,sheets,sc) in enumerate(ROWS,1):
    cells = ''.join(f'<td><span class="cell {CLS[c]}">{c}</span></td>' for c in sc)
    out.append(f'<tr><td class="num">{i}</td><td class="fact">{html.escape(fact)}</td><td><span class="small">{html.escape(sheets)}</span></td>{cells}</tr>')
out.append('</tbody></table></div>')
out.append('<div class="prose"><p class="small">Columns: ' + '; '.join(f'<strong>{k}</strong> {html.escape(t)}' for k,t in COLS) + '.</p></div>')
open('frags/rivals_matrix.html','w',encoding='utf-8').write('\n'.join(out)+'\n')
print("matrix rows", len(ROWS), "cols", len(COLS))
for fact,sheets,sc in ROWS:
    assert len(sc)==len(COLS), fact
