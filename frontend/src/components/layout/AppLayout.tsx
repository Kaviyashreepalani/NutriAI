import React, { useState } from 'react';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../lib/auth';
import { LanguageSelector } from '../ui/LanguageSelector';
import { PrototypeBadge } from '../safety/PrototypeBadge';
import { FloatingAssistantWidget } from '../chat/FloatingAssistantWidget';
import {
  LayoutDashboard,
  Sparkles,
  FlaskConical,
  ShoppingBag,
  ShoppingCart,
  TrendingUp,
  History,
  BookOpen,
  Bot,
  User,
  Settings,
  ShieldCheck,
  LogOut,
  Menu,
  X,
  HeartPulse,
  Scale
} from 'lucide-react';

export const AppLayout: React.FC = () => {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const navItems = [
    { label: 'Generate Product', path: '/app/generate', icon: Sparkles },
    { label: 'Track Progress', path: '/app/progress', icon: TrendingUp },
    { label: 'History', path: '/app/history', icon: History },
    { label: 'Order / Cart', path: '/app/cart', icon: ShoppingCart },
    { label: 'Details (About Anaemia)', path: '/app/details', icon: BookOpen },
    { label: 'User Info', path: '/app/profile', icon: User },
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-[#F7F9F8] flex flex-col md:flex-row">
      {/* Sidebar for Desktop */}
      <aside className="hidden md:flex md:w-64 flex-col bg-white border-r border-gray-200 shrink-0 select-none">
        {/* Brand */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-gray-100">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center text-white shadow-sm">
              <HeartPulse className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-gray-900">
                Nutri<span className="text-primary-600">AI</span>
              </span>
              <span className="block text-[9px] uppercase font-semibold tracking-wider text-primary-700 leading-none">
                Research Platform
              </span>
            </div>
          </Link>
        </div>

        {/* User Info Capsule */}
        <div className="p-4 mx-3 my-2 rounded-xl bg-primary-50/60 border border-primary-100/80">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-primary-600 text-white font-bold text-sm flex items-center justify-center shadow-sm">
              {user?.full_name?.charAt(0) || user?.email?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="overflow-hidden">
              <p className="text-xs font-semibold text-gray-900 truncate">
                {user?.full_name || user?.email?.split('@')[0]}
              </p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="inline-block px-1.5 py-0.2 rounded text-[10px] font-medium bg-primary-200/60 text-primary-800 uppercase tracking-wide">
                  {user?.role || 'user'}
                </span>
                {user?.age && (
                  <span className="text-[10px] text-gray-500 font-medium">
                    {user.age} yrs
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-gray-500'}`} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-100 space-y-3">
          <div className="flex justify-center">
            <PrototypeBadge />
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2.5 w-full px-3 py-2 text-xs font-medium text-red-600 hover:bg-red-50 rounded-xl transition"
          >
            <LogOut className="w-4 h-4" />
            <span>{t('auth.logout', 'Sign Out')}</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="sticky top-0 z-30 h-16 bg-white/95 backdrop-blur-md border-b border-gray-200 px-4 sm:px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileSidebarOpen(!mobileSidebarOpen)}
              className="md:hidden p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100"
              aria-label="Toggle Navigation"
            >
              {mobileSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <span className="text-sm font-semibold text-gray-800 hidden sm:inline-block">
              NutriAI Formulation & Progress Suite
            </span>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:block">
              <PrototypeBadge />
            </div>
            <LanguageSelector />
            <div className="h-6 w-px bg-gray-200"></div>
            <Link to="/app/profile" className="flex items-center gap-2 group">
              <div className="w-8 h-8 rounded-full bg-primary-100 border border-primary-200 text-primary-800 text-xs font-bold flex items-center justify-center">
                {user?.full_name?.charAt(0) || user?.email?.charAt(0).toUpperCase() || 'U'}
              </div>
            </Link>
          </div>
        </header>

        {/* Mobile Sidebar Dropdown */}
        {mobileSidebarOpen && (
          <div className="md:hidden fixed inset-0 z-40 bg-black/40 backdrop-blur-sm flex">
            <div className="w-64 bg-white h-full flex flex-col p-4 shadow-xl">
              <div className="flex items-center justify-between pb-4 border-b border-gray-100">
                <span className="font-bold text-lg text-primary-700">NutriAI</span>
                <button onClick={() => setMobileSidebarOpen(false)}>
                  <X className="w-5 h-5 text-gray-600" />
                </button>
              </div>
              <nav className="flex-1 py-4 space-y-1 overflow-y-auto">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = location.pathname === item.path;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setMobileSidebarOpen(false)}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium ${
                        isActive
                          ? 'bg-primary-600 text-white'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 p-2 text-xs font-medium text-red-600 hover:bg-red-50 rounded-lg"
              >
                <LogOut className="w-4 h-4" />
                <span>{t('auth.logout', 'Sign Out')}</span>
              </button>
            </div>
            <div className="flex-1" onClick={() => setMobileSidebarOpen(false)}></div>
          </div>
        )}

        {/* Page Content Body */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </main>
      </div>

      {/* Floating Chatbot Assistant with Voice and Number Guard */}
      <FloatingAssistantWidget />
    </div>
  );
};

