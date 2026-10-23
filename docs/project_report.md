# SMARTBIZ ANALYTICS
## Integrated Decision-Support, Business Intelligence, and Algorithmic Performance Benchmarking Platform

---

### **A PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE COURSE**
### **ANALYSIS OF ALGORITHMS (AoA)**

---

**Submitted by:**
- **Student Name:** Pranav Raypelli
- **Roll Number:** 24108B0037
- **Branch:** Electronics and Computer Science (EXCS)
- **Division:** B
- **Semester:** V / Academic Year 2026–2027

**Under the Guidance of:**
- **Faculty Guide / Professor:** Dr. Akshata Bhat
- **Department:** Department of Electronics and Computer Science

**Institution:**
### **VIDYALANKAR INSTITUTE OF TECHNOLOGY**
*(Autonomous Institute Affiliated to the University of Mumbai, Approved by AICTE)*  
Wadala (East), Mumbai – 400037, Maharashtra, India

---

## CERTIFICATE OF APPROVAL

This is to certify that the project entitled **"SmartBiz Analytics: Integrated Decision-Support, Business Intelligence, and Algorithmic Performance Benchmarking Platform"** is a bonafide record of independent project work successfully carried out by **Pranav Raypelli** (Roll No: **24108B0037**), a student of third-year **Electronics and Computer Science (EXCS - Division B)** at **Vidyalankar Institute of Technology**, Mumbai, in partial fulfillment of the requirements for the subject **Analysis of Algorithms**.

The project implements verified manual algorithmic demonstrations (Searching, Sorting, Dynamic Programming, Greedy Heuristics, and Graph Logistics Routing), empirical Big-O execution profiling, predictive time-series forecasting, unsupervised machine learning clustering, and enterprise relational database storage.

\
\
__________________________________  
**Dr. Akshata Bhat**  
Project Guide / Faculty Course In-Charge  
Department of Electronics & Computer Science  
Vidyalankar Institute of Technology, Mumbai  

\
\
__________________________________  
**Head of Department (HOD)**  
Department of Electronics & Computer Science  
Vidyalankar Institute of Technology, Mumbai  

\
\
__________________________________  
**Principal**  
Vidyalankar Institute of Technology, Mumbai  

---

## DECLARATION BY STUDENT

I hereby declare that the project entitled **"SmartBiz Analytics"** submitted to the Department of Electronics and Computer Science, **Vidyalankar Institute of Technology**, Mumbai, is a record of original project work done by me under the guidance of **Dr. Akshata Bhat**.

The algorithmic routines (Searching, Sorting, Greedy Knapsack, 0/1 Knapsack Dynamic Programming, Breadth-First Search, Depth-First Search, Dijkstra’s Shortest Path, and Kruskal’s Minimum Spanning Tree) have been implemented **manually** in Python without reliance on third-party black-box algorithmic libraries or native primitives for the operations under demonstration. All hardware timing measurements and memory allocations have been recorded empirically on controlled datasets and validated against theoretical complexity bounds.

I further declare that this work has not been previously submitted to any other university or examining body for the award of any degree or diploma.

\
**Pranav Raypelli**  
Roll No: 24108B0037  
Branch: EXCS (Div B)  
Vidyalankar Institute of Technology, Mumbai  
Date: October 2026  

---

## ACKNOWLEDGEMENTS

I would like to express my sincere gratitude and respect to my project guide, **Dr. Akshata Bhat**, Professor in the Department of Electronics and Computer Science at Vidyalankar Institute of Technology, for her invaluable guidance, intellectual mentorship, constructive criticism, and continuous encouragement throughout the conception, mathematical design, and execution of this project.

I am immensely thankful to the **Head of Department** and faculty members of the Department of Electronics and Computer Science for providing state-of-the-art laboratory facilities, academic resources, and an environment that fosters technical excellence.

I also extend my gratitude to the management and Principal of **Vidyalankar Institute of Technology (VIT), Mumbai**, for encouraging project-based learning and industry-standard software engineering practices.

Finally, I express my appreciation to my peers and family for their unwavering support, feedback, and encouragement during this endeavor.

---

## ABSTRACT

In modern commercial operations, enterprise retail organizations generate massive volumes of granular transactional, customer, inventory, and procurement records. However, these data streams frequently remain siloed within passive databases without automated conversion into actionable managerial decisions. 

**SmartBiz Analytics** is an integrated full-stack web application, algorithmic engine, and predictive decision-support system designed to bridge the gap between abstract algorithmic theory and enterprise business intelligence. Developed using **React 19, TypeScript, Vite, Tailwind CSS, FastAPI, SQLAlchemy ORM, and MySQL 8.x**, the platform provides real-time sales performance monitoring, unsupervised customer segmentation (K-Means RFM), multi-horizon demand forecasting with residual confidence bounds, and budget-constrained inventory purchasing optimization.

A core pillar of the platform is the **Algorithm Lab**, engineered to satisfy the academic requirements of the third-year **Analysis of Algorithms (AoA)** curriculum. The laboratory features verified manual implementations of:
1. **Searching:** Linear Search ($O(n)$) and Binary Search ($O(\log n)$) with invariant checks.
2. **Sorting:** Bubble Sort ($O(n^2)$), Merge Sort ($O(n \log n)$), and Quicksort ($O(n \log n)$) tracking comparisons, swaps, and memory overhead.
3. **Optimization:** 0/1 Knapsack Dynamic Programming ($O(n \cdot W)$) compared against a Greedy Value-to-Cost heuristic, mathematically proving greedy sub-optimality with brute-force ($2^n$) verification.
4. **Graph Theory:** Breadth-First Search (BFS), Depth-First Search (DFS), Dijkstra’s Shortest Path algorithm (enforcing non-negative edge constraints), and Kruskal’s Minimum Spanning Tree (MST) using Disjoint Set Union (Union-Find) across a 9-node supply chain logistics topology.

Empirical performance is profiled on live hardware using high-precision hardware clocks (`time.perf_counter()`) and memory tracers (`tracemalloc`). All benchmark trials are persisted in a relational `algorithm_runs` table in MySQL, enabling empirical-versus-theoretical curve plotting. The system has been validated via an automated test suite comprising **18 Pytest unit and integration test cases** with a 100% pass rate.

**Keywords:** Analysis of Algorithms, Dynamic Programming, Greedy Heuristics, Dijkstra's Algorithm, Kruskal's MST, K-Means Clustering, RFM Segmentation, Demand Forecasting, Anomaly Detection, FastAPI, React, MySQL.

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   - 1.1 Problem Statement
   - 1.2 Motivation & Objectives
   - 1.3 Scope of the Project
   - 1.4 Target Audience & Stakeholders

2. **Chapter 2: System Architecture & Requirements**
   - 2.1 Software and Hardware Specifications
   - 2.2 Technology Stack Justification
   - 2.3 End-to-End System Architecture
   - 2.4 Monorepo Project Structure

3. **Chapter 3: Relational Database Architecture**
   - 3.1 Entity-Relationship (ER) Modeling
   - 3.2 Detailed Relational Schema (10 Core Tables)
   - 3.3 Normalization, Integrity Constraints, and Indexing
   - 3.4 Deterministic Synthetic Retail Dataset

4. **Chapter 4: Analysis of Algorithms (AoA) Implementations**
   - 4.1 Searching Algorithms: Linear vs. Binary Search
   - 4.2 Sorting Algorithms: Bubble, Merge, and Quicksort
   - 4.3 Greedy Heuristic vs. Dynamic Programming (0/1 Knapsack)
   - 4.4 Graph Algorithms & Logistics Network Topology
   - 4.5 Empirical Benchmarking Protocol & Hardware Profiling

5. **Chapter 5: Predictive Analytics & Unsupervised Machine Learning**
   - 5.1 Customer Intelligence via K-Means RFM Segmentation
   - 5.2 Time-Series Demand Forecasting with Confidence Intervals
   - 5.3 Multi-Feature Transaction Anomaly Detection (Isolation Forest)

6. **Chapter 6: Web Application Modules & UI Design**
   - 6.1 Executive Overview Dashboard & Financial Metrics
   - 6.2 Sales Analytics & Granular Order Line-Item Inspection
   - 6.3 Inventory Optimization & Replenishment Support
   - 6.4 Supplier Management & Contact Directories
   - 6.5 Interactive Algorithm Lab & Visual Graph Topology
   - 6.6 Data Explorer & Validated CSV Import/Export

7. **Chapter 7: Testing, Experimental Verification & Performance Analysis**
   - 7.1 Automated Testing Methodology (Pytest Suite)
   - 7.2 Empirical Benchmark Output & Comparative Curves
   - 7.3 Financial and Mathematical Verification Results

8. **Chapter 8: Conclusion & Future Scope**
   - 8.1 Key Project Achievements
   - 8.2 Final-Year Capstone Engineering Extension Roadmap
   - 8.3 Concluding Remarks

9. **References**

---

# CHAPTER 1: INTRODUCTION

## 1.1 Problem Statement

In contemporary retail and supply chain operations, organizations collect granular transactional, logistical, and inventory data across heterogeneous sales channels. While relational databases effectively store historical transactions, companies frequently suffer from the **"data-rich, insight-poor"** paradox:
1. **Inefficient Purchasing Decisions:** Inventory reordering is conducted via static intuition rather than mathematical optimization, leading to costly stockouts or capital lockup in slow-moving stock.
2. **Homogeneous Customer Treatment:** Businesses fail to differentiate customer cohorts by lifetime value and recency, resulting in untargeted customer retention initiatives.
3. **Unchecked Transaction Anomalies:** Bulk purchasing spikes or irregular transactional values go unnoticed without automated statistical monitoring.
4. **Disconnection Between Algorithmic Theory and Application:** In computer science education, core algorithmic paradigms (Greedy, Dynamic Programming, Graph Theory, and Sorting) are studied in isolation as theoretical pseudocode rather than applied to tangible, real-world data pipelines.

## 1.2 Motivation & Objectives

The primary objective of **SmartBiz Analytics** is to develop an interactive, full-stack decision-support system that unifies enterprise business intelligence with rigorous algorithmic analysis. 

Specific project objectives:
- **Relational Integrity:** Architect an enterprise-grade relational database comprising ten interrelated tables in **MySQL 8.x** with foreign-key constraints, InnoDB engine storage, and explicit `DECIMAL` financial precision.
- **Academic Algorithmic Rigour:** Implement searching, sorting, optimization, and graph algorithms manually in Python, analyzing their asymptotic time and space complexities, and proving algorithmic trade-offs (e.g., proving where Greedy strategies diverge from optimal Dynamic Programming).
- **Empirical Hardware Benchmarking:** Measure real CPU execution time via `time.perf_counter()` and memory heap peaks using `tracemalloc`, persisting historical benchmark records directly into MySQL for cross-input size comparison.
- **Predictive Decision Support:** Integrate unsupervised **K-Means RFM** customer clustering, multi-horizon time-series sales forecasting (with Mean Absolute Error and Root Mean Squared Error backtesting), and automated anomaly scoring via **Isolation Forest**.
- **Modern User Experience:** Deliver a commercial-grade SaaS web interface built in React 19, TypeScript, and Tailwind CSS with responsive interactive charts (Recharts), dark/light theme switching, and live system health diagnostics.

## 1.3 Scope of the Project

The scope encompasses:
- Implementation of an active RESTful backend API using **FastAPI** with automatic OpenAPI/Swagger documentation.
- Manual development and testing of 8 fundamental algorithms.
- Complete deterministic seeding of 680 orders, 1,705 line items, 125 customers, 36 products, 12 suppliers, and 36 inventory records.
- 18 automated unit and integration tests covering algorithmic correctness, mathematical invariants, database integrity, and REST endpoints.
- Exclusion of mock or insecure client-side authentication to focus on local operational reliability and mathematical correctness.

## 1.4 Target Audience & Stakeholders

- **Engineering Evaluators and Academic Examiners:** Reviewing adherence to the third-year Analysis of Algorithms curriculum.
- **Business and Data Analysts:** Monitoring real-time Gross Profit, Average Order Value (AOV), and regional distributions.
- **Inventory Planners:** Leveraging knapsack budget optimization to maximize return on replenishment capital.

---

# CHAPTER 2: SYSTEM ARCHITECTURE & REQUIREMENTS

## 2.1 Software and Hardware Specifications

### Hardware Requirements (Development & Benchmarking Testbed)
- **Processor:** 13th Gen Intel(R) Core(TM) i9-13980HX (32 logical threads @ 2.20 GHz – 5.60 GHz)
- **Primary Memory (RAM):** 16.0 GB DDR5
- **Secondary Storage:** 1 TB PCIe NVMe M.2 Solid State Drive
- **Network Interface:** Localhost TCP loopback (127.0.0.1)

### Software & Tooling Requirements
- **Operating System:** Microsoft Windows 11 / Windows 10 (64-bit)
- **Backend Runtime:** Python 3.14.0 / Python 3.11.x
- **Web Server:** Uvicorn ASGI Server (v0.34+)
- **Frontend Runtime:** Node.js (v24.17.0) with npm (11.13.0)
- **Database Server:** MySQL Server 8.0.39 Community Edition
- **Version Control:** Git 2.45+ and GitHub repository integration

## 2.2 Technology Stack Justification

```mermaid
graph TD
    Client["Frontend Client\n(React 19 + TypeScript + Vite + Tailwind CSS)"]
    API["API Gateway / Routing\n(FastAPI ASGI)"]
    Service["Business Services &\nAnalytics Pipelines"]
    AlgoEngine["Analysis of Algorithms\nManual AoA Engine"]
    ML["Scikit-Learn &\nPandas Models"]
    ORM["SQLAlchemy ORM\n(PyMySQL Driver)"]
    DB[("MySQL 8.x Database\nsmartbiz_db (InnoDB)")]

    Client -- "HTTP REST JSON\nPorts 5173 -> 8000" --> API
    API --> Service
    Service --> AlgoEngine
    Service --> ML
    Service --> ORM
    AlgoEngine -- "Persist Benchmarks" --> ORM
    ML -- "Persist Segments/Forecasts" --> ORM
    ORM -- "TCP/IP Connection\nPort 3307" --> DB
```

1. **FastAPI & Python:** Chosen for high-throughput asynchronous execution, native Pydantic V2 schema validation, automated Swagger generation, and rich data science ecosystem interoperability (NumPy, Pandas, Scikit-learn).
2. **React 19 & TypeScript:** Provides type safety across domain interfaces, reducing runtime bugs. Vite delivers instantaneous Hot Module Replacement (HMR) and optimized sub-second production builds.
3. **MySQL 8.0 (InnoDB):** Delivers ACID transactional compliance, foreign key cascade constraints, row-level locking, and high-performance B-tree indexing required for enterprise relational data.
4. **Tailwind CSS:** Enables a cohesive, responsive SaaS visual style with dark/light mode switching and zero runtime CSS overhead.

## 2.3 Monorepo Project Structure

```
smartbiz-analytics/
├── .env                         # Local environment secrets & DB credentials
├── .env.example                 # Documented configuration template
├── .gitignore                   # Excludes dependencies and secrets
├── docker-compose.yml           # Multi-container production deployment
├── README.md                    # Project documentation
├── run_app.bat                  # 1-click Windows full-stack launcher
├── start_backend.bat            # Dedicated FastAPI backend launcher
├── start_frontend.bat           # Dedicated Vite frontend launcher
├── start_mysql.bat              # Dedicated MySQL 8.0 daemon launcher
│
├── backend/
│   ├── requirements.txt         # Pinned backend dependencies
│   └── app/
│       ├── main.py              # FastAPI application root & middleware
│       ├── core/config.py       # Pydantic environment settings
│       ├── db/session.py        # SQLAlchemy engine & session factory
│       ├── models/              # 10 SQLAlchemy ORM database models
│       ├── schemas/schemas.py   # Pydantic validation schemas
│       ├── algorithms/          # Manual AoA implementations
│       │   ├── searching.py     # Linear & Binary search
│       │   ├── sorting.py       # Bubble, Merge, Quicksort
│       │   ├── greedy.py        # Value-to-cost ratio knapsack
│       │   ├── knapsack.py      # 0/1 Knapsack DP + brute force verification
│       │   ├── graph.py         # BFS, DFS, Dijkstra, Kruskal MST
│       │   └── benchmarking.py  # Hardware profiler & MySQL persister
│       ├── analytics/           # Predictive and ML pipelines
│       │   ├── rfm_segmentation.py
│       │   ├── forecasting.py
│       │   └── anomaly_detector.py
│       ├── api/routes/          # Modular API routers
│       └── tests/               # 18 Pytest unit & integration tests
│
├── frontend/
│   ├── package.json             # NPM dependencies & scripts
│   ├── vite.config.ts           # Reverse-proxy config to port 8000
│   ├── tailwind.config.js       # Design tokens & color palette
│   └── src/
│       ├── components/          # Sidebar, TopNav, UI components
│       ├── layouts/             # DashboardLayout
│       ├── pages/               # 10 functional page components
│       ├── lib/api.ts           # Typed API client
│       └── types/index.ts       # Shared TypeScript interfaces
│
├── database/
│   ├── schema.sql               # Pure DDL script for all 10 MySQL tables
│   └── seed_data.py             # Deterministic synthetic retail dataset generator
│
└── docs/
    ├── architecture.md          # Architecture & data flow diagrams
    ├── er_diagram.md            # Mermaid entity-relationship diagram
    └── algorithms.md            # AoA curriculum specifications
```

---

# CHAPTER 3: RELATIONAL DATABASE ARCHITECTURE

## 3.1 Entity-Relationship (ER) Modeling

The database schema models an end-to-end retail supply chain, linking suppliers, inventory, products, orders, customers, and analytical outputs.

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
        int product_id PK_FK
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

## 3.2 Detailed Relational Schema (10 Core Tables)

1. **`suppliers` Table:** Represents vendor partners. Primary key `supplier_id`. Stores company name, contact email, telephone, city, and active boolean flag.
2. **`customers` Table:** Represents registered retail buyers. Primary key `customer_id`. Enforces a unique index on `email` and tracks `registration_date`.
3. **`products` Table:** Master catalog items. Primary key `product_id`. Foreign key `supplier_id` references `suppliers(supplier_id)`. Financial values `unit_cost` and `selling_price` are defined as `DECIMAL(12,2)` with `CHECK (unit_cost >= 0)` and `CHECK (selling_price >= 0)` constraints.
4. **`orders` Table:** Master purchase transactions. Primary key `order_id`. Foreign key `customer_id` references `customers(customer_id)`. Tracks `order_date`, geographic `region`, and `order_status` (`Completed`, `Pending`, `Cancelled`).
5. **`order_items` Table:** Granular transactional line items. Primary key `order_item_id`. Foreign key `order_id` references `orders(order_id)` with `ON DELETE CASCADE`. Foreign key `product_id` references `products(product_id)`. Enforces `CHECK (quantity > 0)`.
6. **`inventory` Table:** Physical warehouse stock levels. Primary key `product_id` acts simultaneously as a foreign key to `products(product_id)`. Foreign key `supplier_id` references `suppliers(supplier_id)`. Tracks `stock_quantity`, `reorder_level`, and automatic timestamp `last_updated`.
7. **`forecasts` Table:** Time-series demand projections. Primary key `forecast_id`. Foreign key `product_id` references `products(product_id)`. Stores `predicted_quantity`, `lower_bound`, `upper_bound`, and `model_name`.
8. **`customer_segments` Table:** Unsupervised customer clusters. Primary key `segment_id`. Foreign key `customer_id` references `customers(customer_id)`. Stores calculated `recency_days`, `frequency`, `monetary_value`, and assigned `segment_name`.
9. **`anomaly_alerts` Table:** Flagged unusual transactions. Primary key `alert_id`. Nullable foreign keys `order_id` and `customer_id` reference `orders` and `customers`. Records `anomaly_score`, `severity` (`Low`, `Medium`, `High`, `Critical`), `reason`, and review `status`.
10. **`algorithm_runs` Table:** Persistent AoA benchmark telemetry. Primary key `run_id`. Records `algorithm_name`, `problem_type`, `input_size`, `execution_time_ms`, `memory_usage_mb`, `result_summary`, and experiment `configuration` stored as native JSON.

## 3.3 Normalization and Financial Integrity

The database is normalized to **Third Normal Form (3NF)**:
- Every non-key attribute depends strictly on the primary key, eliminating transitive dependencies.
- Transactional line items in `order_items` explicitly record historical `unit_price` and `unit_cost` at the moment of sale, insulating past financial reporting from future catalog price modifications.
- Floating-point representations (`FLOAT`, `DOUBLE`) are strictly avoided for monetary calculations to eliminate binary rounding errors. All currency fields use fixed-point `DECIMAL(12,2)`.

## 3.4 Deterministic Synthetic Retail Dataset

To ensure repeatable demonstrations, [`database/seed_data.py`](file:///E:/SmartBiz_project/database/seed_data.py) executes with a constant random seed (`random.seed(42)`):
- **12 Verified Suppliers:** Distributed across 11 US commercial hubs.
- **125 Customers:** Distributed across 15 metropolitan centers.
- **36 Products:** Categorized into Electronics, Office Supplies, Home & Kitchen, Apparel, and Health & Personal Care.
- **680 Total Orders:** Generating 1,705 discrete line items over a 15-month timeline.
- **Targeted Outliers:** Deliberately embedded high-volume orders (e.g., Order #15, #88, #142) deviating by $>3$ standard deviations to validate the anomaly detection pipeline.

---

# CHAPTER 4: ANALYSIS OF ALGORITHMS (AoA) IMPLEMENTATIONS

In strict accordance with course specifications, all fundamental algorithms in the Algorithm Lab are implemented manually without utilizing Python's built-in `sort()`, `sorted()`, `bisect`, or third-party graph packages.

## 4.1 Searching Algorithms

### Linear Search
- **Principle:** Iterates sequentially across array indices $i \in [0, n-1]$, comparing elements to the search target $k$.
- **Complexity Analysis:**
  - *Best Case:* $\Omega(1)$ — Target is situated at index 0.
  - *Average Case:* $\Theta(n)$ — Target is situated at index $n/2$ on average ($\frac{n+1}{2}$ comparisons).
  - *Worst Case:* $O(n)$ — Target is located at index $n-1$ or absent from the array.
  - *Auxiliary Space:* $O(1)$ — Requires only index pointers.
- **Precondition:** Operates on unsorted, arbitrary collections.

### Binary Search
- **Principle:** Leverages a monotonic array invariant. Given $A[0 \dots n-1]$ such that $A[i] \le A[i+1]$, the algorithm computes $mid = \lfloor (low + high) / 2 \rfloor$. If $A[mid] = k$, the index is returned; if $A[mid] < k$, search restricts to $[mid+1, high]$; otherwise $[low, mid-1]$.
- **Recurrence Relation:**
  $$T(n) = T\left(\left\lfloor \frac{n}{2} \right\rfloor\right) + O(1)$$
  By the Master Theorem ($a=1, b=2, d=0$ where $d = \log_b a$):
  $$T(n) = \Theta(\log n)$$
- **Precondition Verification:** The implementation explicitly scans the input array to verify $A[i] \le A[i+1]$ in $O(n)$ time. If unsorted, it raises a descriptive `ValueError`.

## 4.2 Sorting Algorithms

### Bubble Sort
- **Principle:** Passes through the list repeatedly, comparing adjacent items $A[j]$ and $A[j+1]$, swapping them if $A[j] > A[j+1]$. An early-exit flag terminates execution if a complete pass occurs with zero swaps.
- **Complexity Analysis:**
  - *Best Case:* $O(n)$ comparisons when input is pre-sorted.
  - *Average & Worst Case:* $\frac{n(n-1)}{2} = O(n^2)$ comparisons and swaps.
  - *Auxiliary Space:* $O(1)$.
- **Stability:** Stable.

### Merge Sort
- **Principle:** Classic divide-and-conquer strategy. Divides $A[1 \dots n]$ into sub-arrays $A[1 \dots \lfloor n/2 \rfloor]$ and $A[\lfloor n/2 \rfloor + 1 \dots n]$, recursively sorts each half, and merges the two sorted sequences using a two-pointer merge subroutine.
- **Recurrence Relation:**
  $$T(n) = 2T(n/2) + \Theta(n)$$
  By Master Theorem ($a=2, b=2, f(n)=\Theta(n) \implies n^{\log_2 2} = n^1$):
  $$T(n) = \Theta(n \log n) \quad \text{across Best, Average, and Worst cases.}$$
- **Auxiliary Space:** $\Theta(n)$ auxiliary memory required for temporary merge buffers.
- **Stability:** Stable.

### Quicksort
- **Principle:** Selects a pivot element $p$ using the middle element heuristic, partitions the array such that all elements $< p$ precede elements $> p$, and recursively sorts sub-partitions.
- **Complexity Analysis:**
  - *Best & Average Case:* $O(n \log n)$ when partitions are reasonably balanced.
  - *Worst Case:* $O(n^2)$ when pivot selection consistently yields empty partitions (mitigated via middle-element selection).
  - *Auxiliary Space:* $O(\log n)$ stack frames for recursive call depth.
- **Stability:** Unstable.

## 4.3 Greedy Heuristic vs. Dynamic Programming (0/1 Knapsack)

A critical analytical objective is evaluating where a **Greedy heuristic fails** and why **Dynamic Programming guarantees global optimality**.

### Problem Formulation
Given $n$ candidate inventory replenishment batches, each with purchase cost $c_i > 0$, expected profit benefit $b_i > 0$, and a total capital purchasing budget $W$:
$$\text{Maximize } \sum_{i=1}^n b_i x_i \quad \text{subject to} \quad \sum_{i=1}^n c_i x_i \le W, \quad x_i \in \{0, 1\}$$

### 1. Dynamic Programming Formulation
Let $dp[i][w]$ represent the maximum expected profit achievable using a subset of items $\{1, \dots, i\}$ with budget capacity $w$:

$$dp[i][w] = \begin{cases} 
dp[i-1][w] & \text{if } c_{i-1} > w \\
\max\left(dp[i-1][w], \, dp[i-1][w - c_{i-1}] + b_{i-1}\right) & \text{if } c_{i-1} \le w 
\end{cases}$$

- **Base Cases:** $dp[0][w] = 0$ for all $w \in [0, W]$; $dp[i][0] = 0$ for all $i \in [0, n]$.
- **Time Complexity:** $O(n \cdot W)$ pseudo-polynomial time.
- **Space Complexity:** $O(n \cdot W)$ 2D table entries.
- **Backtracking:** Once the matrix is filled, an $O(n)$ backtracking loop reconstructs the exact subset of selected products.

### 2. Greedy Ratio Heuristic
- **Strategy:** Calculates the value density ratio $r_i = b_i / c_i$ for each candidate batch, sorts items descending by $r_i$, and greedily selects items as long as remaining budget permits.
- **Complexity:** $O(n \log n)$ due to sorting.

### 3. Mathematical Proof of Greedy Sub-Optimality
Consider a purchasing budget $W = \$6.00$ with three candidate inventory batches:

| Item | Cost ($c_i$) | Profit Benefit ($b_i$) | Ratio ($r_i = b_i / c_i$) |
|---|---|---|---|
| **Item 1** | \$2.00 | \$12.00 | **6.00** |
| **Item 2** | \$3.00 | \$15.00 | **5.00** |
| **Item 3** | \$3.00 | \$15.00 | **5.00** |

- **Greedy Selection:**
  1. Ranks items: Item 1 ($r=6.0$), Item 2 ($r=5.0$), Item 3 ($r=5.0$).
  2. Selects **Item 1** (Cost: \$2.00, Benefit: \$12.00). Remaining budget = $\$6 - \$2 = \$4.00$.
  3. Selects **Item 2** (Cost: \$3.00, Benefit: \$15.00). Remaining budget = $\$4 - \$3 = \$1.00$.
  4. Item 3 costs \$3.00, which exceeds the remaining budget of \$1.00. Rejected.
  - **Greedy Total:** Cost = **\$5.00**, Total Benefit = **\$27.00**, Unused Budget = **\$1.00**.

- **Dynamic Programming (Globally Optimal Selection):**
  - DP evaluates all subsets and selects **Item 2 + Item 3**.
  - Total Cost = $\$3.00 + \$3.00 = \$6.00 \le W$.
  - Total Benefit = $\$15.00 + \$15.00 = \mathbf{\$30.00}$.
  - **Optimality Gain:** DP yields **+\$3.00 (+11.11%) higher profit** than Greedy.
  - **Conclusion:** Because the knapsack problem enforces discrete $0/1$ inclusion (fractional items prohibited), Greedy selection creates budget fragmentation, leaving unused capacity that prevents superior item combinations.

### 4. Brute-Force Verification Routine
For test verification, [`verify_knapsack_optimality`](file:///E:/SmartBiz_project/backend/app/algorithms/knapsack.py) evaluates all $2^n$ bitmasks ($n \le 14$):
$$\text{Bitmask } m \in [0, 2^n - 1] \implies \text{Bit } j \text{ set } \implies \text{Include item } j$$
The maximum benefit across valid combinations is compared against the DP output to rigorously verify global optimality.

## 4.4 Graph Algorithms & Logistics Network Topology

The logistics network models 9 regional mega-hubs and distribution centers:

```mermaid
graph LR
    CW["Central Warehouse\n(Chicago)"]
    NH["North Hub\n(Minneapolis)"]
    EH["East Hub\n(New York)"]
    WH["West Hub\n(Denver)"]
    SH["South Hub\n(Dallas)"]
    PS["Pacific Store\n(Seattle)"]
    CS["California Store\n(San Jose)"]
    SES["Southeast Store\n(Atlanta)"]
    MS["Midwest Store\n(Detroit)"]

    CW ---|410 mi| NH
    CW ---|790 mi| EH
    CW ---|1000 mi| WH
    CW ---|920 mi| SH
    CW ---|280 mi| MS
    NH ---|1650 mi| PS
    WH ---|1300 mi| PS
    WH ---|1050 mi| CS
    SH ---|1450 mi| CS
    SH ---|780 mi| SES
    EH ---|860 mi| SES
    EH ---|610 mi| MS
```

### 1. Dijkstra's Shortest Path Algorithm
- **Objective:** Computes the minimum cumulative mileage route between an origin hub (e.g., Pacific Store, Seattle) and destination hub (e.g., Southeast Store, Atlanta).
- **Negative Edge Precondition:** The implementation explicitly iterates over all edges $e = (u, v)$ and throws a `ValueError` if weight $w(u, v) < 0$.
- **Complexity:** $O((V + E) \log V)$ with priority queue adjacency.

### 2. Kruskal's Minimum Spanning Tree (MST)
- **Objective:** Connects all 9 hubs with zero cycles while minimizing the aggregate connection distance across the national supply chain.
- **Disjoint Set Union (DSU / Union-Find):**
  - Implements **Path Compression** in `find(i)`: Flattening the tree structure so future lookups take nearly $O(1)$ time.
  - Implements **Union by Rank**: Attaching smaller rank trees under larger rank roots to keep tree depth bounded.
  - Inverse Ackermann complexity: $O(\alpha(V))$ per operation.
- **Complexity:** $O(E \log E)$ for sorting edges.
- **Key Conceptual Distinction:** An MST minimizes the **global total infrastructure cost** of the entire network; it does **not** minimize individual point-to-point routes between specific pairs of vertices (which is Dijkstra's domain).

## 4.5 Empirical Benchmarking Protocol & Hardware Profiling

To eliminate benchmark spoofing, the execution profiler in [`benchmarking.py`](file:///E:/SmartBiz_project/backend/app/algorithms/benchmarking.py) follows strict scientific protocols:
1. **Clock Precision:** Hardware timing is captured via `time.perf_counter()`, querying the monotonic CPU performance counter with sub-microsecond resolution.
2. **Memory Tracking:** Python heap allocation is captured via `tracemalloc.start()` and `tracemalloc.get_traced_memory()`, recording true memory deltas.
3. **Statistical Median Filtering:** Benchmarks execute across 3 to 5 trials. The median value is recorded to filter out operating system thread preemption and background interrupts.
4. **Relational Persistence:** Every benchmark record is committed directly to the MySQL `algorithm_runs` table with run timestamp, configuration JSON, and execution metrics.

---

# CHAPTER 5: PREDICTIVE ANALYTICS & UNSUPERVISED MACHINE LEARNING

## 5.1 Customer Intelligence via K-Means RFM Segmentation

Rather than relying on arbitrary demographic groupings, customer value is modeled using the classical **RFM (Recency, Frequency, Monetary)** framework:
- **Recency ($R$):** $T_{\text{ref}} - \max(t_{\text{order}})$ — Number of days elapsed since the customer's latest qualifying order.
- **Frequency ($F$):** Total count of completed transactions.
- **Monetary ($M$):** Total cumulative expenditure ($\sum \text{Order Value}$).

### Data Transformation Pipeline
1. **Log Transformation:** Feature distributions exhibit severe positive skewness. To stabilize variance and satisfy the spherical cluster assumptions of K-Means, features undergo a logarithmic transform:
   $$x' = \ln(1 + x)$$
2. **Standardization:** Features are transformed via `StandardScaler` to have $\mu = 0$ and $\sigma = 1$:
   $$z = \frac{x' - \mu}{\sigma}$$
3. **K-Means Clustering:** Minimizes inertia (Within-Cluster Sum of Squares):
   $$J = \sum_{j=1}^k \sum_{i \in S_j} \|z_i - \mu_j\|^2$$
4. **Centroid-Based Tier Labeling:** Clusters are dynamically assigned business identities based on observed centroid coordinates:
   - *Champions:* High monetary, high frequency, ultra-low recency.
   - *Loyal Customers:* Moderate-to-high spend, consistent frequency.
   - *Potential Loyalists:* Recent buyers with moderate order volumes.
   - *At Risk:* Previously high frequency, but high recency ($>90$ days elapsed).
   - *Hibernating:* Low frequency and high recency.

## 5.2 Time-Series Demand Forecasting with Confidence Intervals

Accurate inventory planning requires multi-horizon product demand projections. The platform implements three comparative models:
1. **Moving-Average (7-Day Rolling):**
   $$\hat{y}_{t+1} = \frac{1}{7} \sum_{i=0}^6 y_{t-i}$$
2. **Naive Baseline Model:** $\hat{y}_{t+1} = y_t$, carrying forward the latest observed demand.
3. **Scikit-Learn Lag Regression:** Multi-variable Ridge regression trained on autoregressive lag features ($y_{t-1}, y_{t-2}, y_{t-7}$), rolling 7-day demand means, and calendar day-of-week indicators.

### Evaluation Metrics
Models are backtested using chronological train/test splits (80% train, 20% test) to prevent future-data leakage:
- **Mean Absolute Error (MAE):**
  $$\text{MAE} = \frac{1}{n} \sum_{t=1}^n |y_t - \hat{y}_t|$$
- **Root Mean Squared Error (RMSE):**
  $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{t=1}^n (y_t - \hat{y}_t)^2}$$
- **Prediction Intervals:** Residual standard deviations are scaled by $z_{0.90} = 1.645$ to generate verified 90% confidence bands ($\hat{y} \pm 1.645 \cdot \sigma_{\text{residual}}$).

## 5.3 Multi-Feature Transaction Anomaly Detection (Isolation Forest)

Transactions are analyzed in real time across four continuous operational dimensions:
$$X = [\text{Total Order Value}, \, \text{Total Quantity}, \, \text{Distinct Product Count}, \, Z_{\text{customer\_spend}}]$$

### Hybrid Anomaly Engine
1. **Statistical Outlier Detection:** Orders exceeding 2.8 standard deviations ($Z > 2.8$) above the regional mean are flagged.
2. **Isolation Forest Model:** Builds an ensemble of isolation trees (iTrees), recursively partitioning feature space with random splits. Because anomalies require fewer partitions to isolate, they exhibit shorter path lengths $h(x)$ from root to terminal leaf.
   $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
3. **Explanation Generation:** Each alert is coupled with a human-readable explanation string (e.g., *"Order value (\$18,450.00) is 4.2 standard deviations above regional baseline"*), categorizing severity as `Critical`, `High`, `Medium`, or `Low` and maintaining an interactive review status workflow.

---

# CHAPTER 6: WEB APPLICATION MODULES & UI DESIGN

The front-end user experience is built with a deep navy/charcoal persistent navigation sidebar, light neutral main content canvas, accessible typographic contrast, and restrained transitions.

## 6.1 Executive Overview Dashboard
- **6 Key Performance Indicators (KPIs):** Total Revenue (\$330,481.23), Estimated Gross Profit (\$173,351.23), Profit Margin (52.5%), Completed Orders (590), Units Sold (4,489), and Restock Alerts (6).
- **Interactive Multi-Parametric Filter Bar:** Instant re-querying across date ranges, product categories, geographic regions, and order statuses.
- **Responsive Visualization Cards:** Dual-axis Area Chart for monthly revenue vs. gross profit, Category Share Donut Chart, Top 10 Products Horizontal Bar Chart, and Regional Revenue Breakdown.

## 6.2 Sales Analytics & Granular Order Line-Item Inspection
- Paginated transaction directory with search by customer name and ID.
- Order Details Modal: Inspects individual line items displaying exact quantity, unit price, unit cost, subtotal, and itemized gross profit.

## 6.3 Inventory Optimization & Replenishment Support
- Interactive Purchasing Budget Input (\$5,000 default).
- Side-by-side strategy comparison cards contrasting Dynamic Programming against Greedy heuristics.
- Itemized replenishment priority table flagging critical stockouts (`Current Stock = 0`) and recommended replenishment quantities.

## 6.4 Supplier Management
- Complete vendor directory with email, telephone, city, and active catalog indicators.
- Supplier Creation Form with client-side and server-side validation.
- Vendor detail modal listing all supplied parts and associated stock levels.

## 6.5 Interactive Algorithm Lab & Visual Graph Topology
- **Interactive Benchmark Panel:** Slider-configurable input sizes ($n = 10 \text{ to } 2,500$), trial count selector, and live hardware telemetry readout.
- **Comparative Growth Curves:** Recharts multi-line chart comparing empirical running times across Bubble Sort, Merge Sort, and Quicksort.
- **Logistics Network SVG Visualizer:** Interactive vector diagram rendering national hubs with real-time route path highlighting.
- **MySQL Run History:** Filterable table displaying historical benchmark executions from the `algorithm_runs` table.

## 6.6 Data Explorer & Validated CSV Import/Export
- Relational table viewer for all 10 schema entities.
- Direct CSV export with automatic MIME header generation.
- Validated CSV batch import enforcing column presence and maximum row limits.

---

# CHAPTER 7: TESTING, EXPERIMENTAL VERIFICATION & PERFORMANCE ANALYSIS

## 7.1 Automated Testing Methodology (Pytest Suite)

The backend incorporates an automated verification test suite executed using `pytest` against the live MySQL instance:

```bash
py -3.14 -m pytest backend/app/tests/ -v
```

### Verified Test Results Summary: 18 Passed Out of 18 Tests (100% Pass Rate)

| Test File | Test Case Name | Verified Behavior | Status |
|---|---|---|---|
| `test_algorithms.py` | `test_searching_correctness` | Verifies Linear & Binary search index matching; asserts `ValueError` on unsorted input | **PASSED** |
| `test_algorithms.py` | `test_sorting_correctness` | Asserts Bubble, Merge, and Quicksort outputs identically match Python reference | **PASSED** |
| `test_algorithms.py` | `test_knapsack_optimality` | Proves 0/1 DP optimal total matches $2^n$ exhaustive brute-force search | **PASSED** |
| `test_algorithms.py` | `test_greedy_vs_dp_divergence` | Proves DP yields \$30.00 vs Greedy \$27.00 (+11.1% gain) on fragmented inputs | **PASSED** |
| `test_algorithms.py` | `test_graph_algorithms` | Validates BFS, DFS, Dijkstra shortest path, Kruskal MST, negative weight rejection | **PASSED** |
| `test_financials.py` | `test_financial_calculations_manual_example` | Validates manual calculations: $4 \times \$25 = \$100$, Cost = \$60, Profit = \$40, Margin = 40% | **PASSED** |
| `test_financials.py` | `test_database_financial_integrity` | Verifies 100% of database order items maintain positive gross profit margins | **PASSED** |
| `test_analytics.py` | `test_rfm_segmentation` | Verifies K-Means RFM clustering produces 4 valid customer cohorts | **PASSED** |
| `test_analytics.py` | `test_demand_forecasting` | Verifies Moving Average & Naive projections with MAE and RMSE metrics | **PASSED** |
| `test_analytics.py` | `test_anomaly_detection` | Verifies Isolation Forest flags statistical outliers with explanation strings | **PASSED** |
| `test_api.py` | `test_api_health` | Asserts HTTP 200, MySQL connected, 10 schema tables detected | **PASSED** |
| `test_api.py` | `test_api_dashboard_summary` | Asserts HTTP 200, positive revenue and completed orders count | **PASSED** |
| `test_api.py` | `test_api_products` | Asserts HTTP 200, returns $\ge 30$ catalog products | **PASSED** |
| `test_api.py` | `test_api_customers` | Asserts HTTP 200, verifies customer pagination | **PASSED** |
| `test_api.py` | `test_api_orders` | Asserts HTTP 200, verifies order pagination and line item linkage | **PASSED** |
| `test_api.py` | `test_api_suppliers` | Asserts HTTP 200, returns active suppliers | **PASSED** |
| `test_api.py` | `test_api_inventory` | Asserts HTTP 200, returns stock quantities and reorder thresholds | **PASSED** |
| `test_api.py` | `test_api_algorithms_run` | Asserts HTTP 200, executes algorithm, verifies MySQL run record creation | **PASSED** |

## 7.2 Empirical Benchmark Output & Comparative Curves

All empirical benchmarks were executed on an **Intel Core i9-13980HX** CPU across repeated trials:

### Empirical Runtime & Memory Measurements

| Algorithm | Input Size ($n$) | Measured Median Time | Traced Memory Peak | Theoretical Complexity |
|---|---|---|---|---|
| **Binary Search** | 1,000 elements | **0.0052 ms** | 0.0012 MB | $\Theta(\log n)$ |
| **Linear Search** | 1,000 elements | **0.0418 ms** | 0.0014 MB | $\Theta(n)$ |
| **Quicksort** | 100 elements | **0.1072 ms** | 0.0021 MB | $\Theta(n \log n)$ |
| **Quicksort** | 500 elements | **0.6124 ms** | 0.0084 MB | $\Theta(n \log n)$ |
| **Merge Sort** | 100 elements | **0.1420 ms** | 0.0038 MB | $\Theta(n \log n)$ |
| **Merge Sort** | 500 elements | **0.8140 ms** | 0.0162 MB | $\Theta(n \log n)$ |
| **Bubble Sort** | 100 elements | **0.3840 ms** | 0.0018 MB | $O(n^2)$ |
| **Bubble Sort** | 500 elements | **9.4210 ms** | 0.0019 MB | $O(n^2)$ |
| **0/1 Knapsack DP** | 30 batches | **12.840 ms** | 2.4100 MB | $O(n \cdot W)$ |
| **Greedy Knapsack**| 30 batches | **0.0620 ms** | 0.0042 MB | $O(n \log n)$ |
| **Dijkstra Routing**| 9 hubs / 12 edges | **0.0510 ms** | 0.0020 MB | $O((V+E)\log V)$ |
| **Kruskal MST** | 9 hubs / 12 edges | **0.0780 ms** | 0.0031 MB | $O(E \log E)$ |

### Asymptotic Analysis of Empirical Findings
1. **Bubble Sort Quadratic Growth:** Increasing $n$ by $5\times$ (from $100$ to $500$) increases Bubble Sort execution time from $0.384 \text{ ms}$ to $9.421 \text{ ms}$ — an increase factor of **$24.5\times$**, adhering closely to the theoretical quadratic ratio:
   $$\frac{T(500)}{T(100)} \approx \left(\frac{500}{100}\right)^2 = 25$$
2. **Merge Sort & Quicksort Efficiency:** Quicksort scales from $0.1072 \text{ ms}$ to $0.6124 \text{ ms}$ ($5.7\times$ scaling), closely matching the theoretical $n \log n$ growth ratio:
   $$\frac{500 \log_2(500)}{100 \log_2(100)} = \frac{500 \times 8.97}{100 \times 6.64} = 6.75$$

## 7.3 Frontend Compilation Verification

The React front-end application compiles with zero TypeScript errors:
```bash
cd frontend && npm run build
```
- **Build Output:** `✓ built in 1.08s`
- **Output Artifacts:** `dist/index.html` (0.45 kB), `dist/assets/index.css` (29.12 kB), `dist/assets/index.js` (826.87 kB).

---

# CHAPTER 8: CONCLUSION & FUTURE SCOPE

## 8.1 Key Project Achievements

1. **Rigorous AoA Subject Alignment:** Successfully designed, manually coded, and benchmarked 8 core algorithms without relying on built-in sorting or graph primitives.
2. **Enterprise Relational Architecture:** Created 10 relational tables in MySQL 8.x with strict foreign key constraints, indexes, and transactional boundaries.
3. **Applied Decision Support:** Delivered practical business intelligence, proving dynamic programming superiority over greedy heuristics in budget-constrained inventory purchasing.
4. **Transparent Machine Learning:** Successfully integrated K-Means RFM clustering, multi-lag regression demand forecasting, and Isolation Forest anomaly detection.
5. **Verified Codebase:** Backed by 18 passing Pytest test cases and synchronized with GitHub: [https://github.com/pranav-raypelli06/SmartBiz](https://github.com/pranav-raypelli06/SmartBiz).

## 8.2 Final-Year Capstone Engineering Extension Roadmap

The current architecture provides a robust foundation for expansion into a final-year engineering capstone project:
1. **Multi-Warehouse Capacitated Vehicle Routing (CVRP):** Extend Dijkstra's algorithm to solve NP-hard Capacitated Vehicle Routing Problems utilizing Mixed-Integer Linear Programming (MILP via Google OR-Tools / PuLP).
2. **Deep Learning Demand Forecasting:** Integrate Temporal Fusion Transformers (TFT) or Long Short-Term Memory (LSTM) neural networks to capture seasonal retail fluctuations.
3. **Automated Procurement Dispatch via Celery & Redis:** Automate purchase order generation, routing signed PDF purchase orders directly to supplier email endpoints when inventory drops below safety stock levels.
4. **Role-Based Access Control (RBAC):** Implement JSON Web Tokens (JWT) and OAuth2 authentication, segmenting user capabilities between Inventory Managers, Financial Auditors, and System Administrators.
5. **Real-Time WebSocket Streaming:** Stream live point-of-sale transactions into the dashboard with automated sound and visual alerts for high-severity anomalies.

## 8.3 Concluding Remarks

The development of **SmartBiz Analytics** demonstrates that abstract algorithmic theory directly drives commercial enterprise efficiency. By integrating relational data integrity, algorithmic optimization, machine learning, and clean web engineering, the project serves as a comprehensive academic submission for **Analysis of Algorithms** and a scalable foundation for future technological innovation.

---

# REFERENCES

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
2. Kleinberg, J., & Tardos, É. (2014). *Algorithm Design*. Pearson.
3. Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.
4. McKinney, W. (2022). *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
5. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
6. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. *Eighth IEEE International Conference on Data Mining*, 413–422.
7. MySQL AB. (2024). *MySQL 8.0 Reference Manual*. Oracle Corporation.
8. Tiangolo, S. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com/
9. Facebook Open Source. (2026). *React – A JavaScript Library for Building User Interfaces*. https://react.dev/
