#!/usr/bin/env python3
"""
product-label-normalize.py  (idempotent)

Client decision: both sample product rows (the A200 doorbell AND the briefkasten)
use one placeholder label -> "Metzler Briefkasten aus hochwertigem Stahl | Siebert".
The bold product NAME block must show only that label; the inline bold descriptor
that hangs off it via <br /> ("Aufputz | IP54 | Beleuchtung weiss",
"Wandmontage | RAL 9016 weiss") is removed.

Does NOT touch:
- the grey product-sku / Art.-Nr. lines (kept)
- config-tables (Farbe/Schriftart/Namensschild)
- customer-question text that mentions "Modell A200" (no Edelstahl-Tuerklingel prefix)

Two regex passes, both idempotent:
  1. A200 name + optional inline <br/> descriptor -> label
  2. strip any inline <br/> descriptor still hanging off the briefkasten label
"""
import re, pathlib

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / "templates"
LABEL = "Metzler Briefkasten aus hochwertigem Stahl | Siebert"

# 1. Doorbell name (optionally followed by a bold <br/> descriptor) -> label
A200 = re.compile(r"Edelstahl-T&uuml;rklingel Modell A200(?:<br />[^<]*)?")
# 2. Briefkasten label still trailed by an inline <br/> descriptor -> label only
BK = re.compile(r"Metzler Briefkasten aus hochwertigem Stahl \| Siebert<br />[^<]*")

changed = []
for f in sorted(TEMPLATES.glob("*.html")):
    text = f.read_text(encoding="utf-8")
    new = A200.sub(LABEL, text)
    new = BK.sub(LABEL, new)
    if new != text:
        f.write_text(new, encoding="utf-8")
        changed.append(f.name)

print(f"normalized ({len(changed)}): {', '.join(changed) or '-'}")
