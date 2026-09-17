"""Corpus designs for the experiments. Each design returns candidates and test sets."""
import os, json, re, datetime
import corpus
from ngt import word_count

HERE = os.path.dirname(os.path.abspath(__file__))
SPECIALS = json.load(open(os.path.join(HERE, 'specials.json')))
CUT = datetime.date(1860, 5, 18)

def _date(r):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', str(r.get('date') or ''))
    if m:
        try: return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError: pass
    y = r.get('year') or (str(r.get('date') or '')[:4] or None)
    try: return datetime.date(int(y), 7, 1) if y else None
    except (ValueError, TypeError): return None

def load_lincoln():
    recs = corpus.load('lincoln_basler.jsonl', 'lincoln')
    for r in recs:
        d = _date(r)
        if r['volume'] == 'VIII' and d and d.year == 1867:   # OCR '186/5' misread
            d = d.replace(year=1865)
        if r['volume'] == 'VII' and d and d.year not in (1863, 1864): d = None
        if r['volume'] == 'VIII' and d and d.year not in (1864, 1865): d = None
        r['_date'] = d
        AUTO = ('ALS', 'ADS', 'ADfS', 'ADf', 'AD', 'AES', 'AE', 'AL', 'AN', 'ANS', 'AILS')
        sc = (r.get('source_code') or '').split()[0] if r.get('source_code') else ''
        hh = bool(r.get('hay_hand', False))
        r['hay_hand'] = hh and sc not in AUTO          # strict: only when no Lincoln autograph survives
        r['autograph'] = bool(r.get('autograph')) or (sc in AUTO and not r['hay_hand'])
    return recs

RUNHEAD = re.compile(r'\s*\b[A-Za-z0-9]{0,4}\s*LETTERS O[FP] JOHN HAY\s*[A-Za-z0-9]{0,4}\b\s*')

def clean_hay_text(t):
    t = RUNHEAD.sub(' ', t)
    t = re.sub(r'\s*\bDIARY\.?\s*$', '', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

def load_hay():
    if not os.path.exists(os.path.join(corpus.ROOT, 'hay.jsonl')): return []
    recs = corpus.load('hay.jsonl', 'hay')
    out = []
    for r in recs:
        r['text'] = clean_hay_text(r['text'])
        r['wc'] = word_count(r['text'])
        r['_date'] = _date(r)
        if not r.get('period'):
            r['period'] = 'post_war'   # undated Addresses and letters are all post-war
        if r['wc'] >= 5: out.append(r)
    return out

def load_controls():
    if not os.path.exists(os.path.join(corpus.ROOT, 'controls.jsonl')): return []
    return corpus.load('controls.jsonl')

def strip_punct_text(t):
    t = re.sub(r"[^A-Za-z0-9'\s]+", ' ', t)
    return re.sub(r'[ \t]+', ' ', t)

def pairs(recs, sp=False):
    return [(r['id'], strip_punct_text(r['text']) if sp else r['text']) for r in recs]

def specials(sp=False):
    return [(k, strip_punct_text(v['text']) if sp else v['text'], v['author']) for k, v in SPECIALS.items()]

def short(recs, lo=50, hi=400):
    return [r for r in recs if lo <= r['wc'] <= hi]

def lincoln_pre1860(L):
    return [r for r in L if r['_date'] and r['_date'] < CUT and r['wc'] >= 5]

def lapsley_gap(lo=datetime.date(1849, 1, 1), hi=CUT):
    """Clean Gutenberg (Lapsley) items for the years Basler vols II-III would cover
    (1849 to 17 May 1860), used to fill the gap in the Grieve-design Lincoln pool."""
    path = os.path.join(HERE, 'lapsley.jsonl')
    out = []
    for ln in open(path, encoding='utf-8'):
        r = json.loads(ln); d = _date(r)
        if d and lo <= d < hi and r['nwords'] >= 5:
            out.append({'id': r['id'], 'text': r['text'], 'wc': r['nwords'], '_date': d, 'autograph': None, 'hay_hand': False, 'volume': 'Lapsley'})
    return out

def lincoln_war_own(L):
    return [r for r in L if r['_date'] and r['_date'] >= CUT and r['autograph'] and not r['hay_hand'] and r['wc'] >= 5]

def lincoln_war_other(L):
    return [r for r in L if r['_date'] and r['_date'] >= CUT and not r['autograph'] and not r['hay_hand'] and r['wc'] >= 5]

def lincoln_hay_hand(L):
    return [r for r in L if r['hay_hand'] and r['wc'] >= 5]

def hay_war(H):
    return [r for r in H if (r.get('period') == 'civil_war') or (r['_date'] and 1860 <= r['_date'].year <= 1865)]

def dedupe(cands, sp_items, thresh=0.4):
    """Remove from every candidate pool any text that is a copy or near-copy of a
    special test text (drafts of the Gettysburg Address, the Ellsworth and Gurney
    letters, the Second Inaugural are all in Basler). Records the exclusions."""
    from ngt import char_ngrams
    sp_sets = {k: char_ngrams(t, 8) for k, t, _ in sp_items}
    excluded = {}
    for name, texts in cands.items():
        keep = []
        for i, t in texts:
            g = char_ngrams(t, 8)
            hit = None
            for k, sset in sp_sets.items():
                if len(g) < 100 or len(sset) < 100: continue
                inter = len(g & sset)
                ov = inter / min(len(g), len(sset))  # share of the smaller set: copies and partial copies score high
                if ov > thresh: hit = (k, round(ov, 2)); break
            if hit: excluded[i] = (name,) + hit
            else: keep.append((i, t))
        cands[name] = keep
    return excluded

EXCLUDED = {}

def get(name, strip_punct=False):
    sp = strip_punct
    L = load_lincoln(); H = load_hay()
    if name == 'lincoln_periods':
        pre = lincoln_pre1860(L); war = lincoln_war_own(L)
        cands = {'lincoln_pre1860': pairs(pre, sp), 'lincoln_war_own': pairs(war, sp)}
        tests = {'loo_pre1860': [(r['id'], r['text'], 'lincoln_pre1860') for r in short(pre)],
                 'loo_war_own': [(r['id'], r['text'], 'lincoln_war_own') for r in short(war)],
                 'war_other': [(r['id'], r['text'], None) for r in short(lincoln_war_other(L))],
                 'hay_hand': [(r['id'], r['text'], None) for r in short(lincoln_hay_hand(L), 30, 400)],
                 'specials': specials(sp)}
        if sp:
            for k in tests:
                if k != 'specials': tests[k] = [(i, strip_punct_text(t), a) for i, t, a in tests[k]]
        EXCLUDED.update(dedupe(cands, tests['specials']))
        return {'candidates': cands, 'tests': tests, 'excluded': dict(EXCLUDED)}
    if name == 'grieve':
        # Grieve et al. design: Lincoln before 18 May 1860 vs all Hay; the 1849-1860 gap
        # (Basler vols II-III unavailable) is filled from the Lapsley edition
        pre = lincoln_pre1860(L) + lapsley_gap(); war = lincoln_war_own(L)
        cands = {'lincoln': pairs(pre, sp), 'hay': pairs(H, sp)}
        tests = {'loo_lincoln_pre1860': [(r['id'], r['text'], 'lincoln') for r in short(pre)],
                 'loo_hay': [(r['id'], r['text'], 'hay') for r in short(H)],
                 'lincoln_war_own': [(r['id'], r['text'], 'lincoln') for r in short(war)],
                 'lincoln_war_other': [(r['id'], r['text'], None) for r in short(lincoln_war_other(L))],
                 'hay_hand': [(r['id'], r['text'], None) for r in short(lincoln_hay_hand(L), 30, 400)],
                 'specials': specials(sp)}
    elif name == 'ownhand':
        # Own-hand design: Lincoln autograph texts from 18 May 1860 on vs Hay 1860-1865
        war = lincoln_war_own(L); hw = hay_war(H); pre = lincoln_pre1860(L)
        cands = {'lincoln': pairs(war, sp), 'hay': pairs(hw, sp)}
        tests = {'loo_lincoln_war_own': [(r['id'], r['text'], 'lincoln') for r in short(war)],
                 'loo_hay_war': [(r['id'], r['text'], 'hay') for r in short(hw)],
                 'lincoln_pre1860': [(r['id'], r['text'], 'lincoln') for r in short(pre)],
                 'lincoln_war_other': [(r['id'], r['text'], None) for r in short(lincoln_war_other(L))],
                 'hay_hand': [(r['id'], r['text'], None) for r in short(lincoln_hay_hand(L), 30, 400)],
                 'hay_other': [(r['id'], r['text'], 'hay') for r in short([r for r in H if r not in hw])],
                 'specials': specials(sp)}
    elif name == 'ownhand_all':
        # All Lincoln autograph texts (any date) vs all Hay
        own = [r for r in L if r['autograph'] and not r['hay_hand'] and r['wc'] >= 5]
        cands = {'lincoln': pairs(own, sp), 'hay': pairs(H, sp)}
        tests = {'loo_lincoln_own': [(r['id'], r['text'], 'lincoln') for r in short(own)],
                 'loo_hay': [(r['id'], r['text'], 'hay') for r in short(H)],
                 'lincoln_war_other': [(r['id'], r['text'], None) for r in short(lincoln_war_other(L))],
                 'hay_hand': [(r['id'], r['text'], None) for r in short(lincoln_hay_hand(L), 30, 400)],
                 'specials': specials(sp)}
    else:
        raise ValueError(name)
    # register-matched test set (build_register.py): pieces of known elevated-register
    # texts by both authors; their parent texts are removed from the candidate pools
    reg_path = os.path.join(HERE, 'register.json')
    if os.path.exists(reg_path):
        REG = json.load(open(reg_path))
        tests['register'] = [(k, strip_punct_text(v['text']) if sp else v['text'], v['author']) for k, v in REG.items()]
        parents = {p for v in REG.values() for p in v.get('parents', [])} | {k.split('#')[0] for k in REG}
        for cname in cands:
            before = len(cands[cname])
            cands[cname] = [(i, t) for i, t in cands[cname] if i not in parents]
            for i in parents:
                if before != len(cands[cname]): EXCLUDED[i] = (cname, 'register parent', 1.0)
    import glob
    extra = [os.path.join(HERE, n + '_tests.json') for n in os.environ.get('BIXBY_EXTRA_TESTS', '').split(',') if n]
    for f in sorted(glob.glob(os.path.join(HERE, 'tests_*.json'))) + [f for f in extra if os.path.exists(f)]:
        tname = os.path.basename(f)[6:-5] if os.path.basename(f).startswith('tests_') else os.path.basename(f)[:-11]
        T = json.load(open(f))
        tests[tname] = [(k, strip_punct_text(v['text']) if sp else v['text'], v.get('author')) for k, v in T.items()]
        parents = {p for v in T.values() for p in v.get('parents', [])}
        for cname in cands:
            cands[cname] = [(i, t) for i, t in cands[cname] if i not in parents]
    if sp:
        for k in tests:
            if k not in ('specials', 'register', 'paired'):
                tests[k] = [(i, strip_punct_text(t), a) for i, t, a in tests[k]]
    EXCLUDED.update(dedupe(cands, tests['specials'] + tests.get('register', [])))
    return {'candidates': cands, 'tests': tests, 'excluded': dict(EXCLUDED)}
