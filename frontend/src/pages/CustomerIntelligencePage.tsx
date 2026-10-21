import React, { useState, useEffect } from 'react';
import {
  Users,
  Target,
  RefreshCw,
  Search,
  DollarSign,
  Calendar,
  Layers,
  ChevronRight,
  Sparkles,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { api } from '../lib/api';

const SEGMENT_COLORS: Record<string, string> = {
  Champions: '#6366f1',
  'Loyal Customers': '#10b981',
  'Potential Loyalists': '#3b82f6',
  'At Risk': '#f59e0b',
  Hibernating: '#ec4899',
  Lost: '#64748b'
};

export const CustomerIntelligencePage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [clusterCount, setClusterCount] = useState<number>(4);
  const [running, setRunning] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [selectedCustomer, setSelectedCustomer] = useState<any>(null);

  useEffect(() => {
    fetchSegments();
  }, []);

  const fetchSegments = async () => {
    setLoading(true);
    try {
      const res = await api.getCustomerSegments();
      setData(res);
    } catch (err) {
      console.error('Failed to load customer segments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSegmentation = async () => {
    setRunning(true);
    try {
      const res = await api.runCustomerSegmentation(clusterCount);
      setData(res);
      alert(`Customer segmentation recomputed successfully with ${clusterCount} clusters!`);
    } catch (err: any) {
      alert('Segmentation failed: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  const filteredCustomers = (data?.customers || []).filter((c: any) =>
    c.customer_name.toLowerCase().includes(search.toLowerCase()) ||
    c.email.toLowerCase().includes(search.toLowerCase()) ||
    c.segment_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Top Banner & Control Card */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4" />
            <span>K-Means RFM Segmentation Engine</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Customer Cohort & Value Intelligence
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Segments customers based on Recency (days since last purchase), Frequency (order count),
            and Monetary (lifetime spend). Scaled and grouped via unsupervised machine learning.
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-slate-50 dark:bg-slate-800/60 p-2 rounded-xl border border-slate-200 dark:border-slate-700">
          <label className="text-xs text-slate-600 dark:text-slate-300 font-medium">Clusters (k):</label>
          <select
            value={clusterCount}
            onChange={(e) => setClusterCount(Number(e.target.value))}
            className="bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-600 rounded-lg px-2.5 py-1 text-xs focus:outline-none"
          >
            <option value={3}>3 Clusters</option>
            <option value={4}>4 Clusters</option>
            <option value={5}>5 Clusters</option>
            <option value={6}>6 Clusters</option>
          </select>
          <button
            onClick={handleRunSegmentation}
            disabled={running}
            className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${running ? 'animate-spin' : ''}`} />
            <span>{running ? 'Clustering...' : 'Re-Run Model'}</span>
          </button>
        </div>
      </div>

      {/* Segment Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {(data?.segment_summary || []).map((seg: any) => {
          const color = SEGMENT_COLORS[seg.segment_name] || '#6366f1';
          return (
            <div
              key={seg.segment_name}
              className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm relative overflow-hidden"
            >
              <div
                className="absolute top-0 left-0 right-0 h-1.5"
                style={{ backgroundColor: color }}
              />
              <div className="flex justify-between items-start mb-2">
                <span className="font-bold text-slate-900 dark:text-white text-base">
                  {seg.segment_name}
                </span>
                <span
                  className="text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ backgroundColor: `${color}15`, color }}
                >
                  {seg.percentage_of_customers}%
                </span>
              </div>
              <div className="text-2xl font-black text-slate-900 dark:text-white mb-3">
                {seg.customer_count} <span className="text-xs font-normal text-slate-500">customers</span>
              </div>
              <div className="space-y-1.5 text-xs text-slate-600 dark:text-slate-300 border-t border-slate-100 dark:border-slate-800/80 pt-2.5">
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Recency:</span>
                  <span className="font-semibold">{seg.avg_recency_days} days</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Orders:</span>
                  <span className="font-semibold">{seg.avg_frequency}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Spend:</span>
                  <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                    ${seg.avg_monetary.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts: Segment Distribution & Average Spend Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart: Distribution */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
          <h3 className="font-bold text-slate-800 dark:text-white text-base">Cohort Customer Distribution</h3>
          <p className="text-xs text-slate-500 mb-4">Breakdown of customer base across segments</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data?.segment_summary || []}
                  dataKey="customer_count"
                  nameKey="segment_name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  innerRadius={50}
                  paddingAngle={4}
                >
                  {(data?.segment_summary || []).map((entry: any) => (
                    <Cell
                      key={`cell-${entry.segment_name}`}
                      fill={SEGMENT_COLORS[entry.segment_name] || '#6366f1'}
                    />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val: any, name: any) => [`${val} customers`, name]}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart: Avg Monetary Spend by Segment */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
          <h3 className="font-bold text-slate-800 dark:text-white text-base">Average Spending by Segment ($)</h3>
          <p className="text-xs text-slate-500 mb-4">Monetary value contrast across customer tiers</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.segment_summary || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                <XAxis dataKey="segment_name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `$${v}`} />
                <Tooltip
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Avg Monetary Spend']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }}
                />
                <Bar dataKey="avg_monetary" fill="#10b981" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Customer Directory Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Customer Directory & Segment Allocations ({filteredCustomers.length})
          </div>
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name, email, or segment..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-50 dark:bg-slate-800 text-xs border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-200 focus:outline-none w-64"
            />
          </div>
        </div>

        <div className="overflow-x-auto max-h-96">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider sticky top-0 border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="py-3 px-4">Customer Name</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">City</th>
                <th className="py-3 px-4">Assigned Segment</th>
                <th className="py-3 px-4 text-right">Recency (Days)</th>
                <th className="py-3 px-4 text-right">Frequency</th>
                <th className="py-3 px-4 text-right">Monetary Spend</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {filteredCustomers.map((c: any) => {
                const color = SEGMENT_COLORS[c.segment_name] || '#6366f1';
                return (
                  <tr key={c.customer_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                    <td className="py-3.5 px-4 font-semibold text-slate-900 dark:text-white">
                      {c.customer_name}
                    </td>
                    <td className="py-3.5 px-4 text-slate-500">{c.email}</td>
                    <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">{c.city}</td>
                    <td className="py-3.5 px-4">
                      <span
                        className="px-2.5 py-0.5 rounded-full text-[11px] font-bold"
                        style={{ backgroundColor: `${color}15`, color }}
                      >
                        {c.segment_name}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right font-mono text-slate-700 dark:text-slate-200">{c.recency}</td>
                    <td className="py-3.5 px-4 text-right font-mono text-slate-700 dark:text-slate-200">{c.frequency}</td>
                    <td className="py-3.5 px-4 text-right font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                      ${c.monetary.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
