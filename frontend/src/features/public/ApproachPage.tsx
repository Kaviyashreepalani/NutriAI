import React from 'react';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { Card } from '../../components/ui/Card';
import { CheckCircle2, Cpu, Scale, FlaskConical, Sparkles } from 'lucide-react';

export const ApproachPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      <MedicalDisclaimer />

      <div className="space-y-3">
        <h1 className="text-3xl font-extrabold text-gray-900">Our Scientific Approach</h1>
        <p className="text-sm text-gray-600 leading-relaxed max-w-3xl">
          Developed in alignment with the ICMR–NIN Recommended Dietary Allowances (2020) and the Gates Foundation Grand Challenge on aspirational nutrient-dense food products.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary-100 text-primary-800 flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-gray-900">Deterministic Optimization</h3>
          </div>
          <ul className="text-sm text-gray-600 space-y-2 leading-relaxed">
            {[
              'SciPy HiGHS linear programming engine for cost-minimization',
              '40+ verified Indian ingredients from IFCT 2017 database',
              'Hard allergen constraints at SQL, optimizer, and validator levels',
              'Iron 4.0 – 5.0 mg per serving as strict constraint (configurable)',
              'Phytate-to-iron molar ratio ≤ 1:1 hard upper bound',
              'HFSS guards: total fat ≤ 20g, saturated fat ≤ 5g, sugar ≤ 15g, sodium ≤ 400mg per 100g',
            ].map((point, i) => (
              <li key={i} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-primary-600 shrink-0 mt-0.5" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-teal-100 text-teal-800 flex items-center justify-center">
              <FlaskConical className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-gray-900">Bioavailability Science</h3>
          </div>
          <ul className="text-sm text-gray-600 space-y-2 leading-relaxed">
            {[
              'Hallberg ascorbic acid enhancement equations (Vitamin C:Fe molar ratio > 2:1)',
              'Phytate inhibition modeled from IFCT values per ingredient',
              'Non-heme iron baseline absorption rate from Indian dietary patterns',
              'Heme iron from egg/meat is separately tracked (optional inclusion)',
              'Sprouting, fermentation, and milling enhancement factors',
            ].map((point, i) => (
              <li key={i} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center">
              <Scale className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-gray-900">Safety Gates & Constraints</h3>
          </div>
          <ul className="text-sm text-gray-600 space-y-2 leading-relaxed">
            {[
              'Hb < 7.0 g/dL: Blocks formulation and shows medical care guidance',
              'Low MCV + High Ferritin: Flags thalassaemia risk, blocks iron-focused products',
              'Age < 18: Requires guardian consent before data collection',
              'All allergen codes enforced as hard SQL AND conditions (not filtered post-facto)',
              'Template-based fallback if LLM unavailable; Number Guard validates all AI text',
            ].map((point, i) => (
              <li key={i} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-gray-900">Aspirational Product Design Principles</h3>
          </div>
          <ul className="text-sm text-gray-600 space-y-2 leading-relaxed">
            {[
              'Non-medicinal: positioned as delicious, everyday food — not supplements',
              'Appealing formats: energy bar, laddoo, chikki, breakfast mix, drink mix',
              'Affordable target ≤ ₹30/serving at FMCG scale',
              'Uses familiar Indian ingredients (sesame, jaggery, moringa, amla, ragi)',
              'Vegetarian by default; diet-class filter respects user preferences',
              'All products display "Prototype – Demo Checkout" badge prominently',
            ].map((point, i) => (
              <li key={i} className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-purple-600 shrink-0 mt-0.5" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
};

