import csv
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "business_review_data.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "analysis" / "business_review_dashboard.png"


def load_data(path: Path):
    dates = []
    nsm = []
    arpu = []
    retention = []
    churn = []

    with path.open() as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dates.append(datetime.strptime(row["date"], "%Y-%m-%d"))
            nsm.append(float(row["nsm"]))
            arpu.append(float(row["arpu"]))
            retention.append(float(row["retention_rate"]))
            churn.append(float(row["churn_rate"]))
    return dates, nsm, arpu, retention, churn


def compute_quarter_storyline(dates, *metrics):
    phases = ["Quarter Kickoff", "Mid-Quarter Check", "Quarter Close"]
    splits = [len(dates) // 3, 2 * len(dates) // 3]
    indices = [
        range(0, splits[0]),
        range(splits[0], splits[1]),
        range(splits[1], len(dates)),
    ]

    storyline = {label: [] for label in phases}
    for label, idx in zip(phases, indices):
        idx = list(idx)
        for series in metrics:
            if idx:
                avg = sum(series[i] for i in idx) / len(idx)
            else:
                avg = float("nan")
            storyline[label].append(avg)
    return phases, storyline


def normalize(values):
    base = values[0]
    if base == 0 or base != base:  # guard against NaN
        return [0 for _ in values]
    return [v / base for v in values]


def plot_dashboard(dates, nsm, arpu, retention, churn):
    phases, storyline = compute_quarter_storyline(dates, nsm, arpu, retention, churn)

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Synthetic Marketplace Business Review", fontsize=18, fontweight="bold")

    # NSM and ARPU trend
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(dates, nsm, label="NSM (Transactions)", color="#005EB8", linewidth=2)
    ax1.set_ylabel("NSM")
    ax1.grid(True, axis="y", linestyle="--", alpha=0.4)

    ax1b = ax1.twinx()
    ax1b.plot(dates, arpu, label="ARPU", color="#FF8C00", linewidth=2)
    ax1b.set_ylabel("ARPU ($)")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left")
    ax1.set_title("Growth & Monetization Momentum")

    # Retention and churn
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(dates, retention, label="Retention Rate", color="#2E8B57", linewidth=2)
    ax2.plot(dates, churn, label="Churn Rate", color="#C0392B", linewidth=2)
    ax2.set_ylabel("Rate")
    ax2.set_title("Customer Health Signals")
    ax2.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax2.legend(loc="upper right")
    ax2.set_ylim(0, max(max(retention), max(churn)) * 1.2)

    # Quarterly storyline summary
    ax3 = fig.add_subplot(3, 1, 3)
    normalized_metrics = [
        normalize([storyline[phase][i] for phase in phases])
        for i in range(4)
    ]
    colors = ["#005EB8", "#FF8C00", "#2E8B57", "#C0392B"]
    labels = ["NSM", "ARPU", "Retention", "Churn"]

    for metric_values, color, label in zip(normalized_metrics, colors, labels):
        ax3.plot(phases, metric_values, marker="o", linewidth=2, color=color, label=label)

    ax3.set_title("Quarterly Storyline: Momentum Across KPIs")
    ax3.set_ylabel("Indexed to Quarter Kickoff")
    ax3.set_ylim(0, max(max(series) for series in normalized_metrics) * 1.2)
    ax3.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax3.legend(loc="upper left", ncol=2)

    fig.autofmt_xdate()
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUTPUT_PATH, dpi=200)
    plt.close(fig)
    print(f"Dashboard saved to {OUTPUT_PATH}")


def main():
    dates, nsm, arpu, retention, churn = load_data(DATA_PATH)
    plot_dashboard(dates, nsm, arpu, retention, churn)


if __name__ == "__main__":
    main()
