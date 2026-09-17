#!/usr/bin/env python3
"""Download the raw control texts (Project Gutenberg plain text; archive.org OCR djvu.txt).
Outputs go to data/controls/raw/.  Re-runs skip files that already exist.
Every entry records the URL actually fetched; the manifest of the *samples* cut from these
files is written by stylo_build_samples.py (data/controls/manifest.csv)."""
import os, sys, subprocess, json, time
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(B, 'data', 'controls', 'raw')
os.makedirs(RAW, exist_ok=True)

GUTENBERG = {  # id: short description
    16784: 'Jefferson, Memoir, Correspondence and Miscellanies vol. 4 (letters 1816-1826; ed. T.J. Randolph 1829)',
    43774: 'Pike, Expeditions of Zebulon M. Pike vol. 1 (journals 1805-07, publ. 1810; Coues ed. 1895)',
    16565: 'Biddle/Lewis & Clark, History of the Expedition vol. 1 (1814; Coues ed. 1893)',
    44205: 'Gregg, Commerce of the Prairies part 2 (1844; Thwaites ed. 1905)',
    46110: 'Pattie, Personal Narrative (1831; Thwaites ed. 1905)',
    62018: 'Fowler, Journal of Jacob Fowler (1821-22; Coues ed. 1898)',
    39975: 'Audubon and His Journals vol. 1 (European journal 1826-29 etc.; 1897)',
    2323:  'R.E. Lee, Recollections and Letters (letters 1860s-1870; 1904)',
    19831: 'Jefferson Davis, Rise and Fall of the Confederate Government vol. 1 (1881)',
    26725: 'T.N. Page, Two Little Confederates (1888)',
    10234: 'G.W. Cable, Old Creole Days (1879)',
    51211: 'G.C. Eggleston, A Rebel\'s Recollections (1874)',
    245:   'Mark Twain, Life on the Mississippi (1883)',
    10692: 'J.E. Cooke, A Life of Gen. Robert E. Lee (1871)',
    2147:  'Poe, Works vol. 1 (incl. The Gold-Bug, 1843)',
    2148:  'Poe, Works vol. 2',
    8424:  'J.E. Cooke, Mohun (1869)',
    23283: 'J.E. Cooke, The Youth of Jefferson (1854)',
    3195:  'Mark Twain\'s Letters vol. 3, 1876-1885 (Paine ed. 1917)',
}
ARCHIVE = {  # identifier: description
    'selectionsfrommi02bagbrich': 'G.W. Bagby, Selections from the Miscellaneous Writings vol. 2 (1885)',
    'selectionsfromm00bagbgoog':  'G.W. Bagby, Selections from the Miscellaneous Writings vol. 1 (1884)',
    'virginiaahistor02cookgoog':  'J.E. Cooke, Virginia: A History of the People (1883)',
    'correspondenceof0003jack':   'Correspondence of Andrew Jackson vol. 3, 1820-1828 (Bassett ed. 1928)',
    'memjohnquincy05adamrich':    'Memoirs of John Quincy Adams vol. 5 (diary 1819-1821; 1875)',
    'recollectionsofl00flin_0':   'Timothy Flint, Recollections of the Last Ten Years (1826)',
    'lettersofjohnran00rand':     'Letters of John Randolph to a Young Relative (letters 1806-1832; 1834)',
    'memoirsoflifeofw01kenn':     'Kennedy, Memoirs of the Life of William Wirt vol. 1 (Wirt letters 1800-1820s; 1849)',
    'memoirsoflife02kenn':        'Kennedy, Memoirs of the Life of William Wirt vol. 2 (Wirt letters 1820s-1834; 1850)',
    'threeyearsamongi00jame':     'Thomas James, Three Years Among the Indians and Mexicans (1846; 1916 reprint)',
    'sketchesrecollec00cabe':     'M.A. Cabell, Sketches and Recollections of Lynchburg (1858)',
    'lynchburgitspeop00chri':     'W.A. Christian, Lynchburg and Its People (1900)',
    'sketchbookoflync00poll':     'Pollock (ed.), Sketch Book of Lynchburg, Va. (1887)',
    'accountofexpedit02jame':     'Edwin James, Account of an Expedition from Pittsburgh to the Rocky Mountains vol. 2 (1823)',
    'lettersfromsouth00paul':     'J.K. Paulding, Letters from the South (1817)',
    'lettersfromwestc00hall':     'James Hall, Letters from the West (1828)',
    'lifeandletterse00harrgoog':  'J.A. Harrison, Life and Letters of Edgar Allan Poe (1903; Poe letters)',
    'southernhistoric13sout':     'Southern Historical Society Papers vol. 13 (1885)',
    'mannerssocialus00shergoog':  'M.E.W. Sherwood, Manners and Social Usages (1887) [dating check only]',
    'touronprairies00irvi':       'Washington Irving, A Tour on the Prairies (1835)',
}

def fetch(url, out):
    for attempt in range(3):
        r = subprocess.run(['curl', '-sS', '-L', '-m', '300', '-A', 'Mozilla/5.0 (research script)', '-o', out, '-w', '%{http_code}', url],
                           capture_output=True, text=True)
        if r.stdout.strip() == '200' and os.path.getsize(out) > 5000:
            return True
        time.sleep(3)
    if os.path.exists(out): os.remove(out)
    return False

log = []
for gid, desc in GUTENBERG.items():
    out = os.path.join(RAW, f'gutenberg_{gid}.txt')
    if os.path.exists(out):
        log.append((f'gutenberg_{gid}.txt', f'https://www.gutenberg.org/ebooks/{gid}', desc, 'present')); continue
    ok = False
    for url in (f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt', f'https://www.gutenberg.org/files/{gid}/{gid}-0.txt', f'https://www.gutenberg.org/files/{gid}/{gid}.txt'):
        if fetch(url, out): ok = True; break
    log.append((f'gutenberg_{gid}.txt', f'https://www.gutenberg.org/ebooks/{gid}', desc, 'ok' if ok else 'FAILED'))
    print(log[-1], flush=True)
for ident, desc in ARCHIVE.items():
    out = os.path.join(RAW, f'archive_{ident}.txt')
    if os.path.exists(out):
        log.append((f'archive_{ident}.txt', f'https://archive.org/details/{ident}', desc, 'present')); continue
    ok = fetch(f'https://archive.org/download/{ident}/{ident}_djvu.txt', out)
    log.append((f'archive_{ident}.txt', f'https://archive.org/details/{ident}', desc, 'ok' if ok else 'FAILED'))
    print(log[-1], flush=True)
with open(os.path.join(RAW, 'download_log.tsv'), 'w') as f:
    f.write('file\tsource_url\tdescription\tstatus\n')
    for row in log: f.write('\t'.join(row) + '\n')
print('done')
