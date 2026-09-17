#!/usr/bin/env python3
"""Query the Google Books Ngram Viewer JSON endpoint for every word type in one or more texts.

usage: lang_ngram_query.py OUT.csv TEXT1 [TEXT2 ...]
Corpus en-US-2019 (American English), smoothing 0, years 1780-1900, case-insensitive.
All raw responses are cached in results/lang_ngram_cache.json so re-runs are free.
Per word the CSV gives: freq summed over 1780-1821 (mean of yearly relative frequencies),
number of years in 1780-1821 with non-zero frequency, first non-zero year, mean 1822-1849,
mean 1850-1900, and the ratio pre-1822 / 1850-1900.
Words are lower-cased, hyphens split, tokens with digits dropped.  A word is marked
'proper' when it only ever occurs capitalised in a non-sentence-initial position."""
import sys, os, re, json, time, csv, urllib.parse, urllib.request, collections
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.environ.get('NGRAM_CACHE', os.path.join(B, 'results', 'lang_ngram_cache.json'))
# a merged view of every cache file (parallel runs write separate caches; see lang_ngram_analysis.py)
Y0, Y1 = 1780, 1900
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
import glob
for _f in glob.glob(os.path.join(B, 'results', 'lang_ngram_cache*.json')):   # reuse words already fetched by any run
    if _f != CACHE:
        try:
            for _k, _v in json.load(open(_f)).items():
                if _k not in cache and _v is not None: cache[_k] = _v
        except Exception: pass

def tokens_with_context(text):
    text = text.replace('’', "'").replace('—', ' ').replace('“', ' ').replace('”', ' ')
    text = re.sub(r'&c\.', ' etc ', text)
    sents = re.split(r'(?<=[.!?])\s+', text)
    out = []
    for s in sents:
        ws = re.findall(r"[A-Za-z][A-Za-z'\-]*[A-Za-z]|[A-Za-z]", s)
        for i, w in enumerate(ws):
            for part in w.split('-'):
                part = part.strip("'")
                if not part: continue
                out.append((part, i == 0))
    return out

def word_types(texts):
    caps = collections.defaultdict(lambda: [0, 0])  # word -> [n_capitalised_noninitial, n_other]
    for t in texts:
        for w, initial in tokens_with_context(t):
            key = w.lower()
            if w[0].isupper() and not initial: caps[key][0] += 1
            else: caps[key][1] += 1
    return {w: ('proper' if c[0] > 0 and c[1] == 0 else '') for w, c in caps.items()}

def query(words):
    todo = [w for w in words if w not in cache]
    for i in range(0, len(todo), 10):
        batch = todo[i:i+10]
        url = ('https://books.google.com/ngrams/json?content=' + urllib.parse.quote(','.join(batch)) +
               f'&year_start={Y0}&year_end={Y1}&corpus=en-US-2019&smoothing=0&case_insensitive=true')
        for attempt in range(8):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research script)'})
                data = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except Exception as e:
                wait = 30 * (attempt + 1) if '429' in str(e) else 5 * (attempt + 1)
                print('retry', attempt, e, 'sleeping', wait, file=sys.stderr); time.sleep(wait); data = None
        if data is None:
            print('GIVING UP on batch (not cached):', batch, file=sys.stderr)
            continue
        got = {}
        for entry in data:
            name = entry['ngram'].replace(' (All)', '').lower()
            if entry.get('type') == 'CASE_INSENSITIVE' or name not in got:
                got[name] = entry['timeseries']
        for w in batch:
            cache[w] = got.get(w.lower(), [])   # [] = not in corpus at all
        json.dump(cache, open(CACHE, 'w'))
        time.sleep(float(os.environ.get('NGRAM_SLEEP', '1.2')))

def stats(ts):
    if not ts: return dict(pre1822_mean=0.0, pre1822_years=0, first_year='', mean_1822_49=0.0, mean_1850_1900=0.0, ratio='')
    yrs = list(range(Y0, Y1 + 1))
    pre = [v for y, v in zip(yrs, ts) if y <= 1821]
    mid = [v for y, v in zip(yrs, ts) if 1822 <= y <= 1849]
    late = [v for y, v in zip(yrs, ts) if y >= 1850]
    nz = [y for y, v in zip(yrs, ts) if v > 0]
    m_pre = sum(pre) / len(pre); m_late = sum(late) / len(late)
    return dict(pre1822_mean=m_pre, pre1822_years=sum(1 for v in pre if v > 0), first_year=nz[0] if nz else '',
                mean_1822_49=sum(mid) / len(mid), mean_1850_1900=m_late,
                ratio=(m_pre / m_late) if m_late > 0 else '')

if __name__ == '__main__':
    out = sys.argv[1]; files = sys.argv[2:]
    texts = [open(f, encoding='utf-8').read() for f in files]
    types = word_types(texts)
    counts = collections.Counter(w.lower() for t in texts for w, _ in tokens_with_context(t))
    print(len(types), 'word types', file=sys.stderr)
    query(sorted(types))
    with open(out, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['word', 'count', 'proper', 'pre1822_mean', 'pre1822_years', 'first_year', 'mean_1822_49', 'mean_1850_1900', 'ratio_pre1822_to_1850_1900'])
        for w in sorted(types):
            s = stats(cache.get(w))
            wr.writerow([w, counts[w], types[w], f"{s['pre1822_mean']:.3e}", s['pre1822_years'], s['first_year'], f"{s['mean_1822_49']:.3e}", f"{s['mean_1850_1900']:.3e}", (f"{s['ratio']:.3f}" if s['ratio'] != '' else '')])
    print('wrote', out, file=sys.stderr)
