import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './lib/auth';

// Layouts
import { PublicLayout } from './components/layout/PublicLayout';
import { AuthLayout } from './components/layout/AuthLayout';
import { AppLayout } from './components/layout/AppLayout';

// Public pages
import { Home } from './features/public/Home';
import { AnaemiaPage } from './features/public/AnaemiaPage';
import { ApproachPage } from './features/public/ApproachPage';
import { ProductsPage } from './features/public/ProductsPage';
import { AboutPage } from './features/public/AboutPage';
import { ContactPage } from './features/public/ContactPage';
import { DisclaimerPage, PrivacyPage, TermsPage } from './features/public/StaticPages';

// Auth pages
import { LoginPage } from './features/auth/LoginPage';
import { RegisterPage } from './features/auth/RegisterPage';
import { ForgotPasswordPage } from './features/auth/ForgotPasswordPage';

// App pages
import { DashboardPage } from './features/app/DashboardPage';
import { GenerateWizard } from './features/app/GenerateWizard';
import { ResultsPage } from './features/app/ResultsPage';
import { ComparePage } from './features/app/ComparePage';
import { ProfilePage } from './features/app/ProfilePage';
import { ProgressPage } from './features/app/ProgressPage';
import { HistoryPage } from './features/app/HistoryPage';
import { LearnPage, LearnDetailPage } from './features/app/LearnPage';
import { DetailsPage } from './features/app/DetailsPage';
import { AssistantPage } from './features/app/AssistantPage';
import { SettingsPage } from './features/app/SettingsPage';
import { ShopPage } from './features/app/ShopPage';
import { CartPage, CheckoutPage, OrdersPage } from './features/app/OrderPages';

// Error boundary
import { ErrorBoundary } from './components/ui/ErrorBoundary';

// Lazy-loaded admin
const AdminPortal = lazy(() =>
  import('./features/admin/AdminPortal').then((m) => ({ default: m.AdminPortal }))
);

// Loading fallback
const PageLoader: React.FC = () => (
  <div className="flex items-center justify-center min-h-[200px]">
    <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
  </div>
);

// Protected route wrapper
const RequireAuth: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <PageLoader />;

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

// Redirect authenticated users away from auth pages
const RedirectIfAuth: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <PageLoader />;
  if (isAuthenticated) return <Navigate to="/app" replace />;
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* ========== PUBLIC ROUTES ========== */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/anaemia" element={<AnaemiaPage />} />
            <Route path="/approach" element={<ApproachPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/disclaimer" element={<DisclaimerPage />} />
            <Route path="/privacy" element={<PrivacyPage />} />
            <Route path="/terms" element={<TermsPage />} />
          </Route>

          {/* ========== AUTH ROUTES ========== */}
          <Route
            element={
              <RedirectIfAuth>
                <AuthLayout />
              </RedirectIfAuth>
            }
          >
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          </Route>

          {/* ========== PROTECTED APP ROUTES ========== */}
          <Route
            path="/app"
            element={
              <RequireAuth>
                <AppLayout />
              </RequireAuth>
            }
          >
            <Route index element={<Navigate to="/app/generate" replace />} />
            <Route path="generate" element={<GenerateWizard />} />
            <Route path="progress" element={<ProgressPage />} />
            <Route path="history" element={<HistoryPage />} />
            <Route path="cart" element={<CartPage />} />
            <Route path="details" element={<DetailsPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="results" element={<ResultsPage />} />
            <Route path="compare" element={<ComparePage />} />
            <Route path="learn" element={<DetailsPage />} />
            <Route path="learn/:moduleId" element={<LearnDetailPage />} />
            <Route path="assistant" element={<AssistantPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="shop" element={<CartPage />} />
            <Route path="checkout" element={<CheckoutPage />} />
            <Route path="orders" element={<OrdersPage />} />
            <Route
              path="admin"
              element={
                <Suspense fallback={<PageLoader />}>
                  <AdminPortal />
                </Suspense>
              }
            />
          </Route>

          {/* ========== CATCH-ALL ========== */}
          <Route
            path="*"
            element={
              <div className="flex flex-col items-center justify-center min-h-screen gap-4 text-center px-4">
                <div className="text-6xl font-black text-gray-200">404</div>
                <h2 className="text-xl font-bold text-gray-900">Page Not Found</h2>
                <p className="text-sm text-gray-500 max-w-sm">The page you're looking for doesn't exist or has been moved.</p>
                <a href="/" className="text-sm text-primary-600 font-semibold hover:underline">
                  Return to NutriAI Home
                </a>
              </div>
            }
          />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
};

