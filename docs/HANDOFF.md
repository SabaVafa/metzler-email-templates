# Session Handoff — Metzler Email Templates

Paste this at the start of a new session, then say *"continue from this handoff under all listed rules"*.

---

## 🆕 Updates — May 2026 session

Substantial polish + dark-mode work completed. **Read [`DARK-MODE.md`](DARK-MODE.md)** for the dark-mode developer handoff.

### Structural
- **Canvas widened 568 → 640 px** across all 28 templates (`scripts/width-pass-640.py`). Mobile breakpoint 620 → 680. Rationale: 3-col upsell + 5-step tracker were cramped.
- **Upsell moved 06 → 05** — Blumenkasten cross-sell now lives in `track-trace.html`, not `delivered.html`.
- **production-guide section order swapped** — "Aus der Manufaktur" tips now lead, "Ihre Artikel" recap follows.
- **`delivered.html` cleanups** — "Alles passt?" damage-check section removed.
- **`review-request.html` + `review-confirmation.html`** — closing "TEAM NOTE" sign-off paragraphs removed.

### Dark mode (full implementation)
- v1 → v2 → multiple patches. Final: neutral palette (`#121212` body / `#1c1c1c` card / `#222` highlight), brand teal preserved for accents, lighter teal `#4cc4c5` for interactive text on dark. See `docs/DARK-MODE.md`.
- Light mode CSS untouched throughout — dark lives in `@media (prefers-color-scheme: dark)` block.
- **Preview-only JS shim** (`<script>` block in `<head>` of each template) forces light mode in local browser preview. Email clients strip `<script>` so dark mode still works in real inboxes. Append `#dark` to URL for dark preview.
- Tooling: `scripts/dark-mode-pass-v2.py` (idempotent, palette-aware).

### Legal / footer
- **Contact email**: `info@edelstahl-tuerklingel.de` → **`service@metzlergmbh.de`** across all 28
- **Address**: confirmed → **Täleswiesenstrasse 9** (was placeholder Tübingerstraße)
- **Legal IDs**: HRB 768215 · Amtsgericht **Stuttgart** (corrected from Reutlingen) · USt-IdNr DE322754305 · WEEE DE 63539391
- **Phone hotline**: updated to **+49 (0) 7121 / 317 7310 · Mo–Fr.: 09:00–16:00 Uhr** everywhere (tel:+4971213177310)
- **Footer legal-link order** aligned with website: `Datenschutz · AGB · Impressum · Batterieentsorgungsgesetz · Widerrufsrecht · Hinweise zur Elektroaltgeräteentsorgung`
- **Footer copyright**: `© 2013 – 2026 | Metzler GmbH` (dropped "Alle Rechte vorbehalten")
- **§35a GmbHG line** simplified: `Geschäftsführer: Denis Metzler · Amtsgericht Stuttgart · HRB 768215 · USt-IdNr.: DE322754305` (WEEE moved to linked Impressum)
- **"E-Mails abbestellen" link removed** from order-confirmation, gutschein, review-request (transactional emails always sent — misleading to imply unsubscribe)

### Frozen final decisions
- **§7(3) UWG opt-out link** ("Keine Empfehlungen mehr erhalten") permanently removed from upsell templates (track-trace + production-guide). Legal risk acknowledged + accepted. Do NOT propose re-adding.
- **Werkstatt → Manufaktur** global swap in customer-visible text
- **"Was passiert als nächstes?" → "Bestellfortschritt"** in 6 progress-tracker templates only (3 non-tracker templates kept original heading or got contextual rename)
- **Newsletter block heading + intro** rewritten to "Newsletter abonnieren / Verpassen Sie keine Angebote…" in 4 promotional templates
- **Upsell heading**: "Empfehlung aus unserer Manufaktur" → **"Das könnte Ihnen auch gefallen"**
- **Upsell intro**: rewritten to *"Passend zu Ihrer Bestellung: unsere pulverbeschichteten Blumenkästen aus Stahl — in großer Farbauswahl, passend zu Ihrem Briefkasten."* ⚠️ Note: 3 cards still all RAL 7016 — copy says "Farbauswahl" but cards aren't diversified yet

### Copy refinements (iterative — user-driven, one-by-one)
~47 numbered copy refinements applied across hero subtitles, section headings, body paragraphs. Templates touched: order-confirmation, payment-confirmation, production-guide (5+ sections), production-delay, invoice-delivery, track-trace, delivered, review-request, review-confirmation, gutschein, widerrufsbestaetigung.

The 3 "Was passiert als nächstes?" sections in contact-form-confirmation / product-question-confirmation / review-confirmation were **converted from paragraphs to bulleted-list format** (matches registration-welcome pattern: `&bull;&nbsp;` prefix + `line-height:1.7`).

### Tooling new this session
- `scripts/width-pass-640.py` — canvas widen, idempotent
- `scripts/dark-mode-pass-v2.py` — full dark-mode block, idempotent + palette-aware
- `scripts/dark-mode-pass.py` (v1, superseded)
- `scripts/contact-update-2026-05.py` — phone + hours rewrite

### Pending follow-ups flagged this session
- **Upsell card diversification**: cards still all RAL 7016 Anthrazit, copy promises "großer Farbauswahl"
- **Preheader sync**: production-delay preheader matches new hero (done), but consider whether subject/`<title>` should also update on the hero-rewritten templates (currently flagged as "leave as-is" in commit msgs)
- **Image hosting** still blocked (the `werkstatt-einblick.png` thumbnail in production-delay is 488px native but now stretched to 584px — slight blur risk; needs higher-res asset before launch)
- **Inconsistency to flag with web team**: shop-website Impressum still shows OLD phone number (+4971213179114) — email footer uses correct new number

---

## ⚠️ Priority #1: Consistency

Consistency across all 28 templates outranks individual-template polish. Every decision must be checked against the existing cluster first. Reuse canonical blocks, established phrasings, hero patterns, design tokens, and section structures. Backport new better patterns to siblings. The customer reads all 28 emails as one ongoing conversation with one brand; one outlier breaks the spell.

---

## Where the project stands

**28 templates shipped** — 22 customer-facing (Phase 1) + 6 plugin templates (Phase 2). All polished against COPY-RULES, audited end-to-end, plus follow-up passes for accessibility, responsiveness, JTL+guest compatibility, and JTL-honesty.

**Deferred / pending workstreams** (priority-ordered):

| # | Workstream | Status |
|---|---|---|
| 1 | **JTL-honesty fixes** (fabricated data — Verwendungszweck, "Voraussichtliche Lieferung" dates, Rechnungsnummer format) | Audit complete, fixes proposed, **awaiting approval** |
| 2 | **JTL admin verifications** — Gast-Bestellstatus, Gastbewertungen, paymentURL existence, FAQ slug pages | Blocked on dev/admin team |
| 3 | **Unified FAQ block** for 4 emails | Drafted in `OPEN-ITEMS.md §10`, awaiting placeholder confirmation (Werktag-Zeiträume, Sonderanfertigung examples) |
| 4 | **Dark-mode CSS pass 2** (~40 rules per template + `[data-ogsc]` Outlook.com mirrors) | Design palette mapped; deferred as low priority |
| 5 | **Image hosting** (`OPEN-ITEMS.md §5`) — `assets/` to public HTTPS, find/replace `../assets/` → absolute URL | Blocked on hosting decision |
| 6 | **Outlook PNG src URL swap** | Blocked on §5 |
| 7 | **Open business decisions** — street address, contact email, HRB/USt-IdNr, URL slugs, JTL admin path, DOI flow wiring | Blocked on business/dev team |
| 8 | **Email-client QA** before launch | Tooling ready (`scripts/qa-send-all.py`); awaiting trigger |

---

## Templates inventory (28)

**Phase 1 — 22 customer-facing**
1. order-confirmation
2. payment-confirmation
3. production-guide
4. production-delay *(sad-path of 3)*
5. invoice-delivery
6. track-trace
7. track-trace-delay *(sad-path of 6)*
8. delivered
9. review-request
10. review-confirmation
11. gutschein
12. widerrufsbestaetigung
13. product-question-confirmation
14. password-reset
15. registration-verify
16. registration-welcome
17. account-deletion
18. newsletter-activation
19. back-in-stock-doi
20. contact-form-confirmation
21. account-created-by-admin
22. customer-group-assignment

**Phase 2 — 6 plugin templates**

P1. amazon-pay-soft-decline — temporary auth failure → Amazon-Pay-Übersicht retry
P2. amazon-pay-hard-decline — permanent refusal → mailto support for alternative
P3. amazon-pay-info — internal staff alert (red badge, JTL-Backend + Seller Central two-button row, *not* customer-facing)
P4. zahlungs-erinnerung — Vorkasse payment reminder, Bankdaten card-led
P5. zahlungsinformationen-vorkasse — first informational delivery of bank details *(JTL slot is mislabeled "Rechnungskauf" but Metzler uses for Vorkasse)*
P6. paypal-zahlung-abgelehnt — PayPal refused → mailto support for alternative *(sibling of P2)*

---

## Files / structure

- **Repo**: GitHub `SabaVafa/metzler-email-templates` (private). Local at `C:\Users\s.vafakhah\Desktop\Purchase Confirmation Email\metzler-email-templates\`. **All edits go there, then `git add && git commit && git push`.** The flat root-level `.html` files are a frozen backup — **do not edit**.
- **`templates/`** — 28 `.html` files, image paths use `../assets/`
- **`assets/`** — `product-image.jpg`, `logo-white.png`, `promotion/`, `reiniger/`, `video-thumbnail/`
- **`docs/`** — `README`, `COPY-RULES`, `PLACEHOLDERS`, `TRIGGERS`, `LEGAL`, `ASSETS`, `OPEN-ITEMS`, `HANDOFF` *(this file)*
- **`scripts/`** — 5 re-runnable Python transforms + 1 SMTP send-all (see Tooling below)
- **`index.html`** — clickable preview menu at root with all 28 cards (header reads *"28 templates · 22 customer-facing + 6 plug-in · JTL-Shop 5 · edelstahl-tuerklingel.de"*)
- **Preview**: `npx serve -p 5200` from repo root → `http://localhost:5200/`
- **`gh` CLI** at `$LOCALAPPDATA/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`, authenticated as `SabaVafa`

---

## Frozen design tokens

### 3-palette badge system
- **Green** `#eaf3ea` / `#2d6e2d` — confirmation, success, informational
- **Amber** `#fdf3e3` / `#8a5a00` — payment-attention (Soft/Hard-Decline, Zahlungs-Erinnerung, PayPal abgelehnt)
- **Red** `#fde8e8` / `#a91e1e` — internal staff alerts only (Amazon Pay Info P3)
- **No fourth palette.** Don't introduce new colors without explicit reason.

### Card system
- Body bg `#f2f4f2`, page-card `#ffffff`, hero bg `#f7f9f7`, footer `#01292A`, top band `#015253`
- Card max-width 568 px with −40 px teal-band overlap
- Mobile breakpoint `@media (max-width: 620px)`
- MSO/VML fallbacks on all primary/outline buttons

### Bankdaten card structure (frozen)
Identical across `order-confirmation`, `zahlungs-erinnerung`, `zahlungsinformationen-vorkasse`:
- Title: *"Vorkasse — Überweisung"*
- Subtitle (active voice): *"Bitte verwenden Sie den unten stehenden Verwendungszweck, damit wir Ihre Zahlung sicher zuordnen können."*
- Row order: Empfänger / IBAN / BIC / Bank / Betrag
- ref-hint: *"Bitte exakt so angeben — ohne weitere Zusätze."*
- Real bank data: **Metzler GmbH · DE09 6439 1200 0308 5077 00 · GENODES1MTZ · Volksbank Ermstal-Alb eG**

### Numbered-bullet style (frozen — hollow border)
Used in 6 templates (`production-guide`, `amazon-pay-soft-decline`, `amazon-pay-hard-decline`, `paypal-zahlung-abgelehnt`, `zahlungs-erinnerung`, `zahlungsinformationen-vorkasse`):
- 24 × 24 px circle
- Border: `2px solid #015253`, **no fill**
- Number: `#015253`, 12 px Montserrat 700, line-height 20 px
- Cell width: 24 px

### Mailto deep-link pattern (frozen)
Used in P2 + P6 for "switch payment method" CTAs:
- `mailto:info@edelstahl-tuerklingel.de?subject=Andere%20Zahlungsart%20f%C3%BCr%20Bestellung%20%23{$Bestellung->cBestellNr}`
- Pre-filled subject lets support route the request instantly

### Typography
- Body / instruction text: **14 px** minimum (bumped from 12 in a11y pass 2)
- UPPERCASE labels, tracker labels, footer copy, status chips: 12 px (justified by hierarchy/convention)
- Helvetica Neue body, Montserrat headings
- Footer text: opacity 0.65 (bumped from 0.5 for WCAG AA contrast on `#01292A`)

### Accessibility
- All 28 templates have `role="img"` + `aria-label="Metzler GmbH"` on header + footer logos
- All decorative tracker SVGs (16×16 cog/truck/house) have `aria-hidden="true"`
- Generic `alt="Produktbild"` is replaced with `alt=""` (decorative — product name in adjacent cell)
- `<meta name="color-scheme" content="light dark">` declared in all 28
- All layout tables have `role="presentation"`
- All language attributes set (`<html lang="de">`)

### Responsiveness (mobile)
- Footer: 28 px vertical / 20 px horizontal mobile padding
- Support-inner: 20 px horizontal padding mobile (matches hero/section)
- Bankdaten card stacks label/value vertically on mobile in 3 templates (`order-confirmation`, `zahlungs-erinnerung`, `zahlungsinformationen-vorkasse`) so IBAN doesn't wrap mid-number
- Order-confirmation `.del-*` 3-column delivery row stacks correctly on mobile (left/right padding reset)

### Outlook desktop PNG fallback (frozen pattern, src path pending)
All 56 inline-SVG logos (header + footer × 28) wrapped:
```html
<!--[if mso]>
<img src="../assets/logo-white.png" width="W" height="H" alt="Metzler GmbH" style="display:block; border:0; margin:0 auto;" />
<![endif]-->
<!--[if !mso]><!-->
<svg ...>original SVG</svg>
<!--<![endif]-->
```
Path is currently relative — when image hosting (§5) is done, find/replace `../assets/logo-white.png` → absolute URL.

---

## Frozen content rules — single source: `docs/COPY-RULES.md`

Read it before editing any template. Most important rules inlined here so this handoff stands alone.

### Voice & register
- **Formal Sie / Ihre / Ihnen** — capitalized throughout
- **Premium artisan-Manufaktur** zone (Manufactum / Breuninger), not Zalando-casual
- **Calm, confident, factual** — never marketing-flair, never SaaS-startup-y
- **Native German** — no translation flavor, no anglicisms, no calques (e.g., *"Wann immer es Ihnen passt"* = bad)

### Banned phrases (hard rules — never use)
1. *"Vielen Dank für Ihre Geduld"*
2. *"Wir freuen uns, Sie als Kundin / Kunde…"*
3. *"Wir arbeiten hart daran"*
4. *"exklusiv für Sie"*
5. *"Ihre ehrliche Meinung zählt"* (and *"ehrlichste"* / *"ehrliche"* in body copy)
6. *"wir hoffen…"*
7. *"in der Regel"* → use *"meist"*
8. *"nichts weiter tun"*
9. *"als wir ursprünglich geplant hatten"* → use *"als gedacht"*
10. *"Das ist X. Das ist Y."* (AI-parallelism)
11. *"nicht nur X sondern Y"*
12. *"Ihre Meinung zählt"*
13. *"freiwillig & kostenlos"*
14. *"Jetzt anmelden"* (newsletter context — use *"Newsletter abonnieren"*)
15. *"Damit wir … trotzdem [verb] können"* (adversity-overcome framing — superseded by *"Gern [verb] wir mit Ihnen — wir halten Ihre Bestellung bis dahin für Sie bereit"*)

### Translation tells to remove
- `&` outside brand names → *"und"*
- *"hochwertig"* / *"high-quality"* → drop (brand context implies quality)
- *"in Echtzeit"* → *"jederzeit"*
- *"Live verfolgen"* → *"Sendung verfolgen"*
- *"per E-Mail"* / *"dieser E-Mail"* inside an email → drop (channel is implicit)
- *"startklar"* → *"eingerichtet"* / *"bereit"*
- *"kostenlos"* on free items → *"als Dankeschön"* or drop
- *"aus der Praxis"* → drop
- Stacking adjectives → split or simplify
- Compound-noun stacks → split into clauses

### Behördendeutsch / passive → active replacements
- *"Die Zustellung erfolgt"* → *"Voraussichtlich erreicht es Sie"*
- *"liegt uns vor"* → *"Wir bearbeiten / Unser Team sieht sich … an"*
- *"wird … geprüft / bearbeitet"* → *"wir prüfen / wir bearbeiten"*
- *"werden erstattet"* → *"Sie erhalten … zurück"*
- *"einen Hinweis beilegen"* → *"vermerken Sie … auf …"*
- *"Wir informieren Sie aktiv"* → *"Wir melden uns rechtzeitig"*
- *"ist nicht mehr möglich"* → *"Sie können … nicht mehr"*
- *"garantiert"* → *"sorgt für"* / *"bringt"*

### Hero stack rule
Badge + Title + CTA must NOT all repeat the same action verb. Vary register: badge confirms, title pivots, CTA is the verb.

### Hero title pattern (confirmations)
`[noun] ist [state]`:
- *"Ihre Bestellung ist eingegangen."*
- *"Ihre Zahlung ist eingegangen."*
- *"Ihr Paket ist angekommen."*
- *"Ihr Widerruf ist eingegangen."*
- *"Ihre Zahlung ist nicht möglich."* *(Hard-Decline / PayPal abgelehnt)*

### Customer-perspective active voice
*"Sie erhalten 208,90 € zurück"* (not *"208,90 € werden erstattet"*)
*"Wir prüfen Ihre Bewertung"* (not *"Ihre Bewertung wird geprüft"*)

### Drop admin preambles in security/confirmation emails
The customer just clicked the action — they know they did. Action-first.
- ❌ *"Wir haben eine Anfrage zum Zurücksetzen erhalten"*
- ✅ *"Setzen Sie Ihr Passwort über den Button unten neu."*

### No personalised greeting in body
None of the 28 templates open with *"Guten Tag {$Kunde->cVorname}"*. Cluster convention is to open with the action.

### Tone-by-context overrides
- **Delay (in-house)** — calm, reframe as quality, give next-touchpoint promise, no apology-bait
- **Carrier delay (DHL)** — no apology on Metzler's behalf, attribute to carrier, link to their tracking
- **Cancellation / Widerruf** — neutral, respectful, active voice for refund (*"Sie erhalten X zurück"*)
- **Joy moments** — concrete value-led titles
- **Security emails** — action-first, no admin preamble, always include security-fallback section
- **Payment-failure / Decline** — formal-warm Manufaktur: *"Gern vereinbaren wir mit Ihnen eine andere Zahlungsart — Ihre Bestellung halten wir bis dahin für Sie bereit."*

### Punctuation & typography
- Em-dash `—` for emphasis, en-dash `–` for ranges (*"17. – 19. Dez."*)
- HTML entities for umlauts in body, raw UTF-8 only in `<title>`
- Hero titles end with period; section labels don't
- **No `&`** outside brand names — always *"und"*

### Anti-redundancy
At most **two** "we'll get back to you / contact us" beats per email:
- Unique-purpose section (e.g., security fallback)
- Canonical support block at the bottom

### 10-point checklist for every new template
1. Hero stack — title doesn't repeat badge or CTA verb?
2. Banned phrases — none?
3. Active voice from customer perspective?
4. Translation tells gone (`&`, *"hochwertig"*, *"Live"*, *"per E-Mail"*)?
5. Section labels match established phrases?
6. Newsletter / Support / Footer use canonical version?
7. Tracker labels (if used) are nouns, not past participles?
8. Punctuation: em-dash for emphasis, en-dash for ranges?
9. HTML entities for umlauts in body, raw UTF-8 in `<title>`?
10. Tone matches context (delay vs joy vs cancellation vs security)?

---

## Canonical blocks (identical across all 28)

- **Support block**: *"Fragen zu Ihrer Bestellung? — Wir antworten Ihnen persönlich."* + phone `07121 / 317 91 14` + Mo–Fr 08:00–17:00 + E-Mail-Button
- **Newsletter block** (4 emails): *"Neues aus unserer Werkstatt"* heading + canonical body + *"Newsletter abonnieren"* CTA
- **Tracker labels** (8 emails): *Bestellung · Zahlung · Produktion · Versand · Lieferung*
- **Footer**: dark teal `#01292A` with all text at **0.65 opacity** white (post-a11y); legal links left-to-right (Impressum · Datenschutz · AGB · Widerrufsrecht · Batterieentsorgung · Elektroaltgeräte)

---

## JTL realities — what we know now

### Guest customers
**Most Metzler customers check out as guests** (no account). This shapes several decisions:

- `{$bestellungURL}` may resolve to a login-walled URL for guests **unless JTL's "Gast-Bestellstatus" feature is enabled in admin → Einstellungen → Kundenkonto.** Verification pending. If not enabled, 5 templates with *"Bestellung ansehen"* CTAs need rework (`order-confirmation`, `payment-confirmation`, `production-delay`, `zahlungsinformationen-vorkasse`, `delivered`).
- Review-form URLs (`{$produkt1BewertungURL}`) may require login unless **"Gastbewertungen erlauben"** is enabled. Verification pending.

### JTL plugin Smarty scopes
Plugin templates don't get the full `{$Kunde}` / `{$Bestellung}` scope JTL natives do. Specific knowns:
- **Amazon Pay plugin templates** (P1, P2, P3) — order-detail items wrapped in `{if isset($Bestellung->Positionen)}…{/if}` for graceful degradation
- **Zahlungs-Erinnerung** — JTL native, full scope expected
- **Contact form plugin** — exposes Nachricht, Vorname/Nachname, Email, Firma, Telefon, Mobil, Fax (per actual rendered output sample); does **NOT** expose `{$kontaktReferenz}`. Optional fields wrapped in `{if $var}` conditionals in our template.
- **Amazon Pay can't change payment method at this phase via plugin** — manual change by Metzler staff via phone/email is the only path. Hence `Zahlungs-Erinnerung` and other payment-issue templates rely on the support block, not on a self-service CTA.

### What JTL does NOT compute
- "Voraussichtliche Lieferung" date ranges — fabricated in 5 templates, needs `{$liefertermin}` placeholder or removal
- "Voraussichtliche Fertigstellung" date — same issue in `production-guide`
- "Voraussichtlicher Versand" — same in `review-confirmation`
- Custom Verwendungszweck codes (e.g., `C7SOFA7EWM`) — convention is **Bestellnummer = Verwendungszweck**

### What JTL likely does provide (verify per plugin/install)
- `{$Bestellung->cBestellNr}` — order number
- `{$Bestellung->cZahlungsartName}`, `{$Bestellung->cVersandartName}` — method names (currently hardcoded in many templates)
- `{$Bestellung->cGesamtsummeLocalized}` — total
- `{$Bestellung->Positionen}` — items (in JTL natives; varies in plugins)
- `{$Bestellung->oRechnungsadresse}` / `{$Bestellung->oLieferadresse}` — addresses
- `{$smarty.now}` — always available

---

## Tooling — `scripts/` directory

| Script | Purpose |
|---|---|
| `a11y-pass-1.py` | Bulk a11y transforms across 28 templates: footer opacity 0.5→0.65, color-scheme meta tags, logo aria-label, decorative SVG aria-hidden, alt="" replacement |
| `a11y-pass-2-text-size.py` | Bumps body/instruction text 12px→14px (Option A: `.payment-subtitle`, `.ref-hint`, `.del-eta-note`, `.wr-note`, `.support-hours`, 3 inline body sentences) |
| `responsive-pass-1.py` | Mobile fixes: footer/support padding, Bankdaten label/value stack, orphan-CSS cleanup |
| `logo-mso-fallback.py` | Wraps 56 SVG logos in MSO conditional comments with PNG fallback |
| `qa-send-all.py` | SMTP send-all helper for pre-launch email-client testing. Configures via env vars (SMTP_HOST/PORT/USER/PASS, QA_FROM, QA_TO). Filter by filename substring; --dry-run mode |

All scripts are idempotent and re-runnable from repo root.

---

## Recent commit history (all on `main`)

| Phase | Range |
|---|---|
| Phase 1 (22 customer-facing) | initial through `1eb498a` |
| Phase 2 (6 plugin templates) | `ff4e7eb` through `64c2c0e` |
| A11y pass 1 (WCAG fixes) | `baf57fa` |
| Numbered-bullet unification | `9244c62` |
| QA send-all script | `944ab99` |
| Responsive pass 1 | `ce5313e` + `e4f1de3` |
| Outlook PNG fallback wiring | `ddae670` |
| A11y pass 2 (12→14 px body text) | `dddf6f4` |
| FAQ draft parked in OPEN-ITEMS | `31baecb` |
| Delivered.html mock URL fix | `ab9b18f` |
| Zahlungs-Erinnerung CTA removal | `d66fd37` |
| Vorkasse meta-card swap (Datum→Bestellnummer) | `499454d` |
| Index header refresh | `f143180` |
| F1 — replace 6 hardcoded `/mein-konto/` URLs | `03bd6e2` |
| Contact-form realignment with actual JTL output | `39dfee1` + `641e81e` |

---

## Open items still on `docs/OPEN-ITEMS.md`

1. ⚠ **Street address** — footers say *"Tübingerstraße 9"*, Datenschutz says *"Täleswiesenstr. 9"* — client to confirm
2. **Contact email domain** — `info@edelstahl-tuerklingel.de` (shop) vs `info@metzlergmbh.de` (corporate)
3. **URL slugs** to verify — `/batterieentsorgungsgesetz`, `/elektroaltgeraeteentsorgung`
4. **HRB + USt-IdNr.** placeholders still `XXXXX` / `DE XXX XXX XXX`
5. **Image hosting** — `assets/` to public HTTPS, find/replace `../assets/` → absolute URL
6. **Newsletter DOI flow** wiring in JTL backend
7. **Outlook PNG fallback URL swap** — wiring complete; src path swap blocked on §5
8. **Dark-mode CSS** (deferred, low priority)
9. **Product-image `alt` text** — `alt=""` for now; production decision per email-client behavior
10. **Unified FAQ block** — drafted, awaiting placeholder confirmation (Werktag-Zeiträume, Sonderanfertigung examples)
11. **Email-client QA** before launch (use `scripts/qa-send-all.py`)

---

## Pending JTL-honesty fixes (audit complete, awaiting approval)

🔴 **Critical** — fabricated data:
- **H1** *"Voraussichtliche Lieferung"* date ranges in 5 templates — replace with `{$liefertermin}` placeholder
- **H2** *"Voraussichtlicher Versand"* in `review-confirmation` — same fix
- **H3** *"C7SOFA7EWM"* Verwendungszweck in 4 templates — replace with `{$Bestellung->cBestellNr}` (Bestellnummer = Verwendungszweck per JTL convention)
- **H4** *"RE-2024-12345"* Rechnungsnummer in `invoice-delivery` — verify Smarty var name with dev

🟠 **Major**:
- **H5** Cubic II + Rondo prices in `delivered.html` / `production-guide.html` — verify match actual shop or replace
- **H6** FAQ block Werktag-Zeiträume — already deferred to OPEN-ITEMS §10

🟡 **Minor — verify with dev**:
- **H9** Hardcoded *"Vorkasse (Überweisung)"* / *"DHL Paket"* names — switch to `{$Bestellung->cZahlungsartName}` / `{$Bestellung->cVersandartName}` for templates firing across multiple methods (notably `order-confirmation`)
- **H10** `delivered.html` actual delivery time — verify JTL exposes from carrier feedback

---

## Working agreement (collaboration rules)

- **Always propose before editing** — show structural blueprint + every copy decision before writing/changing HTML
- **No inline body-text icons**
- **No banned phrases** (see COPY-RULES)
- **Cross-template consistency**: any new pattern in one template should be considered for backporting to siblings
- **Source of truth**: structured repo only; flat folder is frozen backup
- **`git add && git commit && git push`** after every material change
- **Bulk transforms via Python scripts** (preserved in `scripts/`) for traceability when affecting many templates

---

## How to resume in a new session

1. Open Claude Code in the project directory
2. Paste this handoff doc
3. Pick whichever pending phase matters next:
   - **JTL-honesty fixes** (H1–H4, mostly mechanical, ~10 edits across 7 templates)
   - **JTL admin verifications** (run test sends, check JTL settings) — unblocks 5+ items
   - **FAQ block wiring** (after providing the 3 placeholder confirmations)
   - **Image hosting setup** — unblocks logo PNG fallback + every `<img>` in every template
   - **Dark-mode CSS pass 2** — design palette already mapped
   - **Email-client QA dry-run** via `scripts/qa-send-all.py`

The new session will have full context to:
- Apply `COPY-RULES.md` automatically
- Use canonical blocks unchanged (support, footer, newsletter, tracker, Bankdaten)
- Match the 3-palette badge system
- Inherit hero patterns + tone overrides (`[noun] ist [state]`, formal-warm Manufaktur, no apology-bait, no "trotzdem" framing)
- Honor JTL realities (guest customers, plugin scope variability, no-fabricated-data principle)
- Push to GitHub after every commit
