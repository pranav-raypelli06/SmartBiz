import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';
import { OverviewPage } from './pages/OverviewPage';
import { SalesAnalyticsPage } from './pages/SalesAnalyticsPage';
import { CustomerIntelligencePage } from './pages/CustomerIntelligencePage';
import { DemandForecastingPage } from './pages/DemandForecastingPage';
import { InventoryOptimizationPage } from './pages/InventoryOptimizationPage';
import { AnomalyDetectionPage } from './pages/AnomalyDetectionPage';
import { SupplierManagementPage } from './pages/SupplierManagementPage';
import { AlgorithmLabPage } from './pages/AlgorithmLabPage';
import { DataExplorerPage } from './pages/DataExplorerPage';
import { SettingsPage } from './pages/SettingsPage';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<OverviewPage />} />
          <Route path="sales" element={<SalesAnalyticsPage />} />
          <Route path="customers" element={<CustomerIntelligencePage />} />
          <Route path="forecasting" element={<DemandForecastingPage />} />
          <Route path="inventory" element={<InventoryOptimizationPage />} />
          <Route path="anomalies" element={<AnomalyDetectionPage />} />
          <Route path="suppliers" element={<SupplierManagementPage />} />
          <Route path="algorithm-lab" element={<AlgorithmLabPage />} />
          <Route path="data-explorer" element={<DataExplorerPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
