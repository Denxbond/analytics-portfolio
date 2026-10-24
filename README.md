# Data analytics projects

I focus on product and business analysis with Python and SQL, supported by
reproducible data workflows. This portfolio contains synthetic or public
learning data; results are demonstrations, not business outcomes.

## Selected work

- [Experiment analysis](ab_test_simulator/README.md): binary conversion test
  simulation with a two-proportion test, confidence interval, and design-based
  power estimate.
- [Cohort retention](retention_cohort_dashboard/README.md): weekly active-user
  retention with duplicate handling and incomplete cohort weeks left unobserved.
- [Deposit forecast](revenue_forecast_model/README.md): synthetic monthly gross
  deposits, evaluated against a seasonal-naive baseline with rolling origins.
- [Funnel analysis](funnel_optimization_case/README.md): descriptive 7-day
  registration-to-deposit metric and a test plan that separates hypotheses from
  measured evidence.

## Setup

Requires Python 3.12. From this directory:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

Run a case from this directory:

```bash
.venv/bin/python ab_test_simulator/analysis/ab_test_simulation.py
.venv/bin/python retention_cohort_dashboard/analysis/cohort_retention_analysis.py
.venv/bin/python revenue_forecast_model/analysis/revenue_forecast.py
.venv/bin/python funnel_optimization_case/analysis/funnel_analysis.py
```

The scripts resolve data and report paths from their own locations. Synthetic
input and generated charts/tables are labeled in each case README.

## Other learning work

The [project index](index.md) links to smaller exercises and notes. They remain
available as learning work and are not presented as flagship analyses.
