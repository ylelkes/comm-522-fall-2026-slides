"""Regenerate the notes-view deck and instructor guide from index.qmd.
Run this after editing slide content or speaker notes, then render with Quarto.
"""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base / 'index.qmd').read_text()
(base / 'with-notes.qmd').write_text(source.replace('  revealjs:\n', '  revealjs:\n    show-notes: true\n', 1))
parts = re.split(r'^## ', source, flags=re.M)[1:]
entries = []
for number, part in enumerate(parts, 2):
    title, content = part.split('\n', 1)
    title = re.sub(r'\s+\{[^}]+\}$', '', title)
    match = re.search(r'::: notes\n(.*?)\n:::', content, re.S)
    if not match:
        raise ValueError(f'Missing notes: {title}')
    notes = match.group(1).strip()
    timing = re.search(r'Timing: (\d+) minutes\. Elapsed: (\d+)–(\d+) minutes\.', notes)
    if not timing:
        raise ValueError(f'Missing timing: {title}')
    entries.append((number, title, notes, tuple(map(int, timing.groups()))))
elapsed = 0
for number, title, notes, (duration, start, end) in entries:
    assert start == elapsed and end == start + duration, f'Noncontiguous timing: {title}'
    elapsed = end
assert elapsed == 120

def segment(first, last, label):
    selected = [e for e in entries if first <= e[0] <= last]
    slide_range = str(first) if first == last else f'{first}–{last}'
    return f'| {selected[0][3][1]}–{selected[-1][3][2]} minutes | {label} | {slide_range} |'

schedule = '\n'.join([
    segment(1, 10, 'Workshop vocabulary, explanatory targets, states, and events'),
    segment(11, 18, 'Compare explanatory strategies: laws, probabilities, and criticisms'),
    segment(19, 26, 'Statistical accounts, causal claims, and prediction'),
    segment(27, 34, 'Test rival hypotheses: Semmelweis together, then the forum'),
    segment(35, 35, 'Break'),
    segment(36, 42, 'Mechanisms: components, tendencies, causal descriptions, and stopping points'),
    segment(43, 47, 'Necessitation, functional explanation, just-so stories, and synthesis'),
    segment(48, 51, 'Classification, construction, discussion, and exit'),
])

intro = '''---
title: "Week 2: Instructor Notes"
subtitle: "Laws, Patterns, and Mechanisms · COMM 5220"
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

The seminar lasts **120 minutes, including a five-minute break**. The title slide shares the opening segment's time. Slide numbers below include the title slide and match the presentation counter. Speaker notes supply explanations, anticipated answers, misconceptions, and transitions. The activities fit within the listed timings. The order follows the explanatory task rather than the order of the readings: establish the target, compare accounts, test rivals, investigate processes, and judge adequacy.

| Elapsed time | Segment | Presentation slides |
|---|---|---|
SCHEDULE_TABLE

### Running examples

**Deliberative forum:** A hypothetical continuation of Week 1. Tolerance means extending political rights to a disliked opponent, not agreeing with that opponent. Keep this outcome stable unless explicitly changing the target. The recurring accounts are belief revision, public compliance, and selective departure. No forum findings or numerical examples are claims about a real study.

**Semmelweis:** Students have read Hempel, so reconstruct his reasoning together in plenary. Use the board columns hypothesis, auxiliary assumptions, expected observation, actual observation, and inference. This is a shared worked example rather than a new reading or pair assignment. Its primary teaching role is the hypothetico-deductive method. A dedicated comparison revisits it through DN explanation, probabilistic explanation, and HD testing. The lesson distinguishes a hypothesis’s origin, its test consequences, and its revision in response to new evidence.

**Turnout:** Elster's conceptual example separates explaining the generation of participation from explaining a weather-related difference. His Figure 1.1 is a schematic, not an estimated relationship.

### Shared example, then independent practice

Introduce Elster’s Figure 1.2 at minutes 49–51. At minutes 51–55, students consult the handout and build the Semmelweis hypothesis map together, covering all the rival accounts. Reveal the completed comparison at minutes 55–56; consolidate HD testing, evidence and revision, and explanatory form at minutes 56–59. Use the notes as an answer key after students have reasoned through the branches, not as a script to give them the answers first. Groups work at minutes 59–63 and report at minutes 63–66, immediately before the break.

Fix the forum target as higher tolerance among closing-survey respondents than among opening-survey respondents. Assign genuine attitude change, public compliance, and selection across groups. Each group must specify its hypothesis and assumptions, derive an additional observable implication, compare a rival prediction, and identify a result that would weaken its account. Selection here concerns attrition or nonresponse, not simply who initially attends.

The earlier statistical section uses an attendee/nonattendee contrast. Explicitly return to the opening/closing respondent comparison for this exercise. Students can build on the measurement and composition issues they have already discussed, but must now specify hypotheses, assumptions, and contrasting predictions. Keep the completed answer matrix in the debrief until groups have proposed their tests. After the break, revisit these hypotheses to introduce mechanisms; return to the matrices again in the final workshop.

### Board and discussion setup

Keep **WHAT HAPPENED?**, **WHY?**, and **HOW WOULD WE KNOW?** on the board (target, account, and evidence). Ask students to locate each new claim under the appropriate heading. Retain one descriptive forum target and at least two rival accounts throughout. Students should leave each application with a written claim or proposed discriminating observation.

Use pairs for short applications and groups of three or four for the final workshop. During debriefs, request one claim, one reason, and one unresolved inference. Accept multiple classifications when students justify them.

### Why this sequence

Begin with the workshop vocabulary, description, and turnout. Immediately follow turnout with the four state/event forms, Elster’s event preference, and the absence/decision contrast. This groups the questions about explanatory targets and forms before comparing explanatory strategies. Keep deductive and probabilistic covering-law models together, each with its criticisms; follow them immediately with statistical accounts so the two meanings of probabilistic/statistical explanation can be compared directly.

Prediction leads into the question of how to test rivals. Introduce Elster’s testing figure, let students reconstruct Semmelweis and its rival accounts, consolidate the hypothetico-deductive method, and transfer it to the forum before the break. This is a testing method, not a fourth explanatory strategy.

After the break, give the full account of mechanisms before the associated debates: define entities, activities, and organization; trace the forum process; explain recurring and counteracting tendencies; refer back to the earlier event discussion when examining causal descriptions; then address regress and stopping points, introducing methodological individualism briefly as Elster’s position on the level of social explanation. Follow with necessitation, functional explanation, and just-so stories. The fear-of-darkness example connects the functional claim to the question of whether the proposed selection process actually operated. End with the criticism summary and Elster’s seven distinctions before the workshop.

### If discussion runs long

Preserve the independent forum exercise, its debrief, the break, and the final 18-minute workshop. Recover three minutes by taking one minute each rather than two for “Compare education and work experience together,” “Structures and alternative explanations,” and “A cause under the wrong description.” Keep the Semmelweis reconstruction brisk because students have read it. If another four minutes are needed, shorten “Mechanisms describe tendencies,” “Infinite regress: how much mechanism?,” “Cognitive dissonance: law or mechanism?,” and “A benefit needs a feedback process” to two minutes each. Use one report instead of two in those debriefs.

### Running cognitive-dissonance example

Maya freely pays $150 for a show, is disappointed, then evaluates it more favorably. This is an invented teaching case adapting Elster’s Broadway discussion. Use it first to show why the broad theory does not entail a unique response, then to distinguish a supported probability claim from necessity, and finally to assess a proposed process using Elster’s above/below/lateral tests. Demand remains only a brief optional contrast in the notes. Semmelweis stays the shared worked testing exercise; the forum stays the independent application.

Effort justification could itself produce genuine private attitude change. In the forum, compare it with persuasion as a possible process within the genuine-change category, rather than automatically adding a fourth category alongside change, compliance, and selection. Applause or favorable reports do not by themselves establish that mechanism.

### Model distinctions and criticisms

**DN:** Laws and sufficient conditions entail an outcome. Ask whether the premises are true, the explanatory direction appropriate, the cited factors relevant, and the required laws defensible.

**Probabilistic:** A lawlike conditional probability makes an outcome highly expectable. Ask which reference group and background conditions apply, whether probability identifies the process, and how the account handles rare outcomes.

**HD:** A hypothesis plus auxiliary assumptions implies test consequences. Ask whether rivals predict the same observation and whether a failed prediction challenges the hypothesis or the test assumptions. HD is a testing method, so it can evaluate mechanistic or law-based hypotheses.

**Statistical and mechanistic accounts:** Both retain explicit criticism slides. Statistical adjustment can leave selection, causal identification, and individual pathways unresolved. Mechanism claims face storytelling, unfalsifiable scope adjustments, and infinite regress.

### Source conventions

Elster and Hedström page numbers refer to printed book pagination. Hempel references use the assigned handout's paragraphs and pages. Broader definitions and research-design examples are identified in the relevant notes as instructor elaborations. The deck presents the authors' preference for mechanism-based explanation as an argument to assess, not as a claim that all social science already follows it.

### Readings

- Hempel, Carl. “Semmelweis and Childbed Fever.” Assigned three-page handout, paragraphs 1–13. The handout does not supply its original publication details.
- Elster, Jon. 2007. “Explanation.” In *Explaining Social Behavior: More Nuts and Bolts for the Social Sciences*, pp. 9–31. Cambridge University Press.
- Hedström, Peter. 2005. “Social Mechanisms and Explanatory Theory.” In *Dissecting the Social: On the Principles of Analytical Sociology*, pp. 11–33. Cambridge University Press.

Supplementary teaching example: [“20th Century Theories of Scientific Explanation,” Stanford Encyclopedia of Philosophy, §2.5](https://plato.stanford.edu/entries/scientific-explanation-20th/), for the flagpole-and-shadow asymmetry objection. This supplements the assigned readings.

## Slide-by-slide discussion notes

'''
intro = intro.replace('SCHEDULE_TABLE', schedule)
for number, title, notes, timing in entries:
    intro += f'### Slide {number}: {title}\n\n{notes}\n\n'
(base / 'instructor-notes.qmd').write_text(intro)
print(f'Synchronized notes for {len(entries)} teaching slides; 120 minutes.')
