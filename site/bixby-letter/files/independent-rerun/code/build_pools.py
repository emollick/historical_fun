"""
Build the two candidate writing samples for the paper's design from the
corpus files assembled for The Bixby Letter (data only, so that the tests
are run on the same texts). No code from that implementation was
read; the selection rules below are this rerun's own, written from the
paper's description of its corpus (preprint pp. 9-10).

Paper's design: Lincoln = everything Lincoln wrote before 18 May 1860
(the day Hay could have begun writing for him); Hay = everything by Hay.

Inputs (read only):
  ../../corpus/lincoln_basler.jsonl   Basler, Collected Works, vols I, IV, VII, VIII (OCR)
  ../../analysis/lapsley.jsonl        Lapsley's 1905 edition (Gutenberg), used for 1849-1860,
                                      which Basler vols II-III would cover
  ../../corpus/hay.jsonl              Hay: 1908 Letters and Diary, Thayer letters, Addresses,
                                      Castilian Days, The Bread-Winners, verse
Output:
  ../data/pools.json          {"lincoln_pre1860": [[id, text], ...], "hay_all": [[id, text], ...]}
  ../data/pools_manifest.csv  one line per candidate document: kept or dropped, and why
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ngt  # noqa: E402

BASE = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))
CUTOFF = "1860-05-18"
MIN_WORDS = 5

# Basler source codes that mean the document was only signed by Lincoln
# KEEP_DEBATES=1 in the environment keeps the 1858 campaign speeches and
# Lincoln's side of the Lincoln-Douglas debates (Lapsley vols 3 and 4,
# 83,000 words) in the Lincoln pool; the output is then pools_debates.json.
KEEP_DEBATES = os.environ.get("KEEP_DEBATES") == "1"
SIGNED_ONLY = {"DS", "ES", "LS", "Copies"}
# Lapsley items dated only "1860" whose text carries a full date before the cut-off
YEAR_ONLY_1860_KEEP = {"L5-0047": "Cooper Institute speech, 27 February 1860"}

_SIG = re.compile(r"\s*((A\.|ABRAHAM|Abraham)\s+LINCOLN\.?|A\. L\.)\s*$", re.I)
_YEAR = re.compile(r"\b1[78]\d\d\b")


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def clean_lapsley(text):
    """Remove the frame Lapsley prints inside the text: leading heading,
    dateline and inside-address lines, and the closing signature. Run-in
    salutations and closing formulas stay, as they do in the Basler items
    (the paper removed 'salutations and valedictions'; the Basler corpus
    used here keeps run-in salutations, so both pools are treated alike)."""
    lines = [ln.strip() for ln in text.split("\n")]
    # drop leading frame lines
    while lines:
        ln = lines[0]
        if not ln:
            lines.pop(0)
            continue
        letters = [c for c in ln if c.isalpha()]
        upper = sum(1 for c in letters if c.isupper())
        short = len(ln.split()) <= 14
        caps = letters and upper / len(letters) >= 0.85
        dateline = bool(_YEAR.search(ln)) and short
        address = short and re.match(r"^(HON\.|TO |MESSRS|[A-Z][A-Z. ]+(,\s*Esq\.?)?$)", ln) and ln.rstrip().endswith((":", ".", ",", "--", ":--"))
        if (caps and short) or dateline or address:
            lines.pop(0)
            continue
        break
    # drop the signature at the end
    while lines and (not lines[-1] or _SIG.match(lines[-1])):
        lines.pop()
    if lines:
        lines[-1] = _SIG.sub("", lines[-1])
    out = "\n".join(lines)
    # run-in salutations ("DEAR SIR:--", "FELLOW-CITIZENS:") are kept, as in
    # the Basler items
    return out.strip()


def lincoln_pool():
    docs, manifest = [], []
    # 1. Basler volume I (1824-1848)
    for d in load_jsonl(os.path.join(BASE, "corpus", "lincoln_basler.jsonl")):
        if d["volume"] != "I":
            continue
        why = None
        if (d.get("source_code") or "") in SIGNED_ONLY:
            why = "signed only (%s)" % d["source_code"]
        elif d.get("other_hand") and ("not in lincoln" in d["other_hand"].lower()
                                     or "lincoln's hand" not in d["other_hand"].lower()):
            why = "another hand: %s" % d["other_hand"][:40]
        elif d.get("hay_hand"):
            why = "Hay's hand"
        n = ngt.word_count(d["text"])
        if why is None and n < MIN_WORDS:
            why = "under %d words" % MIN_WORDS
        manifest.append(["lincoln_pre1860", d["id"], "Basler vol. I", d.get("date") or "", n,
                         "kept" if why is None else "dropped: " + why, d["heading"][:80]])
        if why is None:
            docs.append((d["id"], d["text"]))
    # 2. Lapsley for 1849 to 17 May 1860; the Lincoln-Douglas debate volumes
    #    (3 and 4) are excluded because Lapsley prints Douglas's speeches
    #    inside the same items.
    seen_text = set()
    for d in load_jsonl(os.path.join(BASE, "analysis", "lapsley.jsonl")):
        date = d.get("date") or ""
        why = None
        text = clean_lapsley(d["text"])
        if d["volume"] in (3, 4) and not KEEP_DEBATES:
            why = "debate volume (Lincoln's side of the 1858 debates; excluded by default, see KEEP_DEBATES)"
        elif d["volume"] in (3, 4) and d["text"].strip().upper().startswith("MR. DOUGLAS TO"):
            why = "letter by Douglas"
        elif d["volume"] in (3, 4) and (d.get("heading") or "").upper().startswith(("CORRESPONDENCE BETWEEN", "INTERROGATORIES")):
            why = "not Lincoln's prose (section title or Douglas's questions)"
        elif d["text"].strip().upper().startswith("THE WRITINGS OF ABRAHAM LINCOLN") or (d.get("heading") or "").upper().startswith("THE WRITINGS OF ABRAHAM LINCOLN"):
            why = "volume title"
        elif not date:
            why = "no date"
        elif len(date) == 4:
            y = int(date)
            if d["id"] in YEAR_ONLY_1860_KEEP:
                why = None
            elif not (1849 <= y <= 1859):
                why = "year only, not certainly before the cut-off" if y == 1860 else "outside range"
        elif not ("1849-01-01" <= date < CUTOFF):
            why = "outside range"
        n = ngt.word_count(text)
        if why is None and n < MIN_WORDS:
            why = "under %d words" % MIN_WORDS
        key = re.sub(r"\W+", "", text.lower())[:300]
        if why is None and key in seen_text:
            why = "duplicate text"
        if why is None:
            seen_text.add(key)
        in_range = date[:4].isdigit() and 1849 <= int(date[:4]) <= 1860
        if why is None or in_range:
            manifest.append(["lincoln_pre1860", d["id"], "Lapsley vol. %s" % d["volume"], date, n,
                             "kept" if why is None else "dropped: " + why, (d.get("heading") or "")[:80]])
        if why is None:
            docs.append((d["id"], text))
    return docs, manifest


def hay_pool():
    docs, manifest = [], []
    for d in load_jsonl(os.path.join(BASE, "corpus", "hay.jsonl")):
        n = ngt.word_count(d["text"])
        why = None if n >= MIN_WORDS else "under %d words" % MIN_WORDS
        manifest.append(["hay_all", d["id"], "%s (%s)" % (d["source"], d["kind"]), d.get("date") or "", n,
                         "kept" if why is None else "dropped: " + why, (d.get("heading") or "")[:80]])
        if why is None:
            docs.append((d["id"], d["text"]))
    return docs, manifest


def main():
    os.makedirs(OUT, exist_ok=True)
    L, mL = lincoln_pool()
    H, mH = hay_pool()
    suffix = "_debates" if KEEP_DEBATES else ""
    with open(os.path.join(OUT, "pools%s.json" % suffix), "w", encoding="utf-8") as f:
        json.dump({"lincoln_pre1860": L, "hay_all": H}, f, ensure_ascii=False)
    with open(os.path.join(OUT, "pools_manifest%s.csv" % suffix), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pool", "id", "source", "date", "words", "status", "heading"])
        w.writerows(mL + mH)
    for name, docs in (("lincoln_pre1860", L), ("hay_all", H)):
        n = sum(ngt.word_count(t) for _, t in docs)
        print("%s: %d texts, %d words" % (name, len(docs), n))


if __name__ == "__main__":
    main()
