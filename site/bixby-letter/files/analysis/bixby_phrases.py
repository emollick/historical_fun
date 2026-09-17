"""Interpretable view of the n-gram evidence: which strings and words of the Bixby letter
occur in Lincoln's own-hand writing of 1860-65, in all of Lincoln's autograph writing, in
Hay's 1860-65 letters and diary, and in all of Hay's writing."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designs
from ngt import char_ngrams, word_ngrams
from collections import Counter

L = designs.load_lincoln(); H = designs.load_hay()
pools = {
  'lincoln_own_1860_65': [r['text'] for r in designs.lincoln_war_own(L)],
  'lincoln_autograph_all': [r['text'] for r in L if r['autograph'] and not r['hay_hand']],
  'lincoln_pre1860_lapsley_gap': [r['text'] for r in designs.lincoln_pre1860(L)] + [r['text'] for r in designs.lapsley_gap()],
  'hay_1860_65': [r['text'] for r in designs.hay_war(H)],
  'hay_all': [r['text'] for r in H],
}
ex = set(designs.get('ownhand')['excluded'])
# remove copies of the letter and of special test texts (e.g. the Basler printing of the letter itself)
bix = designs.SPECIALS['bixby']['text']
def norm(t): return re.sub(r'\s+', ' ', t.lower())
words = {k: sum(len(t.split()) for t in v) for k, v in pools.items()}
print('pool words', words)
big = {k: norm(' \n '.join(v)) for k, v in pools.items()}
# 1. long character n-grams of the letter found in each pool
out = {'ngrams': {}, 'words': {}}
for n in [10, 12, 14, 16]:
    grams = char_ngrams(bix, n)
    found = {}
    for g in sorted(grams):
        hit = [k for k in pools if g in big[k]]
        if hit: found[g] = hit
    out['ngrams'][n] = found
    print(f"\n=== {n}-char strings of the letter found in any pool: {len(found)} of {len(grams)}")
    only_l = [g for g, h in found.items() if all(k.startswith('lincoln') for k in h)]
    only_h = [g for g, h in found.items() if all(k.startswith('hay') for k in h)]
    print(f"  only in Lincoln pools ({len(only_l)}):", only_l[:60])
    print(f"  only in Hay pools ({len(only_h)}):", only_h[:60])
# 2. words of the letter: rate per 100k words in each pool
stop = set('a an the and or but of to in on at by for from with as is was were be been being that this these those it its he she they them his her their i you your my me we our us have has had do does did not no so if than then there here which who whom what when where while very more most such may might can could shall should will would'.split())
toks = re.findall(r"[a-z']+", bix.lower())
rates = {}
for w in sorted(set(toks)):
    if w in stop or len(w) < 3: continue
    rates[w] = {k: round(100000 * len(re.findall(r'\b' + re.escape(w) + r'\b', big[k])) / words[k], 1) for k in pools}
out['words'] = rates
print("\n=== letter words, occurrences per 100k words:", list(pools))
for w, r in rates.items():
    print(f"  {w:14s}", ' '.join(f"{r[k]:7.1f}" for k in pools))
# 3. specific habits
for pat in ['can not', 'cannot', 'to-day', 'today', 'heavenly father', 'father in heaven', 'i cannot refrain', 'i can not refrain', 'so costly', 'altar of', 'solemn pride', 'loved and lost', 'to assuage', 'beguile', 'cherished', 'tender', 'consolation', 'anguish', 'bereavement', 'gloriously', 'sacrifice', 'weak and fruitless', 'attempt to']:
    print(f"  {pat:20s}", ' '.join(f"{len(re.findall(re.escape(pat), big[k])):6d}" for k in pools))
json.dump(out, open('results/bixby_phrases.json', 'w'), indent=1)
