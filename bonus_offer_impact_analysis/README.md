# Bonus offer simulation

This learning exercise generates 2,000 synthetic user-period records, randomly
assigns each record to control or bonus, and compares deposits per user-period
and gross revenue per user-period. The generator builds an effect into the
bonus group (a deposit multiplier and larger simulated ticket); any group gap
is therefore a property of this simulation, not an estimate of a real offer's
effect. The generated revenue has no stated currency or bonus-cost adjustment.

From the portfolio root, run:

```bash
.venv/bin/python bonus_offer_impact_analysis/analysis/bonus_offer_analysis.py
```

This regenerates `data/bonus_offer_data.csv` and `reports/bonus_offer_uplift.png`
using seed 42. The summary is descriptive, has no confidence interval or
significance test, and cannot support a campaign decision. A real offer
evaluation would need randomized assignment, a defined outcome window, and
incremental margin after offer cost.
