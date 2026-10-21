from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, JSON
from backend.app.db.session import Base

class AlgorithmRun(Base):
    __tablename__ = "algorithm_runs"

    run_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    algorithm_name = Column(String(100), nullable=False, index=True)
    problem_type = Column(String(100), nullable=False, index=True)
    input_size = Column(Integer, nullable=False)
    execution_time_ms = Column(Numeric(12, 4), nullable=False)
    memory_usage_mb = Column(Numeric(10, 4), nullable=False)
    result_summary = Column(Text, nullable=False)
    configuration = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
