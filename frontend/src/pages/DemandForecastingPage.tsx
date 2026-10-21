import React, { useState, useEffect } from 'react';
import {
  LineChart as ChartIcon,
  Play,
  RefreshCw,
  TrendingUp,
  AlertCircle,
  Calendar,
  CheckCircle2,
  Sparkles
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { api } from '../lib/api';
import { ProductItem } from '../types';

export const DemandForecastingPage: React.FC = () => {
  const [products, setProducts] = useState<ProductItem[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<number>(1);
  const [horizonDays, setHorizonDays] = useState<number>(14);
  const [modelType, setModelType] = useState<string>('Moving-Average');
  const [forecastData, setForecastData] = useState<any>(null);
  const [running, setRunning] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const prods = await api.getProducts();
      setProducts(prods);
      if (prods.length > 0) {
        setSelectedProductId(prods[0].product_id);
        runForecast(prods[0].product_id, horizonDays, modelType);
      }
    } catch (err) {
      console.error('Failed to load products:', err);
    } finally {
      setLoading(false);
    }
  };

  const runForecast = async (productId: number, horizon: number, model: string) => {
    setRunning(true);
    try {
      const res = await api.runForecast(productId, horizon, model);
      setForecastData(res);
    } catch (err: any) {
      alert('Forecasting error: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  // Combine historical trend and forecasts for continuous chart plotting
  const combinedChartData = [];
  if (forecastData?.historical_trend) {
    for (const h of forecastData.historical_trend) {
      combinedChartData.push({
        date: h.date,
        actual: h.quantity,
        predicted: null,
        lower: null,
        upper: null,
        type: 'Historical'
      });
    }
  }
  if (forecastData?.forecasts) {
    for (const f of forecastData.forecasts) {
      combinedChartData.push({
        date: f.forecast_date,
        actual: null,
        predicted: f.predicted_quantity,
        lower: f.lower_bound,
        upper: f.upper_bound,
        type: 'Forecast'
      });
    }
  }

  return (
    <div className="space-y-6">
      {/* Control Card */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4" />
            <span>Time-Series Predictive Demand Model</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Product Demand Forecasting Engine
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Generates statistical demand forecasts using actual chronological sales data, evaluated via backtesting
            MAE (Mean Absolute Error) and RMSE with confidence boundaries.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex flex-col">
            <label className="text-[11px] text-slate-500 font-medium mb-1">Select Product</label>
            <select
              value={selectedProductId}
              onChange={(e) => setSelectedProductId(Number(e.target.value))}
              className="bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none max-w-xs"
            >
              {products.map((p) => (
                <option key={p.product_id} value={p.product_id}>
                  {p.product_name} ({p.category})
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col">
            <label className="text-[11px] text-slate-500 font-medium mb-1">Horizon</label>
            <select
              value={horizonDays}
              onChange={(e) => setHorizonDays(Number(e.target.value))}
              className="bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none"
            >
              <option value={7}>7 Days Ahead</option>
              <option value={14}>14 Days Ahead</option>
              <option value={30}>30 Days Ahead</option>
            </select>
          </div>

          <div className="flex flex-col">
            <label className="text-[11px] text-slate-500 font-medium mb-1">Forecasting Model</label>
            <select
              value={modelType}
              onChange={(e) => setModelType(e.target.value)}
              className="bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none"
            >
              <option value="Moving-Average">Moving-Average (7D)</option>
              <option value="Naive">Naive Baseline</option>
              <option value="Scikit-Learn Regression">Scikit-Learn Lag Regression</option>
            </select>
          </div>

          <div className="flex flex-col justify-end">
            <label className="text-[11px] text-transparent mb-1">Run</label>
            <button
              onClick={() => runForecast(selectedProductId, horizonDays, modelType)}
              disabled={running}
              className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 rounded-xl text-xs font-semibold shadow-sm transition disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 ${running ? 'animate-spin' : ''}`} />
              <span>{running ? 'Predicting...' : 'Generate'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Model Performance & Evaluation Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-500 font-medium">Selected Product</span>
          <div className="text-base font-bold text-slate-900 dark:text-white mt-1 truncate">
            {forecastData?.product_name || 'Loading...'}
          </div>
          <div className="text-xs text-indigo-600 dark:text-indigo-400 mt-1 font-semibold">
            {forecastData?.category || ''}
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-500 font-medium">Active Model</span>
          <div className="text-base font-bold text-slate-900 dark:text-white mt-1">
            {forecastData?.model_name || modelType}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Horizon: {forecastData?.horizon_days || horizonDays} days
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-500 font-medium">Mean Absolute Error (MAE)</span>
          <div className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-1">
            {forecastData?.metrics?.mae != null ? `${forecastData.metrics.mae} units` : 'N/A'}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Backtest residual mean error
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
          <span className="text-xs text-slate-500 font-medium">Root Mean Squared Error (RMSE)</span>
          <div className="text-base font-bold text-blue-600 dark:text-blue-400 mt-1">
            {forecastData?.metrics?.rmse != null ? `${forecastData.metrics.rmse} units` : 'N/A'}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Penalizes large outlier errors
          </div>
        </div>
      </div>

      {/* Main Forecast Chart */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-800 dark:text-white text-base">
              Actual Demand vs Forecast Horizon
            </h3>
            <p className="text-xs text-slate-500">
              Historical sales trend (blue line) alongside predicted future demand with 90% confidence bounds (green band).
            </p>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={combinedChartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              {/* Confidence Band */}
              <Area type="monotone" dataKey="upper" name="Upper Bound (90% Conf)" fill="#10b981" stroke="none" fillOpacity={0.15} />
              <Area type="monotone" dataKey="lower" name="Lower Bound" fill="#ffffff" stroke="none" fillOpacity={0.1} />
              {/* Actual Line */}
              <Line type="monotone" dataKey="actual" name="Actual Daily Demand" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 2 }} />
              {/* Forecast Line */}
              <Line type="monotone" dataKey="predicted" name="Predicted Demand" stroke="#10b981" strokeWidth={2.5} strokeDasharray="4 4" dot={{ r: 3 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Forecast Output Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Persisted Predictions for {forecastData?.product_name || 'Selected Item'} ({forecastData?.forecasts?.length || 0} Days Ahead)
        </div>
        <div className="overflow-x-auto max-h-72">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800 sticky top-0">
              <tr>
                <th className="py-3 px-4">Forecast Date</th>
                <th className="py-3 px-4">Applied Model</th>
                <th className="py-3 px-4 text-right">Predicted Demand</th>
                <th className="py-3 px-4 text-right">Lower Bound (90%)</th>
                <th className="py-3 px-4 text-right">Upper Bound (90%)</th>
                <th className="py-3 px-4 text-right">Confidence Spread</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {(forecastData?.forecasts || []).map((f: any, idx: number) => {
                const spread = (f.upper_bound - f.lower_bound).toFixed(2);
                return (
                  <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-medium text-slate-800 dark:text-slate-200">
                      {f.forecast_date}
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">
                      {f.model_name}
                    </td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600 dark:text-emerald-400">
                      {f.predicted_quantity} units
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-500">
                      {f.lower_bound} units
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-500">
                      {f.upper_bound} units
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-600 dark:text-slate-400">
                      ±{(Number(spread) / 2).toFixed(1)}
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
