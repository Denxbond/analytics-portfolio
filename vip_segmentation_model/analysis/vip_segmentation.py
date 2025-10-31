"""VIP player segmentation using KMeans clustering.

This script standardizes behavioral metrics, applies KMeans clustering,
assigns human-readable segment labels, summarizes cluster characteristics,
and produces a scatter plot of deposit vs. revenue colored by segment.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "synthetic_player_metrics.csv"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
PLOT_PATH = REPORTS_DIR / "vip_segment_clusters.png"

SEGMENT_NAMES = {
    "high": "High Roller",
    "mid": "Regular",
    "low": "Dormant",
}

def load_data(path: Path) -> pd.DataFrame:
    """Load player metrics from CSV and ensure numeric types."""
    df = pd.read_csv(path)
    numeric_cols = [col for col in df.columns if col != "user_id"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df.dropna().reset_index(drop=True)

def segment_players(df: pd.DataFrame):
    """Standardize numeric features, fit KMeans, and assign segments."""
    features = df.select_dtypes(include="number")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
    df["cluster"] = kmeans.fit_predict(scaled_features)

    cluster_means = (
        df.groupby("cluster")[features.columns]
        .mean()
        .sort_values(by="net_revenue", ascending=False)
    )

    label_map = {}
    for idx, cluster_id in enumerate(cluster_means.index):
        if idx == 0:
            label_map[cluster_id] = SEGMENT_NAMES["high"]
        elif idx == 1:
            label_map[cluster_id] = SEGMENT_NAMES["mid"]
        else:
            label_map[cluster_id] = SEGMENT_NAMES["low"]

    df["segment"] = df["cluster"].map(label_map)
    return df, cluster_means, label_map

def plot_segments(df: pd.DataFrame, path: Path) -> None:
    """Generate and save scatter plot of deposits vs. net revenue."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="deposits",
        y="net_revenue",
        hue="segment",
        palette="viridis",
        alpha=0.7,
    )
    plt.title("VIP Player Segmentation")
    plt.xlabel("Deposits")
    plt.ylabel("Net Revenue")
    plt.legend(title="Segment")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

def summarize_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary statistics table for each segment."""
    numeric_cols = [col for col in df.columns if col not in {"user_id", "cluster", "segment"}]
    summary = df.groupby("segment")[numeric_cols].mean().round(2)
    summary["player_count"] = df.groupby("segment")["user_id"].count()
    return summary.reset_index()

def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(DATA_PATH)
    segmented_df, cluster_means, label_map = segment_players(df)
    summary = summarize_segments(segmented_df)
    plot_segments(segmented_df, PLOT_PATH)

    print("Segment label mapping (cluster -> segment):")
    for cluster_id, segment_name in label_map.items():
        print(f"  Cluster {cluster_id}: {segment_name}")

    print("\nCluster mean metrics (sorted by net revenue):")
    print(cluster_means.round(2))

    print("\nSegment summary (mean metrics and counts):")
    print(summary)

if __name__ == "__main__":
    main()
