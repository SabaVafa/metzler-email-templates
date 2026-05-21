"""
Responsive pass 8 — fix the .ops-meta-table (internal staff/ops alerts)
overflowing by ~7px on mobile.

Templates affected: production-delay, amazon-pay-info.

The 2-column ops-meta-table (label 38% / value 62%) has long value content
that pushes the table 7px past the 360px content area.

Fix:
  - table-layout: fixed on .ops-meta-table (forces table to 100% of parent)
  - word-break: break-word on .ops-meta-row td (wraps long values)

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

MEDIA_HEADER_RE = re.compile(
    r"(@media\s+only\s+screen\s+and\s+\(\s*max-width:\s*680px\s*\)\s*\{)",
)

INSERT_RULE = (
    "\n      .ops-meta-table { table-layout: fixed !important; }"
    "\n      .ops-meta-row td { word-break: break-word !important; overflow-wrap: break-word !important; }"
)

SENTINEL = ".ops-meta-table { table-layout: fixed"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if "ops-meta-table" not in html:
        return "skip (no ops-meta-table)"
    if SENTINEL in html:
        return "skip (already applied)"

    new_html, n = MEDIA_HEADER_RE.subn(
        lambda m: m.group(1) + INSERT_RULE, html, count=1
    )
    if n == 0:
        return "skip (no @media block)"

    path.write_text(new_html, encoding="utf-8", newline="\n")
    return "patched"


def main():
    files = sorted(
        p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html"
    )
    for path in files:
        result = patch(path)
        print(f"  {result:<35} {path.name}")


if __name__ == "__main__":
    main()
