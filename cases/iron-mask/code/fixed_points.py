#!/usr/bin/env python3
"""Test every proposed Man in the Iron Mask candidate against the seven fixed points.

Reads ../data/fixed_points.json and ../data/candidates.json and prints a markdown
table (default) or JSON.  A candidate "passes" a fixed point when no document
contradicts him at that date; "fails" when a document places him elsewhere,
free, or dead; "open" when the documents do not decide; "na" when the point does
not apply.  The statuses and notes are the analyst's readings of the documents
cited in the two JSON files; the script only tabulates them.

Usage:  python3 fixed_points.py [md|json]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

SYMBOL = {"pass": "pass", "fail": "FAIL", "open": "open", "na": "n/a"}

def main(fmt="md"):
    fps = load("fixed_points.json")
    cands = load("candidates.json")
    fp_ids = [fp["id"] for fp in fps]
    rows = []
    for c in cands:
        res = c.get("results", {})
        statuses = {k: res.get(k, {}).get("status", "open") for k in fp_ids}
        passed = [k for k in fp_ids if statuses[k] == "pass"]
        failed = [k for k in fp_ids if statuses[k] == "fail"]
        opened = [k for k in fp_ids if statuses[k] == "open"]
        first_fail = failed[0] if failed else None
        rows.append({
            "id": c["id"], "name": c["name"], "proponents": c.get("proponents", ""),
            "statuses": statuses, "passed": passed, "failed": failed, "open": opened,
            "first_fail": first_fail, "decisive": c.get("decisive", ""),
            "survives": len(failed) == 0,
        })
    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    print("| Candidate | " + " | ".join(fp_ids) + " | fails | first failure | decisive documents |")
    print("|---|" + "---|" * len(fp_ids) + "---|---|---|")
    for r in rows:
        cells = [SYMBOL[r["statuses"][k]] for k in fp_ids]
        print(f"| {r['name']} | " + " | ".join(cells) +
              f" | {len(r['failed'])} | {r['first_fail'] or '-'} | {r['decisive']} |")
    survivors = [r["name"] for r in rows if r["survives"]]
    print()
    print("Candidates with no documented failure:", "; ".join(survivors) if survivors else "none")
    print("Fixed points:")
    for fp in fps:
        print(f"  ({fp['id']}) {fp['label']}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "md")
