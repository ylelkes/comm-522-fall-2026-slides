"""Generate Week 9 presenter, visible-notes, and instructor-notes views."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / "index.qmd").read_text()

for name, visible in (("presenter.qmd", "false"), ("with-notes.qmd", "true")):
    deck = source.replace("filters: [add-transitions.lua, strip-speaker-notes.lua]\n", "filters: [add-transitions.lua]\n")
    deck = deck.replace("  revealjs:\n", f"  revealjs:\n    show-notes: {visible}\n", 1)
    (base / name).write_text(deck)

intro = '''---
title: "Week 9: Instructor Notes"
subtitle: "Sampling, Selection, and Scope · COMM 5220"
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

The seminar runs in four parts. **Part 1** opens with four cases in which credible evidence was stretched to a broader target: Opower's site selection, published versus government nudges, newspaper time sampling, and political tweets versus public opinion. **Part 2** builds a text sample link by link (population, frame, unit, selection, duplicates, time, censoring, probability designs, sample size, and the reliability subsample) using Bergstrom and West to make selection intuitive. **Part 3** introduces external validity, generalizability and transportability, Henrich, Heine, and Norenzayan's WEIRD critique, and Findley, Kikuta, and Denly's M-STOUT framework. **Part 4** turns the material into the students' sampling plan.

## Source conventions

Figures from Bergstrom and West, Findley, Kikuta, and Denly, and Henrich, Heine, and Norenzayan are identified in slide notes and copied from the assigned Week 9 PDFs. Coding-project examples and corpus counts are hypothetical unless a slide states otherwise. Slide numbers include the automatic title slide.

## Slide-by-slide notes

'''

parts = re.split(r"^## ", source, flags=re.M)[1:]

def slide_id(part):
    title = part.split("\n", 1)[0]
    explicit = re.search(r"\{#([^\s.}]+)", title)
    if explicit:
        return explicit.group(1)
    title = re.sub(r"\s+\{[^}]+\}$", "", title)
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

for index, part in enumerate(parts):
    number = index + 2
    title, body = part.split("\n", 1)
    title = re.sub(r"\s+\{[^}]+\}$", "", title)
    matches = re.findall(r"::: notes\n(.*?)\n:::", body, re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected one notes block: {title}; found {len(matches)}")
    next_title = None
    if index + 1 < len(parts):
        next_title = re.sub(r"\s+\{[^}]+\}$", "", parts[index + 1].split("\n", 1)[0])
    transition = f'**Transition:** next, {next_title}' if next_title else "**Close:** Pause for final questions and collect the exit response."
    intro += f"### Slide {number}: {title}\n\n{matches[0].strip()}\n\n{transition}\n\n"

(base / "instructor-notes.qmd").write_text(intro)
print(f"Synchronized notes for {len(parts)} teaching slides.")
