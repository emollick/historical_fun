#!/usr/bin/env python3
"""Hannibal's pass, 218 BC: an explicit evidential model for ranking the candidate cols.

Method. Each candidate pass H_i gets a prior. Each line of evidence E_k gets, for every
candidate, a likelihood P(E_k | H_i) written as a RANGE [lo, hi] on a relative scale
(the best-fitting candidate for that item sits near 1.0; a candidate the item nearly
excludes sits near 0.02). Posterior ∝ prior_i × Π_k L_ik. The ranges are judgements
argued in the report; the code makes them explicit and shows how fragile the ranking is.

Diagnostics:
  * point estimate at the geometric midpoint of every range;
  * Monte-Carlo draws (log-uniform inside each range, independent across cells) → 5–95% bands;
  * leave-one-out: drop each item and re-rank;
  * shared-source collapse: items that come from the same ancient witness are not
    independent, so within each source family the items are combined by geometric mean
    (the family counts as one item) — a deliberately harsh treatment;
  * tempered: every likelihood raised to the power 0.5 (all judgements halved in strength);
  * sceptic scenarios: named alternative tables that override chosen cells;
  * extremes: each candidate at its own high ends with all rivals at their low ends;
  * factor-to-tie: how much stronger each rival's total case would have to be to draw level.

Usage:  python3 evidence_model.py [n_samples]      (pure Python; no dependencies)
Writes ../data/evidence_model_output.json and .md
"""
import math, random, sys, json, pathlib

from evidence_table import CANDS, PRIOR, EVIDENCE, FAMILIES, SCENARIOS, NOTES

def gm(lo, hi):
    return math.sqrt(lo * hi)

def posterior(table, prior, exponent=1.0, collapse=None, fam_exp=None):
    """table: item -> cand -> likelihood (point values). collapse: item -> family.
    fam_exp: family -> exponent, applied to the items of that family instead of `exponent`
    (used to temper the items that share one ancient source)."""
    logp = {c: math.log(prior[c]) for c in CANDS}
    if fam_exp:
        for it in table:
            e = fam_exp.get(FAMILIES.get(it), exponent)
            for c in CANDS:
                logp[c] += e * math.log(table[it][c])
        m = max(logp.values())
        w = {c: math.exp(logp[c] - m) for c in CANDS}
        z = sum(w.values())
        return {c: w[c] / z for c in CANDS}
    if collapse:
        fam_items = {}
        for it in table:
            fam_items.setdefault(collapse.get(it, it), []).append(it)
        for fam, items in fam_items.items():
            n = len(items)
            for c in CANDS:
                logp[c] += exponent * sum(math.log(table[it][c]) for it in items) / n
    else:
        for it in table:
            for c in CANDS:
                logp[c] += exponent * math.log(table[it][c])
    m = max(logp.values())
    w = {c: math.exp(logp[c] - m) for c in CANDS}
    z = sum(w.values())
    return {c: w[c] / z for c in CANDS}

def point_table(ev):
    return {it: {c: gm(*ev[it][c]) for c in CANDS} for it in ev}

def draw_table(ev, rng):
    t = {}
    for it in ev:
        t[it] = {}
        for c in CANDS:
            lo, hi = ev[it][c]
            t[it][c] = math.exp(rng.uniform(math.log(lo), math.log(hi)))
    return t

def main(n=20000, seed=7):
    rng = random.Random(seed)
    out = {}
    pt = point_table(EVIDENCE)
    out['point'] = posterior(pt, PRIOR)
    out['prior'] = dict(PRIOR)
    # Monte Carlo
    samples = {c: [] for c in CANDS}
    for _ in range(n):
        p = posterior(draw_table(EVIDENCE, rng), PRIOR)
        for c in CANDS:
            samples[c].append(p[c])
    mc = {}
    for c in CANDS:
        s = sorted(samples[c])
        mc[c] = {'p05': s[int(0.05 * n)], 'p50': s[int(0.5 * n)], 'p95': s[int(0.95 * n) - 1],
                 'mean': sum(s) / n}
    out['monte_carlo'] = mc
    # leader frequency
    lead = {c: 0 for c in CANDS}
    rng2 = random.Random(seed + 1)
    for _ in range(n):
        p = posterior(draw_table(EVIDENCE, rng2), PRIOR)
        lead[max(p, key=p.get)] += 1
    out['leader_frequency'] = {c: lead[c] / n for c in CANDS}
    # leave-one-out
    loo = {}
    for it in EVIDENCE:
        sub = {k: v for k, v in pt.items() if k != it}
        loo[it] = posterior(sub, PRIOR)
    out['leave_one_out'] = loo
    # per-item contribution (log-likelihood of each candidate per item, point values)
    out['item_likelihoods'] = pt
    # shared-source collapse
    out['collapsed_by_source'] = posterior(pt, PRIOR, collapse=FAMILIES)
    # tempered
    out['tempered_half'] = posterior(pt, PRIOR, exponent=0.5)
    out['tempered_half_collapsed'] = posterior(pt, PRIOR, exponent=0.5, collapse=FAMILIES)
    # Polybian items (one source) at half strength, everything else at full strength: the headline run
    PH = {'Polybius': 0.5}
    out['polybius_half'] = posterior(pt, PRIOR, fam_exp=PH)
    samples2 = {c: [] for c in CANDS}
    lead2 = {c: 0 for c in CANDS}
    rng3 = random.Random(seed + 2)
    for _ in range(n):
        p2 = posterior(draw_table(EVIDENCE, rng3), PRIOR, fam_exp=PH)
        for c in CANDS:
            samples2[c].append(p2[c])
        lead2[max(p2, key=p2.get)] += 1
    mc2 = {}
    for c in CANDS:
        s2 = sorted(samples2[c])
        mc2[c] = {'p05': s2[int(0.05 * n)], 'p50': s2[int(0.5 * n)], 'p95': s2[int(0.95 * n) - 1], 'mean': sum(s2) / n}
    out['polybius_half_monte_carlo'] = mc2
    out['polybius_half_leader_frequency'] = {c: lead2[c] / n for c in CANDS}
    loo2 = {}
    for it in EVIDENCE:
        sub = {k: v for k, v in pt.items() if k != it}
        loo2[it] = posterior(sub, PRIOR, fam_exp=PH)
    out['polybius_half_leave_one_out'] = loo2
    sc2 = {}
    for name, spec in SCENARIOS.items():
        ev2 = {it: dict(EVIDENCE[it]) for it in EVIDENCE}
        prior2 = dict(PRIOR)
        for it, cells in spec.get('override', {}).items():
            for c, rng_ in cells.items():
                ev2[it][c] = rng_
        for it in spec.get('drop', []):
            ev2.pop(it, None)
        if 'prior' in spec:
            prior2 = spec['prior']
        sc2[name] = {'posterior': posterior(point_table(ev2), prior2, fam_exp=PH), 'note': spec.get('note', '')}
    out['polybius_half_scenarios'] = sc2
    # flat prior
    flat = {c: 1.0 / len(CANDS) for c in CANDS}
    out['flat_prior'] = posterior(pt, flat)
    out['polybius_half_flat_prior'] = posterior(pt, flat, fam_exp=PH)
    # scenarios
    sc = {}
    for name, spec in SCENARIOS.items():
        ev2 = {it: dict(EVIDENCE[it]) for it in EVIDENCE}
        prior2 = dict(PRIOR)
        for it, cells in spec.get('override', {}).items():
            for c, rng_ in cells.items():
                ev2[it][c] = rng_
        for it in spec.get('drop', []):
            ev2.pop(it, None)
        if 'prior' in spec:
            prior2 = spec['prior']
        sc[name] = {'posterior': posterior(point_table(ev2), prior2), 'note': spec.get('note', '')}
    out['scenarios'] = sc
    # extremes: candidate at its high ends, all rivals at low ends
    ext = {}
    for c in CANDS:
        t = {}
        for it in EVIDENCE:
            t[it] = {}
            for d in CANDS:
                lo, hi = EVIDENCE[it][d]
                t[it][d] = hi if d == c else lo
        ext[c] = posterior(t, PRIOR)[c]
    out['best_case_share'] = ext
    # factor to tie
    p = out['point']
    leader = max(p, key=p.get)
    out['leader'] = leader
    out['factor_to_tie'] = {c: (p[leader] / p[c] if p[c] > 0 else float('inf')) for c in CANDS if c != leader}
    out['n_samples'] = n
    out['notes'] = NOTES
    data = pathlib.Path(__file__).resolve().parent.parent / 'data'
    data.mkdir(exist_ok=True)
    (data / 'evidence_model_output.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
    # markdown
    L = []
    L.append('# Evidence model output (Hannibal\'s pass)\n')
    L.append('## Point estimate (geometric midpoints) with Monte-Carlo 5–95%% bands (n=%d)\n' % n)
    L.append('| Candidate | prior | point | p05 | p50 | p95 | leads in draws |')
    L.append('|---|---:|---:|---:|---:|---:|---:|')
    for c in sorted(CANDS, key=lambda c: -p[c]):
        L.append('| %s | %.2f | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.1f%% |' % (
            c, PRIOR[c], 100 * p[c], 100 * mc[c]['p05'], 100 * mc[c]['p50'], 100 * mc[c]['p95'], 100 * out['leader_frequency'][c]))
    L.append('\n## Likelihood table (point values; ranges in evidence_table.py)\n')
    L.append('| Item | ' + ' | '.join(CANDS) + ' |')
    L.append('|---|' + '---:|' * len(CANDS))
    for it in EVIDENCE:
        L.append('| %s | ' % it + ' | '.join('%.2f' % pt[it][c] for c in CANDS) + ' |')
    L.append('\n## Leave-one-out (posterior of each candidate when the item is dropped)\n')
    L.append('| Item dropped | ' + ' | '.join(CANDS) + ' |')
    L.append('|---|' + '---:|' * len(CANDS))
    for it in EVIDENCE:
        L.append('| %s | ' % it + ' | '.join('%.1f%%' % (100 * loo[it][c]) for c in CANDS) + ' |')
    L.append('\n## Robustness variants\n')
    L.append('| Variant | ' + ' | '.join(CANDS) + ' |')
    L.append('|---|' + '---:|' * len(CANDS))
    for name in ['point', 'polybius_half', 'flat_prior', 'polybius_half_flat_prior', 'collapsed_by_source', 'tempered_half', 'tempered_half_collapsed']:
        L.append('| %s | ' % name + ' | '.join('%.1f%%' % (100 * out[name][c]) for c in CANDS) + ' |')
    for name, s in sc.items():
        L.append('| scenario: %s | ' % name + ' | '.join('%.1f%%' % (100 * s['posterior'][c]) for c in CANDS) + ' |')
    L.append('\n## Headline run: Polybian items at half strength (shared source), others full; Monte-Carlo bands\n')
    L.append('| Candidate | point | p05 | p50 | p95 | leads in draws |')
    L.append('|---|---:|---:|---:|---:|---:|')
    ph = out['polybius_half']
    for c in sorted(CANDS, key=lambda c: -ph[c]):
        L.append('| %s | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.1f%% |' % (c, 100 * ph[c], 100 * mc2[c]['p05'], 100 * mc2[c]['p50'], 100 * mc2[c]['p95'], 100 * out['polybius_half_leader_frequency'][c]))
    L.append('\n### Headline run, leave-one-out\n')
    L.append('| Item dropped | ' + ' | '.join(CANDS) + ' |')
    L.append('|---|' + '---:|' * len(CANDS))
    for it in EVIDENCE:
        L.append('| %s | ' % it + ' | '.join('%.1f%%' % (100 * loo2[it][c]) for c in CANDS) + ' |')
    L.append('\n### Headline run, scenarios\n')
    L.append('| Scenario | ' + ' | '.join(CANDS) + ' |')
    L.append('|---|' + '---:|' * len(CANDS))
    for name, s2_ in sc2.items():
        L.append('| %s | ' % name + ' | '.join('%.1f%%' % (100 * s2_['posterior'][c]) for c in CANDS) + ' |')
    L.append('\n## Best-case share (candidate at its high ends, rivals at their low ends)\n')
    for c in CANDS:
        L.append('- %s: %.1f%%' % (c, 100 * ext[c]))
    L.append('\n## Factor by which a rival\'s total case must strengthen to tie the leader (%s)\n' % leader)
    for c, f in sorted(out['factor_to_tie'].items(), key=lambda kv: kv[1]):
        L.append('- %s: ×%.1f' % (c, f))
    (data / 'evidence_model_output.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L[:len(CANDS) + 4]))
    print('written', data / 'evidence_model_output.json')

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
