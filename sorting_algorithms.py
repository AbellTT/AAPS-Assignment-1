"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Standard Sorting Algorithms (Pure Implementation)

This module implements the standard sorting algorithms without instrumentation overhead:
1. Insertion Sort
2. Merge Sort
3. Quick Sort

Used for Part 1: Computing Running Time in Milliseconds (and Appendix A of the report).
Each function returns the sorted list.
"""

from typing import List, Any


def insertion_sort(arr: List[Any]) -> List[Any]:
    arr = list(arr)
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr


def merge_sort(arr: List[Any]) -> List[Any]:
    arr = list(arr)

    def _merge_sort(sub_arr: List[Any]) -> List[Any]:
        n = len(sub_arr)
        if n <= 1:
            return sub_arr

        mid = n // 2
        left = _merge_sort(sub_arr[:mid])
        right = _merge_sort(sub_arr[mid:])

        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return _merge_sort(arr)


def quick_sort(arr: List[Any]) -> List[Any]:
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr

    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        pivot = arr[high]
        i = low

        for j in range(low, high):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[i], arr[high] = arr[high], arr[i]
        pivot_idx = i

        stack.append((low, pivot_idx - 1))
        stack.append((pivot_idx + 1, high))

    return arr


if __name__ == "__main__":
    test_cases = {
        "Random": [8, 3, 10, 1, 7, 4, 9, 2, 6, 5],
        "Ascending": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Descending": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Few items / Duplicates": [3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
    }

    print("=== Testing Standard Sorting Algorithms (Pure Implementations) ===")
    for name, data in test_cases.items():
        expected = sorted(data)
        assert insertion_sort(data) == expected, f"Insertion Sort failed on {name}"
        assert merge_sort(data) == expected, f"Merge Sort failed on {name}"
        assert quick_sort(data) == expected, f"Quick Sort failed on {name}"
        print(f"  [PASS] {name} ({len(data)} items)")

    print("\nAll pure sorting algorithms passed verification successfully!")
