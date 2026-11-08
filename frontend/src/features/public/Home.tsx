import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { api } from '../../lib/api';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import {
  HeartPulse,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Apple,
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  Send,
  Coffee,
  Cookie,
  Flame,
  GlassWater,
  Boxes
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend
} from 'recharts';

export const Home: React.FC = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState<any[]>([]);
  const [statsLoading, setStatsLoading] = useState(true);
  const [contactForm, setContactForm] = useState({ name: '', email: '', message: '' });
  const [contactSuccess, setContactSuccess] = useState(false);
  const [contactError, setContactError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/public/statistics');
        if (Array.isArray(res.data)) {
          setStats(res.data);
        }
      } catch (err) {
        console.warn('Failed to load live statistics, using benchmark data');
      } finally {
        setStatsLoading(false);
      }
    };
    fetchStats();
  }, []);

  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contactForm.email || !contactForm.message) return;
    try {
      await api.post('/public/contact', contactForm);
      setContactSuccess(true);
      setContactForm({ name: '', email: '', message: '' });
    } catch (err) {
      setContactError('Unable to send feedback. Please try again.');
    }
  };

  const nationalAnaemiaData = [
    { group: 'Adolescent Girls (15–19)', prevalence: 59.1, source: 'NFHS-5' },
    { group: 'Women of Repr. Age (15–49)', prevalence: 57.0, source: 'NFHS-5' },
    { group: 'Pregnant Women (15–49)', prevalence: 52.2, source: 'NFHS-5' },
    { group: 'Non-Pregnant Women', prevalence: 57.2, source: 'NFHS-5' },
  ];

  const productFormats = [
    {
      title: 'Nutrient-Dense Energy Bar',
      badge: 'On-the-go snack',
      desc: 'Formulated with amaranth, garden cress seeds, dates, and amla for sustained energy and 4.8 mg bioavailable iron.',
      icon: Cookie,
      color: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    },
    {
      title: 'Ayurvedic Sesame Laddoo',
      badge: 'Traditional taste',
      desc: 'Black sesame, roasted Bengal gram, jaggery, and dry ginger powder naturally paired with ascorbic acid enhancers.',
      icon: Flame,
      color: 'bg-amber-50 text-amber-800 border-amber-200',
    },
    {
      title: 'Fortified Multi-Millet Breakfast Mix',
      badge: 'Porridge / Dosa',
      desc: 'Sprouted ragi, foxtail millet, and moringa leaf powder with low phytate-to-iron molar ratios for optimal absorption.',
      icon: Coffee,
      color: 'bg-blue-50 text-blue-800 border-blue-200',
    },
    {
      title: 'Refreshing Herbal Drink Mix',
      badge: 'Hydration & Iron',
      desc: 'Cold-soluble instant mix of kokum, amla extract, beetroot, and micro-encapsulated ferrous fumarate.',
      icon: GlassWater,
      color: 'bg-rose-50 text-rose-800 border-rose-200',
    },
    {
      title: 'Nut & Seed Crispy Chikki',
      badge: 'Crunchy snack',
      desc: 'Groundnut, roasted pumpkin seeds, and organic jaggery crafted to adhere strictly to ICMR HFSS limits.',
      icon: Boxes,
      color: 'bg-purple-50 text-purple-800 border-purple-200',
    },
  ];

  return (
    <div className="space-y-16 py-8">
      {/* 1. Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-100 text-primary-800 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                ICMR Grand Challenge RFP Prototype
              </span>
              <PrototypeBadge />
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 tracking-tight leading-tight">
              AI-Optimized, Aspirational Nutrient-Dense Food Products for{' '}
              <span className="text-primary-600">Anaemia Prevention</span>
            </h1>

            <p className="text-base sm:text-lg text-gray-600 leading-relaxed">
              Bridging the dietary gap for Indian adolescent girls and women of reproductive age. We combine verified Indian Food Composition Tables (IFCT 2017), deterministic linear optimization, and bioavailability enhancers to formulate delicious, non-medicinal, daily-consumable food prototypes.
            </p>

            <div className="p-4 rounded-xl bg-white border border-gray-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
                  <HeartPulse className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-900">Iron Delivery Benchmark</h4>
                  <p className="text-xs text-gray-500">4.0 – 5.0 mg bioavailable iron per serving with vitamin C pairing</p>
                </div>
              </div>
              <div className="flex items-center gap-2 w-full sm:w-auto">
                <Link to="/register" className="w-full sm:w-auto">
                  <Button variant="primary" className="w-full">
                    Start Assessment
                    <ArrowRight className="w-4 h-4 ml-1.5" />
                  </Button>
                </Link>
                <Link to="/products" className="w-full sm:w-auto">
                  <Button variant="outline" className="w-full">
                    View Formulations
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          <div className="lg:col-span-5">
            <Card className="bg-gradient-to-br from-primary-700 to-emerald-800 text-white p-6 shadow-xl relative overflow-hidden border-0">
              <div className="relative z-10 space-y-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-wider text-primary-200">
                    The One Architectural Rule
                  </span>
                  <Cpu className="w-5 h-5 text-amber-300" />
                </div>
                <h3 className="text-xl font-bold leading-snug">
                  Deterministic Code Does All Numbers. The LLM Only Explains.
                </h3>
                <ul className="text-xs space-y-2.5 text-primary-100">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0 mt-0.5" />
                    <span>OCR parsing and range verification by deterministic code</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0 mt-0.5" />
                    <span>Linear programming (SciPy HiGHS) calculates grams and costs</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0 mt-0.5" />
                    <span>Number Guard audits all AI explanations to eliminate hallucinations</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0 mt-0.5" />
                    <span>Strict safety gates prevent formulation on critical red-flags</span>
                  </li>
                </ul>
                <div className="pt-2 border-t border-primary-600/50 flex items-center justify-between text-[11px] text-primary-200">
                  <span>Target Demographics: 10–49 Years</span>
                  <span>5 Indian Languages</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* 2. Indian National Anaemia Statistics & Recharts Visualizer */}
      <section className="bg-white py-12 border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="text-center max-w-3xl mx-auto space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-primary-700">Epidemiological Evidence</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
              The Anaemia Burden in Indian Women & Adolescent Girls
            </h2>
            <p className="text-sm text-gray-600">
              Data compiled from the National Family Health Survey (NFHS-5, 2019–21). Over half of Indian adolescent girls and women suffer from nutritional anaemia.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Recharts Bar Chart */}
            <div className="lg:col-span-7 bg-[#F7F9F8] p-4 sm:p-6 rounded-2xl border border-gray-200">
              <h3 className="text-sm font-semibold text-gray-900 mb-4 flex items-center justify-between">
                <span>Prevalence of Anaemia (% Hb &lt; 12.0 g/dL)</span>
                <span className="text-xs text-gray-500 font-normal">NFHS-5 National Factsheet</span>
              </h3>
              <div className="h-64 sm:h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={nationalAnaemiaData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                    <XAxis dataKey="group" tick={{ fontSize: 11 }} interval={0} angle={-10} textAnchor="end" />
                    <YAxis domain={[0, 80]} tick={{ fontSize: 11 }} unit="%" />
                    <Tooltip
                      formatter={(val: any) => [`${val}%`, 'Anaemia Prevalence']}
                      contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                    />
                    <Bar dataKey="prevalence" radius={[6, 6, 0, 0]}>
                      {nationalAnaemiaData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={index === 0 ? '#2E7D32' : '#00897B'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Fact Cards */}
            <div className="lg:col-span-5 space-y-4">
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                <div className="text-2xl font-black text-emerald-900">59.1%</div>
                <div className="text-xs font-semibold text-emerald-800">Adolescent Girls (15–19 years)</div>
                <p className="text-xs text-emerald-700 mt-1">
                  Adolescent growth spurts and menarche exponentially increase iron and folate requirements, rarely met by current diets.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-teal-50 border border-teal-200">
                <div className="text-2xl font-black text-teal-900">57.0%</div>
                <div className="text-xs font-semibold text-teal-800">All Women of Reproductive Age (15–49 years)</div>
                <p className="text-xs text-teal-700 mt-1">
                  High phytate consumption from unrefined cereals binds dietary iron, resulting in poor non-heme bioavailability (&lt; 5–8%).
                </p>
              </div>

              <div className="p-4 rounded-xl bg-amber-50 border border-amber-200">
                <div className="flex items-center gap-1.5 text-xs font-bold text-amber-900">
                  <AlertTriangle className="w-4 h-4 text-amber-700" />
                  <span>Important Diagnostic Notice</span>
                </div>
                <p className="text-xs text-amber-800 mt-1">
                  Haemoglobin alone cannot determine the etiology. Microcytosis with normal or elevated ferritin suggests beta-thalassaemia trait or chronic inflammation, where supplemental iron is contraindicated.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. The 5-Stage Scientific Pipeline */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto space-y-2 mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-primary-700">ICMR-Aligned Architecture</span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
            How NutriAI Formulates Bioavailable Nutrition
          </h2>
          <p className="text-sm text-gray-600">
            A 100% deterministic formulation pipeline ensuring safety, affordability, and nutritional efficacy.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {[
            {
              step: '01',
              title: 'OCR & Parsing',
              desc: 'PyMuPDF and fuzzy matching parse blood counts and iron profile reports with canonical unit conversion.',
            },
            {
              step: '02',
              title: 'Clinical Safety Gate',
              desc: 'Flags extreme Hb (< 7.0 g/dL), thalassaemia risk, or ferritin anomalies to block generation and advise clinical care.',
            },
            {
              step: '03',
              title: 'Linear Optimizer',
              desc: 'SciPy HiGHS solves minimum-cost linear programming against 40+ verified Indian ingredients in IFCT 2017.',
            },
            {
              step: '04',
              title: 'Bioavailability Engine',
              desc: 'Applies Hallberg equations to optimize Vitamin C to Non-Heme Iron molar ratio (> 2:1) and phytate reduction.',
            },
            {
              step: '05',
              title: 'Aspirational Prototype',
              desc: 'Generates real formulation specifications, cost breakdowns, and demo checkout prototype orders.',
            },
          ].map((item, idx) => (
            <Card key={idx} className="p-4 flex flex-col justify-between border-gray-200 hover:border-primary-300 transition">
              <div>
                <span className="text-2xl font-black text-primary-600 block mb-2">{item.step}</span>
                <h4 className="text-sm font-bold text-gray-900 mb-1">{item.title}</h4>
                <p className="text-xs text-gray-600 leading-relaxed">{item.desc}</p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* 4. Product Categories */}
      <section className="bg-white py-12 border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-primary-700">Aspirational Prototypes</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
                Diverse Food Formats for Daily Consumption
              </h2>
            </div>
            <Link to="/products">
              <Button variant="outline" size="sm">
                Explore All Prototypes
                <ArrowRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {productFormats.map((p, idx) => {
              const Icon = p.icon;
              return (
                <div key={idx} className={`p-5 rounded-2xl border ${p.color} flex flex-col justify-between`}>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="p-2 rounded-xl bg-white shadow-xs">
                        <Icon className="w-5 h-5 text-gray-800" />
                      </div>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-white/80">
                        {p.badge}
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-gray-900">{p.title}</h3>
                    <p className="text-xs text-gray-700 leading-relaxed">{p.desc}</p>
                  </div>
                  <div className="pt-4 mt-4 border-t border-black/5 flex items-center justify-between text-xs font-semibold">
                    <span>4.5 mg Bioavailable Fe</span>
                    <span>Demo Prototype</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 5. Contact & Clinical Disclaimer */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <MedicalDisclaimer />

        {/* Contact Form */}
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-gray-200 shadow-sm max-w-2xl mx-auto">
          <div className="text-center space-y-2 mb-6">
            <h3 className="text-xl font-bold text-gray-900">Connect with the Research Team</h3>
            <p className="text-xs text-gray-600">
              Inquiries regarding ICMR Grand Challenge protocols, food scientist partnerships, or prototype feedback.
            </p>
          </div>

          {contactSuccess ? (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-center text-xs text-emerald-800">
              <CheckCircle2 className="w-6 h-6 text-emerald-600 mx-auto mb-2" />
              Thank you! Your feedback has been recorded in the research log.
            </div>
          ) : (
            <form onSubmit={handleContactSubmit} className="space-y-4">
              {contactError && <p className="text-xs text-red-600">{contactError}</p>}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Your Name</label>
                  <input
                    type="text"
                    value={contactForm.name}
                    onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                    className="w-full text-xs px-3 py-2 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="Dr. / Ms. Jane Doe"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={contactForm.email}
                    onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                    className="w-full text-xs px-3 py-2 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="researcher@institute.org"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Message or Query *</label>
                <textarea
                  rows={3}
                  required
                  value={contactForm.message}
                  onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                  className="w-full text-xs px-3 py-2 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Share your thoughts on food formulation, safety parameters, or clinical trials..."
                />
              </div>
              <Button type="submit" variant="primary" className="w-full">
                <Send className="w-4 h-4 mr-1.5" />
                Submit Feedback
              </Button>
            </form>
          )}
        </div>
      </section>
    </div>
  );
};

