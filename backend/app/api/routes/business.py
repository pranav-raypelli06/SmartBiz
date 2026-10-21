from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.customer import Customer
from backend.app.models.product import Product
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.supplier import Supplier
from backend.app.models.inventory import Inventory
from backend.app.models.customer_segment import CustomerSegment
from backend.app.schemas.schemas import (
    SupplierCreate, SupplierUpdate, SupplierOut,
    CustomerOut, ProductOut, OrderOut, InventoryOut, InventoryUpdate
)

router = APIRouter(tags=["Business Data"])

# --- CUSTOMERS ---
@router.get("/customers")
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    city: Optional[str] = None,
    sort_by: Optional[str] = "name",
    db: Session = Depends(get_db)
):
    q = db.query(Customer)
    if search:
        search_filter = f"%{search}%"
        q = q.filter(or_(Customer.customer_name.ilike(search_filter), Customer.email.ilike(search_filter)))
    if city:
        q = q.filter(Customer.city == city)

    total_count = q.count()
    if sort_by == "registration_date":
        q = q.order_by(Customer.registration_date.desc())
    else:
        q = q.order_by(Customer.customer_name.asc())

    customers = q.offset((page - 1) * limit).limit(limit).all()

    # Enrich with orders count and total spend
    cust_ids = [c.customer_id for c in customers]
    spend_query = (
        db.query(
            Order.customer_id,
            func.count(func.distinct(Order.order_id)).label("order_count"),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0).label("total_spent"),
            func.max(Order.order_date).label("latest_order")
        )
        .join(OrderItem, Order.order_id == OrderItem.order_id)
        .filter(Order.customer_id.in_(cust_ids), Order.order_status == "Completed")
        .group_by(Order.customer_id)
        .all()
    )
    spend_map = {r[0]: (r[1], float(r[2]), r[3]) for r in spend_query}

    # Latest segment
    seg_query = db.query(CustomerSegment).filter(CustomerSegment.customer_id.in_(cust_ids)).all()
    seg_map = {s.customer_id: s.segment_name for s in seg_query}

    results = []
    for c in customers:
        orders_cnt, spent, latest = spend_map.get(c.customer_id, (0, 0.0, None))
        results.append({
            "customer_id": c.customer_id,
            "customer_name": c.customer_name,
            "email": c.email,
            "city": c.city,
            "registration_date": c.registration_date.isoformat(),
            "created_at": c.created_at.isoformat(),
            "total_orders": orders_cnt,
            "total_spent": round(spent, 2),
            "latest_order_date": latest.isoformat() if latest else None,
            "segment_name": seg_map.get(c.customer_id, "Unclassified")
        })

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "customers": results
    }

@router.get("/customers/{customer_id}")
def get_customer_profile(customer_id: int, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")

    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(Order.order_date.desc())
        .all()
    )

    order_history = []
    total_spent = 0.0
    for o in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == o.order_id).all()
        order_total = sum(float(it.quantity) * float(it.unit_price) for it in items)
        if o.order_status == "Completed":
            total_spent += order_total

        order_history.append({
            "order_id": o.order_id,
            "order_date": o.order_date.isoformat(),
            "region": o.region,
            "order_status": o.order_status,
            "items_count": len(items),
            "total_amount": round(order_total, 2)
        })

    segment = db.query(CustomerSegment).filter(CustomerSegment.customer_id == customer_id).first()

    return {
        "customer_id": c.customer_id,
        "customer_name": c.customer_name,
        "email": c.email,
        "city": c.city,
        "registration_date": c.registration_date.isoformat(),
        "total_orders": len(orders),
        "total_spent": round(total_spent, 2),
        "segment_name": segment.segment_name if segment else "Unclassified",
        "orders": order_history
    }

# --- PRODUCTS ---
@router.get("/products")
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Product, Supplier.supplier_name, Inventory.stock_quantity, Inventory.reorder_level) \
        .join(Supplier, Product.supplier_id == Supplier.supplier_id) \
        .outerjoin(Inventory, Product.product_id == Inventory.product_id)

    if category:
        q = q.filter(Product.category == category)
    if search:
        q = q.filter(Product.product_name.ilike(f"%{search}%"))
    if is_active is not None:
        q = q.filter(Product.is_active == is_active)

    items = q.order_by(Product.product_id.asc()).all()
    results = []
    for prod, sup_name, stock, reorder in items:
        stk = stock if stock is not None else 0
        reord = reorder if reorder is not None else 10
        if stk == 0:
            status = "Out of Stock"
        elif stk <= reord:
            status = "Low Stock"
        else:
            status = "Adequate"

        results.append({
            "product_id": prod.product_id,
            "product_name": prod.product_name,
            "category": prod.category,
            "supplier_id": prod.supplier_id,
            "supplier_name": sup_name,
            "unit_cost": float(prod.unit_cost),
            "selling_price": float(prod.selling_price),
            "margin_pct": round((float(prod.selling_price) - float(prod.unit_cost)) / float(prod.selling_price) * 100, 1),
            "is_active": prod.is_active,
            "stock_quantity": stk,
            "reorder_level": reord,
            "stock_status": status
        })

    return results

# --- ORDERS ---
@router.get("/orders")
def get_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    region: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Order).join(Customer, Order.customer_id == Customer.customer_id)
    if region:
        q = q.filter(Order.region == region)
    if status:
        q = q.filter(Order.order_status == status)
    if start_date:
        q = q.filter(Order.order_date >= start_date)
    if end_date:
        q = q.filter(Order.order_date <= end_date)
    if customer_id:
        q = q.filter(Order.customer_id == customer_id)

    total_count = q.count()
    orders = q.order_by(Order.order_date.desc(), Order.order_id.desc()).offset((page - 1) * limit).limit(limit).all()

    # Pre-fetch items and customer names
    o_ids = [o.order_id for o in orders]
    items_query = (
        db.query(OrderItem, Product.product_name)
        .join(Product, OrderItem.product_id == Product.product_id)
        .filter(OrderItem.order_id.in_(o_ids))
        .all()
    )
    items_by_order: dict = {}
    for item, pname in items_query:
        subtotal = float(item.quantity) * float(item.unit_price)
        cost_total = float(item.quantity) * float(item.unit_cost)
        items_by_order.setdefault(item.order_id, []).append({
            "order_item_id": item.order_item_id,
            "product_id": item.product_id,
            "product_name": pname,
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "unit_cost": float(item.unit_cost),
            "subtotal": round(subtotal, 2),
            "profit": round(subtotal - cost_total, 2)
        })

    cust_map = {c.customer_id: c.customer_name for c in db.query(Customer).filter(Customer.customer_id.in_([o.customer_id for o in orders])).all()}

    results = []
    for o in orders:
        its = items_by_order.get(o.order_id, [])
        tot_amt = sum(it["subtotal"] for it in its)
        tot_prof = sum(it["profit"] for it in its)

        results.append({
            "order_id": o.order_id,
            "customer_id": o.customer_id,
            "customer_name": cust_map.get(o.customer_id, "Unknown"),
            "order_date": o.order_date.isoformat(),
            "region": o.region,
            "order_status": o.order_status,
            "items_count": len(its),
            "total_amount": round(tot_amt, 2),
            "total_profit": round(tot_prof, 2),
            "items": its
        })

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "orders": results
    }

# --- SUPPLIERS ---
@router.get("/suppliers")
def get_suppliers(
    city: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Supplier)
    if city:
        q = q.filter(Supplier.city == city)
    if search:
        q = q.filter(or_(Supplier.supplier_name.ilike(f"%{search}%"), Supplier.contact_email.ilike(f"%{search}%")))
    if is_active is not None:
        q = q.filter(Supplier.is_active == is_active)

    suppliers = q.order_by(Supplier.supplier_id.asc()).all()

    # Product and low stock counts
    results = []
    for s in suppliers:
        prods = db.query(Product).filter(Product.supplier_id == s.supplier_id).all()
        p_ids = [p.product_id for p in prods]
        low_count = 0
        if p_ids:
            low_count = db.query(Inventory).filter(
                Inventory.product_id.in_(p_ids),
                Inventory.stock_quantity <= Inventory.reorder_level
            ).count()

        results.append({
            "supplier_id": s.supplier_id,
            "supplier_name": s.supplier_name,
            "contact_email": s.contact_email,
            "phone": s.phone,
            "city": s.city,
            "is_active": s.is_active,
            "created_at": s.created_at.isoformat(),
            "products_count": len(prods),
            "low_stock_products_count": low_count
        })

    return results

@router.post("/suppliers", status_code=status.HTTP_201_CREATED)
def create_supplier(supplier_in: SupplierCreate, db: Session = Depends(get_db)):
    s = Supplier(
        supplier_name=supplier_in.supplier_name,
        contact_email=supplier_in.contact_email,
        phone=supplier_in.phone,
        city=supplier_in.city,
        is_active=supplier_in.is_active
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, supplier_in: SupplierUpdate, db: Session = Depends(get_db)):
    s = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if supplier_in.supplier_name is not None:
        s.supplier_name = supplier_in.supplier_name
    if supplier_in.contact_email is not None:
        s.contact_email = supplier_in.contact_email
    if supplier_in.phone is not None:
        s.phone = supplier_in.phone
    if supplier_in.city is not None:
        s.city = supplier_in.city
    if supplier_in.is_active is not None:
        s.is_active = supplier_in.is_active

    db.commit()
    db.refresh(s)
    return s

# --- INVENTORY ---
@router.get("/inventory")
def get_inventory(
    stock_status: Optional[str] = None, # 'Low Stock', 'Out of Stock', 'Adequate'
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = (
        db.query(Inventory, Product, Supplier)
        .join(Product, Inventory.product_id == Product.product_id)
        .join(Supplier, Inventory.supplier_id == Supplier.supplier_id)
    )

    if category:
        q = q.filter(Product.category == category)
    if search:
        q = q.filter(or_(Product.product_name.ilike(f"%{search}%"), Supplier.supplier_name.ilike(f"%{search}%")))

    rows = q.order_by(Inventory.stock_quantity.asc()).all()
    results = []

    for inv, prod, sup in rows:
        stk = inv.stock_quantity
        reord = inv.reorder_level

        if stk == 0:
            status_label = "Out of Stock"
        elif stk <= reord:
            status_label = "Low Stock"
        else:
            status_label = "Adequate"

        if stock_status and stock_status != "All" and status_label != stock_status:
            continue

        # Recommended order quantity: (reorder * 2 - stock) if stock <= reorder else 0
        rec_qty = max(0, (reord * 2) - stk) if stk <= reord else 0
        est_cost = rec_qty * float(prod.unit_cost)

        results.append({
            "product_id": prod.product_id,
            "product_name": prod.product_name,
            "category": prod.category,
            "supplier_id": sup.supplier_id,
            "supplier_name": sup.supplier_name,
            "unit_cost": float(prod.unit_cost),
            "selling_price": float(prod.selling_price),
            "stock_quantity": stk,
            "reorder_level": reord,
            "stock_status": status_label,
            "recommended_order_quantity": rec_qty,
            "estimated_reorder_cost": round(est_cost, 2),
            "last_updated": inv.last_updated.isoformat()
        })

    return results

@router.patch("/inventory/{product_id}")
def update_inventory_stock(product_id: int, inv_update: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found for product")

    inv.stock_quantity = max(0, inv_update.stock_quantity)
    if inv_update.reorder_level is not None:
        inv.reorder_level = max(0, inv_update.reorder_level)

    db.commit()
    db.refresh(inv)
    return {
        "status": "success",
        "product_id": inv.product_id,
        "stock_quantity": inv.stock_quantity,
        "reorder_level": inv.reorder_level,
        "last_updated": inv.last_updated.isoformat()
    }
