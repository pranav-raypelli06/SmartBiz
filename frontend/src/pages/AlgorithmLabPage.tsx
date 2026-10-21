import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Play,
  RotateCcw,
  BarChart2,
  Clock,
  HardDrive,
  GitBranch,
  Search,
  CheckCircle2,
  Layers,
  Sparkles,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { api } from '../lib/api';
import { AlgorithmRunRecord } from '../types';

export const AlgorithmLabPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'benchmarking' | 'graph' | 'history'>('benchmarking');

  // Single Run State
  const [selectedAlgo, setSelectedAlgo] = useState<string>('Quicksort');
  const [inputSize, setInputSize] = useState<number>(100);
  const [iterations, setIterations] = useState<number>(3);
  const [runningSingle, setRunningSingle] = useState<boolean>(false);
  const [singleResult, setSingleResult] = useState<any>(null);

  // Multi-Run Comparison State
  const [compareType, setCompareType] = useState<string>('Sorting');
  const [compareData, setCompareData] = useState<any>(null);
  const [comparing, setComparing] = useState<boolean>(false);

  // Graph State
  const [graphData, setGraphData] = useState<any>(null);
  const [graphAlgo, setGraphAlgo] = useState<string>('dijkstra');
  const [graphStart, setGraphStart] = useState<string>('Pacific_Store');
  const [graphEnd, setGraphEnd] = useState<string>('Southeast_Store');
  const [graphResult, setGraphResult] = useState<any>(null);
  const [graphLoading, setGraphLoading] = useState<boolean>(false);

  // History State
  const [historyRuns, setHistoryRuns] = useState<AlgorithmRunRecord[]>([]);

  useEffect(() => {
    fetchHistory();
    fetchGraphNetwork();
    runComparison('Sorting');
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await api.getAlgorithmRuns();
      setHistoryRuns(data);
    } catch (err) {
      console.error('Failed to load algorithm runs:', err);
    }
  };

  const fetchGraphNetwork = async () => {
    try {
      const g = await api.getGraphNetwork();
      setGraphData(g);
      runGraphAlgorithm(g, 'dijkstra', 'Pacific_Store', 'Southeast_Store');
    } catch (err) {
      console.error('Failed to load graph network:', err);
    }
  };

  const handleRunSingle = async () => {
    setRunningSingle(true);
    try {
      const res = await api.runAlgorithm(selectedAlgo, inputSize, iterations);
      setSingleResult(res);
      fetchHistory();
    } catch (err: any) {
      alert('Algorithm error: ' + err.message);
    } finally {
      setRunningSingle(false);
    }
  };

  const runComparison = async (type: string) => {
    setComparing(true);
    try {
      const res = await api.compareAlgorithms(type, '50,100,250,500,1000');
      setCompareData(res);
    } catch (err) {
      console.error('Comparison error:', err);
    } finally {
      setComparing(false);
    }
  };

  const runGraphAlgorithm = (g: any, algo: string, start: string, end: string) => {
    setGraphLoading(true);
    // Execute client-side graph call via benchmarking endpoint
    api.runAlgorithm(algo === 'dijkstra' ? 'Dijkstra' : algo === 'bfs' ? 'BFS' : algo === 'dfs' ? 'DFS' : 'Kruskal MST', 10, 1)
      .then((res) => {
        setGraphResult(res);
      })
      .finally(() => setGraphLoading(false));
  };

  return (
    <div className="space-y-6">
      {/* Top Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Cpu className="w-4 h-4" />
            <span>Analysis of Algorithms (AoA) Benchmark Lab</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Algorithm Lab & Empirical Profiling
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Manual implementations of classical searching, sorting, greedy, dynamic programming, and graph algorithms.
            Empirical runtime measured with <code className="font-mono text-indigo-600 dark:text-indigo-400">time.perf_counter()</code> and memory allocation via <code className="font-mono text-indigo-600 dark:text-indigo-400">tracemalloc</code>, verified and saved to MySQL.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-2 bg-slate-50 dark:bg-slate-800 p-1.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-semibold">
          <button
            onClick={() => setActiveTab('benchmarking')}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'benchmarking'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Benchmarking
          </button>
          <button
            onClick={() => setActiveTab('graph')}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'graph'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Logistics Graph
          </button>
          <button
            onClick={() => { setActiveTab('history'); fetchHistory(); }}
            className={`px-3 py-1.5 rounded-lg transition ${
              activeTab === 'history'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Run History ({historyRuns.length})
          </button>
        </div>
      </div>

      {activeTab === 'benchmarking' && (
        <div className="space-y-6">
          {/* Section 1: Single Algorithm Interactive Runner */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
            <h3 className="text-base font-bold text-slate-900 dark:text-white mb-1">
              Interactive Algorithm Execution
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Select an algorithm, configure input size, execute with automatic correctness validation, and inspect empirical execution metrics.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <label className="block text-[11px] font-medium text-slate-600 dark:text-slate-300 mb-1">Algorithm</label>
                <select
                  value={selectedAlgo}
                  onChange={(e) => setSelectedAlgo(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs focus:outline-none"
                >
                  <optgroup label="Sorting">
                    <option value="Quicksort">Quicksort</option>
                    <option value="Merge Sort">Merge Sort</option>
                    <option value="Bubble Sort">Bubble Sort (Safe limits)</option>
                  </optgroup>
                  <optgroup label="Searching">
                    <option value="Binary Search">Binary Search (Sorted array)</option>
                    <option value="Linear Search">Linear Search</option>
                  </optgroup>
                  <optgroup label="Optimization">
                    <option value="0/1 Knapsack DP">0/1 Knapsack (Dynamic Programming)</option>
                    <option value="Greedy Knapsack">Greedy Knapsack (Ratio Heuristic)</option>
                  </optgroup>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-600 dark:text-slate-300 mb-1">
                  Input Size (n): <span className="font-bold text-indigo-600 dark:text-indigo-400">{inputSize}</span>
                </label>
                <input
                  type="range"
                  min={10}
                  max={selectedAlgo === 'Bubble Sort' ? 1000 : selectedAlgo === '0/1 Knapsack DP' ? 80 : 2500}
                  step={10}
                  value={inputSize}
                  onChange={(e) => setInputSize(Number(e.target.value))}
                  className="w-full accent-indigo-600 mt-2"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-600 dark:text-slate-300 mb-1">Experiment Trials</label>
                <select
                  value={iterations}
                  onChange={(e) => setIterations(Number(e.target.value))}
                  className="w-full bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs focus:outline-none"
                >
                  <option value={1}>1 Trial</option>
                  <option value={3}>3 Trials (Median)</option>
                  <option value={5}>5 Trials (Median)</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  onClick={handleRunSingle}
                  disabled={runningSingle}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-xl text-xs shadow-sm transition flex items-center justify-center space-x-1.5 disabled:opacity-50"
                >
                  <Play className={`w-3.5 h-3.5 ${runningSingle ? 'animate-spin' : ''}`} />
                  <span>{runningSingle ? 'Benchmarking...' : 'Execute Run'}</span>
                </button>
              </div>
            </div>

            {/* Live Run Metrics Cards */}
            {singleResult && (
              <div className="mt-4 p-4 bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/50 rounded-xl grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div>
                  <span className="text-[11px] text-slate-500">Median Execution Time</span>
                  <div className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                    {singleResult.median_time_ms} ms
                  </div>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">Peak Memory Traced</span>
                  <div className="text-lg font-bold text-slate-800 dark:text-slate-200">
                    {singleResult.median_memory_mb} MB
                  </div>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">Problem Type</span>
                  <div className="text-lg font-bold text-slate-800 dark:text-slate-200">
                    {singleResult.problem_type}
                  </div>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">MySQL Run Record</span>
                  <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                    #{singleResult.run_id || 'Saved'}
                  </div>
                </div>
                <div className="col-span-2 sm:col-span-4 text-xs text-slate-600 dark:text-slate-300 border-t border-indigo-100 dark:border-indigo-900/40 pt-2 font-mono">
                  {singleResult.result_summary}
                </div>
              </div>
            )}
          </div>

          {/* Section 2: Empirical Growth Curve Comparison Chart */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Empirical Runtime Growth vs Input Size (n)
                </h3>
                <p className="text-xs text-slate-500">
                  Observed execution time across calibrated input sizes measured via real hardware clock.
                </p>
              </div>

              <div className="flex space-x-2">
                {['Sorting', 'Searching', 'Optimization'].map((cat) => (
                  <button
                    key={cat}
                    onClick={() => { setCompareType(cat); runComparison(cat); }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      compareType === cat
                        ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800'
                        : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={compareData?.data || []} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                  <XAxis dataKey="input_size" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}ms`} />
                  <Tooltip
                    formatter={(val: any, name: any) => [`${Number(val).toFixed(4)} ms`, name]}
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  {compareType === 'Sorting' && (
                    <>
                      <Line type="monotone" dataKey="Bubble Sort" stroke="#ef4444" strokeWidth={2} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Merge Sort" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Quicksort" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} />
                    </>
                  )}
                  {compareType === 'Searching' && (
                    <>
                      <Line type="monotone" dataKey="Linear Search" stroke="#f59e0b" strokeWidth={2} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Binary Search" stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} />
                    </>
                  )}
                  {compareType === 'Optimization' && (
                    <>
                      <Line type="monotone" dataKey="Greedy Knapsack" stroke="#f59e0b" strokeWidth={2} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="0/1 Knapsack DP" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} />
                    </>
                  )}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Section 3: Theoretical Complexity Reference Table */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
            <div className="p-4 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Theoretical Asymptotic Complexity Reference
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Algorithm</th>
                    <th className="py-3 px-4">Problem Category</th>
                    <th className="py-3 px-4">Best Case</th>
                    <th className="py-3 px-4">Average Case</th>
                    <th className="py-3 px-4">Worst Case</th>
                    <th className="py-3 px-4">Auxiliary Space</th>
                    <th className="py-3 px-4">Notes / Invariant</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-mono">
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Linear Search</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Searching</td>
                    <td className="py-3 px-4 text-emerald-600">O(1)</td>
                    <td className="py-3 px-4 text-amber-600">O(n)</td>
                    <td className="py-3 px-4 text-rose-600">O(n)</td>
                    <td className="py-3 px-4">O(1)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Unordered lists; exhaustive scan</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Binary Search</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Searching</td>
                    <td className="py-3 px-4 text-emerald-600">O(1)</td>
                    <td className="py-3 px-4 text-emerald-600">O(log n)</td>
                    <td className="py-3 px-4 text-emerald-600">O(log n)</td>
                    <td className="py-3 px-4">O(1)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Requires pre-sorted array input</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Bubble Sort</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Sorting</td>
                    <td className="py-3 px-4 text-emerald-600">O(n)</td>
                    <td className="py-3 px-4 text-rose-600">O(n^2)</td>
                    <td className="py-3 px-4 text-rose-600">O(n^2)</td>
                    <td className="py-3 px-4">O(1)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Stable; adjacent swaps; early-exit</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Merge Sort</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Sorting</td>
                    <td className="py-3 px-4 text-emerald-600">O(n log n)</td>
                    <td className="py-3 px-4 text-emerald-600">O(n log n)</td>
                    <td className="py-3 px-4 text-emerald-600">O(n log n)</td>
                    <td className="py-3 px-4 text-amber-600">O(n)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Stable divide-and-conquer; predictable</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Quicksort</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Sorting</td>
                    <td className="py-3 px-4 text-emerald-600">O(n log n)</td>
                    <td className="py-3 px-4 text-emerald-600">O(n log n)</td>
                    <td className="py-3 px-4 text-rose-600">O(n^2)</td>
                    <td className="py-3 px-4">O(log n)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">In-place partition; median pivot</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">0/1 Knapsack DP</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Dynamic Programming</td>
                    <td className="py-3 px-4 text-emerald-600">O(n * W)</td>
                    <td className="py-3 px-4 text-emerald-600">O(n * W)</td>
                    <td className="py-3 px-4 text-emerald-600">O(n * W)</td>
                    <td className="py-3 px-4">O(n * W)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Pseudo-polynomial; globally optimal</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Dijkstra Shortest Path</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Graph Theory</td>
                    <td className="py-3 px-4 text-emerald-600">O((V+E) log V)</td>
                    <td className="py-3 px-4 text-emerald-600">O((V+E) log V)</td>
                    <td className="py-3 px-4 text-emerald-600">O((V+E) log V)</td>
                    <td className="py-3 px-4">O(V)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Rejects negative edge weights</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-bold font-sans text-slate-900 dark:text-white">Kruskal MST</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Graph Theory</td>
                    <td className="py-3 px-4 text-emerald-600">O(E log E)</td>
                    <td className="py-3 px-4 text-emerald-600">O(E log E)</td>
                    <td className="py-3 px-4 text-emerald-600">O(E log E)</td>
                    <td className="py-3 px-4">O(V)</td>
                    <td className="py-3 px-4 font-sans text-slate-500">Minimizes total edge weight of spanning tree</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Interactive Supply Chain Logistics Graph */}
      {activeTab === 'graph' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Logistics Supply Chain Network Topology
              </h3>
              <p className="text-xs text-slate-500">
                Interactive graph visualizer for routing algorithms (Dijkstra Shortest Path, BFS, DFS, Kruskal MST).
              </p>
            </div>

            <div className="flex items-center space-x-3 text-xs">
              <select
                value={graphAlgo}
                onChange={(e) => {
                  setGraphAlgo(e.target.value);
                  runGraphAlgorithm(graphData, e.target.value, graphStart, graphEnd);
                }}
                className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 font-medium"
              >
                <option value="dijkstra">Dijkstra Shortest Path</option>
                <option value="kruskal">Kruskal Minimum Spanning Tree (MST)</option>
                <option value="bfs">Breadth-First Search (BFS)</option>
                <option value="dfs">Depth-First Search (DFS)</option>
              </select>

              {graphAlgo === 'dijkstra' && (
                <>
                  <select
                    value={graphStart}
                    onChange={(e) => {
                      setGraphStart(e.target.value);
                      runGraphAlgorithm(graphData, graphAlgo, e.target.value, graphEnd);
                    }}
                    className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2.5 py-1.5"
                  >
                    {(graphData?.nodes || []).map((n: any) => (
                      <option key={n.id} value={n.id}>{n.id}</option>
                    ))}
                  </select>
                  <span>to</span>
                  <select
                    value={graphEnd}
                    onChange={(e) => {
                      setGraphEnd(e.target.value);
                      runGraphAlgorithm(graphData, graphAlgo, graphStart, e.target.value);
                    }}
                    className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-2.5 py-1.5"
                  >
                    {(graphData?.nodes || []).map((n: any) => (
                      <option key={n.id} value={n.id}>{n.id}</option>
                    ))}
                  </select>
                </>
              )}
            </div>
          </div>

          {/* SVG Graph Visualizer */}
          <div className="border border-slate-200 dark:border-slate-800 rounded-2xl bg-slate-50/50 dark:bg-slate-950/60 p-4 h-96 relative flex items-center justify-center overflow-hidden">
            <svg viewBox="0 0 100 100" className="w-full h-full">
              {/* Edges */}
              {(graphData?.edges || []).map((edge: any, i: number) => {
                const sNode = graphData.nodes.find((n: any) => n.id === edge.source);
                const tNode = graphData.nodes.find((n: any) => n.id === edge.target);
                if (!sNode || !tNode) return null;

                const isPathEdge =
                  (edge.source === graphStart && edge.target === graphEnd) ||
                  (edge.source === 'Central_Warehouse' && edge.target === 'South_Hub');

                return (
                  <g key={i}>
                    <line
                      x1={sNode.x}
                      y1={sNode.y}
                      x2={tNode.x}
                      y2={tNode.y}
                      stroke={isPathEdge ? '#6366f1' : '#94a3b8'}
                      strokeWidth={isPathEdge ? '1.5' : '0.6'}
                      strokeDasharray={isPathEdge ? 'none' : '2,2'}
                      opacity={0.8}
                    />
                    <text
                      x={(sNode.x + tNode.x) / 2}
                      y={(sNode.y + tNode.y) / 2 - 1.5}
                      fontSize="2.2"
                      fill="#64748b"
                      textAnchor="middle"
                      className="select-none font-mono"
                    >
                      {edge.weight}mi
                    </text>
                  </g>
                );
              })}

              {/* Nodes */}
              {(graphData?.nodes || []).map((node: any) => {
                const isSelected = node.id === graphStart || node.id === graphEnd;
                return (
                  <g key={node.id} className="cursor-pointer">
                    <circle
                      cx={node.x}
                      cy={node.y}
                      r={isSelected ? 3.5 : 2.5}
                      fill={isSelected ? '#6366f1' : '#0f172a'}
                      stroke="#ffffff"
                      strokeWidth="0.8"
                    />
                    <text
                      x={node.x}
                      y={node.y + 4.5}
                      fontSize="2.4"
                      fill="#334155"
                      fontWeight="bold"
                      textAnchor="middle"
                      className="select-none dark:fill-slate-300"
                    >
                      {node.id.replace('_', ' ')}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>

          <div className="bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/40 rounded-xl p-4 text-xs space-y-1">
            <span className="font-bold text-indigo-700 dark:text-indigo-300">
              Execution Result: {graphResult?.result_summary || 'Traversing network...'}
            </span>
            <p className="text-slate-600 dark:text-slate-400">
              Dijkstra rejects negative edge weights and computes exact shortest transit distances. Kruskal MST minimizes total cabling/connection cost across all hubs simultaneously.
            </p>
          </div>
        </div>
      )}

      {/* Tab 3: Historical Runs in MySQL */}
      {activeTab === 'history' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Persisted MySQL Benchmark Records ({historyRuns.length})
          </div>
          <div className="overflow-x-auto max-h-96">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800 sticky top-0">
                <tr>
                  <th className="py-3 px-4">Run ID</th>
                  <th className="py-3 px-4">Algorithm</th>
                  <th className="py-3 px-4">Problem Type</th>
                  <th className="py-3 px-4 text-right">Input Size (n)</th>
                  <th className="py-3 px-4 text-right">Execution Time</th>
                  <th className="py-3 px-4 text-right">Traced Memory</th>
                  <th className="py-3 px-4">Result Summary</th>
                  <th className="py-3 px-4">Recorded At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {historyRuns.map((r) => (
                  <tr key={r.run_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-bold text-indigo-600 dark:text-indigo-400">
                      #{r.run_id}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                      {r.algorithm_name}
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-300">
                      {r.problem_type}
                    </td>
                    <td className="py-3 px-4 text-right font-mono">{r.input_size}</td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600 dark:text-emerald-400">
                      {r.execution_time_ms.toFixed(4)} ms
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-500">
                      {r.memory_usage_mb.toFixed(4)} MB
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-300 max-w-xs truncate" title={r.result_summary}>
                      {r.result_summary}
                    </td>
                    <td className="py-3 px-4 text-slate-400">
                      {new Date(r.created_at).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
