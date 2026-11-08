import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { api } from '../../lib/api';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import { Badge } from '../../components/ui/Badge';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import {
  ChevronDown,
  ChevronUp,
  ShoppingCart,
  Download,
  Info,
  CheckCircle2,
  Layers,
  FlaskConical,
  Scale,
  IndianRupee,
  ArrowRight,
  BookOpen,
} from 'lucide-react';

interface NutrientRow {
  nutrient: string;
  per_serving: string | null;
  per_100g: string | null;
  rda_pct: string | null;
  unit: string;
}

interface IngredientRow {
  name: string;
  quantity_g: number;
  iron_contribution_mg: number;
  vitc_contribution_mg: number;
  cost_inr: number;
}

interface FormulationResult {
  id: string;
  product_name: string;
  format: string;
  serving_size_g: number;
  iron_mg: number;
  vitc_mg: number;
  bioavailability_index: number;
  cost_inr: number;
  cost_per_month_inr: number;
  nutrients: NutrientRow[];
  ingredients: IngredientRow[];
  preparation_instructions: string;
  storage_instructions: string;
  why_selected: string;
  allergens_free: string[];
  diet_class: string;
  safety_note: string;
}

export const ResultsPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const formulationId = searchParams.get('formulation_id');
  const [result, setResult] = useState<FormulationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showWhy, setShowWhy] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);
  const [cartSuccess, setCartSuccess] = useState(false);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (!formulationId) return;
    const fetchResult = async () => {
      try {
        const res = await api.get(`/formulations/${formulationId}`);
        setResult(res.data);
      } catch (err: any) {
        setError('Could not load formulation. Please return to generate a new one.');
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [formulationId]);

  const handleAddToCart = async () => {
    if (!result) return;
    setAddingToCart(true);
    try {
      await api.post('/cart/items', { formulation_id: result.id, quantity: 1 });
      setCartSuccess(true);
    } catch {
      setError('Could not add to cart. Please try again.');
    } finally {
      setAddingToCart(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!result) return;
    setDownloading(true);
    try {
      const res = await api.get(`/formulations/${result.id}/pdf`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = `NutriAI_Formulation_${result.id}.pdf`;
      a.click();
    } catch {
      setError('PDF generation failed. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return (
    <div className="max-w-4xl mx-auto space-y-4">
      <div className="h-32 bg-gray-200 rounded-2xl animate-pulse" />
      <div className="h-64 bg-gray-200 rounded-2xl animate-pulse" />
    </div>
  );

  if (!result) return (
    <div className="max-w-4xl mx-auto text-center py-16">
      <FlaskConical className="w-12 h-12 text-gray-300 mx-auto mb-3" />
      <h2 className="text-lg font-semibold text-gray-700">No formulation found</h2>
      <p className="text-sm text-gray-500 mt-1">{error || 'Please upload a lab report to generate a formulation.'}</p>
      <Link to="/app/generate" className="mt-4 inline-block">
        <Button variant="primary">
          <FlaskConical className="w-4 h-4 mr-2" />
          Generate Formulation
        </Button>
      </Link>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <MedicalDisclaimer />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-2">
            <PrototypeBadge />
            <Badge variant="outline" className="text-teal-700 border-teal-300 bg-teal-50">
              {result.diet_class}
            </Badge>
            <Badge variant="outline" className="text-primary-700 border-primary-300 bg-primary-50">
              {result.format}
            </Badge>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-gray-900">{result.product_name}</h1>
          <p className="text-xs text-amber-800 bg-amber-50 border border-amber-200 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg">
            <Info className="w-3.5 h-3.5 text-amber-600 shrink-0" />
            {result.safety_note}
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <Button variant="outline" size="sm" onClick={handleDownloadPDF} disabled={downloading}>
            <Download className="w-4 h-4 mr-1.5" />
            {downloading ? 'Preparing PDF…' : 'Download PDF'}
          </Button>
          {cartSuccess ? (
            <Link to="/app/cart">
              <Button variant="primary" size="sm">
                <ShoppingCart className="w-4 h-4 mr-1.5" />
                View Cart
              </Button>
            </Link>
          ) : (
            <Button variant="primary" size="sm" onClick={handleAddToCart} disabled={addingToCart}>
              <ShoppingCart className="w-4 h-4 mr-1.5" />
              {addingToCart ? 'Adding…' : 'Add to Cart (Demo)'}
            </Button>
          )}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Iron per Serving', value: `${result.iron_mg.toFixed(1)} mg`, sub: 'Bioavailable', icon: FlaskConical, color: 'text-primary-700 bg-primary-50 border-primary-200' },
          { label: 'Serving Size', value: `${result.serving_size_g} g`, sub: 'Per portion', icon: Scale, color: 'text-teal-700 bg-teal-50 border-teal-200' },
          { label: 'Bioavailability Index', value: `${(result.bioavailability_index * 100).toFixed(0)}%`, sub: 'Enhanced with Vit C', icon: CheckCircle2, color: 'text-emerald-700 bg-emerald-50 border-emerald-200' },
          { label: 'Est. Cost / Serving', value: `₹${result.cost_inr.toFixed(0)}`, sub: `~₹${result.cost_per_month_inr.toFixed(0)}/month`, icon: IndianRupee, color: 'text-amber-700 bg-amber-50 border-amber-200' },
        ].map((m, i) => {
          const Icon = m.icon;
          return (
            <div key={i} className={`p-4 rounded-xl border ${m.color} space-y-2`}>
              <Icon className="w-5 h-5" />
              <div>
                <div className="text-lg font-black">{m.value}</div>
                <div className="text-[11px] font-semibold">{m.label}</div>
                <div className="text-[10px] opacity-70">{m.sub}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Why Selected — Expandable */}
      <Card className="p-5">
        <button
          className="w-full flex items-center justify-between text-left"
          onClick={() => setShowWhy(!showWhy)}
        >
          <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-primary-600" />
            Why was this product selected? (How was this calculated?)
          </h3>
          {showWhy ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
        </button>
        {showWhy && (
          <div className="mt-4 text-sm text-gray-700 leading-relaxed whitespace-pre-line border-t border-gray-100 pt-4">
            {result.why_selected}
            <p className="mt-3 text-[11px] text-gray-500 italic">
              Note: This explanation was generated from verified computed data. All numbers were calculated deterministically from IFCT 2017 database values and linear programming results — no values were invented by the AI.
            </p>
          </div>
        )}
      </Card>

      {/* Ingredient Composition Table */}
      <Card className="p-5 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
          <Layers className="w-4 h-4 text-primary-600" />
          Ingredient Composition
        </h3>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ingredient</TableHead>
              <TableHead className="text-right">Quantity (g)</TableHead>
              <TableHead className="text-right">Iron Contribution (mg)</TableHead>
              <TableHead className="text-right">Vit C (mg)</TableHead>
              <TableHead className="text-right">Cost (₹)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {result.ingredients.map((ing, i) => (
              <TableRow key={i}>
                <TableCell className="font-medium text-gray-900">{ing.name}</TableCell>
                <TableCell className="text-right font-mono">{ing.quantity_g.toFixed(1)}</TableCell>
                <TableCell className="text-right font-mono text-primary-700">{ing.iron_contribution_mg.toFixed(2)}</TableCell>
                <TableCell className="text-right font-mono text-teal-700">{ing.vitc_contribution_mg.toFixed(1)}</TableCell>
                <TableCell className="text-right font-mono">₹{ing.cost_inr.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Nutrition Table */}
      <Card className="p-5 space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
          <FlaskConical className="w-4 h-4 text-teal-600" />
          Nutrition Information (Computed from IFCT 2017)
        </h3>
        <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-[11px] text-amber-800 flex gap-2">
          <Info className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
          <span>All values are calculated deterministically from verified IFCT 2017 database entries. Values shown as "—" indicate the nutrient is not in the IFCT dataset for the ingredient combination used.</span>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Nutrient</TableHead>
              <TableHead className="text-right">Per Serving ({result.serving_size_g}g)</TableHead>
              <TableHead className="text-right">Per 100g</TableHead>
              <TableHead className="text-right">% RDA</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {result.nutrients.map((n, i) => (
              <TableRow key={i}>
                <TableCell className="font-medium text-gray-900">{n.nutrient}</TableCell>
                <TableCell className="text-right font-mono">
                  {n.per_serving !== null ? `${n.per_serving} ${n.unit}` : <span className="text-gray-400 italic text-xs">not in database</span>}
                </TableCell>
                <TableCell className="text-right font-mono">
                  {n.per_100g !== null ? `${n.per_100g} ${n.unit}` : '—'}
                </TableCell>
                <TableCell className="text-right">
                  {n.rda_pct !== null ? (
                    <span className={`text-xs font-bold ${parseFloat(n.rda_pct) >= 100 ? 'text-emerald-700' : parseFloat(n.rda_pct) >= 50 ? 'text-amber-700' : 'text-red-600'}`}>
                      {n.rda_pct}%
                    </span>
                  ) : '—'}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Preparation & Storage */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <Card className="p-5 space-y-3">
          <h3 className="text-sm font-semibold text-gray-900">Preparation Instructions</h3>
          <p className="text-xs text-gray-700 leading-relaxed whitespace-pre-line">{result.preparation_instructions}</p>
        </Card>
        <Card className="p-5 space-y-3">
          <h3 className="text-sm font-semibold text-gray-900">Storage Guidelines</h3>
          <p className="text-xs text-gray-700 leading-relaxed whitespace-pre-line">{result.storage_instructions}</p>
        </Card>
      </div>

      {/* Action Bar */}
      <div className="flex flex-wrap gap-3 pb-6">
        <Button variant="primary" onClick={handleAddToCart} disabled={addingToCart || cartSuccess}>
          <ShoppingCart className="w-4 h-4 mr-2" />
          {cartSuccess ? 'Added to Cart!' : 'Add to Cart (Demo Order)'}
        </Button>
        <Link to="/app/compare">
          <Button variant="outline">
            Compare Formulations
          </Button>
        </Link>
        <Link to="/app/progress">
          <Button variant="outline">
            Start Tracking Progress
            <ArrowRight className="w-4 h-4 ml-1.5" />
          </Button>
        </Link>
        <Button variant="ghost" onClick={handleDownloadPDF} disabled={downloading}>
          <Download className="w-4 h-4 mr-1.5" />
          Download PDF Report
        </Button>
      </div>

      <MedicalDisclaimer />
    </div>
  );
};

