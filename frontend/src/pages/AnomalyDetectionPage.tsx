import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  CheckCircle,
  Eye,
  RefreshCw,
  Info,
  Clock,
  Filter
} from 'lucide-react';
import { api } from '../lib/api';
import { AnomalyItem } from '../types';

export const AnomalyDetectionPage: React.FC = () => {
  const [alerts, setAlerts] = useState<AnomalyItem[]>([]);
  const [severityFilter, setSeverityFilter] = useState<string>('All');
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [severitySummary, setSeveritySummary] = useState<Record<string, number>>({});
  const [statusSummary, setStatusSummary] = useState<Record<string, number>>({});
  const [running, setRunning] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchAnomalies();
  }, [severityFilter, statusFilter]);

  const fetchAnomalies = async () => {
    setLoading(true);
    try {
      const res = await api.getAnomalies({
        severity: severityFilter,
        status: statusFilter
      });
      setAlerts(res.alerts);
      setSeveritySummary(res.severity_summary || {});
      setStatusSummary(res.status_summary || {});
    } catch (err) {
      console.error('Failed to load anomalies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunDetection = async () => {
    setRunning(true);
    try {
      const res = await api.detectAnomalies(0.05);
      alert(`Anomaly detection completed! Scanned ${res.total_orders_scanned} orders and identified ${res.anomalies_detected_count} unusual transactions.`);
      fetchAnomalies();
    } catch (err: any) {
      alert('Detection failed: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  const handleStatusChange = async (alertId: number, newStatus: string) => {
    try {
      await api.updateAnomalyStatus(alertId, newStatus);
      setAlerts((prev) =>
        prev.map((a) => (a.alert_id === alertId ? { ...a, status: newStatus as any } : a))
      );
    } catch (err: any) {
      alert('Failed to update status: ' + err.message);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-rose-600 dark:text-rose-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <ShieldAlert className="w-4 h-4" />
            <span>Isolation Forest & Multi-Feature Outlier Pipeline</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Transaction Anomaly Detection
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Flags unusual transactions using Z-score statistical bounds and Scikit-Learn Isolation Forest.
            Each alert provides a transparent reason and an interactive investigation status workflow.
          </p>
        </div>

        <button
          onClick={handleRunDetection}
          disabled={running}
          className="flex items-center space-x-2 bg-rose-600 hover:bg-rose-700 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow-sm transition disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${running ? 'animate-spin' : ''}`} />
          <span>{running ? 'Scanning Orders...' : 'Scan All Transactions'}</span>
        </button>
      </div>

      {/* Disclaimer Banner */}
      <div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 rounded-xl p-3.5 flex items-start space-x-3 text-xs text-amber-800 dark:text-amber-300">
        <Info className="w-4 h-4 flex-shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
        <span>
          <strong>Important Review Notice:</strong> Anomalies indicate unusual transaction attributes (e.g. bulk volumes,
          off-pattern spending peaks) that deviate from regional averages. They serve as actionable operational leads for review,
          not conclusive proof of fraud.
        </span>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Critical Alerts</span>
          <div className="text-2xl font-bold text-rose-600 dark:text-rose-400 mt-1">
            {severitySummary['Critical'] || 0}
          </div>
          <span className="text-[11px] text-slate-500">Score &gt; 0.90 / extreme z-score</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">High Severity</span>
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">
            {severitySummary['High'] || 0}
          </div>
          <span className="text-[11px] text-slate-500">Substantial volume outlier</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Pending Review</span>
          <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">
            {statusSummary['Pending Review'] || 0}
          </div>
          <span className="text-[11px] text-slate-500">Awaiting investigator</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Resolved / Closed</span>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">
            {(statusSummary['Resolved'] || 0) + (statusSummary['Dismissed'] || 0)}
          </div>
          <span className="text-[11px] text-slate-500">Investigated alerts</span>
        </div>
      </div>

      {/* Alerts Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        {/* Table Filters */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none"
            >
              <option value="All">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider ml-2">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none"
            >
              <option value="All">All Statuses</option>
              <option value="Pending Review">Pending Review</option>
              <option value="Under Review">Under Review</option>
              <option value="Resolved">Resolved</option>
              <option value="Dismissed">Dismissed</option>
            </select>
          </div>

          <span className="text-xs text-slate-500">
            {alerts.length} alerts matching filter
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Order ID</th>
                <th className="py-3 px-4">Customer</th>
                <th className="py-3 px-4">Order Date</th>
                <th className="py-3 px-4">Score</th>
                <th className="py-3 px-4">Explanation & Reason</th>
                <th className="py-3 px-4">Review Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {alerts.map((a) => (
                <tr key={a.alert_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                  <td className="py-3.5 px-4">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                        a.severity === 'Critical'
                          ? 'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-400'
                          : a.severity === 'High'
                          ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400'
                          : 'bg-blue-50 text-blue-700 dark:bg-blue-950/50 dark:text-blue-400'
                      }`}
                    >
                      {a.severity}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold text-slate-900 dark:text-white">
                    #{a.order_id || 'N/A'}
                  </td>
                  <td className="py-3.5 px-4 font-medium text-slate-800 dark:text-slate-200">
                    {a.customer_name}
                  </td>
                  <td className="py-3.5 px-4 text-slate-500">
                    {a.order_date || 'N/A'}
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold text-indigo-600 dark:text-indigo-400">
                    {a.anomaly_score.toFixed(4)}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300 max-w-md">
                    {a.reason}
                  </td>
                  <td className="py-3.5 px-4">
                    <select
                      value={a.status}
                      onChange={(e) => handleStatusChange(a.alert_id, e.target.value)}
                      className="bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1 text-xs focus:outline-none"
                    >
                      <option value="Pending Review">Pending Review</option>
                      <option value="Under Review">Under Review</option>
                      <option value="Resolved">Resolved</option>
                      <option value="Dismissed">Dismissed</option>
                    </select>
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
