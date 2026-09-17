"""Burrows's Delta (2002) and cosine Delta (Smith & Aldridge 2011; Evert et al. 2017)
on the most frequent words, with validation on held-out short texts."""
import numpy as np, re
from collections import Counter
from ngt import sentences, word_tokens

def tokens(text):
    out = []
    for s in sentences(text):
        out.extend(word_tokens(s))
    return out

def build_vocab(texts, k=150):
    c = Counter()
    for t in texts: c.update(tokens(t))
    return [w for w, _ in c.most_common(k)]

def rel_freq(text, vocab):
    toks = tokens(text)
    n = max(len(toks), 1)
    c = Counter(toks)
    return np.array([c[w] / n for w in vocab])

def zscores(X, mu, sd):
    return (X - mu) / np.where(sd == 0, 1, sd)

def burrows_delta(zq, zp):
    return np.mean(np.abs(zq - zp))

def cosine_delta(zq, zp):
    d = np.linalg.norm(zq) * np.linalg.norm(zp)
    return 1 - float(zq @ zp / d) if d else 1.0
