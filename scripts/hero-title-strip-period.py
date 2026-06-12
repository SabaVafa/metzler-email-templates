"""
Strip the trailing period from each template's <h1 class="hero-title">…</h1>.
26 of 28 templates end the hero title with ".". User wants them removed for a
cleaner punctuation-free hero treatment.

Idempotent — re-running on a stripped title is a no-op.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

# Matches: <h1 class="hero-title">TEXT.</h1> (with an actual period before </h1>)
HERO_RE = re.compile(r'(<h1 class="hero-title">[^<]*?)\.(</h1>)')


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    new_html, n = HERO_RE.subn(r"\1\2", html, count=1)
    if n == 0:
        return "skip (no trailing period)"
    path.write_text(new_html, encoding="utf-8", newline="\n")
    return "patched"


def main():
    files = sorted(p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html")
    for path in files:
        result = patch(path)
        print(f"  {result:<30} {path.name}")


if __name__ == "__main__":
    main()
