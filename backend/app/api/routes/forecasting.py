from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.forecast import Forecast
from backend.app.models.product import Product
from backend.app.analytics.forecasting import generate_product_forecast

router = APIRouter(prefix="/forecasts", tags=["Demand Forecasting"])

@router.get("")
def get_forecasts(
    product_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    q = (
        db.query(Forecast, Product.product_name, Product.category)
        .join(Product, Forecast.product_id == Product.product_id)
    )
    if product_id:
        q = q.filter(Forecast.product_id == product_id)

    forecasts = q.order_by(Forecast.forecast_date.asc()).limit(limit).all()
    results = []
    for f, pname, cat in forecasts:
        results.append({
            "forecast_id": f.forecast_id,
            "product_id": f.product_id,
            "product_name": pname,
            "category": cat,
            "forecast_date": f.forecast_date.isoformat(),
            "predicted_quantity": float(f.predicted_quantity),
            "lower_bound": float(f.lower_bound),
            "upper_bound": float(f.upper_bound),
            "model_name": f.model_name,
            "generated_at": f.generated_at.isoformat()
        })

    return results

@router.post("/run")
def trigger_forecast_run(
    product_id: int = Query(..., ge=1),
    horizon_days: int = Query(14, ge=7, le=30),
    model_name: str = Query("Moving-Average", pattern="^(Moving-Average|Naive|Scikit-Learn Regression)$"),
    db: Session = Depends(get_db)
):
    """
    Computes time-series demand predictions for the specified product.
    """
    return generate_product_forecast(
        db=db,
        product_id=product_id,
        horizon_days=horizon_days,
        model_type=model_name,
        persist=True
    )

@router.get("/metrics")
def get_forecast_metrics(db: Session = Depends(get_db)):
    total_forecasts = db.query(Forecast).count()
    distinct_products = db.query(Forecast.product_id).distinct().count()
    distinct_models = [r[0] for r in db.query(Forecast.model_name).distinct().all()]

    return {
        "total_active_forecasts": total_forecasts,
        "forecasted_products_count": distinct_products,
        "available_models": ["Naive Baseline", "Moving-Average (7D)", "Scikit-Learn Lag Regression"],
        "persisted_models": distinct_models,
        "evaluation_metrics_available": ["MAE (Mean Absolute Error)", "RMSE (Root Mean Squared Error)"]
    }
