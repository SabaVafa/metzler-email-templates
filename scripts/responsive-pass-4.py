"""
Responsive pass 4 — defensive blanket safety net for mobile.

Symptoms before fix (at 375px viewport):
  - Every section overflows by ~30-50px on the right
  - CTA buttons, subtitle text, payment-card, totals, progress tracker — all cropped
  - Indicates one or more elements forcing >375px width despite earlier passes

Rather than chase each element individually, apply broad guards inside each
template's @media (max-width:680px) block:

    body, #bodyTable { overflow-x: hidden !important; }
    .card, .card-wrap { max-width: 100% !important; box-sizing: border-box !important; }
    table { max-width: 100% !important; }
    img { max-width: 100% !important; height: auto !important; }
    .payment-card, .tracking-card, .ref-code, .ref-label { word-break: break-word !important; overflow-wrap: break-word !important; }

This is the canonical "safe mobile email" pattern — overflow-x:hidden on the
root container catches anything still pushing past viewport without affecting
real content layout.

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
      body, #bodyTable { overflow-x: hidden !important; }
      .card, .card-wrap { max-width: 100% !important; box-sizing: border-box !important; }
      table { max-width: 100% !important; }
      img { max-width: 100% !important; height: auto !important; }
      .payment-card, .tracking-card, .ref-code, .ref-label { word-break: break-word !important; overflow-wrap: break-word !important; }"""

SENTINEL = "body, #bodyTable { overflow-x: hidden"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if SENTINEL in html:
        return "skip (already applied)"

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
