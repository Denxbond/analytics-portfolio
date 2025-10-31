# Product Analytics Portfolio Cases

This repository collects portfolio-ready case studies that showcase product
analytics, conversion rate optimization, and analytics engineering skills.

## TL;DR
- Clone the repo and open a case study folder to see the business story,
  dataset, and analysis assets.
- Install any listed Python dependencies (e.g., `pandas`) and run the provided
  scripts to reproduce the metrics.
- Use the SQL models to materialize metrics in your own warehouse or dbt
  project, swapping in anonymized production data when sharing publicly.

## Projects
- [Funnel Optimization Case Study](funnel_optimization_case/README.md):
  Reg→Dep funnel analysis with SQL, Python, and an experiment playbook.
- [Retention Cohort Dashboard](retention_cohort_dashboard/README.md):
  Weekly cohort retention heatmap built from synthetic lifecycle events.
- [A/B Test Simulator](ab_test_simulator/README.md):
  Experiment simulation with statistical lift readout and reporting assets.
- [User Journey Path Analysis](user_journey_path_analysis/README.md):
  Behavioural path aggregation with clickstream data and journey visualisation.

## Getting Started
Each project includes synthetic data, reproducible code, and documentation.
Clone the repo, explore the folders, and adapt the templates with anonymized
metrics from your own work. Each README includes exact run commands so you can
verify the analysis locally before publishing your own numbers.
