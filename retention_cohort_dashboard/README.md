# Weekly cohort retention

## Problem and data

The synthetic CSV has one or more dated activity events per user and a
registration date repeated on each event row. It contains no event-type field,
so any row is treated as an active event. The analysis groups users by the
Monday-start calendar week of registration.

## Metric and approach

For cohort week *c* and age *k*, retention is distinct users with at least one
event in calendar week *c + k* divided by distinct users registered in cohort
week *c*. Duplicate events do not increase the numerator. Week 0 is the
registration calendar week; it is not forced to 100%. A cell is shown only
when that whole calendar week is covered by the input observation end date.
Unobserved future weeks are blank, not zero. A zero in a complete week means
no event was present in the supplied event log.

## Run

From the portfolio root:

```bash
.venv/bin/python retention_cohort_dashboard/analysis/cohort_retention_analysis.py
```

The default observation end is the latest event date. If the extract covers
days with no events, pass its actual inclusive coverage date explicitly:

```bash
.venv/bin/python retention_cohort_dashboard/analysis/cohort_retention_analysis.py \
  --observation-end 2024-03-24
```

The command writes `reports/weekly_retention.csv` and
`reports/retention_heatmap.png`. The notebook calls the same script.

## Limits

The event file has no extract metadata or event taxonomy, so latest-event date
is only a proxy for coverage unless `--observation-end` is supplied. Retention
is descriptive and does not identify why users return or stop returning. The
bundled file has six users across two registration weeks, so its heatmap only
demonstrates calculation and censoring behavior; it is not a useful estimate
of a real product's retention curve.
