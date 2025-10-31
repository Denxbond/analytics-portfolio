# Feature Rollout Simulation

This project simulates the rollout of a new product capability (e.g., a one-click reorder button) and demonstrates how product analysts can evaluate its early impact.

## Contents
- `feature_rollout_analysis.py`: Generates synthetic pre/post launch user data, performs statistical testing, and saves outputs. The script uses pandas/NumPy/seaborn when available, but gracefully falls back to pure Python implementations (including a manual Welch's t-test and PNG renderer) so it can run in constrained environments.
- `data/feature_rollout_metrics.csv`: Simulated user-level engagement and conversion metrics with a post-launch flag.
- `reports/summary_statistics.csv`: Mean changes and Welch's t-test p-values for key metrics.
- `reports/feature_rollout_uplift.png`: Visualization of the uplift across engagement and conversion.

## Analytical Workflow
Product analysts typically:
1. **Collect user-level metrics** that represent feature adoption and business outcomes.
2. **Segment users into pre- and post-launch cohorts** (or treatment/control groups) using flags similar to `is_post_launch`.
3. **Quantify changes** in metrics such as engagement_rate and conversion_rate, focusing on deltas relative to baseline performance.
4. **Validate significance** with statistical tests (e.g., Welch's t-test) to ensure observed uplifts are unlikely to be due to chance.
5. **Visualize results** to communicate effect sizes, confidence intervals, and the overall narrative to stakeholders.

Run the script with `python feature_rollout_analysis.py` from this directory to reproduce the dataset, summary statistics, and visualization.
