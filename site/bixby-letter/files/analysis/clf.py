"""Character n-gram classifier with calibrated probabilities, validated on short texts.
Training units are whole known texts (not chunks) so that validation on 100-200 word
texts is honest: grouped cross-validation by source document."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.calibration import CalibratedClassifierCV
from ngt import sentences

def norm(text, strip_punct=False):
    s = ' '.join(sentences(text)).lower()
    if strip_punct:
        import re
        s = re.sub(r"[^a-z0-9' ]+", ' ', s)
        s = re.sub(r'\s+', ' ', s)
    return s

def make_pipe(analyzer='char', ngram=(3, 5), C=1.0, min_df=2):
    vec = TfidfVectorizer(analyzer=analyzer, ngram_range=ngram, min_df=min_df, sublinear_tf=True, lowercase=False)
    lr = LogisticRegression(C=C, max_iter=2000, class_weight='balanced')
    return make_pipeline(vec, lr)

def cv_probs(texts, labels, pipe_fn, n_splits=5, seed=0):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    labels = np.array(labels)
    probs = np.zeros((len(texts), len(set(labels))))
    classes = sorted(set(labels))
    for tr, te in skf.split(texts, labels):
        pipe = pipe_fn()
        pipe.fit([texts[i] for i in tr], labels[tr])
        p = pipe.predict_proba([texts[i] for i in te])
        # align columns
        cols = list(pipe.classes_)
        for j, c in enumerate(classes):
            probs[te, j] = p[:, cols.index(c)]
    return classes, probs
