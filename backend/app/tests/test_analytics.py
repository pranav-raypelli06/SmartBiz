from backend.app.db.session import SessionLocal
from backend.app.models.product import Product
from backend.app.analytics.rfm_segmentation import run_rfm_segmentation
from backend.app.analytics.forecasting import generate_product_forecast
from backend.app.analytics.anomaly_detector import detect_transaction_anomalies

def test_rfm_segmentation():
    db = SessionLocal()
    try:
        res = run_rfm_segmentation(db, n_clusters=4, persist=False)
        assert res["status"] == "success"
        assert res["total_customers_analyzed"] > 50
        assert len(res["segment_summary"]) == 4
        assert "Champions" in [s["segment_name"] for s in res["segment_summary"]]
    finally:
        db.close()

def test_demand_forecasting():
    db = SessionLocal()
    try:
        prod = db.query(Product).first()
        assert prod is not None

        # Test Moving Average
        res_ma = generate_product_forecast(db, prod.product_id, horizon_days=7, model_type="Moving-Average", persist=False)
        assert res_ma["status"] == "success"
        assert len(res_ma["forecasts"]) == 7
        assert "mae" in res_ma["metrics"]
        assert "rmse" in res_ma["metrics"]
        assert res_ma["forecasts"][0]["lower_bound"] <= res_ma["forecasts"][0]["predicted_quantity"]
        assert res_ma["forecasts"][0]["upper_bound"] >= res_ma["forecasts"][0]["predicted_quantity"]

        # Test Naive
        res_naive = generate_product_forecast(db, prod.product_id, horizon_days=7, model_type="Naive", persist=False)
        assert res_naive["status"] == "success"
        assert len(res_naive["forecasts"]) == 7
    finally:
        db.close()

def test_anomaly_detection():
    db = SessionLocal()
    try:
        res = detect_transaction_anomalies(db, contamination=0.05, persist=False)
        assert res["status"] == "success"
        assert res["total_orders_scanned"] > 100
        assert res["anomalies_detected_count"] > 0
        for alert in res["anomalies"]:
            assert alert["severity"] in ["Low", "Medium", "High", "Critical"]
            assert 0.0 <= alert["anomaly_score"] <= 1.0
            assert len(alert["reason"]) > 10
    finally:
        db.close()
