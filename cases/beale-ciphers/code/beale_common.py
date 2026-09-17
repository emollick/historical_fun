"""Shared loaders for the Beale-cipher analyses.

All paths are resolved relative to this file, so every script in code/ can be run
from anywhere; from the case folder:  python3 code/<script>.py

Tokenisation rules (documented in notes/cryptanalysis_b2_gillogly.md):
  * a word = maximal run of letters, with internal apostrophes kept ("nature's" = 1 word);
  * hyphens and dashes SPLIT words ("self-evident" = 2 words, "war—in" = 2 words).  This is
    the convention the pamphlet's own numbering uses at words 78/79 ("self (78) evident (79)
    that (80)"), and it is also Gillogly's (Table I, row 71: S E T at 78-80);
  * digits and every other character are ignored; the printed word numbers "(20)" are removed
    before counting;
  * an alternative "hyphen-joined" straight count is also produced for comparison.
"""
import os, re, csv, json
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..'))
PRIMARY = os.path.join(B, 'data', 'primary')
SOURCES = os.path.join(B, 'sources')
RESULTS = os.path.join(B, 'results')

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")


def load_cipher(n):
    with open(os.path.join(PRIMARY, f'cipher{n}.txt')) as f:
        return [int(x) for x in f.read().split()]


def load_b2_plaintext_letters():
    """Letters of the decipherment as printed in the pamphlet (770 letters)."""
    t = open(os.path.join(PRIMARY, 'b2_plaintext_as_printed.txt'), encoding='utf-8').read()
    t = t.split('as follows:', 1)[1]
    return re.sub(r'[^A-Za-z]', '', t).lower(), t


def pamphlet_doi_raw():
    return open(os.path.join(PRIMARY, 'doi_pamphlet_as_printed.txt'), encoding='utf-8').read()


def tokenize(text, split_hyphens=True):
    """Return list of lower-cased word tokens."""
    if split_hyphens:
        text = re.sub(r'[-—–]', ' ', text)
    else:
        text = re.sub(r'[—–]', ' ', text)   # dashes always split
        text = text.replace('-', "")                  # hyphenated word counted as one
    return [w.lower() for w in WORD_RE.findall(text)]


def parse_pamphlet_doi(split_hyphens=True):
    """Parse the DOI as printed, keeping the printed word numbers.

    Returns a list of dicts: {'word', 'marker'} where marker is the printed number that
    follows the word (or None).  The printed "(N)" is attached to the word immediately
    preceding it.
    """
    raw = pamphlet_doi_raw()
    if split_hyphens:
        raw = re.sub(r'[-—–]', ' ', raw)
    else:
        raw = re.sub(r'[—–]', ' ', raw).replace('-', '')
    toks = []
    for m in re.finditer(r"([A-Za-z]+(?:'[A-Za-z]+)*)|\((\d+)\)", raw):
        if m.group(1):
            toks.append({'word': m.group(1).lower(), 'marker': None})
        else:
            assert toks, 'marker before any word'
            toks[-1]['marker'] = int(m.group(2))
    return toks


def straight_numbering(toks):
    """(a) straight consecutive count of the printed words: number -> word (1-based)."""
    return OrderedDict((i + 1, t['word']) for i, t in enumerate(toks))


def pamphlet_numbering(toks):
    """(b) numbering implied by the printed markers.

    Returns (forward, backward, anomalies, continued_start):
      forward[n]  : word obtained by counting forward from the previous printed marker
                    (the marked word itself always gets its printed number);
      backward[n] : word obtained by counting backward from the next printed marker;
      the two agree except inside the gaps whose word count disagrees with the marker
      step ("anomalies").  After the last marker the count continues forward.
    Each map is number -> word; where the same number is printed twice (the duplicated
    "(480)") the forward map keeps BOTH words as a list under that number.
    """
    forward, backward = {}, {}
    anomalies = []
    # split into segments ending at each marker
    segs, cur = [], []
    for t in toks:
        cur.append(t['word'])
        if t['marker'] is not None:
            segs.append((t['marker'], cur))
            cur = []
    tail = cur  # words after the last marker
    prev_marker = 0
    for (mk, words) in segs:
        G = len(words)
        step = mk - prev_marker
        if G != step:
            anomalies.append({'segment_end_marker': mk, 'prev_marker': prev_marker,
                              'words_in_segment': G, 'marker_step': step,
                              'words': ' '.join(words)})
        # forward count from previous marker
        for k, w in enumerate(words):
            n = prev_marker + k + 1
            if k == G - 1:
                n = mk  # the marked word gets its printed number
            forward.setdefault(n, [])
            forward[n].append(w)
        # backward count from this marker
        for k, w in enumerate(words):
            n = mk - (G - 1 - k)
            backward.setdefault(n, [])
            backward[n].append(w)
        prev_marker = mk
    last = prev_marker
    for k, w in enumerate(tail):
        n = last + k + 1
        forward.setdefault(n, []).append(w)
        backward.setdefault(n, []).append(w)
    return forward, backward, anomalies, last


def nara_tokens(split_hyphens=True):
    t = open(os.path.join(SOURCES, 'nara_doi_plain.txt'), encoding='utf-8').read()
    i = t.index('When in the Course of human events')
    j = t.index('our sacred Honor.') + len('our sacred Honor.')
    body = t[i:j]
    return tokenize(body, split_hyphens=split_hyphens), body


def gillogly_table1():
    """Parse Gillogly's Table I (initial letters, 1322 words) -> dict number -> letter."""
    t = open(os.path.join(SOURCES, 'gillogly_1980_plain.txt'), encoding='utf-8').read()
    i = t.index(' 1  WITCOHEIBN')
    j = t.index('Table I. Initial letters')
    block = t[i:j]
    key = {}
    for m in re.finditer(r'(\d+|4\dl|41l)\s+([A-Z]{1,10})', block):
        start = int(m.group(1).replace('l', '1'))
        for k, ch in enumerate(m.group(2)):
            key[start + k] = ch
    return key


def gillogly_table2():
    t = open(os.path.join(SOURCES, 'gillogly_1980_plain.txt'), encoding='utf-8').read()
    i = t.index('Table I. Initial letters')
    j = t.index('Table II. The Beale Treasure Cipher')
    block = t[i + len('Table I. Initial letters of words in the Declaration of Independence.'):j]
    raw = re.findall(r'[0-9l]+', block)
    nums = [int(x.replace('l', '1')) for x in raw]
    return nums, raw


def gillogly_table3():
    t = open(os.path.join(SOURCES, 'gillogly_1980_plain.txt'), encoding='utf-8').read()
    i = t.index('Table II. The Beale Treasure Cipher (B1).')
    j = t.index('Table III.')
    block = t[i + len('Table II. The Beale Treasure Cipher (B1).'):j]
    return re.sub(r'[^A-Z?]', '', block)


def initial(word):
    return word[0].upper()


def decode(nums, key, unknown='?'):
    """key: number -> word (str) or list of words; returns string of initials."""
    out = []
    for n in nums:
        w = key.get(n)
        if w is None:
            out.append(unknown)
        elif isinstance(w, list):
            out.append(initial(w[0]) if len(set(initial(x) for x in w)) == 1 else '#')
        else:
            out.append(initial(w))
    return ''.join(out)


def write_csv(path, rows, header):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
