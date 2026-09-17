#!/usr/bin/env python3
"""Stylometric toolkit: corpus loading, chunking, MFW/char-ngram features, Burrows/Cosine Delta, classifiers, markers."""
import json, os, re, math, random
import numpy as np
from collections import Counter, defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SEG = os.path.join(ROOT, 'corpus', 'segments.jsonl')

# tokens that mark the print era / modern contraction habits rather than the author of the underlying text
ERA_MARKED = {"i'm","i'll","i've","i'd","you'll","you're","you've","he'll","she'll","we'll","they'll","don't","can't","won't","shan't","isn't",
              "wasn't","it's","that's","there's","what's","let's","'em","'tis","'twas","'twere","'twill","'twould","ne'er","e'er","o'er","e'en",
              "i'th'","o'th'","th'","its","mr","mrs","madam","sir","ye","hath","doth","ere","unto","betwixt","whilst","o","oh","ah","ay","yes","aye",
              "thou","thee","thy","thine","art","wilt","shalt","dost","hast","didst","canst","wert","then","tho","ha","um","hum","'t","'s"}

def load_segments(groups=None, keys=None):
    out = []
    with open(SEG) as fh:
        for line in fh:
            r = json.loads(line)
            if groups and r['group'] not in groups: continue
            if keys and r['key'] not in keys: continue
            out.append(r)
    return out

def play_tokens(segs):
    """Concatenate tokens per play key, in act/scene order."""
    d = defaultdict(list); meta = {}
    for r in segs:
        d[r['key']].extend(r['tokens']); meta[r['key']] = (r['group'], r['author'], r['date'])
    return d, meta

def chunk(tokens, size, min_frac=0.6):
    """Consecutive chunks of `size` tokens; a short remainder is kept if >= min_frac*size (merged into last chunk otherwise)."""
    out = []
    for i in range(0, len(tokens), size):
        out.append(tokens[i:i + size])
    if len(out) > 1 and len(out[-1]) < min_frac * size:
        last = out.pop(); out[-1] = out[-1] + last
    return out

class MFW:
    """Most-frequent-word relative frequencies with optional exclusion of era-marked tokens."""
    def __init__(self, n=300, exclude=None, culling=0.0):
        self.n = n; self.exclude = set(exclude or []); self.culling = culling; self.vocab = None
    def fit(self, docs):
        c = Counter(); df = Counter()
        for d in docs:
            c.update(d); df.update(set(d))
        cands = [w for w, _ in c.most_common() if w not in self.exclude and not any(ch in w for ch in '^~')]
        if self.culling > 0:
            cands = [w for w in cands if df[w] / len(docs) >= self.culling]
        self.vocab = cands[:self.n]; self.index = {w: i for i, w in enumerate(self.vocab)}
        return self
    def transform(self, docs):
        X = np.zeros((len(docs), len(self.vocab)))
        for i, d in enumerate(docs):
            c = Counter(d); n = max(1, len(d))
            for w, k in c.items():
                j = self.index.get(w)
                if j is not None: X[i, j] = k / n * 1000.0
        return X

class CharNgram:
    def __init__(self, n=4, top=3000):
        self.n = n; self.top = top; self.vocab = None
    @staticmethod
    def grams(tokens, n):
        s = ' ' + ' '.join(tokens) + ' '
        return Counter(s[i:i + n] for i in range(len(s) - n + 1))
    def fit(self, docs):
        c = Counter()
        for d in docs: c.update(self.grams(d, self.n))
        self.vocab = [g for g, _ in c.most_common(self.top) if '^' not in g and '~' not in g]
        self.index = {g: i for i, g in enumerate(self.vocab)}
        return self
    def transform(self, docs):
        X = np.zeros((len(docs), len(self.vocab)))
        for i, d in enumerate(docs):
            g = self.grams(d, self.n); n = max(1, sum(g.values()))
            for k, v in g.items():
                j = self.index.get(k)
                if j is not None: X[i, j] = v / n * 1000.0
        return X

class Delta:
    """Burrows's Delta (z-scored Manhattan) and Cosine Delta (Smith & Aldridge / Evert et al.) nearest-centroid classifier."""
    def __init__(self, kind='cosine'):
        self.kind = kind
    def fit(self, X, y):
        self.mu = X.mean(0); self.sd = X.std(0) + 1e-9
        Z = (X - self.mu) / self.sd
        self.classes = sorted(set(y)); self.cent = {}
        for c in self.classes:
            self.cent[c] = Z[[i for i, t in enumerate(y) if t == c]].mean(0)
        return self
    def dist(self, X):
        Z = (X - self.mu) / self.sd
        D = np.zeros((len(X), len(self.classes)))
        for j, c in enumerate(self.classes):
            v = self.cent[c]
            if self.kind == 'burrows':
                D[:, j] = np.abs(Z - v).mean(1)
            else:
                D[:, j] = 1 - (Z @ v) / (np.linalg.norm(Z, axis=1) * np.linalg.norm(v) + 1e-12)
        return D
    def predict(self, X):
        D = self.dist(X); return [self.classes[i] for i in D.argmin(1)], D

def syllables(word):
    """Rough syllable count for early modern English words."""
    w = word.lower().strip("'")
    if not w: return 0
    w = re.sub(r"'d$", 'd', w)
    # final -ed after t/d is a syllable; otherwise silent when the word is spelled -ed (approximate)
    groups = re.findall(r'[aeiouy]+', w)
    n = len(groups)
    if w.endswith('e') and not w.endswith(('le', 'ee', 'ye', 'ie', 'oe')) and n > 1: n -= 1
    if w.endswith('ed') and not w.endswith(('ted', 'ded', 'eed')) and n > 1: n -= 1
    if w.endswith('es') and not w.endswith(('ses', 'ces', 'ges', 'xes', 'zes', 'shes', 'ches', 'ees', 'ies', 'oes')) and n > 1: n -= 1
    if w.endswith('ion'): n = max(1, n)  # -ion counted as one
    return max(1, n)

def line_syllables(line):
    toks = re.findall(r"[A-Za-z']+", line.replace('ſ', 's'))
    return sum(syllables(t) for t in toks if t.strip("'"))

def markers(rec):
    """Rates per 1000 words of Fletcherian and other linguistic markers, plus a feminine-ending proxy from verse lines."""
    toks = rec['tokens']; n = max(1, len(toks)); c = Counter(toks)
    r = lambda *ws: sum(c[w] for w in ws) / n * 1000.0
    m = {'n_words': n,
         'ye': r('ye'), 'you': r('you'), 'em': r("'em"), 'them': r('them'), 'hath': r('hath'), 'has': r('has'), 'doth': r('doth'), 'does': r('does'),
         'ith': r("i'th'", "o'th'", "a'th'"), 'th': r("th'"), 'tis': r("'tis", "'twas", "'twere", "'twill", "'twould"), 'sir': r('sir'),
         'thou': r('thou', 'thee', 'thy', 'thine'), 'I_am': 0.0, 'im': r("i'm"), 'ill': r("i'll"), 'dont': r("don't"), 'its': r('its'),
         'let_s': r("let's"), 'ere': r('ere'), 'unto': r('unto'), 'oh': r('oh'), 'o': r('o')}
    # bigram "i am"
    ia = sum(1 for a, b in zip(toks, toks[1:]) if a == 'i' and b == 'am'); m['I_am'] = ia / n * 1000.0
    m['ye_ratio'] = c['ye'] / max(1, c['ye'] + c['you'])
    m['em_ratio'] = c["'em"] / max(1, c["'em"] + c['them'])
    m['hath_ratio'] = c['hath'] / max(1, c['hath'] + c['has'])
    m['doth_ratio'] = c['doth'] / max(1, c['doth'] + c['does'])
    # feminine-ending proxy: share of verse lines (with >= 8 syllables) that have >= 11 syllables
    vl = [line_syllables(l) for l in rec.get('verse_lines', [])]
    vl = [s for s in vl if 8 <= s <= 14]
    m['n_verse'] = len(vl)
    m['fem_proxy'] = (sum(1 for s in vl if s >= 11) / len(vl)) if vl else float('nan')
    return m
