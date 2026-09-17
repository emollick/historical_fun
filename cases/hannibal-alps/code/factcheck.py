#!/usr/bin/env python3
"""Compare the facts of two HTML fragments: numbers, capitalised names, Greek text, quoted strings, hrefs and ids.
Usage: python3 factcheck.py OLD NEW   -> prints what disappeared and what appeared. Exit 0 always."""
import re, sys, html
from collections import Counter
def text(p):
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<style.*?</style>|<script.*?</script>", " ", s, flags=re.S)
    return s
def strip(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)
def facts(p):
    raw = text(p); t = strip(raw)
    nums = Counter(re.findall(r"(?<![\w.])[+-]?\d[\d,]*(?:\.\d+)?(?:\s?[×x]\s?10[⁻\-]?\d+)?(?![\w])", t))
    names = Counter(w for w in re.findall(r"\b[A-ZÀ-Ý][\w'’\-]{2,}\b", t) if w not in STOP)
    greek = Counter(re.findall(r"[Ͱ-Ͽἀ-῿][Ͱ-Ͽἀ-῿\s,.;·]+", t))
    quotes = Counter(re.findall(r"[\"“]([^\"”]{6,})[\"”]", t))
    hrefs = Counter(re.findall(r'href="([^"]+)"', raw)); ids = Counter(re.findall(r'\bid="([^"]+)"', raw))
    ph = Counter(re.findall(r"\{\{[A-Z_]+\}\}", raw))
    return dict(numbers=nums, names=names, greek=greek, quotes=quotes, hrefs=hrefs, ids=ids, placeholders=ph)
STOP = set("The This That These Those There Then They Their Them What When Where Which Who Why How And But For Nor Yet So If In On At By To Of As Or An It Its His Her He She We You Our Your One Two Three Four Five Six Seven Eight Nine Ten Both Each Every No Not Nothing None All Any Some Such Same Other Another Here Where Only Even Also Still Just More Most Less Least Much Many Few Very Well Between Above Below Before After Since Until While Because Although Though Whether Either Neither Without Within Against Across Along Around Through Over Under Into Onto From With About Per Cent Its Itself Nobody Anybody".split())
def main(a, b):
    A, B = facts(a), facts(b)
    for k in A:
        gone = A[k] - B[k]; new = B[k] - A[k]
        if k in ("numbers","names","greek","quotes","hrefs","ids","placeholders"):
            if gone: print(f"[{k}] MISSING in new ({sum(gone.values())}):", ", ".join(f"{x}×{n}" if n>1 else x for x,n in sorted(gone.items())))
            if new:  print(f"[{k}] ADDED in new ({sum(new.values())}):", ", ".join(f"{x}×{n}" if n>1 else x for x,n in sorted(new.items())))
    wa = len(strip(text(a)).split()); wb = len(strip(text(b)).split())
    print(f"words: {wa} -> {wb} ({(wb-wa)*100//max(wa,1):+d}%)")
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
