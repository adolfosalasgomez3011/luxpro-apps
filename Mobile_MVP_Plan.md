# MOBILE-FIRST MVP IMPLEMENTATION PLAN
## Freelance Applicator Management System (FAMS)

**Target Platform:** Mobile Web App (Progressive Web App)  
**Timeline:** 2-3 weeks  
**Tech Stack:** Python Streamlit + SQLite + Mobile-Optimized UI

---

## I. MOBILE-FIRST APPROACH

### Why Mobile?
- **Field Use**: Supervisors need access on-site during projects
- **Quick Calls**: Find available freelancers while at obra
- **Instant Contact**: WhatsApp/call directly from app
- **Photo Upload**: Document work from phone camera
- **Real-time Updates**: Mark attendance, update status on the go

### Technology Choice: Streamlit PWA

**Advantages:**
- ✅ Rapid development (1-2 weeks for MVP)
- ✅ Python backend (easy database integration)
- ✅ Mobile-responsive out of box
- ✅ Can be installed as PWA on phone
- ✅ No app store needed
- ✅ Free hosting on Streamlit Cloud

**Mobile Optimizations:**
- Large touch targets (min 44px buttons)
- Card-based layout (scrollable lists)
- Bottom navigation for key actions
- Swipe gestures where possible
- Phone/WhatsApp quick actions
- Camera integration for photos

---

## II. MVP FEATURE SET (Mobile-Optimized)

### Core Screens (5 screens)

#### 1. 🏠 Home / Dashboard
- Quick stats (disponibles hoy, en proyecto, total)
- Search bar (large, prominent)
- Recent freelancers (last contacted)
- Quick actions (+ Add, 🔍 Search, 📊 Stats)

#### 2. 👥 Freelancer List
- Card-based design (one per freelancer)
- Show: Photo, Name, Rating ⭐, Phone 📱
- Quick actions per card:
  - 📞 Call
  - 💬 WhatsApp
  - 👁️ View Profile
- Infinite scroll or pagination
- Pull-to-refresh

#### 3. ➕ Add/Edit Freelancer
- Form with mobile-friendly inputs
- Large text fields
- Dropdowns for categories
- Star rating selector (tap to rate)
- Photo upload from camera
- Save at bottom (sticky button)

#### 4. 🔍 Search & Filter
- Search by name (auto-suggest)
- Filter chips:
  - 📍 Location
  - 🎨 Product/Skill
  - ⭐ Min Rating
  - 📅 Available Today
- Results update in real-time
- Clear all filters button

#### 5. 👤 Freelancer Profile (Read-Only)
- Top: Photo + Name + Rating
- Contact section (phone/email with action buttons)
- Skills & Products (tags)
- Recent projects (last 3)
- Availability status
- Bottom: Actions
  - ✏️ Edit
  - 🏗️ Assign to Project
  - 📝 Add Note

### Secondary Features (Phase 1.5)

#### 6. 🏗️ Assign to Project
- Project selector (dropdown or search)
- Date range picker (mobile-friendly)
- Rate input (auto-filled from freelancer rates)
- Confirm button

#### 7. ⭐ Rate Freelancer
- After project, rate on 5 dimensions
- Large star selector (easy to tap)
- Text area for comments
- Submit rating

---

## III. DATABASE IMPLEMENTATION

### Simplified Schema (MVP Only)

```sql
-- 1. Freelancers (Core)
CREATE TABLE freelancers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni VARCHAR(8) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    distrito VARCHAR(50),
    foto_path VARCHAR(255),
    skills TEXT, -- Comma-separated for MVP
    rating_promedio DECIMAL(3,2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'Activo',
    disponible BOOLEAN DEFAULT 1,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Projects (Simplified)
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    cliente VARCHAR(200),
    ubicacion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    metros_cuadrados DECIMAL(10,2),
    producto VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Planificado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Assignments (Linking table)
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    freelancer_id INTEGER NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    tarifa_m2 DECIMAL(10,2),
    monto_total DECIMAL(10,2),
    estado_pago VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id)
);

-- 4. Ratings
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    calidad INTEGER CHECK(calidad BETWEEN 1 AND 5),
    puntualidad INTEGER CHECK(puntualidad BETWEEN 1 AND 5),
    instrucciones INTEGER CHECK(instrucciones BETWEEN 1 AND 5),
    seguridad INTEGER CHECK(seguridad BETWEEN 1 AND 5),
    profesionalismo INTEGER CHECK(profesionalismo BETWEEN 1 AND 5),
    rating_general DECIMAL(3,2),
    comentarios TEXT,
    fecha DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id)
);

-- 5. Contact Log (Simple)
CREATE TABLE contact_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(20), -- Llamada, WhatsApp, Email
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id)
);
```

---

## IV. MOBILE UI SPECIFICATIONS

### Design System

**Colors:**
- Primary: #2563eb (Blue)
- Success: #16a34a (Green)
- Warning: #f59e0b (Orange)
- Danger: #dc2626 (Red)
- Neutral: #6b7280 (Gray)

**Typography:**
- Headings: 20px-24px (bold)
- Body: 16px (normal)
- Captions: 14px (light)

**Spacing:**
- Touch targets: min 44px height
- Card padding: 16px
- Between cards: 12px
- Screen padding: 16px

**Components:**
- Cards: White background, shadow, rounded corners (8px)
- Buttons: Full width or min 120px, 48px height, rounded (6px)
- Inputs: 48px height, rounded (6px), clear borders

### Mobile UX Patterns

**Navigation:**
```
┌─────────────────────────────────┐
│  FAMS - LUX                     │ (Top bar)
├─────────────────────────────────┤
│                                 │
│  [Main Content Area]            │
│  [Scrollable]                   │
│                                 │
│                                 │
├─────────────────────────────────┤
│  🏠  👥  ➕  🔍  📊           │ (Bottom nav)
└─────────────────────────────────┘
```

**Freelancer Card:**
```
┌─────────────────────────────────┐
│ 📷    Juan Pérez                │
│ [Img]  ⭐⭐⭐⭐⭐ 4.5         │
│        📍 San Juan de Lurigancho│
│        🔧 JP01Y, Epóxico        │
│                                 │
│        📱 987-654-321           │
│   [📞 Call] [💬 WhatsApp]      │
│             [👁️ Ver Más]        │
└─────────────────────────────────┘
```

**Add Freelancer Form:**
```
┌─────────────────────────────────┐
│  ➕ Nuevo Freelancer            │
│                                 │
│  📷 [Tap to add photo]          │
│                                 │
│  Nombre Completo                │
│  [____________________]         │
│                                 │
│  DNI                            │
│  [____________________]         │
│                                 │
│  Teléfono / WhatsApp            │
│  [____________________]         │
│                                 │
│  Distrito                       │
│  [Seleccionar ▼]                │
│                                 │
│  Skills (separados por coma)    │
│  [____________________]         │
│                                 │
│  Rating Inicial                 │
│  ☆☆☆☆☆ (Tap para calificar)  │
│                                 │
│  Estado                         │
│  [●] Activo  [ ] Inactivo      │
│                                 │
│  [        GUARDAR        ]      │ (Sticky)
└─────────────────────────────────┘
```

---

## V. DEVELOPMENT PHASES

### Week 1: Core Setup + Basic CRUD

**Days 1-2: Setup**
- [x] Database schema creation
- [x] Streamlit project initialization
- [x] Mobile CSS customization
- [x] Sample data insertion (10 freelancers)

**Days 3-5: Freelancer Management**
- [ ] Freelancer list view (cards)
- [ ] Add new freelancer form
- [ ] Edit freelancer form
- [ ] Delete confirmation
- [ ] View freelancer profile

**Days 6-7: Search & Actions**
- [ ] Search by name
- [ ] Filter by skill
- [ ] Filter by distrito
- [ ] Quick contact actions (call/WhatsApp links)

### Week 2: Projects & Ratings

**Days 8-10: Project Module**
- [ ] Project list
- [ ] Create project
- [ ] Assign freelancer to project
- [ ] View project details with assigned freelancers

**Days 11-12: Rating System**
- [ ] Rating form (5 dimensions)
- [ ] Save rating to database
- [ ] Update freelancer average rating
- [ ] View ratings history

**Days 13-14: Polish & Testing**
- [ ] Mobile testing on real devices
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Bug fixes

### Week 3: Deployment & Training

**Days 15-17: Deployment**
- [ ] Deploy to Streamlit Cloud
- [ ] PWA configuration (installable)
- [ ] Test on multiple devices
- [ ] Create user documentation

**Days 18-21: Training & Feedback**
- [ ] Train LUX team
- [ ] Collect feedback
- [ ] Quick iterations
- [ ] Plan Phase 2 features

---

## VI. DEPLOYMENT PLAN

### Streamlit Cloud (Free Tier)

**Steps:**
1. Create GitHub repo: `lux-fams-mobile`
2. Push code to repo
3. Connect Streamlit Cloud to repo
4. Configure secrets (if needed)
5. Deploy (auto-updates on git push)

**URL Format:**
`https://lux-fams.streamlit.app`

**PWA Features:**
- Add manifest.json (app name, icons, theme)
- Enable "Add to Home Screen" on mobile
- Works like native app once installed

### Mobile Access:
1. Open URL in phone browser
2. Tap "Share" → "Add to Home Screen"
3. App icon appears on phone
4. Opens full-screen (like native app)

---

## VII. PROJECT STRUCTURE

```
lux-fams-mobile/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── database.py            # Database operations
├── models.py              # Data models/classes
├── utils.py               # Utility functions
│
├── pages/                 # Streamlit pages
│   ├── 1_👥_Freelancers.py
│   ├── 2_🏗️_Projects.py
│   ├── 3_⭐_Ratings.py
│   └── 4_📊_Stats.py
│
├── data/
│   └── fams.db           # SQLite database
│
├── static/
│   ├── style.css         # Mobile-optimized CSS
│   ├── manifest.json     # PWA manifest
│   └── icons/            # App icons
│
├── photos/               # Freelancer photos
│   └── .gitkeep
│
└── README.md
```

---

## VIII. MOBILE-SPECIFIC FEATURES

### Quick Actions
- **Call Direct**: `tel:+51987654321` links
- **WhatsApp**: `https://wa.me/51987654321` links
- **Maps**: `https://maps.google.com/?q=distrito` for location

### Camera Integration
- Photo upload using Streamlit `camera_input()`
- Save to `/photos/` folder
- Display in profile cards

### Offline Support (Future)
- Service worker for basic offline functionality
- Cache freelancer list
- Queue actions when offline, sync when online

### Performance Optimization
- Lazy load images
- Paginate lists (20 per page)
- Cache database queries
- Compress photos automatically

---

## IX. SUCCESS CRITERIA (MVP)

### Must Have (Week 1-2):
- ✅ Add/Edit/Delete freelancers
- ✅ Search by name
- ✅ View freelancer list (mobile cards)
- ✅ Quick call/WhatsApp
- ✅ Basic rating system
- ✅ Works on mobile browser

### Should Have (Week 2-3):
- ✅ Project creation
- ✅ Assign freelancer to project
- ✅ Filter by skill/location
- ✅ Photo upload
- ✅ Deployed to cloud

### Nice to Have (Phase 2):
- Availability calendar
- Advanced analytics
- Bulk import from Excel
- Push notifications
- Offline mode

---

## X. NEXT IMMEDIATE STEPS

1. **Create Database** (15 min)
   - Run schema creation script
   - Insert 10 sample freelancers

2. **Initialize Streamlit App** (30 min)
   - Create basic structure
   - Add mobile CSS
   - Test on phone

3. **Build Freelancer List** (2 hours)
   - Read from database
   - Display as cards
   - Add search box

4. **Add Contact Actions** (1 hour)
   - Call button with tel: link
   - WhatsApp button with wa.me link

5. **Test on Mobile** (30 min)
   - Open on phone browser
   - Test touch interactions
   - Verify responsiveness

**Total Time to Working Prototype: ~4 hours**

---

Ready to start building? 🚀
