# Experimentation System Architecture

Concise blueprint for capturing product events, transforming them into decision-ready metrics, and powering experiment rollouts.

## Architecture Overview

```mermaid
graph LR
    user[User Session] --> app[Product UI]
    app --> gtm[GTM Container + Client SDKs]
    gtm --> collector[Event Collector / Edge Network]
    collector --> raw[Raw Event Tables (Cloud Storage / Landing Zone)]
    raw --> pipelines[Streaming + Batch Pipelines]
    pipelines --> warehouse[Analytics Warehouse]
    warehouse --> metrics[Metrics Layer (dbt models / SQL views)]
    metrics --> evaluator[Experiment Evaluator Service]
    evaluator --> decision[Decision Engine / Feature Flags]
    metrics --> dashboard[Experiment Dashboard]
    dashboard --> decision
```

## Event Tracking (Frontend + GTM)
- **Instrumentation strategy:** Maintain a versioned tracking plan (event names, schemas, experiment metadata keys) shared with engineering. Embed tracking via lightweight SDK wrappers to enforce schema validation and automatic experiment context payloads.
- **Client delivery:** Deploy tags through Google Tag Manager (GTM) to separate release cadences from application deployments. Use a single GTM workspace per environment with automated publishing pipelines.
- **Context enrichment:** Capture user identifiers (anonymous + authenticated), device traits, page/app state, and active experiment assignments before dispatching events. Apply consent management for privacy compliance.
- **Reliability controls:** Queue events with retry logic, batch dispatch on visibility changes, and monitor client drop rates to detect instrumentation regressions.

## Data Ingestion (Warehouse / Pipelines)
- **Streaming ingest:** Fan-out GTM events to an edge collector (e.g., Cloud Functions, Snowplow collector) that writes to append-only raw tables or cloud storage. Partition by event date and namespace for cost-efficient querying.
- **Batch pipelines:** Use scheduled ELT jobs (Airflow, dbt Cloud) to replay GTM export files and backfill late-arriving data. Validate payload schemas using contracts to fail fast.
- **Identity resolution:** Run deterministic + probabilistic stitching to merge anonymous identifiers with user IDs, producing a unified `user_dim` for experiment segmentation.
- **Observability:** Emit pipeline metrics (lag, throughput, schema drift) and integrate with alerting to guarantee SLA adherence.

## Metrics Layer (SQL or dbt)
- **Modeling:** Transform raw events into cleaned fact tables (`fact_event`, `fact_experiment_exposure`) and dimensions (`dim_user`, `dim_feature`). Implement in dbt with tests for uniqueness, nulls, and referential integrity.
- **Metric definitions:** Encode reusable metrics (conversion, retention, revenue) as dbt metrics or SQL views parameterized by windowing, filters, and attribution logic. Version control metric definitions to align experimentation and dashboards.
- **Feature flags + exposures:** Produce canonical exposure tables that record variant, timestamp, traffic allocation, and guardrail metrics for every assignment.
- **Data products:** Publish semantic models to a metrics API (e.g., Transform, MetricFlow) to support downstream applications while enforcing governance and lineage tracking.

## Experiment Evaluation (Python or Dashboard)
- **Computation engine:** Build a Python package (Pandas, PySpark, or SQL-first) that materializes experiment cohorts, computes uplift, and applies sequential testing or Bayesian inference. Bundle guardrail checks and sample ratio mismatch detection.
- **Automation:** Schedule evaluations via orchestrators, writing outputs to a shared schema (`fact_experiment_results`) with confidence intervals, decision status, and recommended actions.
- **Visualization:** Expose metrics through dashboards (Looker, Hex) that source from the metrics layer, enabling drill-down by segment and time. Offer notebooks for ad-hoc deep dives with reproducible query templates.
- **Decision workflow:** Integrate evaluation outputs with feature flag platforms (LaunchDarkly, Optimizely) to auto-update rollout rules, and notify stakeholders via Slack/Email when decisions are ready.
