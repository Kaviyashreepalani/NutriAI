import React, { useEffect, useState } from 'react';
import { useAuth } from '../../lib/auth';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Tabs } from '../../components/ui/Tabs';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Modal } from '../../components/ui/Modal';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { User, Scale, Utensils, AlertTriangle, Heart, Plus, CheckCircle2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('personal');
  const [profile, setProfile] = useState<any>(null);
  const [measurements, setMeasurements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [showMeasModal, setShowMeasModal] = useState(false);
  const [newMeas, setNewMeas] = useState({ height_cm: '', weight_kg: '', measured_on: new Date().toISOString().split('T')[0] });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const [profileRes, measRes] = await Promise.all([
          api.get('/profile'),
          api.get('/profile/measurements'),
        ]);
        setProfile(profileRes.data);
        setMeasurements(measRes.data || []);
      } catch {
        setProfile({});
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSavePersonal = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.patch('/profile', profile);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } finally {
      setSaving(false);
    }
  };

  const handleAddMeasurement = async () => {
    try {
      const res = await api.post('/profile/measurements', {
        height_cm: parseFloat(newMeas.height_cm),
        weight_kg: parseFloat(newMeas.weight_kg),
        measured_on: newMeas.measured_on,
        source: 'self_reported',
      });
      setMeasurements((prev) => [res.data, ...prev]);
      setShowMeasModal(false);
      setNewMeas({ height_cm: '', weight_kg: '', measured_on: new Date().toISOString().split('T')[0] });
    } catch {
      // silent
    }
  };

  const tabs = [
    { id: 'personal', label: 'Personal', icon: <User className="w-4 h-4" /> },
    { id: 'physical', label: 'Physical', icon: <Scale className="w-4 h-4" /> },
    { id: 'diet', label: 'Diet & Allergies', icon: <Utensils className="w-4 h-4" /> },
    { id: 'health', label: 'Health Info', icon: <Heart className="w-4 h-4" /> },
  ];

  if (loading) return <div className="h-96 bg-gray-200 rounded-2xl animate-pulse" />;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2.5">
          <User className="w-6 h-6 text-primary-600" />
          User Info & Profile
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          View and update your personal information, physiology, dietary preferences, and health data.
        </p>
      </div>

      <Tabs tabs={tabs.map(t => ({ id: t.id, label: t.label }))} activeTab={activeTab} onChange={setActiveTab} />

      {/* Personal Tab */}
      {activeTab === 'personal' && (
        <Card className="p-5">
          <form onSubmit={handleSavePersonal} className="space-y-4">
            {saveSuccess && (
              <div className="flex items-center gap-2 text-xs text-emerald-700 bg-emerald-50 p-2.5 rounded-lg border border-emerald-200">
                <CheckCircle2 className="w-4 h-4" /> Profile saved successfully.
              </div>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Full Name</label>
                <Input value={profile?.full_name || ''} onChange={e => setProfile({ ...profile, full_name: e.target.value })} placeholder="Your full name" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Email</label>
                <Input value={user?.email || ''} disabled className="bg-gray-50 cursor-not-allowed" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Phone</label>
                <Input value={profile?.phone || ''} onChange={e => setProfile({ ...profile, phone: e.target.value })} placeholder="+91 98765 43210" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">City</label>
                <Input value={profile?.city || ''} onChange={e => setProfile({ ...profile, city: e.target.value })} placeholder="Chennai" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">State</label>
                <Input value={profile?.state || ''} onChange={e => setProfile({ ...profile, state: e.target.value })} placeholder="Tamil Nadu" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">PIN Code</label>
                <Input value={profile?.pin_code || ''} onChange={e => setProfile({ ...profile, pin_code: e.target.value })} placeholder="600001" pattern="[1-9][0-9]{5}" />
              </div>
            </div>
            <Button type="submit" variant="primary" disabled={saving}>
              {saving ? 'Saving…' : 'Save Personal Details'}
            </Button>
          </form>
        </Card>
      )}

      {/* Physical Tab */}
      {activeTab === 'physical' && (
        <div className="space-y-5">
          <Card className="p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-gray-900">Physical Measurements</h3>
              <Button variant="outline" size="sm" onClick={() => setShowMeasModal(true)}>
                <Plus className="w-4 h-4 mr-1" /> Add Measurement
              </Button>
            </div>

            {measurements.length > 0 ? (
              <>
                {/* BMI Trend Chart */}
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={measurements.slice(0, 10).reverse()} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="measured_on" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 10 }} />
                      <Tooltip contentStyle={{ fontSize: 11, borderRadius: 8 }} />
                      <Line type="monotone" dataKey="bmi" name="BMI" stroke="#2E7D32" strokeWidth={2} dot={{ r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Table */}
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Height (cm)</TableHead>
                      <TableHead>Weight (kg)</TableHead>
                      <TableHead>BMI</TableHead>
                      <TableHead>Source</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {measurements.map((m: any) => (
                      <TableRow key={m.id}>
                        <TableCell>{m.measured_on}</TableCell>
                        <TableCell>{m.height_cm}</TableCell>
                        <TableCell>{m.weight_kg}</TableCell>
                        <TableCell className="font-semibold">{m.bmi?.toFixed(1)}</TableCell>
                        <TableCell className="text-gray-500 capitalize">{m.source?.replace('_', ' ')}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </>
            ) : (
              <p className="text-xs text-gray-500">No measurements recorded. Add your first measurement to track BMI trends.</p>
            )}
          </Card>

          {/* Add Measurement Modal */}
          <Modal isOpen={showMeasModal} onClose={() => setShowMeasModal(false)} title="Add Physical Measurement">
            <div className="space-y-4 p-1">
              <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-800 flex gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <span>Height must be 30–250 cm. Weight must be 10–250 kg. These values are stored and used for life-stage assessment.</span>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Height (cm) *</label>
                <Input type="number" min="30" max="250" value={newMeas.height_cm} onChange={e => setNewMeas({ ...newMeas, height_cm: e.target.value })} placeholder="e.g., 158" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Weight (kg) *</label>
                <Input type="number" min="10" max="250" step="0.1" value={newMeas.weight_kg} onChange={e => setNewMeas({ ...newMeas, weight_kg: e.target.value })} placeholder="e.g., 52.5" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Date Measured *</label>
                <Input type="date" value={newMeas.measured_on} onChange={e => setNewMeas({ ...newMeas, measured_on: e.target.value })} max={new Date().toISOString().split('T')[0]} />
              </div>
              <div className="flex gap-3">
                <Button variant="outline" className="flex-1" onClick={() => setShowMeasModal(false)}>Cancel</Button>
                <Button variant="primary" className="flex-1" onClick={handleAddMeasurement}
                  disabled={!newMeas.height_cm || !newMeas.weight_kg}>
                  Save Measurement
                </Button>
              </div>
            </div>
          </Modal>
        </div>
      )}

      {/* Diet & Allergies Tab */}
      {activeTab === 'diet' && (
        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-gray-900">Dietary Preferences</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Diet Type</label>
              <Select value={profile?.diet_type || 'vegetarian'} onChange={e => setProfile({ ...profile, diet_type: e.target.value })}>
                <option value="vegetarian">Vegetarian</option>
                <option value="eggetarian">Eggetarian</option>
                <option value="non_vegetarian">Non-Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="jain">Jain</option>
              </Select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Budget per Serving (₹)</label>
              <Input type="number" min="5" max="200" value={profile?.budget_per_serving_inr || ''} onChange={e => setProfile({ ...profile, budget_per_serving_inr: e.target.value })} placeholder="e.g., 30" />
            </div>
          </div>
          <div className="p-3 rounded-xl bg-primary-50 border border-primary-200 text-xs text-primary-800">
            Allergen management and dietary restrictions are enforced as hard constraints in the linear optimizer — not soft preferences. Contact the research team to add custom allergen codes.
          </div>
          <Button variant="primary" onClick={handleSavePersonal} disabled={saving}>
            {saving ? 'Saving…' : 'Save Diet Preferences'}
          </Button>
        </Card>
      )}

      {/* Health Info Tab */}
      {activeTab === 'health' && (
        <div className="space-y-4">
          <Card className="p-5 space-y-3">
            <div className="flex items-center gap-2">
              <Heart className="w-4 h-4 text-red-500" />
              <h3 className="text-sm font-semibold text-gray-900">Health Information</h3>
            </div>
            <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>Health information is stored encrypted (AES-256-GCM). Only you can access it via your session. This information is used to generate safe, relevant formulations — not for any other purpose.</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Known Nutrient Deficiencies</label>
                <Input value={profile?.known_deficiencies?.join(', ') || ''} onChange={e => setProfile({ ...profile, known_deficiencies: e.target.value.split(',').map((s: string) => s.trim()) })} placeholder="e.g., iron, vitamin B12" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Pregnancy Status</label>
                <Select value={profile?.pregnancy_status || 'not_pregnant'} onChange={e => setProfile({ ...profile, pregnancy_status: e.target.value })}>
                  <option value="not_pregnant">Not Pregnant</option>
                  <option value="pregnant">Pregnant</option>
                  <option value="lactating">Lactating</option>
                  <option value="planning">Planning Pregnancy</option>
                </Select>
              </div>
            </div>
            <Button variant="primary" onClick={handleSavePersonal} disabled={saving}>
              {saving ? 'Saving…' : 'Save Health Info'}
            </Button>
          </Card>
          <MedicalDisclaimer />
        </div>
      )}
    </div>
  );
};

