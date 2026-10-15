"""Data generation, validation, analysis and reporting helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "student_id", "year", "average_mark", "happiness_score", "study_hours",
    "sleep_hours", "attendance_rate", "stress_score", "financial_pressure",
}


def create_synthetic_dataset(seed: int = 42, students_per_year: int = 120) -> pd.DataFrame:
    """Create a deterministic, clearly labelled teaching dataset.

    Values are simulated; they are not evidence about real students. The data
    has plausible relationships to make the full workflow demonstrable.
    """
    rng = np.random.default_rng(seed)
    years = np.repeat(np.arange(2022, 2027), students_per_year)
    size = len(years)
    sleep = np.clip(rng.normal(7.0, 0.9, size), 4, 10)
    study = np.clip(rng.normal(14, 5, size), 1, 35)
    attendance = np.clip(rng.normal(78, 12, size), 35, 100)
    pressure = np.clip(rng.normal(5.4, 2.1, size), 0, 10)
    stress = np.clip(4.8 + pressure * 0.42 - sleep * 0.24 + rng.normal(0, 1.25, size), 0, 10)
    happiness = np.clip(73 + sleep * 2.3 - stress * 3.1 - pressure * 1.2 + rng.normal(0, 8, size), 20, 100)
    marks = np.clip(31 + study * 1.12 + attendance * 0.26 + happiness * 0.12 - stress * 0.7 + rng.normal(0, 7, size), 0, 100)
    return pd.DataFrame({
        "student_id": [f"S{index:04d}" for index in range(1, size + 1)],
        "year": years,
        "average_mark": marks.round(1),
        "happiness_score": happiness.round(1),
        "study_hours": study.round(1),
        "sleep_hours": sleep.round(1),
        "attendance_rate": attendance.round(1),
        "stress_score": stress.round(1),
        "financial_pressure": pressure.round(1),
    })


def validate_dataset(data: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    if data.empty:
        raise ValueError("Dataset has no observations.")
    if data["student_id"].duplicated().any():
        raise ValueError("student_id values must be unique.")
    bounded = {"average_mark": (0, 100), "happiness_score": (0, 100), "attendance_rate": (0, 100), "stress_score": (0, 10), "financial_pressure": (0, 10)}
    for column, (minimum, maximum) in bounded.items():
        if not data[column].between(minimum, maximum).all():
            raise ValueError(f"{column} must be between {minimum} and {maximum}.")


def load_or_create_dataset(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.exists():
        data = pd.read_csv(path)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = create_synthetic_dataset()
        data.to_csv(path, index=False)
    validate_dataset(data)
    return data


def analyse(data: pd.DataFrame) -> dict:
    validate_dataset(data)
    x = data["happiness_score"].to_numpy(dtype=float)
    y = data["average_mark"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    residuals = y - predicted
    r_squared = 1 - np.sum(residuals ** 2) / np.sum((y - y.mean()) ** 2)
    yearly = data.groupby("year", as_index=False).agg(
        average_mark=("average_mark", "mean"), happiness_score=("happiness_score", "mean"),
        average_sleep=("sleep_hours", "mean"), average_stress=("stress_score", "mean"), observations=("student_id", "count"),
    )
    return {
        "sample_size": len(data), "correlation": float(np.corrcoef(x, y)[0, 1]),
        "slope": float(slope), "intercept": float(intercept), "r_squared": float(r_squared),
        "yearly": yearly, "predicted": predicted, "residuals": residuals,
    }


def write_summary(results: dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yearly_table = markdown_table(results["yearly"].round(2))
    output_path.write_text(
        "# Average Mark vs Happiness — Analysis Summary\n\n"
        f"- **Sample:** {results['sample_size']} simulated student-year observations\n"
        f"- **Pearson correlation:** {results['correlation']:.3f}\n"
        f"- **Linear-model slope:** {results['slope']:.3f} mark points per happiness point\n"
        f"- **R²:** {results['r_squared']:.3f}\n\n"
        "## Yearly descriptive statistics\n\n" + yearly_table + "\n\n"
        "## Interpretation\n\n"
        "The association shown here is descriptive only. The bundled dataset is synthetic and deliberately constructed for teaching and portfolio demonstration; it cannot support claims about real students or causality. A real study would require ethics approval, validated measures, representative sampling and controls for confounders.\n",
        encoding="utf-8",
    )


def markdown_table(data: pd.DataFrame) -> str:
    """Render a small DataFrame as Markdown without optional dependencies."""
    headers = [str(column) for column in data.columns]
    rows = [[str(value) for value in row] for row in data.itertuples(index=False, name=None)]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)
