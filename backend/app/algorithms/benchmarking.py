"""
Algorithm Benchmarking Engine (Analysis of Algorithms)
Measures execution time with time.perf_counter(), memory peaks with tracemalloc,
and persists verified median runs into MySQL algorithm_runs table.
"""

import time
import tracemalloc
import random
import statistics
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.algorithms.searching import linear_search, binary_search
from backend.app.algorithms.sorting import bubble_sort, merge_sort, quicksort
from backend.app.algorithms.knapsack import dp_knapsack
from backend.app.algorithms.greedy import greedy_knapsack
from backend.app.algorithms.graph import bfs, dfs, dijkstra_shortest_path, kruskal_mst, DEFAULT_LOGISTICS_GRAPH
from backend.app.models.algorithm_run import AlgorithmRun

def generate_controlled_input(algorithm_name: str, size: int) -> Any:
    """Generate deterministic inputs of requested size."""
    rng = random.Random(42 + size)
    algo_lower = algorithm_name.lower()

    if "search" in algo_lower:
        # Array of integers
        arr = [rng.randint(1, size * 10) for _ in range(size)]
        if "binary" in algo_lower:
            arr.sort()
            target = arr[len(arr) // 2] if arr else 1
        else:
            target = arr[-1] if arr else 1 # Worst/near-worst case
        return {"array": arr, "target": target}

    elif "sort" in algo_lower:
        # Random unsorted array
        return [rng.randint(1, size * 10) for _ in range(size)]

    elif "knapsack" in algo_lower or "greedy" in algo_lower:
        items = []
        for i in range(size):
            c = round(rng.uniform(10.0, 150.0), 2)
            b = round(c * rng.uniform(1.1, 2.5), 2)
            items.append({"name": f"Product-{i+1}", "cost": c, "benefit": b})
        budget = round(sum(it["cost"] for it in items) * 0.45, 2)
        return {"items": items, "budget": budget}

    elif "graph" in algo_lower or "dijkstra" in algo_lower or "bfs" in algo_lower or "dfs" in algo_lower or "mst" in algo_lower:
        return DEFAULT_LOGISTICS_GRAPH

    return [rng.randint(1, 1000) for _ in range(size)]

def run_benchmark(
    algorithm_name: str,
    input_size: int,
    iterations: int = 3,
    db: Optional[Session] = None
) -> Dict[str, Any]:
    """
    Executes multiple trials, records median time with time.perf_counter()
    and memory peaks with tracemalloc, verifies output, and optionally saves to database.
    """
    problem_type_map = {
        "linear search": "Searching",
        "binary search": "Searching",
        "bubble sort": "Sorting",
        "merge sort": "Sorting",
        "quicksort": "Sorting",
        "greedy knapsack": "Greedy",
        "0/1 knapsack dp": "Dynamic Programming",
        "bfs": "Graph",
        "dfs": "Graph",
        "dijkstra": "Graph",
        "kruskal mst": "Graph"
    }

    norm_name = algorithm_name.strip().lower()
    prob_type = problem_type_map.get(norm_name, "General")

    # Safety limits
    if norm_name == "bubble sort" and input_size > 5000:
        raise ValueError("Bubble Sort is restricted to input sizes <= 5000 due to O(n^2) runtime.")
    if norm_name == "0/1 knapsack dp" and input_size > 100:
        raise ValueError("DP Knapsack demonstration is capped at 100 items.")

    times_ms = []
    peak_memories_mb = []
    last_result_summary = ""

    for _ in range(max(1, iterations)):
        test_data = generate_controlled_input(norm_name, input_size)

        tracemalloc.start()
        start_time = time.perf_counter()

        if norm_name == "linear search":
            res = linear_search(test_data["array"], test_data["target"])
            last_result_summary = f"Found: {res['found']} at index {res['index']}, comparisons: {res['comparisons']}"
        elif norm_name == "binary search":
            res = binary_search(test_data["array"], test_data["target"])
            last_result_summary = f"Found: {res['found']} at index {res['index']}, comparisons: {res['comparisons']}"
        elif norm_name == "bubble sort":
            res = bubble_sort(test_data)
            last_result_summary = f"Sorted {input_size} elements with {res['comparisons']} comparisons and {res['swaps']} swaps"
        elif norm_name == "merge sort":
            res = merge_sort(test_data)
            last_result_summary = f"Sorted {input_size} elements with {res['comparisons']} comparisons"
        elif norm_name == "quicksort":
            res = quicksort(test_data)
            last_result_summary = f"Sorted {input_size} elements with {res['comparisons']} comparisons and {res['swaps']} swaps"
        elif norm_name == "greedy knapsack":
            res = greedy_knapsack(test_data["items"], test_data["budget"])
            last_result_summary = f"Selected {res['selected_count']} items with cost ${res['total_cost']} and benefit ${res['total_benefit']}"
        elif norm_name == "0/1 knapsack dp":
            res = dp_knapsack(test_data["items"], test_data["budget"])
            last_result_summary = f"Optimal DP selected {res['selected_count']} items, cost ${res['total_cost']}, benefit ${res['total_benefit']}"
        elif norm_name == "bfs":
            res = bfs(test_data, "Central_Warehouse")
            last_result_summary = f"BFS traversed {res['nodes_visited_count']} nodes starting from Central_Warehouse"
        elif norm_name == "dfs":
            res = dfs(test_data, "Central_Warehouse")
            last_result_summary = f"DFS traversed {res['nodes_visited_count']} nodes starting from Central_Warehouse"
        elif norm_name == "dijkstra":
            res = dijkstra_shortest_path(test_data, "Pacific_Store", "Southeast_Store")
            last_result_summary = f"Optimal path: {' -> '.join(res['path'])}, transit cost: {res['total_cost']}"
        elif norm_name == "kruskal mst":
            res = kruskal_mst(test_data)
            last_result_summary = f"MST connects {res['total_nodes_connected']} nodes with total cost {res['total_mst_cost']}"
        else:
            raise ValueError(f"Unknown algorithm '{algorithm_name}'")

        end_time = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_ms = (end_time - start_time) * 1000.0
        times_ms.append(elapsed_ms)
        peak_memories_mb.append(peak_mem / (1024.0 * 1024.0))

    median_time_ms = round(statistics.median(times_ms), 4)
    median_mem_mb = round(statistics.median(peak_memories_mb), 4)

    # Persist in MySQL algorithm_runs table if db session provided
    run_id = None
    if db is not None:
        algo_run = AlgorithmRun(
            algorithm_name=algorithm_name,
            problem_type=prob_type,
            input_size=input_size,
            execution_time_ms=Decimal(str(median_time_ms)),
            memory_usage_mb=Decimal(str(median_mem_mb)),
            result_summary=last_result_summary,
            configuration={"iterations": iterations, "tested_at_sample_size": input_size}
        )
        db.add(algo_run)
        db.commit()
        db.refresh(algo_run)
        run_id = algo_run.run_id

    return {
        "run_id": run_id,
        "algorithm_name": algorithm_name,
        "problem_type": prob_type,
        "input_size": input_size,
        "median_time_ms": median_time_ms,
        "median_memory_mb": median_mem_mb,
        "trials_ms": [round(t, 4) for t in times_ms],
        "result_summary": last_result_summary,
        "persisted": run_id is not None
    }
