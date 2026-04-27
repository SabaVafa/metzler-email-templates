# Smarty Placeholders Reference

Every `{$variable}` referenced across the 17 templates. Types and example values match the mock data used during design.

---

## URLs

| Placeholder | Used in | Description | Example |
|---|---|---|---|
| `{$bestellungURL}` | order-confirmation, payment-confirmation, production-guide, production-delay, invoice-delivery | Customer's "Meine Bestellungen" detail link for this order | `https://edelstahl-tuerklingel.de/jtl.php?Suchbegriff=…` |
| `{$trackingURL}` | invoice-delivery, track-trace, track-trace-delay, delivered | DHL tracking deep-link | `https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?piececode=…` |
| `{$kontoURL}` | registration-welcome, password-reset (success), account-deletion (recovery) | Customer account dashboard | `https://edelstahl-tuerklingel.de/jtl.php?Login=1` |
| `{$passwordResetURL}` | password-reset | One-time reset link, 60-min validity | `https://edelstahl-tuerklingel.de/jtl.php?pw_neu=…` |
| `{$verificationURL}` | registration-verify | Email-verification one-time link | `https://edelstahl-tuerklingel.de/jtl.php?bestaetigung=…` |
| `{$werkstattVideoURL}` | production-delay | Workshop video thumbnail target (YouTube unlisted or shop page) | `https://edelstahl-tuerklingel.de/werkstatt-einblick` |
| `{$produkt1BewertungURL}` | review-request | Product 1 review form deep-link | `https://edelstahl-tuerklingel.de/bewertung.php?a=12345` |
| `{$produkt2BewertungURL}` | review-request | Product 2 review form deep-link | same pattern |
| `{$newsletterSubscribeURL}` | order-confirmation, delivered, review-request, review-confirmation | Double-opt-in subscribe endpoint (see TRIGGERS.md) | `https://edelstahl-tuerklingel.de/newsletter?action=subscribe` |
| `{$newsletterConfirmURL}` | newsletter-activation | DOI confirmation link with single-use token (24-hour expiry) | `https://edelstahl-tuerklingel.de/newsletter?bestaetigung=…` |
| `{$backInStockConfirmURL}` | back-in-stock-doi | DOI confirmation link for "notify me when available" subscription (24-hour expiry, single-use) | `https://edelstahl-tuerklingel.de/wieder-verfuegbar?bestaetigung=…` |
| `{$unsubscribeURL}` | (CAN-SPAM compliance, every marketing block) | Unsubscribe link for that specific marketing context | dynamic per-email |
| `{$abmeldeURL}` | order-confirmation, gutschein, review-request | Master "E-Mails abbestellen" link in footer | `https://edelstahl-tuerklingel.de/jtl.php?abmelden=1&token=…` |

---

## Customer & order

| Placeholder | Description | Example |
|---|---|---|
| `{$Kunde->cVorname}` | First name | Anna |
| `{$Kunde->cNachname}` | Last name | Müller |
| `{$Bestellung->cBestellNr}` | Order number | 12345 |
| `{$Bestellung->dErstellt}` | Order date | 08.12.2024 |
| `{$Bestellung->fGesamtsumme}` | Order total (EUR) | 208,90 € |

(Use the standard JTL Smarty objects shown above; the mock template files render plain values and need to be re-wired by the developer.)

---

## Conditional / dynamic flags

| Placeholder | Used in | Type | Purpose |
|---|---|---|---|
| `{$carrierAlert}` | track-trace-delay | bool / string | Fire only when carrier reports delay (≥36 h no scan / failed delivery / manual flag) |
| `{$carrierStatusText}` | track-trace-delay | string | Human carrier-status line (e.g. "Sendung verzögert sich") |
| `{$carrierStatusUpdatedAt}` | track-trace-delay | datetime | Timestamp of latest DHL status |

---

## Account-deletion specific

| Placeholder | Used in | Description |
|---|---|---|
| `{$kontoErstelltAm}` | account-deletion | Date the customer's account was originally created (`tkunde.dErstellt`) |
| `{$deletedAt}` | account-deletion | Server `NOW()` when deletion was completed |

---

## Mock values used during design

The .html files currently contain hard-coded German display values for QA. Replace with Smarty when integrating:

| Mock | Smarty source |
|---|---|
| Anna Müller | `{$Kunde->cVorname} {$Kunde->cNachname}` |
| #12345 | `{$Bestellung->cBestellNr}` |
| 208,90 € | `{$Bestellung->fGesamtsumme\|number_format:2:",":"."} €` |
| 08.12.2024 | `{$Bestellung->dErstellt\|date_format:"%d.%m.%Y"}` |
| 14:37 Uhr | `{$timestamp\|date_format:"%H:%M Uhr"}` |
| K-2024-00845 | `{$Kunde->kKunde}` (or formatted variant) |
| BW-2024-12345 | review-ID generator (plugin) |
| FR-2024-12345 | product-question-ID generator (plugin) |
| DANKE10 | `{$Kupon->cKuponName}` |
