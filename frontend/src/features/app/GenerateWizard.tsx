import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { api } from '../../lib/api';
import { Stepper } from '../../components/ui/Stepper';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import {
  Upload,
  FileText,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Info,
  Eye,
  RefreshCw,
  ArrowRight,
  XCircle,
  Edit3,
  ShieldAlert,
} from 'lucide-react';

const STEPS = [
  { label: 'Upload Report', description: 'PDF or image of blood test' },
  { label: 'Review Results', description: 'Verify extracted values' },
  { label: 'Confirm Context', description: 'Dietary and health info' },
  { label: 'Safety Check', description: 'Assessment & clinical gate' },
  { label: 'Generate', description: 'Formulation in progress' },
];

interface ExtractedResult {
  id: string;
  parameter_code: string;
  display_name: string;
  raw_value: string;
  value_numeric: number | null;
  unit: string;
  canonical_value: number | null;
  canonical_unit: string;
  status: 'low' | 'normal' | 'high' | 'critical' | 'unknown';
  plausible_min: number;
  plausible_max: number;
  out_of_range: boolean;
  user_edited?: boolean;
}

interface AssessmentResult {
  safe_to_formulate: boolean;
  red_flags: string[];
  warnings: string[];
  life_stage: string;
  rda_targets: Record<string, number>;
  anaemia_risk: string;
}

export const GenerateWizard: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [step, setStep] = useState(0);
  const [reportId, setReportId] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'processing' | 'done' | 'error'>('idle');
  const [extractedResults, setExtractedResults] = useState<ExtractedResult[]>([]);
  const [assessment, setAssessment] = useState<AssessmentResult | null>(null);
  const [editingRow, setEditingRow] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (file: File) => {
    if (!['application/pdf', 'image/jpeg', 'image/png', 'image/tiff'].includes(file.type)) {
      setError('Unsupported file type. Please upload a PDF or image (JPEG, PNG, TIFF).');
      return;
    }
    if (file.size > 20 * 1024 * 1024) {
      setError('File size must be under 20 MB.');
      return;
    }
    setUploadedFile(file);
    setError('');
  };

  const handleUploadAndParse = async () => {
    if (!uploadedFile) return;
    setUploadStatus('uploading');
    setError('');
    try {
      const form = new FormData();
      form.append('file', uploadedFile);
      const uploadRes = await api.post('/reports/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const activeReportId = uploadRes.data.report_id || uploadRes.data.id;
      setReportId(activeReportId);
      setUploadStatus('processing');

      // Poll for OCR completion
      let attempts = 0;
      const poll = setInterval(async () => {
        try {
          const statusRes = await api.get(`/reports/${activeReportId}/status`);
          if (statusRes.data.ocr_status === 'confirmed' || statusRes.data.ocr_status === 'needs_review') {
            clearInterval(poll);
            const results = statusRes.data.extracted_results || statusRes.data.results || [];
            setExtractedResults(results);
            setUploadStatus('done');
            setStep(1);
          } else if (statusRes.data.ocr_status === 'failed') {
            clearInterval(poll);
            setError('OCR failed. Please try a clearer image or different file.');
            setUploadStatus('error');
          }
          if (++attempts > 30) {
            clearInterval(poll);
            setError('Processing timed out. Please refresh and try again.');
            setUploadStatus('error');
          }
        } catch {
          clearInterval(poll);
          setUploadStatus('error');
        }
      }, 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setUploadStatus('error');
    }
  };

  const handleEditSave = async (rowId: string) => {
    const numeric = parseFloat(editValue);
    if (isNaN(numeric)) {
      setError('Please enter a valid numeric value.');
      return;
    }
    try {
      await api.patch(`/reports/${reportId}/results/${rowId}`, { value_numeric: numeric, user_edited: true });
      setExtractedResults((prev) =>
        prev.map((r) => r.id === rowId ? { ...r, value_numeric: numeric, canonical_value: numeric, user_edited: true } : r)
      );
      setEditingRow(null);
    } catch {
      setError('Could not save edit. Please try again.');
    }
  };

  const handleConfirmResults = async () => {
    if (!reportId) return;
    setError('');
    try {
      await api.post(`/reports/${reportId}/confirm`);
      const assessRes = await api.post('/assessments', { report_id: reportId });
      setAssessment(assessRes.data);
      setStep(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Assessment failed. Please try again.');
    }
  };

  const handleGenerate = async () => {
    if (!reportId || !assessment?.safe_to_formulate) return;
    setGenerating(true);
    setStep(4);
    try {
      const res = await api.post('/formulations', { report_id: reportId });
      navigate(`/app/results?formulation_id=${res.data.formulation_id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Formulation generation failed. Please try again.');
      setGenerating(false);
      setStep(3);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'low': return 'text-red-600 bg-red-50';
      case 'critical': return 'text-red-800 bg-red-100 font-bold';
      case 'high': return 'text-amber-700 bg-amber-50';
      case 'normal': return 'text-emerald-700 bg-emerald-50';
      default: return 'text-gray-500 bg-gray-50';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <MedicalDisclaimer />

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2.5">
            <Sparkles className="w-6 h-6 text-primary-600" />
            Generate Product
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Upload your blood test report or review lab values to generate a personalized nutrient-dense food formulation.
          </p>
        </div>
        <PrototypeBadge />
      </div>

      <Stepper steps={STEPS} currentStep={step} />

      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2 text-xs text-red-700">
          <XCircle className="w-4 h-4 text-red-500 shrink-0" />
          {error}
        </div>
      )}

      {/* Step 0: File Upload */}
      {step === 0 && (
        <Card className="p-6 space-y-5">
          <div className="space-y-2">
            <h2 className="text-base font-semibold text-gray-900">Step 1: Upload Laboratory Report</h2>
            <p className="text-xs text-gray-600">Supported: Haemogram / CBC panel, Iron Studies (ferritin, TIBC, serum iron), Vitamins B12, D, Folate. Accepts PDF, JPEG, PNG, TIFF up to 20 MB.</p>
          </div>

          {/* Drop Zone */}
          <div
            className={`border-2 border-dashed rounded-2xl p-8 text-center transition ${
              dragOver ? 'border-primary-500 bg-primary-50' : 'border-gray-300 bg-gray-50 hover:border-primary-400'
            }`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              const file = e.dataTransfer.files[0];
              if (file) handleFileSelect(file);
            }}
            onClick={() => fileInputRef.current?.click()}
          >
            {uploadedFile ? (
              <div className="flex flex-col items-center gap-3">
                <FileText className="w-10 h-10 text-primary-500" />
                <div>
                  <p className="text-sm font-semibold text-gray-900">{uploadedFile.name}</p>
                  <p className="text-xs text-gray-500">{(uploadedFile.size / 1024).toFixed(1)} KB</p>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); setUploadedFile(null); }}
                  className="text-xs text-red-500 hover:underline"
                >
                  Remove file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <Upload className="w-10 h-10 text-gray-300" />
                <div>
                  <p className="text-sm font-medium text-gray-700">Drag & drop or <span className="text-primary-600 cursor-pointer">browse file</span></p>
                  <p className="text-xs text-gray-500 mt-1">PDF, JPEG, PNG, TIFF — Max 20 MB</p>
                </div>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.jpg,.jpeg,.png,.tiff,.tif"
              className="hidden"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFileSelect(f); }}
            />
          </div>

          <div className="flex items-start gap-2 text-xs text-amber-800 bg-amber-50 p-3 rounded-xl border border-amber-200">
            <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <span>Your report is processed on-server using PyMuPDF / PaddleOCR. No data is sent to external AI services unless you explicitly enable LLM-vision fallback. The file is stored encrypted with a short-lived signed URL.</span>
          </div>

          <Button
            variant="primary"
            className="w-full"
            disabled={!uploadedFile || uploadStatus === 'uploading' || uploadStatus === 'processing'}
            onClick={handleUploadAndParse}
          >
            {uploadStatus === 'uploading' && <RefreshCw className="w-4 h-4 mr-2 animate-spin" />}
            {uploadStatus === 'processing' && <RefreshCw className="w-4 h-4 mr-2 animate-spin" />}
            {uploadStatus === 'idle' && <Upload className="w-4 h-4 mr-2" />}
            {uploadStatus === 'uploading' ? 'Uploading…' : uploadStatus === 'processing' ? 'Extracting values (OCR)…' : 'Upload & Extract Values'}
          </Button>
        </Card>
      )}

      {/* Step 1: Review Extracted Results */}
      {step === 1 && (
        <Card className="p-6 space-y-5">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold text-gray-900">Step 2: Review Extracted Lab Values</h2>
            <span className="text-xs text-primary-700 font-medium flex items-center gap-1">
              <Eye className="w-3.5 h-3.5" />
              {extractedResults.length} parameters found
            </span>
          </div>

          <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <span>
              <strong>Verification required:</strong> Please review each extracted value. Click the edit icon to correct any value. All numbers are verified against plausibility ranges from ICMR clinical references. Edited values are flagged for audit.
            </span>
          </div>

          <div className="overflow-x-auto rounded-xl border border-gray-200">
            <table className="w-full text-xs">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Parameter</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Raw OCR Text</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Extracted Value</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Unit</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Status</th>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Edit</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {extractedResults.map((row) => (
                  <tr key={row.id} className={`hover:bg-gray-50 ${row.out_of_range ? 'bg-red-50/40' : ''}`}>
                    <td className="px-4 py-3 font-medium text-gray-900">
                      {row.display_name}
                      {row.user_edited && (
                        <span className="ml-1.5 text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded">Edited</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-500 font-mono">{row.raw_value}</td>
                    <td className="px-4 py-3">
                      {editingRow === row.id ? (
                        <div className="flex items-center gap-2">
                          <input
                            type="number"
                            step="0.01"
                            value={editValue}
                            onChange={(e) => setEditValue(e.target.value)}
                            className="w-20 px-2 py-1 border border-primary-500 rounded focus:outline-none text-xs"
                            autoFocus
                          />
                          <button onClick={() => handleEditSave(row.id)} className="text-primary-600 hover:text-primary-800">
                            <CheckCircle2 className="w-4 h-4" />
                          </button>
                          <button onClick={() => setEditingRow(null)} className="text-gray-400 hover:text-gray-600">
                            <XCircle className="w-4 h-4" />
                          </button>
                        </div>
                      ) : (
                        <span className="font-semibold text-gray-900">
                          {row.canonical_value !== null ? row.canonical_value.toFixed(2) : '—'}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-500">{row.canonical_unit}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${getStatusColor(row.status)}`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => { setEditingRow(row.id); setEditValue(String(row.canonical_value ?? '')); }}
                        className="text-gray-400 hover:text-primary-600"
                        title="Edit this value"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {extractedResults.some((r) => r.status === 'critical') && (
            <div className="p-4 rounded-xl bg-red-50 border border-red-300 flex gap-2 text-xs text-red-800">
              <AlertTriangle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
              <span><strong>Critical values detected.</strong> The safety gate will be evaluated in the next step. If Hb is below 7.0 g/dL or other critical thresholds are reached, formulation will be blocked and medical guidance will be shown.</span>
            </div>
          )}

          <div className="flex gap-3">
            <Button variant="outline" className="flex-1" onClick={() => setStep(0)}>Back</Button>
            <Button variant="primary" className="flex-1" onClick={handleConfirmResults}>
              Confirm Values & Run Safety Assessment
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </Button>
          </div>
        </Card>
      )}

      {/* Step 3: Safety Assessment Results */}
      {step === 3 && assessment && (
        <Card className="p-6 space-y-5">
          <h2 className="text-base font-semibold text-gray-900">Step 4: Safety Gate & Assessment Findings</h2>

          {assessment.safe_to_formulate ? (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-300 flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-emerald-900 text-sm">Safety gate passed</h4>
                <p className="text-xs text-emerald-800 mt-0.5">No critical contraindications detected. Formulation can proceed.</p>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-red-50 border border-red-300 space-y-2">
              <div className="flex items-start gap-3">
                <ShieldAlert className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-red-900 text-sm">Formulation blocked by safety gate</h4>
                  <p className="text-xs text-red-800 mt-0.5">Critical findings require clinical evaluation before a food product can be recommended.</p>
                </div>
              </div>
              <ul className="ml-8 space-y-1">
                {assessment.red_flags.map((flag, i) => (
                  <li key={i} className="text-xs text-red-800 flex items-start gap-1.5">
                    <XCircle className="w-3.5 h-3.5 text-red-500 shrink-0 mt-0.5" />
                    {flag}
                  </li>
                ))}
              </ul>
              <p className="ml-8 text-xs text-red-700 font-medium">
                Please consult a qualified healthcare provider. NutriAI supports, not replaces, medical care.
              </p>
            </div>
          )}

          {assessment.warnings.length > 0 && (
            <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 space-y-2">
              <h4 className="text-xs font-semibold text-amber-900 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-700" /> Nutritional Warnings
              </h4>
              <ul className="space-y-1">
                {assessment.warnings.map((w, i) => (
                  <li key={i} className="text-xs text-amber-800">• {w}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="p-4 rounded-xl bg-primary-50 border border-primary-200 space-y-2">
            <h4 className="text-xs font-semibold text-primary-900">Life Stage: {assessment.life_stage}</h4>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2">
              {Object.entries(assessment.rda_targets).map(([nutrient, target]) => (
                <div key={nutrient} className="p-2.5 rounded-lg bg-white border border-primary-100 text-xs">
                  <div className="font-bold text-primary-900">{(target as number).toFixed(1)} {nutrient.includes('iron') ? 'mg' : nutrient.includes('cal') ? 'kcal' : 'µg'}</div>
                  <div className="text-primary-700 capitalize">{nutrient.replace(/_/g, ' ')}</div>
                </div>
              ))}
            </div>
          </div>

          <MedicalDisclaimer />

          <div className="flex gap-3">
            <Button variant="outline" className="flex-1" onClick={() => setStep(1)}>Back to Results</Button>
            <Button
              variant="primary"
              className="flex-1"
              disabled={!assessment.safe_to_formulate || generating}
              onClick={handleGenerate}
            >
              {assessment.safe_to_formulate ? (
                <>
                  <Sparkles className="w-4 h-4 mr-1.5" />
                  Generate Food Formulation
                </>
              ) : (
                'Formulation Blocked by Safety Gate'
              )}
            </Button>
          </div>
        </Card>
      )}

      {/* Step 4: Generating Progress */}
      {step === 4 && (
        <Card className="p-10 text-center space-y-6">
          <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center mx-auto">
            <Sparkles className="w-8 h-8 text-primary-600 animate-pulse" />
          </div>
          <div className="space-y-2">
            <h2 className="text-lg font-bold text-gray-900">Generating Your Formulation</h2>
            <p className="text-sm text-gray-600">
              Running SciPy HiGHS linear optimizer across {'>'}40 Indian ingredients from IFCT 2017 database, applying allergen filters, HFSS constraints, and bioavailability equations…
            </p>
          </div>
          <div className="max-w-xs mx-auto space-y-1.5 text-left text-xs text-gray-500">
            {['Filtering allergen-safe ingredients…', 'Running linear optimizer (HiGHS)…', 'Applying Hallberg bioavailability equations…', 'Validating nutrients and costs…', 'Ranking formulations…'].map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-primary-500" />
                <span>{step}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};

