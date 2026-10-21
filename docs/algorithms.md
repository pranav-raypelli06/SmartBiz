# SmartBiz Analytics: Analysis of Algorithms (AoA) Curriculum Guide

This document details the manual algorithmic implementations in SmartBiz Analytics, their theoretical asymptotic complexities, invariants, and empirical benchmarking methodology.

## 1. Searching Algorithms

### Linear Search
- **Implementation**: [`linear_search`](file:///E:/SmartBiz_project/backend/app/algorithms/searching.py)
- **Mechanism**: Sequentially inspects each index $i \in [0, n-1]$.
- **Complexities**:
  - Best Case: $O(1)$ (target located at index 0)
  - Average Case: $O(n)$
  - Worst Case: $O(n)$ (target at index $n-1$ or absent)
  - Auxiliary Space: $O(1)$
- **Precondition**: Operates on arbitrary unordered lists.

### Binary Search
- **Implementation**: [`binary_search`](file:///E:/SmartBiz_project/backend/app/algorithms/searching.py)
- **Mechanism**: Maintains interval $[low, high]$; queries midpoint $mid = \lfloor (low + high) / 2 \rfloor$ and halves the search space iteratively.
- **Complexities**:
  - Best Case: $O(1)$ (target at middle element)
  - Average Case: $O(\log n)$
  - Worst Case: $O(\log n)$
  - Auxiliary Space: $O(1)$ (iterative)
- **Precondition**: Strictly requires monotonic sorted order. The implementation verifies $arr[i] \le arr[i+1]$ and raises a descriptive `ValueError` on unsorted inputs.

---

## 2. Sorting Algorithms

### Bubble Sort
- **Implementation**: [`bubble_sort`](file:///E:/SmartBiz_project/backend/app/algorithms/sorting.py)
- **Mechanism**: Repeatedly compares adjacent pairs $(a_j, a_{j+1})$ and swaps out-of-order elements with an early-exit flag.
- **Complexities**:
  - Best Case: $O(n)$ (already sorted with early termination)
  - Average Case: $O(n^2)$
  - Worst Case: $O(n^2)$ (reverse ordered)
  - Auxiliary Space: $O(1)$
- **Stability**: Stable.

### Merge Sort
- **Implementation**: [`merge_sort`](file:///E:/SmartBiz_project/backend/app/algorithms/sorting.py)
- **Mechanism**: Divide-and-conquer strategy recursively bisecting arrays into halves, sorting each sublist, and merging in linear time.
- **Recurrence**: $T(n) = 2T(n/2) + O(n) \implies O(n \log n)$ by Master Theorem.
- **Complexities**:
  - Best / Average / Worst: $O(n \log n)$
  - Auxiliary Space: $O(n)$ (temporary merged buffer)
- **Stability**: Stable.

### Quicksort
- **Implementation**: [`quicksort`](file:///E:/SmartBiz_project/backend/app/algorithms/sorting.py)
- **Mechanism**: Divide-and-conquer partitioning using a median-of-three/middle pivot to prevent quadratic degradation on sorted data.
- **Complexities**:
  - Best Case: $O(n \log n)$ (balanced partitions)
  - Average Case: $O(n \log n)$
  - Worst Case: $O(n^2)$ (extremely unbalanced partitions)
  - Space: $O(\log n)$ call stack frames
- **Stability**: Unstable.

---

## 3. Dynamic Programming vs. Greedy Optimization

### 0/1 Knapsack (Dynamic Programming)
- **Implementation**: [`dp_knapsack`](file:///E:/SmartBiz_project/backend/app/algorithms/knapsack.py)
- **Problem Formulation**:
  Given $n$ candidate inventory batches with costs $c_i \in \mathbb{N}$ and expected profits $b_i > 0$, maximize:
  $$\max \sum_{i=1}^n b_i x_i \quad \text{subject to} \quad \sum_{i=1}^n c_i x_i \le W, \quad x_i \in \{0, 1\}$$
- **Recurrence**:
  $$dp[i][w] = \max(dp[i-1][w], dp[i-1][w - c_{i-1}] + b_{i-1}) \quad \text{if } c_{i-1} \le w$$
- **Complexity**: $O(n \cdot W)$ pseudo-polynomial time and $O(n \cdot W)$ space.
- **Formal Verification**: The implementation includes [`verify_knapsack_optimality`](file:///E:/SmartBiz_project/backend/app/algorithms/knapsack.py) executing an exhaustive $2^n$ bitmask search on small inputs ($n \le 14$) to prove mathematical optimality.

### Greedy Heuristic (Ratio Strategy)
- **Implementation**: [`greedy_knapsack`](file:///E:/SmartBiz_project/backend/app/algorithms/greedy.py)
- **Mechanism**: Sorts candidates descending by density ratio $r_i = b_i / c_i$; admits items sequentially while remaining budget permits.
- **Sub-optimality Proof**:
  Consider budget $W=6$, items:
  - Item 1: Cost 2, Benefit 12 (Ratio 6.0)
  - Item 2: Cost 3, Benefit 15 (Ratio 5.0)
  - Item 3: Cost 3, Benefit 15 (Ratio 5.0)
  Greedy selects Item 1, remaining budget 4; then selects Item 2, remaining budget 1. Total benefit = $12 + 15 = 27$ (Cost 5).
  Optimal DP selects Item 2 + Item 3. Total benefit = $15 + 15 = 30$ (Cost 6).
  DP achieves **+11.1% higher profit** than greedy selection.

---

## 4. Graph Theory & Logistics Routing

### Breadth-First Search (BFS)
- **Implementation**: [`bfs`](file:///E:/SmartBiz_project/backend/app/algorithms/graph.py)
- **Complexity**: $O(V + E)$ time, $O(V)$ space.
- **Property**: Discovers hubs in increasing order of unweighted edge hops from Central Warehouse.

### Depth-First Search (DFS)
- **Implementation**: [`dfs`](file:///E:/SmartBiz_project/backend/app/algorithms/graph.py)
- **Complexity**: $O(V + E)$ time, $O(V)$ space.
- **Property**: Explores maximum tree depth along branch paths before backtracking.

### Dijkstra's Shortest Path
- **Implementation**: [`dijkstra_shortest_path`](file:///E:/SmartBiz_project/backend/app/algorithms/graph.py)
- **Precondition**: Strictly rejects negative edge weights ($w_{uv} \ge 0$).
- **Complexity**: $O((V + E) \log V)$ time, $O(V)$ space.
- **Application**: Computes least-cost logistics transit routes between retail outlets and regional mega-hubs.

### Kruskal's Minimum Spanning Tree (MST)
- **Implementation**: [`kruskal_mst`](file:///E:/SmartBiz_project/backend/app/algorithms/graph.py)
- **Mechanism**: Uses Disjoint Set Union (Union-Find) with path compression and union-by-rank.
- **Complexity**: $O(E \log E) = O(E \log V)$ time, $O(V)$ space.
- **Key Conceptual Distinction**:
  An MST minimizes the **global aggregate connection cost** of the entire network with zero cycles; it does **not** minimize individual point-to-point routes between specific pairs of vertices.

---

## 5. Benchmarking Protocol

All empirical benchmarks in SmartBiz Analytics follow these scientific controls:
1. Generate controlled random arrays with fixed seeds (`random.Random(42 + size)`).
2. Start high-precision hardware timer using `time.perf_counter()`.
3. Track memory allocation peaks using `tracemalloc.get_traced_memory()`.
4. Run multiple trials (3 to 5 iterations) and compute the statistical **median** to filter out OS thread jitter.
5. Verify output correctness against assertions before recording.
6. Persist execution results into the MySQL `algorithm_runs` table.
7. Render observed curve against theoretical asymptotic bounds in Recharts.
