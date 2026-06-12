"""
Fix asymmetric breathing room around the meta-card-table CTA button in 16
templates: the hero's default 36px bottom padding stretches the tinted space
below the button much further than the CTA td's own top padding (typically
16px), creating a visible imbalance.

Fix: add inline `style="padding-bottom:16px;"` on each hero td that ends with
a meta-card table CTA. Matches the CTA td's top padding (16px), so the
tinted space above and below the button reads as equal.

Skipped:
- password-reset.html (already fixed manually with padding-bottom:14px)
- templates whose hero doesn't end with a meta-card-table CTA (see HANDOFF list)

Idempotent — re-running is safe.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

AFFECTED = [
    "order-confirmation.html",
    "payment-confirmation.html",
    "invoice-delivery.html",
    "delivered.html",
    "track-trace.html",
    "track-trace-delay.html",
    "production-delay.html",
    "amazon-pay-hard-decline.html",
    "amazon-pay-soft-decline.html",
    "paypal-zahlung-abgelehnt.html",
    "zahlungsinformationen-vorkasse.html",
    "newsletter-activation.html",
    "back-in-stock-doi.html",
    "registration-verify.html",
    "registration-welcome.html",
    "account-created-by-admin.html",
]

OLD = '<td class="hero" bgcolor="#f7f9f7">'
NEW = '<td class="hero" bgcolor="#f7f9f7" style="padding-bottom:16px;">'


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if NEW in html:
        return "skip (already applied)"
    if OLD not in html:
        return "skip (pattern not found)"
    path.write_text(html.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
    return "patched"


def main():
    for name in AFFECTED:
        path = TEMPLATES_DIR / name
        if not path.exists():
            print(f"  skip (missing)                {name}")
            continue
        result = patch(path)
        print(f"  {result:<30} {name}")


if __name__ == "__main__":
    main()
