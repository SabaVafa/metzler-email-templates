#!/usr/bin/env python3
"""
Contact-data update (2026-05): correct general-hotline phone + opening hours
across all customer-facing templates.

OLD (placeholder during build):
  Phone display:  07121 / 317 91 14
  Phone tel href: +4971213179114
  Hours:          Montag - Freitag, 08:00 - 17:00 Uhr

NEW (verified Metzler "Allgemeine Hotline"):
  Phone display:  +49 (0) 7121 / 317 7310
  Phone tel href: +4971213177310
  Hours:          Mo-Fr.: 09:00-16:00 Uhr

Idempotent. Safe to re-run.

Leaves untouched:
  - contact-form-confirmation.html lines 250 / 258 — those are the separate
    contact-form-team phone/mobile lines (3478 2034 / 2035), distinct from
    the general hotline.

Run from repo root:  python scripts/contact-update-2026-05.py
"""

import os
import sys

TEMPLATE_DIR = "templates"

REPLACEMENTS = [
    # Phone tel href (E.164)
    ("tel:+4971213179114", "tel:+4971213177310"),

    # Phone display
    ("07121 / 317 91 14", "+49 (0) 7121 / 317 7310"),

    # Hours — en-dash entity variant
    (
        "Montag &ndash; Freitag, 08:00 &ndash; 17:00 Uhr",
        "Mo&ndash;Fr.: 09:00&ndash;16:00 Uhr",
    ),

    # Hours - raw en-dash variant
    (
        "Montag – Freitag, 08:00 – 17:00 Uhr",
        "Mo–Fr.: 09:00–16:00 Uhr",
    ),
]


def transform(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        original = f.read()
    new = original
    counts = {}
    for old, repl in REPLACEMENTS:
        n = new.count(old)
        if n:
            new = new.replace(old, repl)
            counts[old] = n
    if new == original:
        return None
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    return counts


def main():
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"error: {TEMPLATE_DIR}/ not found - run from repo root", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html"))
    total = {old: 0 for old, _ in REPLACEMENTS}
    touched = 0

    for name in files:
        path = os.path.join(TEMPLATE_DIR, name)
        counts = transform(path)
        if counts is None:
            print(f"  - {name}  (no change)")
            continue
        touched += 1
        summary = ", ".join(f"{c}x {k[:30]!r}" for k, c in counts.items())
        print(f"  [ok] {name}  -- {summary}")
        for k, c in counts.items():
            total[k] += c

    print()
    print(f"Files modified: {touched}/{len(files)}")
    for old, repl in REPLACEMENTS:
        short_old = old[:40] + ("..." if len(old) > 40 else "")
        short_new = repl[:40] + ("..." if len(repl) > 40 else "")
        print(f"  {total[old]:3d} x {short_old!r:48s} -> {short_new!r}")


if __name__ == "__main__":
    main()
