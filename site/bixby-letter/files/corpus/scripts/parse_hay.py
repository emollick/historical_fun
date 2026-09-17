#!/usr/bin/env python3
"""Build the John Hay corpus (hay.jsonl + hay_index.csv).

Sources (see README.md):
  letters_1908   Letters of John Hay and Extracts from Diary (3 vols, 1908) - archive.org OCR
  poet_in_exile  A Poet in Exile: early letters of John Hay (1910) - archive.org OCR (italic OCR is noisy)
  castilian_days Castilian Days (PG #7470, essays 1871)
  bread_winners  The Bread-Winners (PG #16321, novel 1883) - fiction
  addresses      Addresses of John Hay (1906) - archive.org OCR (speeches with year)
  mckinley       William McKinley memorial address (1902) - archive.org OCR
  washington_after_war  Washington after the War (Harper's 1915, diary extracts 1867 ed. Thayer) - OCR
  pike_county / poems   verse (PG #6062, #10518) - kind=verse, kept separate
  thayer         Thayer, Life and Letters of John Hay (1915) - quoted letters only, heuristic delimitation
"""
import re, json, csv, os, sys, collections, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('S', os.path.join(HERE, '..'))   # holds ia/txt/, the archive.org OCR downloads (not included in this folder)
IA = os.path.join(ROOT, 'ia', 'txt')
OUT = os.path.join(HERE, '..')                          # the corpus folder
HAYRAW = os.path.join(OUT, 'hay_raw')

MONTH_MAP = {'jan': 1, 'january': 1, 'jany': 1, 'feb': 2, 'february': 2, 'feby': 2, 'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
             'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7, 'aug': 8, 'august': 8, 'sep': 9, 'sept': 9, 'september': 9,
             'oct': 10, 'october': 10, 'nov': 11, 'november': 11, 'dec': 12, 'december': 12, 'decr': 12, 'mat': 5}
MONTH_ALT = r'(?:Jan(?:uary|y)?|Feb(?:ruary|y)?|Mar(?:ch)?|Apr(?:il)?|May|Mat|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember|r)?)'
DIG = r'[0-9iIlOoQS!\|\\\^/\*\?]'
WEEKDAY = r'(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)'
DIARY_ENTRY_RE = re.compile(r'^\s*(?:' + WEEKDAY + r',?\s+)?(' + MONTH_ALT + r')\.?\s*,?\s+(' + DIG + r'{1,2})(?!' + DIG + r')(?:st|nd|rd|th)?\s*[.,]?\s*(?:\(?\s*(1[89]' + DIG + r'{2})\s*\)?)?\s*[.,]?\s*(?:—|-|\.)?\s*(.*)$')
MONTH_YEAR_ENTRY_RE = re.compile(r'^\s*(' + MONTH_ALT + r')\.?,?\s+(1[89]' + DIG + r'{2})\s*[.,]?\s*(.*)$')
RUNNING_HEAD_RE = re.compile(r'^\s*\d{0,3}\s*L\s*E\s*T\s*T\s*E\s*[RE]\s*S\s+O\s*F\s+J\s*O\s*H\s*N\s+H\s*A\s*[YT]\s*\d{0,3}\s*$', re.I)
PAGE_NUM_RE = re.compile(r'^\s*\d{1,3}\s*$')
LETTER_HEAD_RE = re.compile(r'^\s*(?:JOHN\s+HAY\s+|HAY\s+)?TO\s+([A-Z][A-Z .,\'\-]*?)\s*[.,]?\s*$')
COPY_HEAD_RE = re.compile(r'^\s*COPY\s+OF\s+LETTER\s+TO\s+(.+?)\s*[.,]?\s*$')
DIARY_HEAD_RE = re.compile(r'^\s*D\s*I\s*A\s*R\s*Y\s*[.,]?\s*$')
SALUTATION_RE = re.compile(r'^\s*(?:MY\s+)?(?:DEAR|DEAREST|MADEMOISELLE|MON\s+CHER|MA\s+CHERE|CHER|MESDEMOISELLES|MESSIEURS|SIR|GENTLEMEN|MADAM)\b[^a-z]*$')
SIGNATURE_RE = re.compile(r'^\s*(?:J\.?\s*(?:G\.?\s*)?H\.?|JOHN\s+HAY|JEAN\s+HAY|JNO\.?\s+HAY|J\.?\s+HAY|HAY|J\.\s*H\.\s*)[.,]?\s*$')
CLOSING_LINE_RE = re.compile(r'^\s*(?:Yours|Your|Ever|Always|Faithfully|Sincerely|Affectionately|Truly|Cordially|Very|Most|Believe|With|Au revoir|Adieu|Good-?bye)\b.{0,60}[,.]\s*$')
FOOTNOTE_RE = re.compile(r'^\s*[1-9]\s+\S')
EDITOR_ATTR_RE = re.compile(r'^\s*[—\-]\s*M\.\s*R\.\s*H\.?\s*$')


def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def digitize(tok):
    m = {'i': '1', 'I': '1', 'l': '1', '|': '1', '!': '1', 'o': '0', 'O': '0', 'Q': '9', 'S': '5', '\\': '1', '/': '7', '*': '1', '^': '', '?': ''}
    return ''.join(m.get(c, c) for c in tok)


def parse_date(s):
    """Return (y, m, d) from a dateline string; missing parts are None."""
    s = s.replace('—', '-')
    y = m = d = None
    mm = re.search(r'\b(' + MONTH_ALT + r')\.?\s*,?\s*(' + DIG + r'{1,2})?(?:st|nd|rd|th)?\.?,?\s*(?:\(?\s*(1[89]' + DIG + r'{2})\s*\)?)?', s)
    if mm:
        m = MONTH_MAP.get(mm.group(1).lower().rstrip('.'))
        if mm.group(2):
            dg = digitize(mm.group(2))
            if dg.isdigit() and 1 <= int(dg) <= 31:
                d = int(dg)
        if mm.group(3):
            dg = digitize(mm.group(3))
            if dg.isdigit():
                y = int(dg)
    if y is None:
        my = re.search(r'\(?\b(1[89]' + DIG + r'{2})\b\)?', s)
        if my:
            dg = digitize(my.group(1))
            if dg.isdigit() and 1800 <= int(dg) <= 1910:
                y = int(dg)
    if y is not None and not (1830 <= y <= 1910):
        y = None
    return y, m, d


def period_of(year):
    if year is None:
        return None
    if year < 1861:
        return 'pre_war'
    if year <= 1865:
        return 'civil_war'
    return 'post_war'


def clean_text(t, elision_placeholder='N'):
    """Normalise OCR text of the 1908 edition: rejoin hyphens, replace dashed-out names, drop ellipses."""
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    # editorial ellipses "...." / ". . . ." (elisions) -> marker removed
    n_ellipsis = len(re.findall(r'(?:\.\s*){3,}', t))
    t = re.sub(r'(?:\.\s*){3,}', ' ', t)
    # dashed-out names: capital letter(s) followed by a run of spaces or dashes, e.g. "J.  L     marshalled", "S- 's", "Major  H ,"
    n_elide = 0

    def repl(m):
        nonlocal n_elide
        n_elide += 1
        return m.group(1) + elision_placeholder + m.group(2)
    t, k = re.subn(r'(^|\s)(?:Mc|Mac)?[A-HJ-Z][a-z]{0,2}\s*[-—]{1,4}(\s*(?:\'s|,|\.|;|:|\)|\s))', repl, t)
    t, k2 = re.subn(r'(^|\s)(?:Mc|Mac)?[A-HJ-Z][a-z]{0,2}(?=\s{3,})(\s)', repl, t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip(), n_elide + k + k2, n_ellipsis


def rejoin(lines):
    """Join OCR lines into paragraphs (blank line = paragraph); de-hyphenate line breaks."""
    paras, cur = [], []
    for l in lines:
        s = norm_ws(l)
        if not s:
            if cur:
                paras.append(cur)
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        txt = ''
        for s in p:
            if txt.endswith('-') and re.match(r'^[a-z]', s):
                stem = txt[:-1]
                last = re.search(r'(\w+)$', stem)
                if last and last.group(1).lower() in ('re', 'co', 'pre', 'self', 'well', 'ex', 'non', 'anti', 'semi', 'half', 'pro', 'un', 'sub', 'so', 'to', 'by', 'in', 'brother', 'sister', 'father', 'mother', 'son', 'grand', 'step', 'great', 'ill', 'all', 'to-day', 'to'):
                    txt = txt + s
                else:
                    txt = stem + s
            else:
                txt = (txt + ' ' + s) if txt else s
        out.append(txt)
    return '\n'.join(out)


# ----------------------------------------------------------------------------
# 1. Letters of John Hay (1908)
def parse_letters_1908(vol, ident, start_line, end_line=None, seed_year=None):
    raw = open(os.path.join(IA, ident + '.txt'), encoding='utf-8', errors='replace').read().split('\n')
    lines = raw[start_line - 1:(end_line if end_line else len(raw))]
    # remove running heads / page numbers / editor footnotes
    keep = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if RUNNING_HEAD_RE.match(l) or PAGE_NUM_RE.match(l) or EDITOR_ATTR_RE.match(l):
            i += 1
            continue
        if FOOTNOTE_RE.match(l) and (i == 0 or lines[i - 1].strip() == '') and not DIARY_ENTRY_RE.match(l):
            # footnote block: this line and continuation lines until a blank line
            j = i
            while j < len(lines) and lines[j].strip() != '':
                j += 1
            i = j
            continue
        keep.append((start_line + i, l))
        i += 1
    # segment: headings
    blocks = []   # (kind, heading, recipient, start_idx)
    for k, (ln, l) in enumerate(keep):
        s = norm_ws(l)
        if DIARY_HEAD_RE.match(s):
            blocks.append(('diary', s, None, k))
        elif LETTER_HEAD_RE.match(s) and len(s) <= 60:
            blocks.append(('letter', s, LETTER_HEAD_RE.match(s).group(1), k))
        elif COPY_HEAD_RE.match(s) and len(s) <= 60:
            blocks.append(('letter', s, COPY_HEAD_RE.match(s).group(1), k))
    items = []
    year = seed_year
    month = None
    for bi, (kind, heading, recipient, k) in enumerate(blocks):
        end = blocks[bi + 1][3] if bi + 1 < len(blocks) else len(keep)
        body = keep[k + 1:end]
        page_line = keep[k][0]
        if kind == 'letter':
            # header: dateline(s) + salutation
            hdr, rest, idx = [], [norm_ws(l) for (_, l) in body], 0
            while rest and idx < 8 and (rest[0] == '' or is_letter_header(rest[0], idx)):
                if rest[0]:
                    hdr.append(rest[0])
                    idx += 1
                rest.pop(0)
            y, m, d = None, None, None
            for h in hdr:
                yy, mm, dd = parse_date(h)
                if mm and m is None:
                    m = mm
                    d = dd
                if yy and y is None:
                    y = yy
            if y is None:
                # year carried forward (volumes are chronological); month rollover -> next year
                if year is not None and m is not None and month is not None and m < month - 6:
                    year += 1
                y = year
                date_source = 'carried'
            else:
                date_source = 'dateline'
            if y:
                year = y
            if m:
                month = m
            # drop signature/closing lines anywhere; keep postscripts
            text_lines = []
            for s in rest:
                if SIGNATURE_RE.match(s) or re.match(r'^\s*(?:JNO\.?\s+G\.?\s+NICOLA\s*Y|JOHN\s+G\.\s+NICOLAY)[.,]?\s*$', s):
                    continue
                text_lines.append(s)
            text = rejoin(text_lines)
            text, removed = strip_embedded_lincoln(text)
            text, n_elide, n_ell = clean_text(text)
            items.append(dict(source='letters_1908', volume=vol, line=page_line, kind='letter', heading=heading,
                              recipient=norm_recipient(recipient), year=y, month=m, day=d, date_source=date_source,
                              header=' | '.join(hdr), text=text, word_count=len(text.split()),
                              elisions=n_elide, ellipses=n_ell, flags=(['embedded_lincoln_removed'] if removed else [])))
        else:
            # diary section: split into entries at date lines
            entries = []
            cur = None
            for (ln, l) in body:
                s = norm_ws(l)
                me = DIARY_ENTRY_RE.match(s) if s else None
                my = MONTH_YEAR_ENTRY_RE.match(s) if s else None
                if me and MONTH_MAP.get(me.group(1).lower().rstrip('.')):
                    if cur:
                        entries.append(cur)
                    mm = MONTH_MAP[me.group(1).lower().rstrip('.')]
                    dg = digitize(me.group(2))
                    dd = int(dg) if dg.isdigit() and 1 <= int(dg) <= 31 else None
                    yy = None
                    if me.group(3):
                        dg = digitize(me.group(3))
                        if dg.isdigit():
                            yy = int(dg)
                    cur = dict(m=mm, d=dd, y=yy, lines=[me.group(4)] if me.group(4) else [], line=ln, dateline=s[:40])
                elif my and MONTH_MAP.get(my.group(1).lower().rstrip('.')):
                    if cur:
                        entries.append(cur)
                    dg = digitize(my.group(2))
                    cur = dict(m=MONTH_MAP[my.group(1).lower().rstrip('.')], d=None, y=int(dg) if dg.isdigit() else None,
                               lines=[my.group(3)] if my.group(3) else [], line=ln, dateline=s[:40])
                else:
                    if cur is None:
                        cur = dict(m=None, d=None, y=None, lines=[], line=ln, dateline='')
                    cur['lines'].append(l)
            if cur:
                entries.append(cur)
            for e in entries:
                y = e['y']
                if y is None:
                    if year is not None and e['m'] is not None and month is not None and e['m'] < month - 6:
                        year += 1
                    y = year
                    date_source = 'carried'
                else:
                    date_source = 'dateline'
                if y:
                    year = y
                if e['m']:
                    month = e['m']
                text = rejoin(e['lines'])
                text, removed = strip_embedded_lincoln(text)
                text, n_elide, n_ell = clean_text(text)
                if not text.strip():
                    continue
                items.append(dict(source='letters_1908', volume=vol, line=e['line'], kind='diary', heading='DIARY',
                                  recipient=None, year=y, month=e['m'], day=e['d'], date_source=date_source,
                                  header=e['dateline'], text=text, word_count=len(text.split()),
                                  elisions=n_elide, ellipses=n_ell, flags=(['embedded_lincoln_removed'] if removed else [])))
    return items


def is_letter_header(s, idx):
    if SALUTATION_RE.match(s):
        return True
    if s.upper() == s and len(s.split()) <= 8 and re.search(r'[A-Z]{3}', s):
        return True   # caps salutation or caps dateline
    words = s.split()
    if len(words) > 10:
        return False
    y, m, d = parse_date(s)
    if (y or m) and len(words) <= 9:
        return True
    if re.search(r'\b(This|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Midnight|afternoon|morning|evening|o\'clock|noon|night)\b', s) and len(words) <= 5:
        return True
    toks = [re.sub(r'[^A-Za-z]', '', w) for w in words]
    if len(words) <= 5 and idx <= 3 and all(t == '' or t[0].isupper() for t in toks) and not re.search(r'\b(I|You|He|She|It|We|They|Is|Are|Was|The|A|An|My|Your)\b', s) and not re.search(r'[!?]', s):
        return True   # "Springfield, Ill.," / "(Washington)" / "Hilton Head, S. C," / "Warsaw, Illinois."
    return False


def norm_recipient(r):
    if not r:
        return None
    s = norm_ws(r).strip(' .,')
    s = re.sub(r'\s*[-—]+\s*$', '—', s)
    fixes = {'NTCOLAY': 'NICOLAY', 'NICOLA Y': 'NICOLAY', 'EEID': 'REID', 'EGBERT': 'ROBERT', 'MAEY': 'MARY', 'H ALPINE': 'HALPINE'}
    for a, b in fixes.items():
        s = s.replace(a, b)
    if re.match(r'^C\s*S\s*H\b', s):
        return 'Clara Stone Hay (wife)'
    words = s.split()
    out = []
    for w in words:
        if re.match(r'^[A-Z]\.?$', w) or re.match(r'^[A-Z][—-]$', w) or w.upper() in ('II', 'III'):
            out.append(w)
        else:
            out.append(w.capitalize())
    return ' '.join(out)


def strip_embedded_lincoln(text):
    """Remove quoted Lincoln documents (Executive Mansion ... A. LINCOLN) embedded in Hay's diary."""
    n = 0
    pat = re.compile(r'Executive Mansion,?[^\n]{0,80}?\n?.{0,1500}?A\.\s*LINCOLN[.,]?', re.S)
    text, n = pat.subn(' ', text)
    return text, n


# ----------------------------------------------------------------------------
# 2. A Poet in Exile (1910) - letters to Nora Perry, italic OCR
def parse_poet_in_exile():
    raw = open(os.path.join(IA, 'poetinexileearly00hayj.txt'), encoding='utf-8', errors='replace').read().split('\n')
    items = []
    # letters start at datelines like "October \2^ 1858." / "Warsaw, January 2nd, 1859." and end at "John Hay." signature (plus postscript)
    dl = re.compile(r'^\s*(?:[A-Z][A-Za-z]*,?\s+)?(' + MONTH_ALT + r'|Mat/)\.?\s*[^\n]{0,8}?\b(1[89]' + DIG + r'{2})\s*[.,]?\s*$')
    starts = [i for i, l in enumerate(raw) if dl.match(l) and i > 440]
    for si, i in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(raw)
        seg = raw[i:end]
        y, m, d = parse_date(seg[0].replace('\\2^', '12').replace('Mat/', 'May').replace('4>', '4'))
        # cut at the editor's narrative: signature "John Hay." then optional short P.S.; then the next long block is editorial
        body = []
        sig_seen = False
        for l in seg[1:]:
            s = norm_ws(l)
            if not s:
                body.append('')
                continue
            if re.match(r'^(?:John|Jo7in|Jolin)\s+Hay\s*[.,]?$', s, re.I) or re.match(r'^J\.\s*H\.\s*$', s):
                sig_seen = True
                continue
            if sig_seen and (re.match(r'^(A few|Mr\.|The |In |This |It |Hay|John Hay|These|Those|Another|Later|Here|Meanwhile|Not|After|With)\b', s) and len(s) > 40):
                break
            if re.match(r'^\s*\[?\s*\d{1,3}\s*\]?\s*$', s) or re.match(r'^[^A-Za-z]*$', s):
                continue   # page numbers / OCR junk
            if len(re.sub(r'[A-Za-z ,.;:\'"!?()-]', '', s)) > len(s) * 0.3:
                continue   # decorative-border junk
            body.append(s)
        # salutation
        while body and (body[0] == '' or re.match(r'^(My )?[Dd]ear\b.*[:,]?\s*$', body[0]) and len(body[0]) < 40):
            body.pop(0)
        text = rejoin(body)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text.split()) < 20:
            continue
        items.append(dict(source='poet_in_exile', volume=None, line=i + 1, kind='letter', heading=norm_ws(seg[0]), recipient='Nora Perry',
                          year=y, month=m, day=d, date_source='dateline', header=norm_ws(seg[0]), text=text, word_count=len(text.split()),
                          elisions=0, ellipses=0, flags=['ocr_italic_noisy']))
    return items


# ----------------------------------------------------------------------------
# 3. Project Gutenberg books
def pg_body(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    a = t.find('*** START OF THE PROJECT GUTENBERG EBOOK')
    b = t.find('*** END OF THE PROJECT GUTENBERG EBOOK')
    t = t[t.find('\n', a) + 1:b]
    return t


def parse_castilian():
    t = pg_body(os.path.join(HAYRAW, 'pg7470.txt'))
    titles = ['MADRID AL FRESCO', 'SPANISH LIVING AND DYING', 'INFLUENCE OF TRADITION IN SPANISH LIFE', 'TAUROMACHY', 'RED-LETTER DAYS',
              'AN HOUR WITH THE PAINTERS', 'A CASTLE IN THE AIR', 'THE CITY OF THE VISIGOTHS', 'THE ESCORIAL', 'A MIRACLE PLAY',
              'THE CRADLE AND THE GRAVE OF CERVANTES']
    lines = t.split('\n')
    # chapter starts = second occurrence of each title (first is the contents list)
    pos = {}
    for i, l in enumerate(lines):
        s = l.strip()
        if s in titles:
            pos.setdefault(s, []).append(i)
    starts = sorted((p[-1], tt) for tt, p in pos.items())
    items = []
    for si, (i, tt) in enumerate(starts):
        end = starts[si + 1][0] if si + 1 < len(starts) else len(lines)
        body = '\n'.join(lines[i + 1:end])
        body = re.sub(r'\[Illustration[^\]]*\]', '', body)
        body = re.sub(r'_', '', body)
        paras = [norm_ws(p) for p in re.split(r'\n\s*\n', body) if norm_ws(p)]
        text = '\n'.join(paras)
        items.append(dict(source='castilian_days', volume=None, line=i + 1, kind='essay', heading=tt.title(), recipient=None,
                          year=1871, month=None, day=None, date_source='publication', header='', text=text,
                          word_count=len(text.split()), elisions=0, ellipses=0, flags=['pg_clean', 'pub_1871_holiday_ed_1903']))
    return items


def parse_bread_winners():
    t = pg_body(os.path.join(HAYRAW, 'pg16321.txt'))
    lines = t.split('\n')
    starts = [i for i, l in enumerate(lines) if re.match(r'^\s*[IVXL]+\.\s*$', l)]
    items = []
    for si, i in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(lines)
        # title = next non-empty line
        j = i + 1
        while j < end and not lines[j].strip():
            j += 1
        title = lines[j].strip() if j < end else ''
        body = '\n'.join(lines[j + 1:end])
        body = re.sub(r'\[Illustration[^\]]*\]', '', body)
        body = re.sub(r'_', '', body)
        paras = [norm_ws(p) for p in re.split(r'\n\s*\n', body) if norm_ws(p)]
        text = '\n'.join(paras)
        if len(text.split()) < 50:
            continue
        items.append(dict(source='bread_winners', volume=None, line=i + 1, kind='fiction', heading='%s %s' % (lines[i].strip(), title.title()),
                          recipient=None, year=1883, month=None, day=None, date_source='publication', header='', text=text,
                          word_count=len(text.split()), elisions=0, ellipses=0, flags=['pg_clean', 'fiction']))
    return items


def parse_verse(pgfile, source, year):
    t = pg_body(os.path.join(HAYRAW, pgfile))
    t = re.sub(r'_', '', t)
    # split on poem titles: an all-caps line preceded by blank lines
    lines = t.split('\n')
    starts = [i for i, l in enumerate(lines) if re.match(r'^\s*[A-Z][A-Z0-9 ,\'\.:;!?\-]{2,60}$', l) and (i == 0 or not lines[i - 1].strip())
              and not re.match(r'^\s*(CONTENTS|PIKE COUNTY BALLADS|POEMS|BY JOHN HAY|AND OTHER POEMS|WANDERLIEDER|CONTENTS\.?)\s*$', l)]
    items = []
    for si, i in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(lines)
        body = [l.rstrip() for l in lines[i + 1:end]]
        text = '\n'.join(l for l in body if l.strip())
        text = re.sub(r'\n{2,}', '\n', text)
        if len(text.split()) < 20:
            continue
        items.append(dict(source=source, volume=None, line=i + 1, kind='verse', heading=lines[i].strip().title(), recipient=None,
                          year=year, month=None, day=None, date_source='publication', header='', text=text.strip(),
                          word_count=len(text.split()), elisions=0, ellipses=0, flags=['pg_clean', 'verse']))
    return items


# ----------------------------------------------------------------------------
# 4. Addresses of John Hay (1906) - archive.org OCR
ADDRESS_TITLES = [('I', 'FRANKLIN IN FRANCE'), ('II', 'OMAR KHAYYAM'), ('III', 'SIR WALTER SCOTT'), ('IV', 'SPEECHES BEFORE THE AMERICAN SOCIETY IN LONDON'),
                  ('V', 'A PARTNERSHIP IN BENEFICENCE'), ('VI', 'SPEECH AT THE ANNUAL DINNER OF THE ROYAL SOCIETY'),
                  ('VII', 'SPEECH AT THE ANNUAL DINNER OF THE LITERARY FUND'), ('VIII', 'SPEECH AT THE OPENING OF THE ROBERT BROWNING GARDEN'),
                  ('IX', 'INTERNATIONAL COPYRIGHT'), ('X', 'AMERICAN DIPLOMACY'), ('XI', 'A FESTIVAL OF PEACE'), ('XII', 'WILLIAM MCKINLEY'),
                  ('XIII', 'AT THE UNIVERSITIES'), ('XIV', 'COMMERCIAL CLUB DINNER'), ('XV', 'NEW ORLEANS'), ('XVI', 'THE GRAND ARMY OF THE REPUBLIC'),
                  ('XVII', 'PRESIDENT ROOSEVELT'), ('XVIII', 'EDMUND CLARENCE STEDMAN'), ('XIX', "LINCOLN'S FAITH"), ('XX', 'THE PRESS AND MODERN PROGRESS'),
                  ('XXI', 'FIFTY YEARS OF THE REPUBLICAN PARTY'), ('XXII', "AMERICA'S LOVE OF PEACE"), ('XXIII', 'LIFE IN THE WHITE HOUSE IN THE TIME OF LINCOLN'),
                  ('XXIV', 'CLARENCE KING')]


def caps_key(s):
    return re.sub(r'[^A-Z]', '', s.upper())


def parse_addresses():
    raw = open(os.path.join(IA, 'addressesofjohnh00hayj.txt'), encoding='utf-8', errors='replace').read().split('\n')
    # find chapter starts: a caps line equal (fuzzy) to a title, located after the contents (line > 270), first occurrence
    # a chapter begins with the title, then an all-caps descriptor block (date), then the title again, then text.
    first = {}
    order = []

    def capsish(s):
        return s and len(re.findall(r'[a-z]', s)) <= 1 and len(s) >= 4

    for i, l in enumerate(raw):
        if i < 265:
            continue
        s = l.strip()
        if not capsish(s):
            continue
        # a title may be split over two consecutive caps lines
        cands = [s]
        j = i + 1
        while j < len(raw) and j <= i + 2 and not raw[j].strip():
            j += 1
        if j < len(raw) and capsish(raw[j].strip()) and j <= i + 2:
            cands.append(s + ' ' + raw[j].strip())
        matched = None
        for c in cands:
            k = caps_key(c)
            for num, tt in ADDRESS_TITLES:
                kt = caps_key(tt)
                if k == kt or (len(k) >= 8 and difflib.SequenceMatcher(None, k, kt).ratio() >= 0.9):
                    matched = (num, tt)
                    break
            if matched:
                break
        if matched and matched[1] not in first:
            first[matched[1]] = i
            order.append((i, matched[0], matched[1]))
    order.sort()
    items = []
    for oi, (i, num, tt) in enumerate(order):
        end = order[oi + 1][0] if oi + 1 < len(order) else len(raw)
        seg = raw[i + 1:end]
        # descriptor block: leading all-caps lines (no lowercase) -> year
        desc = []
        j = 0
        while j < len(seg) and j < 25:
            s = seg[j].strip()
            if not s:
                j += 1
                continue
            if not re.search(r'[a-z]', s):
                desc.append(s)
                j += 1
                continue
            break
        ym = [y for y in re.findall(r'\b(1[89]\d\d)\b', ' '.join(desc)) if 1890 <= int(y) <= 1906]
        if not ym:
            ym = [y for y in re.findall(r'\b(1[89]\d\d)\b', ' '.join(seg[:40])) if 1890 <= int(y) <= 1906]
        year = int(ym[0]) if ym else None
        body = []
        for l in seg[j:]:
            s = l.strip()
            if not s:
                body.append('')
                continue
            if PAGE_NUM_RE.match(s):
                continue
            if len(re.findall(r'[a-z]', s)) <= 1 and (difflib.SequenceMatcher(None, caps_key(s), caps_key(tt)).ratio() >= 0.8 or len(s) < 4
                                                       or any(difflib.SequenceMatcher(None, caps_key(s), caps_key(t2)).ratio() >= 0.85 for _, t2 in ADDRESS_TITLES)):
                continue   # running head (title, possibly split over two lines)
            if re.match(r'^\s*[1-9]\s+\S', l) and body and body[-1] == '':
                # footnote (rare) - skip block
                continue
            body.append(s)
        text = rejoin(body)
        text = re.sub(r'\s+', ' ', text).strip()
        flags = ['ocr']
        if tt == 'WILLIAM MCKINLEY':
            flags.append('duplicate_of_mckinley_1902_pamphlet')
        items.append(dict(source='addresses', volume=None, line=i + 1, kind='speech', heading='%s. %s' % (num, tt.title()), recipient=None,
                          year=year, month=None, day=None, date_source='descriptor' if year else None, header=' / '.join(desc)[:200],
                          text=text, word_count=len(text.split()), elisions=0, ellipses=0, flags=flags))
    return items


def parse_mckinley():
    raw = open(os.path.join(IA, 'williammckinleym02hayj.txt'), encoding='utf-8', errors='replace').read().split('\n')
    # text begins after the copyright/front matter ("COPY A.") and ends before the LC stamps
    start = next(i for i, l in enumerate(raw) if l.strip().startswith('COPY  A') or l.strip() == 'COPY A.') + 1
    end = next(i for i, l in enumerate(raw) if i > start + 100 and re.match(r'^\s*APR\.?\s+30\s+1902', l))
    body = []
    for l in raw[start:end]:
        s = l.strip()
        if not s:
            body.append('')
            continue
        if PAGE_NUM_RE.match(s) or (not re.search(r'[a-z]', s) and 'MCKINLEY' in caps_key(s)):
            continue
        body.append(s)
    text = re.sub(r'\s+', ' ', rejoin(body)).strip()
    return [dict(source='mckinley', volume=None, line=start + 1, kind='speech', heading='William McKinley: Memorial Address (Feb. 27, 1902)',
                 recipient=None, year=1902, month=2, day=27, date_source='title', header='', text=text, word_count=len(text.split()),
                 elisions=0, ellipses=0, flags=['ocr'])]


# ----------------------------------------------------------------------------
# 5. Washington after the War (Harper's, Feb. 1915): Thayer narrative + diary extracts (1867)
def parse_washington_after_war():
    raw = open(os.path.join(IA, 'washingtonafterw00hayj.txt'), encoding='utf-8', errors='replace').read().split('\n')
    start = next(i for i, l in enumerate(raw) if 'Compiled' in l and 'Thayer' in l) + 1
    lines = []
    for l in raw[start:]:
        s = l.strip()
        if not s:
            lines.append('')
            continue
        if PAGE_NUM_RE.match(s) or (not re.search(r'[a-z]', s) and len(s) > 3):
            continue   # page numbers, running heads, picture captions
        lines.append(s)
    entry_re = re.compile(r'^\s*(' + MONTH_ALT + r')\.?\s+(' + DIG + r'{1,2})(?!' + DIG + r')(?:st|nd|rd|th)?[.,]?\s*(?:\(?(1[89]' + DIG + r'{2})\)?)?[.,]?\s*(?:\u2014|-|\.)?\s*(.*)$')
    entries = []
    cur = None
    year = 1867
    para_start = True
    for l in lines:
        if not l:
            para_start = True
            if cur is not None:
                cur['lines'].append('')
            continue
        m = entry_re.match(l)
        if m and MONTH_MAP.get(m.group(1).lower().rstrip('.')):
            if cur:
                entries.append(cur)
            dg = digitize(m.group(2))
            yy = int(digitize(m.group(3))) if m.group(3) and digitize(m.group(3)).isdigit() else None
            if yy:
                year = yy
            cur = dict(m=MONTH_MAP[m.group(1).lower().rstrip('.')], d=int(dg) if dg.isdigit() else None, y=year, lines=[m.group(4)] if m.group(4) else [], head=l[:40])
            para_start = False
            continue
        if cur is not None:
            # Thayer's narrative resumes: a paragraph opening with a third-person reference to Hay / the Diary
            if para_start and re.search(r"\bHay\b(?!'s)|\bthe Diary\b|\bThayer\b", l) and not re.search(r'\bI\b', l[:80]):
                entries.append(cur)
                cur = None
                para_start = False
                continue
            cur['lines'].append(l)
        para_start = False
    if cur:
        entries.append(cur)
    out = []
    for e in entries:
        text = rejoin(e['lines'])
        text, n_elide, n_ell = clean_text(text)
        if len(text.split()) < 15:
            continue
        out.append(dict(source='washington_after_war', volume=None, line=None, kind='diary', heading="DIARY (Harper's 1915 extract)", recipient=None,
                        year=e['y'], month=e['m'], day=e['d'], date_source='dateline', header=e['head'], text=text, word_count=len(text.split()),
                        elisions=n_elide, ellipses=n_ell, flags=['ocr', 'delimitation_heuristic', 'edited_by_thayer']))
    return out


# ----------------------------------------------------------------------------
# 6. Thayer, Life and Letters of John Hay (1915): quoted letters, heuristic delimitation
def parse_thayer(vol, ident):
    raw = open(os.path.join(IA, ident + '.txt'), encoding='utf-8', errors='replace').read().split('\n')
    lines = []
    for i, l in enumerate(raw):
        s = l.strip()
        if PAGE_NUM_RE.match(s):
            continue
        if not re.search(r'[a-z]', s) and len(s) > 3 and len(s) < 50:
            continue   # running heads (chapter title / JOHN HAY)
        if re.match(r'^\s*[\^*\'\d]\s+\S', l) and (i == 0 or raw[i - 1].strip() == ''):
            # Thayer footnote block
            lines.append(('FN', s))
            continue
        lines.append((i + 1, l))
    items = []
    head_re = re.compile(r'^\s*To\s+(?:Mrs?\.|Miss|Dr\.|Rev\.|Gen\.|Col\.|Judge|Bishop|Sir|Hon\.|Senator|President|Mademoiselle|Madame|Mme\.|Mlle\.)?\s*(?:[A-Z][\w\'.-]*\s*){1,5}$')
    dateline_re = re.compile(r'^\s*(?:[A-Z][A-Za-z. ]{1,40},\s+)?(?:' + MONTH_ALT + r')\.?\s+' + DIG + r'{1,2}(?:st|nd|rd|th)?,?\s+1[89]\d\d[.,]?\s*$')
    k = 0
    n = len(lines)
    while k < n:
        ln, l = lines[k]
        s = norm_ws(l) if ln != 'FN' else ''
        if ln != 'FN' and head_re.match(s) and len(s) <= 45:
            # dateline within the next 3 non-empty lines?
            j = k + 1
            dl = None
            seen = 0
            while j < n and seen < 3:
                if lines[j][0] == 'FN':
                    j += 1
                    continue
                t = norm_ws(lines[j][1])
                if t:
                    seen += 1
                    if dateline_re.match(t):
                        dl = j
                        break
                j += 1
            if dl is None:
                k += 1
                continue
            y, m, d = parse_date(norm_ws(lines[dl][1]))
            recipient = re.sub(r'^\s*To\s+', '', s)
            body = []
            j = dl + 1
            paras = 0
            stop_reason = 'next_heading'
            while j < n:
                lnj, lj = lines[j]
                if lnj == 'FN':
                    j += 1
                    continue
                t = norm_ws(lj)
                if head_re.match(t) and len(t) <= 45:
                    break
                if not t:
                    if body and body[-1] != '':
                        paras += 1
                    body.append('')
                    j += 1
                    if paras >= 12:
                        stop_reason = 'max_paragraphs'
                        break
                    continue
                if re.match(r'^(CHAPTER|BOOK)\b', t) or (not re.search(r'[a-z]', t) and len(t) > 3):
                    stop_reason = 'chapter'
                    break
                # narrative cue: third-person Hay at paragraph start / signature line
                if (body == [] or body[-1] == '') and re.search(r"\bHay\b(?!'s)", t) and not re.search(r"\b(Mrs|Mr|Colonel|Major|John)\.?\s+Hay\b", t):
                    stop_reason = 'third_person_hay'
                    break
                if re.match(r'^(?:J\.\s*H\.|John Hay|J\. Hay|Hay)[.,]?\s*$', t):
                    stop_reason = 'signature'
                    break
                body.append(t)
                j += 1
            text = rejoin(body)
            text, n_elide, n_ell = clean_text(text)
            if len(text.split()) >= 25:
                items.append(dict(source='thayer', volume=vol, line=ln, kind='letter', heading=s, recipient=recipient, year=y, month=m, day=d,
                                  date_source='dateline', header=norm_ws(lines[dl][1]), text=text, word_count=len(text.split()),
                                  elisions=n_elide, ellipses=n_ell, flags=['ocr', 'delimitation_heuristic', 'stop_' + stop_reason]))
            k = j
            continue
        k += 1
    return items


# ----------------------------------------------------------------------------
def main():
    items = []
    items += parse_letters_1908(1, 'lettersofjohnhay01hayj', 753, seed_year=1860)
    items += parse_letters_1908(2, 'lettersofjohnhay02hayj', 42)
    items += parse_letters_1908(3, 'lettersofjohnhay03hayj', 41)
    items += parse_poet_in_exile()
    items += parse_castilian()
    items += parse_bread_winners()
    items += parse_addresses()
    items += parse_mckinley()
    items += parse_washington_after_war()
    items += parse_verse('pg6062.txt', 'pike_county_ballads', 1871)
    items += parse_verse('pg10518.txt', 'poems', 1890)
    items += parse_thayer(1, 'lifelettersofjoh01thay')
    items += parse_thayer(2, 'lifelettersofjoh02thay')
    for n, it in enumerate(items, 1):
        it['id'] = 'hay-%04d' % n
        it['period'] = period_of(it['year'])
        y, m, d = it['year'], it['month'], it['day']
        it['date'] = ('%04d-%02d-%02d' % (y, m, d)) if (y and m and d) else (('%04d-%02d' % (y, m)) if (y and m) else (('%04d' % y) if y else None))
        it['fiction'] = it['source'] == 'bread_winners'
    with open(os.path.join(OUT, 'hay.jsonl'), 'w', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + '\n')
    with open(os.path.join(OUT, 'hay_index.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'source', 'volume', 'kind', 'date', 'year', 'period', 'recipient', 'heading', 'word_count', 'elisions', 'flags'])
        for it in items:
            w.writerow([it['id'], it['source'], it['volume'], it['kind'], it['date'], it['year'], it['period'], it['recipient'], it['heading'][:80],
                        it['word_count'], it['elisions'], ';'.join(it['flags'])])
    # report
    tab = collections.defaultdict(lambda: [0, 0])
    for it in items:
        key = (it['source'], it['kind'], it['period'])
        tab[key][0] += 1
        tab[key][1] += it['word_count']
    print('source | kind | period | items | words')
    for key in sorted(tab, key=lambda k: (k[0], k[1], str(k[2]))):
        print('  %-22s %-8s %-9s %5d %8d' % (key[0], key[1], key[2], tab[key][0], tab[key][1]))
    print('TOTAL items', len(items), 'words', sum(i['word_count'] for i in items))
    val = [i for i in items if i['source'] == 'letters_1908' and i['kind'] in ('letter', 'diary') and i['year'] and 1861 <= i['year'] <= 1866 and 100 <= i['word_count'] <= 300]
    print('validation set (1908 letters/diary, 1861-1866, 100-300 words):', len(val), '| letters', sum(1 for i in val if i['kind'] == 'letter'), 'diary', sum(1 for i in val if i['kind'] == 'diary'))
    print('date_source:', collections.Counter((i['source'], i['date_source']) for i in items if i['source'] == 'letters_1908'))
    print('year None:', sum(1 for i in items if i['year'] is None))


if __name__ == '__main__':
    main()
