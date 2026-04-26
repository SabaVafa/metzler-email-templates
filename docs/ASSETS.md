# Assets Reference

Every image referenced in the 17 templates, with its source path and which templates use it.

---

## Current state — relative paths (preview-only)

All `<img>` tags currently use **relative paths** like `src="../assets/promotion/foo.png"` so the templates render correctly with `npx serve` for local QA.

**Before going live:** these must be replaced with **absolute HTTPS URLs** on a public host, because email clients (Gmail, Outlook, Apple Mail) cannot reach a sender's local filesystem.

Recommended host base: `https://edelstahl-tuerklingel.de/email-assets/` (same-domain trust = best deliverability). Any `https://…` host works as long as images are publicly reachable without auth.

---

## Find-and-replace plan

After uploading the contents of the `assets/` folder to your chosen host, run a single replace across every file in `templates/`:

| Find | Replace with |
|---|---|
| `src="../assets/` | `src="https://YOUR-CDN/email-assets/` |

Keep the rest of the path identical (`promotion/foo.png`, `reiniger/bar.webp`, etc.) so nothing else needs to change.

---

## Asset inventory

### `assets/product-image.jpg`

Generic product placeholder used in all order-line tables.

Used by: `order-confirmation`, `payment-confirmation`, `production-guide`, `invoice-delivery`, `widerrufsbestaetigung`, `product-question-confirmation`, `review-request`

> Replace with real product images per order line if/when JTL exposes them at email-render time.

### `assets/promotion/`

| File | Used by |
|---|---|
| `blumenkasten-cubic-1-anthrazit.png` | `production-guide`, `delivered` |
| `blumenkasten-cubic-2-anthrazit.png` | `production-guide`, `delivered` |
| `blumenkasten-rondo-anthrazit.png` | `production-guide`, `delivered` |
| `image 628.png` | (not currently referenced — staging asset) |

### `assets/reiniger/`

| File | Used by |
|---|---|
| `metzler-reiniger-fuer-pulverbeschichtete-oberflaechen-edelstahl.webp` | `review-request`, `review-confirmation` |

### `assets/video-thumbnail/`

| File | Used by |
|---|---|
| `werkstatt-einblick.png` | `production-delay` (Werkstatt-Einblick video card) |

---

## Image dimensions used in CSS

| Image type | Rendered size | Notes |
|---|---|---|
| Product line image | 58 × 58 px | `object-fit: cover` |
| Reiniger upsell | 100 × 100 px | `object-fit: cover` |
| Promotion card (Blumenkasten) | 100 % width | aspect preserved |
| Werkstatt video thumbnail | up to 488 px wide | aspect preserved |

Source images may be larger; email clients downscale via `width=` attribute. For Retina, supply 2× source resolution while keeping the rendered `width=` attribute as listed.

---

## Logo

The Metzler logo is rendered as **inline SVG** inside the templates (header `top-band` + dark footer). No image asset to host. If you ever want to swap to PNG fallback (some Outlook configurations strip inline SVG), generate a 220 × 37 px white-on-transparent PNG and host alongside other assets.
