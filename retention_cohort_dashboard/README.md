# Retention Cohort Dashboard

## Business Context
Growth and product teams rely on cohort retention to understand how newly onboarded players behave over time. Tracking week-by-week engagement highlights lifecycle health, reveals decay patterns, and uncovers opportunities for lifecycle interventions (CRM triggers, bonus campaigns, or onboarding refinements).

## Project Goal
This case study simulates an iGaming-style product, generates synthetic event data, and visualizes weekly retention by registration cohort. The deliverable is a heatmap dashboard that surfaces where retention erodes so analysts can prioritize experiments and lifecycle actions.

## How to Run the Analysis
```bash
pip install pandas matplotlib seaborn
jupyter notebook analysis/cohort_retention_analysis.ipynb
```

Open the notebook and execute all cells to reproduce the cohort retention matrix and export the heatmap image to `reports/retention_heatmap.png`.

## Expected Output
Running the notebook produces:
1. A retention matrix table with cohorts in rows and week numbers in columns (week 0–11).
2. A heatmap saved to `reports/retention_heatmap.png` illustrating the retention decay curve across cohorts.

## Repository Contents
```
retention_cohort_dashboard/
├── data/
│   └── synthetic_user_events.csv      # Synthetic events for 12 weeks of activity
├── analysis/
│   └── cohort_retention_analysis.ipynb  # Notebook with cohort logic and visualization
├── reports/
│   └── retention_heatmap.png          # Exported heatmap
└── README.md                          # Project overview and execution steps
```

## Key Learnings Showcased
- Cohort assignment and weekly retention calculations using pandas.
- Communicating decay patterns with a heatmap visualization.
- Reproducible portfolio artifact with synthetic but realistic lifecycle data.
