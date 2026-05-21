"""
Replace the dark-mode brand-teal accent `#4cc4c5 !important` with `#ffffff !important`
across all 28 email templates. Only affects rules inside the
@media (prefers-color-scheme: dark) block (which is where all #4cc4c5 instances
live).

Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

OLD = "#4cc4c5 !important"
NEW = "#ffffff !important"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count == 0:
        return "skip (no matches)"
    path.write_text(html.replace(OLD, NEW), encoding="utf-8", newline="\n")
    return f"patched ({count} occurrence{'s' if count != 1 else ''})"


def main():
    files = sorted(
        p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html"
    )
    for path in files:
        result = patch(path)
        print(f"  {result:<30} {path.name}")


if __name__ == "__main__":
    main()
