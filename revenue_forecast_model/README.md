# Monthly gross deposit forecast

## Problem and data

The input is 24 months of synthetic monthly gross deposit amounts and
synthetic churn rates. The forecast target is **gross deposits in synthetic
currency units per month**, not revenue: this dataset has no stated currency or accounting definition of revenue,
withdrawals, bonus cost, or other adjustments. Churn is retained as a
descriptive field and is not used to transform deposits or forecast the target.

## Approach

The script compares damped Holt trend with a 12-month seasonal-naive baseline.
It uses expanding rolling-origin evaluation: 12 months for the first training
window, a 3-month forecast horizon, and origins advancing by 3 months. MAE is
reported over the resulting 12 forecasted months per method. The lower-MAE
method is selected and refit/extended for the next three months. There are only
four origins, so this is a small illustrative comparison, not evidence of
stable future performance.

## Run and outputs

From the portfolio root:

```bash
.venv/bin/python revenue_forecast_model/analysis/revenue_forecast.py
```

The command writes rolling-origin errors, method MAE, a three-month forecast,
and a chart to `reports/`. The notebook calls the same script.

## Results and limits

On the committed input, seasonal naive has a rolling-origin MAE of 5,951.67
synthetic currency units across 12 held-out months versus 8,373.00 for damped
Holt trend, so the baseline is selected. Its next-three-month total is
379,381.81 synthetic currency units. These values
describe a small synthetic example; no measured business data is used. This
forecast does not estimate net revenue or establish a causal relationship
between churn and deposits. Since the same four origins select and score the
method, the lower MAE is a selection result rather than an unbiased estimate
of future accuracy.
