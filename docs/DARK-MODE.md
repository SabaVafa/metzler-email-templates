# Dark Mode — Developer Handoff

All 28 email templates ship with built-in dark-mode support. This doc explains how it works, what NOT to touch when integrating with JTL-Shop 5, and how to verify it after deployment.

---

## 1. TL;DR

Dark mode is fully self-contained inside each template's `<style>` element. **No additional configuration, Smarty variables, or JTL admin settings are required.** When a customer opens the email in a dark-mode-aware client, the dark palette activates automatically.

When integrating into JTL:

- ✅ Copy/paste HTML **as-is** into the JTL email template slots
- ❌ Do not minify or strip `<style>`, `<meta name="color-scheme">`, or `@media (prefers-color-scheme: dark)` blocks
- ⚪ The `<script>` block in `<head>` is preview-only and safe to leave OR strip — has zero effect on real emails

---

## 2. How it works

Every template includes three independent layers:

### Layer A — Color-scheme declaration (meta tags)

In every `<head>`:

```html
<meta name="color-scheme" content="light dark" />
<meta name="supported-color-schemes" content="light dark" />
```

These tell the email client *"this email supports both modes"* — which makes clients render the email more gracefully in dark mode (vs. aggressive auto-inversion).

### Layer B — Dark-mode CSS overrides (`@media` rule)

Inside every template's `<style>` element, just before the responsive breakpoint:

```css
/* ── DARK MODE ── */
@media (prefers-color-scheme: dark) {
  body, #bodyTable { background-color: #121212 !important; }
  .card { background-color: #1c1c1c !important; ... }
  /* ... etc — full palette mapping ... */
}
```

This block contains explicit dark-mode color overrides for:
- Surfaces (body, card, hero, inner boxes, payment-card, tracking-card)
- Text colors (full 6-step grey ramp inverted)
- Hero badge palette (green / amber / red variants per template)
- Brand-teal text + dashed borders (brightened to `#4cc4c5` for readability on dark)
- Tinted alert cards (amber `Hinweis zur Zustellung`, etc.)
- Inline-styled elements via attribute selectors (`[style*="color:#1a1a1a"]` etc.)

### Layer C — Preview-only light-mode default (JS shim)

The `<head>` of each template ends with this small block:

```html
<!-- PREVIEW-ONLY: defaults browser preview to light mode...
     SAFE TO LEAVE IN — has no effect when sent via email. -->
<script>
  (function(){
    function setMode(){
      var dark = location.hash === "#dark";
      /* finds @media (prefers-color-scheme: dark) rules and sets
         their media-text to "not all" (disabled) by default,
         or to "all" when the URL contains #dark */
    }
    ...
  })();
</script>
```

This only affects **browser previews** during development. Email clients (Apple Mail, Gmail, Outlook, GMX, Web.de, etc.) strip `<script>` tags entirely, so the shim has zero effect on real email rendering.

**Safe to leave in production**. Removing it is optional and only useful for HTML-purity reasons.

---

## 3. Dev integration checklist

When porting templates into JTL-Shop 5:

### Do
- [x] Paste each HTML file as-is into its JTL email-template slot
- [x] Wire up Smarty placeholders (see [`PLACEHOLDERS.md`](PLACEHOLDERS.md)) — they live in the `<body>`, not the dark-mode CSS
- [x] Preserve the entire `<head>` including `<style>`, all three meta tags, and the `<script>` shim
- [x] Test dark mode in at least one real client (Apple Mail or Gmail web with dark mode active)

### Don't
- [ ] Don't run an HTML minifier that strips `@media` rules
- [ ] Don't strip the `color-scheme` / `supported-color-schemes` meta tags
- [ ] Don't replace the dark `<style>` block with anything client-specific (JTL's built-in styles, etc.) — dark mode lives inside the template's own `<style>`
- [ ] Don't auto-inline the CSS using a tool that flattens `@media` queries (some inliners do this — they turn `@media (prefers-color-scheme: dark)` into duplicated inline styles which breaks everything)

---

## 4. QA checklist after deployment

Send each template to a test inbox (or use Litmus / Email on Acid) and verify dark-mode rendering in:

| Client | Expected behavior |
|---|---|
| **Apple Mail (macOS)** — dark mode ON | ✅ Full dark palette, neutral dark surfaces, lighter teal accents |
| **Apple Mail (iOS)** — dark mode ON | ✅ Same as macOS |
| **Gmail web** — browser in dark mode | ✅ Full dark palette |
| **Outlook 365 web** — browser in dark mode | ✅ Full dark palette |
| **Gmail iOS app** — system dark | ⚠️ Partial dark mode (Gmail does its own auto-adjustment); should still be readable |
| **Gmail Android app** — system dark | ⚠️ Partial dark mode (same as iOS) |
| **Outlook desktop (Windows)** — system dark | ⚪ Renders light by default; only goes dark with explicit user setting in Outlook Options |
| **GMX / Web.de** | ⚪ No dark mode |

Spot-check for these specific issues:

- [ ] White boxes inside dark sections (sign that an inline style isn't being caught)
- [ ] Invisible text (especially brand-teal text — `#015253` is too dark on dark; should be `#4cc4c5` in dark mode)
- [ ] Voucher code `DANKE10` in gutschein.html is fully readable
- [ ] Address detail lines (Lieferadresse / Rechnungsadresse) in order-confirmation are fully readable
- [ ] amazon-pay-info ops table card is dark (not white)
- [ ] Amber alert card (`Hinweis zur Zustellung`) in track-trace-delay reads as a dark amber surface with light amber label

---

## 5. Architecture decisions

A few choices documented so future devs/designers don't have to reverse-engineer:

| Decision | Rationale |
|---|---|
| **Neutral dark palette** (`#121212` / `#1c1c1c` / `#222222`) instead of brand-tinted darks | Premium standard (Apple, GitHub, Material 3). Brand teal lives in accents, not surfaces |
| **Brand teal `#015253` for backgrounds, `#4cc4c5` for text/borders on dark** | `#015253` has too-low contrast as text on `#1c1c1c`. As a background with white text, it works fine |
| **Three-step elevation** (body → card → highlight) | Visual depth without contrast escalation |
| **Light mode untouched** | Every dark rule lives inside `@media (prefers-color-scheme: dark) { ... }`. Removing the dark block doesn't affect light rendering |
| **Attribute selectors for inline styles** | Many template elements use inline `style="background-color:..."` or `style="color:..."`. CSS class selectors don't catch them — attribute selectors `[style*="color:#1a1a1a"]` do. This is why the dark block is large (~80 selectors) |
| **Per-template badge palette detection** | Each template has its own `.hero-badge` color (green/amber/red). The Python script detects and applies the matching dark variant per template |

---

## 6. Re-tuning the palette

If you want to adjust the dark-mode colors (e.g., make the dark surface slightly warmer, or tweak the brand-teal-on-dark to a different hue):

```bash
# Source script:
scripts/dark-mode-pass-v2.py
```

The script:
1. Detects each template's hero-badge palette automatically
2. Replaces the entire `@media (prefers-color-scheme: dark)` block atomically across all 28 templates
3. Is **idempotent** — safe to re-run
4. Light mode CSS is never touched

Edit the constants at the top of the script (`DARK_COMMON_TEMPLATE`, `HERO_BADGE_DARK`), then run:

```bash
python scripts/dark-mode-pass-v2.py
```

---

## 7. Known limitations

These are documented as accepted trade-offs:

| Limitation | Why | Workaround |
|---|---|---|
| Outlook desktop (Windows) doesn't auto-activate dark mode | Outlook desktop ignores `prefers-color-scheme` unless user enables a specific setting | None — accept it. ~80% of Outlook desktop users on the customer side will see light mode |
| Gmail mobile apps do their own dark-mode auto-adjustment | Gmail's algorithm overrides our @media in some cases | The `color-scheme` meta tag makes Gmail's adjustment more conservative — but not perfect |
| Some inline-styled elements may slip through | If a template uses a color we didn't anticipate in the attribute selectors | Add the color to `dark-mode-pass-v2.py` and re-run |
| Hero badges lose color distinction in clients that aggressively override colors | Auto-inversion can mute the green/amber/red signaling | Acceptable — the badge is supporting metadata, not the primary signal |

---

## 8. Files touched

| File | Purpose |
|---|---|
| `templates/*.html` (all 28) | Each has the dark `@media` block + color-scheme meta + preview JS shim |
| `scripts/dark-mode-pass-v2.py` | Source-of-truth script for the dark CSS; idempotent |
| `scripts/dark-mode-pass.py` | Initial v1 (kept for reference; v2 supersedes it) |
| `docs/DARK-MODE.md` | This file |

---

## 9. Quick sanity test

To prove dark mode is working in a single template:

```bash
# Open any template in Chrome
# Press F12 → Ctrl+Shift+P → "Show Rendering"
# Find "Emulate CSS media feature prefers-color-scheme"
# Set to "dark"
```

**With the preview-shim active**: the template will stay light (shim disables `@media`).
**To activate dark in preview**: append `#dark` to the URL → `http://localhost:5200/templates/order-confirmation.html#dark`. Then the dark CSS becomes active even with DevTools "no emulation".

For real email-client QA, the shim is irrelevant — clients strip it.
