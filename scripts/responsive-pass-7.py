"""
Responsive pass 7 — backport the progress-tracker fix to the 7 templates
that have a 5-step tracker.

After pass 6 cleaned the support block, a different overflow showed up:
the 5-circle progress tracker (background #f7faf7 with 24px 16px inner padding)
renders at ~345px wide in a 320px section content area, clipping the 5th icon.

Fix (already shipped manually on production-guide):
  1. Add class="progress-tracker" to the outer background table
  2. Add class="progress-tracker-inner" to the inner padding TD
  3. Add class="progress-circles" to the circles+connectors table
  4. Mobile @media rules:
       .progress-tracker, .progress-circles { table-layout: fixed !important; }
       .progress-tracker-inner { padding: 20px 8px !important; }

Applies to: order-confirmation, payment-confirmation, invoice-delivery,
track-trace, delivered, production-guide (already done), production-delay.

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

# 1. Outer background table — add class="progress-tracker"
OUTER_RE = re.compile(
    r'<table(\s+(?![^>]*\bclass=)[^>]*?)style="background-color:#f7faf7;\s*border:1px solid #e0e8e0;[^"]*"',
)


def add_outer_class(m: re.Match) -> str:
    return f'<table class="progress-tracker"{m.group(1)}style="background-color:#f7faf7; border:1px solid #e0e8e0; border-radius:6px; overflow:hidden;"'


# 2. Inner padding TD — add class="progress-tracker-inner"
INNER_RE = re.compile(
    r'<td(\s+(?![^>]*\bclass=)[^>]*?)style="padding:24px 16px;"',
)


def add_inner_class(m: re.Match) -> str:
    return f'<td class="progress-tracker-inner"{m.group(1)}style="padding:24px 16px;"'


# 3. Circles+connectors table — find the <table width="100%"...> immediately
#    inside the progress-tracker-inner td. We'll match the first such table
#    after the inner td opening.
CIRCLES_RE = re.compile(
    r'(<td class="progress-tracker-inner"[^>]*>\s*(?:<!--[^>]*-->\s*)*)'
    r'<table(\s+(?![^>]*\bclass=)[^>]*?width="100%"[^>]*)>',
)


def add_circles_class(m: re.Match) -> str:
    return f'{m.group(1)}<table class="progress-circles"{m.group(2)}>'


# 4. Mobile @media rules
MEDIA_HEADER_RE = re.compile(
    r"(@media\s+only\s+screen\s+and\s+\(\s*max-width:\s*680px\s*\)\s*\{)",
)
MEDIA_RULES = (
    "\n      .progress-tracker, .progress-circles { table-layout: fixed !important; }"
    "\n      .progress-tracker-inner { padding: 20px 8px !important; }"
)
MEDIA_SENTINEL = ".progress-tracker, .progress-circles { table-layout: fixed"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if "background-color:#f7faf7" not in html or "#e0e8e0" not in html:
        return "skip (no tracker)"

    actions = []
    if 'class="progress-tracker"' not in html:
        html, n = OUTER_RE.subn(add_outer_class, html, count=1)
        if n:
            actions.append("outer-class")
    if 'class="progress-tracker-inner"' not in html:
        html, n = INNER_RE.subn(add_inner_class, html, count=1)
        if n:
            actions.append("inner-class")
    if 'class="progress-circles"' not in html:
        html, n = CIRCLES_RE.subn(add_circles_class, html, count=1)
        if n:
            actions.append("circles-class")
    if MEDIA_SENTINEL not in html:
        html, n = MEDIA_HEADER_RE.subn(lambda m: m.group(1) + MEDIA_RULES, html, count=1)
        if n:
            actions.append("media-rules")

    if not actions:
        return "skip (already applied)"

    path.write_text(html, encoding="utf-8", newline="\n")
    return "patched [" + ", ".join(actions) + "]"


def main():
    files = sorted(
        p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html"
    )
    for path in files:
        result = patch(path)
        print(f"  {result:<55} {path.name}")


if __name__ == "__main__":
    main()
