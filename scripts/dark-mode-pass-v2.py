#!/usr/bin/env python3
"""
Dark-mode pass v2 — comprehensive override addressing v1 shortcomings.

Fixes vs v1:
  1. White-box bleed-through: v1 targeted .card/.hero classes only. Inner
     elements with inline `style="background-color:#ffffff"` (meta cards,
     order-date boxes, delivery-window, newsletter signup, etc.) stayed
     white. v2 adds attribute-selector overrides for all common inline
     bg colors.
  2. Palette neutralization: v1 used green-tinted darks (#0f1311, #1a1f1c).
     v2 switches to neutral (#121212, #1c1c1c) — premium standard
     (Apple, GitHub, Twitter, Material 3).
  3. Border accent restraint: v1 used vivid green borders on payment-card,
     bankdaten-card (#2d5c2d). v2 uses subtle neutral dark-gray borders
     (#2a2a2a) with desaturated brand teal accents (#2d5c5d) only where
     needed.
  4. Depth via subtle elevation: body #121212 / card #1c1c1c / inner
     highlight #222222 — three-step elevation.

Idempotent: replaces any existing /* ── DARK MODE ── */ block (v1 or v2).
LIGHT MODE STILL COMPLETELY UNTOUCHED.

Run from repo root:  python scripts/dark-mode-pass-v2.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"

PALETTE_BY_LIGHT_COLOR = {
    "#eaf3ea": "green",
    "#fdf3e3": "amber",
    "#fff4d6": "amber",
    "#fde8e8": "red",
}

HERO_BADGE_DARK = {
    "green": "      .hero-badge { background-color: #1a3a1a !important; color: #7dc97d !important; }",
    "amber": "      .hero-badge { background-color: #3a2a0d !important; color: #e8b860 !important; }",
    "red":   "      .hero-badge { background-color: #3a1818 !important; color: #e87878 !important; }",
}

# Comprehensive dark-mode block
DARK_COMMON_TEMPLATE = """    /* ── DARK MODE ── */
    @media (prefers-color-scheme: dark) {
      /* === SURFACES === */
      body, #bodyTable { background-color: #121212 !important; }
      .card { background-color: #1c1c1c !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; }
      .hero { background-color: #1c1c1c !important; border-bottom-color: #2a2a2a !important; }
      .hero-title { color: #e8e8e8 !important; }
      .hero-subtitle { color: #a8a8a8 !important; }

      /* Catch inline white backgrounds (meta cards, inner boxes) */
      [bgcolor="#ffffff"], [bgcolor="#FFFFFF"],
      [style*="background-color:#ffffff"], [style*="background-color: #ffffff"],
      [style*="background-color:#FFFFFF"], [style*="background-color: #FFFFFF"],
      [style*="background:#ffffff"], [style*="background: #ffffff"] {
        background-color: #1c1c1c !important;
      }

      /* Catch inline light-tint surfaces */
      [bgcolor="#f2f4f2"], [bgcolor="#f7f9f7"], [bgcolor="#f7faf7"],
      [bgcolor="#f5f5f5"], [bgcolor="#f6f9f6"], [bgcolor="#fafafa"],
      [style*="background-color:#f2f4f2"], [style*="background-color: #f2f4f2"],
      [style*="background-color:#f7f9f7"], [style*="background-color: #f7f9f7"],
      [style*="background-color:#f7faf7"], [style*="background-color: #f7faf7"],
      [style*="background-color:#f5f5f5"], [style*="background-color: #f5f5f5"],
      [style*="background-color:#f6f9f6"], [style*="background-color: #f6f9f6"],
      [style*="background-color:#fafafa"], [style*="background-color: #fafafa"],
      [style*="background-color:#f5f8ff"], [style*="background-color: #f5f8ff"],
      [style*="background-color:#dde8e8"], [style*="background-color: #dde8e8"],
      [style*="background-color:#eef4f4"], [style*="background-color: #eef4f4"] {
        background-color: #1c1c1c !important;
      }

      /* Light-green tint highlight boxes — subtle elevation */
      [style*="background-color:#eaf3ea"], [style*="background-color: #eaf3ea"],
      [style*="background-color:#e8f5e0"], [style*="background-color: #e8f5e0"],
      [style*="background-color:#f0f7f0"], [style*="background-color: #f0f7f0"] {
        background-color: #222222 !important;
      }

      /* === BORDERS — neutral dark gray everywhere === */
      [style*="border:1px solid #e8e8e8"], [style*="border: 1px solid #e8e8e8"],
      [style*="border:1px solid #e0e0e0"], [style*="border: 1px solid #e0e0e0"],
      [style*="border:1px solid #ebebeb"], [style*="border: 1px solid #ebebeb"],
      [style*="border:1px solid #e6ebe6"], [style*="border: 1px solid #e6ebe6"],
      [style*="border:1px solid #e8ece8"], [style*="border: 1px solid #e8ece8"],
      [style*="border:1px solid #e0ebe3"], [style*="border: 1px solid #e0ebe3"],
      [style*="border:1px solid #e0e8e0"], [style*="border: 1px solid #e0e8e0"],
      [style*="border:1px solid #efefef"], [style*="border: 1px solid #efefef"],
      [style*="border:1px solid #eaeaea"], [style*="border: 1px solid #eaeaea"],
      [style*="border:1px solid #d6e8d6"], [style*="border: 1px solid #d6e8d6"] {
        border-color: #2a2a2a !important;
      }
      [style*="border-bottom:1px solid #f0f0f0"], [style*="border-bottom: 1px solid #f0f0f0"],
      [style*="border-bottom:1px solid #f5f5f5"], [style*="border-bottom: 1px solid #f5f5f5"],
      [style*="border-bottom:1px solid #ebebeb"], [style*="border-bottom: 1px solid #ebebeb"],
      [style*="border-top:1px solid #e8e8e8"], [style*="border-top: 1px solid #e8e8e8"] {
        border-color: #2a2a2a !important;
      }

      /* === TYPOGRAPHY === */
      .section { border-bottom-color: #2a2a2a !important; }
      .section-label { color: #c0c0c0 !important; }
      .meta-label { color: #909090 !important; }
      .meta-value { color: #e8e8e8 !important; }
      .meta-value-light { color: #c0c0c0 !important; }
      .product-name { color: #e8e8e8 !important; }
      .product-sku { color: #909090 !important; }
      .order-th { color: #909090 !important; border-bottom-color: #2a2a2a !important; }
      .order-td, .order-td-qty, .order-td-price { border-bottom-color: #2a2a2a !important; color: #c0c0c0 !important; }
      .order-last-td { border-bottom: none !important; }
      .totals-td-l { color: #a0a0a0 !important; }
      .totals-td-r { color: #c0c0c0 !important; }
      .totals-sep-l, .totals-sep-r { border-top-color: #2a2a2a !important; }
      .totals-grand-l, .totals-grand-r { color: #e8e8e8 !important; border-top-color: #c0c0c0 !important; }
      .support-title { color: #e8e8e8 !important; }
      .support-sub { color: #a0a0a0 !important; }
      .support-hours { color: #909090 !important; }
      /* === DELIVERY / TOTALS / TEMPLATE-SPECIFIC CLASS OVERRIDES === */
      .del-col-label, .del-eta-note { color: #909090 !important; }
      .del-address { color: #c0c0c0 !important; }
      .del-eta { color: #4cc4c5 !important; }
      .totals-sep-l { color: #a0a0a0 !important; }
      .totals-sep-r { color: #c0c0c0 !important; }
      .free-shipping { color: #5dc97d !important; }
      .config-td-label { color: #909090 !important; }
      .config-td-value { color: #c0c0c0 !important; }
      .wr-main-text { color: #c0c0c0 !important; }
      .wr-note { color: #a0a0a0 !important; }
      .order-th-qty, .order-th-price { color: #909090 !important; }
      .support-phone { color: #4cc4c5 !important; }

      /* Catch dark text on dark-bg from inline styles */
      [style*="color:#1a1a1a"], [style*="color: #1a1a1a"] { color: #e8e8e8 !important; }
      [style*="color:#333"], [style*="color: #333"],
      [style*="color:#333333"], [style*="color: #333333"] { color: #c0c0c0 !important; }
      [style*="color:#444"], [style*="color: #444"],
      [style*="color:#444444"], [style*="color: #444444"] { color: #b0b0b0 !important; }
      [style*="color:#555"], [style*="color: #555"],
      [style*="color:#555555"], [style*="color: #555555"] { color: #a0a0a0 !important; }
      [style*="color:#666"], [style*="color: #666"],
      [style*="color:#666666"], [style*="color: #666666"] { color: #909090 !important; }
      [style*="color:#767676"], [style*="color: #767676"],
      [style*="color:#777"], [style*="color: #777"],
      [style*="color:#777777"], [style*="color: #777777"] { color: #909090 !important; }
      [style*="color:#999"], [style*="color: #999"],
      [style*="color:#999999"], [style*="color: #999999"] { color: #808080 !important; }

      /* === ACCENT (brand teal) === */
      .btn-primary { background-color: #015253 !important; color: #ffffff !important; }
      .btn-outline { background-color: transparent !important; border-color: #4cc4c5 !important; color: #4cc4c5 !important; }
      a { color: #4cc4c5 !important; }
      /* Brand-teal inline backgrounds (eg. CTAs) stay branded */
      [style*="background-color:#015253"], [style*="background-color: #015253"] {
        background-color: #015253 !important;
      }

      /* === TINTED CARDS — payment-card, tracking-card === */
      /* Tone down the bright green left-border accent */
      .payment-card, .tracking-card {
        background-color: #1c2520 !important;
        border-color: #2a2a2a !important;
        border-left-color: #2d6e6f !important;
      }
      .payment-title, .tracking-carrier { color: #e8e8e8 !important; }
      .payment-subtitle { color: #a0a0a0 !important; }
      .tracking-number { color: #4cc4c5 !important; }
      .bank-td-label { color: #909090 !important; }
      .bank-td-value { color: #e8e8e8 !important; }
      .ref-box { background-color: #222222 !important; border-color: #2a2a2a !important; }
      .ref-label { color: #909090 !important; }
      .ref-code { color: #4cc4c5 !important; }
      .ref-hint { color: #a0a0a0 !important; }

      /* === STEPS / TRACKER === */
      .step-num, .tip-num { border-color: #4cc4c5 !important; color: #4cc4c5 !important; }
      .step-text { color: #c0c0c0 !important; }
      .progress-label { color: #4cc4c5 !important; }

      /* === HERO BADGE (palette-specific override below) === */
__HERO_BADGE_RULE__
    }
"""

# Match v1 OR v2 block via the marker comment + closing brace before mobile media query
DARK_BLOCK_RE = re.compile(
    r"    /\* (── DARK MODE ──|-- DARK MODE --) \*/\n"
    r"    @media \(prefers-color-scheme: dark\) \{.*?\n    \}\n",
    re.DOTALL,
)

INSERT_BEFORE = re.compile(
    r"(\n\s*/\* ── RESPONSIVE ── \*/\n)?    @media only screen and \(max-width: 680px\) \{",
)


def detect_palette(content):
    m = re.search(
        r"\.hero-badge\s*\{[^}]*?background-color:\s*(#[0-9a-fA-F]{6})",
        content,
    )
    if not m:
        return "green"
    color = m.group(1).lower()
    return PALETTE_BY_LIGHT_COLOR.get(color, "green")


def transform(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    palette = detect_palette(content)
    badge_rule = HERO_BADGE_DARK[palette]
    new_block = DARK_COMMON_TEMPLATE.replace("__HERO_BADGE_RULE__", badge_rule)

    # Remove any existing dark block (v1 or v2)
    new_content, n = DARK_BLOCK_RE.subn("", content, count=1)
    had_existing = n > 0

    if "@media only screen and (max-width: 680px)" not in new_content:
        return ("error", "no responsive @media found")

    # Insert new dark block before the responsive @media (or its RESPONSIVE comment)
    insertion_marker = "    /* ── RESPONSIVE ── */\n    @media only screen and (max-width: 680px) {"
    fallback_marker = "    @media only screen and (max-width: 680px) {"
    if insertion_marker in new_content:
        new_content = new_content.replace(
            insertion_marker, new_block + "\n" + insertion_marker, 1
        )
    else:
        new_content = new_content.replace(
            fallback_marker, new_block + "\n" + fallback_marker, 1
        )

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)

    return ("replaced" if had_existing else "added", palette)


def main():
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"error: {TEMPLATE_DIR}/ not found", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    counts = {"added": 0, "replaced": 0, "error": 0}
    by_palette = {"green": 0, "amber": 0, "red": 0}

    for name in files:
        path = os.path.join(TEMPLATE_DIR, name)
        status, detail = transform(path)
        counts[status] += 1
        if status in ("added", "replaced"):
            by_palette[detail] += 1
            tag = "[+]" if status == "added" else "[~]"
            print(f"  {tag} {name}  ({detail} palette)")
        else:
            print(f"  [!] {name}  ({detail})")

    print()
    print(f"Added: {counts['added']}  Replaced: {counts['replaced']}  Errors: {counts['error']}  (of {len(files)})")
    for p, n in by_palette.items():
        print(f"  {p}: {n}")


if __name__ == "__main__":
    main()
