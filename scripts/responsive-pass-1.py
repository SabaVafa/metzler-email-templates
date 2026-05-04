#!/usr/bin/env python3
"""
Responsive pass 1 — mobile-padding & Bankdaten fixes across all 28 templates.
Run from repo root:  python scripts/responsive-pass-1.py
"""

import os
import re
import sys

TEMPLATE_DIR = "templates"

# ──────────────────────────────────────────────────────────────────────────────
# Patterns
# ──────────────────────────────────────────────────────────────────────────────

# R1 + R1+ + R2 — footer & support-inner mobile padding (all 28 templates)
#   Insert new rules at the end of the @media (max-width: 620px) block.
#   The block always ends with the last rule line, then `    }` then `  </style>`.
#   We find the closing `    }\n  </style>` and inject before it.
NEW_MOBILE_RULES = """      .footer-main { padding: 28px 20px !important; }
      .footer-legal-row,
      .footer-copy-row { padding-left: 20px !important; padding-right: 20px !important; }
      .support-inner { padding-left: 20px !important; padding-right: 20px !important; }
"""

MEDIA_END_PATTERN = re.compile(
    r"(    \}\n  </style>)",  # end of @media block, then </style>
)

# R3 — Bankdaten stacking on mobile (only 3 templates that have .bank-td-label CSS)
BANKDATEN_MOBILE_RULES = """      .bank-td-label,
      .bank-td-value { display: block !important; width: 100% !important; padding: 4px 0 !important; }
      .bank-td-label { padding-top: 10px !important; font-size: 11px !important; }
      .bank-table tr:first-child .bank-td-label { padding-top: 0 !important; }
"""

BANKDATEN_FILES = {
    "order-confirmation.html",
    "zahlungs-erinnerung.html",
    "zahlungsinformationen-vorkasse.html",
}

# R4 — orphaned CSS cleanup
#
# (a) `.footer-block { padding: 20px 20px !important; }` mobile rule — remove
#     wherever it appears (22 templates have it; class never used in HTML).
ORPHAN_FOOTER_BLOCK_PATTERN = re.compile(
    r"      \.footer-block \{ padding: 20px 20px !important; \}\n"
)

# (b) `.btn-row { ... }` and `.btn-col { ... }` in amazon-pay-info.html only
#     — both classes are referenced nowhere in HTML.
ORPHAN_BTN_ROW_PATTERN = re.compile(
    r"    /\* ── BUTTON ROW \(two equal-width buttons side-by-side, stack on mobile\) ── \*/\n"
    r"    \.btn-row \{[^}]*\}\n\n",
    re.DOTALL,
)

ORPHAN_BTN_COL_MOBILE_PATTERN = re.compile(
    r"      \.btn-col \{[^}]*\}\n"
)


# ──────────────────────────────────────────────────────────────────────────────
# Apply
# ──────────────────────────────────────────────────────────────────────────────

def transform(content: str, fname: str) -> tuple[str, dict]:
    counts = {"r1_r2": 0, "r3": 0, "r4a": 0, "r4b_btn_row": 0, "r4b_btn_col": 0}

    # R1 + R1+ + R2 — only insert if not already present (idempotent)
    if ".footer-main { padding: 28px 20px !important; }" not in content:
        new_content, n = MEDIA_END_PATTERN.subn(
            NEW_MOBILE_RULES + r"\1", content, count=1
        )
        if n:
            content = new_content
            counts["r1_r2"] = 1

    # R3 — Bankdaten stacking, only for the 3 affected templates
    if fname in BANKDATEN_FILES:
        if ".bank-td-label,\n      .bank-td-value { display: block" not in content:
            new_content, n = MEDIA_END_PATTERN.subn(
                BANKDATEN_MOBILE_RULES + r"\1", content, count=1
            )
            if n:
                content = new_content
                counts["r3"] = 1

    # R4a — strip orphaned .footer-block rule
    new_content, n = ORPHAN_FOOTER_BLOCK_PATTERN.subn("", content)
    if n:
        content = new_content
        counts["r4a"] = n

    # R4b — strip orphaned .btn-row + .btn-col (amazon-pay-info only)
    if fname == "amazon-pay-info.html":
        new_content, n = ORPHAN_BTN_ROW_PATTERN.subn("", content)
        if n:
            content = new_content
            counts["r4b_btn_row"] = n

        new_content, n = ORPHAN_BTN_COL_MOBILE_PATTERN.subn("", content)
        if n:
            content = new_content
            counts["r4b_btn_col"] = n

    return content, counts


def main() -> int:
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"ERROR: '{TEMPLATE_DIR}' not found. Run from repo root.", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    print(f"Processing {len(files)} templates ...\n")

    grand = {"r1_r2": 0, "r3": 0, "r4a": 0, "r4b_btn_row": 0, "r4b_btn_col": 0}
    for fname in files:
        path = os.path.join(TEMPLATE_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        new_content, counts = transform(original, fname)
        if new_content != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print(
                f"  {fname:42s}  R1/R2={counts['r1_r2']}  "
                f"R3={counts['r3']}  R4a={counts['r4a']}  "
                f"R4b={counts['r4b_btn_row']+counts['r4b_btn_col']}"
            )
            for k in grand:
                grand[k] += counts[k]
        else:
            print(f"  {fname:42s}  (no changes)")

    print(
        f"\nTotals:  R1/R2={grand['r1_r2']}  R3={grand['r3']}  "
        f"R4a={grand['r4a']}  R4b(btn-row)={grand['r4b_btn_row']}  "
        f"R4b(btn-col)={grand['r4b_btn_col']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
