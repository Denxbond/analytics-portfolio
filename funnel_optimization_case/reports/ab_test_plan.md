# Reg→Dep Funnel Experiment Playbook

## Context
A recent review of the registration-to-deposit funnel highlighted above-average
drop-off for players acquired through Paid Search. Qualitative research revealed
that users hesitated at the payment verification step, resulting in a 12%
lower conversion rate relative to other paid channels.

## Hypothesis
If we streamline the payment verification modal for Paid Search cohorts by
adding contextual copy and reducing required fields, the Reg→Dep conversion rate
will increase without hurting average revenue per paying user (ARPPU).

## Test Design
- **Population:** New users entering the funnel from Paid Search campaigns.
- **Primary KPI:** Reg→Dep conversion rate within 7 days of registration.
- **Secondary KPIs:** ARPU, ARPPU, verification completion time, verification drop-off.
- **Minimum Detectable Effect:** +8% relative lift in conversion.
- **Sample Size:** 4,200 registrations (powered at 90% with alpha = 0.05).
- **Experiment Length:** 14 days (based on average daily registrations).
- **Guardrails:** Monitor deposit error rate, CS tickets, and fraudulent activity
  to ensure there are no regressions.

## Analysis Approach
1. Use the SQL model in `../sql/funnel_conversion.sql` to build baseline metrics.
2. During the test, segment treatment vs. control with experiment metadata.
3. Apply a two-proportion z-test to validate lift in conversion rate.
4. Compare revenue metrics (ARPU, ARPPU) to confirm there is no cannibalization.
5. Share results via dashboard snapshot and executive summary in the project README.

## Rollout Recommendation
Proceed with a phased rollout if the primary KPI shows a statistically
significant lift with neutral secondary metrics. If ARPPU declines by more than
5%, run a follow-up test to refine the verification messaging before full
rollout.
