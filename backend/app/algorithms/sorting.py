"""
Manual Sorting Algorithm Implementations (Analysis of Algorithms)
No reliance on Python's built-in sorted() or list.sort().
"""

from typing import Any, Dict, List, Tuple

def bubble_sort(arr: List[Any]) -> Dict[str, Any]:
    """
    Bubble Sort: Repeatedly steps through the list, compares adjacent elements and swaps them.
    Time Complexity:
      Best: O(n) [already sorted, with early-exit flag]
      Average: O(n^2)
      Worst: O(n^2) [reverse sorted]
    Space Complexity: O(1) auxiliary
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    if n > 5000:
        raise ValueError("Bubble Sort is restricted to input sizes <= 5000 due to O(n^2) complexity.")

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return {
        "sorted_array": a if len(a) <= 100 else a[:50] + ["..."] + a[-50:],
        "comparisons": comparisons,
        "swaps": swaps,
        "input_size": n,
        "algorithm": "Bubble Sort",
        "best_case": "O(n)",
        "average_case": "O(n^2)",
        "worst_case": "O(n^2)",
        "space_complexity": "O(1) auxiliary",
        "stable": True
    }

def merge_sort(arr: List[Any]) -> Dict[str, Any]:
    """
    Merge Sort: Divide-and-conquer algorithm that divides the array into halves,
    sorts them recursively, and merges the sorted halves.
    Time Complexity:
      Best: O(n log n)
      Average: O(n log n)
      Worst: O(n log n)
    Space Complexity: O(n) auxiliary
    """
    a = list(arr)
    comparisons = 0
    swaps = 0  # Merge sort moves elements rather than swapping in-place

    def _merge_sort(sub_arr: List[Any]) -> List[Any]:
        nonlocal comparisons
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left = _merge_sort(sub_arr[:mid])
        right = _merge_sort(sub_arr[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_res = _merge_sort(a)

    return {
        "sorted_array": sorted_res if len(sorted_res) <= 100 else sorted_res[:50] + ["..."] + sorted_res[-50:],
        "comparisons": comparisons,
        "swaps": swaps,
        "input_size": len(arr),
        "algorithm": "Merge Sort",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "space_complexity": "O(n) auxiliary",
        "stable": True
    }

def quicksort(arr: List[Any]) -> Dict[str, Any]:
    """
    Quicksort: Divide-and-conquer algorithm using median-of-three or middle-element pivot partitioning.
    Time Complexity:
      Best: O(n log n)
      Average: O(n log n)
      Worst: O(n^2) [e.g. extremely unbalanced partitions]
    Space Complexity: O(log n) call stack
    """
    a = list(arr)
    comparisons = 0
    swaps = 0

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        # Choose median pivot to prevent worst-case on already sorted inputs
        mid = (low + high) // 2
        pivot = a[mid]
        # Place pivot at end for standard Lomuto/Hoare or swap
        a[mid], a[high] = a[high], a[mid]
        swaps += 1

        i = low
        for j in range(low, high):
            comparisons += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                swaps += 1
                i += 1

        a[i], a[high] = a[high], a[i]
        swaps += 1
        return i

    def _quicksort(low: int, high: int):
        if low < high:
            pi = _partition(low, high)
            _quicksort(low, pi - 1)
            _quicksort(pi + 1, high)

    if len(a) > 0:
        _quicksort(0, len(a) - 1)

    return {
        "sorted_array": a if len(a) <= 100 else a[:50] + ["..."] + a[-50:],
        "comparisons": comparisons,
        "swaps": swaps,
        "input_size": len(arr),
        "algorithm": "Quicksort",
        "best_case": "O(n log n)",
        "average_case": "O(n log n)",
        "worst_case": "O(n^2)",
        "space_complexity": "O(log n) call stack",
        "stable": False
    }
