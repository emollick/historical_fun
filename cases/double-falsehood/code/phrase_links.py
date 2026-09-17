#!/usr/bin/env python3
"""Rare-phrase links (after Jackson's method, here run against our own corpus rather than LION/EEBO).
Index every word 3-gram and 4-gram (normalised tokens) of the corpus by author. For a target scene, a phrase is a 'link' to an author
if it occurs in that author's corpus and in no other author's corpus (target play excluded). Report links per author per 1000 words of
that author's corpus, and a chance calibration from Henry VIII / Two Noble Kinsmen scenes and adaptation scenes.
"""
import sys, os, json, argparse, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stylo import *
from collections import defaultdict, Counter

def author_of(r):
    g = r['group']
    if g in ('SH', 'FL', 'MA', 'R18', 'BE', 'BF', 'FX', 'SRC', 'THEO', 'THEOT', 'THEOV', 'CTRL'): return {'SH':'Shakespeare','FL':'Fletcher','MA':'Massinger','R18':'R18','BE':'Beaumont','BF':'Beaumont+Fletcher','FX':'Fletcher+other','SRC':'Shelton','THEO':'Theobald','THEOT':'Theobald-transl','THEOV':'Theobald-verse','CTRL':'Mestayer'}[g]
    if g == 'JAC': return r['author'].replace('?', '')
    return None   # ADAPT, COLLAB, DF, SHX not indexed as authors

def grams(toks, n):
    return [tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)]

ap = argparse.ArgumentParser()
ap.add_argument('--targets', default='df_double_falsehood,collab_henry8,collab_tnk'); ap.add_argument('--n', type=int, default=3)
ap.add_argument('--out', default='data/results/phrase_links.json'); ap.add_argument('--stop', default=''); ap.add_argument('--exclude_keys', default='')
a = ap.parse_args()
segs = load_segments()
targets = set(a.targets.split(','))
excl = set(x for x in a.exclude_keys.split(',') if x)
index = {}      # gram -> set(author) (small sets)
size = Counter()  # author -> words
play_of_gram = defaultdict(set)
for r in segs:
    au = author_of(r)
    if au is None or r['key'] in targets or r['key'] in excl: continue
    size[au] += len(r['tokens'])
    for g in set(grams(r['tokens'], a.n)):
        s = index.get(g)
        if s is None: index[g] = {au}
        else: s.add(au)
print('indexed authors:', len(size), 'grams:', len(index))
res = {}
for t in sorted(targets):
    for r in segs:
        if r['key'] != t: continue
        links = Counter(); examples = defaultdict(list)
        for g in set(grams(r['tokens'], a.n)):
            s = index.get(g)
            if s and len(s) == 1:
                au = next(iter(s)); links[au] += 1
                if len(examples[au]) < 6: examples[au].append(' '.join(g))
        rate = {au: links[au] / size[au] * 1e5 for au in size}   # links per 100k words of author corpus
        res[f"{t}|{r['act']}.{r['scene']}"] = {'n_words': r['n_words'], 'links': dict(links), 'rate': rate, 'examples': {k: v for k, v in examples.items()}}
        show = [x for x in ['Shakespeare', 'Fletcher', 'Fletcher+other', 'Beaumont+Fletcher', 'Massinger', 'Shirley', 'Middleton', 'Jonson', 'R18', 'Theobald', 'Theobald-transl', 'Shelton'] if x in size]
        print(f"{t[:14]} {r['act']}.{r['scene']:<3d} w={r['n_words']:5d} " + ' '.join(f"{k[:5]}={links[k]:2d}({rate[k]:4.1f})" for k in show))
json.dump({'sizes': dict(size), 'scenes': res}, open(a.out, 'w'), indent=1)
