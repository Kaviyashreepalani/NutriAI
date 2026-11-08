import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { Card } from '../../components/ui/Card';
import { ArrowRight, Cookie, Coffee, GlassWater, Flame, Boxes, CheckCircle2, Info } from 'lucide-react';

const products = [
  {
    id: 'bar',
    title: 'Nutrient-Dense Energy Bar',
    icon: Cookie,
    color: 'bg-emerald-50 border-emerald-200',
    textColor: 'text-emerald-900',
    serving: '35g',
    ironPerServing: '4.8 mg',
    cost: '₹22–28',
    formats: ['Rectangle Bar', 'Bite-size Cubes'],
    ingredients: ['Amaranth (puffed)', 'Garden cress seeds', 'Medjool dates', 'Amla powder', 'Dark jaggery', 'Sesame seeds', 'Almond flakes'],
    desc: 'An on-the-go compact bar with a natural fruit-seed caramel coating. No added sugar; sweetness from dates and jaggery. Amla (Indian gooseberry) provides natural vitamin C for 2.6:1 ascorbic acid to iron molar ratio.',
  },
  {
    id: 'laddoo',
    title: 'Ayurvedic Sesame Laddoo',
    icon: Flame,
    color: 'bg-amber-50 border-amber-200',
    textColor: 'text-amber-900',
    serving: '30g (2 laddoos)',
    ironPerServing: '4.3 mg',
    cost: '₹18–24',
    formats: ['Round Laddoo (15g each)', 'Square Chikki variant'],
    ingredients: ['Black sesame (kala til)', 'Roasted Bengal gram flour', 'Jaggery syrup', 'Dry ginger powder', 'Cardamom', 'Amla powder'],
    desc: 'An aspirational traditional Indian confection reformulated for nutrient density. Black sesame contributes 2.1 mg iron per 100g; Bengal gram adds protein and folate. Familiar taste profile maximizes daily consumability.',
  },
  {
    id: 'breakfast',
    title: 'Fortified Multi-Millet Breakfast Mix',
    icon: Coffee,
    color: 'bg-blue-50 border-blue-200',
    textColor: 'text-blue-900',
    serving: '40g dry mix (makes ~1 cup porridge or 2 dosas)',
    ironPerServing: '5.1 mg',
    cost: '₹16–22',
    formats: ['Porridge (boil with milk/water)', 'Instant Dosa Batter'],
    ingredients: ['Sprouted Ragi (finger millet)', 'Foxtail millet', 'Moringa leaf powder', 'Flaxseed meal', 'Jaggery powder', 'Amla'],
    desc: 'Sprouting ragi reduces phytate content by up to 60%, dramatically improving iron bioavailability. Moringa (drumstick leaves) is one of the richest vegetarian sources of iron at 28 mg/100g dry weight.',
  },
  {
    id: 'drink',
    title: 'Herbal Iron Drink Mix',
    icon: GlassWater,
    color: 'bg-rose-50 border-rose-200',
    textColor: 'text-rose-900',
    serving: '15g sachet (1 glass)',
    ironPerServing: '4.2 mg',
    cost: '₹14–20',
    formats: ['Cold-dissolve sachet', 'Effervescent tablet variant'],
    ingredients: ['Kokum extract', 'Amla concentrate', 'Beetroot powder', 'Micro-encapsulated ferrous fumarate (fortification)', 'Stevia'],
    desc: 'A refreshing summer drink combining natural iron from beetroot with encapsulated ferrous fumarate. Kokum\'s natural tartaric acid creates an acidic environment (pH ~4.5) that significantly enhances non-heme iron absorption.',
  },
  {
    id: 'chikki',
    title: 'Nut & Seed Crispy Chikki',
    icon: Boxes,
    color: 'bg-purple-50 border-purple-200',
    textColor: 'text-purple-900',
    serving: '25g (1 piece)',
    ironPerServing: '3.9 mg',
    cost: '₹12–18',
    formats: ['Traditional square chikki', 'Bite-size rounds'],
    ingredients: ['Groundnut (roasted)', 'Pumpkin seeds', 'Organic dark jaggery', 'Black sesame', 'Amla powder coating'],
    desc: 'A crispy, satisfying traditional Indian sweet. Pumpkin seeds contribute 15 mg iron per 100g dry weight. Jaggery\'s trace minerals (iron: 11 mg/100g) complement seed-based iron. Strictly within ICMR HFSS limits.',
  },
];

export const ProductsPage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      <MedicalDisclaimer />

      <div className="space-y-3">
        <span className="text-xs font-bold uppercase tracking-wider text-primary-700">Research Prototypes</span>
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold text-gray-900">Aspirational Nutrient-Dense Food Products</h1>
            <p className="text-sm text-gray-600 mt-2 max-w-2xl">
              Five prototype product categories formulated using verified IFCT 2017 ingredient data, deterministic linear optimization, and bioavailability science. All products are non-medicinal and positioned as delicious everyday foods.
            </p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <PrototypeBadge />
            <Link to="/register">
              <Button variant="primary" size="sm">
                Get My Personalized Formulation
                <ArrowRight className="w-4 h-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex gap-3 items-start text-xs text-amber-800">
        <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
        <span>All ingredient quantities, nutritional values, and costs shown are calculated deterministically from IFCT 2017 reference data. These are prototype specifications — not commercially manufactured products. Iron delivery values assume bioavailability-optimized ingredient combinations.</span>
      </div>

      <div className="space-y-6">
        {products.map((product) => {
          const Icon = product.icon;
          return (
            <Card key={product.id} className={`p-6 border ${product.color}`}>
              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                {/* Left: Identity */}
                <div className="md:col-span-5 space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="p-2.5 rounded-xl bg-white shadow-xs shrink-0">
                      <Icon className="w-6 h-6 text-gray-700" />
                    </div>
                    <div>
                      <h3 className={`text-base font-bold ${product.textColor}`}>{product.title}</h3>
                      <p className="text-xs text-gray-600 mt-1 leading-relaxed">{product.desc}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      { label: 'Serving', value: product.serving },
                      { label: 'Fe/Serving', value: product.ironPerServing },
                      { label: 'Est. Cost', value: product.cost },
                    ].map((m, idx) => (
                      <div key={idx} className="p-2 rounded-lg bg-white/60 text-center">
                        <div className="text-xs font-bold text-gray-900">{m.value}</div>
                        <div className="text-[10px] text-gray-500 uppercase">{m.label}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Middle: Ingredients */}
                <div className="md:col-span-4 space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700">Key Ingredients</h4>
                  <ul className="space-y-1">
                    {product.ingredients.map((ing, i) => (
                      <li key={i} className="flex items-center gap-2 text-xs text-gray-700">
                        <CheckCircle2 className="w-3.5 h-3.5 text-primary-500 shrink-0" />
                        {ing}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Right: Formats */}
                <div className="md:col-span-3 space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700">Available Formats</h4>
                  <ul className="space-y-1">
                    {product.formats.map((f, i) => (
                      <li key={i} className="text-xs text-gray-700 bg-white/70 rounded-lg px-2.5 py-1.5 border border-gray-200/60">
                        {f}
                      </li>
                    ))}
                  </ul>
                  <Link to="/register">
                    <Button variant="outline" size="sm" className="w-full mt-3 text-xs">
                      Generate Personalized Variant
                      <ArrowRight className="w-3.5 h-3.5 ml-1" />
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <div className="text-center py-6 space-y-3">
        <PrototypeBadge />
        <p className="text-xs text-gray-500 max-w-2xl mx-auto">
          All products are demonstration prototypes with demo checkout. No actual sale, medical claim, or clinical endorsement is implied.
          Nutrient targets comply with ICMR-NIN RDA 2020 for the respective age and life-stage group.
        </p>
      </div>
    </div>
  );
};

