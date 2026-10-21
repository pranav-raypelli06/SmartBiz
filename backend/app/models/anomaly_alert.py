from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class AnomalyAlert(Base):
    __tablename__ = "anomaly_alerts"

    alert_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True, index=True)
    anomaly_score = Column(Numeric(8, 4), nullable=False)
    severity = Column(String(20), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="Pending Review", index=True)
    detected_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    order = relationship("Order", back_populates="anomalies")
    customer = relationship("Customer", back_populates="anomalies")
