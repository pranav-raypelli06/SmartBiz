import React, { useState, useEffect } from 'react';
import {
  Truck,
  Search,
  Plus,
  Mail,
  Phone,
  MapPin,
  Package,
  AlertTriangle,
  CheckCircle,
  X,
  Edit2
} from 'lucide-react';
import { api } from '../lib/api';
import { SupplierItem, ProductItem } from '../types';

export const SupplierManagementPage: React.FC = () => {
  const [suppliers, setSuppliers] = useState<SupplierItem[]>([]);
  const [search, setSearch] = useState<string>('');
  const [cityFilter, setCityFilter] = useState<string>('');
  const [selectedSupplier, setSelectedSupplier] = useState<SupplierItem | null>(null);
  const [supplierProducts, setSupplierProducts] = useState<ProductItem[]>([]);
  const [showAddModal, setShowAddModal] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  // New Supplier Form State
  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [phone, setPhone] = useState<string>('');
  const [city, setCity] = useState<string>('');

  useEffect(() => {
    fetchSuppliers();
  }, [cityFilter]);

  const fetchSuppliers = async () => {
    setLoading(true);
    try {
      const data = await api.getSuppliers({ city: cityFilter });
      setSuppliers(data);
    } catch (err) {
      console.error('Failed to load suppliers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSupplier = async (sup: SupplierItem) => {
    setSelectedSupplier(sup);
    try {
      const allProds = await api.getProducts();
      const filtered = allProds.filter((p) => p.supplier_id === sup.supplier_id);
      setSupplierProducts(filtered);
    } catch (err) {
      console.error('Failed to load supplier products:', err);
    }
  };

  const handleCreateSupplier = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !phone || !city) {
      alert('All fields are required.');
      return;
    }
    try {
      await api.createSupplier({
        supplier_name: name,
        contact_email: email,
        phone,
        city,
        is_active: true
      });
      alert('Supplier registered successfully!');
      setShowAddModal(false);
      setName('');
      setEmail('');
      setPhone('');
      setCity('');
      fetchSuppliers();
    } catch (err: any) {
      alert('Failed to create supplier: ' + err.message);
    }
  };

  const filteredSuppliers = suppliers.filter(
    (s) =>
      s.supplier_name.toLowerCase().includes(search.toLowerCase()) ||
      s.contact_email.toLowerCase().includes(search.toLowerCase()) ||
      s.city.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Truck className="w-4 h-4" />
            <span>Procurement & Vendor Directory</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Supplier Management
          </h2>
          <p className="text-xs text-slate-500 max-w-xl mt-1">
            Maintain active supplier partnerships, inspect linked catalogues, review replenishment shortfalls,
            and create verified supplier accounts.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow-sm transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add New Supplier</span>
        </button>
      </div>

      {/* Search & Filters */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search suppliers by name or email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-50 dark:bg-slate-800 text-xs border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-200 focus:outline-none w-64"
            />
          </div>

          <select
            value={cityFilter}
            onChange={(e) => setCityFilter(e.target.value)}
            className="bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs focus:outline-none"
          >
            <option value="">All Supplier Cities</option>
            <option value="San Jose">San Jose</option>
            <option value="Chicago">Chicago</option>
            <option value="Austin">Austin</option>
            <option value="Seattle">Seattle</option>
            <option value="Denver">Denver</option>
            <option value="Los Angeles">Los Angeles</option>
            <option value="Boston">Boston</option>
            <option value="Atlanta">Atlanta</option>
            <option value="Dallas">Dallas</option>
            <option value="Phoenix">Phoenix</option>
            <option value="Portland">Portland</option>
          </select>
        </div>

        <span className="text-xs text-slate-500">
          {filteredSuppliers.length} active suppliers found
        </span>
      </div>

      {/* Supplier Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredSuppliers.map((s) => (
          <div
            key={s.supplier_id}
            onClick={() => handleSelectSupplier(s)}
            className={`bg-white dark:bg-slate-900 rounded-2xl border p-5 shadow-sm hover:shadow-md cursor-pointer transition-all ${
              selectedSupplier?.supplier_id === s.supplier_id
                ? 'border-indigo-600 ring-2 ring-indigo-500/20'
                : 'border-slate-200 dark:border-slate-800'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-base">
                  {s.supplier_name}
                </h3>
                <div className="flex items-center space-x-1 text-xs text-slate-500 mt-0.5">
                  <MapPin className="w-3 h-3 text-slate-400" />
                  <span>{s.city}</span>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400">
                Active
              </span>
            </div>

            <div className="space-y-1.5 text-xs text-slate-600 dark:text-slate-300 border-t border-slate-100 dark:border-slate-800/80 pt-3">
              <div className="flex items-center space-x-2">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                <span className="truncate">{s.contact_email}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-3.5 h-3.5 text-slate-400" />
                <span>{s.phone}</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 mt-3 border-t border-slate-100 dark:border-slate-800/80 text-xs">
              <div className="flex items-center space-x-1.5 text-slate-600 dark:text-slate-300 font-medium">
                <Package className="w-3.5 h-3.5 text-indigo-500" />
                <span>{s.products_count} Products</span>
              </div>
              {s.low_stock_products_count > 0 ? (
                <div className="flex items-center space-x-1 text-rose-600 dark:text-rose-400 font-semibold">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>{s.low_stock_products_count} Low Stock</span>
                </div>
              ) : (
                <div className="flex items-center space-x-1 text-emerald-600 dark:text-emerald-400 font-medium">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Stock OK</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Supplier Linked Products Drawer / Modal */}
      {selectedSupplier && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Products Supplied by {selectedSupplier.supplier_name}
              </h3>
              <p className="text-xs text-slate-500">
                Location: {selectedSupplier.city} • Email: {selectedSupplier.contact_email} • Phone: {selectedSupplier.phone}
              </p>
            </div>
            <button
              onClick={() => setSelectedSupplier(null)}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 font-semibold uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="py-2.5 px-3">Product Name</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3 text-right">Unit Cost</th>
                  <th className="py-2.5 px-3 text-right">Selling Price</th>
                  <th className="py-2.5 px-3 text-right">Margin %</th>
                  <th className="py-2.5 px-3 text-right">Stock Level</th>
                  <th className="py-2.5 px-3 text-right">Stock Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {supplierProducts.map((p) => (
                  <tr key={p.product_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                    <td className="py-3 px-3 font-semibold text-slate-900 dark:text-white">
                      {p.product_name}
                    </td>
                    <td className="py-3 px-3 text-slate-600 dark:text-slate-300">{p.category}</td>
                    <td className="py-3 px-3 text-right font-mono">${p.unit_cost.toFixed(2)}</td>
                    <td className="py-3 px-3 text-right font-mono font-semibold">${p.selling_price.toFixed(2)}</td>
                    <td className="py-3 px-3 text-right font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                      {p.margin_pct}%
                    </td>
                    <td className="py-3 px-3 text-right font-mono">{p.stock_quantity} units</td>
                    <td className="py-3 px-3 text-right">
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          p.stock_status === 'Adequate'
                            ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400'
                            : 'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-400'
                        }`}
                      >
                        {p.stock_status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Add Supplier Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xl max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Register New Supplier</h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateSupplier} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-slate-600 dark:text-slate-300 font-medium mb-1">Supplier / Company Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Apex Industrial Supplies"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-600 dark:text-slate-300 font-medium mb-1">Contact Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="orders@supplier.com"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-600 dark:text-slate-300 font-medium mb-1">Phone Number</label>
                <input
                  type="text"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+1-555-0199"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-600 dark:text-slate-300 font-medium mb-1">City / Region</label>
                <input
                  type="text"
                  required
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="e.g. Chicago"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none"
                />
              </div>

              <div className="pt-2 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow-sm transition"
                >
                  Save Supplier
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
