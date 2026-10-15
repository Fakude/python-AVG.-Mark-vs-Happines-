"""Run the complete Average Mark vs Happiness analysis."""

from pathlib import Path

from src.analysis import analyse, load_or_create_dataset, write_summary
from src.visualise import create_figures


ROOT = Path(__file__).parent


def main() -> None:
    data = load_or_create_dataset(ROOT / "data" / "student_wellbeing.csv")
    results = analyse(data)
    create_figures(data, results, ROOT / "outputs")
    write_summary(results, ROOT / "outputs" / "summary.md")
    print(f"Analysed {results['sample_size']} student-year observations.")
    print(f"Pearson correlation: {results['correlation']:.3f}")
    print(f"OLS slope: {results['slope']:.3f} marks per happiness point")
    print("Outputs written to outputs/")


if __name__ == "__main__":
    main()
