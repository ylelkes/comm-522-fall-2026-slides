# Week 2 seminar

`index.qmd` is the editable slide source and contains all speaker notes. The deck uses the Week 1 Reveal.js settings and theme, with navy-slide contrast adjustments. It has 51 slides and a 120-minute schedule including a five-minute break.

The sequence follows the explanatory task: establish the outcome → compare law-based and statistical accounts → test rivals with Semmelweis and the forum → break at 66 minutes → mechanisms, explanatory levels, alternatives, and stopping points → the final 18-minute workshop. States, events, and Elster’s event–event preference follow the turnout example, and Elster’s seven distinctions serve as a synthesis before the workshop.

Edit only `week-02/index.qmd` for slide content and speaker notes. From the `slides` directory, build both HTML slide versions and the instructor guide with:

```sh
python3 week-02/build.py
```

A full `quarto render` also synchronizes the notes automatically and renders both versions through the project configuration.

Outputs appear in `docs/week-02/`. The student `index.html` contains no speaker-note text: a Pandoc filter removes note blocks during rendering. The separate `with-notes.html` retains and displays the notes. `instructor-notes.html` provides a continuous reading view of the timetable and discussion notes. `with-notes.html` follows Week 1's notes-view presentation convention.

The synchronization script regenerates `with-notes.qmd` and `instructor-notes.qmd` from `index.qmd`; edit slide-specific notes in `index.qmd` to keep both companions aligned. General teaching-plan text lives in `sync-notes.py`.

The forum case and constructed statistics are hypothetical. The Semmelweis percentages and the turnout figure come from the assigned readings, with attribution in the slides and notes.

Both versions and the source QMD are public on GitHub. Removing notes from the student HTML does not make the separately published notes private.
