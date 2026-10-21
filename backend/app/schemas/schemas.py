from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal

# --- Health ---
class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    database_type: str
    database_name: str
    database_port: int
    tables_found: int
    version: str
    timestamp: datetime

# --- Supplier ---
class SupplierBase(BaseModel):
    supplier_name: str
    contact_email: str
    phone: str
    city: str
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None

class SupplierOut(SupplierBase):
    supplier_id: int
    created_at: datetime
    products_count: Optional[int] = 0
    low_stock_products_count: Optional[int] = 0

    class Config:
        from_attributes = True

# --- Customer ---
class CustomerOut(BaseModel):
    customer_id: int
    customer_name: str
    email: str
    city: str
    registration_date: date
    created_at: datetime
    total_orders: Optional[int] = 0
    total_spent: Optional[float] = 0.0
    latest_order_date: Optional[date] = None
    segment_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Product ---
class ProductOut(BaseModel):
    product_id: int
    product_name: str
    category: str
    supplier_id: int
    supplier_name: Optional[str] = None
    unit_cost: float
    selling_price: float
    is_active: bool
    stock_quantity: Optional[int] = 0
    reorder_level: Optional[int] = 10
    stock_status: Optional[str] = "Normal"

    class Config:
        from_attributes = True

# --- Order & Items ---
class OrderItemOut(BaseModel):
    order_item_id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    unit_price: float
    unit_cost: float
    subtotal: float
    profit: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    order_id: int
    customer_id: int
    customer_name: Optional[str] = None
    order_date: date
    region: str
    order_status: str
    created_at: datetime
    total_amount: float
    total_cost: float
    total_profit: float
    items_count: int
    items: Optional[List[OrderItemOut]] = []

    class Config:
        from_attributes = True

# --- Inventory ---
class InventoryOut(BaseModel):
    product_id: int
    product_name: str
    category: str
    supplier_id: int
    supplier_name: str
    unit_cost: float
    selling_price: float
    stock_quantity: int
    reorder_level: int
    stock_status: str
    recommended_order_quantity: int
    estimated_reorder_cost: float
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    stock_quantity: int
    reorder_level: Optional[int] = None

# --- Algorithm Run ---
class AlgorithmRunRequest(BaseModel):
    algorithm_name: str
    input_size: int = Field(default=50, ge=2, le=5000)
    iterations: int = Field(default=3, ge=1, le=10)

class AlgorithmRunOut(BaseModel):
    run_id: int
    algorithm_name: str
    problem_type: str
    input_size: int
    execution_time_ms: float
    memory_usage_mb: float
    result_summary: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Anomaly Alert ---
class AnomalyUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pending Review|Under Review|Resolved|Dismissed)$")

# --- Inventory Optimization Request ---
class InventoryOptimizeRequest(BaseModel):
    budget: float = Field(..., gt=0)
    planning_horizon_days: int = Field(default=14, ge=7, le=60)
