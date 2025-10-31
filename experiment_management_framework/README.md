# Experiment Management Framework with ROTI Scoring

This lightweight framework demonstrates how a growth team can prioritize and
communicate experiment outcomes using Return on Time Invested (ROTI) as a
portfolio health metric. The tracker captures each experiment's hypothesis,
primary metric, statistical signal, resulting decision, and recommended next
step so stakeholders can quickly understand what is working and what should be
revisited.

## Dataset

The [`experiments.csv`](./experiments.csv) file contains ten synthetic product
experiments with plausible outcomes. ROTI scores combine impact, confidence, and
implementation effort so teams can compare initiatives on an apples-to-apples
basis. By logging next actions alongside decisions, the tracker keeps momentum
on follow-up work while documenting learning.

## Reporting Script

Run [`run_experiment_report.py`](./run_experiment_report.py) to summarize the
portfolio:

```bash
python run_experiment_report.py
```

The script outputs:

- Success and failure rates based on "Ship" decisions.
- Average ROTI per experiment metric to highlight where investments are paying
  off.
- A ranked list of experiments sorted by ROTI to focus attention on the highest
  leverage learnings.

Add the optional `--plot` flag with a destination path to produce a bar chart of
average ROTI by metric when `matplotlib` is installed.

## How it Supports Prioritization and Growth Decisions

- **Focus on Outcomes:** ROTI scoring emphasizes experiments that deliver the
  highest return for the time invested, making it easier to choose the next big
  bet.
- **Structured Learning Loop:** Capturing hypotheses, decisions, and next
  actions ensures that every test closes the loop and informs future backlog
  grooming.
- **Resource Allocation:** Tracking success rates and metric-level ROTI helps
  allocate analyst, design, and engineering effort to the product areas that
  demonstrate the strongest payback.

Teams can extend the framework by adding experiment owners, estimated revenue
impact, or linking out to dashboards for deeper exploration.

