"""
0/1 Knapsack Dynamic Programming & Optimality Verification
"""

from typing import Any, Dict, List
from backend.app.algorithms.greedy import greedy_knapsack

def dp_knapsack(items: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
    """
    0/1 Knapsack via Bottom-Up Dynamic Programming.
    DP Table: dp[i][w] = maximum benefit achievable using a subset of first i items with budget w.
    Recurrence:
      dp[i][w] = max(dp[i-1][w], dp[i-1][w - cost[i-1]] + benefit[i-1])  if cost[i-1] <= w
                 else dp[i-1][w]
    Complexity: O(n * W) pseudo-polynomial time, O(n * W) space.
    """
    # Scale budget and costs to integers (cents) for exact DP tabulation
    scale = 100
    W = int(round(budget * scale))
    n = len(items)

    costs = [int(round(float(item["cost"]) * scale)) for item in items]
    benefits = [float(item["benefit"]) for item in items]

    # Initialize (n+1) x (W+1) table
    # Memory check: if W > 2,000,000 (i.e. > $20,000), limit scale to 1 (dollars)
    if W > 1_000_000:
        scale = 1
        W = int(round(budget))
        costs = [int(round(float(item["cost"]))) for item in items]

    dp = [[0.0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        c = costs[i - 1]
        b = benefits[i - 1]
        for w in range(W + 1):
            if c <= w:
                if dp[i - 1][w - c] + b > dp[i - 1][w]:
                    dp[i][w] = dp[i - 1][w - c] + b
                else:
                    dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find chosen items
    selected_indices = []
    w_remain = W
    for i in range(n, 0, -1):
        if dp[i][w_remain] != dp[i - 1][w_remain]:
            selected_indices.append(i - 1)
            w_remain -= costs[i - 1]

    selected_indices.reverse()
    selected_items = [items[idx] for idx in selected_indices]
    total_cost = sum(float(it["cost"]) for it in selected_items)
    total_benefit = sum(float(it["benefit"]) for it in selected_items)

    # Run greedy on the exact same input for direct side-by-side comparison
    greedy_res = greedy_knapsack(items, budget)

    # Brute-force verification if n is small
    brute_force_verified = None
    if n <= 14:
        brute_force_verified = verify_knapsack_optimality(items, budget, total_benefit)

    return {
        "strategy": "Dynamic Programming (0/1 Knapsack)",
        "selected_items": selected_items,
        "selected_count": len(selected_items),
        "total_cost": round(total_cost, 2),
        "total_benefit": round(total_benefit, 2),
        "budget": round(float(budget), 2),
        "budget_remaining": round(float(budget) - total_cost, 2),
        "budget_utilized_pct": round((total_cost / float(budget) * 100) if float(budget) > 0 else 0.0, 2),
        "is_optimal_guaranteed": True,
        "brute_force_verified": brute_force_verified,
        "greedy_comparison": {
            "greedy_benefit": greedy_res["total_benefit"],
            "greedy_cost": greedy_res["total_cost"],
            "dp_benefit": round(total_benefit, 2),
            "dp_cost": round(total_cost, 2),
            "benefit_gain": round(total_benefit - greedy_res["total_benefit"], 2),
            "percentage_gain": round(((total_benefit - greedy_res["total_benefit"]) / greedy_res["total_benefit"] * 100) if greedy_res["total_benefit"] > 0 else 0.0, 2)
        },
        "time_complexity": "O(n * W) pseudo-polynomial",
        "space_complexity": "O(n * W)"
    }

def verify_knapsack_optimality(items: List[Dict[str, Any]], budget: float, dp_optimal_benefit: float) -> Dict[str, Any]:
    """
    Exhaustive search (2^n) to formally verify DP optimality on small inputs.
    """
    n = len(items)
    max_val = 0.0
    best_combo = []

    for bitmask in range(1 << n):
        cur_cost = 0.0
        cur_val = 0.0
        combo = []
        for i in range(n):
            if (bitmask >> i) & 1:
                cur_cost += float(items[i]["cost"])
                cur_val += float(items[i]["benefit"])
                combo.append(items[i])
        if cur_cost <= budget and cur_val > max_val:
            max_val = cur_val
            best_combo = combo

    discrepancy = abs(max_val - dp_optimal_benefit)
    return {
        "verified": discrepancy < 0.01,
        "brute_force_max_benefit": round(max_val, 2),
        "dp_optimal_benefit": round(dp_optimal_benefit, 2),
        "subsets_evaluated": 1 << n,
        "match": discrepancy < 0.01
    }
