# Week 3 seminar

`index.qmd` is the editable slide source and contains all speaker notes. The deck reuses Week 1's Reveal.js settings and theme, with a teal accent swapped in for Week 2's rust so the weeks stay visually distinct. It has 44 slides (including the title slide) and a 120-minute schedule including a five-minute break.

The sequence teaches concept vocabulary and Gerring's six criteria of conceptualization (with a bad example diagnosed before each criterion is named) in the first half; after the break, Gerring's Strategies of Conceptualization (minimal/maximal/cumulative) and McLeod & Pan's Chaffee-based explication steps are taught side by side as two convergent answers to "how do you actually build a concept," then both are watched together, enacted, in Molina et al.'s (2019) explication of "fake news." All interactive prompts are whole-class discussion — no pair or small-group work.

Edit only `week-03/index.qmd` for slide content and speaker notes. From the `slides` directory, build both HTML slide versions and the instructor guide with:

```sh
python3 week-03/build.py
```

A full `quarto render` also synchronizes the notes automatically and renders both versions through the project configuration.

Outputs appear in `docs/week-03/`. The student `index.html` contains no speaker-note text: a Pandoc filter removes note blocks during rendering. The separate `with-notes.html` retains and displays the notes. `instructor-notes.html` provides a continuous reading view of the timetable and discussion notes.

The synchronization script regenerates `with-notes.qmd` and `instructor-notes.qmd` from `index.qmd`; edit slide-specific notes in `index.qmd` to keep both companions aligned. General teaching-plan text lives in `sync-notes.py`.

Gerring's democracy examples (Tables 5.1–5.4, Figure 5.1) and McLeod & Pan's television-viewing example (Figure 2.1, Table 2.2) are drawn directly from the assigned readings. The Molina et al. material (real news, false news, satire, and polarized content, with their indicator domains) is drawn from the assigned journal article; the paper's remaining four taxonomy categories (misreporting, commentary, persuasive information, citizen journalism) are not covered in this deck. The forum/tolerance example carries over from Week 2 as a hypothetical teaching case, not a reported study.

Both versions and the source QMD are public on GitHub. Removing notes from the student HTML does not make the separately published notes private.

The post-render script removes the RevealNotes plugin and Speaker View menu entry from the student deck, and creates `docs/week-03/student.html` as an explicit student link. Both student URLs contain the same note-free presentation.

`presenter.html` is the plain presentation: notes stay off the main slides, but pressing **S** opens Speaker View with notes. `student.html` removes notes entirely; `with-notes.html` displays them on the main page. All three are generated from `index.qmd` by `python3 week-03/build.py`.
