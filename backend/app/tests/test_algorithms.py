import pytest
from backend.app.algorithms.searching import linear_search, binary_search
from backend.app.algorithms.sorting import bubble_sort, merge_sort, quicksort
from backend.app.algorithms.knapsack import dp_knapsack, verify_knapsack_optimality
from backend.app.algorithms.greedy import greedy_knapsack
from backend.app.algorithms.graph import bfs, dfs, dijkstra_shortest_path, kruskal_mst, DEFAULT_LOGISTICS_GRAPH

def test_searching_correctness():
    arr = [10, 23, 45, 70, 99, 120, 350]
    
    # Linear Search
    res_lin = linear_search(arr, 70)
    assert res_lin["found"] is True
    assert res_lin["index"] == 3
    assert res_lin["comparisons"] == 4

    res_lin_not_found = linear_search(arr, 999)
    assert res_lin_not_found["found"] is False
    assert res_lin_not_found["index"] == -1

    # Binary Search
    res_bin = binary_search(arr, 70)
    assert res_bin["found"] is True
    assert res_bin["index"] == 3
    assert res_bin["comparisons"] <= 4

    # Binary Search rejects unsorted input
    with pytest.raises(ValueError):
        binary_search([50, 10, 30], 10)

def test_sorting_correctness():
    sample = [64, 34, 25, 12, 22, 11, 90, 5, 77, 42]
    expected = sorted(sample)

    res_bubble = bubble_sort(sample)
    assert res_bubble["sorted_array"] == expected
    assert res_bubble["comparisons"] > 0
    assert res_bubble["swaps"] > 0

    res_merge = merge_sort(sample)
    assert res_merge["sorted_array"] == expected
    assert res_merge["comparisons"] > 0

    res_quick = quicksort(sample)
    assert res_quick["sorted_array"] == expected
    assert res_quick["comparisons"] > 0

def test_knapsack_optimality():
    # Small test case with known optimal solution
    items = [
        {"name": "Item A", "cost": 10.0, "benefit": 60.0},
        {"name": "Item B", "cost": 20.0, "benefit": 100.0},
        {"name": "Item C", "cost": 30.0, "benefit": 120.0},
    ]
    budget = 50.0

    dp_res = dp_knapsack(items, budget)
    assert dp_res["total_cost"] <= budget
    assert dp_res["total_benefit"] == 220.0 # Items B and C: cost 50, benefit 220
    assert dp_res["selected_count"] == 2

    # Verify against brute force
    verification = verify_knapsack_optimality(items, budget, dp_res["total_benefit"])
    assert verification["verified"] is True
    assert verification["match"] is True

def test_greedy_vs_dp_divergence():
    # Classic case where Greedy makes suboptimal choice
    # Item 1 has ratio 10/1 = 10, but capacity is 5.
    # Picking item 1 leaves 4 units. Items 2 and 3 each cost 3 with benefit 15 (ratio 5).
    # Greedy picks Item 1 (benefit 10) and cannot fit Item 2 or 3. Total benefit = 10.
    # Optimal DP picks Item 2 and Item 3 (cost 3+3 > 5? let's use: budget 6)
    # Item 1: cost 2, value 12 (ratio 6)
    # Item 2: cost 3, value 15 (ratio 5)
    # Item 3: cost 3, value 15 (ratio 5)
    # Budget = 6.
    # Greedy picks Item 1 (cost 2, val 12), remainder budget 4.
    # Greedy then picks Item 2 (cost 3, val 15), remainder budget 1. Cannot fit Item 3.
    # Greedy total benefit = 12 + 15 = 27 (cost 5).
    # DP picks Item 2 + Item 3 (cost 3+3=6, val 15+15=30).
    # DP total benefit = 30 > 27!
    items = [
        {"name": "High Ratio Small", "cost": 2.0, "benefit": 12.0},
        {"name": "Medium 1", "cost": 3.0, "benefit": 15.0},
        {"name": "Medium 2", "cost": 3.0, "benefit": 15.0},
    ]
    budget = 6.0

    dp_res = dp_knapsack(items, budget)
    greedy_res = greedy_knapsack(items, budget)

    assert dp_res["total_benefit"] == 30.0
    assert greedy_res["total_benefit"] == 27.0
    assert dp_res["total_benefit"] > greedy_res["total_benefit"]

def test_graph_algorithms():
    g = DEFAULT_LOGISTICS_GRAPH

    # BFS
    bfs_res = bfs(g, "Central_Warehouse")
    assert bfs_res["start_node"] == "Central_Warehouse"
    assert len(bfs_res["visited_order"]) == len(g["nodes"])
    assert bfs_res["visited_order"][0] == "Central_Warehouse"

    # DFS
    dfs_res = dfs(g, "Central_Warehouse")
    assert dfs_res["start_node"] == "Central_Warehouse"
    assert len(dfs_res["visited_order"]) == len(g["nodes"])

    # Dijkstra
    dijkstra_res = dijkstra_shortest_path(g, "Central_Warehouse", "Southeast_Store")
    assert dijkstra_res["reachable"] is True
    assert dijkstra_res["total_cost"] > 0
    assert dijkstra_res["path"][0] == "Central_Warehouse"
    assert dijkstra_res["path"][-1] == "Southeast_Store"

    # Kruskal MST
    mst_res = kruskal_mst(g)
    assert mst_res["total_edges_selected"] == len(g["nodes"]) - 1
    assert mst_res["total_mst_cost"] > 0

    # Dijkstra rejects negative edge
    bad_graph = {
        "nodes": [{"id": "A"}, {"id": "B"}],
        "edges": [{"source": "A", "target": "B", "weight": -5}]
    }
    with pytest.raises(ValueError):
        dijkstra_shortest_path(bad_graph, "A", "B")
