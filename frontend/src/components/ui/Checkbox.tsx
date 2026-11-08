import React from 'react';

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: React.ReactNode;
  description?: string;
  error?: string;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ id, label, description, error, className = '', ...props }, ref) => {
    const inputId = id || props.name || (typeof label === 'string' ? label.toLowerCase().replace(/[^a-z0-9]/g, '-') : undefined);

    return (
      <div className="flex flex-col gap-1">
        <div className="flex items-start gap-3">
          <input
            ref={ref}
            type="checkbox"
            id={inputId}
            className={`h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500 mt-1 cursor-pointer ${className}`}
            {...props}
          />
          <label htmlFor={inputId} className="cursor-pointer select-none text-sm text-gray-700">
            <span className="font-medium text-xs sm:text-sm">{label}</span>
            {description && <p className="text-xs text-gray-500 mt-0.5">{description}</p>}
          </label>
        </div>
        {error && <p className="text-xs text-red-600 ml-7">{error}</p>}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';
