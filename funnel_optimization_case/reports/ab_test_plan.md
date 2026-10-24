# Reg→Dep Funnel Experiment Playbook

## Context
The bundled synthetic dataset contains 20 registrations and a descriptive
channel-level conversion gap. It has no payment-step events or qualitative
research, so the cause of the gap is unknown. Treat payment verification as a
testable hypothesis, not an established diagnosis.

## Hypothesis
If we streamline the payment verification modal for Paid Search cohorts by
adding contextual copy and reducing required fields, the 7-day
registration-to-first-deposit conversion rate will increase. This mechanism
and outcome must be tested with randomized assignment.

## Test Design
- **Population:** New users entering the funnel from Paid Search campaigns.
- **Primary KPI:** Distinct users with a first deposit in `[registration, registration + 7 days)` / eligible randomized users.
- **Secondary KPIs:** Deposit errors, verification completion, support contacts, and revenue per randomized user over a predeclared window.
- **Sample size:** Calculate from a measured baseline, chosen minimum detectable effect, two-sided alpha, and target power before launch. The current synthetic sample does not establish these inputs.
- **Experiment length:** Enroll for the planned sample size, then allow each user a full 7-day outcome window.
- **Guardrails:** Monitor deposit error rate, CS tickets, and fraudulent activity
  to ensure there are no regressions.

## Analysis Approach
1. Use the SQL model in `../sql/funnel_conversion.sql` to build baseline metrics.
2. During the test, segment treatment vs. control with experiment metadata.
3. Compare randomized arms with a two-proportion method and report the absolute difference and confidence interval.
4. Analyze revenue per randomized user separately with a predeclared window; do not infer no harm from an underpowered non-significant result.

## Rollout Recommendation
Proceed only if the prespecified primary analysis and guardrails support it.
The sample data in this repository is not an experiment result and cannot
justify a rollout decision.
