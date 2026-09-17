"""Check how the pamphlet's printed word-numbering of the Declaration differs from a
straight count, build candidate numberings, and measure how well each decodes
cipher 2 to the printed decipherment (positional agreement; B2 has 763 numbers).

Outputs results/stats_key_check.json.  The other candidate keys are used only where a
test needs the numbering the B2 encoder actually used (encoder model, letter test 5c).
"""
import re, os, json
import numpy as np
from stats_common import *

with open(os.path.join(DATA, "doi_pamphlet_as_printed.txt")) as f:
    raw = f.read()

# --- 1. tokens with markers -------------------------------------------------------
tokens = raw.split()
words, markers = [], []   # markers: (printed number, index of preceding word in straight count)
for tok in tokens:
    m = re.fullmatch(r"\((\d+)\)", tok)
    if m:
        markers.append((int(m.group(1)), len(words)))   # len(words) = straight-count number of preceding word
    else:
        # a token may carry a trailing marker glued on, e.g. "fundamentally,(811)" - handle
        m2 = re.fullmatch(r"(.*?)\((\d+)\)", tok)
        if m2:
            words.append(m2.group(1)); markers.append((int(m2.group(2)), len(words)))
        else:
            words.append(tok)
straight = words
print("straight count:", len(straight))

# straight count with "self-evident" split into two words (Gillogly 1980 Table I numbering)
split = []
for w in straight:
    if w.lower().startswith("self-evident"):
        split += ["self", "evident" + w[len("self-evident"):]]
    else:
        split.append(w)
print("split count:", len(split))
split_index = {}
j = 0
# map straight index -> split index (1-based)
straight_to_split = []
for w in straight:
    j += 2 if w.lower().startswith("self-evident") else 1
    straight_to_split.append(j)

dev = []
for num, idx in markers:
    dev.append({"printed": num, "straight": idx, "split": straight_to_split[idx - 1],
                "printed_minus_split": num - straight_to_split[idx - 1]})
print("printed marker vs straight/split counts (only where the offset changes):")
last = None
for d in dev:
    if d["printed_minus_split"] != last:
        print("  ", d)
        last = d["printed_minus_split"]

# --- 2. pamphlet numbering: follow the printed markers (each marker (N) fixes the number of
# the word before it; words between markers are numbered consecutively from the previous
# marker).  Where (480) is printed twice, the ten words before the second (480) get 471-480 a
# second time; we keep the FIRST word for each number ("pamphlet_first") or the SECOND
# ("pamphlet_second"), and 'pamphlet_skip' gives those ten words no number at all (same as
# either variant for all numbers >= 481).
def pamphlet_numbering(prefer="first"):
    # work on the split token list (the pamphlet counts "self-evident" as two words: its
    # "(80)" marker follows the 9th token after "(70)"); markers are re-indexed accordingly.
    mk = {straight_to_split[idx - 1]: num for num, idx in markers}   # split index -> printed number
    numbering = [None] * len(split)
    prev_marker_word = 0
    prev_marker_num = 0
    for i in range(1, len(split) + 1):
        if i in mk:
            N = mk[i]
            n_words = i - prev_marker_word
            # words prev_marker_word+1 .. i get numbers N-n_words+1 .. N (counting back from
            # the marker; where a group has 11 words the first word shares a number with the
            # last word of the previous group, where it has 9 a number is skipped)
            for k in range(n_words):
                numbering[prev_marker_word + k] = N - n_words + 1 + k
            prev_marker_word, prev_marker_num = i, N
    for i in range(prev_marker_word, len(split)):
        numbering[i] = prev_marker_num + (i - prev_marker_word) + 1
    key = {}
    for w, n in zip(split, numbering):
        if n in key and prefer == "first":
            continue
        key[n] = w
    return key, numbering

pam_first, numbering = pamphlet_numbering("first")
pam_second, _ = pamphlet_numbering("second")
maxn = max(pam_first)
print("pamphlet numbering: max number", maxn, "; numbers assigned twice:",
      sorted(n for n in set(numbering) if numbering.count(n) > 1)[:3], "...")

def key_to_initials(keydict):
    K = max(keydict)
    return [word_initial(keydict[n]) if n in keydict else None for n in range(1, K + 1)]

cands = {
    "straight": [word_initial(w) for w in straight],
    "split_selfevident": [word_initial(w) for w in split],
    "pamphlet_first": key_to_initials(pam_first),
    "pamphlet_second": key_to_initials(pam_second),
}
# 'resolved': the pamphlet numbering plus three conventions the B2 encoder demonstrably used
# (the DOI has no word beginning with x or y): 811 -> y ("fundamentally" carries a y), 1005 -> x
# ("have"? - the encoder's x; see results/b2_decode_summary.json), and
# 95 -> u ("unalienable", the wording of the original Declaration, printed "inalienable" here).
resolved = list(cands["pamphlet_first"])
while len(resolved) < 1005:
    resolved.append(None)
resolved[811 - 1] = "y"; resolved[1005 - 1] = "x"; resolved[95 - 1] = "u"
cands["resolved"] = resolved

# --- 3. the plaintext of cipher 2 as the encoder must have spelled it (763 letters) -------
# The printed decipherment writes some things as figures ("1819", "$13,000", '"3"') and
# edits the wording ("one thousand and fourteen", "three thousand eight hundred", "eighty-eight
# pounds of silver", "in exchange for silver to save"); the decode under the pamphlet's own
# numbering shows the enciphered wording was "ten hundred", "thirty eight hundred", "eighty
# eight of silver", "in exchange to save", with "Nov" and "Dec" abbreviated.  This spelled-out
# version has exactly 763 letters, one per cipher number.
PT = ("i have deposited in the county of bedford about four miles from bufords in an "
      "excavation or vault six feet below the surface of the ground the following articles "
      "belonging jointly to the parties whose names are given in number three herewith the "
      "first deposit consisted of ten hundred and fourteen pounds of gold and thirty eight "
      "hundred and twelve pounds of silver deposited nov eighteen nineteen the second was made "
      "dec eighteen twenty one and consisted of nineteen hundred and seven pounds of gold and "
      "twelve hundred and eighty eight of silver also jewels obtained in st louis in exchange "
      "to save transportation and valued at thirteen thousand dollars the above is securely "
      "packed in iron pots with iron covers the vault is roughly lined with stone and the "
      "vessels rest on solid stone and are covered with others paper number one describes the "
      "exact locality of the vault so that no difficulty will be had in finding it")
pt = letters_only(PT)
c2 = load_cipher(2)
print("spelled-out plaintext letters:", len(pt), "; cipher 2 numbers:", len(c2))
# The printed cipher has 762 numbers once the spurious leading "2" of the Wikisource
# transcription is dropped (results/transcription_check.json); the intended message has 763
# letters - the printed "108" at position 571 stands for "10 8" (n, i).  The alignment below
# absorbs the difference; here we only compare positionally up to the shorter length.

out = {"straight_count": len(straight), "split_count": len(split),
       "marker_deviations": dev, "plaintext_763": pt, "candidates": {}}
for name, ini in cands.items():
    d = decode(c2, ini)
    m = min(len(d), len(pt))
    agree = np.array([a == b for a, b in zip(d[:m], pt[:m])])
    # positional agreement is only meaningful up to the first insertion/deletion (pos 571);
    # the alignment in section 4 gives the exact error list for the best candidate.
    m2 = 570
    agree2 = agree[:m2]
    out["candidates"][name] = {"key_length": len(ini), "agree_first570": int(agree2.sum()),
                               "agree_frac_first570": float(agree2.mean())}
    print(f"{name:20s} key={len(ini):4d}  positional agreement over the first 570 numbers: "
          f"{agree2.sum()}/570 = {agree2.mean():.3f}")

best = max(out["candidates"], key=lambda k: out["candidates"][k]["agree_first570"])
out["best"] = best
print("best candidate:", best)
# also dump the best key's initials for other scripts
out["best_initials"] = cands[best]
save_json(out, "stats_key_check.json")
with open(os.path.join(RESULTS, "stats_key_best_initials.json"), "w") as f:
    json.dump({"name": best, "initials": cands[best], "straight": cands["straight"]}, f)

# --- 4. alignment of the best decode with the intended plaintext ---------------------
# Needleman-Wunsch (match +1, mismatch -1, gap -2) so that a one-letter shift (an extra
# cipher number, or a skipped plaintext letter) is absorbed by a gap pair instead of a
# long run of 'errors'.  Gives, for every cipher-2 number, the letter the encoder intended.
def align(a, b, match=1, mismatch=-1, gap=-2):
    n, m = len(a), len(b)
    S = np.zeros((n + 1, m + 1)); T = np.zeros((n + 1, m + 1), dtype=int)  # 0 diag,1 up,2 left
    S[:, 0] = gap * np.arange(n + 1); S[0, :] = gap * np.arange(m + 1)
    T[1:, 0] = 1; T[0, 1:] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d = S[i - 1, j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            u = S[i - 1, j] + gap; l = S[i, j - 1] + gap
            best = max(d, u, l)
            S[i, j] = best; T[i, j] = 0 if best == d else (1 if best == u else 2)
    i, j = n, m; pairs = []
    while i > 0 or j > 0:
        t = T[i, j]
        if i > 0 and j > 0 and t == 0:
            pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif i > 0 and (j == 0 or t == 1):
            pairs.append((i - 1, None)); i -= 1
        else:
            pairs.append((None, j - 1)); j -= 1
    return pairs[::-1]

dec_best = decode(c2, cands[best])
pairs = align(dec_best, pt)
assign = [None] * len(c2)       # intended letter for each cipher position
skipped_letters = []
for ci, pj in pairs:
    if ci is not None and pj is not None:
        assign[ci] = pt[pj]
    elif pj is not None:
        skipped_letters.append({"plaintext_pos": pj + 1, "letter": pt[pj]})
extra_numbers = [i + 1 for i, a in enumerate(assign) if a is None]
records = []
for i, n in enumerate(c2):
    records.append({"pos": i + 1, "number": int(n), "decoded": dec_best[i], "intended": assign[i],
                    "error": (assign[i] is not None and dec_best[i] != assign[i])})
n_err = sum(r["error"] for r in records)
print(f"alignment: {n_err} substitution errors, {len(extra_numbers)} extra numbers at {extra_numbers}, "
      f"{len(skipped_letters)} skipped letters {skipped_letters}")
# error offsets: is number +-1 / +-10 a correct homophone?
ini_best = cands[best]
def homs(letter):
    return {i + 1 for i, c in enumerate(ini_best) if c == letter}
err_types = Counter()
for r in records:
    if r["error"]:
        n, L = r["number"], r["intended"]
        H = homs(L)
        kind = "other"
        for d in (1, -1, 10, -10, 2, -2, 11, -11, 9, -9):
            if n + d in H:
                kind = f"{d:+d}"; break
        err_types[kind] += 1
        r["error_kind"] = kind
print("error kinds (offset that would make the number a correct homophone):", dict(err_types))
out["b2_alignment"] = {"n_substitution_errors": n_err, "extra_numbers_pos": extra_numbers,
                       "skipped_letters": skipped_letters, "error_kinds": dict(err_types),
                       "records": records}
save_json(out, "stats_key_check.json")
