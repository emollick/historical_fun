"""
Run Tests 1 to 3 of the second, independent implementation.

  python3 run_tests.py letter      Test 1 and Test 3: the Bixby letter, the
                                   register-matched pieces and the other
                                   special texts, under the paper's design
                                   (50 random sequences per candidate)
  python3 run_tests.py loo         Test 2: leave-one-out attribution of every
                                   pool text, 10 random sequences per candidate,
                                   25 n-gram types (word 1-5, character 1-20)
  python3 run_tests.py summary     Tables from the saved results

Results go to ../results/ as JSON. Seeds are fixed.
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ngt  # noqa: E402

DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
RES = os.path.normpath(os.path.join(HERE, "..", "results"))
CASE_DIR = os.path.normpath(os.path.join(HERE, "..", ".."))

TYPES_ALL = [("word", n) for n in range(1, 6)] + [("char", n) for n in range(1, 21)]
TYPES_LETTER = [("word", n) for n in range(1, 4)] + [("char", n) for n in range(3, 17)]
CHAR_VOTE = [("char", n) for n in range(4, 11)]   # the paper's 4- to 10-character majority
WORD_VOTE = [("word", n) for n in range(1, 4)]    # the paper's 1- to 3-word majority
CANDS = ["lincoln_pre1860", "hay_all"]


POOL_FILE = "pools.json"   # overridden by --pools


def load_pools(pool_file=None):
    with open(os.path.join(DATA, pool_file or POOL_FILE), encoding="utf-8") as f:
        raw = json.load(f)
    return {name: ngt.Pool(name, [tuple(x) for x in raw[name]]) for name in raw}


def load_tests():
    """The questioned texts: the letter, the register-matched pieces and the
    other special texts, taken from the data files of The Bixby Letter, the first implementation."""
    tests = []
    # copies of the first implementation's analysis/specials.json and analysis/register.json
    # (its excerpt lists), kept under ../data as bixby_report_specials.json and
    # bixby_report_register.json so that this folder runs on its own
    with open(os.path.join(DATA, "bixby_report_specials.json"), encoding="utf-8") as f:
        sp = json.load(f)
    for k, v in sp.items():
        tests.append({"id": "special:" + k, "author": v["author"], "label": v["label"],
                      "text": v["text"], "group": "special"})
    with open(os.path.join(DATA, "bixby_report_register.json"), encoding="utf-8") as f:
        reg = json.load(f)
    for k, v in reg.items():
        tests.append({"id": "register:" + k, "author": v["author"], "label": v["label"],
                      "text": v["text"], "group": "register", "parents": v.get("parents", [])})
    return tests


def _letter_worker(args):
    level, n, nseq, seed, frac = args
    pools = load_pools()
    tests = load_tests()
    restrict = set()
    grams = {}
    for t in tests:
        g = ngt.ngram_types(t["text"], level, n)
        grams[t["id"]] = g
        restrict |= g
    orders = {name: ngt.make_orders(len(p.texts), nseq, seed + i * 1000 + n * 10 + (0 if level == "word" else 1))
              for i, (name, p) in enumerate(pools.items())}
    # parents of the register pieces and copies of the special texts must not
    # sit in a pool: check by id (none of them do under this design; the
    # check is kept so that the rule is enforced, not assumed)
    pool_ids = {name: set(p.ids) for name, p in pools.items()}
    pg = {name: ngt.PoolGrams(p, level, n, orders[name], restrict=restrict) for name, p in pools.items()}
    out = {}
    for t in tests:
        own = None
        for par in t.get("parents", []):
            for name in pools:
                if par in pool_ids[name]:
                    own = (name, pools[name].index[par])
        sc = ngt.trace_one(grams[t["id"]], pg, own, frac=frac)
        out[t["id"]] = {"n_types": len(grams[t["id"]]), "scores": sc}
    return (level, n, out)


def run_letter(nseq=50, seed=1, workers=4, frac=1.0, tag=""):
    t0 = time.time()
    jobs = [(lv, n, nseq, seed, frac) for lv, n in TYPES_ALL]
    with mp.Pool(workers) as pool:
        results = pool.map(_letter_worker, jobs)
    tests = load_tests()
    pools = load_pools()
    res = {"nseq": nseq, "seed": seed, "frac": frac, "candidates": CANDS, "pool_file": POOL_FILE,
           "pool_words": {name: p.total_words() for name, p in pools.items()},
           "pool_docs": {name: len(p.texts) for name, p in pools.items()},
           "tests": {t["id"]: {"author": t["author"], "label": t["label"],
                              "words": ngt.word_count(t["text"]), "group": t["group"]} for t in tests},
           "by_type": {}}
    for level, n, out in results:
        res["by_type"]["%s%d" % (level, n)] = out
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "test1_test3_letter_register%s.json" % tag), "w") as f:
        json.dump(res, f, indent=1)
    print("letter/register run done in %.0f s" % (time.time() - t0))


def _loo_worker(args):
    level, n, nseq, seed = args
    t0 = time.time()
    pools = load_pools()
    orders = {name: ngt.make_orders(len(p.texts), nseq, seed + i * 1000 + n * 10 + (0 if level == "word" else 1))
              for i, (name, p) in enumerate(pools.items())}
    pg = {name: ngt.PoolGrams(p, level, n, orders[name]) for name, p in pools.items()}
    loo = ngt.leave_one_out(pg)
    ids, authors, ntypes = [], [], []
    for name, p in pools.items():
        ids += p.ids
        authors += [name] * len(p.ids)
        ntypes += pg[name].types_per_doc.tolist()
    out = {"ids": ids, "authors": authors, "n_types": ntypes,
           "scores": {name: loo[name].tolist() for name in pools}}
    os.makedirs(os.path.join(RES, "loo"), exist_ok=True)
    with open(os.path.join(RES, "loo", "%s%d.json" % (level, n)), "w") as f:
        json.dump(out, f)
    print("loo %s%d done in %.0f s" % (level, n, time.time() - t0), flush=True)
    return (level, n)


def run_loo(nseq=10, seed=2, workers=3, types=None):
    t0 = time.time()
    jobs = [(lv, n, nseq, seed) for lv, n in (types or TYPES_ALL)]
    # longest jobs first
    jobs.sort(key=lambda j: -(j[1] if j[0] == "char" else 0))
    with mp.Pool(workers) as pool:
        for _ in pool.imap_unordered(_loo_worker, jobs):
            pass
    print("loo done in %.0f s" % (time.time() - t0))


def summary(tag=""):
    lines = []
    # ---- Test 1 and 3
    path = os.path.join(RES, "test1_test3_letter_register%s.json" % tag)
    if os.path.exists(path):
        with open(path) as f:
            R = json.load(f)
        L, H = CANDS
        lines.append("== Test 1: the Bixby letter (paper's design; %d random sequences; sample = %.2f x smaller pool)" % (R["nseq"], R.get("frac", 1.0)))
        lines.append("type  n_types  Lincoln  Hay   margin(L-H)  winner")
        votes = {"char4-10": [], "word1-3": [], "all17": []}
        for lv, n in TYPES_ALL:
            key = "%s%d" % (lv, n)
            e = R["by_type"][key]["special:bixby"]
            sc = e["scores"]
            w = ngt.decide(sc)
            wn = {L: "Lincoln", H: "Hay", None: "tie"}[w]
            lines.append("%-6s %5d   %.4f  %.4f  %+.4f     %s" % (key, e["n_types"], sc[L], sc[H], sc[L] - sc[H], wn))
            if (lv, n) in CHAR_VOTE:
                votes["char4-10"].append(wn)
            if (lv, n) in WORD_VOTE:
                votes["word1-3"].append(wn)
            if (lv, n) in TYPES_LETTER:
                votes["all17"].append(wn)
        for k, v in votes.items():
            lines.append("  %s: Lincoln %d, Hay %d, tie %d" % (k, v.count("Lincoln"), v.count("Hay"), v.count("tie")))
        lines.append("")
        lines.append("== Test 3: register-matched pieces (paper's design), majority of char 4-10")
        for author in ["lincoln", "hay"]:
            tests = [tid for tid, t in R["tests"].items() if t["group"] == "register" and t["author"] == author]
            per_type = {}
            maj_wrong, maj_tie = 0, 0
            wrong_list = []
            w17_wrong = 0
            for tid in tests:
                v, v17 = [], []
                for lv, n in TYPES_ALL:
                    key = "%s%d" % (lv, n)
                    sc = R["by_type"][key][tid]["scores"]
                    w = ngt.decide(sc)
                    truth = L if author == "lincoln" else H
                    ok = (w == truth)
                    per_type.setdefault(key, []).append(ok)
                    if (lv, n) in CHAR_VOTE:
                        v.append(w)
                    if (lv, n) in TYPES_LETTER:
                        v17.append(w)
                nL, nH = v.count(L), v.count(H)
                if nL == nH:
                    maj_tie += 1
                elif (nL > nH) != (author == "lincoln"):
                    maj_wrong += 1
                    wrong_list.append("%s L%d/H%d" % (tid.replace("register:", ""), nL, nH))
                n17L, n17H = v17.count(L), v17.count(H)
                if (n17L > n17H) != (author == "lincoln"):
                    w17_wrong += 1
            lines.append("  %s pieces: %d; majority char 4-10 wrong: %d, ties: %d; majority of all 17 wrong: %d" % (
                author, len(tests), maj_wrong, maj_tie, w17_wrong))
            lines.append("    per-type accuracy: " + ", ".join("%s %.2f" % (k, np.mean(v)) for k, v in per_type.items()))
            if wrong_list:
                lines.append("    wrong by char 4-10: " + "; ".join(wrong_list))
        lines.append("")
        lines.append("== Special texts (paper's design), majority of char 4-10 and all 17")
        for tid, t in R["tests"].items():
            if t["group"] != "special":
                continue
            v17, v7 = [], []
            for lv, n in TYPES_LETTER:
                key = "%s%d" % (lv, n)
                w = ngt.decide(R["by_type"][key][tid]["scores"])
                v17.append(w)
                if (lv, n) in CHAR_VOTE:
                    v7.append(w)
            lines.append("  %-28s (%s, %d w): char4-10 L %d H %d; all17 L %d H %d" % (
                tid, t["author"], t["words"], v7.count(L), v7.count(H), v17.count(L), v17.count(H)))
        lines.append("")
    # ---- Test 2
    loo_dir = os.path.join(RES, "loo")
    if os.path.isdir(loo_dir):
        lines.append("== Test 2: leave-one-out attribution of every pool text (paper's design)")
        lines.append("type   Hay: rec  pre  F1 | Lincoln: rec  pre  F1 | acc  (ties counted wrong)")
        L, H = CANDS
        per_doc_votes = {}
        for lv, n in TYPES_ALL:
            p = os.path.join(loo_dir, "%s%d.json" % (lv, n))
            if not os.path.exists(p):
                continue
            with open(p) as f:
                D = json.load(f)
            sL, sH = np.array(D["scores"][L]), np.array(D["scores"][H])
            truth = np.array(D["authors"])
            pred = np.where(sL > sH, L, np.where(sH > sL, H, "tie"))
            stats = {}
            for a in (H, L):
                tp = np.sum((pred == a) & (truth == a))
                fp = np.sum((pred == a) & (truth != a))
                fn = np.sum((pred != a) & (truth == a))
                rec = tp / max(tp + fn, 1)
                pre = tp / max(tp + fp, 1)
                f1 = 2 * pre * rec / max(pre + rec, 1e-9)
                stats[a] = (rec, pre, f1)
            acc = np.mean(pred == truth)
            lines.append("%-6s      %.2f %.2f %.2f |         %.2f %.2f %.2f | %.2f" % (
                "%s%d" % (lv, n), *stats[H], *stats[L], acc))
            for i, d in enumerate(D["ids"]):
                per_doc_votes.setdefault(d, {"truth": truth[i], "char": [], "word": []})
                if (lv, n) in CHAR_VOTE:
                    per_doc_votes[d]["char"].append(pred[i])
                if (lv, n) in WORD_VOTE:
                    per_doc_votes[d]["word"].append(pred[i])
        for vk, need in (("char", 7), ("word", 3)):
            wrong = {L: 0, H: 0}
            tot = {L: 0, H: 0}
            wrong_ids = []
            for d, v in per_doc_votes.items():
                if len(v[vk]) < need:
                    continue
                t = v["truth"]
                tot[t] += 1
                nL, nH = v[vk].count(L), v[vk].count(H)
                win = L if nL > nH else (H if nH > nL else "tie")
                if win != t:
                    wrong[t] += 1
                    wrong_ids.append((d, t, nL, nH))
            lines.append("  majority %s vote: Lincoln texts %d, wrong %d; Hay texts %d, wrong %d" % (
                vk, tot[L], wrong[L], tot[H], wrong[H]))
            if wrong_ids:
                lines.append("    wrong: " + "; ".join("%s (%s, L%d/H%d)" % w for w in wrong_ids[:40]))
    text = "\n".join(lines)
    print(text)
    with open(os.path.join(RES, "summary%s.txt" % tag), "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["letter", "loo", "summary"])
    ap.add_argument("--nseq", type=int, default=None)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--frac", type=float, default=1.0, help="sample size as a fraction of the smaller pool")
    ap.add_argument("--tag", default="", help="suffix for the result file")
    ap.add_argument("--pools", default="pools.json", help="pool file under ../data (pools.json or pools_debates.json)")
    a = ap.parse_args()
    POOL_FILE = a.pools
    if a.cmd == "letter":
        run_letter(nseq=a.nseq or 50, workers=a.workers, frac=a.frac, tag=a.tag)
    elif a.cmd == "loo":
        run_loo(nseq=a.nseq or 10, workers=a.workers)
    else:
        summary(tag=a.tag)
