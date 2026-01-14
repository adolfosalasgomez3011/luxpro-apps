"""
Database operations for FAMS using Supabase
"""
from supabase import create_client, Client
import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime

# Get Supabase credentials from Streamlit secrets
def get_supabase_client() -> Client:
    """Initialize Supabase client"""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        # Create client with minimal options
        return create_client(
            supabase_url=url,
            supabase_key=key
        )
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        st.info("Please configure .streamlit/secrets.toml with your Supabase credentials")
        raise

# CRUD Operations

def get_all_freelancers(search_term: str = "", skill_filter: str = "", distrito_filter: str = "") -> List[Dict]:
    """Get all freelancers with optional filters"""
    supabase = get_supabase_client()
    
    # Start query
    query = supabase.table('freelancers').select('*')
    
    # Apply filters
    if search_term:
        query = query.ilike('nombre', f'%{search_term}%')
    
    if skill_filter:
        query = query.ilike('skills', f'%{skill_filter}%')
    
    if distrito_filter:
        query = query.eq('distrito', distrito_filter)
    
    # Execute query
    response = query.order('rating_promedio', desc=True).order('nombre').execute()
    
    return response.data

def get_freelancer_by_id(freelancer_id: int) -> Optional[Dict]:
    """Get single freelancer by ID"""
    supabase = get_supabase_client()
    
    response = supabase.table('freelancers').select('*').eq('id', freelancer_id).execute()
    
    return response.data[0] if response.data else None

def add_freelancer(data: Dict) -> int:
    """Add new freelancer"""
    supabase = get_supabase_client()
    
    # Prepare data
    freelancer_data = {
        'dni': data.get('dni'),
        'nombre': data['nombre'],
        'telefono': data['telefono'],
        'email': data.get('email'),
        'distrito': data.get('distrito'),
        'skills': data.get('skills'),
        'rating_promedio': data.get('rating_promedio', 0),
        'disponible': data.get('disponible', True),
        'notas': data.get('notas')
    }
    
    # Insert
    response = supabase.table('freelancers').insert(freelancer_data).execute()
    
    return response.data[0]['id'] if response.data else None

def update_freelancer(freelancer_id: int, data: Dict):
    """Update existing freelancer"""
    supabase = get_supabase_client()
    
    # Prepare data
    update_data = {
        'dni': data.get('dni'),
        'nombre': data['nombre'],
        'telefono': data['telefono'],
        'email': data.get('email'),
        'distrito': data.get('distrito'),
        'skills': data.get('skills'),
        'rating_promedio': data.get('rating_promedio', 0),
        'disponible': data.get('disponible', True),
        'notas': data.get('notas')
    }
    
    # Update
    response = supabase.table('freelancers').update(update_data).eq('id', freelancer_id).execute()
    
    return response.data

def delete_freelancer(freelancer_id: int):
    """Delete freelancer"""
    supabase = get_supabase_client()
    
    response = supabase.table('freelancers').delete().eq('id', freelancer_id).execute()
    
    return response.data

def toggle_disponibilidad(freelancer_id: int, disponible: bool):
    """Toggle freelancer availability"""
    supabase = get_supabase_client()
    
    response = supabase.table('freelancers').update({'disponible': disponible}).eq('id', freelancer_id).execute()
    
    return response.data

def get_stats() -> Dict:
    """Get dashboard statistics"""
    supabase = get_supabase_client()
    
    # Get all active freelancers
    all_response = supabase.table('freelancers').select('*', count='exact').eq('estado', 'Activo').execute()
    total = all_response.count if hasattr(all_response, 'count') else len(all_response.data)
    
    # Get available freelancers
    available_response = supabase.table('freelancers').select('*', count='exact').eq('estado', 'Activo').eq('disponible', True).execute()
    disponibles = available_response.count if hasattr(available_response, 'count') else len(available_response.data)
    
    # Calculate in project
    en_proyecto = total - disponibles
    
    # Get average rating
    ratings_response = supabase.table('freelancers').select('rating_promedio').eq('estado', 'Activo').execute()
    ratings = [float(r['rating_promedio']) for r in ratings_response.data if r['rating_promedio']]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
    
    return {
        'total': total,
        'disponibles': disponibles,
        'en_proyecto': en_proyecto,
        'avg_rating': avg_rating
    }

def log_contact(freelancer_id: int, tipo: str, notas: str = ""):
    """Log contact with freelancer"""
    supabase = get_supabase_client()
    
    contact_data = {
        'freelancer_id': freelancer_id,
        'tipo': tipo,
        'notas': notas
    }
    
    response = supabase.table('contact_log').insert(contact_data).execute()
    
    return response.data

def get_contact_history(freelancer_id: int, limit: int = 10) -> List[Dict]:
    """Get contact history for freelancer"""
    supabase = get_supabase_client()
    
    response = supabase.table('contact_log').select('*').eq('freelancer_id', freelancer_id).order('fecha', desc=True).limit(limit).execute()
    
    return response.data

# Project operations

def get_all_projects() -> List[Dict]:
    """Get all projects"""
    supabase = get_supabase_client()
    
    response = supabase.table('projects').select('*').order('created_at', desc=True).execute()
    
    return response.data

def add_project(data: Dict) -> int:
    """Add new project"""
    supabase = get_supabase_client()
    
    response = supabase.table('projects').insert(data).execute()
    
    return response.data[0]['id'] if response.data else None

def assign_freelancer_to_project(project_id: int, freelancer_id: int, assignment_data: Dict) -> int:
    """Assign freelancer to project"""
    supabase = get_supabase_client()
    
    data = {
        'project_id': project_id,
        'freelancer_id': freelancer_id,
        **assignment_data
    }
    
    response = supabase.table('assignments').insert(data).execute()
    
    # Update freelancer availability
    if response.data:
        toggle_disponibilidad(freelancer_id, False)
    
    return response.data[0]['id'] if response.data else None

def get_project_assignments(project_id: int) -> List[Dict]:
    """Get all assignments for a project with freelancer details"""
    supabase = get_supabase_client()
    
    response = supabase.table('assignments').select('*, freelancers(*)').eq('project_id', project_id).execute()
    
    return response.data

def get_freelancer_projects(freelancer_id: int) -> List[Dict]:
    """Get all projects for a freelancer"""
    supabase = get_supabase_client()
    
    response = supabase.table('assignments').select('*, projects(*)').eq('freelancer_id', freelancer_id).execute()
    
    return response.data

# Rating operations

def add_rating(assignment_id: int, rating_data: Dict) -> int:
    """Add rating for an assignment"""
    supabase = get_supabase_client()
    
    # Calculate general rating
    dimensions = ['calidad', 'puntualidad', 'instrucciones', 'seguridad', 'profesionalismo']
    rating_values = [rating_data.get(d, 0) for d in dimensions]
    rating_general = round(sum(rating_values) / len(rating_values), 2)
    
    data = {
        'assignment_id': assignment_id,
        **rating_data,
        'rating_general': rating_general
    }
    
    response = supabase.table('ratings').insert(data).execute()
    
    # Update freelancer's average rating
    if response.data:
        assignment = supabase.table('assignments').select('freelancer_id').eq('id', assignment_id).execute()
        if assignment.data:
            freelancer_id = assignment.data[0]['freelancer_id']
            update_freelancer_rating(freelancer_id)
    
    return response.data[0]['id'] if response.data else None

def update_freelancer_rating(freelancer_id: int):
    """Recalculate and update freelancer's average rating"""
    supabase = get_supabase_client()
    
    # Get all ratings for this freelancer through assignments
    assignments = supabase.table('assignments').select('id').eq('freelancer_id', freelancer_id).execute()
    
    if not assignments.data:
        return
    
    assignment_ids = [a['id'] for a in assignments.data]
    
    # Get all ratings for these assignments
    ratings = supabase.table('ratings').select('rating_general').in_('assignment_id', assignment_ids).execute()
    
    if ratings.data:
        avg_rating = round(sum(r['rating_general'] for r in ratings.data) / len(ratings.data), 2)
        supabase.table('freelancers').update({'rating_promedio': avg_rating}).eq('id', freelancer_id).execute()

def get_freelancer_ratings(freelancer_id: int) -> List[Dict]:
    """Get all ratings for a freelancer"""
    supabase = get_supabase_client()
    
    # Get assignments
    assignments = supabase.table('assignments').select('id, projects(nombre)').eq('freelancer_id', freelancer_id).execute()
    
    if not assignments.data:
        return []
    
    assignment_ids = [a['id'] for a in assignments.data]
    
    # Get ratings with assignment details
    ratings = supabase.table('ratings').select('*').in_('assignment_id', assignment_ids).order('fecha', desc=True).execute()
    
    # Merge project names
    assignment_map = {a['id']: a['projects']['nombre'] for a in assignments.data if a.get('projects')}
    
    for rating in ratings.data:
        rating['proyecto'] = assignment_map.get(rating['assignment_id'], 'Unknown')
    
    return ratings.data

# Utility functions

def get_distritos() -> List[str]:
    """Get list of all unique distritos"""
    supabase = get_supabase_client()
    
    response = supabase.table('freelancers').select('distrito').execute()
    
    distritos = sorted(set(r['distrito'] for r in response.data if r.get('distrito')))
    
    return distritos

def search_available_freelancers(skill: str = "", distrito: str = "") -> List[Dict]:
    """Search for available freelancers"""
    return get_all_freelancers(skill_filter=skill, distrito_filter=distrito)
