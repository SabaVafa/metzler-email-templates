#!/usr/bin/env python3
"""
QA send-all — fire every email template in templates/ to one or more test
inboxes via SMTP. For pre-launch visual QA across email clients.

Setup (once):
  1. Generate an app password from your email provider:
     - Gmail:    https://myaccount.google.com/apppasswords
     - Outlook:  https://account.microsoft.com/security -> Advanced security -> App passwords
     - GMX:      Webmail -> Einstellungen -> POP3/IMAP/SMTP-Zugriff

  2. Set environment variables (Linux/Mac: export …, Windows PowerShell: $env:…):
     SMTP_HOST=smtp.gmail.com
     SMTP_PORT=465
     SMTP_USER=your.address@gmail.com
     SMTP_PASS=your-app-password
     QA_FROM=your.address@gmail.com
     QA_TO=test1@gmail.com,test2@icloud.com,test3@gmx.de

Usage:
  python scripts/qa-send-all.py                  # sends all 28 templates
  python scripts/qa-send-all.py amazon-pay       # sends only matching files
  python scripts/qa-send-all.py --dry-run        # lists what would be sent

Caveats:
  - Image src paths are relative (../assets/…). Real clients will NOT load them.
    For full visual QA, upload assets/ to a public HTTPS host first
    (see docs/OPEN-ITEMS.md §5) and find/replace src paths.
  - Smarty placeholders ({$Bestellung->cBestellNr} etc.) render as literal
    text. Expected — JTL substitutes at production send time.
  - Free Gmail accounts have a ~100/day send limit. 28 templates × N recipients
    can exceed it; split runs across days or use multiple sender addresses.
"""

import os
import smtplib
import ssl
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

TEMPLATE_DIR = Path("templates")
RATE_LIMIT_SECONDS = 0.5  # be gentle to SMTP


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    filter_substr = next((a for a in argv[1:] if not a.startswith("--")), None)

    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "QA_FROM", "QA_TO"]
    if not dry_run:
        missing = [v for v in required if not os.environ.get(v)]
        if missing:
            print(f"ERROR: missing env vars: {', '.join(missing)}", file=sys.stderr)
            print("\nSee top of file for setup instructions.", file=sys.stderr)
            return 1

    if not TEMPLATE_DIR.is_dir():
        print(f"ERROR: '{TEMPLATE_DIR}' not found. Run from repo root.", file=sys.stderr)
        return 1

    files = sorted(TEMPLATE_DIR.glob("*.html"))
    if filter_substr:
        files = [p for p in files if filter_substr in p.name]
        print(f"Filter '{filter_substr}' -> {len(files)} template(s)\n")

    if not files:
        print("No templates matched. Nothing to do.")
        return 0

    if dry_run:
        print(f"DRY RUN -- would send {len(files)} template(s):\n")
        for p in files:
            print(f"  {p.name}")
        recipients = os.environ.get("QA_TO", "(QA_TO not set)")
        print(f"\nTo recipients: {recipients}")
        return 0

    sender = os.environ["QA_FROM"]
    recipients = [r.strip() for r in os.environ["QA_TO"].split(",") if r.strip()]
    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]
    pw = os.environ["SMTP_PASS"]

    total = len(files) * len(recipients)
    print(f"Sending {len(files)} template(s) × {len(recipients)} recipient(s) = {total} emails …\n")

    context = ssl.create_default_context()
    sent, failed = 0, 0

    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(user, pw)
        for path in files:
            html = path.read_text(encoding="utf-8")
            for to in recipients:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"[QA] {path.stem}"
                msg["From"] = sender
                msg["To"] = to
                msg.attach(MIMEText(html, "html", "utf-8"))
                try:
                    smtp.send_message(msg)
                    print(f"  [OK]   {path.stem:42s} -> {to}")
                    sent += 1
                except Exception as e:
                    print(f"  [FAIL] {path.stem:42s} -> {to} : {e}")
                    failed += 1
                time.sleep(RATE_LIMIT_SECONDS)

    print(f"\nDone. Sent: {sent}  Failed: {failed}")
    print("\nQA checklist for each test inbox:")
    print("  - Layout intact: no broken tables, no exploded buttons")
    print("  - Dark mode renders (toggle system theme, then refresh)")
    print("  - Touch targets feel right on a real phone (>= 44 px)")
    print("  - Footer contrast readable (low-contrast text was the audit's C1)")
    print("  - Smarty placeholders show as literal {$...} text (expected)")
    print("  - Images may not load (relative src) - re-test after asset hosting")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
