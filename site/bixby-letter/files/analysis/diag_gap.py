"""Diagnose the gap between this report's register result (30 of 63 Lincoln pieces to Hay
under the 2019 design) and the blind rerun's (19 of 63): pool composition, sample rule,
number of sequences, seed. Runs this report's code on the register set and the special
texts only, under a chosen pool variant and sample rule.
Usage: python3 diag_gap.py <variant> --frac 0.95 --nseq 20 --seed 0
Variants: mine (this report's grieve-design pools), nodebates (mine without the Lapsley
debate-volume items), kept (mine restricted to the rerun's kept ids), theirs (the rerun's
pools.json exactly, its cleaned Lapsley texts included)."""
import sys, os, json, csv, argparse, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from ngt import Author, make_samplers, trace_attribute, word_count
import designs
from run_ngt import NGRAM_TYPES
RERUN = os.path.join(HERE, '..', 'independent-rerun')
TESTS = 'register'

def manifest_status():
    return {r['id']: r['status'] for r in csv.DictReader(open(RERUN + '/data/pools_manifest.csv'))}

def build(variant):
    d = designs.get('grieve')
    tests = {k: v for k, v in d['tests'].items() if k in ('register', 'specials')}
    cands = d['candidates']; st = manifest_status()
    if variant == 'mine': pass
    elif variant == 'nodebates':
        cands['lincoln'] = [(i, t) for i, t in cands['lincoln'] if 'debate' not in st.get(i, '')]
    elif variant == 'kept':
        cands['lincoln'] = [(i, t) for i, t in cands['lincoln'] if st.get(i) == 'kept']
    elif variant == 'theirs':
        raw = json.load(open(RERUN + '/data/pools.json'))
        cands = {'lincoln': [tuple(x) for x in raw['lincoln_pre1860']], 'hay': [tuple(x) for x in raw['hay_all']]}
    else: raise ValueError(variant)
    if TESTS == 'test4':
        # the rerun's own pieces (97 Lincoln, 76 Hay essay, 1 Hay condolence); the 185 pieces cut
        # from Hay's 1861-65 letters and diary are skipped because their parents are pool texts
        P = json.load(open(RERUN + '/data/test4_pieces.json'))
        keep = [p for p in P if p['group'] in ('lincoln_matched', 'hay_essay', 'hay_condolence')]
        docs = {p['doc'] for p in keep}
        for c in cands:
            cands[c] = [(i, t) for i, t in cands[c] if i not in docs]
        tests['register'] = [(p['id'], p['text'], p['author']) for p in keep]
    return cands, tests

def vote(res, lo=4, hi=10):
    c = Counter()
    for n in range(lo, hi + 1):
        o = res['ngrams'][f'c{n}']; d = o['lincoln'] - o['hay']
        c['lincoln' if d > 0 else 'hay' if d < 0 else 'tie'] += 1
    return c

def vote17(res):
    c = Counter()
    for lv, n in NGRAM_TYPES:
        o = res['ngrams'][f'{lv}{n}']; d = o['lincoln'] - o['hay']
        c['lincoln' if d > 0 else 'hay' if d < 0 else 'tie'] += 1
    return c

def summarize(results):
    reg = results['tests']['register']; sp = results['tests']['specials']
    out = {}
    for author in ('lincoln', 'hay'):
        items = {k: v for k, v in reg.items() if v['truth'] == author}
        wrong = []; ties = 0; wrong17 = 0
        for k, v in items.items():
            c = vote(v); nl, nh = c['lincoln'], c['hay']
            if nl == nh: ties += 1
            elif (nl > nh) != (author == 'lincoln'): wrong.append(f'{k} L{nl}/H{nh}')
            c17 = vote17(v)
            if (c17['lincoln'] > c17['hay']) != (author == 'lincoln'): wrong17 += 1
        acc = {}
        for lv, n in NGRAM_TYPES:
            key = f'{lv}{n}'
            ok = [((v['ngrams'][key]['lincoln'] - v['ngrams'][key]['hay']) > 0) == (author == 'lincoln') for v in items.values()]
            acc[key] = round(sum(ok) / len(ok), 3)
        out[author] = {'n': len(items), 'wrong_c4_10': len(wrong), 'ties': ties, 'wrong_all17': wrong17, 'wrong_ids': wrong, 'acc': acc}
    b = sp['bixby']; c = vote(b); c17 = vote17(b)
    out['bixby'] = {'c4_10': dict(c), 'all17': dict(c17), 'margins': {f'{lv}{n}': round(b['ngrams'][f'{lv}{n}']['lincoln'] - b['ngrams'][f'{lv}{n}']['hay'], 4) for lv, n in NGRAM_TYPES}}
    out['specials'] = {k: {'truth': v['truth'], 'c4_10': dict(vote(v)), 'all17': dict(vote17(v))} for k, v in sp.items()}
    return out

def run(variant, frac, nseq, seed, out, target=None):
    cands, tests = build(variant)
    authors = [Author(n, t) for n, t in cands.items()]
    target = target or int(frac * min(a.total_words for a in authors))
    sizes = {a.name: (len(a.ids), a.total_words) for a in authors}
    print(variant, 'sizes', sizes, 'frac', frac, 'nseq', nseq, 'seed', seed, 'target', target, flush=True)
    samplers = make_samplers(authors, nseq, target, seed=seed)
    results = {'variant': variant, 'frac': frac, 'nseq': nseq, 'seed': seed, 'sizes': sizes, 'target_words': target, 'tests': {}}
    for level, n in NGRAM_TYPES:
        t0 = time.time()
        for a in authors: a.prepare(level, n)
        for s in sum(samplers.values(), []): s.counter(level, n)
        key = f'{level}{n}'
        for setname, items in tests.items():
            rs = results['tests'].setdefault(setname, {})
            for tid, text, truth in items:
                res, nq = trace_attribute(text, authors, level, n, samplers)
                r = rs.setdefault(tid, {'truth': truth, 'words': word_count(text), 'ngrams': {}, 'ntypes': {}})
                r['ngrams'][key] = res; r['ntypes'][key] = nq
        for a in authors: a.clear()
        for s in sum(samplers.values(), []): s.counters = {}
        print(f'  {key} done in {time.time()-t0:.1f}s', flush=True)
    json.dump(results, open(out, 'w'))
    s = summarize(results)
    json.dump(s, open(out.replace('.json', '_summary.json'), 'w'), indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'acc'} if k in ('lincoln', 'hay') else v for k, v in s.items() if k != 'specials'}, indent=1))
    return s

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('variant'); ap.add_argument('--frac', type=float, default=0.95)
    ap.add_argument('--nseq', type=int, default=20); ap.add_argument('--seed', type=int, default=0); ap.add_argument('--out', default=None)
    ap.add_argument('--target', type=int, default=None, help='sample size in words, overriding frac (to separate pool composition from sample size)')
    ap.add_argument('--tests', default='register', choices=['register', 'test4'])
    a = ap.parse_args()
    TESTS = a.tests
    tag = ('_test4' if a.tests == 'test4' else '') + (f'_t{a.target}' if a.target else '')
    out = a.out or os.path.join(HERE, 'results', 'diag', f'{a.variant}_f{int(round(a.frac*100)):03d}_n{a.nseq}_s{a.seed}{tag}.json')
    run(a.variant, a.frac, a.nseq, a.seed, out, target=a.target)
