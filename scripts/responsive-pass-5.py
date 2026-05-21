"""
Responsive pass 5 — force table-layout:fixed on the root #bodyTable and .card
to stop them from being widened by min-content of some nested element.

Root cause discovered via DOM inspection:
  - iframe @375px viewport → body clientWidth = 360
  - But #bodyTable rendered at 384.7px (24.7px overflow), with table-layout:auto
  - Auto layout was honoring a 384.7px min-content somewhere in the tree, ignoring
    the table's width:100% / max-width:100% declaration
  - Setting table-layout:fixed snaps it to 360 (= 100% of parent body)

The previous overflow-x:hidden in pass 4 just hid the symptom; this addresses
the cause. Both passes can coexist (defense in depth).

Adds to each template's @media (max-width:680px):

    #bodyTable, .card { table-layout: fixed !important; }

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
    "\n      #bodyTable, .card { table-layout: fixed !important; }"
)

SENTINEL = "#bodyTable, .card { table-layout: fixed"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
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
