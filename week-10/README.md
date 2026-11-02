# Week 10: Causality: Counterfactuals, Selection, and DAGs

Edit **index.qmd**. It is the source for the student slides, presenter slides, visible-notes deck, and instructor notes. The lecture plan is in **outline.md**.

The deck has five parts: (1) four communication claims that invite causal readings, each with a design that tested it (social media and depression, smoking and COVID, TV and test scores, elite colleges and earnings); (2) potential outcomes (TCD ch. 3; HRT); (3) how selection into treatment creates bias (TCD ch. 9; Preuss, elite colleges, police and crime, signing the bias); (4) Rohrer's DAGs (building blocks, back doors, control by design, when control hurts); (5) the opening cases redrawn, fever, Isch et al. (2026) on causal overclaiming and LLM amplification, and the coding projects. Interactive simulations live in `goop-simulation.html` and `lottery-simulation.html`.

Figures generated for this week (DAGs, simulations, HRT plot) come from `make-figures.py`; rerun it after editing a figure. Figures from the readings are copied into `assets/`.

## Build

Run `python3 week-10/build.py` from the slides repository root.

Outputs:

- `docs/week-10/student.html` — student deck with notes and Speaker View removed
- `docs/week-10/presenter.html` — presentation with notes available in Speaker View
- `docs/week-10/with-notes.html` — slides with notes visible
- `docs/week-10/instructor-notes.html` — standalone instructor guide
