from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.session import get_db
from backend.app.models.inventory import Inventory
from backend.app.models.product import Product
from backend.app.models.supplier import Supplier
from backend.app.models.forecast import Forecast
from backend.app.algorithms.knapsack import dp_knapsack
from backend.app.algorithms.greedy import greedy_knapsack
from backend.app.schemas.schemas import InventoryOptimizeRequest

router = APIRouter(prefix="/inventory", tags=["Inventory Optimization"])

@router.get("/recommendations")
def get_inventory_recommendations(
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Computes stock shortage and replenishment requirements based on current stock,
    reorder thresholds, and forecasted demand.
    """
    q = (
        db.query(Inventory, Product, Supplier)
        .join(Product, Inventory.product_id == Product.product_id)
        .join(Supplier, Inventory.supplier_id == Supplier.supplier_id)
    )
    if supplier_id:
        q = q.filter(Inventory.supplier_id == supplier_id)

    rows = q.all()
    recommendations = []

    # Get latest forecasts by product
    forecast_map = {}
    f_rows = (
        db.query(Forecast.product_id, func.sum(Forecast.predicted_quantity).label("forecast_total"))
        .group_by(Forecast.product_id)
        .all()
    )
    for p_id, f_tot in f_rows:
        forecast_map[p_id] = float(f_tot or 0)

    for inv, prod, sup in rows:
        stk = inv.stock_quantity
        reord = inv.reorder_level
        cost = float(prod.unit_cost)
        price = float(prod.selling_price)
        f_demand = forecast_map.get(prod.product_id, 0.0)

        # Proposed replenishment quantity:
        # Accounts for current shortfall below reorder level + forecasted demand buffer
        is_low = stk <= reord
        shortfall = max(0, reord - stk)
        proposed_qty = int(shortfall + (f_demand * 0.5 if f_demand > 0 else reord)) if is_low else 0
        est_cost = round(proposed_qty * cost, 2)
        est_profit = round(proposed_qty * (price - cost), 2)

        if is_low or proposed_qty > 0:
            recommendations.append({
                "product_id": prod.product_id,
                "product_name": prod.product_name,
                "category": prod.category,
                "supplier_id": sup.supplier_id,
                "supplier_name": sup.supplier_name,
                "current_stock": stk,
                "reorder_level": reord,
                "forecasted_demand": round(f_demand, 1),
                "proposed_quantity": proposed_qty,
                "unit_cost": cost,
                "estimated_purchasing_cost": est_cost,
                "estimated_expected_profit": est_profit,
                "priority": "Critical" if stk == 0 else ("High" if stk < reord * 0.5 else "Medium")
            })

    # Sort by priority
    priority_order = {"Critical": 0, "High": 1, "Medium": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))

    total_est_cost = sum(r["estimated_purchasing_cost"] for r in recommendations)
    total_est_profit = sum(r["estimated_expected_profit"] for r in recommendations)

    return {
        "items_requiring_replenishment": len(recommendations),
        "total_estimated_restock_budget": round(total_est_cost, 2),
        "total_estimated_expected_profit": round(total_est_profit, 2),
        "recommendations": recommendations
    }

@router.post("/optimize")
def optimize_inventory_budget(
    payload: InventoryOptimizeRequest,
    db: Session = Depends(get_db)
):
    """
    Compares Greedy (Value-to-Cost heuristic) and Dynamic Programming (0/1 Knapsack)
    under a constrained purchasing budget to determine the optimal product selection.
    """
    # Fetch candidate products that have stock <= reorder_level or all active catalog
    rows = (
        db.query(Inventory, Product, Supplier)
        .join(Product, Inventory.product_id == Product.product_id)
        .join(Supplier, Inventory.supplier_id == Supplier.supplier_id)
        .all()
    )

    candidate_items = []
    for inv, prod, sup in rows:
        cost = float(prod.unit_cost)
        price = float(prod.selling_price)
        profit_per_unit = price - cost
        
        # Candidate batch: pack size of reorder_level units
        batch_size = max(5, inv.reorder_level)
        total_batch_cost = round(batch_size * cost, 2)
        total_batch_benefit = round(batch_size * profit_per_unit, 2)

        candidate_items.append({
            "product_id": prod.product_id,
            "product_name": prod.product_name,
            "category": prod.category,
            "supplier_name": sup.supplier_name,
            "batch_size": batch_size,
            "cost": total_batch_cost,
            "benefit": total_batch_benefit,
            "unit_cost": cost,
            "unit_price": price
        })

    budget = payload.budget

    # 1. Run Dynamic Programming Knapsack
    dp_result = dp_knapsack(candidate_items, budget)

    # 2. Run Greedy Knapsack
    greedy_result = greedy_knapsack(candidate_items, budget)

    return {
        "budget": budget,
        "planning_horizon_days": payload.planning_horizon_days,
        "total_candidates_evaluated": len(candidate_items),
        "dynamic_programming": dp_result,
        "greedy": greedy_result,
        "comparison_analysis": {
            "dp_benefit": dp_result["total_benefit"],
            "greedy_benefit": greedy_result["total_benefit"],
            "advantage_of_dp": round(dp_result["total_benefit"] - greedy_result["total_benefit"], 2),
            "percentage_gain": dp_result["greedy_comparison"]["percentage_gain"],
            "dp_remaining_budget": dp_result["budget_remaining"],
            "greedy_remaining_budget": greedy_result["budget_remaining"]
        },
        "advisory_notice": "Optimization suggestions are non-destructive decision-support recommendations. They do not alter inventory records automatically."
    }
