"""Find Lincoln texts present both in Basler (transcribed from the autograph manuscript,
with Lincoln's own spelling and punctuation) and in Lapsley's 1905-06 edition (normalised
print), so the effect of the edition on the n-gram margins can be measured on identical words."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designs
from ngt import char_ngrams, word_count
from build_register import clean_lapsley, clean_basler

L = [r for r in designs.load_lincoln() if r['autograph'] and not r['hay_hand'] and r['wc'] >= 90 and r['_date'] and r['_date'].year >= 1860]
lap = [json.loads(l) for l in open('lapsley.jsonl')]
lap = [r for r in lap if r['nwords'] >= 90 and r.get('date') and r['date'][:4] in ('1860', '1861', '1863', '1864', '1865')]
print(len(L), 'basler autograph >=90w 1860+;', len(lap), 'lapsley >=90w')
lsets = [(r, char_ngrams(r['text'], 8)) for r in L]
pairs = {}
for r in lap:
    g = char_ngrams(r['text'], 8)
    best = None
    for b, bs in lsets:
        inter = len(g & bs); ov = inter / min(len(g), len(bs))
        if ov >= 0.55 and (best is None or ov > best[1]): best = (b, ov)
    if best:
        b, ov = best
        wb, wl = word_count(b['text']), r['nwords']
        if min(wb, wl) / max(wb, wl) < 0.7: continue  # only whole-text matches
        pairs[r['id']] = (b, ov)
out = {}
for lid, (b, ov) in pairs.items():
    lr = next(x for x in lap if x['id'] == lid)
    tb = clean_basler(b['text']); tl = clean_lapsley(lr['text'])
    if word_count(tb) < 90 or word_count(tl) < 90: continue
    out[f'basler:{b["id"]}'] = {'author': 'lincoln', 'edition': 'basler', 'pair': lid, 'label': b.get('heading'), 'text': tb, 'parents': [b['id']], 'overlap': round(ov, 2)}
    out[f'lapsley:{lid}'] = {'author': 'lincoln', 'edition': 'lapsley', 'pair': b['id'], 'label': lr.get('heading'), 'text': tl, 'parents': [b['id']]}
json.dump(out, open('tests_paired.json', 'w'), indent=1)
print(len(out) // 2, 'pairs')
for k, v in out.items():
    if k.startswith('basler:'): print(k, v['pair'], v['overlap'], word_count(v['text']), (v['label'] or '')[:50])
