from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.session import get_db
from backend.app.models.anomaly_alert import AnomalyAlert
from backend.app.models.order import Order
from backend.app.models.customer import Customer
from backend.app.analytics.anomaly_detector import detect_transaction_anomalies
from backend.app.schemas.schemas import AnomalyUpdate

router = APIRouter(prefix="/anomalies", tags=["Anomaly Detection"])

@router.get("")
def get_anomalies(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = (
        db.query(AnomalyAlert, Order, Customer.customer_name)
        .outerjoin(Order, AnomalyAlert.order_id == Order.order_id)
        .outerjoin(Customer, AnomalyAlert.customer_id == Customer.customer_id)
    )

    if severity and severity != "All":
        q = q.filter(AnomalyAlert.severity == severity)
    if status and status != "All":
        q = q.filter(AnomalyAlert.status == status)

    total_count = q.count()
    alerts = q.order_by(AnomalyAlert.detected_at.desc()).offset((page - 1) * limit).limit(limit).all()

    # Severity counts
    sev_counts = dict(
        db.query(AnomalyAlert.severity, func.count(AnomalyAlert.alert_id))
        .group_by(AnomalyAlert.severity)
        .all()
    )

    # Status counts
    stat_counts = dict(
        db.query(AnomalyAlert.status, func.count(AnomalyAlert.alert_id))
        .group_by(AnomalyAlert.status)
        .all()
    )

    records = []
    for alert, order, cust_name in alerts:
        records.append({
            "alert_id": alert.alert_id,
            "order_id": alert.order_id,
            "customer_id": alert.customer_id,
            "customer_name": cust_name or "Unknown Customer",
            "order_date": order.order_date.isoformat() if order else None,
            "region": order.region if order else None,
            "anomaly_score": float(alert.anomaly_score),
            "severity": alert.severity,
            "reason": alert.reason,
            "status": alert.status,
            "detected_at": alert.detected_at.isoformat()
        })

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "severity_summary": sev_counts,
        "status_summary": stat_counts,
        "alerts": records,
        "disclaimer": "Anomalies represent statistically unusual activity warranting investigation, not definitive proof of fraud."
    }

@router.post("/detect")
def trigger_anomaly_detection(
    contamination: float = Query(0.05, ge=0.01, le=0.20),
    db: Session = Depends(get_db)
):
    """
    Executes transaction feature extraction and Isolation Forest outlier detection across all orders.
    """
    return detect_transaction_anomalies(db, contamination=contamination, persist=True)

@router.patch("/{alert_id}")
def update_anomaly_status(
    alert_id: int,
    payload: AnomalyUpdate,
    db: Session = Depends(get_db)
):
    alert = db.query(AnomalyAlert).filter(AnomalyAlert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = payload.status
    db.commit()
    db.refresh(alert)

    return {
        "status": "success",
        "alert_id": alert.alert_id,
        "new_status": alert.status,
        "message": f"Alert {alert_id} status updated to '{alert.status}'."
    }
