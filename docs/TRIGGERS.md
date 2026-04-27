# Trigger Mapping

Which JTL event fires which template, and any conditional logic the dev team must wire.

---

## Happy-path journey (sequential)

| # | Template | JTL Trigger | Conditions / notes |
|---|---|---|---|
| 1 | `registration-verify.html` | Customer signs up — email-verification required | Send before account is active |
| 2 | `registration-welcome.html` | Email verification clicked | Send after `tkunde.cAktiv = 'Y'` |
| 3 | `order-confirmation.html` | `kBestellung` created, payment method = Vorkasse | **Attach Widerrufsbelehrung PDF** (§312f + §356a BGB) |
| 4 | `payment-confirmation.html` | Vorkasse payment matched / `Bestellung.cStatus` → "bezahlt" | |
| 5 | `production-guide.html` | T+2 days after order, only when `cStatus IN ('bezahlt','in_bearbeitung')` AND order contains custom items | Mid-journey orientation |
| 6 | `invoice-delivery.html` | Order shipped — `Bestellung.cStatus` → "versandt" | **Attach §14 UStG invoice PDF**; **attach Widerrufsbelehrung PDF** (non-custom items only) |
| 7 | `track-trace.html` | DHL status → "in_zustellung" / "out_for_delivery" | |
| 8 | `delivered.html` | DHL status → "zugestellt" | Strip any Widerrufsrecht claim — custom items excluded per §312g(2)(1) BGB |
| 9 | `review-request.html` | T+3 days after delivered, **only if** customer opted in to "Bewertungserinnerung" at checkout (Art. 6(1)(a) DSGVO) | Gate on opt-in |
| 10 | `review-confirmation.html` | Customer submits review form | |
| 11 | `gutschein.html` | Manual / promotional dispatch | Coupon DANKE10, validity 60 days |

---

## Sad / branching paths

| Template | JTL Trigger | Conditions |
|---|---|---|
| `production-delay.html` | Manual flag in admin OR `cStatus` change to "verzögert" | **Custom items only**; replaces `production-guide` for that order |
| `track-trace-delay.html` | DHL status anomaly: ≥36 h no scan / failed delivery / manual flag | Send instead of `track-trace`; do **not** apologize on Metzler's behalf for carrier issues |
| `widerrufsbestaetigung.html` | Customer submits Widerruf form | **Non-custom items only** — §312g(2)(1) BGB excludes Widerrufsrecht for custom-engraved goods |

---

## Account / ancillary

| Template | JTL Trigger | Conditions |
|---|---|---|
| `product-question-confirmation.html` | Customer submits product Q form | Send confirmation only; the actual answer is sent manually |
| `password-reset.html` | "Passwort vergessen?" form submitted | Token validity 60 min |
| `account-deletion.html` | DSGVO Art. 17 deletion completed server-side | Send AFTER deletion job finishes; pass `{$kontoErstelltAm}` from the soon-to-be-deleted record |
| `newsletter-activation.html` | Customer submits newsletter subscription form | DOI per Art. 6 Abs. 1 lit. a DSGVO + § 7 Abs. 2 Nr. 3 UWG. Subscription is only legally valid AFTER the customer clicks `{$newsletterConfirmURL}`. Token expires 24 h; unconfirmed subscriptions are dropped (Art. 17). |
| `back-in-stock-doi.html` | Customer submits "Benachrichtigen, sobald wieder verfügbar" form on a stock-item product page | DOI per Art. 6 Abs. 1 lit. a DSGVO + § 7 Abs. 2 Nr. 3 UWG. **Restrict trigger to non-custom products only** — custom-engraved items are made-to-order, not stocked. Token expires 24 h; unconfirmed subscriptions are dropped. After the actual back-in-stock notification fires, drop the email/product binding (one-shot use). |
| `contact-form-confirmation.html` | Customer submits the general "Kontakt" form on the shop | Send confirmation only; the actual reply is written manually by the support team. Distinct from `product-question-confirmation` (different form, different trigger). |
| `account-created-by-admin.html` | Metzler staff manually creates a customer account in the JTL admin panel | Use cases: B2B onboarding, phone/trade-fair orders, data migration, service intervention. Customer's account is created **without** a password — the email's CTA links to a one-time password-set link (`{$passwortFestlegenURL}`, 24 h expiry). Per Art. 13 DSGVO, the data subject must be informed. The "Sie haben kein Konto angefordert?" section MUST link the customer to support (not 'ignore') because misattributed accounts need correction. **If the trigger context is not customer-requested**, swap the *"Auf Ihren Wunsch hin"* phrasing in the hero subtitle. |

---

## Hard rules to enforce in trigger logic

1. **Newsletter / Produktempfehlung blocks** appear in 4 templates (order-confirmation, delivered, review-request, review-confirmation). They MUST link to the double-opt-in subscribe endpoint, never an instant-subscribe URL — Art. 6(1)(a) DSGVO.
2. **Upsell blocks** in `production-guide` and `delivered` carry "Keine Empfehlungen mehr erhalten" opt-out — §7 Abs. 3 UWG (Bestandskunden).
3. **Review-request gate**: do not send unless the customer ticked the review-reminder consent at checkout.
4. **DHL email forwarding** to DHL requires Art. 6(1)(a) opt-in at checkout.
5. **Widerrufsbestätigung filter**: trigger must check whether ANY item in the order is custom-engraved. If yes → suppress (custom items have no Widerrufsrecht). If mixed cart → trigger only for the non-custom subset.
