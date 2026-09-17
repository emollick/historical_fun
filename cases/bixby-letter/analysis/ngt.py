"""N-gram tracing (Grieve, Clarke, Chiang, Gideon, Heini, Nini & Waibel, DSH 2019).

Implements the algorithm described in section 3 of the paper:
 1. extract all n-gram types (word 1-3, character 3-16; case-insensitive;
    punctuation ignored for words, kept for characters; no n-gram spans a
    sentence boundary) from the questioned document;
 2. take a random sample of texts of equal size (in words) from each
    candidate's writing sample;
 3. measure the percentage of the questioned document's n-gram types that
    occur at least once in each sample (the Overlap Coefficient |Q & A| / |Q|);
 4. attribute to the candidate with the higher percentage; repeat over
    random sequences of texts and average.

Leave-one-out validation removes the test text from its own author's pool
before sampling, exactly as the paper describes (section 5).
"""
import re, random, math
from collections import Counter, defaultdict

_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+|\n\s*\n')
_WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

def sentences(text):
    t = text.replace('\r', '\n')
    t = re.sub(r'(?<=[a-zA-Z])-[ \t]*\n[ \t]*(?=[a-z])', '', t)   # de-hyphenate OCR line breaks
    t = re.sub(r'[ \t]+', ' ', t)
    parts = [p.strip() for p in _SENT_SPLIT.split(t)]
    return [p for p in parts if p]

def word_tokens(sent):
    return _WORD.findall(sent.lower())

def char_string(sent):
    s = sent.lower()
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def word_ngrams(text, n):
    out = set()
    for s in sentences(text):
        toks = word_tokens(s)
        for i in range(len(toks) - n + 1):
            out.add(' '.join(toks[i:i+n]))
    return out

def char_ngrams(text, n):
    out = set()
    for s in sentences(text):
        cs = char_string(s)
        for i in range(len(cs) - n + 1):
            out.add(cs[i:i+n])
    return out

def ngram_types(text, level, n):
    return word_ngrams(text, n) if level == 'w' else char_ngrams(text, n)

def word_count(text):
    return sum(len(word_tokens(s)) for s in sentences(text))

def overlap(qtypes, pool_counter):
    """fraction of q's types present (count>0) in pool"""
    if not qtypes:
        return float('nan')
    return sum(1 for g in qtypes if pool_counter.get(g, 0) > 0) / len(qtypes)


class Author:
    """Holds an author's texts with precomputed per-text n-gram type sets."""
    def __init__(self, name, texts):
        # texts: list of (id, text)
        self.name = name
        self.ids = [i for i, _ in texts]
        self.texts = {i: t for i, t in texts}
        self.wc = {i: word_count(t) for i, t in texts}
        self.total_words = sum(self.wc.values())
        self.types = {}      # (level,n) -> {id: set}

    def prepare(self, level, n):
        key = (level, n)
        if key not in self.types:
            self.types = {key: {i: ngram_types(self.texts[i], level, n) for i in self.ids}}
        return self.types[key]

    def clear(self):
        self.types = {}


class Sampler:
    """One random sequence of an author's texts, with cumulative counters."""
    def __init__(self, author, rng, target_words):
        self.a = author
        self.order = list(author.ids)
        rng.shuffle(self.order)
        self.target = target_words
        # cutoff index k0: smallest k with cumulative words >= target
        cum = 0
        self.k0 = len(self.order)
        for k, i in enumerate(self.order):
            cum += author.wc[i]
            if cum >= target_words:
                self.k0 = k + 1
                break
        self.cum_words_k0 = cum
        self.pos = {i: k for k, i in enumerate(self.order)}
        self.counters = {}

    def counter(self, level, n):
        key = (level, n)
        if key not in self.counters:
            types = self.a.prepare(level, n)
            c = Counter()
            for i in self.order[:self.k0]:
                c.update(types[i])
            self.counters = {key: c}
        return self.counters[key]

    def overlap(self, qtypes, level, n, exclude_id=None):
        """Overlap of q with the sample; if exclude_id is in the sample,
        remove it and extend the sample with the next texts until the target
        size is restored (leave-one-out)."""
        c = self.counter(level, n)
        types = self.a.prepare(level, n)
        if exclude_id is None or self.pos.get(exclude_id, 10**9) >= self.k0:
            return overlap(qtypes, c)
        # exclude_id is inside the sample
        ex = types[exclude_id]
        need = self.a.wc[exclude_id] - (self.cum_words_k0 - self.target)
        extra_ids = []
        k = self.k0
        while need > 0 and k < len(self.order):
            extra_ids.append(self.order[k]); need -= self.a.wc[self.order[k]]; k += 1
        extra_sets = [types[i] for i in extra_ids]
        hits = 0
        for g in qtypes:
            cnt = c.get(g, 0) - (1 if g in ex else 0)
            if cnt <= 0:
                for s in extra_sets:
                    if g in s:
                        cnt = 1; break
            if cnt > 0:
                hits += 1
        return hits / len(qtypes) if qtypes else float('nan')


def trace_attribute(qtext, authors, level, n, samplers, exclude=None):
    """Return {author: mean overlap over samplers} for one n-gram type."""
    q = ngram_types(qtext, level, n)
    res = {}
    for a in authors:
        vals = [s.overlap(q, level, n, exclude_id=exclude if exclude and exclude[0] == a.name else None)
                for s in samplers[a.name]]
        res[a.name] = sum(vals) / len(vals)
    return res, len(q)


def make_samplers(authors, n_seq, target_words, seed=0):
    rng = random.Random(seed)
    return {a.name: [Sampler(a, rng, target_words) for _ in range(n_seq)] for a in authors}
