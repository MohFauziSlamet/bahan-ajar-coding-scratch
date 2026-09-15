#!/bin/bash
# Bangun ulang PDF dari semua *.md di folder ini.
#   bash _build_pdf.sh
set -eu
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BUILD="_build"

# mermaid UMD (3.5 MB) dipakai lokal supaya render deterministik; unduh sekali saja.
mkdir -p "$BUILD/vendor"
[ -f "$BUILD/vendor/mermaid.min.js" ] ||
  curl -sfL -o "$BUILD/vendor/mermaid.min.js" https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js

python3 _md2pdf.py "$BUILD/html"

# Cetak ke folder kosong dulu, JANGAN ke folder ini: di sini sudah ada PDF juknis asli,
# sehingga menghitung "*.pdf" di sini akan salah mengira build sudah selesai.
rm -rf "$BUILD/pdf"
mkdir -p "$BUILD/pdf"

i=0
for f in "$BUILD"/html/*.html; do
  b=$(basename "$f" .html)
  i=$((i + 1))
  "$CHROME" --headless --disable-gpu --no-sandbox --user-data-dir="$BUILD/cp$i" \
    --virtual-time-budget=20000 --allow-file-access-from-files --no-pdf-header-footer \
    --print-to-pdf="$BUILD/pdf/$b.pdf" "file://$PWD/$f" >/dev/null 2>&1 &
done

# Chrome headless kerap tidak keluar sendiri setelah --print-to-pdf; tunggu berkasnya lalu bereskan.
for _ in $(seq 1 60); do
  [ "$(ls "$BUILD"/pdf/*.pdf 2>/dev/null | wc -l)" -ge "$i" ] && break
  sleep 3
done
sleep 5
pkill -f "user-data-dir=$BUILD/cp" 2>/dev/null || true
sleep 1
rm -rf "$BUILD"/cp[0-9]* # profil Chrome sementara, ~20 MB per berkas

if [ "$(ls "$BUILD"/pdf/*.pdf 2>/dev/null | wc -l)" -lt "$i" ]; then
  echo "GAGAL: hanya $(ls "$BUILD"/pdf/*.pdf 2>/dev/null | wc -l) dari $i PDF yang jadi." >&2
  exit 1
fi

cp "$BUILD"/pdf/*.pdf .
echo "BUILD-SELESAI ($i PDF)"
ls -la "$BUILD"/pdf/*.pdf
