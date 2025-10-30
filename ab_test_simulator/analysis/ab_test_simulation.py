"""Simulate an A/B test with synthetic conversion data and export summary artifacts."""
import argparse
import csv
from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def simulate_ab_test(
    users_per_group: int,
    control_rate: float,
    variant_rate: float,
    seed: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate binary conversion outcomes for control and variant groups."""
    rng = np.random.default_rng(seed)
    control = rng.binomial(1, control_rate, size=users_per_group)
    variant = rng.binomial(1, variant_rate, size=users_per_group)
    user_ids = np.arange(1, users_per_group * 2 + 1)
    return user_ids, control, variant


def save_synthetic_data(
    output_path: Path,
    user_ids: np.ndarray,
    control: np.ndarray,
    variant: np.ndarray,
) -> None:
    """Persist the simulated experiment rows to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    half = user_ids.size // 2
    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "group", "converted"])
        for uid, converted in zip(user_ids[:half], control):
            writer.writerow([f"C{uid:05d}", "control", int(converted)])
        for uid, converted in zip(user_ids[half:], variant):
            writer.writerow([f"V{uid:05d}", "variant", int(converted)])


def summarize_results(control, variant):
    """Compute and print experiment summary metrics."""
    control_rate = control.mean()
    variant_rate = variant.mean()
    lift = (variant_rate - control_rate) / control_rate if control_rate > 0 else 0
    z_stat, p_value = stats.ttest_ind(variant, control, equal_var=False)
    power = 1 - stats.norm.cdf(stats.norm.ppf(0.975) - abs(z_stat))
    return control_rate, variant_rate, lift, p_value, power


def plot_results(control_rate, variant_rate, output_path):
    """Generate a simple bar chart comparing conversion rates."""
    plt.figure(figsize=(6, 4))
    plt.bar(["Control", "Variant"], [control_rate, variant_rate], color=["gray", "blue"])
    plt.ylabel("Conversion Rate")
    plt.title("A/B Test Results")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Run a synthetic A/B test simulation.")
    parser.add_argument("--users", type=int, default=2000)
    parser.add_argument("--control-rate", type=float, default=0.10)
    parser.add_argument("--variant-rate", type=float, default=0.12)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    user_ids, control, variant = simulate_ab_test(
        args.users, args.control_rate, args.variant_rate, args.seed
    )

    data_path = Path(__file__).resolve().parents[1] / "data" / "synthetic_experiment_data.csv"
    save_synthetic_data(data_path, user_ids, control, variant)

    control_rate, variant_rate, lift, p_value, power = summarize_results(control, variant)
    print("\n=== A/B Test Simulation Summary ===")
    print(f"Control: {control.sum()}/{len(control)} ({control_rate:.2%})")
    print(f"Variant: {variant.sum()}/{len(variant)} ({variant_rate:.2%})")
    print(f"Lift: {lift:.2%}")
    print(f"P-value: {p_value:.5f}")
    print(f"Power: {power:.2%}")

    output_path = Path(__file__).resolve().parents[1] / "reports" / "ab_test_results.png"
    plot_results(control_rate, variant_rate, output_path)
    print(f"\nSaved report to {output_path.resolve()}")


if __name__ == "__main__":
    main()
