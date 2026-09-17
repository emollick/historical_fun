"""Write per-text CSV tables from the saved JSON results, for checking."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ngt  # noqa: E402
from run_tests import TYPES_ALL, TYPES_LETTER, CHAR_VOTE, RES  # noqa: E402


def vote(R, pid, L, H, types):
    v = [ngt.decide(R["by_type"]["%s%d" % (lv, n)][pid]["scores"]) for lv, n in types]
    return v.count(L), v.count(H)


def export_letter_register(tag=""):
    path = os.path.join(RES, "test1_test3_letter_register%s.json" % tag)
    if not os.path.exists(path):
        return
    with open(path) as f:
        R = json.load(f)
    L, H = R["candidates"]
    keys = ["%s%d" % (lv, n) for lv, n in TYPES_ALL]
    with open(os.path.join(RES, "test1_letter_by_type%s.csv" % tag), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["type", "n_gram_types_in_letter", "overlap_lincoln", "overlap_hay", "margin_L_minus_H", "winner"])
        for k in keys:
            e = R["by_type"][k]["special:bixby"]
            sc = e["scores"]
            win = ngt.decide(sc)
            w.writerow([k, e["n_types"], "%.4f" % sc[L], "%.4f" % sc[H], "%+.4f" % (sc[L] - sc[H]),
                        {L: "Lincoln", H: "Hay", None: "tie"}[win]])
    with open(os.path.join(RES, "test3_pieces%s.csv" % tag), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["piece", "author", "label", "words", "char4-10_L", "char4-10_H", "all17_L", "all17_H", "vote_char4-10", "vote_all17"] + keys)
        for pid, t in R["tests"].items():
            l7, h7 = vote(R, pid, L, H, CHAR_VOTE)
            l17, h17 = vote(R, pid, L, H, TYPES_LETTER)
            row = [pid, t["author"], t["label"], t["words"], l7, h7, l17, h17,
                   "Lincoln" if l7 > h7 else ("Hay" if h7 > l7 else "tie"),
                   "Lincoln" if l17 > h17 else ("Hay" if h17 > l17 else "tie")]
            for k in keys:
                sc = R["by_type"][k][pid]["scores"]
                row.append("%+.4f" % (sc[L] - sc[H]))
            w.writerow(row)


def export_loo():
    d = os.path.join(RES, "loo")
    if not os.path.isdir(d):
        return
    rows = {}
    keys = []
    for lv, n in TYPES_ALL:
        p = os.path.join(d, "%s%d.json" % (lv, n))
        if not os.path.exists(p):
            continue
        keys.append("%s%d" % (lv, n))
        with open(p) as f:
            D = json.load(f)
        L, H = list(D["scores"])
        for i, pid in enumerate(D["ids"]):
            rows.setdefault(pid, {"author": D["authors"][i]})
            rows[pid][keys[-1]] = D["scores"][L][i] - D["scores"][H][i]
    with open(os.path.join(RES, "test2_loo_margins.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "author"] + ["margin_L_minus_H_" + k for k in keys])
        for pid, r in rows.items():
            w.writerow([pid, r["author"]] + ["%+.4f" % r[k] for k in keys])


def export_test4():
    for design in ("A", "B", "B2"):
        path = os.path.join(RES, "test4_design%s.json" % design)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            R = json.load(f)
        L, H = R["candidates"]
        keys = ["%s%d" % (lv, n) for lv, n in TYPES_ALL]
        with open(os.path.join(RES, "test4_pieces_design%s.csv" % design), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["piece", "author", "group", "document", "label", "words", "char4-10_L", "char4-10_H", "all17_L", "all17_H", "vote_char4-10"] + keys)
            for pid, t in R["pieces"].items():
                l7, h7 = vote(R, pid, L, H, CHAR_VOTE)
                l17, h17 = vote(R, pid, L, H, TYPES_LETTER)
                row = [pid, t["author"], t["group"], t["doc"], t["label"], t["words"], l7, h7, l17, h17,
                       "Lincoln" if l7 > h7 else ("Hay" if h7 > l7 else "tie")]
                for k in keys:
                    sc = R["by_type"][k][pid]["scores"]
                    row.append("%+.4f" % (sc[L] - sc[H]))
                w.writerow(row)


if __name__ == "__main__":
    export_letter_register()
    export_letter_register("_frac095_nseq10")
    export_letter_register("_debates")
    export_loo()
    export_test4()
    print("exported")
