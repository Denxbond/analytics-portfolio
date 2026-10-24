# Binary conversion experiment simulation

## Problem and data

This script generates independent binary outcomes for a control and a variant
arm from configured conversion probabilities. Each row in the CSV is one
simulated user assigned to exactly one arm. The data is synthetic; it is not an
observed product experiment.

## Approach

The observed absolute difference is variant conversion rate minus control
conversion rate. The relative difference divides that value by the control
rate. A two-sided pooled two-proportion z-test is reported with a Newcombe
confidence interval based on Wilson score intervals. Planned power is a normal
approximation calculated from the configured rates, group size, and alpha; it
does not use the observed test statistic. The simulation assumes independent
users, fixed assignment, no repeated testing, and one binary outcome per user.

## Run

From the portfolio root, after installing `requirements.txt`:

```bash
.venv/bin/python ab_test_simulator/analysis/ab_test_simulation.py \
  --users 2000 --control-rate 0.10 --variant-rate 0.12 --seed 42
```

This writes the user-level sample to `data/synthetic_experiment_data.csv` and
the chart to `reports/ab_test_results.png`.

## Results and limits

With the default seed and parameters, the simulated rates are 10.45% and
11.75%: a +1.30 percentage-point difference, 95% CI [-0.65, 3.25] points,
two-sided p=0.19065, and planned power 52.45%. A simulated p-value or difference
is not evidence of a real product effect. Power depends on the configured
effect size and sample size; it is not an estimate of the probability that an
observed result is true.
