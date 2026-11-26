"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Step 2: Automated Benchmarking Harness

This script automates:
1. Generating 4 input distributions: Random, Ascending, Descending, and Few Items.
2. Measuring running time (ms) using pure sorting algorithms (sorting_algorithms.py).
3. Measuring comparison counts using instrumented algorithms (sorting_algorithms_counted.py).
4. Running multiple trials to eliminate CPU noise.
5. Exporting all results to a structured CSV file (benchmark_results.csv) for plotting and report analysis.

Algorithms benchmarked:
- Insertion Sort
- Quick Sort (Lomuto last-element pivot)
- Quick Sort M3 (Lomuto median-of-three pivot)
- Merge Sort
"""

import sys
import time
import random
import argparse
from typing import List, Dict, Any, Callable
import pandas as pd

from sorting_algorithms import (
    insertion_sort,
    merge_sort,
    quick_sort,
    quick_sort_m3,
)
from sorting_algorithms_counted import (
    insertion_sort_counted,
    merge_sort_counted,
    quick_sort_counted,
    quick_sort_m3_counted,
)

# Standard experimental input sizes
DEFAULT_SIZES = [100, 500, 1000, 2000, 3000, 5000, 10000]

# Number of timing trials per data point to eliminate system noise
DEFAULT_TRIALS = 3


def generate_data(input_type: str, n: int, seed: int = 42) -> List[int]:
    """Generates an input list of length n according to the specified distribution."""
    rng = random.Random(seed + n)
    if input_type == "Random":
        return [rng.randint(1, 1000000) for _ in range(n)]
    elif input_type == "Ascending":
        return list(range(1, n + 1))
    elif input_type == "Descending":
        return list(range(n, 0, -1))
    elif input_type == "Few Items":
        # Array with few unique elements (high duplication, values 1..5)
        return [rng.randint(1, 5) for _ in range(n)]
    else:
        raise ValueError(f"Unknown input type: {input_type}")


def benchmark_timing(
    sort_func: Callable[[List[Any]], List[Any]],
    data: List[int],
    trials: int = 3,
) -> float:
    """Measures the execution time of a sorting function in milliseconds (average of trials)."""
    times = []
    for _ in range(trials):
        arr_copy = list(data)
        start = time.perf_counter()
        sort_func(arr_copy)
        end = time.perf_counter()
        times.append((end - start) * 1000.0)
    return round(sum(times) / len(times), 4)


def benchmark_comparisons(
    counted_sort_func: Callable[[List[Any]], Any],
    data: List[int],
) -> int:
    """Counts the exact number of key comparisons performed by the algorithm."""
    arr_copy = list(data)
    _, comparisons = counted_sort_func(arr_copy)
    return comparisons


def run_benchmarks(
    sizes: List[int],
    trials: int = DEFAULT_TRIALS,
    output_file: str = "benchmark_results.csv",
) -> pd.DataFrame:
    """Runs the complete benchmark suite across all algorithms, input types, and sizes."""
    input_types = ["Random", "Ascending", "Descending", "Few Items"]

    algorithms = {
        "Insertion Sort": {
            "pure": insertion_sort,
            "counted": insertion_sort_counted,
        },
        "Quick Sort": {
            "pure": quick_sort,
            "counted": quick_sort_counted,
        },
        "Quick Sort M3": {
            "pure": quick_sort_m3,
            "counted": quick_sort_m3_counted,
        },
        "Merge Sort": {
            "pure": merge_sort,
            "counted": merge_sort_counted,
        },
    }

    records = []
    total_steps = len(sizes) * len(input_types) * len(algorithms)
    current_step = 0

    print("=" * 75)
    print(" SWEG 5012: Sorting Algorithms Benchmark Suite (Step 2)")
    print(f" Input sizes: {sizes}")
    print(f" Input types: {input_types}")
    print(f" Trials per timing measurement: {trials}")
    print("=" * 75)

    for n in sizes:
        print(f"\n---> Benchmarking input size n = {n} ...")
        for itype in input_types:
            dataset = generate_data(itype, n)

            for algo_name, funcs in algorithms.items():
                current_step += 1

                # 1. Measure pure running time in milliseconds
                time_ms = benchmark_timing(funcs["pure"], dataset, trials=trials)

                # 2. Count comparison operations
                comparisons = benchmark_comparisons(funcs["counted"], dataset)

                records.append({
                    "Algorithm": algo_name,
                    "Input Type": itype,
                    "Size (n)": n,
                    "Time (ms)": time_ms,
                    "Comparisons": comparisons,
                })

                progress = (current_step / total_steps) * 100
                print(
                    f"  [{progress:5.1f}%] {algo_name:14} | {itype:10} | "
                    f"n={n:5} | Time: {time_ms:9.3f} ms | Comparisons: {comparisons:12,d}"
                )

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print("\n" + "=" * 75)
    print(f"[SUCCESS] Benchmark complete! Results saved to '{output_file}'.")
    print(f"Total data points collected: {len(df)}")
    print("=" * 75)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sorting algorithms benchmarks.")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run on smaller subset of sizes for a rapid check (n up to 3000)",
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=None,
        help="Custom list of input sizes",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=DEFAULT_TRIALS,
        help="Number of trials per timing measurement (default: 3)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="benchmark_results.csv",
        help="Output CSV file name (default: benchmark_results.csv)",
    )

    args = parser.parse_args()

    if args.sizes:
        test_sizes = args.sizes
    elif args.quick:
        test_sizes = [100, 500, 1000, 2000, 3000]
    else:
        test_sizes = DEFAULT_SIZES

    run_benchmarks(sizes=test_sizes, trials=args.trials, output_file=args.output)

