#!/bin/bash
cd "$(dirname "$0")/.."
while IFS=$'\t' read -r id fname label; do
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$fname")
  out="lr_text/${label}__${id}.txt"
  if [ ! -s "$out" ]; then
    curl -sS -L -m 900 --retry 3 "https://archive.org/download/$id/$enc" -o "$out" && echo "OK $id $(stat -c %s "$out")" || echo "FAIL $id"
  fi
done < lr_volumes.tsv
echo DONE
