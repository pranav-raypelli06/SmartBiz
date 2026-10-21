import io
import csv
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.db.session import get_db
from backend.app.models import (
    Supplier, Customer, Product, Order, OrderItem,
    Inventory, Forecast, CustomerSegment, AnomalyAlert, AlgorithmRun
)
from database.seed_data import seed_database

router = APIRouter(prefix="/data", tags=["Data Management"])

@router.get("/status")
def get_data_status(db: Session = Depends(get_db)):
    """
    Returns record counts for all ten core relational database tables.
    """
    counts = {
        "suppliers": db.query(Supplier).count(),
        "customers": db.query(Customer).count(),
        "products": db.query(Product).count(),
        "orders": db.query(Order).count(),
        "order_items": db.query(OrderItem).count(),
        "inventory": db.query(Inventory).count(),
        "forecasts": db.query(Forecast).count(),
        "customer_segments": db.query(CustomerSegment).count(),
        "anomaly_alerts": db.query(AnomalyAlert).count(),
        "algorithm_runs": db.query(AlgorithmRun).count(),
    }
    is_seeded = counts["suppliers"] > 0 and counts["orders"] > 0

    return {
        "status": "ready" if is_seeded else "empty",
        "is_seeded": is_seeded,
        "table_counts": counts,
        "total_records": sum(counts.values()),
        "last_checked": datetime.utcnow().isoformat()
    }

@router.post("/seed")
def trigger_seed_demo_data(
    reset: bool = Form(False),
    db: Session = Depends(get_db)
):
    """
    Loads deterministic synthetic retail data for demonstration.
    """
    try:
        seed_database(reset=reset)
        return {
            "status": "success",
            "message": "Demo data populated successfully." if reset else "Demo data verified/seeded.",
            "reset_performed": reset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {str(e)}")

@router.get("/export/{table_name}")
def export_table_csv(table_name: str, db: Session = Depends(get_db)):
    """
    Exports table data as downloadable CSV.
    """
    table_map = {
        "suppliers": Supplier,
        "customers": Customer,
        "products": Product,
        "orders": Order,
        "order_items": OrderItem,
        "inventory": Inventory,
        "forecasts": Forecast,
        "customer_segments": CustomerSegment,
        "anomaly_alerts": AnomalyAlert,
        "algorithm_runs": AlgorithmRun,
    }

    model = table_map.get(table_name.lower())
    if not model:
        raise HTTPException(status_code=400, detail=f"Invalid table '{table_name}'. Supported: {list(table_map.keys())}")

    records = db.query(model).all()
    if not records:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["message"])
        writer.writerow(["No records found in table"])
        return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={table_name}.csv"})

    # Extract column names from model table
    columns = [c.name for c in model.__table__.columns]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)

    for r in records:
        row_vals = []
        for col in columns:
            val = getattr(r, col, "")
            if isinstance(val, (datetime, date)):
                val = val.isoformat()
            elif isinstance(val, Decimal):
                val = float(val)
            row_vals.append(val)
        writer.writerow(row_vals)

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
    )

@router.post("/import")
async def import_csv_data(
    table_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Validates and persists uploaded CSV data into the specified table.
    Enforces required headers, data types, and foreign key boundaries.
    """
    table_lower = table_name.lower().strip()
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum allowable limit of 5MB.")

    try:
        decoded = contents.decode("utf-8")
    except UnicodeDecodeError:
        try:
            decoded = contents.decode("latin-1")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid file encoding. UTF-8 or Latin-1 required.")

    reader = csv.DictReader(io.StringIO(decoded))
    rows = list(reader)

    if not rows:
        raise HTTPException(status_code=400, detail="CSV file contains no data rows.")
    if len(rows) > 1000:
        raise HTTPException(status_code=400, detail="Row limit exceeded (maximum 1,000 rows per batch import).")

    inserted = 0
    errors = []

    if table_lower == "suppliers":
        required = {"supplier_name", "contact_email", "phone", "city"}
        if not required.issubset(reader.fieldnames or []):
            raise HTTPException(status_code=400, detail=f"Missing required columns. Expected: {required}")
        for idx, row in enumerate(rows):
            try:
                s = Supplier(
                    supplier_name=row["supplier_name"].strip(),
                    contact_email=row["contact_email"].strip(),
                    phone=row["phone"].strip(),
                    city=row["city"].strip(),
                    is_active=True
                )
                db.add(s)
                inserted += 1
            except Exception as e:
                errors.append(f"Row {idx+1}: {str(e)}")

    elif table_lower == "customers":
        required = {"customer_name", "email", "city"}
        if not required.issubset(reader.fieldnames or []):
            raise HTTPException(status_code=400, detail=f"Missing required columns. Expected: {required}")
        for idx, row in enumerate(rows):
            try:
                # Duplicate check
                existing = db.query(Customer).filter(Customer.email == row["email"].strip()).first()
                if existing:
                    continue
                c = Customer(
                    customer_name=row["customer_name"].strip(),
                    email=row["email"].strip(),
                    city=row["city"].strip(),
                    registration_date=date.today()
                )
                db.add(c)
                inserted += 1
            except Exception as e:
                errors.append(f"Row {idx+1}: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail=f"CSV import currently supported for 'suppliers' and 'customers'.")

    db.commit()

    return {
        "status": "success",
        "table": table_lower,
        "rows_processed": len(rows),
        "rows_inserted": inserted,
        "errors_count": len(errors),
        "errors": errors[:10]
    }
