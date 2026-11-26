"""
SWEG 5012: Advanced Algorithms and Problem Solving
Assignment 1 - Standard Sorting Algorithms (Pure Implementation)

This module implements the standard sorting algorithms without instrumentation overhead:
1. Insertion Sort
2. Merge Sort
3. Quick Sort (Lomuto last-element pivot)
4. Quick Sort M3 (Lomuto median-of-three pivot)

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


def quick_sort_recursive(arr: List[Any]) -> List[Any]:
    """
    Standard In-Place Recursive Quick Sort (Textbook Lomuto Scheme).
    Ideal for conceptual understanding and pedagogical study.
    """
    arr = list(arr)

    def _partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low
        for j in range(low, high):
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
        return arr
    except RecursionError:
        # Graceful fallback to stack implementation to prevent recursion crashes on large inputs
        return quick_sort(arr)


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


def _median_of_three(arr: list, low: int, high: int) -> int:
    """
    Selects the median of arr[low], arr[mid], arr[high] as pivot,
    places it at arr[high-1], and returns the pivot value.
    Also sorts arr[low], arr[mid], arr[high] in-place as a side effect
    so the three sentinel elements are already in position.
    """
    mid = (low + high) // 2
    # Sort the three candidates into order: arr[low] <= arr[mid] <= arr[high]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    # Median is now at arr[mid]; place it just before arr[high] (Lomuto convention)
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    return arr[high - 1]


def quick_sort_m3(arr: List[Any]) -> List[Any]:
    """
    Quick Sort with Median-of-Three Pivot Selection (Lomuto partition scheme).

    Pivot is chosen as the median of the first, middle, and last elements,
    which eliminates worst-case O(n^2) behaviour on already-sorted and
    reverse-sorted inputs. For sub-arrays of length <= 3 falls back to a
    direct insertion-style sort so the median selection never under-indexes.

    Uses an explicit stack to avoid Python recursion depth limits.
    """
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr

    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        length = high - low + 1

        if length <= 1:
            continue
        elif length == 2:
            if arr[low] > arr[high]:
                arr[low], arr[high] = arr[high], arr[low]
            continue
        elif length == 3:
            # Sort three elements directly
            if arr[low] > arr[low + 1]:
                arr[low], arr[low + 1] = arr[low + 1], arr[low]
            if arr[low] > arr[high]:
                arr[low], arr[high] = arr[high], arr[low]
            if arr[low + 1] > arr[high]:
                arr[low + 1], arr[high] = arr[high], arr[low + 1]
            continue

        # Median-of-three pivot placed at high-1
        pivot = _median_of_three(arr, low, high)

        # Lomuto partition on arr[low+1 .. high-2] (sentinels at low, high-1, high)
        i = low + 1
        for j in range(low + 1, high - 1):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        # Place pivot into final position
        arr[i], arr[high - 1] = arr[high - 1], arr[i]
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
        assert quick_sort_recursive(data) == expected, f"Recursive Quick Sort failed on {name}"
        assert quick_sort_m3(data) == expected, f"Quick Sort M3 failed on {name}"
        print(f"  [PASS] {name} ({len(data)} items)")

    print("\nAll pure sorting algorithms passed verification successfully!")
