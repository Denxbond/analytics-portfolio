"""Backtest and forecast synthetic monthly gross deposits."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import pandas as pd
from statsmodels.tsa.holtwinters import Holt

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def rolling_origin_backtest(series: pd.Series, horizon: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare Holt's linear trend with a seasonal-naive (12-month) baseline.

    Origins start after one year and advance by the evaluation horizon. All
    forecast errors are computed against observations strictly after each fit.
    """
    if len(series) < 12 + horizon:
        raise ValueError("at least 12 months plus the forecast horizon are required")
    if series.isna().any() or (series <= 0).any():
        raise ValueError("gross deposits must be complete and positive")
    rows: list[dict[str, object]] = []
    for origin in range(12, len(series) - horizon + 1, horizon):
        train = series.iloc[:origin]
        actual = series.iloc[origin : origin + horizon]
        ets = Holt(train, damped_trend=True, initialization_method="estimated").fit(optimized=True)
        predictions = {
            "holt_damped_trend": ets.forecast(horizon).to_numpy(),
            "seasonal_naive_12m": series.iloc[origin - 12 : origin - 12 + horizon].to_numpy(),
        }
        for method, values in predictions.items():
            for offset, (date, observed, predicted) in enumerate(zip(actual.index, actual, values), start=1):
                rows.append({"origin": train.index[-1], "horizon_months": offset,
                             "month": date, "method": method,
                             "actual_gross_deposits": observed, "forecast_gross_deposits": float(predicted),
                             "absolute_error_currency_units": abs(float(observed) - float(predicted))})
    detail = pd.DataFrame(rows)
    summary = (detail.groupby("method", as_index=False)
               .agg(mae_currency_units=("absolute_error_currency_units", "mean"),
                    evaluated_months=("absolute_error_currency_units", "size")))
    return detail, summary


def load_history(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, parse_dates=["month"])
    required = {"month", "deposits", "churn_rate"}
    if not required.issubset(frame.columns):
        raise ValueError(f"input must include columns: {', '.join(sorted(required))}")
    if frame["month"].duplicated().any() or not frame["month"].is_monotonic_increasing:
        raise ValueError("month values must be unique and increasing")
    expected_months = pd.date_range(frame["month"].min(), frame["month"].max(), freq="MS")
    if not frame["month"].equals(pd.Series(expected_months, name="month")):
        raise ValueError("month values must be contiguous month starts")
    if frame[["deposits", "churn_rate"]].isna().any().any():
        raise ValueError("input rows must contain deposits and churn_rate")
    if (frame["deposits"] <= 0).any() or not frame["churn_rate"].between(0, 1, inclusive="left").all():
        raise ValueError("deposits must be positive and churn_rate must be in [0, 1)")
    return frame


def run(input_path: Path, output_dir: Path, horizon: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    history = load_history(input_path)
    deposits = history.set_index("month")["deposits"].astype(float).asfreq("MS")
    backtest, scores = rolling_origin_backtest(deposits, horizon)
    # Select the lower-MAE method from the predeclared set using rolling origins.
    selected = str(scores.sort_values(["mae_currency_units", "method"]).iloc[0]["method"])
    if selected == "holt_damped_trend":
        forecast = Holt(deposits, damped_trend=True, initialization_method="estimated").fit(optimized=True).forecast(horizon)
    else:
        forecast = pd.Series(deposits.iloc[-12 : -12 + horizon].to_numpy(),
                             index=pd.date_range(deposits.index[-1] + pd.offsets.MonthBegin(), periods=horizon, freq="MS"))
    forecast.index = pd.date_range(deposits.index[-1] + pd.offsets.MonthBegin(), periods=horizon, freq="MS")
    forecast_frame = pd.DataFrame({"month": forecast.index, "forecast_gross_deposits": forecast.to_numpy(), "selected_method": selected})
    output_dir.mkdir(parents=True, exist_ok=True)
    backtest.to_csv(output_dir / "rolling_origin_errors.csv", index=False)
    scores.to_csv(output_dir / "backtest_summary.csv", index=False)
    forecast_frame.to_csv(output_dir / "deposit_forecast.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(deposits.index, deposits, marker="o", label="Synthetic monthly gross deposits")
    ax.plot(forecast.index, forecast, marker="o", linestyle="--", label=f"Selected: {selected}")
    ax.axvline(deposits.index[-1], color="#777777", linestyle=":", linewidth=1)
    ax.set_title("Three-month gross deposit forecast (synthetic data)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Gross deposits (synthetic currency units per month)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "deposit_forecast.png", dpi=180)
    plt.close(fig)
    print(scores.to_string(index=False, formatters={"mae_currency_units": "{:,.2f}".format}))
    print(f"Selected method by rolling-origin MAE: {selected}")
    print(f"Forecast total gross deposits: {forecast.sum():,.2f} synthetic currency units")
    return backtest, forecast_frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1] / "data/synthetic_monthly_activity.csv")
    parser.add_argument("--horizon", type=int, default=3)
    args = parser.parse_args()
    run(args.data, Path(__file__).resolve().parents[1] / "reports", args.horizon)


if __name__ == "__main__":
    main()
