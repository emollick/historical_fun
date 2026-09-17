"""
Test 4: run this implementation's own register-matched pieces.

Design A  the paper's design: Lincoln before 18 May 1860 against all of Hay
          (../data/pools.json). A piece cut from a Hay letter or diary
          entry that is itself in the Hay pool is tested with that entry
          left out of the pool.
Design B  period-matched pools built from the Test 4 documents themselves:
          Lincoln 1861-1865 (the register-matched segments) against Hay
          1861-1865 (the two essays, the condolence, and the letters and
          diary entries). Every piece is tested with its whole parent
          document left out of its author's pool (document-level
          validation). B2 restricts the Hay side to the two essays and the
          condolence.

10 random sequences per candidate, 25 n-gram types. Output:
  ../results/test4_designA.json, test4_designB.json, test4_designB2.json,
  ../results/test4_summary.txt
"""
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ngt  # noqa: E402
from run_tests import TYPES_ALL, TYPES_LETTER, CHAR_VOTE, WORD_VOTE, load_pools, DATA, RES  # noqa: E402

NSEQ, SEED = 10, 7


def load_test4():
    with open(os.path.join(DATA, "test4_docs.json"), encoding="utf-8") as f:
        docs = json.load(f)
    with open(os.path.join(DATA, "test4_pieces.json"), encoding="utf-8") as f:
        pieces = json.load(f)
    return docs, pieces


def build_design(design):
    docs, pieces = load_test4()
    if design == "A":
        pools = load_pools()
        lname, hname = "lincoln_pre1860", "hay_all"
    else:
        L = [(d["id"], d["text"]) for d in docs if d["author"] == "lincoln"]
        if design == "B":
            H = [(d["id"], d["text"]) for d in docs if d["author"] == "hay"]
        else:
            H = [(d["id"], d["text"]) for d in docs if d["group"] in ("hay_essay", "hay_condolence")]
        pools = {"lincoln_1861_65": ngt.Pool("lincoln_1861_65", L), "hay_1861_65": ngt.Pool("hay_1861_65", H)}
        lname, hname = "lincoln_1861_65", "hay_1861_65"
    if design == "B2":
        pieces = [p for p in pieces if p["author"] == "lincoln" or p["group"] in ("hay_essay", "hay_condolence")]
    if design in ("B", "B2"):
        # the letter and the four letters Hay wrote for Lincoln's signature,
        # from the first implementation's specials.json; none of them is a pool document
        with open(os.path.join(DATA, "bixby_report_specials.json"), encoding="utf-8") as f:
            sp = json.load(f)
        for k in ("bixby", "boker_1863", "garrison_1865", "driggs_1865", "charles_butler_1864"):
            v = sp[k]
            pieces.append({"id": "special:" + k, "doc": "special:" + k, "author": v["author"] or "unknown",
                           "group": "special_" + (v["author"] or "questioned"), "label": v["label"],
                           "text": v["text"], "words": ngt.word_count(v["text"])})
    return pools, pieces, lname, hname


def _worker(args):
    design, level, n = args
    pools, pieces, lname, hname = build_design(design)
    restrict, grams = set(), {}
    for p in pieces:
        g = ngt.ngram_types(p["text"], level, n)
        grams[p["id"]] = g
        restrict |= g
    orders = {name: ngt.make_orders(len(pl.texts), NSEQ, SEED + i * 1000 + n * 10 + (0 if level == "word" else 1))
              for i, (name, pl) in enumerate(pools.items())}
    pg = {name: ngt.PoolGrams(pl, level, n, orders[name], restrict=restrict) for name, pl in pools.items()}
    out = {}
    for p in pieces:
        own = None
        for name, pl in pools.items():
            if p["doc"] in pl.index:
                own = (name, pl.index[p["doc"]])
        sc = ngt.trace_one(grams[p["id"]], pg, own)
        out[p["id"]] = {"n_types": len(grams[p["id"]]), "scores": sc, "left_out": own is not None}
    return (design, level, n, out)


def run(design, workers=3):
    t0 = time.time()
    jobs = [(design, lv, n) for lv, n in TYPES_ALL]
    with mp.Pool(workers) as pool:
        results = pool.map(_worker, jobs)
    pools, pieces, lname, hname = build_design(design)
    res = {"design": design, "nseq": NSEQ, "seed": SEED, "candidates": [lname, hname],
           "pool_words": {name: pl.total_words() for name, pl in pools.items()},
           "pool_docs": {name: len(pl.texts) for name, pl in pools.items()},
           "pieces": {p["id"]: {"author": p["author"], "group": p["group"], "doc": p["doc"], "words": p["words"], "label": p["label"]} for p in pieces},
           "by_type": {}}
    for d, level, n, out in results:
        res["by_type"]["%s%d" % (level, n)] = out
    with open(os.path.join(RES, "test4_design%s.json" % design), "w") as f:
        json.dump(res, f, indent=1)
    print("design %s done in %.0f s" % (design, time.time() - t0), flush=True)


def summary():
    lines = []
    for design in ("A", "B", "B2"):
        path = os.path.join(RES, "test4_design%s.json" % design)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            R = json.load(f)
        L, H = R["candidates"]
        lines.append("== Test 4, design %s: pools %s" % (design, ", ".join("%s %d docs / %d words" % (k, R["pool_docs"][k], R["pool_words"][k]) for k in R["pool_words"])))
        groups = sorted(set(p["group"] for p in R["pieces"].values()))
        for g in groups:
            ids = [pid for pid, p in R["pieces"].items() if p["group"] == g]
            author = R["pieces"][ids[0]]["author"]
            if g.startswith("special_"):
                for pid in ids:
                    v7 = [ngt.decide(R["by_type"]["%s%d" % (lv, n)][pid]["scores"]) for lv, n in CHAR_VOTE]
                    v17 = [ngt.decide(R["by_type"]["%s%d" % (lv, n)][pid]["scores"]) for lv, n in TYPES_LETTER]
                    lines.append("  %s (%s, %d words): char 4-10 Lincoln %d Hay %d; all 17 Lincoln %d Hay %d" % (
                        pid, R["pieces"][pid]["label"][:60], R["pieces"][pid]["words"], v7.count(L), v7.count(H), v17.count(L), v17.count(H)))
                continue
            truth = L if author == "lincoln" else H
            per_type = {}
            wrong7 = wrong17 = tie7 = 0
            wrong_docs = {}
            for pid in ids:
                v7, v17 = [], []
                for lv, n in TYPES_ALL:
                    key = "%s%d" % (lv, n)
                    w = ngt.decide(R["by_type"][key][pid]["scores"])
                    per_type.setdefault(key, []).append(w == truth)
                    if (lv, n) in CHAR_VOTE:
                        v7.append(w)
                    if (lv, n) in TYPES_LETTER:
                        v17.append(w)
                nL, nH = v7.count(L), v7.count(H)
                if nL == nH:
                    tie7 += 1
                elif (nL > nH) != (author == "lincoln"):
                    wrong7 += 1
                    wrong_docs[R["pieces"][pid]["doc"]] = wrong_docs.get(R["pieces"][pid]["doc"], 0) + 1
                n17L, n17H = v17.count(L), v17.count(H)
                if (n17L > n17H) != (author == "lincoln"):
                    wrong17 += 1
            ndocs = len(set(R["pieces"][pid]["doc"] for pid in ids))
            lines.append("  %s: %d pieces from %d documents; char 4-10 majority wrong %d (ties %d) = %.0f%%; all-17 majority wrong %d = %.0f%%" % (
                g, len(ids), ndocs, wrong7, tie7, 100.0 * wrong7 / len(ids), wrong17, 100.0 * wrong17 / len(ids)))
            lines.append("    per-type accuracy: " + ", ".join("%s %.2f" % (k, np.mean(v)) for k, v in per_type.items()))
            if wrong_docs:
                lines.append("    documents with wrong pieces (char 4-10): " + "; ".join("%s (%d)" % kv for kv in sorted(wrong_docs.items())))
        lines.append("")
    text = "\n".join(lines)
    print(text)
    with open(os.path.join(RES, "test4_summary.txt"), "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("A", "B", "B2"):
        run(cmd)
    elif cmd == "summary":
        summary()
    else:
        for d in ("A", "B", "B2"):
            run(d)
        summary()
