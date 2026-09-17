#!/usr/bin/env python3
"""Extract Polybius (Büttner-Wobst text, Perseus canonical-greekLit TEI) chapters
for the Hannibal Alps dossier, with book.chapter.section numbering.

Input : texts/polybius_perseus_grc2.xml  (tlg0543.tlg001.perseus-grc2.xml)
Output: texts/polybius_3_greek.txt        (3.33.17-18, 3.34-35, 3.39-42, 3.44-56, 3.60-61)
        texts/polybius_34_10_greek.txt    (34.10 = Strabo 4.6.12 fragment, if present)
Pure python3, stdlib only.
"""
import re, sys, os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'texts', 'polybius_perseus_grc2.xml')
NS = {'t': 'http://www.tei-c.org/ns/1.0'}

def norm(s):
    s = re.sub(r'\s+', ' ', s or '')
    return s.strip()

tree = ET.parse(SRC)
root = tree.getroot()
body = root.find('.//t:text/t:body', NS)

def book_div(n):
    for d in body.iter('{%s}div' % NS['t']):
        if d.get('subtype') == 'book' and d.get('n') == str(n):
            return d
    return None

def chapters(bookdiv):
    out = {}
    for ch in bookdiv.findall('t:div[@subtype="chapter"]', NS):
        secs = []
        for sec in ch.findall('t:div[@subtype="section"]', NS):
            txt = norm(''.join(sec.itertext()))
            secs.append((sec.get('n'), txt))
        out[ch.get('n')] = secs
    return out

def dump(book, want, fh, header):
    bd = book_div(book)
    if bd is None:
        fh.write(f'# book {book} not found\n'); return
    chs = chapters(bd)
    fh.write(header)
    for ch, sec_filter in want:
        if str(ch) not in chs:
            fh.write(f'\n## {book}.{ch}  [NOT IN XML]\n'); continue
        fh.write(f'\n## Polybius {book}.{ch}\n')
        for n, txt in chs[str(ch)]:
            if sec_filter and int(n) not in sec_filter:
                continue
            fh.write(f'{book}.{ch}.{n}  {txt}\n')

want3 = [(33, {17, 18})] + [(c, None) for c in list(range(34, 36)) + list(range(39, 43)) + list(range(44, 57)) + list(range(60, 62))]
with open(os.path.join(ROOT, 'texts', 'polybius_3_greek.txt'), 'w', encoding='utf-8') as fh:
    dump(3, want3, fh,
         '# Polybius, Historiae book 3 (Greek). Text: Th. Büttner-Wobst, Teubner (1893-), as digitised by Perseus\n'
         '# (canonical-greekLit tlg0543.tlg001.perseus-grc2.xml, CC BY-SA 4.0). Numbering book.chapter.section.\n'
         '# Extracted by code/extract_polybius_greek.py. Chapters: 3.33.17-18 (Lacinian inscription), 3.34-35, 3.39-42, 3.44-56, 3.60-61.\n')

bd34 = book_div(34)
with open(os.path.join(ROOT, 'texts', 'polybius_34_10_greek.txt'), 'w', encoding='utf-8') as fh:
    if bd34 is None:
        fh.write('# book 34 not in XML\n')
    else:
        chs = chapters(bd34)
        fh.write('# Polybius book 34 fragments (Büttner-Wobst numbering, Perseus XML). Chapters present: ' + ', '.join(chs.keys()) + '\n')
        for ch in ('10', '11'):
            if ch in chs:
                fh.write(f'\n## Polybius 34.{ch}\n')
                for n, txt in chs[ch]:
                    fh.write(f'34.{ch}.{n}  {txt}\n')
print('done')
