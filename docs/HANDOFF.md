# Session Handoff — Metzler Email Templates

Paste this at the start of a new session, then say *"continue from this handoff under all listed rules"*.

---

## ⚠️ Priority #1: Consistency

**Consistency across all templates is the single most important constraint.** It outranks individual-template polish, novelty, and personal preference. Every decision you make in a new template must be checked against the existing 22 templates first.

What this means in practice:

- **Reuse canonical blocks unchanged** — support block, footer, newsletter block, tracker labels. Never tweak them in one template only; if you have a reason to change, change them everywhere in a coordinated pass.
- **Reuse established phrasings** — *"Wir antworten Ihnen persönlich"*, *"Was passiert als nächstes?"*, *"Sie haben sich nicht angemeldet?"*, *"Tracking-Link"* (not *"Sendungsverfolgung"*), *"Lieferung"* (not *"Geliefert"*) — these are project standards. Inventing synonyms breaks the journey.
- **Reuse hero patterns** — `[noun] ist [state]` for confirmations, gratitude pivot for thank-yous, welcome-pivot for new-customer moments. Don't introduce a fourth pattern.
- **Reuse design tokens** — colors, type stack, spacing, button styles, mobile breakpoint. The design system is frozen. New templates inherit it; they don't propose new tokens.
- **Reuse section structures** — security-fallback section in confirmation/security emails, echo-back card in customer-message emails, meta card in transactional emails. Same patterns, same HTML structure.
- **Backport new patterns to siblings** — if a new template surfaces a better pattern (e.g., the *"Eine weitere Verwendung Ihrer E-Mail-Adresse findet nicht statt"* trust signal in `back-in-stock-doi`), check whether it should also apply to its siblings (`newsletter-activation`, `registration-verify`). Coordinate updates.
- **Audit cross-email when a small fix lands** — when fixing a banned phrase in one template, grep all 22 for the same phrase. We caught two of these in late audit passes (the *"ehrlichste"* in `review-confirmation` and `review-request`); both should have been caught earlier.
- **Consistency over polish on edge cases** — if a phrasing has been audited and accepted across the journey, don't re-litigate it in a new template just because something marginally better exists. The customer experiences all 22 emails as one cohesive voice; one outlier breaks the spell.

**The customer reads these emails as a single ongoing conversation with one brand.** Inconsistency makes the brand feel sloppy; consistency makes it feel quietly premium. When in doubt, match the existing pattern.

---

## Where the project stands

**28 templates shipped** — phase 1 (22 customer-facing) + phase 2 (6 plugin templates) both complete.

- **Phase 1 — 22 customer-facing**: all 9 active JTL-native customer-facing slots covered, plus 5 custom templates for the brand journey, plus 8 supplementary (DOI, security, contact, etc.). All polished against the established copy rules (audited end-to-end, including a redundancy + banned-phrase pass).
- **Phase 2 — 6 plugin templates**: Amazon Pay Soft-Decline / Hard-Decline / Info (staff alert) · Zahlungs-Erinnerung · Zahlungsinformationen Vorkasse · PayPal Zahlung abgelehnt. Cluster-consistent design tokens (amber for payment-attention, red for staff alerts, green for confirmations), shared Bankdaten card across order-confirmation + zahlungs-erinnerung + zahlungsinformationen-vorkasse, mailto-deep-link CTAs for Hard-Decline + PayPal, formal-warm Manufaktur subtitles (*"Gern vereinbaren wir mit Ihnen … — Ihre Bestellung halten wir bis dahin für Sie bereit"*).

### Templates inventory

**Transactional journey (12)**
1. `order-confirmation` — §312f order confirmation, Vorkasse, tracker step 1
2. `payment-confirmation` — Vorkasse received, tracker step 2
3. `production-guide` — T+2 mid-journey, Änderungen-Deadline, tracker step 3
4. `production-delay` — sad-path variant of #3
5. `invoice-delivery` — shipped + §14 UStG invoice PDF, tracker step 4
6. `track-trace` — DHL out-for-delivery, tracker step 5
7. `track-trace-delay` — sad-path variant of #6
8. `delivered` — arrived, tracker complete
9. `review-request` — T+3 invite + Dankeschön Reiniger
10. `review-confirmation` — review submitted + Reiniger shipping
11. `gutschein` — 10 % voucher DANKE10
12. `widerrufsbestaetigung` — cancellation confirmed (non-custom only)

**Ancillary & account (10)**
13. `product-question-confirmation` — product Q submitted
14. `password-reset` — reset password
15. `registration-verify` — signup email verification
16. `registration-welcome` — post-verification welcome
17. `account-deletion` — DSGVO Art. 17 deletion complete
18. `newsletter-activation` — newsletter DOI confirmation
19. `back-in-stock-doi` — back-in-stock notify DOI confirmation
20. `contact-form-confirmation` — general "Kontakt" form
21. `account-created-by-admin` — admin-created account (B2B, phone orders)
22. `customer-group-assignment` — customer moved to new group

**Plug-in templates (6) — phase 2**
P1. `amazon-pay-soft-decline` — temporary Amazon Pay auth failure → Amazon-Pay-Übersicht retry
P2. `amazon-pay-hard-decline` — permanent Amazon Pay refusal → mailto support for alternative
P3. `amazon-pay-info` — internal staff alert (red badge, JTL-Backend + Seller Central two-button row, *not* customer-facing)
P4. `zahlungs-erinnerung` — Vorkasse payment reminder, "Jetzt bezahlen" CTA + Bankdaten card
P5. `zahlungsinformationen-vorkasse` — first informational delivery of bank details (slot is JTL-labeled "Rechnungskauf" but Metzler uses for Vorkasse)
P6. `paypal-zahlung-abgelehnt` — PayPal refused → mailto support for alternative (sibling of P2)

### Files / structure

- **Repo**: GitHub `SabaVafa/metzler-email-templates` (private). Local at `C:\Users\s.vafakhah\Desktop\Purchase Confirmation Email\metzler-email-templates\`. **All edits go there, then `git add && git commit && git push`.** The flat root-level `.html` files are a frozen backup — **do not edit**.
- **`templates/`** — 22 `.html` files, image paths use `../assets/`
- **`assets/`** — `product-image.jpg`, `promotion/`, `reiniger/`, `video-thumbnail/`
- **`docs/`** — `README`, `COPY-RULES`, `PLACEHOLDERS`, `TRIGGERS`, `LEGAL`, `ASSETS`, `OPEN-ITEMS`
- **`index.html`** — clickable preview menu at root, all 22 cards present (numbering uses 03b/05b for sad-path variants)
- **Preview**: `npx serve -p 5200` from repo root → `http://localhost:5200/`
- **`gh` CLI** installed at `$LOCALAPPDATA/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`, authenticated as `SabaVafa`

### Single source of truth for copy

`docs/COPY-RULES.md` is the canonical document. Read it before designing or editing any template. The most important rules — inlined here so this handoff stands alone:

#### Voice & register
- **Formal Sie / Ihre / Ihnen** — capitalized, throughout
- **Premium artisan-Manufaktur** zone (Manufactum / Breuninger), not Zalando-casual
- **Calm, confident, factual** — never marketing-flair, never SaaS-startup-y
- **Native German** — no translation flavor, no anglicisms

#### Banned phrases (hard rules — never use)
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
12. *"Ihre Meinung zählt"* (banned-list adjacent)
13. *"freiwillig & kostenlos"*
14. *"Jetzt anmelden"* (newsletter context — use *"Newsletter abonnieren"*)

#### Translation tells to remove
- `&` outside brand names → *"und"*
- *"hochwertig"* / *"high-quality"* → drop entirely (brand context implies quality)
- *"in Echtzeit"* → *"jederzeit"*
- *"gültig für 60 Minuten"* → *"60 Minuten gültig"*
- *"Live verfolgen"* → *"Sendung verfolgen"*
- *"Plus ein Dankeschön"* → drop *"plus"*
- *"startklar"* → *"eingerichtet"* / *"bereit"*
- *"kostenlos"* on free items → *"als Dankeschön"* or drop
- *"aus der Praxis"* → drop entirely (filler)
- Stacking adjectives → split or simplify
- Compound-noun stacks → split into clauses
- *"per E-Mail"* / *"dieser E-Mail"* inside an email → drop (channel is implicit)

#### Behördendeutsch / passive → active replacements
- *"Die Zustellung erfolgt"* → *"Voraussichtlich erreicht es Sie"*
- *"liegt uns / Ihrem Team vor"* → *"Wir bearbeiten / Unser Team sieht sich … an"*
- *"wird … geprüft / bearbeitet"* → *"wir prüfen / wir bearbeiten"*
- *"werden erstattet"* → *"Sie erhalten … zurück"*
- *"einen Hinweis beilegen"* → *"vermerken Sie … auf …"*
- *"Wir informieren Sie aktiv"* → *"Wir melden uns rechtzeitig"*
- *"ist nicht mehr möglich"* → *"Sie können … nicht mehr"*
- *"garantiert"* → *"sorgt für"* / *"bringt"*

#### Hero stack rule
Badge + Title + CTA must NOT all repeat the same action verb. Vary register: badge confirms, title pivots to gratitude or welcome, CTA is the verb. *Examples in COPY-RULES.md.*

#### Hero title pattern (confirmation emails)
`[noun] ist [state]`:
- *"Ihre Bestellung ist eingegangen."*
- *"Ihre Zahlung ist eingegangen."*
- *"Ihr Paket ist angekommen."*
- *"Ihr Widerruf ist eingegangen."*
- *"Ihr Kundenkonto ist eingerichtet."*

#### Customer-perspective active voice
Frame from customer's POV, not the system's:
- *"Sie erhalten 208,90 € zurück"* (not *"208,90 € werden erstattet"*)
- *"Wir prüfen Ihre Bewertung"* (not *"Ihre Bewertung wird geprüft"*)

#### Drop admin preambles in security/confirmation emails
The customer just clicked the action — they know they did. Action-first.
- ❌ *"Wir haben eine Anfrage zum Zurücksetzen erhalten"*
- ✅ *"Setzen Sie Ihr Passwort über den Button unten neu."*

#### Tone-by-context overrides
- **Delay (in-house)** — calm, reframe as quality, give next-touchpoint promise, no apology-bait
- **Carrier delay (DHL)** — no apology on Metzler's behalf, attribute to carrier, link to their tracking
- **Cancellation / Widerruf** — neutral, respectful, active voice for refund (*"Sie erhalten X zurück"*)
- **Account deletion** — calm, customer-perspective for what changed, warm welcome-back invitation
- **Joy moments** — concrete value-led titles where appropriate
- **Security emails (verify, reset)** — action-first, no admin preamble, always include security-fallback section *"Sie haben sich nicht angemeldet?"* / *"Sie haben keine Anfrage gestellt?"*
- **Admin-initiated lifecycle (account-by-admin, group-assignment)** — anchor brand explicitly, security-fallback uses *"melden Sie sich"* (active path, not *"ignorieren Sie"*)

#### Punctuation & typography
- Em-dash `—` for emphasis, en-dash `–` for ranges (*"17. – 19. Dez."*)
- HTML entities for umlauts in body, raw UTF-8 only in `<title>`
- Hero titles end with period; section labels don't
- **No `&`** outside brand names — always *"und"*

#### Anti-redundancy rule
At most **two** "we'll get back to you / contact us" beats per email:
- Unique-purpose section (e.g., security fallback, *"Bei Transportschäden melden Sie sich"*)
- Canonical support block at the bottom

If the team-note above the support block also says *"Bei Fragen sind wir … für Sie da"*, that's a third redundant beat — **trim it**.

#### 10-point checklist for new templates
1. Hero stack — title doesn't repeat badge or CTA verb?
2. Banned phrases — none present?
3. Active voice from customer perspective?
4. Translation tells gone (`&`, *"hochwertig"*, *"Live"*, *"per E-Mail"* …)?
5. Section labels match established phrases (*"Was passiert als nächstes?"*, etc.)?
6. Newsletter / Support / Footer use the canonical version?
7. Tracker labels (if used) are nouns, not past participles?
8. Punctuation: em-dash for emphasis, en-dash for ranges?
9. HTML entities for umlauts in body, raw UTF-8 in `<title>`?
10. Tone matches the context (delay vs joy vs cancellation vs security)?

**All new templates must inherit `docs/COPY-RULES.md` automatically.**

### Canonical blocks (identical across all 22 templates)

- **Support block**: *"Fragen zu Ihrer Bestellung? — Wir antworten Ihnen persönlich."* + phone `07121 / 317 91 14` + Mo–Fr 08:00–17:00 + E-Mail-Button
- **Newsletter block** (4 emails): *"Neues aus unserer Werkstatt"* heading + canonical body + *"Newsletter abonnieren"* CTA
- **Tracker labels** (7 emails): *Bestellung · Zahlung · Produktion · Versand · Lieferung*
- **Footer**: dark teal `#01292A` with all text at 50 % white opacity; legal links left-to-right (Impressum · Datenschutz · AGB · Widerrufsrecht · Batterieentsorgung · Elektroaltgeräte)

### Design system (frozen)

Colors `#015253` teal, `#01292A` footer, `#f2f4f2` page, `#f7f9f7` hero, `#ffffff` card. Type Montserrat headings + Helvetica Neue body. Card max-width 568 px with −40 px teal-band overlap. Mobile breakpoint `@media (max-width: 620px)`. MSO/VML fallbacks on all primary/outline buttons. HTML entities for umlauts in body, raw UTF-8 only in `<title>`.

---

## Phase 2: plugin templates — DONE

The user-selected scope for phase 2 was the **payment-issue cluster** (6 templates). Shipped as commits 1eb498a → ef6944e on `main`. Full plugin slot list with current status:

| # | Plugin template | Active? | Status |
|---|---|---|---|
| 1 | Bestandswarnung Benachrichtigung | ✓ active | *not in scope this round* |
| 2 | Amazon Pay Soft-Decline | ✓ active | ✅ shipped (P1) |
| 3 | Amazon Pay Hard-Decline | ✓ active | ✅ shipped (P2) |
| 4 | Amazon Pay Info | ✓ active | ✅ shipped (P3 — staff alert) |
| 5 | Amazon Pay Abo Reminder | ✓ active | *not in scope* |
| 6 | Amazon Pay Abo Start | ✓ active | *not in scope* |
| 7 | Amazon Pay Abo Ende | ✓ active | *not in scope* |
| 8 | Zahlungs-Erinnerungsemail | ✓ active | ✅ shipped (P4) |
| 9 | Rechnungskauf — Zahlungsinformationen | ✓ active | ✅ shipped (P5 — Metzler uses this slot for Vorkasse-Zahlungsinformationen, file named `zahlungsinformationen-vorkasse.html`) |
| 10 | PayPal Zahlung abgelehnt | ✓ active | ✅ shipped (P6) |
| 11 | Abandoned Cart — Erste Erinnerung | ✓ active | *not in scope* |
| 12 | Abandoned Cart — Zweite Erinnerung | ✓ active | *not in scope* |
| 13 | Abandoned Cart — Letzte Erinnerung | ✓ active | *not in scope* |
| 14 | General review confirmation mail template | ✗ inactive | *skip unless activated* |

### Future phases (when ready)

7 plugin slots remain unstarted. Suggested order (by customer-impact):

1. **Abandoned Cart** trio (3 templates) — high-volume marketing, big revenue lever, must feel premium not pushy
2. **Amazon Pay Abo lifecycle** (3 templates: Reminder, Start, Ende) — subscription handling
3. **Bestandswarnung Benachrichtigung** — the actual back-in-stock fire (after DOI)

### Phase 2 design decisions worth preserving

- **Three-palette badge system** — green (`#eaf3ea` / `#2d6e2d`) for confirmation/informational, amber (`#fdf3e3` / `#8a5a00`) for payment-attention, red (`#fde8e8` / `#a91e1e`) for internal staff alerts. Do not introduce additional palettes without explicit reason.
- **Bankdaten card structure** identical across `order-confirmation`, `zahlungs-erinnerung`, `zahlungsinformationen-vorkasse`. Title *"Vorkasse — Überweisung"*, active-voice subtitle, row order Empfänger / IBAN / BIC / Bank / Betrag, ref-hint *"Bitte exakt so angeben — ohne weitere Zusätze."* Real bank data: Volksbank Ermstal-Alb eG · DE09 6439 1200 0308 5077 00 · GENODES1MTZ.
- **Mailto deep-link pattern** for Hard-Decline + PayPal: pre-filled subject *"Andere Zahlungsart für Bestellung #{Bestellnr}"*. Routes to `info@edelstahl-tuerklingel.de`.
- **Formal-warm Manufaktur subtitle** for payment-failure context: *"Gern vereinbaren wir mit Ihnen eine andere Zahlungsart — Ihre Bestellung halten wir bis dahin für Sie bereit."* Replaces earlier draft's *"Damit wir Ihre Bestellung trotzdem fertigen können"* (was off-tone — *"trotzdem"* drew attention to failure, *"Damit wir können"* was self-focused).
- **Step 2 alternatives** for PayPal-decline: *"Vorkasse, SEPA-Lastschrift oder Kreditkarte"* (not *"Vorkasse, Rechnungskauf oder PayPal"* — PayPal can't be the alternative when PayPal is what just failed).
- **No personalized greeting** — none of the 28 templates open with *"Guten Tag {$Kunde->...}"*. Cluster convention is to open with the action.
- **Conditional `{if isset($Bestellung->Positionen)}` wrap** as a DEV-comment hint around the item-loop section in plugin templates, since some plugin Smarty scopes may not expose Positionen.

---

## Pending items still on `docs/OPEN-ITEMS.md`

1. ⚠ **Street address**: footers say *"Tübingerstraße 9"*, Datenschutzerklärung says *"Täleswiesenstr. 9"* — client to confirm
2. **HRB + USt-IdNr.** placeholder values still `XXXXX` / `DE XXX XXX XXX`
3. **URL slugs** to verify (`/batterieentsorgungsgesetz`, `/elektroaltgeraeteentsorgung`)
4. **Logo PNG fallback** for Outlook desktop — user has the white-wordmark PNG, needs to save it to `assets/logo-white.png`. Then I wire 34 fallback wrappings (header + footer × 22 templates).
5. **Image hosting** — upload `assets/` to a public HTTPS host, find/replace `../assets/` → absolute URL (see `docs/ASSETS.md`)
6. **Newsletter DOI flow** wiring in JTL backend
7. **Header / Footer JTL shared partials** — optional Path-B refactor (extract from individual templates)
8. **Compatibility testing** — Litmus / Email on Acid pass before launch

---

## Working agreement (from collaboration rules)

- **Always propose before editing** — show the structural blueprint + every copy decision in a confirmation step before writing/changing HTML
- **No inline body-text icons**
- **No banned phrases** (see `COPY-RULES.md`)
- **Cross-template consistency**: any new pattern that emerges in a template should be considered for backporting to siblings
- **Source of truth**: structured repo only; flat folder is frozen backup
- **`git add && git commit && git push`** after every material change

---

## How to resume in a new session

1. Open Claude Code in the project directory
2. Paste this handoff doc into the first message
3. Pick whichever pending phase is next:
   - **Abandoned Cart trio** (3 templates) — highest revenue lever
   - **Amazon Pay Abo lifecycle** (3 templates) — subscription handling
   - **Bestandswarnung Benachrichtigung** — the actual back-in-stock fire

Add: *"continue from this handoff under all listed rules. Start the [chosen phase]."*

The new session will have full context to:
- Apply `COPY-RULES.md` automatically
- Use canonical blocks unchanged (support, footer, newsletter, tracker)
- Match design system frozen tokens (3-palette badge, Bankdaten card structure, mailto deep-link pattern)
- Inherit hero patterns + tone overrides (`[noun] ist [state]`, formal-warm Manufaktur, no apology-bait, no "trotzdem" framing)
- Push to GitHub after every commit
