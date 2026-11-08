# NutriAI – API Specification (/api/v1)

All endpoints follow consistent JSON envelopes:
- Success: Standard JSON payload or `{ "data": ... }`.
- Error: `{ "error": { "code": "STRING_CODE", "message": "Human readable message", "details": {} } }`.

---

## 1. Public Endpoints
- `GET /api/v1/health` -> `{ "status": "healthy", "platform": "...", "timestamp": "..." }`
- `GET /api/v1/public/statistics` -> Returns verified statistics (`status=verified`) for Indian epidemiological indicators.
- `GET /api/v1/public/products/categories` -> Formats & categories with prototype notices.
- `POST /api/v1/public/contact` -> Submit contact form inquiry (sanitized, saved, and acknowledged).
- `GET /api/v1/education` -> List educational modules in the requested language.
- `GET /api/v1/education/{slug}` -> Fetch detailed module with reference citations and review status.

---

## 2. Authentication & Consent
- `POST /api/v1/auth/session` -> Verify ID token (Supabase/Firebase/Dev) and return internal session + user profile.
- `POST /api/v1/auth/register-profile` -> Create initial user profile with DOB, language, and role.
- `POST /api/v1/auth/guardian-consent` -> Submit minor (under 18) guardian consent.
- `DELETE /api/v1/auth/account` -> GDPR/DPDP compliant account deletion & data anonymization.

---

## 3. User Profile & Health Data
- `GET /api/v1/profile` -> Fetch user profile.
- `PATCH /api/v1/profile` -> Update demographic information.
- `GET /api/v1/profile/measurements` -> Fetch anthropometric history (height, weight, computed BMI).
- `POST /api/v1/profile/measurements` -> Append new physical measurement.
- `PUT /api/v1/profile/diet` -> Save dietary preferences (diet type, allergies, budget, format preference).
- `PUT /api/v1/profile/allergies` -> Update active allergens and restrictions.
- `PUT /api/v1/profile/health` -> Update encrypted health details (deficiencies, medications).

---

## 4. Reports & OCR Pipeline
- `POST /api/v1/reports` -> Upload PDF / image lab report (multipart/form-data; max 10MB; runs OCR asynchronously).
- `GET /api/v1/reports` -> List user's uploaded reports.
- `GET /api/v1/reports/{id}` -> Fetch report status and extracted laboratory parameters.
- `PATCH /api/v1/reports/{id}/results` -> Update/correct flagged extracted parameters.
- `POST /api/v1/reports/{id}/confirm` -> Mark all parameters reviewed and confirmed.
- `DELETE /api/v1/reports/{id}` -> Delete report and extracted values.

---

## 5. Assessment & Formulation Generation
- `POST /api/v1/assessments` -> Run deterministic clinical safety gate and generate nutrient targets.
- `GET /api/v1/assessments/{id}` -> Fetch assessment findings and safety status (`ok`, `caution`, `refer_to_doctor`, `blocked`).
- `POST /api/v1/formulations/generate` -> Run HiGHS Linear Programming optimizer to produce prototype candidates.
- `GET /api/v1/recommendations/{id}` -> Get ranked recommendation details, why-selected rationale, and instructions.
- `POST /api/v1/recommendations/{id}/save` -> Save formulation to user's saved list.
- `GET /api/v1/recommendations/compare?ids=id1,id2,id3` -> Side-by-side comparison of formulations.
- `GET /api/v1/recommendations/{id}/report.pdf` -> Download nutritional specification PDF.

---

## 6. Shop, Cart & Sandbox Orders
- `GET /api/v1/shop/products` -> Browse formulations and category catalog.
- `GET /api/v1/shop/products/{id}` -> Product specification view.
- `GET /api/v1/cart/items` -> View active cart with server-side recalculated subtotals.
- `POST /api/v1/cart/items` -> Add prototype item to cart.
- `PATCH /api/v1/cart/items/{id}` -> Update item quantity.
- `DELETE /api/v1/cart/items/{id}` -> Remove item from cart.
- `POST /api/v1/checkout` -> Place sandbox demo order (`is_prototype=true`, `payment_mode=demo_sandbox`).
- `GET /api/v1/orders` -> List user orders.
- `GET /api/v1/orders/{id}` -> Order details with status lifecycle events.
- `POST /api/v1/orders/{id}/cancel` -> Cancel order if still pending.

---

## 7. Progress & Adherence
- `POST /api/v1/progress/plans` -> Create consumption adherence plan from order item.
- `POST /api/v1/progress/plans/{id}/logs` -> Log daily consumption.
- `GET /api/v1/progress/overview` -> Adherence score, calendar heatmap, remaining servings.
- `GET /api/v1/progress/lab-comparison` -> Historical Hb and Ferritin trend lines over time.
- `POST /api/v1/reminders` -> Configure daily notification time.

---

## 8. Chatbot & Voice
- `POST /api/v1/chat/sessions` -> Start chat session (`general` or `personalized`).
- `POST /api/v1/chat/sessions/{id}/messages` -> Send query; responds with grounded, number-guarded answer.
- `POST /api/v1/voice/stt` -> Audio speech-to-text endpoint.
- `POST /api/v1/voice/tts` -> Text-to-speech audio synthesis endpoint.

---

## 9. Admin & Audit
- Admin CRUD: `/api/v1/admin/ingredients`, `/api/v1/admin/ingredient-nutrients`, `/api/v1/admin/reference-values`, `/api/v1/admin/rule-sets`, `/api/v1/admin/statistics`, `/api/v1/admin/education`.
- `PATCH /api/v1/admin/orders/{id}/status` -> Advance order lifecycle (pending -> confirmed -> processing -> shipped -> delivered).
- `GET /api/v1/admin/audit-logs` -> Query immutable security & clinical audit events.

