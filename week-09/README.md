# Week 9: Sampling, Selection, and Scope

Edit **index.qmd**. It is the source for the student slides, presenter slides, visible-notes deck, and instructor notes.

The deck has four parts: (1) four cases where credible evidence traveled badly; (2) building a text sample, using Bergstrom and West's selection logic; (3) scope, using Findley, Kikuta, and Denly's M-STOUT framework and Henrich, Heine, and Norenzayan's WEIRD critique; (4) the students' sampling plan.

Slides render in the order they appear in `index.qmd`. `add-transitions.lua` appends a "next slide" line to each slide's notes; `strip-speaker-notes.lua` removes notes from the student deck.

## Build

Run `python3 week-09/build.py` from the slides repository root.

Outputs:

- `docs/week-09/student.html` — student deck with notes and Speaker View removed
- `docs/week-09/presenter.html` — presentation with notes available in Speaker View
- `docs/week-09/with-notes.html` — slides with notes visible
- `docs/week-09/instructor-notes.html` — standalone instructor guide
