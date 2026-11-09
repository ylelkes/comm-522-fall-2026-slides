# Week 11 outline: Experiments, from DAGs to Design

**Working title:** "Closing the back door by design"
**Subtitle:** What makes something an experiment, and how two studies used one

**Readings:** Druckman (2023), *Experimental Thinking*, chs. 2–3 ("The Scientific Process and How to Think about Experiments"; "Evaluating Experiments: Realism, Validity, and Samples") · Correll, Benard & Paik (2007), "Getting a Job: Is There a Motherhood Penalty?" · Craig & Richeson (2014/2015 corrigendum), "On the Precipice of a 'Majority-Minority' America"

**Current length:** 79 visible teaching slides, plus 11 hidden optional/backup slides retained in the source.

**Arc in one sentence:** Last week gave students a tool (DAGs) for diagnosing where bias comes from and what to control for; this week asks what happens when, instead of measuring and controlling for a confounder, you redesign the study so the back door never opens — and uses Druckman's vocabulary plus two full experimental papers to show exactly how.

---

## Where this sits in the course

- **Week 10** gave DAGs, the three building blocks (chain/fork/collider), the back-door criterion, and "control by design" as one of several fixes (twins, adoption, lotteries, natural experiments) — with a few worked communication examples (Facebook deactivation, Sinclair) but no deep dive on a single paper's full experimental logic, and six practice/control-or-not slides that weren't reached in class.
- **Week 9** already covered external validity in depth — M-STOUT, WEIRD samples, Henrich et al. Druckman ch. 3 covers some of the same ground (sample representativeness, generalizability) but reframes it around a sharper claim (the three-scenario homogeneity/heterogeneity argument). **Decision: do not re-teach M-STOUT/WEIRD. Treat Druckman's framework as a formal extension and callback, in ~3-4 slides, not a re-derivation.**
- **This week** is the first time students see a published experiment's *complete* design logic end to end: theory → naive observational relationship → DAG → what the randomization closes → findings → what's left open. Both papers are chosen so the DAG work from last week pays off immediately.

---

## Today's route

| Part | Question | Target # slides |
|---|---|:-:|
| 0 · Cold open | — | 2 |
| 1 · DAG recap + core practice | Can you still find a back door and decide what to control for? | ~13 visible |
| 2 · Druckman: what makes something an experiment | What exactly does randomization buy you, and what doesn't it buy you? | ~15 visible |
| 3 · Case 1: Correll, Benard & Paik (motherhood penalty) | What exactly was randomized, and what causal claim does that support? | ~20 |
| 4 · Case 2: Craig & Richeson (majority-minority threat) | How do you experimentally manipulate a proposed *mechanism*, not just measure it? | ~15 |
| 5 · Synthesis + exit | What did randomization close in each case, and what's still open? | ~4 |

The visible route now explains verbally why conditioning on a collider induces dependence, transfers the logic to beauty and talent among famous actors, then introduces mediation and moderation together with the DAG concepts. Moderation uses the running selective-college example: pre-college family SES may change the size of the college effect on income while also acting as a confounder of college attendance. The experiment block now distinguishes assignment, sampling, and precision; translates the typology and validity tables; and qualifies the external-validity argument. Advanced DAG practice and the corrected Study 1 figure remain in the source with `visibility="hidden"`. Correll begins around slide 36; Craig and Richeson mirror its estimand-treatment-outcome-limit structure.

---

## Part 0 · Cold open (1–2 slides)

One slide: restate last week's closing line — "even a carefully chosen control set leaves uncertainty about unmeasured confounders." Today's answer: sometimes you don't control for the confounder, you design around it. Title/route slide.

---

## Part 1 · DAG recap + the practice we didn't get to (~16 slides)

**Goal:** re-establish the vocabulary fast, then actually run the six practice/control slides from week 10 that got cut, using an interactive graphic instead of static reveals where it helps.

1. **One recap slide per building block** (chain/fork/collider) — reuse week 10's three definitions in a single condensed table, not three separate slides. (1 slide)
2. **New interactive graphic: "Open or closed?" (scored).** An SVG/JS panel (same build pattern as `goop-simulation.html`/`lottery-simulation.html`) presenting a DAG with a treatment, outcome, and several intermediate nodes (a mix of confounders, mediators, and colliders, so no single rule works for every node). Students click nodes to toggle "control for this" on/off. Live feedback for every path from treatment to outcome: green = blocked, red = open, with a running tally ("2 of 3 back doors closed") and a final score once they commit to a control set ("identified" / "not identified, because the path through X is still open" / "overcontrolled: you blocked a mediator"). Three presets load into the same widget (chain-only, fork-only, collider-only) followed by one graded "final" DAG — structurally the practice-mediator case (confounder *and* mediator on separate paths) — where getting it wrong shows *exactly which path is still open* rather than just "incorrect." (3 slides: one per preset-building pass, one for the graded final DAG)
3. **Back-door criterion, one-slide restatement.** (1 slide)
4. **The three "Practice:" DAG-drawing slides from week 10, run live:**
   - Practice: what should we control for? (Rohrer Fig. 2, grades/intelligence/income) (1 slide)
   - Practice: a skeptic's DAG (Rohrer Fig. 3, genetic confounding) (1 slide)
   - Practice: a confounder and a mediator (campaign ad / party ID / views of candidate) (1 slide)
5. **Control by design, one-slide restatement** (twins, adoption, lotteries) — compressed from week 10's full version, since it's about to become the whole point of Part 2–4. (1 slide)
6. **The three "Control or not?" rapid-fire tables from week 10, run live:**
   - Today's examples (statins, publication, chess skill, selective college) (1 slide)
   - More practice (cable news, exercise, parents' income, ad spending, candidate looks) (1 slide)
   - Round two (misinformation, college degree, social media/sleep, post virality, newspaper ownership) (1 slide)
7. **Transition slide**: "Every fix so far assumed you could find and measure the confounder. What if you can't?" → sets up Part 2's distinction between the *scientific* solution (find/measure/match) and the *statistical* solution (randomize) to the Fundamental Problem of Causal Inference. (1 slide)

Running count: ~13 content slides + 2–3 for the interactive graphic ≈ 16.

---

## Part 2 · Druckman: what makes something an experiment (~20 slides)

**Goal:** give students Druckman's vocabulary precisely enough that they can use it to narrate Parts 3–4 themselves: the Fundamental Problem of Causal Inference, the two solutions, the experiment typology, setting, realism, experimental goals, the four validities, and a *compressed* callback to external validity/sampling.

1. **The Fundamental Problem of Causal Inference** (1 slide) — you cannot observe the same unit treated and untreated at once. Draw the Y₁/Y₀ table (callback to Week 10's Body Vibes table if useful, or fresh).
2. **Two solutions** (1 slide) — scientific solution (assume unit homogeneity / within-unit stability over time) vs. statistical solution (randomize across many units). Name which one last week's "control by design" examples actually used (twins ≈ scientific; lotteries ≈ statistical).
3. **Druckman's inclusive definition of "experiment"** (1 slide) — a study where an intervention resolves the FPCI; broader than "random assignment required."
4. **Table 2.3: the 2×2 typology** (1 slide, image from `assets/table-2.3-experimental-approaches-typology.png`) — source of intervention (researcher vs. natural) × solution type (statistical vs. scientific). Name where Correll (lab + field, researcher-caused, statistical) and Craig & Richeson (researcher-caused, statistical, with Study 1 as a natural/opportunistic variant) sit.
5. **SUTVA, independence, exclusion restriction** (1 slide) — the assumptions randomization needs to actually deliver on its promise. One worked example (campaign-finance story spillover) per assumption or combined.
6. **Experimental settings: lab, survey, field** (1 slide) — classify by *where* the intervention happens. Place both papers: Correll Study 1 = lab; Correll Study 2 = field audit; Craig & Richeson Study 1 = opportunistic survey experiment; Studies 2/3a/3b = purpose-built survey/online experiments.
7. **Mundane realism vs. experimental realism** (1 slide) — explain why Druckman privileges activating and isolating the causal mechanism over making a study superficially resemble daily life. Put Plott's theory-first standard on screen and qualify it for policy forecasts.
8. **Immigrant threat across settings** (1 slide) — compare Enos's randomized insertion of Spanish-speaking confederates into real commuter routines with Brader, Valentino, and Suhay's laboratory-style computer-station experiment. Use the contrast to show that field realism identifies the effect of a bundled experience, while a constructed stimulus isolates ethnicity cue × skill stereotype.
9. **Experimental goals: fact-finding, theory-testing, policy** (1 slide, Roth 1995) — students classify three examples: Correll's parent cue, an ultimatum-style bargaining game, and a city vaccination reminder. Contrast "searching for facts," "speaking to theorists," and "whispering in the ears of princes."
10. **The bargaining game in full** (1 slide) — responders randomly receive a $5/$5 or $8/$2 division of $10 and choose whether to accept or reject, with rejection paying both parties $0. Contrast strict monetary self-interest with fairness/costly-punishment predictions and identify what must feel real for the artificial task to work.
11. **Treatment validity and manipulation checks** (1 slide) — tie to Craig & Richeson's comprehension/attention checks and their explicit manipulation check that the status-threat condition *did* raise perceived threat while the assuaged-threat condition did not.
12. **Table 3.1: four types of validity** (1 slide, image from `assets/table-3.1-types-of-validity.png`) — statistical conclusion, internal, construct, external. One line per type with a concrete anchor from one of the two papers.
13. **External validity, compressed callback to Week 9** (1 slide) — "you already have the tools for this." One-line M-STOUT recap (mechanisms, treatments, outcomes, units, setting, time — the dimensions of a generalizability claim) plus the WEIRD-sample headline, then: "Druckman adds one sharper claim on top of M-STOUT's units/settings axes."
14. **The three-scenario generalizability argument** (1–2 slides) — homogeneous effect → any sample works; heterogeneous + sample has variance on the moderator → still fine; heterogeneous + no variance on the moderator → only now is sample composition a real threat. Apply it live: does Correll's undergraduate lab sample threaten generalizability? (Authors' own answer: qualitative/quantitative comparisons suggest student and manager judgments track similarly — an implicit "no strong moderator, or sample has enough variance" argument.) Does Craig & Richeson's heavily male MTurk sample in 3a/3b threaten generalizability? (Open question — assign as discussion.)
15. **"The burden falls on the critic"** (1 slide) — the provocative one-liner, as a discussion prompt: is this fair?
16. **What a DAG/experiment still can't do** (1 slide) — identification ≠ estimation; the design is only as good as the assumptions (SUTVA, exclusion restriction, "the DAG is an assumption" callback to week 10).
17. **Transition slide into the two cases** (1 slide) — "Now watch two published papers use exactly this logic."

That's ~17–18 slides; pad to ~20 with 1–2 more worked micro-examples if the pacing needs it (e.g., a quick "type vs. goal" matching activity).

---

## Part 3 · Case 1: Correll, Benard & Paik — the motherhood penalty (~14 slides)

**Throughline for every case in Parts 3–4:** theory → students draw the naive/observational DAG themselves → what the experiment closes → discuss and critique the actual design *before* seeing results → findings read back through the DAG → critique what's still open.

1. **The puzzle** (1 slide) — the real-world correlation: mothers earn ~5% less per child than childless women, even controlling for human capital (Budig & England 2001).
2. **Draw it with me: the naive DAG** (1 slide, live) — don't show the finished DAG. Put up Motherhood and Wages only, and ask students to propose what belongs between them and what kind of node it is. Build the back door through **Productivity/Human Capital** on the board/slide as they propose it (a fork: unmeasured ability/effort/experience interruptions → both motherhood-linked job choices and wages). Ask: what would you need to control for, and why is that hard here? (Answer: productivity — unmeasured and endogenous.)
3. **Status characteristics theory, briefly** (1 slide) — the competing "discrimination explanation": a status characteristic (motherhood) shifts the *evaluation standard* itself, not just beliefs about average productivity. Double-standard proposition: mothers need a higher percentile score to be judged hirable.
4. **Status-based vs. statistical discrimination as two DAGs** (1 slide) — statistical discrimination predicts the gap vanishes once information is equalized (arrow from Productivity closes if measured perfectly); status-based discrimination predicts a direct arrow from the *motherhood label itself* to the evaluation, independent of information quality. Ask students which DAG the upcoming design is built to distinguish before revealing.
5. **Design it yourselves, then compare** (1 slide, discussion) — before describing Study 1, ask in pairs: "If you wanted to test whether this is status-based discrimination and not just statistical discrimination, and you can't randomly assign real women to become mothers, what would you do?" Give them 2–3 minutes before revealing the actual design.
6. **The actual design: Study 1** (1 slide) — identical résumés, randomly assigned parental-status label within matched pairs. Name precisely what this is in Druckman's terms: the statistical solution to the FPCI applied at the level of the *applicant profile*, holding productivity constant by construction rather than by measurement.
7. **Critique it, before the results** (1 slide, discussion) — "What's a legitimate objection to this design, before you know what it found?" Let students raise: undergraduates aren't real hiring managers; one job type (high-status marketing); deception; a single résumé pair per condition. Note which of these the authors address themselves (student/manager comparability; pretested résumé equivalence) and which stay open.
8. **Table 1 findings** (1 slide, image) — competence 5.19 vs. 5.75; hire recommendation 46.8% vs. 84.0%; required exam percentile 72.4 vs. 67.9 (the double standard, directly). No penalty (even a premium) for fathers.
9. **Mediation, read through last week's warning** (1 slide) — competence/commitment ratings mediate 31–46% of the effect. Flag explicitly: this mediation analysis *measures* the mediator rather than manipulating it, so by Rohrer's own warning from last week it is suggestive, not fully causal — unlike what Craig & Richeson will do in Part 4.
10. **Study 2: the field audit, a second experiment** (1 slide) — same logic, real resumes to real employers, callback as the outcome. Ask before revealing why it exists: "Study 1 already identified the effect. Why run a second study?" (External validity — the lab closes the back door perfectly but leaves open whether real-world institutions behave the same way.)
11. **Table 6 findings** (1 slide, image) — 3.13% vs. 6.56% callback; no detectable father bonus in the field.
12. **Critique round two: what's still open** (1 slide, discussion then reveal) — ask students first, then compare against: *why* employers discriminate in the field (no rating data there); the residual 54–69% unmediated effect in the lab; generalizability beyond one high-status job type; the unexplained race-based salary penalty the authors themselves flag but don't resolve.
13. **Redraw the DAG with the experiment on it** (1 slide, pairs) — students draw the full DAG including the randomized arrow into parental status and mark which path is now severed; cold-call a pair to present.
14. **Bridge to Case 2** (1 slide) — "Correll closed one back door by randomizing the treatment. Craig & Richeson will go one step further: randomizing the *mediator itself*."

---

## Part 4 · Case 2: Craig & Richeson — majority-minority status threat (~15 slides)

1. **The puzzle** (1 slide) — Giles & Hertz (1994): more local Black population % predicts more White Republican registration. Real-world correlational motivation.
2. **Draw it with me: the naive DAG** (1 slide, live) — same build-it-live approach as Part 3. Put up Racial Composition and White Conservatism only, and have students propose structures: political feedback through policy and migration (explicitly noting that its sign is ambiguous), a regional historical confounder, or a genuine causal arrow. Do not treat feedback as a clean explanation for the positive association: exclusion and White flight can move population share in opposite directions. Ask which structure fits Giles & Hertz's correlational data and what additional evidence each story would require.
3. **Theory: motivated social cognition + group-status threat** (1 slide) — threat/uncertainty → conservatism (Jost et al.), extended from mortality/terrorism threats to a slow, abstract, decades-out *social* threat. Group-status threat as a specific, zero-sum mechanism, distinguished from system threat/system justification/uncertainty (only the first tracks the manipulation).
4. **Design it yourselves: isolating the status-shift framing** (1 slide, discussion) — "You want to test whether it's specifically the *majority-minority/status* framing doing the work, not just any news about demographic change. What's your control condition?" Let them propose before revealing Study 1's control (Black/Hispanic-parity framing, which holds "racial composition news" constant).
5. **Study 1: an opportunistic natural/survey experiment** (1 slide) — Pew's embedded survey experiment. Name it in Druckman's terms: researcher-caused (the survey form was randomized), statistical solution, repurposed from an existing dataset rather than purpose-built.
6. **Study 1 findings + the corrigendum, part one: the error** (1 slide) — the 2015 corrigendum corrected a probability-weighting error (frequency weights mishandled as probability weights in the statistical software) in Studies 1 and 2. A real example of post-publication correction without retraction.
7. **Study 1 findings + the corrigendum, part two: what changed** (1 slide, Figure 1 image) — originally published as significant; corrected analysis: marginal (p = .081) nationally, stronger in the West region subsample (OR ≈ 3.22, p = .063). Ask: how much should this downgrade your confidence in the whole four-study program?
8. **Critique the design so far** (1 slide, discussion) — before Study 2: what does Study 1 *not* establish yet? (A measured outcome only — no mediator tested; a single secondary dataset; self-reported party lean, not behavior.)
9. **Study 2: purpose-built experiment, with a measured mediator** (1 slide) — TESS nationally representative sample; racial-shift press release vs. geographic-mobility control; four candidate mediators measured. Only group-status threat differs by condition and mediates (Table 2 image).
10. **Why "measuring a mediator" isn't enough — direct callback to Rohrer** (1 slide) — restate last week's warning: controlling for/analyzing a measured mediator can be biased even in an experiment, because of unmeasured confounding *between the mediator and the outcome*. Study 2 cannot rule this out on its own. Ask: "What would fix it?" before revealing Studies 3a/3b.
11. **Design it yourselves: manipulating the mediator** (1 slide, discussion) — "You need to manipulate group-status threat directly, not just measure it, while holding the demographic information constant. What's your third condition?" Let them propose before revealing the assuaged-threat condition (identical demographic article plus a paragraph stating Whites' relative status will remain stable).
12. **Table 3 findings** (1 slide, image) — status-threat condition more conservative than *both* control and assuaged-threat; control and assuaged-threat statistically indistinguishable from each other. The "elimination" pattern.
13. **Reading the result back through the DAG** (1 slide) — draw the full chain live: Racial-shift info → Status threat → Conservatism, with the assuaged-threat condition cutting the arrow from information to threat while leaving the information itself constant.
14. **Critique round two: what's still open** (1 slide, discussion then reveal) — ask first, then compare against: immigration attitudes specifically didn't move (awkward for a clean "race-status" story); heavily male, young MTurk samples in 3a/3b; brief artificial stimuli vs. real political-media exposure; divergent Black/Latino patterns relegated to footnotes.
15. **Bridge to synthesis** (1 slide, pairs) — compare: what did Correll's randomization close, and what did Craig & Richeson's *second* randomization (of the mediator) close that the first one didn't?

---

## Part 5 · Synthesis + exit (~4 slides)

1. **Side-by-side comparison slide** — both papers, one row each: naive back door → what was randomized → what's still open. Make the parallel explicit: Correll randomizes the treatment once; Craig & Richeson randomize the treatment *and*, in 3a/3b, the mediator.
2. **Druckman's typology, revisited with both papers placed on it** — Table 2.3 again, now with Correll Study 1/Study 2 and Craig & Richeson Studies 1–3b each dropped into a cell.
3. **Project tie-in** — if your own project claim is causal, could you ever randomize the treatment? The mediator? What would the naive DAG look like, and what's the smallest intervention that would close the relevant back door?
4. **Exit question** — "Pick one back door from your own project's naive DAG. Could it be closed by design, or only by measurement? What design would it take?"

---

## Figures/assets needed

- From week 10 (already built, reusable as a condensed recap): `assets/dag-chain.svg`, `assets/dag-fork.svg`, `assets/dag-collider.svg`, `assets/rohrer-fig2-grades-backdoor.png`, `assets/rohrer-fig3-genetic-confounding.png`, `assets/dag-practice-ad.svg`
- From the Druckman summary (already extracted): `table-2.3-experimental-approaches-typology.png`, `table-2.1-measurement-validity-concepts.png`, `table-3.1-types-of-validity.png`
- From the Correll summary (already extracted): `table1-lab-experiment-ratings.png`, `table6-audit-study-callbacks.png`
- From the Craig & Richeson summary (already extracted): `figure1-study1-corrected.png`, `table2-mediation-study2.png`, `table3-study3.png`
- **To build:**
  - the naive DAGs for both cases (motherhood/productivity fork; racial-shift/status-threat chain with the assuaged-threat cut)
  - the interactive "open or closed?" DAG graphic (new JS/SVG, same pattern as `goop-simulation.html`)
  - a condensed single-slide version of the chain/fork/collider table (reuse week 10's table, trimmed)

## Decided (from your feedback)

- **Interactive graphic is scored.** Students build a control set by toggling nodes; live feedback shows which paths are blocked vs. still open, with a running tally and a final verdict ("identified" / "not identified — path through X still open" / "overcontrolled — you blocked a mediator"). Three preset passes (chain/fork/collider) plus one graded mixed DAG.
- **M-STOUT callback kept, compressed to one line** inside the external-validity slide in Part 2, rather than cut entirely or re-taught at length.
- **Both cases get full live treatment**: students draw the naive DAG themselves (not shown pre-built), discuss/design the study themselves before each design reveal, and critique the design and its remaining limitations before and after seeing results. This is why Parts 3–4 grew from ~12 to ~14–15 slides each.
- **Corrigendum gets two slides** (Part 4, slides 6–7): one on the weighting error itself, one on the corrected numbers and what they change.
- **The "manipulate vs. measure a mediator" callback appears twice**: first as a general point in Part 2 (slide 8, mediation vs. moderation), then again at its sharpest, case-specific payoff in Part 4 (slide 10), directly before Studies 3a/3b.

## Open decisions

- **Whether to trim the ~71-slide running total back toward 65** (see the note under the route table) — your call on which of the three suggested cuts, if any, to apply, or whether to just run long.
