# SOURCES.md — fetch log for the literature dossier (Great Chicago Fire, cause)

The files below were saved under a `sources/` working folder; working copies of the raw downloads are not included in this folder. Every row gives UTC fetch time, HTTP status, bytes, local file and URL, copied from the raw logs (`FETCH_LOG.txt`, `ca/CA_FETCH_LOG.txt`, `gbooks/QUERY_LOG.txt`). Status 000 = connection failed (proxy reset); 403/429/401 = blocked or rate-limited; 202/406/500/522 = host errors. Files of only a few bytes are failed fetches kept as evidence of the attempt.

User-Agent for all curl fetches: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36. No browser automation was used. web.archive.org / archive.ph were never requested (per ACCESS_NOTES).

## Notes on access, blocks and substitutes (hand-written; the machine-generated tables follow)

- **Hosts blocked or dead, per ACCESS_NOTES and confirmed here:** web.archive.org / archive.ph (never requested); hydeparkmedia.com, chsmedia.org, dig.lib.niu.edu (dead); catalog/babel.hathitrust.org, explore.chicagocollections.org, images.chicagohistory.org, idnc.library.illinois.edu, digital.lib.niu.edu (Cloudflare "Verifying connection" — a saved sample is in `misc/niu_search_cow.html`). No browser automation was attempted.
- **Google Books:** volume rppt7mgfiKMC (Bales, McFarland; Google's edition record dated 2015-09-01) answers search-within queries with page-numbered snippets; Google's bot-block ("Sorry") page was hit repeatedly, so queries were spread over books.google.com / .co.uk / .com.au with 40–70 s pauses. Every query and its outcome is in `gbooks/QUERY_LOG.txt`; the parsed snippets are in `gbooks/SNIPPETS.jsonl` and, grouped by query, in `gbooks/BALES_SNIPPETS_BY_QUERY.txt`. The background job `gbsearch4.py` may still be adding rows after this file was generated; re-run `python3 ../make_sources_md.py` and the digest snippet in REPORT.md Appendix B to refresh.
- **Library of Congress (Chronicling America):** JSON API (`?fo=json`, then `resource.fulltext_file`); persistent HTTP 429 rate-limiting — some pages (Evening Star 12 Oct 1871 p. 1) were never obtained after five spaced attempts. Chicago dailies of October 1871 are not in Chronicling America.
- **archive.org:** full djvu texts obtained for Andreas vol. 2, Critchell 1909, Donnelly 1883, Musham 1940 (`papersinillinois1940illi`); lending-only items (Cromie, Sawislak, Kogan & Cromie, Smith, Miller, Bales, second Musham copy) return 401/403 and were not retried. The advancedsearch endpoint was used for discovery (`misc/ia_search_*.json`); one connection reset was retried once.
- **Wikipedia:** REST HTML and `action=raw` succeeded; the `prop=revisions` API returned 429 twice, so revision histories were taken from `action=history` HTML where needed. Old revisions were fetched with `oldid=`.
- **Chicago Tribune:** legacy `ct-xpm-…` URLs served the full text of DeBartolo 1997, DeBartolo 1998, Mills 1997 and Potash 2006 (fetched 07:10–07:11 UTC); the Tribune's own 2021 archive was not searchable (search engine refuses chicagotribune.com), so the 2021 Tribune coverage is represented by a syndicated Clarence Page column (phillytrib.com) and one 2021 Tribune feature found via Wikipedia.
- **Page-fetch tool:** used only for pages that refused curl; results are model extractions, saved in `webfetch/` and labelled as such in REPORT.md. WTTW, Forward, UPI and Chicago magazine refused it too.
- **Fetch stubs:** files of a few bytes (e.g., `web/wttw_2021.txt`, `web/newsweek_2021.txt`, `web/howstuffworks.txt`) are the empty results of refused fetches and are kept as evidence of the attempt; their HTTP codes are in the tables below.
- **Domain hijack noticed:** chicago1871.org (the Chicago History Museum's 2021 exhibition domain, cited in 2021 coverage) now serves gambling spam (`web/chicago1871_media_mentions.txt`).


## A. General fetches (FETCH_LOG.txt)

| time (UTC) | code | bytes | local file | URL |
|---|---|---|---|---|
| 2026-09-14T05:59:07Z | 200 | 3038 bytes | `jstor_test.html` | https://www.jstor.org/stable/40193095 |
| 2026-09-14T05:59:08Z | 200 | 5477 bytes | `wiki_Catherine_OLeary.wikitext` | https://en.wikipedia.org/w/index.php?title=Catherine_O%27Leary&action=raw |
| 2026-09-14T05:59:08Z | 200 | 55005 bytes | `wiki_Great_Chicago_Fire.wikitext` | https://en.wikipedia.org/w/index.php?title=Great_Chicago_Fire&action=raw |
| 2026-09-14T05:59:08Z | 000 | 0 bytes | `tcf_home.html` | https://www.thechicagofire.com/ |
| 2026-09-14T05:59:08Z | 200 | 340 bytes | `ia_search_musham.json` | https://archive.org/advancedsearch.php?q=title%3A%28transactions%20illinois%20state%20historical%20society%29%20AND%20year%3A%5B1940%20TO%201942%5D&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&rows=50&output=json |
| 2026-09-14T05:59:08Z | 403 | 1103 bytes | `gb_test_dalton.json` | https://books.google.com/books?id=rppt7mgfiKMC&jscmd=SearchWithinVolume2&q=Dalton |
| 2026-09-14T05:59:08Z | 404 | 1930 bytes | `wiki_Daniel_Sullivan.wikitext` | https://en.wikipedia.org/w/index.php?title=Daniel_Sullivan_(Chicago_Fire)&action=raw |
| 2026-09-14T05:59:08Z | 200 | 46 bytes | `wiki_Louis_M_Cohn.wikitext` | https://en.wikipedia.org/w/index.php?title=Louis_M._Cohn&action=raw |
| 2026-09-14T05:59:08Z | 200 | 5074 bytes | `fulton_home.html` | https://fultonhistory.com/ |
| 2026-09-14T05:59:20Z | 200 | 2349696 bytes | `ca_test.json` | https://www.loc.gov/collections/chronicling-america/?q=%22O%27Leary%22+cow+fire&dates=1871&fo=json |
| 2026-09-14T05:59:58Z | 200 | 19065 bytes | `gcf/media-event-library.html` | https://greatchicagofire.org/media-event/media-event-library/ |
| 2026-09-14T05:59:58Z | 200 | 39188 bytes | `gcf/oleary-legend.html` | https://greatchicagofire.org/oleary-legend/ |
| 2026-09-14T05:59:58Z | 200 | 19191 bytes | `gcf/oleary-legend-library.html` | https://greatchicagofire.org/oleary-legend/oleary-legend-library/ |
| 2026-09-14T05:59:58Z | 200 | 24647 bytes | `gcf/star-born.html` | https://greatchicagofire.org/oleary-legend/star-born/ |
| 2026-09-14T05:59:58Z | 200 | 26103 bytes | `gcf/saga-continues.html` | https://greatchicagofire.org/oleary-legend/saga-continues/ |
| 2026-09-14T05:59:59Z | 200 | 27077 bytes | `gcf/media-event.html` | https://greatchicagofire.org/media-event/ |
| 2026-09-14T05:59:59Z | 200 | 34082 bytes | `gcf/oleary-home.html` | https://greatchicagofire.org/landmarks/oleary-home/ |
| 2026-09-14T05:59:59Z | 200 | 18184 bytes | `gcf/string-of-endorsements.html` | https://greatchicagofire.org/oleary-legend/string-of-endorsements/ |
| 2026-09-14T05:59:59Z | 200 | 22740 bytes | `gcf/tour-saturday-night-fire.html` | https://greatchicagofire.org/tours/saturday-night-fire-and-oleary-cottage/ |
| 2026-09-14T05:59:59Z | 429 | 278 bytes | `wiki/search_cohn.json` | https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Louis%20Cohn%20Chicago%20fire%20craps&format=json |
| 2026-09-14T05:59:59Z | 429 | 278 bytes | `wiki/search_sullivan.json` | https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Daniel%20Sullivan%20Chicago%20Fire%20O%27Leary&format=json |
| 2026-09-14T06:00:00Z | 200 | 11027 bytes | `ia/search_papers_ill.json` | https://archive.org/advancedsearch.php?q=title%3A%28%22papers%20in%20illinois%20history%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&rows=100&output=json |
| 2026-09-14T06:00:00Z | 200 | 10784 bytes | `ia/search_musham2.json` | https://archive.org/advancedsearch.php?q=%28musham%29%20AND%20mediatype%3Atexts&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=creator&rows=100&output=json |
| 2026-09-14T06:00:00Z | 200 | 3862 bytes | `gb_feed_volume.xml` | https://www.google.com/books/feeds/volumes/rppt7mgfiKMC |
| 2026-09-14T06:00:00Z | 200 | 306234 bytes | `gb_test2.json` | https://books.google.com/books?id=rppt7mgfiKMC&q=Dalton&output=json |
| 2026-09-14T06:00:00Z | 200 | 618 bytes | `chicagology/sitemap.xml` | https://chicagology.com/sitemap.xml |
| 2026-09-14T06:00:00Z | 200 | 157685 bytes | `chicagology/search_oleary.html` | https://chicagology.com/?s=O%27Leary |
| 2026-09-14T06:01:05Z | 200 | 457932 bytes | `ia/occ_ishs_1940_djvu.txt` | https://archive.org/download/occasional-publications-of-ishs_1940/occasional-publications-of-ishs_1940_djvu.txt |
| 2026-09-14T06:01:07Z | 401 | 574 bytes | `ia/papersinillinois0000illi_djvu.txt` | https://archive.org/download/papersinillinois0000illi/papersinillinois0000illi_djvu.txt |
| 2026-09-14T06:01:07Z | 200 | 507828 bytes | `ia/papersinillinois1940illi_djvu.txt` | https://archive.org/download/papersinillinois1940illi/papersinillinois1940illi_djvu.txt |
| 2026-09-14T06:01:07Z | 200 | 39596 bytes | `chicagology/chicago-fire-index.html` | https://chicagology.com/chicago-fire/ |
| 2026-09-14T06:01:07Z | 200 | 67893 bytes | `chicagology/olearys.html` | https://chicagology.com/notorious-chicago/olearys/ |
| 2026-09-14T06:01:12Z | 200 | 476636 bytes | `ia/papersinillinois1941illi_djvu.txt` | https://archive.org/download/papersinillinois1941illi/papersinillinois1941illi_djvu.txt |
| 2026-09-14T06:01:12Z | 200 | 35848 bytes | `chicagology/fire050.html` | https://chicagology.com/chicago-fire/fire050/ |
| 2026-09-14T06:01:12Z | 200 | 44440 bytes | `chicagology/fire052.html` | https://chicagology.com/chicago-fire/fire052/ |
| 2026-09-14T06:01:13Z | 200 | 21755 bytes | `ia/search_books.json` | https://archive.org/advancedsearch.php?q=%28cromie%20chicago%20fire%29%20OR%20%28sawislak%29%20OR%20%28%22urban%20disorder%22%20smith%29%20OR%20%28%22american%20apocalypse%22%20miller%29%20OR%20%28waskin%20comet%29%20OR%20%28donnelly%20ragnarok%29%20OR%20%28%22chicago%27s%20great%20fire%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=creator&fl%5B%5D=collection&rows=100&output=json |
| 2026-09-14T06:02:14Z | 400 | 1726 bytes | `ia/fts_test_beta.json` | https://archive.org/services/search/beta/page_production/?user_query=Dalton&page_type=collection_details&page_target=greatchicagofire0000bale&hits_per_page=50&page=1&sin=TXT |
| 2026-09-14T06:02:14Z | 200 | 44570 bytes | `ia/papersinillinois1940illi_page_numbers.json` | https://archive.org/download/papersinillinois1940illi/papersinillinois1940illi_page_numbers.json |
| 2026-09-14T06:02:15Z | 200 | 896775 bytes | `ia/ragnarok_donnelly_1883_djvu.txt` | https://archive.org/download/ragnarokageoffir00donn/ragnarokageoffir00donn_djvu.txt |
| 2026-09-14T06:02:15Z | 429 | 278 bytes | `wiki/Great_Chicago_Fire.html` | https://en.wikipedia.org/api/rest_v1/page/html/Great_Chicago_Fire |
| 2026-09-14T06:02:15Z | 429 | 278 bytes | `wiki/Catherine_OLeary.html` | https://en.wikipedia.org/api/rest_v1/page/html/Catherine_O%27Leary |
| 2026-09-14T06:02:16Z | 200 | 88 bytes | `ia/fts_test_cromie.json` | https://ia800809.us.archive.org/fulltext/inside.php?item_id=greatchicagofire0000crom&doc=greatchicagofire0000crom&q=Sullivan&path=%2F3%2Fitems%2Fgreatchicagofire0000crom |
| 2026-09-14T06:02:46Z | 200 | 35193 bytes | `chicagology/fire030_learys_cottage.html` | https://chicagology.com/chicago-fire/fire030/ |
| 2026-09-14T06:02:46Z | 200 | 53173 bytes | `chicagology/fire010_evening_post.html` | https://chicagology.com/chicago-fire/fire010/ |
| 2026-09-14T06:03:11Z | 200 | 52095 bytes | `ca_tribune_1871-10-11_p1.json` | https://www.loc.gov/resource/sn82014064/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:03:11Z | 200 | 101044 bytes | `ca_tribune_item.json` | https://www.loc.gov/item/sn82014064/?fo=json |
| 2026-09-14T06:04:03Z | 200 | 49275 bytes | `ca/tribune_1871-10-11_p2.txt` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_clark_ver03/data/sn82014064/no_reel/1871101101/0002.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:04:03Z | 200 | 82837 bytes | `ca/tribune_1871-10-11_p1.txt` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_clark_ver03/data/sn82014064/no_reel/1871101101/0001.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:04:09Z | 200 | 3144115 bytes | `ca/search_leary_cow_oct1871.json` | https://www.loc.gov/collections/chronicling-america/?q=leary+cow&start_date=1871-10-08&end_date=1871-10-31&ops=AND&fo=json&c=100 |
| 2026-09-14T06:04:50Z | 200 | 2230122 bytes | `ca/s2_leary_cow_kerosene_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=Leary+cow+kerosene&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:04:51Z | 200 | 3140205 bytes | `ca/s1_oleary_cow_fire_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=%22O%27Leary%22+cow+fire&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:04:54Z | 200 | 2897671 bytes | `ca/s1_oleary_cow_fire_p2.json` | https://www.loc.gov/collections/chronicling-america/?q=%22O%27Leary%22+cow+fire&dates=1871&fo=json&c=100&sp=2 |
| 2026-09-14T06:05:01Z | 200 | 3136038 bytes | `ca/s3_cow_kicked_lamp_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=cow+kicked+lamp+chicago&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:05:02Z | 200 | 2409876 bytes | `ca/s4_dekoven_cow_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=%22De+Koven%22+cow&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:05:09Z | 200 | 326015 bytes | `wiki/Great_Chicago_Fire.html` | https://en.wikipedia.org/api/rest_v1/page/html/Great_Chicago_Fire |
| 2026-09-14T06:11:55Z | 403 | 5861 bytes | `forward_cohn_2021.html` | https://forward.com/culture/476328/chicago-fire-jewish-1871-louis-cohn-oleary-how-did-it-start/ |
| 2026-09-14T06:11:55Z | 200 | 19168 bytes | `jewage_cohn.html` | https://www.jewage.org/wiki/en/Article:Louis_M._Cohn_-_Biography |
| 2026-09-14T06:11:55Z | 200 | 90508 bytes | `nws_lot_1871fire.html` | https://www.weather.gov/lot/1871fire |
| 2026-09-14T06:11:55Z | 200 | 376949 bytes | `wbur_2021.html` | https://www.wbur.org/hereandnow/2021/10/08/great-chicago-fire |
| 2026-09-14T06:11:56Z | 200 | 66194 bytes | `nws_grb_peshtigofire2.html` | https://www.weather.gov/grb/peshtigofire2 |
| 2026-09-14T06:11:56Z | 200 | 73433 bytes | `chm_150th_exhibition.html` | https://www.chicagohistory.org/chicago-history-museum-commemorates-150th-anniversary-of-great-chicago-fire-in-new-exhibition/ |
| 2026-09-14T06:11:57Z | 406 | 0 bytes | `time_2015.html` | https://time.com/4055770/great-chicago-fire-origins/ |
| 2026-09-14T06:11:57Z | 200 | 254476 bytes | `mentalfloss.html` | https://www.mentalfloss.com/history/misconceptions/did-cow-really-cause-great-chicago-fire |
| 2026-09-14T06:11:57Z | 200 | 128484 bytes | `npr_1997.html` | https://www.npr.org/1997/10/07/1038129/mrs-olearys-cow |
| 2026-09-14T06:11:58Z | 403 | 548 bytes | `blockclub_2025.html` | https://blockclubchicago.org/2025/10/08/5-things-you-probably-didnt-know-about-the-great-chicago-fire/ |
| 2026-09-14T06:11:58Z | 403 | 5019 bytes | `medium_annacivil_ahern.html` | https://annacivil.medium.com/reporter-confesses-to-writing-fake-news-about-the-chicago-fire-a1b6613e776c |
| 2026-09-14T06:11:58Z | 200 | 375746 bytes | `breezecourier_2021.html` | https://www.breezecourier.com/2021/10/08/great-chicago-fire-mrs-olearys-cow-not-to-blame/ |
| 2026-09-14T06:11:59Z | 403 | 548 bytes | `cemeteries_2018.html` | https://chicagoandcookcountycemeteries.com/2018/10/06/october-8-1871-the-cow-was-framed/ |
| 2026-09-14T06:12:00Z | 200 | 392312 bytes | `chipublib_whodunit.html` | https://www.chipublib.org/blogs/post/whodunit-the-mystery-of-mrs-olearys-cow/ |
| 2026-09-14T06:12:00Z | 200 | 147275 bytes | `irishamerica_2021.html` | https://www.irishamerica.com/2021/10/mrs-oleary-exonerated/ |
| 2026-09-14T06:12:00Z | 000 | 0 bytes | `encyclopedia_chicago_410070.html` | http://www.encyclopedia.chicagohistory.org/pages/410070.html |
| 2026-09-14T06:12:00Z | 403 | 5697 bytes | `aiaa_wood_2004_abs.html` | https://arc.aiaa.org/doi/abs/10.2514/6.2004-1419 |
| 2026-09-14T06:12:01Z | 200 | 350306 bytes | `nbcchicago.html` | https://www.nbcchicago.com/news/local/dont-blame-mrs-olearys-cow-for-the-great-chicago-fire/2631627/ |
| 2026-09-14T06:12:01Z | 406 | 0 bytes | `newsweek_2021.html` | https://www.newsweek.com/150-years-later-debate-still-rages-over-cause-great-chicago-fire-1637181 |
| 2026-09-14T06:12:02Z | 200 | 160389 bytes | `physicsforums_comet.html` | https://www.physicsforums.com/threads/is-the-cometary-debris-theory-of-the-chicago-fire-pseudo-science.524243/ |
| 2026-09-14T06:12:03Z | 200 | 138020 bytes | `thirdcoast_smith_review.html` | https://thirdcoastreview.com/uncategorized/2020/10/14/review-a-long-ago-blaze-that-echoes-the-pandemic-chicagos-great-fire-by-carl-smith |
| 2026-09-14T06:12:04Z | 200 | 57452 bytes | `uiuc_peshtigo_guide.html` | https://guides.library.illinois.edu/historical_wildfires/peshtigo |
| 2026-09-14T06:12:04Z | 200 | 104078 bytes | `americanheritage_olearys.html` | https://www.americanheritage.com/olearys-and-great-chicago-fire |
| 2026-09-14T06:12:04Z | 200 | 19129 bytes | `earthmagazine_peshtigo.html` | https://www.earthmagazine.org/article/benchmarks-october-8-1871-deadliest-wildfire-american-history-incinerates-peshtigo-wisconsin/ |
| 2026-09-14T06:12:04Z | 200 | 6243 bytes | `../wiki/wiki_James_Patrick_OLeary.wikitext` | https://en.wikipedia.org/w/index.php?title=James_Patrick_O%27Leary&action=raw |
| 2026-09-14T06:12:04Z | 200 | 24301 bytes | `../wiki/wiki_Peshtigo_fire.wikitext` | https://en.wikipedia.org/w/index.php?title=Peshtigo_fire&action=raw |
| 2026-09-14T06:12:04Z | 200 | 25692 bytes | `../wiki/wiki_Bielas_Comet.wikitext` | https://en.wikipedia.org/w/index.php?title=Biela%27s_Comet&action=raw |
| 2026-09-14T06:12:04Z | 200 | 22442 bytes | `../wiki/wiki_Great_Fires_of_1871.wikitext` | https://en.wikipedia.org/w/index.php?title=Great_Fires_of_1871&action=raw |
| 2026-09-14T06:12:05Z | 200 | 3576 bytes | `../gb_feed_smith2020.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Chicago%27s+Great+Fire%22+inauthor:Smith&max-results=5 |
| 2026-09-14T06:12:05Z | 200 | 5203 bytes | `../gb_feed_sawislak.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Smoldering+City%22+inauthor:Sawislak&max-results=5 |
| 2026-09-14T06:12:05Z | 200 | 5461 bytes | `../gb_feed_smith1995.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Urban+Disorder%22+inauthor:Smith&max-results=5 |
| 2026-09-14T06:12:05Z | 200 | 3349 bytes | `../gb_feed_kogan.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Great+Fire%22+inauthor:Kogan+inauthor:Cromie&max-results=5 |
| 2026-09-14T06:12:05Z | 200 | 6684 bytes | `../gb_feed_cromie.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Great+Chicago+Fire%22+inauthor:Cromie&max-results=5 |
| 2026-09-14T06:12:06Z | 500 | 35 bytes | `../gb_feed_miller.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22American+Apocalypse%22+inauthor:Miller&max-results=5 |
| 2026-09-14T06:12:06Z | 200 | 3671 bytes | `../gb_feed_gess.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Firestorm+at+Peshtigo%22&max-results=5 |
| 2026-09-14T06:12:06Z | 200 | 3096 bytes | `../gb_feed_waskin.xml` | https://www.google.com/books/feeds/volumes?q=intitle:%22Mrs.+O%27Leary%27s+Comet%22&max-results=5 |
| 2026-09-14T06:13:49Z | 000 | 0 bytes | `meteorite_identification_2004.html` | http://meteorite-identification.com/mwnews/08232004.htm |
| 2026-09-14T06:13:50Z | 200 | 238932 bytes | `theticket953_michigan.html` | https://theticket953.com/michigan-great-fire-1871/ |
| 2026-09-14T06:13:50Z | 200 | 126260 bytes | `myhuntleynews_2021.html` | https://www.myhuntleynews.com/2021/10/07/some-holy-cow-facts-about-the-great-chicago-fire/ |
| 2026-09-14T06:14:38Z | 200 | 3134587 bytes | `ca/s6_kicked_over_cow_p2.json` | https://www.loc.gov/collections/chronicling-america/?q=%22kicked+over%22+cow+chicago&dates=1871&fo=json&c=100&sp=2 |
| 2026-09-14T06:14:42Z | 200 | 3136018 bytes | `ca/s5_milk_a_cow_kerosene_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=%22milk+a+cow%22+kerosene&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:14:49Z | 522 | 16 bytes | `ca/s6_kicked_over_cow_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=%22kicked+over%22+cow+chicago&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:16:25Z | 200 | 1835560 bytes | `ca/s7_taylor_halsted_p1.json` | https://www.loc.gov/collections/chronicling-america/?q=%22Taylor+and+Halsted%22+cow&dates=1871&fo=json&c=100&sp=1 |
| 2026-09-14T06:17:36Z | 200 | 319562 bytes | `irishcentral_2021.html` | https://www.irishcentral.com/roots/history/catherine-olearys-cow-great-chicago-fire |
| 2026-09-14T06:17:36Z | 200 | 280171 bytes | `modernfarmer_2014.html` | https://modernfarmer.com/2014/09/mrs-olearys-cow-heated-debate/ |
| 2026-09-14T06:17:36Z | 200 | 199782 bytes | `baltimoresun_1997-10-12.html` | https://www.baltimoresun.com/1997/10/12/chicago-ready-to-clear-olearys-cow-culprit-in-1871-fire-was-man-who-sounded-alarm-research-shows/ |
| 2026-09-14T06:17:37Z | 200 | 31485 bytes | `pw_sawislak.html` | https://www.publishersweekly.com/9780226735474 |
| 2026-09-14T06:17:37Z | 200 | 147916 bytes | `npr_2021.html` | https://www.npr.org/2021/10/02/1042595858/opinion-150-years-after-the-great-chicago-fire-were-more-vulnerable |
| 2026-09-14T06:17:37Z | 200 | 619668 bytes | `suntimes_2021.html` | https://chicago.suntimes.com/2021/10/7/22715595/great-chicago-fire-1871-150th-anniversary |
| 2026-09-14T06:18:07Z | 200 | 33399 bytes | `loc_guide_gcf.html` | https://guides.loc.gov/chronicling-america-great-chicago-fire |
| 2026-09-14T06:18:07Z | 403 | 5824 bytes | `smithsonian_2012.html` | https://www.smithsonianmag.com/history/what-or-who-caused-the-great-chicago-fire-61481977/ |
| 2026-09-14T06:18:07Z | 200 | 12052 bytes | `genealogytrails_fire.html` | https://genealogytrails.com/ill/cook/fire.html |
| 2026-09-14T06:18:07Z | 200 | 42624 bytes | `missedhistory.html` | https://www.missedhistory.com/article/chicago-great-fire-1871-olearys-cow |
| 2026-09-14T06:18:07Z | 200 | 39481 bytes | `loc_guide_gcf_articles.html` | https://guides.loc.gov/chronicling-america-great-chicago-fire/selected-articles |
| 2026-09-14T06:18:08Z | 200 | 28325 bytes | `newherald.html` | https://newherald.news/mrs-olearys-cow-was-not-to-blame-p26491-103.htm |
| 2026-09-14T06:22:12Z | 200 | 9575 bytes | `agilewriter_pegleg.html` | https://agilewriter.com/History/PegLegSullivan.htm |
| 2026-09-14T06:22:12Z | 200 | 71803 bytes | `uchicago_mag_2021.html` | https://mag.uchicago.edu/law-policy-society/great-fire-chicago-1871 |
| 2026-09-14T06:22:12Z | 200 | 3509673 bytes | `chicago_landmark_site_of_fire.pdf` | https://www.chicago.gov/content/dam/city/depts/zlup/Historic_Preservation/Publications/Site_of_Chicago_Fire.pdf |
| 2026-09-14T06:22:12Z | 403 | 548 bytes | `thechicagofiles_sullivan.html` | https://thechicagofiles.com/tag/daniel-pegleg-sullivan/ |
| 2026-09-14T06:22:13Z | 202 | 0 bytes | `howstuffworks.html` | https://history.howstuffworks.com/history-vs-myth/chicago-fire-cow.htm |
| 2026-09-14T06:22:13Z | 200 | 142946 bytes | `timeout_2015.html` | https://timeout.com/chicago/blog/catherine-olearys-cow-probably-did-not-start-the-great-chicago-fire-100815 |
| 2026-09-14T06:22:13Z | 200 | 16127 bytes | `didthecowdoit_weebly.html` | https://didthecowdoit.weebly.com/daniel-peg-leg-sullivan.html |
| 2026-09-14T06:22:15Z | 200 | 276940 bytes | `morningagclips.html` | https://www.morningagclips.com/still-smoldering-mrs-olearys-cow-the-great-chicago-fire-and-a-myth-that-never-died/ |
| 2026-09-14T06:25:13Z | 403 | 6266 bytes | `satevepost_2021.html` | https://www.saturdayeveningpost.com/2021/10/considering-history-mrs-olearys-cow-didnt-start-the-great-chicago-fire-why-does-it-matter/ |
| 2026-09-14T06:25:14Z | 200 | 317557 bytes | `abc7_2021.html` | https://abc7chicago.com/post/great-chicago-fire-history-musuem-in-historic/11098508/ |
| 2026-09-14T06:25:14Z | 200 | 751084 bytes | `suntimes_steinberg_2021.html` | https://chicago.suntimes.com/2021/10/8/22673310/chicago-fire-150-anniversary-oleary-mary-todd-lincoln-sheridan-grant-park-steinberg |
| 2026-09-14T06:25:15Z | 403 | 5815 bytes | `wttw_2021.html` | https://news.wttw.com/2021/10/07/chicago-history-museum-remembers-great-fire-1871 |
| 2026-09-14T06:25:15Z | 200 | 56911 bytes | `smithsonian_2021.html` | https://www.smithsonianmag.com/smart-news/chicagos-great-fire-150-years-later-180978861/ |
| 2026-09-14T06:25:15Z | 404 | 88251 bytes | `chicagomag_2021.html` | https://www.chicagomag.com/chicago-magazine/october-2021/inside-the-great-chicago-fire/ |
| 2026-09-14T06:27:41Z | 200 | 12812 bytes | `../gcf/selected-bibliography.html` | https://greatchicagofire.org/selected-bibliography/ |
| 2026-09-14T06:27:41Z | 403 | 5776 bytes | `newspapers_blog_150th.html` | https://blog.newspapers.com/150th-anniversary-of-the-great-chicago-fire/ |
| 2026-09-14T06:27:41Z | 200 | 3984 bytes | `imh_review_miller.html` | https://scholarworks.iu.edu/journals/index.php/imh/article/view/11244/16198 |
| 2026-09-14T06:27:41Z | 403 | 5949 bytes | `studs_terkel_miller.html` | https://studsterkel.wfmt.com/programs/ross-miller-discusses-his-book-american-apocalypse-great-fire-and-myth-chicago |
| 2026-09-14T06:27:42Z | 200 | 134888 bytes | `hhhistory_2021.html` | https://www.hhhistory.com/2021/10/the-great-chicago-fire-its-150-year.html |
| 2026-09-14T06:27:43Z | 200 | 664484 bytes | `suntimes_exhibit_2021.html` | https://chicago.suntimes.com/2021/10/8/22667265/great-chicago-fire-150th-anniversary-marked-new-museum-exhibit-city-tours |
| 2026-09-14T06:28:23Z | 200 | 146750 bytes | `imh_review_miller.pdf` | https://scholarworks.iu.edu/journals/index.php/imh/article/download/11244/16198 |
| 2026-09-14T06:29:04Z | 200 | 95 bytes | `wiki/opensearch_pegleg.json` | https://en.wikipedia.org/w/api.php?action=opensearch&search=Peg%20Leg%20Sullivan&limit=10&format=json |
| 2026-09-14T06:29:04Z | 403 | 5879 bytes | `web/upi_1985_waskin.html` | https://www.upi.com/Archives/1985/12/31/Author-links-Chicago-fire-to-stray-comet/9971504853200 |
| 2026-09-14T06:29:04Z | 200 | 36 bytes | `wiki/opensearch_sullivan.json` | https://en.wikipedia.org/w/api.php?action=opensearch&search=Daniel%20Sullivan%20Chicago&limit=10&format=json |
| 2026-09-14T06:29:29Z | 200 | 46 bytes | `wiki/wiki_Pegleg_Sullivan.wikitext` | https://en.wikipedia.org/w/index.php?title=Pegleg_Sullivan&action=raw |
| 2026-09-14T06:29:29Z | 429 | 278 bytes | `wiki/Catherine_OLeary.html` | https://en.wikipedia.org/api/rest_v1/page/html/Catherine_O%27Leary |
| 2026-09-14T06:29:29Z | 200 | 326015 bytes | `wiki/Pegleg_Sullivan.html` | https://en.wikipedia.org/api/rest_v1/page/html/Pegleg_Sullivan |
| 2026-09-14T06:32:13Z | 200 | 120207 bytes | `web/glessner_olearys_2021.html` | http://glessnerhouse.blogspot.com/2021/10/chicago-fire-stories-part-iii-catherine.html |
| 2026-09-14T06:32:13Z | 200 | 718825 bytes | `web/chm_meet_the_olearys.pdf` | https://www.chicagohistory.org/app/uploads/2023/08/Meet-the-OLearys-Biography-English.pdf |
| 2026-09-14T06:32:13Z | 202 | 0 bytes | `web/wikitree_hannigan405.html` | https://www.wikitree.com/wiki/Hannigan-405 |
| 2026-09-14T06:32:14Z | 200 | 55827 bytes | `web/carlsmith_nu_webprojects.html` | https://carlsmith.northwestern.edu/web-projects |
| 2026-09-14T06:32:14Z | 200 | 59400 bytes | `web/carlsmith_nu_p15.html` | https://carlsmith.northwestern.edu/?p=15 |
| 2026-09-14T06:32:56Z | 429 | 278 bytes | `wiki/rev_Louis_M_Cohn.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Louis_M._Cohn&rvlimit=30&rvprop=ids|timestamp|comment|size&format=json |
| 2026-09-14T06:33:02Z | 200 | 794 bytes | `wiki/rev_Pegleg_Sullivan.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Pegleg_Sullivan&rvlimit=30&rvprop=ids|timestamp|comment|size&format=json |
| 2026-09-14T06:33:03Z | 200 | 9279 bytes | `wiki/infogalactic_GCF.html` | https://infogalactic.com/info/Great_Chicago_Fire |
| 2026-09-14T06:33:03Z | 200 | 1070428 bytes | `web/ethier_backmatter.pdf` | http://www.math.utah.edu/~ethier/backmatter.pdf |
| 2026-09-14T06:33:46Z | 429 | 278 bytes | `wiki/rev_Daniel_Sullivan_GCF.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Daniel_Sullivan_(Great_Chicago_Fire)&rvlimit=20&rvprop=ids|timestamp|comment|size&format=json |
| 2026-09-14T06:34:01Z | 200 | 3547 bytes | `wiki/rev_Louis_M_Cohn.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Louis_M._Cohn&rvlimit=20&rvprop=ids|timestamp|comment|size&format=json |
| 2026-09-14T06:38:25Z | 200 | 1856 bytes | `wiki/Louis_M_Cohn_oldid613162809.wikitext` | https://en.wikipedia.org/w/index.php?title=Louis_M._Cohn&action=raw&oldid=613162809 |
| 2026-09-14T06:38:44Z | 200 | 611 bytes | `wiki/rev_Daniel_Sullivan_GCF.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Daniel_Sullivan_(Great_Chicago_Fire)|Daniel_Sullivan_(Chicago_Fire)|Pegleg_Sullivan&rvprop=ids|timestamp|comment|size|user&rvlimit=30&format=json&formatversion=2 |
| 2026-09-14T06:39:14Z | 429 | 278 bytes | `wiki/rev_Daniel_Sullivan_GCF.json` | https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Daniel_Sullivan_(Great_Chicago_Fire)&rvprop=ids|timestamp|comment|size|user&rvlimit=40&format=json&formatversion=2 |
| 2026-09-14T06:41:06Z | 200 | 216777 bytes | `wiki/history_Daniel_Sullivan_GCF.html` | https://en.wikipedia.org/w/index.php?title=Daniel_Sullivan_(Great_Chicago_Fire)&action=history&limit=50 |
| 2026-09-14T06:42:34Z | 200 | 1819 bytes | `wiki/Daniel_Sullivan_GCF_oldid531309478.wikitext` | https://en.wikipedia.org/w/index.php?title=Daniel_Sullivan_(Great_Chicago_Fire)&action=raw&oldid=531309478 |
| 2026-09-14T06:45:20Z | 000 | 0 bytes | `misc/ia_search_bales1997.json` | https://archive.org/advancedsearch.php?q=%28%22did+the+cow+do+it%22%29+OR+%28bales+%22illinois+historical+journal%22%29+OR+%28%22illinois+historical+journal%22+1997%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=creator&fl%5B%5D=collection&rows=50&output=json |
| 2026-09-14T06:45:31Z | 000 | 0 bytes | `misc/ia_search_ihj.json` | https://archive.org/advancedsearch.php?q=title%3A%28%22illinois+historical+journal%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=volume&rows=100&output=json |
| 2026-09-14T06:45:32Z | 200 | 1103 bytes | `misc/niu_search_cow.html` | https://digital.lib.niu.edu/islandora/search/%22did%20the%20cow%20do%20it%22?type=dismax |
| 2026-09-14T06:45:33Z | 200 | 1089 bytes | `misc/niu_search_bales.html` | https://digital.lib.niu.edu/islandora/search/bales%20o%27leary?type=dismax |
| 2026-09-14T06:46:01Z | 200 | 714 bytes | `misc/ia_search_bales1997.json` | https://archive.org/advancedsearch.php?q=%28%22did+the+cow+do+it%22%29+OR+%28bales+%22illinois+historical+journal%22%29+OR+title%3A%28%22illinois+historical+journal%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=creator&fl%5B%5D=collection&rows=100&output=json |
| 2026-09-14T06:47:43Z | 200 | 1437767 bytes | `web/fedler_1985_ERIC_ED257108.pdf` | https://files.eric.ed.gov/fulltext/ED257108.pdf |
| 2026-09-14T06:47:46Z | 200 | 2109 bytes | `misc/ia_search_andreas_critchell.json` | https://archive.org/advancedsearch.php?q=%28creator%3A%28andreas%29+AND+title%3A%28history+of+chicago%29%29+OR+%28critchell+recollections%29+OR+%28identifier%3Arecollectionsaf00critgoog%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=volume&fl%5B%5D=creator&rows=60&output=json |
| 2026-09-14T06:48:09Z | 200 | 7058582 bytes | `ia/andreas_history_of_chicago_v2_1885_djvu.txt` | https://archive.org/download/historyofchicago02andr/historyofchicago02andr_djvu.txt |
| 2026-09-14T06:48:16Z | 200 | 299092 bytes | `ia/critchell_recollections_1909_djvu.txt` | https://archive.org/download/recollectionsaf00critgoog/recollectionsaf00critgoog_djvu.txt |
| 2026-09-14T07:10:22Z | 200 | 184847 bytes | `web/tribune_debartolo_1997-10-08.html` | https://www.chicagotribune.com/news/ct-xpm-1997-10-08-9710080167-story.html |
| 2026-09-14T07:10:23Z | 200 | 189600 bytes | `web/tribune_debartolo_1998-03-03.html` | https://www.chicagotribune.com/news/ct-xpm-1998-03-03-9803030082-story.html |
| 2026-09-14T07:10:40Z | 200 | 178617 bytes | `web/tribune_potash_2006-10-06.html` | https://www.chicagotribune.com/news/ct-xpm-2006-10-06-0610060372-story.html |
| 2026-09-14T07:10:59Z | 200 | 177043 bytes | `web/tribune_1997-10-06_council_committee.html` | https://www.chicagotribune.com/news/ct-xpm-1997-10-06-9710070022-story.html |
| 2026-09-14T07:11:26Z | 200 | 209697 bytes | `web/tribune_2021-09-28_survivors.html` | https://www.chicagotribune.com/2021/09/28/the-great-chicago-fire-destroyed-17450-buildings-here-are-six-that-survived-and-still-stand-today/ |
| 2026-09-14T07:12:02Z | 200 | 296549 bytes | `web/abebooks_bales_signed.html` | https://www.abebooks.com/signed-first-edition/Great-Chicago-Fire-Myth-Mrs-OLearys/32111547520/bd |
| 2026-09-14T07:12:03Z | 200 | 53488 bytes | `web/iaedjournal_lesson_in_prevention.html` | https://www.iaedjournal.org/a-lesson-in-prevention |
| 2026-09-14T07:12:04Z | 200 | 422137 bytes | `web/phillytrib_clarence_page.html` | https://www.phillytrib.com/commentary/clarence-page-still-we-ask-what-caused-the-great-chicago-fire/article_da09ffba-4ab9-5c5c-978d-2ab2f06283ea.html |
| 2026-09-14T07:12:04Z | 000 | 0 bytes | `web/chicagonow_byrne_2021.html` | https://www.chicagonow.com/dennis-byrnes-barbershop/2021/10/a-comet-caused-the-chicago-fire-and-a-worse-one-in-peshtigo-wis/ |
| 2026-09-14T07:12:05Z | 403 | 5886 bytes | `web/umich_works_cited.html` | https://public.websites.umich.edu/~eng217/student_projects/chicago%20fire/Works%20Cited.htm |
| 2026-09-14T07:14:05Z | 403 | 5751 bytes | `web/wttw_city_on_fire.html` | https://www.wttw.com/chicago-stories/chicago-fire/the-city-on-fire |
| 2026-09-14T07:14:05Z | 403 | 5835 bytes | `web/wttw_investigating_cause.html` | https://www.wttw.com/chicago-stories/chicago-fire/video?v=investigating-cause-fire |
| 2026-09-14T07:14:06Z | 200 | 123416 bytes | `web/chicago1871_media_mentions.html` | https://www.chicago1871.org/media-mentions |
| 2026-09-14T07:14:06Z | 200 | 73433 bytes | `web/chm_press_2021.html` | https://www.chicagohistory.org/chicago-history-museum-commemorates-150th-anniversary-of-great-chicago-fire-in-new-exhibition/ |
| 2026-09-14T07:14:07Z | 200 | 225752 bytes | `web/firehouse_exhibit_2021.html` | https://www.firehouse.com/historical-incidents/news/21240263/exhibit-marks-150-years-since-great-chicago-fire-firefighters |
| 2026-09-14T07:14:07Z | 200 | 300532 bytes | `web/archive_cspan_smith_2021.html` | https://archive.org/details/CSPAN3_20211128_151100_Carl_Smith_Chicagos_Great_Fire |
| 2026-09-14T07:14:08Z | 200 | 664484 bytes | `web/suntimes_2021-10-08_anniversary.html` | https://chicago.suntimes.com/2021/10/8/22667265/great-chicago-fire-150th-anniversary-marked-new-museum-exhibit-city-tours |
| 2026-09-14T07:14:08Z | 200 | 349329 bytes | `web/nbcchicago_dont_blame.html` | https://www.nbcchicago.com/news/local/dont-blame-mrs-olearys-cow-for-the-great-chicago-fire/2631627/ |
| 2026-09-14T07:14:15Z | 200 | 182294 bytes | `web/kirkus_smith_2020.html` | https://www.kirkusreviews.com/book-reviews/carl-smith/chicagos-great-fire/ |

## B. Library of Congress Chronicling America page fetches (ca/CA_FETCH_LOG.txt)

Each page = item JSON (`fo=json`) then the OCR full-text JSON named in `resource.fulltext_file`; the plain text was saved as `ca/<lccn>_<date>_ed<N>_p<M>.txt`. KEY_*.txt files are hand-cut excerpts of those OCR texts.

| time (UTC) | code | local file | URL |
|---|---|---|---|
| 2026-09-14T06:08:02Z | 200 | `ca/sn83021205_1871-10-10_ed1_p2.json` | https://www.loc.gov/resource/sn83021205/1871-10-10/ed-1/?sp=2&fo=json |
| 2026-09-14T06:08:02Z | 200 | `ca/sn83021205_1871-10-10_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/mb/batch_mb_demeter_ver01/data/sn83021205/00517171888/1871101001/0958.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:04Z | 200 | `ca/sn83030313_1871-10-11_ed1_p5.json` | https://www.loc.gov/resource/sn83030313/1871-10-11/ed-1/?sp=5&fo=json |
| 2026-09-14T06:08:04Z | 200 | `ca/sn83030313_1871-10-11_ed1_p5.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_juneberry_ver01/data/sn83030313/00271743762/1871101101/0152.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:41Z | 200 | `ca/sn82014367_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn82014367/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:08:41Z | 200 | `ca/sn82014367_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/arhi/batch_arhi_aragonite_ver01/data/sn82014367/00513688350/1871101101/0928.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:43Z | 200 | `ca/sn82014248_1871-10-11_ed1_p3.json` | https://www.loc.gov/resource/sn82014248/1871-10-11/ed-1/?sp=3&fo=json |
| 2026-09-14T06:08:43Z | 200 | `ca/sn82014248_1871-10-11_ed1_p3.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/me/batch_me_dyerbrook_ver01/data/sn82014248/00332895175/1871101101/1018.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:45Z | 200 | `ca/sn84026118_1871-10-11_ed1_p2.json` | https://www.loc.gov/resource/sn84026118/1871-10-11/ed-1/?sp=2&fo=json |
| 2026-09-14T06:08:45Z | 200 | `ca/sn84026118_1871-10-11_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/pst/batch_pst_fenske_ver02/data/sn84026118/00280776348/1871101101/0167.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:47Z | 200 | `ca/sn83021432_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83021432/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:08:47Z | 200 | `ca/sn83021432_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/rp/batch_rp_jarlstorvald_ver01/data/sn83021432/00529045207/1871101101/1007.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:49Z | 200 | `ca/sn84026847_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn84026847/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:08:49Z | 200 | `ca/sn84026847_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/wvu/batch_wvu_deforest_ver02/data/sn84026847/00415665131/1871101101/0351.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:08:51Z | 200 | `ca/sn82014064_1871-10-19_ed1_p2.json` | https://www.loc.gov/resource/sn82014064/1871-10-19/ed-1/?sp=2&fo=json |
| 2026-09-14T06:08:51Z | 200 | `ca/sn82014064_1871-10-19_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_clark_ver03/data/sn82014064/no_reel/1871101901/0002.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:09:01Z | 200 | `ca/sn82014064_1871-10-20_ed1_p2.json` | https://www.loc.gov/resource/sn82014064/1871-10-20/ed-1/?sp=2&fo=json |
| 2026-09-14T06:09:01Z | 200 | `ca/sn82014064_1871-10-20_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_clark_ver03/data/sn82014064/no_reel/1871102001/0002.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:09:02Z | 200 | `ca/sn83030214_1871-10-13_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-13/ed-1/?sp=1&fo=json |
| 2026-09-14T06:09:02Z | 200 | `ca/sn83030214_1871-10-13_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_fortran_ver02/data/sn83030214/00206531095/1871101301/0299.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:09:04Z | 200 | `ca/sn85033123_1871-10-12_ed1_p4.json` | https://www.loc.gov/resource/sn85033123/1871-10-12/ed-1/?sp=4&fo=json |
| 2026-09-14T06:09:04Z | 200 | `ca/sn85033123_1871-10-12_ed1_p4.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/whi/batch_whi_dynamite_ver01/data/sn85033123/00514151222/1871101201/0156.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:09:07Z | 200 | `ca/sn82014064_1871-10-27_ed1_p2.json` | https://www.loc.gov/resource/sn82014064/1871-10-27/ed-1/?sp=2&fo=json |
| 2026-09-14T06:09:07Z | 200 | `ca/sn82014064_1871-10-27_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_clark_ver03/data/sn82014064/no_reel/1871102701/0002.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:17Z | 200 | `ca/sn84024670_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn84024670/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:17Z | 200 | `ca/sn84024670_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/vi/batch_vi_forego_ver01/data/sn84024670/00280762398/1871101001/0354.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:18Z | 200 | `ca/sn83030272_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83030272/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:18Z | 200 | `ca/sn83030272_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/nn/batch_nn_brown_ver01/data/sn83030272/00206536135/1871101101/0142.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:20Z | 200 | `ca/sn83045462_1871-10-13_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-13/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:20Z | 200 | `ca/sn83045462_1871-10-13_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_mastiff_ver01/data/sn83045462/0028065436A/1871101301/0532.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:22Z | 200 | `ca/sn85033437_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn85033437/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:22Z | 200 | `ca/sn85033437_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/tu/batch_tu_grady_ver01/data/sn85033437/0020029371A/1871101101/0336.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:24Z | 200 | `ca/sn84026994_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn84026994/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:24Z | 200 | `ca/sn84026994_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/scu/batch_scu_brandonblaze_ver01/data/sn84026994/00294551608/1871101101/0137.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:15:27Z | 200 | `ca/sn84026844_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn84026844/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:15:27Z | 200 | `ca/sn84026844_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/wvu/batch_wvu_belgium_ver01/data/sn84026844/00202190868/1871101101/0964.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:18:49Z | 200 | `ca/sn83030214_1871-10-09_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-09/ed-1/?sp=1&fo=json |
| 2026-09-14T06:18:49Z | 200 | `ca/sn83030214_1871-10-09_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_fortran_ver02/data/sn83030214/00206531095/1871100901/0263.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:18:52Z | 200 | `ca/sn83045462_1871-10-09_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-09/ed-1/?sp=1&fo=json |
| 2026-09-14T06:18:52Z | 200 | `ca/sn83045462_1871-10-09_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_mastiff_ver01/data/sn83045462/0028065436A/1871100901/0516.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:18:54Z | 429 | `ca/sn83030214_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:39Z | 520 | `ca/sn85033699_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn85033699/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:42Z | 200 | `ca/sn84026994_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn84026994/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:42Z | 200 | `ca/sn84026994_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/scu/batch_scu_brandonblaze_ver01/data/sn84026994/00294551608/1871101001/0133.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:19:44Z | 200 | `ca/sn83030272_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83030272/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:44Z | 200 | `ca/sn83030272_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/nn/batch_nn_brown_ver01/data/sn83030272/00206536135/1871101001/0138.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:19:45Z | 429 | `ca/sn83030214_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:45Z | 429 | `ca/sn83045462_1871-10-12_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-12/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:45Z | 200 | `ca/sn85033699_1871-10-19_ed1_p2.json` | https://www.loc.gov/resource/sn85033699/1871-10-19/ed-1/?sp=2&fo=json |
| 2026-09-14T06:19:45Z | 200 | `ca/sn85033699_1871-10-19_ed1_p2.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/tu/batch_tu_elvis_ver01/data/sn85033699/00200293447/1871101901/0378.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:19:47Z | 200 | `ca/sn85033699_1871-11-11_ed1_p1.json` | https://www.loc.gov/resource/sn85033699/1871-11-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:47Z | 200 | `ca/sn85033699_1871-11-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/tu/batch_tu_elvis_ver01/data/sn85033699/00200293447/1871111101/0457.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:19:48Z | 429 | `ca/sn83045462_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:19:50Z | 200 | `ca/sn83030313_1871-10-10_ed1_p3.json` | https://www.loc.gov/resource/sn83030313/1871-10-10/ed-1/?sp=3&fo=json |
| 2026-09-14T06:19:50Z | 200 | `ca/sn83030313_1871-10-10_ed1_p3.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_juneberry_ver01/data/sn83030313/00271743762/1871101001/0132.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:20:31Z | 429 | `ca/sn83030214_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:20:41Z | 200 | `ca/sn85033699_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn85033699/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:20:41Z | 525 | `ca/sn85033699_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/tu/batch_tu_elvis_ver01/data/sn85033699/00200293447/1871101001/0345.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:21:30Z | 429 | `ca/sn83045462_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:21:38Z | 429 | `ca/sn83030214_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:26:13Z | 200 | `ca/sn83030214_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:26:13Z | 200 | `ca/sn83030214_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_fortran_ver02/data/sn83030214/00206531095/1871101001/0271.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:26:25Z | 200 | `ca/sn83045462_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:26:25Z | 200 | `ca/sn83045462_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_mastiff_ver01/data/sn83045462/0028065436A/1871101001/0520.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:27:46Z | 200 | `ca/sn85033699_1871-10-10_ed1_p1.json` | https://www.loc.gov/resource/sn85033699/1871-10-10/ed-1/?sp=1&fo=json |
| 2026-09-14T06:27:46Z | 200 | `ca/sn85033699_1871-10-10_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/tu/batch_tu_elvis_ver01/data/sn85033699/00200293447/1871101001/0345.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:27:57Z | 429 | `ca/sn83030214_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:28:08Z | 429 | `ca/sn83045462_1871-10-12_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-12/ed-1/?sp=1&fo=json |
| 2026-09-14T06:39:31Z | 200 | `ca/sn83030214_1871-10-11_ed1_p1.json` | https://www.loc.gov/resource/sn83030214/1871-10-11/ed-1/?sp=1&fo=json |
| 2026-09-14T06:39:31Z | 200 | `ca/sn83030214_1871-10-11_ed1_p1.fulltext.json` | https://tile.loc.gov/text-services/word-coordinates-service?segment=/service/ndnp/dlc/batch_dlc_fortran_ver02/data/sn83030214/00206531095/1871101101/0283.xml&format=alto_xml&full_text=1 |
| 2026-09-14T06:39:44Z | 429 | `ca/sn83045462_1871-10-12_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-12/ed-1/?sp=1&fo=json |
| 2026-09-14T06:41:47Z | 429 | `ca/sn83045462_1871-10-12_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-12/ed-1/?sp=1&fo=json |
| 2026-09-14T06:44:16Z | 429 | `ca/sn83045462_1871-10-12_ed1_p1.json` | https://www.loc.gov/resource/sn83045462/1871-10-12/ed-1/?sp=1&fo=json |

## C. Google Books search-within queries (gbooks/QUERY_LOG.txt)

Volume rppt7mgfiKMC = Richard F. Bales, *The Great Chicago Fire and the Myth of Mrs. O'Leary's Cow* (McFarland; Google Books "partial view" edition dated 2015-09-01, ISBN 9781476604763). Each query returns page-numbered snippets; parsed results are in `gbooks/SNIPPETS.jsonl` and, in readable form, `gbooks/BALES_SNIPPETS_BY_QUERY.txt`. "SORRY-BLOCK" = Google's bot-block page; such attempts were retried on another Google host after a pause.

| time (UTC) | code | query | result | attempt | URL |
|---|---|---|---|---|---|
| 2026-09-14T06:03:44Z \| 403 \| q='Peg Leg' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Peg%20Leg&output=json | | | | | |
| 2026-09-14T06:03:47Z \| 200 \| q='William White' \| n=9 \| https://books.google.com/books?id=rppt7mgfiKMC&q=William%20White&output=json | | | | | |
| 2026-09-14T06:03:50Z \| 403 \| q='Dalton house' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Dalton%20house&output=json | | | | | |
| 2026-09-14T06:03:53Z \| 200 \| q='Regan' \| n=10 \| https://books.google.com/books?id=rppt7mgfiKMC&q=Regan&output=json | | | | | |
| 2026-09-14T06:03:56Z \| 403 \| q='McLaughlin' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=McLaughlin&output=json | | | | | |
| 2026-09-14T06:03:59Z \| 403 \| q='Cohn' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Cohn&output=json | | | | | |
| 2026-09-14T06:04:03Z \| 200 \| q='craps' \| n=6 \| https://books.google.com/books?id=rppt7mgfiKMC&q=craps&output=json | | | | | |
| 2026-09-14T06:04:06Z \| 403 \| q='Ahern' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Ahern&output=json | | | | | |
| 2026-09-14T06:04:09Z \| 403 \| q='Evening Journal' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Evening%20Journal&output=json | | | | | |
| 2026-09-14T06:04:12Z \| 200 \| q='Haynie' \| n=0 \| https://books.google.com/books?id=rppt7mgfiKMC&q=Haynie&output=json | | | | | |
| 2026-09-14T06:04:15Z \| 403 \| q='English' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=English&output=json | | | | | |
| 2026-09-14T06:04:18Z \| 403 \| q='tract' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=tract&output=json | | | | | |
| 2026-09-14T06:04:21Z \| 403 \| q='Chicago Title' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Title&output=json | | | | | |
| 2026-09-14T06:04:25Z \| 403 \| q='kerosene' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json | | | | | |
| 2026-09-14T06:04:28Z \| 403 \| q='lamp' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=lamp&output=json | | | | | |
| 2026-09-14T06:04:31Z \| 200 \| q='pipe' \| n=6 \| https://books.google.com/books?id=rppt7mgfiKMC&q=pipe&output=json | | | | | |
| 2026-09-14T06:04:34Z \| 403 \| q='smoking' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=smoking&output=json | | | | | |
| 2026-09-14T06:04:37Z \| 403 \| q='boys' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=boys&output=json | | | | | |
| 2026-09-14T06:04:40Z \| 200 \| q='spontaneous combustion' \| n=9 \| https://books.google.com/books?id=rppt7mgfiKMC&q=spontaneous%20combustion&output=json | | | | | |
| 2026-09-14T06:04:44Z \| 403 \| q='green hay' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=green%20hay&output=json | | | | | |
| 2026-09-14T06:04:47Z \| 200 \| q='comet' \| n=10 \| https://books.google.com/books?id=rppt7mgfiKMC&q=comet&output=json | | | | | |
| 2026-09-14T06:04:50Z \| 200 \| q='Biela' \| n=0 \| https://books.google.com/books?id=rppt7mgfiKMC&q=Biela&output=json | | | | | |
| 2026-09-14T06:04:53Z \| 200 \| q='Peshtigo' \| n=9 \| https://books.google.com/books?id=rppt7mgfiKMC&q=Peshtigo&output=json | | | | | |
| 2026-09-14T06:04:56Z \| 403 \| q='Pratt' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Pratt&output=json | | | | | |
| 2026-09-14T06:04:59Z \| 403 \| q='Burke' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Burke&output=json | | | | | |
| 2026-09-14T06:05:02Z \| 403 \| q='City Council' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=City%20Council&output=json | | | | | |
| 2026-09-14T06:05:05Z \| 403 \| q='exonerate' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=exonerate&output=json | | | | | |
| 2026-09-14T06:05:08Z \| 403 \| q='resolution' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=resolution&output=json | | | | | |
| 2026-09-14T06:05:11Z \| 403 \| q='Musham' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=Musham&output=json | | | | | |
| 2026-09-14T06:05:14Z \| 200 \| q='coverup' \| n=10 \| https://books.google.com/books?id=rppt7mgfiKMC&q=coverup&output=json | | | | | |
| 2026-09-14T06:05:18Z \| 403 \| q='charade' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=charade&output=json | | | | | |
| 2026-09-14T06:05:21Z \| 403 \| q='final report' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=final%20report&output=json | | | | | |
| 2026-09-14T06:05:24Z \| 200 \| q='spark' \| n=9 \| https://books.google.com/books?id=rppt7mgfiKMC&q=spark&output=json | | | | | |
| 2026-09-14T06:05:27Z \| 403 \| q='chimney' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=chimney&output=json | | | | | |
| 2026-09-14T06:05:30Z \| 403 \| q='unknown' \| n=no-results-block SORRY-BLOCK \| https://books.google.com/books?id=rppt7mgfiKMC&q=unknown&output=json | | | | | |
| 2026-09-14T06:07:41Z | 200 | 'Peg Leg' | 8 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Peg%20Leg&output=json |
| 2026-09-14T06:07:49Z | 403 | 'Dalton house' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Dalton%20house&output=json |
| 2026-09-14T06:08:16Z | 403 | 'Dalton house' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Dalton%20house&output=json |
| 2026-09-14T06:08:51Z | 200 | 'Dalton house' | 7 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Dalton%20house&output=json |
| 2026-09-14T06:09:03Z | 403 | 'McLaughlin' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=McLaughlin&output=json |
| 2026-09-14T06:09:44Z | 403 | 'McLaughlin' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=McLaughlin&output=json |
| 2026-09-14T06:10:20Z | 200 | 'McLaughlin' | 7 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=McLaughlin&output=json |
| 2026-09-14T06:10:33Z | 403 | 'Cohn' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:11:13Z | 403 | 'Cohn' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:11:53Z | 403 | 'Cohn' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:12:35Z | 403 | 'Cohn' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:13:17Z | 403 | 'Ahern' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Ahern&output=json |
| 2026-09-14T06:13:49Z | 200 | 'Ahern' | 9 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Ahern&output=json |
| 2026-09-14T06:13:58Z | 403 | 'Evening Journal' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Evening%20Journal&output=json |
| 2026-09-14T06:14:33Z | 403 | 'Evening Journal' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Evening%20Journal&output=json |
| 2026-09-14T06:15:08Z | 403 | 'Evening Journal' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Evening%20Journal&output=json |
| 2026-09-14T06:15:38Z | 200 | 'Evening Journal' | 10 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Evening%20Journal&output=json |
| 2026-09-14T06:15:47Z | 403 | 'English' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=English&output=json |
| 2026-09-14T06:16:13Z | 200 | 'English' | 0 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=English&output=json |
| 2026-09-14T06:16:23Z | 403 | 'tract' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=tract&output=json |
| 2026-09-14T06:16:50Z | 200 | 'tract' | 5 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=tract&output=json |
| 2026-09-14T06:16:58Z | 403 | 'Chicago Title' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Title&output=json |
| 2026-09-14T06:17:28Z | 403 | 'Chicago Title' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Title&output=json |
| 2026-09-14T06:17:58Z | 403 | 'Chicago Title' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Title&output=json |
| 2026-09-14T06:18:40Z | 200 | 'Chicago Title' | 9 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Title&output=json |
| 2026-09-14T06:18:47Z | 403 | 'kerosene' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:19:27Z | 403 | 'kerosene' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:19:57Z | 403 | 'kerosene' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:20:41Z | 403 | 'kerosene' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:21:18Z | 403 | 'lamp' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:21:52Z | 403 | 'lamp' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:22:21Z | 403 | 'lamp' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:22:52Z | 403 | 'lamp' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:23:34Z | 403 | 'smoking' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:24:44Z | 403 | 'Cohn' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:24:48Z | 200 | 'Cohn' | 10 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Cohn&output=json |
| 2026-09-14T06:24:54Z | 403 | 'kerosene' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:01Z | 403 | 'kerosene' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:07Z | 403 | 'kerosene' | SORRY-BLOCK | 2 | https://books.google.co.nz/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:13Z | 403 | 'kerosene' | SORRY-BLOCK | 3 | https://books.google.ie/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:20Z | 403 | 'kerosene' | SORRY-BLOCK | 4 | https://books.google.co.in/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:27Z | 403 | 'kerosene' | SORRY-BLOCK | 5 | https://books.google.co.za/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:25:37Z | 403 | 'lamp' | SORRY-BLOCK | 0 | https://books.google.com.sg/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:25:41Z | 403 | 'lamp' | SORRY-BLOCK | 1 | https://books.google.fr/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:25:46Z | 200 | 'lamp' | 10 | 2 | https://books.google.es/books?id=rppt7mgfiKMC&q=lamp&output=json |
| 2026-09-14T06:25:50Z | 403 | 'smoking' | SORRY-BLOCK | 0 | https://books.google.es/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:25:56Z | 403 | 'smoking' | SORRY-BLOCK | 1 | https://books.google.it/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:26:00Z | 403 | 'smoking' | SORRY-BLOCK | 2 | https://books.google.nl/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:26:05Z | 403 | 'smoking' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:26:11Z | 200 | 'smoking' | 9 | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=smoking&output=json |
| 2026-09-14T06:26:17Z | 403 | 'boys' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:26:24Z | 403 | 'boys' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:26:31Z | 403 | 'boys' | SORRY-BLOCK | 2 | https://books.google.co.nz/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:26:37Z | 403 | 'boys' | SORRY-BLOCK | 3 | https://books.google.ie/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:26:41Z | 403 | 'boys' | SORRY-BLOCK | 4 | https://books.google.co.in/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:26:48Z | 403 | 'boys' | SORRY-BLOCK | 5 | https://books.google.co.za/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:29:29Z | 403 | 'kerosene' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:30:25Z | 200 | 'kerosene' | 7 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=kerosene&output=json |
| 2026-09-14T06:30:39Z | 200 | 'boys' | 8 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=boys&output=json |
| 2026-09-14T06:30:53Z | 403 | 'green hay' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:32:03Z | 403 | 'green hay' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:33:10Z | 403 | 'green hay' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:34:00Z | 403 | 'green hay' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:34:55Z | 403 | 'green hay' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:35:40Z | 403 | 'green hay' | SORRY-BLOCK | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=green%20hay&output=json |
| 2026-09-14T06:36:35Z | 200 | 'Pratt' | 2 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Pratt&output=json |
| 2026-09-14T06:36:51Z | 403 | 'Burke' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Burke&output=json |
| 2026-09-14T06:37:46Z | 403 | 'Burke' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Burke&output=json |
| 2026-09-14T06:38:32Z | 200 | 'Burke' | 1 | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Burke&output=json |
| 2026-09-14T06:38:51Z | 403 | 'City Council' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=City%20Council&output=json |
| 2026-09-14T06:39:44Z | 200 | 'City Council' | 9 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=City%20Council&output=json |
| 2026-09-14T06:40:02Z | 200 | 'exonerate' | 0 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=exonerate&output=json |
| 2026-09-14T06:40:15Z | 403 | 'resolution' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=resolution&output=json |
| 2026-09-14T06:41:11Z | 403 | 'resolution' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=resolution&output=json |
| 2026-09-14T06:41:52Z | 403 | 'resolution' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=resolution&output=json |
| 2026-09-14T06:42:37Z | 200 | 'resolution' | 1 | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=resolution&output=json |
| 2026-09-14T06:42:57Z | 403 | 'Musham' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:43:44Z | 403 | 'Musham' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:44:32Z | 403 | 'Musham' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:45:17Z | 403 | 'Musham' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:46:19Z | 403 | 'Musham' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:47:28Z | 403 | 'Musham' | SORRY-BLOCK | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Musham&output=json |
| 2026-09-14T06:48:51Z | 403 | 'charade' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=charade&output=json |
| 2026-09-14T06:49:33Z | 200 | 'charade' | 10 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=charade&output=json |
| 2026-09-14T06:49:53Z | 403 | 'final report' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=final%20report&output=json |
| 2026-09-14T06:50:44Z | 200 | 'final report' | 9 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=final%20report&output=json |
| 2026-09-14T06:51:04Z | 403 | 'chimney' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=chimney&output=json |
| 2026-09-14T06:52:05Z | 403 | 'chimney' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=chimney&output=json |
| 2026-09-14T06:53:06Z | 403 | 'chimney' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=chimney&output=json |
| 2026-09-14T06:53:48Z | 403 | 'chimney' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=chimney&output=json |
| 2026-09-14T06:54:48Z | 200 | 'chimney' | 9 | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=chimney&output=json |
| 2026-09-14T06:55:03Z | 403 | 'unknown' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=unknown&output=json |
| 2026-09-14T06:55:46Z | 200 | 'unknown' | 10 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=unknown&output=json |
| 2026-09-14T06:56:00Z | 403 | 'timeline' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=timeline&output=json |
| 2026-09-14T06:56:53Z | 200 | 'timeline' | 0 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=timeline&output=json |
| 2026-09-14T06:57:09Z | 403 | 'Sunday evening' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T06:58:08Z | 403 | 'Sunday evening' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T06:59:09Z | 403 | 'Sunday evening' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T07:00:16Z | 403 | 'Sunday evening' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T07:01:18Z | 403 | 'Sunday evening' | SORRY-BLOCK | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T07:01:59Z | 200 | 'Sunday evening' | 8 | 5 | https://books.google.com/books?id=rppt7mgfiKMC&q=Sunday%20evening&output=json |
| 2026-09-14T07:02:21Z | 200 | "eight o'clock" | 9 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=eight%20o%27clock&output=json |
| 2026-09-14T07:02:39Z | 200 | "nine o'clock" | 9 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=nine%20o%27clock&output=json |
| 2026-09-14T07:02:58Z | 403 | 'Goll' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Goll&output=json |
| 2026-09-14T07:04:06Z | 200 | 'Goll' | 9 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Goll&output=json |
| 2026-09-14T07:04:21Z | 403 | 'Schaefer' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Schaefer&output=json |
| 2026-09-14T07:05:25Z | 403 | 'Schaefer' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Schaefer&output=json |
| 2026-09-14T07:06:25Z | 200 | 'Schaefer' | 0 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Schaefer&output=json |
| 2026-09-14T07:06:50Z | 403 | 'watchman' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=watchman&output=json |
| 2026-09-14T07:07:39Z | 200 | 'watchman' | 8 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=watchman&output=json |
| 2026-09-14T07:08:00Z | 200 | 'Denis Regan' | 10 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Denis%20Regan&output=json |
| 2026-09-14T07:08:21Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:09:06Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:10:01Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:11:01Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:11:53Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:12:54Z | 403 | 'Catherine Sullivan' | SORRY-BLOCK | 5 | https://books.google.com/books?id=rppt7mgfiKMC&q=Catherine%20Sullivan&output=json |
| 2026-09-14T07:13:59Z | 200 | "Sullivan's mother" | 0 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Sullivan%27s%20mother&output=json |
| 2026-09-14T07:14:11Z | 403 | 'Forbes' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Forbes&output=json |
| 2026-09-14T07:15:21Z | 200 | 'Forbes' | 7 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Forbes&output=json |
| 2026-09-14T07:15:35Z | 200 | 'Cromie' | 8 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Cromie&output=json |
| 2026-09-14T07:15:48Z | 403 | 'Kogan' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Kogan&output=json |
| 2026-09-14T07:16:50Z | 200 | 'Kogan' | 0 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Kogan&output=json |
| 2026-09-14T07:17:05Z | 403 | 'Sawislak' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Sawislak&output=json |
| 2026-09-14T07:17:53Z | 200 | 'Sawislak' | 8 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Sawislak&output=json |
| 2026-09-14T07:18:15Z | 403 | 'Carl Smith' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Carl%20Smith&output=json |
| 2026-09-14T07:19:05Z | 200 | 'Carl Smith' | 9 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Carl%20Smith&output=json |
| 2026-09-14T07:19:23Z | 403 | 'Andreas' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:20:17Z | 403 | 'Andreas' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:21:22Z | 403 | 'Andreas' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:22:09Z | 403 | 'Andreas' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:23:07Z | 403 | 'Andreas' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:24:12Z | 200 | 'Andreas' | 7 | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Andreas&output=json |
| 2026-09-14T07:24:30Z | 403 | 'milk' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=milk&output=json |
| 2026-09-14T07:25:14Z | 200 | 'milk' | 9 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=milk&output=json |
| 2026-09-14T07:25:27Z | 200 | 'steal milk' | 3 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=steal%20milk&output=json |
| 2026-09-14T07:25:48Z | 403 | 'party' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:26:34Z | 403 | 'party' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:27:37Z | 403 | 'party' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:28:29Z | 403 | 'party' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:29:14Z | 403 | 'party' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:30:20Z | 403 | 'party' | SORRY-BLOCK | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=party&output=json |
| 2026-09-14T07:31:27Z | 200 | 'beer' | 0 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=beer&output=json |
| 2026-09-14T07:31:44Z | 403 | 'oyster' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=oyster&output=json |
| 2026-09-14T07:32:49Z | 403 | 'oyster' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=oyster&output=json |
| 2026-09-14T07:33:58Z | 403 | 'oyster' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=oyster&output=json |
| 2026-09-14T07:34:44Z | 403 | 'oyster' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=oyster&output=json |
| 2026-09-14T07:35:54Z | 200 | 'oyster' | 4 | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=oyster&output=json |
| 2026-09-14T07:36:07Z | 403 | 'Chicago Times' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chicago%20Times&output=json |
| 2026-09-14T07:36:49Z | 200 | 'Chicago Times' | 0 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Chicago%20Times&output=json |
| 2026-09-14T07:37:11Z | 403 | 'old hag' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:38:06Z | 403 | 'old hag' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:39:10Z | 403 | 'old hag' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:40:03Z | 403 | 'old hag' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:41:09Z | 403 | 'old hag' | SORRY-BLOCK | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:42:06Z | 403 | 'old hag' | SORRY-BLOCK | 5 | https://books.google.com/books?id=rppt7mgfiKMC&q=old%20hag&output=json |
| 2026-09-14T07:43:14Z | 403 | 'McDermott' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=McDermott&output=json |
| 2026-09-14T07:44:23Z | 200 | 'McDermott' | 0 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=McDermott&output=json |
| 2026-09-14T07:44:46Z | 403 | 'Big Jim' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Big%20Jim&output=json |
| 2026-09-14T07:45:42Z | 403 | 'Big Jim' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Big%20Jim&output=json |
| 2026-09-14T07:46:49Z | 403 | 'Big Jim' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Big%20Jim&output=json |
| 2026-09-14T07:47:41Z | 200 | 'Big Jim' | 0 | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Big%20Jim&output=json |
| 2026-09-14T07:48:02Z | 200 | "James O'Leary" | 0 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=James%20O%27Leary&output=json |
| 2026-09-14T07:48:18Z | 403 | 'Republican' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Republican&output=json |
| 2026-09-14T07:49:27Z | 403 | 'Republican' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Republican&output=json |
| 2026-09-14T07:50:26Z | 403 | 'Republican' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Republican&output=json |
| 2026-09-14T07:51:11Z | 200 | 'Republican' | 0 | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Republican&output=json |
| 2026-09-14T07:51:33Z | 403 | 'Inter Ocean' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Inter%20Ocean&output=json |
| 2026-09-14T07:52:29Z | 403 | 'Inter Ocean' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Inter%20Ocean&output=json |
| 2026-09-14T07:53:36Z | 403 | 'Inter Ocean' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Inter%20Ocean&output=json |
| 2026-09-14T07:54:30Z | 200 | 'Inter Ocean' | 0 | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Inter%20Ocean&output=json |
| 2026-09-14T07:54:47Z | 200 | 'Ryan' | 9 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Ryan&output=json |
| 2026-09-14T07:55:09Z | 200 | 'Benner' | 8 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Benner&output=json |
| 2026-09-14T07:55:30Z | 403 | 'Chadwick' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Chadwick&output=json |
| 2026-09-14T07:56:32Z | 200 | 'Chadwick' | 0 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=Chadwick&output=json |
| 2026-09-14T07:56:52Z | 403 | 'Sheridan' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Sheridan&output=json |
| 2026-09-14T07:57:42Z | 403 | 'Sheridan' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Sheridan&output=json |
| 2026-09-14T07:58:24Z | 403 | 'Sheridan' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Sheridan&output=json |
| 2026-09-14T07:59:24Z | 200 | 'Sheridan' | 5 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Sheridan&output=json |
| 2026-09-14T07:59:45Z | 403 | 'Schank' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Schank&output=json |
| 2026-09-14T08:00:38Z | 403 | 'Schank' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Schank&output=json |
| 2026-09-14T08:01:38Z | 403 | 'Schank' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Schank&output=json |
| 2026-09-14T08:02:27Z | 200 | 'Schank' | 9 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Schank&output=json |
| 2026-09-14T08:02:40Z | 403 | 'Mason' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:03:25Z | 403 | 'Mason' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:04:13Z | 403 | 'Mason' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:04:57Z | 403 | 'Mason' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:05:57Z | 403 | 'Mason' | SORRY-BLOCK | 4 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:06:56Z | 200 | 'Mason' | 6 | 5 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Mason&output=json |
| 2026-09-14T08:07:10Z | 200 | 'Medill' | 0 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Medill&output=json |
| 2026-09-14T08:07:28Z | 403 | 'cannot be proven' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=cannot%20be%20proven&output=json |
| 2026-09-14T08:08:26Z | 200 | 'cannot be proven' | 0 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=cannot%20be%20proven&output=json |
| 2026-09-14T08:08:48Z | 200 | 'I believe' | 5 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=I%20believe&output=json |
| 2026-09-14T08:09:07Z | 403 | 'speculation' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=speculation&output=json |
| 2026-09-14T08:10:08Z | 403 | 'speculation' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=speculation&output=json |
| 2026-09-14T08:11:00Z | 200 | 'speculation' | 1 | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=speculation&output=json |
| 2026-09-14T08:11:16Z | 403 | 'no one knows' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=no%20one%20knows&output=json |
| 2026-09-14T08:12:23Z | 403 | 'no one knows' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=no%20one%20knows&output=json |
| 2026-09-14T08:13:28Z | 403 | 'no one knows' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=no%20one%20knows&output=json |
| 2026-09-14T08:14:31Z | 403 | 'no one knows' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=no%20one%20knows&output=json |
| 2026-09-14T08:15:20Z | 200 | 'no one knows' | 9 | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=no%20one%20knows&output=json |
| 2026-09-14T08:15:43Z | 403 | 'circumstantial' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=circumstantial&output=json |
| 2026-09-14T08:16:37Z | 200 | 'circumstantial' | 0 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=circumstantial&output=json |
| 2026-09-14T08:16:51Z | 403 | 'impossible to determine' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=impossible%20to%20determine&output=json |
| 2026-09-14T08:17:34Z | 403 | 'impossible to determine' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=impossible%20to%20determine&output=json |
| 2026-09-14T08:18:22Z | 200 | 'impossible to determine' | 0 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=impossible%20to%20determine&output=json |
| 2026-09-14T08:18:44Z | 200 | 'beyond a reasonable doubt' | 1 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=beyond%20a%20reasonable%20doubt&output=json |
| 2026-09-14T08:18:58Z | 403 | 'hobbled' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:20:06Z | 403 | 'hobbled' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:21:02Z | 403 | 'hobbled' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:21:56Z | 403 | 'hobbled' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:22:49Z | 403 | 'hobbled' | SORRY-BLOCK | 4 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:23:46Z | 403 | 'hobbled' | SORRY-BLOCK | 5 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=hobbled&output=json |
| 2026-09-14T08:25:09Z | 403 | 'wooden leg' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=wooden%20leg&output=json |
| 2026-09-14T08:26:14Z | 403 | 'wooden leg' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=wooden%20leg&output=json |
| 2026-09-14T08:27:01Z | 403 | 'wooden leg' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=wooden%20leg&output=json |
| 2026-09-14T08:27:58Z | 200 | 'wooden leg' | 8 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=wooden%20leg&output=json |
| 2026-09-14T08:28:11Z | 403 | '193 feet' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=193%20feet&output=json |
| 2026-09-14T08:28:59Z | 403 | '193 feet' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=193%20feet&output=json |
| 2026-09-14T08:30:05Z | 403 | '193 feet' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=193%20feet&output=json |
| 2026-09-14T08:30:49Z | 200 | '193 feet' | 5 | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=193%20feet&output=json |
| 2026-09-14T08:31:07Z | 403 | 'feet' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=feet&output=json |
| 2026-09-14T08:32:13Z | 403 | 'feet' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=feet&output=json |
| 2026-09-14T08:32:57Z | 200 | 'feet' | 7 | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=feet&output=json |
| 2026-09-14T08:33:10Z | 403 | 'blocked' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=blocked&output=json |
| 2026-09-14T08:33:54Z | 403 | 'blocked' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=blocked&output=json |
| 2026-09-14T08:34:49Z | 200 | 'blocked' | 7 | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=blocked&output=json |
| 2026-09-14T08:35:11Z | 200 | 'line of sight' | 5 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=line%20of%20sight&output=json |
| 2026-09-14T08:35:30Z | 200 | 'fence' | 0 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=fence&output=json |
| 2026-09-14T08:35:51Z | 403 | 'Wykes' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Wykes&output=json |
| 2026-09-14T08:36:40Z | 403 | 'Wykes' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Wykes&output=json |
| 2026-09-14T08:37:32Z | 200 | 'Wykes' | 0 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Wykes&output=json |
| 2026-09-14T08:37:45Z | 200 | 'Feinberg' | 0 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Feinberg&output=json |
| 2026-09-14T08:38:06Z | 200 | '1944' | 5 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=1944&output=json |
| 2026-09-14T08:38:27Z | 200 | 'Medill School' | 0 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Medill%20School&output=json |
| 2026-09-14T08:38:43Z | 200 | 'Northwestern' | 0 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Northwestern&output=json |
| 2026-09-14T08:39:04Z | 200 | 'eighteen' | 0 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=eighteen&output=json |
| 2026-09-14T08:39:18Z | 403 | 'Rochester' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Rochester&output=json |
| 2026-09-14T08:40:22Z | 403 | 'Rochester' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Rochester&output=json |
| 2026-09-14T08:41:28Z | 403 | 'Rochester' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Rochester&output=json |
| 2026-09-14T08:42:10Z | 403 | 'Rochester' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Rochester&output=json |
| 2026-09-14T08:42:51Z | 200 | 'Rochester' | 0 | 4 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Rochester&output=json |
| 2026-09-14T08:43:05Z | 200 | '1893' | 0 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=1893&output=json |
| 2026-09-14T08:43:20Z | 403 | '1911' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=1911&output=json |
| 2026-09-14T08:44:01Z | 403 | '1911' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=1911&output=json |
| 2026-09-14T08:44:48Z | 403 | '1911' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=1911&output=json |
| 2026-09-14T08:45:49Z | 200 | '1911' | 9 | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=1911&output=json |
| 2026-09-14T08:46:11Z | 403 | '1921' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=1921&output=json |
| 2026-09-14T08:46:52Z | 403 | '1921' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=1921&output=json |
| 2026-09-14T08:47:57Z | 403 | '1921' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=1921&output=json |
| 2026-09-14T08:48:56Z | 403 | '1921' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=1921&output=json |
| 2026-09-14T08:49:52Z | 200 | '1921' | 9 | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=1921&output=json |
| 2026-09-14T08:50:05Z | 200 | 'reminiscences' | 7 | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=reminiscences&output=json |
| 2026-09-14T08:50:21Z | 403 | 'confession' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=confession&output=json |
| 2026-09-14T08:51:25Z | 200 | 'confession' | 4 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=confession&output=json |
| 2026-09-14T08:51:44Z | 403 | 'Journal extra' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Journal%20extra&output=json |
| 2026-09-14T08:52:31Z | 200 | 'Journal extra' | 10 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Journal%20extra&output=json |
| 2026-09-14T08:52:48Z | 200 | 'extra' | 10 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=extra&output=json |
| 2026-09-14T08:53:02Z | 200 | '9 October' | 8 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=9%20October&output=json |
| 2026-09-14T08:53:16Z | 403 | 'October 9' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=October%209&output=json |
| 2026-09-14T08:54:04Z | 200 | 'October 9' | 9 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=October%209&output=json |
| 2026-09-14T08:54:26Z | 403 | 'cow kicked' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T08:55:35Z | 403 | 'cow kicked' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T08:56:18Z | 403 | 'cow kicked' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T08:57:21Z | 403 | 'cow kicked' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T08:58:23Z | 403 | 'cow kicked' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T08:59:18Z | 403 | 'cow kicked' | SORRY-BLOCK | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=cow%20kicked&output=json |
| 2026-09-14T09:00:23Z | 403 | 'kicked over' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=kicked%20over&output=json |
| 2026-09-14T09:01:20Z | 403 | 'kicked over' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=kicked%20over&output=json |
| 2026-09-14T09:02:10Z | 200 | 'kicked over' | 9 | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=kicked%20over&output=json |
| 2026-09-14T09:02:24Z | 403 | 'October 18' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=October%2018&output=json |
| 2026-09-14T09:03:14Z | 200 | 'October 18' | 8 | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=October%2018&output=json |
| 2026-09-14T09:03:33Z | 403 | 'old woman' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:04:38Z | 403 | 'old woman' | SORRY-BLOCK | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:05:42Z | 403 | 'old woman' | SORRY-BLOCK | 2 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:06:31Z | 403 | 'old woman' | SORRY-BLOCK | 3 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:07:28Z | 403 | 'old woman' | SORRY-BLOCK | 4 | https://books.google.com/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:08:32Z | 200 | 'old woman' | 9 | 5 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=old%20woman&output=json |
| 2026-09-14T09:08:46Z | 403 | 'hag' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=hag&output=json |
| 2026-09-14T09:09:53Z | 403 | 'hag' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=hag&output=json |
| 2026-09-14T09:11:01Z | 200 | 'hag' | 5 | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=hag&output=json |
| 2026-09-14T09:11:22Z | 403 | 'pension' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=pension&output=json |
| 2026-09-14T09:12:10Z | 200 | 'pension' | 0 | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=pension&output=json |
| 2026-09-14T09:12:25Z | 200 | 'January 1997' | 0 | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=January%201997&output=json |
| 2026-09-14T09:12:41Z | 403 | 'Parsons' | SORRY-BLOCK | 0 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:13:29Z | 403 | 'Parsons' | SORRY-BLOCK | 1 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:14:14Z | 403 | 'Parsons' | SORRY-BLOCK | 2 | https://books.google.com/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:14:58Z | 403 | 'Parsons' | SORRY-BLOCK | 3 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:15:49Z | 403 | 'Parsons' | SORRY-BLOCK | 4 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:16:49Z | 200 | 'Parsons' | 0 | 5 | https://books.google.com/books?id=rppt7mgfiKMC&q=Parsons&output=json |
| 2026-09-14T09:17:09Z | 403 | 'Historian Finds' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:17:56Z | 403 | 'Historian Finds' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:18:55Z | 403 | 'Historian Finds' | SORRY-BLOCK | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:19:51Z | 403 | 'Historian Finds' | SORRY-BLOCK | 3 | https://books.google.com/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:20:34Z | 403 | 'Historian Finds' | SORRY-BLOCK | 4 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:21:26Z | 403 | 'Historian Finds' | SORRY-BLOCK | 5 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Historian%20Finds&output=json |
| 2026-09-14T09:22:45Z | 200 | 'Illinois Historical Journal' | 10 | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Illinois%20Historical%20Journal&output=json |
| 2026-09-14T09:23:00Z | 403 | 'Did the Cow Do It' | SORRY-BLOCK | 0 | https://books.google.com/books?id=rppt7mgfiKMC&q=Did%20the%20Cow%20Do%20It&output=json |
| 2026-09-14T09:23:44Z | 403 | 'Did the Cow Do It' | SORRY-BLOCK | 1 | https://books.google.co.uk/books?id=rppt7mgfiKMC&q=Did%20the%20Cow%20Do%20It&output=json |
| 2026-09-14T09:24:25Z | 200 | 'Did the Cow Do It' | 8 | 2 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=Did%20the%20Cow%20Do%20It&output=json |
| 2026-09-14T09:24:44Z | 403 | '1997' | SORRY-BLOCK | 0 | https://books.google.com.au/books?id=rppt7mgfiKMC&q=1997&output=json |
| 2026-09-14T09:25:39Z | 200 | '1997' | 0 | 1 | https://books.google.com/books?id=rppt7mgfiKMC&q=1997&output=json |

## D. Page-fetch tool attempts (webfetch/WEBFETCH_LOG.txt)

The page-fetch tool returns text extracted by a model from the live page, not raw HTML. It was used only for pages that refused curl (403/406). Saved extractions are in `webfetch/*.md`, each headed with URL, time and a warning; quotations from them are labelled "page-fetch extraction" in REPORT.md.

| status | local file | URL |
|---|---|---|
| 200 | `webfetch/newsweek_2021-10-08_cagnassola.md` | https://www.newsweek.com/150-years-later-debate-still-rages-over-cause-great-chicago-fire-1637181 |
| 200 | `webfetch/blockclub_2025-10-08_bauer.md` | https://blockclubchicago.org/2025/10/08/5-things-you-probably-didnt-know-about-the-great-chicago-fire/ |
| 200 | `webfetch/time_2015-10-08_latson.md` | https://time.com/4055770/great-chicago-fire-origins/ |
| 200 | `webfetch/satevepost_2021-10-08_railton.md` | https://www.saturdayeveningpost.com/2021/10/considering-history-mrs-olearys-cow-didnt-start-the-great-chicago-fire-why-does-it-matter/ |
| 403 | `webfetch/(none)` | https://news.wttw.com/2021/10/07/chicago-history-museum-remembers-great-fire-1871 |
| 403 | `webfetch/(none)` | https://forward.com/culture/476328/chicago-fire-jewish-1871-louis-cohn-oleary-how-did-it-start/ |
| 403 | `webfetch/(none)` | https://www.upi.com/Archives/1985/12/31/Author-links-Chicago-fire-to-stray-comet/9971504853200 |
| 404 | `webfetch/(none)` | https://www.chicagomag.com/chicago-magazine/october-2021/inside-the-great-chicago-fire/ |
