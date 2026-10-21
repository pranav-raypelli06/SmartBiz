"""
Greedy Inventory Purchasing Strategy
Ranks candidate items based on profitability ratio: (Expected Benefit / Unit Cost).
Takes items in descending order of ratio until the budget is exhausted.
"""

from typing import Any, Dict, List

def greedy_knapsack(items: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
    """
    Greedy 0/1 selection:
    1. Calculate ratio = benefit / cost for each item.
    2. Sort candidate items descending by ratio.
    3. Iterate through candidates and select any item whose cost fits in the remaining budget.
    
    Note: The greedy heuristic for 0/1 knapsack is NOT guaranteed to find the globally optimal value
    because it cannot take fractional amounts and may leave unused budget capacity.
    """
    annotated = []
    for item in items:
        cost = float(item["cost"])
        benefit = float(item["benefit"])
        ratio = benefit / cost if cost > 0 else 0.0
        annotated.append({
            **item,
            "cost": cost,
            "benefit": benefit,
            "ratio": round(ratio, 4)
        })

    # Manual sorting by ratio descending
    for i in range(len(annotated)):
        for j in range(len(annotated) - 1 - i):
            if annotated[j]["ratio"] < annotated[j + 1]["ratio"]:
                annotated[j], annotated[j + 1] = annotated[j + 1], annotated[j]

    selected = []
    total_cost = 0.0
    total_benefit = 0.0
    current_budget = float(budget)

    for item in annotated:
        if total_cost + item["cost"] <= current_budget:
            selected.append(item)
            total_cost += item["cost"]
            total_benefit += item["benefit"]

    return {
        "strategy": "Greedy (Value-to-Cost Ratio)",
        "selected_items": selected,
        "selected_count": len(selected),
        "total_cost": round(total_cost, 2),
        "total_benefit": round(total_benefit, 2),
        "budget": round(current_budget, 2),
        "budget_remaining": round(current_budget - total_cost, 2),
        "budget_utilized_pct": round((total_cost / current_budget * 100) if current_budget > 0 else 0.0, 2),
        "is_optimal_guaranteed": False,
        "explanation": (
            "Greedy selection prioritizes items with the highest immediate return per dollar. "
            "While fast (O(n log n)), it can get trapped in sub-optimal solutions for 0/1 problems "
            "if high-ratio items leave awkward budget remainders that prevent picking combinations of items "
            "with higher aggregate benefit."
        )
    }
