#!/usr/bin/env python3
"""
Accessibility pass 1 — bulk transforms across all 28 templates.
Run from repo root:  python scripts/a11y-pass-1.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"

# ──────────────────────────────────────────────────────────────────────────────
# Patterns
# ──────────────────────────────────────────────────────────────────────────────

# C1 — footer text contrast bump: 0.5 → 0.65 (passes WCAG AA on #01292A bg)
#      Don't touch 0.10 (separators) or 0.2 (middot dividers)
C1_PATTERNS = [
    ("rgba(255,255,255,0.5)",  "rgba(255,255,255,0.65)"),
    ("rgba(255,255,255,0.50)", "rgba(255,255,255,0.65)"),
]

# C2-meta — declare color-scheme support (full dark-mode CSS comes in pass 2)
C2_INSERT_AFTER  = '<meta name="x-apple-disable-message-reformatting" />'
C2_TAGS_TO_INSERT = (
    '<meta name="x-apple-disable-message-reformatting" />\n'
    '  <meta name="color-scheme" content="light dark" />\n'
    '  <meta name="supported-color-schemes" content="light dark" />'
)

# M1 — logo SVGs: add role="img" + aria-label="Metzler GmbH"
#      Header (220x37) and footer (160x27)
M1_HEADER_OLD = '<svg width="220" height="37" viewBox="0 0 493 83" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;">'
M1_HEADER_NEW = '<svg width="220" height="37" viewBox="0 0 493 83" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Metzler GmbH" style="display:block;margin:0 auto;">'

M1_FOOTER_OLD = '<svg width="160" height="27" viewBox="0 0 493 83" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 14px;">'
M1_FOOTER_NEW = '<svg width="160" height="27" viewBox="0 0 493 83" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Metzler GmbH" style="display:block;margin:0 auto 14px;">'

# M2 — decorative tracker icons (16x16 / 24x24): add aria-hidden="true"
#      All 16x16 SVGs in our templates are decorative cog/truck/house icons
M2_PATTERN_OLD = '<svg width="16" height="16" viewBox="0 0 24 24" '
M2_PATTERN_NEW = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" '

# M3 — generic placeholder alt → empty (product name is in adjacent cell)
#      WCAG: redundant with adjacent text → alt="" is correct
M3_OLD = 'alt="Produktbild"'
M3_NEW = 'alt=""'


# ──────────────────────────────────────────────────────────────────────────────
# Apply
# ──────────────────────────────────────────────────────────────────────────────

def transform(content: str, fname: str) -> tuple[str, dict]:
    counts = {"c1": 0, "c2": 0, "m1": 0, "m2": 0, "m3": 0}

    # C1
    for old, new in C1_PATTERNS:
        n = content.count(old)
        if n:
            content = content.replace(old, new)
            counts["c1"] += n

    # C2 (meta tags) — only if not already present
    if 'name="color-scheme"' not in content:
        if C2_INSERT_AFTER in content:
            content = content.replace(C2_INSERT_AFTER, C2_TAGS_TO_INSERT, 1)
            counts["c2"] = 1

    # M1
    if M1_HEADER_OLD in content:
        content = content.replace(M1_HEADER_OLD, M1_HEADER_NEW)
        counts["m1"] += 1
    if M1_FOOTER_OLD in content:
        content = content.replace(M1_FOOTER_OLD, M1_FOOTER_NEW)
        counts["m1"] += 1

    # M2 — only apply where the icon is decorative (24x24 viewBox)
    n_m2 = content.count(M2_PATTERN_OLD)
    if n_m2:
        content = content.replace(M2_PATTERN_OLD, M2_PATTERN_NEW)
        counts["m2"] = n_m2

    # M3
    n_m3 = content.count(M3_OLD)
    if n_m3:
        content = content.replace(M3_OLD, M3_NEW)
        counts["m3"] = n_m3

    return content, counts


def main() -> int:
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"ERROR: '{TEMPLATE_DIR}' not found. Run from repo root.", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    print(f"Processing {len(files)} templates …\n")

    grand = {"c1": 0, "c2": 0, "m1": 0, "m2": 0, "m3": 0}
    for fname in files:
        path = os.path.join(TEMPLATE_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        new_content, counts = transform(original, fname)
        if new_content != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print(
                f"  {fname:42s}  "
                f"C1={counts['c1']}  C2={counts['c2']}  "
                f"M1={counts['m1']}  M2={counts['m2']}  M3={counts['m3']}"
            )
            for k in grand:
                grand[k] += counts[k]
        else:
            print(f"  {fname:42s}  (no changes)")

    print(f"\nTotals:  C1={grand['c1']}  C2={grand['c2']}  "
          f"M1={grand['m1']}  M2={grand['m2']}  M3={grand['m3']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
