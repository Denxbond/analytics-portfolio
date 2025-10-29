# Funnel Optimization Case Study

This project simulates a registration-to-deposit (Reg→Dep) funnel optimization
initiative for an iGaming product. It demonstrates how a product analyst can
combine business context, SQL/dbt-friendly transformations, and lightweight
Python automation to produce a quantified case study suitable for a public
portfolio.

## Business Scenario
- **Problem:** Paid Search cohorts exhibit the lowest Reg→Dep conversion rate
  due to friction in the payment verification flow.
- **Goal:** Improve conversion without hurting monetization metrics (ARPU/ARPPU).
- **Approach:** Diagnose the funnel, design an experiment, and quantify the
  expected uplift.

## Repository Tour
| Path | Description |
| --- | --- |
| `data/synthetic_funnel_data.csv` | Synthetic dataset representing 20 recent registrations with revenue outcomes. |
| `sql/funnel_conversion.sql` | Example SQL (dbt-ready) model for Reg→Dep conversion and revenue by channel. |
| `analysis/funnel_analysis.py` | Python script that summarizes funnel metrics using pandas. |
| `reports/ab_test_plan.md` | Experiment design outlining hypothesis, KPIs, and rollout recommendation. |

## How to Reproduce the Analysis
1. Install dependencies (only `pandas` is required):
   ```bash
   pip install pandas
   ```
2. Run the analysis script:
   ```bash
   python analysis/funnel_analysis.py
   ```
3. Use the SQL model to materialize metrics in your warehouse or dbt project.

## Sample Findings
Running the script produces channel-level KPIs, highlighting a ~40% conversion
for Affiliates vs. ~20% for Paid Search. This gap frames the optimization
opportunity and provides baselines for the A/B test plan.

## Portfolio Tips
- Replace the synthetic dataset with anonymized production data when possible.
- Add dashboard screenshots (e.g., Power BI) to visualize the funnel.
- Link to a write-up or blog post summarizing results for hiring managers.
