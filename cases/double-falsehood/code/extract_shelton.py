#!/usr/bin/env python3
"""Extract Shelton's Don Quixote (1652 ed. of the 1612/1620 translation) Part I by chapter into corpus/shelton/partI_chNN.txt
and the Cardenio chapters (23-36) into one file, normalised tokens included."""
import os, sys, re, json
from lxml import etree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize_tokens
NS = '{http://www.tei-c.org/ns/1.0}'
root = etree.parse('corpus/tcp_xml/A31538.xml').getroot()
os.makedirs('corpus/shelton', exist_ok=True)
def text_of(el):
    return re.sub(r'\s+', ' ', ' '.join(el.itertext())).replace('ſ', 's').strip()
chapters = []  # (part_index, chap_head, text)
part = 0
for el in root.iter(NS + 'div'):
    t = el.get('type')
    if t == 'part':
        part += 1
    elif t == 'chapter':
        h = el.find(NS + 'head'); head = text_of(h) if h is not None else ''
        # chapter body without nested divs' heads is fine; take all text
        chapters.append((part, head, text_of(el)))
print('parts', part, 'chapters', len(chapters))
# Shelton's 1612 Part I is divided into four "parts" (books) with chapters restarting; the 1652 edition keeps that.
# Cumulative chapter numbering: Book1 ch1-8, Book2 ch9-14, Book3 ch15-27, Book4 ch28-52.
cum = 0; out = []
for p, head, txt in chapters:
    if p >= 5: break   # Part II of the novel starts at part index 5
    cum += 1
    out.append((cum, p, head, txt))
    with open(f'corpus/shelton/partI_ch{cum:02d}.txt', 'w') as fh: fh.write(txt)
card = ' '.join(txt for cum, p, head, txt in out if 23 <= cum <= 36)
with open('corpus/shelton/cardenio_ch23_36.txt', 'w') as fh: fh.write(card)
toks = normalize_tokens(card)
json.dump({'n_words': len(toks), 'tokens': toks}, open('corpus/shelton/cardenio_ch23_36.json', 'w'))
print('Part I chapters:', cum, '; Cardenio chapters 23-36 words:', len(toks))
for cum_, p, head, txt in out[21:37]:
    print(cum_, p, head[:12], txt[:110])
