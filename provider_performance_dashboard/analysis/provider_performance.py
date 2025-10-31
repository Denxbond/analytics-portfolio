"""Provider performance dashboard analysis.

This script simulates provider-level gaming performance data, calculates
contribution metrics, and creates summary visualizations for product mix
optimization.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
CSV_PATH = DATA_DIR / "synthetic_provider_stats.csv"
CHART_PATH = REPORTS_DIR / "provider_performance_chart.png"


def simulate_provider_data(num_providers: int = 50, random_state: int = 42) -> pd.DataFrame:
    """Create a synthetic dataset that mimics provider-level performance metrics.

    Parameters
    ----------
    num_providers:
        Number of unique providers to generate metrics for.
    random_state:
        Random seed for reproducibility.
    """

    rng = np.random.default_rng(random_state)

    provider_ids = [f"provider_{i:03d}" for i in range(1, num_providers + 1)]
    games_count = rng.integers(10, 120, size=num_providers)
    unique_players = rng.integers(500, 20000, size=num_providers)
    total_bets = rng.uniform(5e5, 8e6, size=num_providers)

    # Assume payout ratios vary across providers, influencing total wins.
    payout_ratio = rng.uniform(0.85, 0.98, size=num_providers)
    total_wins = total_bets * payout_ratio

    # Revenue as the difference between total bets and total wins (gross gaming revenue).
    revenue = total_bets - total_wins

    # Retention rate influenced by game mix, capped between 0.2 and 0.75.
    retention_rate = np.clip(
        rng.normal(loc=0.45, scale=0.1, size=num_providers)
        + (games_count - games_count.mean()) / (games_count.std() * 50),
        0.2,
        0.75,
    )

    data = pd.DataFrame(
        {
            "provider_id": provider_ids,
            "games_count": games_count,
            "unique_players": unique_players,
            "total_bets": total_bets,
            "total_wins": total_wins,
            "revenue": revenue,
            "retention_rate": retention_rate,
        }
    )

    return data


def compute_contribution_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate GGR share for each provider and sort descending."""

    df = df.copy()
    total_revenue = df["revenue"].sum()
    df["ggr_share"] = df["revenue"] / total_revenue

    # Sort providers descending by share to highlight biggest contributors first.
    df.sort_values("ggr_share", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def plot_top_providers(df: pd.DataFrame, output_path: pathlib.Path) -> None:
    """Create a bar chart showing the top providers by revenue and retention."""

    sns.set_theme(style="whitegrid")

    top_revenue = df.nlargest(10, "revenue")
    top_retention = df.nlargest(10, "retention_rate")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.barplot(
        data=top_revenue,
        x="revenue",
        y="provider_id",
        palette="Blues_d",
        ax=axes[0],
    )
    axes[0].set_title("Top 10 Providers by Revenue")
    axes[0].set_xlabel("Revenue (Gross Gaming Revenue)")
    axes[0].set_ylabel("Provider")

    sns.barplot(
        data=top_retention,
        x="retention_rate",
        y="provider_id",
        palette="Greens_d",
        ax=axes[1],
    )
    axes[1].set_title("Top 10 Providers by Retention")
    axes[1].set_xlabel("Retention Rate")
    axes[1].set_ylabel("Provider")

    fig.suptitle("Provider Performance Overview", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = simulate_provider_data()
    df = compute_contribution_metrics(df)
    df.to_csv(CSV_PATH, index=False)

    plot_top_providers(df, CHART_PATH)

    print(f"Saved synthetic dataset to {CSV_PATH}")
    print(f"Saved performance chart to {CHART_PATH}")


if __name__ == "__main__":
    main()
