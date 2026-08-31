# COMM 5220 — Fall 2026 Slides

Quarto and Reveal.js slides organized as a multi-week GitHub Pages site.

## Structure

```text
slides/
├── _quarto.yml
├── index.qmd
├── week-01/
│   ├── index.qmd
│   └── week1-seminar.scss
└── docs/
```

Add future decks in `week-02/`, `week-03/`, and so on. Each week should contain its own `index.qmd` and any week-specific assets or theme files. Add a link to the course landing page in the root `index.qmd`.

## Build locally

```sh
quarto render
```

The rendered GitHub Pages site is written to `docs/`. Within a Reveal.js presentation, press `S` for speaker view and notes.
