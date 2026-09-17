"""Driver for replicate.py: Jackson's word test, phoneme-pair test (re-derived on our
corpora with leave-one-poem-out), and expression rates with Poisson tails."""
import os, sys, json, math
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis, replicate, phon
from stylo import tokens, word_count, make_samples

MOORE, LIV = analysis.MOORE, analysis.LIV
OUT = analysis.OUT

def main(tag='base'):
    moore, liv, ctrl = analysis.load_all()
    poem = analysis.load_visit('1823')
    poem44 = analysis.load_visit('1844')
    res = {}
    # ---------- Jackson ch. 16 word lists, per 56-line sample
    sm = make_samples(moore, 56); sl = make_samples(liv, 56)
    rows = []
    for s in sm + sl:
        pct, n = replicate.jackson_words(tokens(s['text']))
        rows.append(dict(author=s['author'], form=s['form_class'], ids=s['ids'], pct=pct, n=n))
    pp, pn = replicate.jackson_words(tokens(poem['text']))
    res['jackson_words'] = dict(samples=rows, poem_1823=dict(pct=pp, n=pn),
                                poem_1844=dict(pct=replicate.jackson_words(tokens(poem44['text']))[0]))
    def summ(rows, a, f=None):
        v = [r['pct'] for r in rows if r['author'] == a and (f is None or r['form'] == f) and not math.isnan(r['pct'])]
        return dict(n=len(v), mean=float(np.mean(v)) if v else None, sd=float(np.std(v)) if v else None,
                    min=float(min(v)) if v else None, max=float(max(v)) if v else None)
    res['jackson_words_summary'] = {
        'moore_all': summ(rows, MOORE), 'moore_anap': summ(rows, MOORE, 'anapestic'),
        'liv_all': summ(rows, LIV), 'liv_anap': summ(rows, LIV, 'anapestic'), 'liv_other': summ(rows, LIV, 'other')}
    # ---------- phoneme pairs (Jackson chs. 10-12), re-derived with LOO
    for d in moore + liv + [poem]:
        d['_pairs'] = replicate.phoneme_pairs(d['verse_lines'])
    favL, favM = replicate.discriminating_pairs(liv, moore)
    res['phoneme_pairs_discriminating'] = dict(livingston_favoured=[' '.join(p) for p in favL],
                                               moore_favoured=[' '.join(p) for p in favM])
    prow = []
    for d in moore + liv:
        fl, fm = replicate.discriminating_pairs(liv, moore, exclude_ids={d['id']})
        share, n = replicate.phoneme_share(d['_pairs'], fl, fm)
        prow.append(dict(author=d['author'], form=d['form_class'], id=d['id'], share=share, n=n, words=word_count(d['text'])))
    ps, pn_ = replicate.phoneme_share(poem['_pairs'], favL, favM)
    res['phoneme_pairs'] = dict(poems=prow, poem_1823=dict(share=ps, n=pn_))
    def summ2(rows, a, f=None, min_n=12):
        v = [r['share'] for r in rows if r['author'] == a and (f is None or r['form'] == f) and r['n'] >= min_n and not math.isnan(r['share'])]
        return dict(n=len(v), mean=float(np.mean(v)) if v else None, sd=float(np.std(v)) if v else None,
                    min=float(min(v)) if v else None, max=float(max(v)) if v else None)
    res['phoneme_pairs_summary'] = {
        'moore_all': summ2(prow, MOORE), 'moore_anap': summ2(prow, MOORE, 'anapestic'),
        'liv_all': summ2(prow, LIV), 'liv_anap': summ2(prow, LIV, 'anapestic'), 'liv_other': summ2(prow, LIV, 'other')}
    # ---------- expressions
    corp = {
        'moore': '\n'.join(d['text'] for d in moore),
        'moore_anap': '\n'.join(d['text'] for d in moore if d['form_class'] == 'anapestic'),
        'livingston': '\n'.join(d['text'] for d in liv),
        'liv_anap': '\n'.join(d['text'] for d in liv if d['form_class'] == 'anapestic'),
        'controls_anap': '\n'.join(d['text'] for d in ctrl if d['form_class'] == 'anapestic'),
        'controls': '\n'.join(d['text'] for d in ctrl),
    }
    replicate.WORDS_POEM[0] = word_count(poem['text'])
    tab = replicate.expression_table(poem['text'], corp)
    res['expressions'] = tab
    llr8, det8 = replicate.loglik_ratio_expressions(tab, 'moore', 'livingston', list(replicate.NORSWORTHY_8))
    llr6, det6 = replicate.loglik_ratio_expressions(tab, 'moore', 'livingston', list(replicate.JACKSON_FAV))
    res['expressions_llr'] = dict(norsworthy8_log_lr_moore_vs_liv=llr8, norsworthy8_detail=det8,
                                  jackson6_log_lr_moore_vs_liv=llr6, jackson6_detail=det6)
    json.dump(res, open(os.path.join(OUT, f'replicate_{tag}.json'), 'w'), indent=1)
    # ---------- print
    print('Jackson words: poem', round(pp, 1), '| summary', json.dumps(res['jackson_words_summary']))
    print('Phoneme pairs L-fav:', res['phoneme_pairs_discriminating']['livingston_favoured'])
    print('Phoneme pairs M-fav:', res['phoneme_pairs_discriminating']['moore_favoured'])
    print('Phoneme share: poem', round(ps, 1), 'n', pn_, '| summary', json.dumps(res['phoneme_pairs_summary']))
    print('Expressions (obs | per-1000 moore, liv, moore_anap, liv_anap, controls_anap):')
    for k, row in tab.items():
        print(f"  {k:12s} obs={row['observed']:2d} | " + ' '.join(f"{lab}={row[lab]['per1000']:.2f}(p={row[lab]['p_tail']:.2g})" for lab in ('moore', 'livingston', 'moore_anap', 'liv_anap', 'controls_anap')))
    print('log LR (Moore vs Liv) Norsworthy8:', round(llr8, 2), det8)
    print('log LR (Moore vs Liv) Jackson6:', round(llr6, 2), det6)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'base')
