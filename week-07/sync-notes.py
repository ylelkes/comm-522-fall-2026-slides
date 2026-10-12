"""Generate Week 7 presenter, visible-notes, and instructor-notes views."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / "index.qmd").read_text()

for name, visible in (("presenter.qmd", "false"), ("with-notes.qmd", "true")):
    deck = source.replace("filters: [strip-speaker-notes.lua]\n", "")
    deck = deck.replace("  revealjs:\n", f"  revealjs:\n    show-notes: {visible}\n", 1)
    (base / name).write_text(deck)

intro = '''---
title: "Week 7: Instructor Notes"
subtitle: "Measurement and Description · COMM 5220"
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 3
    number-sections: false
    embed-resources: true
    css: notes.css
lang: en
---

[Open presenter slides](presenter.html) · [Open slides with visible notes](with-notes.html)

## Teaching approach

The seminar moves from conceptualizing and operationalizing media bias to evaluating Kim, Lelkes, and McCrain's visibility measure. It then uses Gerring to distinguish indicator, typological, and associational descriptive claims and Huntington-Klein to connect those claims to distributions, center, spread, and graphical description.

Kim's validation evidence appears immediately after the measure. The paper's substantive results return later as examples of descriptive association. Semetko and Valkenburg provide a content-coding example, while the simulated network figures separate a network pattern from its later ideological interpretation.

## Source conventions

Kim figures are identified in the slide notes. DIME Senate rankings use the 1979–2024 recipient file and are described as 2024 incumbent-coded records. Distribution and network figures are simulated teaching examples. Slide numbers include the automatic title slide.

## Slide-by-slide notes

'''

parts = re.split(r"^## ", source, flags=re.M)[1:]
for number, part in enumerate(parts, 2):
    title, body = part.split("\n", 1)
    title = re.sub(r"\s+\{[^}]+\}$", "", title)
    matches = re.findall(r"::: notes\n(.*?)\n:::", body, re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected one notes block: {title}; found {len(matches)}")
    intro += f"### Slide {number}: {title}\n\n{matches[0].strip()}\n\n"

(base / "instructor-notes.qmd").write_text(intro)
print(f"Synchronized notes for {len(parts)} teaching slides.")
