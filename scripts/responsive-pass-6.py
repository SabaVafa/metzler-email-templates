"""
Responsive pass 6 — backport `class="support-inner"` onto the 18 templates that
have an unclassed inner table inside their support block.

Root cause discovered after pass-5b: only 10 of 28 templates have the class.
The other 18 use:
    <td class="support-block" align="center">
      <table width="640" ...>

All the mobile fixes targeting .support-inner (width:100%, table-layout:fixed)
never matched on those 18, so the support block kept rendering at 640px and
overflowing the iframe.

Strategy: locate `<td class="support-block"` followed by `<table width="640"`
(with intermediate whitespace) and inject class="support-inner" if not already
present.

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

# Match: <td class="support-block" ...> ... whitespace ... <table width="640" ...>
# Capture the table tag so we can rewrite it with class="support-inner".
PATTERN = re.compile(
    r"(<td[^>]*class=\"support-block\"[^>]*>\s*)<table(\s+(?![^>]*\bclass=)[^>]*?width=\"640\"[^>]*?)>",
    re.DOTALL,
)


def add_class(match: re.Match) -> str:
    prefix = match.group(1)
    attrs = match.group(2)
    return f'{prefix}<table class="support-inner"{attrs}>'


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    new_html, n = PATTERN.subn(add_class, html)
    if n == 0:
        if 'class="support-inner"' in html:
            return "skip (already has class)"
        return "skip (pattern not found)"
    path.write_text(new_html, encoding="utf-8", newline="\n")
    return f"patched ({n} occurrence{'s' if n != 1 else ''})"


def main():
    files = sorted(
        p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html"
    )
    for path in files:
        result = patch(path)
        print(f"  {result:<35} {path.name}")


if __name__ == "__main__":
    main()
