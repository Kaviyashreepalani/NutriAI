import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Tabs } from '../../components/ui/Tabs';
import { Button } from '../../components/ui/Button';
import { EmptyState } from '../../components/ui/EmptyState';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { FlaskConical, FileText, ShoppingBag, Activity, ArrowRight, Download, History } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('formulations');
  const [data, setData] = useState<Record<string, any[]>>({
    formulations: [],
    reports: [],
    orders: [],
    logs: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const [forms, reports, orders, logs] = await Promise.all([
          api.get('/formulations').then(r => r.data),
          api.get('/reports').then(r => r.data),
          api.get('/orders').then(r => r.data),
          api.get('/progress/logs').then(r => r.data),
        ]);
        setData({ formulations: forms || [], reports: reports || [], orders: orders || [], logs: logs || [] });
      } catch {
        // graceful degradation
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const tabs = [
    { id: 'formulations', label: 'Generated Products', icon: <FlaskConical className="w-4 h-4" /> },
    { id: 'reports', label: 'Uploaded Reports', icon: <FileText className="w-4 h-4" /> },
    { id: 'orders', label: 'Demo Orders', icon: <ShoppingBag className="w-4 h-4" /> },
    { id: 'logs', label: 'Progress Logs', icon: <Activity className="w-4 h-4" /> },
  ];

  if (loading) return <div className="h-64 bg-gray-200 rounded-2xl animate-pulse" />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2.5">
            <History className="w-6 h-6 text-primary-600" />
            History
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Review your past generated food products, uploaded lab reports, and demo orders.
          </p>
        </div>
        <PrototypeBadge />
      </div>

      <Tabs
        tabs={tabs.map(t => ({ id: t.id, label: t.label }))}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      {/* Generated Formulations */}
      {activeTab === 'formulations' && (
        data.formulations.length === 0 ? (
          <EmptyState
            icon={<FlaskConical className="w-10 h-10 text-gray-400" />}
            title="No formulations yet"
            description="Generate your first personalized food product."
            action={<Link to="/app/generate"><Button variant="primary">Generate Formulation</Button></Link>}
          />
        ) : (
          <div className="space-y-3">
            {data.formulations.map((f: any) => (
              <Card key={f.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <FlaskConical className="w-4 h-4 text-primary-500" />
                    <h3 className="text-sm font-bold text-gray-900">{f.product_name}</h3>
                    <PrototypeBadge />
                  </div>
                  <p className="text-xs text-gray-500">
                    {f.format} • Iron: {f.iron_mg} mg • Cost: ₹{f.cost_inr} • {new Date(f.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Link to={`/app/results?formulation_id=${f.id}`}>
                    <Button variant="outline" size="sm">View <ArrowRight className="w-3.5 h-3.5 ml-1" /></Button>
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        )
      )}

      {/* Uploaded Reports */}
      {activeTab === 'reports' && (
        data.reports.length === 0 ? (
          <EmptyState
            icon={<FileText className="w-10 h-10 text-gray-400" />}
            title="No reports uploaded"
            description="Upload a lab report to begin."
            action={<Link to="/app/generate"><Button variant="primary">Upload Report</Button></Link>}
          />
        ) : (
          <div className="space-y-3">
            {data.reports.map((r: any) => (
              <Card key={r.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-teal-500" />
                    <h3 className="text-sm font-bold text-gray-900">{r.original_filename}</h3>
                  </div>
                  <p className="text-xs text-gray-500">
                    Status: <span className={`font-semibold ${r.ocr_status === 'confirmed' ? 'text-emerald-600' : r.ocr_status === 'failed' ? 'text-red-600' : 'text-amber-600'}`}>{r.ocr_status}</span>
                    {' '}• Lab: {r.lab_name || 'Unknown'} • {new Date(r.uploaded_at).toLocaleDateString()}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        )
      )}

      {/* Demo Orders */}
      {activeTab === 'orders' && (
        data.orders.length === 0 ? (
          <EmptyState
            icon={<ShoppingBag className="w-10 h-10 text-gray-400" />}
            title="No demo orders"
            description="Place a demo order from the prototype shop."
            action={<Link to="/app/shop"><Button variant="primary">Browse Shop</Button></Link>}
          />
        ) : (
          <div className="space-y-3">
            {data.orders.map((o: any) => (
              <Card key={o.id} className="p-4 flex items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <ShoppingBag className="w-4 h-4 text-purple-500" />
                    <code className="text-xs font-mono bg-gray-100 px-1.5 py-0.5 rounded">{o.id.slice(0, 8)}</code>
                    <PrototypeBadge />
                    <span className="text-xs text-gray-500 capitalize">{o.status}</span>
                  </div>
                  <p className="text-xs text-gray-500">₹{o.total_inr} (Demo) • {new Date(o.created_at).toLocaleDateString()}</p>
                </div>
                <Link to={`/app/orders/${o.id}`}>
                  <Button variant="outline" size="sm">Details</Button>
                </Link>
              </Card>
            ))}
          </div>
        )
      )}

      {/* Progress Logs */}
      {activeTab === 'logs' && (
        data.logs.length === 0 ? (
          <EmptyState
            icon={<Activity className="w-10 h-10 text-gray-400" />}
            title="No logs yet"
            description="Start logging daily servings from the Progress page."
            action={<Link to="/app/progress"><Button variant="primary">Go to Progress</Button></Link>}
          />
        ) : (
          <div className="space-y-2">
            {data.logs.map((log: any, idx: number) => (
              <div key={idx} className="p-3 rounded-xl bg-white border border-gray-200 flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-primary-500" />
                  <span className="font-medium text-gray-900">{log.date}</span>
                  <span className="text-gray-500">— {log.servings} serving(s)</span>
                </div>
                <span className="text-xs text-gray-400">{log.product_name}</span>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
};

