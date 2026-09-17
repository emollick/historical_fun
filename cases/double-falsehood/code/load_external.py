#!/usr/bin/env python3
"""Load OCR-derived external texts (Theobald's own plays, early-18th-century adaptations, contrast texts)
into corpus/segments.jsonl as fixed-size pseudo-scenes.

OCR cleaning per line: drop stage directions / headings, strip speech prefixes, drop tokens with digits or symbols,
keep a line only if >= 60% of its word tokens are lexicon words after spelling normalisation.
The play body is located automatically as the span between the first and last stretches of dialogue
(speech-prefix density), which strips dedications, prefaces, prologues and epilogues.
"""
import sys, os, re, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize_tokens, tokenize, norm, LEX

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXT = os.path.join(ROOT, 'corpus', 'raw_external')

# (folder/file, key, group, author, date, note, kind)
TEXTS = [
 ('df_ocr_1728/df_ocr_1728.clean.txt', 'dfocr_double_falsehood', 'DFOCR', 'Theobald?', 1728, 'Double Falsehood 1728, BL microfilm OCR (control for OCR effects; same pipeline as Theobald plays)', 'play'),
 ('persian_princess_1715/persian_princess_1715.clean.txt', 'theo_persian_princess', 'THEO', 'Theobald', 1715, 'Persian Princess 1715 (OCR)', 'play'),
 ('perfidious_brother_1715/perfidious_brother_1715.clean.txt', 'theo_perfidious_brother', 'THEO', 'Theobald', 1715, 'Perfidious Brother 1715 (OCR; Theobald rewriting of Mestayer draft)', 'play'),
 ('orestes_1731/orestes_1731.clean.txt', 'theo_orestes', 'THEO', 'Theobald', 1731, 'Orestes 1731 (OCR)', 'play'),
 ('happy_captive_1741/happy_captive_1741.clean.txt', 'theo_happy_captive', 'THEO', 'Theobald', 1741, 'Happy Captive 1741 (OCR)', 'play'),
 ('cave_of_poverty_1715/cave_of_poverty_1715_copyA.clean.txt', 'theo_cave_of_poverty', 'THEOV', 'Theobald', 1715, 'Cave of Poverty 1715, poem in imitation of Shakespeare (OCR)', 'poem'),
 ('electra_1714/electra_1714_copyA.clean.txt', 'theo_electra', 'THEOT', 'Theobald', 1714, 'Electra 1714, translation of Sophocles (OCR)', 'play'),
 ('oedipus_1715/oedipus_1715.clean.txt', 'theo_oedipus', 'THEOT', 'Theobald', 1715, 'Oedipus 1715, translation of Sophocles (OCR)', 'play'),
 ('plutus_1715/plutus_1715.clean.txt', 'theo_plutus', 'THEOT', 'Theobald', 1715, 'Plutus 1715, translation of Aristophanes (OCR)', 'play'),
 ('clouds_1715/clouds_1715.clean.txt', 'theo_clouds', 'THEOT', 'Theobald', 1715, 'Clouds 1715, translation of Aristophanes (OCR)', 'play'),
 ('mestayer_perfidious_brother_1720/mestayer_perfidious_brother_1720.clean.txt', 'mestayer_perfidious_brother', 'CTRL', 'Mestayer', 1720, 'Mestayer Perfidious Brother 1720 (OCR; contrast text)', 'play'),
 ('cibber_richard_iii_1700/cibber_richard_iii_1700.clean.txt', 'ad_richard3_1700', 'ADAPT', 'C. Cibber', 1700, 'orig=sh_richard3 by Shakespeare', 'play'),
 ('cibber_love_makes_a_man_1701/cibber_love_makes_a_man_1701_copyA_1701.clean.txt', 'ad_love_makes_a_man_1701', 'ADAPT', 'C. Cibber', 1701, 'orig=fx_elder_brother+fx_custom_of_country by Fletcher', 'play'),
 ('farquhar_inconstant_1702/farquhar_inconstant_1702.clean.txt', 'ad_inconstant_1702', 'ADAPT', 'Farquhar', 1702, 'orig=fl_wild_goose_chase by Fletcher', 'play'),
 ('granville_jew_of_venice_1701/granville_jew_of_venice_1701.clean.txt', 'ad_jew_of_venice_1701', 'ADAPT', 'Granville', 1701, 'orig=sh_merchant by Shakespeare', 'play'),
 ('hill_henry_v_1723/hill_henry_v_1723.clean.txt', 'ad_henry5_1723', 'ADAPT', 'A. Hill', 1723, 'orig=sh_henry5 by Shakespeare', 'play'),
 ('sheffield_julius_caesar_1723/sheffield_julius_caesar_1723.clean.txt', 'ad_julius_caesar_1723', 'ADAPT', 'Sheffield', 1723, 'orig=sh_julius_caesar by Shakespeare', 'play'),
 ('sheffield_julius_caesar_1723/sheffield_marcus_brutus_1723.clean.txt', 'ad_marcus_brutus_1723', 'ADAPT', 'Sheffield', 1723, 'orig=sh_julius_caesar by Shakespeare', 'play'),
 ('burnaby_love_betrayd_1703/burnaby_love_betrayd_1703.clean.txt', 'ad_love_betrayd_1703', 'ADAPT', 'Burnaby', 1703, 'orig=sh_twelfth_night by Shakespeare', 'play'),
]

PREFIX = re.compile(r"^\s*(?:\d\.?\s*)?(?:[A-Z][A-Za-z']{0,9}\.|[A-Z][a-z]{1,8}\s[A-Z][a-z]{1,8}\.)\s+")
DIRECTION = re.compile(r"^\s*(Enter|Exit|Exeunt|Manent|Manet|Re-enter|SCENE|Scene|ACT|Act\b|The End|FINIS|EPILOGUE|PROLOGUE|Dramatis|\[|\()")
WORD = re.compile(r"^[a-z][a-z']*$")
SHORT_OK = {'a','i','o','an','to','of','in','it','is','be','by','he','me','my','no','on','or','so','we','ye','as','at','do','go','if','up','us','am','oh','em','th','ah','ha','st'}
ADVERT = re.compile(r"(printed for|sold by|price|edition|translated|books|octavo|folio|quarto|lately publish|just publish|proposals|subscri)", re.I)

def clean_line(line):
    if DIRECTION.match(line): return None
    line = PREFIX.sub('', line, count=1)
    toks = tokenize(line)
    words = [t for t in toks if WORD.match(t)]
    if len(words) < 3: return None
    good = sum(1 for w in words if norm(w) in LEX and (len(w) > 2 or w in SHORT_OK))
    if good / len(words) < 0.5: return None
    words = [w for w in words if len(w) > 2 or w in SHORT_OK]  # drop 1-2 letter OCR fragments
    if len(words) < 3: return None
    if sum(1 for w in words if len(w) <= 2) > 0.4 * len(words): return None
    if sum(len(w) for w in words) / len(words) < 2.8: return None
    if sum(len(t) for t in toks if not WORD.match(t)) > 0.3 * sum(len(t) for t in toks): return None
    return ' '.join(words)

def body_span(lines, window=40, need=4):
    """first and last index where a window of lines holds >= need speech-prefix lines"""
    flags = [1 if PREFIX.match(l) else 0 for l in lines]
    n = len(lines); first = None; last = None
    for i in range(n):
        if sum(flags[i:i+window]) >= need: first = i; break
    for i in range(n - 1, -1, -1):
        if sum(flags[max(0, i-window):i+1]) >= need: last = i; break
    if first is None: return 0, n
    return first, last + 1

def load_one(path, kind, chunk=800):
    lines = open(path, encoding='utf-8').read().split('\n')
    if kind == 'play':
        a, b = body_span(lines)
    else:
        a, b = 0, len(lines)
    # cut a trailing book-list advertisement
    tail = int(len(lines) * 0.92)
    for i in range(max(tail, a), b):
        if ADVERT.search(lines[i]) and i < b:
            b = i; break
    kept = []
    for l in lines[a:b]:
        c = clean_line(l)
        if c: kept.append(c)
    return kept, (a, b, len(lines))

def main(chunk=800, write=False):
    out_recs = []
    for rel, key, group, author, date, note, kind in TEXTS:
        path = os.path.join(EXT, rel)
        kept, span = load_one(path, kind, chunk)
        text = '\n'.join(kept)
        raw = tokenize(text); toks = normalize_tokens(text)
        # fixed-size pseudo-scenes
        nseg = max(1, round(len(kept) / max(1, chunk / 8)))  # ~8 words per line
        per = max(1, len(kept) // nseg)
        segs = [kept[i*per:(i+1)*per] if i < nseg - 1 else kept[i*per:] for i in range(nseg)]
        tot = 0
        for i, sl in enumerate(segs):
            t = '\n'.join(sl)
            r = {'key': key, 'group': group, 'author': author, 'date': date, 'note': note, 'source_id': 'ext:' + rel.split('/')[0],
                 'play_title': key, 'act': 0, 'scene': i + 1, 'head': f'chunk {i+1}', 'n_words': 0, 'n_verse_lines': len(sl),
                 'n_prose_words': 0, 'verse_lines': sl, 'prose': [], 'tokens': normalize_tokens(t), 'raw_tokens': tokenize(t)}
            r['n_words'] = len(r['tokens']); tot += r['n_words']
            out_recs.append(r)
        print(f'{key:32s} {group:5s} span={span} lines_kept={len(kept):5d} words={tot:6d} segs={len(segs)}')
        print('   first:', ' | '.join(kept[:2])[:150])
        print('   last :', ' | '.join(kept[-2:])[:150])
    if write:
        fn = os.path.join(ROOT, 'corpus', 'segments.jsonl')
        existing = [json.loads(l) for l in open(fn)]
        keys_new = {r['key'] for r in out_recs}
        existing = [r for r in existing if r['key'] not in keys_new]
        with open(fn, 'w') as fh:
            for r in existing + out_recs: fh.write(json.dumps(r) + '\n')
        print('wrote', len(existing) + len(out_recs), 'records')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true'); ap.add_argument('--chunk', type=int, default=800)
    a = ap.parse_args(); main(a.chunk, a.write)
