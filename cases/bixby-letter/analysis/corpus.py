"""Common loader for the Lincoln / Hay / control corpora built by the scripts in corpus/scripts/.
Expected files under corpus/: lincoln_basler.jsonl, hay.jsonl, controls.jsonl,
bixby_letter_basler.txt. Field names are normalised here so the analysis scripts
do not depend on those scripts' exact choices."""
import json, os, re, datetime
from ngt import word_count

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'corpus')

def _norm(rec, author):
    r = dict(rec)
    r['author'] = author
    r['text'] = (r.get('text') or '').strip()
    r['id'] = str(r.get('id') or r.get('doc_id') or '')
    r['wc'] = r.get('word_count') or word_count(r['text'])
    d = r.get('date') or r.get('date_iso') or ''
    r['date'] = d
    m = re.match(r'(\d{4})', str(d))
    r['year'] = int(m.group(1)) if m else None
    r['source_code'] = (r.get('source_code') or r.get('source') or '').strip()
    r['autograph'] = bool(r.get('autograph', False))
    r['period'] = r.get('period') or ''
    r['genre'] = r.get('genre') or ''
    return r

def load(name, author=None):
    path = os.path.join(ROOT, name)
    out = []
    with open(path, encoding='utf-8') as f:
        for ln in f:
            ln = ln.strip()
            if not ln: continue
            rec = json.loads(ln)
            out.append(_norm(rec, author or rec.get('author') or name.split('.')[0]))
    return out

def bixby():
    with open(os.path.join(ROOT, 'bixby_letter_basler.txt'), encoding='utf-8') as f:
        return f.read().strip()

def lincoln_pre1860(recs):
    """Grieve's Lincoln design: everything dated before 18 May 1860."""
    cut = datetime.date(1860, 5, 18)
    out = []
    for r in recs:
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})', str(r['date']))
        if m:
            try:
                d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                d = datetime.date(int(m.group(1)), 1, 1)
            if d < cut: out.append(r)
        elif r['year'] and r['year'] < 1860:
            out.append(r)
    return out

def lincoln_war_autograph(recs):
    return [r for r in recs if r['year'] and r['year'] >= 1861 and r['autograph']]

def lincoln_war_nonautograph(recs):
    return [r for r in recs if r['year'] and r['year'] >= 1861 and not r['autograph']]
