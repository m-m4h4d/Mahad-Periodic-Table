#!/bin/sh
# Assemble the static site for Vercel in dist/.
#   /         landing page (web/index.html)
#   /app/     the Tkinter app ported to the browser (web/app/)
#   /app/assets/  element pictures and text files from project/
set -eu
cd "$(dirname "$0")/.."

rm -rf dist
mkdir -p dist/app/assets
cp -R web/. dist/
cp project/*.png dist/app/assets/
cp project/Periodictable.txt project/students_account.txt project/user_element_info.txt dist/app/assets/
cp logo/rsz_1logo.png dist/favicon.png
echo "Built dist/ ($(find dist -type f | wc -l | tr -d ' ') files)"
