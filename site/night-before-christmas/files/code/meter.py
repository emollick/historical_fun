"""
meter.py -- identify features (words / character n-grams / phonemes) whose
frequency is driven by anapestic metre itself, using the control authors who
wrote in both anapestic and non-anapestic verse. A feature is 'metre-sensitive'
when, across authors, its rate in anapestic verse differs consistently from its
rate in that same author's other verse (paired comparison, so authorial habit
cancels out). Such features can then be dropped from attribution feature sets
so that a metre difference between candidates is not mistaken for authorship.
"""
import os, sys, math
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import counts_for, tokens

def author_form_profiles(ctrl, kind='word', n=4, min_words=1500):
    """dict author -> {'anapestic': Counter, 'other': Counter} for authors with
    at least min_words in each form."""
    prof = defaultdict(lambda: {'anapestic': Counter(), 'other': Counter()})
    words = defaultdict(lambda: {'anapestic': 0, 'other': 0})
    for d in ctrl:
        c = counts_for(d, kind, n)
        prof[d['author']][d['form_class']].update(c)
        words[d['author']][d['form_class']] += len(tokens(d['text']))
    return {a: p for a, p in prof.items()
            if words[a]['anapestic'] >= min_words and words[a]['other'] >= min_words}

def metre_sensitivity(profiles, feats, alpha=0.5):
    """For each feature: paired log-ratio (anapestic vs other, per author, with
    additive smoothing), its mean across authors, a paired t statistic, and the
    number of authors. Returns dict feat -> (mean_logratio, t, n_authors)."""
    out = {}
    authors = list(profiles)
    tot = {a: {f: sum(profiles[a][f].values()) for f in ('anapestic', 'other')} for a in authors}
    for feat in feats:
        lr = []
        for a in authors:
            pa = (profiles[a]['anapestic'][feat] + alpha) / (tot[a]['anapestic'] + alpha * len(feats))
            po = (profiles[a]['other'][feat] + alpha) / (tot[a]['other'] + alpha * len(feats))
            lr.append(math.log(pa / po))
        lr = np.array(lr)
        m = lr.mean(); s = lr.std(ddof=1) if len(lr) > 1 else 1.0
        t = m / (s / math.sqrt(len(lr))) if s > 0 else 0.0
        out[feat] = (float(m), float(t), len(lr))
    return out

def metre_neutral(feats, sens, t_cut=3.0, lr_cut=0.25):
    """Keep features that are NOT consistently metre-driven: |t| < t_cut or
    |mean log ratio| < lr_cut."""
    keep, drop = [], []
    for f in feats:
        m, t, n = sens.get(f, (0.0, 0.0, 0))
        if abs(t) >= t_cut and abs(m) >= lr_cut:
            drop.append(f)
        else:
            keep.append(f)
    return keep, drop
