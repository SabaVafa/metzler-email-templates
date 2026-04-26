# Legal Framework

Every legal hook baked into the templates, with the BGB / DSGVO / UWG reference and what the dev team must do.

---

## PDF attachments — mandatory

| Template | Attach | Legal basis |
|---|---|---|
| `order-confirmation.html` | **Widerrufsbelehrung PDF** + **Muster-Widerrufsformular PDF** | §312f BGB (Bestätigung des Vertrags in Textform) + §356a BGB (Widerrufsfrist), Art. 246a §1 EGBGB |
| `invoice-delivery.html` | **§14 UStG invoice PDF**; Widerrufsbelehrung PDF for **non-custom** items only | §14 UStG / GoBD |

DEV note in each template's `<!-- LEGAL NOTE -->` block at top of `<body>` lists which PDFs to attach.

---

## Widerrufsrecht logic

- **§312g Abs. 2 Nr. 1 BGB** — Widerrufsrecht is **excluded for custom-engraved goods** (eindeutig auf den Kunden zugeschnitten).
- `widerrufsbestaetigung.html` therefore filters to **non-custom items only** (see TRIGGERS.md).
- `delivered.html` does NOT advertise Widerrufsrecht (cart may contain custom items).

---

## DSGVO opt-in gates

| Block | Where it appears | Legal basis | Dev wiring |
|---|---|---|---|
| Newsletter | `order-confirmation`, `delivered`, `review-request`, `review-confirmation` | Art. 6(1)(a) DSGVO | Use **double-opt-in**, never instant-subscribe |
| Bewertungserinnerung (review reminder) | gates `review-request` send | Art. 6(1)(a) DSGVO | Checkbox at checkout; suppress send if not ticked |
| DHL carrier-email forwarding | `track-trace*` flow | Art. 6(1)(a) DSGVO | Checkbox at checkout; gates whether shop forwards customer email to DHL |
| Account retention beyond active use | not user-facing — disclosed via Datenschutzerklärung footer link | §§ 147 AO + 257 HGB (10-year retention for invoices/tax docs) | Isolate retained data from marketing systems |

---

## §7 Abs. 3 UWG (Bestandskunden — existing-customer marketing)

Upsell blocks in `production-guide.html` and `delivered.html` carry an opt-out:

> "Keine Empfehlungen mehr erhalten"

This is required because §7(3) UWG allows product recommendations to existing customers without prior opt-in only if every email offers a clear opt-out.

---

## Footer requirements (uniform across all 17)

Mandatory footer link order (dev — do not reorder):

1. Impressum
2. Datenschutz
3. AGB
4. Widerrufsrecht
5. Batterieentsorgungsgesetz
6. Hinweise zur Elektroaltgeräteentsorgung

Plus `E-Mails abbestellen` (`{$abmeldeURL}`) on order-confirmation, gutschein, review-request — required by §7 Abs. 3 UWG.

Company line (every template):

```
Metzler GmbH · [STREET] · 72770 Reutlingen
Geschäftsführer: Denis Metzler · HRB XXXXX · Amtsgericht Reutlingen · USt-IdNr.: DE XXX XXX XXX
```

> **Open**: Street currently rendered as "Tübingerstraße 9"; Datenschutzerklärung says "Täleswiesenstr. 9". HRB & USt-IdNr. are placeholders. See [`OPEN-ITEMS.md`](OPEN-ITEMS.md).

---

## DSGVO Art. 17 (account deletion)

`account-deletion.html`:

- Sent AFTER deletion job completes server-side
- Confirms login revoked + marketing flags set to opt-out
- Does NOT mention retained tax records in body — disclosure is via Datenschutzerklärung link in footer (§§ 147 AO / 257 HGB 10-year retention)
- Retained data MUST be isolated from marketing/recommendation systems

---

## Trusted Shops / ODR

If Trusted Shops integration is active, ensure the shop's general legal pages already include:
- ODR link (Art. 14 ODR-VO): `https://ec.europa.eu/consumers/odr/`
- Trusted Shops Käuferschutz disclosure if used

These are typically rendered in shop-wide footer / Impressum, not per-email.
