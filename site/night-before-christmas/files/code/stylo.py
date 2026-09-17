"""
stylo.py -- small, dependency-light stylometry toolkit written for the
"A Visit from St. Nicholas" authorship study (Moore vs Livingston).

Corpus file format (plain text):
    title: ...
    author: ...
    date: ...
    source: ...
    form: ...
    lines: N
    attribution: certain|probable|doubtful
    notes: ...
    <blank line>
    <poem, one verse line per text line, blank line between stanzas>

Everything here is deliberately transparent: no black boxes, so that the
numbers in the report can be checked line by line.
"""
import os, re, glob, math, random, json
from collections import Counter, defaultdict
import numpy as np

# ----------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------
HEADER_KEYS = ('title', 'author', 'date', 'source', 'form', 'lines',
               'attribution', 'notes')

def load_poem(path):
    with open(path, encoding='utf-8') as fh:
        raw = fh.read()
    raw = raw.replace('\r\n', '\n')
    meta, body_lines = {}, []
    in_header = True
    for line in raw.split('\n'):
        if in_header:
            if line.strip() == '':
                if meta:
                    in_header = False
                continue
            m = re.match(r'^([a-z_]+):\s*(.*)$', line)
            if m and m.group(1) in HEADER_KEYS:
                meta[m.group(1)] = m.group(2).strip()
                continue
            # header without recognised key: treat as start of body
            in_header = False
        body_lines.append(line)
    body = '\n'.join(body_lines).strip('\n')
    verse_lines = [l for l in body.split('\n') if l.strip()]
    d = dict(meta)
    d['path'] = path
    d['id'] = os.path.splitext(os.path.basename(path))[0]
    d['text'] = body
    d['verse_lines'] = verse_lines
    d['n_lines'] = len(verse_lines)
    d.setdefault('author', 'unknown')
    d.setdefault('form', 'unknown')
    d.setdefault('attribution', 'unknown')
    return d

def load_corpus(root, pattern='**/*.txt', exclude_re=r'MANIFEST'):
    out = []
    for p in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
        if re.search(exclude_re, os.path.basename(p)):
            continue
        try:
            out.append(load_poem(p))
        except Exception as e:  # pragma: no cover
            print('could not load', p, e)
    return out

# ----------------------------------------------------------------------
# Normalisation and tokenisation
# ----------------------------------------------------------------------
_APOS = "['’ʼ`]"

def normalise(text):
    t = text.replace('’', "'").replace('‘', "'").replace('ʼ', "'")
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('æ', 'ae').replace('œ', 'oe').replace('ſ', 's')
    t = t.replace('—', ' -- ').replace('–', ' - ')
    t = t.replace('&', ' and ')
    return t


# ----------------------------------------------------------------------
# Orthographic normalisation (robustness check): editions and transcribers
# differ in "-'d" vs "-ed", "thro'" vs "through" etc. When ORTHO_NORMALISE is
# True these are unified before tokenisation so that such habits cannot drive
# an attribution.
# ----------------------------------------------------------------------
ORTHO_NORMALISE = False

def ortho_normalise(t):
    t = re.sub(r"([a-z])'d\b", r"\1ed", t)          # danc'd -> danced
    t = re.sub(r"\bthro'?(?!\w)", "through", t)
    t = re.sub(r"\btho'?(?!\w)", "though", t)
    t = re.sub(r"(?<!\w)'till\b", "till", t)
    t = re.sub(r"\bev'ry\b", "every", t)
    t = re.sub(r"\bheav'n\b", "heaven", t)
    t = re.sub(r"\bne'er\b", "never", t)
    t = re.sub(r"\be'er\b", "ever", t)
    t = re.sub(r"\bo'er\b", "over", t)
    return t

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*|'[A-Za-z]+(?:'[A-Za-z]+)*")

def tokens(text):
    """Lower-cased word tokens. Leading apostrophes are dropped ('twas -> twas,
    'tis -> tis) so that editions differing in apostrophe use agree; internal
    apostrophes are kept (e'er, o'er, don't)."""
    t = normalise(text).lower()
    if ORTHO_NORMALISE:
        t = ortho_normalise(t)
    toks = []
    for w in WORD_RE.findall(t):
        w = w.strip("'")
        if w:
            toks.append(w)
    return toks

def char_stream(text):
    """Text reduced to lower-case letters, apostrophes and single spaces,
    for character n-grams. Punctuation is dropped because it varies between
    editions and transcribers more than between authors."""
    t = normalise(text).lower()
    if ORTHO_NORMALISE:
        t = ortho_normalise(t)
    t = re.sub(r"[^a-z' \n]", ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return ' ' + t + ' '

def char_ngrams(text, n=4):
    s = char_stream(text)
    return Counter(s[i:i+n] for i in range(len(s) - n + 1))

# ----------------------------------------------------------------------
# Feature matrices
# ----------------------------------------------------------------------
def counts_for(doc, kind='word', n=4):
    if kind == 'word':
        return Counter(tokens(doc['text']))
    if kind == 'char':
        return char_ngrams(doc['text'], n)
    if kind == 'phone':
        from phon import phone_counts
        return phone_counts(doc['text'])
    raise ValueError(kind)

def top_features(count_list, k=150, culling=0.0):
    """k most frequent features over the pooled counts. `culling` = minimum
    fraction of documents a feature must occur in (0 = none)."""
    pooled = Counter()
    df = Counter()
    for c in count_list:
        pooled.update(c)
        df.update(set(c))
    n_docs = len(count_list)
    feats = [f for f, _ in pooled.most_common()
             if df[f] >= culling * n_docs]
    return feats[:k]

def rel_freq_matrix(count_list, feats):
    X = np.zeros((len(count_list), len(feats)))
    for i, c in enumerate(count_list):
        tot = sum(c.values()) or 1
        for j, f in enumerate(feats):
            X[i, j] = c.get(f, 0) / tot
    return X

def zscore(X, mean=None, std=None):
    if mean is None:
        mean = X.mean(axis=0)
    if std is None:
        std = X.std(axis=0)
    std = np.where(std == 0, 1e-9, std)
    return (X - mean) / std, mean, std

# ----------------------------------------------------------------------
# Distances
# ----------------------------------------------------------------------
def burrows_delta(a, b):
    return float(np.mean(np.abs(a - b)))

def cosine_dist(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 1.0
    return float(1.0 - np.dot(a, b) / (na * nb))

def minmax_dist(a, b):
    """Ruzicka / min-max distance on non-negative vectors (Kestemont et al.)."""
    mn = np.minimum(a, b).sum()
    mx = np.maximum(a, b).sum()
    return float(1.0 - mn / mx) if mx > 0 else 1.0

DIST = {'delta': burrows_delta, 'cosine': cosine_dist, 'minmax': minmax_dist}

# ----------------------------------------------------------------------
# Sampling: cut a corpus into samples of roughly N verse lines
# ----------------------------------------------------------------------
def make_samples(docs, target_lines=56, min_lines=40, bundle_short=True,
                 key=lambda d: (d['author'], d.get('form_class', d['form']))):
    """Return a list of samples, each dict(author, form, lines, text,
    poem_ids, ids). Long poems are cut into consecutive windows of
    ~target_lines (never crossing a poem); short poems (< min_lines) are
    bundled with the next short poem(s) of the same author and form until
    the bundle reaches min_lines. Every sample records which poems it draws
    on so that hold-out tests can exclude same-poem material."""
    samples = []
    bundles = defaultdict(list)
    for d in docs:
        L = d['verse_lines']
        n = len(L)
        if n >= min_lines:
            k = max(1, int(round(n / target_lines)))
            # equal-ish windows
            bounds = [int(round(i * n / k)) for i in range(k + 1)]
            for i in range(k):
                chunk = L[bounds[i]:bounds[i+1]]
                samples.append(dict(author=d['author'], form=d['form'],
                                    form_class=d.get('form_class', d['form']),
                                    attribution=d['attribution'],
                                    lines=len(chunk), text='\n'.join(chunk),
                                    poem_ids={d['id']}, ids=[d['id'] + f'#{i+1}']))
        elif bundle_short:
            bundles[key(d)].append(d)
    for k_, ds in bundles.items():
        cur, cur_ids, cur_pids, cur_n = [], [], set(), 0
        for d in ds:
            cur.extend(d['verse_lines']); cur_ids.append(d['id'])
            cur_pids.add(d['id']); cur_n += d['n_lines']
            if cur_n >= min_lines:
                samples.append(dict(author=d['author'], form=d['form'],
                                    form_class=d.get('form_class', d['form']),
                                    attribution=d['attribution'],
                                    lines=cur_n, text='\n'.join(cur),
                                    poem_ids=set(cur_pids), ids=list(cur_ids),
                                    bundle=True))
                cur, cur_ids, cur_pids, cur_n = [], [], set(), 0
        if cur_n >= min_lines * 0.6 and cur:
            samples.append(dict(author=ds[0]['author'], form=ds[0]['form'],
                                form_class=ds[0].get('form_class', ds[0]['form']),
                                attribution=ds[0]['attribution'],
                                lines=cur_n, text='\n'.join(cur),
                                poem_ids=set(cur_pids), ids=list(cur_ids),
                                bundle=True))
    return samples

# ----------------------------------------------------------------------
# Form classification helper
# ----------------------------------------------------------------------
def form_class(form_str):
    f = (form_str or '').lower()
    if 'anap' in f:
        return 'anapestic'
    return 'other'

# ----------------------------------------------------------------------
# Nearest-profile Delta attribution
# ----------------------------------------------------------------------
def profile_attribution(test_counts, ref_samples_counts, ref_authors, feats,
                        dist='cosine', standardise=True):
    """ref_samples_counts: list of Counters (reference samples); ref_authors:
    their author labels. Returns dict author -> distance from test to the
    author's centroid (in z-score space computed over reference samples)."""
    Xr = rel_freq_matrix(ref_samples_counts, feats)
    xt = rel_freq_matrix([test_counts], feats)[0]
    if standardise:
        Zr, mu, sd = zscore(Xr)
        zt = (xt - mu) / sd
    else:
        Zr, zt = Xr, xt
    authors = sorted(set(ref_authors))
    out = {}
    for a in authors:
        idx = [i for i, x in enumerate(ref_authors) if x == a]
        cen = Zr[idx].mean(axis=0)
        out[a] = DIST[dist](zt, cen)
    return out

def instance_attribution(test_counts, ref_samples_counts, ref_authors, feats,
                         dist='cosine', standardise=True, k=1):
    """Nearest-instance (k-NN) variant: returns author -> mean distance to
    the k nearest reference samples of that author."""
    Xr = rel_freq_matrix(ref_samples_counts, feats)
    xt = rel_freq_matrix([test_counts], feats)[0]
    if standardise:
        Zr, mu, sd = zscore(Xr)
        zt = (xt - mu) / sd
    else:
        Zr, zt = Xr, xt
    out = {}
    for a in sorted(set(ref_authors)):
        idx = [i for i, x in enumerate(ref_authors) if x == a]
        ds = sorted(DIST[dist](zt, Zr[i]) for i in idx)
        out[a] = float(np.mean(ds[:k]))
    return out

# ----------------------------------------------------------------------
# General Imposters verification (Koppel & Winter 2014; Kestemont et al. 2016)
# ----------------------------------------------------------------------
def general_imposters(test_counts, cand_counts, imp_counts, feats,
                      n_iter=200, feat_frac=0.5, imp_frac=0.5,
                      dist='minmax', standardise=False, seed=0, rng=None):
    """Score in [0,1]: fraction of random (feature-subset, impostor-subset)
    trials in which the test text is nearer to the CANDIDATE's nearest
    sample than to the nearest IMPOSTOR sample. cand_counts / imp_counts:
    lists of Counters. Distance defaults to min-max on relative frequencies
    (Kestemont's recommended setting); 'cosine' on z-scores also supported."""
    rng = rng or random.Random(seed)
    allc = cand_counts + imp_counts
    X = rel_freq_matrix(allc, feats)
    xt = rel_freq_matrix([test_counts], feats)[0]
    if standardise:
        Z, mu, sd = zscore(X)
        zt = (xt - mu) / sd
    else:
        Z, zt = X, xt
    nc = len(cand_counts)
    n_imp = len(imp_counts)
    nf = len(feats)
    wins = 0
    for _ in range(n_iter):
        fidx = rng.sample(range(nf), max(2, int(nf * feat_frac)))
        iidx = rng.sample(range(n_imp), max(1, int(n_imp * imp_frac)))
        f = DIST[dist]
        dc = min(f(zt[fidx], Z[i][fidx]) for i in range(nc))
        di = min(f(zt[fidx], Z[nc + i][fidx]) for i in iidx)
        if dc < di:
            wins += 1
    return wins / n_iter

# ----------------------------------------------------------------------
# Misc helpers
# ----------------------------------------------------------------------
def word_count(text):
    return len(tokens(text))

def summarise_docs(docs):
    rows = []
    for d in docs:
        rows.append(dict(id=d['id'], author=d['author'], form=d['form'],
                         attribution=d['attribution'], lines=d['n_lines'],
                         words=word_count(d['text'])))
    return rows
