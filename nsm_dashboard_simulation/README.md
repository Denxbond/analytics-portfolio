# North Star Metric Dashboard Simulation

This simulation demonstrates how a composite North Star Metric (NSM) can be decomposed into the three operational levers that most often drive digital product growth: activation, retention, and monetization. By tracking each contributor alongside the aggregate NSM, teams can quickly diagnose where improvements will have the highest business impact.

## Conceptual Framework

- **Activation Rate** measures the proportion of new users that reach a defined success milestone. It captures the effectiveness of onboarding experiences, messaging, and product fit during early usage.
- **Retention Rate** reflects how well the product continues to deliver value over time. Improvements to core product features, lifecycle marketing, and support are typically designed to lift this metric.
- **Monetization Rate** captures the fraction of retained users that convert to revenue, either through direct purchases or ad impressions. Pricing, packaging, and paywall optimization directly influence this lever.

The North Star Metric is modeled as the product of these three rates:

\[ \text{NSM} = \text{Activation} \times \text{Retention} \times \text{Monetization} \]

Because the NSM compounds the three components, incremental gains in any driver propagate throughout the customer lifecycle. The dashboard provides month-over-month views so operators can align initiatives—such as onboarding experiments, feature launches, or pricing tests—with observed performance changes in each lever and the resulting NSM movement.

## Deliverables

Running `nsm_dashboard_simulation.py` generates:

1. `nsm_metrics.csv` – Monthly activation, retention, monetization, and NSM values (expressed as percentages).
2. `nsm_trends.png` – A line chart showing the trends for the three input metrics and the resulting NSM.
3. This README – A reference for how the metrics map to actionable growth levers.

