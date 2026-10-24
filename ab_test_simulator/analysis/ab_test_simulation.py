"""Simulate and analyze a two-arm binary conversion experiment."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def simulate_ab_test(
    users_per_group: int,
    control_rate: float,
    variant_rate: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate independent binary outcomes using configured conversion rates."""
    if users_per_group < 2:
        raise ValueError("users_per_group must be at least 2")
    if not 0 <= control_rate <= 1 or not 0 <= variant_rate <= 1:
        raise ValueError("conversion rates must be between 0 and 1")
    rng = np.random.default_rng(seed)
    control = rng.binomial(1, control_rate, size=users_per_group)
    variant = rng.binomial(1, variant_rate, size=users_per_group)
    user_ids = np.arange(1, users_per_group * 2 + 1)
    return user_ids, control, variant


def wilson_interval(successes: int, total: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wilson score interval for one binomial proportion."""
    if total < 1 or not 0 < alpha < 1:
        raise ValueError("total must be positive and alpha must be between 0 and 1")
    z = stats.norm.ppf(1 - alpha / 2)
    p = successes / total
    denom = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / denom
    radius = z * np.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denom
    return float(center - radius), float(center + radius)


def planned_power(
    users_per_group: int,
    control_rate: float,
    variant_rate: float,
    alpha: float = 0.05,
) -> float:
    """Normal-approximation power under the configured design rates."""
    if users_per_group < 1 or not 0 < alpha < 1:
        raise ValueError("sample size must be positive and alpha must be between 0 and 1")
    if not 0 < control_rate < 1 or not 0 < variant_rate < 1:
        raise ValueError("design conversion rates must be between 0 and 1, exclusive")
    pooled = (control_rate + variant_rate) / 2
    se_null = np.sqrt(2 * pooled * (1 - pooled) / users_per_group)
    se_alt = np.sqrt(
        control_rate * (1 - control_rate) / users_per_group
        + variant_rate * (1 - variant_rate) / users_per_group
    )
    critical = stats.norm.ppf(1 - alpha / 2) * se_null
    effect = abs(variant_rate - control_rate)
    return float(stats.norm.cdf((-critical - effect) / se_alt) + 1 - stats.norm.cdf((critical - effect) / se_alt))


def summarize_results(
    control: np.ndarray,
    variant: np.ndarray,
    planned_control_rate: float,
    planned_variant_rate: float,
    alpha: float = 0.05,
) -> dict[str, float]:
    """Return observed difference and uncertainty plus design-based power."""
    if control.size == 0 or variant.size == 0:
        raise ValueError("both groups must contain observations")
    if control.size != variant.size:
        raise ValueError("this simulator requires equal group sizes")
    if not np.isin(control, [0, 1]).all() or not np.isin(variant, [0, 1]).all():
        raise ValueError("outcomes must be binary 0/1 values")
    n_control, n_variant = int(control.size), int(variant.size)
    p_control, p_variant = float(control.mean()), float(variant.mean())
    pooled = (int(control.sum()) + int(variant.sum())) / (n_control + n_variant)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n_control + 1 / n_variant))
    z_stat = (p_variant - p_control) / se if se else 0.0
    p_value = float(2 * stats.norm.sf(abs(z_stat)))
    lo_c, hi_c = wilson_interval(int(control.sum()), n_control, alpha)
    lo_v, hi_v = wilson_interval(int(variant.sum()), n_variant, alpha)
    # Newcombe's method combines the two Wilson score intervals.
    diff = p_variant - p_control
    ci_low = diff - np.sqrt((p_variant - lo_v) ** 2 + (hi_c - p_control) ** 2)
    ci_high = diff + np.sqrt((hi_v - p_variant) ** 2 + (p_control - lo_c) ** 2)
    return {
        "control_rate": p_control,
        "variant_rate": p_variant,
        "absolute_lift": diff,
        "relative_lift": diff / p_control if p_control else float("nan"),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "z_statistic": float(z_stat),
        "p_value": p_value,
        "planned_power": planned_power(
            n_control, planned_control_rate, planned_variant_rate, alpha
        ),
    }


def save_synthetic_data(output_path: Path, user_ids: np.ndarray, control: np.ndarray, variant: np.ndarray) -> None:
    """Persist one row per simulated user."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    half = control.size
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "group", "converted"])
        for uid, converted in zip(user_ids[:half], control):
            writer.writerow([f"C{uid:05d}", "control", int(converted)])
        for uid, converted in zip(user_ids[half:], variant):
            writer.writerow([f"V{uid:05d}", "variant", int(converted)])


def plot_results(summary: dict[str, float], output_path: Path) -> None:
    """Plot observed rates with 95% Wilson intervals for each group."""
    fig, ax = plt.subplots(figsize=(6, 4))
    rates = [summary["control_rate"], summary["variant_rate"]]
    # The comparison interval is the relevant uncertainty; avoid implying that
    # individual group bars communicate the uncertainty of their difference.
    ax.bar(["Control", "Variant"], rates, color=["#777777", "#2674b8"])
    ax.set_ylim(0, max(rates) * 1.25 + 0.02)
    ax.set_ylabel("Observed conversion rate")
    ax.set_title("Simulated experiment (synthetic outcomes)")
    ax.text(0.5, 0.96, f"Difference: {summary['absolute_lift']:.2%}  |  95% CI [{summary['ci_low']:.2%}, {summary['ci_high']:.2%}]",
            ha="center", va="top", transform=ax.transAxes, fontsize=8)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--users", type=int, default=2000, help="users per group")
    parser.add_argument("--control-rate", type=float, default=0.10)
    parser.add_argument("--variant-rate", type=float, default=0.12)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    user_ids, control, variant = simulate_ab_test(args.users, args.control_rate, args.variant_rate, args.seed)
    base_dir = Path(__file__).resolve().parents[1]
    save_synthetic_data(base_dir / "data/synthetic_experiment_data.csv", user_ids, control, variant)
    summary = summarize_results(
        control, variant, args.control_rate, args.variant_rate
    )
    print(f"Control: {control.sum()}/{len(control)} ({summary['control_rate']:.2%})")
    print(f"Variant: {variant.sum()}/{len(variant)} ({summary['variant_rate']:.2%})")
    print(f"Absolute difference: {summary['absolute_lift']:.2%}")
    print(f"Relative difference: {summary['relative_lift']:.2%}")
    print(f"95% CI for difference: [{summary['ci_low']:.2%}, {summary['ci_high']:.2%}]")
    print(f"Two-sided pooled proportion z-test p-value: {summary['p_value']:.5f}")
    print(f"Planned power under configured design rates (normal approximation): {summary['planned_power']:.2%}")
    plot_results(summary, base_dir / "reports/ab_test_results.png")


if __name__ == "__main__":
    main()
