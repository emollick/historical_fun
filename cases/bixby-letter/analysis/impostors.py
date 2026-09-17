"""General Impostors method (Koppel & Winter 2014; Kestemont et al. 2016).
score(Q, A) = fraction of K random feature subsets in which the candidate A's
profile (or one of A's documents) is more similar to Q than every impostor document.
Similarity: min-max (Ruzicka) on relative frequencies, as in Kestemont et al."""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from ngt import sentences

def norm(text):
    return ' '.join(sentences(text)).lower()

def minmax(a, b):
    mn = np.minimum(a, b).sum(); mx = np.maximum(a, b).sum()
    return mn / mx if mx else 0.0

def gi_score(q_vec, cand_vecs, imp_vecs, rng, K=100, frac=0.5):
    """cand_vecs: array (n_cand_docs, F); imp_vecs: (n_imp_docs, F). Each iteration
    samples a random subset of features and a random subset of impostors, then asks
    whether the nearest candidate doc beats the nearest impostor doc."""
    F = q_vec.shape[0]
    wins = 0
    for _ in range(K):
        feats = rng.choice(F, size=max(1, int(F * frac)), replace=False)
        imps = imp_vecs[rng.choice(imp_vecs.shape[0], size=min(imp_vecs.shape[0], max(5, imp_vecs.shape[0] // 2)), replace=False)]
        q = q_vec[feats]
        sc = max(minmax(q, c[feats]) for c in cand_vecs)
        si = max(minmax(q, i[feats]) for i in imps)
        if sc > si: wins += 1
    return wins / K

def vectorize(texts, analyzer='char', ngram=(4, 4), max_features=10000):
    cv = CountVectorizer(analyzer=analyzer, ngram_range=ngram, max_features=max_features, lowercase=False)
    X = cv.fit_transform([norm(t) for t in texts]).astype(float)
    X = X.toarray()
    X = X / np.maximum(X.sum(axis=1, keepdims=True), 1)
    return cv, X
