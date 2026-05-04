#!/usr/bin/env python3
"""
Accessibility pass 2 — bump body/instruction text from 12px -> 14px.

Scope (per audit, Option A):
  CSS classes:
    .payment-subtitle  (Bankdaten card description)
    .ref-hint          (Verwendungszweck instruction)
    .del-eta-note      (delivery ETA helper text)
    .wr-note           (Widerruf info note)
    .support-hours     (support availability line)
  Inline body sentences (3 specific instances):
    payment-confirmation.html  "Die Rechnung senden wir Ihnen separat zu."
    order-confirmation.html    "Ihre Zahlung ist eingegangen..."
    production-guide.html      "Alle Preise inkl. 19% MwSt..."

NOT bumped (kept at 12px per Categorization A/C/D/E):
  - Uppercase labels (.section-label, .meta-label, .order-th, .ref-label,
    .bank-td-label, .del-col-label, .tracking-carrier, .hero-badge)
  - Tracker progress labels (.progress-label)
  - Footer (.footer-desc, .footer-legal-row a, .footer-copy-row p, separators)
  - Status chips and pills

Run from repo root: python scripts/a11y-pass-2-text-size.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"

# CSS class bumps — 12px -> 14px
CSS_CLASSES_TO_BUMP = [
    "payment-subtitle",
    "ref-hint",
    "del-eta-note",
    "wr-note",
    "support-hours",
]

# Inline body sentences (per-file, exact match)
INLINE_BUMPS = {
    "payment-confirmation.html": [
        (
            '<div style="font-size:12px; color:#767676; line-height:1.6;">Die Rechnung senden wir Ihnen separat zu.</div>',
            '<div style="font-size:14px; color:#767676; line-height:1.6;">Die Rechnung senden wir Ihnen separat zu.</div>',
        ),
    ],
    "order-confirmation.html": [
        (
            '<div style="font-size:12px; color:#667; margin-bottom:16px;">Ihre Zahlung ist eingegangen. Ihre Bestellung geht damit direkt in die Vorbereitung.</div>',
            '<div style="font-size:14px; color:#667; margin-bottom:16px;">Ihre Zahlung ist eingegangen. Ihre Bestellung geht damit direkt in die Vorbereitung.</div>',
        ),
    ],
    "production-guide.html": [
        (
            '<p style="font-size:12px; color:#767676; margin:6px 0 0; line-height:1.55;">Alle Preise inkl. 19&nbsp;% MwSt., zzgl. Versandkosten gem&auml;&szlig; Ihrer Bestell&uuml;bersicht.</p>',
            '<p style="font-size:14px; color:#767676; margin:6px 0 0; line-height:1.55;">Alle Preise inkl. 19&nbsp;% MwSt., zzgl. Versandkosten gem&auml;&szlig; Ihrer Bestell&uuml;bersicht.</p>',
        ),
    ],
}


def transform(content: str, fname: str) -> tuple[str, dict]:
    counts = {"css": 0, "inline": 0}

    # CSS class bumps — match the class block and replace its 12px declaration
    for cls in CSS_CLASSES_TO_BUMP:
        # Pattern: .classname { ... font-size: 12px ... }
        # We do a non-greedy match within a single CSS rule (between the class
        # selector and the next closing brace).
        pattern = re.compile(
            r"(\." + re.escape(cls) + r"\s*\{[^}]*?font-size:\s*)12px",
            re.DOTALL,
        )
        new_content, n = pattern.subn(r"\g<1>14px", content)
        if n:
            content = new_content
            counts["css"] += n

    # Inline body-sentence bumps (per-file)
    if fname in INLINE_BUMPS:
        for old, new in INLINE_BUMPS[fname]:
            if old in content:
                content = content.replace(old, new)
                counts["inline"] += 1

    return content, counts


def main() -> int:
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"ERROR: '{TEMPLATE_DIR}' not found. Run from repo root.", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    print(f"Processing {len(files)} templates ...\n")

    grand_css, grand_inline = 0, 0
    for fname in files:
        path = os.path.join(TEMPLATE_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        new_content, counts = transform(original, fname)
        if new_content != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print(
                f"  {fname:42s}  CSS={counts['css']}  inline={counts['inline']}"
            )
            grand_css += counts["css"]
            grand_inline += counts["inline"]
        else:
            print(f"  {fname:42s}  (no changes)")

    print(f"\nTotals:  CSS class bumps = {grand_css}  inline bumps = {grand_inline}  "
          f"total = {grand_css + grand_inline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
