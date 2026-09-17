"""
phon.py -- pronunciation-based features (syllables, stress, rhyme, phonemes)
using the CMU Pronouncing Dictionary via the `pronouncing`/`cmudict` packages,
with a conservative fallback for words the dictionary lacks (archaic forms,
proper names, elisions such as o'er, e'er, 'kerchief).
"""
import re
from collections import Counter
import pronouncing
from stylo import normalise, tokens

_CMU = None
def cmu():
    global _CMU
    if _CMU is None:
        import cmudict
        _CMU = cmudict.dict()
    return _CMU

# Poetic elisions and archaic forms not in CMU
EXTRA = {
    "o'er": ['OW1 R'], "e'er": ['EH1 R'], "ne'er": ['N EH1 R'],
    "'twas": ['T W AH1 Z'], "twas": ['T W AH1 Z'], "tis": ['T IH1 Z'],
    "'tis": ['T IH1 Z'], "ere": ['EH1 R'], "kerchief": ['K ER1 CH IH0 F'],
    "'kerchief": ['K ER1 CH IH0 F'], "blixem": ['B L IH1 K S AH0 M'],
    "dunder": ['D AH1 N D ER0'], "donder": ['D AA1 N D ER0'],
    "blitzen": ['B L IH1 T S AH0 N'], "nick": ['N IH1 K'],
    "st": ['S EY1 N T'], "thro'": ['TH R UW1'], "thro": ['TH R UW1'],
    "e'en": ['IY1 N'], "ev'ry": ['EH1 V R IY0'], "heav'n": ['HH EH1 V AH0 N'],
    "o'": ['AH0'], "i'": ['IH0'], "wi'": ['W IH0'], "th'": [''],
    "sugar-plums": ['SH UH1 G ER0 P L AH2 M Z'],
    "sugarplums": ['SH UH1 G ER0 P L AH2 M Z'],
    "stockings": ['S T AA1 K IH0 NG Z'], "reindeer": ['R EY1 N D IH2 R'],
    "hoof": ['HH UW1 F'], "prancing": ['P R AE1 N S IH0 NG'],
    "pawing": ['P AO1 IH0 NG'], "tarnished": ['T AA1 R N IH0 SH T'],
    "twinkled": ['T W IH1 NG K AH0 L D'], "encircled": ['EH0 N S ER1 K AH0 L D'],
    "chubby": ['CH AH1 B IY0'], "jolly": ['JH AA1 L IY0'],
    "elf": ['EH1 L F'], "moon": ['M UW1 N'], "lustre": ['L AH1 S T ER0'],
    "coursers": ['K AO1 R S ER0 Z'], "dasher": ['D AE1 SH ER0'],
    "prancer": ['P R AE1 N S ER0'], "vixen": ['V IH1 K S IH0 N'],
    "comet": ['K AA1 M IH0 T'], "cupid": ['K Y UW1 P IH0 D'],
}

VOWELS = set('AEIOU')

def phones_for(word):
    w = word.lower()
    if w in EXTRA:
        return EXTRA[w]
    ps = cmu().get(w)
    if ps:
        return [' '.join(p) for p in ps]
    w2 = w.strip("'")
    if w2 in EXTRA:
        return EXTRA[w2]
    ps = cmu().get(w2)
    if ps:
        return [' '.join(p) for p in ps]
    # -'d and -eth, -est endings
    m = re.match(r"^(.*)'d$", w2)
    if m:
        base = cmu().get(m.group(1) + 'ed') or cmu().get(m.group(1))
        if base:
            return [' '.join(base[0]) + ' D']
    return None

def syllables_heuristic(word):
    w = re.sub(r"[^a-z]", '', word.lower())
    if not w:
        return 0
    w = re.sub(r'e$', '', w) if len(w) > 2 and not w.endswith(('le', 'ee', 'ye', 'oe')) else w
    groups = re.findall(r'[aeiouy]+', w)
    n = len(groups)
    return max(1, n)

def syllables(word):
    ps = phones_for(word)
    if ps:
        p = ps[0]
        return sum(1 for ph in p.split() if ph and ph[-1].isdigit())
    return syllables_heuristic(word)

def stress_pattern(word):
    """String like '10' for a trochee, '01' iamb, '1' monosyllable.
    Monosyllabic function words are marked '0' (unstressed) so that
    line-initial foot detection is sensible; content monosyllables '1'."""
    ps = phones_for(word)
    if ps:
        s = ''.join(ph[-1] for ph in ps[0].split() if ph and ph[-1].isdigit())
        s = s.replace('2', '1')
        if len(s) == 1:
            return '0' if word.lower() in FUNCTION_MONO else '1'
        return s
    n = syllables_heuristic(word)
    return '?' * n

FUNCTION_MONO = set("""a an the and but or nor of to in on at by for from with as
if than that this these those his her its my our your their it he she we they
you i me him them us who whom which what when where while so too not no yes
up down out off o'er e'er ne'er was were is are be been am had has have do did
does shall will should would could may might must can then there here all each
some any such both few more most o' i' wi' th' 'twas twas tis 'tis ere yet still
just now how ah oh""".split())

def line_words(line):
    return tokens(line)

def line_syllables(line):
    return sum(syllables(w) for w in line_words(line))

def line_stress(line):
    return ''.join(stress_pattern(w) for w in line_words(line))

def initial_foot(line):
    """'anapest' if the first stressed syllable is the 3rd syllable,
    'iamb' if the 2nd, 'trochee/spondee' if the 1st, '?' if unknown."""
    s = line_stress(line)
    if not s or '?' in s[:3]:
        return '?'
    i = s.find('1')
    if i == 2:
        return 'anapest'
    if i == 1:
        return 'iamb'
    if i == 0:
        return 'stressed'
    return 'other'

def final_word(line):
    ws = line_words(line)
    return ws[-1] if ws else ''

def feminine_ending(line):
    w = final_word(line)
    s = stress_pattern(w)
    return len(s) > 1 and s.endswith('0')

def rhyme_part(word):
    ps = phones_for(word)
    if not ps:
        return None
    return pronouncing.rhyming_part(ps[0])

def couplet_rhymes(verse_lines):
    """Assume rhymed couplets (aabb): return list of (w1, w2, kind) where
    kind in {'perfect','identical','imperfect','unknown'}."""
    out = []
    ends = [final_word(l) for l in verse_lines]
    for i in range(0, len(ends) - 1, 2):
        a, b = ends[i], ends[i + 1]
        ra, rb = rhyme_part(a), rhyme_part(b)
        if a == b:
            kind = 'identical'
        elif ra is None or rb is None:
            kind = 'unknown'
        elif ra == rb:
            kind = 'perfect'
        else:
            kind = 'imperfect'
        out.append((a, b, kind))
    return out

def phone_counts(text, strip_stress=True):
    c = Counter()
    for w in tokens(text):
        ps = phones_for(w)
        if not ps:
            continue
        for ph in ps[0].split():
            if not ph:
                continue
            c[re.sub(r'\d', '', ph) if strip_stress else ph] += 1
    return c

def coverage(text):
    ws = tokens(text)
    known = sum(1 for w in ws if phones_for(w))
    return known / max(1, len(ws))
