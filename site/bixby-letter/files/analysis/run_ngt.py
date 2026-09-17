"""Run n-gram tracing experiments for a given design.
Usage: python3 run_ngt.py <design> [--nseq 10] [--loo] [--out results/<design>]
Designs are defined in designs.py and return:
  candidates: {name: [(id, text), ...]}
  tests: {setname: [(id, text, true_author_or_None), ...]}
"""
import sys, os, json, time, argparse, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ngt import Author, make_samplers, trace_attribute, word_count, ngram_types
import designs

NGRAM_TYPES = [('w', 1), ('w', 2), ('w', 3)] + [('c', n) for n in range(3, 17)]

def run(design_name, nseq, loo, out_dir, seed=0, types=NGRAM_TYPES, strip_punct=False, size_frac=0.95, test_sets=None):
    d = designs.get(design_name, strip_punct=strip_punct)
    if test_sets:
        d['tests'] = {k: v for k, v in d['tests'].items() if k in test_sets}
    authors = [Author(name, texts) for name, texts in d['candidates'].items()]
    sizes = {a.name: (len(a.ids), a.total_words) for a in authors}
    target = int(size_frac * min(a.total_words for a in authors))
    print(design_name, 'sizes', sizes, 'target', target, flush=True)
    samplers = make_samplers(authors, nseq, target, seed=seed)
    results = {'design': design_name, 'sizes': sizes, 'target_words': target, 'nseq': nseq, 'strip_punct': strip_punct, 'tests': {}}
    for level, n in types:
        t0 = time.time()
        for a in authors: a.prepare(level, n)
        for s in sum(samplers.values(), []): s.counter(level, n)
        key = f'{level}{n}'
        for setname, items in d['tests'].items():
            res_set = results['tests'].setdefault(setname, {})
            for tid, text, truth in items:
                excl = (truth, tid) if (loo and truth in d['candidates']) else None
                res, nq = trace_attribute(text, authors, level, n, samplers, exclude=excl)
                r = res_set.setdefault(tid, {'truth': truth, 'words': word_count(text), 'ngrams': {}, 'ntypes': {}})
                r['ngrams'][key] = res
                r['ntypes'][key] = nq
        print(f'  {key} done in {time.time()-t0:.1f}s', flush=True)
        for a in authors: a.clear()
        for s in sum(samplers.values(), []): s.counters = {}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'results.json'), 'w') as f:
        json.dump(results, f)
    return results

def summarize(results, vote_types=None):
    """Accuracy per n-gram type and by majority vote of char 4-10 (Grieve's aggregate)."""
    vote_types = vote_types or [f'c{n}' for n in range(4, 11)]
    out = {}
    for setname, items in results['tests'].items():
        keys = sorted({k for r in items.values() for k in r['ngrams']}, key=lambda k: (k[0], int(k[1:])))
        summ = {}
        for k in keys:
            per_author = {}
            for tid, r in items.items():
                res = r['ngrams'].get(k)
                if not res: continue
                best = max(res.values())
                winners = [a for a, v in res.items() if v == best]
                pred = winners[0] if len(winners) == 1 else 'tie'
                per_author.setdefault(r['truth'], []).append(pred)
            summ[k] = {t: {p: preds.count(p) for p in set(preds)} for t, preds in per_author.items()}
        # majority vote
        mv = {}
        for tid, r in items.items():
            votes = []
            for k in vote_types:
                res = r['ngrams'].get(k)
                if not res: continue
                best = max(res.values()); winners = [a for a, v in res.items() if v == best]
                votes.append(winners[0] if len(winners) == 1 else 'tie')
            if votes:
                from collections import Counter
                c = Counter(v for v in votes if v != 'tie')
                pred = c.most_common(1)[0][0] if c else 'tie'
                mv.setdefault(r['truth'], []).append(pred)
        summ['vote_c4-10'] = {t: {p: preds.count(p) for p in set(preds)} for t, preds in mv.items()}
        out[setname] = summ
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('design'); ap.add_argument('--nseq', type=int, default=10); ap.add_argument('--loo', action='store_true')
    ap.add_argument('--out', default=None); ap.add_argument('--strip-punct', action='store_true'); ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--types', default=None, help='comma list like w1,w2,c7')
    ap.add_argument('--tests', default=None, help='comma list of test set names, e.g. specials')
    a = ap.parse_args()
    types = NGRAM_TYPES
    if a.types:
        types = [(t[0], int(t[1:])) for t in a.types.split(',')]
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', a.design + ('_nopunct' if a.strip_punct else ''))
    res = run(a.design, a.nseq, a.loo, out, seed=a.seed, types=types, strip_punct=a.strip_punct, test_sets=a.tests.split(',') if a.tests else None)
    s = summarize(res)
    with open(os.path.join(out, 'summary.json'), 'w') as f: json.dump(s, f, indent=1)
    print(json.dumps(s, indent=1)[:6000])
