from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    forecast_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, index=True)
    forecast_date = Column(Date, nullable=False)
    predicted_quantity = Column(Numeric(10, 2), nullable=False)
    lower_bound = Column(Numeric(10, 2), nullable=False)
    upper_bound = Column(Numeric(10, 2), nullable=False)
    model_name = Column(String(100), nullable=False)
    generated_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    product = relationship("Product", back_populates="forecasts")
