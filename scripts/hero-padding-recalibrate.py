"""
Recalibrate the hero td's inline `padding-bottom` for each template so that the
tinted space ABOVE the badge and BELOW the last inner content are visually equal.

Formula: hero pad-bottom = 36 - (last_inner_row_bottom_padding)
- Top tinted space = 36px (hero pad-top, from .hero class)
- Bottom tinted space = hero pad-bottom + last_inner_row_bottom_padding
- Symmetric when sum = 36

Audited via scripts/hero-padding-audit.py.

Per-template targets:
- Templates with CTA row `padding:16px 22px` → hero pad-bottom = 20px
- Templates with CTA row `padding:14px 10px` → hero pad-bottom = 22px
- Templates with meta card row `padding:10px` → hero pad-bottom = 26px
- Templates with meta card row `padding:16px 22px 20px` → hero pad-bottom = 16px (already correct)
- Templates with no inner padding td (subtitle-only heroes) → no fix needed

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

# {template_name: target_padding_bottom_px}
TARGETS = {
    # CTA row 16px → 20px
    "order-confirmation.html": 20,
    "payment-confirmation.html": 20,
    "invoice-delivery.html": 20,
    "delivered.html": 20,
    "amazon-pay-hard-decline.html": 20,
    "amazon-pay-soft-decline.html": 20,
    "paypal-zahlung-abgelehnt.html": 20,
    "production-delay.html": 20,
    "zahlungsinformationen-vorkasse.html": 20,
    # CTA row 14px → 22px
    "password-reset.html": 22,
    # Meta-card row 10px → 26px
    "account-created-by-admin.html": 26,
    "back-in-stock-doi.html": 26,
    "newsletter-activation.html": 26,
    "registration-verify.html": 26,
    "registration-welcome.html": 26,
    "customer-group-assignment.html": 26,
    "product-question-confirmation.html": 26,
    "production-guide.html": 26,
    "review-confirmation.html": 26,
    "review-request.html": 26,
    "zahlungs-erinnerung.html": 26,
    # Already correct (no edit needed, but listed for completeness):
    # track-trace.html, track-trace-delay.html, widerrufsbestaetigung.html → 16
    # No fix needed (no internal meta card):
    # account-deletion.html, amazon-pay-info.html, contact-form-confirmation.html, gutschein.html
}

HERO_RE = re.compile(r'(<td class="hero"[^>]*?)(\s*style="([^"]*)")?(\s*>)')


def patch(path: Path, target: int) -> str:
    html = path.read_text(encoding="utf-8")
    m = HERO_RE.search(html)
    if not m:
        return "skip (no hero td)"
    prefix = m.group(1)
    has_style = m.group(2) is not None
    existing_style = (m.group(3) or "").strip()
    close = m.group(4)

    target_prop = f"padding-bottom:{target}px;"

    if has_style:
        # Strip any existing padding-bottom, then prepend the target
        cleaned = re.sub(r'padding-bottom:\s*\d+px;?\s*', '', existing_style).strip()
        if cleaned and not cleaned.endswith(';'):
            cleaned += ';'
        new_style_value = f" {target_prop}{(' ' + cleaned) if cleaned else ''}".strip()
        new_tag = f'{prefix} style="{new_style_value}"{close}'
        if existing_style == new_style_value:
            return "skip (already at target)"
    else:
        new_tag = f'{prefix} style="{target_prop}"{close}'

    new_html = html[:m.start()] + new_tag + html[m.end():]
    if new_html == html:
        return "skip (no change)"
    path.write_text(new_html, encoding="utf-8", newline="\n")
    return f"patched ({target}px)"


def main():
    for name, target in TARGETS.items():
        path = TEMPLATES_DIR / name
        if not path.exists():
            print(f"  skip (missing)                {name}")
            continue
        result = patch(path, target)
        print(f"  {result:<35} {name}")


if __name__ == "__main__":
    main()
