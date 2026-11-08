# NutriAI – Production Deployment Guide

## 1. Architecture & Services Deployment Targets

| Layer | Recommended Platforms | Alternative |
| :--- | :--- | :--- |
| **Frontend** | Vercel | Netlify / Cloudflare Pages |
| **Backend** | Render / Railway (Docker container) | Fly.io / AWS ECS |
| **Database** | Supabase Postgres (Managed PG 15+) | Neon Postgres |
| **File Storage** | Supabase Storage | Cloudflare R2 / AWS S3 |

---

## 2. Backend Deployment (e.g. Render / Railway via Docker)
1. Link your Git repository to Render or Railway.
2. Select **Web Service** using the Dockerfile located at `backend/Dockerfile`.
3. Set Environment Variables:
   - `APP_ENV=production`
   - `DEBUG=false`
   - `SECRET_KEY=[GENERATED_64_CHAR_HEX]`
   - `ENCRYPTION_KEY=[32_BYTE_BASE64_KEY]`
   - `DATA_PLATFORM=supabase`
   - `AUTH_PROVIDER=supabase` (or `firebase`)
   - `STORAGE_PROVIDER=supabase` (or `s3`)
   - `DATABASE_URL=postgresql+asyncpg://...` (pooled connection string)
   - `DATABASE_DIRECT_URL=postgresql://...` (direct connection string for Alembic)
   - `SUPABASE_URL=...`
   - `SUPABASE_ANON_KEY=...`
   - `SUPABASE_SERVICE_ROLE_KEY=...`
   - `SUPABASE_JWT_SECRET=...`
   - `FRONTEND_URL=https://your-frontend-domain.vercel.app`
   - `ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app`
4. Pre-deploy or release command:
   ```bash
   alembic upgrade head && python -m app.seed.load
   ```

---

## 3. Frontend Deployment (e.g. Vercel)
1. Import repository on Vercel.
2. Set Root Directory to `frontend`.
3. Framework Preset: **Vite**.
4. Build Command: `npm run build`.
5. Output Directory: `dist`.
6. Environment Variables:
   - `VITE_API_BASE_URL=https://your-backend-domain.onrender.com/api/v1`
   - `VITE_SUPABASE_URL=https://your-project.supabase.co`
   - `VITE_SUPABASE_ANON_KEY=...`
7. Ensure SPA rewriting is enabled via `frontend/vercel.json`:
   ```json
   {
     "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
   }
   ```

---

## 4. Pre-Launch Security Checklist
- [ ] `AUTH_MODE=dev` is strictly disallowed in production (`APP_ENV=production` fails startup if enabled).
- [ ] `SUPABASE_SERVICE_ROLE_KEY` is nowhere in frontend repository or build bundles.
- [ ] CORS `ALLOWED_ORIGINS` is restricted only to trusted frontend domains.
- [ ] All database user-level tables have PostgreSQL Row-Level Security (RLS) active.
- [ ] Storage buckets are private; downloads strictly require signed tokens.
- [ ] Rate limiting is activated on `/api/v1/auth/*`, `/api/v1/reports`, `/api/v1/chat/*`.
- [ ] Medical disclaimer and prototype badges appear in all production interfaces.

