# Access notes

Network goes through a policy proxy. What works and what does not (tested with curl):

- founders.archives.gov: DIRECT ACCESS FAILS (AWS WAF JavaScript challenge, HTTP 202 empty body; headless Chromium also fails).
  USE THE WAYBACK MACHINE COPIES: `python3 code/wbfetch.py --fo Jefferson/03-01-02-0480 [outfile]`
  (or `wbfetch.py <any url> [outfile]`). Document ids are sequential in date order inside each volume:
  Jefferson Retirement Series vol. 1 = 03-01-02-NNNN (4 Mar to 15 Nov 1809), vol. 2 = 03-02-02-NNNN (16 Nov 1809 to 11 Aug 1810),
  vol. 3 = 03-03-02-NNNN (12 Aug 1810 to 17 Jun 1811), vol. 4 = 03-04-02 (18 Jun 1811 to 30 Apr 1812), vol. 6 = 03-06-02 (11 Mar to 27 Nov 1813).
  Madison Presidential Series vol. 1 = Madison/03-01-02-NNNN (1 Mar to 30 Sep 1809), vol. 2 = Madison/03-02-02-NNNN (1 Oct 1809 to 2 Nov 1810).
  A title index is at data/fo_index_ret1.tsv (ids 0470-0560 of vol. 1) and data/fo_index_ret2a.tsv (vol. 2, ids 1-120);
  `python3 code/fo_index.py <prefix> <start> <end> <out.tsv>` extends it. Be gentle: about one request per second; Wayback returns 429 when hammered (sleep and retry).
- archive.org (search API, full texts, djvu txt): works.
- Google Books API (https://www.googleapis.com/books/v1/volumes?q=...) : works; previews are sometimes readable via the "books.google.com/books?id=...&pg=...&output=text" trick, sometimes not.
- babel.hathitrust.org: 403 with plain curl; try a browser User-Agent, or the Wayback Machine, or archive.org copies of the same scan.
- lewis-clark.org, monticello.org: 403 direct; use Wayback (web.archive.org/web/2024/<url>).
- en.wikisource.org / wikipedia API: 429 when hit fast; one request every 2 s is fine.
- chroniclingamerica.loc.gov old search URLs are 404; the new API is https://www.loc.gov/collections/chronicling-america/?q=...&fo=json (test it).
- jstor.org: returns pages but article text is usually behind the login; first-page previews sometimes work via the "stable" URL; try Wayback and the author's own PDF copies.
- Prefer curl with a browser User-Agent and save the raw file next to your notes.

Save every source text you rely on under sources/ as a plain text or markdown file whose first lines give: the citation (edition, volume, page), the URL fetched, and the date fetched. Quote verbatim; mark your own summaries clearly as summaries.

## Further notes
- Founders Online documents that have enclosures or editorial notes are split into sub-ids (`…-0088-0001` letter, `…-0088-0002` enclosure; `…-0341-0001` editorial note, `-0002` letter). The parent id 404s on Wayback. Find sub-ids with the CDX API: `https://web.archive.org/cdx/search/cdx?url=founders.archives.gov/documents/<id>&matchType=prefix&output=txt&fl=original,statuscode&collapse=original` (filter out IA's occasional "Temporarily Offline" HTML with `grep -v '^<'`).
- Chronicling America: the loc.gov page JSON/OCR endpoints 429 after a few requests, but `tile.loc.gov` does not: ALTO OCR at `https://tile.loc.gov/storage-services/service/<batch path>/<lccn>/print/<yyyymmdd>01/<seq>.xml`, images via IIIF `https://tile.loc.gov/image-services/iiif/service:<batch path with colons>:<seq>/<x,y,w,h>/full/0/default.jpg` (use `curl --http1.1`). Sequence numbers run through the reel; adjacent issues can be guessed (4 pages per issue). See notes/A_documents_report.md §5 for the batch paths used.
- Google Books API quota was exhausted for the day (429); HathiTrust 403 (Cloudflare); archive.org lending-only items 401 and "search inside" 403.
