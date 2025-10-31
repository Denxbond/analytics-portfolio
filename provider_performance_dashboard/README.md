# Provider Performance Dashboard

This dashboard simulates provider-level performance data to evaluate how each
content partner contributes to overall revenue, retention, and volatility. By
quantifying gross gaming revenue (GGR) share and highlighting top performers,
the analysis helps product and partnership teams prioritize optimization
opportunities.

## What the analysis includes

- Synthetic dataset covering provider_id, games_count, unique_players,
  total_bets, total_wins, revenue, and retention_rate.
- Calculation of each provider's GGR share to quantify contribution to total
  revenue.
- Visualization of the top 10 providers by revenue and by retention to spot
  outliers that may deserve deeper review.

## How this dashboard informs strategy

- **Optimize the game mix:** Identify high-revenue providers with weaker
  retention for potential content refreshes or targeted promotions.
- **Strengthen partnerships:** Use retention standouts to negotiate new
  exclusives or prioritize integration support.
- **Manage volatility:** Understanding each provider's revenue contribution and
  player engagement helps balance the portfolio and reduce reliance on a few
  partners.

Run `analysis/provider_performance.py` to regenerate the dataset and charts.
