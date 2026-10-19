"""Generate Week 6 presenter, visible-notes, and instructor-notes views."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / "index.qmd").read_text()

for name, visible in (("presenter.qmd", "false"), ("with-notes.qmd", "true")):
    deck = source.replace("filters: [strip-speaker-notes.lua]\n", "")
    deck = deck.replace("  revealjs:\n", f"  revealjs:\n    show-notes: {visible}\n", 1)
    (base / name).write_text(deck)

intro = '''---
title: "Week 6: Instructor Notes"
subtitle: "Association, Comparison, and the Target · COMM 5220"
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

The seminar begins by completing the Week 7 transition from forms of descriptive claim to appropriate descriptive tools. Junn and Masuoka show how comparison choices can reveal consequential associations. *Thinking Clearly with Data* supplies the formal logic of association, covariance, correlation, and comparison sets. Lundberg, Johnson, and Stewart then frame every reported quantity as an estimand that should be defined outside the model.

The deck reserves “association” for the broad idea that variables vary together and “correlation coefficient” or Pearson's *r* for the standardized measure of linear association. Descriptive and associational estimands remain central; causal effects appear as one possible family of estimands.

## Source conventions

Junn and Masuoka, TCD, and Lundberg sources are identified in the relevant slide notes. The interactive covariance display and nonlinear plots are original teaching graphics. Numerical teaching examples identify whether they are hypothetical or reconstructed from a source. Slide numbers include the automatic title slide.

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
