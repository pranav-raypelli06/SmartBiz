from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    registration_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer")
    segments = relationship("CustomerSegment", back_populates="customer")
    anomalies = relationship("AnomalyAlert", back_populates="customer")
