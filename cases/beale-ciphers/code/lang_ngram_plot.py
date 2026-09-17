#!/usr/bin/env python3
"""Plot Google Books (American English) yearly relative frequencies, 1800-1900, for the
words/phrases flagged in the Beale letters (results/lang_ngram_phrases.json)."""
import os, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.join(B, 'results')
d = json.load(open(os.path.join(R, 'lang_ngram_phrases.json'))); yrs = np.arange(1780, 1901)
panels = [('stampeding', 'stampede', 'stampeded'), ('improvised', 'grizzlies', 'objective point'), ('reliable', 'appliances', 'locality'), ('everything', 'every thing', 'in the mean time', 'in the meantime')]
fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), sharex=True)
cols = ['#2a6fdb', '#c98a1b', '#1a9e6e', '#b3261e']
for ax, words in zip(axes.flat, panels):
    for w, c in zip(words, cols):
        ts = np.array(d.get(w) or [np.nan] * len(yrs)) * 1e9
        sm = np.convolve(ts, np.ones(5) / 5, mode='same')     # 5-year moving average for readability
        ax.plot(yrs, sm, color=c, lw=1.8, label=w)
    ax.axvline(1822, color='#888', ls='--', lw=1); ax.axvline(1885, color='#888', ls=':', lw=1)
    ax.set_xlim(1800, 1900); ax.set_ylabel('per 10^9 words'); ax.legend(fontsize=8, loc='upper left'); ax.grid(alpha=0.25)
axes[0, 0].set_title('Words of the "Beale" letters in American books (5-yr average); dashed = 1822, dotted = 1885', fontsize=9.5, loc='left')
fig.tight_layout(); fig.savefig(os.path.join(R, 'lang_ngram_timeseries.svg')); print('saved')
