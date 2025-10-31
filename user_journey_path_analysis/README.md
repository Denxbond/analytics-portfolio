# User Journey Path Analysis

## Project Purpose
This project simulates anonymized clickstream behaviour for a fictional product to
identify the most common navigation paths from landing to monetisation. It shows
how behavioural analytics and journey visualisation can uncover conversion
bottlenecks before running live experiments.

## How to Run the Analysis
1. Create a virtual environment and install the required libraries:
   ```bash
   pip install pandas numpy matplotlib networkx
   ```
2. Execute the simulator from the project root to regenerate all assets:
   ```bash
   python analysis/user_path_analysis.py
   ```
   Optional flags:
   - `--users` to change the number of synthetic users (default: 5000).
   - `--seed` to control randomness for reproducibility.

Running the script saves the dataset to `data/synthetic_clickstream_data.csv`
and exports the journey graph to `reports/user_journey_graph.png`.

## Example Console Output
```
Top user journey paths
--------------------------------------------------------------------------------
Path                                                   Users     Conv.     Rate
--------------------------------------------------------------------------------
landing > browse > exit                                 1875         0      0.0%
landing > browse > register > deposit > exit             845       845    100.0%
landing > exit                                           740         0      0.0%
landing > browse > register > exit                       722         0      0.0%
landing > browse > browse > exit                         454         0      0.0%
--------------------------------------------------------------------------------
Overall conversion rate across all paths: 20.9%
```

## Visualisation Output
The script builds a directed network diagram stored at
`reports/user_journey_graph.png`. Node sizes correspond to event frequency,
and edge labels show how many users move between steps (landing → browse,
browse → register, and so on). This makes it easy to spot the strongest
conversion routes and identify where players drop out.
