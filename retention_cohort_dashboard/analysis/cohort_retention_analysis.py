"""Calculate weekly active-user retention by registration cohort."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def calculate_retention(events: pd.DataFrame, observation_end: str | pd.Timestamp | None = None) -> pd.DataFrame:
    """Return active users divided by registered users for complete cohort weeks.

    A cohort is the Monday-start calendar week of registration. A user is
    active in a week when at least one event occurs in that week. Periods are
    measured from the cohort week. Incomplete weeks are NaN, not zero.
    """
    required = {"user_id", "registration_date", "event_date"}
    missing = required - set(events.columns)
    if missing:
        raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
    frame = events.loc[:, list(required)].copy()
    if frame.empty:
        raise ValueError("at least one event is required")
    if frame[list(required)].isna().any().any():
        raise ValueError("user_id, registration_date, and event_date cannot be null")
    frame["registration_date"] = pd.to_datetime(frame["registration_date"], errors="raise").dt.normalize()
    frame["event_date"] = pd.to_datetime(frame["event_date"], errors="raise").dt.normalize()
    if (frame["event_date"] < frame["registration_date"]).any():
        raise ValueError("event_date cannot precede registration_date")
    registration_counts = frame.groupby("user_id")["registration_date"].nunique()
    if (registration_counts > 1).any():
        raise ValueError("each user must have one registration date")
    cutoff = pd.Timestamp(observation_end).normalize() if observation_end is not None else frame["event_date"].max()
    if cutoff < frame["event_date"].max():
        raise ValueError("observation_end cannot precede an event")

    # Deduplicate users within a cohort-week before counting activity.
    frame["cohort_week"] = frame["registration_date"] - pd.to_timedelta(frame["registration_date"].dt.day_of_week, unit="D")
    frame["event_week"] = frame["event_date"] - pd.to_timedelta(frame["event_date"].dt.day_of_week, unit="D")
    frame["period"] = ((frame["event_week"] - frame["cohort_week"]).dt.days // 7).astype(int)
    frame = frame.loc[frame["period"].between(0, 11)]
    cohorts = frame[["user_id", "cohort_week"]].drop_duplicates().groupby("cohort_week")["user_id"].nunique()
    active = frame.groupby(["cohort_week", "period"])["user_id"].nunique().unstack("period")
    index = cohorts.index.sort_values()
    columns = pd.RangeIndex(0, 12, name="weeks_since_cohort")
    active = active.reindex(index=index, columns=columns)
    retained = active.div(cohorts.reindex(index), axis=0)
    end_exclusive = cutoff + pd.Timedelta(days=1)
    for cohort_week in index:
        for period in columns:
            complete = cohort_week + pd.Timedelta(days=7 * (period + 1)) <= end_exclusive
            if not complete:
                retained.loc[cohort_week, period] = float("nan")
            else:
                # With a complete observation window, no recorded activity is 0.
                retained.loc[cohort_week, period] = retained.loc[cohort_week, period] if pd.notna(retained.loc[cohort_week, period]) else 0.0
    retained.index.name = "registration_week"
    retained.columns = columns
    return retained


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1] / "data/synthetic_user_events.csv")
    parser.add_argument("--observation-end", help="inclusive YYYY-MM-DD coverage date; defaults to the latest event date")
    args = parser.parse_args()
    events = pd.read_csv(args.data)
    retention = calculate_retention(events, args.observation_end)
    base_dir = Path(__file__).resolve().parents[1]
    base_dir.joinpath("reports").mkdir(parents=True, exist_ok=True)
    retention.to_csv(base_dir / "reports/weekly_retention.csv", na_rep="")
    sns.set_theme(style="whitegrid", palette="Blues")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(retention, annot=True, fmt=".0%", cmap="Blues", vmin=0, vmax=1,
                cbar_kws={"label": "Active users / cohort registrations"}, ax=ax)
    ax.set_yticklabels([pd.Timestamp(value).strftime("%Y-%m-%d") for value in retention.index], rotation=0)
    ax.set_title("Weekly retention by registration cohort (synthetic data)")
    ax.set_xlabel("Calendar weeks since registration week")
    ax.set_ylabel("Registration week")
    fig.tight_layout()
    fig.savefig(base_dir / "reports/retention_heatmap.png", dpi=180)
    plt.close(fig)
    print(retention.to_string(float_format=lambda value: f"{value:.1%}"))
    print(f"Observation end: {pd.Timestamp(args.observation_end).date() if args.observation_end else events['event_date'].max()}")


if __name__ == "__main__":
    main()
