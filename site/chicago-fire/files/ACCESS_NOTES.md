# Access notes
- All outbound HTTPS goes via a policy proxy. web.archive.org (Wayback) and archive.ph are BLOCKED.
- chsmedia.org (Chicago History Museum media server, hosts the 1871 inquiry transcription at
  http://chsmedia.org/media/fa/fa/M-C/ChgoFire-transcript.htm) is DOWN (503 upstream connect error / reset).
- Cloudflare JS challenge (HTTP 403 "Just a moment"): explore.chicagocollections.org, catalog/babel.hathitrust.org, images.chicagohistory.org, idnc.library.illinois.edu.
- Working: chicagology.com, greatchicagofire.org, loc.gov (Chronicling America JSON API at https://www.loc.gov/collections/chronicling-america/?q=...&dates=1871&fo=json), archive.org (public items; lending-library items give 401 on text files), google.com/books feeds (googleapis.com/books/v1 rate-limited 429), fultonhistory.com, newberry.org, digital.lib.niu.edu (islandora).
- Dead: dig.lib.niu.edu (no DNS), hydeparkmedia.com (521).
