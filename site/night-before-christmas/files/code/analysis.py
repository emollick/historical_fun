"""
analysis.py -- the full computational study for "A Visit from St. Nicholas".

Stages (run all with `python3 analysis.py`, or one with `python3 analysis.py stageX`):
  describe   : corpus inventory
  validate   : leave-one-poem-out attribution accuracy on ~56-line samples
               (Moore vs Livingston; all feature sets; overall and by metre)
  gi_calib   : General Imposters score distributions for known samples
  attribute  : distances / GI scores for the disputed poem
  markers    : lexical, metrical and rhyme habits
  write      : results -> data/results/*.json and *.md

All randomness is seeded. Results are written to ../data/results/.
"""
import os, sys, json, math, random, re
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stylo
from stylo import (load_corpus, load_poem, tokens, counts_for, top_features,
                   rel_freq_matrix, zscore, profile_attribution,
                   instance_attribution, general_imposters, make_samples,
                   form_class, word_count, DIST)
import phon
import meter as meter_mod

_NEUTRAL_CACHE = {}
def neutral_filter(feats, ctrl, kind, n, t_cut=3.0, lr_cut=0.25):
    """Drop features that the control authors show to be metre-driven."""
    key = (kind, n)
    if key not in _NEUTRAL_CACHE:
        _NEUTRAL_CACHE[key] = meter_mod.author_form_profiles(ctrl, kind, n)
    prof = _NEUTRAL_CACHE[key]
    sens = meter_mod.metre_sensitivity(prof, feats)
    keep, drop = meter_mod.metre_neutral(feats, sens, t_cut, lr_cut)
    return keep, drop

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, 'corpus')
OUT = os.path.join(ROOT, 'data', 'results')
os.makedirs(OUT, exist_ok=True)

MOORE, LIV = 'Clement Clarke Moore', 'Henry Livingston Jr.'
INCLUDE_MSS = True
EXCLUDE_TRANSLATIONS = True

FEATURE_SETS = {
    # name: (kind, n, k, culling)
    'mfw100':  ('word', None, 100, 0.0),
    'mfw200':  ('word', None, 200, 0.0),
    'mfw300':  ('word', None, 300, 0.0),
    'char3':   ('char', 3, 500, 0.0),
    'char4':   ('char', 4, 1000, 0.0),
    'phone':   ('phone', None, 45, 0.0),
}

# ----------------------------------------------------------------------
def load_all(min_attr=('certain', 'probable')):
    moore = load_corpus(os.path.join(CORPUS, 'moore'))
    if INCLUDE_MSS:
        moore += load_corpus(os.path.join(CORPUS, 'moore_mss'))
    liv = load_corpus(os.path.join(CORPUS, 'livingston'))
    ctrl = load_corpus(os.path.join(CORPUS, 'control'))
    # drop prose, drop the disputed poem if it slipped into moore/, drop doubtful
    EXCL_DIRS = ('/not_moore/', '/hoffman_1837/', '/prose/', '/disputed/', '/visit/')
    # translations (Jackson's practice) and the 1824 newspaper variant of an in-book poem
    EXCL_IDS = {'04_the_mischievous_muse', '10_translation_of_an_ode_of_metastasio',
                '15_translation_of_a_chorus_in_aeschylus', '19_petrarchs_sonnet',
                '03_lines_written_after_a_snow_storm_1824'}
    def ok(d):
        if any(x in d['path'] for x in EXCL_DIRS):
            return False
        if EXCLUDE_TRANSLATIONS and d['id'] in EXCL_IDS:
            return False
        if 'preface' in d['id'].lower():
            return False
        if 'nicholas' in d.get('title', '').lower() and 'visit' in d.get('title', '').lower():
            return False
        if d.get('form', '').lower().startswith('prose'):
            return False
        return True
    moore = [d for d in moore if ok(d) and d['author'] == MOORE]
    liv = [d for d in liv if ok(d) and d['author'] == LIV
           and d['attribution'].lower().split()[0] in min_attr]
    ctrl = [d for d in ctrl if ok(d)]
    for d in moore + liv + ctrl:
        d['form_class'] = form_class(d['form'])
    return moore, liv, ctrl

def load_visit(which='1823'):
    cand = [p for p in os.listdir(os.path.join(CORPUS, 'visit'))
            if p.endswith('.txt') and which in p]
    if not cand:
        raise FileNotFoundError(which)
    d = load_poem(os.path.join(CORPUS, 'visit', sorted(cand)[0]))
    # keep only the verse: cut at any editorial marker appended after the poem
    vl = []
    for l in d['verse_lines']:
        if re.match(r'^[A-Z][A-Z .,()\-]{8,}', l.strip()):   # e.g. "EDITORIAL PREFACE (..."
            break
        vl.append(l)
    d['verse_lines'] = vl[:56] if len(vl) >= 56 else vl
    d['text'] = '\n'.join(d['verse_lines'])
    d['n_lines'] = len(d['verse_lines'])
    d['form_class'] = 'anapestic'
    return d

# ----------------------------------------------------------------------
def describe(moore, liv, ctrl):
    rows = []
    for name, docs in (('Moore', moore), ('Livingston', liv), ('Controls', ctrl)):
        by = defaultdict(lambda: [0, 0, 0])
        for d in docs:
            key = (name, d['author'], d['form_class'], d['attribution'])
            by[key][0] += 1; by[key][1] += d['n_lines']; by[key][2] += word_count(d['text'])
        for k, v in sorted(by.items()):
            rows.append(dict(group=k[0], author=k[1], form=k[2], attribution=k[3],
                             poems=v[0], lines=v[1], words=v[2]))
    return rows

# ----------------------------------------------------------------------
def sample_counts(samples, fs):
    kind, n, k, cull = FEATURE_SETS[fs]
    return [counts_for(s, kind, n) for s in samples]

def validate(moore, liv, ctrl, feature_sets=None, target_lines=56,
             dist_names=('delta', 'cosine'), reference='both'):
    """Leave-one-poem-out: each sample is attributed with profiles built from
    all OTHER samples (same-poem material excluded). reference='both' uses the
    whole Moore and Livingston corpora; 'anapestic' uses only their anapestic
    samples as reference; 'multi' adds the control authors as classes."""
    feature_sets = feature_sets or list(FEATURE_SETS)
    sm = make_samples(moore, target_lines); sl = make_samples(liv, target_lines)
    samples = sm + sl
    classes = [MOORE, LIV]
    if reference == 'multi':
        sc = make_samples(ctrl, target_lines)
        samples = samples + sc
        classes = sorted(set(s['author'] for s in samples))
    results = {}
    cache = {fs: sample_counts(samples, fs) for fs in feature_sets}
    for fs in feature_sets:
        kind, n, k, cull = FEATURE_SETS[fs]
        cnts = cache[fs]
        for dn in dist_names:
            recs = []
            for i, s in enumerate(samples):
                if reference != 'multi' and s['author'] not in (MOORE, LIV):
                    continue
                ref_idx = [j for j, t in enumerate(samples)
                           if j != i and not (t['poem_ids'] & s['poem_ids'])]
                if reference == 'anapestic':
                    ref_idx = [j for j in ref_idx if samples[j]['form_class'] == 'anapestic']
                ref_c = [cnts[j] for j in ref_idx]
                ref_a = [samples[j]['author'] for j in ref_idx]
                feats = top_features(ref_c, k, cull)
                if reference == 'both_neutral':
                    feats, _ = neutral_filter(feats, ctrl, kind, n)
                dists = profile_attribution(cnts[i], ref_c, ref_a, feats, dist=dn)
                pred = min(dists, key=dists.get)
                recs.append(dict(ids=s['ids'], author=s['author'], form=s['form_class'],
                                 lines=s['lines'], pred=pred, correct=pred == s['author'],
                                 d_moore=dists.get(MOORE), d_liv=dists.get(LIV),
                                 margin=(dists.get(LIV, 0) - dists.get(MOORE, 0))))
            acc = np.mean([r['correct'] for r in recs]) if recs else float('nan')
            by = defaultdict(list)
            for r in recs:
                by[(r['author'], r['form'])].append(r['correct'])
            results[f'{fs}|{dn}'] = dict(
                accuracy=float(acc), n=len(recs),
                by_author_form={f'{a}|{f}': dict(n=len(v), acc=float(np.mean(v)))
                                for (a, f), v in sorted(by.items())},
                records=recs)
    return results, samples

# ----------------------------------------------------------------------
def cap_control_samples(sc, per_author=12, seed=0):
    """Keep at most per_author samples per control author, anapestic first."""
    rng = random.Random(seed)
    by = defaultdict(list)
    for s in sc:
        by[s['author']].append(s)
    out = []
    for a, ss in sorted(by.items()):
        an = [s for s in ss if s['form_class'] == 'anapestic']
        ot = [s for s in ss if s['form_class'] != 'anapestic']
        rng.shuffle(an); rng.shuffle(ot)
        out.extend((an + ot)[:per_author])
    return out

def gi_calibration(moore, liv, ctrl, feature_sets=('mfw200', 'char4'),
                   target_lines=56, n_iter=150, seed=1, include_other=True):
    """For every Moore/Livingston sample, GI score with candidate=Moore and
    candidate=Livingston, impostors = control authors' samples (+ the other
    candidate's samples when include_other). Same-poem material excluded."""
    rng = random.Random(seed)
    sm = make_samples(moore, target_lines); sl = make_samples(liv, target_lines)
    sc = cap_control_samples(make_samples(ctrl, target_lines))
    out = {}
    for fs in feature_sets:
        kind, n, k, cull = FEATURE_SETS[fs]
        cm, cl, cc = sample_counts(sm, fs), sample_counts(sl, fs), sample_counts(sc, fs)
        feats = top_features(cm + cl + cc, k, cull)
        recs = []
        for cand_name, cand_s, cand_c, other_s, other_c in (
                (MOORE, sm, cm, sl, cl), (LIV, sl, cl, sm, cm)):
            # true-author trials
            for i, s in enumerate(cand_s):
                own = [cand_c[j] for j, t in enumerate(cand_s)
                       if j != i and not (t['poem_ids'] & s['poem_ids'])]
                imps = cc + (other_c if include_other else [])
                sc_ = general_imposters(cand_c[i], own, imps, feats, n_iter=n_iter, rng=rng)
                recs.append(dict(candidate=cand_name, truth=cand_name, ids=s['ids'],
                                 form=s['form_class'], score=sc_, true=True))
            # false-author trials: the other candidate's samples tested against cand
            for i, s in enumerate(other_s):
                imps = cc + ([other_c[j] for j, t in enumerate(other_s)
                              if j != i and not (t['poem_ids'] & s['poem_ids'])]
                             if include_other else [])
                sc_ = general_imposters(other_c[i], cand_c, imps, feats, n_iter=n_iter, rng=rng)
                recs.append(dict(candidate=cand_name, truth=s['author'], ids=s['ids'],
                                 form=s['form_class'], score=sc_, true=False))
        out[fs] = recs
    return out

# ----------------------------------------------------------------------
def attribute_poem(poem, moore, liv, ctrl, target_lines=56, n_iter=400, seed=2):
    """All methods applied to the disputed poem."""
    rng = random.Random(seed)
    sm = make_samples(moore, target_lines); sl = make_samples(liv, target_lines)
    sc = cap_control_samples(make_samples(ctrl, target_lines))
    res = {}
    for fs in FEATURE_SETS:
        kind, n, k, cull = FEATURE_SETS[fs]
        pc = counts_for(poem, kind, n)
        cm, cl, cc = sample_counts(sm, fs), sample_counts(sl, fs), sample_counts(sc, fs)
        r = {}
        # (a) two-class nearest centroid, whole corpora
        feats = top_features(cm + cl, k, cull)
        for dn in ('delta', 'cosine'):
            d = profile_attribution(pc, cm + cl, [MOORE]*len(cm) + [LIV]*len(cl), feats, dist=dn)
            r[f'centroid_both_{dn}'] = d
            # (b) anapestic-only reference
            am = [c for c, s in zip(cm, sm) if s['form_class'] == 'anapestic']
            al = [c for c, s in zip(cl, sl) if s['form_class'] == 'anapestic']
            if am and al:
                feats_a = top_features(am + al, k, cull)
                r[f'centroid_anapestic_{dn}'] = profile_attribution(
                    pc, am + al, [MOORE]*len(am) + [LIV]*len(al), feats_a, dist=dn)
            # (c) multi-class with controls
            allc = cm + cl + cc
            alla = [MOORE]*len(cm) + [LIV]*len(cl) + [s['author'] for s in sc]
            feats_m = top_features(allc, k, cull)
            dm = profile_attribution(pc, allc, alla, feats_m, dist=dn)
            r[f'centroid_multi_{dn}'] = dict(sorted(dm.items(), key=lambda kv: kv[1]))
            # (d) nearest instance
            r[f'nearest_instance_multi_{dn}'] = dict(sorted(instance_attribution(
                pc, allc, alla, feats_m, dist=dn, k=1).items(), key=lambda kv: kv[1]))
        # (b2) metre-neutral features, whole corpora
        feats_n, dropped = neutral_filter(feats, ctrl, kind, n)
        for dn in ('delta', 'cosine'):
            r[f'centroid_both_neutral_{dn}'] = profile_attribution(
                pc, cm + cl, [MOORE]*len(cm) + [LIV]*len(cl), feats_n, dist=dn)
        r['neutral_dropped'] = dropped
        # (e) General Imposters
        feats_g = top_features(cm + cl + cc, k, cull)
        feats_gn, _ = neutral_filter(feats_g, ctrl, kind, n)
        r['gi_moore_vs_controls+liv_neutral'] = general_imposters(pc, cm, cc + cl, feats_gn, n_iter=n_iter, rng=rng)
        r['gi_liv_vs_controls+moore_neutral'] = general_imposters(pc, cl, cc + cm, feats_gn, n_iter=n_iter, rng=rng)
        r['gi_moore_vs_controls+liv'] = general_imposters(pc, cm, cc + cl, feats_g, n_iter=n_iter, rng=rng)
        r['gi_liv_vs_controls+moore'] = general_imposters(pc, cl, cc + cm, feats_g, n_iter=n_iter, rng=rng)
        r['gi_moore_vs_controls'] = general_imposters(pc, cm, cc, feats_g, n_iter=n_iter, rng=rng)
        r['gi_liv_vs_controls'] = general_imposters(pc, cl, cc, feats_g, n_iter=n_iter, rng=rng)
        # GI for each control author as candidate (sanity: does anyone else score high?)
        gi_ctrl = {}
        for a in sorted(set(s['author'] for s in sc)):
            own = [c for c, s in zip(cc, sc) if s['author'] == a]
            oth = [c for c, s in zip(cc, sc) if s['author'] != a] + cm + cl
            if len(own) >= 3:
                gi_ctrl[a] = general_imposters(pc, own, oth, feats_g, n_iter=n_iter // 2, rng=rng)
        r['gi_controls_as_candidates'] = gi_ctrl
        res[fs] = r
    return res

# ----------------------------------------------------------------------
def markers(poem, moore, liv, ctrl):
    """Lexical, metrical and rhyme habits per author (all verse and anapestic
    verse only), with the poem's values."""
    import re
    def stats(docs, label):
        lines = [l for d in docs for l in d['verse_lines']]
        text = '\n'.join(lines)
        toks = tokens(text)
        N = len(toks); L = len(lines)
        if N == 0:
            return None
        c = Counter(toks)
        def per1000(x): return 1000.0 * x / N
        low = [l.strip().lower() for l in lines]
        def starts(w): return sum(1 for l in low if re.match(r"^[\"'(]*" + w + r"\b", l))
        syl = Counter(); feet = Counter(); fem = 0
        for l in lines:
            s = phon.line_syllables(l); syl[s] += 1
            fem += phon.feminine_ending(l)
        anap_full = sum(v for k, v in syl.items() if k in (12, 13))
        anap_short = sum(v for k, v in syl.items() if k in (11,))
        excl = sum(1 for l in lines if l.count('!') >= 2)
        return dict(label=label, words=N, lines=L,
                    all_per1000=per1000(c['all']),
                    ere_per1000=per1000(c['ere']),
                    twas_per1000=per1000(c['twas']),
                    tis_per1000=per1000(c['tis']),
                    like_per1000=per1000(c['like']),
                    little_per1000=per1000(c['little']),
                    and_line_initial_pct=100.0 * starts('and') / L,
                    when_line_initial_pct=100.0 * starts('when') / L,
                    the_per1000=per1000(c['the']),
                    a_per1000=per1000(c['a']),
                    his_per1000=per1000(c['his']),
                    of_per1000=per1000(c['of']),
                    i_per1000=per1000(c['i']),
                    now_per1000=per1000(c['now']),
                    feminine_ending_pct=100.0 * fem / L,
                    multi_exclaim_line_pct=100.0 * excl / L,
                    syll11_pct_of_11_13=100.0 * anap_short / max(1, anap_short + anap_full),
                    happy=c['happy'], merry=c['merry'],
                    dutch_terms={w: c[w] for w in ('dunder', 'blixem', 'donder', 'blitzen', 'santa', 'santeclaus', 'nick', 'nicholas', 'sinterklaas') if c[w]})
    out = {}
    out['poem'] = stats([poem], 'poem')
    for name, docs in (('moore', moore), ('livingston', liv)):
        out[name + '_all'] = stats(docs, name + ' (all verse)')
        out[name + '_anapestic'] = stats([d for d in docs if d['form_class'] == 'anapestic'], name + ' (anapestic)')
    out['controls_anapestic'] = stats([d for d in ctrl if d['form_class'] == 'anapestic'], 'controls (anapestic)')
    out['controls_all'] = stats(ctrl, 'controls (all)')
    return out

def rhyme_repertoire(poem, moore, liv, ctrl):
    """For each couplet rhyme pair in the poem, count how often the same
    end-word pair (either order) rhymes in each corpus, normalised per 1000
    couplets; also the fraction of the poem's rhyme *words* that appear as
    rhyme words in each corpus."""
    def pairs(docs):
        cnt = Counter(); words = Counter(); n = 0
        for d in docs:
            for a, b, kind in phon.couplet_rhymes(d['verse_lines']):
                cnt[frozenset((a, b))] += 1; words[a] += 1; words[b] += 1; n += 1
        return cnt, words, n
    pp = phon.couplet_rhymes(poem['verse_lines'])
    out = {}
    for name, docs in (('moore', moore), ('livingston', liv), ('controls', ctrl),
                       ('moore_anap', [d for d in moore if d['form_class']=='anapestic']),
                       ('liv_anap', [d for d in liv if d['form_class']=='anapestic']),
                       ('controls_anap', [d for d in ctrl if d['form_class']=='anapestic'])):
        cnt, words, n = pairs(docs)
        matches = {f'{a}/{b}': cnt[frozenset((a, b))] for a, b, k in pp}
        n_match_pairs = sum(1 for v in matches.values() if v)
        rw = sum(1 for a, b, k in pp for w in (a, b) if words[w])
        out[name] = dict(couplets=n, pairs_matched=n_match_pairs,
                         pairs_matched_per1000couplets=1000.0 * n_match_pairs / max(1, n),
                         rhyme_words_seen_pct=100.0 * rw / (2 * len(pp)),
                         matches={k: v for k, v in matches.items() if v})
    out['poem_pairs'] = [f'{a}/{b} ({k})' for a, b, k in pp]
    return out

# ----------------------------------------------------------------------
def main(stages=None):
    stages = stages or ['describe', 'validate', 'gi_calib', 'attribute', 'markers']
    moore, liv, ctrl = load_all()
    print(f'loaded: moore {len(moore)} poems, livingston {len(liv)}, controls {len(ctrl)}')
    if 'describe' in stages:
        rows = describe(moore, liv, ctrl)
        json.dump(rows, open(os.path.join(OUT, 'describe.json'), 'w'), indent=1)
        for r in rows: print(r)
    if 'validate' in stages:
        allv = {}
        for ref in ('both', 'both_neutral', 'anapestic'):
            res, samples = validate(moore, liv, ctrl, reference=ref)
            allv[ref] = {k: {kk: vv for kk, vv in v.items() if kk != 'records'} for k, v in res.items()}
            allv[ref + '_records'] = {k: v['records'] for k, v in res.items()}
            print(f'--- validation reference={ref}, samples={len(samples)}')
            for k, v in res.items():
                print(f"{k:16s} acc={v['accuracy']:.3f} n={v['n']} ", {kk: round(vv['acc'], 2) for kk, vv in v['by_author_form'].items()})
        json.dump(allv, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=list)
    if 'gi_calib' in stages:
        g = gi_calibration(moore, liv, ctrl)
        json.dump(g, open(os.path.join(OUT, 'gi_calibration.json'), 'w'), indent=1, default=list)
        for fs, recs in g.items():
            for cand in (MOORE, LIV):
                t = [r['score'] for r in recs if r['candidate'] == cand and r['true']]
                f = [r['score'] for r in recs if r['candidate'] == cand and not r['true']]
                print(f'{fs} cand={cand}: true mean={np.mean(t):.2f} (n={len(t)}), false mean={np.mean(f):.2f} (n={len(f)})')
    if 'attribute' in stages:
        for which in ('1823', '1844'):
            try:
                poem = load_visit(which)
            except FileNotFoundError:
                print('no visit text for', which); continue
            r = attribute_poem(poem, moore, liv, ctrl)
            json.dump(r, open(os.path.join(OUT, f'attribute_{which}.json'), 'w'), indent=1)
            print(f'--- attribution of {which} text')
            for fs, rr in r.items():
                print(fs, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in rr.items() if k.startswith('gi_') and k != 'gi_controls_as_candidates'})
                print('   centroid both cosine:', {k: round(v, 3) for k, v in rr['centroid_both_cosine'].items()},
                      '| anapestic:', {k: round(v, 3) for k, v in rr.get('centroid_anapestic_cosine', {}).items()})
    if 'markers' in stages:
        poem = load_visit('1823')
        m = markers(poem, moore, liv, ctrl)
        json.dump(m, open(os.path.join(OUT, 'markers.json'), 'w'), indent=1)
        rr = rhyme_repertoire(poem, moore, liv, ctrl)
        json.dump(rr, open(os.path.join(OUT, 'rhymes.json'), 'w'), indent=1)
        for k, v in m.items():
            if v: print(k, {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk not in ('label',)})
        for k, v in rr.items():
            print(k, v if k == 'poem_pairs' else {kk: vv for kk, vv in v.items() if kk != 'matches'})

if __name__ == '__main__':
    main(sys.argv[1:] or None)
