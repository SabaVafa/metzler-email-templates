"""
Responsive pass 2 — override HTML width="640" attribute on .card and .support-inner
inside each template's @media (max-width:680px) block.

Why: the cards use <table class="card" width="640"> for Outlook desktop. That HTML
width attribute survives until mobile, where the CSS @media only set margin/radius —
nothing overrode the 640px width. Result: at 375px viewport, the card stays 640
wide and the iframe overflows.

This script adds:
    .card, .support-inner { width: 100% !important; max-width: 100% !important; }
right after the @media opening brace, idempotently.

Run from repo root:
    python scripts/responsive-pass-2.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

MEDIA_HEADER_RE = re.compile(
    r"(@media\s+only\s+screen\s+and\s+\(\s*max-width:\s*680px\s*\)\s*\{)",
)

INSERT_RULE = (
    "\n      .card, .support-inner "
    "{ width: 100% !important; max-width: 100% !important; }"
)

# Sentinel to detect "already applied"
SENTINEL = ".card, .support-inner { width: 100% !important;"


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
