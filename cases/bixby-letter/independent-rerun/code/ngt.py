"""
n-gram tracing, reimplemented from the published description.

Source of the method: Jack Grieve, Emily Chiang, Isobelle Clarke, Hannah Gideon,
Annina Heini, Andrea Nini and Emily Waibel, "Attributing the Bixby Letter using
n-gram tracing", Digital Scholarship in the Humanities 34(3), 2019, 493-512,
section 3 (method), section 5 (evaluation) and section 6 (results). Read in the
author-accepted preprint, University of Birmingham repository,
https://pure-oai.bham.ac.uk/ws/files/53402456/Bixby_PREPRINT.pdf

This file was written without reading any other implementation. The choices the
paper leaves open are listed in the README (sentence splitting, word tokens,
how the equal-size samples are cut).

The method, as the paper describes it (preprint pp. 11-14):
  1. extract all n-gram types of one length and level (word or character) from
     the questioned document Q;
  2. take a random sample of texts from each candidate, "roughly equal in
     length to the total number of words in the possible author writing sample
     with the fewest words";
  3. measure the share of Q's n-gram types that occur at least once in each
     sample (the overlap coefficient |Q and A| / |Q|);
  4. attribute Q to the candidate with the larger share; repeat over several
     random sequences of texts and compare the averages; ties count as wrong
     for both authors (p. 24).
Word n-grams ignore case and punctuation; character n-grams are
case-insensitive and keep punctuation and spaces; neither may span a
sentence boundary (pp. 16, 18).
"""
from __future__ import annotations

import re
import numpy as np

# ----------------------------------------------------------------------------
# text handling
# ----------------------------------------------------------------------------

_ABBREV = {
    "mr", "mrs", "dr", "gen", "col", "hon", "st", "capt", "lieut", "maj", "gov",
    "sen", "rev", "prof", "esq", "jr", "sr", "vs", "no", "co", "brig", "adjt",
    "sept", "oct", "nov", "dec", "jan", "feb", "aug", "vol", "chap", "ult",
    "inst", "prox", "messrs", "gens", "cols", "u", "s", "a", "j", "w", "h",
    "e", "b", "c", "d", "f", "g", "i", "k", "l", "m", "n", "o", "p", "r", "t",
    "v", "y", "z", "wm", "jno", "geo", "chas", "thos", "jas", "benj", "saml",
}

_SPLIT = re.compile(r"(?<=[.!?][\"'”’)])\s+|(?<=[.!?])\s+")
_WS = re.compile(r"\s+")
_WORD = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")


def sentences(text: str, lower: bool = True) -> list[str]:
    """Split a text into sentences. Everything is lower-cased (unless
    lower=False); whitespace is collapsed to single spaces; punctuation is
    kept. A full stop after a common abbreviation or a single initial does
    not end a sentence."""
    t = _WS.sub(" ", text.replace("­", "")).strip()
    if not t:
        return []
    raw = _SPLIT.split(t)
    out: list[str] = []
    buf = ""
    for piece in raw:
        piece = piece.strip()
        if not piece:
            continue
        buf = (buf + " " + piece).strip() if buf else piece
        last = buf.rstrip("\"'”’)")
        m = re.search(r"([A-Za-z]+)\.$", last)
        if m and m.group(1).lower() in _ABBREV:
            continue  # abbreviation: keep accumulating
        out.append(buf.lower() if lower else buf)
        buf = ""
    if buf:
        out.append(buf.lower() if lower else buf)
    return out


def words(sentence: str) -> list[str]:
    return _WORD.findall(sentence)


def word_count(text: str) -> int:
    return sum(len(words(s)) for s in sentences(text))


def ngram_types(text: str, level: str, n: int) -> set[str]:
    """All distinct n-grams of one level and length in a text; none spans a
    sentence boundary. Word n-grams are joined with a single space."""
    out: set[str] = set()
    for s in sentences(text):
        if level == "word":
            w = words(s)
            for i in range(len(w) - n + 1):
                out.add(" ".join(w[i:i + n]))
        elif level == "char":
            for i in range(len(s) - n + 1):
                out.add(s[i:i + n])
        else:
            raise ValueError(level)
    return out


# ----------------------------------------------------------------------------
# a candidate's writing sample
# ----------------------------------------------------------------------------

class Pool:
    """One candidate author's writing sample: a list of texts with ids."""

    def __init__(self, name: str, docs: list[tuple[str, str]]):
        self.name = name
        self.ids = [d[0] for d in docs]
        self.texts = [d[1] for d in docs]
        self.nwords = np.array([word_count(t) for t in self.texts], dtype=np.int64)
        self.index = {d: i for i, d in enumerate(self.ids)}

    def total_words(self) -> int:
        return int(self.nwords.sum())


class PoolGrams:
    """The n-gram inventory of a pool for one level and length, and the
    first-occurrence positions of every n-gram under each random order."""

    def __init__(self, pool: Pool, level: str, n: int, orders: list[np.ndarray],
                 restrict: set[str] | None = None):
        """`restrict`: when given, only these n-grams are indexed (enough when
        the questioned texts are known in advance and are not pool texts)."""
        self.pool, self.level, self.n = pool, level, n
        gram2id: dict[str, int] = {}
        doc_col: list[np.ndarray] = []
        gram_col: list[np.ndarray] = []
        for di, text in enumerate(pool.texts):
            g = ngram_types(text, level, n)
            if restrict is not None:
                g = g & restrict
            ids = np.fromiter((gram2id.setdefault(x, len(gram2id)) for x in g),
                              dtype=np.int64, count=len(g))
            doc_col.append(np.full(len(g), di, dtype=np.int32))
            gram_col.append(ids)
        self.gram2id = gram2id
        self.pair_doc = np.concatenate(doc_col) if doc_col else np.zeros(0, np.int32)
        self.pair_gram = np.concatenate(gram_col) if gram_col else np.zeros(0, np.int64)
        self.types_per_doc = np.bincount(self.pair_doc, minlength=len(pool.texts))
        G = len(gram2id)
        # per order: position of the first doc holding each gram, that doc's
        # index, and the position of the second doc holding it
        self.orders = orders
        self.pos = []      # pos[r][doc] = position of doc in order r
        self.cum = []      # cum[r][c] = words in the first c docs of order r
        self.first_pos, self.first_doc, self.second_pos = [], [], []
        BIG = np.iinfo(np.int32).max
        for order in orders:
            pos = np.empty(len(order), dtype=np.int32)
            pos[order] = np.arange(len(order))
            self.pos.append(pos)
            cum = np.concatenate([[0], np.cumsum(pool.nwords[order])])
            self.cum.append(cum)
            p = pos[self.pair_doc]
            srt = np.lexsort((p, self.pair_gram))
            gs, ps, ds = self.pair_gram[srt], p[srt], self.pair_doc[srt]
            uniq, first = np.unique(gs, return_index=True)
            fp = np.full(G, BIG, dtype=np.int32)
            fd = np.full(G, -1, dtype=np.int32)
            sp = np.full(G, BIG, dtype=np.int32)
            fp[uniq] = ps[first]
            fd[uniq] = ds[first]
            second = first + 1
            ok = second < len(gs)
            ok[ok] &= gs[second[ok]] == gs[first[ok]]
            sp[uniq[ok]] = ps[second[ok]]
            self.first_pos.append(fp)
            self.first_doc.append(fd)
            self.second_pos.append(sp)

    def cutoff(self, r: int, target: int, exclude_doc: int | None) -> int:
        """Number of leading docs of order r whose words (without the excluded
        doc) first reach the target. The paper takes texts at random until the
        sample is 'roughly equal' to the smaller writing sample."""
        cum = self.cum[r]
        c = int(np.searchsorted(cum, target, side="left"))
        if exclude_doc is not None and self.pos[r][exclude_doc] < c:
            c = int(np.searchsorted(cum, target + self.pool.nwords[exclude_doc], side="left"))
        return min(c, len(cum) - 1)

    def present(self, r: int, gram_ids: np.ndarray, cut: int, exclude_doc: int | None) -> np.ndarray:
        """Boolean array: is each gram (by id, -1 = not in the pool at all)
        present in the first `cut` docs of order r, ignoring the excluded doc."""
        out = np.zeros(len(gram_ids), dtype=bool)
        ok = gram_ids >= 0
        g = gram_ids[ok]
        fp, fd, sp = self.first_pos[r][g], self.first_doc[r][g], self.second_pos[r][g]
        if exclude_doc is None:
            res = fp < cut
        else:
            res = np.where(fd == exclude_doc, sp < cut, fp < cut)
        out[ok] = res
        return out

    def ids_for(self, grams: set[str]) -> np.ndarray:
        d = self.gram2id
        return np.fromiter((d.get(x, -1) for x in grams), dtype=np.int64, count=len(grams))


# ----------------------------------------------------------------------------
# the attribution step
# ----------------------------------------------------------------------------

def make_orders(n_docs: int, n_orders: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    return [rng.permutation(n_docs) for _ in range(n_orders)]


def trace_one(q_grams: set[str], pools: dict[str, PoolGrams], own: tuple[str, int] | None,
              frac: float = 1.0) -> dict[str, float]:
    """Average overlap coefficient of Q's n-gram types with each candidate's
    equal-size random samples. `own` = (pool name, doc index) when Q is itself
    one of the pool texts and must be left out. `frac` scales the sample size
    (1.0 = the size of the smaller writing sample, as in the paper)."""
    sizes = {}
    for name, pg in pools.items():
        tot = pg.pool.total_words()
        if own is not None and own[0] == name:
            tot -= int(pg.pool.nwords[own[1]])
        sizes[name] = tot
    target = int(round(min(sizes.values()) * frac))
    nq = len(q_grams)
    result = {}
    for name, pg in pools.items():
        if nq == 0:
            result[name] = 0.0
            continue
        gid = pg.ids_for(q_grams)
        excl = own[1] if (own is not None and own[0] == name) else None
        vals = []
        for r in range(len(pg.orders)):
            cut = pg.cutoff(r, target, excl)
            vals.append(pg.present(r, gid, cut, excl).mean())
        result[name] = float(np.mean(vals))
    return result


def leave_one_out(pools: dict[str, PoolGrams], frac: float = 1.0) -> dict[str, np.ndarray]:
    """Overlap of every pool text with every candidate's samples, the text
    itself left out of its own author's sample. Returns, per candidate name,
    an array (n_texts_of_all_pools_concatenated,) of averaged overlaps, in the
    order of `pools` and of each pool's docs."""
    names = list(pools)
    out = {name: [] for name in names}
    for qname in names:
        qpg = pools[qname]
        n_docs = len(qpg.pool.texts)
        # gram ids of every doc's n-grams, in each candidate's numbering
        gram_strs = None
        for cname in names:
            cpg = pools[cname]
            if cname == qname:
                gid = qpg.pair_gram
            else:
                if gram_strs is None:
                    inv = np.empty(len(qpg.gram2id), dtype=object)
                    for s, i in qpg.gram2id.items():
                        inv[i] = s
                    gram_strs = inv[qpg.pair_gram]
                d = cpg.gram2id
                gid = np.fromiter((d.get(s, -1) for s in gram_strs), dtype=np.int64, count=len(gram_strs))
            acc = np.zeros(n_docs, dtype=np.float64)
            for r in range(len(cpg.orders)):
                # per doc: target and cutoff
                pres = np.zeros(len(gid), dtype=bool)
                ok = gid >= 0
                fp = cpg.first_pos[r][gid[ok]]
                fd = cpg.first_doc[r][gid[ok]]
                sp = cpg.second_pos[r][gid[ok]]
                docs_ok = qpg.pair_doc[ok]
                # sample size for each held-out doc
                sizes = {}
                for name in names:
                    tot = pools[name].pool.total_words()
                    sizes[name] = np.full(n_docs, tot, dtype=np.int64)
                sizes[qname] = sizes[qname] - qpg.pool.nwords
                target = np.round(np.minimum.reduce([sizes[nm] for nm in names]) * frac).astype(np.int64)
                cum = cpg.cum[r]
                cut = np.searchsorted(cum, target, side="left")
                if cname == qname:
                    posq = cpg.pos[r]
                    inside = posq < cut
                    cut2 = np.searchsorted(cum, target + qpg.pool.nwords, side="left")
                    cut = np.where(inside, cut2, cut)
                cut = np.minimum(cut, len(cum) - 1)
                cut_pair = cut[docs_ok]
                if cname == qname:
                    res = np.where(fd == docs_ok, sp < cut_pair, fp < cut_pair)
                else:
                    res = fp < cut_pair
                pres[ok] = res
                hits = np.bincount(qpg.pair_doc, weights=pres, minlength=n_docs)
                acc += hits / np.maximum(qpg.types_per_doc, 1)
            out[cname].append(acc / len(cpg.orders))
    return {name: np.concatenate(v) for name, v in out.items()}


def decide(scores: dict[str, float]) -> str | None:
    """Winner by the larger overlap; None on a tie."""
    items = sorted(scores.items(), key=lambda kv: -kv[1])
    if len(items) > 1 and items[0][1] == items[1][1]:
        return None
    return items[0][0]
