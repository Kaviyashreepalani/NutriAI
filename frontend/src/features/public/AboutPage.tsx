import React from 'react';
import { Card } from '../../components/ui/Card';
import { ExternalLink, Microscope, Database, Shield, Award } from 'lucide-react';

export const AboutPage: React.FC = () => (
  <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
    <div className="space-y-3">
      <span className="text-xs font-bold uppercase tracking-wider text-primary-700">About This Project</span>
      <h1 className="text-3xl font-extrabold text-gray-900">
        Development and Validation of AI-Optimized, Aspirational Nutrient-Dense Food Products
      </h1>
      <p className="text-sm text-gray-600 leading-relaxed max-w-3xl">
        A research prototype developed in response to the ICMR–Gates Foundation Grand Challenge RFP for anaemia prevention among adolescent girls and women of reproductive age in India.
      </p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card className="p-6 space-y-3">
        <div className="flex items-center gap-3">
          <Award className="w-6 h-6 text-primary-600" />
          <h3 className="font-bold text-gray-900">Research Mandate</h3>
        </div>
        <p className="text-sm text-gray-600 leading-relaxed">
          Responding to India's national anaemia burden — where over 57% of women of reproductive age are anaemic (NFHS-5, 2019–21) — this initiative develops aspirational, non-medicinal, daily-consumable food prototypes that deliver 4–5 mg bioavailable iron per serving.
        </p>
      </Card>

      <Card className="p-6 space-y-3">
        <div className="flex items-center gap-3">
          <Database className="w-6 h-6 text-teal-600" />
          <h3 className="font-bold text-gray-900">Data Integrity</h3>
        </div>
        <p className="text-sm text-gray-600 leading-relaxed">
          All ingredient nutritional data is sourced from the Indian Food Composition Tables (IFCT 2017) published by the National Institute of Nutrition (NIN), ICMR. No estimates, interpolations, or unverified values are used in formulation calculations.
        </p>
      </Card>

      <Card className="p-6 space-y-3">
        <div className="flex items-center gap-3">
          <Microscope className="w-6 h-6 text-purple-600" />
          <h3 className="font-bold text-gray-900">Scientific Principles</h3>
        </div>
        <ul className="text-sm text-gray-600 space-y-1.5">
          {[
            'Iron benchmark: 4.0–5.0 mg per serving (configurable)',
            'Vitamin C to iron molar ratio > 2:1 for absorption enhancement',
            'Phytate-to-iron molar ratio ≤ 1:1 hard upper bound',
            'HFSS compliance: total fat, saturated fat, sugar, sodium caps',
            'Affordability target: ≤ ₹30 per serving at FMCG scale',
          ].map((pt, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-2 shrink-0" />
              {pt}
            </li>
          ))}
        </ul>
      </Card>

      <Card className="p-6 space-y-3">
        <div className="flex items-center gap-3">
          <Shield className="w-6 h-6 text-amber-600" />
          <h3 className="font-bold text-gray-900">Safety & Ethics Commitments</h3>
        </div>
        <ul className="text-sm text-gray-600 space-y-1.5">
          {[
            'Platform does not diagnose, prescribe, or treat any condition',
            'Non-iron anaemia safeguards prevent inappropriate iron products',
            'Red-flag lab values block formulation and suggest clinical care',
            'All users < 18 years require documented guardian consent',
            'Column-level AES-256-GCM encryption for sensitive health data',
          ].map((pt, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-2 shrink-0" />
              {pt}
            </li>
          ))}
        </ul>
      </Card>
    </div>

    <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-3 text-xs text-gray-600">
      <h4 className="font-semibold text-gray-900 text-sm">References & Guidelines</h4>
      <ul className="space-y-1.5">
        {[
          { label: 'ICMR-NIN Recommended Dietary Allowances 2020', url: 'https://www.nin.res.in' },
          { label: 'National Family Health Survey (NFHS-5), 2019–21', url: 'https://rchiips.org/nfhs/nfhs-5Reports/NFHS-5_INDIA_REPORT.pdf' },
          { label: 'Indian Food Composition Tables, IFCT 2017', url: 'https://www.nin.res.in/ifct2017.html' },
          { label: 'ICMR Grand Challenge – Aspirational Foods RFP', url: 'https://main.icmr.nic.in/' },
        ].map((ref, i) => (
          <li key={i}>
            <a href={ref.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-primary-700 hover:underline">
              {ref.label}
              <ExternalLink className="w-3 h-3" />
            </a>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

