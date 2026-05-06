#!/usr/bin/env python3
"""
Width pass — bump card canvas from 568 → 640 px across all 28 templates.

Rationale: 3-col upsell grid + 5-step progress tracker were cramped at 568
(usable content width 512). Going to 640 (usable 584) gives ~+15% per
upsell card and ~+16% per tracker step while keeping body-copy line length
in the 80-char editorial sweet spot. Mobile breakpoint bumps 620 → 680
to keep the buffer between desktop card width and the mobile cutoff.

Idempotent — safe to re-run; only acts on exact attribute / CSS-rule
strings, never raw "568" substrings (which would corrupt SVG path data).

Run from repo root:  python scripts/width-pass-640.py
"""

import os
import sys

TEMPLATE_DIR = "templates"

REPLACEMENTS = [
    # Card + support-inner table widths (HTML attribute)
    ('width="568"', 'width="640"'),
    # Wrapper + bodyTable max-widths (CSS rule)
    ('max-width: 568px', 'max-width: 640px'),
    # Mobile breakpoint
    ('max-width: 620px', 'max-width: 680px'),
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
        print(f"error: {TEMPLATE_DIR}/ not found — run from repo root", file=sys.stderr)
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
        summary = ", ".join(f"{c}x {k!r}" for k, c in counts.items())
        print(f"  [ok] {name}  -- {summary}")
        for k, c in counts.items():
            total[k] += c

    print()
    print(f"Files modified: {touched}/{len(files)}")
    for old, repl in REPLACEMENTS:
        print(f"  {total[old]:3d} x {old!r:30s} -> {repl!r}")


if __name__ == "__main__":
    main()
