#!/usr/bin/env python3
"""Copy the working folders of the cases into cases/.

The working folders live outside the repository, one folder per case, under the directory named by the
environment variable CASES_SRC (default: ../mysteries). This script copies each folder into cases/<slug>/,
leaving out Python caches, the files listed in sources_left_out.csv and any file over 95 MB (GitHub's
limit is 100 MB); skipped large files are listed in cases/<slug>/NOT_IN_REPO.md.
    python3 sync_cases.py                # all folders present at the source
    python3 sync_cases.py pied-piper     # one folder
"""
import os, shutil, sys
from pathlib import Path

SRC = Path(os.environ.get("CASES_SRC", "../mysteries"))
REPO_CAP = 95_000_000   # bytes; GitHub refuses files over 100 MB, so larger files are listed in NOT_IN_REPO.md instead
# Files that stay out of the public repository: copies of works still in copyright (and one fictitious paper), listed with
# their sources in sources_left_out.csv and SOURCES_LEFT_OUT.md at the repository root.  A re-sync leaves them out again.
def _left_out():
    out = {}
    listing = Path(__file__).resolve().parent / "sources_left_out.csv"
    if listing.exists():
        import csv
        with listing.open(newline="") as f:
            for row in csv.DictReader(f):
                _, slug, rel = row["path"].split("/", 2)
                out.setdefault(slug, set()).add(rel)
    out.setdefault("smenkhkare", set()).update({"sources/miskatonic2025_reevaluating_amarna.pdf",   # a fictitious paper found during the
                                                 "sources/miskatonic2025_reevaluating_amarna.txt"})  # search; the case README says so
    return out
LEFT_OUT = _left_out()
DST = Path(__file__).resolve().parent / "cases"
slugs = sys.argv[1:] or sorted(p.name for p in SRC.iterdir() if p.is_dir())
for slug in slugs:
    src, dst = SRC / slug, DST / slug
    if not src.is_dir():
        print(f"{slug}: not found at {src}"); continue
    if dst.exists(): shutil.rmtree(dst)
    skipped = []
    def ignore(d, names):
        out = set(shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")(d, names))
        for n in names:
            f = Path(d) / n
            if f.is_file() and f.stat().st_size > REPO_CAP:
                out.add(n); skipped.append((f.relative_to(src), f.stat().st_size))
            if str(f.relative_to(src)) in LEFT_OUT.get(slug, ()):
                out.add(n)
        return out
    shutil.copytree(src, dst, ignore=ignore)
    if skipped:
        lines = ["# Files kept out of the repository", "",
                 f"GitHub rejects files over 100 MB, so these files from the case's working folder were not copied. "
                 "Each is a public dataset or download the notes in this folder identify.", ""]
        lines += [f"- `{rel}` ({size / 1e6:.0f} MB)" for rel, size in skipped]
        (dst / "NOT_IN_REPO.md").write_text("\n".join(lines) + "\n")
        for rel, size in skipped: print(f"{slug}: skipped {rel} ({size / 1e6:.0f} MB, over the repository cap)")
    n = sum(len(f) for _, _, f in __import__("os").walk(dst))
    print(f"{slug}: {n} files")
