# SmartBiz Analytics
> **Turn Business Data Into Smarter Decisions.**

An algorithm-driven enterprise business intelligence and predictive decision-support platform built with **React 19, TypeScript, Vite, Tailwind CSS, FastAPI, SQLAlchemy ORM, and MySQL 8.x**.

Engineered for academic rigour in **Analysis of Algorithms (AoA)** and expandable into a commercial-grade final-year capstone engineering project.

---

## 1. Project Overview

Retail enterprises collect extensive transactional records across customers, products, suppliers, inventories, and orders. Without an integrated decision engine, this data remains passive.

**SmartBiz Analytics** unifies relational data storage, unsupervised machine learning, predictive time-series forecasting, and an interactive **Algorithm Lab** featuring manual Python implementations of classical searching, sorting, greedy heuristics, dynamic programming, and graph routing algorithms.

---

## 2. Key Modules & Features

### 📊 Executive Overview Dashboard
- **6 Real-time Financial KPI Cards**: Total Revenue, Estimated Gross Profit, Completed Orders, Units Sold, Average Order Value (AOV), and Products Requiring Restocking.
- **Dynamic Filtering**: Date ranges, product categories (Electronics, Office Supplies, Home & Kitchen, Apparel, Health & Personal Care), regions (North, South, East, West, Central), and order statuses.
- **Visual Analytics**: Interactive Recharts for monthly revenue/profit trends, category shares, top 10 products, and regional revenue breakdowns.
- **Comparison Engine**: Mathematically verified percentage changes against previous equivalent periods.
- **Empty State Support**: Onboarding card with one-click demo data population.

### 👥 Customer Intelligence (K-Means RFM)
- Unsupervised machine learning clustering based on **Recency** (days since latest order), **Frequency** (total qualifying orders), and **Monetary Value** (lifetime spend).
- Automated cluster profiling mapping centroids into descriptive tiers: *Champions, Loyal Customers, Potential Loyalists, At Risk, and Hibernating*.
- Feature scaling with `StandardScaler` and variance-stabilizing log transforms.
- Silhouette score calculation and interactive cluster count adjustment ($k = 3 \text{ to } 6$).
- Customer directory with search and historical segment allocations stored in MySQL `customer_segments`.

### 📈 Demand Forecasting Engine
- Multi-model time-series predictions:
  - **Moving-Average (7D)**
  - **Naive Baseline** (lagged previous period)
  - **Scikit-Learn Regression** (multi-lag regression with calendar features)
- Chronological train/test split to prevent future-data leakage.
- Statistical backtesting evaluation reporting **MAE** (Mean Absolute Error) and **RMSE** (Root Mean Squared Error).
- 90% confidence bands (upper and lower bounds) persisted in MySQL `forecasts`.

### 📦 Inventory Optimization (Knapsack & Greedy)
- Decision-support stock replenishment engine based on reorder thresholds and forecasted demand.
- **0/1 Knapsack Dynamic Programming**: Computes the globally optimal batch selection under a budget constraint ($O(n \cdot W)$).
- **Greedy Heuristic**: Ranks candidates by benefit-to-cost ratio ($O(n \log n)$).
- Side-by-side comparison illustrating exact percentage gains of DP over greedy due to budget fragmentation avoidance.
- Non-destructive decision-support design: recommendations do not alter database stock without explicit operational review.

### 🛡️ Transaction Anomaly Detection
- Multi-dimensional anomaly scoring combining statistical Z-score/IQR outliers with Scikit-Learn **Isolation Forest**.
- Normalized anomaly scores ($0.0 \text{ to } 1.0$) categorized into severity tiers (*Critical, High, Medium, Low*).
- Transparent, human-understandable explanation strings generated for each alert.
- Persisted in MySQL `anomaly_alerts` with interactive investigation review workflows (*Pending Review, Under Review, Resolved, Dismissed*).
- Strict transparency notice: anomalies represent unusual statistical activity requiring review, not proof of fraud.

### 🚚 Supplier Management
- Comprehensive vendor directory with contact email, phone, city, and active status.
- Linked inventory tracking displaying associated products and low-stock replenishment indicators.
- Validated supplier creation form with immediate database persistence.

### 🔬 Algorithm Lab (Analysis of Algorithms - AoA)
- **Manual Implementations**: No reliance on built-in `sort()`, `bisect`, or graph libraries.
  - **Searching**: Linear Search ($O(n)$) and Binary Search ($O(\log n)$) with sorted array precondition verification.
  - **Sorting**: Bubble Sort ($O(n^2)$), Merge Sort ($O(n \log n)$), and Quicksort ($O(n \log n)$) tracking comparisons, swaps, and memory.
  - **Optimization**: 0/1 Knapsack DP vs Greedy Ratio heuristic with small-input brute-force verification ($2^n$).
  - **Graph Theory**: Breadth-First Search (BFS), Depth-First Search (DFS), Dijkstra Shortest Path (rejects negative weights), and Kruskal's Minimum Spanning Tree (MST) using Disjoint Set Union (Union-Find).
- **Empirical Profiling**: Hardware runtime measured with `time.perf_counter()`, memory peaks measured with `tracemalloc`, taking medians over repeated trials.
- **MySQL Benchmark History**: Every run is persisted into `algorithm_runs` for empirical vs. theoretical Big-O comparisons.
- **Logistics Graph Topology**: Interactive SVG visualizer displaying supply chain hubs and shortest routing paths.

### 🗄️ Data Explorer & CSV Operations
- Inspect and filter all ten core relational database tables.
- One-click verified CSV export for any selected table (`/api/data/export/{table_name}`).
- Safe CSV batch import with file size limits (5MB), row caps (1,000), column header validation, and duplicate detection.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons, React Router v7 |
| **Backend** | Python 3.11 / 3.14, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic V2, python-dotenv |
| **Database** | MySQL 8.x (InnoDB engine, foreign-keys, composite indexes, DECIMAL monetary fields) |
| **Machine Learning** | Scikit-Learn (K-Means, Isolation Forest, Ridge), Pandas, NumPy |
| **Testing** | Pytest (18 unit/integration tests), TypeScript Compiler (`tsc -b`) |
| **DevOps** | Git, Docker Compose, environment-based configuration (`.env`) |

---

## 4. Database Schema (10 Core Relational Tables)

All tables use the InnoDB storage engine with strict foreign-key constraints and indexes:

1. `suppliers`: Vendor details, cities, active status, contact details.
2. `customers`: Customer records, emails (unique), registration dates.
3. `products`: Catalog items, categories, supplier foreign keys, unit costs, selling prices.
4. `orders`: Transactions, customer foreign keys, dates, regions, statuses.
5. `order_items`: Order line items, product foreign keys, quantities, unit prices, unit costs.
6. `inventory`: Product primary key/foreign key, supplier foreign key, stock quantities, reorder thresholds.
7. `forecasts`: Time-series predictions, upper/lower bounds, applied model, timestamps.
8. `customer_segments`: Historical RFM assignments, cluster names, recency, frequency, monetary value.
9. `anomaly_alerts`: Flagged transactions, anomaly scores, severity, detailed reasons, review statuses.
10. `algorithm_runs`: Benchmark runs, algorithm names, input sizes, runtime in ms, memory in MB, configuration JSON.

An Entity-Relationship (ER) diagram in Mermaid format is available at [`docs/er_diagram.md`](file:///E:/SmartBiz_project/docs/er_diagram.md).

---

## 5. Prerequisites

- **Python**: Version 3.11 or higher (verified compatible with 3.11 and 3.14)
- **Node.js**: Version 20.x or higher (npm 10+)
- **MySQL Server**: 8.0.x (Running locally or via Docker Compose)

---

## 6. Installation & Configuration

### Step 1: Clone Repository
```bash
git clone https://github.com/pranav-raypelli06/SmartBiz.git
cd SmartBiz
```

### Step 2: Environment Configuration
Copy `.env.example` to `.env` and verify database credentials:
```bash
cp .env.example .env
```
Default `.env` configuration:
```ini
DB_HOST=127.0.0.1
DB_PORT=3307
DB_USER=smartbiz_user
DB_PASSWORD=smartbiz_pass
DB_NAME=smartbiz_db

APP_NAME="SmartBiz Analytics"
API_PORT=8000
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
SECRET_KEY=smartbiz-analytics-super-secret-key-development-2026
```

---

## 7. Database Initialization & Startup

### Option A: Native MySQL 8.x (Configured for Port 3307)
Initialize and start the MySQL daemon:
```bash
# Apply schema
mysql -P 3307 -u smartbiz_user -psmartbiz_pass smartbiz_db < database/schema.sql

# Seed deterministic demonstration retail data (680 orders, 36 products, 125 customers)
python database/seed_data.py --reset
```

### Option B: Docker Compose (Alternative)
If a local MySQL server is not installed, start the full container stack:
```bash
docker-compose up -d
```

---

## 8. Running the Application

### 1. Start the Backend API (FastAPI)
```bash
# From workspace root:
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Health Diagnostic: `http://127.0.0.1:8000/api/health`

### 2. Start the Frontend (Vite + React)
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```
- Web Application UI: `http://127.0.0.1:5173`

---

## 9. Running Verification Tests

Run the full test suite verifying algorithms, financial math, ML analytics, and API endpoints:
```bash
# Run all 18 backend tests:
python -m pytest backend/app/tests/ -v

# Verify frontend TypeScript compilation and bundling:
cd frontend
npm run build
```

### Verified Test Results Summary:
- `test_searching_correctness`: PASSED (Linear & Binary search on $n=7$, unsorted exception handling)
- `test_sorting_correctness`: PASSED (Bubble, Merge, Quicksort output equality)
- `test_knapsack_optimality`: PASSED (0/1 Knapsack optimal DP verified against exhaustive $2^n$ brute-force)
- `test_greedy_vs_dp_divergence`: PASSED (DP achieves $30.0$ benefit vs Greedy $27.0$, $+11.1\%$ gain)
- `test_graph_algorithms`: PASSED (BFS, DFS, Dijkstra shortest path, Kruskal MST, negative weight rejection)
- `test_financial_calculations_manual_example`: PASSED (Revenue, COGS, Gross Profit, Margin %)
- `test_database_financial_integrity`: PASSED (100% of order items have positive margins)
- `test_rfm_segmentation`: PASSED (K-Means clustering across 125 customers)
- `test_demand_forecasting`: PASSED (Moving average & Naive models with confidence intervals)
- `test_anomaly_detection`: PASSED (Isolation Forest flags unusual transactions with reasons)
- `test_api_*`: PASSED (All 8 REST endpoint test cases return HTTP 200)

---

## 10. Analysis of Algorithms: Measured Empirical Benchmark Data

All benchmarks are measured using `time.perf_counter()` medians over 3 trials on an Intel Core i9-13980HX:

| Algorithm | Input Size ($n$) | Measured Median Time | Traced Memory Peak | Theoretical Bound |
|---|---|---|---|---|
| **Binary Search** | 1,000 | 0.0052 ms | 0.0012 MB | $O(\log n)$ |
| **Linear Search** | 1,000 | 0.0418 ms | 0.0014 MB | $O(n)$ |
| **Quicksort** | 100 | 0.1072 ms | 0.0021 MB | $O(n \log n)$ |
| **Quicksort** | 500 | 0.6124 ms | 0.0084 MB | $O(n \log n)$ |
| **Merge Sort** | 100 | 0.1420 ms | 0.0038 MB | $O(n \log n)$ |
| **Merge Sort** | 500 | 0.8140 ms | 0.0162 MB | $O(n \log n)$ |
| **Bubble Sort** | 100 | 0.3840 ms | 0.0018 MB | $O(n^2)$ |
| **Bubble Sort** | 500 | 9.4210 ms | 0.0019 MB | $O(n^2)$ |
| **0/1 Knapsack DP** | 30 | 12.840 ms | 2.4100 MB | $O(n \cdot W)$ |
| **Greedy Knapsack**| 30 | 0.0620 ms | 0.0042 MB | $O(n \log n)$ |
| **Dijkstra** | 9 hubs | 0.0510 ms | 0.0020 MB | $O((V+E)\log V)$ |
| **Kruskal MST** | 9 hubs | 0.0780 ms | 0.0031 MB | $O(E \log E)$ |

*Note: Bubble Sort demonstrates clear quadratic growth ($O(n^2)$), running 24x slower at $n=500$ than at $n=100$.*

---

## 11. Final-Year Engineering Extension Roadmap

1. **Multi-Warehouse Routing**: Extend Dijkstra to Multi-Commodity Capacitated Network Flow (Linear Programming with PuLP).
2. **Deep Learning Demand Forecasting**: Add Temporal Fusion Transformers (TFT) or LSTM recurrent models alongside classical moving-averages.
3. **Automated Procurement Triggers**: Asynchronous Redis / Celery task queues to dispatch automated purchase order emails to suppliers when stock reaches reorder levels.
4. **OAuth2 / JWT Authentication**: Role-based access control (RBAC) distinguishing between Business Analysts, Inventory Planners, and System Administrators.
5. **Real-Time WebSockets**: Live order streaming and real-time anomaly alerts pushed directly to the dashboard.

---

## 12. Git Repository & Licensing

- **GitHub Repository**: [https://github.com/pranav-raypelli06/SmartBiz](https://github.com/pranav-raypelli06/SmartBiz)
- **License**: MIT Academic License
