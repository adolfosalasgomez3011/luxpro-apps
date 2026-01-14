"""
LuxPro Aplicadores - Portal de Oportunidades
Plataforma para aplicadores de pisos poliméricos
Version: 2.0 - Public Access
"""
import streamlit as st
import database_supabase as db
from datetime import datetime
from PIL import Image

# Page config
st.set_page_config(
    page_title="LuxPro - Oportunidades",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS - LUX Brand Colors (Mobile-First)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%) !important;
    }
    
    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    p, div, span, label {
        color: #94a3b8 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.875rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(249,115,22,0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button * {
        color: white !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%) !important;
        box-shadow: 0 6px 20px rgba(249,115,22,0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(249,115,22,0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 3px rgba(249,115,22,0.2) !important;
    }
    
    .job-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(249,115,22,0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .job-card:hover {
        border-color: #f97316;
        background: rgba(249,115,22,0.1);
    }
    
    .badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-available {
        background: rgba(34,197,94,0.2);
        color: #22c55e;
        border: 1px solid rgba(34,197,94,0.4);
    }
    
    .badge-urgent {
        background: rgba(239,68,68,0.2);
        color: #ef4444;
        border: 1px solid rgba(239,68,68,0.4);
    }
    
    /* Form submit button specific */
    .stForm button[type="submit"] {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    }
    
    .stForm button[type="submit"]:hover {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
    }
    
    /* Animated Registration CTA */
    .register-cta {
        background: linear-gradient(135deg, rgba(249,115,22,0.2) 0%, rgba(234,88,12,0.15) 100%);
        border: 2px solid #f97316;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite;
        box-shadow: 0 8px 32px rgba(249,115,22,0.4), 0 0 20px rgba(249,115,22,0.3);
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 8px 32px rgba(249,115,22,0.4), 0 0 20px rgba(249,115,22,0.3);
            border-color: #f97316;
        }
        50% {
            box-shadow: 0 12px 48px rgba(249,115,22,0.6), 0 0 40px rgba(249,115,22,0.5);
            border-color: #fb923c;
        }
    }
    
    .register-cta h3 {
        font-size: 1.75rem !important;
        margin-bottom: 0.75rem !important;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .register-cta-button {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load LUX Logo
try:
    logo = Image.open("assets/logo.png")
except:
    logo = None

# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'opportunities'

def show_header():
    """Show logo and header"""
    if logo:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(logo, width=80)
        with col2:
            st.markdown("<h2 style='margin-top:0.5rem;'>Portal de Oportunidades</h2>", unsafe_allow_html=True)
            st.caption("Encuentra trabajos de aplicación de pisos")
    else:
        st.markdown("<h2>Portal de Oportunidades LUX</h2>", unsafe_allow_html=True)
        st.caption("Encuentra trabajos de aplicación de pisos")

def show_opportunities():
    """Show available job opportunities"""
    show_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Registration CTA - Prominent at top
    st.markdown("""
    <div class="register-cta">
        <h3>🌟 ¡Únete al Equipo LUX! 🌟</h3>
        <p style="color:#e2e8f0;font-size:1.1rem;margin-bottom:0;">Regístrate ahora y accede a las mejores oportunidades de trabajo</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("📝 REGISTRARME AHORA", key="top_register", use_container_width=True):
            st.session_state.view = 'register'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter section
    col1, col2 = st.columns(2)
    with col1:
        ciudad = st.selectbox("Ciudad", ["Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo"])
    with col2:
        if ciudad == "Lima":
            distritos = ["Todos", "Villa El Salvador", "San Juan de Miraflores", "Ate", "Los Olivos", "Callao", "Surco", "Miraflores", "Chorrillos"]
        else:
            distritos = ["Todos"]
        distrito = st.selectbox("Distrito", distritos)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mock job opportunities (in production, fetch from jobs table)
    jobs = [
        {
            "titulo": "Aplicación de Epóxico Industrial",
            "distrito": "Villa El Salvador",
            "fecha": "18 Enero 2026",
            "vacantes": 3,
            "tipo": "Epóxico",
            "urgente": True
        },
        {
            "titulo": "Poliaspártico en Almacén",
            "distrito": "Ate",
            "fecha": "22 Enero 2026",
            "vacantes": 2,
            "tipo": "Poliaspártico",
            "urgente": False
        },
        {
            "titulo": "Microcemento Residencial",
            "distrito": "Surco",
            "fecha": "25 Enero 2026",
            "vacantes": 1,
            "tipo": "Microcemento",
            "urgente": False
        },
        {
            "titulo": "Epóxico Decorativo - Centro Comercial",
            "distrito": "San Juan de Miraflores",
            "fecha": "20 Enero 2026",
            "vacantes": 4,
            "tipo": "Epóxico",
            "urgente": True
        },
        {
            "titulo": "Piso de Resina para Estacionamiento",
            "distrito": "Miraflores",
            "fecha": "28 Enero 2026",
            "vacantes": 2,
            "tipo": "Resina",
            "urgente": False
        }
    ]
    
    # Filter jobs by district
    if distrito != "Todos":
        filtered_jobs = [j for j in jobs if j["distrito"] == distrito]
    else:
        filtered_jobs = jobs
    
    st.markdown(f"<h3>{len(filtered_jobs)} Oportunidades Disponibles</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display jobs
    for job in filtered_jobs:
        urgente_badge = '<span class="badge badge-urgent">⚡ URGENTE</span>' if job["urgente"] else ''
        available_badge = f'<span class="badge badge-available">✓ {job["vacantes"]} Vacantes</span>'
        
        st.markdown(f"""
        <div class="job-card">
            <h3 style="color:#e2e8f0;margin-bottom:0.5rem;">{job["titulo"]}</h3>
            <p style="color:#94a3b8;margin-bottom:1rem;">📍 {job["distrito"]} • 📅 {job["fecha"]}</p>
            <div style="margin-bottom:1rem;">
                {urgente_badge}
                {available_badge}
                <span class="badge" style="background:rgba(234,179,8,0.2);color:#eab308;border:1px solid rgba(234,179,8,0.4);">🔧 {job["tipo"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📋 Ver Detalles", key=f"details_{jobs.index(job)}", use_container_width=True):
                st.info(f"**Descripción:** Proyecto de {job['tipo']} en {job['distrito']}\n\n**Fecha:** {job['fecha']}\n\n**Vacantes:** {job['vacantes']} aplicadores necesarios\n\n**Contacto:** Regístrate para recibir más información")
        with col2:
            if st.button("✅ Postular", key=f"apply_{jobs.index(job)}", use_container_width=True):
                st.session_state.view = 'register'
                st.session_state.selected_job = job["titulo"]
                st.rerun()

def show_register():
    """Simple registration form for aplicadores"""
    show_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Registro de Aplicador</h3>", unsafe_allow_html=True)
    st.caption("Completa tus datos para postular a trabajos")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("registro_form"):
        nombre = st.text_input("Nombre Completo *", placeholder="Ej: Juan Pérez García")
        
        col1, col2 = st.columns(2)
        with col1:
            telefono = st.text_input("WhatsApp / Teléfono *", placeholder="987654321")
        with col2:
            dni = st.text_input("DNI / Carnet de Extranjería *", placeholder="12345678")
        
        col1, col2 = st.columns(2)
        with col1:
            ciudad = st.selectbox("Ciudad de Residencia *", ["Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Otra"])
        with col2:
            if ciudad == "Lima":
                distrito = st.selectbox("Distrito *", ["Villa El Salvador", "San Juan de Miraflores", "Ate", "Los Olivos", "Callao", "Surco", "Miraflores", "Chorrillos", "Otro"])
            else:
                distrito = st.text_input("Distrito *")
        
        email = st.text_input("Email (opcional)", placeholder="ejemplo@email.com")
        
        skills = st.text_input("Especialidades (Opcional)", placeholder="Ej: Epóxico, Poliaspártico, Microcemento")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("✅ Registrarme", use_container_width=True)
        
        if submitted:
            if nombre and telefono and dni and distrito:
                try:
                    # Create new freelancer in database
                    new_freelancer = {
                        'nombre': nombre,
                        'telefono': telefono,
                        'email': email if email else None,
                        'dni': dni,
                        'distrito': distrito if distrito != "Otro" else ciudad,
                        'skills': skills if skills else None,
                        'disponible': True,
                        'rating_promedio': 5.0,
                        'notas': 'Registrado desde Portal de Aplicadores'
                    }
                    
                    db.add_freelancer(new_freelancer)
                    
                    st.success("✅ ¡Registro exitoso! Te contactaremos pronto para asignarte trabajos.")
                    st.balloons()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔙 Ver Oportunidades"):
                        st.session_state.view = 'opportunities'
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Error al registrar: {e}")
            else:
                st.warning("⚠️ Por favor completa todos los campos obligatorios (*)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 Volver a Oportunidades"):
        st.session_state.view = 'opportunities'
        st.rerun()

# Main app routing
if st.session_state.view == 'opportunities':
    show_opportunities()
elif st.session_state.view == 'register':
    show_register()
