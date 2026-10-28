#!/bin/sh
# Download APT's source files (not redistributed in this repo) into raw/.
# Needs curl and pdftotext (poppler). APT's server rate-limits, so this pauses between requests.
set -e
cd "$(dirname "$0")"
mkdir -p raw/toc raw/toc_txt
curl -sSL -o raw/comprehensive_index_2025-12-19.xlsx \
  "https://irp.cdn-website.com/4f321b91/files/uploaded/Comprehensive+Index+for+Website+12-19-25.xlsx"
i=0
while read -r u; do
  i=$((i+1))
  f="raw/toc/$(printf %02d $i)_$(basename "$u" | sed 's/%20/_/g;s/%28/(/g;s/%29/)/g;s/;/_/g')"
  u2=$(echo "$u" | sed 's#https://www.apti.org/assets#https://apt.memberclicks.net/assets#')
  sleep 5
  curl -sSL -f -o "$f" "$u2" || { echo "missing: $u2"; rm -f "$f"; continue; }
  pdftotext -layout "$f" "raw/toc_txt/$(basename "${f%.*}").txt"
done < raw/toc_urls.txt
