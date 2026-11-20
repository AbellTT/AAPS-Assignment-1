"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Step 3: High-Resolution Plot Generation

This script reads benchmark_results.csv and produces:
1. Part 1 Graphs (12 plots): Execution Time (ms) vs. Input Size (n)
   for each Algorithm x Input Type combination.
2. Part 2 Graphs (12 plots): Number of Comparisons vs. Input Size (n)
   for each Algorithm x Input Type combination.
3. Comparative Overlay Graphs (8 plots): Direct head-to-head comparisons
   of all 3 algorithms for each input type (Time and Comparisons).
4. Master 2x2 Dashboards (2 plots): Consolidated multi-panel figures
   for easy inclusion in academic reports and presentations.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configure publication-quality plot appearance
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

CSV_PATH = "benchmark_results.csv"
OUTPUT_DIR = "figures"

# Distinct color palette per algorithm
ALGO_COLORS = {
    "Insertion Sort": "#d62728",  # Red
    "Quick Sort": "#1f77b4",      # Blue
    "Merge Sort": "#2ca02c",      # Green
}

ALGO_MARKERS = {
    "Insertion Sort": "s",  # Square
    "Quick Sort": "o",      # Circle
    "Merge Sort": "^",      # Triangle
}


def create_directories():
    """Creates directory structure for output figures."""
    for sub in ["time", "comparisons", "comparative", "dashboards"]:
        os.makedirs(os.path.join(OUTPUT_DIR, sub), exist_ok=True)


def plot_single(
    df: pd.DataFrame,
    algo: str,
    itype: str,
    metric: str,
    output_path: str,
):
    """Generates an individual high-resolution plot for a single algorithm & input type."""
    subset = df[(df["Algorithm"] == algo) & (df["Input Type"] == itype)].sort_values("Size (n)")

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=300)
    color = ALGO_COLORS.get(algo, "#333333")
    marker = ALGO_MARKERS.get(algo, "o")

    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Execution Time" if metric == "Time (ms)" else "Comparison Operations"

    ax.plot(
        subset["Size (n)"],
        subset[metric],
        marker=marker,
        color=color,
        linewidth=2,
        markersize=6,
        label=f"{algo} ({itype})",
    )

    ax.set_title(f"{algo} — {title_metric}\n[{itype} Input]", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=10, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=10, fontweight="bold")

    ax.grid(True, linestyle="--", alpha=0.6)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))

    # Annotate final data point
    last_row = subset.iloc[-1]
    last_x, last_y = last_row["Size (n)"], last_row[metric]
    val_str = f"{last_y:,.1f} ms" if metric == "Time (ms)" else f"{int(last_y):,}"
    ax.annotate(
        f"n={int(last_x):,}\n{val_str}",
        xy=(last_x, last_y),
        xytext=(-45, 12),
        textcoords="offset points",
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.3", fc="#f0f0f0", ec="#cccccc", lw=0.8),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#666666"),
    )

    ax.legend(loc="upper left", frameon=True, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_comparative_overlay(
    df: pd.DataFrame,
    itype: str,
    metric: str,
    output_path: str,
):
    """Generates a head-to-head comparison graph of all 3 algorithms for a specific input type."""
    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=300)
    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Running Time" if metric == "Time (ms)" else "Comparison Counts"

    for algo in ["Insertion Sort", "Quick Sort", "Merge Sort"]:
        subset = df[(df["Algorithm"] == algo) & (df["Input Type"] == itype)].sort_values("Size (n)")
        ax.plot(
            subset["Size (n)"],
            subset[metric],
            marker=ALGO_MARKERS[algo],
            color=ALGO_COLORS[algo],
            linewidth=2.2,
            markersize=6,
            label=algo,
        )

    ax.set_title(f"Algorithm Comparison: {title_metric}\n[{itype} Input]", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=11, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=11, fontweight="bold")

    ax.grid(True, linestyle="--", alpha=0.6)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))

    ax.legend(loc="upper left", frameon=True, framealpha=0.95, fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_dashboard(df: pd.DataFrame, metric: str, output_path: str):
    """Generates a 2x2 multi-panel dashboard comparing all 3 algorithms across all 4 input types."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    metric_name = "Execution Time (ms)" if metric == "Time (ms)" else "Comparison Count"
    fig.suptitle(f"SWEG 5012: Comprehensive {metric_name} Analysis", fontsize=16, fontweight="bold", y=0.98)

    for idx, itype in enumerate(input_types):
        ax = axes[idx // 2, idx % 2]

        for algo in ["Insertion Sort", "Quick Sort", "Merge Sort"]:
            subset = df[(df["Algorithm"] == algo) & (df["Input Type"] == itype)].sort_values("Size (n)")
            ax.plot(
                subset["Size (n)"],
                subset[metric],
                marker=ALGO_MARKERS[algo],
                color=ALGO_COLORS[algo],
                linewidth=2,
                markersize=5,
                label=algo,
            )

        ax.set_title(f"Input Type: {itype}", fontsize=12, fontweight="bold", pad=8)
        ax.set_xlabel("Input Size (n)", fontsize=9, fontweight="bold")
        ax.set_ylabel(metric_name, fontsize=9, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))
        ax.legend(loc="upper left", frameon=True, fontsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path)
    plt.close()


def main():
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] '{CSV_PATH}' not found. Please run benchmark_runner.py first.")
        return

    df = pd.read_csv(CSV_PATH)
    create_directories()

    algorithms = ["Insertion Sort", "Quick Sort", "Merge Sort"]
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    print("=" * 70)
    print(" SWEG 5012: Generating High-Resolution Figures (Step 3)")
    print("=" * 70)

    # 1. Part 1: Individual Execution Time Plots (12 plots)
    print("\n[1/4] Generating 12 Individual Execution Time Plots (Part 1)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "time", f"time_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Time (ms)", out_file)
            print(f"  Created: {out_file}")

    # 2. Part 2: Individual Comparison Count Plots (12 plots)
    print("\n[2/4] Generating 12 Individual Comparison Count Plots (Part 2)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "comparisons", f"comp_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Comparisons", out_file)
            print(f"  Created: {out_file}")

    # 3. Comparative Overlays (8 plots: 4 for Time, 4 for Comparisons)
    print("\n[3/4] Generating 8 Head-to-Head Comparative Plots...")
    for itype in input_types:
        itype_slug = itype.lower().replace(" ", "_")
        time_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_time_{itype_slug}.png")
        comp_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_comp_{itype_slug}.png")
        plot_comparative_overlay(df, itype, "Time (ms)", time_out)
        plot_comparative_overlay(df, itype, "Comparisons", comp_out)
        print(f"  Created: {time_out}")
        print(f"  Created: {comp_out}")

    # 4. Master 2x2 Dashboards (2 plots)
    print("\n[4/4] Generating Master 2x2 Dashboards...")
    time_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_running_time.png")
    comp_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_comparisons.png")
    plot_dashboard(df, "Time (ms)", time_dash)
    plot_dashboard(df, "Comparisons", comp_dash)
    print(f"  Created: {time_dash}")
    print(f"  Created: {comp_dash}")

    print("\n" + "=" * 70)
    print(f"[SUCCESS] All 34 publication-quality plots generated in '{OUTPUT_DIR}/'!")
    print("=" * 70)


if __name__ == "__main__":
    main()
