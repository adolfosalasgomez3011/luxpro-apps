# FREELANCE APPLICATOR MANAGEMENT SYSTEM (FAMS)
## Sistema de Gestión de Aplicadores Freelance - LUX

**Versión:** 1.0  
**Fecha:** 13 de Enero, 2026  
**Autor:** Adolfo Salas - LUX Pisos Industriales

---

## I. EXECUTIVE SUMMARY

### Problem Statement
LUX necesita escalar la ejecución de proyectos de aplicación de revestimientos poliméricos sin contratar personal permanente de tiempo completo. La solución es crear una red de aplicadores freelance calificados que puedan ser convocados bajo demanda según las necesidades del proyecto.

### Solution Overview
Un sistema integral de gestión que permite:
- **Registro y perfilado** de aplicadores freelance
- **Seguimiento de capacitación** y certificaciones
- **Sistema de calificación** basado en proyectos previos
- **Disponibilidad y localización** para asignación rápida
- **Gestión de tarifas** y pagos
- **Historial de proyectos** y rendimiento

### Key Benefits
1. **Escalabilidad**: Capacidad de ejecutar múltiples proyectos simultáneos sin overhead fijo
2. **Flexibilidad**: Contratar según demanda real del proyecto
3. **Control de Calidad**: Sistema de rating y certificación
4. **Reducción de Costos**: Sin cargas laborales permanentes
5. **Cobertura Geográfica**: Red distribuida en Lima y provincias

---

## II. SYSTEM REQUIREMENTS

### 2.1 Functional Requirements

#### A. Freelancer Profile Management
- Registro de información personal (nombre, DNI, contacto, dirección)
- Documentos (CV, certificados, SCTR, pólizas)
- Habilidades técnicas (productos que domina, equipos que maneja)
- Disponibilidad (calendario, zona geográfica)
- Expectativa de tarifa (por m², por día, por proyecto)
- Fotografías/videos de trabajos previos

#### B. Training & Certification Tracking
- Registro de capacitaciones completadas
  * Productos específicos (JP01Y, JS02Y, epóxicos, etc.)
  * Técnicas de aplicación (rodillo, spray, brocha)
  * Preparación de superficie (CSP, imprimación)
  * Seguridad industrial
- Certificaciones oficiales (si aplica)
- Fecha de última capacitación
- Próximas capacitaciones programadas
- Nivel de competencia: Aprendiz / Intermedio / Experto / Master

#### C. Project History & Performance
- Proyectos completados con LUX
- Fecha, cliente, tipo de proyecto
- Metros cuadrados aplicados
- Producto(s) utilizado(s)
- Calificación por proyecto (1-5 estrellas)
- Comentarios de supervisores
- Incidencias (retrabajos, problemas, cumplimiento)
- Puntualidad y asistencia

#### D. Rating & Reputation System
- Calificación general (promedio de todos los proyectos)
- Dimensiones de evaluación:
  * **Calidad de Trabajo** (acabado, adherencia, uniformidad)
  * **Puntualidad** (llegada a obra, cumplimiento de cronograma)
  * **Seguimiento de Instrucciones** (normas técnicas, supervisión)
  * **Seguridad** (uso de EPP, cumplimiento de protocolos)
  * **Profesionalismo** (trato con cliente, presentación)
- Nivel de confiabilidad: Nuevo / En Prueba / Confiable / Preferido / Top Performer

#### E. Availability & Scheduling
- Estado actual: Disponible / Ocupado / Fuera de servicio
- Calendario de disponibilidad (próximos 30/60/90 días)
- Zonas de cobertura (distritos/provincias donde trabaja)
- Restricciones (no trabaja fines de semana, solo medio tiempo, etc.)

#### F. Rate Management
- Tarifa base por m² (por producto)
- Tarifa por día completo
- Recargos especiales:
  * Trabajo nocturno (+30%)
  * Fines de semana (+40%)
  * Alturas >3m (+20%)
  * Provincias (transporte + viáticos)
- Forma de pago preferida (efectivo, transferencia, depósito)
- Historial de pagos realizados

#### G. Contact & Communication
- Teléfono principal (WhatsApp preferido)
- Email
- Contacto de emergencia
- Última fecha de contacto
- Canal de comunicación preferido
- Historial de llamadas/mensajes

#### H. Search & Filter
- Buscar por:
  * Ubicación geográfica
  * Producto específico (ej: solo expertos en poliurea)
  * Disponibilidad en fecha específica
  * Calificación mínima (ej: solo 4+ estrellas)
  * Tarifa máxima
  * Nivel de experiencia
- Ordenar por: Rating / Tarifa / Proyectos completados / Último contacto

### 2.2 Non-Functional Requirements

#### Performance
- Tiempo de búsqueda < 2 segundos
- Carga de perfil completo < 1 segundo
- Soporte para 100-500 freelancers registrados

#### Usability
- Interfaz simple, no requiere capacitación
- Accesible desde celular (campo) y escritorio (oficina)
- Exportación a Excel para reportes

#### Security
- Backup automático diario
- Información personal protegida (GDPR compliance)
- Solo personal autorizado de LUX tiene acceso

#### Reliability
- Disponibilidad 99% (permite trabajar offline)
- Sincronización cuando hay conexión

---

## III. DATABASE SCHEMA DESIGN

### Tables Structure

#### 1. **freelancers** (Información Principal)
```sql
CREATE TABLE freelancers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni VARCHAR(8) UNIQUE NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    whatsapp VARCHAR(15),
    email VARCHAR(100),
    direccion TEXT,
    distrito VARCHAR(50),
    provincia VARCHAR(50),
    fecha_nacimiento DATE,
    contacto_emergencia VARCHAR(100),
    telefono_emergencia VARCHAR(15),
    foto_perfil_path VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'Activo', -- Activo, Inactivo, Suspendido
    nivel_confiabilidad VARCHAR(20) DEFAULT 'Nuevo', -- Nuevo, En Prueba, Confiable, Preferido, Top Performer
    rating_general DECIMAL(3,2) DEFAULT 0.00,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. **skills** (Habilidades Técnicas)
```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    categoria VARCHAR(50) NOT NULL, -- Producto, Técnica, Equipo, Preparación
    skill_nombre VARCHAR(100) NOT NULL,
    nivel_competencia VARCHAR(20), -- Aprendiz, Intermedio, Experto, Master
    certificado BOOLEAN DEFAULT 0,
    fecha_certificacion DATE,
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

#### 3. **trainings** (Capacitaciones)
```sql
CREATE TABLE trainings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    titulo_capacitacion VARCHAR(200) NOT NULL,
    producto VARCHAR(50), -- JP01Y, JS02Y, 1002A, etc.
    instructor VARCHAR(100),
    fecha DATE NOT NULL,
    duracion_horas DECIMAL(4,1),
    calificacion_obtenida VARCHAR(20), -- Aprobado, Sobresaliente, etc.
    certificado_path VARCHAR(255),
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

#### 4. **projects** (Proyectos Ejecutados)
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_proyecto VARCHAR(50) UNIQUE,
    nombre_proyecto VARCHAR(200) NOT NULL,
    cliente VARCHAR(200),
    ubicacion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    metros_cuadrados DECIMAL(10,2),
    producto_principal VARCHAR(50),
    tipo_trabajo VARCHAR(100), -- Piso industrial, impermeabilización, etc.
    supervisor VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'Planificado', -- Planificado, En Ejecución, Completado, Cancelado
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. **project_assignments** (Asignaciones a Proyectos)
```sql
CREATE TABLE project_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    freelancer_id INTEGER NOT NULL,
    rol VARCHAR(50), -- Aplicador Principal, Ayudante, Preparador
    fecha_asignacion DATE DEFAULT CURRENT_DATE,
    m2_asignados DECIMAL(10,2),
    tarifa_acordada DECIMAL(10,2),
    unidad_tarifa VARCHAR(20), -- por m², por día, monto fijo
    dias_trabajados INTEGER DEFAULT 0,
    m2_completados DECIMAL(10,2) DEFAULT 0,
    monto_total DECIMAL(10,2),
    fecha_pago DATE,
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(20) DEFAULT 'Pendiente', -- Pendiente, Pagado, Parcial
    notas TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

#### 6. **ratings** (Calificaciones por Proyecto)
```sql
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    calidad_trabajo INTEGER CHECK(calidad_trabajo BETWEEN 1 AND 5),
    puntualidad INTEGER CHECK(puntualidad BETWEEN 1 AND 5),
    seguimiento_instrucciones INTEGER CHECK(seguimiento_instrucciones BETWEEN 1 AND 5),
    seguridad INTEGER CHECK(seguridad BETWEEN 1 AND 5),
    profesionalismo INTEGER CHECK(profesionalismo BETWEEN 1 AND 5),
    rating_general DECIMAL(3,2),
    comentarios TEXT,
    evaluador VARCHAR(100),
    fecha_evaluacion DATE DEFAULT CURRENT_DATE,
    recomendaria BOOLEAN,
    FOREIGN KEY (assignment_id) REFERENCES project_assignments(id) ON DELETE CASCADE
);
```

#### 7. **availability** (Disponibilidad)
```sql
CREATE TABLE availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'Disponible', -- Disponible, Ocupado, Fuera de servicio
    proyecto_asignado INTEGER,
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_asignado) REFERENCES projects(id) ON DELETE SET NULL,
    UNIQUE(freelancer_id, fecha)
);
```

#### 8. **rates** (Tarifas)
```sql
CREATE TABLE rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    tipo_trabajo VARCHAR(100), -- Aplicación piso, impermeabilización, etc.
    producto VARCHAR(50), -- JP01Y, epóxico, etc.
    tarifa_m2 DECIMAL(10,2),
    tarifa_dia DECIMAL(10,2),
    tarifa_minima DECIMAL(10,2), -- Monto mínimo por proyecto pequeño
    recargo_nocturno_pct DECIMAL(5,2) DEFAULT 30.00,
    recargo_fin_semana_pct DECIMAL(5,2) DEFAULT 40.00,
    recargo_altura_pct DECIMAL(5,2) DEFAULT 20.00,
    incluye_herramientas BOOLEAN DEFAULT 0,
    incluye_transporte BOOLEAN DEFAULT 0,
    zona_cobertura TEXT, -- Lima Norte, Lima Sur, Callao, etc.
    vigencia_desde DATE DEFAULT CURRENT_DATE,
    vigencia_hasta DATE,
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

#### 9. **documents** (Documentos)
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    tipo_documento VARCHAR(50), -- CV, Certificado, SCTR, Contrato, etc.
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    fecha_subida DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE,
    estado VARCHAR(20) DEFAULT 'Vigente', -- Vigente, Por vencer, Vencido
    notas TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

#### 10. **communication_log** (Historial de Comunicación)
```sql
CREATE TABLE communication_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freelancer_id INTEGER NOT NULL,
    fecha_contacto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_contacto VARCHAR(20), -- Llamada, WhatsApp, Email, Presencial
    motivo VARCHAR(100), -- Consulta disponibilidad, Coordinación proyecto, Seguimiento
    resumen TEXT,
    proximo_seguimiento DATE,
    usuario_lux VARCHAR(100),
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
);
```

---

## IV. SYSTEM ARCHITECTURE

### 4.1 Technology Stack Options

#### Option A: Web Application (Recommended for Multi-User)
- **Frontend**: React/Vue.js + Tailwind CSS
- **Backend**: Python Flask/FastAPI or Node.js Express
- **Database**: PostgreSQL (production) or SQLite (MVP)
- **Hosting**: Heroku, Railway, Render (low cost)
- **Mobile**: Responsive web (works on phone browser)

**Pros**: Accessible from anywhere, multi-user, automatic updates
**Cons**: Requires internet, monthly hosting cost (~$10-20)

#### Option B: Desktop Application (Simpler Start)
- **Framework**: Python + Streamlit or Tkinter
- **Database**: SQLite (local file)
- **Deployment**: Executable for Windows

**Pros**: No hosting costs, works offline, simple to develop
**Cons**: Single user, manual updates, no remote access

#### Option C: Hybrid (Best of Both)
- **Start**: Streamlit + SQLite (MVP, 2-3 weeks)
- **Migrate**: Cloud database when needed
- **Mobile**: Progressive Web App (PWA)

### 4.2 Core Features by Phase

#### Phase 1 - MVP (2-3 weeks)
1. Freelancer CRUD (Create, Read, Update, Delete)
2. Basic search and filter
3. Project assignment tracking
4. Simple rating system (1-5 stars)
5. Contact information management

#### Phase 2 - Enhanced (1 month)
6. Availability calendar
7. Training/certification tracking
8. Rate management
9. Document upload/storage
10. Advanced search with multiple filters

#### Phase 3 - Advanced (2 months)
11. Dashboard with KPIs (freelancers disponibles, proyectos activos)
12. Communication log
13. Automated reminders (SCTR vencido, seguimiento)
14. Reporting and analytics
15. Mobile-optimized interface

#### Phase 4 - Integration (Future)
16. WhatsApp integration for notifications
17. Payment tracking integration
18. Photo gallery of work samples
19. Map view of freelancer locations
20. Automated scheduling optimization

---

## V. KEY FEATURES DETAIL

### 5.1 Smart Search Engine

**Search Scenarios:**

**Scenario 1: "Necesito aplicador de poliurea para mañana en San Juan de Lurigancho"**
- Filter: Producto = "JP01Y" OR "Poliurea"
- Filter: Zona = "Lima Este" OR "San Juan de Lurigancho"
- Filter: Disponibilidad = "2026-01-14"
- Sort: Rating desc
- Result: Lista de 3-5 candidatos con rating, tarifa, última experiencia

**Scenario 2: "Proyecto grande 500m² epóxico, necesito equipo de 3 personas en Callao, 5 días"**
- Filter: Producto = "Epóxico"
- Filter: Zona = "Callao"
- Filter: Disponibilidad = "2026-01-15 a 2026-01-19" (5 días consecutivos)
- Filter: Rating >= 4.0 (solo confiables)
- Sort: Experiencia (m² completados) desc
- Result: Top 10 aplicadores, sugerir el equipo óptimo

### 5.2 Rating System Detail

**Evaluation Form After Each Project:**

```
Proyecto: [Nombre] - [Cliente]
Freelancer: [Nombre]
Evaluador: [Supervisor LUX]

Calidad de Trabajo (1-5): [___]
- ¿El acabado cumple con estándares LUX?
- ¿Hay adherencia correcta?
- ¿Espesor uniforme?

Puntualidad (1-5): [___]
- ¿Llegó a tiempo todos los días?
- ¿Respetó el cronograma?

Seguimiento de Instrucciones (1-5): [___]
- ¿Siguió procedimientos técnicos?
- ¿Aceptó supervisión?

Seguridad (1-5): [___]
- ¿Usó EPP completo?
- ¿Siguió protocolos de seguridad?

Profesionalismo (1-5): [___]
- ¿Trato adecuado con cliente?
- ¿Presentación personal?

Comentarios: [_________________]

¿Recomendarías este freelancer para futuros proyectos? [Sí / No]

¿Hubo algún incidente o retrabajo? [Descripción]
```

### 5.3 Availability Calendar

**Visual Interface:**
- Monthly view with color coding:
  * Verde: Disponible
  * Amarillo: Preferencia no trabajar (pero puede si es necesario)
  * Rojo: Ocupado (proyecto asignado)
  * Gris: Fuera de servicio (vacaciones, enfermedad)

**Quick Actions:**
- Block dates (vacaciones programadas)
- Mark available for urgent calls
- See all projects scheduled

### 5.4 Rate Calculator

**Example Calculation:**

```
Proyecto: 200m² piso industrial JP01Y
Ubicación: Ate (Lima Este)
Fecha: Sábado (fin de semana)
Altura: <3m

Freelancer: Juan Pérez
- Tarifa base JP01Y: S/. 15/m²
- Recargo fin de semana: +40%
- Zona cobertura: Lima Este (sin recargo transporte)

Cálculo:
Base: 200m² × S/. 15 = S/. 3,000
Recargo FdS: S/. 3,000 × 40% = S/. 1,200
Total: S/. 4,200

Tiempo estimado: 2 días
Tarifa efectiva: S/. 21/m²
```

---

## VI. MVP SPECIFICATIONS

### Minimum Viable Product (2-3 weeks development)

#### Core Features:
1. **Freelancer Database**
   - Add/Edit/Delete freelancers
   - Basic info: nombre, DNI, teléfono, email, dirección
   - Skills list (text field, comma separated)
   - Rating (1-5 stars, manual input)

2. **Simple Search**
   - Search by name
   - Filter by skill
   - Filter by rating (>= X stars)
   - Sort by rating or name

3. **Project Tracking**
   - Create project
   - Assign freelancers to project
   - Record: fecha, m², producto, pago
   - Mark project complete

4. **Rating Entry**
   - After project, rate freelancer
   - 5 categories × 1-5 stars
   - Comments field
   - Auto-calculate average

5. **Contact Management**
   - View contact details
   - Log last contact date
   - Quick WhatsApp link

#### Tech Stack for MVP:
- Python + Streamlit (web interface)
- SQLite database (local file)
- Pandas (data manipulation)
- Deployment: Streamlit Cloud (free) or local

#### Data Entry:
- Manual entry initially
- Import from Excel (batch upload)

---

## VII. IMPLEMENTATION ROADMAP

### Week 1-2: MVP Development
- [ ] Set up database schema (SQLite)
- [ ] Create Streamlit app structure
- [ ] Implement freelancer CRUD
- [ ] Basic search and filter
- [ ] Project assignment module
- [ ] Rating system

### Week 3-4: Testing & Initial Data
- [ ] Test with 10-15 sample freelancers
- [ ] Import existing contacts (if any)
- [ ] User testing with LUX team
- [ ] Refinements based on feedback

### Month 2: Enhanced Features
- [ ] Availability calendar
- [ ] Rate management
- [ ] Document upload
- [ ] Advanced search
- [ ] Export to Excel

### Month 3: Polish & Scale
- [ ] Dashboard and KPIs
- [ ] Communication log
- [ ] Mobile optimization
- [ ] Training materials
- [ ] Onboard 50+ freelancers

### Month 4+: Advanced Features
- [ ] WhatsApp integration
- [ ] Photo gallery
- [ ] Analytics and reporting
- [ ] Scheduling optimization
- [ ] Payment integration

---

## VIII. SUCCESS METRICS

### KPIs to Track:

1. **Network Size**
   - Total freelancers registered
   - Active freelancers (worked in last 90 days)
   - Top performers (rating >= 4.5)

2. **Project Coverage**
   - % of projects covered by network
   - Average response time (hours to confirm freelancer)
   - Geographic coverage (distritos covered)

3. **Quality**
   - Average rating across all projects
   - % projects with rating >= 4.0
   - Retrabajo rate

4. **Economics**
   - Average cost per m² (freelance vs. permanent)
   - Payment turnaround time
   - Cost savings vs. hiring full-time

5. **Efficiency**
   - Time to find freelancer (from request to confirmed)
   - Utilization rate (days worked / days available)
   - Repeat hire rate (same freelancer multiple projects)

---

## IX. RISK MITIGATION

### Risks & Solutions:

| Risk | Mitigation Strategy |
|------|---------------------|
| Low quality work | Rating system, probation period for new freelancers, supervisor verification |
| No-shows | Backup list, require confirmation 24h before, penalty system |
| Safety incidents | Mandatory SCTR, safety training, PPE verification checklist |
| Price inflation | Fixed rates in system, annual review, competitive benchmarking |
| Data loss | Daily backups, cloud storage, redundant copies |
| Freelancer poaching | Non-compete clause (optional), value relationship over just price |
| Inconsistent availability | Maintain 3X freelancers vs. concurrent project needs |
| Communication failures | WhatsApp integration, automatic reminders, confirmation system |

---

## X. NEXT STEPS

### Immediate Actions (This Week):

1. **Validate Concept**
   - [ ] Review this document with LUX team
   - [ ] Identify 5-10 current freelancers to start database
   - [ ] Confirm must-have vs. nice-to-have features

2. **Prepare Data**
   - [ ] Gather existing freelancer contacts (Excel, phone, notes)
   - [ ] List current skills/products needed most
   - [ ] Define initial rate ranges per product

3. **Start MVP Development**
   - [ ] Set up development environment
   - [ ] Create database schema
   - [ ] Build first Streamlit prototype (freelancer list)

### Decision Points:

- **Platform choice**: Desktop (Streamlit local) or Web (Streamlit Cloud)?
- **Starting scope**: MVP only or add Phase 2 features?
- **Data migration**: Import existing contacts or start fresh?
- **Access**: Single user (Adolfo) or multi-user (team)?

---

## APPENDIX A: Sample Data Structure

### Example Freelancer Profile:

```json
{
  "id": 1,
  "dni": "12345678",
  "nombre_completo": "Juan Carlos Pérez Gonzales",
  "telefono": "987654321",
  "whatsapp": "987654321",
  "email": "jperez@email.com",
  "direccion": "Av. Los Próceres 123, San Juan de Lurigancho",
  "distrito": "San Juan de Lurigancho",
  "provincia": "Lima",
  "nivel_confiabilidad": "Confiable",
  "rating_general": 4.5,
  "estado": "Activo",
  
  "skills": [
    {"categoria": "Producto", "skill": "JP01Y Poliurea", "nivel": "Experto"},
    {"categoria": "Producto", "skill": "Epóxico 1002A", "nivel": "Intermedio"},
    {"categoria": "Técnica", "skill": "Aplicación con rodillo", "nivel": "Experto"},
    {"categoria": "Técnica", "skill": "Aplicación con spray", "nivel": "Aprendiz"}
  ],
  
  "trainings": [
    {
      "titulo": "Certificación JP01Y - Aplicación Poliurea",
      "producto": "JP01Y",
      "fecha": "2025-03-15",
      "duracion_horas": 8,
      "instructor": "LUX Technical Team"
    }
  ],
  
  "projects_completed": 12,
  "m2_totales": 3450,
  "ultima_fecha_trabajo": "2025-12-10",
  
  "rates": {
    "JP01Y": {"tarifa_m2": 15, "incluye_herramientas": true},
    "Epóxico": {"tarifa_m2": 12, "incluye_herramientas": true},
    "tarifa_dia": 250
  },
  
  "availability_next_week": "Disponible Lun-Vie, Ocupado Sab-Dom",
  "zona_cobertura": ["Lima Este", "Lima Centro", "Ate", "Santa Anita"]
}
```

---

## APPENDIX B: User Interface Mockup Ideas

### Dashboard View:
```
+----------------------------------------------------------+
| 🏠 FAMS - Freelance Applicator Management System         |
+----------------------------------------------------------+
| 📊 DASHBOARD                                             |
|                                                          |
| [50] Total Freelancers    [28] Disponibles Hoy         |
| [12] En Proyecto          [4.3⭐] Rating Promedio      |
|                                                          |
| 🔍 BÚSQUEDA RÁPIDA                                      |
| Buscar por nombre: [___________________] [🔍 Buscar]    |
|                                                          |
| Filtros:                                                 |
| Producto: [Todos ▼]  Zona: [Todos ▼]  Rating: [>=4 ▼] |
| Disponibilidad: [Hoy ▼]                   [Filtrar]    |
|                                                          |
| 📋 RESULTADOS (15 freelancers)                          |
| ┌─────────────────────────────────────────────────────┐|
| │ Juan Pérez | ⭐4.5 | JP01Y, Epóxico | Lima Este   │|
| │ Tel: 987-654-321 | Disponible | S/.15/m²          │|
| │ [Ver Perfil] [Asignar a Proyecto] [Contactar]     │|
| ├─────────────────────────────────────────────────────┤|
| │ María López | ⭐4.8 | Poliurea | Callao          │|
| │ Tel: 912-345-678 | Ocupada hasta 15/01 | S/.18/m²│|
| │ [Ver Perfil] [Ver Calendario] [Contactar]          │|
| └─────────────────────────────────────────────────────┘|
|                                                          |
| [+ Agregar Nuevo Freelancer] [📊 Reportes] [⚙️ Config] |
+----------------------------------------------------------+
```

---

**FIN DEL DOCUMENTO**

¿Deseas proceder con el desarrollo del MVP o prefieres ajustar el diseño primero?
