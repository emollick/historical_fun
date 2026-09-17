#!/bin/bash
# usage: sgclip.sh <articleid>  -> downloads all clipping areas as PNG into clips/<articleid>_aN.png and saves metadata
id=$1; base=https://eresources.nlb.gov.sg/newspapers/digitised/article/$id
curl -sS -c sgjar.txt -b sgjar.txt -o "clips/$id.html" "$base"
n=$(grep -o 'Image clipping #[0-9]*' "clips/$id.html" | sort -u | wc -l)
title=$(grep -o '<title>[^<]*' "clips/$id.html" | head -1 | sed 's/<title>NewspaperSG - //')
echo "$id : $n clippings : $title"
for a in $(seq 1 $n); do
  curl -sS -c sgjar.txt -b sgjar.txt -e "$base" -o "clips/${id}_a$a.webp" "https://eservice.nlb.gov.sg/newspapercontent/digitised/article/$id.webp?area=$a&width=1000&ct=ARTICLE&ns=yes&coord="
  python3 -c "from PIL import Image; im=Image.open('clips/${id}_a$a.webp'); im.save('clips/${id}_a$a.png'); print('  area $a', im.size)"
done
