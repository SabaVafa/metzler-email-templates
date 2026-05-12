#!/usr/bin/env python3
"""
Dark-mode pass — add @media (prefers-color-scheme: dark) overrides to all 28
templates. LIGHT MODE IS NOT TOUCHED. Dark styles live in a parallel @media
block inserted just before the existing responsive (mobile) breakpoint.

Targeted clients (dark mode aware):
  - Apple Mail (macOS, iOS)
  - Outlook 365 web
  - Outlook iOS / Android (partial)
  - Gmail web (respects color-scheme meta)

Clients that auto-invert (Gmail mobile app) will still do their own thing,
but at least the meta tag declares "we support dark" so they're nicer about it.

Idempotent: skips templates that already contain the dark-mode marker.

Hero-badge palette is detected per template from existing CSS:
  green (#eaf3ea)  - confirmation
  amber (#fdf3e3/#fff4d6) - payment-attention
  red   (#fde8e8)  - internal staff alert

Run from repo root:  python scripts/dark-mode-pass.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"

# Light hero-badge bg color -> palette name
PALETTE_BY_LIGHT_COLOR = {
    "#eaf3ea": "green",
    "#fdf3e3": "amber",
    "#fff4d6": "amber",  # production-guide variant
    "#fde8e8": "red",
}

# Hero-badge dark-mode rule per palette
HERO_BADGE_DARK = {
    "green": "      .hero-badge { background-color: #1f3a1f !important; color: #7dc97d !important; }",
    "amber": "      .hero-badge { background-color: #3a2a0d !important; color: #e8b860 !important; }",
    "red":   "      .hero-badge { background-color: #3a1818 !important; color: #e87878 !important; }",
}

# Common dark-mode block (all templates)
DARK_COMMON_TEMPLATE = """    /* -- DARK MODE -- */
    @media (prefers-color-scheme: dark) {
      body, #bodyTable { background-color: #0f1311 !important; }
      .card { background-color: #1a1f1c !important; box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important; }
      .hero { background-color: #1f2522 !important; border-bottom-color: #2a3530 !important; }
      .hero-title { color: #f0f0f0 !important; }
      .hero-subtitle { color: #a8a8a8 !important; }
      .section { border-bottom-color: #2a2f2c !important; }
      .section-label { color: #909090 !important; }
      .meta-label { color: #909090 !important; }
      .meta-value { color: #f0f0f0 !important; }
      .meta-value-light { color: #d0d0d0 !important; }
      .product-name { color: #f0f0f0 !important; }
      .product-sku { color: #909090 !important; }
      .order-th { color: #909090 !important; border-bottom-color: #2a2f2c !important; }
      .order-td, .order-td-qty, .order-td-price { border-bottom-color: #2a2f2c !important; color: #d0d0d0 !important; }
      .order-last-td { border-bottom: none !important; }
      .totals-td-l { color: #a8a8a8 !important; }
      .totals-td-r { color: #d0d0d0 !important; }
      .totals-sep-l, .totals-sep-r { border-top-color: #2a2f2c !important; }
      .totals-grand-l, .totals-grand-r { color: #f0f0f0 !important; border-top-color: #f0f0f0 !important; }
      .support-title { color: #f0f0f0 !important; }
      .support-sub { color: #a8a8a8 !important; }
      .support-hours { color: #909090 !important; }
      .support-phone { color: #3aa9aa !important; }
      .btn-primary { background-color: #015253 !important; color: #ffffff !important; }
      .btn-outline { background-color: transparent !important; border-color: #3aa9aa !important; color: #3aa9aa !important; }
      .payment-card, .tracking-card { background-color: #1a2e1a !important; border-color: #2d5c2d !important; }
      .payment-title, .tracking-carrier { color: #f0f0f0 !important; }
      .payment-subtitle { color: #a8a8a8 !important; }
      .tracking-number { color: #3aa9aa !important; }
      .bank-td-label { color: #909090 !important; }
      .bank-td-value { color: #f0f0f0 !important; }
      .ref-box { background-color: #1f2522 !important; border-color: #2d5c2d !important; }
      .ref-label { color: #909090 !important; }
      .ref-code { color: #3aa9aa !important; }
      .ref-hint { color: #a8a8a8 !important; }
      .step-num, .tip-num { border-color: #3aa9aa !important; color: #3aa9aa !important; }
      .step-text { color: #d0d0d0 !important; }
      .progress-label { color: #3aa9aa !important; }
      a { color: #3aa9aa !important; }
__HERO_BADGE_RULE__
    }
"""

# Marker for idempotency check
MARKER = "/* -- DARK MODE -- */"

# Where to insert (just before the existing mobile @media block)
INSERT_BEFORE = "    @media only screen and (max-width: 680px) {"


def detect_palette(content):
    """Detect hero-badge palette from existing CSS rule."""
    # Look for .hero-badge { ... background-color: #XXXXXX ... }
    m = re.search(
        r"\.hero-badge\s*\{[^}]*?background-color:\s*(#[0-9a-fA-F]{6})",
        content,
    )
    if not m:
        return "green"  # default
    color = m.group(1).lower()
    return PALETTE_BY_LIGHT_COLOR.get(color, "green")


def transform(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    if MARKER in content:
        return ("skip", "already has dark mode")

    if INSERT_BEFORE not in content:
        return ("error", "no responsive @media query found")

    palette = detect_palette(content)
    badge_rule = HERO_BADGE_DARK[palette]
    dark_block = DARK_COMMON_TEMPLATE.replace("__HERO_BADGE_RULE__", badge_rule)

    new_content = content.replace(INSERT_BEFORE, dark_block + "\n" + INSERT_BEFORE)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)

    return ("ok", palette)


def main():
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"error: {TEMPLATE_DIR}/ not found - run from repo root", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    counts = {"ok": 0, "skip": 0, "error": 0}
    by_palette = {"green": 0, "amber": 0, "red": 0}

    for name in files:
        path = os.path.join(TEMPLATE_DIR, name)
        status, detail = transform(path)
        counts[status] += 1
        if status == "ok":
            by_palette[detail] += 1
            print(f"  [ok] {name}  ({detail} badge palette)")
        elif status == "skip":
            print(f"  [skip] {name}  ({detail})")
        else:
            print(f"  [error] {name}  ({detail})")

    print()
    print(f"Files modified: {counts['ok']}/{len(files)}  (skipped {counts['skip']}, errors {counts['error']})")
    print(f"  green palette: {by_palette['green']}")
    print(f"  amber palette: {by_palette['amber']}")
    print(f"  red palette:   {by_palette['red']}")


if __name__ == "__main__":
    main()
