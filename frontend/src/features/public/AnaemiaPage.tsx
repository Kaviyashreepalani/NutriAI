import React from 'react';
import { Link } from 'react-router-dom';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { AlertTriangle, ArrowRight, Microscope, Stethoscope, Shield, Info } from 'lucide-react';

export const AnaemiaPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      <MedicalDisclaimer />

      <div className="space-y-3">
        <span className="text-xs font-bold uppercase tracking-wider text-primary-700">Educational Content</span>
        <h1 className="text-3xl font-extrabold text-gray-900">Understanding Anaemia: Causes, Types & Nutritional Management</h1>
        <p className="text-sm text-gray-600 leading-relaxed max-w-3xl">
          Anaemia is not a single disease but a symptom of multiple underlying conditions. Iron deficiency anaemia (IDA) is the most common nutritional cause in India, but other types require different management approaches.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[
          {
            title: 'Iron Deficiency Anaemia (IDA)',
            icon: Microscope,
            color: 'text-primary-700',
            markers: 'Low Hb, Low ferritin, Low MCV, Elevated TIBC',
            desc: 'The most common nutritional cause. Occurs when dietary iron intake is insufficient to compensate for losses from menstruation, growth, or inadequate absorption due to high phytate diets.',
          },
          {
            title: 'Folate Deficiency Anaemia',
            icon: Stethoscope,
            color: 'text-teal-700',
            markers: 'Low Hb, Low folate, Elevated MCV (macrocytosis)',
            desc: 'Green leafy vegetable deficiency combined with high heat cooking destroys folate. Elevated requirements during pregnancy and adolescent growth exacerbate the deficit.',
          },
          {
            title: 'Vitamin B12 Deficiency',
            icon: Shield,
            color: 'text-purple-700',
            markers: 'Low B12, Macrocytosis, Elevated homocysteine',
            desc: 'Exclusively found in animal products; strict vegetarian women are at high risk. B12 deficiency shares anaemia presentation with folate deficiency but has different neural implications.',
          },
          {
            title: 'Beta-Thalassaemia Trait',
            icon: AlertTriangle,
            color: 'text-amber-700',
            markers: 'Low MCV, Normal or High Ferritin, Low MCH',
            desc: 'Genetic variant causing microcytosis that mimics iron deficiency. Iron supplementation is contraindicated and potentially harmful. NutriAI\'s safety gate blocks formulation for this pattern.',
          },
        ].map((item, idx) => {
          const Icon = item.icon;
          return (
            <Card key={idx} className="p-6 space-y-3 hover:border-primary-300 transition">
              <div className="flex items-start gap-3">
                <div className={`mt-0.5 ${item.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-gray-900">{item.title}</h3>
                  <p className="text-xs font-semibold text-gray-500 mt-0.5">Lab Markers: {item.markers}</p>
                  <p className="text-sm text-gray-600 mt-2 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <div className="p-5 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-sm text-amber-900">
          <strong>Important:</strong> Haemoglobin values alone are insufficient to determine the type of anaemia or its treatment. A full iron studies panel including serum ferritin, MCV, MCH, TIBC, and transferrin saturation is necessary for accurate classification. NutriAI uses all available lab markers to generate formulations safely, applying conservative safeguards when markers are ambiguous.
        </div>
      </div>

      <div className="text-center">
        <Link to="/register">
          <Button variant="primary">
            Upload Your Lab Report to Begin
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      </div>
    </div>
  );
};

