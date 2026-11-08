import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../lib/auth';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Select } from '../../components/ui/Select';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { SUPPORTED_LANGUAGES } from '../../lib/i18n';
import { Download, Trash2, Shield, Globe, Bell, LogOut, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const SettingsPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [language, setLanguage] = useState(i18n.language);
  const [exporting, setExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState('');
  const [deleteError, setDeleteError] = useState('');
  const [consentRevoking, setConsentRevoking] = useState<string | null>(null);
  const [consentStatuses, setConsentStatuses] = useState<Record<string, boolean>>({
    data_processing: true,
    health_data: true,
    report_ocr: true,
    chatbot: true,
  });

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    i18n.changeLanguage(lang);
    document.documentElement.lang = lang;
    api.patch('/profile/language', { language: lang }).catch(() => {});
  };

  const handleExportData = async () => {
    setExporting(true);
    try {
      const res = await api.get('/settings/export', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `NutriAI_Export_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      setExportSuccess(true);
    } catch {
      // silent
    } finally {
      setExporting(false);
    }
  };

  const handleRevokeConsent = async (category: string) => {
    setConsentRevoking(category);
    try {
      await api.patch(`/settings/consent/${category}`, { granted: false });
      setConsentStatuses((prev) => ({ ...prev, [category]: false }));
    } finally {
      setConsentRevoking(null);
    }
  };

  const handleDeleteAccount = async () => {
    if (confirmDelete !== user?.email) {
      setDeleteError('Email does not match. Type your registered email to confirm.');
      return;
    }
    setDeleting(true);
    try {
      await api.delete('/settings/account');
      await logout();
      navigate('/');
    } catch (err: any) {
      setDeleteError(err.response?.data?.detail || 'Account deletion failed. Please contact support.');
    } finally {
      setDeleting(false);
    }
  };

  const consentLabels: Record<string, { label: string; desc: string; critical: boolean }> = {
    data_processing: { label: 'Data Processing', desc: 'Allow NutriAI to process your personal data for nutritional research', critical: true },
    health_data: { label: 'Health & Lab Data', desc: 'Allow processing of health information and lab report data for formulation', critical: true },
    report_ocr: { label: 'Report OCR Analysis', desc: 'Allow automated OCR extraction of your lab reports', critical: false },
    chatbot: { label: 'AI Chatbot', desc: 'Allow the AI assistant to access your formulation data for explanations', critical: false },
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-xl font-bold text-gray-900">Settings & Privacy</h1>

      {/* Language Preference */}
      <Card className="p-5 space-y-4">
        <div className="flex items-center gap-2">
          <Globe className="w-5 h-5 text-primary-600" />
          <h3 className="text-sm font-semibold text-gray-900">Language Preference</h3>
        </div>
        <div className="max-w-xs">
          <Select value={language} onChange={(e) => handleLanguageChange(e.target.value)}>
            <option value="en">English</option>
            <option value="ta">தமிழ் (Tamil)</option>
            <option value="hi">हिन्दी (Hindi)</option>
            <option value="te">తెలుగు (Telugu)</option>
            <option value="ml">മലയാളം (Malayalam)</option>
          </Select>
        </div>
        <p className="text-xs text-gray-500">This updates your preferred language across the app and sets the language for your formulation explanations and chatbot responses.</p>
      </Card>

      {/* Consent Management */}
      <Card className="p-5 space-y-4">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-teal-600" />
          <h3 className="text-sm font-semibold text-gray-900">Consent Management</h3>
        </div>
        <p className="text-xs text-gray-600">View and revoke individual consent categories. Revoking health data consent will disable formulation generation.</p>

        <div className="space-y-3">
          {Object.entries(consentLabels).map(([key, info]) => (
            <div key={key} className="flex items-start justify-between gap-4 p-3 rounded-xl bg-gray-50 border border-gray-200">
              <div className="space-y-0.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-900">{info.label}</span>
                  {info.critical && (
                    <span className="text-[10px] font-bold text-red-700 bg-red-100 px-1.5 py-0.5 rounded">Required for core features</span>
                  )}
                </div>
                <p className="text-xs text-gray-600">{info.desc}</p>
              </div>
              <div className="shrink-0">
                {consentStatuses[key] ? (
                  <button
                    onClick={() => handleRevokeConsent(key)}
                    disabled={consentRevoking === key}
                    className="text-xs text-red-600 hover:underline font-medium disabled:opacity-50"
                  >
                    {consentRevoking === key ? 'Revoking…' : 'Revoke'}
                  </button>
                ) : (
                  <span className="text-xs text-gray-400 italic">Revoked</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Data Export */}
      <Card className="p-5 space-y-4">
        <div className="flex items-center gap-2">
          <Download className="w-5 h-5 text-blue-600" />
          <h3 className="text-sm font-semibold text-gray-900">Export My Data</h3>
        </div>
        <p className="text-xs text-gray-600">Download a full export of your data in JSON format including profile, formulations, lab reports metadata, orders, and progress logs.</p>
        {exportSuccess ? (
          <div className="flex items-center gap-2 text-xs text-emerald-700">
            <CheckCircle2 className="w-4 h-4" /> Export downloaded successfully.
          </div>
        ) : (
          <Button variant="outline" onClick={handleExportData} disabled={exporting}>
            <Download className="w-4 h-4 mr-2" />
            {exporting ? 'Preparing export…' : 'Download Data Export (JSON)'}
          </Button>
        )}
      </Card>

      {/* Medical Disclaimer */}
      <MedicalDisclaimer />

      {/* Sign Out */}
      <Card className="p-5 space-y-4">
        <div className="flex items-center gap-2">
          <LogOut className="w-5 h-5 text-gray-500" />
          <h3 className="text-sm font-semibold text-gray-900">Sign Out</h3>
        </div>
        <Button variant="outline" onClick={() => { logout(); navigate('/'); }}>
          Sign Out of NutriAI
        </Button>
      </Card>

      {/* Danger Zone: Delete Account */}
      <Card className="p-5 space-y-4 border-red-200 bg-red-50/40">
        <div className="flex items-center gap-2">
          <Trash2 className="w-5 h-5 text-red-600" />
          <h3 className="text-sm font-semibold text-red-900">Delete Account</h3>
        </div>
        <p className="text-xs text-red-700">
          Permanently deletes your account, all health data, lab reports, formulations, and progress logs. This action cannot be undone.
        </p>
        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-red-700 mb-1">Type your email address to confirm:</label>
            <input
              type="email"
              value={confirmDelete}
              onChange={(e) => { setConfirmDelete(e.target.value); setDeleteError(''); }}
              placeholder={user?.email || 'your@email.com'}
              className="w-full text-sm px-3 py-2 border border-red-300 rounded-lg focus:ring-2 focus:ring-red-500 bg-white"
            />
          </div>
          {deleteError && (
            <div className="flex items-start gap-2 text-xs text-red-700">
              <AlertTriangle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
              {deleteError}
            </div>
          )}
          <Button
            variant="ghost"
            className="text-red-600 hover:bg-red-100 border border-red-200"
            onClick={handleDeleteAccount}
            disabled={deleting || confirmDelete !== user?.email}
          >
            <Trash2 className="w-4 h-4 mr-2" />
            {deleting ? 'Deleting account…' : 'Permanently Delete My Account'}
          </Button>
        </div>
      </Card>
    </div>
  );
};

