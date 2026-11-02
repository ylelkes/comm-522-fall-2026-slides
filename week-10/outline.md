# Week 10 outline: Causality, Potential Outcomes, and DAGs

**Working title:** "What would have happened otherwise?"
**Subtitle:** Correlation, counterfactuals, and the structures that make them diverge

**Readings:** Bergstrom & West (2021), *Calling Bullshit*, ch. 4 "Causality" · Bueno de Mesquita & Fowler, *Thinking Clearly with Data* (TCD), chs. 3 & 9 · Rohrer (2018), "Thinking Clearly About Correlations and Causation"

**Arc in one sentence:** Students first argue about real causal claims without any vocabulary. Potential outcomes then give them a precise definition of an effect, and the bias decomposition shows exactly how selection into treatment makes a correlation differ from that effect. DAGs then give them a tool to draw where the bias comes from and decide what to control for. We finish by redrawing the opening cases.

---

## Where this sits in the course

- **Week 6** introduced estimands (Lundberg et al.) and mentioned the causal estimand $E[Y(1)-Y(0)]$ only in the notes. This week makes that formal.
- **Week 9** covered *selection into the sample*: Berkson's paradox, deletion and archive survival, and sampling on the dependent variable. This week's "selection" is a different thing: **selection into treatment**. Students will mix these up unless we name the difference. The DAG section brings the two back together: selection into treatment is a fork (confounding), and selection into the sample is a collider.
- **Week 7** separated descriptive from explanatory claims. Today is the first week that is entirely about explanatory, causal claims.

---

## Today's route

| Part | Question | Time |
|---|---|---|
| 1 · Four claims | What would you need to know before believing this? | ~20 min |
| 2 · Potential outcomes | What does "X causes Y" actually mean? | ~25 min |
| 3 · How selection creates bias | Why does the difference in means differ from the effect? | ~25 min |
| — break — | | 10 min |
| 4 · Rohrer's DAGs | Where does the bias come from, and what should you control for? | ~40 min |
| 5 · Back to the cases, fever, and the project | Can you now diagnose the opening claims? | ~10 min |

---

## Part 1 · Four claims (talk-through cases, like Week 9)

**Format:** the same as Week 9's opening cases. Each slide shows the claim and the evidence (with its figure). Students say whether they believe it, offer alternative explanations, and say what evidence would settle it, and only then do we reveal the answer. Hold back the vocabulary (confounder, reverse causation, collider) so the cases make students want it.

Each case is chosen to show a **different structure**, so that Part 4 can map them onto DAGs.

*Revised: the opening cases are now real-data communication examples, not the books' examples. Each pairs a tempting correlation with a design that tested it.*

1. **Social media and teen depression**: direction is the question. Three stories (social media → depression; depression → social media; loneliness/family stress → both). *Reveal:* Heffer et al. (2019, *Clinical Psychological Science*) followed 594 adolescents for 2 years. Depressive symptoms predicted later social media use (among girls); social media did not predict later depression. Caveat: Orben & Przybylski (2019), >300,000 teens, found tech use explains at most 0.4% of the variance in well-being; the literature is contested.
2. **News coverage and public attention**: reverse causation. Editors cover what audiences already care about. *Reveal:* King, Schneer & White (2017, *Science*) randomly assigned publish dates for stories at 48 outlets. Discussion of the topic rose 62.7% of a day's volume (~13,166 posts over the week). Reverse causation is real, but coverage also has an effect.
3. **TV and children's test scores**: a common cause (family background). *Reveal:* Gentzkow & Shapiro (2008, *QJE*) used TV's staggered arrival in the 1940s–50s, with 1965 Coleman test scores. About +0.02 SD per year of preschool TV; harms larger than 0.03 SD ruled out; gains largest for disadvantaged children.
4. **Fox News**: selection into treatment (unchanged).

**Synthesis slide:** "What changed between the correlation and the claim?" List what students came up with: direction, reverse causation, a common cause, who chose the treatment. Then: "Today we build a language that makes each of these precise."

*Cut from earlier versions:* Zillow and storks/organic food. If needed, either can be one line on the synthesis slide ("also: shared trends, selective migration").

---

## Part 2 · Potential outcomes, explained very plainly

**Goal:** students can define a causal effect for one person, say why it can never be observed, and say why averages rescue us.

1. **Two worlds** (TCD ch. 3, Body Vibes). In one world you wear the $6 stickers. In another, identical up to that moment, a friend secretly swapped them for 10¢ stickers. The effect is the difference in your skin between the two worlds. Visual: a split-screen or forking-path graphic.
2. **Notation, introduced slowly.** $T$ = treatment, $Y$ = outcome, $Y_{1i}$ and $Y_{0i}$ = the outcomes person $i$ *would* have. Individual effect = $Y_{1i} - Y_{0i}$. Show one person first, then a table.
3. **The full table: the view only the author of a made-up example gets.** TCD Table 3.1 (Body Vibes, 10 people). Every effect is 0.
4. **Hide half the table.** Grey out the counterfactual cells, leaving what a researcher actually sees. **This is the fundamental problem of causal inference**: each person is observed in only one world. (TCD's college example: you can't live both lives.)
5. **What the naive comparison says.** Wearers: 3/5 have clear skin. Non-wearers: 2/5. Difference = **+20 points**, but the true effect is **0 for everyone**. Ask students *why* before explaining.
6. **It can even flip the sign** (TCD Table 3.2, flu shot). True average effect = **+0.2**, yet the naive comparison = **−0.2**, because the vaccinated group happened to be full of "always sick" types. Introduce the types: always sick, never sick, responders. This also deals with "I got the shot and still got the flu" (effects vary across people; one counterexample doesn't refute an average).
   **Real-world version: hormone replacement therapy** (new slide after the flu table). In the observational Nurses' Health Study (48,470 nurses, 10 years), current estrogen users had **about half the risk** of major coronary disease (RR ≈ 0.56). The randomized Women's Health Initiative (estrogen + progestin) found a **29% higher risk** (HR 1.29). Same sign flip as the flu table, with real data and real prescriptions. The study's own authors had warned in 1991: "healthier women are selected for such therapy." Follow-up: Hernán et al. (2008) reanalyzed the observational data as if it were a trial (comparing women who started hormones with women who didn't) and got much closer to the randomized result. Bring HRT back in Part 3 as a case of selection into treatment.
7. **Averages answer a different, still useful question.** ATE = average of $Y_1 - Y_0$. The FDA asks about averages; a court asks a but-for question about one person. Which questions can our methods answer?
8. **Quick check (pair work, 3 min):** a small blank table for a communication example (e.g., T = saw a fact-check, Y = believes the false claim). Students fill in plausible potential outcomes for 4 people and compute the individual effects and the ATE.

*Link back:* Week 6 estimands. The ATE is a causal estimand; the difference in means is an associational one. Today asks when they are equal.

---

## Part 3 · How selection creeps in and produces different potential outcomes

**Goal:** students see that a correlation = effect + baseline difference, and that "selection bias" here means *the treated and untreated groups would have differed even with no treatment*.

1. **Go back to the Body Vibes numbers.** The +20 came entirely from people who would have had clear skin anyway choosing the stickers. Among wearers, $\bar Y_0$ = 3/5; among non-wearers, 2/5. That gap *is* the bias.
2. **The decomposition, built in steps** (TCD ch. 9). Reveal one term at a time:
   - Observed: $\bar Y_{1T} - \bar Y_{0U}$
   - Add and subtract the missing piece $\bar Y_{0T}$, the treated group's world without treatment
   - $= \underbrace{(\bar Y_{1T} - \bar Y_{0T})}_{\text{ATT}} + \underbrace{(\bar Y_{0T} - \bar Y_{0U})}_{\text{baseline difference (bias)}} + \text{noise}$
   - Connect it to TCD's "favorite equation": **Estimate = Estimand + Bias + Noise**.
   - Check that the numbers work on both tables: Body Vibes 0 + 0.2 = 0.2, flu shot 0.2 − 0.4 = −0.2.
3. **Worked case: charter schools** (TCD ch. 9, Preuss School; now the main worked example rather than an opening case). Preuss students pass at nearly 100% vs. under 80% for San Diego City Schools (Fig. 9.1). Who enters the lottery? Talented children and invested parents. So $\bar Y_{0}$ for Preuss students > $\bar Y_{0}$ for others: they would score higher at *any* school. Among lottery applicants, winners and losers score about the same (Fig. 9.2: Language +5, Geometry −24, Physics +7). This is how a 20-point raw gap can coexist with a near-zero effect. Then the Fox News case from Part 1 in the same terms: the viewer gap = a small ATT + a large baseline difference.
4. **Why the lottery fixes it.** Randomization makes the potential outcomes the same *on average* across groups, so the baseline-difference term → 0 and only noise is left. The lottery "broke the link between talent and attendance."
5. **Name the two sources of baseline differences** (TCD ch. 9):
   - **Confounders**: affect treatment *and* the outcome (talent; sexual activity in the contraception–HIV study).
   - **Confounding, real case:** HRT from Part 2. Healthier, wealthier, more health-conscious women chose hormones, so $\bar Y_0$ (heart health without hormones) was higher among users. The bias was large enough to flip the sign.
   - **Reverse causality**: the outcome affects treatment (civil war → economy; beer pitchers).
   - **Reverse causality, real case: police and crime** (Di Tella & Schargrodsky 2004, *AER*). Places with more police have more crime, because police are sent where crime is. After the 1994 AMIA bombing in Buenos Aires, every Jewish institution got 24-hour police protection, for reasons unrelated to car theft. Comparing protected blocks with other blocks before and after: **car thefts fell about 75%** on protected blocks, with no detectable effect one or two blocks away. *Prompt:* what would the raw cross-city correlation between police and crime have said?
6. **Signing the bias** (TCD). Exercise: hormonal contraception and HIV. Sexual activity → more likely to choose contraception (+), and → HIV risk (+), so the bias is **positive**, and the doubled risk is an overstatement. (Ending: the ECHO randomized trial found no meaningful difference.) Then the students sign one themselves: statins and pre-treatment cholesterol.
7. **Not the same as last week's selection bias** (one slide, two columns):
   - *Selection into the sample* (Week 9): who ends up in our data → threatens descriptive and causal claims.
   - *Selection into treatment* (today): who ends up treated → baseline differences → biased causal comparison.
   - Both are about a process we didn't control deciding what we observe. Part 4 shows they have different shapes.

---

## Part 4 · Rohrer's DAGs: drawing where bias comes from (~40 min)

**Goal:** students can read and draw a DAG, identify the three elementary structures, find back-door paths, and decide what to control for, and especially what *not* to control for.

**Why this part follows Rohrer's structure:** Rohrer is the reading that makes potential outcomes *usable*. Part 3 ends with "bias = baseline differences." Rohrer answers the practical question that comes next: *I can't randomize, so which variables do I control for?* Her answer is that controlling for a variable can help, do nothing, or hurt, depending on where it sits in the graph. The part follows her argument in order.

**4a · Rohrer's dilemma (5 min).** Many important questions can't be randomized (divorce and well-being, social class, childhood adversity, and for us, media exposure over years). Rohrer names three common workarounds and what is wrong with each:
1. *Surrogate interventions*: manipulate a lab proxy (Piff et al.'s "social ladder" priming in place of actual social class). Is the proxy the cause you care about?
2. *Avoiding causal language*: "associated with… future experiments are needed." The question is still causal, and readers read it causally anyway (callback to B&W on grammar).
3. *Garbage-can regressions*: control for everything available because "more control is better." Rohrer calls this "a methodological urban legend."

*Prompt:* which of these have you seen in communication papers? (Most students will recognize #2 and #3 right away.)

**4b · The grammar of a DAG (5 min).** Nodes = variables. An arrow = a direct causal effect ("if you intervened on the start, the end would change"). Arrows can encode any functional form, not just linear effects. **No cycles**: feedback is handled by indexing variables by time. That is how a DAG represents reverse causation, so redraw beer pitchers as *intention (t₀) → pitcher (t₁) → consumption (t₂)* and *intention → consumption*. Rohrer's running example (Fig. 1): education → income ($1,500 vs. $700 per week at age 40), with intelligence → both. The $800 gap = the causal path + an open back-door path.

**4c · Three building blocks (8 min).** Every path is built from these. One slide each, each with a small simulated scatterplot showing the association with and without conditioning (the same visual style as Week 9's Berkson panels):

| Structure | Form | Open by default? | Conditioning on the middle… | Opening/reading example |
|---|---|---|---|---|
| Chain | X → M → Y | yes (causal) | blocks part of the real effect (**overcontrol**) | TCD: charter → AP classes → scores |
| Fork | X ← C → Y | yes (**non-causal**) | removes the bias | marshmallow (parental SES); Preuss (talent) |
| Inverted fork | X → C ← Y | **no** | *creates* bias (**collider bias**) | Rohrer Fig. 4: rigor → publication ← innovation |

Key sentence: **the fork is today's selection into treatment, and the collider is last week's selection into the sample.** Same picture as Week 9's Berkson panels.

**4d · The back-door criterion (7 min).** A back-door path starts with an arrow *into* the treatment. To identify the effect, block every back-door path (any non-collider on the path will do) and don't condition on anything caused by the treatment. **Practice on Rohrer Fig. 2** (adding grades): students list the paths, then fill in the table: control for nothing / grades / intelligence / both. → Only sets that include intelligence close both back doors. Then Fig. 3 (maternal behavior and child depression, with genetic confounding): find the one back-door path.

**4e · Control by design (5 min).** Instead of measuring confounders, choose a design where the back-door path doesn't exist.
- *Twins*: Turkheimer & Harden. Religiosity and delinquency are negatively correlated, but within identical-twin pairs the association disappears.
- *Adoption* cuts the gene → gene arrow.
- *Natural experiments and lotteries*: callbacks to the Preuss lottery and the Fox News cable rollout. Rohrer describes natural experiments as an intermediate case between observational studies and experiments.
- **Communication designs that cut the back door** (one slide, three panels; each panel shows the selection problem, the design, and the result):
  - **Facebook deactivation** (Allcott, Braghieri, Eichmeyer & Gentzkow 2020, *AER*). The selection problem: heavy users differ from light users. The design: participants randomly paid to deactivate for the 4 weeks before the 2018 midterms. Result: deactivation **reduced polarization and news knowledge and increased subjective well-being**; 80% of the treatment group said it was good for them. A randomized experiment on the real treatment, not a lab proxy (contrast with Rohrer's surrogate interventions).
  - **Sesame Street** (Kearney & Levine 2019, *AEJ: Applied*). The selection problem: families who choose educational TV differ. The design: reception depended on distance to the tower and on whether PBS broadcast on UHF or VHF (coverage ≈ 83% in strong-reception vs. 55% in weak-reception counties). Result: children in strong-reception areas were **about 3 points more likely to be at grade level for their age**, more so for boys and in disadvantaged areas. Long-run effects were inconclusive.
  - **Sinclair acquisitions** (Martin & McCrain 2019, *APSR*). The selection problem: Sinclair chooses which stations to buy. The design: difference-in-differences comparing 10 stations acquired in 2017 with other programs in the same markets. Result: **national politics coverage up about 25%, local politics down about 10%, a rightward shift in slant**, and slightly fewer viewers. The outcomes are measured from **text**, which ties directly to the coding project.
  - *(Option: Lelkes, Sood & Iyengar 2017 on broadband and polarization, using right-of-way laws, as a fourth panel or a mention.)*

**4f · "Learning to let go": when control hurts (7 min).** The rule of thumb is **don't control for post-treatment variables.**
- *Colliders built into data collection* (Rohrer's "endogenous selection"): only completed questionnaires (grit and IQ), panel stayers (attrition, Fig. 5), only college students, only published studies. For text data: posts that survived moderation, articles that made it into the archive (direct callback to Week 9).
- **A real collider: smoking and COVID** (Griffith et al. 2020, *Nature Communications*). Early hospital studies found fewer smokers than expected among COVID patients, and some suggested smoking was protective. But smoking and COVID both make hospitalization more likely, so **hospitalization is a collider**, and analyzing only hospitalized patients creates a negative association. Griffith et al. show that collider bias alone can produce associations as large as the reported "protective" effect. Draw it: Smoking → Hospitalized ← COVID, with the analysis restricted to Hospitalized = 1. Same structure as Rohrer's publication example and Week 9's Berkson panels.
  - *Optional second case:* the birth-weight paradox (Hernández-Díaz, Schisterman & Hernán 2006). Among low-birth-weight infants, maternal smoking looks protective, because low birth weight is a collider between smoking and other, more serious causes. *(Check the numbers before using it.)*
- *Mediators*: Fig. 6, where adult intelligence is both a mediator *and* a collider, so controlling for it does two kinds of damage at once.
- **The communication research link:** mediation analysis in the Baron & Kenny / Hayes PROCESS tradition (Hayes 2009 appeared in *Communication Monographs*) controls for the mediator. Rohrer warns this is biased **even in experiments** unless the mediator is randomized. Many students will have run PROCESS, so it's worth a slide.

**4g · What a DAG can't do (3 min).**
- *Identification ≠ estimation*: the right control set still needs the right functional form.
- *Measurement error*: a noisily measured confounder leaves residual confounding. False-positive rates can approach 100% in large samples (Westfall & Yarkoni).
- *The DAG is an assumption*: be transparent, check robustness across plausible DAGs, and triangulate. Rohrer's cases accepted without RCTs (smoking, climate, parachutes) lead into the fever example in Part 5.

**Activity: control or not? (built into 4f, ~3 min).** A rapid-fire slide with Rohrer's decision table hidden. Students classify each variable before the reveal: pre-treatment cholesterol (confounder → control), post-treatment cholesterol (mediator → don't), publication status (collider → don't), chess skill as a proxy for adult IQ (descendant of a mediator → don't).

---

## Part 5 · Back to the cases, fever, and the project (~10 min)

1. **Pairs draw the opening cases (4 min).** Each pair takes one: kiss (three candidate DAGs), pitchers (time-indexed intention), marshmallow (fork through parental SES), Fox News (self-selection fork + the rollout as a design fix). Mark the back-door paths and say what you'd control for, what you wouldn't, and what design would cut the path. Reveal all four DAGs on one slide.
2. **How a causal case gets built: fever** (B&W). Taken in order, each step rules out one DAG:
   - Correlation (fever patients survive more) → fever → outcome? (Fig. 12a)
   - Common-cause alternative: good condition → fever and good condition → survival (Fig. 12b, a fork)
   - Natural experiments with antipyretics: patients weren't randomized, so the fork is still possible
   - Randomized trials: blocking fever slows recovery and increases transmission. This closes the back door.
   - Cooling lab animals with no drug gives the same harm. This isolates the mechanism (the chain runs through temperature, not the drug).

   This ties together all three parts of the session: potential outcomes (what effect?), bias (why the raw correlation misleads), and DAGs (which alternative each design rules out).
3. **Project tie-in.** The coding projects are descriptive, but the write-ups will be tempted by causal language ("coverage *drives*…", "outlets *respond to*…"). Each group writes one causal-sounding claim their data invites, draws its DAG, and rewrites it as the descriptive or associational claim the data can support. (B&W: graph axis placement and grammar also signal causation.) Use **Sinclair** as the model: the same kind of coded-text outcome becomes causal evidence *only* because of the acquisition design. Ask what event or rule in their own domain could do that.
4. **Exit question:** "Name one correlation in your own area that is usually read causally. Draw the DAG that would make it non-causal."

---

## Figures available (Readings/Week 10/figures/)

- B&W: beer by vessel (fig06), marshmallow common cause (fig07), fever DAGs (fig12a/b)
- TCD: Table 3.1 Body Vibes, Table 3.2 flu shot, Fig 9.1 Preuss vs SDCS, Fig 9.2 lottery, Fig 9.3 confounders, Fig 9.4–9.5 reverse causality, Fig 9.8 contraception/HIV, Fig 9.9 confounder vs mechanism
- Rohrer: Fig 1 (intelligence confounding), Fig 2 (grades/back-door), Fig 3 (genetic confounding), Fig 4 (publication collider), Fig 5 (attrition), Fig 6 (adult IQ mediator/collider)
- Need to build:
  - the Body Vibes table with counterfactual cells greyed out (an animated reveal)
  - the decomposition built in steps
  - chain/fork/collider simulations, in the same style as Week 9's Berkson scatterplots
  - clean DAGs for the four opening cases (kiss ×3, pitchers, marshmallow, Fox)
  - a Fox News figure, or the numbers from DellaVigna & Kaplan
  - HRT: a two-bar "observational vs. randomized" figure (RR 0.56 vs. HR 1.29)
  - Smoking/COVID collider DAG, and possibly a simulation panel in the same style as the Berkson figures
  - the three-panel communication-designs slide (Facebook, Sesame Street, Sinclair)

## Decided

- Four opening cases, all real-data communication examples outside the books: social media and depression (direction), news coverage (reverse causation), TV and test scores (common cause), Fox News (selection). Preuss is the worked example in Part 3.
- Fever is the closer in Part 5.
- Part 4 is built around Rohrer's argument, in order, with ~40 min.
- Real-data examples beyond the readings: HRT (Parts 2–3), police and crime (Part 3), Facebook deactivation / Sesame Street / Sinclair (4e), smoking and COVID (4f), Sinclair again in the project tie-in.

## Open decisions

- How much notation: full ATT/ATU decomposition, or only ATT? (Suggestion: ATT only on slides, ATU in the notes.)
- Is ~40 min for Part 4 realistic? The added examples make it tighter. If needed, collapse 4e to the three-panel communication slide alone and mention the twins study in the notes only.
- Include Lelkes, Sood & Iyengar (2017) as a fourth design panel?

## Sources for added (non-reading) examples

- DellaVigna & Kaplan (2007), *QJE* 122(3): 1187–1234. Verified: 0.42–0.69 pt presidential; ~0.8 Senate; 9,256 towns; 3–28% persuasion rate.
- Allcott, Braghieri, Eichmeyer & Gentzkow (2020), *AER* 110(3): 629–76. Verified qualitatively. Get the effect sizes in SD units from the paper before putting numbers on a slide.
- Kearney & Levine (2019), *AEJ: Applied* 11(1): 318–350. Verified: coverage 83% vs. 55%; ~3 pt grade-for-age.
- Martin & McCrain (2019), *APSR* 113(2): 372–384. Verified: 10 stations (Bonten purchase, 2017); +25% national / −10% local; rightward slant; small viewership drop.
- Stampfer et al., Nurses' Health Study 10-year follow-up, *NEJM* 325(11), 1991 (RR 0.56, CI 0.40–0.80); WHI 2002 (HR 1.29, CI 1.02–1.63); Hernán et al. 2008, *Epidemiology*.
- Griffith et al. (2020), *Nature Communications* 11: 5749.
- Di Tella & Schargrodsky (2004), *AER* 94(1): 115–133. Verified: ~75% decline; no spillover 1–2 blocks away.
- Hernández-Díaz, Schisterman & Hernán (2006), *AJE*. Not yet verified.

## Added after the first build

- **Readings:** Isch, Dörr, Fasching, Jennings & Watts (2026), "Quantifying the prevalence and impact of overreaching causal claims in social science," *Nature Human Behaviour*. Summary: `Readings/Week 10/Summary - Isch et al 2026 - Overreaching Causal Claims.md`.
- **Part 2:** the flu shot is now four slides (setup with types → full table with a type column → what a researcher sees → why the sign flipped).
- **Part 3:** an interactive "Who buys Body Vibes?" simulation (selection slider and true-effect buttons; readout shows difference = effect + baseline difference). After "Why randomization removes the bias": a lottery potential-outcomes table (invented, 10 applicants) and an interactive balance table (simulated; winners vs. losers vs. non-applicants; re-run button).
- **Part 5, before the project slide:** five Isch slides covering prevalence (46.3%; 20% → 60%), where claims hide (intro 60.0%, discussion 55.1%, methods 6.1%; 44% behind descriptive abstracts), the reader experiment (N = 1,105; 5.1/7; rewrite −0.4, note −0.5, AI −0.8), LLM amplification (34% → ~55–59%; careful prompt below baseline; GPT-4.1 3.1/7 yet 99.3% causal summaries), and the Isch vs. Rohrer discussion. The project slide adds a check of introductions, discussions and LLM drafts for causal verbs.
- **Caveats on Isch:** text and figure disagree on the careful-prompt rate (5.0% vs. ~15%); the classifier counts causal research questions as overreach; only 68% of elite-journal "cross-sectional" articles were strictly cross-sectional on manual review.

- **Case 4 replaced:** Fox News, a staggered rollout like the TV case, is replaced by elite colleges and earnings (Dale & Krueger 2002, *QJE*; 2014, *JHR*). Among students admitted to the same colleges, attending the more selective one did not raise earnings, except for low-income students. The design conditions on a proxy (the admission set), not randomization. The finding is contested (Hoxby). The Fox figures were removed; DellaVigna & Kaplan is no longer in the deck.
- **Cases made distinct:** Case 1 (social media) is now the reverse-causation case. Case 2 is now smoking and COVID in hospital studies, a collider (moved up from Part 4). News coverage (King et al. 2017) moves to Part 4's communication-designs slide, replacing Sesame Street, whose staggered-reception design repeated the TV case. The four cases cover reverse causation, a collider, a common cause, and selection into treatment.
- **Notation trimmed:** removed "Four averages, two observed," "Building the decomposition," and "Checking the equation on both tables." Part 3 now uses the baseline-difference idea in words. Ȳ notation is gone from the slides. Y₁/Y₀ remain in the Part 2 potential-outcomes tables.
