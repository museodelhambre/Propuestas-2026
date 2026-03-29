import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
    page_title="Catálogo de Propuestas Culturales",
    page_icon="🎨",
    layout="wide"
)

# Estilo CSS personalizado (Mantenemos tu diseño original que es excelente)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
        transition: transform 0.2s ease-in-out;
        min-height: 350px;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .title {
        color: #1e3a8a;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .artist {
        color: #3b82f6;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 16px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 8px;
        margin-bottom: 12px;
    }
    .badge-eje { background-color: #dbeafe; color: #1e40af; }
    .badge-disc { background-color: #f1f5f9; color: #475569; }
    .description {
        color: #475569;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 20px;
        height: 100px;
        overflow-y: auto;
    }
    .btn-container {
        display: flex;
        gap: 10px;
        margin-top: auto;
    }
    .contact-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 12px;
        border-radius: 10px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 700;
        transition: filter 0.2s;
        flex: 1;
    }
    .btn-mail { background-color: #1e3a8a; color: white !important; }
    .btn-ws { background-color: #25d366; color: white !important; }
    .contact-btn:hover { filter: brightness(1.1); }
    </style>
""", unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path):
        return None
    
    try:
        # Cargamos el CSV
        df = pd.read_csv(file_path)
        
        # Limpiamos nombres de columnas por si tienen espacios invisibles
        df.columns = df.columns.str.strip()
        
        # Mapeo de columnas para asegurar que el código funcione siempre
        mapping = {
            'Nombre del Artista / Colectivo': 'Artista',
            'Disciplina': 'Disciplina',
            'Nombre de la Propuesta': 'Propuesta',
            'Breve descripción de la obra': 'Descripción',
            'Contacto (mail)': 'Mail',
            'Contacto (whatsapp)': 'WhatsApp',
            'Eje temático': 'Eje'
        }
        
        # Renombramos solo las que existan en el CSV
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None

df = load_data()

if df is None:
    st.error("### ❌ Error: No se encontró el archivo 'propuestas.csv'")
    st.info("Asegúrate de que el archivo se llame exactamente 'propuestas.csv' en GitHub.")
else:
    # --- SIDEBAR: FILTROS ---
    st.sidebar.header("🎯 Filtrar Resultados")
    
    # IMPORTANTE: Aquí usamos 'Eje' porque ya se renombró arriba
    ejes = sorted(df['Eje'].dropna().unique())
    eje_sel = st.sidebar.multiselect("Filtrar por Eje Temático", ejes)
    
    disciplinas = sorted(df['Disciplina'].dropna().unique())
    disc_sel = st.sidebar.multiselect("Filtrar por Disciplina", disciplinas)
    
    # --- MAIN: BUSCADOR Y TÍTULO ---
    st.title("🎨 Museo del Hambre: Propuestas 2026")
    st.markdown("Explora las propuestas de artistas y colectivos de nuestra comunidad.")
    
    search = st.text_input("🔍 Buscar por artista o nombre de propuesta", placeholder="Ej: Juan Perez o Taller de Cocina...")
    
    # --- LÓGICA DE FILTRADO ---
    filtered_df = df.copy()
    
    if eje_sel:
        filtered_df = filtered_df[filtered_df['Eje'].isin(eje_sel)]
    if disc_sel:
        filtered_df = filtered_df[filtered_df['Disciplina'].isin(disc_sel)]
    if search:
        filtered_df = filtered_df[
            filtered_df['Artista'].astype(str).str.contains(search, case=False, na=False) |
            filtered_df['Propuesta'].astype(str).str.contains(search, case=False, na=False)
        ]
    
    # --- RENDERIZADO DE TARJETAS ---
    if filtered_df.empty:
        st.info("✨ No se encontraron resultados que coincidan con tu búsqueda.")
    else:
        st.write(f"Se encontraron *{len(filtered_df)}* propuestas")
        
        # Grid de 3 columnas para PC, se apila solo en móvil
        cols = st.columns(3)
        
        for idx, row in filtered_df.reset_index().iterrows():
            # Limpiar número de WhatsApp
            ws_num = str(row['WhatsApp']).replace('+', '').replace(' ', '').replace('-', '').split('.')[0]
            
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="card">
                        <div class="title">{row['Propuesta']}</div>
                        <div class="artist">{row['Artista']}</div>
                        <div>
                            <span class="badge badge-eje">{row['Eje']}</span>
                            <span class="badge badge-disc">{row['Disciplina']}</span>
                        </div>
                        <div class="description">{row['Descripción']}</div>
                        <div class="btn-container">
                            <a href="mailto:{row['Mail']}" class="contact-btn btn-mail">📧 Mail</a>
                            <a href="https://wa.me/{ws_num}" target="_blank" class="contact-btn btn-ws">💬 WhatsApp</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.caption("Plataforma de Gestión Cultural - Museo del Hambre 2026")
