#!/bin/sh
# Rasteriza arte.html (desenho do quadro branco) para arte_<setup>.png com fundo transparente.
cd "$(dirname "$0")"
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
U="file:///$(pwd -W | sed 's# #%20#g')/arte.html"
for s in C2118 C2120 C2121 C2122 C2123 C2124 C2125; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --default-background-color=00000000 \
    --window-size=1080,1920 --virtual-time-budget=3000 --screenshot="$(pwd -W)/arte_$s.png" "$U?setup=$s" 2>/dev/null
done
