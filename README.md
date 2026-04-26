# Metzler Email Templates

17 transactional and account email templates for **edelstahl-tuerklingel.de** (JTL-Shop 5).
Built for Metzler GmbH — premium custom-engraved stainless steel doorbells & mailboxes.

---

## Quick start (local preview)

```bash
npx serve -p 5200
```

Then open <http://localhost:5200/> — the index page lists all 17 emails as clickable cards.

> Requires Node.js. No install step; `npx` fetches `serve` on demand.

---

## Folder structure

```
metzler-email-templates/
├── templates/        17 .html email files
├── assets/           images referenced by templates (relative paths)
│   ├── promotion/
│   ├── reiniger/
│   └── video-thumbnail/
├── docs/             handoff documentation (read these)
├── index.html        preview menu (auto-served at /)
└── package.json      npm run preview shortcut
```

---

## Documentation — read in this order

| Doc | What's inside |
|---|---|
| [`docs/PLACEHOLDERS.md`](docs/PLACEHOLDERS.md) | Every `{$smartyVar}` used across the templates, with type + example value |
| [`docs/TRIGGERS.md`](docs/TRIGGERS.md) | Which JTL trigger fires which template + conditional rules (custom vs. non-custom, opt-in gates) |
| [`docs/LEGAL.md`](docs/LEGAL.md) | PDF attachments, §312f / §356a / §357 BGB, §14 UStG, DSGVO opt-ins, retention |
| [`docs/ASSETS.md`](docs/ASSETS.md) | Every image referenced, grouped by template — your find/replace checklist for production CDN |
| [`docs/OPEN-ITEMS.md`](docs/OPEN-ITEMS.md) | Pending items requiring decisions (street address, HRB, opt-in flow, etc.) |

---

## Production deployment — one critical step

The `<img>` paths are currently **relative** (`../assets/...`) so the templates preview locally.
Before going live, replace every relative `src="../assets/..."` with an **absolute HTTPS URL**
on a public host (e.g. `https://edelstahl-tuerklingel.de/email-assets/...`).
Email clients cannot fetch images from the sender's local filesystem.

See [`docs/ASSETS.md`](docs/ASSETS.md) for the complete list.

---

## Design system (frozen)

- **Colors**: primary teal `#015253` · dark band `#01292A` · page `#f2f4f2` · card `#ffffff` · body `#555` · primary text `#1a1a1a` · muted `#767676`
- **Type**: Montserrat (headings, buttons) · Helvetica Neue stack (body) · 24/16/14/13/12 px
- **Card**: max-width 568 px · -40 px teal-band overlap · 6 px radius
- **Mobile breakpoint**: `@media (max-width: 620px)`
- **Outlook**: VML fallbacks on every primary/outline button
- **Umlauts**: HTML entities in body, raw UTF-8 only inside `<title>`
- **Dark mode**: palette defined but **disabled on every email** (forced light mode); restorable from git history

---

## Tone rules (hard-enforced — keep when editing)

- Formal **Sie / Ihre / Ihnen**, capitalized; native-German register
- Section-label standard: **"Was passiert als nächstes?"**
- Hero-title pattern: **"Ihre/Ihr [X] ist/wurde …"**
- No inline icons inside body text (standalone pills OK)
- No step counts ("5-Schritt …")
- No apology for third-party (DHL, carrier) delays
- No mock strikethrough on delay dates (looks like discount)

---

## Contact

Saba Vafakhah · <s.vafakhah@metzlergmbh.de>
