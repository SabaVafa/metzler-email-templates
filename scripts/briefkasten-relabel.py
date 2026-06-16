#!/usr/bin/env python3
"""
briefkasten-relabel.py  (idempotent)

Content fix: the sample briefkasten was labelled "Edelstahl-Briefkasten Modell B350",
which contradicts the content briefing -- briefkasten bodies are powder-coated steel
(only the engraving plates are stainless), so "Edelstahl" must not be claimed here.
It was also internally inconsistent with the "RAL 9016 weiss" powder-coat finish.

Replaces the product NAME with the client-supplied placeholder. Subtitles
(Wandmontage, RAL 9016 weiss, Art.-Nr.) are left untouched -- now consistent.

Re-runnable: only touches files still containing the old name.
"""
import pathlib

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / "templates"
OLD = "Edelstahl-Briefkasten Modell B350"
NEW = "Metzler Briefkasten aus hochwertigem Stahl | Siebert"

changed = []
for f in sorted(TEMPLATES.glob("*.html")):
    text = f.read_text(encoding="utf-8")
    if OLD not in text:
        continue
    n = text.count(OLD)
    f.write_text(text.replace(OLD, NEW), encoding="utf-8")
    changed.append(f"{f.name} ({n})")

print(f"relabelled ({len(changed)}): {', '.join(changed) or '-'}")
