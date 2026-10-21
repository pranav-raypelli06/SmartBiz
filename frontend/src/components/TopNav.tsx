import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Search, Database, Sun, Moon, RefreshCw, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';
import { api } from '../lib/api';
import { HealthStatus } from '../types';

interface TopNavProps {
  sidebarCollapsed: boolean;
  onRefresh?: () => void;
}

const routeTitles: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Executive Overview Dashboard', subtitle: 'Real-time sales, profitability, and operational key metrics.' },
  '/sales': { title: 'Sales & Revenue Analytics', subtitle: 'Category trends, regional distributions, and product revenue rankings.' },
  '/customers': { title: 'Customer Intelligence & RFM', subtitle: 'Machine learning customer segmentation using K-Means.' },
  '/forecasting': { title: 'Demand Forecasting Engine', subtitle: 'Time-series sales predictions with confidence intervals and backtesting.' },
  '/inventory': { title: 'Inventory Optimization', subtitle: 'Decision-support stock recommendations using Greedy & 0/1 Knapsack DP.' },
  '/anomalies': { title: 'Transaction Anomaly Detection', subtitle: 'Statistical outlier scoring and Isolation Forest transaction review.' },
  '/suppliers': { title: 'Supplier Directory & Management', subtitle: 'Manage active suppliers, product linkages, and replenishment orders.' },
  '/algorithm-lab': { title: 'Algorithm Lab (AoA Benchmark)', subtitle: 'Manual algorithm implementations, empirical benchmarking, and Big-O verification.' },
  '/data-explorer': { title: 'Data Explorer & CSV Operations', subtitle: 'Inspect, filter, export, and import relational database records.' },
  '/settings': { title: 'System Health & Settings', subtitle: 'Database connectivity status, MySQL table statistics, and environment config.' }
};

export const TopNav: React.FC<TopNavProps> = ({ sidebarCollapsed, onRefresh }) => {
  const location = useLocation();
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    return document.documentElement.classList.contains('dark') ||
      window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [seeding, setSeeding] = useState(false);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const data = await api.getHealth();
      setHealth(data);
    } catch {
      setHealth(null);
    }
  };

  const toggleDarkMode = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add('dark');
      setIsDarkMode(true);
    }
  };

  const handleSeedDemoData = async () => {
    if (confirm('Re-seed database with clean synthetic retail demo data?')) {
      setSeeding(true);
      try {
        await api.seedDemoData(true);
        alert('Demo data seeded successfully!');
        if (onRefresh) onRefresh();
        window.location.reload();
      } catch (err: any) {
        alert('Seeding error: ' + err.message);
      } finally {
        setSeeding(false);
      }
    }
  };

  const currentRoute = routeTitles[location.pathname] || {
    title: 'SmartBiz Analytics',
    subtitle: 'Integrated Data Science & Algorithms Platform'
  };

  return (
    <header
      className={`fixed top-0 right-0 z-30 h-16 transition-all duration-300 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-6 ${
        sidebarCollapsed ? 'left-20' : 'left-64'
      }`}
    >
      {/* Title & Breadcrumb */}
      <div className="flex flex-col">
        <h1 className="text-base font-bold text-slate-800 dark:text-white leading-tight">
          {currentRoute.title}
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 hidden sm:block">
          {currentRoute.subtitle}
        </p>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Database Status Pill */}
        <div
          className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
            health?.database_connected
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800'
              : 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800'
          }`}
          title={
            health?.database_connected
              ? `Connected to ${health.database_type} (${health.database_name} on port ${health.database_port}) - ${health.tables_found} tables active.`
              : 'Database Disconnected'
          }
        >
          {health?.database_connected ? (
            <>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <Database className="w-3.5 h-3.5" />
              <span className="hidden md:inline font-semibold">MySQL 8.x: Connected</span>
            </>
          ) : (
            <>
              <AlertTriangle className="w-3.5 h-3.5 text-rose-500" />
              <span className="hidden md:inline">MySQL Offline</span>
            </>
          )}
        </div>

        {/* Load Demo Data Quick Action */}
        <button
          onClick={handleSeedDemoData}
          disabled={seeding}
          className="flex items-center space-x-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 dark:bg-indigo-950/50 dark:hover:bg-indigo-900/50 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${seeding ? 'animate-spin' : ''}`} />
          <span className="hidden sm:inline">{seeding ? 'Seeding...' : 'Reset Demo Data'}</span>
        </button>

        {/* Swagger Docs Link */}
        <a
          href="http://127.0.0.1:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="p-2 rounded-lg text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          title="FastAPI Swagger Documentation (/docs)"
        >
          <ExternalLink className="w-4 h-4" />
        </a>

        {/* Theme Toggle */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-lg text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {isDarkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
        </button>
      </div>
    </header>
  );
};
