# NutriAI – Architecture & Engineering Decisions Log (ADR)

## Decision 1: Hybrid PostgreSQL + Supabase / Local Docker Strategy
- **Status**: Approved & Implemented
- **Context**: The application requires complex relational constraints, transactions for checkout, JSONB storage for flexible OCR outputs/rule sets, and full-text trigram (`pg_trgm`) matching for ingredient aliases.
- **Decision**: Use PostgreSQL 15+ as the single database engine. Support Supabase Postgres as the managed production environment and local Docker PostgreSQL for offline development. SQLite is strictly disallowed per specification.
- **Consequences**: Ensures full SQL schema and RLS parity across all environments.

## Decision 2: Linear Programming Engine using `scipy.optimize.linprog` (HiGHS)
- **Status**: Approved & Implemented
- **Context**: The formulation engine requires deterministic optimization to minimize cost and deviation penalties while fulfilling dietary constraints (serving size, iron, vitamin C ratio, folate, HFSS caps).
- **Decision**: Use `scipy.optimize.linprog` with the modern HiGHS interior-point/simplex solver. It provides robust, deterministic polynomial-time guarantees and ships standard with SciPy without external binary dependencies.
- **Consequences**: High determinism, reproducible recipes across identical inputs, and detailed solver status codes (`feasible`, `infeasible`, `unbounded`).

## Decision 3: Deterministic "Number Guard" on LLM Explanations
- **Status**: Approved & Implemented
- **Context**: Clinical nutrition prohibits LLM hallucinations of nutrient numbers, RDA percentages, or clinical dosages.
- **Decision**: Post-process every LLM generation using regex extraction of numerical tokens (`\b\d+(?:\.\d+)?\b`). Reject responses containing numbers not present in the assessment/recommendation source JSON, falling back immediately to pre-rendered template text.
- **Consequences**: Zero numerical hallucinations reach the user interface.

## Decision 4: Tri-Provider Authentication Interface
- **Status**: Approved & Implemented
- **Context**: Different deployment targets may prefer Supabase Auth, Firebase Auth, or offline development (`AUTH_MODE=dev`).
- **Decision**: Implement an abstract `AuthProvider` protocol (`verify_token(token) -> AuthUser`) with three concrete implementations: `SupabaseAuthProvider`, `FirebaseAuthAdminProvider`, and `DevLocalAuthProvider`. Ensure `DevLocalAuthProvider` throws a fatal error if executed under `APP_ENV=production`.
- **Consequences**: Pluggable authentication with zero vendor lock-in.

## Decision 5: Tri-Provider Storage Interface
- **Status**: Approved & Implemented
- **Context**: File uploads (PDFs, images) require short-lived signed URLs and private bucket isolation.
- **Decision**: Create an abstract `StorageProvider` protocol with adapters for `S3StorageProvider` (MinIO/R2 via boto3), `SupabaseStorageProvider`, and `FirebaseStorageProvider`.
- **Consequences**: Portable encrypted storage across cloud and local setups.

