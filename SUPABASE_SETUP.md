# SUPABASE SETUP GUIDE
## FAMS - Freelance Applicator Management System

**Why Supabase?**
- ✅ Cloud database (accessible from any device)
- ✅ Free tier (up to 500MB database, 2GB bandwidth)
- ✅ Real-time updates (see changes instantly)
- ✅ Built-in authentication (if needed later)
- ✅ PostgreSQL (more powerful than SQLite)
- ✅ Automatic API generation

---

## STEP 1: Create Supabase Project (5 minutes)

1. Go to https://supabase.com
2. Sign up / Log in (use your email)
3. Click "New Project"
4. Fill in:
   - **Name**: `lux-fams`
   - **Database Password**: [Create strong password - SAVE THIS!]
   - **Region**: South America (São Paulo) - closest to Peru
   - **Pricing**: Free tier
5. Click "Create new project"
6. Wait 2-3 minutes for setup

---

## STEP 2: Get Connection Details

Once project is created:

1. Go to **Project Settings** (gear icon bottom left)
2. Go to **API** section
3. Copy these values:

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
Project API Key (anon, public): eyJhbGc...
```

4. Save these in a file `secrets.txt` (DON'T commit to git!)

---

## STEP 3: Create Database Schema

1. In Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click "New Query"
3. Copy and paste the SQL schema below:

```sql
-- 1. Freelancers table
CREATE TABLE freelancers (
    id BIGSERIAL PRIMARY KEY,
    dni VARCHAR(8) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    distrito VARCHAR(50),
    foto_url TEXT,
    skills TEXT,
    rating_promedio DECIMAL(3,2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'Activo',
    disponible BOOLEAN DEFAULT true,
    notas TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. Projects table
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    cliente VARCHAR(200),
    ubicacion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    metros_cuadrados DECIMAL(10,2),
    producto VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Planificado',
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Assignments table
CREATE TABLE assignments (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    freelancer_id BIGINT NOT NULL REFERENCES freelancers(id) ON DELETE CASCADE,
    fecha_inicio DATE,
    fecha_fin DATE,
    tarifa_m2 DECIMAL(10,2),
    monto_total DECIMAL(10,2),
    estado_pago VARCHAR(20) DEFAULT 'Pendiente'
);

-- 4. Ratings table
CREATE TABLE ratings (
    id BIGSERIAL PRIMARY KEY,
    assignment_id BIGINT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    calidad INTEGER CHECK(calidad BETWEEN 1 AND 5),
    puntualidad INTEGER CHECK(puntualidad BETWEEN 1 AND 5),
    instrucciones INTEGER CHECK(instrucciones BETWEEN 1 AND 5),
    seguridad INTEGER CHECK(seguridad BETWEEN 1 AND 5),
    profesionalismo INTEGER CHECK(profesionalismo BETWEEN 1 AND 5),
    rating_general DECIMAL(3,2),
    comentarios TEXT,
    fecha DATE DEFAULT CURRENT_DATE
);

-- 5. Contact log table
CREATE TABLE contact_log (
    id BIGSERIAL PRIMARY KEY,
    freelancer_id BIGINT NOT NULL REFERENCES freelancers(id) ON DELETE CASCADE,
    fecha TIMESTAMP DEFAULT NOW(),
    tipo VARCHAR(20),
    notas TEXT
);

-- Create indexes for better performance
CREATE INDEX idx_freelancers_nombre ON freelancers(nombre);
CREATE INDEX idx_freelancers_distrito ON freelancers(distrito);
CREATE INDEX idx_freelancers_disponible ON freelancers(disponible);
CREATE INDEX idx_projects_estado ON projects(estado);
CREATE INDEX idx_assignments_project ON assignments(project_id);
CREATE INDEX idx_assignments_freelancer ON assignments(freelancer_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add trigger to freelancers
CREATE TRIGGER update_freelancers_updated_at BEFORE UPDATE ON freelancers
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO freelancers (dni, nombre, telefono, email, distrito, skills, rating_promedio, disponible, notas) VALUES
('12345678', 'Juan Carlos Pérez', '987654321', 'jperez@email.com', 'San Juan de Lurigancho', 'JP01Y, Epóxico, Rodillo', 4.5, true, 'Muy confiable, trabaja hace 2 años'),
('23456789', 'María López Gonzales', '912345678', 'mlopez@email.com', 'Callao', 'Poliurea, Spray, JP02R', 4.8, false, 'Especialista en impermeabilización'),
('34567890', 'Carlos Ramírez', '998877665', 'cramirez@email.com', 'Ate', 'Epóxico, JP01Y, Preparación superficie', 4.2, true, 'Bueno para proyectos grandes'),
('45678901', 'Ana Torres', '987123456', 'atorres@email.com', 'Villa El Salvador', 'JS02Y, Poliaspártico, Rodillo', 4.6, true, 'Excelente acabado, puntual'),
('56789012', 'Roberto Silva', '965432109', 'rsilva@email.com', 'San Martín de Porres', 'Epóxico, Preparación, Lijado', 3.9, true, 'En capacitación, mejorando'),
('67890123', 'Patricia Vargas', '923456789', 'pvargas@email.com', 'Surco', 'Poliurea, JP01Y, Spray', 4.7, false, 'Proyecto grande hasta 20/01'),
('78901234', 'Luis Mendoza', '945678901', 'lmendoza@email.com', 'Los Olivos', 'Epóxico, 1002A, Rodillo', 4.4, true, 'Especialista en talleres automotrices'),
('89012345', 'Rosa Fernández', '978901234', 'rfernandez@email.com', 'Chorrillos', 'JS02Y, Poliurea, Preparación', 4.3, true, 'Buena para zonas costeras'),
('90123456', 'Miguel Castro', '912567890', 'mcastro@email.com', 'Independencia', 'Epóxico, JP01Y, Brocha', 3.8, true, 'Nuevo, necesita supervisión'),
('01234567', 'Sandra Ruiz', '987654123', 'sruiz@email.com', 'Breña', 'Poliurea, Impermeabilización, JP02R', 4.9, true, 'Top performer, muy recomendada');
```

4. Click **Run** (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

---

## STEP 4: Enable Row Level Security (RLS) - Optional

For now, we'll keep it simple. Later you can add authentication and permissions.

Go to **Authentication** → **Policies** and enable RLS when ready.

---

## STEP 5: Test Connection

1. Go to **Table Editor** (left sidebar)
2. You should see 5 tables: freelancers, projects, assignments, ratings, contact_log
3. Click `freelancers` - you should see 10 sample records

---

## STEP 6: Configure Python App

Create a file `.streamlit/secrets.toml` in your project:

```toml
# .streamlit/secrets.toml
[supabase]
url = "https://xxxxxxxxxxxxx.supabase.co"
key = "eyJhbGc..."
```

**IMPORTANT:** Add `.streamlit/` to `.gitignore` to keep secrets safe!

---

## Cost Estimate

**Free Tier Limits:**
- 500MB database storage
- 2GB bandwidth/month
- 50,000 monthly active users
- Unlimited API requests

**Estimated Usage (50 freelancers):**
- Database: ~5MB
- Bandwidth: ~100MB/month
- **Cost: $0 (well within free tier)**

---

## Next Steps

1. Create Supabase project
2. Run SQL schema
3. Update `secrets.toml` with your credentials
4. Run the app!

---

## Troubleshooting

**Can't connect?**
- Check URL and API key are correct
- Verify project is "Active" in Supabase dashboard

**Sample data not showing?**
- Go to SQL Editor and run the INSERT statements again

**Need help?**
- Supabase docs: https://supabase.com/docs
- Support: support@supabase.io
