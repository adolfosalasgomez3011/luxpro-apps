"""
Database initialization and operations for FAMS (Freelance Applicator Management System)
"""
import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'fams.db')

def init_database():
    """Initialize database with schema"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Freelancers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS freelancers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni VARCHAR(8) UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            telefono VARCHAR(15) NOT NULL,
            email VARCHAR(100),
            distrito VARCHAR(50),
            foto_path VARCHAR(255),
            skills TEXT,
            rating_promedio DECIMAL(3,2) DEFAULT 0,
            estado VARCHAR(20) DEFAULT 'Activo',
            disponible BOOLEAN DEFAULT 1,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
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
        )
    ''')
    
    # 3. Assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
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
        )
    ''')
    
    # 4. Ratings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
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
        )
    ''')
    
    # 5. Contact log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            freelancer_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo VARCHAR(20),
            notas TEXT,
            FOREIGN KEY (freelancer_id) REFERENCES freelancers(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized at: {DB_PATH}")

def insert_sample_data():
    """Insert sample freelancers for testing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sample_freelancers = [
        ('12345678', 'Juan Carlos Pérez', '987654321', 'jperez@email.com', 'San Juan de Lurigancho', None, 'JP01Y, Epóxico, Rodillo', 4.5, 'Activo', 1, 'Muy confiable, trabaja hace 2 años'),
        ('23456789', 'María López Gonzales', '912345678', 'mlopez@email.com', 'Callao', None, 'Poliurea, Spray, JP02R', 4.8, 'Activo', 0, 'Especialista en impermeabilización'),
        ('34567890', 'Carlos Ramírez', '998877665', 'cramirez@email.com', 'Ate', None, 'Epóxico, JP01Y, Preparación superficie', 4.2, 'Activo', 1, 'Bueno para proyectos grandes'),
        ('45678901', 'Ana Torres', '987123456', 'atorres@email.com', 'Villa El Salvador', None, 'JS02Y, Poliaspártico, Rodillo', 4.6, 'Activo', 1, 'Excelente acabado, puntual'),
        ('56789012', 'Roberto Silva', '965432109', 'rsilva@email.com', 'San Martín de Porres', None, 'Epóxico, Preparación, Lijado', 3.9, 'Activo', 1, 'En capacitación, mejorando'),
        ('67890123', 'Patricia Vargas', '923456789', 'pvargas@email.com', 'Surco', None, 'Poliurea, JP01Y, Spray', 4.7, 'Activo', 0, 'Proyecto grande hasta 20/01'),
        ('78901234', 'Luis Mendoza', '945678901', 'lmendoza@email.com', 'Los Olivos', None, 'Epóxico, 1002A, Rodillo', 4.4, 'Activo', 1, 'Especialista en talleres automotrices'),
        ('89012345', 'Rosa Fernández', '978901234', 'rfernandez@email.com', 'Chorrillos', None, 'JS02Y, Poliurea, Preparación', 4.3, 'Activo', 1, 'Buena para zonas costeras'),
        ('90123456', 'Miguel Castro', '912567890', 'mcastro@email.com', 'Independencia', None, 'Epóxico, JP01Y, Brocha', 3.8, 'Activo', 1, 'Nuevo, necesita supervisión'),
        ('01234567', 'Sandra Ruiz', '987654123', 'sruiz@email.com', 'Breña', None, 'Poliurea, Impermeabilización, JP02R', 4.9, 'Activo', 1, 'Top performer, muy recomendada')
    ]
    
    try:
        cursor.executemany('''
            INSERT INTO freelancers (dni, nombre, telefono, email, distrito, foto_path, skills, rating_promedio, estado, disponible, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_freelancers)
        
        conn.commit()
        print(f"✅ Inserted {len(sample_freelancers)} sample freelancers")
    except sqlite3.IntegrityError:
        print("⚠️ Sample data already exists, skipping...")
    finally:
        conn.close()

# CRUD Operations

def get_all_freelancers(search_term: str = "", skill_filter: str = "", distrito_filter: str = "") -> List[Dict]:
    """Get all freelancers with optional filters"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM freelancers WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND nombre LIKE ?"
        params.append(f"%{search_term}%")
    
    if skill_filter:
        query += " AND skills LIKE ?"
        params.append(f"%{skill_filter}%")
    
    if distrito_filter:
        query += " AND distrito = ?"
        params.append(distrito_filter)
    
    query += " ORDER BY rating_promedio DESC, nombre"
    
    cursor.execute(query, params)
    freelancers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return freelancers

def get_freelancer_by_id(freelancer_id: int) -> Optional[Dict]:
    """Get single freelancer by ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM freelancers WHERE id = ?", (freelancer_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

def add_freelancer(data: Dict) -> int:
    """Add new freelancer"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO freelancers (dni, nombre, telefono, email, distrito, skills, rating_promedio, disponible, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('dni'),
        data['nombre'],
        data['telefono'],
        data.get('email'),
        data.get('distrito'),
        data.get('skills'),
        data.get('rating_promedio', 0),
        data.get('disponible', 1),
        data.get('notas')
    ))
    
    freelancer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return freelancer_id

def update_freelancer(freelancer_id: int, data: Dict):
    """Update existing freelancer"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE freelancers
        SET dni = ?, nombre = ?, telefono = ?, email = ?, distrito = ?, 
            skills = ?, rating_promedio = ?, disponible = ?, notas = ?
        WHERE id = ?
    ''', (
        data.get('dni'),
        data['nombre'],
        data['telefono'],
        data.get('email'),
        data.get('distrito'),
        data.get('skills'),
        data.get('rating_promedio', 0),
        data.get('disponible', 1),
        data.get('notas'),
        freelancer_id
    ))
    
    conn.commit()
    conn.close()

def delete_freelancer(freelancer_id: int):
    """Delete freelancer"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM freelancers WHERE id = ?", (freelancer_id,))
    
    conn.commit()
    conn.close()

def get_stats() -> Dict:
    """Get dashboard statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total freelancers
    cursor.execute("SELECT COUNT(*) FROM freelancers WHERE estado = 'Activo'")
    total = cursor.fetchone()[0]
    
    # Available today
    cursor.execute("SELECT COUNT(*) FROM freelancers WHERE estado = 'Activo' AND disponible = 1")
    disponibles = cursor.fetchone()[0]
    
    # In project
    en_proyecto = total - disponibles
    
    # Average rating
    cursor.execute("SELECT AVG(rating_promedio) FROM freelancers WHERE estado = 'Activo'")
    avg_rating = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total': total,
        'disponibles': disponibles,
        'en_proyecto': en_proyecto,
        'avg_rating': round(avg_rating, 1)
    }

def log_contact(freelancer_id: int, tipo: str, notas: str = ""):
    """Log contact with freelancer"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO contact_log (freelancer_id, tipo, notas)
        VALUES (?, ?, ?)
    ''', (freelancer_id, tipo, notas))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("🔧 Initializing FAMS Database...")
    init_database()
    insert_sample_data()
    print("✅ Database ready!")
