import React, { useState, useEffect } from 'react';
import {
  Boxes,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  Zap,
  Info,
  Scale
} from 'lucide-react';
import { api } from '../lib/api';

export const InventoryOptimizationPage: React.FC = () => {
  const [budget, setBudget] = useState<number>(5000);
  const [recommendations, setRecommendations] = useState<any>(null);
  const [optimization, setOptimization] = useState<any>(null);
  const [optimizing, setOptimizing] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchRecommendations();
    runOptimization(5000);
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const res = await api.getInventoryRecommendations();
      setRecommendations(res);
    } catch (err) {
      console.error('Failed to load inventory recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const runOptimization = async (targetBudget: number) => {
    setOptimizing(true);
    try {
      const res = await api.optimizeInventory(targetBudget);
      setOptimization(res);
    } catch (err: any) {
      alert('Optimization error: ' + err.message);
    } finally {
      setOptimizing(false);
    }
  };

  const handleBudgetSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (budget > 0) {
      runOptimization(budget);
    }
  };

  const dp = optimization?.dynamic_programming;
  const greedy = optimization?.greedy;
  const analysis = optimization?.comparison_analysis;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Zap className="w-4 h-4" />
            <span>Knapsack & Greedy Decision Support</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Inventory Purchasing Optimization
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Calculates proposed replenishment quantities by integrating reorder thresholds and demand forecasts.
            Solves optimal budget allocation using 0/1 Knapsack Dynamic Programming versus a Greedy benchmark.
          </p>
        </div>

        {/* Budget Form */}
        <form onSubmit={handleBudgetSubmit} className="flex items-center space-x-2 bg-slate-50 dark:bg-slate-800/60 p-2 rounded-xl border border-slate-200 dark:border-slate-700">
          <DollarSign className="w-4 h-4 text-slate-400" />
          <input
            type="number"
            min={100}
            step={100}
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="w-28 bg-transparent text-sm font-semibold text-slate-800 dark:text-slate-100 focus:outline-none"
            placeholder="Budget ($)"
          />
          <button
            type="submit"
            disabled={optimizing}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition disabled:opacity-50"
          >
            {optimizing ? 'Optimizing...' : 'Run Solver'}
          </button>
        </form>
      </div>

      {/* Side-by-Side Algorithm Comparison Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Dynamic Programming (0/1 Knapsack) Card */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border-2 border-indigo-500/40 dark:border-indigo-500/30 p-6 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-indigo-600 text-white text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-bl-xl shadow-sm">
            Globally Optimal Solution
          </div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-bold text-sm mb-1">
            <Scale className="w-4 h-4" />
            <span>Dynamic Programming (0/1 Knapsack)</span>
          </div>
          <p className="text-xs text-slate-500 mb-4">
            Bottom-up 2D tabulation guarantee: achieves the mathematically highest possible gross profit.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Total Profit</span>
              <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                ${dp?.total_benefit?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Total Cost</span>
              <div className="text-lg font-bold text-slate-900 dark:text-white">
                ${dp?.total_cost?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Remaining</span>
              <div className="text-lg font-bold text-slate-700 dark:text-slate-300">
                ${dp?.budget_remaining?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Selected</span>
              <div className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                {dp?.selected_count || 0} batches
              </div>
            </div>
          </div>

          <div className="text-xs text-slate-600 dark:text-slate-400 bg-indigo-50/50 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/50 p-3 rounded-xl">
            {analysis?.advantage_of_dp > 0 ? (
              <span className="font-semibold text-indigo-700 dark:text-indigo-300">
                DP achieves +${analysis.advantage_of_dp} ({analysis.percentage_gain}%) higher benefit than greedy selection by eliminating budget fragmentation.
              </span>
            ) : (
              <span>DP and Greedy matched identical optimal totals for this budget distribution.</span>
            )}
          </div>
        </div>

        {/* Greedy Heuristic Card */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
          <div className="flex items-center space-x-2 text-slate-700 dark:text-slate-300 font-bold text-sm mb-1">
            <Zap className="w-4 h-4 text-amber-500" />
            <span>Greedy Strategy (Value-to-Cost Ratio)</span>
          </div>
          <p className="text-xs text-slate-500 mb-4">
            Ranks candidate batches by profit ratio; takes highest ratio until budget exhausts.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Total Profit</span>
              <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                ${greedy?.total_benefit?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Total Cost</span>
              <div className="text-lg font-bold text-slate-900 dark:text-white">
                ${greedy?.total_cost?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Remaining</span>
              <div className="text-lg font-bold text-slate-700 dark:text-slate-300">
                ${greedy?.budget_remaining?.toLocaleString() || '0.00'}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
              <span className="text-[11px] text-slate-400">Selected</span>
              <div className="text-lg font-bold text-slate-700 dark:text-slate-300">
                {greedy?.selected_count || 0} batches
              </div>
            </div>
          </div>

          <div className="text-xs text-slate-500 bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl">
            Heuristic time complexity: O(n log n). Note: Greedy is fast but does not guarantee global optimality for discrete 0/1 knapsacks.
          </div>
        </div>
      </div>

      {/* Stock Replenishment Requirements Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Items Requiring Replenishment ({recommendations?.items_requiring_replenishment || 0})
          </div>
          <span className="text-xs font-semibold text-slate-600 dark:text-slate-400">
            Total Est. Restock Budget: <strong className="text-slate-900 dark:text-white">${recommendations?.total_estimated_restock_budget?.toLocaleString()}</strong>
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="py-3 px-4">Priority</th>
                <th className="py-3 px-4">Product Name</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Preferred Supplier</th>
                <th className="py-3 px-4 text-right">Current Stock</th>
                <th className="py-3 px-4 text-right">Reorder Point</th>
                <th className="py-3 px-4 text-right">Forecast Demand</th>
                <th className="py-3 px-4 text-right">Proposed Qty</th>
                <th className="py-3 px-4 text-right">Estimated Cost</th>
                <th className="py-3 px-4 text-right">Expected Profit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {(recommendations?.recommendations || []).map((r: any) => (
                <tr key={r.product_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                  <td className="py-3.5 px-4">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[11px] font-bold ${
                        r.priority === 'Critical'
                          ? 'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-400'
                          : r.priority === 'High'
                          ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400'
                          : 'bg-blue-50 text-blue-700 dark:bg-blue-950/50 dark:text-blue-400'
                      }`}
                    >
                      {r.priority}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-semibold text-slate-900 dark:text-white">
                    {r.product_name}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">
                    {r.category}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">
                    {r.supplier_name}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-bold text-rose-600 dark:text-rose-400">
                    {r.current_stock}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-slate-500">
                    {r.reorder_level}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-indigo-600 dark:text-indigo-400">
                    {r.forecasted_demand}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-bold text-slate-900 dark:text-white">
                    {r.proposed_quantity} units
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-semibold text-slate-900 dark:text-white">
                    ${r.estimated_purchasing_cost.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                    +${r.estimated_expected_profit.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
