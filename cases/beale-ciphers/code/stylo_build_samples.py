#!/usr/bin/env python3
"""Cut ~2000-word samples from the raw control texts (data/controls/raw) and write them to
data/controls/samples/<author>_<n>.txt with a manifest (data/controls/manifest.csv).

Each raw file has a small config: how to find the author's own prose (start/end markers or
percent offsets), which lines to drop (editor footnotes, running heads, page numbers), and,
for letter collections, how to isolate the letters (header-split or salutation..signature).
Samples are cut at paragraph boundaries, evenly spaced through the usable region, so that
no two samples of an author are adjacent (reduces topical clustering).  The Beale texts
themselves are copied into the same folder so every later script reads one directory."""
import os, re, csv, sys, math
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(B, 'data', 'controls', 'raw'); OUT = os.path.join(B, 'data', 'controls', 'samples')
os.makedirs(OUT, exist_ok=True)
TARGET = 2000; MAXS = 4

def clean(text, ocr=False):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    if ocr:
        text = re.sub(r'(\w)-\s*\n\s*(?=[a-z])', r'\1', text)        # join hyphenated line breaks
        text = re.sub(r'[\^*|~_\u00a5\u00ab\u00bb\u2022]', '', text)   # OCR junk characters
        text = re.sub(r'[ \t]{2,}', ' ', text)
    # Gutenberg header/footer
    m = re.search(r'\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', text)
    if m: text = text[m.end():]
    m = re.search(r'\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK', text)
    if m: text = text[:m.start()]
    return text

def paragraphs(text, ocr=False):
    paras = re.split(r'\n\s*\n', text)
    out = []
    for p in paras:
        lines = [l.strip() for l in p.split('\n')]
        if ocr:   # drop running heads / page numbers: short lines with digits or all-caps
            lines = [l for l in lines if not (len(l) < 40 and re.search(r'\d', l)) and not (len(l) < 40 and l.isupper())]
        p = ' '.join(l for l in lines if l)
        p = re.sub(r'\{[^}]{0,30}\}|\[Pg ?\d+\]|\[\d+\]', '', p)     # Thwaites/Gutenberg page + note markers
        p = re.sub(r'\s+', ' ', p).strip()
        if not p or p.startswith('['): continue             # editor's bracketed notes
        if len(p.split()) < 3: continue
        if p.count('\u2014') + p.count('--') > 6 or p[:200].count('\u2014') >= 3: continue    # chapter synopses ("A -- B -- C")
        if re.search(r"\b(gwine|dat ar|dey|dis here|nuffin|marster|massa)\b", p, flags=re.I): continue  # dialect passages
        if p.count("'") > 0.05 * len(p.split()) + 2 and re.search(r"\w'\s|\s'\w", p): continue  # elision-heavy dialect
        if re.match(r'^\d+ [A-Z]', p): continue              # numbered editorial footnote (Bassett)
        out.append(p)
    return out

def region(text, start=None, end=None, nth=1, pct=(0.0, 1.0)):
    a, b = int(len(text) * pct[0]), int(len(text) * pct[1])
    if start:
        ms = list(re.finditer(start, text))
        if len(ms) >= nth: a = ms[nth - 1].end()
        else: print('  WARNING start marker not found', start, file=sys.stderr)
    if end:
        me = re.search(end, text[a:])
        if me: b = a + me.start()
        else: print('  WARNING end marker not found', end, file=sys.stderr)
    return text[a:b]

def letters_by_header(text, header, ocr=True, stop=None):
    """Blocks that follow a header line (e.g. 'To JOHN COFFEE.') up to the next header
    (or up to a signature line matching `stop`, which cuts off an editor's commentary)."""
    parts = re.split(r'\n(?=' + header + r')', text, flags=re.M)
    blocks = []
    for p in parts[1:]:
        p = re.sub(r'^' + header + r'[^\n]*\n', '', p, flags=re.M)
        if stop:
            ms = re.search(stop, p, flags=re.M)
            if ms: p = p[:ms.start()]
        ps = paragraphs(p, ocr)
        w = sum(len(x.split()) for x in ps)
        if w >= 120: blocks.extend(ps + ['¶'])
    return blocks

def letters_by_salutation(text, salutation, signature, ocr=False):
    blocks = []
    for m in re.finditer(salutation + r'(.*?)' + signature, text, flags=re.S):
        body = m.group(1)
        if len(body.split()) < 100 or len(body.split()) > 4000: continue
        blocks.extend(paragraphs(body, ocr) + ['¶'])
    return blocks

def quoted_paragraphs(text, minwords=25):
    """Paragraphs that open with a curly double quote (Lee's letters as quoted by his son)."""
    out = []
    for p in paragraphs(text):
        if p.startswith('\u201c') and len(p.split()) >= minwords:
            p = p.replace('\u201c', '').replace('\u201d', '')
            if not re.match(r'^(Always|Very|Truly|Most|Your|Yours|R\. E\. Lee)', p): out.append(p)
    return out

def letters_before_signature(text, signature, salutation, ocr=True, maxwords=3500):
    """For every signature line, take the text back to the nearest preceding salutation line."""
    out = []
    sal = [m.start() for m in re.finditer(salutation, text)]
    for m in re.finditer(signature, text):
        prev = [a for a in sal if a < m.start()]
        if not prev: continue
        body = text[prev[-1]:m.start()]
        if 60 <= len(body.split()) <= maxwords: out.extend(paragraphs(body, ocr) + ['\u00b6'])
    return out

def cut_samples(paras, target=TARGET, maxs=MAXS):
    paras = [p for p in paras if p != '¶']
    total = sum(len(p.split()) for p in paras)
    if total < target: return []
    n = min(maxs, max(1, total // target))
    n = min(n, max(1, total // (target * 2)))  # keep gaps: need >= 2x target per sample
    if total < target * 1.2: n = 1
    starts = [int(i * (total - target) / max(1, n - 1)) if n > 1 else 0 for i in range(n)]
    samples = []; cum = 0; idx = 0
    bounds = []
    for p in paras: bounds.append((cum, cum + len(p.split()))); cum += len(p.split())
    for s in starts:
        i = next((k for k, (a, b) in enumerate(bounds) if b > s), None)
        if i is None: continue
        chunk = []; w = 0
        while i < len(paras) and w < target:
            chunk.append(paras[i]); w += len(paras[i].split()); i += 1
        samples.append('\n\n'.join(chunk))
    return samples

CONFIG = [
 # key, raw file, author, title, written, published, group, genre, extraction
 ('jefferson', 'gutenberg_16784.txt', 'Thomas Jefferson (Va.)', 'Letters 1816-1826 (Memoir, Correspondence and Miscellanies vol. 4, 1829)', '1816-1826', 1829, 'early', 'letters',
    dict(kind='region', start=r'Monticello, \w+ \d+, 1816\.', end=None)),
 ('randolph', 'archive_lettersofjohnran00rand.txt', 'John Randolph of Roanoke (Va.)', 'Letters to a Young Relative (1834)', '1806-1832', 1834, 'early', 'letters',
    dict(kind='region', start=r'Theodorick', end=None, ocr=True)),
 ('jackson', 'archive_correspondenceof0003jack.txt', 'Andrew Jackson (Tenn.)', 'Correspondence vol. 3 (letters 1820-1828; Bassett 1928)', '1820-1828', 1928, 'early', 'letters',
    dict(kind='header', header=r'To [A-Z][A-Za-z.]*(?: [A-Za-z.]+)* [A-Z][A-Za-z.]+\.?[ \t]*$')),
 ('jqadams', 'archive_memjohnquincy05adamrich.txt', 'John Quincy Adams (Mass.)', 'Memoirs vol. 5 (diary 1819-1821; publ. 1875)', '1819-1821', 1875, 'early', 'diary',
    dict(kind='region', ocr=True, pct=(0.03, 0.97))),
 ('ejames', 'archive_accountofexpedit02jame.txt', 'Edwin James (Long expedition)', 'Account of an Expedition from Pittsburgh to the Rocky Mountains vol. 2 (1823)', '1819-1820', 1823, 'early', 'travel narrative',
    dict(kind='region', start=r'CHAPTER\s+I\.', end=r'\n\s*APPENDIX', ocr=True)),
 ('flint', 'archive_recollectionsofl00flin_0.txt', 'Timothy Flint (Mass./Mississippi valley)', 'Recollections of the Last Ten Years (1826)', '1815-1825', 1826, 'early', 'letters',
    dict(kind='region', start=r'\nLETTER\s+(I|L)\b', end=None, ocr=True, pct=(0, 0.97))),
 ('hall', 'archive_lettersfromwestc00hall.txt', 'James Hall (Pa./Ill.)', 'Letters from the West (1828)', '1820-1826', 1828, 'early', 'letters',
    dict(kind='region', ocr=True, pct=(0.05, 0.97))),
 ('paulding', 'archive_lettersfromsouth00paul.txt', 'James Kirke Paulding (N.Y.)', 'Letters from the South, written during an excursion in the summer of 1816 (1817)', '1816', 1817, 'early', 'letters',
    dict(kind='region', ocr=True, pct=(0.03, 0.97))),
 ('pike', 'gutenberg_43774.txt', 'Zebulon M. Pike (N.J.)', 'Expeditions vol. 1 (journals 1805-1807; publ. 1810; Coues ed. 1895)', '1805-1807', 1810, 'early', 'journal',
    dict(kind='region', start=r'\n\s*CHAPTER I\.\s*\n', nth=2, end=r'APPENDIX TO PART I')),
 ('biddle', 'gutenberg_16565.txt', 'Nicholas Biddle (Pa.; Lewis & Clark narrative)', 'History of the Expedition under Lewis and Clark vol. 1 (1814; Coues ed. 1893)', '1804-1814', 1814, 'early', 'travel narrative',
    dict(kind='region', start=r'\n\s*CHAPTER I\.\s*\n', nth=1, end=None)),
 ('gregg', 'gutenberg_44205.txt', 'Josiah Gregg (Mo./Santa Fe trade)', 'Commerce of the Prairies part 2 (1844)', '1831-1843', 1844, 'early', 'travel narrative',
    dict(kind='region', pct=(0.05, 0.97))),
 ('pattie', 'gutenberg_46110.txt', 'James Ohio Pattie (Ky./Mo.; ed. Flint)', 'Personal Narrative (1831)', '1824-1830', 1831, 'early', 'travel narrative',
    dict(kind='region', start=r'\n\s*CHAPTER I\s*\n', nth=1, end=r"(?i)INLAND TRADE WITH NEW MEXICO", pct=(0.065, 0.75))),
 ('tjames', 'archive_threeyearsamongi00jame.txt', 'Thomas James (Mo.; Santa Fe 1821-22)', 'Three Years Among the Indians and Mexicans (1846)', '1846 (about 1809-1822)', 1846, 'early', 'memoir',
    dict(kind='region', start=r'CHAPTER\s+ONE', nth=1, end=r'\n\s*(INDEX|APPENDIX)', ocr=True)),
 ('irving', 'archive_touronprairies00irvi.txt', 'Washington Irving (N.Y.)', 'A Tour on the Prairies (1835)', '1832-1835', 1835, 'early', 'travel narrative',
    dict(kind='region', start=r'CHAPTER\s+I\.', nth=2, end=None, ocr=True, pct=(0, 0.98))),
 # ---- late (c. 1858-1900), Virginian / Southern
 ('bagby', 'archive_selectionsfrommi02bagbrich.txt', 'George W. Bagby (Lynchburg/Richmond, Va.)', 'Selections from the Miscellaneous Writings vol. 2 (1885)', '1860s-1883', 1885, 'late', 'sketches/essays',
    dict(kind='region', ocr=True, pct=(0.06, 0.97))),
 ('cooke', 'archive_virginiaahistor02cookgoog.txt', 'John Esten Cooke (Va.)', 'Virginia: A History of the People (1883)', '1883', 1883, 'late', 'history',
    dict(kind='region', ocr=True, pct=(0.07, 0.97))),
 ('cooke_lee', 'gutenberg_10692.txt', 'John Esten Cooke (Va.)', 'A Life of Gen. Robert E. Lee (1871)', '1871', 1871, 'late', 'biography',
    dict(kind='region', pct=(0.05, 0.95))),
 ('davis', 'gutenberg_19831.txt', 'Jefferson Davis (Miss.)', 'Rise and Fall of the Confederate Government vol. 1 (1881)', '1881', 1881, 'late', 'history/memoir',
    dict(kind='region', pct=(0.08, 0.95))),
 ('page', 'gutenberg_26725.txt', 'Thomas Nelson Page (Va.)', 'Two Little Confederates (1888)', '1888', 1888, 'late', 'fiction',
    dict(kind='region', pct=(0.03, 0.97))),
 ('cable', 'gutenberg_10234.txt', 'George W. Cable (La.)', 'Old Creole Days (1879)', '1873-1879', 1879, 'late', 'fiction',
    dict(kind='region', pct=(0.03, 0.97))),
 ('eggleston', 'gutenberg_51211.txt', 'George Cary Eggleston (Va.)', "A Rebel's Recollections (1874)", '1874', 1874, 'late', 'memoir',
    dict(kind='region', pct=(0.04, 0.97))),
 ('twain', 'gutenberg_245.txt', 'Mark Twain (Mo.)', 'Life on the Mississippi (1883)', '1874-1883', 1883, 'late', 'memoir/travel',
    dict(kind='region', pct=(0.12, 0.95))),
 ('twain_letters', 'gutenberg_3195.txt', 'Mark Twain (Mo.)', "Mark Twain's Letters vol. 3 (letters 1876-1885; Paine ed. 1917)", '1876-1885', 1917, 'late', 'letters',
    dict(kind='header', header=r'To [A-Z][A-Za-z. ]+,? (?:in|at|on) [A-Z][^\n]*[:.]\s*$',
         stop=r'^\s*(?:Yrs|Yours|Ys|Affectionately|Sincerely|Lovingly|Truly|Ever yours)[^\n]*$|^\s*(?:MARK|S\. ?L\. ?C(?:LEMENS)?|SAML?\. L\. CLEMENS|CLEMENS|S\. L\. C\.)\.?\s*$')),
 ('lee', 'gutenberg_2323.txt', 'Robert E. Lee (Va.)', 'Letters 1861-1870 quoted in Recollections and Letters (1904)', '1861-1870', 1904, 'late', 'letters',
    dict(kind='quoted')),
 ('cabell', 'archive_sketchesrecollec00cabe.txt', 'Margaret Anthony Cabell (Lynchburg, Va.)', 'Sketches and Recollections of Lynchburg (1858)', '1858', 1858, 'mid', 'local history',
    dict(kind='region', ocr=True, pct=(0.05, 0.95))),
 ('christian', 'archive_lynchburgitspeop00chri.txt', 'W. Asbury Christian (Lynchburg, Va.)', 'Lynchburg and Its People (1900)', '1900', 1900, 'late', 'local history',
    dict(kind='region', ocr=True, pct=(0.05, 0.95))),
 ('pollock', 'archive_sketchbookoflync00poll.txt', 'Edward Pollock (ed.) (Lynchburg, Va.)', 'Sketch Book of Lynchburg, Va. (1887)', '1887', 1887, 'late', 'local description',
    dict(kind='region', ocr=True, pct=(0.05, 0.95))),
 ('shsp', 'archive_southernhistoric12sout.txt', 'Southern Historical Society Papers (various Va. authors)', 'SHSP vol. 12 (1884)', '1884', 1884, 'late', 'history/memoir',
    dict(kind='region', ocr=True, pct=(0.05, 0.95))),
 ('poe_goldbug', 'gutenberg_2147.txt', 'Edgar Allan Poe (Va./Md.)', 'The Gold-Bug (1843)', '1843', 1843, 'poe', 'fiction',
    dict(kind='region', start=r'\n\s*THE GOLD-BUG\s*\n', nth=2, end=r'\n\s*FOUR BEASTS IN ONE')),
 ('poe_letters', 'archive_lifeandletterse00harrgoog.txt', 'Edgar Allan Poe (Va./Md.)', 'Letters quoted in Harrison, Life and Letters of E. A. Poe (1903)', '1829-1849', 1903, 'poe', 'letters',
    dict(kind='before_signature', salutation=r'\n\s*(?:My )?[Dd]ear\b', signature=r'(?m)^[^\n]{0,40}(?:Edgar A\. Poe|E\. A\. Poe|EDGAR A\. POE|Edgar Allan Poe|E\. A\. P\.|Poe)\.?\s*$', ocr=True)),
]

def main():
    rows = []
    urls = {}
    lp = os.path.join(RAW, 'download_log.tsv')
    if os.path.exists(lp):
        for line in open(lp).read().splitlines()[1:]:
            f, u = line.split('\t')[:2]; urls[f] = u
    for key, fname, author, title, written, published, group, genre, cfg in CONFIG:
        path = os.path.join(RAW, fname)
        if not os.path.exists(path): print('MISSING', fname, file=sys.stderr); continue
        ocr = cfg.get('ocr', False)
        text = clean(open(path, encoding='utf-8', errors='replace').read(), ocr)
        if cfg['kind'] == 'region':
            reg = region(text, cfg.get('start'), cfg.get('end'), cfg.get('nth', 1), cfg.get('pct', (0, 1)))
            paras = paragraphs(reg, ocr)
        elif cfg['kind'] == 'header':
            paras = letters_by_header(text, cfg['header'], stop=cfg.get('stop'))
        elif cfg['kind'] == 'salutation':
            paras = letters_by_salutation(text, cfg['salutation'], cfg['signature'], ocr)
        elif cfg['kind'] == 'quoted':
            paras = quoted_paragraphs(text)
        elif cfg['kind'] == 'before_signature':
            paras = letters_before_signature(text, cfg['signature'], cfg['salutation'], ocr)
        usable = sum(len(p.split()) for p in paras if p != '¶')
        samples = cut_samples(paras)
        print(f'{key:12s} usable {usable:7d} words -> {len(samples)} samples', file=sys.stderr)
        for i, s in enumerate(samples, 1):
            sf = f'{key}_{i}.txt'
            open(os.path.join(OUT, sf), 'w', encoding='utf-8').write(s + '\n')
            rows.append(dict(sample=sf, author_key=key, author=author, title=title, written=written, published=published, group=group, genre=genre, words=len(s.split()), raw_file=fname, source_url=urls.get(fname, '')))
    # the Beale texts
    P = os.path.join(B, 'data', 'primary')
    L = ''.join(open(os.path.join(P, f), encoding='utf-8').read() + '\n\n' for f in ['letter_1822-01-04.txt', 'letter_1822-01-05.txt', 'letter_1822-05-09.txt'])
    mor_full = open(os.path.join(P, 'morriss_statement.txt'), encoding='utf-8').read()
    i = mor_full.index('Such, in substance')
    morriss, tail = mor_full[:i], mor_full[i:]
    narr = open(os.path.join(P, 'narrative_anonymous_author.txt'), encoding='utf-8').read()
    narr_full = narr + '\n\n' + tail        # the 403 words after the Morriss quotation are the anonymous author's too
    b2 = open(os.path.join(P, 'b2_plaintext_as_printed.txt'), encoding='utf-8').read()
    b2 = b2.split('\n', 1)[1] if b2.startswith('the translation') else b2
    beale = [('beale_letters', L, 'Beale letters (3 letters, 1822 as printed 1885)', 'letters'),
             ('beale_letter1', open(os.path.join(P, 'letter_1822-01-04.txt'), encoding='utf-8').read(), 'Beale letter of 4 Jan 1822', 'letters'),
             ('beale_b2', b2, 'Cipher 2 plaintext as printed', 'inventory'),
             ('narrative', narr_full, 'Anonymous author narrative (1885)', 'narrative'),
             ('morriss', morriss, "Morriss's statement as quoted (1862 as printed 1885)", 'narrative')]
    # narrative split into halves for within-author comparison
    np_ = [p for p in re.split(r'\n\s*\n', narr_full) if p.strip()]
    half = len(narr_full.split()) // 2; acc = 0; first = []; second = []
    for p in np_:
        (first if acc < half else second).append(p); acc += len(p.split())
    beale += [('narrative_A', '\n\n'.join(first), 'Anonymous narrative, first half', 'narrative'), ('narrative_B', '\n\n'.join(second), 'Anonymous narrative, second half', 'narrative')]
    for key, txt, title, genre in beale:
        open(os.path.join(OUT, key + '.txt'), 'w', encoding='utf-8').write(txt.strip() + '\n')
        rows.append(dict(sample=key + '.txt', author_key=key, author='Beale Papers (1885 pamphlet)', title=title, written='?', published=1885, group='beale', genre=genre, words=len(txt.split()), raw_file='data/primary', source_url='https://en.wikisource.org/wiki/The_Beale_Papers'))
    with open(os.path.join(B, 'data', 'controls', 'manifest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('manifest rows', len(rows), file=sys.stderr)

if __name__ == '__main__': main()
