# Design plan: "The Death at Grinder's Stand"

Subject: an October 1809 death in a log stand on the Natchez Trace, known only through letters written by people who were not in the room. Audience: historians who will check each step. The page's single job: deliver a verdict that a specialist can audit line by line.

Grounding detail carried as content: Wilson's description of Lewis arriving in "a loose gown, white, striped with blue". The one motif on the page is a thin white-and-blue stripe band at the head of the verdict panel. Dates and money in the record are set in tabular figures; documents are cited by their Founders Online identifiers.

## Color
- Ground, "stripe white": #F4F5F2 (a cool white with a limestone cast, after the "Tennessee marble" of the 1848 monument)
- Ink, "iron gall": #22262A
- Accent, "Prussian blue": #2F4B7C (the blue of the striped gown and the 1809 army coat)
- Rule, "limestone": #C8CBC4
- Muted text: #5B6168
- Counter-case marker, "dried iron": #7A3B31 (semantic only: used where the homicide case is stated)
- Dark theme: ground #171A1D, ink #E4E3DD, accent #93B2E6, rule #363B41, muted #9AA1A8, counter #D08A7C

## Type
- Display: Libre Caslon Display (headings). Caslon is the face of the 1809 printings that carried the news (the Port Folio, the Clarion's reprints).
- Body: Libre Caslon Text.
- Utility: Public Sans (labels, tables, captions, the evidence model). Public Sans is the US federal government's typeface; the death was a federal matter and the site is federal ground.
- Fallbacks: Georgia, "Times New Roman", serif; system-ui, sans-serif.

## Layout
One reading column of about 66 characters, left-aligned, with a wider verdict panel at the top that sets the verdict, the confidence and the sensitivity table side by side. Tables that need width (the concordance, the evidence items) run wider than the column and scroll sideways on a phone. Section labels are small capitals in the utility face; the timeline uses a date column in tabular figures because it is a real sequence.
