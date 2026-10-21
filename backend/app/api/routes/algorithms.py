from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.algorithm_run import AlgorithmRun
from backend.app.algorithms.benchmarking import run_benchmark
from backend.app.algorithms.searching import linear_search, binary_search
from backend.app.algorithms.sorting import bubble_sort, merge_sort, quicksort
from backend.app.algorithms.knapsack import dp_knapsack
from backend.app.algorithms.greedy import greedy_knapsack
from backend.app.algorithms.graph import bfs, dfs, dijkstra_shortest_path, kruskal_mst, DEFAULT_LOGISTICS_GRAPH
from backend.app.schemas.schemas import AlgorithmRunRequest

router = APIRouter(prefix="/algorithms", tags=["Algorithm Lab"])

@router.post("/run")
def run_single_algorithm(
    payload: AlgorithmRunRequest,
    db: Session = Depends(get_db)
):
    try:
        res = run_benchmark(
            algorithm_name=payload.algorithm_name,
            input_size=payload.input_size,
            iterations=payload.iterations,
            db=db
        )
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

@router.get("/runs")
def get_algorithm_runs(
    algorithm_name: Optional[str] = None,
    problem_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    q = db.query(AlgorithmRun)
    if algorithm_name:
        q = q.filter(AlgorithmRun.algorithm_name.ilike(f"%{algorithm_name}%"))
    if problem_type:
        q = q.filter(AlgorithmRun.problem_type == problem_type)

    runs = q.order_by(AlgorithmRun.created_at.desc()).limit(limit).all()
    results = []
    for r in runs:
        results.append({
            "run_id": r.run_id,
            "algorithm_name": r.algorithm_name,
            "problem_type": r.problem_type,
            "input_size": r.input_size,
            "execution_time_ms": float(r.execution_time_ms),
            "memory_usage_mb": float(r.memory_usage_mb),
            "result_summary": r.result_summary,
            "configuration": r.configuration,
            "created_at": r.created_at.isoformat()
        })

    return results

@router.get("/compare")
def compare_algorithms(
    problem_type: str = Query("Sorting", pattern="^(Sorting|Searching|Optimization)$"),
    sizes: str = Query("50,100,250,500,1000"),
    db: Session = Depends(get_db)
):
    """
    Executes comparative benchmarks across multiple input sizes using genuine time.perf_counter() measurements.
    """
    try:
        size_list = [int(s.strip()) for s in sizes.split(",") if s.strip().isdigit()]
    except Exception:
        size_list = [50, 100, 250, 500, 1000]

    comparison_results = []

    if problem_type == "Sorting":
        algos = ["Bubble Sort", "Merge Sort", "Quicksort"]
        for size in size_list:
            size_metrics = {"input_size": size}
            for algo in algos:
                if algo == "Bubble Sort" and size > 2500:
                    size_metrics[algo] = None
                    continue
                bench = run_benchmark(algo, size, iterations=3, db=db)
                size_metrics[algo] = bench["median_time_ms"]
            comparison_results.append(size_metrics)

        return {
            "problem_type": "Sorting",
            "algorithms": algos,
            "complexity_reference": {
                "Bubble Sort": {"best": "O(n)", "average": "O(n^2)", "worst": "O(n^2)", "space": "O(1)"},
                "Merge Sort": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
                "Quicksort": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n^2)", "space": "O(log n)"}
            },
            "data": comparison_results
        }

    elif problem_type == "Searching":
        algos = ["Linear Search", "Binary Search"]
        for size in size_list:
            size_metrics = {"input_size": size}
            for algo in algos:
                bench = run_benchmark(algo, size, iterations=3, db=db)
                size_metrics[algo] = bench["median_time_ms"]
            comparison_results.append(size_metrics)

        return {
            "problem_type": "Searching",
            "algorithms": algos,
            "complexity_reference": {
                "Linear Search": {"best": "O(1)", "average": "O(n)", "worst": "O(n)", "space": "O(1)"},
                "Binary Search": {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)", "space": "O(1)"}
            },
            "data": comparison_results
        }

    else: # Optimization
        algos = ["Greedy Knapsack", "0/1 Knapsack DP"]
        opt_sizes = [min(s, 60) for s in size_list if s <= 60]
        for size in opt_sizes:
            size_metrics = {"input_size": size}
            for algo in algos:
                bench = run_benchmark(algo, size, iterations=2, db=db)
                size_metrics[algo] = bench["median_time_ms"]
            comparison_results.append(size_metrics)

        return {
            "problem_type": "Optimization",
            "algorithms": algos,
            "complexity_reference": {
                "Greedy Knapsack": {"time": "O(n log n)", "space": "O(n)", "optimality": "Approximate / Heuristic"},
                "0/1 Knapsack DP": {"time": "O(n * W) pseudo-polynomial", "space": "O(n * W)", "optimality": "Globally Optimal"}
            },
            "data": comparison_results
        }

@router.get("/graph/default")
def get_default_logistics_network():
    return DEFAULT_LOGISTICS_GRAPH
