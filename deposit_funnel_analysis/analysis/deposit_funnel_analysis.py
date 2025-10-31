"""Deposit Funnel Analysis.

This script generates synthetic event-level data for a casino onboarding funnel
and produces funnel conversion metrics and a corresponding visualization.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FunnelStep:
    """Represents a step in the funnel with a probability to advance."""

    name: str
    advance_probability: float
    min_delay_minutes: int
    max_delay_minutes: int


class DepositFunnelAnalysis:
    """Encapsulates the logic for generating and analyzing funnel data."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.data_path = base_dir / "data" / "synthetic_funnel_events.csv"
        self.report_path = base_dir / "reports" / "funnel_dropoff_chart.png"
        self.random_state = np.random.RandomState(42)
        self.funnel_steps: List[FunnelStep] = [
            FunnelStep("landing", 1.0, 0, 0),
            FunnelStep("registration", 0.72, 1, 45),
            FunnelStep("deposit_form", 0.58, 3, 60),
            FunnelStep("deposit_success", 0.65, 1, 30),
        ]

    def generate_synthetic_events(self, n_users: int = 1200) -> pd.DataFrame:
        """Create synthetic funnel events with realistic timestamps."""
        base_timestamp = pd.Timestamp("2024-03-01 09:00:00")
        users = [f"user_{idx:04d}" for idx in range(1, n_users + 1)]
        events: List[Dict[str, object]] = []

        for user_id in users:
            timestamp = base_timestamp + pd.to_timedelta(
                self.random_state.uniform(0, 72), unit="h"
            )
            progressed = True

            for idx, step in enumerate(self.funnel_steps):
                if idx == 0:
                    # Landing step always occurs.
                    events.append({
                        "user_id": user_id,
                        "step": step.name,
                        "timestamp": timestamp,
                    })
                    continue

                if not progressed:
                    break

                if self.random_state.rand() <= step.advance_probability:
                    delay_minutes = self.random_state.randint(
                        step.min_delay_minutes, step.max_delay_minutes + 1
                    )
                    timestamp = timestamp + pd.to_timedelta(delay_minutes, unit="m")
                    events.append({
                        "user_id": user_id,
                        "step": step.name,
                        "timestamp": timestamp,
                    })
                else:
                    progressed = False

        df = pd.DataFrame(events).sort_values("timestamp").reset_index(drop=True)
        return df

    def save_events(self, events: pd.DataFrame) -> None:
        """Persist synthetic events to the data directory."""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        events.to_csv(self.data_path, index=False)

    def compute_funnel_metrics(self, events: pd.DataFrame) -> pd.DataFrame:
        """Aggregate conversion and drop-off metrics across the funnel."""
        step_order = [step.name for step in self.funnel_steps]
        users_per_step = (
            events.groupby("step")["user_id"].nunique().reindex(step_order, fill_value=0)
        )

        conversion = users_per_step / users_per_step.iloc[0] * 100
        dropoff = conversion.shift(1) - conversion
        progression_ratio = users_per_step / users_per_step.shift(1)
        dropoff_rate = (1 - progression_ratio) * 100

        metrics = pd.DataFrame(
            {
                "users": users_per_step,
                "conversion_pct": conversion.round(2),
                "dropoff_pct_points": dropoff.round(2),
                "dropoff_rate_pct": dropoff_rate.round(2),
            }
        )
        metrics = metrics.fillna(0.0)
        metrics.iloc[0, metrics.columns.get_loc("dropoff_pct_points")] = 0.0
        metrics.iloc[0, metrics.columns.get_loc("dropoff_rate_pct")] = 0.0
        return metrics

    def plot_funnel(self, metrics: pd.DataFrame) -> None:
        """Generate a horizontal bar chart for the funnel conversion."""
        self.report_path.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        step_names = metrics.index.tolist()
        conversion = metrics["conversion_pct"].tolist()

        bars = ax.barh(step_names, conversion, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Conversion rate (%)")
        ax.set_title("Deposit Funnel Conversion")

        for bar, pct in zip(bars, conversion):
            ax.text(
                pct + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{pct:.1f}%",
                va="center",
                ha="left",
                fontsize=10,
            )

        ax.grid(axis="x", linestyle="--", alpha=0.4)
        fig.tight_layout()
        fig.savefig(self.report_path, dpi=150)
        plt.close(fig)

    def run(self) -> pd.DataFrame:
        """Execute the full analysis workflow."""
        events = self.generate_synthetic_events()
        self.save_events(events)
        metrics = self.compute_funnel_metrics(events)
        self.plot_funnel(metrics)
        return metrics


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    analysis = DepositFunnelAnalysis(base_dir)
    metrics = analysis.run()
    print("Funnel metrics (conversion & drop-off):")
    print(metrics)


if __name__ == "__main__":
    main()
