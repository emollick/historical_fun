#!/usr/bin/env python3
"""Turn the saved HTML pages into numbered plain text.
 - LacusCurtius Polybius book 3 (Paton, Loeb 1922; anchors <A CLASS="chapter" NAME="49"> and <A CLASS="sec" NAME="49.6">)
   -> texts/polybius_3_english.txt  (chapters 33(17-18), 34-35, 39-42, 44-56, 60-61) plus Thayer's/Paton's footnotes
 - la.wikisource Ab Urbe Condita liber XXI (Foster's Loeb Latin text, sections in [n])
   -> texts/livy_21_latin.txt (chapters 21-39)
 - en.wikisource Roberts (1905) Book 21 -> texts/livy_21_english.txt (chapters 21-39; Roberts has no section numbers)
Usage: parse_html_texts.py <scratch dir with lacus_polyb3.html livy21_lawiki.html livy21_enwiki.html>
"""
import re, sys, os, html
SCR = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'texts')

def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('⁠', '').replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', s).strip()

# ---------- Polybius (LacusCurtius) ----------
h = open(os.path.join(SCR, 'lacus_polyb3.html'), encoding='utf-8', errors='replace').read()
body = h[h.find('<A CLASS="chapter" NAME="1">'):]
# footnotes: collect <p class="footnote"> or elements with id="note..." (Thayer uses <A NAME="..."> in a notes section)
notes = {}
for m in re.finditer(r'<A NAME="(ref\d+|n\d+)"[^>]*>.*?</A>(.*?)(?=<A NAME="(?:ref\d+|n\d+)"|</DIV>|<HR)', body, re.S):
    notes[m.group(1)] = clean(m.group(2))[:1500]
# split at chapter anchors
parts = re.split(r'<A CLASS="chapter" NAME="(\d+)">\d+</A>', body)
chap = {}
for i in range(1, len(parts), 2):
    chap[int(parts[i])] = parts[i+1]
want = {33: {17, 18}}
for c in list(range(34, 36)) + list(range(39, 43)) + list(range(44, 57)) + list(range(60, 62)):
    want[c] = None
with open(os.path.join(OUT, 'polybius_3_english.txt'), 'w', encoding='utf-8') as fh:
    fh.write('# Polybius, Histories book 3, English: W. R. Paton, Loeb Classical Library (1922), as transcribed by Bill Thayer,\n'
             '# LacusCurtius https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Polybius/3*.html (fetched 2026-09-14).\n'
             '# Section numbers are Thayer\'s (Loeb/Büttner-Wobst numbering). Numbering: 3.chapter.section. Footnote markers kept as [n].\n'
             '# Chapters: 3.33.17-18, 3.34-35, 3.39-42, 3.44-56, 3.60-61.\n')
    for c in sorted(want):
        if c not in chap:
            fh.write(f'\n## 3.{c} [NOT FOUND]\n'); continue
        seg = chap[c]
        # cut at next chapter already done by split; remove trailing footnote block if any
        seg = re.sub(r'<A CLASS="ref"[^>]*HREF="#(ref\d+|n\d+)"[^>]*>[^<]*</A>', lambda m: f' [{m.group(1)}] ', seg)
        secs = re.split(r'<A CLASS="sec" NAME="\d+\.(\d+)">\d+</A>', seg)
        fh.write(f'\n## Polybius 3.{c}\n')
        # secs[0] is text before first sec anchor = section 1
        cur = 1
        text0 = clean(secs[0])
        if text0 and (want[c] is None or 1 in want[c]):
            fh.write(f'3.{c}.1  {text0}\n')
        for j in range(1, len(secs), 2):
            n = int(secs[j]); t = clean(secs[j+1])
            if want[c] is None or n in want[c]:
                fh.write(f'3.{c}.{n}  {t}\n')
    fh.write('\n## Footnotes (LacusCurtius: Paton\'s Loeb notes and Thayer\'s additions)\n')
    for k, v in notes.items():
        fh.write(f'[{k}] {v}\n')

# ---------- Livy Latin (la.wikisource, Foster's text) ----------
h = open(os.path.join(SCR, 'livy21_lawiki.html'), encoding='utf-8', errors='replace').read()
roman = {'XXI':21,'XXII':22,'XXIII':23,'XXIV':24,'XXV':25,'XXVI':26,'XXVII':27,'XXVIII':28,'XXIX':29,'XXX':30,'XXXI':31,'XXXII':32,'XXXIII':33,'XXXIV':34,'XXXV':35,'XXXVI':36,'XXXVII':37,'XXXVIII':38,'XXXIX':39,'XL':40}
parts = re.split(r'<h2 id="([IVXL]+)\.">[IVXL]+\.</h2>', h)
with open(os.path.join(OUT, 'livy_21_latin.txt'), 'w', encoding='utf-8') as fh:
    fh.write('# Livy, Ab Urbe Condita 21.21-39, Latin. Source: la.wikisource.org/wiki/Ab_Urbe_Condita/liber_XXI (fetched 2026-09-14),\n'
             '# whose header states "editio: Benjamin Oliver Foster, Ph.D., 1926; fons: Perseus" (i.e. the Loeb text, Foster 1929 vol. V).\n'
             '# Section numbers [n] are those of the source. Numbering 21.chapter.section.\n')
    for i in range(1, len(parts), 2):
        cnum = roman.get(parts[i])
        if cnum is None or not (21 <= cnum <= 39): continue
        seg = parts[i+1]
        seg = seg.split('<div class="mw-heading')[0]
        txt = clean(seg)
        fh.write(f'\n## Livy 21.{cnum}\n')
        secs = re.split(r'\[(\d+)\]\s*', txt)
        if secs[0].strip(): fh.write(f'21.{cnum}.?  {secs[0].strip()}\n')
        for j in range(1, len(secs), 2):
            fh.write(f'21.{cnum}.{secs[j]}  {secs[j+1].strip()}\n')

# ---------- Livy English (en.wikisource, Roberts 1905) ----------
h = open(os.path.join(SCR, 'livy21_enwiki.html'), encoding='utf-8', errors='replace').read()
with open(os.path.join(OUT, 'livy_21_english.txt'), 'w', encoding='utf-8') as fh:
    fh.write('# Livy 21.21-39, English: Rev. Canon W. M. Roberts (Everyman, 1905), from en.wikisource.org/wiki/From_the_Founding_of_the_City/Book_21\n'
             '# (fetched 2026-09-14). Roberts gives chapters only; section numbers are not marked in this translation.\n')
    # chapters marked as <span class="mw-headline" id="21">21</span> or headings like <h3>21</h3>; be liberal
    ms = list(re.finditer(r'<(h[2-4])[^>]*>(?:<span[^>]*>)*\s*(\d{1,2})\s*(?:</span>)*\s*</\1>', h))
    if not ms:
        ms = list(re.finditer(r'id="(\d{1,2})"', h))
    for k, m in enumerate(ms):
        cnum = int(m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1))
        if not (21 <= cnum <= 39): continue
        end = ms[k+1].start() if k+1 < len(ms) else len(h)
        seg = h[m.end():end]
        txt = clean(seg)
        fh.write(f'\n## Livy 21.{cnum}\n{txt}\n')
print('ok')
