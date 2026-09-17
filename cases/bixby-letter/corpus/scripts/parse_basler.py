#!/usr/bin/env python3
"""Parse the archive.org OCR of Basler's Collected Works of Abraham Lincoln
(vols I, IV, VII, VIII) into individual items.

Usage: python3 parse_basler.py  (output goes to the corpus folder, one level up from this script; the OCR is read from ia/txt/ there, or from $S/ia/txt/ when S is set)

Layout rules used (see README.md):
  * a page ends with a bracketed page number "[116]" on its own line;
  * the next page begins with a running head, an all-caps date such as
    "NOVEMBER 21, 1864" (heavily OCR-garbled: "JTAISTUARY 15, 1864");
  * every item begins with a title-cased heading carrying a superscript "1"
    ("To William S. Rosecrans1"); the superscript is OCR'd as 1 l i I * ! x ^ ' ";
  * the item text follows (dateline / inside address / salutation, body,
    signature), then the footnote block: "1 ALS, DLC-RTL. ..." The first
    footnote starts with the manuscript-source code (ALS, ADfS, ADf, AD, ADS,
    AES, AE, AL, LS, DS, Df, DfS, ES, Copy) or a printed source (newspaper,
    catalog, book). The footnote block runs to the next heading.
"""
import re, json, csv, os, sys, difflib, collections, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('S', os.path.join(HERE, '..'))   # holds ia/txt/, the archive.org OCR downloads (not included in this folder)
IA = os.path.join(ROOT, 'ia', 'txt')
OUT = os.path.join(HERE, '..')                          # the corpus folder

VOLUMES = [
    # (volume label, identifier, first item line (1-based), year range of the main chronological run)
    ('I',    'collectedworksof015581mbp', 1298, (1824, 1848)),
    ('IV',   'collectedworksof015582mbp', 500,  (1860, 1861)),
    ('VII',  'collectedworksof015583mbp', 478,  (1863, 1864)),
    ('VIII', 'collectedworksof015584mbp', 536,  (1864, 1865)),
]

# ----------------------------------------------------------------------------
# regexes
PAGE_RE = re.compile(r'^\s*[\[£(\{]\s*(\d{1,3})\s*[\]\)\}]?\s*$|^\s*[\[£(\{]\s*(\d{1,3})\s*$')
MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST',
          'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
MONTH_RE = re.compile(r'\b(Jan(?:uary|y|\.)?|Feb(?:ruary|y|\.)?|Mar(?:ch|\.)?|Apr(?:il|\.)?|May|June?|July?|'
                      r'Aug(?:ust|\.)?|Sep(?:t(?:ember|\.)?|\.)?|Oct(?:ober|o|\.)?|Nov(?:ember|\.)?|Dec(?:ember|r|\.)?|Deer\.?|Decr\.?)\b\.?', re.I)
DIGITISH = r'[0-9iIlOoQaSZBG|±!§/\?\*\^]'
DAY_RE = re.compile(r'(' + DIGITISH + r'{1,2})\s*(?:st|nd|rd|th|d|ist|aist|loth|nth)?[.,]?')
YEAR_RE = re.compile(r'((?:1|i|I|l|±|\*|!)\s?[8]\s?' + DIGITISH + r'\s?' + DIGITISH + r')')
BRACKET_DATE_RE = re.compile(r'\[\s*c\.?\s*([^\]]*?)\]|\[\s*([A-Z][a-z]+\.?\s+' + DIGITISH + r'{1,2}[^\]]*?\d{4})\s*\]')

HEAD_WORDS = ('To Speech Speeches Proclamation Order Orders Endorsement Endorsements Indorsement Memorandum Memoranda '
              'Telegram Reply Response Annual Message Remarks Address Draft Drafts Fragment Fragments Notes Note Opinion '
              'Pass Passes Recommendation Recommendations Instructions Instruction Call Approval Check Receipt Bill Agreement '
              'Deed Contract Verses Communication Petition Report Amendment Bond Promissory Answer Answers Announcement '
              'Discharge Pardon Interview Appointment Certificate Executive Autograph Toast Emancipation Last Second First '
              'Gettysburg Resolution Resolutions Circular Handbill Advertisement Legal Plat Survey Table List Editorial Letter '
              'Form Document Appraisal Election Eulogy Lecture Debate Farewell Inaugural Temperance Protest Poll Warrant '
              'Affidavit Mortgage Power Lease Assignment Declaration Plea Brief Argument Motion Notice Subscription Estimate '
              'Estimated Inscription Copy Tribute Statement Suggestion Suggestions Tabulation Calculation Calculations Proposed '
              'Proposal Preamble Ordinance Testimonial Remission Commission Sketch Story Anecdote Prayer Poem Poetry Rhymes '
              'Marginal Comment Comments Conversation Definition Concurrent Joint Dispatch Despatch Authorization Permit '
              'Introduction Remonstrance Application Certification Refusal Acceptance Special General Presidential Testimony '
              'Deposition Sale Account Accounts Receipts Payment Voucher Record Records Minute Minutes Tally Names Signature '
              'Autobiography Autobiographical Reward Bail Judgment Decree Writ Summons Complaint Demurrer Replication Praecipe '
              'Bond Award Reasons Guarantee Guaranty Petitions Grant Nomination Nominations Query Queries Explanation Suggested '
              'Notation Endorsed Directions Direction Confidential Private Proposition Propositions Compromise Amendments '
              'Speeches Statement Conditions Terms Additional Substitute Draft Points Basis Plan Outline Analysis Abstract '
              'Chart Map Ballot Counting Count Vote Deposition Charge Charges Verdict Reply Rejoinder Duplicate Fee Fees '
              'Order Interlineations Revision Corrections Correction Insertion Instruments Instrument Assignment Release '
              'Certificates Exercise Exercises Grammar Arithmetic Sums Sum Exhibit Exhibits Address Speech').split()
HEAD_WORDS = set(HEAD_WORDS) - set('Executive General Special Private Confidential Copy Grant Judge Names Record Account Sale Vote Sum Fee Fees Bond Points Basis Plan Terms Conditions Reasons Direction Directions Chart Map Count Charge Charges Verdict Release Exercise Exercises Grammar Arithmetic Sums Exhibit Exhibits Signature Duplicate Presidential Payment Voucher Records Minute Minutes Tally Award Story Prayer Poem Poetry Rhymes Query Queries Comment Comments Marginal Conversation Definition Introduction Explanation Analysis Abstract Outline Substitute Additional Notation Endorsed Suggested Insertion Instruments Instrument Interlineations Revision Correction Corrections Nomination Nominations Compromise Testimony Deposition Sketch Anecdote'.split())
MARKER_CHARS = "1lIi*!x^'\"¹»~"
HEAD_END_RE = re.compile(r'(?<=[A-Za-z\)\]\'"])[.,]?[' + re.escape(MARKER_CHARS) + r']{1,2}\s*$')
HEAD_END_SP_RE = re.compile(r'(?<=[A-Za-z\)\]\'"])[.,]?\s+[1*!^¹»~]{1,2}\s*$')
YEARISH_RE = re.compile(r'\b[1iIl±*!]\s?8\s?[0-9iIlOoQaS±*!§/]\s?[0-9iIlOoQaS±*!§/]\b|\b1[89]\d\d\b')
DATELINE_WORDS = re.compile(r'\b(Mansion|Executive Office|Hon\.?|Hon:|Esq\.?|Messrs|Mr\.|Mrs\.|Dear|Sir\b|Gentlemen|Madam|Private|Confidential|Cypher|Cipher|Telegraph|War Department|Head\s*-?\s*Quarters|Headquarters|Major|General|Lieut|Col\.|Capt\.|Gov\.|Governor|Secretary|Commanding|Officer|Attorney)\b')
TO_NAME_RE = re.compile(r'^To\s+(?:(?:Mrs?|Messrs|Miss|Dr|Rev|Gov|Gen|Col|Capt|Maj|Judge|Hon|Lieut|Bishop|Sister|Brother)\.?\s+)?(?:[A-Z][\w\'.,&-]*\s*){1,6}$')

CODES = ['ALS', 'ADfS', 'ADf', 'ADS', 'AD', 'AES', 'AE', 'AL', 'LS', 'DS', 'DfS', 'Df', 'ES', 'Copy', 'Copies',
         'Photostat', 'Facsimile', 'Text', 'Typescript', 'Broadside', 'Pamphlet', 'Printed', 'Ms', 'MS', 'Recorded']
AUTOGRAPH = {'ALS', 'ADfS', 'ADf', 'ADS', 'AD', 'AES', 'AE', 'AL'}
CODE_FIX = {'AIS': 'ALS', 'AI': 'AL', 'DSt': 'DS', 'ALSt': 'ALS', 'ADfSt': 'ADfS', 'ALSj': 'ALS', 'AXS': 'ALS', 'ALSs': 'ALS',
            'ADfSs': 'ADfS', 'AESs': 'AES', 'ADSs': 'ADS', 'ADs': 'AD', 'AEs': 'AE', 'ADFS': 'ADfS', 'ADF': 'ADf', 'DFS': 'DfS', 'DF': 'Df',
            'AIDS': 'ADS', 'AID': 'AD', 'AILS': 'ALS', 'ALSP': 'ALS', 'ALSF': 'ALS', 'ADP': 'AD', 'AESP': 'AES', 'ADfSP': 'ADfS',
            'ADSP': 'ADS', 'DSP': 'DS', 'LSP': 'LS', 'CopyP': 'Copy', 'Copv': 'Copy', 'Gopy': 'Copy', 'Copj': 'Copy'}
FN_MARK = r'^\s*(?:[' + re.escape(MARKER_CHARS) + r']|\(1\)|1\.|\*\*|\'\'|\'\s*\')\s*'
FN_STRICT_RE = re.compile(FN_MARK + r'([A-Za-z]{1,6})\b[-\s,.;:]')
SIGILS = ('DLC DNA IHi ICHi ORB ISLA NHi CSmH NN RPB MH MHi PHi CtY NjP InU IU ICU OFH OCHP WHi MoSHi NcD ViU DLM NBuHi NRU '
          'NIC MB MWA MdHi OClWHi THaroL NAuE InFtwL IJI ICN NNP MiU CLU CSt NhHi NjMoHP OO PU MeHi Vi WvU NNC NcU TxU IaDaM OHi '
          'CCamarSJ InHi IaHA MnHi NN-P NNPM PPRF PHC PSC OCU OrU RHi RPAB ViHi WHi NbO KyLoF OCl DNM DGU DAU NjR MB-P NhD OMC '
          'IaU KHi MoHi MdAN NIHi NHi-Bryant ICHi-Barrett NR-P NN-Berg CtHi CLSU CSmH-P DLC-RTL DLC-Nicolay').split()
SIGIL_RE = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, SIGILS), key=len, reverse=True)) + r')\b')
PRINTED_CUES = re.compile(r'\b(Journal|Register|Tribune|Times|Herald|Transcript|Press|Gazette|Democrat|Republican|Chronicle|'
                          r'Intelligencer|Star|Sentinel|Courier|Bulletin|Advertiser|Post|Globe|Statesman|Enquirer|Union|Argus|Whig|'
                          r'Telegraph|Ledger|Record|Sangamo|Illinois|Boston|New York|Chicago|Washington|Philadelphia|Cincinnati|'
                          r'Daily|Weekly|National|Evening|Morning|Congressional|House|Senate|Official|OR|Nicolay|Hay|Herndon|Tracy|'
                          r'Hertz|Angle|Lambert|Barrett|Parke-Bernet|Anderson|American|Autograph|Stan\.|Emanuel|Proceedings|Report|'
                          r'Reports|Executive|Statutes|Laws|Catalog|Catalogue|Sale|Owned|owned|supra|infra|Photostat|Facsimile|'
                          r'Debates|Political|Life|History|Memoir|Reminiscences|Works|Beveridge|Sandburg|Pratt|Tarbell|Weik|'
                          r'Lapsley|Rothschild|Diary|Letters|Papers|Collection|Speech|Speeches|Book Shop|Bookshop|Broadside|Pamphlet|'
                          r'Printed|Original|Missing|Text|copy|Copy|Photocopy|manuscript|Manuscript|Ms\.|MS\.|Lincoln|Item|No\.|'
                          r'Session|Cong\.|Congress|Document|Doc\.|Exec\.|Message|Messages|Richardson|Basler|Thomas|Randall|Wilson|NH|Sold|Photograph|Typescript|Hay-Nicolay|Nicolay-Hay|Association|Bulletin|Quarterly|Magazine|Review|Herald)\b')

HEADER_CUES = re.compile(r'^\s*(Hon\b|Hon:|Maj\b|Major|Gen\b|Gen:|General|Lieut|Lt\b|Col\b|Colonel|Capt\b|Captain|Dr\b|Rev\b|Mr\b|Mrs\b|Miss\b|'
                         r'Messrs|Esq|His Excellency|Her Excellency|Governor|Gov\b|Secretary|Sec\b|Officer|Commanding|Friend|Dear|My [Dd]ear|'
                         r'Sir\b|Sirs\b|Gentlemen|Madam|Judge|Brother|Private|Confidential|Cypher|Cipher|To the|President|Commodore|'
                         r'Admiral|Surgeon|Provost|Adjutant|Commissioner|Attorney|Postmaster|Paymaster|Quartermaster|Chief|Speaker|'
                         r'Executive|War Department|Head|Office|United States|U\.S\.|Washington|Springfield|Vandalia|New Salem|'
                         r'Lieutenant|Doctor|Bishop|Rev\.|Honorable|Hon\.|Superintendent|Marshal|Sheriff|Clerk|Excellency|'
                         r'Mother|Father|Son|Daughter|Cousin|Uncle|Aunt|Wife|Husband|Sister|Master|Comdg|Commander|Sergeant|Serg\b|'
                         r'Sergt|Corporal|Corp\b|Chaplain|Agent|Collector|Assessor|Register|Receiver|Editor|Editors|Publisher|'
                         r'Mayor|Senator|Representative|Member|Members|Delegate|Delegates|Committee|Board|Trustees|Directors|'
                         r'Citizens|People|Voters|Electors|Whigs|Republicans|Democrats|Sangamon|Sangamo|Illinois|Ills\b|Ill\b)')
PLACE_CUES = re.compile(r'(Executive\s+Mansion|Executive\s+Office|War\s+Department|Washington|Springfield|Head\s*-?\s*Quarters|'
                        r'Headquarters|Military\s+Telegraph|Cypher|Cipher|House\s+of\s+Representatives|Vandalia|New\s+Salem|'
                        r'\bIlls\b|\bIllinois\b|\bD\.\s*C\.|\bVa\.|\bPa\.|\bKy\.|\bInd\.|\bMo\.|\bTenn\.|\bMd\.|City\s*-?\s*Point|'
                        r'Navy\s+Department|Treasury\s+Department|State\s+Department|Department\s+of|Bloomington|Chicago|Peoria|'
                        r'Tremont|Beardstown|Danville|Urbana|Clinton|Decatur|Jacksonville|Quincy|Alton|Cincinnati|Harrisburg|'
                        r'Fortress\s+Monroe|Fort\s+Monroe|Albany|New\s+York|Philadelphia|Baltimore|Lexington|Louisville|Nashville|'
                        r'Steamer|Aboard|On\s+board)', re.I)

CLOSING_RE = re.compile(r'(truly|friend|serv(?:an)?t|respectfully|sincerely|&c|ever|obediently|obed[ti]?\.?|yours|Yours|affectionately|'
                        r'faithfully|gratefully|cordially|hastily|haste|haste,|regards|compliments|Very|Your|A\.\s*Lincoln|farewell)\W*$', re.I)


def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def digitize(tok):
    m = {'i': '1', 'I': '1', 'l': '1', '|': '1', '±': '1', '!': '1', 'o': '0', 'O': '0', 'Q': '9', 'a': '2', 'S': '5',
         'Z': '2', 'B': '8', 'G': '6', '/': '7', '*': '1', '^': '', '?': '', '§': '8', 'D': '0', 'T': '7'}
    return ''.join(m.get(c, c) for c in tok if c.isalnum() or c in '|±!/*^?§')


def exact_month(word):
    w = re.sub(r'[^A-Za-z]', '', word).upper()
    full = {m: i + 1 for i, m in enumerate(MONTHS)}
    abbr = {'JAN': 1, 'JANY': 1, 'JANUAY': 1, 'FEB': 2, 'FEBY': 2, 'FEBRUAY': 2, 'MAR': 3, 'MCH': 3, 'APR': 4, 'APL': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7,
            'AUG': 8, 'AUGT': 8, 'SEP': 9, 'SEPT': 9, 'SEPTR': 9, 'OCT': 10, 'OCTO': 10, 'OCTR': 10, 'NOV': 11, 'NOVR': 11, 'NOVEM': 11,
            'DEC': 12, 'DECR': 12, 'DEER': 12, 'DECEM': 12, 'DECEMB': 12, 'NOVEMB': 11, 'SEPTEM': 9, 'FEBR': 2, 'JANR': 1}
    return full.get(w) or abbr.get(w) or 0


def fuzzy_month(word):
    """Return 1-12 for an (OCR-garbled) month word, else 0."""
    w = re.sub(r'[^A-Za-z]', '', word).upper()
    if not w:
        return 0
    full = {m: i + 1 for i, m in enumerate(MONTHS)}
    abbr = {'JAN': 1, 'JANY': 1, 'FEB': 2, 'FEBY': 2, 'MAR': 3, 'APR': 4, 'APL': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9,
            'SEPT': 9, 'OCT': 10, 'OCTO': 10, 'NOV': 11, 'DEC': 12, 'DECR': 12, 'DEER': 12, 'DECEM': 12}
    if w in full:
        return full[w]
    if w in abbr:
        return abbr[w]
    if len(w) >= 5:
        best = difflib.get_close_matches(w, MONTHS, n=1, cutoff=0.6)
        if best:
            return full[best[0]]
        # garbled with junk letters like JTAISTUARY -> strip common OCR junk
        w2 = re.sub(r'^(JT|IST|3NT|JN|TST|ISTO|JTA|JTU)', '', w)
        best = difflib.get_close_matches(w2, MONTHS, n=1, cutoff=0.55)
        if best:
            return full[best[0]]
    return 0


def parse_date_string(s, year_range=None):
    """Parse 'Nov. ai, 1864' / 'November 19, 1864' / '2ist. November, 1864' / 'Deer. 8— 1847' -> (y, m, d) with None for missing."""
    s = s.replace('—', '-')
    s = re.sub(r'\b(1[89]\d)/(\d)\b', r'\1\2', s)          # "186/5" -> "1865"
    tokens = re.findall(r'[A-Za-z]+\.?|' + DIGITISH + r'+(?:st|nd|rd|th|d)?|[,.;:\-\[\]()]', s)
    y = m = d = None
    for i, t in enumerate(tokens):
        mi = exact_month(t) if re.match(r'^[A-Za-z]', t) else 0
        if not mi and re.match(r'^[A-Za-z]', t) and len(re.sub(r'[^A-Za-z]', '', t)) >= 5:
            # fuzzy month names only when followed by a day-like token and a year-like token
            nxt = [x for x in tokens[i + 1:i + 4] if x not in (',', '.', ';', '-', ':')]
            if len(nxt) >= 2 and re.match(r'^' + DIGITISH + r'{1,2}(?:st|nd|rd|th|d)?$', nxt[0]) and re.match(r'^' + DIGITISH + r'{4}$', nxt[1]):
                mi = fuzzy_month(t)
        if mi and m is None and (len(re.sub(r'[^A-Za-z]', '', t)) >= 3):
            m = mi
            # day after month
            j = i + 1
            while j < len(tokens) and j <= i + 3:
                tj = tokens[j]
                if re.match(r'^' + DIGITISH + r'+(?:st|nd|rd|th|d)?$', tj):
                    core = re.sub(r'(st|nd|rd|th|d)$', '', tj)
                    dg = digitize(core)
                    if len(dg) == 4 and dg.startswith('1'):
                        y = int(dg) if dg.isdigit() else None
                        break
                    if dg.isdigit() and 1 <= int(dg) <= 31 and d is None:
                        d = int(dg)
                    elif dg.isdigit() and len(dg) == 3 and 1 <= int(dg[:2]) <= 31 and d is None:
                        d = int(dg[:2])
                    j += 1
                    continue
                if tj in (',', '.', ';', '-', ':'):
                    j += 1
                    continue
                break
            # day before month ("2ist. November, 1864")
            if d is None and i >= 1:
                prev = tokens[i - 1] if tokens[i - 1] not in (',', '.', '-') else (tokens[i - 2] if i >= 2 else '')
                if re.match(r'^' + DIGITISH + r'+(?:st|nd|rd|th|d)?$', prev or ''):
                    dg = digitize(re.sub(r'(st|nd|rd|th|d)$', '', prev))
                    if dg.isdigit() and 1 <= int(dg) <= 31:
                        d = int(dg)
    if y is None:
        for t in tokens:
            if re.match(r'^' + DIGITISH + r'{4}$', t):
                dg = digitize(t)
                if dg.isdigit() and 1800 <= int(dg) <= 1899:
                    y = int(dg)
                    break
        if y is None:
            mm = re.search(r'\b[1iIl±*!]\s?8\s?' + DIGITISH + r'\s?' + DIGITISH + r'\b', s)
            if mm:
                dg = digitize(mm.group(0).replace(' ', ''))
                if dg.isdigit() and 1800 <= int(dg) <= 1899:
                    y = int(dg)
    if y is not None and year_range and not (year_range[0] <= y <= year_range[1]):
        y = None
    return y, m, d


def is_running_head(line):
    s = line.strip()
    if not s or len(s) > 60 or re.search(r'[a-z]', s):
        return False
    letters = re.sub(r'[^A-Z]', '', s)
    if not letters:
        return False
    has_year = re.search(r'(?:1|I|l|±|\*|!|i)\s?8\s?' + DIGITISH + r'\s?' + DIGITISH, s) is not None
    m = fuzzy_month(letters[:12]) or fuzzy_month(re.split(r'\s{2,}', s)[0])
    if has_year and (m or len(letters) <= 14):
        return True
    if m and re.search(r'\d', s):
        return True
    if s in ('APPENDIX I', 'APPENDIX II', 'ADDITIONS') or re.match(r'^APPENDIX\s+I+$', s):
        return True
    return False


def looks_like_heading(line, nxt, in_dateline_zone=False):
    """Return (is_heading, has_marker)."""
    s = norm_ws(line)
    if not s or len(s) > 80:
        return False, False
    w = s.split()
    if len(w) > 14:
        return False, False
    first = re.sub(r'[^A-Za-z]', '', w[0])
    if first not in HEAD_WORDS or not w[0][0].isupper():
        return False, False
    if re.search(r'[:;,?]\s*$', s):
        return False, False
    if YEARISH_RE.search(s) or re.search(r'\bMansion\b', s):
        return False, False
    has_marker = HEAD_END_RE.search(s) is not None or (HEAD_END_SP_RE.search(s) is not None and title_case(s))
    if has_marker and re.search(r'\b[A-Z]\.\s*$', s):
        has_marker = False
    if has_marker:
        if re.search(r'\s[lixI]\s*$', s):
            return False, False
        if not (len(w) == 1 or title_case(s) or TO_NAME_RE.match(s)):
            return False, False
        if DATELINE_WORDS.search(s) and not TO_NAME_RE.match(s) and not title_case(s):
            return False, False
        if is_signature_line(re.sub(r'[*^!]', '', s)):
            return False, False
        return True, True
    if re.search(r'\.\s*$', s):
        return False, False
    # two-line heading: this line has no marker, the continuation line is short and carries it
    n2 = norm_ws(nxt)
    if n2 and len(n2) <= 62 and n2[:1].isupper() and HEAD_END_RE.search(n2) and not YEARISH_RE.search(n2) \
            and not re.search(r'[:;,]\s*$', n2) and not is_signature_line(re.sub(r'[*^!]', '', n2)) and (len(w) == 1 or title_case(s)) \
            and not re.search(r'\bMansion\b|\bDepartment\b', s):
        return True, False
    # no marker: require title case, shortness, no dateline vocabulary, not in the dateline zone of the previous item
    if in_dateline_zone:
        return False, False
    if DATELINE_WORDS.search(s) or PLACE_CUES.search(s):
        return False, False
    if s.startswith('To ') and not TO_NAME_RE.match(s):
        return False, False
    if len(s) <= 62 and title_case(s):
        return True, False
    return False, False


SMALL = {'of', 'the', 'and', 'for', 'to', 'at', 'in', 'on', 'a', 'an', 'by', 'with', 'from', 'or', 'concerning', 'as', 'against',
         'upon', 'into', 'et', 'al', 'v', 'vs', 'de', 'la', 'about', 'before', 'after', 'under', 'over', 'is'}


def title_case(s):
    words = [re.sub(r'[^A-Za-z]', '', x) for x in s.split()]
    words = [x for x in words if x]
    if len(words) < 2:
        return False
    big = [x for x in words[1:] if x.lower() not in SMALL]
    if not big:
        return True
    caps = sum(1 for x in big if x[0].isupper())
    return caps / len(big) >= 0.75


FN_TOL_RE = re.compile(r'^\s*[^A-Za-z0-9(]{0,5}\s*(?:\(1\)|1\.|[' + re.escape(MARKER_CHARS) + r']{1,2})?\s*([A-Za-z]{1,12})(?=[^A-Za-z]|$)')
FN_PRINT_RE = re.compile(r'^\s*(?:\(1\)|1\.|[1lIi*!x^¹»~]{1,2})\s*([A-Z][A-Za-z.\'-]*)')
CITATION_CUES = re.compile(r'\bp{1,2}\.\s*\d|\b(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\s*,\s*\d|\bNo\.\s*\d|\bvol\b|\bVol\b|\b1[89]\d\d\b|\bn\.d\.|\bibid|\bSold\b|\bsold\b|\bPhotograph|\bSpringfield\b|\bPeoria|\bQuincy|\bAlton|\bBloomington|\bGalena|\bBelleville|\bOttawa|\bDanville|\bJacksonville|\bPekin|\bBeardstown|\bColumbus|\bCleveland|\bDetroit|\bLouisville|\bIndianapolis|\bPittsburgh|\bAlbany|\bHartford|\bProvidence|\bBaltimore|\bWilmington|\bSt\.\s*Louis|\bMissouri|\bOhio|\bIndiana|\bKentucky|\bPennsylvania|\bMassachusetts|\bVermont|\bMaine|\bConnecticut|\bWisconsin|\bIowa|\bMichigan|\bNH\b|\bAGO\b|\bRG\s*\d')
STRONG_SIGILS = ('DLC DNA IHi ICHi ORB ISLA NHi CSmH RPB MHi PHi CtY NjP InU ICU OFH OCHP WHi MoSHi NcD ViU DLM NBuHi NRU NIC MWA MdHi '
                 'OClWHi THaroL NAuE InFtwL IJI ICN NNP CLU CSt NhHi NjMoHP MeHi WvU NNC NcU TxU IaDaM OHi CCamarSJ InHi IaHA MnHi NNPM PPRF '
                 'PHC PSC OCU OrU RHi ViHi NbO KyLoF DNM DGU DAU NjR NhD OMC IaU KHi MoHi MdAN NIHi CtHi CLSU MiU-C DLC-RTL DLC-Nicolay').split()
STRONG_SIGIL_RE = re.compile(r'(?<![A-Za-z])(' + '|'.join(sorted(map(re.escape, STRONG_SIGILS), key=len, reverse=True)) + r')(?![A-Za-z])')


def footnote_start(line):
    """Return (kind, code_token) if the line starts a footnote block, else (None, None).
    kind: 'strict' (marker + manuscript code) | 'printed' (marker + printed-source cue) | 'bare' (code/sigil, marker lost)."""
    s = line.rstrip()
    m = FN_TOL_RE.match(s)
    if m:
        tok = m.group(1)
        tokn = CODE_FIX.get(tok, tok)
        if tokn in CODES:
            # the code must be followed by a delimiter/space (e.g. "ALS, DLC-RTL"), not be a word like "Copy of"
            after = s[m.end():m.end() + 3]
            if tokn in ('Copy', 'Copies', 'Text', 'Printed', 'Recorded', 'Ms', 'MS') and not re.match(r'^\s*[,;:\-]', after) and not re.match(r'^\s*(owned|in|of|by|from|made|furnished|supplied|sent|signed|enclosed)', after):
                pass
            else:
                return 'strict', tokn
    m2 = FN_PRINT_RE.match(s)
    if m2 and (STRONG_SIGIL_RE.search(s) or PRINTED_CUES.search(s) or CITATION_CUES.search(s)):
        return 'printed', m2.group(1)
    # bare code/sigil at line start followed by comma/period (marker lost)
    m3 = re.match(r'^\s*\(?(ALS|ADfS|ADf|ADS|AD|AES|AE|AL|LS|DS|DfS|Df|ES|Copy|copy)\??\)?\b\s*[-,.;]', s)
    if m3:
        return 'bare', CODE_FIX.get(m3.group(1), m3.group(1)) if m3.group(1) != 'copy' else 'Copy'
    m4 = re.match(r'^\s*(' + '|'.join(map(re.escape, STRONG_SIGILS)) + r')\b\s*[,.;-]', s)
    if m4:
        return 'bare', m4.group(1)
    # sigil very early in the line (first 40 chars) with a garbled marker/code before it
    m5 = STRONG_SIGIL_RE.search(s[:40])
    if m5 and not re.match(r'^\s*[a-z]', s) and len(s[:m5.start()].split()) <= 3:
        return 'bare', None
    return None, None


def line_ends_with_signature(s):
    t = norm_ws(s)
    if is_signature_line(t):
        return True
    if re.search(r'(?:A[.,]?\s*L[iIl1]NC[O0]LN|A[BR]RAHAM\s+L[iIl1]NC[O0]LN|\bA[.,]\s*L[.,]?|\bA\.\s*L\.)[.,]?\s*$', t):
        return True
    if re.search(r'(?:' + CLOSING_RE.pattern[:-4] + r')\W*\s+A[.,*]?\s*$', t, re.I):
        return True
    if re.search(r'1[89]\d\d[.,]?\s+A[.,*]?\s*$', t):
        return True
    return False


def is_signature_line(s):
    t = norm_ws(s)
    if not t:
        return False
    if re.fullmatch(r'(?:By the President[:.]?\s*)?A[.,]?\s*L[iIl1]NC[O0]LN[.,]?', t) or re.fullmatch(r'A[.,]?\s*L[.,]?', t):
        return True
    if re.fullmatch(r'A[BR]RAHAM\s+L[iIl1]NC[O0]LN[.,]?', t) or re.fullmatch(r'L[iIl1]NC[O0]LN[.,]?', t) or re.fullmatch(r'A[.,*]?', t):
        return True
    if re.fullmatch(r'A\.?\s*L[.,]?\s*$', t):
        return True
    # fuzzy: short all-caps-ish line resembling A LINCOLN
    letters = re.sub(r'[^A-Za-z]', '', t).upper()
    if 4 <= len(letters) <= 12 and t.count(' ') <= 3 and difflib.SequenceMatcher(None, letters, 'ALINCOLN').ratio() >= 0.7 and t.upper() == t:
        return True
    return False


def strip_trailing_signature(text):
    """Remove a trailing signature from the last prose line."""
    t = text.rstrip()
    pats = [r'(?:By\s+the\s+President[:.]?\s*)?A[BR]RAHAM\s+L[iIl1]NC[O0]LN[.,]?\s*$',
            r'\bA[.,]?\s*L[iIl1]NC[O0]LN[.,]?\s*$', r'\bA[.,]\s*L[.,]?\s*$', r'\bA\.\s*L\.\s*$']
    for p in pats:
        m = re.search(p, t)
        if m:
            return t[:m.start()].rstrip()
    # bare "A." / "A" after a closing formula or a date
    m = re.search(r'(?:' + CLOSING_RE.pattern[:-4] + r')\W*\s+A[.,*]?\s*$', t, re.I)
    if m:
        m2 = re.search(r'\s+A[.,*]?\s*$', t)
        return t[:m2.start()].rstrip()
    m = re.search(r'(1[89]\d\d[.,]?)\s+A[.,*]?\s*$', t)
    if m:
        return t[:m.end(1)].rstrip()
    # fuzzy caps signature at end e.g. "A.  Lmcoi^sr" / "A LINGO UNT"
    toks = t.split()
    for n in (3, 2):
        if len(toks) >= n:
            tail = ' '.join(toks[-n:])
            letters = re.sub(r'[^A-Za-z]', '', tail).upper()
            if 5 <= len(letters) <= 12 and difflib.SequenceMatcher(None, letters, 'ALINCOLN').ratio() >= 0.65 and re.match(r'^A[.,]?$', toks[-n]):
                return ' '.join(toks[:-n]).rstrip()
    return t


VERBISH = re.compile(r"\b(please|let|furnish|may|have|has|see|hear|report|read|return|submitted|accepted|approved|referred|granted|denied|"
                     r"declined|done|examined|considered|received|allowed|disallowed|answered|suspended|commuted|pardoned|discharged|released|"
                     r"appointed|recommended|respectfully|will|is|are|be|was|were|not|this|these|oblige|send|sent|give|given|make|made|do|did|"
                     r"take|taken|wish|want|think|know|say|said|shall|should|would|could|can|must|come|go|allow|ask|asks|asked|desire|desires|"
                     r"present|presents|presented|carry|attend|write|wrote|call|called|meet|leave|hold|keep|put|bring|brought|thank|thanks|"
                     r"telegraph|telegraphed|order|ordered|direct|directed|authorize|authorized|permit|permitted|deliver|delivered|pay|paid|"
                     r"pass|passed|admit|admitted|examine|inquire|look|find|found|tell|told|it|him|her|them|me|you|we|they|my|your|our|their)\b", re.I)


def is_header_line(s, idx):
    """Dateline / inside-address / salutation line at the start of an item body."""
    t = norm_ws(s)
    if not t:
        return False
    words = t.split()
    if len(words) > 13:
        return False
    if VERBISH.search(t) and not (parse_date_string(t)[0] and parse_date_string(t)[1] and len(words) <= 6):
        # a line with a verb/pronoun is text, not an address block (unless it is only a short dateline)
        if not (re.match(r'^\[', t) and re.search(r'\]$', t)):
            return False
    y, m, d = parse_date_string(t)
    has_full_date = (y is not None and m is not None)
    if has_full_date:
        return True
    if re.search(r'^\[?c?\.?\s*[A-Z][a-z]+\.?\s+' + DIGITISH + r'{1,2}', t) and y is not None:
        return True
    if BRACKET_DATE_RE.search(t) or re.match(r'^\[[^\]]*\]$', t):
        return True
    if PLACE_CUES.search(t) and len(words) <= 9:
        return True
    if HEADER_CUES.match(t) and len(words) <= 9 and not re.search(r'[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}', t):
        return True
    if len(words) <= 9 and re.search(r'[:,]\s*$', t) and idx <= 3 and not re.search(r'[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}', t):
        return True
    if t.upper() == t and len(words) <= 8:
        return True
    return False


def is_trailer_line(s):
    """Lines after the signature: addressee, date, attestation."""
    t = norm_ws(s)
    if not t:
        return False
    words = t.split()
    if len(words) > 12:
        return False
    if is_signature_line(t):
        return True
    if VERBISH.search(t) and not re.search(r'(?:A[.,]?\s*L[iIl1]NC[O0]LN|A[BR]RAHAM\s+L[iIl1]NC[O0]LN|\bA[.,]\s*L[.,]?|\bA\.)\s*$', t):
        return False
    if re.search(r'Secretary\s+of\s+(State|War|the\s+Navy|the\s+Treasury|the\s+Interior)', t) and len(words) <= 9:
        return True
    if re.match(r'^(By\s+the\s+President|\[?L\.?\s*S\.?\]?|EX-|\[SEAL\]|SEAL)', t):
        return True
    y, m, d = parse_date_string(t)
    if y is not None and m is not None and len(words) <= 8:
        return True
    if HEADER_CUES.match(t) and len(words) <= 9 and re.search(r'[.,:]\s*$', t) and not re.search(r'[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}', t):
        return True
    if re.match(r'^(Hon|Mrs|Mr|Maj|Gen|Col|Capt|Dr|Rev|Lieut|Messrs|His Excellency|Governor|Gov|Miss|Judge|Commodore|Admiral)\b', t) and len(words) <= 9:
        return True
    return False


BRACKET_COMMENT = re.compile(r'\[(?:sic|\?|illegible|torn|blank|erased|deleted|missing|indecipherable|in ink|in pencil|written in|'
                             r'endorsement|indorsement|enclosure|inclosure|marginal note|note|and|etc\.?|see|not in|in Lincoln|in another|'
                             r'in the hand|signature|unsigned|undated|no date|footnote|copy|draft|fragment|remainder|page|remains|words|'
                             r'word|line|lines|space|blank space|left blank|manuscript|MS|paper|torn|mutilated|partly|part|illegibly)[^\]]*\]', re.I)


def clean_brackets(t):
    t = BRACKET_COMMENT.sub('', t)

    def repl(m):
        inner = m.group(1).strip()
        if len(inner.split()) <= 2 and not re.search(r'\d{4}', inner):
            return inner
        return ''
    t = re.sub(r'\[([^\]]*)\]', repl, t)
    return t


def rejoin_lines(lines):
    """Join OCR lines into paragraphs; de-hyphenate line-end breaks."""
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
                if last and last.group(1).lower() in ('re', 'co', 'pre', 'self', 'well', 'ex', 'non', 'anti', 'semi', 'half', 'pro', 'un', 'sub', 'vice', 'so', 'to', 'by', 'law', 'in', 'brother', 'sister', 'father', 'mother', 'son', 'grand', 'step', 'great', 'ill', 'all'):
                    txt = txt + s
                else:
                    txt = stem + s
            else:
                txt = (txt + ' ' + s) if txt else s
        out.append(txt)
    return '\n'.join(out)


HAY_HAND_RE = re.compile(r"(?:John\s+)?Hay's\s+(?:hand\b|autograph|handwriting)|in\s+(?:the\s+)?hand(?:writing)?\s+of\s+(?:John\s+)?Hay\b|"
                         r"written\s+by\s+(?:John\s+)?Hay\b|in\s+Hay's\s+hand|autograph\s+of\s+(?:John\s+)?Hay\b|Hay's\s+autograph|"
                         r"(?:John\s+)?Hay\s+wrote\s+(?:this|the)\s+(?:note|telegram|letter|draft|order|document|endorsement|memorandum|dispatch|despatch|copy|body|text|reply|message)", re.I)
OTHER_HAND_RE = re.compile(r"(?:in\s+(?:the\s+)?(?:hand|handwriting|autograph)\s+of\s+(?!Lincoln)(?:an?\s+)?[A-Z][\w.]*(?:\s+[A-Z][\w.]*){0,3}|"
                           r"(?<!Lincoln)(?<!Lincoln')\b(?!Lincoln)[A-Z][\w.]*(?:\s+[A-Z][\w.]*){0,2}'s\s+(?:hand\b|handwriting|autograph)|"
                           r"not\s+in\s+Lincoln's\s+(?:hand|handwriting|autograph)|in\s+an?\s+(?:unidentified|clerk's|clerical|secretary's|different|unknown)\s+hand(?:writing)?|"
                           r"written\s+by\s+(?:John\s+G\.\s+)?Nicolay|Nicolay's\s+(?:hand|handwriting|autograph))", re.I)


def relaxed_heading(keep, j):
    """Second-chance heading test used only between two footnote blocks of one region."""
    s = norm_ws(keep[j][1])
    if not s or len(s) < 4 or len(s) > 62 or not s[0].isupper():
        return False
    if is_signature_line(s) or is_signature_line(re.sub(r'[*^]', '', s)):
        return False
    if j > 0 and keep[j - 1][1].strip() != '':
        return False
    if re.search(r'[.:;,?]\s*$', s) and not HEAD_END_RE.search(s):
        return False
    if YEARISH_RE.search(s) or DATELINE_WORDS.search(s) or re.search(r'[a-z]{3,}\s+[a-z]{3,}\s+[a-z]{3,}', s):
        return False
    if HEAD_END_RE.search(s) and (title_case(s) or TO_NAME_RE.match(s)):
        return True
    if s.startswith('To ') and TO_NAME_RE.match(s):
        return True
    w = s.split()
    if len(w) >= 2 and title_case(s) and re.sub(r'[^A-Za-z]', '', w[0]) in HEAD_WORDS:
        for jj in range(j + 1, min(j + 6, len(keep))):
            t = keep[jj][1].strip()
            if t and is_header_line(t, 0):
                return True
    return False


def genre_of(heading, code, fn_first):
    h = heading.lower()
    fn = (fn_first or '').lower()
    if code in ('AES', 'AE', 'ES') or h.startswith('endorsement') or h.startswith('indorsement'):
        return 'endorsement'
    if re.match(r'^to the (senate|house)', h):
        return 'message'
    if h.startswith('to '):
        if re.search(r'telegram|telegraph|cypher|cipher', fn) or re.search(r'presidential telegrams', fn):
            return 'telegram'
        return 'letter'
    if re.match(r'^(speech|address|remarks|response|reply|toast|eulogy|lecture|debate|farewell|inaugural|last public|gettysburg|second inaugural|first inaugural|temperance)', h):
        return 'speech'
    if re.match(r'^(proclamation|emancipation proclamation)', h):
        return 'proclamation'
    if re.search(r'^(annual message|message|communication to|special message)', h):
        return 'message'
    if re.match(r'^(memorandum|memoranda|note[s]? (on|for|of|concerning)|notes)', h):
        return 'memorandum'
    if re.match(r'^(order|orders|executive order|general order|special order|pass|passes|pardon|discharge|commission|appointment|instructions|call for|authorization|permit|direction)', h):
        return 'order'
    return 'other'


def parse_volume(vol, ident, start_line, year_range):
    path = os.path.join(IA, ident + '.txt')
    raw = open(path, encoding='utf-8', errors='replace').read().split('\n')
    # ---- determine parse ranges (main run; vol VIII: appendix I and additions; exclude appendix II list) ----
    n = len(raw)
    ranges = []
    if vol == 'VIII':
        app1 = next(i for i, l in enumerate(raw) if re.match(r'^\s*APPENDIX\s+I\s*$', l))
        app2 = next(i for i, l in enumerate(raw) if re.match(r'^\s*APPENDIX\s+II\s*$', l))
        adds = next(i for i, l in enumerate(raw) if re.match(r'^\s*ADDITIONS\s*$', l) and i > app2)
        colophon = next(i for i, l in enumerate(raw) if 'THE  COLLECTED  WORKS' in l and i > adds)
        ranges = [(start_line - 1, app1, 'main'), (app1, app2, 'appendix_1'), (adds, colophon, 'additions')]
    else:
        colophon = next((i for i, l in enumerate(raw) if re.search(r'THE\s+COLLECTED\s+WO[RE]KS|COMPOSED\s+IN\s+INTERTYP', l) and i > n - 60), n)
        ranges = [(start_line - 1, colophon, 'main')]

    items = []
    for (a, b, section) in ranges:
        # ---- pass 1: page markers + running heads ----
        page_at = {}   # line index -> page number for lines
        cur_page = None
        keep = []      # (line_idx, text)
        i = a
        last_page = None
        while i < b:
            l = raw[i]
            pm = PAGE_RE.match(l)
            if pm and len(norm_ws(l)) <= 7:
                pg = int(pm.group(1) or pm.group(2))
                if last_page is not None and not (last_page < pg <= last_page + 12):
                    pg = last_page + 1
                last_page = pg
                cur_page = pg + 1
                # skip running head(s): first non-empty line(s) after the marker
                j = i + 1
                seen = 0
                while j < b and seen < 2:
                    if raw[j].strip() == '':
                        j += 1
                        continue
                    if is_running_head(raw[j]):
                        j += 1
                        seen += 1
                        continue
                    break
                i = j
                continue
            if cur_page is None:
                # before the first marker: page = first marker - ... approximate later
                pass
            keep.append((i, l, cur_page))
            i += 1
        # fill pages before the first marker
        first_pg = next((p for (_, _, p) in keep if p is not None), None)
        keep = [(ix, l, (p if p is not None else (first_pg - 1 if first_pg else None))) for (ix, l, p) in keep]

        # ---- pass 2: heading detection ----
        heads = []  # indices into keep
        k = 0
        last_head_end = -100
        while k < len(keep):
            ix, l, pg = keep[k]
            nxt = ''
            for kk in range(k + 1, min(k + 3, len(keep))):
                if keep[kk][1].strip():
                    nxt = keep[kk][1]
                    break
            ok, marker = looks_like_heading(l, nxt, in_dateline_zone=(k - last_head_end) <= 6)
            if ok:
                # two-line heading: no marker on this line, next non-empty line short & ends with marker
                span = 1
                if not marker:
                    kk = k + 1
                    while kk < len(keep) and keep[kk][1].strip() == '':
                        kk += 1
                    if kk < len(keep):
                        s2 = norm_ws(keep[kk][1])
                        if len(s2) <= 60 and s2[:1].isupper() and HEAD_END_RE.search(s2) and not re.search(r'[:;,]\s*$', s2) and kk - k <= 2:
                            span = kk - k + 1
                            marker = True
                # a heading must be preceded by a blank line (or be at the region start)
                prev_blank = (k == 0) or keep[k - 1][1].strip() == ''
                if prev_blank or marker:
                    heads.append((k, span, marker, ''))
                    last_head_end = k + span - 1
                    k += span
                    continue
            k += 1
        # ---- pass 2b: recover missed headings where one region holds two strict footnote blocks ----
        extra = []
        for hi, (k, span, marker, _) in enumerate(heads):
            end = heads[hi + 1][0] if hi + 1 < len(heads) else len(keep)
            strict_pos = [j for j in range(k + span, end) if footnote_start(keep[j][1])[0] == 'strict']
            for a_, b_ in zip(strict_pos, strict_pos[1:]):
                found = None
                for j in range(b_ - 1, a_, -1):
                    if relaxed_heading(keep, j):
                        found = j
                        break
                if found is not None:
                    extra.append((found, 1, False, 'heading_relaxed'))
        if extra:
            heads = sorted(heads + extra)
        # ---- pass 3: build items ----
        for hi, (k, span, marker, hflag) in enumerate(heads):
            end = heads[hi + 1][0] if hi + 1 < len(heads) else len(keep)
            heading = norm_ws(' '.join(keep[k + s][1] for s in range(span)))
            heading_clean = re.sub(r'\s*[' + re.escape(MARKER_CHARS) + r']{1,2}\s*$', '', heading)
            heading_clean = re.sub(r'([A-Za-z])[1l*!x^]$', r'\1', heading_clean)
            body_lines = keep[k + span:end]
            # locate footnote start
            fn_idx = None
            fn_kind = None
            code_tok = None
            cands = []
            for j, (ix, l, pg) in enumerate(body_lines):
                kind, tok = footnote_start(l)
                if kind:
                    cands.append((j, kind, tok))
            strict = [c for c in cands if c[1] == 'strict']
            if strict:
                fn_idx, fn_kind, code_tok = strict[0]
            elif cands:
                fn_idx, fn_kind, code_tok = cands[0]
            flags = [hflag] if hflag else []
            if fn_idx is None:
                # fall back: the block after the first signature line is the (marker-less) footnote
                sig = [j for j, (ix, l, pg) in enumerate(body_lines) if line_ends_with_signature(l)]
                if sig and sig[0] + 1 < len(body_lines):
                    fn_idx = sig[0] + 1
                    while fn_idx < len(body_lines) and (body_lines[fn_idx][1].strip() == '' or is_trailer_line(body_lines[fn_idx][1])):
                        fn_idx += 1
                    fn_kind = 'after_signature'
                    flags.append('footnote_by_signature')
                else:
                    fn_idx = len(body_lines)
                    flags.append('no_footnote_found')
            if len(strict) > 1:
                flags.append('multiple_strict_footnotes:%d' % len(strict))
            text_lines = body_lines[:fn_idx]
            fn_lines = body_lines[fn_idx:]
            fn_text = norm_ws(' '.join(l for (_, l, _) in fn_lines[:6]))[:300]
            note_lines = []
            for (_, l, _) in fn_lines:
                if note_lines and re.match(r'^\s*(?:[2-9]|aa|a|s|8|3|z)\s+[A-Z"]', l) and len(norm_ws(l)) > 12:
                    break
                note_lines.append(l)
            source_note = rejoin_lines(note_lines)[:3000]
            hay_hand = HAY_HAND_RE.search(source_note) is not None
            oh = OTHER_HAND_RE.search(source_note)
            other_hand = norm_ws(oh.group(0)) if oh else None
            # source code
            code = None
            if fn_kind == 'strict':
                code = CODE_FIX.get(code_tok, code_tok)
            elif fn_kind == 'bare' and code_tok in CODES:
                code = code_tok
            source_type = 'manuscript' if code in ('ALS', 'ADfS', 'ADf', 'ADS', 'AD', 'AES', 'AE', 'AL', 'LS', 'DS', 'DfS', 'Df', 'ES') else \
                ('copy' if code in ('Copy', 'Copies', 'Photostat', 'Facsimile') else ('printed' if fn_idx is not None and fn_kind else 'unknown'))
            autograph = bool(code and code in AUTOGRAPH) and not hay_hand
            # ---- strip header lines ----
            tl = [norm_ws(l) for (_, l, _) in text_lines]
            # drop empties at start
            header, rest = [], list(tl)
            idx = 0
            while rest and (rest[0] == '' or (idx < 8 and is_header_line(rest[0], idx))):
                if rest[0] != '':
                    header.append(rest[0])
                    idx += 1
                rest.pop(0)
            # ---- strip trailer lines ----
            trailer = []
            while rest and (rest[-1] == '' or is_trailer_line(rest[-1])):
                if rest[-1] != '':
                    trailer.insert(0, rest[-1])
                rest.pop()
            text = rejoin_lines(rest)
            text = strip_trailing_signature(text)
            text = clean_brackets(text)
            text = re.sub(r'[ \t]+', ' ', text)
            text = re.sub(r' \n', '\n', text).strip()
            # dates
            date_src = None
            y = m = d = None
            for cand in header + [heading] + trailer:
                yy, mm, dd = parse_date_string(cand, year_range if section == 'main' else None)
                if yy is None and mm is None:
                    continue
                if (yy and mm) or (y is None and m is None) or (yy and y is None) or (mm and m is None):
                    y = yy if yy else y
                    m = mm if mm else m
                    d = dd if dd else d
                    date_src = 'dateline'
                    if yy and mm:
                        break
            page = keep[k][2]
            items.append(dict(
                id='%s-%s-%04d' % ('basler', vol, len(items) + 1),
                volume=vol, section=section, page=page, line=keep[k][0] + 1,
                heading=heading_clean, y=y, m=m, d=d, date_source=date_src,
                header=' | '.join(header), trailer=' | '.join(trailer),
                heading_marker=bool(marker),
                source_code=code, source_kind=fn_kind, source_type=source_type, autograph=autograph,
                hay_hand=hay_hand, other_hand=other_hand, source_note=source_note,
                footnote_head=fn_text, text=text, word_count=len(text.split()), flags=flags))
    return items, raw


def finalize(items, vol, year_range):
    """Carry dates forward within the chronological main run; build ISO date; genre; addressee."""
    prev_y = None
    prev_m = None
    for it in items:
        if it['section'] == 'main':
            if it['y'] is None:
                it['y'] = prev_y
                it['date_source'] = 'carried' if prev_y else None
                it['m'] = it['m'] if it['y'] else None
            else:
                if not (year_range[0] <= it['y'] <= year_range[1]):
                    it['flags'].append('year_ocr_rejected:%d' % it['y'])
                    it['y'] = prev_y
                    it['date_source'] = 'carried' if prev_y else None
                elif prev_y and it['y'] < prev_y - 1:
                    it['flags'].append('date_out_of_sequence')
                    it['y'] = prev_y
                    it['date_source'] = 'carried'
            if it['y']:
                prev_y = it['y']
        y, m, d = it['y'], it['m'], it['d']
        if y and m and d:
            it['date'] = '%04d-%02d-%02d' % (y, m, d)
        elif y and m:
            it['date'] = '%04d-%02d' % (y, m)
        elif y:
            it['date'] = '%04d' % y
        else:
            it['date'] = None
        it['year'] = y
        h = it['heading']
        it['addressee'] = re.sub(r'^To\s+', '', h).strip() if h.startswith('To ') else None
        it['genre'] = genre_of(h, it['source_code'], it['footnote_head'])
        for kk in ('y', 'm', 'd'):
            it.pop(kk)
    return items


def main():
    os.makedirs(OUT, exist_ok=True)
    all_items = []
    stats = collections.OrderedDict()
    for vol, ident, start, yr in VOLUMES:
        items, raw = parse_volume(vol, ident, start, yr)
        items = finalize(items, vol, yr)
        all_items.extend(items)
        stats[vol] = dict(items=len(items), words=sum(i['word_count'] for i in items),
                          no_fn=sum('no_footnote_found' in i['flags'] for i in items),
                          multi_fn=sum(any(f.startswith('multiple') for f in i['flags']) for i in items),
                          no_date=sum(i['date'] is None for i in items),
                          autograph=sum(i['autograph'] for i in items))
    with open(os.path.join(OUT, 'lincoln_basler.jsonl'), 'w', encoding='utf-8') as f:
        for it in all_items:
            f.write(json.dumps(it, ensure_ascii=False) + '\n')
    with open(os.path.join(OUT, 'lincoln_basler_index.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'volume', 'section', 'page', 'date', 'year', 'heading', 'addressee', 'genre', 'source_code', 'autograph', 'hay_hand', 'other_hand', 'word_count', 'flags'])
        for it in all_items:
            w.writerow([it['id'], it['volume'], it['section'], it['page'], it['date'], it['year'], it['heading'], it['addressee'], it['genre'],
                        it['source_code'], it['autograph'], it['hay_hand'], it['other_hand'], it['word_count'], ';'.join(it['flags'])])
    print(json.dumps(stats, indent=1))
    print('TOTAL items', len(all_items), 'words', sum(i['word_count'] for i in all_items))
    # report
    by = collections.Counter(i['genre'] for i in all_items)
    print('by genre', dict(by))
    print('autograph', collections.Counter(i['autograph'] for i in all_items))
    print('source codes', collections.Counter(i['source_code'] for i in all_items).most_common(25))
    val = [i for i in all_items if i['autograph'] and i['year'] and 1861 <= i['year'] <= 1865 and 100 <= i['word_count'] <= 300]
    print('validation set (autograph, 1861-65, 100-300 words):', len(val))
    print('hay_hand items:', sum(i['hay_hand'] for i in all_items), 'other_hand items:', sum(1 for i in all_items if i['other_hand']))
    print('flags:', collections.Counter(f.split(':')[0] for i in all_items for f in i['flags']))
    print('date_source:', collections.Counter(i['date_source'] for i in all_items))
    print('heading without marker:', sum(1 for i in all_items if not i['heading_marker']))
    wc = [i['word_count'] for i in all_items]
    print('word count quantiles', sorted(wc)[len(wc) // 10], sorted(wc)[len(wc) // 2], sorted(wc)[9 * len(wc) // 10], 'zero-length', sum(1 for x in wc if x == 0))
    bix = [i for i in all_items if 'Bixby' in i['heading']]
    if bix:
        open(os.path.join(OUT, 'bixby_letter_basler.txt'), 'w').write(bix[0]['text'] + '\n')
        print('BIXBY:', json.dumps(bix[0], indent=1)[:1500])


if __name__ == '__main__':
    main()
