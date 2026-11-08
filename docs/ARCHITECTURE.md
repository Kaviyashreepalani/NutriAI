# NutriAI – Architecture & System Design

## 1. System Overview
**NutriAI** is an AI-assisted, clinical-safety gated nutrition support and prototype food-formulation platform designed specifically for adolescent girls (10–19 years) and women of reproductive age (20–49 years) in India. Its goal is anaemia prevention through aspirational, nutrient-dense food formulations (such as roasted millet bars, multigrain laddoos, fortified breakfast mixes, and cold beverage mixes).

### The One Architectural Rule
> **Deterministic code computes all numbers. The LLM only explains.**

- **Calculations**: OCR extraction, laboratory unit conversions, range validation, clinical safety checks, nutrient RDA targets, linear programming formulation optimization, bioavailability indices, cost calculations, and serving nutrition tables are **100% computed deterministically** in Python and Postgres.
- **LLM Role**: The Large Language Model receives pre-computed, structured JSON data. It translates, simplifies, and explains this data into plain language across 5 languages (English, Tamil, Hindi, Telugu, Malayalam). The LLM is strictly prohibited from inventing numbers, diagnoses, or ingredient quantities.
- **Number Guard**: Every LLM response is scanned by regex and parsed numbers are compared against the input JSON. Any hallucinated number triggers rejection and falls back to deterministic template-generated explanations.

---

## 2. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  Frontend                                         |
|    React 18 + Vite + TypeScript + Tailwind CSS + TanStack Query + react-i18next   |
|               (5 Languages: EN, TA, HI, TE, ML | Responsive UI Kit)               |
+-----------------------------------------------------------------------------------+
                                        | (HTTPS / REST API)
                                        v
+-----------------------------------------------------------------------------------+
|                             FastAPI Backend (/api/v1)                             |
|  +-----------------------------------------------------------------------------+  |
|  | Middleware: Auth (Supabase/Firebase/Dev) | Rate Limiting | Audit Logging   |  |
|  +-----------------------------------------------------------------------------+  |
|         |                     |                      |                    |       |
|         v                     v                      v                    v       |
|  +--------------+    +------------------+    +---------------+   +--------------+ |
|  | OCR Pipeline |    |   Safety Gate    |    |  Formulation  |   | LLM & Voice  | |
|  | PyMuPDF /    |    | Assessment Rules |    |  Optimizer    |   | Number Guard | |
|  | pdfplumber   |    | (JSON RuleSets)  |    |  (HiGHS / LP) |   | STT/TTS      | |
|  +--------------+    +------------------+    +---------------+   +--------------+ |
+-----------------------------------------------------------------------------------+
             |                                                  |
             v                                                  v
+------------------------------------+          +-----------------------------------+
|         Object Storage             |          |     PostgreSQL 15+ Database       |
| (Cloudflare R2 / MinIO / Supabase) |          | (JSONB, pg_trgm, pgcrypto, RLS)   |
| - Private Encrypted Lab Reports    |          | - Append-only Health Assessments  |
| - Illustrative Product Assets      |          | - Versioned Formulations & Rules  |
+------------------------------------+          +-----------------------------------+
```

---

## 3. Medical Safety Boundaries
1. **Supportive, Not Curative**: NutriAI is a dietary support and food formulation system. It does not diagnose, treat, or cure medical conditions. UI vocabulary strictly enforces this ("supports nutritional intake", "may help meet daily dietary needs").
2. **Etiological Differentiation**: Anaemia is not assumed to be iron deficiency. If MCV is low but Ferritin is elevated/normal, or if B12/Folate is deficient, an etiological review flag is raised without pushing iron-heavy formulations.
3. **Safety Gate Actions**:
   - `ok`: Standard formulation generation permitted.
   - `caution`: Moderate values or dietary conditions noted; advisory warning shown on result.
   - `refer_to_doctor`: Guidance issued; formulation permitted only if `ALLOW_GENERATION_WITH_REFERRAL=true`.
   - `blocked`: Severe haemoglobin (< 7.0 g/dL) or critical red flags abort product generation and mandate urgent clinical evaluation.
4. **Allergens as Invariable Constraints**: Allergens are excluded at the SQL filter level, in linear programming constraints, and verified post-solver by an independent validator.

---

## 4. Service Boundaries
- `app.services.ocr`: File verification, extraction via PyMuPDF/pdfplumber, regex token parsing, rapidfuzz parameter alias matching, unit normalization.
- `app.services.assessment`: Deterministic evaluation of lab results and demographic factors against versioned rule sets.
- `app.services.formulation`: Candidate filtering, linear programming optimization (HiGHS via `scipy.optimize.linprog`), bioavailability scoring, and dual validation.
- `app.services.llm`: LLM provider adapter (Gemini, Anthropic, Mock), template fallback, and strict numerical auditing via the Number Guard.
- `app.services.speech`: Browser Web Speech API fallback, Google Cloud STT/TTS, and Bhashini placeholder adapters.
- `app.services.storage`: S3/MinIO and Supabase Storage signed URL management.

