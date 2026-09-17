"""Delta, character n-gram classifier and impostors on the own-hand design.
Outputs results/other/<name>.json with validation accuracies on short known texts
and scores for the Bixby letter and the special texts."""
import sys, os, json, random, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designs, delta, clf, impostors
from ngt import word_count, sentences, word_tokens
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results', 'other'); os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(0)

def chunk(text, size=160):
    toks = text.split()
    return [' '.join(toks[i:i+size]) for i in range(0, len(toks), size) if len(toks[i:i+size]) >= 60]

def build(design='ownhand', lo=50, hi=400, controls=True):
    L = designs.load_lincoln(); H = designs.load_hay(); C = designs.load_controls() if controls else []
    if design == 'ownhand':
        lin = designs.lincoln_war_own(L); hay = designs.hay_war(H)
    elif design == 'ownhand_all':
        lin = [r for r in L if r['autograph'] and not r['hay_hand']]; hay = H
    elif design == 'grieve':
        lin = designs.lincoln_pre1860(L); hay = H
    excluded = set(designs.get(design)['excluded'])  # register parents and copies of test texts
    lin = [r for r in lin if r['id'] not in excluded]; hay = [r for r in hay if r['id'] not in excluded]
    docs = []  # (id, text, label, group)
    for r in lin:
        if lo <= r['wc'] <= hi: docs.append((r['id'], r['text'], 'lincoln', r['id']))
        elif r['wc'] > hi:
            for k, c in enumerate(chunk(r['text'])): docs.append((f"{r['id']}#{k}", c, 'lincoln', r['id']))
    for r in hay:
        if lo <= r['wc'] <= hi: docs.append((r['id'], r['text'], 'hay', r['id']))
        elif r['wc'] > hi:
            for k, c in enumerate(chunk(r['text'])): docs.append((f"{r['id']}#{k}", c, 'hay', r['id']))
    for r in C:
        auth = r.get('author') or 'control'
        if lo <= r['wc'] <= hi: docs.append((r['id'], r['text'], 'control:' + auth, r['id']))
        elif r['wc'] > hi:
            for k, c in enumerate(chunk(r['text'])): docs.append((f"{r['id']}#{k}", c, 'control:' + auth, r['id']))
    extra = {'lincoln_war_other': designs.lincoln_war_other(L), 'hay_hand': designs.lincoln_hay_hand(L)}
    return docs, extra

def grouped_folds(docs, n=5, seed=0):
    groups = sorted({g for _, _, _, g in docs}); r = random.Random(seed); r.shuffle(groups)
    fold_of = {g: i % n for i, g in enumerate(groups)}
    return [fold_of[g] for _, _, _, g in docs]

def run_delta(docs, specials, extra, k=150):
    texts = [t for _, t, _, _ in docs]; labels = [l.split(':')[0] for _, _, l, _ in docs]
    folds = grouped_folds(docs)
    res = {'val': [], 'specials': {}, 'extra': {}}
    def fit(train_idx):
        vocab = delta.build_vocab([texts[i] for i in train_idx], k)
        X = np.array([delta.rel_freq(texts[i], vocab) for i in train_idx])
        mu = X.mean(0); sd = X.std(0)
        Z = delta.zscores(X, mu, sd)
        cents = {}
        for lab in set(labels[i] for i in train_idx):
            idx = [j for j, i in enumerate(train_idx) if labels[i] == lab]
            cents[lab] = Z[idx].mean(0)
        return vocab, mu, sd, cents
    def score(text, model):
        vocab, mu, sd, cents = model
        z = delta.zscores(delta.rel_freq(text, vocab), mu, sd)
        return {lab: {'burrows': float(delta.burrows_delta(z, c)), 'cosine': float(delta.cosine_delta(z, c))} for lab, c in cents.items()}
    for f in range(5):
        tr = [i for i in range(len(docs)) if folds[i] != f]; te = [i for i in range(len(docs)) if folds[i] == f]
        model = fit(tr)
        for i in te:
            s = score(texts[i], model)
            res['val'].append({'id': docs[i][0], 'truth': labels[i], 'words': word_count(texts[i]), 'scores': s})
    model = fit(list(range(len(docs))))
    for k_, t, a in specials: res['specials'][k_] = {'truth': a, 'scores': score(t, model)}
    for name, recs in extra.items():
        res['extra'][name] = [{'id': r['id'], 'words': r['wc'], 'scores': score(r['text'], model)} for r in recs if 50 <= r['wc'] <= 400]
    return res

def run_clf(docs, specials, extra, analyzer='char', ngram=(3, 5), two_class=True, C=1.0, strip_punct=False):
    texts = [clf.norm(t, strip_punct) for _, t, _, _ in docs]
    labels = np.array([l.split(':')[0] if two_class else l for _, _, l, _ in docs])
    if two_class:
        keep = [i for i in range(len(docs)) if labels[i] in ('lincoln', 'hay')]
        texts = [texts[i] for i in keep]; labels = labels[keep]; docs_k = [docs[i] for i in keep]
    else:
        docs_k = docs
    folds = grouped_folds(docs_k)
    classes = sorted(set(labels))
    probs = np.zeros((len(texts), len(classes)))
    def mk(): return make_pipeline(TfidfVectorizer(analyzer=analyzer, ngram_range=ngram, min_df=2, sublinear_tf=True, lowercase=False),
                                   LogisticRegression(C=C, max_iter=3000, class_weight='balanced'))
    for f in range(5):
        tr = [i for i in range(len(texts)) if folds[i] != f]; te = [i for i in range(len(texts)) if folds[i] == f]
        p = mk(); p.fit([texts[i] for i in tr], labels[tr])
        pr = p.predict_proba([texts[i] for i in te]); cols = list(p.classes_)
        for j, c in enumerate(classes): probs[te, j] = pr[:, cols.index(c)]
    res = {'classes': classes, 'val': [{'id': docs_k[i][0], 'truth': str(labels[i]), 'words': word_count(docs_k[i][1]), 'probs': probs[i].tolist()} for i in range(len(texts))]}
    p = mk(); p.fit(texts, labels); cols = list(p.classes_)
    def prob(t):
        pr = p.predict_proba([clf.norm(t, strip_punct)])[0]
        return {c: float(pr[cols.index(c)]) for c in classes}
    res['specials'] = {k: {'truth': a, 'probs': prob(t)} for k, t, a in specials}
    res['extra'] = {name: [{'id': r['id'], 'words': r['wc'], 'probs': prob(r['text'])} for r in recs if 50 <= r['wc'] <= 400] for name, recs in extra.items()}
    return res

def run_impostors(docs, specials, extra, K=100, ngram=(4, 4), max_features=8000, n_val=200):
    texts = [t for _, t, _, _ in docs]; labels = [l for _, _, l, _ in docs]
    base = [l.split(':')[0] for l in labels]
    cv, X = impostors.vectorize(texts, ngram=ngram, max_features=max_features)
    def vec(t):
        v = cv.transform([impostors.norm(t)]).astype(float).toarray()[0]
        return v / max(v.sum(), 1)
    idx = {lab: [i for i in range(len(docs)) if base[i] == lab] for lab in ('lincoln', 'hay')}
    ctrl = [i for i in range(len(docs)) if base[i] == 'control']
    r = np.random.default_rng(0)
    def scores(v, exclude=None):
        out = {}
        for cand in ('lincoln', 'hay'):
            cand_idx = [i for i in idx[cand] if i != exclude]
            other = [i for i in idx['hay' if cand == 'lincoln' else 'lincoln'] if i != exclude]
            imp = X[ctrl + other] if ctrl else X[other]
            out[cand] = impostors.gi_score(v, X[cand_idx], imp, r, K=K)
        return out
    res = {'val': [], 'specials': {}, 'extra': {}}
    val_idx = list(r.choice(idx['lincoln'], size=min(n_val, len(idx['lincoln'])), replace=False)) + list(r.choice(idx['hay'], size=min(n_val, len(idx['hay'])), replace=False))
    for i in val_idx:
        res['val'].append({'id': docs[i][0], 'truth': base[i], 'words': word_count(texts[i]), 'scores': scores(X[i], exclude=i)})
    for k, t, a in specials: res['specials'][k] = {'truth': a, 'scores': scores(vec(t))}
    for name, recs in extra.items():
        res['extra'][name] = [{'id': rr['id'], 'words': rr['wc'], 'scores': scores(vec(rr['text']))} for rr in recs if 50 <= rr['wc'] <= 400][:150]
    return res

if __name__ == '__main__':
    design = sys.argv[1] if len(sys.argv) > 1 else 'ownhand'
    which = sys.argv[2].split(',') if len(sys.argv) > 2 else ['delta', 'clf', 'imp']
    docs, extra = build(design, controls=os.path.exists(os.path.join(designs.corpus.ROOT, "controls.jsonl")))
    specials = designs.specials()
    reg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'register.json')
    if os.path.exists(reg_path):
        specials += [('reg:' + k, v['text'], v['author']) for k, v in json.load(open(reg_path)).items()]
    import collections
    print('docs', collections.Counter(l for _, _, l, _ in docs))
    if 'delta' in which:
        r = run_delta(docs, specials, extra); json.dump(r, open(os.path.join(OUT, f'delta_{design}.json'), 'w')); print('delta done')
    if 'clf' in which:
        for tag, kw in [('char35', dict(analyzer='char', ngram=(3, 5))), ('char35_nopunct', dict(analyzer='char', ngram=(3, 5), strip_punct=True)), ('word12', dict(analyzer='word', ngram=(1, 2)))]:
            r = run_clf(docs, specials, extra, **kw); json.dump(r, open(os.path.join(OUT, f'clf_{tag}_{design}.json'), 'w')); print('clf', tag, 'done')
        r = run_clf(docs, specials, extra, two_class=False); json.dump(r, open(os.path.join(OUT, f'clf_multi_{design}.json'), 'w')); print('clf multi done')
    if 'imp' in which:
        r = run_impostors(docs, specials, extra); json.dump(r, open(os.path.join(OUT, f'imp_{design}.json'), 'w')); print('imp done')
