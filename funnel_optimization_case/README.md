# Funnel Optimization Case Study

This case study simulates a registration-to-deposit (Reg→Dep) funnel optimization initiative for a digital product.
It demonstrates how product analytics combines business context, SQL transformations, and Python automation to quantify performance opportunities within the conversion flow.

## Business Scenario
- **Problem:** Paid Search cohorts show the lowest Reg→Dep conversion rate due to friction in the payment verification step.
- **Goal:** Improve conversion without negatively impacting monetization metrics (ARPU, ARPPU).
- **Approach:** Diagnose the funnel, identify key drop-off points, design an A/B experiment, and quantify the expected uplift.

## Repository Structure
| Path | Description |
| --- | --- |
| `data/synthetic_funnel_data.csv` | Synthetic dataset representing 20 recent registrations with revenue outcomes. |
| `sql/funnel_conversion.sql` | Example SQL (dbt-ready) model for Reg→Dep conversion and revenue by channel. |
| `analysis/funnel_analysis.py` | Python script that summarizes funnel metrics using `pandas`. |
| `reports/ab_test_plan.md` | Experiment design outlining hypothesis, KPIs, and rollout recommendation. |

## Run the Analysis
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
