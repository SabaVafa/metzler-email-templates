"""
Responsive pass 3 — fix mobile overflow caused by un-breakable long product names
and the .order-table-wrap propagating width to its parent table-cell.

Symptoms before fix (at 375px viewport in iframe):
  - Order table column expands to fit "Edelstahl-Türklingel" → table > 335px
  - Parent <td class="section"> expands → card expands → page horizontal scrolls
  - Totals table (sibling of order table) inherits the expanded section width

Fix: append these rules inside each template's @media (max-width:680px) block:

    .product-name, .product-sku {
      word-break: break-word !important;
      overflow-wrap: break-word !important;
    }
    .order-table-wrap {
      display: block !important;
      max-width: 100% !important;
      width: 100% !important;
      overflow-x: auto !important;
    }
    .order-table, .totals-table { table-layout: fixed !important; width: 100% !important; }

Idempotent — safe to re-run.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

MEDIA_HEADER_RE = re.compile(
    r"(@media\s+only\s+screen\s+and\s+\(\s*max-width:\s*680px\s*\)\s*\{)",
)

INSERT_RULES = """
      .product-name, .product-sku { word-break: break-word !important; overflow-wrap: break-word !important; }
      .order-table-wrap { display: block !important; max-width: 100% !important; width: 100% !important; overflow-x: auto !important; }
      .order-table, .totals-table { table-layout: fixed !important; width: 100% !important; }"""

SENTINEL = ".product-name, .product-sku { word-break: break-word"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if SENTINEL in html:
        return "skip (already applied)"
    if ".order-table" not in html and ".totals-table" not in html and ".product-name" not in html:
        return "skip (no order/totals table)"

    new_html, n = MEDIA_HEADER_RE.subn(
        lambda m: m.group(1) + INSERT_RULES, html, count=1
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
