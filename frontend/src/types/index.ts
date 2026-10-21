export interface HealthStatus {
  status: string;
  database_connected: boolean;
  database_type: string;
  database_name: string;
  database_host: string;
  database_port: number;
  server_version: string;
  tables_found: number;
  version: string;
  timestamp: string;
}

export interface DashboardMetrics {
  total_revenue: number;
  gross_profit: number;
  profit_margin_pct: number;
  completed_orders: number;
  units_sold: number;
  average_order_value: number;
  low_stock_count: number;
}

export interface PeriodComparison {
  previous_start: string;
  previous_end: string;
  previous_revenue: number;
  revenue_change_pct: number | null;
  profit_change_pct: number | null;
  orders_change_pct: number | null;
}

export interface DashboardSummaryResponse {
  is_empty_database: boolean;
  message?: string;
  metrics: DashboardMetrics;
  comparison: PeriodComparison | null;
}

export interface SalesTrendPoint {
  month: string;
  revenue: number;
  profit: number;
  orders: number;
  units: number;
}

export interface CategoryPerformancePoint {
  category: string;
  revenue: number;
  profit: number;
  units: number;
}

export interface TopProductPoint {
  product_id: number;
  product_name: string;
  category: string;
  revenue: number;
  profit: number;
  units_sold: number;
}

export interface RegionalPerformancePoint {
  region: string;
  revenue: number;
  profit: number;
  order_count: number;
}

export interface CustomerItem {
  customer_id: number;
  customer_name: string;
  email: string;
  city: string;
  registration_date: string;
  created_at: string;
  total_orders: number;
  total_spent: number;
  latest_order_date: string | null;
  segment_name: string;
}

export interface ProductItem {
  product_id: number;
  product_name: string;
  category: string;
  supplier_id: number;
  supplier_name: string;
  unit_cost: number;
  selling_price: number;
  margin_pct: number;
  is_active: boolean;
  stock_quantity: number;
  reorder_level: number;
  stock_status: 'Adequate' | 'Low Stock' | 'Out of Stock';
}

export interface OrderItemDetail {
  order_item_id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  unit_cost: number;
  subtotal: number;
  profit: number;
}

export interface OrderRecord {
  order_id: number;
  customer_id: number;
  customer_name: string;
  order_date: string;
  region: string;
  order_status: string;
  items_count: number;
  total_amount: number;
  total_profit: number;
  items: OrderItemDetail[];
}

export interface SupplierItem {
  supplier_id: number;
  supplier_name: string;
  contact_email: string;
  phone: string;
  city: string;
  is_active: boolean;
  created_at: string;
  products_count: number;
  low_stock_products_count: number;
}

export interface InventoryItem {
  product_id: number;
  product_name: string;
  category: string;
  supplier_id: number;
  supplier_name: string;
  unit_cost: number;
  selling_price: number;
  stock_quantity: number;
  reorder_level: number;
  stock_status: string;
  recommended_order_quantity: number;
  estimated_reorder_cost: number;
  last_updated: string;
}

export interface AnomalyItem {
  alert_id: number;
  order_id: number | null;
  customer_id: number | null;
  customer_name: string;
  order_date: string | null;
  region: string | null;
  anomaly_score: number;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  reason: string;
  status: 'Pending Review' | 'Under Review' | 'Resolved' | 'Dismissed';
  detected_at: string;
}

export interface AlgorithmRunRecord {
  run_id: number;
  algorithm_name: string;
  problem_type: string;
  input_size: number;
  execution_time_ms: number;
  memory_usage_mb: number;
  result_summary: string;
  created_at: string;
}
