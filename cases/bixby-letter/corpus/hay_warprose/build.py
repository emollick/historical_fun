import re, json, sys, os
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hay_warprose.jsonl')

def wc(s): return len(s.split())

ABBR = {'Mr','Mrs','Dr','St','Gen','Col','Capt','Lieut','M','Hon','No','vs','Jr','Sr','Messrs','Rev','Prof'}
def split_sentences(p):
    # split after . ! ? (optionally followed by closing quotes/parens) when followed by space + capital/quote
    parts, last = [], 0
    for m in re.finditer(r'[.!?][\"\'”’)\]]?\s+(?=[A-Z\"\'“‘(\[])', p):
        parts.append(p[last:m.end()].strip()); last = m.end()
    parts.append(p[last:].strip())
    parts = [x for x in parts if x]
    # re-merge splits after abbreviations
    out = []
    for s in parts:
        if out:
            prev = out[-1]
            m = re.search(r'(\w+)\.[\"\'”’)]*$', prev)
            if m and m.group(1) in ABBR:
                out[-1] = prev + ' ' + s; continue
        out.append(s)
    return out

def pack(paragraphs, lo=130, hi=250):
    units = []
    for p in paragraphs:
        ss = split_sentences(p)
        for i, s in enumerate(ss):
            units.append((s, i == len(ss)-1))
    pieces, cur, curwc = [], [], 0
    for s, endp in units:
        w = wc(s)
        if cur and curwc + w > hi:
            pieces.append(cur); cur, curwc = [], 0
        cur.append((s, endp)); curwc += w
        if endp and curwc >= lo:
            pieces.append(cur); cur, curwc = [], 0
    if cur:
        if curwc < lo and pieces and sum(wc(t) for t,_ in pieces[-1]) + curwc <= hi + 30:
            pieces[-1] = pieces[-1] + cur
        else:
            pieces.append(cur)
    texts = []
    for pc in pieces:
        buf, paras = [], []
        for s, endp in pc:
            buf.append(s)
            if endp:
                paras.append(' '.join(buf)); buf = []
        if buf: paras.append(' '.join(buf))
        texts.append('\n\n'.join(paras))
    return texts

def clean_ellsworth():
    raw = open(W + 'raw_ellsworth_gutenberg_pg11154_lines7748-8166.txt').read()
    lines = raw.split('\n')
    lines = [l for l in lines if l.strip() != 'ELLSWORTH.']
    txt = '\n'.join(lines)
    # remove footnote paragraph and its marker
    txt = re.sub(r'\[Footnote A:.*?\]\s*', '', txt, flags=re.S)
    txt = txt.replace('[A]', '')
    txt = txt.replace('_', '')            # Gutenberg italics markers
    txt = txt.replace('--', '—')     # Gutenberg em-dash convention
    paras = []
    for blk in re.split(r'\n\s*\n', txt):
        ls = [l for l in blk.split('\n') if l.strip()]
        if not ls: continue
        if all(l.startswith('  ') for l in ls):          # verse block
            paras.append(' / '.join(l.strip() for l in ls))
        else:
            paras.append(re.sub(r'\s+', ' ', ' '.join(ls)).strip())
    merged = []
    for p in paras:
        if merged and re.search(r'[\u2014;,]$', merged[-1]):   # "these lines:—" + verse + "and the rest,—" + verse
            merged[-1] = merged[-1] + ' ' + p
        else:
            merged.append(p)
    return merged

BAKER_FIXES = [
    ('passage o^|hnies', 'passage of armies'),
    ('republicwere', 'republic were'),
    ('settle^ in', 'settled in'),
    ('s;iw the triumph', 'saw the triumph'),
    ('in 1 835.', 'in 1835.'),
    ('In 1837, w hen', 'In 1837, when'),
    ('1840 to 1 844,', '1840 to 1844,'),
    ('account of.an', 'account of an'),
    ('Keniucky admirers', 'Kentucky admirers'),
    ('backwoods towrn,', 'backwoods town,'),
    ("M 'Dougal", "M'Dougal"),
    ('had be^un to', 'had begun to'),
    ('refuse ruffinnism', 'refuse ruffianism'),
    ('tin; Gulf', 'the Gulf'),
    ('he look his life', 'he took his life'),
    ('Par more crushingly', 'Far more crushingly'),
    ('Prom all the streets', 'From all the streets'),
    ('and ithe tones', 'and the tones'),
    ('sometimes you sec,', 'sometimes you see,'),
    ('Pie went to say', 'He went to say'),
    ('proper di imposition', 'proper disposition'),
    ('gayly awa}r to', 'gayly away to'),
    ("Edwards's Perry,", "Edwards's Ferry,"),
    ("Edwards's Eerry", "Edwards's Ferry"),
    ('dying lire.', 'dying fire.'),
    ("''Good friend!", '"Good friend!'),
    ('Steady there!\n\nKeep cool', 'Steady there! Keep cool'),   # page 108/109 break falls mid-paragraph
]

def clean_baker():
    raw = open(W + 'archive_harpersnew24harper_djvu.txt').read()
    raw = re.sub(r'[ \t]+', ' ', raw)
    a = raw.index('RIVERS form no less striking')
    b = raw.index('seeks to apologize."', a) + len('seeks to apologize."')
    txt = raw[a:b]
    fixes_applied = []
    lines = txt.split('\n')
    out = []
    heads = re.compile(r"^\s*(COLONEL BAKER[.,]?|HARPER'S NEW MONTHLY MAGAZINE\.?|\d{3}|Vol\. XXIV\.— No\. 139\.— II)\s*$")
    for l in lines:
        if heads.match(l):
            continue
        out.append(l)
    # paragraphs: separated by blank lines; running heads removed above leave blank runs at page breaks
    return out, fixes_applied

KEEP_HYPHEN = {('Wheel-','Horse.'), ('red-','hot'), ('half-','estranged'), ('recruiting-','officer.'), ('pro-','slavery')}

def join_baker(lines):
    """Join OCR lines into paragraphs. Paragraph break = blank line, EXCEPT blank runs at page/column
    breaks where the previous line ends mid-sentence (no terminal punctuation) or next line begins lowercase."""
    paras, buf = [], []
    i = 0
    n = len(lines)
    def flush():
        nonlocal buf
        if buf:
            paras.append(buf); buf = []
    while i < n:
        l = lines[i].strip()
        if l == '':
            # look ahead to next non-blank
            j = i
            while j < n and lines[j].strip() == '': j += 1
            if j >= n: break
            nxt = lines[j].strip()
            prev = buf[-1] if buf else ''
            if buf and (not re.search(r'[.!?]\s*[\"\'”’)]*$', prev) or nxt[:1].islower() or prev.endswith('-')):
                i = j; continue   # page/column break inside a paragraph
            flush(); i = j; continue
        buf.append(l); i += 1
    flush()
    res = []
    for p in paras:
        s = ''
        for l in p:
            if s.endswith('-'):
                lastw = s.split()[-1]
                if (lastw, l.split()[0]) in KEEP_HYPHEN or lastw in ('Wheel-','red-','half-','recruiting-','pro-'):
                    s = s + l           # true compound broken at the hyphen: keep it
                else:
                    s = s[:-1] + l      # hyphenated line break: rejoin
            elif s.endswith('—') or l.startswith('—'):
                s = s + l
            else:
                s = (s + ' ' + l) if s else l
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r'\s+([;:,.!?])', r'\1', s)   # OCR spaces before punctuation (French-style spacing in Harper's)
        res.append(s)
    return res

def fix_quotes(s):
    # Harper's OCR sets quotes off with spaces (`" word ... word "`). Within a paragraph, odd-numbered
    # straight quotes are openers (drop the space after), even-numbered are closers (drop the space before).
    out, n = [], 0
    parts = s.split('"')
    for i, part in enumerate(parts[:-1]):
        n += 1
        if n % 2 == 1:   # opener
            out.append(part.rstrip() + ' "' if part and not part.endswith((' ', '(', '\u2014')) else part)
            parts[i+1] = parts[i+1].lstrip()
        else:            # closer
            out.append(part.rstrip())
    out.append(parts[-1])
    s = '"'.join(out)
    s = re.sub(r'\s+([;:,.!?])', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()

def emit(records, f):
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    ell = clean_ellsworth()
    bak_lines, fixes = clean_baker()
    bak = join_baker(bak_lines)
    joined = '\n\n'.join(bak)
    for old, new in BAKER_FIXES:
        if old in joined:
            joined = joined.replace(old, new); fixes.append((old, new))
        else:
            print('FIX NOT FOUND:', repr(old), file=sys.stderr)
    bak = [fix_quotes(p) for p in joined.split('\n\n')]
    joined = re.sub(r'\s*\u2014\s*', '\u2014', '\n\n'.join(bak))   # closed em-dashes, as printed in Harper's
    bak = joined.split('\n\n')
    ell = [re.sub(r'\s*\u2014\s*', '\u2014', p) for p in ell]
    open(W + 'clean_ellsworth.txt', 'w').write('\n\n'.join(ell) + '\n')
    open(W + 'clean_baker.txt', 'w').write('\n\n'.join(bak) + '\n')
    records = []
    for src, title, year, paras, sid in [
        ('atlantic_1861_07', 'Ellsworth', 1861, ell, 'ellsworth'),
        ('harpers_1861_12', 'Colonel Baker', 1861, bak, 'baker')]:
        pieces = pack(paras)
        total = sum(wc(p) for p in paras)
        print(f'{title}: paragraphs={len(paras)} words={total} pieces={len(pieces)} piece_wc={[wc(p) for p in pieces]}')
        for k, t in enumerate(pieces, 1):
            records.append(dict(id=f'hay_{sid}_{k:02d}', author='hay', source=src, title=title, year=year,
                                kind='essay', period='civil_war', word_count=wc(t), text=t))
    with open(OUT, 'w') as f: emit(records, f)
    print('wrote', OUT, len(records), 'records; baker fixes applied:', len(fixes))
