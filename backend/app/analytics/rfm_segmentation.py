"""
RFM Customer Segmentation Engine (Scikit-Learn K-Means)
Calculates Recency, Frequency, and Monetary metrics from real transaction history.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sqlalchemy.orm import Session

from backend.app.models.customer import Customer
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.customer_segment import CustomerSegment

def run_rfm_segmentation(db: Session, n_clusters: int = 4, persist: bool = True) -> Dict[str, Any]:
    """
    Computes RFM features for all registered customers and performs K-Means clustering.
    Persists results to customer_segments if requested.
    """
    # 1. Fetch completed orders with items
    customers = db.query(Customer).all()
    if not customers:
        return {"error": "No customers found in database"}

    orders = db.query(Order).filter(Order.order_status == "Completed").all()
    
    # Map order totals
    order_items = db.query(OrderItem).all()
    order_totals: Dict[int, float] = {}
    for item in order_items:
        val = float(item.quantity) * float(item.unit_price)
        order_totals[item.order_id] = order_totals.get(item.order_id, 0.0) + val

    # Build customer order records
    cust_orders: Dict[int, List[Dict[str, Any]]] = {c.customer_id: [] for c in customers}
    for o in orders:
        if o.customer_id in cust_orders:
            cust_orders[o.customer_id].append({
                "date": o.order_date,
                "amount": order_totals.get(o.order_id, 0.0)
            })

    reference_date = date.today()
    rfm_rows = []

    for c in customers:
        c_orders = cust_orders.get(c.customer_id, [])
        if c_orders:
            latest_date = max(o["date"] for o in c_orders)
            recency = (reference_date - latest_date).days
            frequency = len(c_orders)
            monetary = sum(o["amount"] for o in c_orders)
        else:
            # Customer has never made a completed order
            recency = (reference_date - c.registration_date).days
            frequency = 0
            monetary = 0.0

        rfm_rows.append({
            "customer_id": c.customer_id,
            "customer_name": c.customer_name,
            "email": c.email,
            "city": c.city,
            "recency": max(1, recency),
            "frequency": frequency,
            "monetary": round(monetary, 2)
        })

    df = pd.DataFrame(rfm_rows)

    # 2. Scaling & Clustering
    features = df[["recency", "frequency", "monetary"]].copy()
    # Log-transform right-skewed frequency & monetary features to stabilize variance
    features["frequency_log"] = np.log1p(features["frequency"])
    features["monetary_log"] = np.log1p(features["monetary"])
    features["recency_log"] = np.log1p(features["recency"])

    scaler = StandardScaler()
    scaled_feats = scaler.fit_transform(features[["recency_log", "frequency_log", "monetary_log"]])

    # Adjust cluster count if insufficient unique rows
    n_clusters = min(n_clusters, len(df))
    if n_clusters < 2:
        n_clusters = 2

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_feats)
    df["cluster"] = cluster_labels

    # Calculate Silhouette score if valid
    sil_score = None
    if len(df) > n_clusters:
        try:
            sil_score = round(float(silhouette_score(scaled_feats, cluster_labels)), 4)
        except Exception:
            sil_score = 0.0

    # 3. Label clusters based on their observed centroid behaviors
    centroids = df.groupby("cluster")[["recency", "frequency", "monetary"]].mean()
    
    # Sort clusters by monetary value and frequency to rank customer tiers
    cluster_rank = centroids.sort_values(by=["monetary", "frequency"], ascending=[False, False]).index.tolist()
    
    tier_labels = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Hibernating"]
    cluster_name_map = {}
    for rank_idx, c_id in enumerate(cluster_rank):
        cluster_name_map[c_id] = tier_labels[rank_idx] if rank_idx < len(tier_labels) else f"Segment {rank_idx+1}"

    df["segment_name"] = df["cluster"].map(cluster_name_map)

    # 4. Optional Persistence to customer_segments
    model_version = f"KMeans-RFM-k{n_clusters}-v2.0"
    if persist:
        # Delete old assignments for these customers or keep historical
        db.query(CustomerSegment).delete()
        for _, row in df.iterrows():
            cs = CustomerSegment(
                customer_id=int(row["customer_id"]),
                segment_name=str(row["segment_name"]),
                recency_days=int(row["recency"]),
                frequency=int(row["frequency"]),
                monetary_value=Decimal(str(row["monetary"])),
                model_version=model_version,
                assigned_at=datetime.utcnow()
            )
            db.add(cs)
        db.commit()

    # 5. Build summary metrics
    summary = df.groupby("segment_name").agg(
        customer_count=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_spending=("monetary", "sum")
    ).reset_index()

    summary_records = []
    for _, row in summary.iterrows():
        summary_records.append({
            "segment_name": row["segment_name"],
            "customer_count": int(row["customer_count"]),
            "avg_recency_days": round(float(row["avg_recency"]), 1),
            "avg_frequency": round(float(row["avg_frequency"]), 1),
            "avg_monetary": round(float(row["avg_monetary"]), 2),
            "total_spending": round(float(row["total_spending"]), 2),
            "percentage_of_customers": round(float(row["customer_count"] / len(df) * 100), 1)
        })

    customer_details = df[["customer_id", "customer_name", "email", "city", "recency", "frequency", "monetary", "segment_name"]].to_dict(orient="records")

    return {
        "status": "success",
        "model_version": model_version,
        "n_clusters": n_clusters,
        "silhouette_score": sil_score,
        "total_customers_analyzed": len(df),
        "segment_summary": summary_records,
        "customers": customer_details[:100],  # Return preview
        "description": "RFM (Recency, Frequency, Monetary) clustering dynamically categorizes customers based on actual purchasing habits."
    }
