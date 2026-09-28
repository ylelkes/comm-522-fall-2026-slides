# Week 4: From Concepts to Measures

Edit **index.qmd**. It is the source for the slides and all speaker notes.

The deck contains 51 teaching slides plus the title slide. It opens with Week 3 review followed by a consolidated Paxton case, including the historical figures and welfare application. An explicit transition then introduces social media use as the main working example for measurement instruction. Gerring and Lauderdale's democracy examples remain where they teach specific conceptual and scale distinctions. Activities are whole-class discussions. There is no teaching-time metadata or timing validation.

## Readings and coverage

Page numbers are printed pages in the supplied PDFs.

| Reading | Material covered | Where it appears |
|---|---|---|
| Lauderdale, ch. 1, §§1.1–1.3, pp. 17–25 | Measurement as scientific inference; theory and instruments developing together; population/causal/measurement inference; representational and pragmatic perspectives | Opening framework; thermometer discussion in notes; perspectives and procedural-definition discussion |
| Lauderdale, ch. 1, §§1.4–1.5, pp. 25–40 | Value of quantification; narrowness, fairness, unintended consequences, malign intentions; responsible use | Description and quantification section; four perils and follow-up slides |
| Lauderdale, ch. 2 opening and §§2.1–2.3, pp. 41–49 | Generative/discriminative concepts; target and estimate; bent coin; indicators; proxies and calibration | Concept–measure section; original Figures 2.1–2.2 on separate slides; Figure 2.3 in instructor notes with a plain-language comparison on the slide; coin and heavy-use examples; proxy slide |
| Lauderdale, §§2.4–2.6, pp. 49–52 | Theory/supervised/unsupervised mapping; minimal/maximal scope; levels of measurement | Mapping table; scope discussion; scales and arithmetic exercise |
| Lauderdale, §2.7–2.8, pp. 52–61 | DD and V-Dem ambitions; binary/ordinal/interval-ratio choices; lexical scale; tradeoffs in composite scores | Democracy comparisons; graded scales, full lexical hierarchy, aggregation and profiles |
| Toshkov, selected material from pp. 107–116 | Measurement/classing; dimensions, variables and recorded values; levels of measurement | Dimension/subdimension hierarchy and figure; table of indicators within each activity type; scales section |
| Toshkov, pp. 119–122 | Observation strategies; party positions from experts, texts, and votes; theory in measurement | Sources table and the party-position slide |
| Paxton, pp. 92–111 | Definition/operationalization mismatch; suffrage as necessary but insufficient; changes to dates, duration, waves, and causal accounts; graded measures and their limitations | Recurring empirical thread; reported dates and counts; synthesis |

Deferred as requested: case design, levels of analysis, sampling, distributions, networks, and broader descriptive methods. Twelve slides and their notes are preserved in `deferred-toshkov-topics.md`, outside the deck and build, for a later week. The brief distinction between measurement, population, and causal inference remains because it is part of Lauderdale's definition of measurement; it does not introduce sampling methods. Reliability, validity, and formal measurement-error analysis also remain deferred, including Toshkov pp. 117–119 and Lauderdale's later chapters. Fairness remains a conceptual/normative discussion; no error taxonomy is taught. Technical algorithms are introduced at the depth of the assigned chapters, not taught as separate statistical methods.

## Source and example conventions

- Lauderdale references use the supplied September 15, 2026 draft.
- Paxton's recoding illustrates the consequences of including women. It is **not** a definitive new dating of full democracy. Source-reported dates are labeled accordingly; other restrictions and institutional requirements remain relevant.
- `assets/paxton-waves.svg` replots the counts reported on Paxton pp. 100–102. The periodization also changes; these are not fixed-bin counts or a new country-level replication.
- All social media definitions, records, and numerical examples are hypothetical teaching constructions. Social media **use** remains the main concept, with activity types kept as dimensions or explicitly narrower targets.
- `assets/lauderdale-figure-2-1.png`, `lauderdale-figure-2-2.png`, and `lauderdale-figure-2-3.png` reproduce the original diagrams from the assigned PDF, pp. 43–44. Notes explain the symbols, the unspecified relationship in 2.2, and the defining rather than behavioral-causal interpretation of the arrow in 2.3.
- `assets/use-distributions.svg` is retained for the deferred material only. It uses invented data: [30, 30, 30, 30, 30] and [0, 0, 10, 20, 120].

## Build

From the repository root:

```sh
python3 week-04/build.py
```

This synchronizes notes and renders student, presenter, visible-notes, and continuous instructor-guide versions into `docs/week-04/`. Project hooks also synchronize other existing weeks, as in the current repository setup. The student deck has no speaker notes or presenter controls.

To regenerate source views without rendering:

```sh
python3 week-04/sync-notes.py
```

To recreate the two chart assets, with matplotlib installed:

```sh
python3 week-04/make-figures.py
```

Edit `index.qmd`, not the generated `presenter.qmd`, `with-notes.qmd`, `instructor-notes.qmd`, or HTML files.

## Re-extracting Lauderdale's figures

The following commands crop the diagrams directly from the supplied PDF, preserving its original notation. Run from the repository root after setting `reading_pdf` to the assigned file's path:

```sh
pdftoppm -f 43 -l 43 -singlefile -scale-to 4800 -x 2460 -y 2445 -W 876 -H 876 -png "$reading_pdf" week-04/assets/lauderdale-figure-2-1
pdftoppm -f 44 -l 44 -singlefile -scale-to 4800 -x 2460 -y 570 -W 876 -H 876 -png "$reading_pdf" week-04/assets/lauderdale-figure-2-2
pdftoppm -f 44 -l 44 -singlefile -scale-to 4800 -x 2460 -y 1917 -W 876 -H 876 -png "$reading_pdf" week-04/assets/lauderdale-figure-2-3
```

The original classroom diagram `assets/social-media-use-hierarchy.svg` organizes use by activity type, then duration and frequency within each type. Its branches are conceptual, not causal.

## Expanded Paxton case

The deck includes the original Figures 1 and 2 (pp. 99 and 101), each followed by enlarged lower rows with the original headings repeated. Complete figures provide context; detail views support reading the country trajectories. The existing chart still summarizes Paxton's reported counts.

Four welfare-application slides distinguish democracy as a proposed cause from democracy as an outcome. A six-country school-completion dataset is wholly hypothetical. Recoding two countries changes the descriptive difference from 30 percentage points to zero; this is not Paxton's empirical result or a causal estimate. A separate invented 1910 welfare event shows how the reported 1870/1920 starting dates change the before–after interpretation. Notes also acknowledge Paxton's actual report in note 16 that recoding strengthened Muller's results.

The Paxton sequence introduces Huntington’s wave/reverse-wave argument before the figures and contrasts it with Paxton’s interpretation afterward. Notes explain why recoding can remove apparent reversals as well as delay transitions, and bound the challenge to the historical periodization.
