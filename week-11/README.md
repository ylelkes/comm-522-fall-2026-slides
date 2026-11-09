# Week 11: Experiments, from DAGs to Design

Edit **index.qmd**. It is the source for the student slides, presenter slides, visible-notes deck, and instructor notes. The lecture plan is in **outline.md**.

The deck has five parts: (1) a compact Week 10 DAG recap using the selective-college running example, including a dedicated verbal explanation of why conditioning on a collider opens a path and adjacent mediation/moderation slides; (2) Druckman's experiment vocabulary, with explicit distinctions among random assignment, population coverage, and precision, plus translated typology/validity tables and a qualified transportability argument; (3) an expanded Correll, Benard, and Paik (2007) case that distinguishes the population wage-gap puzzle from the randomized parental-status-signal estimand and makes both the lab and field-audit procedures visible; (4) Craig and Richeson (2014/2015), rebuilt around the narrower message-exposure estimand, exact treatments/outcomes, calibrated corrected evidence, measured mediation, and an experimental manipulation of the proposed mechanism; and (5) synthesis and the project tie-in. Fourteen advanced or backup slides remain in `index.qmd` with `visibility="hidden"`. The interactive widget lives in `open-closed-simulation.html`.

Figures generated for this week (the case-specific DAGs for Parts 2–4, and the assumption-violation DAGs) come from `make-figures.py`; rerun it after editing a figure. Figures extracted from the three readings, plus one reused Week 10 figure (Rohrer's Figure 3), are in `assets/`.

## Build

Run `python3 week-11/build.py` from the slides repository root.

Outputs:

- `docs/week-11/student.html` — student deck with notes and Speaker View removed
- `docs/week-11/presenter.html` — presentation with notes available in Speaker View
- `docs/week-11/with-notes.html` — slides with notes visible
- `docs/week-11/instructor-notes.html` — standalone instructor guide
