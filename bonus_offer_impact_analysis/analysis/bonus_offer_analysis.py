"""Bonus offer impact analysis.

Generates synthetic user-level data to simulate a bonus campaign impact,
computes KPI lift, and visualizes the results.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
OUTPUT_DATA_PATH = DATA_DIR / "bonus_offer_data.csv"
OUTPUT_CHART_PATH = REPORTS_DIR / "bonus_offer_uplift.png"


@dataclass
class LiftMetrics:
    """Holds lift metrics for a KPI."""

    control: float
    bonus: float

    @property
    def absolute_lift(self) -> float:
        return self.bonus - self.control

    @property
    def relative_lift(self) -> float:
        if math.isclose(self.control, 0.0):
            return math.inf
        return (self.bonus - self.control) / self.control


def generate_synthetic_data(seed: int = 42, user_count: int = 2000) -> pd.DataFrame:
    """Create a synthetic dataset representing control vs. bonus exposure."""

    rng = np.random.default_rng(seed)
    user_ids = np.arange(1, user_count + 1)

    groups = np.array(["control", "bonus"])
    assignments = rng.choice(groups, size=user_count, p=[0.5, 0.5])

    # Control users have a lower deposit frequency and spend per deposit
    base_deposits = rng.poisson(lam=2.2, size=user_count)
    bonus_multiplier = np.where(assignments == "bonus", 1.35, 1.0)
    deposits_count = np.maximum(0, np.round(base_deposits * bonus_multiplier + rng.normal(0, 0.5, user_count))).astype(int)

    # Total revenue is correlated with deposits and includes variability per user.
    avg_ticket_control = 45
    avg_ticket_bonus_uplift = 1.15
    avg_ticket = np.where(assignments == "bonus", avg_ticket_control * avg_ticket_bonus_uplift, avg_ticket_control)

    total_revenue = deposits_count * avg_ticket * rng.lognormal(mean=0, sigma=0.35, size=user_count)

    df = pd.DataFrame(
        {
            "user_id": user_ids,
            "group": assignments,
            "deposits_count": deposits_count,
            "total_revenue": total_revenue,
        }
    )

    return df


def compute_group_metrics(df: pd.DataFrame) -> Dict[str, LiftMetrics]:
    """Compute group-level metrics and lift between control and bonus."""

    grouped = df.groupby("group").agg(
        deposits_per_user=("deposits_count", "mean"),
        arpu=("total_revenue", "mean"),
    )

    control_metrics = grouped.loc["control"]
    bonus_metrics = grouped.loc["bonus"]

    return {
        "deposits_per_user": LiftMetrics(
            control=float(control_metrics["deposits_per_user"]),
            bonus=float(bonus_metrics["deposits_per_user"]),
        ),
        "arpu": LiftMetrics(
            control=float(control_metrics["arpu"]),
            bonus=float(bonus_metrics["arpu"]),
        ),
    }


def build_summary_table(metrics: Dict[str, LiftMetrics]) -> pd.DataFrame:
    """Construct a summary table with lift calculations."""

    records = []
    for metric_name, metric_values in metrics.items():
        records.append(
            {
                "metric": metric_name,
                "group": "control",
                "value": metric_values.control,
                "absolute_lift": 0.0,
                "relative_lift_pct": 0.0,
            }
        )
        records.append(
            {
                "metric": metric_name,
                "group": "bonus",
                "value": metric_values.bonus,
                "absolute_lift": metric_values.absolute_lift,
                "relative_lift_pct": metric_values.relative_lift * 100,
            }
        )

    summary_df = pd.DataFrame(records)
    return summary_df


def plot_metrics(summary_df: pd.DataFrame) -> None:
    """Create and save a side-by-side bar chart with lift annotations."""

    pivot_df = summary_df.pivot(index="metric", columns="group", values="value")
    melted = summary_df[["metric", "group", "value"]]

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(
        data=melted,
        x="metric",
        y="value",
        hue="group",
        hue_order=["control", "bonus"],
        palette=["#4C72B0", "#55A868"],
    )
    ax.set_title("Bonus Offer Impact on Deposits and Revenue")
    ax.set_ylabel("Value")
    ax.set_xlabel("Metric")

    # Annotate relative lift for each metric above the bonus bar.
    for i, metric in enumerate(pivot_df.index):
        control_val = pivot_df.loc[metric, "control"]
        bonus_val = pivot_df.loc[metric, "bonus"]
        relative_pct = (bonus_val - control_val) / control_val * 100 if control_val else float("inf")
        bonus_bar = ax.patches[i * 2 + 1]
        ax.text(
            bonus_bar.get_x() + bonus_bar.get_width() / 2,
            bonus_bar.get_height() + max(pivot_df.loc[metric]) * 0.05,
            f"+{relative_pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#2F4F4F",
            fontweight="bold",
        )

    ax.legend(title="Group")
    plt.tight_layout()
    plt.savefig(OUTPUT_CHART_PATH, dpi=300)
    plt.close()


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ensure_directories()

    df = generate_synthetic_data()
    df.to_csv(OUTPUT_DATA_PATH, index=False)

    metrics = compute_group_metrics(df)
    summary_df = build_summary_table(metrics)

    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    print("\nBonus Offer KPI Summary:\n")
    print(summary_df)

    plot_metrics(summary_df)


if __name__ == "__main__":
    main()
