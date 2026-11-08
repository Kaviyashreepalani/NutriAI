import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../lib/auth';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import {
  Sparkles,
  TrendingUp,
  FlaskConical,
  Upload,
  CheckCircle2,
  AlertCircle,
  Clock,
  ShoppingBag,
  BookOpen,
  User,
  ArrowRight,
  Activity,
  Target,
} from 'lucide-react';
import { ProgressBar } from '../../components/ui/ProgressBar';

interface DashboardData {
  profile_completion: number;
  latest_assessment: any | null;
  active_formulation: any | null;
  recent_activities: any[];
  stats: { label: string; value: string; change?: string; icon?: string }[];
}

export const DashboardPage: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/dashboard');
        setData(res.data);
      } catch {
        // Provide graceful fallback if endpoint not available yet
        setData({
          profile_completion: user ? 40 : 0,
          latest_assessment: null,
          active_formulation: null,
          recent_activities: [],
          stats: [],
        });
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, [user]);

  const greeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const quickActions = [
    {
      title: 'Generate Formulation',
      desc: 'Upload lab report and get a personalized food product',
      icon: Sparkles,
      path: '/app/generate',
      color: 'bg-primary-50 border-primary-200 text-primary-800',
      cta: 'Start now',
    },
    {
      title: 'Track Progress',
      desc: 'Log today\'s serving and view your adherence calendar',
      icon: TrendingUp,
      path: '/app/progress',
      color: 'bg-teal-50 border-teal-200 text-teal-800',
      cta: 'Log serving',
    },
    {
      title: 'Prototype Shop',
      desc: 'Browse and place a demo order for prototype products',
      icon: ShoppingBag,
      path: '/app/shop',
      color: 'bg-purple-50 border-purple-200 text-purple-800',
      cta: 'Browse',
    },
    {
      title: 'Anaemia Guide',
      desc: 'Learn about iron, folate, B12 and bioavailability',
      icon: BookOpen,
      path: '/app/learn',
      color: 'bg-amber-50 border-amber-200 text-amber-800',
      cta: 'Read guide',
    },
  ];

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="h-28 bg-gray-200 rounded-2xl animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => <div key={i} className="h-24 bg-gray-200 rounded-xl animate-pulse" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-primary-700 to-emerald-700 text-white rounded-2xl p-6 sm:p-8 relative overflow-hidden">
        <div className="relative z-10 space-y-2">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h1 className="text-xl sm:text-2xl font-bold">
                {greeting()}, {user?.full_name?.split(' ')[0] || 'User'}!
              </h1>
              <p className="text-primary-200 text-sm mt-1">
                {user?.life_stage
                  ? `Life stage: ${user.life_stage}`
                  : 'Complete your profile to unlock personalized formulations'}
              </p>
            </div>
            <PrototypeBadge />
          </div>

          {/* Profile Completion Progress */}
          <div className="mt-4 space-y-1.5">
            <div className="flex items-center justify-between text-xs text-primary-200">
              <span>Profile completion</span>
              <span className="font-bold text-white">{data?.profile_completion ?? 0}%</span>
            </div>
            <div className="h-2 bg-primary-900/40 rounded-full overflow-hidden">
              <div
                className="h-full bg-amber-300 rounded-full transition-all duration-700"
                style={{ width: `${data?.profile_completion ?? 0}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Action Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link key={action.path} to={action.path}>
              <div className={`p-4 rounded-xl border ${action.color} flex flex-col gap-3 h-full hover:shadow-md transition`}>
                <Icon className="w-6 h-6" />
                <div className="flex-1">
                  <h3 className="text-sm font-bold">{action.title}</h3>
                  <p className="text-xs opacity-80 mt-0.5 leading-relaxed">{action.desc}</p>
                </div>
                <span className="text-xs font-semibold flex items-center gap-1 group">
                  {action.cta} <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                </span>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Main Grid: Assessment + Formulation Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Latest Assessment */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary-600" />
              Latest Assessment
            </h3>
            <Link to="/app/generate" className="text-xs text-primary-600 hover:underline font-medium flex items-center gap-1">
              New <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {data?.latest_assessment ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: 'Haemoglobin', value: `${data.latest_assessment.hb} g/dL`, status: data.latest_assessment.hb_status },
                  { label: 'Serum Ferritin', value: `${data.latest_assessment.ferritin} ng/mL`, status: data.latest_assessment.ferritin_status },
                ].map((m, i) => (
                  <div key={i} className="p-3 bg-gray-50 rounded-xl">
                    <div className="text-xs text-gray-500">{m.label}</div>
                    <div className="text-base font-bold text-gray-900 mt-0.5">{m.value}</div>
                    <div className={`text-[10px] font-semibold mt-0.5 ${m.status === 'low' ? 'text-red-600' : m.status === 'normal' ? 'text-emerald-600' : 'text-amber-600'}`}>
                      {m.status?.toUpperCase()}
                    </div>
                  </div>
                ))}
              </div>
              <Link to="/app/results">
                <Button variant="outline" size="sm" className="w-full">
                  View Full Formulation <ArrowRight className="w-3.5 h-3.5 ml-1" />
                </Button>
              </Link>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 space-y-3 text-center">
              <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center">
                <Upload className="w-6 h-6 text-gray-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">No assessment yet</p>
                <p className="text-xs text-gray-500 mt-0.5">Upload a lab report to generate your first formulation.</p>
              </div>
              <Link to="/app/generate">
                <Button variant="primary" size="sm">
                  <Sparkles className="w-4 h-4 mr-1.5" />
                  Upload Lab Report
                </Button>
              </Link>
            </div>
          )}
        </Card>

        {/* Active Product Plan */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2">
              <Target className="w-4 h-4 text-teal-600" />
              Active Product Plan
            </h3>
            <PrototypeBadge />
          </div>

          {data?.active_formulation ? (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-teal-50 border border-teal-200">
                <h4 className="text-sm font-bold text-teal-900">{data.active_formulation.product_name}</h4>
                <p className="text-xs text-teal-700 mt-1">{data.active_formulation.format}</p>
                <div className="mt-3 grid grid-cols-3 gap-2">
                  {[
                    { label: 'Iron/Serving', value: `${data.active_formulation.iron_mg} mg` },
                    { label: 'Serving Size', value: data.active_formulation.serving_size },
                    { label: 'Est. Cost', value: `₹${data.active_formulation.cost_inr}` },
                  ].map((m, i) => (
                    <div key={i} className="text-center">
                      <div className="text-xs font-bold text-teal-900">{m.value}</div>
                      <div className="text-[10px] text-teal-700">{m.label}</div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex gap-2">
                <Link to="/app/progress" className="flex-1">
                  <Button variant="primary" size="sm" className="w-full">
                    <CheckCircle2 className="w-4 h-4 mr-1" />
                    Log Today's Serving
                  </Button>
                </Link>
                <Link to="/app/shop" className="flex-1">
                  <Button variant="outline" size="sm" className="w-full">
                    <ShoppingBag className="w-4 h-4 mr-1" />
                    Demo Order
                  </Button>
                </Link>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 space-y-3 text-center">
              <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center">
                <FlaskConical className="w-6 h-6 text-gray-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">No active formulation</p>
                <p className="text-xs text-gray-500 mt-0.5">Generate a food product to start tracking progress.</p>
              </div>
            </div>
          )}
        </Card>
      </div>

      {/* Recent Activity */}
      {data?.recent_activities && data.recent_activities.length > 0 && (
        <Card className="p-5 space-y-4">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-500" />
            Recent Activity
          </h3>
          <div className="space-y-3">
            {data.recent_activities.slice(0, 5).map((activity: any, idx: number) => (
              <div key={idx} className="flex items-center gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-primary-400 shrink-0" />
                <span className="text-gray-700 flex-1">{activity.description}</span>
                <span className="text-xs text-gray-400 shrink-0">{activity.time_ago}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Medical Disclaimer */}
      <MedicalDisclaimer />
    </div>
  );
};

