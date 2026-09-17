#!/usr/bin/env python3
"""Burrows's Delta / Cosine Delta on most-frequent words, and character 4-gram profiles,
for the Beale letters, the anonymous 1885 narrative, Morriss's quoted statement and Poe
against a control corpus of American authors (data/controls/samples, manifest.csv).

Outputs (results/):
  stylo_delta_distances_<method>.csv   full distance matrices
  stylo_delta_summary.json             key numbers (Beale pairs, calibration, LOO accuracy)
  stylo_delta_report.md                human-readable tables (nearest neighbours etc.)
  stylo_delta_calibration.svg          same-author vs different-author distance densities
  stylo_delta_mds.svg                  2-D classical MDS map of all samples
Z-scores are computed on the control samples only (the Beale texts do not influence the
standardisation).  "Same author" pairs are two different samples of one control author;
"different author" pairs are samples of two different control authors."""
import os, re, csv, json, math, itertools, collections
import numpy as np
from scipy.stats import gaussian_kde, percentileofscore
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(B, 'data', 'controls', 'samples'); R = os.path.join(B, 'results')
man = list(csv.DictReader(open(os.path.join(B, 'data', 'controls', 'manifest.csv'))))
AUTHOR_OF = {'cooke_lee': 'cooke', 'poe_goldbug': 'poe', 'poe_letters': 'poe', 'twain_letters': 'twain'}
def author(key): return AUTHOR_OF.get(key, key)

def tokens(text):
    text = text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    text = text.replace('&c.', ' &c ').replace('&c', ' &c ')
    return re.findall(r"[a-z]+(?:'[a-z]+)?|&c", text.lower())

def char_ngrams(text, n=4):
    t = re.sub(r'\s+', ' ', text.replace('’', "'").replace('“', '"').replace('”', '"').lower())
    return [t[i:i+n] for i in range(len(t) - n + 1)]

texts = {}; meta = {}
for row in man:
    txt = open(os.path.join(S, row['sample']), encoding='utf-8').read()
    key = row['sample'][:-4]
    texts[key] = txt; meta[key] = row
controls = [k for k in texts if meta[k]['group'] not in ('beale',)]
beale_keys = [k for k in texts if meta[k]['group'] == 'beale']
# length-matched versions of the Beale texts (first 2000 words, like the controls)
def first_n_words(txt, n=2000):
    ws = txt.split(); return ' '.join(ws[:n])
for k in ['beale_letters', 'narrative']:
    texts[k + '_2000'] = first_n_words(texts[k]); meta[k + '_2000'] = dict(meta[k], sample=k + '_2000.txt', title=meta[k]['title'] + ' (first 2000 words)')
beale_keys += ['beale_letters_2000', 'narrative_2000']
keys = controls + beale_keys

word_counts = {k: collections.Counter(tokens(texts[k])) for k in keys}
char_counts = {k: collections.Counter(char_ngrams(texts[k])) for k in keys}
lengths = {k: sum(word_counts[k].values()) for k in keys}

def rel_matrix(counts, feats):
    M = np.zeros((len(keys), len(feats)))
    for i, k in enumerate(keys):
        tot = sum(counts[k].values())
        for j, f in enumerate(feats): M[i, j] = counts[k][f] / tot
    return M

def zscore(M, ref_idx):
    mu = M[ref_idx].mean(0); sd = M[ref_idx].std(0, ddof=1); sd[sd == 0] = 1
    return (M - mu) / sd

def burrows(Z): return np.abs(Z[:, None, :] - Z[None, :, :]).mean(2)
def cosine(Z):
    n = np.linalg.norm(Z, axis=1); n[n == 0] = 1
    return 1 - (Z @ Z.T) / np.outer(n, n)

ctrl_idx = [keys.index(k) for k in controls]
ctrl_word_tot = collections.Counter()
for k in controls: ctrl_word_tot.update(word_counts[k])
ctrl_char_tot = collections.Counter()
for k in controls: ctrl_char_tot.update(char_counts[k])

methods = {}
for N in (100, 150, 200, 300, 500):
    feats = [w for w, _ in ctrl_word_tot.most_common(N)]
    Z = zscore(rel_matrix(word_counts, feats), ctrl_idx)
    methods[f'burrows_delta_{N}mfw'] = burrows(Z)
    methods[f'cosine_delta_{N}mfw'] = cosine(Z)
PRON = set('i me my mine myself you your yours yourself he him his himself she her hers herself we us our ours ourselves they them their theirs themselves it its itself'.split())
for N in (200, 300):
    feats = [w for w, _ in ctrl_word_tot.most_common(N + 40) if w not in PRON][:N]
    Z = zscore(rel_matrix(word_counts, feats), ctrl_idx)
    methods[f'cosine_delta_{N}mfw_nopronouns'] = cosine(Z)
FUNCTION_WORDS = set('''the of and to a in that it is was i for be as with his he by on at not this which have from or are but had were you my an all so their they one we been will if more no her its them would there our when who what has him me your do than any some into can may should these could up then now out very only such upon other those us shall must did might over after also being here where how well before too again those most much through both same own ever never yet still each while about against because under between since without against thus hence whether either neither nor though although until unless even indeed perhaps quite rather almost always often sometimes soon already once whose whom myself himself themselves itself yourself ourselves another every few many less least far further last first next several whatever whenever wherever off down back away along across among within around during above below near till'''.split())
ffeats = [w for w, _ in ctrl_word_tot.most_common(3000) if w in FUNCTION_WORDS][:150]
Zf = zscore(rel_matrix(word_counts, ffeats), ctrl_idx)
methods['cosine_delta_function_words_150'] = cosine(Zf)
methods['burrows_delta_function_words_150'] = burrows(Zf)
FEATS_FOR_CONTRIB = ffeats; Z_FOR_CONTRIB = Zf
cfeats = [c for c, _ in ctrl_char_tot.most_common(2000)]
Zc = zscore(rel_matrix(char_counts, cfeats), ctrl_idx)
methods['cosine_delta_char4gram_2000'] = cosine(Zc)
Mc = rel_matrix(char_counts, cfeats)
methods['cosine_raw_char4gram_2000'] = cosine(Mc)

def pairs_ctrl(D):
    same, diff, same_x, diff_x = [], [], [], []   # _x: cross-genre pairs (letters vs non-letters)
    for a, b in itertools.combinations(controls, 2):
        d = D[keys.index(a), keys.index(b)]
        xg = (meta[a]['genre'] == 'letters') != (meta[b]['genre'] == 'letters')
        if author(meta[a]['author_key']) == author(meta[b]['author_key']):
            same.append(d); (same_x.append(d) if xg else None)
        else:
            diff.append(d); (diff_x.append(d) if xg else None)
    return np.array(same), np.array(diff), np.array(same_x), np.array(diff_x)

def loo_accuracy(D):
    hits = 0; n = 0
    for a in controls:
        if sum(1 for b in controls if author(meta[b]['author_key']) == author(meta[a]['author_key'])) < 2: continue
        i = keys.index(a); best = None; bd = 1e9
        for b in controls:
            if b == a: continue
            d = D[i, keys.index(b)]
            if d < bd: bd, best = d, b
        n += 1; hits += author(meta[best]['author_key']) == author(meta[a]['author_key'])
    return hits / n, n

BEALE_PAIRS = [('beale_letters', 'narrative'), ('beale_letters_2000', 'narrative_2000'), ('beale_letter1', 'narrative_2000'),
               ('beale_letters', 'narrative_A'), ('beale_letters', 'narrative_B'), ('narrative_A', 'narrative_B'),
               ('morriss', 'narrative'), ('morriss', 'beale_letters'), ('beale_b2', 'narrative'), ('beale_b2', 'beale_letters')]

summary = {'n_control_samples': len(controls), 'n_control_authors': len(set(author(meta[k]['author_key']) for k in controls)),
           'lengths': {k: lengths[k] for k in beale_keys}, 'methods': {}}
report = ['# Stylometric distances: Beale letters vs. the 1885 narrative, calibrated on control authors\n',
          f'Control corpus: {len(controls)} samples from {summary["n_control_authors"]} authors (see data/controls/manifest.csv). '
          'Z-scores computed on control samples only. Distances: Burrows Delta = mean |z-difference|; Cosine Delta = cosine distance between z-vectors.\n']
for name, D in methods.items():
    same, diff, same_x, diff_x = pairs_ctrl(D)
    acc, n_acc = loo_accuracy(D)
    kde_s = gaussian_kde(same); kde_d = gaussian_kde(diff)
    entry = {'loo_nn_accuracy': acc, 'loo_n': n_acc, 'same_author_pairs': len(same), 'diff_author_pairs': len(diff),
             'same_mean': float(same.mean()), 'same_sd': float(same.std(ddof=1)), 'diff_mean': float(diff.mean()), 'diff_sd': float(diff.std(ddof=1)),
             'cross_genre_same_mean': float(same_x.mean()) if len(same_x) else None, 'cross_genre_diff_mean': float(diff_x.mean()) if len(diff_x) else None,
             'pairs': {}}
    report.append(f'\n## {name}\n\nLeave-one-out nearest-neighbour attribution accuracy on controls: {acc:.2f} (n={n_acc}). '
                  f'Same-author pairs: mean {same.mean():.3f} (sd {same.std(ddof=1):.3f}, n={len(same)}); different-author pairs: mean {diff.mean():.3f} (sd {diff.std(ddof=1):.3f}, n={len(diff)}). '
                  + (f'Cross-genre (letters vs other) different-author mean {diff_x.mean():.3f} (n={len(diff_x)}); cross-genre same-author mean {same_x.mean():.3f} (n={len(same_x)}).\n' if len(same_x) else '\n'))
    report.append('| pair | distance | z vs diff-author | %ile among diff-author pairs | %ile among same-author pairs | P(diff-author pair this close) | LR same:diff (KDE) |\n|---|---|---|---|---|---|---|')
    for a, b in BEALE_PAIRS:
        d = float(D[keys.index(a), keys.index(b)])
        p_diff = float((diff <= d).mean()); p_same = float((same <= d).mean())
        lr = float(kde_s(d)[0] / kde_d(d)[0]) if kde_d(d)[0] > 0 else float('inf')
        z = (d - diff.mean()) / diff.std(ddof=1)
        entry['pairs'][f'{a}|{b}'] = {'distance': d, 'z_vs_diff': float(z), 'pct_diff_pairs_closer': p_diff, 'pct_same_pairs_closer': p_same, 'LR_same_vs_diff': lr}
        report.append(f'| {a} vs {b} | {d:.3f} | {z:+.2f} | {percentileofscore(diff, d, kind="weak"):.1f} | {percentileofscore(same, d, kind="weak"):.1f} | {p_diff:.3f} | {lr:.2f} |')
    # author-level bootstrap: resample control authors with replacement, recompute the share of different-author
    # pairs at least as close as the length-matched Beale pair (95% interval)
    rng = np.random.default_rng(0); auths_all = sorted(set(author(meta[k]['author_key']) for k in controls))
    d_pair = float(D[keys.index('beale_letters_2000'), keys.index('narrative_2000')]); boots = []
    for _ in range(300):
        pick = rng.choice(auths_all, size=len(auths_all), replace=True)
        samp = [k for a in pick for k in controls if author(meta[k]['author_key']) == a]
        vals = [D[keys.index(x), keys.index(y)] for x, y in itertools.combinations(samp, 2) if author(meta[x]['author_key']) != author(meta[y]['author_key'])]
        boots.append(np.mean(np.array(vals) <= d_pair))
    entry['bootstrap_pct_diff_pairs_closer_lengthmatched'] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
    report.append(f'\nAuthor-level bootstrap (300 resamples of the control authors): share of different-author pairs at least as close as the length-matched Beale pair = {np.mean(boots):.3f} (95% interval {np.percentile(boots, 2.5):.3f}-{np.percentile(boots, 97.5):.3f}).')
    # nearest neighbours of the test texts
    report.append('\nNearest neighbours (5 closest samples; distance, z within the row over control samples):\n')
    for t in ['beale_letters', 'narrative', 'morriss', 'beale_letter1', 'poe_goldbug_1', 'poe_letters_1']:
        if t not in keys: continue
        i = keys.index(t); row = D[i]
        others = [(row[keys.index(k)], k) for k in controls + beale_keys if k != t and not (t.startswith('narrative') and k.startswith('narrative')) and not (t.startswith('beale_letter') and k.startswith('beale_letter'))]
        others.sort()
        cd = np.array([row[keys.index(k)] for k in controls if k != t])
        nn = ', '.join(f'{k} ({d:.3f}, z={(d-cd.mean())/cd.std(ddof=1):+.2f})' for d, k in others[:5])
        report.append(f'- **{t}**: {nn}')
        entry.setdefault('nearest', {})[t] = [(k, float(d)) for d, k in others[:5]]
    # nearest author centroids (mean distance to each author's samples) for the test texts
    auths = sorted(set(author(meta[k]['author_key']) for k in controls))
    report.append('\nNearest authors (mean distance to that author\'s control samples; the narrative is included as a candidate author for the letters):\n')
    for t in ['beale_letters', 'beale_letters_2000', 'narrative', 'morriss']:
        i = keys.index(t)
        cand = {a: float(np.mean([D[i, keys.index(k)] for k in controls if author(meta[k]['author_key']) == a])) for a in auths}
        if t.startswith('beale') or t == 'morriss': cand['NARRATIVE(1885)'] = float(np.mean([D[i, keys.index(k)] for k in ('narrative_A', 'narrative_B')]))
        if t.startswith('narrative'): cand['BEALE LETTERS'] = float(D[i, keys.index('beale_letters')])
        ranked = sorted(cand.items(), key=lambda x: x[1])
        report.append(f'- **{t}**: ' + ', '.join(f'{a} {d:.3f}' for a, d in ranked[:6]))
        entry.setdefault('nearest_authors', {})[t] = ranked[:8]
    # period classification by style: mean distance to early (1805-1846) vs late (1858-1900) control samples
    def period_scores(i, exclude_author=None):
        e = [D[i, keys.index(k)] for k in controls if meta[k]['group'] == 'early' and author(meta[k]['author_key']) != exclude_author]
        l = [D[i, keys.index(k)] for k in controls if meta[k]['group'] in ('late', 'mid') and author(meta[k]['author_key']) != exclude_author]
        return float(np.mean(e)), float(np.mean(l))
    hits = n = 0
    for k in controls:
        if meta[k]['group'] not in ('early', 'late'): continue
        e, l = period_scores(keys.index(k), author(meta[k]['author_key']))
        n += 1; hits += (e < l) == (meta[k]['group'] == 'early')
    entry['period_classification_accuracy_controls'] = hits / n
    report.append(f'\nStyle-based period classification (nearest period by mean distance, author held out): accuracy on controls {hits/n:.2f} (n={n}).')
    for t in ['beale_letters', 'beale_letters_2000', 'beale_letter1', 'narrative', 'morriss']:
        e, l = period_scores(keys.index(t)); entry.setdefault('period', {})[t] = {'mean_dist_early': e, 'mean_dist_late': l}
        report.append(f'- {t}: mean distance to 1805-1846 samples {e:.3f}, to 1858-1900 samples {l:.3f} -> looks {"EARLY" if e < l else "LATE"} (diff {l-e:+.3f})')
    summary['methods'][name] = entry
    with open(os.path.join(R, f'stylo_delta_distances_{name}.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow([''] + keys)
        for i, k in enumerate(keys): w.writerow([k] + [f'{x:.4f}' for x in D[i]])

# which function words make the letters and the narrative alike?  Contribution to the cosine
# similarity of z-vectors: z_letters[w] * z_narr[w] (both far from the control mean in the same direction).
i, j = keys.index('beale_letters'), keys.index('narrative')
contrib = sorted([(Z_FOR_CONTRIB[i, f] * Z_FOR_CONTRIB[j, f], w, Z_FOR_CONTRIB[i, f], Z_FOR_CONTRIB[j, f]) for f, w in enumerate(FEATS_FOR_CONTRIB)], reverse=True)
report.append('\n## Function words that make the Beale letters and the narrative alike (150 function words; z-scores vs control samples)\n')
report.append('| word | z letters | z narrative | product |\n|---|---|---|---|')
for c, w, za, zb in contrib[:25]: report.append(f'| {w} | {za:+.2f} | {zb:+.2f} | {c:.2f} |')
report.append('\nFunction words where they differ most (opposite signs):\n\n| word | z letters | z narrative | product |\n|---|---|---|---|')
for c, w, za, zb in contrib[-12:]: report.append(f'| {w} | {za:+.2f} | {zb:+.2f} | {c:.2f} |')
summary['function_word_contributions_top'] = [(w, float(za), float(zb), float(c)) for c, w, za, zb in contrib[:25]]
# genre-matched period test: Beale letters vs letter-genre controls only
D = methods['cosine_delta_function_words_150']
early_letters = [k for k in controls if meta[k]['genre'] == 'letters' and meta[k]['group'] == 'early']
late_letters = [k for k in controls if meta[k]['genre'] == 'letters' and meta[k]['group'] in ('late', 'poe')]
report.append('\n## Genre-matched period test (function words): mean distance of each text to letter-genre controls only\n')
report.append(f'Early letters: {sorted(set(meta[k]["author_key"] for k in early_letters))}; late letters: {sorted(set(meta[k]["author_key"] for k in late_letters))}\n')
for t in ['beale_letters', 'beale_letters_2000', 'narrative', 'morriss']:
    e = float(np.mean([D[keys.index(t), keys.index(k)] for k in early_letters])); l = float(np.mean([D[keys.index(t), keys.index(k)] for k in late_letters]))
    report.append(f'- {t}: to early letters {e:.3f}, to late letters {l:.3f} ({"EARLY" if e < l else "LATE"}, diff {l-e:+.3f})')
    summary.setdefault('genre_matched_period', {})[t] = {'early_letters': e, 'late_letters': l}
hits = n = 0
for k in early_letters + late_letters:
    a = author(meta[k]['author_key'])
    e = np.mean([D[keys.index(k), keys.index(x)] for x in early_letters if author(meta[x]['author_key']) != a])
    l = np.mean([D[keys.index(k), keys.index(x)] for x in late_letters if author(meta[x]['author_key']) != a])
    n += 1; hits += (e < l) == (k in early_letters)
report.append(f'- control accuracy of this letters-only period test (author held out): {hits/n:.2f} (n={n})')
summary['genre_matched_period']['control_accuracy'] = hits / n
json.dump(summary, open(os.path.join(R, 'stylo_delta_summary.json'), 'w'), indent=1)
open(os.path.join(R, 'stylo_delta_report.md'), 'w').write('\n'.join(report) + '\n')

# ---- figures
D = methods['cosine_delta_200mfw']; same, diff, same_x, diff_x = pairs_ctrl(D)
fig, ax = plt.subplots(figsize=(7.5, 4.2))
xs = np.linspace(0, max(diff.max(), same.max()) * 1.05, 400)
ax.plot(xs, gaussian_kde(same)(xs), color='#2a7f62', lw=2, label=f'same author, different samples (n={len(same)})')
ax.plot(xs, gaussian_kde(diff)(xs), color='#8a6d3b', lw=2, label=f'different authors (n={len(diff)})')
for (a, b), col, ls in [(('beale_letters', 'narrative'), '#b3261e', '-'), (('beale_letters_2000', 'narrative_2000'), '#b3261e', '--'), (('narrative_A', 'narrative_B'), '#444', ':'), (('morriss', 'narrative'), '#7a4db8', '-.')]:
    d = D[keys.index(a), keys.index(b)]; ax.axvline(d, color=col, ls=ls, lw=1.5, label=f'{a} vs {b}: {d:.2f}')
ax.set_xlabel('Cosine Delta distance (200 most frequent words)'); ax.set_ylabel('density'); ax.legend(fontsize=7.5, loc='upper left'); ax.set_title('Calibration of the Beale-letters / narrative distance', fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(R, 'stylo_delta_calibration.svg')); plt.close(fig)

# classical MDS
n = len(keys); J = np.eye(n) - np.ones((n, n)) / n; Bm = -0.5 * J @ (D ** 2) @ J
w, v = np.linalg.eigh(Bm); idx = np.argsort(w)[::-1][:2]; X = v[:, idx] * np.sqrt(np.maximum(w[idx], 0))
fig, ax = plt.subplots(figsize=(9, 7))
groups = {'early': '#2a6fdb', 'mid': '#888', 'late': '#c98a1b', 'poe': '#1a9e6e', 'beale': '#b3261e'}
for i, k in enumerate(keys):
    g = meta[k]['group']; ax.scatter(X[i, 0], X[i, 1], s=18 if g != 'beale' else 60, color=groups[g], alpha=0.8, marker='o' if g != 'beale' else '*')
    if g == 'beale' or k.endswith('_1') or k.startswith('poe'): ax.annotate(k, (X[i, 0], X[i, 1]), fontsize=6.5, xytext=(3, 2), textcoords='offset points')
for g, c in groups.items(): ax.scatter([], [], color=c, label={'early': 'American 1805-1846', 'mid': 'Cabell 1858', 'late': 'Southern 1869-1900', 'poe': 'Poe', 'beale': 'Beale Papers 1885'}[g])
ax.legend(fontsize=8); ax.set_title('Classical MDS of Cosine Delta (200 MFW); labels on first sample of each author', fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(R, 'stylo_delta_mds.svg')); plt.close(fig)
print(open(os.path.join(R, 'stylo_delta_report.md')).read()[:6000])
