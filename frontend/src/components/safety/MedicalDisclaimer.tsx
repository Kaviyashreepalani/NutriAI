import React from 'react';
import { useTranslation } from 'react-i18next';
import { ShieldAlert } from 'lucide-react';

interface MedicalDisclaimerProps {
  compact?: boolean;
  className?: string;
}

export const MedicalDisclaimer: React.FC<MedicalDisclaimerProps> = ({ compact = false, className = '' }) => {
  const { t } = useTranslation();

  return (
    <div
      className={`rounded-xl border border-gray-200 bg-gray-50 text-gray-700 ${
        compact ? 'p-3 text-xs' : 'p-4 text-sm'
      } flex items-start gap-3 ${className}`}
      role="note"
      aria-label="Medical safety notice"
    >
      <ShieldAlert className={`text-primary-700 shrink-0 ${compact ? 'w-4 h-4 mt-0.5' : 'w-5 h-5 mt-0.5'}`} />
      <div className="leading-relaxed">
        <strong className="font-semibold text-gray-900 block mb-0.5">Medical &amp; Safety Notice:</strong>
        {t('safety.disclaimer', 'This platform supports nutritional awareness and may help meet nutrient needs. It does not diagnose, prescribe, treat, or cure any medical condition. Always consult a qualified healthcare professional for medical advice.')}
      </div>
    </div>
  );
};
