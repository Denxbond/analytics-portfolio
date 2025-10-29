"""Funnel conversion analysis using synthetic data.

This script demonstrates how a product analyst could quantify the impact of a
registration-to-deposit (Reg→Dep) optimization initiative. It reads synthetic
player data, calculates conversion rates by marketing channel, and compares
performance before and after an experiment variant was introduced.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

import pandas as pd


@dataclass
class FunnelMetrics:
    marketing_channel: str
    registrations: int
    first_time_depositors: int
    reg_to_dep_conversion_rate: float
    arpu: float
    arppu: float


def load_data(path: pathlib.Path) -> pd.DataFrame:
    """Load the synthetic funnel dataset."""

    df = pd.read_csv(path, parse_dates=["registration_date", "deposit_date"])
    return df


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate conversion and revenue metrics by marketing channel."""

    grouped = (
        df.groupby("marketing_channel")
        .agg(
            registrations=("user_id", "nunique"),
            first_time_depositors=("deposit_date", lambda s: s.notna().sum()),
            total_revenue=("gross_revenue", "sum"),
        )
        .reset_index()
    )

    grouped["reg_to_dep_conversion_rate"] = (
        grouped["first_time_depositors"] / grouped["registrations"]
    )
    grouped["arpu"] = grouped["total_revenue"] / grouped["registrations"]
    grouped["arppu"] = grouped.apply(
        lambda row: (
            row["total_revenue"] / row["first_time_depositors"]
            if row["first_time_depositors"] > 0
            else 0
        ),
        axis=1,
    )

    return grouped.sort_values("reg_to_dep_conversion_rate", ascending=False)


def format_metrics(df: pd.DataFrame) -> list[FunnelMetrics]:
    """Convert the aggregated DataFrame into structured metrics."""

    return [
        FunnelMetrics(
            marketing_channel=row["marketing_channel"],
            registrations=int(row["registrations"]),
            first_time_depositors=int(row["first_time_depositors"]),
            reg_to_dep_conversion_rate=round(row["reg_to_dep_conversion_rate"], 3),
            arpu=round(row["arpu"], 2),
            arppu=round(row["arppu"], 2),
        )
        for _, row in df.iterrows()
    ]


def main() -> None:
    data_path = pathlib.Path(__file__).parents[1] / "data" / "synthetic_funnel_data.csv"
    df = load_data(data_path)
    aggregated = calculate_metrics(df)
    metrics = format_metrics(aggregated)

    print("Marketing Channel Performance (Reg→Dep Funnel)\n")
    for metric in metrics:
        print(
            f"{metric.marketing_channel:>12} | Reg: {metric.registrations:>2} | "
            f"FTD: {metric.first_time_depositors:>2} | Conversion: {metric.reg_to_dep_conversion_rate:.1%} | "
            f"ARPU: ${metric.arpu:>6.2f} | ARPPU: ${metric.arppu:>6.2f}"
        )


if __name__ == "__main__":
    main()
