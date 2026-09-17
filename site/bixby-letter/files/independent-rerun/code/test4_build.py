"""
Test 4: assemble this implementation's own register-matched texts.

Lincoln, 1861-1865: 38 documents chosen for this implementation for their register
(condolence, ceremony, personal or elevated public prose), listed in
LINCOLN_DOCS below with the source of each text. Texts come from Basler's
Collected Works (OCR, vols IV, VII, VIII; autograph items preferred) and,
for 1862-1863 and for a few printed-only items, from Lapsley's 1905 edition
(Project Gutenberg). Long documents contribute only the head or the tail,
capped at five pieces, so that no single state paper dominates.

Hay, 1861-1865: his two war-time magazine essays, "Ellsworth" (Atlantic
Monthly, July 1861; text cut for this implementation from Project Gutenberg 11154)
and "Colonel Baker" (Harper's New Monthly Magazine, December 1861; text cut
for this implementation from the archive.org OCR of vol. 24, item harpersnew24harper);
his condolence letter of 9 June 1864 (Bullard 1946, p. 154, as transcribed
in the specials.json of The Bixby Letter); and, as a period-matched but not
register-matched set, every letter and diary entry of 1861-1865 of at
least 100 words in the hay.jsonl of The Bixby Letter (the 1908 Letters and Diary).

Pieces: sentences are accumulated until a piece holds at least 130 words;
a last fragment under 70 words is merged into the previous piece when the
result stays under 260 words, otherwise dropped.

Outputs: ../data/test4_docs.json, ../data/test4_pieces.json,
         ../data/test4_sources.csv
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ngt  # noqa: E402
from build_pools import clean_lapsley, load_jsonl  # noqa: E402

BASE = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))
SCRATCH = os.environ.get("TEST4_DOWNLOADS", os.path.normpath(os.path.join(HERE, "..", "data", "downloads")))  # the Gutenberg and archive.org texts

# (id, take, cap, label)   take = head | tail
LINCOLN_DOCS = [
    ("L5-0090", "head", 5, "Farewell address at Springfield, 11 Feb 1861 (Lapsley)"),
    ("basler-IV-0356", "head", 5, "Speech at Independence Hall, Philadelphia, 22 Feb 1861 (reported)"),
    ("L5-0128", "tail", 5, "First Inaugural Address, 4 Mar 1861, closing part (Lapsley)"),
    ("basler-IV-0617", "head", 5, "To Ephraim D. and Phoebe Ellsworth, 25 May 1861 (ALS)"),
    ("basler-IV-0931", "head", 5, "To Mrs. John C. Fremont, 12 Sep 1861 (ADfS)"),
    ("L6-0118", "head", 3, "Appeal to the border-state representatives, 12 Jul 1862 (Lapsley)"),
    ("L6-0150", "head", 5, "To Horace Greeley, 22 Aug 1862 (Lapsley)"),
    ("L6-0192", "head", 5, "Reply to a serenade, 24 Sep 1862 (Lapsley)"),
    ("L6-0232", "head", 5, "To Carl Schurz, 24 Nov 1862 (Lapsley)"),
    ("L6-0237", "tail", 5, "Annual message to Congress, 1 Dec 1862, closing part (Lapsley)"),
    ("L6-0261", "head", 5, "To Fanny McCullough, 23 Dec 1862 (Lapsley)"),
    ("L6-0288", "head", 5, "To the working-men of Manchester, 19 Jan 1863 (Lapsley)"),
    ("L6-0294", "head", 5, "To Joseph Hooker, 26 Jan 1863 (Lapsley)"),
    ("L6-0399", "tail", 4, "To Erastus Corning and others, 12 Jun 1863, closing part (Lapsley)"),
    ("L6-0440", "head", 5, "Response to a serenade, 7 Jul 1863 (Lapsley)"),
    ("L6-0481", "head", 5, "To James H. Hackett, 17 Aug 1863 (Lapsley)"),
    ("L6-0486", "tail", 5, "To James C. Conkling, 26 Aug 1863, closing part (Lapsley)"),
    ("basler-VII-0038", "head", 5, "Remarks to citizens of Gettysburg, 18 Nov 1863 (reported)"),
    ("L7-0027", "head", 5, "Gettysburg Address, 19 Nov 1863 (Lapsley)"),
    ("L7-0012", "head", 5, "To James H. Hackett, 2 Nov 1863 (Lapsley)"),
    ("basler-VII-0555", "head", 5, "Reply to New York Workingmen's Democratic Republican Association, 21 Mar 1864 (reported)"),
    ("basler-VII-0606", "head", 5, "To Albert G. Hodges, 4 Apr 1864 (ADfS)"),
    ("basler-VII-0654", "head", 5, "Address at Sanitary Fair, Baltimore, 18 Apr 1864 (AD)"),
    ("basler-VII-0765", "head", 5, "Response to Methodists, 18 May 1864 (ADS)"),
    ("L7-0172", "head", 5, "Address at the Sanitary Fair, Philadelphia, 16 Jun 1864 (Lapsley)"),
    ("basler-VII-1103", "head", 5, "Speech to the 166th Ohio Regiment, 22 Aug 1864 (reported)"),
    ("basler-VII-1153", "head", 5, "To Eliza P. Gurney, 4 Sep 1864 (ALS)"),
    ("L7-0237", "head", 5, "Reply to the loyal colored people of Baltimore, 7 Sep 1864 (Lapsley)"),
    ("basler-VIII-0182", "head", 5, "Response to a serenade, 8 Nov 1864 (reported)"),
    ("L7-0276", "head", 5, "Response to a serenade, 10 Nov 1864 (Lapsley)"),
    ("basler-VIII-0216", "head", 5, "Reply to Maryland Union Committee, 17 Nov 1864 (reported)"),
    ("basler-VIII-0334", "head", 5, "To William T. Sherman, 26 Dec 1864 (ALS)"),
    ("L7-0324", "head", 5, "Reply to a committee, 24 Jan 1865 (Lapsley)"),
    ("L7-0332", "head", 5, "Response to a serenade on the Thirteenth Amendment, 1 Feb 1865 (Lapsley)"),
    ("basler-VIII-0657", "head", 5, "Reply to notification committee, 1 Mar 1865 (AD)"),
    ("L7-0364", "head", 5, "Second Inaugural Address, 4 Mar 1865 (Lapsley)"),
    ("basler-VIII-0724", "head", 5, "To Thurlow Weed, 15 Mar 1865 (ALS)"),
    ("L7-0408", "head", 5, "Last public address, 11 Apr 1865, opening part (Lapsley)"),
]

MIN_PIECE, MERGE_UNDER, MAX_MERGED = 130, 70, 260


def cut_pieces(text, take="head", cap=None):
    sents = ngt.sentences(text, lower=False)
    pieces, buf, n = [], [], 0
    for s in sents:
        buf.append(s)
        n += len(ngt.words(s.lower()))
        if n >= MIN_PIECE:
            pieces.append(" ".join(buf))
            buf, n = [], 0
    if buf:
        if pieces and n < MERGE_UNDER and len(ngt.words(pieces[-1].lower())) + n <= MAX_MERGED:
            pieces[-1] = pieces[-1] + " " + " ".join(buf)
        elif n >= MERGE_UNDER:
            pieces.append(" ".join(buf))
    if cap:
        pieces = pieces[:cap] if take == "head" else pieces[-cap:]
    return pieces


def gutenberg_ellsworth():
    path = os.path.join(SCRATCH, "pg11154.txt")
    lines = open(path, encoding="utf-8").read().split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "ELLSWORTH.")
    end = next(i for i, ln in enumerate(lines) if "why Ellsworth died" in ln)
    body = "\n".join(lines[start + 1:end + 1])
    body = re.sub(r"\[Footnote A:.*?\]", "", body, flags=re.S)
    body = body.replace("[A]", "").replace("_", "")
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body)]
    paras = [p for p in paras if p]
    return "\n\n".join(paras)


def archive_baker():
    path = os.path.join(SCRATCH, "harpersnew24harper_djvu.txt")
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    # the essay opens "RIVERS form no less striking features ..." (p. 102-103)
    # and closes "... seeks to apologize." (p. 110); the OCR carries double
    # spaces between words and hyphenates at line ends
    start = next(i for i, ln in enumerate(lines) if re.match(r"^\s*RIVERS\s+form\s+no\s+less", ln))
    end = next(i for i in range(start, len(lines)) if re.search(r"seeks\s+to\s+apologize", lines[i]))
    raw = lines[start:end + 1]
    keep = []
    for ln in raw:
        s = ln.strip()
        if re.match(r"^(COLONEL\s+BAKER\.?|HARPER'?S\s+NEW\s+MONTHLY\s+MAGAZINE\.?)$", s):
            continue
        if re.match(r"^\d{1,4}$", s) or re.match(r"^Vol\.\s*XXIV", s):
            continue
        keep.append(s)
    # paragraphs: a blank line is a break only after a sentence end and before a capital
    paras, cur = [], []
    for i, s in enumerate(keep):
        if s == "":
            nxt = next((k for k in keep[i + 1:] if k != ""), "")
            if cur and re.search(r"[.!?][\"']?$", cur[-1]) and nxt[:1].isupper():
                paras.append(cur)
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        t = ""
        for s in p:
            if t.endswith("-"):
                t = t[:-1] + s
            else:
                t = (t + " " + s) if t else s
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"\s+([;:!?,.])", r"\1", t)
        out.append(t.strip())
    text = "\n\n".join(x for x in out if x)
    # plain OCR faults, each checked against the December-issue scan
    # (archive.org sim_harpers-magazine_1861-12_24_139)
    for bad, good in [("o^|hnies", "of armies"), ("republic-were", "republic were"), ("settle^", "settled"),
                      ("w hen", "when"), ("Keniucky", "Kentucky"), ("towrn", "town"), ("M 'Dougal", "M'Dougal"),
                      ("s;iw", "saw"), ("dying lire", "dying fire"), ("be^un", "begun"), ("ruffinnism", "ruffianism"),
                      ("tin; Gulf", "the Gulf"), ("look his life", "took his life"), ("Par more", "Far more"),
                      ("Prom all", "From all"), ("you sec", "you see"), ("Pie went", "He went"),
                      ("di imposition", "disposition"), ("awa}r", "away"), ("Edwards's Perry", "Edwards's Ferry"),
                      ("Edwards's Eerry", "Edwards's Ferry")]:
        text = text.replace(bad, good)
    text = re.sub(r"\b1 (8\d\d)\b", r"1\1", text)   # "1 835" -> "1835"
    text = re.sub(r"[\^|]", "", text)
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    basler = {d["id"]: d for d in load_jsonl(os.path.join(BASE, "corpus", "lincoln_basler.jsonl"))}
    lapsley = {d["id"]: d for d in load_jsonl(os.path.join(BASE, "analysis", "lapsley.jsonl"))}
    hay = load_jsonl(os.path.join(BASE, "corpus", "hay.jsonl"))
    with open(os.path.join(BASE, "analysis", "specials.json"), encoding="utf-8") as f:
        specials = json.load(f)

    docs, pieces, sources = [], [], []

    def add_doc(doc_id, author, group, label, source, text, take="head", cap=None):
        ps = cut_pieces(text, take, cap)
        if not ps:
            sources.append([doc_id, author, group, label, source, ngt.word_count(text), 0, "dropped: no piece of %d words" % MIN_PIECE])
            return
        segment = " ".join(ps)
        docs.append({"id": doc_id, "author": author, "group": group, "label": label, "source": source,
                     "text": segment, "words": ngt.word_count(segment), "full_words": ngt.word_count(text)})
        for k, p in enumerate(ps):
            pieces.append({"id": "%s#%d" % (doc_id, k), "doc": doc_id, "author": author, "group": group,
                           "label": label, "text": p, "words": ngt.word_count(p)})
        sources.append([doc_id, author, group, label, source, ngt.word_count(text), len(ps), "kept"])

    # Lincoln
    for doc_id, take, cap, label in LINCOLN_DOCS:
        if doc_id.startswith("basler-"):
            d = basler[doc_id]
            text = d["text"]
            source = "Basler, Collected Works, vol. %s, p. %s, source code %s (archive.org OCR via the lincoln_basler.jsonl of The Bixby Letter)" % (
                d["volume"], d["page"], d.get("source_code"))
        else:
            d = lapsley[doc_id]
            text = clean_lapsley(d["text"])
            source = "Lapsley, Writings of Abraham Lincoln (1905), vol. %s, Project Gutenberg (via the lapsley.jsonl of The Bixby Letter)" % d["volume"]
        add_doc(doc_id, "lincoln", "lincoln_matched", label, source, text, take, cap)

    # Hay: the two essays and the condolence (register-matched)
    add_doc("hay_ellsworth_1861", "hay", "hay_essay", "Ellsworth (Atlantic Monthly, July 1861)",
            "Project Gutenberg 11154, The Atlantic Monthly vol. 8 no. 45, cut for this implementation", gutenberg_ellsworth())
    add_doc("hay_baker_1861", "hay", "hay_essay", "Colonel Baker (Harper's New Monthly Magazine, December 1861)",
            "archive.org harpersnew24harper_djvu.txt, cut and lightly cleaned for this implementation", archive_baker())
    c = specials["hay_condolence_1864"]
    docs.append({"id": "hay_condolence_1864", "author": "hay", "group": "hay_condolence", "label": c["label"],
                 "source": "Bullard 1946 p. 154, as transcribed in the specials.json of The Bixby Letter",
                 "text": c["text"], "words": ngt.word_count(c["text"]), "full_words": ngt.word_count(c["text"])})
    pieces.append({"id": "hay_condolence_1864#0", "doc": "hay_condolence_1864", "author": "hay",
                   "group": "hay_condolence", "label": c["label"], "text": c["text"], "words": ngt.word_count(c["text"])})
    sources.append(["hay_condolence_1864", "hay", "hay_condolence", c["label"], "Bullard 1946 p. 154 via specials.json",
                    ngt.word_count(c["text"]), 1, "kept (55 words, under the piece minimum)"])
    # Hay: letters and diary entries of 1861-1865 (period-matched)
    for d in hay:
        if d.get("period") == "civil_war" and d.get("kind") in ("letter", "diary") and d.get("word_count", 0) >= 100:
            label = "%s, %s (%s)" % (d.get("heading", "").strip() or d["kind"], d.get("date") or d.get("year"), d["kind"])
            add_doc(d["id"], "hay", "hay_letters_diary_1861_65", label,
                    "Letters of John Hay and Extracts from Diary (1908), vol. %s (archive.org OCR via the hay.jsonl of The Bixby Letter)" % d.get("volume"),
                    d["text"], "head", 2)

    with open(os.path.join(OUT, "test4_docs.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "test4_pieces.json"), "w", encoding="utf-8") as f:
        json.dump(pieces, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "test4_sources.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "author", "group", "label", "source", "words_in_source", "pieces", "status"])
        w.writerows(sources)
    from collections import Counter
    print("docs:", Counter(d["group"] for d in docs))
    print("pieces:", Counter(p["group"] for p in pieces))
    for g in sorted(set(d["group"] for d in docs)):
        print(g, "words used:", sum(d["words"] for d in docs if d["group"] == g))


if __name__ == "__main__":
    main()
