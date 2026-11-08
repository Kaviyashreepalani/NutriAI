import React from 'react';
import { Check } from 'lucide-react';

export interface StepItem {
  label: string;
  description?: string;
}

interface StepperProps {
  steps: StepItem[];
  currentStep: number; // 0-indexed
  className?: string;
}

export const Stepper: React.FC<StepperProps> = ({ steps, currentStep, className = '' }) => {
  return (
    <nav aria-label="Progress" className={`w-full ${className}`}>
      <ol className="flex items-start w-full overflow-x-auto pb-1">
        {steps.map((step, idx) => {
          const isCompleted = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <li key={idx} className="relative flex-1 flex flex-col items-center min-w-0">
              {/* Connector line */}
              {idx > 0 && (
                <div
                  className={`absolute top-4 left-[-50%] right-[50%] h-0.5 z-0 ${
                    isCompleted ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                />
              )}
              {/* Circle */}
              <div
                className={`relative z-10 w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors ${
                  isCompleted
                    ? 'bg-primary-600 text-white'
                    : isCurrent
                    ? 'border-2 border-primary-600 bg-white text-primary-700 ring-4 ring-primary-50'
                    : 'border-2 border-gray-200 bg-white text-gray-400'
                }`}
                aria-current={isCurrent ? 'step' : undefined}
              >
                {isCompleted ? <Check className="w-4 h-4" /> : idx + 1}
              </div>
              {/* Label */}
              <div className="mt-2 text-center px-1 min-w-0">
                <span
                  className={`block text-[11px] font-semibold truncate ${
                    isCurrent ? 'text-primary-700' : isCompleted ? 'text-gray-700' : 'text-gray-400'
                  }`}
                >
                  {step.label}
                </span>
                {step.description && (
                  <span className="block text-[10px] text-gray-400 truncate">{step.description}</span>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </nav>
  );
};
