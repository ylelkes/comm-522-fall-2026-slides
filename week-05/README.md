# Week 5: Measurement Error, Reliability, and Fairness

Edit **index.qmd**. It is the source for the slides and all speaker notes.

51 teaching slides plus the title slide. The deck introduces each of the four perils of quantification before moving to the true-score equation and fairness in measurement, introduces reliability and validity with a dartboard analogy, introduces Toshkov's levels of measurement before applying them to measurement error in Lauderdale ch. 3, works through Semetko & Valkenburg and Burla et al. as content-analysis cases, and returns to fairness formally (separation/sufficiency) with Lauderdale's ch. 4 examples.

## Readings and coverage

| Reading | Material | Where |
|---|---|---|
| Lauderdale ch. 1, pp. 29–31 | Fairness as measurement error; comparative/noncomparative; SAT and teacher examples | Opening fairness section |
| Lauderdale §§4.1–4.2, pp. 99–102 | Bedtime example; treat likes alike; Hellman's four noncomparative critiques | Opening fairness section |
| Lauderdale §§3.1–3.2, pp. 63–72 | Error by level; δ/γ/η decomposition; MSE; CTT reliability; confusion matrix; Se/Sp/PPV/NPV | Measurement error section |
| Lauderdale §§3.3–3.6, pp. 72–88 | Gold/silver/no benchmark; correlated errors; parallel measurement; ICR metrics (Table 3.1); validity evidence (Table 3.2) | Benchmarks and validity |
| Lauderdale §§3.7–3.9, pp. 89–97 | NHANES height/weight and cotinine applications; three overclaims | Applications; closing |
| Lauderdale §§4.3–4.6, pp. 102–113 | Separation, sufficiency, impossibility; COMPAS; predicted A-levels | Formal fairness section |
| Semetko & Valkenburg (2000) | Frame concept; 20-item instrument; ICR, PCA, KR-20; claims | Content analysis case; cross-media comparison |
| Burla et al. (2008) | Codebook development; κ = .67; code-level diagnostics; limits | Content analysis case |

## Conventions

- Figures cropped from the assigned PDFs: `lauderdale-figure-3-3.png` (p. 89), `lauderdale-figure-4-1.png` (p. 105), `lauderdale-figure-4-2-school.png` and `-race.png` (p. 110), `semetko-table-1.png` (article p. 100).
- Invented examples, labeled on slides: self-reported social media minutes (δ = −30, γ = ±20, η = ±5), the kappa table, and the toxicity classifier.

## Build

```sh
python3 week-05/build.py
```

Re-extract figures (set `L` to Lauderdale's PDF and `S` to the Semetko PDF):

```sh
pdftoppm -f 89 -l 89 -singlefile -r 300 -x 250 -y 250 -W 2100 -H 950 -png "$L" week-05/assets/lauderdale-figure-3-3
pdftoppm -f 105 -l 105 -singlefile -r 300 -x 250 -y 250 -W 2100 -H 720 -png "$L" week-05/assets/lauderdale-figure-4-1
pdftoppm -f 110 -l 110 -singlefile -r 300 -x 280 -y 945 -W 1400 -H 700 -png "$L" week-05/assets/lauderdale-figure-4-2-school
pdftoppm -f 110 -l 110 -singlefile -r 300 -x 280 -y 2245 -W 1400 -H 640 -png "$L" week-05/assets/lauderdale-figure-4-2-race
pdftoppm -f 8 -l 8 -singlefile -r 200 -x 130 -y 160 -W 1160 -H 1650 -png "$S" week-05/assets/semetko-table-1
```
