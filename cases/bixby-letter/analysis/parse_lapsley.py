"""Parse the Project Gutenberg Lapsley edition (Papers and Writings of Abraham Lincoln,
Constitutional Edition, 1905-06) into dated items. Used (a) as a clean-text
pre-1860 Lincoln corpus for replicating Grieve et al.'s design, and (b) as a
cross-check on OCR noise in the Basler scans. Editorial captions, tables of
contents and Gutenberg boilerplate are dropped."""
import re, json, sys, os
MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
MON = {m: i+1 for i, m in enumerate(MONTHS.split('|'))}
DATE_RE = re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(18\d\d)', re.I)
ABBR = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'sept':9,'oct':10,'nov':11,'dec':12}
YEAR_RE = re.compile(r'\b(18[2-6]\d)\b')

def parse(path, vol):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    body = raw.split('*** START')[1].split('*** END')[0]
    body = body.split('\n', 1)[1]
    # drop contents block: everything before the first item heading "TO ..." or a speech heading followed by dateline
    blocks = re.split(r'\n\s*\n\s*\n\s*\n+', body)
    items = []
    cur_year = None
    for b in blocks:
        lines = [l.rstrip() for l in b.strip('\n').splitlines()]
        if not lines: continue
        # peel heading lines: ALL CAPS lines at the top (allow digits, punctuation)
        heads = []
        while lines and lines[0].strip() and lines[0].strip() == lines[0].strip().upper() and re.search(r'[A-Z]', lines[0]):
            heads.append(lines.pop(0).strip())
            while lines and not lines[0].strip(): lines.pop(0)
        text = '\n'.join(lines).strip()
        m = re.fullmatch(r'\s*(18\d\d)\s*', b)
        if m: cur_year = int(m.group(1)); continue
        if not heads and len(text.split()) < 5: continue
        if any(k in ' '.join(heads).upper() for k in ('INTRODUCT', 'ESSAY BY', 'BY JOSEPH', 'PAPERS AND WRITINGS', 'VOLUME ', 'CONTENTS')): continue
        headtxt = ' | '.join(heads)
        # date from heading/dateline or first lines
        d = None
        for src in heads + lines[:3]:
            mm = DATE_RE.search(src)
            if mm:
                d = '%s-%02d-%02d' % (mm.group(3), ABBR[mm.group(1).lower()], int(mm.group(2))); break
        if d is None:
            for src in heads + lines[:3]:
                my = YEAR_RE.search(src)
                if my: d = my.group(1); break
        if d is None and cur_year: d = str(cur_year)
        if d: cur_year = int(d[:4])
        items.append({'volume': vol, 'heading': headtxt, 'date': d or '', 'text': text, 'nwords': len(text.split())})
    return items

if __name__ == '__main__':
    out = []
    root = sys.argv[1]; dest = sys.argv[2]
    for vol, pg in [(1, 2653), (2, 2654), (3, 2655), (4, 2656), (5, 2657), (6, 2658), (7, 2659)]:
        p = os.path.join(root, f'pg{pg}.txt')
        if not os.path.exists(p): continue
        its = parse(p, vol)
        for k, it in enumerate(its):
            it['id'] = f'L{vol}-{k:04d}'
        out.extend(its)
        print(vol, len(its), sum(i['nwords'] for i in its), 'undated', sum(1 for i in its if not i['date']))
    with open(dest, 'w', encoding='utf-8') as f:
        for it in out: f.write(json.dumps(it, ensure_ascii=False) + '\n')
    print('total', len(out), sum(i['nwords'] for i in out))
