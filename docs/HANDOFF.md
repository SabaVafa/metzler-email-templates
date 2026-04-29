# Session Handoff — Metzler Email Templates

Paste this at the start of a new session, then say *"continue from this handoff under all listed rules"*.

---

## Where the project stands

**22 customer-facing templates done** — all 9 active JTL-native customer-facing slots covered, plus 5 custom templates for the brand journey, plus 8 supplementary (DOI, security, contact, etc.). All polished against the established copy rules (audited end-to-end, including a redundancy + banned-phrase pass).

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

### Files / structure

- **Repo**: GitHub `SabaVafa/metzler-email-templates` (private). Local at `C:\Users\s.vafakhah\Desktop\Purchase Confirmation Email\metzler-email-templates\`. **All edits go there, then `git add && git commit && git push`.** The flat root-level `.html` files are a frozen backup — **do not edit**.
- **`templates/`** — 22 `.html` files, image paths use `../assets/`
- **`assets/`** — `product-image.jpg`, `promotion/`, `reiniger/`, `video-thumbnail/`
- **`docs/`** — `README`, `COPY-RULES`, `PLACEHOLDERS`, `TRIGGERS`, `LEGAL`, `ASSETS`, `OPEN-ITEMS`
- **`index.html`** — clickable preview menu at root, all 22 cards present (numbering uses 03b/05b for sad-path variants)
- **Preview**: `npx serve -p 5200` from repo root → `http://localhost:5200/`
- **`gh` CLI** installed at `$LOCALAPPDATA/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`, authenticated as `SabaVafa`

### Single source of truth for copy

`docs/COPY-RULES.md` captures everything from the audit pass:
- Voice (formal Sie, premium-Manufaktur register)
- 14 banned phrases
- Translation tells with replacements
- Behördendeutsch / passive constructions to remove
- Hero stack rule (badge / title / CTA must vary)
- `[noun] ist [state]` hero pattern
- Canonical blocks (newsletter, support, tracker, footer)
- Tone-by-context overrides (delay, joy, security, cancellation, account)
- 10-point checklist for any new template

**All new templates must inherit `COPY-RULES.md` automatically.**

### Canonical blocks (identical across all 22 templates)

- **Support block**: *"Fragen zu Ihrer Bestellung? — Wir antworten Ihnen persönlich."* + phone `07121 / 317 91 14` + Mo–Fr 08:00–17:00 + E-Mail-Button
- **Newsletter block** (4 emails): *"Neues aus unserer Werkstatt"* heading + canonical body + *"Newsletter abonnieren"* CTA
- **Tracker labels** (7 emails): *Bestellung · Zahlung · Produktion · Versand · Lieferung*
- **Footer**: dark teal `#01292A` with all text at 50 % white opacity; legal links left-to-right (Impressum · Datenschutz · AGB · Widerrufsrecht · Batterieentsorgung · Elektroaltgeräte)

### Design system (frozen)

Colors `#015253` teal, `#01292A` footer, `#f2f4f2` page, `#f7f9f7` hero, `#ffffff` card. Type Montserrat headings + Helvetica Neue body. Card max-width 568 px with −40 px teal-band overlap. Mobile breakpoint `@media (max-width: 620px)`. MSO/VML fallbacks on all primary/outline buttons. HTML entities for umlauts in body, raw UTF-8 only in `<title>`.

---

## Next phase: plugin templates

JTL admin has a separate **Plug-in Templates** tab (distinct from system templates). Per screenshot of the Metzler shop, the plugin slots are:

| # | Plugin template | Active? |
|---|---|---|
| 1 | Bestandswarnung Benachrichtigung | ✓ active *(we covered the DOI side; this is the actual notify-when-back-in-stock fire — different template)* |
| 2 | Amazon Pay Soft-Decline | ✓ active |
| 3 | Amazon Pay Hard-Decline | ✓ active |
| 4 | Amazon Pay Info | ✓ active |
| 5 | Amazon Pay Abo Reminder | ✓ active |
| 6 | Amazon Pay Abo Start | ✓ active |
| 7 | Amazon Pay Abo Ende | ✓ active |
| 8 | Zahlungs-Erinnerungsemail | ✓ active |
| 9 | Rechnungskauf — Zahlungsinformationen | ✓ active |
| 10 | PayPal Zahlung abgelehnt | ✓ active |
| 11 | Abandoned Cart — Erste Erinnerung | ✓ active |
| 12 | Abandoned Cart — Zweite Erinnerung | ✓ active |
| 13 | Abandoned Cart — Letzte Erinnerung | ✓ active |
| 14 | General review confirmation mail template | ✗ inactive |

**13 of 14 are active and need brand-system templates.** Suggested order (by customer-impact):

1. **Abandoned Cart** trio (3 templates) — high-volume marketing, big revenue lever, must feel premium not pushy
2. **Payment-issue cluster** (5 templates) — Amazon Pay Soft/Hard-Decline, PayPal abgelehnt, Zahlungs-Erinnerung, Rechnungskauf — high anxiety potential, calm confident voice critical
3. **Amazon Pay Abo lifecycle** (3 templates: Reminder, Start, Ende) — subscription handling
4. **Amazon Pay Info** + **Bestandswarnung Benachrichtigung** (the actual fire, after DOI) (2 templates)
5. **General review confirmation** (inactive — skip unless activated)

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
3. Add: *"continue from this handoff under all listed rules. Start phase 2 — plugin templates. Begin with the Abandoned Cart trio (highest customer impact)."*

The new session will have full context to:
- Apply `COPY-RULES.md` automatically
- Use canonical blocks unchanged
- Match design system frozen tokens
- Inherit hero patterns + tone overrides
- Push to GitHub after every commit
