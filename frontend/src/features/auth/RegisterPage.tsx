import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuth } from '../../lib/auth';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Checkbox } from '../../components/ui/Checkbox';
import { Stepper } from '../../components/ui/Stepper';
import { HeartPulse, UserPlus, AlertTriangle, Eye, EyeOff, ShieldCheck, RefreshCw } from 'lucide-react';

// --- Schemas ---
const accountSchema = z.object({
  full_name: z.string().min(2, 'Full name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirm_password: z.string(),
  date_of_birth: z.string().min(1, 'Date of birth is required'),
  preferred_language: z.enum(['en', 'ta', 'hi', 'te', 'ml']),
  consent_data: z.boolean().default(true),
  consent_health: z.boolean().default(true),
}).refine((d) => d.password === d.confirm_password, {
  message: 'Passwords do not match',
  path: ['confirm_password'],
});

const guardianSchema = z.object({
  guardian_name: z.string().min(2, 'Guardian name required'),
  guardian_relation: z.string().min(1, 'Relation required'),
  guardian_contact: z.string().min(10, 'Valid contact number required'),
  guardian_consent: z.boolean().default(true),
});

type AccountForm = z.infer<typeof accountSchema>;
type GuardianForm = z.infer<typeof guardianSchema>;

function getAge(dob: string): number {
  if (!dob) return 0;
  const today = new Date();
  const birth = new Date(dob);
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return isNaN(age) ? 0 : age;
}

const STEPS = [
  { label: 'Account', description: 'Personal details' },
  { label: 'Consent', description: 'Guardian (for minors)' },
  { label: 'Ready', description: 'Access dashboard' },
];

export const RegisterPage: React.FC = () => {
  const { t } = useTranslation();
  const { register: registerUser, loginWithToken } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState(0);
  const [accountData, setAccountData] = useState<AccountForm | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<AccountForm>({
    resolver: zodResolver(accountSchema),
    defaultValues: {
      preferred_language: 'en',
      consent_data: true,
      consent_health: true,
    },
  });

  const {
    register: gRegister,
    handleSubmit: gHandleSubmit,
    formState: { errors: gErrors },
  } = useForm<GuardianForm>({
    resolver: zodResolver(guardianSchema),
    defaultValues: {
      guardian_consent: true,
    },
  });

  const dobValue = watch('date_of_birth');
  const isMinor = dobValue ? getAge(dobValue) < 18 : false;

  const onAccountSubmit = async (data: AccountForm) => {
    setAccountData(data);
    setError('');

    if (isMinor) {
      setStep(1); // Advance to guardian consent step for minors (< 18)
      return;
    }

    // Adult user (>= 18) -> Register and log in directly to dashboard
    setLoading(true);
    try {
      const res = await registerUser(data);
      if (res?.token) {
        await loginWithToken(res.token);
        navigate('/app/generate', { replace: true });
      } else {
        setStep(2);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const onGuardianSubmit = async (guardianData: GuardianForm) => {
    if (!accountData) return;
    setLoading(true);
    setError('');
    try {
      const res = await registerUser({ ...accountData, guardian: guardianData });
      if (res?.token) {
        await loginWithToken(res.token);
        navigate('/app/generate', { replace: true });
      } else {
        setStep(2);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-1">
        <div className="flex justify-center">
          <div className="w-12 h-12 rounded-2xl bg-primary-600 flex items-center justify-center text-white shadow-sm mb-2">
            <HeartPulse className="w-6 h-6" />
          </div>
        </div>
        <h2 className="text-xl font-bold text-gray-900">Create Your Account</h2>
        <p className="text-xs text-gray-500">NutriAI Personalized Nutrition Research Platform</p>
      </div>

      {/* Stepper */}
      <Stepper steps={STEPS} currentStep={step} />

      {/* Step 0: Account Details */}
      {step === 0 && (
        <form onSubmit={handleSubmit(onAccountSubmit)} className="space-y-4">
          {error && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Full Name *</label>
            <Input {...register('full_name')} placeholder="e.g. Priya Sharma" error={errors.full_name?.message} />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Email Address *</label>
            <Input type="email" {...register('email')} placeholder="you@example.com" error={errors.email?.message} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Password *</label>
              <div className="relative">
                <Input
                  type={showPassword ? 'text' : 'password'}
                  {...register('password')}
                  placeholder="Min. 8 characters"
                  error={errors.password?.message}
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Confirm Password *</label>
              <Input
                type="password"
                {...register('confirm_password')}
                placeholder="Repeat password"
                error={errors.confirm_password?.message}
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Date of Birth *</label>
            <Input
              type="date"
              {...register('date_of_birth')}
              error={errors.date_of_birth?.message}
              max={new Date().toISOString().split('T')[0]}
            />
            {isMinor && dobValue && (
              <div className="mt-2 p-2.5 rounded-lg bg-amber-50 border border-amber-200 flex items-start gap-2 text-xs text-amber-800">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <span>Since you are under 18, guardian consent will be requested next.</span>
              </div>
            )}
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Preferred Language</label>
            <Select {...register('preferred_language')}>
              <option value="en">English</option>
              <option value="ta">தமிழ் (Tamil)</option>
              <option value="hi">हिन्दी (Hindi)</option>
              <option value="te">తెలుగు (Telugu)</option>
              <option value="ml">മലയാളம் (Malayalam)</option>
            </Select>
          </div>

          <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-3">
            <h4 className="text-xs font-semibold text-gray-900">Required Consents (DPDPA 2023)</h4>
            <Checkbox
              {...register('consent_data')}
              label="I consent to the processing of my personal data for nutritional research"
              error={errors.consent_data?.message}
            />
            <Checkbox
              {...register('consent_health')}
              label="I consent to the processing of my health and laboratory data to generate food formulations"
              error={errors.consent_health?.message}
            />
          </div>

          <Button type="submit" variant="primary" className="w-full" disabled={loading}>
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <RefreshCw className="w-4 h-4 animate-spin" />
                Creating your account...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <UserPlus className="w-4 h-4" />
                Continue{isMinor ? ' (Guardian Consent Next)' : ''}
              </span>
            )}
          </Button>
        </form>
      )}

      {/* Step 1: Guardian Consent for Minors */}
      {step === 1 && (
        <form onSubmit={gHandleSubmit(onGuardianSubmit)} className="space-y-4">
          <div className="p-4 rounded-xl bg-primary-50 border border-primary-200 text-xs text-primary-800 flex gap-2">
            <ShieldCheck className="w-4 h-4 text-primary-600 shrink-0 mt-0.5" />
            <span>Since this user is under 18, a parent or legal guardian must provide consent before health data can be processed.</span>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Guardian Full Name *</label>
            <Input {...gRegister('guardian_name')} placeholder="Parent / Guardian name" error={gErrors.guardian_name?.message} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Relation to User *</label>
              <Select {...gRegister('guardian_relation')}>
                <option value="">Select...</option>
                <option value="mother">Mother</option>
                <option value="father">Father</option>
                <option value="grandparent">Grandparent</option>
                <option value="sibling">Elder Sibling</option>
                <option value="legal_guardian">Legal Guardian</option>
              </Select>
              {gErrors.guardian_relation && (
                <p className="text-xs text-red-600 mt-1">{gErrors.guardian_relation.message}</p>
              )}
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Guardian Contact *</label>
              <Input {...gRegister('guardian_contact')} placeholder="+91 98765 43210" error={gErrors.guardian_contact?.message} />
            </div>
          </div>

          <Checkbox
            {...gRegister('guardian_consent')}
            label="I, as parent/guardian, consent to the collection and processing of this minor's health data for nutritional research and food formulation purposes."
            error={gErrors.guardian_consent?.message}
          />

          <div className="flex gap-3">
            <Button type="button" variant="outline" className="flex-1" onClick={() => setStep(0)}>
              Back
            </Button>
            <Button type="submit" variant="primary" className="flex-1" disabled={loading}>
              {loading ? 'Creating account...' : 'Create Account'}
            </Button>
          </div>
        </form>
      )}

      {/* Step 2: Email Verification */}
      {step === 2 && (
        <div className="text-center space-y-5 py-4">
          <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto">
            <ShieldCheck className="w-8 h-8 text-emerald-600" />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-gray-900">Account Created!</h3>
            <p className="text-sm text-gray-600">
              Welcome to NutriAI, <strong>{accountData?.full_name}</strong>! You can now sign in to your dashboard.
            </p>
          </div>
          <Button variant="primary" className="w-full" onClick={() => navigate('/login')}>
            Go to Sign In
          </Button>
        </div>
      )}

      {step < 2 && (
        <p className="text-center text-xs text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-primary-600 font-semibold hover:underline">
            Sign In
          </Link>
        </p>
      )}
    </div>
  );
};
