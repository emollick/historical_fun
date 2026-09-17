"""Shared helpers for the Beale-cipher statistics scripts (stats_*.py).

Data: $B/data/primary/  (parsed from the Wikisource transcription of the 1885 pamphlet).
Key:  a straight consecutive count of the words of the Declaration as printed in the
      pamphlet (parenthetical numbers stripped).  The pamphlet's own printed numbering
      differs from a straight count (its "(480)" appears twice, so from there on the
      pamphlet numbers run 10 behind a straight count); see stats_00_key_check.py for
      how far the straight count reproduces the printed decipherment of cipher 2.
"""
import json
import os
import re
from collections import Counter

import numpy as np

B = os.environ.get("BEALE_DIR", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
DATA = os.path.join(B, "data", "primary")
RESULTS = os.path.join(B, "results")
CODE = os.path.join(B, "code")

ALPHA = "abcdefghijklmnopqrstuvwxyz"


def load_cipher(n):
    with open(os.path.join(DATA, f"cipher{n}.txt")) as f:
        return np.array([int(x) for x in f.read().split()], dtype=int)


def load_ciphers():
    return {k: load_cipher(k) for k in (1, 2, 3)}


def load_key_words():
    """Words of the Declaration as printed in the pamphlet, straight count (1-based
    positions = index+1).  Parenthetical numbers are stripped first."""
    with open(os.path.join(DATA, "doi_pamphlet_as_printed.txt")) as f:
        t = f.read()
    t = re.sub(r"\(\d+\)", " ", t)
    return t.split()


def word_initial(w):
    m = re.search(r"[A-Za-z]", w)
    return m.group(0).lower() if m else None


def load_key_initials():
    return [word_initial(w) for w in load_key_words()]


def decode(cipher, initials, oob="?"):
    """Book-cipher decode: number n -> initial letter of key word n (1-based)."""
    out = []
    K = len(initials)
    for n in cipher:
        if 1 <= n <= K and initials[n - 1]:
            out.append(initials[n - 1])
        else:
            out.append(oob)
    return "".join(out)


def letters_only(text):
    return re.sub(r"[^a-z]", "", text.lower())


def load_b2_plaintext_letters():
    with open(os.path.join(DATA, "b2_plaintext_as_printed.txt")) as f:
        t = f.read()
    # drop the editorial lead-in line of the pamphlet
    t = t.split("as follows:", 1)[1]
    return letters_only(t)


def load_prose_letters():
    """English prose of the pamphlet's 'Beale' letters, letters only (for simulations)."""
    parts = []
    for fn in ("letter_1822-01-04.txt", "letter_1822-01-05.txt", "letter_1822-05-09.txt"):
        with open(os.path.join(DATA, fn)) as f:
            parts.append(f.read())
    return letters_only(" ".join(parts))


def load_pamphlet_prose_letters():
    """All narrative prose in the pamphlet except the ciphers and the Declaration."""
    parts = []
    for fn in ("narrative_anonymous_author.txt", "morriss_statement.txt",
               "letter_1822-01-04.txt", "letter_1822-01-05.txt", "letter_1822-05-09.txt"):
        with open(os.path.join(DATA, fn)) as f:
            parts.append(f.read())
    return letters_only(" ".join(parts))


# Letter frequencies of English text (per cent), from Peter Norvig's count over the
# Google Books n-gram corpus (http://norvig.com/mayzner.html, "Letter counts" table).
ENGLISH_FREQ_NORVIG = {
    "e": 12.49, "t": 9.28, "a": 8.04, "o": 7.64, "i": 7.57, "n": 7.23, "s": 6.51,
    "r": 6.28, "h": 5.05, "l": 4.07, "d": 3.82, "c": 3.34, "u": 2.73, "m": 2.51,
    "f": 2.40, "p": 2.14, "g": 1.87, "w": 1.68, "y": 1.66, "b": 1.48, "v": 1.05,
    "k": 0.54, "x": 0.23, "j": 0.16, "q": 0.12, "z": 0.09,
}


def english_probs():
    p = np.array([ENGLISH_FREQ_NORVIG[c] for c in ALPHA], dtype=float)
    return p / p.sum()


def freq_vector(text):
    c = Counter(text)
    return np.array([c.get(ch, 0) for ch in ALPHA], dtype=float)


def chi2_gof(obs, expected_probs, min_expected=None):
    """Pearson chi-square goodness-of-fit against given probabilities; returns
    (statistic, dof, p).  Categories with tiny expectation are pooled if requested."""
    from scipy import stats
    obs = np.asarray(obs, dtype=float)
    p = np.asarray(expected_probs, dtype=float)
    p = p / p.sum()
    exp = obs.sum() * p
    if min_expected is not None:
        # pool small categories into one
        big = exp >= min_expected
        if (~big).sum() > 1:
            obs = np.concatenate([obs[big], [obs[~big].sum()]])
            exp = np.concatenate([exp[big], [exp[~big].sum()]])
    stat = float(((obs - exp) ** 2 / exp).sum())
    dof = len(obs) - 1
    return stat, dof, float(stats.chi2.sf(stat, dof))


def kl_div(p, q, eps=1e-12):
    p = np.asarray(p, float); q = np.asarray(q, float)
    p = p / p.sum(); q = q / q.sum()
    mask = p > 0
    return float(np.sum(p[mask] * np.log((p[mask] + eps) / (q[mask] + eps))))


def js_div(p, q):
    p = np.asarray(p, float) / np.sum(p); q = np.asarray(q, float) / np.sum(q)
    m = 0.5 * (p + q)
    return 0.5 * kl_div(p, m) + 0.5 * kl_div(q, m)


def save_json(obj, name):
    path = os.path.join(RESULTS, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=_default)
    return path


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(str(type(o)))


def mc_se(p, n):
    """Monte Carlo standard error of an estimated proportion p from n draws."""
    return float(np.sqrt(max(p * (1 - p), 1.0 / n / 4) / n))


def perm_pvalue(count_ge, n):
    """(count+1)/(n+1) permutation p-value (Phipson & Smyth 2010)."""
    return (count_ge + 1) / (n + 1)
