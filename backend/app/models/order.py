from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False, index=True)
    order_date = Column(Date, nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    order_status = Column(String(50), nullable=False, default="Completed", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    anomalies = relationship("AnomalyAlert", back_populates="order")
