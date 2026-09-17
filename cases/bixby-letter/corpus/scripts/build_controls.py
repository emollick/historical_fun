#!/usr/bin/env python3
"""Build controls.jsonl: public-domain prose by educated American men writing 1850-1890, cut into pieces.

One JSON line per piece (about 150-300 words, cut at paragraph / diary-entry / letter boundaries):
  id, author, source, title, url, kind, year, year_source, period, word_count, text
Extraction modes (per CONFIG entry):
  pg_whole     Project Gutenberg text: everything between the start and end markers.
  pg_flush     Project Gutenberg text of Sumner's Works: keep only flush-left paragraphs (Sumner's speeches) and
               2-space-indented ones (his own letters); drop the 4+-space-indented editorial headnotes, quoted
               matter and epigraphs, and skip every APPENDIX section.
  pg_twain     Project Gutenberg "Mark Twain's Letters" (Paine): keep the flush-left letter blocks, drop Paine's
               indented narrative, letter headers, datelines and signatures.
  ocr_whole    archive.org OCR: everything between the markers, dropping running heads, page numbers, digit-led
               footnote blocks and chapter synopses.
  ocr_letters  archive.org OCR letter collection: text between "TO X" letter headers (optionally stopped at an
               editorial third-person cue), running heads / page numbers / datelines / signatures dropped.
Years: for diaries, letters and speeches (track=True) the year is carried forward from the last dateline or
heading that names a year inside the source's plausible range (year_source="dateline"); for books it is the
nominal year of composition/publication (year_source="nominal"); None when unknown.
Run:  python3 build_controls.py [--probe]      (--probe prints samples and writes nothing)
"""
import re, json, os, sys, collections, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')                          # the corpus folder
RAW = os.path.join(OUT, 'controls_raw')
CAP = 60000            # words per author (pieces are taken from the start of each source)
PIECE_MIN = 100        # a piece is closed only once it holds at least this many words
PIECE_MAX = 300        # target upper bound; a piece may exceed it only by one paragraph
SPLIT_LONG = 300       # paragraphs longer than this are split at sentence ends into <= PIECE_MAX-word parts
DROP_TAIL = 60         # pieces shorter than this (end of a source) are dropped

MONTHS = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
MONTH_RE = re.compile(r'\b' + MONTHS + r'\b', re.I)
WEEKDAY_RE = re.compile(r'\b(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day\b', re.I)
APOS_YEAR_RE = re.compile(r"^\W{0,3}(?:_?[A-Za-z][A-Za-z.]*,?_?\s+){0,6}'(\d\d)\b")

CONFIG = [
 dict(author='William H. Seward', title='The Works of William H. Seward, vol. 4 (speeches, addresses and papers 1853-1861), ed. G. E. Baker, 1884', src='ia:sewardwilliam04sewarich', year='1853-1861', kind='speech', years=(1853, 1861), track=True, mode='ocr_whole',
      start=r'^\s*ORATIONS\s+AND\s+ADDRESSES\.?\s*$', start_occurrence=1, end=r'^\s*APPENDIX\.\s*$', hint_footnotes=True,
      note='Orations and addresses 1853-1855, the biography of De Witt Clinton, political speeches 1855-1860 and Senate speeches 1853-1861 (pp. 119-678); the editor G. E. Baker\'s 100-page memoir that opens the volume and the appendix (speeches by others at the Chicago convention) are excluded; the date of each item is given in a footnote, which is the year source here; register: oratory.'),
 dict(author='Salmon P. Chase', title='Diary and Correspondence of Salmon P. Chase (AHA Annual Report 1902, publ. 1903), Part II: diary July-Oct. 1862 and later fragments', src='ia:diaryandcorrespo00chasrich', year='1862-1863', kind='diary', years=(1829, 1863), track=True, mode='ocr_whole', cap=30000,
      start=r'PART\s+II\.\s+DIARY', end=r'PART\s+III\.\s+SELECTED\s+LETTERS', note='Chase\'s own diary; the editor\'s footnotes are digit-led lines and are dropped by rule.'),
 dict(author='Salmon P. Chase', title='Diary and Correspondence of Salmon P. Chase (1903), Part III: selected letters of Chase 1846-1861', src='ia:diaryandcorrespo00chasrich', year='1846-1861', kind='letter', years=(1846, 1863), track=True, mode='ocr_whole', cap=30000,
      start=r'PART\s+III\.\s+SELECTED\s+LETTERS', end=r'LETTERS\s+TO\s+SALMON', note='Letters written by Chase (the later section of letters TO Chase is excluded); letter headers ("To Charles Sumner.") and datelines dropped by rule; editorial footnotes (digit-led) dropped.'),
 dict(author='Gideon Welles', title='Diary of Gideon Welles, vol. 1 (Aug. 1862-March 1864), 1911', src='ia:diaryofgideonwelv1well', year='1862-1864', kind='diary', years=(1861, 1864), track=True, mode='ocr_whole',
      start=r'^\s*1862\s*$|^\s*DIARY\s+OF\s+GIDEON\s+WELLES\s*$', end=r'^\s*APPENDIX\s*$', note='Diary entries; the editor\'s introduction is skipped; chapter synopses (dash-separated headings) and footnotes (digit/^-led lines) dropped; Welles revised the diary in the 1870s.'),
 dict(author='Charles Sumner', title='Charles Sumner: His Complete Works (Statesman ed., 1900), vol. 7: speeches and letters Sept. 1860-Oct. 1861, PG #48077', src='pg:48077', year='1860-1861', kind='speech', years=(1860, 1861), track=True, hint_indent_max=2, mode='pg_flush', cap=30000,
      start=r'^THE UNCONSTITUTIONALITY OF SLAVERY SHOWN FROM ITS BARBARISM\.\s*$', end=r'^FOOTNOTES\s*$', note='Flush-left paragraphs only (Sumner\'s speeches; his own letters are set 2 spaces in and are kept); the editors\' 4-space-indented headnotes, quoted matter and all APPENDIX sections are dropped; register: oratory.'),
 dict(author='Charles Sumner', title='Charles Sumner: His Complete Works (Statesman ed., 1900), vol. 8: speeches Dec. 1861-1863, PG #48170', src='pg:48170', year='1861-1863', kind='speech', years=(1861, 1863), track=True, hint_indent_max=2, mode='pg_flush', cap=30000,
      start=r'^REVISION AND CONSOLIDATION OF THE NATIONAL STATUTES\.\s*$', end=r'^FOOTNOTES\s*$', note='As vol. 7.'),
 dict(author='William O. Stoddard', title='Inside the White House in War Times (1890)', src='ia:insidewhitehouse00stod', year='1890', kind='memoir', nominal=1890, mode='ocr_whole',
      start=r'^\s*CHAPTER\s+I\.\s*$', start_occurrence=2, end=r'^\s*THE\s+END\.?\s*$|^\s*ADVERTISEMENTS', note='Memoir by Lincoln\'s third secretary; whole book after the contents.'),
 dict(author='Noah Brooks', title="Washington in Lincoln's Time (1895)", src='ia:washingtoninlinc00broo', year='1895', kind='memoir', nominal=1895, mode='ocr_whole',
      start=r'^\s*CHAPTER\s+I\b|^\s*I\s*$', end=r'^\s*INDEX\.?\s*$', note='Memoir (reworked from his 1862-65 Sacramento Union dispatches); whole book after the contents.'),
 dict(author='John G. Nicolay', title='The Outbreak of Rebellion (1881)', src='ia:outbreakofrebell00nico', year='1881', kind='history', nominal=1881, mode='ocr_whole',
      start=r'^\s*CHA[RK]LESTON\s+HARBOR\.\s*$', start_occurrence=2, end=r'^\s*INDEX\.?\s*$', note='Narrative history by Lincoln\'s other secretary; whole book after the contents.'),
 dict(author='Edward Everett', title='Orations and Speeches on Various Occasions, vol. 4 (1856-1865), 1868', src='ia:orationsspeeches04ever', year='1856-1865', kind='speech', years=(1856, 1868), track=True, mode='ocr_whole',
      start=r'^\s*THE\s+CHARACTER\s+OF\s+WASHINGTON', start_occurrence=1, end=r'ANALYTICAL\s+INDEX|^\s*INDEX\.?\s*$', note='Orations 1856-1865 (the volume opens with the title of the first oration; the analytical index at the end is excluded); the editor\'s bracketed notes are dropped by rule; register: oratory.'),
 dict(author='Walt Whitman', title='Specimen Days (1882; in Complete Prose Works, PG #8813): war memoranda 1862-65 and nature notes 1876-81', src='pg:8813', year='1862-1882', kind='diary', years=(1855, 1882), track=True, mode='pg_whole',
      start=r'^\s*SPECIMEN\s+DAYS\s*$', start_occurrence=2, end=r'^\s*COLLECT\s*$', note='Dated notes and memoranda (diary-like prose); the section titles carry the years ("SUMMER OF 1864", "Feb. \'64"); the autobiographical opening sections are undated and get the year of the nearest heading.'),
 dict(author='Ulysses S. Grant', title='Personal Memoirs of U. S. Grant (1885-86), PG #4367', src='pg:4367', year='1885', kind='memoir', nominal=1885, mode='pg_whole',
      start=r'^\s*CHAPTER\s+I\.\s*$', end=r'^\s*APPENDIX\s*$', note='Memoirs; pieces sampled evenly across the two volumes (which include quoted orders and dispatches that are not separable).'),
 dict(author='William T. Sherman', title='Memoirs of General William T. Sherman (1875), PG #4361', src='pg:4361', year='1875', kind='memoir', nominal=1875, mode='pg_whole',
      start=r'^\s*CHAPTER\s+I\.\s*$', note='Memoirs; pieces sampled evenly across the book; quoted official documents are embedded and not separable.'),
 dict(author='James Russell Lowell', title='Letters of James Russell Lowell, ed. C. E. Norton (1894), vol. 1', src='ia:lettersofjamesru01lowe_0', year='1844-1869', kind='letter', years=(1836, 1869), track=True, mode='ocr_letters',
      start=r'^\s*TO\s+C\.\s*F\.\s*BRIGGS', end=r'^\s*APPENDIX\.?\s*$', header=r'^\s*TO\s+[A-Z][A-Z .,\'\-]{2,50}(?:\s+[A-Z][a-z]+\.?\s+\d.*)?$', stop=None,
      note='Letters from 1844 onward; Norton\'s connecting notes are few and short and could not be separated from OCR; running heads/page numbers dropped.'),
 dict(author='Ralph Waldo Emerson', title='The Conduct of Life (1860), PG #39827', src='pg:39827', year='1860', kind='essay', nominal=1860, mode='pg_whole',
      start=r'^\s*I\.\s*$', note='Essays; whole book.'),
 dict(author='Frederick Douglass', title='Life and Times of Frederick Douglass (1881; PG #71893, 1892 ed.)', src='pg:71893', year='1881', kind='memoir', nominal=1881, mode='pg_whole',
      start=r'^\s*CHAPTER\s+I\.\s*$', start_occurrence=3, note='Autobiography; pieces sampled evenly after the introduction by G. L. Ruffin (the text starts at the first chapter of Part I; the two contents tables are skipped and the dash-separated chapter synopses dropped by rule).'),
 dict(author='Horace Greeley', title='Recollections of a Busy Life (1868)', src='ia:recollectionsofb00greeuoft', year='1868', kind='memoir', nominal=1868, mode='ocr_whole',
      start=r'^\s*I\.\s*$', end=r'^\s*(?:INDEX|APPENDIX)\.?\s*$', note='Autobiography; pieces sampled evenly across the book.'),
 dict(author='George William Curtis', title='Literary and Social Essays (1894; essays of 1853-1892), PG #8108', src='pg:8108', year='1853-1892', kind='essay', years=(1853, 1892), track=False, title_years=True, mode='pg_whole',
      start=r'^\s*(?:EMERSON|CONTENTS)\s*$', start_occurrence=2, note='Essays; the year of each essay is taken from the contents table (first year named for each title).'),
 dict(author='Bayard Taylor', title='Life and Letters of Bayard Taylor, ed. M. Hansen-Taylor and H. Scudder (1884), vol. 1', src='ia:lifelettersofbay00tayl', year='1840-1863', kind='letter', years=(1840, 1863), track=True, mode='ocr_letters',
      start=r'^\s*TO\s+HIS\s+MOTHER', end=r'^\s*INDEX\.?\s*$|^\s*END\s+OF\s+VOL', header=r'^\s*TO\s+[A-Z][A-Z .,\'\-]{2,50}\.?\s*$', stop=r"\b(?:Taylor|Bayard)\b",
      note='Quoted letters within an editorial biography; a letter is cut at the next paragraph that names Taylor in the third person or at the next letter header (heuristic).'),
 dict(author='John Lothrop Motley', title='The Correspondence of John Lothrop Motley, ed. G. W. Curtis (1889), vol. 1', src='ia:correspondenceof01motluoft', year='1832-1861', kind='letter', years=(1832, 1861), track=True, mode='ocr_letters',
      start=r'^\s*To\s+(?:Ms|his|Us)\s+Mother', end=r'^\s*INDEX\s*$', header=r'^\s*To\s+(?:Ms|his|Us|the|Mrs|Mr|Dr|Lady|Miss|Prof|Rev|Sir|Lord|Count|Baron|Madame|Mme|Mlle|[A-Z][a-z]+)\b[A-Za-z .,\'\-]{0,40}[.,]?\s*$', stop=None,
      note='Letters; the editor\'s brief connecting notes are not separable in OCR; "To his Mother" headers OCR as "To Ms Mother".'),
 dict(author='Mark Twain', title="Mark Twain's Letters, ed. A. B. Paine (1917), vols. 1-3 (1853-1885), PG #3193-3195", src='pg:3193+3194+3195', year='1853-1885', kind='letter', years=(1853, 1885), track=True, hint_indent_not=5, mode='pg_twain',
      note='Letters only: Paine\'s narrative is indented in the Gutenberg text and is dropped; letter headers ("To X:"), datelines and signatures dropped.'),
 dict(author='Henry Adams', title='The Education of Henry Adams (written 1905-07, publ. 1918), PG #2044', src='pg:2044', year='1907', kind='memoir', nominal=1907, mode='pg_whole',
      start=r'^\s*CHAPTER\s+I\s*$', note='Autobiography in the third person; pieces sampled evenly across the book; later than the 1850-1890 window (included as requested).'),
]


def period_of(year):
    if year is None:
        return None
    if year < 1861:
        return 'pre_war'
    if year <= 1865:
        return 'civil_war'
    return 'post_war'


def read_src(src):
    if src.startswith('pg:'):
        ids = src[3:].split('+')
        texts = []
        for i in ids:
            t = open(os.path.join(RAW, 'pg%s.txt' % i), encoding='utf-8', errors='replace').read()
            a = t.find('*** START OF THE PROJECT GUTENBERG EBOOK')
            b = t.find('*** END OF THE PROJECT GUTENBERG EBOOK')
            t = t[t.find('\n', a) + 1:b] if a >= 0 and b > 0 else t
            texts.append(t)
        t = '\n'.join(texts)
    else:
        t = open(os.path.join(RAW, 'ia_%s.txt' % src[3:]), encoding='utf-8', errors='replace').read()
    return t.replace('\r\n', '\n').replace('\r', '\n')


def find_line(lines, pat, occurrence=1, after=0):
    if not pat:
        return None
    rx = re.compile(pat)
    n = 0
    for i in range(after, len(lines)):
        if rx.search(lines[i]):
            n += 1
            if n == occurrence:
                return i
    return None


# ---------------------------------------------------------------- year tracking
def line_year(l, lo, hi):
    """Year named by a dateline / heading / running-head line, if any (None otherwise)."""
    s = l.strip()
    if not s or (re.match(r'^[1-9*^ijl]\s+[A-Z][a-z]', s) and not FOOTNOTE_HINTS):
        return None   # (footnote citation lines such as "1 An oration at Plymouth, 1855." are not datelines)
    w = s.split()
    ys = [int(y) for y in re.findall(r'(?<!\w)(1[89]\d\d)(?!\w)', s)]
    ys = [y for y in ys if lo <= y <= hi]
    if ys and len(w) <= 12 and (MONTH_RE.search(s) or WEEKDAY_RE.search(s) or not re.search(r'[a-z]', s)
                                or len(w) <= 4 or re.match(r'^\[?1[89]\d\d[\].]', s)):
        return ys[0]
    m = APOS_YEAR_RE.match(s)
    if m and MONTH_RE.search(s[:m.end()]):
        y = 1800 + int(m.group(1))
        if lo <= y <= hi:
            return y
    return None


def parse_title_years(lines):
    """Contents table of the form 'TITLE _source_, 1854.' -> {TITLE: 1854} (entries may wrap onto a second line)."""
    out = {}
    start = find_line(lines, r'^\s*CONTENTS\s*$')
    if start is None:
        return out
    entry = ''
    for l in lines[start + 1:start + 80]:
        s = l.strip()
        if not s:
            if entry:
                m = re.match(r"^([A-Z][A-Z .,'\-]+?)\s+(?:_|HARPER|Hitherto|Read|Printed|Putnam|North|Homes|Written).*?(?<!\w)(1[89]\d\d)(?!\w)", entry)
                if m:
                    out[m.group(1).strip().rstrip('.').upper()] = int(m.group(2))
                entry = ''
            continue
        entry = (entry + ' ' + s) if entry else s
    return out


FOOTNOTE_HINTS = False


def tag_years(seg, cfg):
    global FOOTNOTE_HINTS
    FOOTNOTE_HINTS = bool(cfg.get('hint_footnotes'))
    lo, hi = cfg.get('years', (1800, 1910))
    track = cfg.get('track', False)
    title_years = cfg.get('_title_years')
    max_ind = cfg.get('hint_indent_max')
    not_ind = cfg.get('hint_indent_not')
    out, year = [], None
    for l in seg:
        if track:
            ind = len(l) - len(l.lstrip(' '))
            ok = (max_ind is None or ind <= max_ind) and (not_ind is None or ind != not_ind)
            if ok:
                y = line_year(l, lo, hi)
                if y:
                    year = y
        if title_years:
            t = re.sub(r'[\s.]+$', '', l.strip()).upper()
            if t in title_years:
                year = title_years[t]
        out.append((l, year))
    return out


# ---------------------------------------------------------------- line / paragraph cleaning
def ocr_clean_lines(tagged):
    """Drop running heads, bare page numbers and digit-led footnote blocks from OCR text (tagged lines)."""
    out = []
    i = 0
    while i < len(tagged):
        l = tagged[i][0]
        s = l.strip()
        if re.match(r'^\s*\d{1,4}\s*$', s) or re.match(r'^[\[\(]?\s*\d{1,4}\s*[\]\)]$', s):
            i += 1
            continue
        if s and not re.search(r'[a-z]', s) and len(s) <= 70 and len(s) >= 3:
            i += 1
            continue   # running head / caps heading
        if re.match(r'^\s*[1-9*^]\s*\S', l) and (i == 0 or tagged[i - 1][0].strip() == '') and not re.match(r'^\s*\d{1,2}(st|nd|rd|th)?\s+[A-Z][a-z]+', l):
            j = i
            while j < len(tagged) and tagged[j][0].strip():
                j += 1
            i = j
            continue
        out.append(tagged[i])
        i += 1
    return out


def ocr_clean_lines_keep_headers(tagged, hdr):
    out = []
    i = 0
    while i < len(tagged):
        l = tagged[i][0]
        s = l.strip()
        if hdr.match(l) and len(s) <= 60:
            out.append(tagged[i])
            i += 1
            continue
        if re.match(r'^\s*\d{1,4}\s*$', s):
            i += 1
            continue
        if s and not re.search(r'[a-z]', s) and len(s) <= 70 and len(s) >= 3:
            i += 1
            continue
        if re.match(r'^\s*[1-9*]\s+\S', l) and (i == 0 or tagged[i - 1][0].strip() == ''):
            j = i
            while j < len(tagged) and tagged[j][0].strip():
                j += 1
            i = j
            continue
        out.append(tagged[i])
        i += 1
    return out


def synopsis_or_junk(p):
    """Chapter synopses ('A -- B -- C'), tables of contents, headers, OCR junk, third-person editorial notes."""
    if p.count(' — ') + p.count('--') >= 3 and p.count('. ') <= 2:
        return True
    letters = sum(c.isalpha() or c == ' ' for c in p)
    if letters / max(1, len(p)) < 0.82:
        return True
    w = p.split()
    if len(w) <= 8 and (re.search(r'\b1[89]\d\d\b', p) or re.match(r'^To [A-Z]', p) or re.search(r'\.\s*\d+$', p)):
        return True
    if re.search(r'\bMr\. Sumner\b', p) and not re.search(r'\bI\b', p):
        return True
    if p.startswith('[') and p.rstrip().endswith(']'):
        return True   # editor's bracketed note
    weird = sum(1 for t in w if re.search(r'[\^~|\\=+#@<>{}§¶£_]', t) or re.search(r'[a-z][A-Z][a-z]', t))
    if weird >= 3 and weird / len(w) > 0.03:
        return True   # garbled OCR page
    return False


def blocks_from(tagged):
    """Group tagged lines into blank-line-separated blocks: (raw_lines, joined_text, year_at_first_line)."""
    out, cur = [], []

    def finish(cur):
        t = ''
        for l, y in cur:
            s = re.sub(r'\s+', ' ', l).strip()
            if t.endswith('-') and re.match(r'^[a-z]', s):
                t = t[:-1] + s
            else:
                t = (t + ' ' + s) if t else s
        return [l for l, y in cur], t, cur[0][1]

    for l, y in tagged:
        if not l.strip():
            if cur:
                out.append(finish(cur))
                cur = []
            continue
        cur.append((l, y))
    if cur:
        out.append(finish(cur))
    return out


def pg_filter(t):
    """Cleaned paragraph text of a Gutenberg block, or None if it is not the author's prose."""
    if len(t.split()) < 3:
        return None
    t = re.sub(r'\[Illustration[^\]]*\]', '', t)
    if not re.search(r'[a-z]', t):
        return None
    if re.match(r'^\s*(CHAPTER|BOOK|PART)\s+[IVXLC\d]+', t):
        return None
    t = t.replace('_', '')
    if re.match(r'^\[\d+\]', t) or synopsis_or_junk(t):
        return None
    t = re.sub(r'\s+', ' ', re.sub(r'\[\d+\]', '', t)).strip()
    return t if len(t.split()) >= 3 else None


def skip_appendices(tagged):
    """Sumner's Works: drop each APPENDIX section up to the next speech title (flush all-caps line + all-caps subtitle)."""
    out, skipping, dropped = [], False, 0
    for i, (l, y) in enumerate(tagged):
        s = l.rstrip()
        if not skipping and s == 'APPENDIX.':
            skipping = True
            dropped += 1
            continue
        if skipping:
            if s and not s.startswith(' ') and not re.search(r'[a-z]', s) and len(s) >= 20 and s.endswith('.'):
                j = i + 1
                while j < len(tagged) and not tagged[j][0].strip():
                    j += 1
                if j < len(tagged) and not tagged[j][0].startswith(' ') and not re.search(r'[a-z]', tagged[j][0]):
                    skipping = False
                    out.append((l, y))
            continue
        out.append((l, y))
    return out, dropped


def twain_blocks(blocks):
    out, started = [], False
    for raw, s, y in blocks:
        if not started:
            if re.match(r'^To [A-Z].*:$', s):
                started = True
            continue
        if all(l.startswith('     ') or not l.strip() for l in raw):
            continue   # Paine's indented narrative (and right-aligned datelines)
        if re.match(r'^To [A-Z].*:$', s) or (re.match(r'^(?:[A-Z][A-Za-z.\' ]+, )?[A-Z][a-z]+\.? \d', s) and len(s) < 60):
            continue   # header / dateline
        if len(s.split()) <= 6 and (s.upper() == s or re.match(r'^(?:Yours|Affectionately|Truly|Your|Lovingly|Sincerely|Cordially|Ever|Love|With|Mark|Sam|Saml|S\. L\.)', s)):
            continue   # closing / signature
        if re.match(r'^(?:VOLUME|CHAPTER|LETTERS|MARK TWAIN)', s) or re.match(r'^[IVXLC]+\.', s):
            continue
        if re.match(r'^\(', s) and len(s) < 120:
            continue   # editor's parenthetical
        if s.upper() == s:
            continue
        s = s.replace('_', '')
        if len(s.split()) < 3 or synopsis_or_junk(s):
            continue
        out.append((s, y))
    return out


def ocr_letters(tagged, cfg):
    hdr = re.compile(cfg['header'])
    stop = re.compile(cfg['stop']) if cfg.get('stop') else None
    seg = ocr_clean_lines_keep_headers(tagged, hdr)
    heads = [i for i, (l, y) in enumerate(seg) if hdr.match(l) and len(l.strip()) <= 60]
    out = []
    for k, h in enumerate(heads):
        end = heads[k + 1] if k + 1 < len(heads) else len(seg)
        paras = [(t, y) for raw, t, y in blocks_from(seg[h + 1:end])]
        # drop dateline(s) at the start of the letter
        while paras and (re.search(r'\b1[89]\d\d\b', paras[0][0]) and len(paras[0][0].split()) <= 10 or len(paras[0][0].split()) <= 3):
            paras.pop(0)
        for t, y in paras:
            if stop and stop.search(t) and not re.search(r'\bI\b', t[:60]):
                break   # editor's narrative resumes
            if len(t.split()) <= 4 and re.match(r'^[A-Z][A-Za-z. ]+[.,]?$', t):
                continue   # signature / initials
            if len(t.split()) >= 3 and not synopsis_or_junk(t):
                out.append((t, y))
    return out


# ---------------------------------------------------------------- extraction
def extract(cfg):
    text = read_src(cfg['src'])
    lines = text.split('\n')
    info = {}
    a = find_line(lines, cfg.get('start'), cfg.get('start_occurrence', 1)) if cfg.get('start') else 0
    if a is None:
        a, info['start_not_found'] = 0, True
    b = find_line(lines, cfg.get('end'), 1, after=a + 50) if cfg.get('end') else len(lines)
    if b is None:
        b, info['end_not_found'] = len(lines), True
    info['start_line'], info['end_line'] = a + 1, b
    if cfg.get('title_years'):
        cfg['_title_years'] = parse_title_years(lines)
        info['title_years'] = sorted(cfg['_title_years'].items())
    tagged = tag_years(lines[a:b], cfg)
    mode = cfg['mode']
    paras = []
    if mode in ('pg_whole', 'pg_flush'):
        if mode == 'pg_flush':
            tagged, info['appendices_skipped'] = skip_appendices(tagged)
        for raw, t, y in blocks_from(tagged):
            if mode == 'pg_flush' and len(raw[0]) - len(raw[0].lstrip(' ')) > 2:
                continue
            if len(raw) >= 4 and sum(len(l.strip()) < 50 for l in raw) >= 0.8 * len(raw) and sum(bool(re.match(r'\s*[A-Z]', l)) for l in raw) >= 0.7 * len(raw):
                continue   # verse (short capitalised lines)
            t = pg_filter(t)
            if t:
                paras.append((t, y))
    elif mode == 'pg_twain':
        paras = twain_blocks(blocks_from(tagged))
    elif mode == 'ocr_whole':
        for raw, t, y in blocks_from(ocr_clean_lines(tagged)):
            if len(t.split()) >= 3 and not synopsis_or_junk(t):
                paras.append((t, y))
    elif mode == 'ocr_letters':
        paras = ocr_letters(tagged, cfg)
    else:
        raise ValueError(mode)
    avail = sum(len(t.split()) for t, y in paras)
    return paras, avail, info


# ---------------------------------------------------------------- pieces
def split_long(t):
    w = len(t.split())
    if w <= SPLIT_LONG:
        return [t]
    n = math.ceil(w / PIECE_MAX)
    limit = math.ceil(w / n) + 15
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'(\[])|(?<=[.!?][\'")\]])\s+(?=[A-Z"\'(\[])', t)
    parts, cur, cw = [], [], 0
    for s in sents:
        sw = len(s.split())
        if cur and cw + sw > limit:
            parts.append(' '.join(cur))
            cur, cw = [], 0
        cur.append(s)
        cw += sw
    if cur:
        if parts and cw < 60:
            parts[-1] += ' ' + ' '.join(cur)
        else:
            parts.append(' '.join(cur))
    return parts


def make_pieces(paras):
    pieces, cur, cw, cy = [], [], 0, None

    def flush():
        nonlocal cur, cw, cy
        if cur:
            pieces.append(dict(text='\n'.join(cur), word_count=cw, year=cy))
        cur, cw, cy = [], 0, None

    for t, y in paras:
        for part in split_long(t):
            w = len(part.split())
            if cur and ((cw + w > PIECE_MAX and cw >= PIECE_MIN) or (y != cy and cw >= PIECE_MIN)):
                flush()
            if not cur:
                cy = y
            cur.append(part)
            cw += w
    flush()
    return pieces


def slug(author):
    return re.sub(r'[^a-z]', '', author.split()[-1].lower())


def main():
    probe = '--probe' in sys.argv
    rows, summary = [], collections.OrderedDict()
    counters = collections.defaultdict(int)
    for cfg in CONFIG:
        paras, avail, info = extract(cfg)
        pieces = make_pieces(paras)
        short = [p for p in pieces if p['word_count'] < DROP_TAIL]
        pieces = [p for p in pieces if p['word_count'] >= DROP_TAIL]
        au = cfg['author']
        st = summary.setdefault(au, dict(author=au, sources=[], pieces=0, words=0, periods=collections.Counter(), kinds=collections.Counter(), years=collections.Counter()))
        cap_entry = min(cfg.get('cap', CAP), CAP - st['words'])
        total = sum(p['word_count'] for p in pieces)
        step = max(1.0, total / cap_entry) if cap_entry > 0 else 1e9   # pieces are sampled evenly across the source
        idx = sorted(set(int(i * step) for i in range(int(math.ceil(len(pieces) / step)) + 1) if int(i * step) < len(pieces)))
        taken, tw = [], 0
        for i in idx:
            p = pieces[i]
            if tw + p['word_count'] > cap_entry + 100:
                break
            taken.append(p)
            tw += p['word_count']
        url = ('https://www.gutenberg.org/ebooks/' + cfg['src'][3:].split('+')[0]) if cfg['src'].startswith('pg:') else 'https://archive.org/details/' + cfg['src'][3:]
        nominal = cfg.get('nominal')
        for p in taken:
            counters[au] += 1
            year = p['year'] if p['year'] is not None else nominal
            ysrc = 'dateline' if p['year'] is not None else ('nominal' if nominal else None)
            rows.append(dict(id='ctrl-%s-%04d' % (slug(au), counters[au]), author=au, source=cfg['src'], title=cfg['title'], url=url,
                             kind=cfg['kind'], year=year, year_source=ysrc, period=period_of(year), word_count=p['word_count'], text=p['text']))
            st['periods'][period_of(year) or 'unknown'] += 1
            st['kinds'][cfg['kind']] += 1
            st['years'][year or 'unknown'] += 1
        st['sources'].append(dict(title=cfg['title'], src=cfg['src'], url=url, kind=cfg['kind'], mode=cfg['mode'], words_available=avail, pieces=len(taken), words=tw, note=cfg['note'], probe=info))
        st['pieces'] += len(taken)
        st['words'] += tw
        yc = collections.Counter(p['year'] for p in taken)
        print('%-24s %-11s %-8s avail=%7d pieces=%4d words=%6d short_dropped=%d years=%s %s' % (
            au, cfg['mode'], cfg['kind'], avail, len(taken), tw, len(short), dict(sorted(yc.items(), key=lambda kv: str(kv[0]))), {k: v for k, v in info.items() if k != 'title_years'}))
        if probe and taken:
            print('     FIRST:', taken[0]['text'][:230].replace('\n', ' / '))
            mid = len(taken) // 2
            print('     MID  :', taken[mid]['text'][:230].replace('\n', ' / '))
            print('     LAST :', taken[-1]['text'][-200:].replace('\n', ' / '))
            wc = sorted(p['word_count'] for p in taken)
            print('     piece words: min=%d median=%d max=%d  >300: %d  <150: %d' % (wc[0], wc[len(wc) // 2], wc[-1], sum(w > 300 for w in wc), sum(w < 150 for w in wc)))
    if not probe:
        with open(os.path.join(OUT, 'controls.jsonl'), 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        for st in summary.values():
            st['periods'] = dict(st['periods'])
            st['kinds'] = dict(st['kinds'])
            st['years'] = {str(k): v for k, v in sorted(st['years'].items(), key=lambda kv: str(kv[0]))}
        with open(os.path.join(OUT, 'controls_summary.json'), 'w', encoding='utf-8') as f:
            json.dump(list(summary.values()), f, ensure_ascii=False, indent=1)
        print('TOTAL authors', len(summary), 'pieces', len(rows), 'words', sum(r['word_count'] for r in rows))


if __name__ == '__main__':
    main()
