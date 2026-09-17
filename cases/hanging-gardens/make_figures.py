# Draws Figure 2 (how the descriptions of the garden were passed down) as an inline SVG for the report
# page and as a standalone SVG, and Figure 1 (the probability bar) as a standalone SVG. Run it in
# this folder: python3 make_figures.py. The PNGs are renders of the SVGs at twice the drawn size.
import io, re, html

W, H = 1180, 756
NW, NH = 190, 74
XS = [150 + k*206 for k in range(5)]
BANDS = ["c. 400–330 BC", "c. 300–290 BC", "2nd c. BC to AD 20", "1st–2nd c. AD", "4th c. AD and later"]
# id: (col, ytop, lines, blue)
NODES = {
 'CT': (0, 52,  ["Ctesias, c. 400 BC", "Semiramis builds Babylon;", "Nineveh 'on the Euphrates'"], False),
 'D1': (2, 52,  ["Diodorus 2.7–9, 1st c. BC", "walls, palaces with", "hunting reliefs"], False),
 'AX': (0, 150, ["Unnamed Alexander-era source", "late 4th c. BC"], True),
 'ST': (2, 150, ["Strabo 16.1.5, c. AD 20", "screws from the Euphrates;", "garden on the river bank"], True),
 'CL': (1, 240, ["Clitarchus, c. 300 BC", "Alexander's Babylon"], True),
 'D2': (2, 240, ["Diodorus 2.10, 1st c. BC", "from Clitarchus: 'a later Syrian", "king'; Persian concubine;", "vaults of brick and bitumen"], True),
 'CU': (3, 240, ["Curtius 5.1.31–35, 1st c. AD", "'a king of Syria ruling in", "Babylon'; stone pillars;", "on the citadel"], True),
 'BE': (1, 350, ["Berossus, c. 290 BC", "Nebuchadnezzar's new palace;", "stone terraces; Median wife"], True),
 'PO': (2, 350, ["Alexander Polyhistor, 1st c. BC", "summarises Berossus"], True),
 'JO': (3, 350, ["Josephus, c. AD 95", "quotes Polyhistor's Berossus:", "Antiquities 10.226; Apion 1.141"], True),
 'SY': (4, 350, ["Eusebius and Syncellus", "copy Josephus: Chronicle,", "4th c. AD; Syncellus, c. AD 800"], True),
 'AB': (3, 440, ["Abydenus, 2nd c. AD", "'adorned the palace with trees,", "calling them hanging paradeisoi'"], True),
 'EU': (4, 440, ["Eusebius, Praeparatio 9.41", "early 4th c. AD; quotes Abydenus"], True),
 'HC': (2, 540, ["Hellenistic wonder canon", "Alexandria"], False),
 'PH': (4, 540, ["'Philo of Byzantium'", "4th–6th c. AD; columns,", "palm-trunk beams, screws"], False),
 'AN': (2, 644, ["Antipater, Anthology 9.58", "2nd or 1st c. BC"], False),
}
LANES = [("Ctesias' Assyrian", "history", 52, 126), ("Alexander's", "historians", 150, 314),
         ("Babylonian priestly", "tradition", 350, 514), ("Wonder lists", "", 540, 718)]
SEPS = [138, 340, 528]

def box(nid):
    c, y, lines, blue = NODES[nid]
    x = XS[c]
    return x, y, x+NW, y+NH, x+NW/2, y+NH/2

def esc(t): return html.escape(t, quote=False)

def build(mode):
    blue = 'var(--babylon)' if mode == 'inline' else '#1C6FA6'
    font = 'var(--ui)' if mode == 'inline' else "'IBM Plex Sans','Segoe UI',Helvetica,Arial,'Liberation Sans','DejaVu Sans',sans-serif"
    out = []
    root_attrs = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="How the descriptions of the garden were passed down: the Ctesias line, the Alexander historians, the Babylonian priestly tradition through Berossus, and the wonder lists, with the two independent lines that place the garden in Babylon outlined in blue"' % (W, H)
    if mode == 'inline':
        out.append('<svg %s style="max-width:100%%;height:auto;display:block;font-family:%s">' % (root_attrs, font))
    else:
        out.append('<svg %s width="%d" height="%d" color="#1B1F22" style="font-family:%s">' % (root_attrs, W, H, font))
        out.append('<rect x="0" y="0" width="%d" height="%d" fill="#F7F8F6"/>' % (W, H))
    out.append('<defs><marker id="hg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')
    # column bands
    for k, b in enumerate(BANDS):
        out.append('<text x="%d" y="30" font-size="11" fill="currentColor" fill-opacity="0.7" text-anchor="middle" letter-spacing="0.06em">%s</text>' % (XS[k]+NW/2, esc(b.upper())))
    # lane separators and labels
    for y in SEPS:
        out.append('<line x1="14" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.18" stroke-width="1"/>' % (y, W-14, y))
    for l1, l2, y0, y1 in LANES:
        ym = (y0+y1)/2
        if l2:
            out.append('<text x="14" y="%d" font-size="11" fill="currentColor" fill-opacity="0.75">%s</text>' % (ym-2, esc(l1)))
            out.append('<text x="14" y="%d" font-size="11" fill="currentColor" fill-opacity="0.75">%s</text>' % (ym+12, esc(l2)))
        else:
            out.append('<text x="14" y="%d" font-size="11" fill="currentColor" fill-opacity="0.75">%s</text>' % (ym+5, esc(l1)))
    # edges: (from, to, label, style)
    def hedge(a, b, label, dotted=False):
        ax0, ay0, ax1, ay1, acx, acy = box(a); bx0, by0, bx1, by1, bcx, bcy = box(b)
        dash = ' stroke-dasharray="4 4"' if dotted else ''
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"%s marker-end="url(#hg-arrow)"/>' % (ax1, acy, bx0-1, bcy, dash))
        if label:
            out.append('<text x="%d" y="%d" font-size="10.5" fill="currentColor" fill-opacity="0.8" text-anchor="middle">%s</text>' % ((ax1+bx0)/2, acy-5, esc(label)))
    def vedge(a, b, label):
        ax0, ay0, ax1, ay1, acx, acy = box(a); bx0, by0, bx1, by1, bcx, bcy = box(b)
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4" marker-end="url(#hg-arrow)"/>' % (acx, ay1, bcx, by0-1))
        out.append('<text x="%d" y="%d" font-size="10.5" fill="currentColor" fill-opacity="0.8">%s</text>' % (acx+6, (ay1+by0)/2+4, esc(label)))
    def elbow_below(a, b, yrun, label, dotted=False, enter='top'):
        ax0, ay0, ax1, ay1, acx, acy = box(a); bx0, by0, bx1, by1, bcx, bcy = box(b)
        dash = ' stroke-dasharray="4 4"' if dotted else ''
        if enter == 'top':
            pts = '%d,%d %d,%d %d,%d %d,%d' % (acx, ay1, acx, yrun, bcx, yrun, bcx, by1+1)
            lx, ly = (acx+bcx)/2, yrun+12
        else:  # enter left edge at the run height
            pts = '%d,%d %d,%d %d,%d' % (acx, ay1, acx, yrun, bx0-1, yrun)
            lx, ly = (acx+bx0)/2, yrun-4
        out.append('<polyline points="%s" fill="none" stroke="currentColor" stroke-width="1.4"%s marker-end="url(#hg-arrow)"/>' % (pts, dash))
        out.append('<text x="%d" y="%d" font-size="10.5" fill="currentColor" fill-opacity="0.8" text-anchor="middle">%s</text>' % (lx, ly, esc(label)))
    hedge('CT', 'D1', 'used by')
    hedge('AX', 'ST', 'used by')
    hedge('CL', 'D2', '')
    elbow_below('CL', 'CU', 324, 'used by')
    hedge('BE', 'PO', '')
    hedge('PO', 'JO', '')
    hedge('JO', 'SY', '')
    elbow_below('BE', 'AB', 477, 'via Megasthenes?', dotted=True, enter='left')
    hedge('AB', 'EU', '')
    hedge('HC', 'PH', 'used by')
    vedge('HC', 'AN', 'used by')
    # nodes
    for nid, (c, y, lines, isblue) in NODES.items():
        x = XS[c]
        stroke = ('style="stroke:%s"' % blue) if isblue else 'stroke="currentColor" stroke-opacity="0.45"'
        sw = '2' if isblue else '1'
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="currentColor" fill-opacity="0.05" %s stroke-width="%s"/>' % (x, y, NW, NH, stroke, sw))
        ty = y + 18
        for i, line in enumerate(lines):
            if i == 0:
                out.append('<text x="%d" y="%d" font-size="11.5" font-weight="600" fill="currentColor">%s</text>' % (x+9, ty, esc(line)))
            else:
                out.append('<text x="%d" y="%d" font-size="11" fill="currentColor" fill-opacity="0.85">%s</text>' % (x+9, ty, esc(line)))
            ty += 14 if i == 0 else 13
    # legend
    out.append('<rect x="14" y="732" width="22" height="12" rx="3" fill="currentColor" fill-opacity="0.05" style="stroke:%s" stroke-width="2"/>' % blue)
    out.append('<text x="44" y="742" font-size="11" fill="currentColor" fill-opacity="0.8">the two independent lines that place the garden in Babylon</text>')
    out.append('<line x1="380" y1="738" x2="420" y2="738" stroke="currentColor" stroke-width="1.4" marker-end="url(#hg-arrow)"/>')
    out.append('<text x="428" y="742" font-size="11" fill="currentColor" fill-opacity="0.8">the later writer used the earlier one</text>')
    out.append('<line x1="660" y1="738" x2="700" y2="738" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" marker-end="url(#hg-arrow)"/>')
    out.append('<text x="708" y="742" font-size="11" fill="currentColor" fill-opacity="0.8">a likely but unproven line</text>')
    out.append('</svg>')
    return '\n'.join(out)

def bar_svg():
    segs = [("Babylon", 55, "#1C6FA6"), ("No single structure", 35, "#7B5BA6"), ("Nineveh", 10, "#B8621B")]
    W2, H2 = 800, 120
    o = ["""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Probabilities: Babylon 55 percent, no single structure 35 percent, Nineveh 10 percent" style="font-family:'IBM Plex Sans','Segoe UI',Helvetica,Arial,'Liberation Sans','DejaVu Sans',sans-serif">""" % (W2, H2, W2, H2),
         '<rect x="0" y="0" width="%d" height="%d" fill="#F7F8F6"/>' % (W2, H2)]
    x = 20; total = 760
    for name, pct, col in segs:
        w = total*pct/100
        o.append('<rect x="%.1f" y="24" width="%.1f" height="26" fill="%s"/>' % (x, w-2, col))
        o.append('<text x="%.1f" y="86" font-size="20" font-weight="600" fill="#1B1F22">%d%%</text>' % (x, pct))
        o.append('<text x="%.1f" y="106" font-size="12" fill="#454D52">%s</text>' % (x, name))
        x += w
    o.append('</svg>')
    return '\n'.join(o)

inline = build('inline'); standalone = build('standalone')
io.open('figure2-transmission.svg', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + standalone + '\n')
io.open('figure1-probabilities.svg', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n' + bar_svg() + '\n')
io.open('fig2_inline.svg.txt', 'w', encoding='utf-8').write(inline)
# wrapper pages for PNG renders
for name, w, h in [('figure2-transmission', W, H), ('figure1-probabilities', 800, 120)]:
    svg = io.open(name + '.svg', encoding='utf-8').read()
    io.open('render_' + name + '.html', 'w', encoding='utf-8').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap"><style>html,body{margin:0;background:#F7F8F6}</style></head><body>' + svg + '</body></html>')
print('svg ok', len(inline), len(standalone))
