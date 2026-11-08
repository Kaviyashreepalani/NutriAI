# NutriAI – Mock Policy & Inventory

## 1. Mock Policy
To ensure total transparency, scientific integrity, and compliance with the ICMR–Gates Foundation RFP:
1. **Isolation**: Every mock, placeholder, or simulation must be isolated behind an explicit adapter interface or feature flag.
2. **Visible UI Badging**: Every interface displaying simulated or prototype data must present an unambiguous badge (e.g., *"Prototype product – demo checkout"*, *"Demo nutrient data – not validated"*, *"Mock Voice Service"*).
3. **No Fake Compute**: Calculations (nutrients, costs, safety thresholds, solver equations) are **never faked or hard-coded**. If data is incomplete or infeasible, the engine explicitly reports `"not in database"` or `"infeasible"`.

---

## 2. Inventory of Mocks & Real Implementations

| Mock Component | Location in Codebase | UI Indicator | Real Implementation Replacement |
| :--- | :--- | :--- | :--- |
| **Dev Authentication** | `app.services.auth.dev_provider` | Banner in Dev: *"Dev Auth Active"* | Supabase Auth JWT / Firebase Auth Admin SDK |
| **Demo Payment Sandbox** | `app.api.v1.shop` | *"Prototype product – demo checkout"* | Razorpay / Stripe Indian Payments Gateway |
| **LLM Mock Adapter** | `app.services.llm.providers.mock` | *"Generated via deterministic template"* | Gemini 1.5 Pro / Anthropic Claude 3.5 Sonnet |
| **Speech Mock Adapter** | `app.services.speech.providers.mock` | *"Mock audio stream"* | Browser Web Speech API / Google Cloud STT/TTS / Bhashini |
| **Draft Nutrient Database** | `app.seed.data.ingredients` | *"Demo nutrient data – not validated"* | Indian Food Composition Tables (IFCT 2017 / ICMR-NIN) |
| **Illustrative SVG Images** | `app.services.formulation.assets` | *"Illustrative prototype image"* | High-res studio photography of pilot pilot products |
| **Email Dispatch Stub** | `app.services.notifications.email` | Logged to console / Dev inbox | SendGrid / AWS SES / Postmark |

---

## 3. How to Replace Mocks for Production
1. **Database Nutrients**: Run `python -m app.seed.import_ifct data/ifct_2017_verified.csv` to replace draft values with verified laboratory assays.
2. **Authentication**: Set `AUTH_PROVIDER=supabase` or `AUTH_PROVIDER=firebase` in `.env`.
3. **LLM**: Set `LLM_PROVIDER=gemini` and provide `GEMINI_API_KEY`.
4. **Speech**: Set `SPEECH_PROVIDER=google` or rely on client-side Web Speech API in modern browsers.

