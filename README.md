# Average Mark vs Happiness

A reproducible data-science case study investigating the association between academic performance and self-reported happiness. It develops the original single chart into an end-to-end analysis pipeline with validation, exploratory visualisation, linear modelling, testing and responsible reporting.

> **Data note:** The project generates a deterministic synthetic dataset for teaching and portfolio demonstration. It is not a study of real students and must not be used to make causal or population-level claims.

## Research question

Within a simulated student dataset, how is happiness associated with average academic mark, and how do related variables such as sleep, attendance, stress and financial pressure contextualise that relationship?

## Method

1. Generate or load a documented dataset with one record per student-year.
2. Validate required columns, unique IDs and sensible score bounds.
3. Calculate descriptive statistics and yearly aggregates.
4. Estimate Pearson correlation and an ordinary least squares trend.
5. Save a figure and a transparent Markdown summary.

The model is descriptive. Confounding, reverse causation and selection bias remain possible even with genuine observational data.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run_analysis.py
```

The first run creates `data/student_wellbeing.csv`. It then writes `outputs/wellbeing_analysis.png` and `outputs/summary.md`.

## Test

```bash
python -m unittest discover -s tests -v
```

## Structure

```text
src/analysis.py    data generation, validation, analysis and report writing
src/visualise.py   charts
tests/             deterministic unit tests
run_analysis.py    reproducible pipeline entry point
```
