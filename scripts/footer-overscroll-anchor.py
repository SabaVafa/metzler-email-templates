#!/usr/bin/env python3
"""
footer-overscroll-anchor.py  (idempotent)

Mobile fix: the <html> element had no background, so the light body background
(#f2f4f2) propagated to the canvas -- including the iOS/Android rubber-band
overscroll area. Scrolling past the dark footer (#01292A) revealed a light strip,
making the footer look detached from the bottom edge.

Setting an explicit <html> background to the footer's dark teal anchors the bottom
overscroll to the footer colour. The page is already bookended by teal (header band
#015253, footer #01292A), so the top overscroll reads as intentional too.

Inserts `html { background-color: #01292A; }` immediately after the CSS reset line
in every template's <style> block. Re-runnable: skips files already patched.
"""
import pathlib

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / "templates"
RESET = "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
RULE = "\n    /* Anchor mobile overscroll to the footer colour (canvas background) */\n    html { background-color: #01292A; }\n"

patched, skipped, missing = [], [], []

for f in sorted(TEMPLATES.glob("*.html")):
    text = f.read_text(encoding="utf-8")
    if "html { background-color: #01292A; }" in text:
        skipped.append(f.name)
        continue
    if RESET not in text:
        missing.append(f.name)
        continue
    text = text.replace(RESET, RESET + RULE, 1)
    f.write_text(text, encoding="utf-8")
    patched.append(f.name)

print(f"patched ({len(patched)}): {', '.join(patched) or '-'}")
print(f"skipped/already ({len(skipped)}): {', '.join(skipped) or '-'}")
print(f"reset-line not found ({len(missing)}): {', '.join(missing) or '-'}")
