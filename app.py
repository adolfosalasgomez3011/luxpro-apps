"""
LuxPro - Plataforma de Gestión de Aplicadores LUX
Sistema de gestión para contratistas especializados en pisos poliméricos
Version: 3.0 - LUX Brand
"""
import streamlit as st
import database_supabase as db
from datetime import datetime
from PIL import Image

# Page config
st.set_page_config(
    page_title="LuxPro - Gestión de Aplicadores",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS - LUX Brand Colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Hide defaults */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* LUX Brand Background - Dark gradient to show white logo */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%) !important;
    }
    
    /* Container */
    .block-container {
        padding: 1.5rem 1rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Logo Header */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .logo-container img {
        height: 50px;
        width: auto;
    }
    
    /* Typography - Light colors for dark background */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        margin-bottom: 0.75rem !important;
    }
    
    h3 {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }
    
    p, div, span, label {
        color: #94a3b8 !important;
        font-size: 0.9375rem !important;
        line-height: 1.6 !important;
    }
    
    .stCaption {
        color: #64748b !important;
        font-size: 0.8125rem !important;
    }
    
    /* Primary Buttons - LUX Orange/Amber */
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(249,115,22,0.3) !important;
    }
    
    .stButton > button * {
        color: white !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%) !important;
        box-shadow: 0 4px 16px rgba(249,115,22,0.5) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Inputs - Dark theme */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 0.625rem !important;
        background: rgba(255,255,255,0.05) !important;
        color: #e2e8f0 !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 3px rgba(249,115,22,0.2) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    
    /* Info/Success Boxes - Dark theme */
    .stInfo, .stSuccess {
        background: rgba(249,115,22,0.1) !important;
        border: 1px solid rgba(249,115,22,0.3) !important;
        border-left: 4px solid #f97316 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #e2e8f0 !important;
    }
    
    .stInfo p, .stSuccess p, .stInfo div, .stSuccess div {
        color: #e2e8f0 !important;
    }
    
    /* Expander Fix - Dark theme */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stExpander"] summary {
        padding: 0.75rem 1rem !important;
        color: #e2e8f0 !important;
    }
    
    [data-testid="stExpander"] summary p {
        display: inline-block !important;
        margin-left: 0.5rem !important;
        color: #e2e8f0 !important;
    }
    
    /* Hide broken Material icon text */
    [data-testid="stExpander"] [data-testid="stIconMaterial"] {
        font-size: 0 !important;
        width: 20px !important;
        height: 20px !important;
        color: #f97316 !important;
    }
    
    [data-testid="stExpander"] [data-testid="stIconMaterial"]::before {
        content: "▼" !important;
        font-size: 12px !important;
        display: inline-block !important;
        color: #f97316 !important;
    }
    
    [data-testid="stExpander"][open] [data-testid="stIconMaterial"]::before {
        content: "▲" !important;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        border-top: 1px solid #e5e7eb !important;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.75rem !important;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.25rem !important;
        }
        .stButton > button {
            padding: 0.75rem 1rem !important;
            font-size: 0.875rem !important;
            color: white !important;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 1.375rem !important;
        }
        h2 {
            font-size: 1.125rem !important;
        }
    }
    
    .card-name {
        font-size: 15px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 4px;
    }
    
    .card-rating {
        font-size: 14px;
        color: #f59e0b;
        font-weight: 500;
    }
    
    .card-detail {
        font-size: 12px;
        color: #6b7280;
        margin: 2px 0;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .card-skills {
        font-size: 11px;
        color: #2563eb;
        margin: 4px 0;
        background: #eff6ff;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    
    .card-compact-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }
    
    .btn-call {
        background: #16a34a;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
        flex: 1;
        text-align: center;
    }
    
    .btn-whatsapp {
        background: #25d366;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
        flex: 1;
        text-align: center;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Status badges - Compact */
    .badge-disponible {
        background: #dcfce7;
        color: #16a34a;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
        display: inline-block;
    }
    
    .badge-ocupado {
        background: #fee2e2;
        color: #dc2626;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Filter section */
    .filter-container {
        background: #f9fafb;
        border-radius: 8px;
        padding: 12px;
        margin: 12px 0;
        border: 1px solid #e5e7eb;
    }
    
    .stSelectbox > div > div {
        font-size: 14px !important;
    }
    
    /* Search box */
    .stTextInput > div > div > input {
        font-size: 16px !important;
        padding: 12px !important;
        border-radius: 8px !important;
    }
    
    /* Large touch targets for mobile */
    .stButton > button {
        min-height: 48px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Emoji icons bigger */
    .icon {
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Test Supabase connection
try:
    db.get_supabase_client()
except Exception as e:
    st.error(f"⚠️ Supabase connection error: {e}")
    st.stop()

# Load LUX Logo
try:
    logo = Image.open("assets/logo.png")
except Exception as e:
    logo = None

# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_freelancer' not in st.session_state:
    st.session_state.selected_freelancer = None

def show_home():
    """Home / Dashboard view"""
    
    # Logo and Header
    if logo:
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            st.image(logo, width=120)
        with col_title:
            st.markdown("<h1 style='margin-top:1.5rem;'>LuxPro</h1>", unsafe_allow_html=True)
            st.caption("Plataforma de Gestión de Aplicadores Especializados")
    else:
        st.markdown("<h1>LuxPro</h1>", unsafe_allow_html=True)
        st.caption("Plataforma de Gestión de Aplicadores Especializados")
    
    # Get stats
    stats = db.get_stats()
    
    # Professional stat cards - Dark theme with LUX colors
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background:rgba(249,115,22,0.1);border-radius:12px;padding:1.5rem;border:1px solid rgba(249,115,22,0.3);backdrop-filter:blur(10px);">
            <div style="font-size:2.5rem;font-weight:700;color:#f97316;">{stats['total']}</div>
            <div style="font-size:0.875rem;color:#cbd5e1;margin-top:0.5rem;">Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:rgba(34,197,94,0.1);border-radius:12px;padding:1.5rem;border:1px solid rgba(34,197,94,0.3);backdrop-filter:blur(10px);">
            <div style="font-size:2.5rem;font-weight:700;color:#22c55e;">{stats['disponibles']}</div>
            <div style="font-size:0.875rem;color:#cbd5e1;margin-top:0.5rem;">Disponibles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background:rgba(239,68,68,0.1);border-radius:12px;padding:1.5rem;border:1px solid rgba(239,68,68,0.3);backdrop-filter:blur(10px);">
            <div style="font-size:2.5rem;font-weight:700;color:#ef4444;">{stats['en_proyecto']}</div>
            <div style="font-size:0.875rem;color:#cbd5e1;margin-top:0.5rem;">En Proyecto</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background:rgba(234,179,8,0.1);border-radius:12px;padding:1.5rem;border:1px solid rgba(234,179,8,0.3);backdrop-filter:blur(10px);">
            <div style="font-size:2.5rem;font-weight:700;color:#eab308;">{stats['avg_rating']}</div>
            <div style="font-size:0.875rem;color:#cbd5e1;margin-top:0.5rem;">Rating ★</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ver Aplicadores", use_container_width=True):
            st.session_state.view = 'list'
            st.rerun()
    
    with col2:
        if st.button("Agregar Nuevo", use_container_width=True):
            st.session_state.view = 'add'
            st.rerun()

def show_freelancer_list():
    """Aplicadores list view"""
    
    # Logo and Header
    if logo:
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            st.image(logo, width=100)
        with col_title:
            st.markdown("<h2 style='margin-top:1rem;'>Aplicadores</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2>Aplicadores</h2>", unsafe_allow_html=True)
    
    # Header actions
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Inicio", key="back_home"):
            st.session_state.view = 'home'
            st.rerun()
    with col2:
        if st.button("Agregar Nuevo", use_container_width=True):
            st.session_state.view = 'add'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Search bar
    search_term = st.text_input("", "", key="search", placeholder="🔍 Buscar por nombre...")
    
    # Filters in expander
    with st.expander("Filtros", expanded=False):
        all_freelancers = db.get_all_freelancers()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            distritos = ["Todos"] + sorted(set([f['distrito'] for f in all_freelancers if f.get('distrito')]))
            distrito_filter = st.selectbox("Distrito", distritos, index=0)
            distrito_filter = "" if distrito_filter == "Todos" else distrito_filter
        
        with col2:
            disponibilidad_options = ["Todos", "Disponible", "Ocupado"]
            disponibilidad = st.selectbox("Estado", disponibilidad_options, index=0)
            
            disp_filter = None
            if disponibilidad == "Disponible":
                disp_filter = True
            elif disponibilidad == "Ocupado":
                disp_filter = False
        
        with col3:
            sort_options = ["Nombre", "Rating (Mayor)", "Rating (Menor)"]
            sort_by = st.selectbox("Ordenar por", sort_options, index=0)
        
        skill_filter = st.text_input("Skill", "", placeholder="Ej: Epóxico, Poliaspártico...")
    
    # Get and filter freelancers
    freelancers = db.get_all_freelancers(search_term, skill_filter, distrito_filter)
    
    if disp_filter is not None:
        freelancers = [f for f in freelancers if f['disponible'] == disp_filter]
    
    # Apply sorting
    if sort_by == "Nombre":
        freelancers = sorted(freelancers, key=lambda x: x['nombre'])
    elif sort_by == "Rating (Mayor)":
        freelancers = sorted(freelancers, key=lambda x: x['rating_promedio'], reverse=True)
    elif sort_by == "Rating (Menor)":
        freelancers = sorted(freelancers, key=lambda x: x['rating_promedio'])
    
    st.caption(f"{len(freelancers)} resultados")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Professional Grid - 4 columns
    cols_per_row = 4
    for i in range(0, len(freelancers), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(freelancers):
                freelancer = freelancers[i + j]
                with col:
                    # Status
                    status_color = "#22c55e" if freelancer['disponible'] else "#ef4444"
                    status_text = "Disponible" if freelancer['disponible'] else "Ocupado"
                    
                    # Truncate name for display - get first and last name only
                    name_parts = freelancer['nombre'].split()
                    if len(name_parts) > 2:
                        display_name = f"{name_parts[0]} {name_parts[-1]}"
                    else:
                        display_name = freelancer['nombre']
                    
                    # Clean professional card - Dark theme with LUX colors
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(249,115,22,0.3);border-radius:12px;padding:1.25rem;height:160px;display:flex;flex-direction:column;justify-content:space-between;transition:all 0.2s;cursor:pointer;overflow:hidden;backdrop-filter:blur(10px);" onmouseover="this.style.borderColor='#f97316';this.style.boxShadow='0 4px 12px rgba(249,115,22,0.3)';this.style.background='rgba(249,115,22,0.1)'" onmouseout="this.style.borderColor='rgba(249,115,22,0.3)';this.style.boxShadow='none';this.style.background='rgba(255,255,255,0.05)'">
                        <div>
                            <div style="font-size:1rem;font-weight:600;color:#e2e8f0;margin-bottom:0.25rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{display_name}</div>
                            <div style="font-size:0.8125rem;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{freelancer['distrito'] or 'Sin ubicación'}</div>
                        </div>
                        <div>
                            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.75rem;">
                                <div style="font-size:1.75rem;font-weight:700;color:#eab308;line-height:1;">{freelancer['rating_promedio']}<span style="font-size:1rem;">★</span></div>
                                <div style="font-size:0.75rem;font-weight:600;color:{status_color};background:{status_color}20;padding:0.25rem 0.625rem;border-radius:6px;white-space:nowrap;">{status_text}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Ver Perfil", key=f"view_{freelancer['id']}", use_container_width=True):
                        st.session_state.selected_freelancer = freelancer['id']
                        st.session_state.view = 'profile'
                        st.rerun()

def show_add_freelancer():
    """Add new freelancer form"""
    st.title("➕ Nuevo Freelancer")
    
    if st.button("← Atrás"):
        st.session_state.view = 'list'
        st.rerun()
    
    with st.form("add_freelancer_form"):
        st.subheader("Información Básica")
        
        nombre = st.text_input("Nombre Completo *", "")
        
        col1, col2 = st.columns(2)
        with col1:
            dni = st.text_input("DNI", "", max_chars=8)
        with col2:
            telefono = st.text_input("Teléfono / WhatsApp *", "")
        
        email = st.text_input("Email", "")
        distrito = st.text_input("Distrito", "")
        
        st.subheader("Habilidades")
        skills = st.text_area("Skills / Productos (separados por coma)", 
                             placeholder="Ej: JP01Y, Epóxico, Rodillo, Preparación")
        
        st.subheader("Estado")
        col1, col2 = st.columns(2)
        with col1:
            rating = st.slider("Rating Inicial", 0.0, 5.0, 3.0, 0.5)
        with col2:
            disponible = st.checkbox("Disponible", value=True)
        
        notas = st.text_area("Notas", placeholder="Información adicional sobre el freelancer")
        
        submit = st.form_submit_button("💾 Guardar Freelancer", use_container_width=True)
        
        if submit:
            if not nombre or not telefono:
                st.error("❌ Nombre y teléfono son obligatorios")
            else:
                try:
                    data = {
                        'nombre': nombre,
                        'dni': dni if dni else None,
                        'telefono': telefono,
                        'email': email if email else None,
                        'distrito': distrito if distrito else None,
                        'skills': skills if skills else None,
                        'rating_promedio': rating,
                        'disponible': 1 if disponible else 0,
                        'notas': notas if notas else None
                    }
                    
                    freelancer_id = db.add_freelancer(data)
                    st.success(f"✅ Freelancer agregado correctamente (ID: {freelancer_id})")
                    st.balloons()
                    
                    # Wait a moment then redirect
                    import time
                    time.sleep(1)
                    st.session_state.view = 'list'
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")

def show_profile():
    """Freelancer profile detail view - Professional & Clean"""
    freelancer_id = st.session_state.selected_freelancer
    freelancer = db.get_freelancer_by_id(freelancer_id)
    
    if not freelancer:
        st.error("Freelancer no encontrado")
        st.session_state.view = 'list'
        st.rerun()
        return
    
    # Back button
    if st.button("← Regresar"):
        st.session_state.view = 'list'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Professional profile card
    phone = freelancer['telefono'].replace(' ', '').replace('-', '')
    status_color = "#10b981" if freelancer['disponible'] else "#ef4444"
    status_text = "Disponible" if freelancer['disponible'] else "Ocupado"
    
    # Header with name and rating
    st.markdown(f"""
    <div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
            <div>
                <h2 style="margin:0;font-size:1.75rem;color:#1a1a1a;">{freelancer['nombre']}</h2>
                <p style="margin:0.25rem 0 0 0;font-size:0.875rem;color:#6b7280;">ID: {freelancer['id']} • Registrado: {freelancer['created_at'][:10]}</p>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2.5rem;font-weight:700;color:#f59e0b;line-height:1;">{freelancer['rating_promedio']}<span style="font-size:1.5rem;">★</span></div>
                <div style="font-size:0.75rem;font-weight:600;color:{status_color};background:{status_color}15;padding:0.375rem 0.75rem;border-radius:6px;margin-top:0.5rem;display:inline-block;">{status_text}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info section
    st.markdown("""
    <div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
        <h3 style="margin:0 0 1rem 0;font-size:1.125rem;color:#1a1a1a;">Información</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Ubicación**")
        st.write(freelancer['distrito'] or "No especificado")
        st.markdown("**DNI**")
        st.write(freelancer['dni'] or "No especificado")
    
    with col2:
        st.markdown("**Teléfono**")
        st.write(freelancer['telefono'])
        if freelancer['email']:
            st.markdown("**Email**")
            st.write(freelancer['email'])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Contact buttons
    st.markdown("""
    <div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
        <h3 style="margin:0 0 1rem 0;font-size:1.125rem;color:#1a1a1a;">Contacto</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<a href="tel:+51{phone}" style="display:block;background:#10b981;color:white;padding:0.875rem;border-radius:8px;text-decoration:none;text-align:center;font-weight:500;font-size:0.9375rem;">📞 Llamar</a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="https://wa.me/51{phone}" style="display:block;background:#25d366;color:white;padding:0.875rem;border-radius:8px;text-decoration:none;text-align:center;font-weight:500;font-size:0.9375rem;">💬 WhatsApp</a>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Skills
    if freelancer['skills']:
        st.markdown("""
        <div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <h3 style="margin:0 0 0.75rem 0;font-size:1.125rem;color:#1a1a1a;">Skills</h3>
        """, unsafe_allow_html=True)
        st.info(freelancer['skills'])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Notes
    if freelancer['notas']:
        st.markdown("""
        <div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <h3 style="margin:0 0 0.75rem 0;font-size:1.125rem;color:#1a1a1a;">Notas</h3>
        """, unsafe_allow_html=True)
        st.info(freelancer['notas'])
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Editar", use_container_width=True):
            st.session_state.view = 'edit'
            st.rerun()
    
    with col2:
        if st.button("🗑️ Eliminar", use_container_width=True, type="secondary"):
            st.session_state.view = 'delete_confirm'
            st.rerun()

# Main navigation
if st.session_state.view == 'home':
    show_home()
elif st.session_state.view == 'list':
    show_freelancer_list()
elif st.session_state.view == 'add':
    show_add_freelancer()
elif st.session_state.view == 'profile':
    show_profile()
else:
    show_home()

# Bottom navigation (simple version)
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠", key="nav_home", help="Inicio", use_container_width=True):
        st.session_state.view = 'home'
        st.rerun()

with col2:
    if st.button("👥", key="nav_list", help="Freelancers", use_container_width=True):
        st.session_state.view = 'list'
        st.rerun()

with col3:
    if st.button("➕", key="nav_add", help="Agregar", use_container_width=True):
        st.session_state.view = 'add'
        st.rerun()

with col4:
    if st.button("📊", key="nav_stats", help="Estadísticas", use_container_width=True):
        st.session_state.view = 'home'
        st.rerun()
