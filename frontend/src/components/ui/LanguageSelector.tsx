import React from 'react';
import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';
import { useAuth } from '../../lib/auth';
import { apiClient } from '../../lib/api';

const LANGUAGES = [
  { code: 'en', label: 'English',   native: 'English' },
  { code: 'ta', label: 'Tamil',     native: 'தமிழ்' },
  { code: 'hi', label: 'Hindi',     native: 'हिन्दी' },
  { code: 'te', label: 'Telugu',    native: 'తెలుగు' },
  { code: 'ml', label: 'Malayalam', native: 'മലയാളം' },
];

export const LanguageSelector: React.FC<{ compact?: boolean }> = ({ compact = false }) => {
  const { i18n } = useTranslation();
  const { user } = useAuth();

  const handleLanguageChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLang = e.target.value;
    await i18n.changeLanguage(newLang);
    document.documentElement.lang = newLang;
    localStorage.setItem('i18nextLng', newLang);

    if (user) {
      try {
        await apiClient.patch('/profile', { preferred_language: newLang });
      } catch {
        // Silent ignore for guest / demo
      }
    }
  };

  return (
    <div className="inline-flex items-center gap-1.5 bg-white border border-gray-200 rounded-lg px-2.5 py-1 text-sm text-gray-700 shadow-sm">
      <Globe className="w-4 h-4 text-primary-600 shrink-0" />
      <select
        value={i18n.language ? i18n.language.split('-')[0] : 'en'}
        onChange={handleLanguageChange}
        className="bg-transparent text-xs sm:text-sm font-medium focus:outline-none cursor-pointer py-1 min-h-0"
        aria-label="Select preferred language"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {compact ? lang.code.toUpperCase() : `${lang.native}`}
          </option>
        ))}
      </select>
    </div>
  );
};
