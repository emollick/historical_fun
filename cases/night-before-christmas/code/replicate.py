"""
replicate.py -- replications of the specific tests argued over in the literature,
run on our cleaned corpora with corpus-size normalisation and calibration.

  jackson_words   : Jackson (2016) ch. 16 Livingston-favoured vs Moore-favoured
                    common words, per-poem percentage of Livingston-favoured tokens.
  jackson_phonemes: Jackson chs. 10-12 phoneme pairs (last phoneme of a word +
                    first phoneme of the next word within a line), discriminating
                    pairs found afresh by chi-square on OUR corpora, then the
                    per-poem Livingston share, with leave-one-poem-out honesty
                    (the discriminating pairs are re-derived without the poem
                    being scored).
  expressions     : Jackson's six 'favourite expressions' and Norsworthy's eight
                    Moore markers, rates per 1,000 words, and Poisson probabilities
                    of the poem's counts under each author's rate.
"""
import os, sys, re, math, json
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import tokens, word_count
import phon

MOORE, LIV = 'Clement Clarke Moore', 'Henry Livingston Jr.'

JACKSON_LIV = ['i', 'his', 'my', 'her', 'on', 'as', 'is', 'was', 'at', 'thy', 'will',
               'day', 'when', 'me', 'where', 'while']
JACKSON_MOORE = ['to', 'from', 'your', 'for', 'they', 'be', 'with', 'this', 'our',
                 'not', 'which', 'so', 'would', 'it', 'heart', 'of', 'are', 'we']

def jackson_words(doc_tokens):
    c = Counter(doc_tokens)
    l = sum(c[w] for w in JACKSON_LIV); m = sum(c[w] for w in JACKSON_MOORE)
    return (100.0 * l / (l + m)) if (l + m) else float('nan'), l + m

# ---------------------------------------------------------------- phoneme pairs
def phoneme_pairs(verse_lines):
    """Counter of (last phone of word_i, first phone of word_{i+1}) within lines,
    stress digits stripped, using CMU dict + phon.EXTRA; unknown words break the chain."""
    c = Counter()
    for line in verse_lines:
        ws = tokens(line)
        prev_last = None
        for w in ws:
            ps = phon.phones_for(w)
            if not ps or not ps[0].strip():
                prev_last = None; continue
            phs = [re.sub(r'\d', '', p) for p in ps[0].split() if p]
            if prev_last is not None:
                c[(prev_last, phs[0])] += 1
            prev_last = phs[-1]
    return c

def discriminating_pairs(docsA, docsB, top=100, n_each=10, exclude_ids=()):
    """Chi-square on each pair among the union of the two authors' top-`top`
    pairs; return the n_each most A-favoured and most B-favoured (by chi-square
    with the right sign), as Jackson did (ten each)."""
    cA = Counter(); cB = Counter()
    for d in docsA:
        if d['id'] not in exclude_ids: cA.update(d['_pairs'])
    for d in docsB:
        if d['id'] not in exclude_ids: cB.update(d['_pairs'])
    NA, NB = sum(cA.values()), sum(cB.values())
    cand = set(p for p, _ in cA.most_common(top)) | set(p for p, _ in cB.most_common(top))
    rows = []
    for p in cand:
        a, b = cA[p], cB[p]
        # 2x2 chi-square
        ra, rb = NA - a, NB - b
        n = NA + NB
        ea = (a + b) * NA / n; eb = (a + b) * NB / n
        if ea == 0 or eb == 0: continue
        chi = (a - ea) ** 2 / ea + (b - eb) ** 2 / eb + (ra - (NA - ea)) ** 2 / (NA - ea) + (rb - (NB - eb)) ** 2 / (NB - eb)
        rows.append((p, chi, (a / NA) > (b / NB)))
    favA = sorted([r for r in rows if r[2]], key=lambda r: -r[1])[:n_each]
    favB = sorted([r for r in rows if not r[2]], key=lambda r: -r[1])[:n_each]
    return [r[0] for r in favA], [r[0] for r in favB]

def phoneme_share(pairs_counter, favL, favM):
    l = sum(pairs_counter[p] for p in favL); m = sum(pairs_counter[p] for p in favM)
    return (100.0 * l / (l + m)) if (l + m) else float('nan'), l + m

# ---------------------------------------------------------------- expressions
JACKSON_FAV = {  # Jackson ch. 15 'favourite expressions' of Moore
    'some': r"\bsome\b", 'oft': r"\boft\b", 'many a': r"\bmany an?\b",
    'in vain': r"\bin vain\b", 'at length': r"\bat length\b", "that's": r"\bthat's\b"}
NORSWORTHY_8 = {  # Norsworthy 28 Apr 2017 'eight great favorite expressions'
    'should': r"\bshould\b", 'would': r"\bwould\b", 'like': r"\blike\b",
    'hope': r"\bhope[sd]?\b", 'ere': r"\bere\b", 'dread': r"\bdread(?:s|ed|ful)?\b",
    'vision(s)': r"\bvisions?\b", 'brain(s)': r"\bbrains?\b"}
EXTRA_MARKERS = {
    'all': r"\ball\b", 'twas': r"\b'?twas\b", 'oh': r"\boh\b", 'ah': r"\bah\b",
    'little': r"\blittle\b", 'happy': r"\bhappy\b", 'merry': r"\bmerry\b",
    'snug': r"\bsnug\b", 'jolly': r"\bjolly\b", 'chin': r"\bchin\b", 'broad': r"\bbroad\b",
    'opening': r"\bop'?ening\b", 'lustre': r"\blustre\b", 'objects': r"\bobjects?\b",
    'soon': r"\bsoon\b", 'could': r"\bcould\b", 'twinkl': r"\btwinkl", 'nap': r"\bnap\b",
    'st nick': r"\bst\.? nick\b", 'nicholas': r"\bnicholas\b", 'santa': r"\bsant[ae]",
}

def count_regex(text, pat):
    return len(re.findall(pat, text.lower()))

def expression_table(poem_text, corpora):
    """corpora: dict label -> text. Returns rows per marker with counts, rate per
    1,000 words, expected count in a poem of this length, Poisson P(X >= observed)
    (or <= when observed is 0) under each corpus's rate."""
    n_poem = word_count(poem_text)
    out = {}
    for name, pat in {**JACKSON_FAV, **NORSWORTHY_8, **EXTRA_MARKERS}.items():
        obs = count_regex(poem_text, pat)
        row = dict(observed=obs)
        for label, text in corpora.items():
            n = word_count(text); k = count_regex(text, pat)
            rate = k / n if n else 0.0
            lam = rate * n_poem
            # Poisson tail with add-half smoothing so that zero-rate authors do not give p=0
            lam_s = ((k + 0.5) / (n + 1)) * n_poem
            if obs == 0:
                p = math.exp(-lam_s)                      # P(X = 0)
            else:
                p = 1 - sum(math.exp(-lam_s) * lam_s ** i / math.factorial(i) for i in range(obs))  # P(X >= obs)
            row[label] = dict(count=k, words=n, per1000=1000.0 * rate, expected=lam, p_tail=p)
        out[name] = row
    return out

def loglik_ratio_expressions(table, a='moore', b='livingston', markers=None):
    """Sum of log Poisson likelihoods (smoothed) of the poem's counts under a vs b.
    Positive = favours a."""
    markers = markers or list(table)
    tot = 0.0; detail = {}
    for m in markers:
        row = table[m]; obs = row['observed']
        def ll(lab):
            r = row[lab]; lam = ((r['count'] + 0.5) / (r['words'] + 1)) * WORDS_POEM[0]
            return -lam + obs * math.log(lam) - math.lgamma(obs + 1)
        d = ll(a) - ll(b); detail[m] = d; tot += d
    return tot, detail

WORDS_POEM = [545]
