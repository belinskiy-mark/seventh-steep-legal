#!/usr/bin/env python3
"""Render the Open Graph images (1200x630), one per language, with local headless Chrome.

Run:  python3 -I tools/make_og.py
Writes assets/img/og.png (en), og-uk.png, og-zh-hans.png, og-zh-hant.png. No network is used:
the page loads only assets/site.css and the self-hosted fonts. Chinese text uses the system font.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TEXT = {
    "en": dict(file="og.png", lang="en", brand="Seventh Steep", h1="Gongfu tea timer for ", em="puerh and Yunnan white tea",
               p="Grams, temperature and every infusion, on time."),
    "uk": dict(file="og-uk.png", lang="uk", brand="Сьомий пролив", h1="Гунфу-таймер для ", em="пуеру і юньнанського білого чаю",
               p="Грами, температура і кожен пролив вчасно."),
    "zh-hans": dict(file="og-zh-hans.png", lang="zh-Hans", brand="第七泡", h1="普洱与云南白茶的", em="功夫茶计时器",
                    p="投茶量、水温，每一泡都准时。"),
    "zh-hant": dict(file="og-zh-hant.png", lang="zh-Hant", brand="第七泡", h1="普洱與雲南白茶的", em="功夫茶計時器",
                    p="投茶量、水溫，每一泡都準時。"),
}

TEMPLATE = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><link rel="stylesheet" href="../assets/site.css">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:#14110E;background-image:radial-gradient(700px 520px at 900px 300px,rgba(224,169,78,.22),transparent 65%)}}
.og{{display:flex;align-items:center;justify-content:space-between;height:630px;padding:0 90px}}
.txt{{max-width:660px}}
.mark{{display:flex;align-items:center;gap:18px;margin-bottom:34px}}
.mark .glyph{{font-family:"Seventh Brand",serif;color:#E0A94E;font-size:64px;line-height:1}}
.mark .name{{font-family:"Seventh Brand","Cormorant Garamond",serif;font-size:44px;color:#F1E8DA}}
h1{{font-size:{h1size}px;line-height:1.08;color:#F1E8DA}}
h1 em{{font-style:normal;color:#E0A94E;{em_style}}}
p{{font-family:var(--ui);font-size:26px;color:#A29684;margin-top:26px}}
.cups{{position:relative;width:340px;height:340px;flex:none}}
.cups::before{{content:"";position:absolute;inset:-60px;border-radius:50%;background:repeating-radial-gradient(circle,transparent 0 38px,rgba(233,224,208,.06) 39px 40px)}}
.cups .cup{{position:absolute}}
</style></head>
<body><div class="og">
<div class="txt"><div class="mark"><span class="glyph">七</span><span class="name">{brand}</span></div>
<h1>{h1}<em>{em}</em></h1>
<p>{p}</p></div>
<div class="cups">
<span class="cup" style="--size:190px;--liquor:#7A2E1C;left:75px;top:75px"></span>
<span class="cup" style="--size:92px;--liquor:#C9B45A;left:0;top:10px"></span>
<span class="cup" style="--size:80px;--liquor:#C47A2C;right:0;top:20px"></span>
<span class="cup" style="--size:76px;--liquor:#D6C98C;left:20px;bottom:0"></span>
<span class="cup" style="--size:86px;--liquor:#B58A44;right:10px;bottom:10px"></span>
</div></div></body></html>
"""


def main() -> int:
    for key, t in TEXT.items():
        src = ROOT / "tools" / f".og-{key}.html"
        h1size = 62 if key.startswith("zh") else (56 if key == "uk" else 68)
        em_style = "display:block" if key.startswith("zh") else ""  # keep the CJK highlight on its own line
        src.write_text(TEMPLATE.format(h1size=h1size, em_style=em_style, **t), encoding="utf-8")
        out = ROOT / "assets" / "img" / t["file"]
        try:
            subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                 "--window-size=1200,630", "--virtual-time-budget=3000", f"--screenshot={out}", src.as_uri()],
                check=True, capture_output=True,
            )
        finally:
            src.unlink()
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
