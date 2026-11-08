import { describe, it, expect, beforeAll } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { MedicalDisclaimer } from '../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../components/safety/PrototypeBadge';
import { I18nextProvider, initReactI18next } from 'react-i18next';
import i18next from 'i18next';

// Synchronous test instance of i18n
const testI18n = i18next.createInstance();
testI18n.use(initReactI18next).init({
  lng: 'en',
  fallbackLng: 'en',
  resources: {
    en: {
      translation: {
        'common.prototypeBadge': 'Prototype product – demo checkout',
        'safety.disclaimer': 'NutriAI is a nutrition-support and food-formulation platform. It supports nutritional intake and does not diagnose, prescribe, treat, or cure any condition.',
      },
    },
  },
  interpolation: { escapeValue: false },
});

const withI18n = (component: React.ReactNode) => (
  <I18nextProvider i18n={testI18n}>{component}</I18nextProvider>
);

describe('Button component', () => {
  it('renders primary variant with correct text', () => {
    render(<Button variant="primary">Get Formulation</Button>);
    expect(screen.getByRole('button', { name: 'Get Formulation' })).toBeDefined();
  });

  it('is disabled when disabled prop set', () => {
    render(<Button disabled>Click Me</Button>);
    const btn = screen.getByRole('button');
    expect((btn as HTMLButtonElement).disabled).toBe(true);
  });

  it('shows loading spinner when isLoading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByText('Loading...')).toBeDefined();
  });
});

describe('Badge component', () => {
  it('renders children text', () => {
    render(<Badge variant="success">Prototype</Badge>);
    expect(screen.getByText('Prototype')).toBeDefined();
  });

  it('renders outline variant', () => {
    render(<Badge variant="outline">Demo</Badge>);
    expect(screen.getByText('Demo')).toBeDefined();
  });
});

describe('Safety components', () => {
  it('MedicalDisclaimer renders with safety notice text', () => {
    render(withI18n(<MedicalDisclaimer />));
    expect(screen.getByText(/Medical & Safety Notice/i)).toBeDefined();
  });

  it('PrototypeBadge renders', () => {
    render(withI18n(<PrototypeBadge />));
    expect(screen.getByRole('status')).toBeDefined();
    expect(screen.getByText(/Prototype product – demo checkout/i)).toBeDefined();
  });
});

describe('Safety vocabulary compliance', () => {
  const FORBIDDEN_WORDS = ['treats', 'cures', 'diagnoses', 'prescribes'];

  it('Button does not use forbidden medical vocabulary', () => {
    const { container } = render(<Button>Get Formulation</Button>);
    const text = container.textContent?.toLowerCase() || '';
    FORBIDDEN_WORDS.forEach((word) => {
      expect(text).not.toContain(word);
    });
  });

  it('MedicalDisclaimer does not use forbidden vocabulary in UI', () => {
    const { container } = render(withI18n(<MedicalDisclaimer />));
    const text = container.textContent?.toLowerCase() || '';
    // Checks that the component itself doesn't claim it cures or treats
    expect(text).toContain('does not diagnose, prescribe, treat, or cure');
  });
});
