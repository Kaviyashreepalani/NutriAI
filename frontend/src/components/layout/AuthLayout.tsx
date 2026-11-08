import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { HeartPulse, ShieldAlert } from 'lucide-react';
import { LanguageSelector } from '../ui/LanguageSelector';
import { PrototypeBadge } from '../safety/PrototypeBadge';

export const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#F7F9F8] flex flex-col justify-between py-8 px-4 sm:px-6 lg:px-8">
      {/* Top Header */}
      <div className="flex items-center justify-between max-w-md w-full mx-auto">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center text-white shadow-sm group-hover:bg-primary-700 transition">
            <HeartPulse className="w-4 h-4" />
          </div>
          <span className="font-bold text-lg text-gray-900">
            Nutri<span className="text-primary-600">AI</span>
          </span>
        </Link>
        <div className="flex items-center gap-3">
          <PrototypeBadge />
          <LanguageSelector />
        </div>
      </div>

      {/* Main Form Container */}
      <div className="w-full max-w-md mx-auto my-6">
        <div className="bg-white py-8 px-6 sm:px-8 rounded-2xl shadow-sm border border-gray-200">
          <Outlet />
        </div>
      </div>

      {/* Footer Info */}
      <div className="max-w-md w-full mx-auto text-center space-y-2">
        <div className="flex items-center justify-center gap-1.5 text-xs text-gray-500">
          <ShieldAlert className="w-3.5 h-3.5 text-gray-400" />
          <span>Research prototype. Does not diagnose or prescribe.</span>
        </div>
        <p className="text-xs text-gray-400">
          © {new Date().getFullYear()} NutriAI • Supporting ICMR Anaemia Prevention Goals
        </p>
      </div>
    </div>
  );
};

