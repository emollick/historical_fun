#!/usr/bin/env python3
"""Rule-and-dictionary spelling normaliser for early modern English (VARD-lite).
Order: explicit map of frequent early-modern forms (EM_MAP) -> keep if in the modern frequent lexicon (TIER1)
-> orthographic rewrite candidates checked against TIER1 -> keep if in the large dictionary (LEX) -> candidates in LEX -> keep.
Marker forms (ye, 'em, 'tis, hath, doth, i'th', o'th' ...) are preserved as spelled (lowercased).
"""
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = set()
with open(os.path.join(HERE, '..', 'corpus', 'words_alpha.txt')) as fh:
    for w in fh:
        LEX.add(w.strip().lower())
TIER1 = set()
with open(os.path.join(HERE, '..', 'corpus', 'en_50k.txt')) as fh:
    for w in fh:
        x = w.split()[0].lower()
        if x in LEX: TIER1.add(x)   # drop names and noise absent from the dictionary list
for w in ['hath','doth','ye','thee','thou','thy','thine','art','wilt','shalt','canst','dost','didst','hast','wert','ere','oft','ay','nay','yea',
          'sirrah','prithee','marry','faith','troth','betwixt','whilst','methinks','anon','forsooth','wherefore','whither','hither','thither',
          'hence','thence','whence','ope','wast','saith','goest','doest','sir','madam','lady','lord','duke','prince','king','queen']:
    TIER1.add(w)

EM_MAP = {
 'hee':'he','shee':'she','wee':'we','mee':'me','bee':'be','doe':'do','goe':'go','soe':'so','noe':'no','toe':'to','loe':'lo','yee':'ye',
 'onely':'only','olde':'old','bodie':'body','againe':'again','sonne':'son','beleeve':'believe','beleeue':'believe','beleive':'believe',
 'ile':"i'll","i'le":"i'll",'ime':"i'm","i'me":"i'm","wee'l":"we'll","wee'll":"we'll","we'l":"we'll","you'l":"you'll","you'le":"you'll",
 "he'l":"he'll","she'l":"she'll","they'l":"they'll","it'l":"it'll","y'are":"you're","y'ar":"you're","yare":"you're",
 "tha'rt":"thou'rt","th'art":"thou'rt","yo'are":"you're","ye'are":"you're",
 'cald':'called','kild':'killed','sayes':'says','saies':'says','sayd':'said','saide':'said','tould':'told','shold':'should','shoulde':'should',
 'wold':'would','woulde':'would','coulde':'could','ther':'there','theyr':'their',"ther's":"there's",'heer':'here','heere':'here',
 'wher':'where','whear':'where','farre':'far','warre':'war','starre':'star','sunne':'sun','runne':'run','beene':'been','bin':'been','bene':'been',
 'growne':'grown','knowne':'known','downe':'down','towne':'town','crowne':'crown','gowne':'gown','owne':'own','yong':'young',
 'toung':'tongue','frend':'friend','freind':'friend','frends':'friends','freinds':'friends','deere':'dear','deare':'dear',
 'feare':'fear','heare':'hear','neere':'near','neare':'near','yeare':'year','yeares':'years','teares':'tears','eares':'ears',
 'sweete':'sweet','greate':'great','gret':'great','wel':'well','al':'all','shal':'shall','til':'till','stil':'still','wil':'will','ful':'full',
 'els':'else','whome':'whom','whoe':'who','howe':'how','nowe':'now','thinke':'think','thinck':'think','speake':'speak','looke':'look',
 'tooke':'took','shooke':'shook','booke':'book','poore':'poor','doore':'door','sonnes':'sons','sinne':'sin','sinnes':'sins',
 'blesse':'bless','tis':"'tis",'twas':"'twas",'twere':"'twere",'twill':"'twill",'twould':"'twould",'em':"'em",'ith':"i'th'",
 'oth':"o'th'",'yf':'if','yt':'it','hym':'him','hys':'his','dyd':'did','thys':'this','whych':'which','sayth':'saith',
 'honor':'honour','honors':'honours','favor':'favour','favors':'favours','labor':'labour','humor':'humour','humors':'humours','color':'colour',
 'shew':'show','shewn':'shown','shewed':'showed','shews':'shows','murther':'murder','murthered':'murdered','murtherer':'murderer',
 'burthen':'burden','mistris':'mistress','mistriss':'mistress','goodnesse':'goodness','madnesse':'madness',
 'happinesse':'happiness','busines':'business','businesse':'business','villaine':'villain','captaine':'captain',
 'maister':'master','mayster':'master','maisters':'masters','servaunt':'servant','sirha':'sirrah','sirra':'sirrah','sirrha':'sirrah',
 'prethee':'prithee','prythee':'prithee','preethee':'prithee','fayth':'faith','troath':'troth',
 'marrie':'marry','marie':'marry','ayre':'air','aire':'air','faire':'fair','fayre':'fair','payne':'pain','paine':'pain','vaine':'vain','plaine':'plain',
 'maine':'main','raine':'rain','chaine':'chain','straine':'strain','remaine':'remain','obtaine':'obtain','containe':'contain','complaine':'complain',
 'entertaine':'entertain','maintaine':'maintain','certaine':'certain','mountaine':'mountain','fountaine':'fountain','captaines':'captains',
 'ould':'old','beare':'bear','weare':'wear','sweare':'swear','teare':'tear','yeere':'year','desyre':'desire','fyre':'fire',
 'lyfe':'life','wyfe':'wife','tyme':'time','ha':'have',
 "ha's":'has',"do's":'does',"doe's":'does',"do'st":'dost',"goe's":'goes',"i'st":"is't","wer't":"wert",
 "doo't":"do't","hee'd":"he'd","hee's":"he's","shee's":"she's","hee'l":"he'll","shee'l":"she'll","yo'":'you',"y'":'you',
 'vs':'us','vp':'up','vpon':'upon','vnto':'unto','vntill':'until','vntil':'until','vnder':'under','vse':'use','vsed':'used',
 'souldier':'soldier','souldiers':'soldiers','soldiour':'soldier','souldiour':'soldier',
 "shou'd":'should',"wou'd":'would',"cou'd":'could','coud':'could','woud':'would','shoud':'should','tho':'though',"tho'":'though',
 "heav'n":'heaven',"heav'ns":'heavens',"ev'n":'even',"o're":"o'er","ore":"o'er","ne're":"ne'er","e're":"e'er","ev'ry":'every',"gen'rous":'generous',
 "pow'r":'power',"pow'rs":'powers',"flow'r":'flower',"flow'rs":'flowers',"tow'r":'tower',"whate'er":"whate'er","whatere":"whate'er","where'er":"where'er",
 'than':'then','then':'then',
}
for k, v in EM_MAP.items(): TIER1.add(v)
KEEP = {"'em","'tis","'twas","'twere","'twill","'twould","i'th'","o'th'","th'","a'th'","in's","on's","to's","for's","'s","'t","'ll","'d",
        "ne'er","e'er","o'er","e'en","i'","o'","a'","y'","'gainst","'mongst","'twixt","is't","an't","on't","in't","to't","for't","do't","thou'rt","thou'st"}
LEX |= KEEP
TIER1 |= KEEP

VOW = 'aeiou'
def candidates(w):
    """Generate normalised candidates in order of preference."""
    c = []
    def push(x):
        if x and x not in c: c.append(x)
    if 'vv' in w: w = w.replace('vv', 'w'); push(w)
    if w.startswith('v') and len(w) > 1 and w[1] not in VOW and w[1] != 'y': push('u' + w[1:]); w = 'u' + w[1:]
    m = re.sub(r'(?<=[aeiouy])u(?=[aeiouy])', 'v', w)
    if m != w: push(m); w = m
    m = re.sub(r'^(gi|ha|lo|li|mo|sa|se|ser|ne|di|de|re|pre|obser|deli|beha|graue)u', lambda k: k.group(0)[:-1] + 'v', w)
    if m != w: push(m)
    if w.startswith('i') and len(w) > 1 and w[1] in 'aeouy': push('j' + w[1:])
    m = re.sub(r'(?<=[aeiou])i(?=[aeiou])', 'j', w)
    if m != w: push(m)
    if 'ay' in w[:-1]: push(w.replace('ay', 'ai'))
    if 'ey' in w[:-1]: push(w.replace('ey', 'ei'))
    if w.endswith('es') and len(w) > 4:
        push(w[:-2] + 's')
        if w[-3] == w[-4] and w[-3] not in VOW: push(w[:-3] + 's')
    m = re.sub(r'(?<=[bcdfghjklmnpqrstvwxz])y(?=[bcdfghjklmnpqrstvwxz]|$)', 'i', w)
    if m != w and not w.endswith('ly'): push(m)
    if re.search(r'(ee|oe)$', w) and len(w) <= 4: push(w[:-1])
    if w.endswith('ie'): push(w[:-2] + 'y')
    if w.endswith('ies'): push(w[:-3] + 'ys')
    for a, b in [('nesse','ness'),('lesse','less'),('full','ful'),('icke','ic'),('ick','ic'),('ique','ic'),('aunce','ance'),('ounde','ound'),('yng','ing'),('inge','ing')]:
        if w.endswith(a): push(w[:-len(a)] + b)
    if w.endswith('e') and len(w) > 3:
        push(w[:-1])
        if len(w) > 4 and w[-2] == w[-3] and w[-2] not in VOW: push(w[:-2])
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in VOW and w[-1] != 's': push(w[:-1])
    if w.endswith('our'): push(w[:-3] + 'or')
    if w.endswith("'d"): push(w[:-2] + 'ed'); push(w[:-2] + 'd')
    outs = list(c)
    for x in outs:
        if x.endswith('e') and len(x) > 3: push(x[:-1])
        if x.endswith('ie'): push(x[:-2] + 'y')
        y = re.sub(r'(?<=[aeiouy])u(?=[aeiouy])', 'v', x)
        if y != x: push(y)
        if 'ee' in x: push(x.replace('ee', 'ie'))
    return c

_cache = {}
def _norm_core(core):
    if core in EM_MAP: return EM_MAP[core]
    if core in TIER1: return core
    cs = candidates(core)
    for cnd in cs:
        if cnd in EM_MAP: return EM_MAP[cnd]
        if cnd in TIER1: return cnd
    if core in LEX: return core
    for cnd in cs:
        if cnd in LEX: return cnd
    return core

def norm(tok):
    """Normalise one lowercase token (letters and apostrophes only)."""
    if tok in _cache: return _cache[tok]
    t = tok
    if t in KEEP or t in EM_MAP:
        r = EM_MAP.get(t, t); _cache[tok] = r; return r
    lead = "'" if t.startswith("'") else ''
    core = t.strip("'")
    suffix = ''
    if core.endswith("'s") and len(core) > 3:
        core, suffix = core[:-2], "'s"
    r = _norm_core(core)
    if lead and (lead + core) in LEX: r = lead + core
    r = r + suffix
    _cache[tok] = r
    return r

TOKRE = re.compile(r"[a-z]+(?:'[a-z]+)*'?|'[a-z]+(?:'[a-z]+)*'?")
def tokenize(text):
    """Lowercase, replace long s and curly apostrophes, split hyphens; return raw tokens (letters/apostrophes)."""
    t = text.lower().replace('ſ', 's').replace('’', "'").replace('‘', "'").replace('&', ' and ').replace('-', ' ').replace('—', ' ')
    return [x for x in TOKRE.findall(t) if not re.fullmatch(r"'+", x)]

def normalize_tokens(text):
    return [norm(x) for x in tokenize(text)]

if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        print(' '.join(normalize_tokens(line)))
