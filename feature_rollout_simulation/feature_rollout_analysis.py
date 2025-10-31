"""Simulate rollout of a new product feature and evaluate post-launch performance."""

from __future__ import annotations

import csv
import math
import random
import struct
import zlib
from functools import lru_cache
from pathlib import Path
from statistics import mean, variance
from typing import List, Sequence

try:  # Optional scientific stack
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - fallback when numpy unavailable
    np = None  # type: ignore

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover
    pd = None  # type: ignore

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    HAS_SEABORN = True
except ModuleNotFoundError:  # pragma: no cover
    HAS_SEABORN = False

try:
    from scipy import stats
except ModuleNotFoundError:  # pragma: no cover
    stats = None  # type: ignore


OUTPUT_DIR = Path(__file__).resolve().parent
DATA_DIR = OUTPUT_DIR / "data"
REPORTS_DIR = OUTPUT_DIR / "reports"


def simulate_user_metrics(n_users: int = 2000, seed: int = 42) -> List[dict]:
    """Generate synthetic engagement and conversion rates for pre and post launch periods."""
    rng = random.Random(seed)
    half = n_users // 2

    records: List[dict] = []

    for idx in range(1, half + 1):
        engagement = rng.betavariate(2.5, 5)
        conversion = rng.betavariate(1.5, 10)
        records.append(
            {
                "user_id": idx,
                "engagement_rate": engagement,
                "conversion_rate": conversion,
                "is_post_launch": False,
            }
        )

    for idx in range(half + 1, n_users + 1):
        base_idx = idx - (half + 1)
        baseline_engagement = records[base_idx]["engagement_rate"]
        baseline_conversion = records[base_idx]["conversion_rate"]

        engagement = max(0.0, min(1.0, baseline_engagement + rng.gauss(0.08, 0.05)))
        conversion = max(0.0, min(1.0, baseline_conversion + rng.gauss(0.03, 0.03)))

        records.append(
            {
                "user_id": idx,
                "engagement_rate": engagement,
                "conversion_rate": conversion,
                "is_post_launch": True,
            }
        )

    return records


def _manual_welchs_ttest(sample_a: Sequence[float], sample_b: Sequence[float]) -> tuple[float, float]:
    """Compute Welch's t-test when SciPy is not available."""
    n1 = len(sample_a)
    n2 = len(sample_b)
    if n1 < 2 or n2 < 2:
        raise ValueError("Samples must have at least two observations for a t-test.")

    mean1 = mean(sample_a)
    mean2 = mean(sample_b)
    var1 = variance(sample_a)
    var2 = variance(sample_b)

    se = math.sqrt(var1 / n1 + var2 / n2)
    if se == 0:
        return 0.0, 1.0

    t_stat = (mean1 - mean2) / se

    numerator = (var1 / n1 + var2 / n2) ** 2
    denominator = ((var1 / n1) ** 2) / (n1 - 1) + ((var2 / n2) ** 2) / (n2 - 1)
    df = numerator / denominator

    p_value = _two_tailed_p_value(t_stat, df)
    return t_stat, p_value


@lru_cache(maxsize=None)
def _student_t_coeff(df: float) -> float:
    lgamma_num = math.lgamma((df + 1) / 2)
    lgamma_den = math.lgamma(df / 2)
    log_coeff = lgamma_num - lgamma_den - 0.5 * (math.log(df) + math.log(math.pi))
    return math.exp(log_coeff)


def _student_t_pdf(x: float, df: float) -> float:
    return _student_t_coeff(df) * (1 + (x * x) / df) ** (-(df + 1) / 2)


def _student_t_cdf(x: float, df: float) -> float:
    if x == 0:
        return 0.5
    sign = 1 if x > 0 else -1
    x = abs(x)
    n_intervals = 1000 if x < 10 else 2000
    if n_intervals % 2 == 1:
        n_intervals += 1
    h = x / n_intervals
    total = _student_t_pdf(0.0, df) + _student_t_pdf(x, df)
    for i in range(1, n_intervals):
        weight = 4 if i % 2 == 1 else 2
        total += weight * _student_t_pdf(i * h, df)
    integral = (h / 3.0) * total
    cdf = 0.5 + sign * integral
    return max(0.0, min(1.0, cdf))


def _two_tailed_p_value(t_stat: float, df: float) -> float:
    if df <= 0:
        return 1.0
    cdf = _student_t_cdf(t_stat, df)
    return max(min(2 * min(cdf, 1 - cdf), 1.0), 0.0)


def run_analysis(records: Sequence[dict]) -> List[dict]:
    """Compute mean differences and t-test p-values between pre and post launch periods."""
    pre_records = [row for row in records if not row["is_post_launch"]]
    post_records = [row for row in records if row["is_post_launch"]]

    summary_rows: List[dict] = []
    for metric in ("engagement_rate", "conversion_rate"):
        pre_values = [row[metric] for row in pre_records]
        post_values = [row[metric] for row in post_records]

        pre_mean = sum(pre_values) / len(pre_values)
        post_mean = sum(post_values) / len(post_values)
        mean_change = post_mean - pre_mean

        if stats is not None:
            _, p_value = stats.ttest_ind(post_values, pre_values, equal_var=False)
            p_value = float(p_value)
        else:
            _, p_value = _manual_welchs_ttest(post_values, pre_values)

        summary_rows.append(
            {
                "metric": metric,
                "pre_mean": pre_mean,
                "post_mean": post_mean,
                "mean_change": mean_change,
                "p_value": p_value,
            }
        )

    return summary_rows


def _create_canvas(width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)) -> List[List[List[int]]]:
    return [[[color[0], color[1], color[2]] for _ in range(width)] for _ in range(height)]


def _write_png(rgb_matrix: Sequence[Sequence[Sequence[int]]], output_path: Path) -> None:
    height = len(rgb_matrix)
    width = len(rgb_matrix[0]) if height else 0

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return len(data).to_bytes(4, "big") + chunk_type + data + crc.to_bytes(4, "big")

    raw_data = bytearray()
    for row in rgb_matrix:
        raw_data.append(0)  # No filter
        for pixel in row:
            raw_data.extend(bytes(pixel))

    with output_path.open("wb") as png_file:
        png_file.write(b"\x89PNG\r\n\x1a\n")
        png_file.write(
            chunk(
                b"IHDR",
                struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0),
            )
        )
        png_file.write(chunk(b"IDAT", zlib.compress(bytes(raw_data), level=9)))
        png_file.write(chunk(b"IEND", b""))


def _fallback_plot(summary: Sequence[dict], output_path: Path) -> Path:
    width, height = 700, 420
    canvas = _create_canvas(width, height)

    title = "Feature Rollout Impact"
    subtitle = "Fallback visualization (seaborn unavailable)"

    FONT = {
        "A": [" 1 ", "1 1", "111", "1 1", "1 1"],
        "B": ["11 ", "1 1", "11 ", "1 1", "11 "],
        "C": [" 11", "1  ", "1  ", "1  ", " 11"],
        "D": ["11 ", "1 1", "1 1", "1 1", "11 "],
        "E": ["111", "1  ", "11 ", "1  ", "111"],
        "F": ["111", "1  ", "11 ", "1  ", "1  "],
        "G": [" 11", "1  ", "1  ", "1 1", " 11"],
        "H": ["1 1", "1 1", "111", "1 1", "1 1"],
        "I": ["111", " 1 ", " 1 ", " 1 ", "111"],
        "K": ["1 1", "11 ", "1  ", "11 ", "1 1"],
        "L": ["1  ", "1  ", "1  ", "1  ", "111"],
        "M": ["1 1", "111", "111", "1 1", "1 1"],
        "N": ["1 1", "111", "111", "111", "1 1"],
        "O": ["111", "1 1", "1 1", "1 1", "111"],
        "P": ["111", "1 1", "111", "1  ", "1  "],
        "R": ["111", "1 1", "111", "11 ", "1 1"],
        "S": [" 11", "1  ", "111", "  1", "11 "],
        "T": ["111", " 1 ", " 1 ", " 1 ", " 1 "],
        "U": ["1 1", "1 1", "1 1", "1 1", "111"],
        "V": ["1 1", "1 1", "1 1", "1 1", " 1 "],
        "Z": ["111", "  1", " 1 ", "1  ", "111"],
        " ": ["   ", "   ", "   ", "   ", "   "],
        "(": [" 1", "1 ", "1 ", "1 ", " 1"],
        ")": ["1 ", " 1", " 1", " 1", "1 "],
        "-": ["   ", "   ", "111", "   ", "   "],
        "=": ["   ", "111", "   ", "111", "   "],
        ":": ["   ", " 1 ", "   ", " 1 ", "   "],
        "0": ["111", "1 1", "1 1", "1 1", "111"],
        "1": [" 1 ", "11 ", " 1 ", " 1 ", "111"],
        "2": ["111", "  1", "111", "1  ", "111"],
        "3": ["111", "  1", "111", "  1", "111"],
        "4": ["1 1", "1 1", "111", "  1", "  1"],
        "5": ["111", "1  ", "111", "  1", "111"],
        "6": ["111", "1  ", "111", "1 1", "111"],
        "7": ["111", "  1", " 1 ", " 1 ", " 1 "],
        "8": ["111", "1 1", "111", "1 1", "111"],
        "9": ["111", "1 1", "111", "  1", "111"],
        ".": ["   ", "   ", "   ", "   ", " 1 "],
        ",": ["   ", "   ", "   ", " 1 ", " 1 "],
    }

    def draw_text(text: str, x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        for ch in text.upper():
            glyph = FONT.get(ch, FONT[" "])
            for gy, row in enumerate(glyph):
                for gx, val in enumerate(row):
                    if val == "1":
                        px = x + gx
                        py = y + gy
                        if 0 <= px < width and 0 <= py < height:
                            canvas[py][px] = [color[0], color[1], color[2]]
            x += len(glyph[0]) + 1

    draw_text(title, 40, 30)
    draw_text(subtitle, 40, 60)

    bar_width = 80
    gap = 60
    base_x = 80
    base_y = 340
    scale = 240  # pixel height for rate=1

    colors = {
        "Pre-launch": (70, 130, 180),
        "Post-launch": (46, 204, 113),
    }

    draw_text("Legend:", 520, 260)
    legend_y = 280
    for label, color in colors.items():
        for y in range(legend_y, legend_y + 20):
            for x in range(520, 540):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = [color[0], color[1], color[2]]
        draw_text(label.upper(), 550, legend_y + 5)
        legend_y += 30

    for i, row in enumerate(summary):
        pre_height = int(row["pre_mean"] * scale)
        post_height = int(row["post_mean"] * scale)

        x0 = base_x + i * (2 * bar_width + gap)
        for y in range(max(base_y - pre_height, 0), base_y):
            for x in range(x0, x0 + bar_width):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = list(colors["Pre-launch"])

        x1 = x0 + bar_width
        for y in range(max(base_y - post_height, 0), base_y):
            for x in range(x1, x1 + bar_width):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = list(colors["Post-launch"])

        label = row["metric"].replace("_", " ").upper()
        draw_text(label, x0, base_y + 15)

        change_text = f"DELTA {row['mean_change']:.3f}".upper()
        p_text = f"P={row['p_value']:.3g}".upper()
        draw_text(change_text, x0, max(base_y - post_height - 50, 20))
        draw_text(p_text, x0, max(base_y - post_height - 30, 40))

    _write_png(canvas, output_path)
    return output_path


def plot_uplift(records: Sequence[dict], summary: Sequence[dict]) -> Path:
    """Create a visualization showing pre/post mean uplift per metric."""
    output_path = REPORTS_DIR / "feature_rollout_uplift.png"

    if HAS_SEABORN and pd is not None and np is not None:
        df = pd.DataFrame(records)
        summary_df = pd.DataFrame(summary)

        long_df = df.melt(
            id_vars=["is_post_launch"],
            value_vars=["engagement_rate", "conversion_rate"],
            var_name="metric",
            value_name="rate",
        )
        long_df["period"] = np.where(long_df["is_post_launch"], "Post-launch", "Pre-launch")

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(
            data=long_df,
            x="metric",
            y="rate",
            hue="period",
            estimator=np.mean,
            errorbar="se",
            palette="viridis",
        )

        for xtick, metric in zip(ax.get_xticks(), summary_df["metric"]):
            row = summary_df.loc[summary_df["metric"] == metric].iloc[0]
            ax.text(
                xtick,
                min(row["post_mean"] + 0.03, 1.05),
                f"Δ {row['mean_change']:.3f}\n(p={row['p_value']:.3g})",
                ha="center",
                va="bottom",
                fontsize=9,
                color="black",
            )

        ax.set_title("Feature Rollout Impact on Engagement and Conversion")
        ax.set_ylabel("Average Rate")
        ax.set_xlabel("")
        ax.legend(title="Period")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
        return output_path

    return _fallback_plot(summary, output_path)


def _write_records_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[dict]) -> None:
    with path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _format_summary(summary: Sequence[dict]) -> str:
    header = f"{'metric':<18}{'pre_mean':>12}{'post_mean':>12}{'mean_change':>14}{'p_value':>12}"
    lines = [header, "-" * len(header)]
    for row in summary:
        lines.append(
            f"{row['metric']:<18}{row['pre_mean']:>12.4f}{row['post_mean']:>12.4f}{row['mean_change']:>14.4f}{row['p_value']:>12.4g}"
        )
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    records = simulate_user_metrics()
    summary = run_analysis(records)

    metrics_path = DATA_DIR / "feature_rollout_metrics.csv"
    summary_path = REPORTS_DIR / "summary_statistics.csv"

    _write_records_csv(metrics_path, ["user_id", "engagement_rate", "conversion_rate", "is_post_launch"], records)
    _write_records_csv(summary_path, ["metric", "pre_mean", "post_mean", "mean_change", "p_value"], summary)

    plot_path = plot_uplift(records, summary)

    print("Data saved to:", metrics_path)
    print("Summary saved to:", summary_path)
    print("Plot saved to:", plot_path)
    print("\nStatistical Summary:\n" + _format_summary(summary))


if __name__ == "__main__":
    main()
