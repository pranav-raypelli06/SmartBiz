import React, { useState, useEffect } from 'react';
import {
  Database,
  Download,
  Upload,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  FileSpreadsheet,
  CheckCircle,
  AlertCircle,
  X
} from 'lucide-react';
import { api } from '../lib/api';

const TABLES = [
  'suppliers',
  'customers',
  'products',
  'orders',
  'inventory',
  'forecasts',
  'customer_segments',
  'anomaly_alerts',
  'algorithm_runs'
];

export const DataExplorerPage: React.FC = () => {
  const [activeTable, setActiveTable] = useState<string>('suppliers');
  const [dataStatus, setDataStatus] = useState<any>(null);
  const [tableRows, setTableRows] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [showImportModal, setShowImportModal] = useState<boolean>(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importing, setImporting] = useState<boolean>(false);

  useEffect(() => {
    fetchStatus();
  }, []);

  useEffect(() => {
    fetchTableData(activeTable);
  }, [activeTable]);

  const fetchStatus = async () => {
    try {
      const status = await api.getDataStatus();
      setDataStatus(status);
    } catch (err) {
      console.error('Failed to load status:', err);
    }
  };

  const fetchTableData = async (tbl: string) => {
    setLoading(true);
    try {
      if (tbl === 'suppliers') {
        const res = await api.getSuppliers();
        setTableRows(res);
      } else if (tbl === 'customers') {
        const res = await api.getCustomers({ limit: 50 });
        setTableRows(res.customers);
      } else if (tbl === 'products') {
        const res = await api.getProducts();
        setTableRows(res);
      } else if (tbl === 'orders') {
        const res = await api.getOrders({ limit: 50 });
        setTableRows(res.orders);
      } else if (tbl === 'inventory') {
        const res = await api.getInventory();
        setTableRows(res);
      } else if (tbl === 'forecasts') {
        const res = await api.getForecasts();
        setTableRows(res);
      } else if (tbl === 'customer_segments') {
        const res = await api.getCustomerSegments();
        setTableRows(res.customers || []);
      } else if (tbl === 'anomaly_alerts') {
        const res = await api.getAnomalies({ limit: 50 });
        setTableRows(res.alerts);
      } else if (tbl === 'algorithm_runs') {
        const res = await api.getAlgorithmRuns();
        setTableRows(res);
      }
    } catch (err) {
      console.error(`Failed to fetch table ${tbl}:`, err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    window.open(`/api/data/export/${activeTable}`, '_blank');
  };

  const handleImportSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!importFile) return;

    setImporting(true);
    const fd = new FormData();
    fd.append('table_name', activeTable);
    fd.append('file', importFile);

    try {
      const res = await fetch('/api/data/import', {
        method: 'POST',
        body: fd
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail || 'Import failed');

      alert(`Import Success: Inserted ${json.rows_inserted} rows into ${json.table}!`);
      setShowImportModal(false);
      setImportFile(null);
      fetchTableData(activeTable);
      fetchStatus();
    } catch (err: any) {
      alert('Import failed: ' + err.message);
    } finally {
      setImporting(false);
    }
  };

  const columns = tableRows.length > 0 ? Object.keys(tableRows[0]).filter((k) => k !== 'items') : [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Database className="w-4 h-4" />
            <span>Relational Schema & File Operations</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Data Explorer & CSV Pipelines
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Inspect raw relational records, download verified CSV exports, and validate incoming data batches against foreign keys.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportCSV}
            className="flex items-center space-x-1.5 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 px-3.5 py-2 rounded-xl text-xs font-semibold shadow-sm transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>

          {(activeTable === 'suppliers' || activeTable === 'customers') && (
            <button
              onClick={() => setShowImportModal(true)}
              className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-2 rounded-xl text-xs font-semibold shadow-sm transition"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Import CSV</span>
            </button>
          )}
        </div>
      </div>

      {/* Table Navigation Tabs */}
      <div className="flex overflow-x-auto space-x-2 pb-2 text-xs font-semibold">
        {TABLES.map((t) => {
          const count = dataStatus?.table_counts?.[t] ?? 0;
          return (
            <button
              key={t}
              onClick={() => setActiveTable(t)}
              className={`px-3.5 py-2 rounded-xl whitespace-nowrap transition flex items-center space-x-1.5 ${
                activeTable === t
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <span className="capitalize">{t.replace('_', ' ')}</span>
              <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${activeTable === t ? 'bg-indigo-700 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-500'}`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Table Data View */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider capitalize">
            Table: {activeTable.replace('_', ' ')} ({tableRows.length} displayed)
          </span>
          <span className="text-xs text-slate-400">
            Engine: MySQL 8.x InnoDB
          </span>
        </div>

        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/75 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800 sticky top-0">
              <tr>
                {columns.map((col) => (
                  <th key={col} className="py-3 px-4 capitalize">
                    {col.replace('_', ' ')}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {tableRows.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                  {columns.map((col) => {
                    const val = row[col];
                    const isNum = typeof val === 'number';
                    const isBool = typeof val === 'boolean';
                    return (
                      <td key={col} className={`py-3 px-4 ${isNum ? 'font-mono' : 'text-slate-800 dark:text-slate-200'}`}>
                        {isBool ? (
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${val ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
                            {val ? 'TRUE' : 'FALSE'}
                          </span>
                        ) : val !== null && val !== undefined ? (
                          String(val)
                        ) : (
                          <span className="text-slate-400 italic">null</span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* CSV Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xl max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white capitalize">
                Import CSV into {activeTable}
              </h3>
              <button
                onClick={() => setShowImportModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleImportSubmit} className="space-y-4 text-xs">
              <div className="p-4 border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl text-center cursor-pointer hover:border-indigo-500 transition">
                <FileSpreadsheet className="w-8 h-8 mx-auto text-indigo-500 mb-2" />
                <label className="block text-slate-700 dark:text-slate-300 font-medium mb-1 cursor-pointer">
                  {importFile ? importFile.name : 'Select or drop CSV file'}
                </label>
                <span className="text-[11px] text-slate-400">
                  Maximum file size: 5MB (UTF-8 formatted)
                </span>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="csv-file-input"
                />
                <div className="mt-3">
                  <label
                    htmlFor="csv-file-input"
                    className="inline-block px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 rounded-lg cursor-pointer transition"
                  >
                    Browse Files
                  </label>
                </div>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl text-[11px] text-slate-500 space-y-1">
                <div className="font-semibold text-slate-700 dark:text-slate-300">Expected Columns for {activeTable}:</div>
                {activeTable === 'suppliers' && (
                  <div>supplier_name, contact_email, phone, city</div>
                )}
                {activeTable === 'customers' && (
                  <div>customer_name, email, city</div>
                )}
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowImportModal(false)}
                  className="px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-600 dark:text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!importFile || importing}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow-sm transition disabled:opacity-50"
                >
                  {importing ? 'Validating & Importing...' : 'Upload & Persist'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
