# A/B Test Simulator

This portfolio case simulates an online experiment that tests whether a new product feature improves conversions compared with the current experience. It generates synthetic user-level outcomes, calculates classical hypothesis test statistics, and visualizes the lift so stakeholders can understand the impact at a glance.

## Project Structure

```
ab_test_simulator/
├── analysis/
│   └── ab_test_simulation.py
├── data/
│   └── synthetic_experiment_data.csv
├── reports/
│   └── ab_test_results.png
└── README.md
```

## How to Run the Simulation

1. Install the required libraries:
   ```bash
   pip install numpy scipy matplotlib
   ```
2. Execute the simulator script with optional parameters for sample size or conversion rates:
   ```bash
   python analysis/ab_test_simulation.py --users 5000 --control-rate 0.12 --variant-rate 0.14 --seed 42
   ```
   Arguments:
   - `--users`: users per group (default 5000)
   - `--control-rate`: probability of conversion for the control group (default 0.12)
   - `--variant-rate`: probability of conversion for the variant group (default 0.14)
   - `--seed`: random seed for reproducibility (default 42)

## Expected Output

Running the script will:
- Save a user-level dataset to `data/synthetic_experiment_data.csv`
- Produce a bar chart comparing conversion rates at `reports/ab_test_results.png`
- Print a console summary similar to:
  ```
  A/B Test Summary
  -----------------------------------------------------------------------------
  Group        Conversions/Total    Rate %    Lift %      p-value     Power
  Control              587 / 5000     11.74      0.00       0.0000     0.983
  Variant              725 / 5000     14.50     23.51       0.0000     0.983

  Additional statistics
  -----------------------------------------------------------------------------
  Observed lift: 23.51%
  z-score: 4.087
  p-value: 0.0000
  Power: 0.983

  Saved synthetic dataset to /path/to/data/synthetic_experiment_data.csv
  Saved conversion chart to /path/to/reports/ab_test_results.png
  ```
