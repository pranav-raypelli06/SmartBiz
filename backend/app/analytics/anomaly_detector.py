"""
Transparent Anomaly Detection Engine
Combines statistical Z-score/IQR outlier detection with Scikit-Learn IsolationForest.
Flags unusual transactions with transparent explanations.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.customer import Customer
from backend.app.models.anomaly_alert import AnomalyAlert

def detect_transaction_anomalies(
    db: Session,
    contamination: float = 0.05,
    persist: bool = True
) -> Dict[str, Any]:
    """
    Extracts transaction features across all orders and detects anomalous spending or order volume.
    Flags unusual transactions for manual business review.
    """
    orders = db.query(Order).all()
    if not orders:
        return {"error": "No orders found to evaluate."}

    # Aggregate order items
    order_items = db.query(OrderItem).all()
    items_by_order: Dict[int, List[OrderItem]] = {}
    for item in order_items:
        items_by_order.setdefault(item.order_id, []).append(item)

    features_list = []
    for o in orders:
        items = items_by_order.get(o.order_id, [])
        total_val = sum(float(it.quantity) * float(it.unit_price) for it in items)
        total_qty = sum(it.quantity for it in items)
        distinct_products = len(set(it.product_id for it in items))

        features_list.append({
            "order_id": o.order_id,
            "customer_id": o.customer_id,
            "order_date": o.order_date,
            "region": o.region,
            "total_value": total_val,
            "total_quantity": total_qty,
            "distinct_products": distinct_products
        })

    df = pd.DataFrame(features_list)

    # 1. Statistical Baselines (mean & std for value and quantity)
    val_mean = df["total_value"].mean()
    val_std = df["total_value"].std() or 1.0
    qty_mean = df["total_quantity"].mean()
    qty_std = df["total_quantity"].std() or 1.0

    df["z_value"] = (df["total_value"] - val_mean) / val_std
    df["z_quantity"] = (df["total_quantity"] - qty_mean) / qty_std

    # 2. Isolation Forest Model
    X = df[["total_value", "total_quantity", "distinct_products"]].values
    iso = IsolationForest(contamination=contamination, random_state=42)
    iso.fit(X)
    raw_scores = iso.decision_function(X) # Higher = normal, Lower = anomalous
    
    # Invert and normalize to [0, 1] range: 1.0 = highly anomalous
    min_score, max_score = raw_scores.min(), raw_scores.max()
    score_range = max_score - min_score if max_score != min_score else 1.0
    normalized_scores = 1.0 - ((raw_scores - min_score) / score_range)
    df["anomaly_score"] = normalized_scores

    # 3. Identify and explain anomalies
    alerts_created = 0
    new_alerts = []

    # Get customer lookup
    cust_map = {c.customer_id: c.customer_name for c in db.query(Customer).all()}

    # Existing alerted order IDs to avoid duplicate alerts
    existing_alerted_orders = set(r[0] for r in db.query(AnomalyAlert.order_id).filter(AnomalyAlert.order_id.isnot(None)).all())

    for _, row in df.iterrows():
        score = float(row["anomaly_score"])
        is_stat_outlier = row["z_value"] > 2.8 or row["z_quantity"] > 2.8
        is_iso_outlier = score > 0.75

        if is_stat_outlier or is_iso_outlier:
            # Build reasons
            reasons = []
            if row["z_value"] > 2.8:
                reasons.append(f"Order value (${row['total_value']:,.2f}) is {row['z_value']:.1f} standard deviations above the average (${val_mean:,.2f})")
            if row["z_quantity"] > 2.8:
                reasons.append(f"Order quantity ({int(row['total_quantity'])} units) is {row['z_quantity']:.1f} std deviations above normal ({qty_mean:.1f} units)")
            if not reasons:
                reasons.append(f"Isolation Forest multidimensional outlier score of {score:.2f}")

            reason_str = "; ".join(reasons) + ". Flagged as unusual activity requiring review (not proof of fraud)."

            # Determine severity
            if score > 0.88 or row["z_value"] > 4.0:
                severity = "Critical"
            elif score > 0.78 or row["z_value"] > 3.0:
                severity = "High"
            elif score > 0.65:
                severity = "Medium"
            else:
                severity = "Low"

            alert_dict = {
                "order_id": int(row["order_id"]),
                "customer_id": int(row["customer_id"]),
                "customer_name": cust_map.get(int(row["customer_id"]), "Unknown Customer"),
                "order_date": row["order_date"].isoformat() if hasattr(row["order_date"], "isoformat") else str(row["order_date"]),
                "anomaly_score": round(score, 4),
                "severity": severity,
                "reason": reason_str,
                "status": "Pending Review",
                "total_value": round(float(row["total_value"]), 2),
                "total_quantity": int(row["total_quantity"])
            }
            new_alerts.append(alert_dict)

            if persist and int(row["order_id"]) not in existing_alerted_orders:
                alert_obj = AnomalyAlert(
                    order_id=int(row["order_id"]),
                    customer_id=int(row["customer_id"]),
                    anomaly_score=Decimal(str(round(score, 4))),
                    severity=severity,
                    reason=reason_str,
                    status="Pending Review",
                    detected_at=datetime.utcnow()
                )
                db.add(alert_obj)
                alerts_created += 1

    if persist:
        db.commit()

    return {
        "status": "success",
        "total_orders_scanned": len(df),
        "anomalies_detected_count": len(new_alerts),
        "new_alerts_persisted": alerts_created,
        "anomalies": new_alerts[:50],
        "severity_distribution": {
            "Critical": sum(1 for a in new_alerts if a["severity"] == "Critical"),
            "High": sum(1 for a in new_alerts if a["severity"] == "High"),
            "Medium": sum(1 for a in new_alerts if a["severity"] == "Medium"),
            "Low": sum(1 for a in new_alerts if a["severity"] == "Low"),
        },
        "disclaimer": "Anomalies indicate unusual statistical patterns that warrant operational review, not conclusive fraud."
    }
