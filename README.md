# Product Analytics Portfolio Cases

This portfolio demonstrates how data can be used to evaluate product, growth, and monetization decisions under uncertainty using experimentation, forecasting, and economic modeling.
Each case study represents analytical frameworks I’ve used in real-world environments.

- Explore each case folder for business context, dataset, and analysis outputs.
- Install standard Python dependencies (`pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`) to reproduce metrics locally.
- SQL models illustrate how key metrics could be materialized in a data warehouse or dbt project using anonymized data.

## Projects
- [Funnel Optimization Case Study](funnel_optimization_case/README.md):  
  Reg→Dep funnel analysis with SQL, Python, and an experiment playbook.

- [Retention Cohort Dashboard](retention_cohort_dashboard/README.md):  
  Weekly cohort retention heatmap built from synthetic lifecycle events.

- [A/B Test Simulator](ab_test_simulator/README.md):  
  Controlled experiment simulation with lift, p-value, and power reporting.

- [User Journey Path Analysis](user_journey_path_analysis/README.md):  
  Behavioural path aggregation and journey visualization from clickstream data.

- [Revenue Forecast Model](revenue_forecast_model/README.md):  
  Forecasts next-quarter revenue using deposit and churn data.

- [Bonus Offer Impact Analysis](bonus_offer_impact_analysis/README.md):  
  Evaluates how a promotional bonus affects deposit frequency and ARPU using simulated user data.

- [Deposit Funnel Analysis](deposit_funnel_analysis/README.md):  
  Quantifies user drop-off and conversion across key funnel stages using synthetic event logs.

- [VIP Segmentation Model](vip_segmentation_model/README.md):  
  Clusters players into behavioral segments (Dormant, Regular, High Roller) using KMeans and financial activity data.

- [Provider Performance Dashboard](provider_performance_dashboard/README.md):  
  Compares revenue, bet volume, and RTP across slot providers to highlight top performers.

- [Conversion Forecast Bonus](conversion_forecast_bonus/README.md):  
  Models short-term uplift in conversion following a promotional campaign using exponential smoothing.

- [Growth Experiment Tracker](experiment_management_framework/README.md):  
  Centralized framework for managing hypotheses, test results, and ROTI scoring using synthetic experiment data.

- [North Star Metric Dashboard](nsm_dashboard_simulation/README.md):  
  Integrates activation, retention, and monetization metrics to visualize the product’s primary growth driver.

- [Pricing & Incentive Elasticity Model](bonus_sensitivity_model/README.md):  
  Simulates how varying bonus percentages impact LTV and margin to find the optimal trade-off between growth and profitability.

- [Feature Impact Analysis](feature_rollout_simulation/README.md):  
  Measures engagement and conversion uplift pre/post feature release using synthetic rollout metrics.

- [Growth Strategy Playbook](growth_strategy_playbook/README.md):  
  Documentation outlining strategic hypotheses and experiment roadmap for scaling key metrics of a rider app.

- [Experimentation System Architecture](experimentation_system_architecture/README.md):  
  Describes event flow from tracking to data warehouse to dashboards, demonstrating system-level thinking in analytics design.

- [Business Review Dashboard](business_review_dashboard/README.md):  
  Aggregates core KPIs (NSM, ARPU, retention, churn) into a quarterly business health overview with insights narrative.

## Disclaimer
All projects are inspired by analytical challenges I’ve solved professionally, but no proprietary data, logic, or business context is included.  
All datasets are synthetic and anonymized, created solely for demonstration.  
Any resemblance to real products, metrics, or organizations is purely coincidental.
