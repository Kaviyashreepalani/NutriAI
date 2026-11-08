import React, { useEffect, useState, useRef } from 'react';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { EmptyState } from '../../components/ui/EmptyState';
import {
  CheckCircle2,
  TrendingUp,
  Calendar,
  Bell,
  Info,
  AlertTriangle,
  BarChart2,
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';

export const ProgressPage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [logging, setLogging] = useState(false);
  const [logSuccess, setLogSuccess] = useState(false);
  const [reminderTime, setReminderTime] = useState('08:00');

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/progress');
        setData(res.data);
      } catch {
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const handleLogServing = async () => {
    setLogging(true);
    try {
      await api.post('/progress/log', { date: new Date().toISOString().split('T')[0], servings: 1 });
      setLogSuccess(true);
      // Refresh progress data
      const res = await api.get('/progress');
      setData(res.data);
    } catch {
      // silent
    } finally {
      setLogging(false);
    }
  };

  const handleSetReminder = async () => {
    try {
      await api.post('/progress/reminder', { time: reminderTime });
    } catch {
      // silent
    }
  };

  if (loading) return (
    <div className="space-y-4">
      <div className="h-32 bg-gray-200 rounded-2xl animate-pulse" />
      <div className="h-64 bg-gray-200 rounded-2xl animate-pulse" />
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <MedicalDisclaimer />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2.5">
            <TrendingUp className="w-6 h-6 text-primary-600" />
            Track Progress
          </h1>
          <p className="text-sm text-gray-600 mt-1">Log daily servings and monitor your adherence over time.</p>
        </div>
        <PrototypeBadge />
      </div>

      {/* Disclaimer on efficacy */}
      <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex gap-2 text-xs text-amber-800">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <span>
          <strong>Important:</strong> Changes in laboratory values must not be attributed to NutriAI and must be interpreted by a qualified healthcare professional. This tracker measures product adherence only — not clinical efficacy.
        </span>
      </div>

      {!data?.active_formulation ? (
        <EmptyState
          icon={<BarChart2 className="w-10 h-10 text-gray-400" />}
          title="No active formulation"
          description="Generate a personalized food product to start tracking your daily servings."
        />
      ) : (
        <>
          {/* Quick Log & Current Product */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <Card className="p-5 space-y-4">
              <h3 className="text-sm font-semibold text-gray-900">Today's Log</h3>
              <div className="p-4 rounded-xl bg-primary-50 border border-primary-200 space-y-1">
                <h4 className="text-sm font-bold text-primary-900">{data.active_formulation.product_name}</h4>
                <p className="text-xs text-primary-700">{data.active_formulation.format} • {data.active_formulation.serving_size_g}g serving</p>
                <div className="mt-2 flex items-center gap-2 text-xs text-primary-800">
                  <CheckCircle2 className="w-4 h-4 text-primary-600" />
                  <span>{data.today_logged ? 'Served today ✓' : 'Not yet logged today'}</span>
                </div>
              </div>
              {logSuccess ? (
                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Serving logged successfully for today!
                </div>
              ) : (
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={handleLogServing}
                  disabled={logging || data.today_logged}
                >
                  <CheckCircle2 className="w-4 h-4 mr-2" />
                  {data.today_logged ? 'Already logged today' : logging ? 'Logging…' : 'Log Today\'s Serving'}
                </Button>
              )}
            </Card>

            {/* Adherence Stats */}
            <Card className="p-5 space-y-4">
              <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-primary-600" />
                Adherence Stats
              </h3>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: 'This Week', value: `${data.adherence?.week_pct ?? 0}%`, sub: `${data.adherence?.week_days ?? 0}/7 days` },
                  { label: 'This Month', value: `${data.adherence?.month_pct ?? 0}%`, sub: `${data.adherence?.month_days ?? 0} days` },
                  { label: 'Current Streak', value: `${data.adherence?.streak ?? 0}d`, sub: 'consecutive days' },
                  { label: 'Total Logged', value: `${data.adherence?.total_days ?? 0}`, sub: 'days since start' },
                ].map((stat, i) => (
                  <div key={i} className="p-3 bg-gray-50 rounded-xl text-center">
                    <div className="text-lg font-black text-gray-900">{stat.value}</div>
                    <div className="text-xs font-semibold text-gray-700">{stat.label}</div>
                    <div className="text-[10px] text-gray-500">{stat.sub}</div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Weekly Adherence Calendar Heatmap */}
          <Card className="p-5 space-y-4">
            <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-primary-600" />
              30-Day Adherence Calendar
            </h3>
            <div className="grid grid-cols-10 sm:grid-cols-15 gap-1.5 flex-wrap">
              {(data.calendar_days || []).map((day: any, idx: number) => (
                <div
                  key={idx}
                  title={`${day.date}: ${day.logged ? 'Served ✓' : 'Not logged'}`}
                  className={`w-7 h-7 rounded-md border text-[9px] font-bold flex items-center justify-center cursor-default transition ${
                    day.logged
                      ? 'bg-primary-500 border-primary-600 text-white'
                      : day.is_future
                      ? 'bg-gray-100 border-gray-200 text-gray-300'
                      : 'bg-gray-200 border-gray-300 text-gray-500'
                  }`}
                >
                  {new Date(day.date).getDate()}
                </div>
              ))}
            </div>
            <div className="flex items-center gap-4 text-xs text-gray-500">
              <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-primary-500 inline-block" /> Served</span>
              <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-gray-200 inline-block" /> Missed</span>
              <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-gray-100 inline-block" /> Future</span>
            </div>
          </Card>

          {/* Lab Trend Chart */}
          {data.lab_trends && data.lab_trends.length > 1 && (
            <Card className="p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-teal-600" />
                  Lab Value Trend
                </h3>
                <span className="text-xs text-gray-400">Source: uploaded lab reports</span>
              </div>

              <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-[11px] text-amber-800 flex gap-2">
                <Info className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                <span>Lab values are displayed from your uploaded reports only. Changes must be interpreted by a healthcare professional. NutriAI does not claim clinical efficacy.</span>
              </div>

              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data.lab_trends} margin={{ top: 10, right: 20, left: -10, bottom: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                    <Line type="monotone" dataKey="hb" name="Hb (g/dL)" stroke="#2E7D32" strokeWidth={2} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="ferritin" name="Ferritin (ng/mL)" stroke="#00897B" strokeWidth={2} dot={{ r: 4 }} strokeDasharray="5 5" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          {/* Reminder Settings */}
          <Card className="p-5 space-y-4">
            <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
              <Bell className="w-4 h-4 text-amber-600" />
              Daily Reminder
            </h3>
            <div className="flex items-center gap-3">
              <input
                type="time"
                value={reminderTime}
                onChange={(e) => setReminderTime(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
              />
              <Button variant="outline" size="sm" onClick={handleSetReminder}>
                Save Reminder
              </Button>
              <span className="text-xs text-gray-500">Get a daily reminder to log your serving.</span>
            </div>
          </Card>
        </>
      )}

      <MedicalDisclaimer />
    </div>
  );
};

