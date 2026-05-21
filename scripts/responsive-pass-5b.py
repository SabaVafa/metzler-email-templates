"""
Responsive pass 5b — extend pass-5's table-layout:fixed to .support-inner too.

After pass 5 fixed #bodyTable and .card, a different overflow showed up in the
support block at the bottom of every template (phone, hours, button cropped).
Same root cause: .support-inner is a <table class="support-inner" width="640">
with auto table-layout, so it bloats from min-content the same way.

Replaces the pass-5 rule with an extended selector list. Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

OLD = "#bodyTable, .card { table-layout: fixed !important; }"
NEW = "#bodyTable, .card, .support-inner { table-layout: fixed !important; }"


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if NEW in html:
        return "skip (already applied)"
    if OLD not in html:
        return "skip (pass-5 rule not found)"
    path.write_text(html.replace(OLD, NEW), encoding="utf-8", newline="\n")
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
