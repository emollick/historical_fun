#!/usr/bin/env python3
"""Brunanburh 937: explicit evidential model for ranking candidate sites.

Method. Each candidate H_i (plus a catch-all 'some other, unidentified place') gets a
prior. Each line of evidence E_k gets, for every candidate, a likelihood ratio
LR_ik = P(E_k | H_i) / P(E_k | catch-all), written as a RANGE [lo, hi] so that the
uncertainty of the judgement is explicit. Posterior ∝ prior_i × Π_k LR_ik.
A Monte-Carlo draw (log-uniform inside each range, independent across cells) gives a
distribution of posteriors; a leave-one-out pass shows which item carries the ranking;
a 'what would it take' pass finds the single-item change that would dethrone the leader.

The cells are judgements argued in the report ('How the probabilities were built').
Edit the table and re-run:  python3 evidence_model.py [n_samples]
Pure python; no dependencies. Writes evidence_model_output.json and .md
"""
import math, random, sys, json

CANDS = [
 'Bromborough (Wirral)',
 'Went valley / Burghwallis (Wood 2013)',
 'Brinsworth / Tinsley (Wood 1980)',
 'Other Humber-bank sites (E. Riding, Barrow, Brough)',
 'Burnswark (Dumfriesshire)',
 'Lanchester (Co. Durham)',
 'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)',
 'Southern / inland (Bourn, Bromswold, Bourne, Axminster)',
 'Other, unidentified site',
]
OTHER = 'Other, unidentified site'

# Prior. The catch-all carries most of the mass: the true site could be a place whose
# name changed or was lost. Named candidates get a little more than a random parish
# because each was proposed for a reason that is itself weak evidence.
PRIOR = {
 'Bromborough (Wirral)': 0.05,
 'Went valley / Burghwallis (Wood 2013)': 0.04,
 'Brinsworth / Tinsley (Wood 1980)': 0.03,
 'Other Humber-bank sites (E. Riding, Barrow, Brough)': 0.04,
 'Burnswark (Dumfriesshire)': 0.04,
 'Lanchester (Co. Durham)': 0.03,
 'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': 0.05,
 'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': 0.02,
 'Other, unidentified site': 0.70,
}

# Likelihood-ratio ranges relative to the catch-all (fixed at 1).
EVIDENCE = {
 'E1 Name: a place-name at the site regularly descends from OE Brunanburh / Brunnanwerc / Brunandun': {
   'Bromborough (Wirral)': (3.0, 12.0),          # only regular descendant (Dodgson 1957; Cavill 2011 §6.1); Bruna rare (4 names, 3 on Wirral: Cavill & Harding 2025); contested by Deakin 2022
   'Went valley / Burghwallis (Wood 2013)': (0.8, 1.3),   # Burghwallis = DB 'Burg', a burh, no Brunan- element (Cavill 2022/23)
   'Brinsworth / Tinsley (Wood 1980)': (0.7, 1.2),        # Brynesford (DB): Bryni, -s genitive, not Bruna (Page; Cavill §5.2)
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (0.9, 1.6),  # Nunburnholme = DB Brunham (ON brunnr, springs)
   'Burnswark (Dumfriesshire)': (0.9, 1.6),      # Burniswerkhill 1541, Burnyswarke 1542; -wark ~ -werc, but first element burn + -is; no forms within 600 yrs (Cavill §5.1)
   'Lanchester (Co. Durham)': (0.8, 1.4),        # Breeze: burh by the Browney (Brune c.1190, Brun c.1195: strong Brun, not weak Brunan-); Lanchester itself = Langecestre; rejected Cavill 2023
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (0.9, 1.6),  # River Brun / Burnley (Brunlaia 1124)
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.9, 1.5), # Bourn (DB Brune); Bruneswald; brunnr not inflected -an (Cavill §5.3-5.4)
 },
 'E2 Dingesmere: a Thing-name beside the water from which the Norse sailed for Dublin': {
   'Bromborough (Wirral)': (1.5, 5.0),           # Thingwall 5 km; Dee wetlands (Cavill, Harding & Jesch 2004); D- for þ- and wetland contested (Deakin 2022; Cavill 2023)
   'Went valley / Burghwallis (Wood 2013)': (0.8, 1.3),   # Tingley (OE þing-hlaw) 23 km but no 'mere' to sail from
   'Brinsworth / Tinsley (Wood 1980)': (0.8, 1.3),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (0.7, 1.2),
   'Burnswark (Dumfriesshire)': (1.2, 3.0),      # Tinwald (ON þingvöllr) 19 km on the Solway side
   'Lanchester (Co. Durham)': (0.7, 1.2),
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (1.0, 2.0),  # Thingwall (Knotty Ash) by the Mersey
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.7, 1.2),
 },
 'E3 Humber tradition: John of Worcester (c.1140) says the fleet entered the Humber': {
   'Bromborough (Wirral)': (0.5, 1.1),           # JW formulaic, misreads poem, confuses the two Anlafs (Cavill 2011 §4; 2022; Woolf 2007)
   'Went valley / Burghwallis (Wood 2013)': (1.6, 2.7),
   'Brinsworth / Tinsley (Wood 1980)': (1.6, 2.7),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (1.6, 2.7),
   'Burnswark (Dumfriesshire)': (0.5, 1.1),
   'Lanchester (Co. Durham)': (0.9, 1.6),        # Breeze: Humber then north
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (0.5, 1.1),
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.8, 1.3),
 },
 'E4 We(o)ndun and Brunandun: independent traditions that the site was a dun (low hill), with a Durham name': {
   'Bromborough (Wirral)': (0.8, 1.3),           # no dun-name; Welondrys/Harrow names (Cavill §6.5) weak
   'Went valley / Burghwallis (Wood 2013)': (0.9, 1.6),   # Wendun = Went + dun (Wood 2013); but Went = Wenet/Wente, Went Hill 'a hyll'; rejected Cavill 2022/23
   'Brinsworth / Tinsley (Wood 1980)': (0.9, 1.4),        # White Hill (wiht/wih)
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (0.9, 1.4),
   'Burnswark (Dumfriesshire)': (0.6, 1.1),      # dun-names absent NW England / SW Scotland; not used of hill-forts (Gelling & Cole)
   'Lanchester (Co. Durham)': (1.0, 1.6),        # Durham tradition; Breeze's wen-hill
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (0.7, 1.1),  # no dun-names north of the Ribble
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.8, 1.2),
 },
 "E5 Egil's saga: Vinheidr, a northern heath with a borg, on the Scottish frontier": {
   'Bromborough (Wirral)': (0.8, 1.1),
   'Went valley / Burghwallis (Wood 2013)': (1.0, 1.4),
   'Brinsworth / Tinsley (Wood 1980)': (1.0, 1.4),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (1.0, 1.4),
   'Burnswark (Dumfriesshire)': (1.0, 1.3),
   'Lanchester (Co. Durham)': (1.0, 1.4),
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (0.9, 1.1),
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.7, 1.0),
 },
 'E6 The poem: Norse sail from Dingesmere over deep water to Dublin; Constantine goes north by land; Irish annals': {
   'Bromborough (Wirral)': (1.3, 2.5),           # direct Irish Sea crossing; 'oth Lynne' = the Lyme (Higham) speculative
   'Went valley / Burghwallis (Wood 2013)': (0.6, 1.0),   # a 700+ nmi voyage compressed into one line
   'Brinsworth / Tinsley (Wood 1980)': (0.6, 1.0),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (0.6, 1.0),
   'Burnswark (Dumfriesshire)': (1.2, 2.0),
   'Lanchester (Co. Durham)': (0.6, 1.0),
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (1.3, 2.5),
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.5, 0.9),
 },
 'E7 Strategy and logistics: convergence of three armies, an English battlefield that Aethelstan defended (ealgian), routes and distances': {
   'Bromborough (Wirral)': (1.2, 2.5),           # 108 nmi crossing; Norse enclave; Chester roads to York (Downham 2021); Scots' 430 km march is the weakness
   'Went valley / Burghwallis (Wood 2013)': (0.9, 1.8),   # York objective, Great North Road; fleet 700-800 nmi round Scotland
   'Brinsworth / Tinsley (Wood 1980)': (0.8, 1.5),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (0.8, 1.5),
   'Burnswark (Dumfriesshire)': (0.5, 1.1),      # not English land to defend; Aethelstan 550 km away
   'Lanchester (Co. Durham)': (0.5, 1.0),        # 17 miles from any coast, 7-8 miles from St Cuthbert's community at Chester-le-Street, whose records are silent (Cavill 2023)
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (1.0, 2.0),
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (0.3, 0.8),
 },
 'E8 Archaeology: the mid-Wirral assemblage (consistent with a camp, not conclusive; no findspots)': {
   'Bromborough (Wirral)': (1.0, 1.5),
   'Went valley / Burghwallis (Wood 2013)': (1.0, 1.0),
   'Brinsworth / Tinsley (Wood 1980)': (1.0, 1.0),
   'Other Humber-bank sites (E. Riding, Barrow, Brough)': (1.0, 1.0),
   'Burnswark (Dumfriesshire)': (1.0, 1.0),
   'Lanchester (Co. Durham)': (1.0, 1.0),
   'Lancashire west coast (Ribble, Fylde, Wigan, Burnley)': (1.0, 1.0),
   'Southern / inland (Bourn, Bromswold, Bourne, Axminster)': (1.0, 1.0),
 },
}

def posterior(lr_of):
    """lr_of(evidence, cand) -> LR. Returns normalised posterior dict."""
    w = {}
    for c in CANDS:
        v = PRIOR[c]
        if c != OTHER:
            for e in EVIDENCE:
                v *= lr_of(e, c)
        w[c] = v
    z = sum(w.values())
    return {c: w[c]/z for c in CANDS}

def geo(lo, hi): return math.sqrt(lo*hi)

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    random.seed(937)
    # point estimate at geometric midpoints
    point = posterior(lambda e, c: geo(*EVIDENCE[e][c]))
    # Monte Carlo
    samples = {c: [] for c in CANDS}
    for _ in range(n):
        draw = {e: {c: math.exp(random.uniform(math.log(lo), math.log(hi))) for c, (lo, hi) in EVIDENCE[e].items()} for e in EVIDENCE}
        p = posterior(lambda e, c: draw[e][c])
        for c in CANDS: samples[c].append(p[c])
    def q(xs, f):
        xs = sorted(xs); return xs[min(len(xs)-1, int(f*len(xs)))]
    mc = {c: {'mean': sum(samples[c])/n, 'p05': q(samples[c], .05), 'p50': q(samples[c], .5), 'p95': q(samples[c], .95)} for c in CANDS}
    # probability that each candidate is top-ranked across draws (ignoring the catch-all)
    top = {c: 0 for c in CANDS}
    for i in range(n):
        best = max((c for c in CANDS if c != OTHER), key=lambda c: samples[c][i]); top[best] += 1
    # leave-one-out
    loo = {}
    for e in EVIDENCE:
        loo[e] = posterior(lambda ee, c: 1.0 if ee == e else geo(*EVIDENCE[ee][c]))
    # what would it take: for each rival, the factor by which its total LR product must be multiplied to tie Bromborough (point estimate)
    lead = 'Bromborough (Wirral)'
    need = {c: point[lead]/point[c] for c in CANDS if c not in (lead, OTHER)}
    # extreme cases: all Wirral cells at lo and all rivals at hi (worst case for Bromborough), and the reverse
    worst = posterior(lambda e, c: EVIDENCE[e][c][0] if c == lead else EVIDENCE[e][c][1])
    best = posterior(lambda e, c: EVIDENCE[e][c][1] if c == lead else EVIDENCE[e][c][0])
    out = {'n': n, 'prior': PRIOR, 'point': point, 'mc': mc, 'top_share': {c: top[c]/n for c in CANDS}, 'leave_one_out': loo, 'factor_needed_to_tie_leader': need, 'worst_case_for_leader': worst, 'best_case_for_leader': best, 'evidence': EVIDENCE}
    json.dump(out, open('evidence_model_output.json', 'w'), indent=1)
    # markdown summary
    L = ['| candidate | prior | point | MC mean | 5% | 95% | share of draws ranked first |', '|---|---|---|---|---|---|---|']
    for c in sorted(CANDS, key=lambda c: -point[c]):
        L.append(f"| {c} | {PRIOR[c]:.2f} | {point[c]:.3f} | {mc[c]['mean']:.3f} | {mc[c]['p05']:.3f} | {mc[c]['p95']:.3f} | {top[c]/n:.3f} |")
    L.append('\nLeave-one-out (point posterior of the leader and the best rival when each item is removed):')
    for e in EVIDENCE:
        p = loo[e]; rival = max((c for c in CANDS if c not in (lead, OTHER)), key=lambda c: p[c])
        L.append(f"- without {e[:60]}…: {lead} {p[lead]:.3f}; best rival {rival} {p[rival]:.3f}; other {p[OTHER]:.3f}")
    L.append('\nFactor by which a rival\'s combined likelihood would have to rise to tie the leader (point estimate):')
    for c, f in sorted(need.items(), key=lambda kv: kv[1]):
        L.append(f"- {c}: x{f:.1f}")
    L.append(f"\nWorst case for leader (all its cells at low end, rivals at high end): {lead} {worst[lead]:.3f}; other {worst[OTHER]:.3f}; best rival {max((c for c in CANDS if c not in (lead,OTHER)), key=lambda c: worst[c])} {max(worst[c] for c in CANDS if c not in (lead,OTHER)):.3f}")
    L.append(f"Best case for leader: {best[lead]:.3f}")
    open('evidence_model_output.md', 'w').write('\n'.join(L))
    print('\n'.join(L))

if __name__ == '__main__':
    main()
