"""
Mobile responsive audit:
For each template, compare classes USED in <body> against classes covered by the
@media (max-width: 680px) block. Report multi-column / mobile-critical classes
that are used but uncovered.

This is read-only; produces a report to stdout.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

# Classes that matter for mobile responsiveness — multi-column layouts,
# tables, buttons, address blocks, etc. If used in body but not in @media,
# that's likely a mobile-rendering gap.
MOBILE_CRITICAL = {
    # Multi-column rows that should stack
    "del-left", "del-right", "del-third",
    "meta-col", "meta-col-spacer",
    "rev-cta-col",
    # Bank transfer table (Vorkasse Bankdaten)
    "bank-table", "bank-td-label", "bank-td-value",
    # Order/product table
    "order-table", "order-table-wrap", "order-th-qty", "order-td-qty",
    "product-name", "product-sku",
    # Totals table
    "totals-table", "totals-td-l", "totals-td-r",
    # Config table (production-guide, invoice)
    "config-table", "config-td-label", "config-td-value",
    # Tracking card
    "tracking-card",
    # Buttons & core layout (most templates already cover these)
    "btn-primary", "btn-outline",
    "card", "card-wrap",
    "hero", "section", "hero-title", "hero-subtitle",
    "support-block", "support-inner",
    "footer-main", "footer-legal-row", "footer-copy-row",
}

MEDIA_HEADER_RE = re.compile(
    r"@media\s+only\s+screen\s+and\s+\(\s*max-width:\s*680px\s*\)\s*\{",
)


def extract_media_block(html: str) -> str | None:
    """Find the @media (max-width:680px) block and return its inner contents,
    balancing braces correctly (nested rules)."""
    m = MEDIA_HEADER_RE.search(html)
    if not m:
        return None
    start = m.end()  # one char after the opening {
    depth = 1
    i = start
    while i < len(html) and depth > 0:
        c = html[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return html[start:i]
        i += 1
    return None
SELECTOR_RE = re.compile(r"\.([a-zA-Z][a-zA-Z0-9_-]*)")
CLASS_ATTR_RE = re.compile(r'class\s*=\s*"([^"]+)"')
BODY_RE = re.compile(r"<body[^>]*>(.*?)</body>", re.DOTALL)


def extract_media_classes(html: str) -> set[str]:
    block = extract_media_block(html)
    if block is None:
        return set()
    return set(SELECTOR_RE.findall(block))


def extract_body_classes(html: str) -> set[str]:
    body_m = BODY_RE.search(html)
    if not body_m:
        return set()
    body = body_m.group(1)
    classes = set()
    for attr in CLASS_ATTR_RE.findall(body):
        for tok in attr.split():
            classes.add(tok)
    return classes


def main():
    files = sorted(p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html")
    rows = []
    for path in files:
        html = path.read_text(encoding="utf-8", errors="ignore")
        media = extract_media_classes(html)
        body = extract_body_classes(html)
        used_critical = body & MOBILE_CRITICAL
        missing = sorted(used_critical - media)
        covered = sorted(used_critical & media)
        rows.append((path.name, covered, missing))

    # Sort: most missing first, then alpha
    rows.sort(key=lambda r: (-len(r[2]), r[0]))

    print(f"{'Template':<42} {'Missing':<7} Uncovered mobile-critical classes")
    print("-" * 110)
    for name, covered, missing in rows:
        if not missing:
            continue
        print(f"{name:<42} {len(missing):<7} {', '.join(missing)}")

    print()
    print("Templates with NO missing mobile-critical classes:")
    for name, covered, missing in rows:
        if not missing:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
