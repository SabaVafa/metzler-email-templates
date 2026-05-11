# Open Items

Pending decisions / data the dev team or client must resolve before going live.

---

## 1. Street address ⚠ blocking

All 17 footers currently render **"Tübingerstraße 9"**. The Datenschutzerklärung (authoritative legal doc) says **"Täleswiesenstr. 9"**. Client to confirm correct street, then a single find/replace updates all files.

## 2. Contact email domain

All templates use `info@edelstahl-tuerklingel.de` (shop domain). Datenschutzerklärung uses `info@metzlergmbh.de` (corporate). Client to confirm which is correct for customer-facing transactional email.

## 3. URL slugs to verify

Footer links currently guess these slugs:

- `https://edelstahl-tuerklingel.de/batterieentsorgungsgesetz`
- `https://edelstahl-tuerklingel.de/elektroaltgeraeteentsorgung`

Dev to confirm against actual JTL CMS pages and update if different.

## 4. HRB number + USt-IdNr.

Footer placeholder text:

```
HRB XXXXX · Amtsgericht Reutlingen · USt-IdNr.: DE XXX XXX XXX
```

Replace with real values from the Impressum.

## 5. Image hosting

All `<img src>` paths are relative. Upload the `assets/` folder to a public HTTPS host and run the find/replace described in [`ASSETS.md`](ASSETS.md).

## 6. Newsletter double-opt-in flow

The 4 templates with newsletter blocks currently link to `{$newsletterSubscribeURL}`. Dev must wire this to a **double-opt-in** endpoint (Art. 6(1)(a) DSGVO requires confirmed consent), not an instant-subscribe URL.

## 7. Outlook desktop logo PNG fallback — wiring complete, image hosting still pending

The 56 inline-SVG logos (header + footer × 28) are now wrapped in MSO conditional comments with a PNG fallback (`assets/logo-white.png`). Modern clients (Apple Mail, Gmail, etc.) render the SVG; Outlook desktop renders the PNG.

**Still pending before launch**: the PNG `src` is currently `../assets/logo-white.png` (relative path). When the email is sent and opened in Outlook desktop, that path resolves to nothing — the image fails to load. The PNG fallback only fully works after assets are hosted on a public HTTPS URL (see §5 Image hosting).

When §5 is done, find/replace `../assets/logo-white.png` → `https://your-host/path/logo-white.png` in all 28 templates.

## 8. Dark-mode CSS — pending separate pass

Light/dark color-scheme **meta tags** are now declared in all 28 templates (`<meta name="color-scheme" content="light dark">`). The CSS palette for `@media (prefers-color-scheme: dark)` and `[data-ogsc]` (Outlook.com) is **not yet implemented** — pending a focused design pass with token mapping (cards `#252525`, body `#1a1a1a`, badges adjusted, etc.). Without that CSS, dark-mode-aware clients (Apple Mail, Gmail) will fall back to their auto-darken behavior, which is acceptable but not optimal. Track as a follow-up workstream.

## 9. Product-image `alt` text in plugin templates

The 12 templates with mock `product-image.jpg` rows now use `alt=""` (decorative — relies on the product name in the adjacent `<div class="product-name">` cell to convey meaning, which is WCAG-compliant). For production:

- Recommended: keep `alt=""` (product name is already visible to AT users via the next cell — descriptive alt would be redundant)
- Alternative: set `alt="{$oPosition->cName|escape}"` and use `alt=""` only when the cName is also visible inline. Decide once per email-client behavior testing.

Templates affected: order-confirmation, payment-confirmation, review-request, production-guide, invoice-delivery, widerrufsbestaetigung, product-question-confirmation, amazon-pay-soft-decline, amazon-pay-hard-decline, paypal-zahlung-abgelehnt, zahlungs-erinnerung, zahlungsinformationen-vorkasse.

## 10. Unified FAQ block — pending

A unified *"Häufige Fragen"* block was drafted but not yet wired. Decision: same 3 Q+A across `order-confirmation`, `production-guide`, `production-delay`, `invoice-delivery`. Replaces the two existing production-only FAQ blocks (which used different per-email content and linked out to `/faq/[slug]` pages).

Format: Q in bold 14 px `#1a1a1a`, A in regular 14 px `#555` line-height 1.65, `1px solid #ebebeb` divider between rows. No outbound link — answers are inlined in the email so customers don't need to leave.

### Drafted content (awaiting confirmation)

**Q1.** Wann erhalte ich meine Bestellung?
> Lagerware versenden wir innerhalb von 1–3 Werktagen. Sonderanfertigungen aus unserer Werkstatt brauchen meist 8–14 Werktage. Sobald Ihr Paket unterwegs ist, melden wir uns mit der Sendungsnummer.

**Q2.** Kann ich meine Bestellung noch ändern oder stornieren?
> Solange Ihre Bestellung noch nicht in der Produktion ist, ändern wir sie gern für Sie — bitte melden Sie sich kurz bei uns. Für nicht individuell gefertigte Artikel gilt nach Erhalt der Ware Ihr 14-tägiges Widerrufsrecht.

**Q3.** Wie lange dauert die Fertigung Ihrer Bestellung?
> Standardware ist bei uns lagernd und geht direkt in den Versand. Sonderanfertigungen — etwa Beschriftungen, Sonderfarben oder individuelle Maße — fertigen wir einzeln in unserer Werkstatt in Reutlingen und brauchen meist 8–14 Werktage.

### Placeholder details to confirm before launch

- **1–3 Werktage** for Lagerware shipping (Q1) — confirm against actual operations
- **8–14 Werktage** for Sonderanfertigungen (Q1 + Q3) — confirm against actual operations
- **Beschriftungen, Sonderfarben, individuelle Maße** (Q3) — confirm these are the most representative Sonderanfertigung types, or replace with the right three (Gravur, Klingelplatten, Hausnummern, …)

## 11. ⚠ § 7(3) UWG opt-out — re-add OR remove upsell before launch

The cross-sell §7(3) Nr. 4 opt-out link *"Keine Empfehlungen mehr erhalten"* was removed from `track-trace.html` + `production-guide.html` (commit a484784) on user request "for now". The Blumenkasten 3-card upsell remains in both templates.

**Current state is not safely launchable.** Under § 7 Abs. 3 UWG, the upsell carve-out requires *"bei jeder Verwendung klar und deutlich"* opt-out info on every send. Without the link, exposes Metzler to Abmahnung from competitors / Wettbewerbszentrale (typical cost 800–2.000 € per warning).

Pick one of:

- **(a) Re-add the opt-out link** — wire `{$unsubscribeURL}` to an endpoint that records "this customer doesn't want product recommendations" (distinct from full newsletter unsubscribe). The block to reinstate:
  ```html
  <!-- Opt-out footer (§7(3) Nr. 3 UWG) -->
  <p style="font-size:11px; color:#999; line-height:1.6; margin:20px 0 0; text-align:center;">
    <a href="{$unsubscribeURL}" target="_blank" style="color:#999; text-decoration:underline;">Keine Empfehlungen mehr erhalten</a>
  </p>
  ```
- **(b) Add explicit opt-in checkbox at checkout** (DSGVO Art. 6(1)(a)): *"Ich möchte Produktempfehlungen erhalten"*. Replaces §7(3) as the legal basis.
- **(c) Remove the upsell entirely** — strip the Blumenkasten 3-card grid from both templates. No werbliche content = no opt-out required.

Decision and implementation must be in place before either template is sent to a real customer.

## 12. Email-client QA before launch

Send each of the 28 templates to a test inbox in each major German-market client and verify rendering:

- **Apple Mail** (macOS + iOS) — both light and dark mode
- **Gmail** (web + iOS app + Android app)
- **Outlook.com** (web)
- **Outlook desktop** (Windows) — confirm logo PNG fallback renders, VML buttons render
- **GMX / Web.de** — significant German market share, often missed by international testers

Use Litmus 7-day free trial, Brevo's free transactional tier, or fire from JTL backend itself for full Smarty rendering test.

---

## Quick checklist for dev integration

- [ ] Replace `[STREET]` placeholder logic — pick correct street, find/replace
- [ ] Replace `info@edelstahl-tuerklingel.de` if corporate `info@metzlergmbh.de` is preferred
- [ ] Verify `/batterieentsorgungsgesetz` and `/elektroaltgeraeteentsorgung` slugs
- [ ] Fill in HRB + USt-IdNr.
- [ ] Upload `assets/` to public host, find/replace `../assets/` → absolute URL
- [ ] Wire `{$newsletterSubscribeURL}` to double-opt-in
- [ ] Wire all other Smarty placeholders (see [`PLACEHOLDERS.md`](PLACEHOLDERS.md))
- [ ] Configure JTL triggers per [`TRIGGERS.md`](TRIGGERS.md)
- [ ] Attach Widerrufsbelehrung PDF to order-confirmation + invoice-delivery (non-custom only)
- [ ] Attach §14 UStG invoice PDF to invoice-delivery
- [ ] Gate review-request on Bewertungserinnerung opt-in
- [ ] QA: send each of the 17 templates to a Gmail / Outlook / Apple Mail / Mobile-Gmail test inbox before launch
