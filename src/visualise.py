"""Publication-ready visualisations for the analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_figures(data: pd.DataFrame, results: dict, output_directory: str | Path) -> None:
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), constrained_layout=True)
    scatter = axes[0].scatter(data["happiness_score"], data["average_mark"], c=data["stress_score"], cmap="viridis", alpha=.72, edgecolor="white", linewidth=.25)
    order = np.argsort(data["happiness_score"].to_numpy())
    axes[0].plot(data["happiness_score"].to_numpy()[order], np.asarray(results["predicted"])[order], color="#db5a42", linewidth=2.5, label="OLS trend")
    axes[0].set(title="Marks and happiness", xlabel="Happiness score (0–100)", ylabel="Average mark (0–100)")
    axes[0].legend(frameon=False)
    fig.colorbar(scatter, ax=axes[0], label="Stress score")
    yearly = results["yearly"]
    axes[1].plot(yearly["year"], yearly["average_mark"], marker="o", linewidth=2.5, color="#355c7d", label="Average mark")
    axes[1].plot(yearly["year"], yearly["happiness_score"], marker="o", linewidth=2.5, color="#c06c84", label="Happiness score")
    axes[1].set(title="Yearly averages", xlabel="Year", ylabel="Average score")
    axes[1].set_xticks(yearly["year"])
    axes[1].legend(frameon=False)
    fig.suptitle("Student wellbeing case study (synthetic data)", fontsize=16, fontweight="bold")
    fig.savefig(output_directory / "wellbeing_analysis.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
