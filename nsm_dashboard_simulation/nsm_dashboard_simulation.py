import math
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_nsm_data() -> pd.DataFrame:
    """Generate deterministic monthly metrics for a North Star Metric dashboard."""
    months = pd.date_range("2023-01-01", periods=12, freq="MS")
    month_index = pd.Series(range(len(months)), dtype=float)

    activation = 0.52 + 0.05 * (month_index.apply(lambda x: math.sin((x + 1) * math.pi / 6)))
    retention = 0.62 + 0.04 * (month_index.apply(lambda x: math.cos((x + 1) * math.pi / 7)))
    monetization = 0.36 + 0.05 * (month_index.apply(lambda x: 1 / (1 + math.exp(-0.8 * (x - 5))) - 0.5))

    data = pd.DataFrame(
        {
            "Month": months,
            "Activation Rate": activation.clip(lower=0.45, upper=0.70),
            "Retention Rate": retention.clip(lower=0.55, upper=0.78),
            "Monetization Rate": monetization.clip(lower=0.30, upper=0.60),
        }
    )

    data["NSM"] = (
        data["Activation Rate"]
        * data["Retention Rate"]
        * data["Monetization Rate"]
    )
    return data


def format_percentage_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return a copy of the dataframe with percentage columns formatted."""
    formatted = df.copy()
    for column in columns + ["NSM"]:
        formatted[column] = (formatted[column] * 100).round(2)
    formatted.insert(0, "Month", formatted.pop("Month").dt.strftime("%Y-%m"))
    return formatted


def plot_nsm_trends(df: pd.DataFrame, output_path: Path) -> None:
    """Plot NSM and its drivers over time and save the figure."""
    sns.set_theme(style="whitegrid")
    melted = df.melt("Month", var_name="Metric", value_name="Value")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=melted, x="Month", y="Value", hue="Metric", marker="o")
    plt.title("North Star Metric Drivers Over Time")
    plt.ylabel("Rate")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    output_dir = Path("nsm_dashboard_simulation")
    output_dir.mkdir(exist_ok=True)

    data = generate_nsm_data()
    plot_nsm_trends(data, output_dir / "nsm_trends.png")

    formatted = format_percentage_columns(
        data, ["Activation Rate", "Retention Rate", "Monetization Rate"]
    )
    formatted.to_csv(output_dir / "nsm_metrics.csv", index=False)


if __name__ == "__main__":
    main()
