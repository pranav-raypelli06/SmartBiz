from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.session import get_db
from backend.app.models.customer import Customer
from backend.app.models.customer_segment import CustomerSegment
from backend.app.analytics.rfm_segmentation import run_rfm_segmentation

router = APIRouter(prefix="/customers/segments", tags=["Customer Intelligence"])

@router.get("")
def get_customer_segments(db: Session = Depends(get_db)):
    segments = db.query(CustomerSegment).all()
    if not segments:
        # Run segmentation dynamically if not present
        return run_rfm_segmentation(db, n_clusters=4, persist=True)

    # Group summary
    summary_q = (
        db.query(
            CustomerSegment.segment_name,
            func.count(CustomerSegment.segment_id).label("customer_count"),
            func.avg(CustomerSegment.recency_days).label("avg_recency"),
            func.avg(CustomerSegment.frequency).label("avg_frequency"),
            func.avg(CustomerSegment.monetary_value).label("avg_monetary"),
            func.sum(CustomerSegment.monetary_value).label("total_spending")
        )
        .group_by(CustomerSegment.segment_name)
        .order_by(func.sum(CustomerSegment.monetary_value).desc())
        .all()
    )

    total_customers = len(segments)
    summary_records = []
    for row in summary_q:
        cnt = int(row.customer_count)
        summary_records.append({
            "segment_name": row.segment_name,
            "customer_count": cnt,
            "avg_recency_days": round(float(row.avg_recency or 0), 1),
            "avg_frequency": round(float(row.avg_frequency or 0), 1),
            "avg_monetary": round(float(row.avg_monetary or 0), 2),
            "total_spending": round(float(row.total_spending or 0), 2),
            "percentage_of_customers": round((cnt / total_customers * 100), 1) if total_customers > 0 else 0.0
        })

    # Customer assignment preview
    cust_query = (
        db.query(CustomerSegment, Customer.customer_name, Customer.email, Customer.city)
        .join(Customer, CustomerSegment.customer_id == Customer.customer_id)
        .limit(100)
        .all()
    )
    cust_list = []
    for cs, cname, email, city in cust_query:
        cust_list.append({
            "customer_id": cs.customer_id,
            "customer_name": cname,
            "email": email,
            "city": city,
            "segment_name": cs.segment_name,
            "recency": cs.recency_days,
            "frequency": cs.frequency,
            "monetary": float(cs.monetary_value)
        })

    return {
        "status": "success",
        "total_customers_analyzed": total_customers,
        "segment_summary": summary_records,
        "customers": cust_list,
        "model_version": segments[0].model_version if segments else "v1.0"
    }

@router.post("/run")
def trigger_rfm_segmentation(
    clusters: int = Query(4, ge=2, le=6),
    db: Session = Depends(get_db)
):
    """
    Explicitly re-runs K-Means RFM clustering on latest customer order transactions.
    """
    return run_rfm_segmentation(db, n_clusters=clusters, persist=True)
