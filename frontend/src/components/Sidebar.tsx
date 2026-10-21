import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  TrendingUp,
  Users,
  LineChart,
  Boxes,
  ShieldAlert,
  Truck,
  Cpu,
  Database,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const navItems = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Sales Analytics', path: '/sales', icon: TrendingUp },
  { name: 'Customer Intelligence', path: '/customers', icon: Users },
  { name: 'Demand Forecasting', path: '/forecasting', icon: LineChart },
  { name: 'Inventory Optimization', path: '/inventory', icon: Boxes },
  { name: 'Anomaly Detection', path: '/anomalies', icon: ShieldAlert },
  { name: 'Supplier Management', path: '/suppliers', icon: Truck },
  { name: 'Algorithm Lab', path: '/algorithm-lab', icon: Cpu },
  { name: 'Data Explorer', path: '/data-explorer', icon: Database },
  { name: 'Settings & Health', path: '/settings', icon: Settings },
];

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggle }) => {
  return (
    <aside
      className={`fixed top-0 left-0 z-40 h-screen transition-all duration-300 ease-in-out border-r border-slate-800 bg-[#0b1120] text-slate-300 flex flex-col ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-slate-800/80">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-indigo-500/20 flex-shrink-0">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-bold text-lg text-white tracking-tight leading-tight">
                SmartBiz
              </span>
              <span className="text-xs text-indigo-400 font-medium tracking-wide uppercase">
                Analytics
              </span>
            </div>
          )}
        </div>
        <button
          onClick={onToggle}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation List */}
      <div className="flex-1 py-4 px-3 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`
            }
          >
            <item.icon className={`w-5 h-5 flex-shrink-0`} />
            {!collapsed && <span className="truncate">{item.name}</span>}
          </NavLink>
        ))}
      </div>

      {/* Footer Tagline */}
      {!collapsed && (
        <div className="p-4 border-t border-slate-800/80 text-xs text-slate-500 text-center">
          Turn Business Data Into Smarter Decisions.
        </div>
      )}
    </aside>
  );
};
