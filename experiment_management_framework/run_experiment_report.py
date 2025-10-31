#!/usr/bin/env python3
"""Experiment Management Framework reporting script.

This script loads experiment results from a CSV file, evaluates success rates,
calculates average Return on Time Invested (ROTI) by experiment metric, and
prints a concise report sorted by ROTI descending.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import pandas as pd

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:  # pragma: no cover - matplotlib optional
    plt = None  # type: ignore


def load_experiments(csv_path: Path) -> pd.DataFrame:
    """Load experiment data from a CSV file and ensure proper types."""
    df = pd.read_csv(csv_path)
    df["p_value"] = pd.to_numeric(df["p_value"], errors="coerce")
    df["ROTI_score"] = pd.to_numeric(df["ROTI_score"], errors="coerce")
    return df


def compute_success_failure_rate(df: pd.DataFrame) -> Tuple[float, float]:
    """Compute success and failure rates based on the decision column.

    Decisions marked as "Ship" are treated as successes. All other decisions are
    counted as failures for the purpose of the summary rate.
    """
    total = len(df)
    if total == 0:
        return 0.0, 0.0
    success_count = (df["decision"].str.lower() == "ship").sum()
    failure_count = total - success_count
    success_rate = success_count / total
    failure_rate = failure_count / total
    return success_rate, failure_rate


def average_roti_by_metric(df: pd.DataFrame) -> pd.Series:
    """Return the average ROTI score for each experiment metric."""
    return df.groupby("metric")["ROTI_score"].mean().sort_values(ascending=False)


def build_report(df: pd.DataFrame) -> str:
    """Create a text report for the experiments sorted by ROTI descending."""
    success_rate, failure_rate = compute_success_failure_rate(df)
    avg_roti = average_roti_by_metric(df)
    sorted_df = df.sort_values("ROTI_score", ascending=False)

    lines = [
        "Experiment Portfolio Summary",
        "-----------------------------",
        f"Total Experiments: {len(df)}",
        f"Success Rate (Ship decisions): {success_rate:.0%}",
        f"Failure Rate (non-Ship decisions): {failure_rate:.0%}",
        "",
        "Average ROTI by Metric:",
    ]

    for metric, roti in avg_roti.items():
        lines.append(f"  - {metric}: {roti:.2f}")

    lines.extend([
        "",
        "Experiments Sorted by ROTI (High to Low):",
    ])

    for _, row in sorted_df.iterrows():
        lines.append(
            "  - {id}: {hypothesis} | Metric: {metric} | ROTI: {roti:.1f} | Decision: {decision} | Next: {next}".format(
                id=row["experiment_id"],
                hypothesis=row["hypothesis"],
                metric=row["metric"],
                roti=row["ROTI_score"],
                decision=row["decision"],
                next=row["next_action"],
            )
        )

    return "\n".join(lines)


def maybe_plot_roti(avg_roti: pd.Series, output_path: Path | None) -> None:
    """Optionally create a bar chart of average ROTI by metric."""
    if plt is None or output_path is None:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    avg_roti.sort_values().plot.barh(ax=ax, color="#2b8cbe")
    ax.set_xlabel("Average ROTI Score")
    ax.set_ylabel("Metric")
    ax.set_title("Average ROTI by Experiment Metric")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an experiment portfolio report.")
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",
        default=Path(__file__).with_name("experiments.csv"),
        help="Path to the experiments CSV file.",
    )
    parser.add_argument(
        "--plot",
        type=Path,
        default=None,
        help="Optional path to save a bar chart of average ROTI by metric.",
    )
    args = parser.parse_args()

    df = load_experiments(args.csv_path)
    report = build_report(df)
    print(report)

    if args.plot is not None:
        maybe_plot_roti(average_roti_by_metric(df), args.plot)


if __name__ == "__main__":
    main()

