"""Funnel conversion analysis using synthetic data.

This script summarizes synthetic 7-day registration-to-first-deposit conversion
rates by marketing channel. Channel differences are descriptive, not causal.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

import pandas as pd


@dataclass
class FunnelMetrics:
    marketing_channel: str
    registrations: int
    first_time_depositors_7d: int
    reg_to_dep_conversion_rate: float


def load_data(path: pathlib.Path) -> pd.DataFrame:
    """Load the synthetic funnel dataset."""

    df = pd.read_csv(path, parse_dates=["registration_date", "deposit_date"])
    if df["user_id"].duplicated().any():
        raise ValueError("expected one row per registered user")
    if df[["user_id", "registration_date", "marketing_channel"]].isna().any().any():
        raise ValueError("user_id, registration_date, and marketing_channel are required")
    return df


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate seven-day conversion metrics by marketing channel."""

    if df["user_id"].duplicated().any():
        raise ValueError("expected one row per registered user")

    df = df.copy()
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="raise")
    df["deposit_date"] = pd.to_datetime(df["deposit_date"], errors="coerce")
    elapsed = (df["deposit_date"] - df["registration_date"]).dt.days
    df["converted_7d"] = elapsed.ge(0) & elapsed.lt(7)
    grouped = df.groupby("marketing_channel").agg(
        registrations=("user_id", "nunique"),
        first_time_depositors_7d=("converted_7d", "sum"),
    ).reset_index()
    grouped["reg_to_dep_conversion_rate"] = (
        grouped["first_time_depositors_7d"] / grouped["registrations"]
    )

    return grouped.sort_values("reg_to_dep_conversion_rate", ascending=False)


def format_metrics(df: pd.DataFrame) -> list[FunnelMetrics]:
    """Convert the aggregated DataFrame into structured metrics."""

    return [
        FunnelMetrics(
            marketing_channel=row["marketing_channel"],
            registrations=int(row["registrations"]),
            first_time_depositors_7d=int(row["first_time_depositors_7d"]),
            reg_to_dep_conversion_rate=round(row["reg_to_dep_conversion_rate"], 3),
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
            f"FTD within 7d: {metric.first_time_depositors_7d:>2} | "
            f"Conversion within 7d: {metric.reg_to_dep_conversion_rate:.1%}"
        )


if __name__ == "__main__":
    main()
