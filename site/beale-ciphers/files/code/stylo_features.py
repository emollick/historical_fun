#!/usr/bin/env python3
"""Punctuation and syntax habits, per 1000 words, for the Beale letters, the 1885 narrative,
Morriss's statement and every control sample (data/controls/samples).  Features are
heuristic (no parser): relativisers = which/who/whom/whose; infinitives = 'to' + a word that
cannot be a determiner/pronoun/adverb/noun-suffix; coordinators = and/but/or/nor; sentences
are split on . ! ? followed by a capital, with common abbreviations protected.
Writes results/stylo_features.csv, results/stylo_features_report.md and
results/stylo_features_summary.json (z-scores of the Beale texts against the controls and a
standardised-distance calibration like stylo_delta.py)."""
import os, re, csv, json, itertools, collections
import numpy as np
from scipy.stats import gaussian_kde, percentileofscore
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(B, 'data', 'controls', 'samples'); R = os.path.join(B, 'results')
man = list(csv.DictReader(open(os.path.join(B, 'data', 'controls', 'manifest.csv'))))
AUTHOR_OF = {'cooke_lee': 'cooke', 'poe_goldbug': 'poe', 'poe_letters': 'poe', 'twain_letters': 'twain'}
author = lambda k: AUTHOR_OF.get(k, k)
ABBR = ['Mr', 'Mrs', 'Dr', 'St', 'Mo', 'Va', 'Esq', 'No', 'Col', 'Gen', 'Capt', 'Lieut', 'Jr', 'Sr', 'Robt', 'Wm', 'Jan', 'Feb', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'vol', 'p', 'pp', 'i', 'e', 'viz', 'ult', 'inst']
NOT_INF = set('''the a an this that these those his her their my our your its him me us them it you which whom what some any all no every each such one two three four five six ten several many much more most few other another same own be'''.split())

def norm(t):
    return t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('—', ' -- ').replace('–', ' -- ')

def sentences(t):
    t = re.sub(r'&c\.', '&c', t)
    for a in ABBR: t = re.sub(r'\b' + a + r'\.', a + '<P>', t)
    t = re.sub(r'\b([A-Z])\.', r'\1<P>', t)              # initials  T. J. B.
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', t)
    parts = re.split(r'(?<=[.!?])["\')]?\s+(?=["\'(]?[A-Z0-9])', t)
    return [p.replace('<P>', '.') for p in parts if len(p.split()) >= 2]

def features(text):
    t = norm(text); words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", t); n = len(words); low = [w.lower() for w in words]
    per = lambda c: 1000 * c / n
    sents = sentences(t); sl = np.array([len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", s)) for s in sents])
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    pl = np.array([len(p.split()) for p in paras])
    inf = 0
    for i in range(len(low) - 1):
        if low[i] == 'to':
            nx = low[i + 1]
            if nx not in NOT_INF and not re.search(r'(ly|ness|tion|ment|ity|ance|ence|ship|ism|ist|ers|ors|ings|est)$', nx) and not nx.endswith("'s"):
                inf += 1
    f = {
        'words': n,
        'semicolons': per(t.count(';')), 'colons': per(len(re.findall(r':(?!\d)', t))), 'dashes': per(len(re.findall(r'--', t))),
        'parentheses': per(t.count('(')), 'commas': per(t.count(',')), 'exclamations': per(t.count('!')), 'questions': per(t.count('?')),
        'etc_&c': per(len(re.findall(r'&c', t))), 'quotation_marks': per(t.count('"')),
        'relativisers_which_who': per(sum(low.count(w) for w in ('which', 'who', 'whom', 'whose'))), 'which': per(low.count('which')), 'that': per(low.count('that')),
        'infinitives': per(inf), 'coordinators_and_but_or_nor': per(sum(low.count(w) for w in ('and', 'but', 'or', 'nor'))), 'and': per(low.count('and')),
        'however': per(low.count('however')), 'doubtless': per(low.count('doubtless')), 'upon': per(low.count('upon')), 'until': per(low.count('until')),
        'passive_be_+_ed': per(len(re.findall(r'\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en|wn|ne)\b', t.lower()))),
        # Pival-style features (as summarised in secondary sources): negative passives and 'untriggered' reflexives
        'negative_passive': per(len(re.findall(r"\b(?:not|never|no|nothing|none|nor|neither)\b(?:\s+\w+){0,3}?\s+(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en|wn|ne)\b|\b(?:is|are|was|were|be|been|being)\s+(?:not|never)\s+(?:\w+ly\s+)?\w+(?:ed|en|wn|ne)\b", t.lower()))),
        'never_or_not_to_be_+_participle': per(len(re.findall(r"\b(?:not|never)\s+to\s+be\s+\w+(?:ed|en|wn|ne)\b", t.lower()))),
        'reflexive_pronouns': per(sum(low.count(w) for w in ('myself', 'himself', 'herself', 'yourself', 'ourselves', 'themselves', 'itself'))),
        'untriggered_reflexives': per(len(re.findall(r"\b(?:than|like|as|and|or|for|from|to|with|by|of|regarding|besides|except|but|between|upon|on|in)\s+(?:myself|himself|herself|yourself|ourselves|themselves)\b", t.lower()))),
        'the_pct': 100 * low.count('the') / n, 'and_pct': 100 * low.count('and') / n, 'of_pct': 100 * low.count('of') / n,
        'sentence_len_mean': sl.mean(), 'sentence_len_sd': sl.std(ddof=1) if len(sl) > 1 else 0, 'sentence_len_median': float(np.median(sl)),
        'long_sentences_40plus_pct': 100 * (sl >= 40).mean(), 'paragraph_len_mean': pl.mean(), 'n_paragraphs': len(paras),
        'word_len_mean': np.mean([len(w) for w in words]), 'long_words_7plus_pct': 100 * np.mean([len(w) >= 7 for w in words]),
        'type_token_ratio_first1000': len(set(low[:1000])) / min(1000, n),
    }
    return f

rows = []
for m in man:
    txt = open(os.path.join(S, m['sample']), encoding='utf-8').read()
    f = features(txt); f.update(sample=m['sample'][:-4], author_key=m['author_key'], group=m['group'], genre=m['genre']); rows.append(f)
FEAT = [k for k in rows[0] if k not in ('sample', 'author_key', 'group', 'genre', 'words', 'n_paragraphs')]
with open(os.path.join(R, 'stylo_features.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['sample', 'author_key', 'group', 'genre', 'words', 'n_paragraphs'] + FEAT); w.writeheader(); w.writerows(rows)
ctrl = [r for r in rows if r['group'] != 'beale']; byname = {r['sample']: r for r in rows}
M = np.array([[r[f] for f in FEAT] for r in ctrl]); mu, sd = M.mean(0), M.std(0, ddof=1); sd[sd == 0] = 1
early = np.array([[r[f] for f in FEAT] for r in ctrl if r['group'] == 'early']); late = np.array([[r[f] for f in FEAT] for r in ctrl if r['group'] in ('late', 'mid')])
rep = ['# Punctuation and syntax habits (rates per 1000 words unless stated)\n',
       f'Controls: {len(ctrl)} samples. z = (value - control mean) / control sd. Beale texts: letters (3 letters, 2716 words), narrative (3954 words), Morriss statement (865 words).\n',
       '| feature | letters | narrative | Morriss | z letters | z narrative | controls mean (sd) | early 1805-46 mean | late 1858-1900 mean |', '|---|---|---|---|---|---|---|---|---|']
L, N, Mo = byname['beale_letters'], byname['narrative'], byname['morriss']
summary = {'features': {}}
for j, f in enumerate(FEAT):
    zl, zn = (L[f] - mu[j]) / sd[j], (N[f] - mu[j]) / sd[j]
    rep.append(f'| {f} | {L[f]:.1f} | {N[f]:.1f} | {Mo[f]:.1f} | {zl:+.1f} | {zn:+.1f} | {mu[j]:.1f} ({sd[j]:.1f}) | {early[:, j].mean():.1f} | {late[:, j].mean():.1f} |')
    summary['features'][f] = {'letters': L[f], 'narrative': N[f], 'morriss': Mo[f], 'z_letters': zl, 'z_narrative': zn, 'ctrl_mean': mu[j], 'ctrl_sd': sd[j], 'early_mean': early[:, j].mean(), 'late_mean': late[:, j].mean()}
# standardised distance in feature space (rates only, exclude counts): calibrate as in stylo_delta.py
USE = [f for f in FEAT if f not in ('type_token_ratio_first1000',)]
idx = [FEAT.index(f) for f in USE]
def vec(r): return (np.array([r[f] for f in USE]) - mu[idx]) / sd[idx]
def dist(a, b): return float(np.sqrt(((vec(a) - vec(b)) ** 2).mean()))
same, diff = [], []
for a, b in itertools.combinations(ctrl, 2):
    (same if author(a['author_key']) == author(b['author_key']) else diff).append(dist(a, b))
same, diff = np.array(same), np.array(diff); ks, kd = gaussian_kde(same), gaussian_kde(diff)
rep.append('\nStandardised Euclidean distance over these features (z-scored, RMS): calibration on control pairs.\n')
rep.append(f'Same-author pairs mean {same.mean():.3f} (sd {same.std(ddof=1):.3f}, n={len(same)}); different-author pairs mean {diff.mean():.3f} (sd {diff.std(ddof=1):.3f}, n={len(diff)}).\n')
rep.append('| pair | distance | %ile among diff-author pairs | %ile among same-author pairs | LR same:diff |\n|---|---|---|---|---|')
summary['pairs'] = {}
for a, b in [('beale_letters', 'narrative'), ('beale_letter1', 'narrative_A'), ('beale_letters', 'narrative_A'), ('beale_letters', 'narrative_B'), ('narrative_A', 'narrative_B'), ('morriss', 'narrative'), ('morriss', 'beale_letters')]:
    d = dist(byname[a], byname[b]); lr = float(ks(d)[0] / kd(d)[0])
    rep.append(f'| {a} vs {b} | {d:.3f} | {percentileofscore(diff, d, kind="weak"):.1f} | {percentileofscore(same, d, kind="weak"):.1f} | {lr:.2f} |')
    summary['pairs'][f'{a}|{b}'] = {'distance': d, 'pct_diff_closer': float((diff <= d).mean()), 'pct_same_closer': float((same <= d).mean()), 'LR': lr}
# nearest control samples to the letters and the narrative in this space
for t in ('beale_letters', 'narrative'):
    ds = sorted((dist(byname[t], r), r['sample']) for r in ctrl)
    rep.append(f'\nNearest control samples to {t} in feature space: ' + ', '.join(f'{k} ({d:.2f})' for d, k in ds[:6]))
    rep.append(f'Distance {t} to the other Beale text: ' + (f"{dist(byname['beale_letters'], byname['narrative']):.2f}"))
# per-feature agreement: for how many features do letters and narrative fall on the same side of the control median, and both beyond +-0.5 sd?
agree = [(f, summary['features'][f]['z_letters'], summary['features'][f]['z_narrative']) for f in USE]
both = [(f, a, b) for f, a, b in agree if abs(a) > 0.5 and abs(b) > 0.5 and np.sign(a) == np.sign(b)]
opp = [(f, a, b) for f, a, b in agree if abs(a) > 0.5 and abs(b) > 0.5 and np.sign(a) != np.sign(b)]
rep.append('\nFeatures where BOTH Beale texts deviate from the controls in the same direction (|z|>0.5): ' + ', '.join(f'{f} ({a:+.1f}/{b:+.1f})' for f, a, b in both))
rep.append('\nFeatures where they deviate in OPPOSITE directions (|z|>0.5): ' + ', '.join(f'{f} ({a:+.1f}/{b:+.1f})' for f, a, b in opp))
summary['shared_deviations'] = both; summary['opposite_deviations'] = opp
# how unusual are the shared habits?  number of control samples (and authors) reaching the lower of the two Beale rates
rep.append('\n| shared feature | letters | narrative | control samples >= min(letters,narr) | control authors with such a sample | which authors |\n|---|---|---|---|---|---|')
summary['rarity'] = {}
for f, a, b in both:
    lo = min(L[f], N[f]); hi_dir = a > 0
    ok = [r for r in ctrl if (r[f] >= lo if hi_dir else r[f] <= max(L[f], N[f]))]
    auths = sorted(set(author(r['author_key']) for r in ok))
    rep.append(f"| {f} | {L[f]:.1f} | {N[f]:.1f} | {len(ok)}/{len(ctrl)} | {len(auths)} | {', '.join(auths)[:120]} |")
    summary['rarity'][f] = {'n_samples': len(ok), 'authors': auths}
open(os.path.join(R, 'stylo_features_report.md'), 'w').write('\n'.join(rep) + '\n')
json.dump(summary, open(os.path.join(R, 'stylo_features_summary.json'), 'w'), indent=1, default=float)
print('\n'.join(rep))
