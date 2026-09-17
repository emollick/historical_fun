#!/usr/bin/env python3
"""Fetch a page through the Wayback Machine (latest capture) and print or save its text.

Usage:
  python3 wbfetch.py URL [outfile]           # latest capture, text extracted
  python3 wbfetch.py --raw URL [outfile]     # save the raw archived HTML
  python3 wbfetch.py --fo Jefferson/03-01-02-0480 [outfile]   # Founders Online shorthand

Why: founders.archives.gov sits behind an AWS WAF JavaScript challenge that curl and
headless Chromium cannot pass through the proxy; the Wayback Machine holds
copies of nearly every document page, and those are served plain.
"""
import sys, re, html, urllib.request, urllib.parse, json, time

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def get(url, tries=4, timeout=90):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (i + 1))
    raise last

def latest_capture(url):
    q = "https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")
    j = json.loads(get(q).decode("utf-8", "ignore"))
    snap = j.get("archived_snapshots", {}).get("closest")
    return snap["url"] if snap else None

def to_text(raw):
    t = raw.decode("utf-8", "ignore")
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<(br|p|div|li|h\d|tr)[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

def founders_text(t):
    """Trim Wayback/Founders chrome to the document body plus the citation block."""
    m = re.search(r"\[ Back to normal view \](.*?)(NHPRC|The National Historical Publications)", t, flags=re.S)
    body = m.group(1) if m else t
    body = re.sub(r"^\s*(Thomas Jefferson Papers|Permanent Link view|Start New Search|View Previous Searches|Print View|Max Page View|Normal Page View|Share|Email This|Share this on Facebook|\+1 this on Google|Tweet)\s*$", "", body, flags=re.M)
    body = re.sub(r"\n\s*\n+", "\n", body)
    return body.strip()

def main():
    args = sys.argv[1:]
    raw = False
    if args and args[0] == "--raw":
        raw = True; args = args[1:]
    fo = False
    if args and args[0] == "--fo":
        fo = True; args = args[1:]
        args[0] = "https://founders.archives.gov/documents/" + args[0]
    url = args[0]
    out = args[1] if len(args) > 1 else None
    # The availability API rate-limits quickly (429); the timestamp-redirect form is
    # reliable and returns the nearest capture, so use it directly.
    cap = "https://web.archive.org/web/2024id_/" + url if raw else "https://web.archive.org/web/2024/" + url
    data = get(cap)
    if raw:
        content = data
        if out:
            open(out, "wb").write(content)
        else:
            sys.stdout.buffer.write(content)
        return
    t = to_text(data)
    if fo or "founders.archives.gov" in url:
        t = founders_text(t)
    t = "SOURCE CAPTURE: " + cap + "\nORIGINAL URL: " + url + "\n\n" + t
    if out:
        open(out, "w", encoding="utf-8").write(t)
        print("wrote", out, len(t), "chars")
    else:
        print(t)

if __name__ == "__main__":
    main()
