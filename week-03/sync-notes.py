"""Regenerate the notes-view deck and instructor guide from index.qmd.
Run this after editing slide content or speaker notes, then render with Quarto.
"""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / 'index.qmd').read_text()
(base / 'with-notes.qmd').write_text(source.replace('filters: [strip-speaker-notes.lua]\n', '').replace('  revealjs:\n', '  revealjs:\n    show-notes: true\n', 1))
(base / 'presenter.qmd').write_text(source.replace('filters: [strip-speaker-notes.lua]\n', '').replace('  revealjs:\n', '  revealjs:\n    show-notes: false\n', 1))
parts = re.split(r'^## ', source, flags=re.M)[1:]
entries = []
for number, part in enumerate(parts, 2):
    title, content = part.split('\n', 1)
    title = re.sub(r'\s+\{[^}]+\}$', '', title)
    match = re.search(r'::: notes\n(.*?)\n:::', content, re.S)
    if not match:
        raise ValueError(f'Missing notes: {title}')
    notes = match.group(1).strip()
    entries.append((number, title, notes))

intro = '''---
title: "Week 3: Instructor Notes"
subtitle: "Concepts and Conceptualization · COMM 5220"
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 2
    number-sections: false
    embed-resources: true
    css: notes.css
lang: en
---

[Open presentation](index.html) · [Open notes-view presentation](with-notes.html)

## Teaching plan

Slide numbers below include the title slide and match the presentation counter. Speaker notes supply explanations, anticipated answers, misconceptions, and transitions. The order runs from vocabulary through the criteria of a good concept, into the two readings' shared account of how a concept actually gets built, and finally into one continuous worked example (Molina et al.'s explication of "fake news") that enacts both frameworks together.

### Running examples

**Tolerance/the forum (carried over from Week 2):** Used throughout as the concept nobody explicated. Returns at the open (why this matters), in the "name the type" check, in the intension/extension tradeoff exercise, and again when choosing a minimal/maximal/cumulative strategy — deliberately the same case revisited under each new piece of vocabulary, rather than a new example per slide.

**Democracy (Gerring's own running example):** Used for the four elements of a concept (term/intension/indicator/extension), the intension/extension tradeoff, all six criteria's good/bad pairs, and the full minimal/maximal/cumulative strategies section (Tables 5.3–5.4). This is Gerring's own worked example throughout his chapter; the deck does not invent a substitute.

**Television viewing (McLeod & Pan's own running example):** Used for the mega-concept diagnosis, the seven weak everyday definitional approaches, and the dimensions/indicators ladder (Figure 2.1). Explicitly parallel to "fake news" later — flag this parallel aloud when introducing Molina et al., since students should notice the diagnosis is the same move run twice.

**"Fake news" (Molina, Sundar, Le & Lee 2019):** The extended second-half worked example. Real news and false news get the deep dive; satire and polarized/hyperpartisan content are faster contrast cases used specifically to demonstrate Gerring's differentiation criterion operating inside a live methods paper. The paper's own eight-category taxonomy is not covered exhaustively — misreporting, commentary, persuasive information, and citizen journalism are not part of this deck and should not be invented if a student asks; say the paper covers four more categories not discussed today.

### Board and discussion setup

Interactivity today is **whole-class only** — no pair or small-group work, a deliberate departure from Week 2's paired exercises. Keep a running board column for "criterion diagnosed" so that by the break, all six of Gerring's criteria are visible together as an accumulating checklist. After the break, keep a second column tracking "minimal / maximal / cumulative" so the Molina et al. real-news definition can be explicitly slotted into it when it arrives.

For every bad-example diagnosis slide, resist supplying the criterion's name before taking at least one or two student guesses — the pedagogical value is in the diagnosis, not the label. For the two post-break contrast cases (satire, polarized content), press for the specific indicator or dimension doing the differentiating work, not just "it feels different."

### Why this sequence

Concept vocabulary comes first in two parallel forms — McLeod & Pan's types-of-concepts and Gerring's term/intension/indicator/extension — taught side by side immediately, so students have both vocabularies before any criterion or process language is introduced. The intension/extension tradeoff follows immediately because it is reused twice: once to explain conceptual "stretching" under the Consistency criterion, and again to explain why tightening a scope condition works the way it does under Causal Utility.

The six criteria are taught in Gerring's own order (resonance, domain, consistency, fecundity, differentiation, causal utility) because each leans on the one before it: domain refines resonance's audience question; consistency is the intension/extension tradeoff named; fecundity and differentiation are explicitly "flip sides of the same coin" per Gerring; causal utility's minimal/maximal contrast is the direct setup for the entire post-break segment.

After the break, Gerring's Strategies of Conceptualization and McLeod & Pan's Chaffee steps are taught together, not sequentially, because they are answering the same question from two literatures — showing this convergence explicitly is more persuasive than teaching them as two unrelated frameworks. Molina et al. then enacts both frameworks at once on a single, current, live paper, which is the deck's real payoff: students should leave having watched an actual published methods paper make the same minimal/maximal choice, hit the same differentiation problem, and use the same survey-then-define logic that the readings describe in the abstract.

### Model distinctions carried from Week 2

**Explanandum vs. variable:** a concept can serve as either; today's criteria and processes apply to both, but causal utility specifically distinguishes what a *causal* variable needs (minimal, parsimonious) from what a *descriptive* target can afford (maximal, rich) — this is a direct extension of Hedström's variable-concept discussion from Week 2, not a new idea.

**Mega-concept vs. explicated concept:** "television," "fake news," and "tolerance" are all mega-concepts until dimensionalized. The diagnosis is identical each time: ask what several different, independently plausible things the label might mean, and notice that the original claim doesn't specify which one.

### Source conventions

Gerring page numbers refer to the assigned chapter's printed pagination (pp. 107–140). McLeod & Pan references use their chapter's own pagination. Molina et al. references use the journal's printed pagination. Broader framing, worked applications to "tolerance," and all whole-class prompts are identified in the relevant notes as instructor elaborations, not claims from the readings.

### Readings

- Gerring, John. 2012. "Concepts." In *Social Science Methodology: A Unified Framework*, 2nd ed., pp. 107–140. Cambridge University Press.
- McLeod, Jack M., and Zhongdang Pan. "Concept Explication and Theory Construction." Course handout chapter.
- Molina, Maria D., S. Shyam Sundar, Thai Le, and Dongwon Lee. 2021. "'Fake News' Is Not Simply False Information: A Concept Explication and Taxonomy of Online Content." *American Behavioral Scientist* 65(2): 180–212.

## Slide-by-slide discussion notes

'''
for number, title, notes in entries:
    intro += f'### Slide {number}: {title}\n\n{notes}\n\n'
(base / 'instructor-notes.qmd').write_text(intro)
print(f'Synchronized notes for {len(entries)} teaching slides.')
