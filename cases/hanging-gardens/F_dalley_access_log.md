# F_dalley_access_log.md — every route tried for Dalley 1994, Dalley 2013 and Reade 2000

Network: all HTTPS through a proxy; TLS verification never disabled. No Sci-Hub/LibGen/Z-Library-type sources were used. Retry policy: one retry on transient failure, then Wayback `id_` form, then move on; proxy policy denials (403/407) not retried.

## 0. Outcome in one paragraph

Dalley 1994 (Iraq 56): full text NOT obtained — Cambridge Core and JSTOR closed, no open copy anywhere; obtained the Cambridge Extract (opening paragraphs), all 75 footnotes, JSTOR/BISI metadata, and 45 page-keyed quotations/paraphrases via Bichler & Rollinger 2005 (F_dalley_1994.txt). Dalley 2013 (OUP book): full text NOT obtained (not open access; IA lending copy restricted); obtained TOC, chapter page ranges, 236 page-numbered Google Books snippets, 39 reconstructed passages and c. 1,300 short OCR fragments from the Internet Archive full-text index (F_dalley_2013.txt). Reade 2000 (Iraq 62): Extract + reference list only. Fully obtained instead: Dalley 1993 (Garden History), Dalley 2008 (SAOC 62), Dalley & Oleson 2003, Dalley 2017 (Sidestone chapter), Dalley's OUPblog/PBS/NatGeo statements, the CSMC 2018 report, and two long reviews in full — Bagg, BiOr 71 (2014) and Potts, NYRB 2013 — plus the opening of Holland's Literary Review piece (F_dalley_other.md).

## 1. HTTP fetch log (single-URL fetches)

| name | URL | HTTP | bytes | content-type | result |
|---|---|---|---|---|---|
| cc_dalley1994_abs | https://www.cambridge.org/core/journals/iraq/article/abs/nineveh-babylon-and-the-hanging-gardens-cuneiform-and-classical-sources-reconciled1/C024A9417036B87AB6D772A98274E0D0 | 200 | 969735 | text/html | Article page: Extract + all 75 footnotes exposed; body/PDF closed ('Access options': purchase/subscribe). |
| cc_dalley1994_full | https://www.cambridge.org/core/journals/iraq/article/nineveh-babylon-and-the-hanging-gardens-cuneiform-and-classical-sources-reconciled1/C024A9417036B87AB6D772A98274E0D0 | 200 | 969735 | text/html | Redirects to the /abs/ page (no HTML full text without access). |
| doi_dalley1994 | https://doi.org/10.2307/4200384 | 200 | 969732 | text/html | DOI resolves to the Cambridge abstract page. |
| jstor_4200384 | https://www.jstor.org/stable/4200384 | 200 | 3038 | text/html | JSTOR live page returns a 3 kB bot-check shell. |
| wb_jstor_4200384 | https://web.archive.org/web/2024id_/https://www.jstor.org/stable/4200384 | 200 | 12182 | text/html | Wayback 2024 capture: bot-check shell only. |
| s2_dalley1994 | https://api.semanticscholar.org/graph/v1/paper/DOI:10.2307/4200384?fields=title,openAccessPdf,externalIds,isOpenAccess,citationCount | 404 | 56 | application/json | Semantic Scholar has no record for the DOI (404). |
| unpaywall_dalley1994 | https://api.unpaywall.org/v2/10.2307/4200384?email=research@example.org | 200 | 754 | application/json | is_oa=false, no OA locations. |
| openalex_dalley1994 | https://api.openalex.org/works/doi:10.2307/4200384 | 200 | 10854 | application/json | Work record; open_access.is_oa=false; no PDF URL. |
| cc_dalley1994_pdf | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C024A9417036B87AB6D772A98274E0D0/S0021088900002801a.pdf/div-class-title-nineveh-babylon-and-the-hanging-gardens-cuneiform-and-classical-sources-reconciled-a-href-fn01-ref-type-fn-span-class-sup-1-span-a-div.pdf | 200 | 970153 | text/html | citation_pdf_url returns the HTML abstract page instead of the PDF (no access). |
| wb_cc_dalley1994_pdf | https://web.archive.org/web/2024id_/https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C024A9417036B87AB6D772A98274E0D0/S0021088900002801a.pdf/div-class-title-nineveh-babylon-and-the-hanging-gardens-cuneiform-and-classical-sources-reconciled-a-href-fn01-ref-type-fn-span-class-sup-1-span-a-div.pdf | 200 | 989001 | text/html | Wayback has only a 2025 capture of the redirect target (abstract page), not the PDF. |
| gb_isbn_hb | https://www.googleapis.com/books/v1/volumes?q=isbn:9780199662265 | 429 | 1306 | application/json | Google Books API quota exhausted (429). |
| gb_isbn_pb | https://www.googleapis.com/books/v1/volumes?q=isbn:9780198728849 | 429 | 1306 | application/json | 429. |
| gb_intitle | https://www.googleapis.com/books/v1/volumes?q=intitle:%22Mystery+of+the+Hanging+Garden+of+Babylon%22&maxResults=10 | 429 | 1306 | application/json | 429. |
| ia_search_book | https://archive.org/advancedsearch.php?q=title%3A%28%22Hanging+Garden%22%29+AND+creator%3A%28Dalley%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=date&fl%5B%5D=mediatype&fl%5B%5D=collection&rows=50&output=json | 200 | 1152 | application/json | archive.org: the lending copy only. |
| ia_search_dalley | https://archive.org/advancedsearch.php?q=Dalley+AND+%28%22Hanging+Gardens%22+OR+%22Hanging+Garden%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=date&fl%5B%5D=mediatype&fl%5B%5D=collection&rows=100&output=json | 200 | 2015 | application/json | archive.org: only the 1993 Garden History scan (dalley-1993-hanging-gardens) and the 2013 lending copy. |
| ia_search_iraq56 | https://archive.org/advancedsearch.php?q=%22Nineveh%2C+Babylon+and+the+Hanging+Gardens%22&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=date&fl%5B%5D=mediatype&rows=50&output=json | 200 | 442 | application/json | archive.org advancedsearch: no item for the article title. |
| scholar_ia_1994 | https://scholar.archive.org/search?q=%22Nineveh%2C+Babylon+and+the+Hanging+Gardens%22 | 200 | 470 | text/html | scholar.archive.org returns a 470 B JS shell (no results renderable). |
| scholar_ia_dalley | https://scholar.archive.org/search?q=Dalley+%22Hanging+Gardens%22 | 200 | 470 | text/html |  |
| hathi_1994title | https://babel.hathitrust.org/cgi/ls?q1=%22Nineveh%2C+Babylon+and+the+Hanging+Gardens%22;anyall1=phrase;lmt=ft | 403 | 6007 | text/html | HathiTrust full-text search blocked (403) by the proxy/policy. |
| hathi_book | https://catalog.hathitrust.org/api/volumes/brief/isbn/9780199662265.json | 200 | 31 | application/json | HathiTrust: no record for the ISBN. |
| ol_search | https://openlibrary.org/search.json?q=Mystery+of+the+Hanging+Garden+of+Babylon&fields=key,title,author_name,isbn,ia,lending_edition_s,ebook_access,public_scan_b,edition_key | 200 | 4620 | application/json | Open Library: edition OL25987675M, ia mysteryofhanging0000dall, lending only (ebook_access 'borrowable'). |
| doi_reade2000 | https://doi.org/10.2307/4200490 | 200 | 905213 | text/html | Reade 2000: Cambridge abstract page (Extract + 62 references); PDF closed. |
| cc_iraq_vol56 | https://www.cambridge.org/core/journals/iraq/volume/56 | 404 | 653106 | text/html |  |
| oup_global | https://global.oup.com/academic/product/the-mystery-of-the-hanging-garden-of-babylon-9780199662265 | 202 | 2003 | text/html | Live OUP page returns a 202 bot-check shell. |
| ora_search | https://ora.ox.ac.uk/catalog?q=Dalley+Hanging+Gardens | 404 | 22185 | text/html | ORA (Oxford Research Archive): no deposit by Dalley on the subject (404 page/no results). |
| core_api | https://api.core.ac.uk/v3/search/works?q=%22Hanging+Gardens%22+Dalley+Nineveh&limit=10 | 200 | 19949 | application/json | CORE search: only unrelated works; no copy of the article. |
| openalex_dalley_hg | https://api.openalex.org/works?search=Dalley%20Hanging%20Gardens%20Nineveh&per-page=25 | 429 | 350 | application/json | 429 (rate-limited). |
| ia_meta_book | https://archive.org/metadata/mysteryofhanging0000dall | 200 | 14901 | application/json | IA metadata: access-restricted-item true; collections inlibrary/printdisabled; 322 images. |
| ol_inside_test1 | https://openlibrary.org/search/inside.json?q=%22Nineveh+was+called+Babylon%22 | 200 | 891 | application/json | Open Library search-inside works (returns highlight fragments from the lending copy). |
| ol_inside_test2 | https://openlibrary.org/search/inside.json?q=alamittu | 200 | 39568 | application/json | Same (alamittu hits). |
| gb_vid | https://books.google.com/books?vid=ISBN9780199662265 | 403 | 1103 | text/html | books.google.com blocked (403) for direct page/preview requests. |
| gb_feeds | https://www.google.com/books/feeds/volumes?q=isbn:9780199662265 | 200 | 3465 | application/atom+xml | Google Books GData feed works: identifies volume id 7HUZYru5UiIC (hb) and 6IUivLRnGC0C (pb). |
| wb_oup_global | https://web.archive.org/web/2024id_/https://global.oup.com/academic/product/the-mystery-of-the-hanging-garden-of-babylon-9780199662265 | 200 | 100700 | text/html | Wayback 2016 capture of the OUP product page: description, TOC, author info, review quotes. |
| oxacad_doi | https://doi.org/10.1093/acprof:oso/9780199662265.001.0001 | 404 | 10646 | text/html | No Oxford Scholarship Online/Oxford Academic edition exists (404). |
| ora_search2 | https://ora.ox.ac.uk/catalog?utf8=%E2%9C%93&q=Dalley+Hanging+Garden&search_field=all_fields | 404 | 22204 | text/html | Same. |
| ora_json | https://ora.ox.ac.uk/catalog.json?q=Dalley+Hanging+Garden | 500 | 182 | text/plain | ORA JSON endpoint 500. |
| bmcr_search | https://bmcr.brynmawr.edu/?s=Dalley+Hanging+Garden | 200 | 54396 | text/html | BMCR site search: no review of the book. |
| oxpod_search | https://podcasts.ox.ac.uk/search/node?keys=Dalley+Hanging | 404 | 21607 | text/html | podcasts.ox.ac.uk search: 404 (no HG lecture podcast). |
| oxpod_person | https://podcasts.ox.ac.uk/people/stephanie-dalley | 200 | 27692 | text/html | No Dalley podcasts listed. |
| s2_search_1994 | https://api.semanticscholar.org/graph/v1/paper/search?query=Nineveh%20Babylon%20Hanging%20Gardens%20cuneiform%20classical%20sources%20reconciled&fields=title,year,openAccessPdf,externalIds&limit=10 | 429 | 144 | text/html | Rate-limited (429). |
| s2_search_book | https://api.semanticscholar.org/graph/v1/paper/search?query=Mystery%20of%20the%20Hanging%20Garden%20of%20Babylon%20Dalley&fields=title,year,openAccessPdf,externalIds&limit=10 | 429 | 144 | text/html | 429. |
| crossref_chapters | https://api.crossref.org/works?query.bibliographic=Mystery+of+the+Hanging+Garden+of+Babylon+Dalley&filter=type:book-chapter&rows=40&select=DOI,title,container-title,page,URL | 200 | 8557 | application/json | Crossref: no chapter DOIs. |
| crossref_book | https://api.crossref.org/works?query.bibliographic=Mystery+of+the+Hanging+Garden+of+Babylon+Dalley&filter=type:book,type:monograph&rows=10&select=DOI,title,ISBN,publisher,URL | 200 | 2312 | application/json | Crossref: no DOI registered for the book. |
| hathi_issn | https://catalog.hathitrust.org/api/volumes/brief/issn/0021-0889.json | 200 | 4838 | application/json | HathiTrust catalogue: Iraq (ISSN 0021-0889) volumes are search-only, not full view. |
| wb_jstor_pdf | https://web.archive.org/web/2024id_/https://www.jstor.org/stable/pdf/4200384.pdf | 404 | 4614 | text/html | No Wayback capture of the JSTOR PDF (404). |
| cdx_jstor | https://web.archive.org/cdx/search/cdx?url=jstor.org/stable/4200384*&output=json&limit=60 | 503 | 11832 | text/html | 503 on first try; see cdx_jstor2. |
| cdx_cc | https://web.archive.org/cdx/search/cdx?url=cambridge.org/core/services/aop-cambridge-core/content/view/C024A9417036B87AB6D772A98274E0D0*&output=json&limit=60 | 200 | 4555 | application/json | CDX: captures exist only for the article HTML, none for the /services/aop-cambridge-core/content/view/... PDF. |
| lrb_search | https://www.lrb.co.uk/search-results?search=Dalley+Hanging+Gardens | 200 | 244062 | text/html | LRB search: no review. |
| tls_search | https://www.the-tls.co.uk/?s=Dalley+Hanging+Garden | 200 | 1337 | text/html | TLS search: nothing (1 kB shell). |
| litrev_holland | https://literaryreview.co.uk/by-the-rivers-of-nineveh | 200 | 74668 | text/html | Literary Review page: opening paragraphs only; rest paywalled. |
| ia_search_vols | https://archive.org/advancedsearch.php?q=title%3A%28%22Of+Pots+and+Plans%22%29+OR+title%3A%28%22Assyrien+im+Wandel+der+Zeiten%22%29+OR+title%3A%28%22Proceedings+of+the+51st+Rencontre%22%29+OR+title%3A%28%22Iraq%22+AND+%22British+School+of+Archaeology%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=date&rows=50&output=json | 200 | 914 | application/json | archive.org: no scans of Of Pots and Plans, HSAO 6 or RAI 51 volumes; some Iraq volumes are in the lending library only. |
| wb2020_cc_pdf | https://web.archive.org/web/20200326100031id_/https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C024A9417036B87AB6D772A98274E0D0/S0021088900002801a.pdf/div-class-title-nineveh-babylon-and-the-hanging-gardens-cuneiform-and-classical-sources-reconciled-a-href-fn01-ref-type-fn-span-class-sup-1-span-a-div.pdf | 200 | 246108 | text/html | Wayback 2020 capture of the article URL = HTML abstract page (246 kB), no PDF. |
| gb_feeds_vol | https://www.google.com/books/feeds/volumes/7HUZYru5UiIC | 200 | 3886 | application/atom+xml | Volume feed for 7HUZYru5UiIC (viewability: partial preview). |
| gb_feeds_q1 | https://www.google.com/books/feeds/volumes?q=alamittu+inauthor:Dalley | 200 | 5167 | application/atom+xml | inauthor: query returns the book with its blurb, no snippet. |
| gb_feeds_q2 | https://www.google.com/books/feeds/volumes?q=%22Nineveh+was+called+Babylon%22 | 200 | 5967 | application/atom+xml | Phrase query: snippet with page anchor returned. |
| gb_feeds_q3 | https://www.google.com/books/feeds/volumes/7HUZYru5UiIC?q=alamittu | 200 | 3886 | application/atom+xml | Volume-scoped q= returns the volume entry, no snippet. |
| crossref_isbn | https://api.crossref.org/works?filter=isbn:9780199662265&rows=20&select=DOI,title,container-title,page,URL,type | 200 | 187 | application/json | Crossref: nothing under either ISBN. |
| crossref_isbn_pb | https://api.crossref.org/works?filter=isbn:9780198728849&rows=20&select=DOI,title,container-title,page,URL,type | 200 | 187 | application/json | Same. |
| oxacad_search | https://academic.oup.com/search-results?q=%22Hanging%20Garden%20of%20Babylon%22%20Dalley | 403 | 5866 | text/html | academic.oup.com search blocked (403). |
| cdx_jstor2 | https://web.archive.org/cdx/search/cdx?url=jstor.org/stable/4200384&output=json&limit=60 | 200 | 4012 | application/json | CDX list of captures of the JSTOR item page (used to pick the 2018 capture). |
| cdx_jstor_reade | https://web.archive.org/cdx/search/cdx?url=jstor.org/stable/4200490&output=json&limit=60 | 200 | 3856 | application/json | CDX captures of JSTOR 4200490 item page only. |
| babel_pt_search_test | https://babel.hathitrust.org/cgi/pt/search?q1=Hanging+Gardens;id=mdp.39015008413463 | 403 | 5887 | text/html | HathiTrust page-search blocked (403). |
| inside_alt_server | https://dn720001.ca.archive.org/fulltext/inside.php?item_id=mysteryofhanging0000dall&doc=mysteryofhanging0000dall&path=/0/items/mysteryofhanging0000dall&q=alamittu | 404 | 146 | text/html | dn720001.ca.archive.org inside.php: 404. |
| inside_d2_server | https://ia801407.us.archive.org/fulltext/inside.php?item_id=mysteryofhanging0000dall&doc=mysteryofhanging0000dall&path=/9/items/mysteryofhanging0000dall&q=alamittu | 403 | 4868 | text/html | ia801407.us.archive.org inside.php: 403. |
| inside_generic | https://archive.org/fulltext/inside.php?item_id=mysteryofhanging0000dall&doc=mysteryofhanging0000dall&path=/9/items/mysteryofhanging0000dall&q=alamittu | 404 | 4963 | text/html | archive.org/fulltext/inside.php: 404 'item not available'. |
| ol_inside_amytis | https://openlibrary.org/search/inside.json?q=%22Amytis%22+Sennacherib | 200 | 59241 | application/json | Same. |
| gg_searchwithin | https://www.google.com/books?id=7HUZYru5UiIC&jscmd=SearchWithin&q=alamittu | 403 | 1103 | text/html | 403. |
| gg_pa66_text | https://www.google.com/books?id=7HUZYru5UiIC&pg=PA66&output=text | 403 | 1103 | text/html | 403 (no page text via output=text). |
| gb_feeds_vol2 | https://www.google.com/books/feeds/volumes/6IUivLRnGC0C | 200 | 3747 | application/atom+xml | Volume feed for 6IUivLRnGC0C. |
| gb_feeds_q4 | https://www.google.com/books/feeds/volumes?q=%22Tashmetu-sharrat%22 | 200 | 12846 | application/atom+xml | Snippets with page numbers (Tashmetu-sharrat -> p. 145). |
| gb_feeds_q5 | https://www.google.com/books/feeds/volumes?q=%22kirimahu%22 | 200 | 23994 | application/atom+xml | Snippets (kirimahu). |
| cc_reade2000_pdf | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6D7FD83FF93A9BCF77A0F852C430E7C2/S0021088900006318a.pdf/div-class-title-alexander-the-great-and-the-hanging-gardens-of-babylon-div.pdf | 200 | 905631 | text/html | citation_pdf_url returns the HTML abstract page (no access). |
| oupblog_2013 | https://blog.oup.com/2013/06/mystery-hanging-garden-babylon/ | 200 | 63543 | text/html | Dalley's OUPblog essay, full text saved. |
| pbs_qa | https://www.pbs.org/wnet/secrets/the-lost-gardens-of-babylon-qa-with-dr-stephanie-dalley-tv-host-author-of-lost-gardens-of-babylon/1172/ | 200 | 63584 | text/html | PBS Q&A, full text saved. |
| isac_lecture | https://isac.uchicago.edu/article/lecture-stephanie-dalley-hanging-garden-babylon-elusive-world-wonder-traced | 200 | 22539 | text/html | Lecture abstract saved. |
| yale_lecture | https://archaia.yale.edu/node/137 | 200 | 25843 | text/html | Yale event page (redirect). |
| orinst_dalley | https://www.orinst.ox.ac.uk/people/stephanie-m-dalley | 200 | 151927 | text/html | Oxford faculty profile (current projects; no HG paper deposits). |
| goodreads_blog | https://www.goodreads.com/author_blog_posts/4443052-demystifying-the-hanging-garden-of-babylon | 200 | 76711 | text/html | Syndicated copy of the OUPblog video interview post. |
| natgeo_2013 | https://www.nationalgeographic.com/science/article/130531-babylon-hanging-gardens-nineveh-seven-wonders | 200 | 266128 | text/html | News article with Dalley quotations; extract saved. |
| bisi_iraq56 | https://www.bisi.ac.uk/publication/iraq-56/ | 200 | 208217 | text/html | BISI contents page for Iraq 56 (article listed at p. 45). |
| wb_academia_review | https://web.archive.org/web/2024id_/https://www.academia.edu/42720953/Review_of_S_Dalley_The_Mystery_of_the_Hanging_Garden_of_Babylon_An_Elusive_World_Wonder_Traced_Oxford_2013 | 200 | 168564 | text/html | Wayback copy of the academia.edu page for the 2014 BiOr review (Ariel M. Bagg): only an AI-generated abstract visible; PDF not accessible. |
| blog_imoac | https://itsmoreofacomment.com/2023/05/19/book-review-the-mystery-of-the-hanging-garden-of-babylon-by-s-dalley/ | 200 | 134424 | text/html | 2023 non-specialist blog review; saved. |
| wb_jstor_2018 | https://web.archive.org/web/20180921154556id_/https://www.jstor.org/stable/4200384 | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | First attempt reset by the proxy tunnel; retried below. |
| ora_home | https://ora.ox.ac.uk/ | 200 | 28440 | text/html | ORA reachable; nothing relevant. |
| wiki_dalley | https://en.wikipedia.org/w/index.php?title=Stephanie_Dalley&action=raw | 200 | 20807 | text/x-wiki | Wikipedia raw wikitext (bibliography of Dalley's HG publications). |
| core_api2 | https://api.core.ac.uk/v3/search/works?q=title%3A%22Hanging+Gardens%22+AND+authors%3ADalley&limit=20 | 429 | 0 | text/html | Rate-limited (429). |
| br_jsia | https://ia601407.us.archive.org/BookReader/BookReaderJSIA.php?id=mysteryofhanging0000dall&itemPath=/9/items/mysteryofhanging0000dall&server=ia601407.us.archive.org&format=jsonp&subPrefix=mysteryofhanging0000dall | 200 | 127581 | application/x-javascript | BookReader JSIA: returns reader config but page images/OCR are restricted. |
| gapi_vol_q | https://www.googleapis.com/books/v1/volumes/7HUZYru5UiIC?q=alamittu | 429 | 1306 | application/json | 429. |
| wb_jstor_2018b | https://web.archive.org/web/20180921154556id_/https://www.jstor.org/stable/4200384 | 200 | 92317 | text/html | Wayback 21 Sep 2018 capture: full metadata (title, vol. 56 pp. 45-58, Page Count 14, topics) but no text/PDF. |
| wb_jstor_reade2021 | https://web.archive.org/web/20210823223347id_/https://www.jstor.org/stable/4200490 | 200 | 94914 | text/html | Wayback 2021 JSTOR page for Reade 2000: metadata only (23 pages). |
| s2_reade | https://api.semanticscholar.org/graph/v1/paper/DOI:10.2307/4200490?fields=title,openAccessPdf,externalIds,isOpenAccess | 200 | 300 | application/json | Semantic Scholar: record exists, no open-access PDF. |
| scholar_ia_1994b | https://scholar.archive.org/search?q=%22Nineveh%2C+Babylon+and+the+Hanging+Gardens%22 | 200 | 470 | text/html | Same. |
| unpaywall_reade | https://api.unpaywall.org/v2/10.2307/4200490?email=research@example.org | 200 | 720 | application/json | is_oa=false. |
| peeters_bior_search | https://poj.peeters-leuven.be/content.php?url=journal&journal_code=BIOR | 200 | 24923 | text/html | Peeters Online Journals BiOr journal page (issue list). |
| ol_inside_restrict1 | https://openlibrary.org/search/inside.json?q=Amytis+AND+identifier%3Amysteryofhanging0000dall | 200 | 895 | application/json | identifier: restriction works. |
| ol_inside_restrict2 | https://openlibrary.org/search/inside.json?q=%22Nineveh%22+identifier%3Amysteryofhanging0000dall | 200 | 5421 | application/json | Same. |
| ia_marc | https://archive.org/download/mysteryofhanging0000dall/mysteryofhanging0000dall_marc.xml | 200 | 6938 | text/xml | MARC record downloadable (bibliographic data). |
| ia_dc | https://archive.org/download/mysteryofhanging0000dall/mysteryofhanging0000dall_dc.xml | 200 | 3061 | text/xml | Dublin Core record. |
| ia_scandata | https://archive.org/download/mysteryofhanging0000dall/mysteryofhanging0000dall_scandata.xml | 200 | 342873 | text/xml | Scandata: leaf-to-page map (used to build raw_F/ia_leaf_page_map.json). |
| ia_details | https://archive.org/details/mysteryofhanging0000dall | 200 | 216770 | text/html | IA details page (borrow only). |
| fts_guess1 | https://be-api.us.archive.org/fts/v1/search?q=alamittu&identifier=mysteryofhanging0000dall | 200 | 4734 | application/json | be-api.us.archive.org/fts/v1/search with identifier= : returns up to 5 highlight fragments per query, no page numbers. This became the main IA route (see Section 3). |
| fts_guess2 | https://archive.org/services/search/v1/scrape?q=alamittu&fields=identifier | 200 | 32 | application/json | scrape API: no full-text results. |
| fts_v1 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&size=50 | 200 | 869 | application/json | size= parameter ignored (still 5 fragments). |
| fts_v2 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&fields=page_num,identifier&hl=true | 200 | 870 | application/json | fields=/hl= ignored. |
| fts_v3 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&scope=page | 200 | 870 | application/json | scope=page ignored. |
| fts_v4 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&type=page | 200 | 870 | application/json | type=page ignored. |
| fts_v5 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&page_search=true | 200 | 870 | application/json | page_search ignored. |
| fts_v6 | https://be-api.us.archive.org/fts/v1/search?q=Amytis&identifier=mysteryofhanging0000dall&pretty=true&explain=true | 200 | 870 | application/json | explain=true: shows only the ES highlight, no page_num field. |
| fatcat_1994 | https://api.fatcat.wiki/v0/release/lookup?doi=10.2307/4200384&expand=files,container&hide=abstracts,refs | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | api.fatcat.wiki tunnel reset by proxy (relay failure), not retried further. |
| fatcat_reade | https://api.fatcat.wiki/v0/release/lookup?doi=10.2307/4200490&expand=files,container&hide=abstracts,refs | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Proxy tunnel reset. |
| fatcat_1993 | https://api.fatcat.wiki/v0/release/lookup?doi=10.2307/1587050&expand=files,container&hide=abstracts,refs | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Proxy tunnel reset. |
| fatcat_search | https://search.fatcat.wiki/fatcat_release/_search?q=title:%22Hanging+Gardens%22+AND+contrib_names:Dalley | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Proxy tunnel reset. |
| base_search | https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&query=dctitle:%22Nineveh,+Babylon+and+the+Hanging+Gardens%22&format=json | 200 | 143 | application/json | BASE: 0 hits for the title. |
| yale_nelc | https://nelc.yale.edu/node/584 | 200 | 27069 | text/html | Yale NELC event listing (no abstract). |
| cdx_cjo | https://web.archive.org/cdx/search/cdx?url=journals.cambridge.org/*S0021088900002801*&output=json&limit=50 | 200 | 3 | application/json | No captures of the old journals.cambridge.org S0021088900002801 URL. |
| cdx_cjo2 | https://web.archive.org/cdx/search/cdx?url=journals.cambridge.org/*&filter=original:.*4200384.*&output=json&limit=20 | 504 | 160 | text/html | Gateway timeout. |
| csmc_hamburg | https://www.csmc.uni-hamburg.de/publications/mesopotamia/2018-01-30.html | 200 | 39466 | text/html | Hamburg CSMC bulletin on the thesis; full text saved. |
| propylaeum_search | https://archiv.ub.uni-heidelberg.de/propylaeumdok/cgi/search/simple?q=Dalley+Hanging+Gardens&_action_search=Search | 200 | 4552 | text/html | Propylaeum-DOK (Heidelberg): no deposit of the HSAO 6 article or the volume. |
| propylaeum_hsao | https://archiv.ub.uni-heidelberg.de/propylaeumdok/cgi/search/simple?q=Assyrien+im+Wandel+der+Zeiten&_action_search=Search | 200 | 4552 | text/html | Same. |
| crossref_bior | https://api.crossref.org/works?query.bibliographic=Dalley+Mystery+Hanging+Garden+Babylon&filter=issn:0006-1913&rows=10&select=DOI,title,container-title,page,volume,issue,URL,author | 200 | 187 | application/json | Crossref: BiOr reviews are not registered as items. |
| crossref_bior2 | https://api.crossref.org/works?filter=issn:0006-1913,from-pub-date:2014-01,until-pub-date:2015-06&query=Dalley&rows=20&select=DOI,title,page,volume,issue,author | 200 | 191 | application/json | Same. |
| tvg_doi | https://doi.org/10.5117/tvgesch2013.4.b4 | 403 | 5787 | text/html | van der Spek review: Cloudflare challenge (403). |
| wb_tvg | https://web.archive.org/web/2024id_/https://www.aup-online.com/content/journals/10.5117/TVGESCH2013.4.B4 | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Wayback fetch reset by proxy tunnel. |
| core_doi | https://api.core.ac.uk/v3/search/works?q=doi%3A%2210.2307%2F4200384%22&limit=5 | 429 | 0 | text/html | Rate-limited (429). |
| poj_bior71a | https://poj.peeters-leuven.be/content.php?url=issue&journal_code=BIOR&issue=5&vol=71 | 200 | 19635 | text/html | BiOr 71 issue 5-6 contents (sections with 'download (open access)'). |
| poj_bior71b | https://poj.peeters-leuven.be/content.php?url=issue&journal_code=BIOR&issue=5-6&vol=71 | 404 | 24 | text/html | Wrong issue parameter (404). |
| poj_bior71c | https://poj.peeters-leuven.be/content.php?url=journal&journal_code=BIOR&vol=71 | 200 | 24923 | text/html | BiOr volume 71 page. |
| wb_tvg2 | https://web.archive.org/web/2024id_/https://www.aup-online.com/content/journals/10.5117/TVGESCH2013.4.B4 | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Same. |
| wb_tvg3 | https://web.archive.org/web/2020id_/https://www.aup.nl/journal/article/10.5117/TVGESCH2013.4.B4 | FAIL | 0 | ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) | Same (aup.nl URL). |

## 2. Routes tried through dedicated scripts (not in the table above)

### 2.1 Google Books (Dalley 2013)
* `https://www.googleapis.com/books/v1/volumes?...` — 429 for every call (quota exhausted), including `volumes/7HUZYru5UiIC?q=`.
* `https://books.google.com/books?vid=ISBN...`, `...?id=7HUZYru5UiIC&jscmd=SearchWithin&q=`, `...&pg=PA66&output=text` — 403 (blocked).
* `https://www.google.com/books/feeds/volumes?q=<query>&max-results=20` (GData Atom feed) — WORKS. Queried by script, modes: plain `"term"`; `intitle:` (returns blurb only); `inauthor:Dalley` (blurb only); `hg` = `"term" "Hanging Garden"` (best: returns a <dc:description> snippet and a preview link whose `pg=PA<n>` gives the page). Three batteries (logs raw_F/gfeeds_hg.log, gfeeds_hg2.log, gfeeds_hg3.log; raw XML in raw_F/gfeeds/; results raw_F/gfeeds_hits.jsonl, 262 rows, 236 unique page-anchored snippets). Roughly 300 distinctive terms were queried (names, Akkadian words, place names, phrases from the IA fragments).

### 2.2 Internet Archive (Dalley 2013 lending copy mysteryofhanging0000dall)
* `archive.org/fulltext/inside.php`, `ia601407/ia801407.us.archive.org/fulltext/inside.php`, `dn720001.ca.archive.org/fulltext/inside.php` — 403/404 'item not available' (restricted item).
* `https://openlibrary.org/search/inside.json?q=<term> identifier:mysteryofhanging0000dall` — works (highlights, no page numbers).
* `https://be-api.us.archive.org/fts/v1/search?q=<term>&identifier=mysteryofhanging0000dall` — works; up to 5 highlight fragments (~100-130 chars, match marked {{{ }}}) per query; quoted phrases and AND work; size/fields/scope/type/page_search/explain parameters have no effect; wildcards unsupported. Queried by script in batteries A-E (logs raw_F/fts_batchA.log ... fts_batchE.log; raw JSON raw_F/fts/; results raw_F/fts_hits.jsonl, 1,407 rows / 1,332 unique fragments) over c. 700 terms (including screw, alamittu, Amytis, Polyhistor, Berossus, Bavian, Jerwan, kirimahu, Khinis, Tashmetu-sharrat, 'Nineveh was called Babylon', 'Old Babylon').
* 'Walking' the OCR: a script repeatedly quotes the last 3-6 words of a fragment to obtain its continuation (≈50-100 new characters per request); 40 passages reconstructed (raw_F/fts_walks.jsonl), e.g. Conclusion pp. 203-205, ch. 6 opening pp. 107-109, prism passage pp. 63-64, Koldewey/Nagel pp. 13-16, Archimedes pp. 57-59.
* Item files: metadata, MARC, DC and scandata XML downloadable (raw_F/ia_meta_book.json, ia_marc.xml, ia_dc.xml, ia_scandata.xml -> ia_leaf_page_map.json: 322 leaves, printed pages 1-279 = leaves 27-305); page images, DjVu/text and the BookReader OCR are restricted (`isRestricted`), and no attempt was made to circumvent the lending restriction.
* archive.org advancedsearch for the 1994 article, Iraq 56, Of Pots and Plans, HSAO 6, RAI 51: nothing usable; scholar.archive.org returns an empty JS shell through the proxy.

### 2.3 Peeters Online Journals (Bagg's BiOr review)
* Issue pages `https://poj.peeters-leuven.be/content.php?url=issue&journal_code=BIOR&issue={1,3,5}&vol=71` list the review sections as 'download (open access)'. First attempts at `secure/POJ/downloadpdf.php?id=...` failed ('no such transaction ticket'). Working flow: `secure/POJ/purchaseform.php?id=<id>&sid=` -> redirect to `viewpdf.php?ticket_id=...` with meta-refresh -> `downloaded.php?ticket_id=...&newlayout=0` -> `downloadpdf.php?ticket_id=...` = PDF. Fetched the Assyriologie sections of 71/1-2 (id 3034658, cols. 148-202), 71/3-4 (3062124, cols. 455-497) and 71/5-6 (3073489, cols. 782-790) and the Archeologie sections (3034661, 3062128, 3073496) — raw_F/bior71_<id>.pdf. Bagg's review of Dalley found in 3062124 at cols. 485-492 (raw_F/bagg_2014_bior71_review_dalley.txt).

### 2.4 Other publisher/library routes for the 1994 article
* Cambridge Core: article page (Extract, footnotes, references list), citation_pdf_url, the `/core/services/aop-cambridge-core/content/view/C024A9417036B87AB6D772A98274E0D0/S0021088900002801a.pdf/...` link, the volume-56 TOC page (404 on Cambridge) — all closed or metadata only. No Wayback capture of any Cambridge PDF (CDX checked).
* JSTOR: live pages serve a bot-check shell; Wayback `id_` captures (2018, 2021, 2024) give metadata only; no PDF capture.
* Unpaywall, OpenAlex, Semantic Scholar, CORE, BASE, fatcat (tunnel reset), HathiTrust (blocked/search-only), ORA, Propylaeum-DOK, Google Books (no scan of Iraq 56): no open copy.
* Dalley's other restatements: SAOC 62 open PDF (ISAC) — obtained; Sidestone open PDF — obtained (via raw_D); HSAO 6 (Heidelberg 1997), Of Pots and Plans (2002), ARAM 13/14, AfO 48/49, BAIAS 18 — no open copies found (archive.org, Propylaeum, CORE, HathiTrust).

### 2.5 Other fetch and search attempts
* Fetches of https://www.aup-online.com/content/journals/10.5117/TVGESCH2013.4.B4 (van der Spek review) — 403 (Cloudflare); of https://www.academia.edu/42720953/... — 403. Web search used only to identify review venues (Potts NYRB, Holland Literary Review, van der Spek TvG, Bagg BiOr, Choice).

## 3. Sites that block or fail through the proxy (for the record)
* 403: academia.edu, researchgate.net, britishmuseum.org, books.google.com (page/preview endpoints), babel.hathitrust.org, academic.oup.com search, aup-online.com (Cloudflare), ia801407.us.archive.org/fulltext.
* 429 (rate limits): googleapis.com/books, api.semanticscholar.org search, api.core.ac.uk, api.openalex.org search.
* Connection reset by the proxy relay: api.fatcat.wiki, search.fatcat.wiki, several web.archive.org fetches (retried once each).
* Bot-check shells (HTML without content): jstor.org live pages, global.oup.com live page, the-tls.com search, scholar.archive.org.

## 4. Files produced
* F_dalley_1994.txt — Extract, 75 footnotes, page-by-page reconstruction, 45 B-R page-keyed citations.
* F_dalley_2013.txt — TOC with page spans, Bagg's chapter précis, 236 Google page-numbered snippets, 39 walked passages and c. 1,300 IA fragments organised by chapter/page (323 fragments placed on a page, 944 unplaced but grouped by search term).
* F_dalley_other.md — full texts of Dalley 1993, 2008, 2003 (with Oleson), 2017, OUPblog/PBS/NatGeo/CSMC/ISAC; full Bagg 2014 and Potts 2013; Holland opening; Reade 2000 extract and references; notes on what was not obtained.
* raw_F/ — all downloads (≈180 files) plus helper outputs (_recovered_fetch_results.txt / _recovered_fetch_urls.txt = this log's table); these working copies are not included in this folder.