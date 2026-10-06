#!/usr/bin/env python3
"""split_slides.py — split slides/scripting-101.pdf into one PDF per module.

Writes slides/modules/00_introduction.pdf and module1_slides.pdf … module8_slides.pdf.
Run it after rebuilding the deck (needs:  pip install pypdf).
"""
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
reader = PdfReader(str(ROOT / "slides" / "scripting-101.pdf"))
starts = {}
for i, page in enumerate(reader.pages):
    m = re.search(r"MODULE\s+(\d)\b", page.extract_text() or "")
    if m and int(m.group(1)) not in starts:
        starts[int(m.group(1))] = i
bounds = sorted(starts.items()) + [(99, len(reader.pages))]
ranges = {0: (0, bounds[0][1])} | {n: (s, bounds[k + 1][1]) for k, (n, s) in enumerate(bounds[:-1])}
out = ROOT / "slides" / "modules"
out.mkdir(exist_ok=True)
for n, (a, b) in ranges.items():
    w = PdfWriter()
    for p in range(a, b):
        w.add_page(reader.pages[p])
    name = "00_introduction.pdf" if n == 0 else f"module{n}_slides.pdf"
    with open(out / name, "wb") as fh:
        w.write(fh)
    print(f"{name}: slides {a + 1}-{b}")
