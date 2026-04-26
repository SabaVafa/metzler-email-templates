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

## 7. Optional — restore dark-mode palette

Dark-mode CSS was disabled across all templates (forced light mode) per design decision. The palette is preserved in git history if the client later wants to re-enable it.

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
