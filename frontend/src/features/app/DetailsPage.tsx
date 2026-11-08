import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import {
  BookOpen,
  HeartPulse,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ChevronRight,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const DetailsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'what' | 'symptoms' | 'diet' | 'targets' | 'safety'>('what');

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Top Banner & Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2.5">
            <BookOpen className="w-6 h-6 text-primary-600" />
            Details (About Anaemia)
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Essential knowledge about iron deficiency, symptoms, absorption science, and ICMR guidelines.
          </p>
        </div>
        <PrototypeBadge />
      </div>

      <MedicalDisclaimer />

      {/* Clean Tab Bar */}
      <div className="flex flex-wrap gap-2 border-b border-gray-200 pb-2">
        {[
          { id: 'what', label: '1. What is Anaemia?' },
          { id: 'symptoms', label: '2. Signs & Symptoms' },
          { id: 'diet', label: '3. Food & Absorption' },
          { id: 'targets', label: '4. ICMR Daily Targets' },
          { id: 'safety', label: '5. When to See a Doctor' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === tab.id
                ? 'bg-primary-600 text-white shadow-sm'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab 1: What is Anaemia */}
      {activeTab === 'what' && (
        <div className="space-y-4">
          <Card className="p-6 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-red-50 text-red-600 flex items-center justify-center">
                <HeartPulse className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-gray-900">What is Anaemia?</h3>
                <p className="text-xs text-gray-500">Definition and Indian epidemiological context</p>
              </div>
            </div>

            <p className="text-sm text-gray-700 leading-relaxed">
              Anaemia is a condition where your blood has a lower than normal amount of healthy red blood cells or haemoglobin. Haemoglobin is the iron-rich protein that carries oxygen from your lungs to every organ and tissue in your body. When haemoglobin levels fall, your body receives less oxygen, leading to fatigue and weakness.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-primary-50/60 border border-primary-100">
                <span className="text-xs font-bold text-primary-800 uppercase tracking-wider block mb-1">Prevalence</span>
                <p className="text-2xl font-black text-primary-700">57%+</p>
                <p className="text-xs text-gray-600 mt-1">
                  According to NFHS-5, more than half of adolescent girls and women of reproductive age in India are anaemic.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-100">
                <span className="text-xs font-bold text-amber-800 uppercase tracking-wider block mb-1">Primary Cause</span>
                <p className="text-2xl font-black text-amber-700">Iron Deficiency</p>
                <p className="text-xs text-gray-600 mt-1">
                  Low dietary iron bioavailability and phytate-rich cereals are the leading contributors in India.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-blue-50/60 border border-blue-100">
                <span className="text-xs font-bold text-blue-800 uppercase tracking-wider block mb-1">Our Approach</span>
                <p className="text-2xl font-black text-blue-700">Food-First</p>
                <p className="text-xs text-gray-600 mt-1">
                  ICMR Grand Challenge focus: delicious, nutrient-dense daily foods instead of unpalatable tablets.
                </p>
              </div>
            </div>

            <div className="pt-2">
              <Link to="/app/generate">
                <Button variant="primary" className="w-full sm:w-auto">
                  <Sparkles className="w-4 h-4 mr-2" />
                  Generate Your Personalized Product
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      )}

      {/* Tab 2: Symptoms */}
      {activeTab === 'symptoms' && (
        <div className="space-y-4">
          <Card className="p-6 space-y-4">
            <h3 className="text-base font-bold text-gray-900">Common Signs & Symptoms</h3>
            <p className="text-xs text-gray-600">
              Anaemia often develops slowly. Early signs are frequently mistaken for everyday stress or tiredness.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {[
                { title: 'Persistent Fatigue & Weakness', desc: 'Feeling constantly tired even after a full night of sleep.' },
                { title: 'Pale or Yellowish Skin', desc: 'Noticeable paleness on face, inner eyelids, gums, or nail beds.' },
                { title: 'Dizziness or Lightheadedness', desc: 'Feeling faint when standing up quickly due to reduced oxygen delivery.' },
                { title: 'Cold Hands & Feet', desc: 'Poor peripheral circulation leaving fingers and toes cold.' },
                { title: 'Shortness of Breath', desc: 'Feeling winded during normal daily activities like walking or climbing stairs.' },
                { title: 'Brittle Nails & Hair Fall', desc: 'Nails splitting or flattening (koilonychia) and accelerated hair shedding.' },
              ].map((item, idx) => (
                <div key={idx} className="p-3.5 rounded-xl border border-gray-100 bg-gray-50/60 flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary-600 mt-1.5 shrink-0" />
                  <div>
                    <h4 className="text-xs font-bold text-gray-900">{item.title}</h4>
                    <p className="text-xs text-gray-600 mt-0.5">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* Tab 3: Food & Absorption Science */}
      {activeTab === 'diet' && (
        <div className="space-y-4">
          <Card className="p-6 space-y-5">
            <div>
              <h3 className="text-base font-bold text-gray-900">Food Sources & Absorption Science</h3>
              <p className="text-xs text-gray-600 mt-1">
                Eating iron is only half the battle. Your body must actually absorb it (bioavailability).
              </p>
            </div>

            {/* Iron Boosters vs Blockers */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 space-y-2">
                <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs uppercase tracking-wide">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Absorption Boosters (Do These)
                </div>
                <ul className="text-xs text-emerald-950 space-y-1.5 pl-1">
                  <li>• <strong>Vitamin C:</strong> Consuming Amla, lemon, guava, or oranges with iron-rich meals boosts non-heme iron absorption by up to 300%.</li>
                  <li>• <strong>Sprouting & Fermentation:</strong> Reduces anti-nutrient phytates naturally in legumes and millets.</li>
                  <li>• <strong>Cast Iron Cooking:</strong> Enhances elemental iron content in traditional preparations.</li>
                </ul>
              </div>

              <div className="p-4 rounded-xl bg-red-50 border border-red-200 space-y-2">
                <div className="flex items-center gap-2 text-red-800 font-bold text-xs uppercase tracking-wide">
                  <XCircle className="w-4 h-4 text-red-600" />
                  Absorption Inhibitors (Avoid Near Meals)
                </div>
                <ul className="text-xs text-red-950 space-y-1.5 pl-1">
                  <li>• <strong>Tea & Coffee:</strong> Polyphenols and tannins strongly bind iron. Wait at least 1 hour after meals.</li>
                  <li>• <strong>Calcium Supplements:</strong> Compete for the same intestinal absorption pathways. Take 2 hours apart.</li>
                  <li>• <strong>Unprocessed Bran / Phytates:</strong> High phytic acid binds iron into insoluble complexes.</li>
                </ul>
              </div>
            </div>

            {/* Top Indian Food Ingredients */}
            <div className="pt-2 space-y-2">
              <h4 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                Top Bioavailable Indian Ingredients in NutriAI
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {[
                  { name: 'Moringa Leaves', note: '28 mg iron / 100g dry', tag: 'Herb' },
                  { name: 'Garden Cress (Halim)', note: '100 mg iron / 100g', tag: 'Seeds' },
                  { name: 'Black Sesame', note: 'Rich in iron & zinc', tag: 'Seeds' },
                  { name: 'Sprouted Ragi', note: 'High calcium & iron', tag: 'Millet' },
                ].map((ing, i) => (
                  <div key={i} className="p-3 rounded-lg border border-gray-200 bg-white text-center">
                    <p className="text-xs font-bold text-gray-900">{ing.name}</p>
                    <p className="text-[11px] text-primary-700 font-medium mt-0.5">{ing.note}</p>
                    <span className="inline-block mt-1 text-[9px] px-1.5 py-0.5 bg-gray-100 rounded text-gray-600">
                      {ing.tag}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Tab 4: ICMR RDA Targets */}
      {activeTab === 'targets' && (
        <div className="space-y-4">
          <Card className="p-6 space-y-4">
            <div>
              <h3 className="text-base font-bold text-gray-900">ICMR-NIN 2020 Recommended Dietary Allowances (RDA)</h3>
              <p className="text-xs text-gray-600 mt-1">
                Official Indian clinical benchmarks for women and adolescent girls:
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-gray-100 text-gray-700 uppercase font-semibold text-[10px]">
                  <tr>
                    <th className="p-3 rounded-l-lg">Target Group</th>
                    <th className="p-3">Iron (mg/day)</th>
                    <th className="p-3">Vitamin C (mg/day)</th>
                    <th className="p-3">Folate (µg/day)</th>
                    <th className="p-3 rounded-r-lg">Vitamin B12 (µg/day)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 text-gray-800">
                  <tr>
                    <td className="p-3 font-medium">Adolescent Girls (13–15 yrs)</td>
                    <td className="p-3 font-bold text-primary-700">30 mg</td>
                    <td className="p-3">66 mg</td>
                    <td className="p-3">245 µg</td>
                    <td className="p-3">2.2 µg</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium">Adolescent Girls (16–18 yrs)</td>
                    <td className="p-3 font-bold text-primary-700">32 mg</td>
                    <td className="p-3">68 mg</td>
                    <td className="p-3">270 µg</td>
                    <td className="p-3">2.2 µg</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium">Adult Women (19–49 yrs, Non-pregnant)</td>
                    <td className="p-3 font-bold text-primary-700">29 mg</td>
                    <td className="p-3">65 mg</td>
                    <td className="p-3">220 µg</td>
                    <td className="p-3">2.2 µg</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium">Pregnant Women</td>
                    <td className="p-3 font-bold text-amber-700">27 mg</td>
                    <td className="p-3">80 mg</td>
                    <td className="p-3">570 µg</td>
                    <td className="p-3">2.5 µg</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-[11px] text-gray-500 italic">
              Source: ICMR-National Institute of Nutrition (NIN) Dietary Guidelines & Nutrient Requirements for Indians.
            </p>
          </Card>
        </div>
      )}

      {/* Tab 5: Safety & Medical Red Flags */}
      {activeTab === 'safety' && (
        <div className="space-y-4">
          <Card className="p-6 space-y-4 border-l-4 border-l-red-500">
            <div className="flex items-center gap-2.5 text-red-700 font-bold text-sm">
              <ShieldAlert className="w-5 h-5 text-red-600" />
              When to Consult a Qualified Doctor Immediately
            </div>

            <p className="text-xs text-gray-700 leading-relaxed">
              NutriAI develops nutritional food prototypes for prevention and dietary support. It is <strong>not a medical diagnostic tool or prescription replacement</strong>. You should seek direct clinical attention if you experience:
            </p>

            <div className="space-y-2 text-xs text-gray-800">
              <div className="p-3 rounded-lg bg-red-50/60 border border-red-100 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                <span><strong>Severe Anaemia:</strong> Haemoglobin test report below 8.0 g/dL requires clinical medical intervention.</span>
              </div>
              <div className="p-3 rounded-lg bg-red-50/60 border border-red-100 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                <span><strong>Thalassaemia Trait or Iron Overload:</strong> Low MCV (&lt;80 fL) with normal or elevated Ferritin (&gt;150 ng/mL). Iron supplementation can be hazardous in these cases.</span>
              </div>
              <div className="p-3 rounded-lg bg-red-50/60 border border-red-100 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                <span><strong>Pregnancy with Complications:</strong> Always consult your obstetrician for clinical prenatal care.</span>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

