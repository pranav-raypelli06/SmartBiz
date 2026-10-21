"""
Graph Algorithms for Logistics and Supply Chain Optimization (Analysis of Algorithms)
Implements BFS, DFS, Dijkstra's Shortest Path, and Kruskal's / Prim's MST.
No reliance on networkx or external graph libraries.
"""

from typing import Any, Dict, List, Optional, Set, Tuple

# Standard retail logistics network representing distribution centers, hubs, and stores
DEFAULT_LOGISTICS_GRAPH = {
    "nodes": [
        {"id": "Central_Warehouse", "label": "Central Mega-Hub (Chicago)", "x": 50, "y": 40},
        {"id": "North_Hub", "label": "North Distribution Center (Minneapolis)", "x": 45, "y": 20},
        {"id": "East_Hub", "label": "East Distribution Center (New York)", "x": 80, "y": 35},
        {"id": "West_Hub", "label": "West Distribution Center (Denver)", "x": 30, "y": 50},
        {"id": "South_Hub", "label": "South Distribution Center (Dallas)", "x": 48, "y": 75},
        {"id": "Pacific_Store", "label": "Pacific Retail Outlet (Seattle)", "x": 15, "y": 20},
        {"id": "California_Store", "label": "California Retail Outlet (San Jose)", "x": 10, "y": 60},
        {"id": "Southeast_Store", "label": "Southeast Retail Outlet (Atlanta)", "x": 70, "y": 70},
        {"id": "Midwest_Store", "label": "Midwest Retail Outlet (Detroit)", "x": 62, "y": 32},
    ],
    "edges": [
        {"source": "Central_Warehouse", "target": "North_Hub", "weight": 410, "label": "410 miles"},
        {"source": "Central_Warehouse", "target": "East_Hub", "weight": 790, "label": "790 miles"},
        {"source": "Central_Warehouse", "target": "West_Hub", "weight": 1000, "label": "1000 miles"},
        {"source": "Central_Warehouse", "target": "South_Hub", "weight": 920, "label": "920 miles"},
        {"source": "Central_Warehouse", "target": "Midwest_Store", "weight": 280, "label": "280 miles"},
        {"source": "North_Hub", "target": "Pacific_Store", "weight": 1650, "label": "1650 miles"},
        {"source": "West_Hub", "target": "Pacific_Store", "weight": 1300, "label": "1300 miles"},
        {"source": "West_Hub", "target": "California_Store", "weight": 1050, "label": "1050 miles"},
        {"source": "South_Hub", "target": "California_Store", "weight": 1450, "label": "1450 miles"},
        {"source": "South_Hub", "target": "Southeast_Store", "weight": 780, "label": "780 miles"},
        {"source": "East_Hub", "target": "Southeast_Store", "weight": 860, "label": "860 miles"},
        {"source": "East_Hub", "target": "Midwest_Store", "weight": 610, "label": "610 miles"},
    ]
}

def build_adjacency(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, List[Tuple[str, float]]]:
    adj = {node["id"]: [] for node in nodes}
    for e in edges:
        u = e["source"]
        v = e["target"]
        w = float(e["weight"])
        if u in adj and v in adj:
            adj[u].append((v, w))
            adj[v].append((u, w)) # Undirected logistics network
    return adj

def bfs(graph: Dict[str, Any], start_node: str) -> Dict[str, Any]:
    """
    Breadth-First Search: Explores the neighbor nodes first, before moving to the next level neighbors.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    nodes = graph.get("nodes", DEFAULT_LOGISTICS_GRAPH["nodes"])
    edges = graph.get("edges", DEFAULT_LOGISTICS_GRAPH["edges"])
    adj = build_adjacency(nodes, edges)

    if start_node not in adj:
        raise ValueError(f"Start node '{start_node}' not found in graph.")

    visited: List[str] = []
    visited_set: Set[str] = set()
    queue: List[str] = [start_node]
    visited_set.add(start_node)
    traversal_tree: List[Dict[str, Any]] = []

    while queue:
        curr = queue.pop(0) # FIFO
        visited.append(curr)

        for neighbor, weight in adj.get(curr, []):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)
                traversal_tree.append({"from": curr, "to": neighbor, "weight": weight})

    return {
        "algorithm": "Breadth-First Search (BFS)",
        "start_node": start_node,
        "visited_order": visited,
        "nodes_visited_count": len(visited),
        "traversal_edges": traversal_tree,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": "Level-order traversal discovering nodes in increasing order of unweighted edge distance."
    }

def dfs(graph: Dict[str, Any], start_node: str) -> Dict[str, Any]:
    """
    Depth-First Search: Explores as far as possible along each branch before backtracking.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    nodes = graph.get("nodes", DEFAULT_LOGISTICS_GRAPH["nodes"])
    edges = graph.get("edges", DEFAULT_LOGISTICS_GRAPH["edges"])
    adj = build_adjacency(nodes, edges)

    if start_node not in adj:
        raise ValueError(f"Start node '{start_node}' not found in graph.")

    visited: List[str] = []
    visited_set: Set[str] = set()
    traversal_tree: List[Dict[str, Any]] = []

    def _dfs(u: str):
        visited_set.add(u)
        visited.append(u)
        for v, w in adj.get(u, []):
            if v not in visited_set:
                traversal_tree.append({"from": u, "to": v, "weight": w})
                _dfs(v)

    _dfs(start_node)

    return {
        "algorithm": "Depth-First Search (DFS)",
        "start_node": start_node,
        "visited_order": visited,
        "nodes_visited_count": len(visited),
        "traversal_edges": traversal_tree,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": "Explores deep paths down each branch before backtracking, suitable for cycle detection and topological sorting."
    }

def dijkstra_shortest_path(graph: Dict[str, Any], start_node: str, end_node: str) -> Dict[str, Any]:
    """
    Dijkstra's Algorithm: Computes single-source shortest path in weighted graphs with non-negative weights.
    Rejects negative edge weights.
    Time Complexity: O(V^2) or O((V + E) log V) with priority queue.
    """
    nodes = graph.get("nodes", DEFAULT_LOGISTICS_GRAPH["nodes"])
    edges = graph.get("edges", DEFAULT_LOGISTICS_GRAPH["edges"])

    for e in edges:
        if float(e["weight"]) < 0:
            raise ValueError(f"Dijkstra algorithm requires strictly non-negative edge weights. Found negative weight {e['weight']} on edge {e['source']} -> {e['target']}.")

    adj = build_adjacency(nodes, edges)
    if start_node not in adj or end_node not in adj:
        raise ValueError("Start or destination node not present in graph.")

    dist = {n["id"]: float("inf") for n in nodes}
    prev: Dict[str, Optional[str]] = {n["id"]: None for n in nodes}
    unvisited = set(dist.keys())

    dist[start_node] = 0.0

    while unvisited:
        # Pick unvisited node with smallest distance
        curr = min(unvisited, key=lambda n: dist[n])
        if dist[curr] == float("inf"):
            break # Remaining nodes unreachable

        unvisited.remove(curr)
        if curr == end_node:
            break

        for neighbor, weight in adj.get(curr, []):
            if neighbor in unvisited:
                alt = dist[curr] + weight
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = curr

    # Reconstruct path from end to start
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    if not path or path[0] != start_node:
        path = []
        total_dist = float("inf")
    else:
        total_dist = dist[end_node]

    # Build edge segments for visual highlight
    path_edges = []
    for i in range(len(path) - 1):
        path_edges.append({"source": path[i], "target": path[i + 1]})

    return {
        "algorithm": "Dijkstra's Shortest Path",
        "start_node": start_node,
        "end_node": end_node,
        "path": path,
        "path_edges": path_edges,
        "total_cost": round(total_dist, 2) if total_dist != float("inf") else -1,
        "reachable": total_dist != float("inf"),
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "explanation": f"The optimal path from {start_node} to {end_node} traverses {len(path)} logistics hubs with total transit cost {total_dist:,.2f}."
    }

def kruskal_mst(graph: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kruskal's Algorithm: Finds a Minimum Spanning Tree (MST) for a connected weighted graph.
    Sorts all edges and uses Disjoint Set Union (Union-Find) with path compression and rank.
    Time Complexity: O(E log E) = O(E log V)
    Space Complexity: O(V + E)
    """
    nodes = graph.get("nodes", DEFAULT_LOGISTICS_GRAPH["nodes"])
    edges = list(graph.get("edges", DEFAULT_LOGISTICS_GRAPH["edges"]))

    # Union-Find data structure
    parent = {n["id"]: n["id"] for n in nodes}
    rank = {n["id"]: 0 for n in nodes}

    def find(i: str) -> str:
        if parent[i] == i:
            return i
        parent[i] = find(parent[i]) # Path compression
        return parent[i]

    def union(i: str, j: str) -> bool:
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    # Sort edges by weight
    edges_sorted = sorted(edges, key=lambda e: float(e["weight"]))
    mst_edges = []
    total_weight = 0.0

    for e in edges_sorted:
        u = e["source"]
        v = e["target"]
        w = float(e["weight"])
        if union(u, v):
            mst_edges.append(e)
            total_weight += w
            if len(mst_edges) == len(nodes) - 1:
                break

    return {
        "algorithm": "Kruskal's Minimum Spanning Tree (MST)",
        "mst_edges": mst_edges,
        "total_mst_cost": round(total_weight, 2),
        "total_edges_selected": len(mst_edges),
        "total_nodes_connected": len(nodes),
        "time_complexity": "O(E log E)",
        "space_complexity": "O(V)",
        "distinction_note": (
            "A Minimum Spanning Tree minimizes the TOTAL connection cost across the entire logistics network, "
            "connecting all hubs with no cycles using minimum aggregate cable/transit distance. "
            "Unlike Dijkstra's algorithm, an MST does NOT guarantee the shortest point-to-point path between any specific pair."
        )
    }
