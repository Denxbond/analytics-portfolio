# VIP Segmentation Model

This project segments a synthetic portfolio of casino players into actionable VIP cohorts using unsupervised clustering. The workflow highlights how behavioral data informs VIP targeting, retention programs, and cross-sell strategies.

## Project Structure

```
vip_segmentation_model/
├── analysis/
│   └── vip_segmentation.py
├── data/
│   └── synthetic_player_metrics.csv
└── reports/
    └── vip_segment_clusters.png
```

## Data

The `data/synthetic_player_metrics.csv` file contains 500 synthetic player records with the following metrics:

- **deposits** – total amount deposited during the observed period
- **sessions** – count of active gaming sessions
- **wagered_amount** – aggregate amount wagered
- **net_revenue** – contribution margin after bonuses
- **days_active** – number of unique active days

## Methodology

1. **Standardization** – Continuous metrics are standardized to remove scale bias.
2. **Clustering** – A KMeans model with `k=3` segments players into behaviorally similar groups.
3. **Segment Naming** – Clusters are ordered by mean net revenue and mapped to business-friendly labels:
   - **High Roller** – Highest value customers with large deposits, high wagering volume, and frequent activity.
   - **Regular** – Consistent players with moderate deposit and play patterns.
   - **Dormant** – Low activity users with limited deposits and revenue contributions.
4. **Visualization** – A scatter plot of deposits vs. net revenue highlights segment separation.
5. **Reporting** – A summary table provides mean metrics and player counts for each segment, supporting downstream analysis.

## Running the Analysis

```bash
python analysis/vip_segmentation.py
```

The script prints the cluster-to-segment mapping, cluster means, and segment summary table. It also saves the `reports/vip_segment_clusters.png` chart.

## CRO Value

Targeting VIP cohorts based on behavioral segmentation enables marketing teams to:

- Prioritize **High Rollers** with personalized retention offers and loyalty tiers that maximize lifetime value.
- Nurture **Regular** players with timely promotions and cross-sell messaging to grow their engagement.
- Re-engage **Dormant** users through win-back campaigns optimized for low activity players.

By aligning incentives with segment-specific behaviors, the business can improve conversion rates, reduce churn, and capture incremental VIP revenue.
