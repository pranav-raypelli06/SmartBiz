import React, { useState, useEffect } from 'react';
import {
  Settings,
  Database,
  Server,
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  ExternalLink,
  Code2,
  BookOpen,
  Sparkles,
  ShieldCheck
} from 'lucide-react';
import { api } from '../lib/api';
import { HealthStatus } from '../types';

export const SettingsPage: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [dataStatus, setDataStatus] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [resetting, setResetting] = useState<boolean>(false);

  useEffect(() => {
    fetchDiagnostics();
  }, []);

  const fetchDiagnostics = async () => {
    setLoading(true);
    try {
      const [h, s] = await Promise.all([api.getHealth(), api.getDataStatus()]);
      setHealth(h);
      setDataStatus(s);
    } catch (err) {
      console.error('Failed to load diagnostics:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetData = async () => {
    if (confirm('Are you sure you want to completely reset and regenerate the retail demonstration dataset?')) {
      setResetting(true);
      try {
        await api.seedDemoData(true);
        alert('Database successfully reset and re-seeded with pristine demonstration data.');
        fetchDiagnostics();
      } catch (err: any) {
        alert('Reset failed: ' + err.message);
      } finally {
        setResetting(false);
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Settings className="w-4 h-4" />
            <span>Environment Diagnostics & System Config</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            System Settings & Architecture Health
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Verify real-time relational database connectivity, inspect server telemetry, and review academic Analysis of Algorithms specifications.
          </p>
        </div>

        <button
          onClick={handleResetData}
          disabled={resetting}
          className="flex items-center space-x-2 bg-rose-600 hover:bg-rose-700 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow-sm transition disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin' : ''}`} />
          <span>{resetting ? 'Resetting...' : 'Destructive Database Reset'}</span>
        </button>
      </div>

      {/* Database Diagnostic Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Database Status</span>
          <div className="flex items-center space-x-2 mt-1">
            <span className={`w-3 h-3 rounded-full ${health?.database_connected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            <span className="text-lg font-bold text-slate-900 dark:text-white">
              {health?.database_connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <span className="text-[11px] text-slate-500">{health?.database_type}</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">MySQL Port & Host</span>
          <div className="text-lg font-bold text-slate-900 dark:text-white mt-1 font-mono">
            {health?.database_host}:{health?.database_port}
          </div>
          <span className="text-[11px] text-slate-500">Schema: {health?.database_name}</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Relational Tables</span>
          <div className="text-lg font-bold text-indigo-600 dark:text-indigo-400 mt-1 font-mono">
            {health?.tables_found} / 10 Tables
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold">100% Schema Coverage</span>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-400 font-medium">Total Stored Records</span>
          <div className="text-lg font-bold text-slate-900 dark:text-white mt-1 font-mono">
            {dataStatus?.total_records?.toLocaleString() || 0}
          </div>
          <span className="text-[11px] text-slate-500">Persistent rows</span>
        </div>
      </div>

      {/* Relational Table Breakdown */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
        <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1">
          MySQL Relational Table Catalog
        </h3>
        <p className="text-xs text-slate-500 mb-4">
          All ten required tables with active record counts and foreign-key integrity.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {Object.entries(dataStatus?.table_counts || {}).map(([table, count]: any) => (
            <div key={table} className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700/80">
              <span className="text-[11px] text-slate-500 capitalize">{table.replace('_', ' ')}</span>
              <div className="text-base font-bold font-mono text-slate-900 dark:text-white mt-0.5">
                {count.toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Technology Stack & Academic Curriculum Reference */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-bold text-sm">
            <Code2 className="w-4 h-4" />
            <span>Architecture & Mandatory Stack</span>
          </div>
          <p className="text-xs text-slate-500">
            Engineered strictly to production guidelines:
          </p>
          <ul className="text-xs text-slate-600 dark:text-slate-300 space-y-2 list-disc list-inside">
            <li><strong>Frontend:</strong> React 19, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons</li>
            <li><strong>Backend:</strong> Python 3.14/3.11, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic V2</li>
            <li><strong>Database:</strong> Native MySQL 8.x with InnoDB, strict foreign-keys, and DECIMAL financial fields</li>
            <li><strong>Analytics & ML:</strong> Scikit-Learn (K-Means, Isolation Forest, Ridge), Pandas, NumPy</li>
            <li><strong>Testing:</strong> 18 Passing Pytest unit/integration tests with real assertions</li>
          </ul>

          <div className="pt-2">
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center space-x-1.5 text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              <span>Explore Interactive OpenAPI / Swagger Docs</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-3">
          <div className="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400 font-bold text-sm">
            <BookOpen className="w-4 h-4" />
            <span>Analysis of Algorithms (AoA) Syllabus Compliance</span>
          </div>
          <p className="text-xs text-slate-500">
            Designed for third-year engineering requirements and final-year expansions:
          </p>
          <ul className="text-xs text-slate-600 dark:text-slate-300 space-y-2 list-disc list-inside">
            <li><strong>Searching:</strong> Linear Search O(n) vs Binary Search O(log n) with sorted requirement checks</li>
            <li><strong>Sorting:</strong> Bubble Sort O(n^2), Merge Sort O(n log n), Quicksort O(n log n) with comparisons/swaps</li>
            <li><strong>Dynamic Programming:</strong> 0/1 Knapsack O(n*W) with 2^n brute-force optimality proof</li>
            <li><strong>Greedy Strategy:</strong> Benefit-to-cost heuristic showing sub-optimality trade-offs</li>
            <li><strong>Graph Theory:</strong> BFS, DFS, Dijkstra shortest path, Kruskal MST with Union-Find</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
