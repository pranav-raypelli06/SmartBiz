# SmartBiz Analytics: Entity-Relationship (ER) Diagram

The following Mermaid diagram models all ten core relational database tables in SmartBiz Analytics, their primary and foreign key constraints, relationship cardinalities, and key column types.

```mermaid
erDiagram
    suppliers ||--o{ products : supplies
    suppliers ||--o{ inventory : stocks
    customers ||--o{ orders : places
    customers ||--o{ customer_segments : classifies
    customers ||--o{ anomaly_alerts : flagged_in
    orders ||--o{ order_items : contains
    orders ||--o{ anomaly_alerts : triggers
    products ||--|| inventory : tracked_in
    products ||--o{ order_items : ordered_as
    products ||--o{ forecasts : forecasted_for

    suppliers {
        int supplier_id PK
        string supplier_name
        string contact_email
        string phone
        string city
        boolean is_active
        datetime created_at
    }

    customers {
        int customer_id PK
        string customer_name
        string email UK
        string city
        date registration_date
        datetime created_at
    }

    products {
        int product_id PK
        string product_name
        string category
        int supplier_id FK
        decimal unit_cost
        decimal selling_price
        boolean is_active
    }

    orders {
        int order_id PK
        int customer_id FK
        date order_date
        string region
        string order_status
        datetime created_at
    }

    order_items {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal unit_cost
    }

    inventory {
        int product_id PK, FK
        int supplier_id FK
        int stock_quantity
        int reorder_level
        datetime last_updated
    }

    forecasts {
        int forecast_id PK
        int product_id FK
        date forecast_date
        decimal predicted_quantity
        decimal lower_bound
        decimal upper_bound
        string model_name
        datetime generated_at
    }

    customer_segments {
        int segment_id PK
        int customer_id FK
        string segment_name
        int recency_days
        int frequency
        decimal monetary_value
        string model_version
        datetime assigned_at
    }

    anomaly_alerts {
        int alert_id PK
        int order_id FK
        int customer_id FK
        decimal anomaly_score
        string severity
        text reason
        string status
        datetime detected_at
    }

    algorithm_runs {
        int run_id PK
        string algorithm_name
        string problem_type
        int input_size
        decimal execution_time_ms
        decimal memory_usage_mb
        text result_summary
        json configuration
        datetime created_at
    }
```
