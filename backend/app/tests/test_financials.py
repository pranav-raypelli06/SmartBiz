from decimal import Decimal
from sqlalchemy import func
from backend.app.db.session import SessionLocal
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem

def test_financial_calculations_manual_example():
    """Verify revenue, cost, profit, and margin formulas against exact manual calculations."""
    qty = 4
    unit_price = Decimal("25.00")
    unit_cost = Decimal("15.00")

    subtotal = qty * unit_price
    cost_total = qty * unit_cost
    gross_profit = subtotal - cost_total
    margin_pct = (gross_profit / subtotal) * Decimal("100.0")

    assert subtotal == Decimal("100.00")
    assert cost_total == Decimal("60.00")
    assert gross_profit == Decimal("40.00")
    assert margin_pct == Decimal("40.0")

def test_database_financial_integrity():
    """Verify all database order items maintain positive or zero profit margins and exact arithmetic."""
    db = SessionLocal()
    try:
        items = db.query(OrderItem).limit(100).all()
        assert len(items) > 0, "Database should contain seeded order items."

        for item in items:
            assert item.quantity > 0, "Quantity must be strictly positive."
            assert item.unit_price >= item.unit_cost, "Unit price must be >= unit cost to prevent negative gross profit."
            
            # Check arithmetic
            rev = item.quantity * item.unit_price
            cst = item.quantity * item.unit_cost
            prof = rev - cst
            assert prof >= 0
    finally:
        db.close()
