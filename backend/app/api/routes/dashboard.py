from datetime import date, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.product import Product
from backend.app.models.inventory import Inventory
from backend.app.models.customer import Customer
from backend.app.models.customer_segment import CustomerSegment

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    order_status: Optional[str] = "Completed",
    db: Session = Depends(get_db)
):
    # Total count check
    total_orders_in_db = db.query(Order).count()
    if total_orders_in_db == 0:
        return {
            "is_empty_database": True,
            "message": "Database is currently empty. Click 'Load Demo Data' to populate full retail dataset.",
            "metrics": {
                "total_revenue": 0.0,
                "gross_profit": 0.0,
                "completed_orders": 0,
                "units_sold": 0,
                "average_order_value": 0.0,
                "low_stock_count": 0
            }
        }

    # Base query for current period
    filters = []
    if order_status:
        filters.append(Order.order_status == order_status)
    if start_date:
        filters.append(Order.order_date >= start_date)
    if end_date:
        filters.append(Order.order_date <= end_date)
    if region:
        filters.append(Order.region == region)
    if category:
        filters.append(Product.category == category)

    q = (
        db.query(
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0).label("revenue"),
            func.coalesce(func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)), 0).label("profit"),
            func.count(func.distinct(Order.order_id)).label("order_count"),
            func.coalesce(func.sum(OrderItem.quantity), 0).label("units")
        )
        .join(OrderItem, Order.order_id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.product_id)
        .filter(and_(*filters) if filters else True)
    )

    current_res = q.first()
    rev = float(current_res.revenue)
    profit = float(current_res.profit)
    completed_orders = int(current_res.order_count)
    units_sold = int(current_res.units)
    aov = round(rev / completed_orders, 2) if completed_orders > 0 else 0.0

    # Low stock items count (stock <= reorder_level)
    low_stock_q = db.query(Inventory).filter(Inventory.stock_quantity <= Inventory.reorder_level)
    low_stock_count = low_stock_q.count()

    # Compare against equivalent previous period if date filters are provided
    prev_period_comparison = None
    if start_date and end_date:
        period_days = (end_date - start_date).days + 1
        prev_end = start_date - timedelta(days=1)
        prev_start = prev_end - timedelta(days=period_days - 1)

        prev_filters = []
        if order_status:
            prev_filters.append(Order.order_status == order_status)
        prev_filters.append(Order.order_date >= prev_start)
        prev_filters.append(Order.order_date <= prev_end)
        if region:
            prev_filters.append(Order.region == region)
        if category:
            prev_filters.append(Product.category == category)

        prev_q = (
            db.query(
                func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0).label("revenue"),
                func.coalesce(func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)), 0).label("profit"),
                func.count(func.distinct(Order.order_id)).label("order_count"),
                func.coalesce(func.sum(OrderItem.quantity), 0).label("units")
            )
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.product_id)
            .filter(and_(*prev_filters))
        )
        prev_res = prev_q.first()
        prev_rev = float(prev_res.revenue)
        prev_profit = float(prev_res.profit)
        prev_orders = int(prev_res.order_count)

        def pct_change(curr, prev):
            if prev > 0:
                return round(((curr - prev) / prev) * 100.0, 1)
            return None

        prev_period_comparison = {
            "previous_start": prev_start.isoformat(),
            "previous_end": prev_end.isoformat(),
            "previous_revenue": prev_rev,
            "revenue_change_pct": pct_change(rev, prev_rev),
            "profit_change_pct": pct_change(profit, prev_profit),
            "orders_change_pct": pct_change(completed_orders, prev_orders),
        }

    return {
        "is_empty_database": False,
        "metrics": {
            "total_revenue": round(rev, 2),
            "gross_profit": round(profit, 2),
            "profit_margin_pct": round((profit / rev * 100) if rev > 0 else 0.0, 1),
            "completed_orders": completed_orders,
            "units_sold": units_sold,
            "average_order_value": aov,
            "low_stock_count": low_stock_count
        },
        "comparison": prev_period_comparison
    }

@router.get("/sales-trend")
def get_sales_trend(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filters = [Order.order_status == "Completed"]
    if start_date:
        filters.append(Order.order_date >= start_date)
    if end_date:
        filters.append(Order.order_date <= end_date)
    if region:
        filters.append(Order.region == region)
    if category:
        filters.append(Product.category == category)

    # Group by month (YYYY-MM)
    query = (
        db.query(
            func.date_format(Order.order_date, "%Y-%m").label("month"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)).label("profit"),
            func.count(func.distinct(Order.order_id)).label("orders"),
            func.sum(OrderItem.quantity).label("units")
        )
        .join(OrderItem, Order.order_id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.product_id)
        .filter(and_(*filters))
        .group_by(func.date_format(Order.order_date, "%Y-%m"))
        .order_by(func.date_format(Order.order_date, "%Y-%m").asc())
    )

    results = []
    for row in query.all():
        results.append({
            "month": row.month,
            "revenue": round(float(row.revenue or 0), 2),
            "profit": round(float(row.profit or 0), 2),
            "orders": int(row.orders or 0),
            "units": int(row.units or 0)
        })

    return results

@router.get("/category-performance")
def get_category_performance(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filters = [Order.order_status == "Completed"]
    if start_date:
        filters.append(Order.order_date >= start_date)
    if end_date:
        filters.append(Order.order_date <= end_date)
    if region:
        filters.append(Order.region == region)

    query = (
        db.query(
            Product.category,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)).label("profit"),
            func.sum(OrderItem.quantity).label("units")
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.order_id)
        .filter(and_(*filters))
        .group_by(Product.category)
        .order_by(func.sum(OrderItem.quantity * OrderItem.unit_price).desc())
    )

    results = []
    for row in query.all():
        results.append({
            "category": row.category,
            "revenue": round(float(row.revenue or 0), 2),
            "profit": round(float(row.profit or 0), 2),
            "units": int(row.units or 0)
        })

    return results

@router.get("/top-products")
def get_top_products(
    limit: int = 10,
    category: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filters = [Order.order_status == "Completed"]
    if category:
        filters.append(Product.category == category)
    if region:
        filters.append(Order.region == region)

    query = (
        db.query(
            Product.product_id,
            Product.product_name,
            Product.category,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)).label("profit"),
            func.sum(OrderItem.quantity).label("units_sold")
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.order_id)
        .filter(and_(*filters))
        .group_by(Product.product_id, Product.product_name, Product.category)
        .order_by(func.sum(OrderItem.quantity * OrderItem.unit_price).desc())
        .limit(limit)
    )

    results = []
    for row in query.all():
        results.append({
            "product_id": row.product_id,
            "product_name": row.product_name,
            "category": row.category,
            "revenue": round(float(row.revenue or 0), 2),
            "profit": round(float(row.profit or 0), 2),
            "units_sold": int(row.units_sold or 0)
        })

    return results

@router.get("/regional-performance")
def get_regional_performance(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filters = [Order.order_status == "Completed"]
    if start_date:
        filters.append(Order.order_date >= start_date)
    if end_date:
        filters.append(Order.order_date <= end_date)
    if category:
        filters.append(Product.category == category)

    query = (
        db.query(
            Order.region,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            func.sum(OrderItem.quantity * (OrderItem.unit_price - OrderItem.unit_cost)).label("profit"),
            func.count(func.distinct(Order.order_id)).label("order_count")
        )
        .join(OrderItem, Order.order_id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.product_id)
        .filter(and_(*filters))
        .group_by(Order.region)
        .order_by(func.sum(OrderItem.quantity * OrderItem.unit_price).desc())
    )

    results = []
    for row in query.all():
        results.append({
            "region": row.region,
            "revenue": round(float(row.revenue or 0), 2),
            "profit": round(float(row.profit or 0), 2),
            "order_count": int(row.order_count or 0)
        })

    return results
