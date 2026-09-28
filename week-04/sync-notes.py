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
title: "Week 4: Instructor Notes"
subtitle: "From Concepts to Measures · COMM 5220"
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

Begin by recovering the class's Week 3 definition of social media, including its intension, extension, and borderline cases. Make the shift from platforms to person-period activity explicit. Keep a shared board record of the working definition and the evolving measurement specification.

Use whole-class discussion throughout. Notes include expected answers, concrete explanations, and transitions. There is no prescribed timing or timing validation. Slide numbers include the automatic title slide.

Paxton's suffrage analysis provides the empirical thread: definition, coding rule, changed dates, changed descriptions, and implications for explanation. Her recoding is a demonstration of the consequences of including women, not a complete new chronology of democracy. Social media use provides a parallel classroom design exercise. It remains broad use throughout; more specific activities are dimensions or explicitly narrower targets.

The sequence integrates Lauderdale's conceptual and causal distinctions with Toshkov's measurement material: dimensions, operationalization, evidence sources, and scales. Lauderdale's original Figures 2.1–2.3 each receive a dedicated slide with a walkthrough of the notation and arrows. Case design, sampling, levels of analysis, and broader descriptive methods are saved in deferred-toshkov-topics.md for a later week. Reliability, validity, and the formal analysis of measurement error also remain deferred. The four perils of quantification remain included, with fairness discussed at the conceptual and normative level.

## Source conventions

Printed page numbers refer to the supplied PDFs. Lauderdale references use the September 15, 2026 draft. Paxton is the 2000 article in *Studies in Comparative International Development*, pp. 92–111. Her Table 1 supplies the attributed suffrage comparison; her discussion on pp. 100–102 supplies the replotted wave counts. Original Figures 1–2 appear in full and in enlarged extracts. The school-completion table, its group means, and the 1910 welfare event are explicitly hypothetical teaching examples, not Paxton results. The source article documents additional historical coding qualifications in its notes.

All social media definitions, scenarios, and numerical examples are teaching constructions, not empirical findings or definitions attributed to the authors. The count chart reproduces reported results, not an independent reanalysis. Figures 2.1–2.3 are cropped directly from the assigned Lauderdale PDF, pp. 43–44. The use-distribution illustration is preserved with the deferred material, outside this presentation.

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
