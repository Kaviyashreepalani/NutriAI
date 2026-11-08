# Setting up NutriAI with Supabase (Configuration A - Recommended)

This guide walks you through setting up NutriAI with Supabase for PostgreSQL, Supabase Auth, and Supabase Storage.

---

## 1. Create a Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign in.
2. Click **New Project**.
3. Name it `nutriai-prod` (or `nutriai-dev`), choose a secure database password, and select a region close to your users (e.g. `ap-south-1` Mumbai).
4. Wait for database provisioning to complete.

---

## 2. Obtain Credentials & Environment Variables
In the Supabase Dashboard:
1. Navigate to **Project Settings** -> **API**:
   - Copy **Project URL** -> `SUPABASE_URL`
   - Copy **anon public** key -> `SUPABASE_ANON_KEY`
   - Copy **service_role secret** -> `SUPABASE_SERVICE_ROLE_KEY` *(NEVER expose to frontend)*
   - Copy **JWT Secret** -> `SUPABASE_JWT_SECRET`
2. Navigate to **Project Settings** -> **Database**:
   - Under **Connection string**, select **URI**:
     - Pooled (Transaction Mode, port 6543) -> `DATABASE_URL`
     - Direct (Session Mode, port 5432) -> `DATABASE_DIRECT_URL`

Update your `.env`:
```env
DATA_PLATFORM=supabase
AUTH_PROVIDER=supabase
STORAGE_PROVIDER=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.your-project.supabase.co:6543/postgres
DATABASE_DIRECT_URL=postgresql://postgres:[YOUR-PASSWORD]@db.your-project.supabase.co:5432/postgres
```

---

## 3. Run Database Migrations & Seed Data
Execute from the backend directory:
```bash
cd backend
# Run Alembic migrations
alembic upgrade head

# Load initial seed data (ingredients, rules, reference values)
python -m app.seed.load
```

---

## 4. Create Storage Buckets
In the Supabase Dashboard, go to **Storage**:
1. Click **New Bucket**.
2. Name: `reports`.
   - Set as **Private** (Not public).
   - Set File size limit to `10MB`.
   - Allowed MIME types: `application/pdf, image/jpeg, image/png`.
3. Name: `product-images`.
   - Set as **Public** bucket.

---

## 5. Enable Row-Level Security (RLS)
The Alembic migrations automatically apply RLS policies ensuring that:
- Users can only view and mutate their own profiles, lab reports, assessments, and orders.
- Reference tables (ingredients, rules) are read-only for authenticated users and writable only by admin/service roles.

