"""Hand-picked feature tests raised in the literature:
 - Pival (1990s, via Nickell 1989 / Emerson 2008): Lincoln prefers shall/should, Hay will/would;
   perfect aspect (have/has/had + participle); passive voice.
 - Burlingame 1995: 'beguile', 'gloriously', 'cherish', 'Republic', 'Heavenly Father', 'tender'.
 - Townsend / Bullard 1946: Lincoln's fondness for adverbial 'so' ('so costly a sacrifice').
Counts per 10,000 words in each corpus, with document-level presence rates."""
import re
from collections import Counter
from ngt import sentences, word_tokens

def toks(text):
    out = []
    for s in sentences(text): out.extend(word_tokens(s))
    return out

PARTICIPLE_IRREG = set('been done gone seen given taken known written made said come become fallen laid lain lost found held kept left met paid put sent set shown told thought brought bought caught fought sought taught felt built dealt meant read spent stood understood won begun drunk sung sworn torn worn born borne chosen driven risen spoken stolen striven woven forgotten gotten hidden ridden bidden forbidden beaten eaten shaken mistaken undertaken overtaken'.split())

def perfect_count(t):
    n = 0
    for i, w in enumerate(t[:-1]):
        if w in ('have', 'has', 'had', 'having'):
            nxt = t[i+1]
            if nxt.endswith('ed') or nxt in PARTICIPLE_IRREG or nxt in ('been',):
                n += 1
            elif nxt in ('not', 'never', 'also', 'always', 'been', 'already', 'just', 'ever', 'long', 'since') and i+2 < len(t):
                n2 = t[i+2]
                if n2.endswith('ed') or n2 in PARTICIPLE_IRREG: n += 1
    return n

def passive_count(t):
    n = 0
    BE = ('is', 'are', 'was', 'were', 'be', 'been', 'being', 'am')
    for i, w in enumerate(t[:-1]):
        if w in BE:
            nxt = t[i+1]
            if (nxt.endswith('ed') and len(nxt) > 3) or nxt in PARTICIPLE_IRREG:
                n += 1
            elif nxt in ('not', 'never', 'also', 'always', 'so', 'thus', 'now', 'then', 'well', 'often') and i+2 < len(t):
                n2 = t[i+2]
                if (n2.endswith('ed') and len(n2) > 3) or n2 in PARTICIPLE_IRREG: n += 1
    return n

def modal_counts(t):
    c = Counter(w for w in t if w in ('shall', 'should', 'will', 'would', 'may', 'might', 'can', 'could', 'must'))
    return c

def so_adverb(t):
    """'so' immediately followed by an adjective/adverb-like token, excluding common
    fixed phrases (so far, so much, so that, do so, so called, so as, so long as...)."""
    n = 0
    stop = {'far', 'much', 'that', 'called', 'as', 'long', 'many', 'on', 'forth', 'and', 'to', 'the', 'it', 'i', 'he', 'we', 'they', 'you', 'is', 'do', 'be', 'in', 'if', 'of', 'a', 'well', 'soon', 'often', 'little', 'few', 'great', 'very'}
    for i, w in enumerate(t[:-1]):
        if w == 'so' and t[i+1] not in stop and t[i+1].isalpha():
            n += 1
    return n

WORDS = ['beguile', 'gloriously', 'cherish', 'cherished', 'republic', 'tender', 'tendering', 'assuage', 'anguish', 'bereavement', 'altar', 'overwhelming', 'solemn', 'fruitless', 'consolation', 'costly', 'sacrifice']

def profile(texts):
    T = [toks(t) for t in texts]
    N = sum(len(t) for t in T) or 1
    res = {'words': N, 'docs': len(T)}
    m = Counter()
    for t in T: m.update(modal_counts(t))
    res['modals_per10k'] = {k: round(10000 * v / N, 2) for k, v in m.items()}
    sw = m['shall'] + m['should']; ww = m['will'] + m['would']
    res['shall_should_share'] = round(sw / (sw + ww), 3) if sw + ww else None
    res['perfect_per10k'] = round(10000 * sum(perfect_count(t) for t in T) / N, 2)
    res['passive_per10k'] = round(10000 * sum(passive_count(t) for t in T) / N, 2)
    res['so_adverb_per10k'] = round(10000 * sum(so_adverb(t) for t in T) / N, 2)
    wc = Counter()
    for t in T: wc.update(w for w in t if w in WORDS)
    res['words_per10k'] = {w: round(10000 * wc[w] / N, 3) for w in WORDS}
    res['words_count'] = {w: wc[w] for w in WORDS}
    joined = [' '.join(t) for t in T]
    res['heavenly_father_docs'] = sum(1 for j in joined if 'heavenly father' in j)
    res['father_in_heaven_docs'] = sum(1 for j in joined if 'father in heaven' in j)
    return res
