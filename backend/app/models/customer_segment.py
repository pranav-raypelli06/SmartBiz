from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    segment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, index=True)
    segment_name = Column(String(100), nullable=False, index=True)
    recency_days = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    monetary_value = Column(Numeric(12, 2), nullable=False)
    model_version = Column(String(50), nullable=False)
    assigned_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    customer = relationship("Customer", back_populates="segments")
