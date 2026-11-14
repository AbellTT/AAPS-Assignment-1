"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Sorting Algorithms with Comparison Counting

This module implements:
1. Insertion Sort
2. Merge Sort
3. Quick Sort

Each algorithm accepts a list of comparable elements and returns:
- The sorted list
- The exact count of element comparisons performed during sorting
"""

from typing import List, Tuple, Any


def insertion_sort(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Sorts an array using the Insertion Sort algorithm and counts comparisons.

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

        # Count element comparisons only when the index condition (j >= 0) holds
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key

    return arr, comparisons


def merge_sort(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Sorts an array using the Merge Sort algorithm and counts comparisons.

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

        # Merge step: compare front elements of left and right sublists
        while i < len(left) and j < len(right):
            merge_comp += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # Append remaining elements (no further comparisons needed)
        merged.extend(left[i:])
        merged.extend(right[j:])

        total_comp = left_comp + right_comp + merge_comp
        return merged, total_comp

    return _merge_sort(arr)


def quick_sort(arr: List[Any]) -> Tuple[List[Any], int]:
    """
    Sorts an array using the Quick Sort algorithm (Lomuto partition scheme)
    and counts comparisons.

    Implemented using an explicit call stack (iterative QuickSort) to avoid
    Python's recursion depth limit when sorting large ascending/descending
    arrays (e.g., n = 5,000 or 10,000).

    Complexity:
    - Best / Average Case (Random): O(n log n) comparisons
    - Worst Case (Ascending / Descending with naive pivot): O(n^2) comparisons

    Returns:
        (sorted_list, comparisons_count)
    """
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr, 0

    comparisons = 0
    # Stack stores (low, high) index bounds of subarrays to partition
    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        # Standard Lomuto partition: choosing the last element as the pivot
        pivot = arr[high]
        i = low

        for j in range(low, high):
            comparisons += 1
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        # Place the pivot in its final sorted position
        arr[i], arr[high] = arr[high], arr[i]
        pivot_idx = i

        # Push sub-array bounds onto the stack
        # (Pushing larger sub-array first keeps stack depth minimal)
        left_range = (low, pivot_idx - 1)
        right_range = (pivot_idx + 1, high)

        stack.append(left_range)
        stack.append(right_range)

    return arr, comparisons


if __name__ == "__main__":
    # Self-test verification
    test_cases = {
        "Random": [8, 3, 10, 1, 7, 4, 9, 2, 6, 5],
        "Ascending": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Descending": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Few items / Duplicates": [3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
    }

    print("=== Sorting Algorithms Verification ===")
    for name, data in test_cases.items():
        print(f"\nTest case: {name} ({len(data)} items)")
        sorted_expected = sorted(data)

        # Insertion Sort
        res_ins, comp_ins = insertion_sort(data)
        assert res_ins == sorted_expected, f"Insertion Sort failed on {name}"
        print(f"  Insertion Sort: comparisons = {comp_ins}")

        # Merge Sort
        res_merge, comp_merge = merge_sort(data)
        assert res_merge == sorted_expected, f"Merge Sort failed on {name}"
        print(f"  Merge Sort:     comparisons = {comp_merge}")

        # Quick Sort
        res_quick, comp_quick = quick_sort(data)
        assert res_quick == sorted_expected, f"Quick Sort failed on {name}"
        print(f"  Quick Sort:     comparisons = {comp_quick}")

    print("\nAll algorithms passed self-test verification successfully!")

