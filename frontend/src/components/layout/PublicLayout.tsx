import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../lib/auth';
import { LanguageSelector } from '../ui/LanguageSelector';
import { Button } from '../ui/Button';
import { Menu, X, ShieldAlert, Sparkles, HeartPulse, ChevronRight } from 'lucide-react';

export const PublicLayout: React.FC = () => {
  const { t } = useTranslation();
  const { user, isAuthenticated } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navLinks = [
    { label: t('nav.home'), path: '/' },
    { label: t('nav.anaemia_info'), path: '/anaemia' },
    { label: t('nav.approach'), path: '/approach' },
    { label: t('nav.products'), path: '/products' },
    { label: t('nav.about'), path: '/about' },
    { label: t('nav.contact'), path: '/contact' },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#F7F9F8] text-gray-800">
      {/* Top Banner: Research Prototype Notice */}
      <div className="bg-primary-900 text-primary-100 text-xs px-4 py-1.5 text-center flex items-center justify-center gap-2">
        <Sparkles className="w-3.5 h-3.5 text-amber-300 shrink-0" />
        <span>
          ICMR–Gates Foundation Grand Challenge Prototype • Non-medicinal, nutrient-dense aspirational food products
        </span>
      </div>

      {/* Main Navbar */}
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Brand */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-primary-600 flex items-center justify-center text-white shadow-sm group-hover:bg-primary-700 transition">
              <HeartPulse className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-xl tracking-tight text-gray-900">
                Nutri<span className="text-primary-600">AI</span>
              </span>
              <span className="block text-[10px] uppercase font-semibold tracking-wider text-primary-700 leading-none">
                Bioavailable Nutrition
              </span>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => {
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`text-sm font-medium transition-colors ${
                    isActive
                      ? 'text-primary-700 font-semibold border-b-2 border-primary-600 pb-0.5'
                      : 'text-gray-600 hover:text-primary-600'
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* Controls: Language & Auth */}
          <div className="hidden md:flex items-center gap-3">
            <LanguageSelector />
            {isAuthenticated ? (
              <Link to="/app">
                <Button size="sm" variant="primary">
                  {t('nav.dashboard')}
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </Link>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login">
                  <Button size="sm" variant="ghost">
                    {t('auth.login')}
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm" variant="primary">
                    {t('auth.register')}
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center gap-2">
            <LanguageSelector />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-gray-600 hover:text-gray-900 rounded-md focus:outline-none"
              aria-label="Toggle Menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-b border-gray-200 bg-white px-4 pt-2 pb-4 space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100"
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-3 border-t border-gray-100 flex flex-col gap-2">
              {isAuthenticated ? (
                <Link to="/app" onClick={() => setMobileMenuOpen(false)}>
                  <Button className="w-full" variant="primary">
                    {t('nav.dashboard')}
                  </Button>
                </Link>
              ) : (
                <>
                  <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                    <Button className="w-full" variant="outline">
                      {t('auth.login')}
                    </Button>
                  </Link>
                  <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                    <Button className="w-full" variant="primary">
                      {t('auth.register')}
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </header>

      {/* Main Page Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 pt-12 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
            {/* Col 1: About NutriAI */}
            <div className="space-y-4 md:col-span-1">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-primary-600 flex items-center justify-center text-white">
                  <HeartPulse className="w-4 h-4" />
                </div>
                <span className="font-bold text-lg text-gray-900">NutriAI</span>
              </div>
              <p className="text-sm text-gray-600 leading-relaxed">
                Development and validation of AI-optimized, aspirational nutrient-dense food products for anaemia prevention among adolescent girls and women of reproductive age.
              </p>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-50 text-amber-800 text-xs font-medium border border-amber-200">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>Prototype Demonstration</span>
              </div>
            </div>

            {/* Col 2: Navigation Links */}
            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-gray-900 mb-4">Explore</h4>
              <ul className="space-y-2 text-sm">
                <li><Link to="/anaemia" className="text-gray-600 hover:text-primary-600">Understanding Anaemia</Link></li>
                <li><Link to="/approach" className="text-gray-600 hover:text-primary-600">ICMR Principles & Pipeline</Link></li>
                <li><Link to="/products" className="text-gray-600 hover:text-primary-600">Product Categories</Link></li>
                <li><Link to="/about" className="text-gray-600 hover:text-primary-600">About the Project</Link></li>
                <li><Link to="/contact" className="text-gray-600 hover:text-primary-600">Contact & Feedback</Link></li>
              </ul>
            </div>

            {/* Col 3: Target Groups & Formats */}
            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-gray-900 mb-4">Target Demographics</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Adolescent Girls (10–19 yrs)</li>
                <li>• Young Reproductive Age (20–35 yrs)</li>
                <li>• Older Reproductive Age (35–49 yrs)</li>
                <li>• Formats: Bars, Laddoos, Breakfast Mixes, Drink Mixes, Chikkis</li>
              </ul>
            </div>

            {/* Col 4: Medical & Regulatory Compliance */}
            <div>
              <h4 className="text-sm font-semibold uppercase tracking-wider text-gray-900 mb-4">Ethical & Safety Commitments</h4>
              <ul className="space-y-2 text-sm">
                <li><Link to="/disclaimer" className="text-gray-600 hover:text-primary-600">Medical Disclaimer</Link></li>
                <li><Link to="/privacy" className="text-gray-600 hover:text-primary-600">Privacy & Health Data Policy</Link></li>
                <li><Link to="/terms" className="text-gray-600 hover:text-primary-600">Terms of Use</Link></li>
                <li><a href="https://main.icmr.nic.in/" target="_blank" rel="noreferrer" className="text-gray-600 hover:text-primary-600">ICMR Reference Guidelines ↗</a></li>
              </ul>
            </div>
          </div>

          {/* Medical Disclaimer Banner */}
          <div className="rounded-xl bg-amber-50/80 border border-amber-200 p-4 text-xs text-amber-900 leading-relaxed mb-6">
            <div className="flex items-start gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <div>
                <strong>Medical & Clinical Notice:</strong> NutriAI is a dietary assessment and food-formulation research prototype. It does not diagnose, prescribe, treat, or cure any medical condition. It supports nutritional intake planning based on dietary guidelines and laboratory markers. Never disregard professional medical advice or delay seeking care because of any information generated here. All products displayed are prototypes with demo checkout.
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between pt-6 border-t border-gray-200 text-xs text-gray-500 gap-4">
            <p>© {new Date().getFullYear()} NutriAI Research Initiative. Built adhering to ICMR–NIN dietary recommendations.</p>
            <p>Languages: English • தமிழ் • हिन्दी • తెలుగు • മലയാളം</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

