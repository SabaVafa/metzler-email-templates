#!/usr/bin/env python3
"""
Wire Outlook desktop PNG fallback around the 56 inline-SVG logos
(header + footer x 28 templates).

Pattern:
  <!--[if mso]>
  <img src="../assets/logo-white.png" width="W" height="H" alt="Metzler GmbH"
       style="display:block; border:0; margin:0 auto;" />
  <![endif]-->
  <!--[if !mso]><!-->
  <svg ...>...original SVG...</svg>
  <!--<![endif]-->

Modern clients (Apple Mail, Gmail, etc.) ignore the [if mso] block and
render the SVG. Outlook desktop (which strips inline SVG) ignores the
[if !mso] block and renders the PNG.

Idempotent: skips files that already have the fallback wrapping.

NOTE on launch readiness:
  The img src uses the relative path ../assets/logo-white.png. In a sent
  email this will fail to load until assets are hosted publicly (see
  OPEN-ITEMS.md §5). The wiring is complete; the path swap is a
  separate launch-time step.

Run from repo root: python scripts/logo-mso-fallback.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"
LOGO_PATH = "../assets/logo-white.png"

# Header SVG: 220 x 37, style="display:block;margin:0 auto;"
HEADER_SVG_RE = re.compile(
    r'(<svg width="220" height="37" viewBox="0 0 493 83"[^>]*?'
    r'role="img" aria-label="Metzler GmbH"[^>]*?'
    r'style="display:block;margin:0 auto;">.*?</svg>)',
    re.DOTALL,
)

# Footer SVG: 160 x 27, style="display:block;margin:0 auto 14px;"
FOOTER_SVG_RE = re.compile(
    r'(<svg width="160" height="27" viewBox="0 0 493 83"[^>]*?'
    r'role="img" aria-label="Metzler GmbH"[^>]*?'
    r'style="display:block;margin:0 auto 14px;">.*?</svg>)',
    re.DOTALL,
)


def wrap_with_fallback(svg_block: str, width: int, height: int, footer_margin: bool = False) -> str:
    """Wrap a single SVG in MSO conditional comments with a PNG fallback."""
    img_style = "display:block; border:0; margin:0 auto"
    if footer_margin:
        img_style += "; margin-bottom:14px"
    img_style += ";"

    img_tag = (
        f'<img src="{LOGO_PATH}" width="{width}" height="{height}" '
        f'alt="Metzler GmbH" style="{img_style}" />'
    )

    return (
        f"<!--[if mso]>\n          {img_tag}\n          <![endif]-->\n"
        f"          <!--[if !mso]><!-->\n          {svg_block}\n          <!--<![endif]-->"
    )


def transform(content: str) -> tuple[str, dict]:
    counts = {"header": 0, "footer": 0, "skipped": 0}

    # Skip if already wrapped (idempotency)
    if 'src="' + LOGO_PATH + '"' in content:
        counts["skipped"] = 1
        return content, counts

    # Header (220x37) — first SVG opening of this size in the file
    def replace_header(m):
        counts["header"] += 1
        return wrap_with_fallback(m.group(1), 220, 37)
    content = HEADER_SVG_RE.sub(replace_header, content, count=1)

    # Footer (160x27)
    def replace_footer(m):
        counts["footer"] += 1
        return wrap_with_fallback(m.group(1), 160, 27, footer_margin=True)
    content = FOOTER_SVG_RE.sub(replace_footer, content, count=1)

    return content, counts


def main() -> int:
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"ERROR: '{TEMPLATE_DIR}' not found. Run from repo root.", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    print(f"Processing {len(files)} templates ...\n")

    grand_h, grand_f, grand_skip = 0, 0, 0
    for fname in files:
        path = os.path.join(TEMPLATE_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        new_content, counts = transform(original)
        if counts["skipped"]:
            print(f"  {fname:42s}  (already wrapped, skipping)")
            grand_skip += 1
            continue

        if new_content != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print(
                f"  {fname:42s}  header={counts['header']}  footer={counts['footer']}"
            )
            grand_h += counts["header"]
            grand_f += counts["footer"]
        else:
            print(f"  {fname:42s}  (no SVGs matched - check patterns)")

    print(f"\nTotals:  headers wrapped = {grand_h}  footers wrapped = {grand_f}  "
          f"already-done = {grand_skip}  total = {grand_h + grand_f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
