# Copy Rules

The single source of truth for copywriting tone, banned phrases, and patterns across all Metzler email templates. Inherit everything below when writing new templates or editing existing ones.

---

## Voice & register

- **Formal Sie / Ihre / Ihnen** — capitalized, throughout
- **Premium artisan-Manufaktur register** — Manufactum/Breuninger zone, not Zalando-casual
- **Calm, confident, factual** — never marketing-flair, never SaaS-startup-y
- **Native German native-speaker voice** — no translation flavor, no anglicisms

---

## Banned phrases (hard rules)

| ❌ Banned | Reason |
|---|---|
| *"Vielen Dank für Ihre Geduld"* | cliché, defensive |
| *"Wir freuen uns, Sie als Kundin / Kunde…"* | corporate-marketing |
| *"Wir arbeiten hart daran"* | hollow promise |
| *"exklusiv für Sie"* | marketing-spam |
| *"Ihre ehrliche Meinung zählt"* | review-platform cliché |
| *"wir hoffen…"* | weak/uncertain |
| *"in der Regel"* | use *"meist"* instead |
| *"nichts weiter tun"* | dismissive of customer time |
| *"als wir ursprünglich geplant hatten"* | use *"als gedacht"* |
| *"Das ist X. Das ist Y."* | AI-parallelism |
| *"nicht nur X sondern Y"* | AI/marketing tic |
| *"Ihre ehrliche Meinung"* / *"Ihre Meinung zählt"* | banned-list adjacent |
| *"freiwillig & kostenlos"* | defensive, marketing-y |
| *"Jetzt anmelden"* (newsletter context) | false urgency push |

---

## Translation tells (systematically removed)

| ❌ Tell | ✅ Replacement / fix |
|---|---|
| `&` outside brand names | *"und"* (German style guides reject `&`) |
| *"hochwertig"* / *"high-quality"* | drop entirely (brand context implies quality) |
| *"in Echtzeit"* | *"jederzeit"* (less SaaS-y) |
| *"gültig für 60 Minuten"* | *"60 Minuten gültig"* / *"Der Link ist 60 Minuten gültig"* |
| *"Live verfolgen"* | *"Sendung verfolgen"* (anglicism) |
| *"Plus ein Dankeschön"* | drop *"plus"* — English construction |
| *"startklar"* | *"eingerichtet"* / *"bereit"* (tech-startup energy) |
| *"kostenlos"* on free items | drop or use *"als Dankeschön"* (marketing-promo flavor) |
| *"aus der Praxis"* | drop entirely (filler) |
| Stacking adjectives (*"harmonische, barrierefreie Optik"*) | split or simplify |
| Compound-noun stacks (*"Versandbestätigung mit Sendungsverfolgung"*) | split into clauses |

---

## Behördendeutsch / passive constructions removed

| ❌ Bureaucratic | ✅ Active replacement |
|---|---|
| *"Die Zustellung erfolgt"* | *"Voraussichtlich erreicht es Sie"* |
| *"liegt uns / Ihrem Team vor"* | *"Wir bearbeiten / Unser Team sieht sich … an"* |
| *"wird … geprüft / bearbeitet"* | *"wir prüfen / wir bearbeiten"* |
| *"werden erstattet"* | *"Sie erhalten … zurück"* |
| *"die Brillanz … zu schützen"* | *"so bleibt die Oberfläche brillant"* |
| *"einen Hinweis beilegen"* | *"vermerken Sie … auf der Rücksendung"* |
| *"Wir informieren Sie aktiv"* | *"Wir melden uns rechtzeitig"* |
| *"ist nicht mehr möglich"* | *"Sie können … nicht mehr"* |
| *"garantiert"* (marketing-promise) | *"sorgt für"* / *"bringt"* |

---

## Established patterns

### Hero stack rule

Badge + Title + CTA must NOT all repeat the same action verb. Vary register: badge confirms (status), title pivots to **gratitude** or **welcome**, CTA is the verb.

| Email | Badge | Title | CTA |
|---|---|---|---|
| payment-confirmation | *Zahlung erhalten* | *Vielen Dank für Ihre Zahlung.* | *Bestellung ansehen* |
| registration-verify | *E-Mail bestätigen* | *Willkommen bei Metzler.* | *E-Mail bestätigen* |
| review-confirmation | *Bewertung eingegangen* | *Vielen Dank für Ihre Bewertung.* | *(none)* |

### Hero title pattern (confirmation emails)

Use `[noun] ist [state]` across the journey:

- *"Ihre Bestellung ist eingegangen."*
- *"Ihre Zahlung ist eingegangen."*
- *"Ihr Paket ist angekommen."*
- *"Ihr Widerruf ist eingegangen."*
- *"Ihr Kundenkonto ist eingerichtet."*

### Customer-perspective active voice

Frame from the customer's point of view, not the system's:

- *"Sie erhalten 208,90 € zurück"* (not *"208,90 € werden erstattet"*)
- *"Wir prüfen Ihre Bewertung"* (not *"Ihre Bewertung wird geprüft"*)

### Drop admin preambles in security/confirmation emails

The customer just clicked *"Passwort vergessen"* / *"Registrieren"* / etc. — they know they did. Action-first phrasing is premium:

- ❌ *"Wir haben eine Anfrage zum Zurücksetzen erhalten"*
- ✅ *"Setzen Sie Ihr Passwort über den Button unten neu."*

### Drop redundant *"per E-Mail"* / *"dieser E-Mail"* inside emails

The customer is reading an email — the channel is implicit.

### Section labels (canonical phrases)

- *"Was passiert als nächstes?"* — universal next-steps section
- *"Aus der Werkstatt"* — workshop tips, recommendations
- *"Sie haben sich nicht angemeldet?"* / *"Sie haben keine Anfrage gestellt?"* — security-fallback in verification emails
- Section labels are plain, native, no English

---

## Canonical blocks (identical across emails)

### Newsletter block

Used in 4 emails: `order-confirmation`, `delivered`, `review-request`, `review-confirmation`.

> **Neues aus unserer Werkstatt**
> *Erfahren Sie als Erste von neuen Modellen, Sonderanfertigungen und Geschichten aus unserer Manufaktur in Reutlingen.*
>
> CTA: **Newsletter abonnieren**

### Support block

Identical across all 17 templates.

> **Fragen zu Ihrer Bestellung?**
> *Wir antworten Ihnen persönlich.*
>
> 07121 / 317 91 14
> Montag – Freitag, 08:00 – 17:00 Uhr
> [E-Mail schreiben]

### Tracker labels (5-step progress)

Used in 7 emails: `order-confirmation`, `payment-confirmation`, `production-guide`, `production-delay`, `invoice-delivery`, `track-trace`, `delivered`.

*Bestellung · Zahlung · Produktion · Versand · Lieferung*

(All nouns — no past participles. State communicated by color, not label.)

### Footer

- Background `#01292A` (dark teal)
- All text uniform at **50% white opacity** on dark teal
- Separator dots at 20% (decorative)
- No PDF/Acrobat helpdesk note

---

## Tone-by-context overrides

| Context | Adjustment |
|---|---|
| **Delay (in-house)** | Acknowledge calmly, reframe as quality (*"Qualitätsprozess"* OK). Give next-touchpoint promise. No apology-bait. Don't pile additional warnings. |
| **Carrier delay (third-party)** | No apology on Metzler's behalf — attribute clearly to DHL, give customer the link to check directly. |
| **Cancellation / Widerruf** | Neutral / respectful — don't celebrate, don't apologize. Active customer-perspective phrasing for refund. |
| **Account deletion** | Calm, calm, calm. Customer-perspective for what changed, warm welcome-back invitation. |
| **Joy moments (delivered, voucher)** | Concrete value-led titles where appropriate (*"10 % auf Ihre nächste Bestellung"*). |
| **Security emails (verify, reset)** | Action-first, no admin preamble. Always include security-fallback section: *"Sie haben sich nicht angemeldet?"* / *"Sie haben keine Anfrage gestellt?"* |

---

## Punctuation & typography

- **Em-dash `—`** for emphasis (in pairs or as a sentence break)
- **En-dash `–`** for ranges (between dates: *"17. – 19. Dez."* with spaces)
- **HTML entities** for umlauts in body (`&auml;`, `&ouml;`, `&uuml;`, `&szlig;`)
- **Raw UTF-8** only inside `<title>` tags
- **Hero titles end with period** (matches design system)
- **Section labels** do **not** end with period (they're labels, not sentences)
- ***"Sie / Ihre / Ihnen"*** always capitalized
- **No `&`** outside brand names — always *"und"*

---

## Quick checklist for new templates

1. ✅ Hero stack — does the title repeat the badge or CTA verb? If yes → vary
2. ✅ Banned phrases — none present?
3. ✅ Active voice from customer perspective?
4. ✅ Translation tells gone (`&`, *"hochwertig"*, *"Live"*, *"per E-Mail"* …)?
5. ✅ Section labels match the established phrases (*"Was passiert als nächstes?"*, etc.)?
6. ✅ Newsletter / Support / Footer use the canonical version?
7. ✅ Tracker labels (if used) are nouns, not past participles?
8. ✅ Punctuation: em-dash for emphasis, en-dash for ranges?
9. ✅ HTML entities for umlauts in body, raw UTF-8 in `<title>`?
10. ✅ Tone matches the context (delay vs joy vs cancellation vs security)?
