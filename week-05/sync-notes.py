"""Generate all notes views from the editable index.qmd; no timing metadata."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / "index.qmd").read_text()
for name, visible in (("presenter.qmd", "false"), ("with-notes.qmd", "true")):
    deck = source.replace("filters: [strip-speaker-notes.lua]\n", "")
    deck = deck.replace("  revealjs:\n", f"  revealjs:\n    show-notes: {visible}\n", 1)
    (base / name).write_text(deck)

intro = '''---
title: "Week 5: Instructor Notes"
subtitle: "Measurement Error, Reliability, and Fairness · COMM 5220"
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

The session opens by introducing the four perils of quantification and fairness in measurement at the conceptual level of Lauderdale ch. 1 (pp. 29–31) and ch. 4 §§4.1–4.2. It then introduces levels of measurement and builds the vocabulary of ch. 3: error by level, the common/unit-specific/noise decomposition, MSE, CTT reliability as an upper bound, the confusion matrix, benchmarks, correlated errors, intercoder reliability as consistency, and validity evidence.

Semetko and Valkenburg (2000) are used as an extended example of a content-analytic measurement procedure, not as a substantive reading. Burla et al. (2008) shows intercoder reliability used diagnostically. The session closes by returning to fairness formally with separation and sufficiency, using Lauderdale's COMPAS and A-level examples, and applying the same logic to Semetko and Valkenburg's cross-media comparison.

Social media use remains the running example from Week 4. Use whole-class discussion throughout. There is no prescribed timing. Slide numbers include the automatic title slide.

## Source conventions

Printed page numbers refer to the supplied PDFs. Lauderdale references use the September 15, 2026 draft. Figures 3.3, 4.1, and two rows of 4.2 are cropped directly from the assigned PDF (pp. 89, 105, 110). Semetko and Valkenburg's Table 1 is cropped from p. 100 of the article. The self-reported social media minutes, the kappa table, and the toxicity classifier are invented teaching examples and are labeled as such on the slides.

## Slide-by-slide notes

'''
parts = re.split(r"^## ", source, flags=re.M)[1:]
for number, part in enumerate(parts, 2):
    title, body = part.split("\n", 1)
    title = re.sub(r"\s+\{[^}]+\}$", "", title)
    matches = re.findall(r"::: notes\n(.*?)\n:::", body, re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected one notes block: {title}")
    intro += f"### Slide {number}: {title}\n\n{matches[0].strip()}\n\n"
(base / "instructor-notes.qmd").write_text(intro)
print(f"Synchronized notes for {len(parts)} teaching slides.")
