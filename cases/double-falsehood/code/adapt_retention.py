#!/usr/bin/env python3
"""For each adaptation scene, measure how much of the original play's wording it retains:
share of the scene's normalised word 4-grams that occur anywhere in the original play (whole-play set), and the same for 2-grams.
Output data/results/adapt_retention.json and a TSV."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *

def ngrams(toks, n):
    return set(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))

segs = load_segments()
plays, meta = play_tokens(segs)
orig_sets = {}
rows = []
for r in segs:
    if r['group'] != 'ADAPT': continue
    ok = r['note'].split('orig=')[1].split(' by ')[0]
    if any(o not in plays for o in ok.split('+')):
        rows.append({'key': r['key'], 'act': r['act'], 'scene': r['scene'], 'n_words': r['n_words'], 'orig': ok, 'ret4': None, 'ret2': None}); continue
    if ok not in orig_sets:
        s4 = set(); s2 = set()
        for o in ok.split('+'):
            s4 |= ngrams(plays[o], 4); s2 |= ngrams(plays[o], 2)
        orig_sets[ok] = (s4, s2)
    s4, s2 = orig_sets[ok]
    g4 = [tuple(r['tokens'][i:i + 4]) for i in range(len(r['tokens']) - 3)]
    g2 = [tuple(r['tokens'][i:i + 2]) for i in range(len(r['tokens']) - 1)]
    ret4 = sum(1 for g in g4 if g in s4) / max(1, len(g4)); ret2 = sum(1 for g in g2 if g in s2) / max(1, len(g2))
    rows.append({'key': r['key'], 'adapter': r['author'], 'date': r['date'], 'act': r['act'], 'scene': r['scene'], 'n_words': r['n_words'],
                 'n_verse_lines': r['n_verse_lines'], 'orig': ok, 'ret4': round(ret4, 4), 'ret2': round(ret2, 4)})
json.dump(rows, open('data/results/adapt_retention.json', 'w'), indent=1)
# play-level summary
from collections import defaultdict
agg = defaultdict(lambda: [0, 0.0, 0])
for x in rows:
    if x['ret4'] is None: continue
    a = agg[x['key']]; a[0] += x['n_words']; a[1] += x['ret4'] * x['n_words']; a[2] += 1
print(f"{'adaptation':32s} {'words':>6s} {'scenes':>6s} {'ret4':>6s}")
for k, a in sorted(agg.items(), key=lambda kv: -kv[1][1] / kv[1][0]):
    print(f"{k:32s} {a[0]:6d} {a[2]:6d} {a[1]/a[0]:6.3f}")
