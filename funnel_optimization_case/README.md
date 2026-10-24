# Registration-to-deposit funnel

## Data and question

The synthetic CSV contains one row per registered user (20 rows, January 2024)
with a registration date, an optional first deposit date, channel, and a
revenue field. It contains no payment-step events or randomized treatment.

## Metric and approach

For each channel, conversion is distinct registered users with a deposit in
`[registration, registration + 7 days)` divided by registered users. Python
and the SQL example use the same half-open window. The `gross_revenue` field is
not analyzed because its time window and accounting definition are unspecified.
Channel differences are descriptive; there is no evidence here that payment
friction caused them.

## Run

From the portfolio root, install the pinned dependencies and run:

```bash
.venv/bin/python funnel_optimization_case/analysis/funnel_analysis.py
```

The SQL in `sql/funnel_conversion.sql` is an example against an event table;
its source table must provide one registration event per user ID and timestamped
deposit events.

## Results and limits

The included sample prints 6/6 Affiliates, 4/5 Paid Social, 0/4 Organic, and
0/5 Paid Search users converting within the window. With only 20 synthetic
users, these proportions do not support a channel ranking, causal claim, or
rollout decision. `reports/ab_test_plan.md` is a hypothesis and test plan, not
an experiment result.
