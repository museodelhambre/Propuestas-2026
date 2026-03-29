import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Museo del Hambre - Propuestas 2026",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (Estilo Google AI - Limpio y Moderno)
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stMarkdown { width: 100%; }
    
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        min-height: 450px;
    }
    
    .title {
        color: #1a73e8;
        font-family: 'Google Sans', Roboto, Arial, sans-serif;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .artist {
        color: #5f6368;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 12px;
    }

    .badge-container { margin-bottom: 15px; }
    
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
    }
    
    .badge-eje { background-color: #e8f0fe; color: #1967d2; }
    .badge-disc { background-color: #f1f3f4; color: #3c4043; }
    
    .description {
        color: #3c4043;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 20px;
        flex-grow: 1;
    }

    .contact-box {
        background-color: #f8f9fa;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #eee;
    }

    .data-label {
        font-size: 10px;
        font-weight: 700;
        color: #70757a;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .data-value {
        font-size: 13px;
        color: #202124;
        margin-bottom: 8px;
        word-break: break-all;
    }
    
    .data-value a { color: #1a73e8; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        
        # Mapeo de columnas
        new_cols = {}
        for col in df.columns:
            c = col.lower()
            if 'artista' in c: new_cols[col] = 'Artista'
            elif 'propuesta' in c and 'nombre' in c: new_cols[col] = 'Propuesta'
            elif 'disciplina' in c: new_cols[col] = 'Disciplina'
            elif 'eje' in c: new_cols[col] = 'Eje'
            elif 'mail' in c: new_cols[col] = 'Mail'
            elif 'whatsapp' in c: new_cols[col] = 'WhatsApp'
            elif 'descrip' in c: new_cols[col] = 'Descripción'
            elif 'referencia' in c: new_cols[col] = 'Referencia'
            
        df = df.rename(columns=new_cols)
        
        # Completar faltantes
        for col in ['Artista', 'Propuesta', 'Eje', 'Disciplina', 'Descripción', 'Mail', 'WhatsApp', 'Referencia']:
            if col not in df.columns: df[col] = "No disponible"
            df[col] = df[col].fillna("No disponible").astype(str)
        return df
    except: return None

df = load_data()

if df is not None:
    # FILTROS
    st.sidebar.header("🎯 Filtros")
    eje_sel = st.sidebar.multiselect("Eje Temático", sorted(df['Eje'].unique()))
    disc_sel = st.sidebar.multiselect("Disciplina", sorted(df['Disciplina'].unique()))
    
    st.title("🎨 Catálogo de Propuestas 2026")
    search = st.text_input("🔍 Buscar artista o propuesta...")

    # Filtrado
    f_df = df.copy()
    if eje_sel: f_df = f_df[f_df['Eje'].isin(eje_sel)]
    if disc_sel: f_df = f_df[f_df['Disciplina'].isin(disc_sel)]
    if search:
        f_df = f_df[f_df['Artista'].str.contains(search, case=False) | f_df['Propuesta'].str.contains(search, case=False)]

    # RENDERIZADO (Corregido para evitar el error visual de código)
    if f_df.empty:
        st.info("No hay resultados.")
    else:
        st.write(f"Mostrando *{len(f_df)}* propuestas")
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            with cols[i % 3]:
                # USAMOS HTML PURO SIN INDENTACIÓN PARA EVITAR EL FONDO OSCURO
                card_html = f"""
<div class="card">
    <div class="title">{row['Propuesta']}</div>
    <div class="artist">{row['Artista']}</div>
    <div class="badge-container">
        <span class="badge badge-eje">{row['Eje']}</span>
        <span class="badge badge-disc">{row['Disciplina']}</span>
    </div>
    <div class="description">{row['Descripción']}</div>
    <div class="contact-box">
        <div class="data-label">📍 Referencia</div>
        <div class="data-value"><a href="{row['Referencia']}" target="_blank">Abrir enlace</a></div>
        <div class="data-label">📧 Correo</div>
        <div class="data-value">{row['Mail']}</div>
        <div class="data-label">📱 WhatsApp</div>
        <div class="data-value">{row['WhatsApp']}</div>
    </div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - 2026")
