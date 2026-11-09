#!/bin/sh
# Render tools/og.html to assets/img/og.png (1200x630) with local headless Chrome. No network needed.
set -e
cd "$(dirname "$0")/.."
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=3000 \
  --screenshot="$PWD/assets/img/og.png" "file://$PWD/tools/og.html"
