import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Tabs } from '../../components/ui/Tabs';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { useAuth } from '../../lib/auth';
import { Navigate } from 'react-router-dom';
import { Shield, FlaskConical, ShoppingBag, Database, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const AdminPortal: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('ingredients');
  const [ingredients, setIngredients] = useState<any[]>([]);
  const [stats, setStats] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Guard: only admin/nutritionist roles
  if (user?.role !== 'admin' && user?.role !== 'nutritionist') {
    return <Navigate to="/app" replace />;
  }

  useEffect(() => {
    const fetchAdmin = async () => {
      try {
        const [ingRes, statsRes, ordersRes] = await Promise.all([
          api.get('/admin/ingredients'),
          api.get('/admin/statistics'),
          api.get('/admin/orders'),
        ]);
        setIngredients(ingRes.data || []);
        setStats(statsRes.data || []);
        setOrders(ordersRes.data || []);
      } finally {
        setLoading(false);
      }
    };
    fetchAdmin();
  }, []);

  const handleVerifyIngredient = async (id: string) => {
    await api.patch(`/admin/ingredients/${id}`, { verification_status: 'verified' });
    setIngredients((prev) => prev.map((ing) => ing.id === id ? { ...ing, verification_status: 'verified' } : ing));
  };

  const handlePublishStat = async (id: string) => {
    await api.patch(`/admin/statistics/${id}`, { is_published: true });
    setStats((prev) => prev.map((s) => s.id === id ? { ...s, is_published: true } : s));
  };

  const tabs = [
    { id: 'ingredients', label: 'Ingredients DB' },
    { id: 'statistics', label: 'Survey Statistics' },
    { id: 'orders', label: 'Demo Orders' },
    { id: 'audit', label: 'Audit Trail' },
  ];

  if (loading) return <div className="h-64 bg-gray-200 rounded-2xl animate-pulse" />;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-primary-100">
          <Shield className="w-5 h-5 text-primary-700" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-gray-900">Admin Portal</h1>
          <p className="text-xs text-gray-500">Manage ingredients, verify statistics, and monitor demo orders.</p>
        </div>
        <Badge variant="outline" className="ml-auto text-primary-700 border-primary-300 bg-primary-50">
          {user?.role?.toUpperCase()}
        </Badge>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      {/* Ingredients Tab */}
      {activeTab === 'ingredients' && (
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
              <Database className="w-4 h-4 text-teal-600" />
              IFCT 2017 Ingredient Database ({ingredients.length} records)
            </h3>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Ingredient Name</TableHead>
                <TableHead>Iron (mg/100g)</TableHead>
                <TableHead>Vit C (mg/100g)</TableHead>
                <TableHead>Diet Class</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ingredients.slice(0, 20).map((ing: any) => (
                <TableRow key={ing.id}>
                  <TableCell className="font-medium text-gray-900">{ing.name}</TableCell>
                  <TableCell className="font-mono text-primary-700">{ing.iron_mg_per_100g?.toFixed(2)}</TableCell>
                  <TableCell className="font-mono text-teal-700">{ing.vitamin_c_mg_per_100g?.toFixed(1)}</TableCell>
                  <TableCell className="capitalize">{ing.diet_class}</TableCell>
                  <TableCell>
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                      ing.verification_status === 'verified' ? 'bg-emerald-100 text-emerald-800' :
                      ing.verification_status === 'draft' ? 'bg-amber-100 text-amber-800' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {ing.verification_status}
                    </span>
                  </TableCell>
                  <TableCell>
                    {ing.verification_status !== 'verified' && (
                      <Button variant="ghost" size="sm" onClick={() => handleVerifyIngredient(ing.id)} className="text-xs text-primary-600">
                        <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Verify
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}

      {/* Survey Statistics Tab */}
      {activeTab === 'statistics' && (
        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
            <FlaskConical className="w-4 h-4 text-primary-600" />
            Survey Statistics (NFHS/CNNS Data)
          </h3>
          <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <span>Only verified and published statistics are visible to end users on the public home page. Review source data before publishing.</span>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Metric</TableHead>
                <TableHead>Value</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Year</TableHead>
                <TableHead>Published</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {stats.map((s: any) => (
                <TableRow key={s.id}>
                  <TableCell className="font-medium text-gray-900">{s.metric_name}</TableCell>
                  <TableCell className="font-mono font-bold text-gray-900">{s.value}{s.unit}</TableCell>
                  <TableCell>{s.source}</TableCell>
                  <TableCell>{s.year}</TableCell>
                  <TableCell>
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${s.is_published ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-700'}`}>
                      {s.is_published ? 'Published' : 'Draft'}
                    </span>
                  </TableCell>
                  <TableCell>
                    {!s.is_published && (
                      <Button variant="ghost" size="sm" onClick={() => handlePublishStat(s.id)} className="text-xs text-primary-600">
                        Publish
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}

      {/* Orders Tab */}
      {activeTab === 'orders' && (
        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
            <ShoppingBag className="w-4 h-4 text-purple-600" />
            Demo Order Monitoring
          </h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Order ID</TableHead>
                <TableHead>User</TableHead>
                <TableHead>Total (₹)</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Placed At</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {orders.map((o: any) => (
                <TableRow key={o.id}>
                  <TableCell className="font-mono text-xs">{o.id.slice(0, 8)}</TableCell>
                  <TableCell>{o.user_email}</TableCell>
                  <TableCell>₹{o.total_inr} (Demo)</TableCell>
                  <TableCell><span className="capitalize text-xs text-gray-700">{o.status}</span></TableCell>
                  <TableCell className="text-gray-500 text-xs">{new Date(o.created_at).toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}

      {/* Audit Trail Tab */}
      {activeTab === 'audit' && (
        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-gray-900">Audit Trail</h3>
          <p className="text-sm text-gray-600">
            All significant system actions (formulation generation, safety gate decisions, consent changes, account deletions) are logged to the audit trail in the backend database with timestamps, user IDs, and action details.
            Full audit log is available via the backend admin API (<code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">/api/v1/admin/audit</code>).
          </p>
          <Button variant="outline" size="sm" onClick={() => window.open('/api/v1/admin/audit', '_blank')}>
            View Raw Audit Log (API)
          </Button>
        </Card>
      )}
    </div>
  );
};

