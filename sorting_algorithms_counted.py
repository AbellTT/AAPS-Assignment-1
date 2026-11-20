"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Modified Sorting Algorithms for Comparison Counting

This module implements sorting algorithms modified to count element comparisons:
1. Insertion Sort
2. Merge Sort
3. Quick Sort

Used for Part 2: Counting the Number of Operations (and Appendix B of the report).
Each function returns a tuple of (sorted_list, comparisons_count).
"""

from typing import List, Tuple, Any


def insertion_sort_counted(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Modified Insertion Sort that counts element comparisons.

    Counts key comparisons:
    - In the inner loop, comparisons are incremented only when j >= 0 permits
      the array element comparison (arr[j] > key).

    Complexity:
    - Best Case (Ascending): O(n) comparisons
    - Average Case (Random): O(n^2) comparisons
    - Worst Case (Descending): O(n^2) comparisons

    Returns:
        (sorted_list, comparisons_count)
    """
    arr = list(arr)
    n = len(arr)
    comparisons = 0

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key

    return arr, comparisons


def merge_sort_counted(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Modified Merge Sort that counts element comparisons during the merge stage.

    Complexity:
    - Best, Average, Worst Case: Theta(n log n) comparisons

    Returns:
        (sorted_list, comparisons_count)
    """
    arr = list(arr)

    def _merge_sort(sub_arr: List[Any]) -> Tuple[List[Any], int]:
        n = len(sub_arr)
        if n <= 1:
            return sub_arr, 0

        mid = n // 2
        left, left_comp = _merge_sort(sub_arr[:mid])
        right, right_comp = _merge_sort(sub_arr[mid:])

        merged = []
        i = j = 0
        merge_comp = 0

        while i < len(left) and j < len(right):
            merge_comp += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        total_comp = left_comp + right_comp + merge_comp
        return merged, total_comp

    return _merge_sort(arr)


def quick_sort_recursive_counted(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Recursive Quick Sort (Lomuto partition scheme) with comparison counting.
    Ideal for conceptual study and tracing.
    """
    arr = list(arr)
    comparisons = 0

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons
        pivot = arr[high]
        i = low
        for j in range(low, high):
            comparisons += 1
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        return i

    def _quick_sort(low: int, high: int):
        if low < high:
            pi = _partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    try:
        _quick_sort(0, len(arr) - 1)
        return arr, comparisons
    except RecursionError:
        # Graceful fallback to stack implementation to prevent recursion crashes on large inputs
        return quick_sort_counted(arr)


def quick_sort_counted(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Modified Quick Sort (Lomuto partition scheme) that counts element comparisons.

    Uses an explicit stack to prevent recursion depth overflow on large inputs.
    Comparisons are counted whenever an element is compared against the pivot
    in the partition loop (arr[j] <= pivot).

    Complexity:
    - Best / Average Case (Random): O(n log n) comparisons
    - Worst Case (Ascending / Descending): O(n^2) comparisons

    Returns:
        (sorted_list, comparisons_count)
    """
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr, 0

    comparisons = 0
    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        pivot = arr[high]
        i = low

        for j in range(low, high):
            comparisons += 1
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[i], arr[high] = arr[high], arr[i]
        pivot_idx = i

        stack.append((low, pivot_idx - 1))
        stack.append((pivot_idx + 1, high))

    return arr, comparisons


if __name__ == "__main__":
    test_cases = {
        "Random": [8, 3, 10, 1, 7, 4, 9, 2, 6, 5],
        "Ascending": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Descending": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Few items / Duplicates": [3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
    }

    print("=== Testing Modified Sorting Algorithms (Comparison Counting) ===")
    for name, data in test_cases.items():
        expected = sorted(data)
        res_i, comp_i = insertion_sort_counted(data)
        res_m, comp_m = merge_sort_counted(data)
        res_q, comp_q = quick_sort_counted(data)
        res_qr, comp_qr = quick_sort_recursive_counted(data)

        assert res_i == expected, f"Insertion Sort failed on {name}"
        assert res_m == expected, f"Merge Sort failed on {name}"
        assert res_q == expected, f"Quick Sort failed on {name}"
        assert res_qr == expected, f"Recursive Quick Sort failed on {name}"
        assert comp_qr == comp_q, f"Recursive count mismatch: {comp_qr} vs {comp_q}"

        print(f"\n{name} (n={len(data)}):")
        print(f"  Insertion Sort comparisons: {comp_i}")
        print(f"  Merge Sort comparisons:     {comp_m}")
        print(f"  Quick Sort comparisons:     {comp_q}")

    print("\nAll modified algorithms passed verification successfully!")

