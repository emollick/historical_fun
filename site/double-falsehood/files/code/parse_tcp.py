#!/usr/bin/env python3
"""Parse TCP (EEBO/ECCO) TEI P5 XML into play/act/scene segments of spoken text.

Output: corpus/parsed/<TCPID>.json  with structure
  {"id","title","author","date","plays":[{"play_title","segments":[{"act","scene","head","speeches":[{"speaker","verse":[lines],"prose":[paras]}]}]}]}
Stage directions, speaker labels, notes and front matter are dropped. <g ref="char:EOLhyphen"/> joins split words.
Illegible <gap> is rendered as a caret (^) so tokens containing it can be excluded.
"""
import sys, os, json, re
from lxml import etree

NS = '{http://www.tei-c.org/ns/1.0}'
def ln(el):
    return etree.QName(el).localname if isinstance(el.tag, str) else ''

def text_of(el):
    """Text content of an element, dropping <note>, <stage>, <speaker>, handling <g> and <gap>."""
    out = []
    def rec(e):
        t = ln(e)
        if t in ('note', 'stage', 'speaker', 'figure', 'fw', 'pb', 'milestone'):
            if e.tail: out.append(e.tail)
            return
        if t == 'g':
            ref = e.get('ref', '')
            if ref.endswith('EOLhyphen'):
                out.append('')  # word continues on next line
            elif ref.endswith('cmbAbbrStroke') or ref.endswith('abque') or ref.endswith('abquam'):
                out.append('~')  # abbreviation stroke; mark for exclusion
            elif ref.endswith('punc'):
                out.append('.')
            else:
                out.append('~')
            if e.tail: out.append(e.tail)
            return
        if t == 'gap':
            out.append('^')
            if e.tail: out.append(e.tail)
            return
        if t == 'lb':
            out.append('\n')
            if e.tail: out.append(e.tail)
            return
        if e.text: out.append(e.text)
        for c in e:
            rec(c)
        if e.tail: out.append(e.tail)
    if el.text: out.append(el.text)
    for c in el:
        rec(c)
    s = ''.join(out).replace('\u017f', 's').replace('\u017F', 's')
    s = re.sub(r'[ \t\r]+', ' ', s)
    s = re.sub(r' ?\n ?', '\n', s).strip()
    return s

def head_text(div):
    for c in div:
        if ln(c) == 'head':
            return text_of(c)
    return ''

def collect_speeches(div, speeches, stop_types):
    """Collect <sp> under div, but do not descend into child divs of the given types."""
    for c in div:
        t = ln(c)
        if t == 'div' and (c.get('type') in stop_types or c.get('type') in PLAY_TYPES):
            continue
        if t == 'sp':
            sp = {'speaker': '', 'verse': [], 'prose': []}
            for x in c:
                xt = ln(x)
                if xt == 'speaker':
                    sp['speaker'] = text_of(x)
                elif xt == 'l':
                    s = text_of(x)
                    if s: sp['verse'].append(s)
                elif xt == 'lg':
                    for l in x.iter(NS + 'l'):
                        s = text_of(l)
                        if s: sp['verse'].append(s)
                elif xt == 'p':
                    # a <p> may contain <l> lines (verse set as paragraph) or plain prose
                    ls = [l for l in x if ln(l) == 'l']
                    if ls:
                        for l in ls:
                            s = text_of(l)
                            if s: sp['verse'].append(s)
                    else:
                        s = text_of(x)
                        if s: sp['prose'].append(s)
                elif xt in ('stage', 'note', 'pb', 'figure'):
                    pass
                elif xt == 'div':
                    pass
                else:
                    s = text_of(x)
                    if s: sp['prose'].append(s)
            if sp['verse'] or sp['prose']:
                speeches.append(sp)
        elif t in ('stage', 'head', 'trailer', 'closer', 'opener', 'note', 'pb', 'figure', 'fw'):
            continue
        elif t == 'div':
            collect_speeches(c, speeches, stop_types)
        elif t in ('l', 'p', 'lg'):
            # unassigned lines outside <sp> (rare): attach as anonymous speech
            s = text_of(c)
            if s:
                speeches.append({'speaker': '', 'verse': [s] if t != 'p' else [], 'prose': [s] if t == 'p' else []})
        else:
            collect_speeches(c, speeches, stop_types)

PLAY_TYPES = ('play', 'masque', 'comedy', 'tragedy', 'tragicomedy', 'opera', 'interlude', 'text', 'drama')

def owned(d, play_div):
    """True if the nearest play-type ancestor of d is play_div (i.e. d is not inside a nested play)."""
    for a in d.iterancestors():
        if ln(a) == 'div' and a.get('type') in PLAY_TYPES:
            return a is play_div
    return True

def parse_play(play_div, play_title):
    segments = []
    acts = [d for d in play_div.iter(NS + 'div') if d.get('type') in ('act',) and owned(d, play_div)]
    # keep only acts that belong to this play (iter includes nested); fine since play_div is the root
    if acts:
        for ai, act in enumerate(acts, 1):
            scenes = [d for d in act.iter(NS + 'div') if d.get('type') == 'scene']
            ahead = head_text(act)
            if scenes:
                # speeches directly under act but outside scenes (e.g. before scene 1)
                pre = []
                collect_speeches(act, pre, stop_types={'scene'})
                if pre:
                    segments.append({'act': ai, 'scene': 0, 'head': ahead, 'speeches': pre})
                for si, sc in enumerate(scenes, 1):
                    sps = []
                    collect_speeches(sc, sps, stop_types=set())
                    segments.append({'act': ai, 'scene': si, 'head': (ahead + ' | ' + head_text(sc)).strip(' |'), 'speeches': sps})
            else:
                sps = []
                collect_speeches(act, sps, stop_types=set())
                segments.append({'act': ai, 'scene': 0, 'head': ahead, 'speeches': sps})
    else:
        scenes = [d for d in play_div.iter(NS + 'div') if d.get('type') == 'scene' and owned(d, play_div)]
        if scenes:
            pre = []
            collect_speeches(play_div, pre, stop_types={'scene'})
            if pre:
                segments.append({'act': 0, 'scene': 0, 'head': '', 'speeches': pre})
            for si, sc in enumerate(scenes, 1):
                sps = []
                collect_speeches(sc, sps, stop_types=set())
                segments.append({'act': 0, 'scene': si, 'head': head_text(sc), 'speeches': sps})
        else:
            sps = []
            collect_speeches(play_div, sps, stop_types=set())
            segments.append({'act': 0, 'scene': 0, 'head': head_text(play_div), 'speeches': sps})
    return {'play_title': play_title, 'segments': segments}

FRONT = {'title_page', 'dedication', 'editors_preface', 'preface', 'prologue', 'epilogue', 'dramatis_personae', 'license', 'half_title',
         'encomium', 'encomia', 'to_the_reader', 'stationer_to_the_reader', 'poem_to_the_stationer', 'poem_by_stationer', 'notice',
         'list_of_plays', 'verse_letter', 'poem', 'sonnet', 'epigram', 'frontispiece', 'prologue_and_epilogue', 'list_of_actors',
         'table_of_contents', 'colophon', 'song', 'advertisement', 'errata', 'contents', 'commendatory_verse', 'commendatory_poem',
         'letter', 'epistle', 'argument', 'dialogue', 'masque', 'act_and_scene'}

def parse_file(fn):
    tree = etree.parse(fn)
    root = tree.getroot()
    hdr = root.find(NS + 'teiHeader')
    title = author = date = ''
    if hdr is not None:
        t = hdr.find('.//' + NS + 'titleStmt/' + NS + 'title')
        if t is not None: title = text_of(t)
        a = hdr.find('.//' + NS + 'titleStmt/' + NS + 'author')
        if a is not None: author = text_of(a)
        d = hdr.find('.//' + NS + 'sourceDesc//' + NS + 'date')
        if d is not None: date = text_of(d)
    text = root.find('.//' + NS + 'text')
    plays = []
    play_divs = [d for d in text.iter(NS + 'div') if d.get('type') in PLAY_TYPES
                 and not any(ln(a) == 'front' or ln(a) == 'back' for a in d.iterancestors())]
    if not play_divs:
        play_divs = [b for b in text.iter(NS + 'body')] or [text]
    for pd in play_divs:
        pt = head_text(pd) or title
        plays.append(parse_play(pd, pt))
    return {'id': os.path.basename(fn).replace('.xml', ''), 'title': title, 'author': author, 'date': date, 'plays': plays}

def words(seg):
    n = 0
    for sp in seg['speeches']:
        for l in sp['verse']: n += len(l.split())
        for p in sp['prose']: n += len(p.split())
    return n

if __name__ == '__main__':
    src = sys.argv[1]; out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    files = sorted(f for f in os.listdir(src) if f.endswith('.xml'))
    rows = []
    for f in files:
        try:
            d = parse_file(os.path.join(src, f))
        except Exception as e:
            print('ERROR', f, e); continue
        with open(os.path.join(out, d['id'] + '.json'), 'w') as fh:
            json.dump(d, fh)
        for pi, p in enumerate(d['plays']):
            nseg = len(p['segments']); nw = sum(words(s) for s in p['segments'])
            nv = sum(len(sp['verse']) for s in p['segments'] for sp in s['speeches'])
            npw = sum(len(x.split()) for s in p['segments'] for sp in s['speeches'] for x in sp['prose'])
            rows.append((d['id'], pi, p['play_title'][:70], nseg, nw, nv, npw))
    with open(os.path.join(out, 'INDEX.tsv'), 'w') as fh:
        fh.write('id\tplay_index\tplay_title\tn_segments\tn_words\tn_verse_lines\tn_prose_words\n')
        for r in rows: fh.write('\t'.join(str(x) for x in r) + '\n')
    print('parsed', len(files), 'files;', len(rows), 'plays')
