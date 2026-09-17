#!/usr/bin/env python3
"""Build corpus/segments.jsonl from parsed TCP JSON + manifest (+ external OCR texts if present).
Each line: {key, group, author, date, note, act, scene, head, n_words, verse_lines (raw), prose (raw paragraphs),
            tokens (normalised), raw_tokens, n_verse_lines, n_prose_words}
"""
import json, os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize_tokens, tokenize

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
man = list(csv.DictReader(open(os.path.join(ROOT, 'corpus', 'MANIFEST.tsv')), delimiter='\t'))
out = open(os.path.join(ROOT, 'corpus', 'segments.jsonl'), 'w')
stats = []
for m in man:
    fn = os.path.join(ROOT, 'corpus', 'parsed', m['id'] + '.json')
    if not os.path.exists(fn):
        print('missing parsed file', m['id']); continue
    d = json.load(open(fn))
    pi = int(m['play_index'])
    if pi >= len(d['plays']):
        print('missing play index', m['id'], pi); continue
    p = d['plays'][pi]
    tot = 0
    for seg in p['segments']:
        verse = []; prose = []
        for sp in seg['speeches']:
            verse.extend(sp['verse']); prose.extend(sp['prose'])
        text = '\n'.join(verse) + '\n' + '\n'.join(prose)
        raw = tokenize(text)
        toks = normalize_tokens(text)
        rec = {'key': m['key'], 'group': m['group'], 'author': m['author'], 'date': int(m['date']), 'note': m['note'], 'source_id': m['id'],
               'play_title': p['play_title'], 'act': seg['act'], 'scene': seg['scene'], 'head': seg['head'],
               'n_words': len(toks), 'n_verse_lines': len(verse), 'n_prose_words': sum(len(x.split()) for x in prose),
               'verse_lines': verse, 'prose': prose, 'tokens': toks, 'raw_tokens': raw}
        out.write(json.dumps(rec) + '\n'); tot += len(toks)
    stats.append((m['key'], m['group'], len(p['segments']), tot))
out.close()
with open(os.path.join(ROOT, 'corpus', 'PLAYS.tsv'), 'w') as fh:
    fh.write('key\tgroup\tn_segments\tn_words\n')
    for s in stats: fh.write('\t'.join(str(x) for x in s) + '\n')
print(len(stats), 'plays;', sum(s[3] for s in stats), 'words')
