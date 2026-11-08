import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { EmptyState } from '../../components/ui/EmptyState';
import { BookOpen, ArrowRight, Clock, Tag, ChevronLeft } from 'lucide-react';

export const LearnPage: React.FC = () => {
  const [modules, setModules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModules = async () => {
      try {
        const res = await api.get('/learn');
        setModules(res.data || []);
      } catch {
        // Use static fallback content
        setModules([
          { id: 'anaemia-basics', title: 'Understanding Anaemia', category: 'Foundations', read_time_min: 5, summary: 'What is anaemia, its types, and why iron deficiency is the most common form in India.', tags: ['anaemia', 'iron', 'basics'] },
          { id: 'bioavailability', title: 'Iron Bioavailability & Absorption', category: 'Nutrition Science', read_time_min: 7, summary: 'How vitamin C enhances iron absorption and how phytates in Indian diets inhibit it.', tags: ['bioavailability', 'vitamin C', 'phytate'] },
          { id: 'indian-foods-iron', title: 'Iron-Rich Indian Foods', category: 'Food & Diet', read_time_min: 6, summary: 'A guide to the richest vegetarian iron sources in Indian cuisine — moringa, garden cress, sesame.', tags: ['foods', 'moringa', 'sesame', 'Indian diet'] },
          { id: 'icmr-rda', title: 'ICMR-NIN Recommended Dietary Allowances', category: 'Clinical Guidelines', read_time_min: 8, summary: 'RDA values for iron, folate, B12, and vitamin C across life stages (adolescent girls, women 20–49).', tags: ['ICMR', 'RDA', 'guidelines'] },
          { id: 'thalassaemia', title: 'Thalassaemia Trait vs. Iron Deficiency', category: 'Clinical Safety', read_time_min: 6, summary: 'Why low MCV with normal ferritin is a critical safety signal and what it means for formulation.', tags: ['thalassaemia', 'safety', 'MCV', 'ferritin'] },
          { id: 'aspirational-foods', title: 'Aspirational Food Products for Anaemia Prevention', category: 'ICMR Grand Challenge', read_time_min: 10, summary: 'The rationale for non-medicinal food formats and why daily consumability beats clinical supplementation.', tags: ['ICMR', 'aspirational', 'food products'] },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchModules();
  }, []);

  const categoryColors: Record<string, string> = {
    'Foundations': 'bg-primary-100 text-primary-800',
    'Nutrition Science': 'bg-teal-100 text-teal-800',
    'Food & Diet': 'bg-emerald-100 text-emerald-800',
    'Clinical Guidelines': 'bg-blue-100 text-blue-800',
    'Clinical Safety': 'bg-red-100 text-red-800',
    'ICMR Grand Challenge': 'bg-amber-100 text-amber-800',
  };

  if (loading) return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
      {[1, 2, 3, 4].map(i => <div key={i} className="h-40 bg-gray-200 rounded-2xl animate-pulse" />)}
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <MedicalDisclaimer />

      <div>
        <h1 className="text-xl font-bold text-gray-900">Anaemia & Nutrition Guide</h1>
        <p className="text-sm text-gray-600 mt-1">Multilingual educational content grounded in ICMR-NIN guidelines and peer-reviewed research.</p>
      </div>

      {modules.length === 0 ? (
        <EmptyState
          icon={<BookOpen className="w-10 h-10 text-gray-400" />}
          title="No modules available"
          description="Educational content is being prepared."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {modules.map((mod: any) => (
            <Link key={mod.id} to={`/app/learn/${mod.id}`}>
              <Card className="p-5 h-full flex flex-col gap-3 hover:border-primary-300 hover:shadow-md transition group">
                <div className="flex items-start justify-between gap-2">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${categoryColors[mod.category] || 'bg-gray-100 text-gray-700'}`}>
                    {mod.category}
                  </span>
                  <div className="flex items-center gap-1 text-[11px] text-gray-400">
                    <Clock className="w-3 h-3" />
                    {mod.read_time_min} min
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-bold text-gray-900 group-hover:text-primary-700 transition leading-tight">{mod.title}</h3>
                  <p className="text-xs text-gray-600 mt-1.5 leading-relaxed">{mod.summary}</p>
                </div>
                <div className="flex items-center justify-between pt-2 border-t border-gray-100">
                  <div className="flex flex-wrap gap-1">
                    {(mod.tags || []).slice(0, 2).map((tag: string) => (
                      <span key={tag} className="inline-flex items-center gap-0.5 text-[10px] text-gray-500">
                        <Tag className="w-2.5 h-2.5" />{tag}
                      </span>
                    ))}
                  </div>
                  <span className="text-xs text-primary-600 font-medium flex items-center gap-1 group-hover:gap-2 transition-all">
                    Read <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export const LearnDetailPage: React.FC = () => {
  const [module, setModule] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const id = window.location.pathname.split('/').pop();

  useEffect(() => {
    const fetchModule = async () => {
      try {
        const res = await api.get(`/learn/${id}`);
        setModule(res.data);
      } catch {
        setModule(null);
      } finally {
        setLoading(false);
      }
    };
    fetchModule();
  }, [id]);

  if (loading) return <div className="max-w-3xl mx-auto h-96 bg-gray-200 rounded-2xl animate-pulse" />;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <MedicalDisclaimer />

      <Link to="/app/learn" className="inline-flex items-center gap-1 text-xs text-primary-600 hover:underline">
        <ChevronLeft className="w-3.5 h-3.5" /> Back to Guide
      </Link>

      {!module ? (
        <EmptyState
          icon={<BookOpen className="w-10 h-10 text-gray-400" />}
          title="Module not found"
          description="This educational module could not be loaded."
        />
      ) : (
        <Card className="p-6 sm:p-8 space-y-6">
          <div className="space-y-3">
            <h1 className="text-2xl font-extrabold text-gray-900">{module.title}</h1>
            <p className="text-xs text-gray-500 flex items-center gap-2">
              <Clock className="w-3.5 h-3.5" />{module.read_time_min} min read • {module.category}
            </p>
          </div>
          <div
            className="prose prose-sm max-w-none text-gray-700 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: module.content_html || `<p>${module.summary}</p><p class="text-gray-400 italic mt-4">Full content is being prepared. Please check back later.</p>` }}
          />
          {module.citations?.length > 0 && (
            <div className="pt-4 border-t border-gray-100 space-y-2">
              <h4 className="text-xs font-semibold text-gray-700 uppercase tracking-wider">References</h4>
              <ul className="space-y-1 text-xs text-gray-600">
                {module.citations.map((cite: string, i: number) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="font-bold text-gray-400 shrink-0">[{i + 1}]</span>
                    <span>{cite}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};

