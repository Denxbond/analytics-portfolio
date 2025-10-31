## Bonus Offer Impact Analysis

### Business Context
Gaming operators frequently test deposit bonuses to boost player value. This
simulation estimates how exposing users to a bonus affects deposit frequency
and Average Revenue Per User (ARPU). The synthetic dataset mimics a 50/50 split
between control and bonus cohorts so you can practice calculating KPI lift and
packaging experiment insights.

### Repository Assets
- `data/bonus_offer_data.csv` – 2,000 simulated users with group assignment,
  deposit counts, and total revenue.
- `analysis/bonus_offer_analysis.py` – pandas workflow that regenerates the
  dataset, computes KPI lift, prints a summary table, and produces the KPI
  comparison chart.
- `reports/bonus_offer_uplift.png` – Side-by-side bar chart annotated with the
  relative lift for deposits per user and ARPU.

### How to Run the Analysis
1. (Optional) Create and activate a virtual environment.
2. Install dependencies: `pip install pandas matplotlib seaborn`.
3. Execute the analysis: `python analysis/bonus_offer_analysis.py`.

The script prints a console table with per-group KPIs plus absolute and relative
lift, saves an updated dataset in `data/`, and exports the PNG chart to
`reports/`.

### KPI Readout & Interpretation

| Metric | Control | Bonus | Absolute Lift | Relative Lift |
| --- | ---: | ---: | ---: | ---: |
| Deposits per User | 2.20 | 3.02 | +0.82 | +37.4% |
| ARPU | 107.14 | 164.17 | +57.03 | +53.2% |

The bonus cohort deposits 37% more frequently and generates 53% higher ARPU.
Those increases suggest the promotion successfully nudges players to place more
deposits and spend more per user. When applying this template to real campaigns,
confirm that higher monetization offsets bonus costs and validate uplift with a
statistically powered experiment.
