import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../lib/auth';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { HeartPulse, LogIn, User, FlaskConical, Shield, ChefHat, Eye, EyeOff } from 'lucide-react';

const DEV_ACCOUNTS = [
  { id: 'dev-user-adolescent', label: 'Adolescent Girl (14 yrs)', icon: User, color: 'bg-emerald-50 text-emerald-800 border-emerald-300' },
  { id: 'dev-user-woman28', label: 'Woman 28 yrs (Pregnant)', icon: User, color: 'bg-teal-50 text-teal-800 border-teal-300' },
  { id: 'dev-user-woman42', label: 'Woman 42 yrs (Non-Pregnant)', icon: User, color: 'bg-blue-50 text-blue-800 border-blue-300' },
  { id: 'dev-admin', label: 'Admin / Researcher', icon: Shield, color: 'bg-amber-50 text-amber-800 border-amber-300' },
  { id: 'dev-nutritionist', label: 'Nutritionist', icon: ChefHat, color: 'bg-purple-50 text-purple-800 border-purple-300' },
];

export const LoginPage: React.FC = () => {
  const { t } = useTranslation();
  const { login, loginWithDevAccount } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as any)?.from?.pathname || '/app';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [devLoading, setDevLoading] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDevLogin = async (accountId: string) => {
    setDevLoading(accountId);
    try {
      await loginWithDevAccount(accountId);
      navigate('/app/generate', { replace: true });
    } catch (err: any) {
      setError(err.message || 'Dev login failed');
    } finally {
      setDevLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-1">
        <div className="flex justify-center">
          <div className="w-12 h-12 rounded-2xl bg-primary-600 flex items-center justify-center text-white shadow-sm mb-2">
            <HeartPulse className="w-6 h-6" />
          </div>
        </div>
        <h2 className="text-xl font-bold text-gray-900">{t('auth.welcome_back', 'Welcome back')}</h2>
        <p className="text-xs text-gray-500">NutriAI Nutrition Research Platform</p>
      </div>

      {/* Email/Password Form */}
      <form onSubmit={handleLogin} className="space-y-4">
        {error && (
          <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700">{error}</div>
        )}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-700">Email address</label>
          <Input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            autoComplete="email"
          />
        </div>
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label className="block text-xs font-medium text-gray-700">Password</label>
            <Link to="/forgot-password" className="text-xs text-primary-600 hover:underline">
              {t('auth.forgot_password', 'Forgot password?')}
            </Link>
          </div>
          <div className="relative">
            <Input
              type={showPassword ? 'text' : 'password'}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="current-password"
            />
            <button
              type="button"
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>
        <Button type="submit" variant="primary" className="w-full" disabled={loading}>
          <LogIn className="w-4 h-4 mr-2" />
          {loading ? 'Signing in...' : t('auth.login', 'Sign In')}
        </Button>
      </form>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="px-2 bg-white text-gray-500">or sign in quickly as a demo account</span>
        </div>
      </div>

      {/* Dev Account Quick Login */}
      <div className="space-y-2">
        <div className="flex items-center gap-1.5 text-[11px] text-amber-700 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200">
          <FlaskConical className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          <span>Demo accounts available only in development mode (AUTH_MODE=dev). Disabled in production.</span>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {DEV_ACCOUNTS.map((acc) => {
            const Icon = acc.icon;
            return (
              <button
                key={acc.id}
                onClick={() => handleDevLogin(acc.id)}
                disabled={!!devLoading}
                className={`flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-xs font-medium border transition hover:opacity-90 disabled:opacity-50 ${acc.color}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span className="flex-1 text-left">{acc.label}</span>
                {devLoading === acc.id && (
                  <span className="text-[10px] opacity-70">Signing in...</span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <p className="text-center text-xs text-gray-600">
        {t('auth.no_account', "Don't have an account?")}{' '}
        <Link to="/register" className="text-primary-600 font-semibold hover:underline">
          {t('auth.register', 'Create account')}
        </Link>
      </p>
    </div>
  );
};

