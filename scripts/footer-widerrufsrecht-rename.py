"""
Rename the footer legal-link label "Widerrufsrecht" -> "Vertrag widerrufen"
across all 28 email templates. Action-phrased label, not noun-phrased.

Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

OLD = ">Widerrufsrecht<"
NEW = ">Vertrag widerrufen<"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if OLD not in html:
        return "skip (no match)"
    path.write_text(html.replace(OLD, NEW), encoding="utf-8", newline="\n")
    return "patched"


def main():
    files = sorted(
        p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html"
    )
    for path in files:
        result = patch(path)
        print(f"  {result:<20} {path.name}")


if __name__ == "__main__":
    main()
