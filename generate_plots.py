"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Step 3: High-Resolution Plot Generation (Clean Single-Graph Standard)

This script reads benchmark_results.csv and produces 42 standard linear plots:
1. Part 1 Graphs (16 plots): Execution Time (ms) vs. Input Size (n)
   for each Algorithm x Input Type combination (4 algorithms x 4 input types).
2. Part 2 Graphs (16 plots): Number of Comparisons vs. Input Size (n)
   for each Algorithm x Input Type combination.
3. Comparative Overlay Graphs (8 plots): Direct head-to-head comparisons
   of Insertion Sort, Quick Sort M3, and Merge Sort for each input type.
   - Uses Quick Sort M3 (median-of-three pivot) in comparative/dashboard views
     because it represents the corrected, production-quality version of Quick Sort.
   - Solves the overlapping problem using concentric marker styling and dual-strip line rendering:
     * Insertion Sort: Thick solid red line (linewidth=3.8) with large squares (size=9, dark red border).
     * Quick Sort M3: Medium dashed blue line (linewidth=2.0) with circles (size=5.5, white border).
     * Merge Sort: Dash-dot green line (linewidth=2.0) with triangles (size=7.5).
   - Includes an explicit data callout box at n = 10,000 for each algorithm.
4. Master 2x2 Dashboards (2 plots):
   - dashboard_running_time.png (Execution Time across all 4 input types, using Quick Sort M3)
   - dashboard_comparisons.png (Comparison Counts across all 4 input types, using Quick Sort M3)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Publication-grade typography and canvas setup
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

CSV_PATH = "benchmark_results.csv"
OUTPUT_DIR = "figures"


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

    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=300)

    # Distinct color and marker per algorithm
    color_map = {
        "Insertion Sort": ("#d62728", "s", "#800000"),
        "Quick Sort":     ("#1f77b4", "o", "#0d47a1"),
        "Quick Sort M3":  ("#9467bd", "D", "#5c2d91"),
        "Merge Sort":     ("#2ca02c", "^", "#1b5e20"),
    }
    color, marker, edge_color = color_map.get(algo, ("#333333", "o", "#000000"))

    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Execution Time" if metric == "Time (ms)" else "Comparison Operations"

    ax.plot(
        subset["Size (n)"],
        subset[metric],
        marker=marker,
        color=color,
        linestyle="-",
        linewidth=2.2,
        markersize=6.5,
        markerfacecolor=color,
        markeredgecolor=edge_color,
        markeredgewidth=1.0,
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
        fontsize=8.5,
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
    """
    Generates a head-to-head comparison graph of all 3 algorithms for an input type.
    Uses concentric markers and dual-width lines so identical overlapping curves are both clearly visible.
    """
    sub = df[df["Input Type"] == itype]
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)

    ins = sub[sub["Algorithm"] == "Insertion Sort"].sort_values("Size (n)")
    qs  = sub[sub["Algorithm"] == "Quick Sort M3"].sort_values("Size (n)")
    ms  = sub[sub["Algorithm"] == "Merge Sort"].sort_values("Size (n)")

    # 1. Insertion Sort: Solid Crimson Line (thick) with large Square markers
    ax.plot(
        ins["Size (n)"],
        ins[metric],
        color="#d62728",
        linestyle="-",
        linewidth=3.8,
        marker="s",
        markersize=9.0,
        markerfacecolor="#d62728",
        markeredgecolor="#800000",
        markeredgewidth=1.2,
        label="Insertion Sort",
        zorder=2,
    )

    # 2. Quick Sort M3: Dashed Purple Line with Diamond markers
    ax.plot(
        qs["Size (n)"],
        qs[metric],
        color="#9467bd",
        linestyle=(0, (4, 3)),
        linewidth=2.0,
        marker="D",
        markersize=8.5,
        markerfacecolor="#9467bd",
        markeredgecolor="white",
        markeredgewidth=1.2,
        label="Quick Sort M3",
        zorder=3,
    )

    # 3. Merge Sort: Dash-dot Emerald Line with Triangle markers
    ax.plot(
        ms["Size (n)"],
        ms[metric],
        color="#2ca02c",
        linestyle="-.",
        linewidth=2.0,
        marker="^",
        markersize=7.5,
        markerfacecolor="#2ca02c",
        markeredgecolor="#005500",
        markeredgewidth=1.0,
        label="Merge Sort",
        zorder=4,
    )

    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Running Time" if metric == "Time (ms)" else "Comparison Counts"

    ax.set_title(f"Algorithm Comparison: {title_metric}\n[{itype} Input]", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=11, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=11, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))

    # Summary callout box at n = 10,000
    ins_10k = ins[ins["Size (n)"] == 10000][metric].values[0]
    qs_10k  = qs[qs["Size (n)"] == 10000][metric].values[0]
    ms_10k  = ms[ms["Size (n)"] == 10000][metric].values[0]

    if metric == "Time (ms)":
        box_text = (
            f"At n = 10,000:\n"
            f"  Insertion Sort:  {ins_10k:,.1f} ms\n"
            f"  Quick Sort M3:   {qs_10k:,.1f} ms\n"
            f"  Merge Sort:      {ms_10k:,.1f} ms"
        )
    else:
        box_text = (
            f"At n = 10,000:\n"
            f"  Insertion Sort:  {int(ins_10k):,} comps\n"
            f"  Quick Sort M3:   {int(qs_10k):,} comps\n"
            f"  Merge Sort:      {int(ms_10k):,} comps"
        )

    ax.text(
        0.03,
        0.72,
        box_text,
        transform=ax.transAxes,
        fontsize=8.5,
        family="monospace",
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", fc="#f8f9fa", ec="#cccccc", lw=1),
    )

    ax.legend(loc="upper left", frameon=True, framealpha=0.95, fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_dashboard(df: pd.DataFrame, metric: str, output_path: str):
    """Generates a 2x2 multi-panel dashboard comparing all 3 algorithms across all 4 input types."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), dpi=300)
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    metric_name = "Execution Time (ms)" if metric == "Time (ms)" else "Comparison Count"
    fig.suptitle(f"SWEG 5012: Comprehensive {metric_name} Analysis", fontsize=16, fontweight="bold", y=0.98)

    for idx, itype in enumerate(input_types):
        ax = axes[idx // 2, idx % 2]
        sub = df[df["Input Type"] == itype]

        ins = sub[sub["Algorithm"] == "Insertion Sort"].sort_values("Size (n)")
        qs  = sub[sub["Algorithm"] == "Quick Sort M3"].sort_values("Size (n)")
        ms  = sub[sub["Algorithm"] == "Merge Sort"].sort_values("Size (n)")

        # Insertion Sort
        ax.plot(
            ins["Size (n)"],
            ins[metric],
            color="#d62728",
            linestyle="-",
            linewidth=3.2,
            marker="s",
            markersize=7.5,
            markerfacecolor="#d62728",
            markeredgecolor="#800000",
            markeredgewidth=1.0,
            label="Insertion Sort",
            zorder=2,
        )

        # Quick Sort M3
        ax.plot(
            qs["Size (n)"],
            qs[metric],
            color="#9467bd",
            linestyle=(0, (4, 3)),
            linewidth=1.8,
            marker="D",
            markersize=7.5,
            markerfacecolor="#9467bd",
            markeredgecolor="white",
            markeredgewidth=1.0,
            label="Quick Sort M3",
            zorder=3,
        )

        # Merge Sort
        ax.plot(
            ms["Size (n)"],
            ms[metric],
            color="#2ca02c",
            linestyle="-.",
            linewidth=1.8,
            marker="^",
            markersize=6.5,
            markerfacecolor="#2ca02c",
            markeredgecolor="#005500",
            markeredgewidth=1.0,
            label="Merge Sort",
            zorder=4,
        )

        ax.set_title(f"Input Type: {itype}", fontsize=12, fontweight="bold", pad=8)
        ax.set_xlabel("Input Size (n)", fontsize=9, fontweight="bold")
        ax.set_ylabel(metric_name, fontsize=9, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))

        # Summary callout box at n = 10,000
        ins_10k = ins[ins["Size (n)"] == 10000][metric].values[0]
        qs_10k  = qs[qs["Size (n)"] == 10000][metric].values[0]
        ms_10k  = ms[ms["Size (n)"] == 10000][metric].values[0]

        if metric == "Time (ms)":
            box_text = (
                f"At n = 10,000:\n"
                f"  Ins Sort:  {ins_10k:,.1f} ms\n"
                f"  QS M3:     {qs_10k:,.1f} ms\n"
                f"  Merge:     {ms_10k:,.1f} ms"
            )
        else:
            box_text = (
                f"At n = 10,000:\n"
                f"  Ins Sort:  {int(ins_10k):,}\n"
                f"  QS M3:     {int(qs_10k):,}\n"
                f"  Merge:     {int(ms_10k):,}"
            )

        ax.text(
            0.03, 0.97,
            box_text,
            transform=ax.transAxes,
            fontsize=7.5,
            family="monospace",
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f8f9fa", ec="#cccccc", lw=0.8),
        )

        ax.legend(loc="upper left", frameon=True, fontsize=8.5, bbox_to_anchor=(0.03, 0.72))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path)
    plt.close()


def main():
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] '{CSV_PATH}' not found. Please run benchmark_runner.py first.")
        return

    df = pd.read_csv(CSV_PATH)
    create_directories()

    algorithms = ["Insertion Sort", "Quick Sort", "Quick Sort M3", "Merge Sort"]
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    print("=" * 70)
    print(" SWEG 5012: Generating 42 Clean Single Plots (Step 3)")
    print("=" * 70)

    # 1. Part 1: Individual Execution Time Plots (16 plots: 4 algos x 4 input types)
    print("\n[1/4] Generating 16 Individual Execution Time Plots (Part 1)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "time", f"time_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Time (ms)", out_file)
            print(f"  Created: {out_file}")

    # 2. Part 2: Individual Comparison Count Plots (16 plots: 4 algos x 4 input types)
    print("\n[2/4] Generating 16 Individual Comparison Count Plots (Part 2)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "comparisons", f"comp_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Comparisons", out_file)
            print(f"  Created: {out_file}")

    # 3. Comparative Overlays (8 plots: 4 for Time, 4 for Comparisons)
    # Uses Quick Sort M3 in comparative overlays (corrected production variant)
    print("\n[3/4] Generating 8 Clean Comparative Plots (using Quick Sort M3)...")
    for itype in input_types:
        itype_slug = itype.lower().replace(" ", "_")
        time_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_time_{itype_slug}.png")
        comp_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_comp_{itype_slug}.png")
        plot_comparative_overlay(df, itype, "Time (ms)", time_out)
        plot_comparative_overlay(df, itype, "Comparisons", comp_out)
        print(f"  Created: {time_out}")
        print(f"  Created: {comp_out}")

    # 4. Master 2x2 Dashboards (2 plots, using Quick Sort M3)
    print("\n[4/4] Generating 2 Master Dashboards (using Quick Sort M3)...")
    time_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_running_time.png")
    comp_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_comparisons.png")
    plot_dashboard(df, "Time (ms)", time_dash)
    plot_dashboard(df, "Comparisons", comp_dash)
    print(f"  Created: {time_dash}")
    print(f"  Created: {comp_dash}")

    print("\n" + "=" * 70)
    print(f"[SUCCESS] All 42 figures generated cleanly in '{OUTPUT_DIR}/'!")
    print("=" * 70)


if __name__ == "__main__":
    main()
