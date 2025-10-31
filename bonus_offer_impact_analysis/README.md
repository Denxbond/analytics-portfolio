## Bonus Offer Impact Analysis

### Business Context
Gaming products often use deposit bonuses to increase player engagement and value.
This simulation models how bonus exposure impacts deposit frequency and Average Revenue Per User (ARPU).
The dataset represents a 50/50 split between control and bonus groups, allowing clear KPI comparison and uplift measurement.

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

Bonus exposure led to 37% more deposits and 53% higher ARPU per user, indicating the promotion effectively increased engagement and spending.
When applying this framework to real campaigns, ensure that the incremental revenue exceeds bonus cost and validate results using a statistically powered A/B test.
