# NutriAI 🥗
**AI-Optimized, Aspirational Nutrient-Dense Food Products for Anaemia Prevention among Adolescent Girls and Women of Reproductive Age**

> **Reference**: ICMR–Gates Foundation Grand Challenge RFP on aspirational nutrient-dense food products for adolescent girls (10–19 yrs), young women of reproductive age (20–35 yrs), and older women of reproductive age (35–49 yrs).

---

## 📌 The One Architectural Rule
> **Deterministic code computes all numbers. The LLM only explains.**

- **Deterministic Pipeline**: All laboratory OCR parsing, unit conversions, reference range validation, clinical safety scoring, ICMR nutrient targets, linear programming formulation (SciPy HiGHS), bioavailable iron calculation, and nutrition tables are computed purely in Python/PostgreSQL.
- **Constrained LLM**: The LLM receives pre-computed JSON and generates plain-language explanations and cultural educational tips. It never invents numbers, diagnoses, or dosages.
- **The Number Guard**: An automated auditor inspects every LLM response. If any number appears that was not in the deterministic JSON input, the response is rejected and replaced with verified clinical templates.

---

## 📱 Simplified Application Structure (6 Core Sections)

The platform has been streamlined into **6 focused, easy-to-understand sections**:

| # | Section | Route | Description |
|---|---|---|---|
| **1** | **Generate Product** | `/app/generate` | Upload a blood test report (CBC, Ferritin, Iron profile) or review extracted values to generate an ICMR-aligned, bioavailable prototype food formulation. |
| **2** | **Track Progress** | `/app/progress` | Daily 1-click serving tracker, visual adherence calendar, and long-term adherence monitoring. |
| **3** | **History** | `/app/history` | View all past generated formulations, uploaded lab reports, and demo orders in unified tabs. |
| **4** | **Order / Cart** | `/app/cart` | Browse prototype food products, manage your cart, and test the sandbox demo checkout flow. |
| **5** | **Details (About Anaemia)** | `/app/details` | Clear, accessible education: signs & symptoms, Indian food sources (moringa, halim/garden cress, sesame), absorption boosters (Vitamin C), inhibitors (tea/coffee), and official ICMR RDA targets. |
| **6** | **User Info** | `/app/profile` | View and edit your personal profile, age group, dietary preferences (vegetarian, vegan, allergies), and consents. |

---

## 🛡️ Medical Safety & Clinical Guardrails
1. **Supportive, Not Curative**: NutriAI is a nutritional research and food product formulation prototype. It does not diagnose, treat, or replace medical therapies.
2. **Etiological Differentiation**: Anaemia is not blindly treated as iron deficiency. Low MCV (< 80 fL) with normal or elevated ferritin (> 150 ng/mL) triggers safety alerts for thalassaemia trait or inflammatory anaemia.
3. **Clinical Safety Gate**: Evaluates lab values before formulation. Severe anaemia (Hb < 8.0 g/dL) triggers an immediate medical referral banner and halts unguided supplementation.
4. **Hard Allergen Constraints**: Strict exclusion of user-specified allergens (e.g., nuts, gluten, dairy) at the database query, linear programming, and post-solve validation layers.
5. **Prototype Badges**: Every formulation, product, and checkout screen is marked with `Prototype product – demo checkout`.
6. **No Efficacy Claims**: Clear disclaimers that lab changes must not be attributed solely to NutriAI products and must be evaluated by a healthcare professional.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, TanStack Query, React Hook Form + Zod, Recharts, Lucide Icons, react-i18next (English, Tamil, Hindi, Telugu, Malayalam).
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (asyncpg + psycopg2), Alembic, SciPy HiGHS Linear Programming, Uvicorn.
- **Database**: PostgreSQL 15+ (hosted on **Supabase** Cloud PostgreSQL) with `pg_trgm`, `pgcrypto`, `citext`, and Row-Level Security (RLS) across 24 relational tables.
- **Storage**: S3-compatible (Supabase Storage / Cloudflare R2 / MinIO).
- **AI & NLP**: Google Gemini API / Anthropic Claude API (with deterministic fallback mode).

---

## 🗄️ Database & Supabase Integration

NutriAI manages all user accounts, lab data, clinical assessments, food formulations, and demo orders directly in **Supabase PostgreSQL**.

### 24 Relational Tables
- **Users & Auth**: `users`, `user_profiles`, `user_consents`, `audit_logs`
- **Clinical Data**: `uploaded_reports`, `extracted_lab_results`, `nutritional_assessments`, `clinical_reference_ranges`
- **Formulations**: `product_formulations`, `formulation_ingredients`, `ifct_ingredients`, `product_categories`
- **E-Commerce & Orders**: `prototype_products`, `carts`, `cart_items`, `orders`, `order_items`
- **Adherence Tracking**: `adherence_logs`, `hemoglobin_trackers`

### Supabase Connection Strings
In `.env` and `backend/.env`:
```env
# Async engine used by FastAPI application runtime
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR_PASSWORD]@[YOUR_HOST]:5432/postgres

# Direct sync engine used by Alembic migrations
DATABASE_DIRECT_URL=postgresql+psycopg2://postgres:[YOUR_PASSWORD]@[YOUR_HOST]:5432/postgres?sslmode=require
```

> [!IMPORTANT]
> **Special Characters in Passwords**: If your database password contains characters like `@`, `#`, or `$`, URL-encode them in the connection strings (e.g., replace `@` with `%40`).

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Node.js**: v18+ and `npm`
- **Python**: v3.11+ (tested on Python 3.11 – 3.13)
- **Supabase Account** (or local PostgreSQL 15+)

### 2. Configure Environment Variables
Copy `.env.example` to `.env` in the root and in `backend/`:
```bash
cp .env.example .env
cp .env.example backend/.env
```
Fill in your Supabase connection strings, secret keys, and API credentials.

### 3. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (creates all 24 tables + RLS)
alembic upgrade head

# Seed 40 IFCT raw ingredients, ICMR rules, and demo data
python -m app.seed.load

# Start backend API server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```
The backend API is now running at `http://127.0.0.1:8001` (Interactive Swagger docs: `http://127.0.0.1:8001/docs`).

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Testing & Verification

### Run Full Test Suite
```bash
# Backend unit and API tests
cd backend
pytest

# Frontend unit tests
cd frontend
npm test

# Production build check (TypeScript + Vite bundling)
npm run build
```

---

## 🧭 End-to-End Demo Walkthrough

1. **Sign In**: Navigate to `http://localhost:5173/login`. You can sign in using your credentials or use the 1-click **Demo Accounts** (e.g., Adolescent Girl 14 yrs, Pregnant Woman 28 yrs, Adult Woman 42 yrs).
2. **Generate Product (`/app/generate`)**:
   - Upload a sample blood test report (PDF, PNG, JPG) or proceed with simulated values.
   - Review extracted lab parameters (Hb, Ferritin, MCV, TIBC) and canonical units.
   - Choose food format preferences (Crunchy Bar, Drink Mix, Savory Crisp, Spoonable Paste).
   - Review the clinical safety assessment and click **Generate**.
3. **View Formulation**: Examine the ingredient breakdown (Moringa, Halim/Garden Cress, Black Sesame, Sprouted Ragi), bioavailable iron delivery, and macro/micronutrient compliance with ICMR targets.
4. **Order / Cart (`/app/cart`)**: Add prototype items to your demo cart, proceed to checkout, and complete a sandbox order.
5. **Track Progress (`/app/progress`)**: Log daily product servings to update your adherence calendar.
6. **Learn Details (`/app/details`)**: Explore the interactive guide on anaemia symptoms, absorption science, and ICMR RDA standards.

---

## 📚 Documentation Index
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): System architecture, linear programming engine, and data flow.
- [`docs/SAFETY.md`](docs/SAFETY.md): Medical safety framework, referral criteria, and clinical rules.
- [`docs/DATABASE.md`](docs/DATABASE.md): Entity-relationship diagrams, schema definitions, and RLS policies.
- [`docs/API.md`](docs/API.md): Complete OpenAPI contract and endpoint specifications.
- [`docs/SETUP_SUPABASE.md`](docs/SETUP_SUPABASE.md): Supabase PostgreSQL and Storage configuration guide.
- [`docs/EXPERT_REVIEW_CHECKLIST.md`](docs/EXPERT_REVIEW_CHECKLIST.md): Clinical, nutritional, and food technology sign-off checklist.

---

## ⚖️ License & Research Disclaimer
This software is developed for research and prototyping under the ICMR–Gates Foundation Grand Challenge framework. All product formulations and nutritional calculations represent experimental prototypes for research validation and demo purposes.
