"""User journey path analysis using synthetic clickstream data."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


EVENT_SEQUENCE = ["landing", "browse", "register", "deposit", "exit"]


def generate_user_path(rng: np.random.Generator) -> List[str]:
    """Generate a synthetic navigation path with up to five steps."""

    path: List[str] = ["landing"]

    # Browsing usually happens after landing.
    if rng.random() < 0.85:
        path.append("browse")
        # A subset of users continue browsing instead of registering immediately.
        if rng.random() < 0.2 and len(path) < 5:
            path.append("browse")

    # Registration depends on the browsing intent.
    if "browse" in path and rng.random() < 0.45 and len(path) < 5:
        path.append("register")
        if rng.random() < 0.55 and len(path) < 5:
            path.append("deposit")

    if len(path) < 5:
        path.append("exit")

    # Ensure we keep at most five steps.
    return path[:5]


def build_clickstream_dataframe(num_users: int, seed: int) -> pd.DataFrame:
    """Create a synthetic clickstream dataset for the requested number of users."""

    rng = np.random.default_rng(seed)
    records: List[Dict[str, object]] = []
    base_timestamp = pd.Timestamp("2024-01-01")

    for idx in range(num_users):
        user_id = f"U{idx + 1:05d}"
        path = generate_user_path(rng)
        start_offset_days = int(rng.integers(0, 30))
        event_time = base_timestamp + pd.Timedelta(days=start_offset_days)

        for step, event in enumerate(path):
            if step > 0:
                # Add a few hours between events to emulate realistic timelines.
                event_time += pd.Timedelta(hours=int(rng.integers(1, 36)))

            records.append(
                {
                    "user_id": user_id,
                    "event_index": step,
                    "event_type": event,
                    "event_timestamp": event_time,
                }
            )

    return pd.DataFrame.from_records(records)


def summarize_paths(clickstream: pd.DataFrame) -> pd.DataFrame:
    """Aggregate user paths and compute conversion for each path."""

    ordered = clickstream.sort_values(["user_id", "event_index"])

    path_data = (
        ordered.groupby("user_id")
        .agg(
            path=("event_type", lambda events: " > ".join(list(events)[:5])),
            converted=(
                "event_type",
                lambda events: int("deposit" in set(events)),
            ),
        )
        .reset_index()
    )

    summary = (
        path_data.groupby("path")
        .agg(users=("user_id", "nunique"), conversions=("converted", "sum"))
        .reset_index()
    )
    summary["conversion_rate"] = summary["conversions"] / summary["users"]
    summary = summary.sort_values(["users", "conversion_rate"], ascending=[False, False])
    return summary


def print_top_paths(summary: pd.DataFrame, top_n: int = 5) -> None:
    """Display the top navigation paths with their performance metrics."""

    print("Top user journey paths")
    print("-" * 80)
    header = f"{'Path':50}  {'Users':>8}  {'Conv.':>8}  {'Rate':>8}"
    print(header)
    print("-" * 80)

    for _, row in summary.head(top_n).iterrows():
        path = row["path"]
        users = int(row["users"])
        conversions = int(row["conversions"])
        rate = row["conversion_rate"]
        print(f"{path[:50]:50}  {users:8d}  {conversions:8d}  {rate:7.1%}")

    print("-" * 80)
    overall_rate = summary["conversions"].sum() / summary["users"].sum()
    print(f"Overall conversion rate across all paths: {overall_rate:.1%}\n")


def build_transition_graph(clickstream: pd.DataFrame) -> Tuple[nx.DiGraph, Counter]:
    """Create a directed graph of event transitions and node visit counts."""

    ordered = clickstream.sort_values(["user_id", "event_index"])
    transitions: Counter[Tuple[str, str]] = Counter()
    node_counts: Counter[str] = Counter()

    for _, group in ordered.groupby("user_id"):
        events = group["event_type"].tolist()
        node_counts.update(events)
        for src, dst in zip(events[:-1], events[1:]):
            transitions[(src, dst)] += 1

    graph = nx.DiGraph()
    for (src, dst), weight in transitions.items():
        graph.add_edge(src, dst, weight=weight)

    for node, weight in node_counts.items():
        graph.add_node(node, visits=weight)

    return graph, node_counts


def plot_user_journey_graph(
    graph: nx.DiGraph,
    node_counts: Counter,
    output_path: Path,
) -> None:
    """Visualize the journey transitions and save the diagram to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 5))

    order = {event: idx for idx, event in enumerate(EVENT_SEQUENCE)}
    pos = {node: (order.get(node, idx), 0) for idx, node in enumerate(graph.nodes)}

    max_visits = max(node_counts.values()) if node_counts else 1
    node_sizes = [400 + 1200 * (node_counts[node] / max_visits) for node in graph.nodes]

    max_weight = max((data["weight"] for _, _, data in graph.edges(data=True)), default=1)
    edge_widths = [1 + 4 * (data["weight"] / max_weight) for _, _, data in graph.edges(data=True)]

    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color="#3C7DC4", alpha=0.85)
    nx.draw_networkx_labels(graph, pos, font_color="white", font_weight="bold")
    nx.draw_networkx_edges(
        graph,
        pos,
        width=edge_widths,
        arrowstyle="-|>",
        arrowsize=20,
        edge_color="#243447",
    )
    edge_labels = {(u, v): data["weight"] for u, v, data in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9, label_pos=0.5)

    plt.title("User Journey Transition Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved journey graph to {output_path.resolve()}")


def save_clickstream(clickstream: pd.DataFrame, output_path: Path) -> None:
    """Persist the synthetic clickstream dataset to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    clickstream.to_csv(output_path, index=False)
    print(f"Saved synthetic clickstream data to {output_path.resolve()}")


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate and analyze user journeys.")
    parser.add_argument("--users", type=int, default=5000, help="Number of synthetic users to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("../data/synthetic_clickstream_data.csv"),
        help="Output path for the generated dataset.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("../reports/user_journey_graph.png"),
        help="Output path for the journey graph visualization.",
    )
    return parser.parse_args(args)


def main() -> None:
    args = parse_args()

    clickstream = build_clickstream_dataframe(args.users, args.seed)
    save_clickstream(clickstream, args.data_path)

    summary = summarize_paths(clickstream)
    print_top_paths(summary)

    graph, node_counts = build_transition_graph(clickstream)
    plot_user_journey_graph(graph, node_counts, args.report_path)


if __name__ == "__main__":
    main()
