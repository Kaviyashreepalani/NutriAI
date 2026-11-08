import React from 'react';
import { useTranslation } from 'react-i18next';
import { FlaskConical } from 'lucide-react';

interface PrototypeBadgeProps {
  className?: string;
}

export const PrototypeBadge: React.FC<PrototypeBadgeProps> = ({ className = '' }) => {
  const { t } = useTranslation();

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300 shadow-sm ${className}`}
      role="status"
      aria-label={t('common.prototypeBadge')}
    >
      <FlaskConical className="w-3.5 h-3.5 text-amber-700 animate-pulse" />
      <span>{t('common.prototypeBadge')}</span>
    </div>
  );
};

