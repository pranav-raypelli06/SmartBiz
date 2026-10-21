"""
Manual Search Algorithm Implementations (Analysis of Algorithms)
No reliance on bisect or built-in search primitives.
"""

from typing import Any, Dict, List, Optional, Tuple

def linear_search(arr: List[Any], target: Any) -> Dict[str, Any]:
    """
    Linear Search: Sequentially checks each element of the list until a match is found.
    Time Complexity:
      Best: O(1) [target is first element]
      Average: O(n)
      Worst: O(n) [target is last element or not present]
    Space Complexity: O(1) auxiliary
    """
    comparisons = 0
    found_index = -1
    
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            found_index = i
            break

    return {
        "found": found_index != -1,
        "index": found_index,
        "comparisons": comparisons,
        "input_size": len(arr),
        "target": target,
        "algorithm": "Linear Search",
        "requires_sorted": False,
        "best_case": "O(1)",
        "average_case": "O(n)",
        "worst_case": "O(n)",
        "space_complexity": "O(1)",
    }

def binary_search(arr: List[Any], target: Any) -> Dict[str, Any]:
    """
    Binary Search: Search a sorted array by repeatedly dividing the search interval in half.
    Operates strictly on sorted arrays. Checks if array is sorted first.
    Time Complexity:
      Best: O(1) [target is middle element]
      Average: O(log n)
      Worst: O(log n)
    Space Complexity: O(1) iterative auxiliary
    """
    # Verify input is sorted
    is_sorted = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    if not is_sorted:
        raise ValueError("Binary Search requires the input array to be sorted in ascending order.")

    low = 0
    high = len(arr) - 1
    comparisons = 0
    found_index = -1

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        
        if arr[mid] == target:
            found_index = mid
            break
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "found": found_index != -1,
        "index": found_index,
        "comparisons": comparisons,
        "input_size": len(arr),
        "target": target,
        "algorithm": "Binary Search",
        "requires_sorted": True,
        "best_case": "O(1)",
        "average_case": "O(log n)",
        "worst_case": "O(log n)",
        "space_complexity": "O(1)",
    }
