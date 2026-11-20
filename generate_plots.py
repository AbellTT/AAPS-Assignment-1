"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Step 3: High-Resolution Plot Generation (Enhanced Overlap Prevention)

This script reads benchmark_results.csv and produces:
1. Part 1 Graphs (12 plots): Execution Time (ms) vs. Input Size (n)
   for each Algorithm x Input Type combination.
2. Part 2 Graphs (12 plots): Number of Comparisons vs. Input Size (n)
   for each Algorithm x Input Type combination.
3. Comparative Overlay Graphs (Linear + Log-scale):
   - Solves overlapping by using distinct line styles, widths, z-orders, and nested markers:
     * Insertion Sort: Thick solid red line with hollow red squares.
     * Quick Sort: Medium dashed blue line with filled blue circles.
     * Merge Sort: Dash-dot green line with filled green triangles.
   - When Insertion and Quick Sort have identical values (e.g. Descending comparisons = n(n-1)/2),
     the red line and hollow squares show through the blue dashes and dots clearly.
4. Master 2x2 Dashboards: Linear and Log-scaled consolidated figures.
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

# Distinct visual style per algorithm to prevent overlapping / hiding
ALGO_STYLES = {
    "Insertion Sort": {
        "color": "#d62728",           # Red
        "linestyle": "-",              # Solid line
        "linewidth": 3.4,              # Thicker line so it peeks around overlays
        "marker": "s",                # Square
        "markersize": 8,
        "markerfacecolor": "none",     # Hollow marker
        "markeredgewidth": 2.2,
        "zorder": 2,                   # Underneath dashed line
        "alpha": 0.95,
    },
    "Quick Sort": {
        "color": "#1f77b4",           # Blue
        "linestyle": "--",             # Dashed line (lets solid red line peek through!)
        "linewidth": 2.2,
        "marker": "o",                # Circle
        "markersize": 5,
        "markerfacecolor": "#1f77b4",  # Filled circle (nests inside hollow red square!)
        "markeredgewidth": 1.0,
        "zorder": 3,                   # Above solid line
        "alpha": 0.95,
    },
    "Merge Sort": {
        "color": "#2ca02c",           # Green
        "linestyle": "-.",             # Dash-dot
        "linewidth": 2.2,
        "marker": "^",                # Triangle
        "markersize": 6,
        "markerfacecolor": "#2ca02c",
        "markeredgewidth": 1.0,
        "zorder": 4,
        "alpha": 0.95,
    },
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
    style = ALGO_STYLES.get(algo, {})
    color = style.get("color", "#333333")

    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Execution Time" if metric == "Time (ms)" else "Comparison Operations"

    ax.plot(
        subset["Size (n)"],
        subset[metric],
        marker=style.get("marker", "o"),
        color=color,
        linestyle="-",
        linewidth=2.2,
        markersize=6,
        markerfacecolor=color,
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
    log_scale: bool = False,
):
    """
    Generates a head-to-head comparison graph of all 3 algorithms for a specific input type.
    Uses layered dashed and hollow line styles so identical overlapping curves remain visible.
    """
    fig, ax = plt.subplots(figsize=(8.2, 5.4), dpi=300)
    y_label = "Execution Time (ms)" if metric == "Time (ms)" else "Number of Comparisons"
    title_metric = "Running Time" if metric == "Time (ms)" else "Comparison Counts"

    if log_scale:
        y_label += " (Log Scale)"
        title_metric += " (Log Scale)"

    # Plot algorithms in explicit order: Insertion Sort first, then Quick Sort on top
    for algo in ["Insertion Sort", "Quick Sort", "Merge Sort"]:
        subset = df[(df["Algorithm"] == algo) & (df["Input Type"] == itype)].sort_values("Size (n)")
        style = ALGO_STYLES[algo]

        ax.plot(
            subset["Size (n)"],
            subset[metric],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            marker=style["marker"],
            markersize=style["markersize"],
            markerfacecolor=style["markerfacecolor"],
            markeredgewidth=style["markeredgewidth"],
            label=algo,
            zorder=style["zorder"],
            alpha=style["alpha"],
        )

    if log_scale:
        ax.set_yscale("log")
    else:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y):,}" if y >= 1 else f"{y:.2f}"))

    ax.set_title(f"Algorithm Comparison: {title_metric}\n[{itype} Input]", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=11, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=11, fontweight="bold")

    ax.grid(True, linestyle="--", alpha=0.6, which="both" if log_scale else "major")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))

    # Informative callout if Insertion and Quick Sort have identical values
    if itype == "Descending" and metric == "Comparisons" and not log_scale:
        ax.annotate(
            "Note: Insertion Sort & Quick Sort comparison counts are\n"
            "mathematically identical: n(n-1)/2 (both curves overlap exactly).\n"
            "Red solid line shows through blue dashes; hollow squares frame circles.",
            xy=(0.04, 0.70),
            xycoords="axes fraction",
            fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.5", fc="#fff9e6", ec="#e6b800", lw=1),
        )

    ax.legend(loc="upper left", frameon=True, framealpha=0.95, fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_dashboard(df: pd.DataFrame, metric: str, output_path: str, log_scale: bool = False):
    """Generates a 2x2 multi-panel dashboard comparing all 3 algorithms across all 4 input types."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    metric_name = "Execution Time (ms)" if metric == "Time (ms)" else "Comparison Count"
    scale_label = " [Log Scale]" if log_scale else ""
    fig.suptitle(f"SWEG 5012: Comprehensive {metric_name} Analysis{scale_label}", fontsize=16, fontweight="bold", y=0.98)

    for idx, itype in enumerate(input_types):
        ax = axes[idx // 2, idx % 2]

        for algo in ["Insertion Sort", "Quick Sort", "Merge Sort"]:
            subset = df[(df["Algorithm"] == algo) & (df["Input Type"] == itype)].sort_values("Size (n)")
            style = ALGO_STYLES[algo]

            ax.plot(
                subset["Size (n)"],
                subset[metric],
                color=style["color"],
                linestyle=style["linestyle"],
                linewidth=style["linewidth"],
                marker=style["marker"],
                markersize=style["markersize"],
                markerfacecolor=style["markerfacecolor"],
                markeredgewidth=style["markeredgewidth"],
                label=algo,
                zorder=style["zorder"],
                alpha=style["alpha"],
            )

        ax.set_title(f"Input Type: {itype}", fontsize=12, fontweight="bold", pad=8)
        ax.set_xlabel("Input Size (n)", fontsize=9, fontweight="bold")
        ax.set_ylabel(metric_name + (" (log)" if log_scale else ""), fontsize=9, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.6, which="both" if log_scale else "major")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))

        if log_scale:
            ax.set_yscale("log")
        else:
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
    print(" SWEG 5012: Generating Figures with Overlap Prevention (Step 3)")
    print("=" * 70)

    # 1. Part 1: Individual Execution Time Plots (12 plots)
    print("\n[1/5] Generating 12 Individual Execution Time Plots (Part 1)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "time", f"time_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Time (ms)", out_file)
            print(f"  Created: {out_file}")

    # 2. Part 2: Individual Comparison Count Plots (12 plots)
    print("\n[2/5] Generating 12 Individual Comparison Count Plots (Part 2)...")
    for algo in algorithms:
        algo_slug = algo.lower().replace(" ", "_")
        for itype in input_types:
            itype_slug = itype.lower().replace(" ", "_")
            out_file = os.path.join(OUTPUT_DIR, "comparisons", f"comp_{algo_slug}_{itype_slug}.png")
            plot_single(df, algo, itype, "Comparisons", out_file)
            print(f"  Created: {out_file}")

    # 3. Comparative Overlays - Linear Scale (8 plots)
    print("\n[3/5] Generating 8 Linear Comparative Plots (with Overlap Prevention)...")
    for itype in input_types:
        itype_slug = itype.lower().replace(" ", "_")
        time_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_time_{itype_slug}.png")
        comp_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_comp_{itype_slug}.png")
        plot_comparative_overlay(df, itype, "Time (ms)", time_out, log_scale=False)
        plot_comparative_overlay(df, itype, "Comparisons", comp_out, log_scale=False)
        print(f"  Created: {time_out}")
        print(f"  Created: {comp_out}")

    # 4. Comparative Overlays - Log Scale (8 plots)
    print("\n[4/5] Generating 8 Log-Scale Comparative Plots (Resolves Flat Baseline)...")
    for itype in input_types:
        itype_slug = itype.lower().replace(" ", "_")
        time_log_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_time_{itype_slug}_log.png")
        comp_log_out = os.path.join(OUTPUT_DIR, "comparative", f"compare_comp_{itype_slug}_log.png")
        plot_comparative_overlay(df, itype, "Time (ms)", time_log_out, log_scale=True)
        plot_comparative_overlay(df, itype, "Comparisons", comp_log_out, log_scale=True)
        print(f"  Created: {time_log_out}")
        print(f"  Created: {comp_log_out}")

    # 5. Master 2x2 Dashboards (4 plots: Linear & Log for both metrics)
    print("\n[5/5] Generating Master 2x2 Dashboards (Linear & Log)...")
    time_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_running_time.png")
    time_dash_log = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_running_time_log.png")
    comp_dash = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_comparisons.png")
    comp_dash_log = os.path.join(OUTPUT_DIR, "dashboards", "dashboard_comparisons_log.png")

    plot_dashboard(df, "Time (ms)", time_dash, log_scale=False)
    plot_dashboard(df, "Time (ms)", time_dash_log, log_scale=True)
    plot_dashboard(df, "Comparisons", comp_dash, log_scale=False)
    plot_dashboard(df, "Comparisons", comp_dash_log, log_scale=True)

    print(f"  Created: {time_dash}")
    print(f"  Created: {time_dash_log}")
    print(f"  Created: {comp_dash}")
    print(f"  Created: {comp_dash_log}")

    print("\n" + "=" * 70)
    print(f"[SUCCESS] All figures regenerated with anti-overlap styling in '{OUTPUT_DIR}/'!")
    print("=" * 70)


if __name__ == "__main__":
    main()
