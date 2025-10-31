# Revenue Forecast Model

## Overview
This project simulates monthly deposit activity and churn behavior for a fictional online gaming platform. Using the synthetic history, it fits an exponential smoothing model to forecast revenue for the upcoming quarter and produces a report-ready visualization.

## How to Run the Notebook
1. Open `analysis/revenue_forecast.ipynb` in Jupyter Lab, Jupyter Notebook, or VS Code.
2. Execute the cells in order to regenerate the synthetic dataset, train the Holt-Winters model, and refresh all outputs.
3. The notebook saves updated artifacts to:
   - `data/synthetic_revenue_data.csv`
   - `reports/revenue_forecast_chart.png`

## Example Summary Output
```
Total historical revenue: $2,555,915.66
Forecasted next-quarter revenue: $316,762.63
Churn trend: decreasing
```

## Skill Demonstrated
- Forecasting & business modeling
