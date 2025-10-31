# Bonus Sensitivity Model

This project provides a lightweight simulation of how promotional bonus levels influence key commercial metrics such as user conversion, lifetime value (LTV), and contribution margin. By sweeping bonus percentages from 0% to 50%, the model quantifies the elasticity of LTV relative to bonus changes and highlights the trade-off between growth and profitability.

## Files
- `bonus_sensitivity_analysis.ipynb` – interactive notebook that generates synthetic data, calculates LTV elasticity, visualizes sensitivity, and prints a growth-versus-profitability table.
- `bonus_sensitivity_data.csv` – synthetic dataset covering bonus percentages, conversion rates, LTV, gross margin, and derived contribution metrics.
- `ltv_elasticity.png` – static visualization of LTV elasticity across bonus levels.

## How to Use the Model
1. Open the notebook in Jupyter and run the cells to regenerate the dataset and figures.
2. Update the base assumptions (e.g., conversion baseline, LTV uplift, margin drag) to reflect specific iGaming or SaaS business contexts.
3. Compare elasticity and contribution margin across bonus levels to identify efficient incentive ranges.

## Informing Pricing and Bonus Policy Decisions
Sensitivity analysis like this helps go-to-market teams answer three core questions:
- **Growth impact:** Higher bonuses typically lift conversion and near-term revenue. The elasticity chart clarifies how much incremental LTV is gained for each extra percentage point of bonus.
- **Profitability guardrails:** Contribution margin combines conversion, LTV, and gross margin to show whether aggressive bonuses erode profitability beyond acceptable limits.
- **Policy calibration:** Product and CRM teams can use the trade-off table to set tiered bonus offers (e.g., welcome vs. retention promos) or SaaS discount ladders that balance user acquisition goals with sustainable margins.

By iterating on the assumptions, operators can pressure-test scenarios such as seasonal promotions, VIP incentives, or enterprise discount negotiations and align stakeholders on financially viable bonus strategies.
