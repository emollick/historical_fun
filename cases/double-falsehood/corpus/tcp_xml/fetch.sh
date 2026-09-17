#!/bin/bash
# fetch TCP XML files from GitHub raw; skip existing
while read id; do
  [ -z "$id" ] && continue
  if [ -s "$id.xml" ]; then continue; fi
  code=$(curl -sS -o "$id.xml" -w "%{http_code}" --max-time 300 "https://raw.githubusercontent.com/textcreationpartnership/$id/master/$id.xml")
  if [ "$code" != "200" ]; then echo "FAIL $id $code" >> fetch.log; rm -f "$id.xml"; else echo "OK $id $(stat -c %s $id.xml)" >> fetch.log; fi
done < "$1"
echo "DONE $1" >> fetch.log
