# Deposit Funnel Analysis

## Overview
This project simulates a casino onboarding journey from first landing on site to making a successful deposit. Conversion optimization teams can use the resulting funnel analytics to diagnose where prospective players are abandoning the flow and prioritize experimentation.

The synthetic dataset mimics four critical milestones in the registration and funding process:
1. Landing on the site
2. Completing registration
3. Reaching the deposit form
4. Successfully submitting a deposit

By analyzing the conversion rate at each step, product and CRM stakeholders can quickly pinpoint friction points, quantify drop-off, and monitor whether promotional campaigns improve throughput in the deposit funnel.

## Repository Structure
```
deposit_funnel_analysis/
├── analysis/
│   └── deposit_funnel_analysis.py
├── data/
│   └── synthetic_funnel_events.csv
├── reports/
│   └── funnel_dropoff_chart.png
└── README.md
```

## How to Run the Analysis
1. **Set up the environment**
   - Ensure Python 3.9+ is installed with `pandas`, `numpy`, and `matplotlib` available. You can install them via `pip install -r requirements.txt` (create a requirements file with these packages) or install individually: `pip install pandas numpy matplotlib`.

2. **Execute the analysis script**
   ```bash
   python analysis/deposit_funnel_analysis.py
   ```
   The script will:
   - Generate synthetic event-level funnel data.
   - Save the dataset to `data/synthetic_funnel_events.csv`.
   - Calculate conversion and drop-off metrics per funnel step.
   - Produce a horizontal funnel visualization saved to `reports/funnel_dropoff_chart.png`.

3. **Inspect outputs**
   - Review the console output for conversion and drop-off percentages.
   - Explore the CSV for detailed event logs.
   - Reference the PNG chart for a quick executive-ready summary of funnel health.
