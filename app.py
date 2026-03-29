import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
    page_title="Catálogo de Propuestas Culturales",
    page_icon="🎨",
    layout="wide"
)

# Estilo CSS personalizado para las tarjetas y botones
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
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .title {
        color: #1e3a8a;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .artist {
        color: #3b82f6;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
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
        line-height: 1.6;
        margin-bottom: 20px;
        height: 80px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    .btn-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .contact-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 16px;
        border-radius: 10px;
        text-decoration: none !important;
        font-size: 13px;
        font-weight: 700;
        transition: filter 0.2s;
    }
    .btn-mail { background-color: #1e3a8a; color: white !important; }
    .btn-ws { background-color: #25d366; color: white !important; }
    .contact-btn:hover { filter: brightness(1.1); }
    </style>
""", unsafe_allow_html=True)

# Función para cargar datos con manejo de errores
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path)
        # Mapeo de columnas para asegurar compatibilidad
        mapping = {
            'Nombre del Artista / Colectivo': 'Artista',
            'Nombre del Artista': 'Artista',
            'Disciplina': 'Disciplina',
            'Nombre de la Propuesta': 'Propuesta',
            'Breve descripción de la obra': 'Descripción',
            'Breve descripción': 'Descripción',
            'Contacto (mail)': 'Mail',
            'Contacto (whatsapp)': 'WhatsApp',
            'Eje temático': 'Eje'
        }
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None

df = load_data()

if df is None:
    st.error("### ❌ Error: No se encontró el archivo 'propuestas.csv'")
    st.info("Asegúrate de que el archivo CSV esté en la misma carpeta que este script.")
else:
    # --- SIDEBAR: FILTROS ---
    st.sidebar.header("🎯 Filtrar Resultados")
    
    ejes = sorted(df['Eje temático'].dropna().unique())
    eje_sel = st.sidebar.multiselect("Eje temático", ejes)
    
    disciplinas = sorted(df['Disciplina'].dropna().unique())
    disc_sel = st.sidebar.multiselect("Disciplina", disciplinas)
    
    # --- MAIN: BUSCADOR Y TÍTULO ---
    st.title("🎨 Propuestas Culturales")
    st.markdown("Explora las propuestas de artistas y colectivos de nuestra comunidad.")
    
    search = st.text_input("🔍 Buscar por artista o propuesta", placeholder="Escribe aquí...")
    
    # --- LÓGICA DE FILTRADO ---
    filtered_df = df.copy()
    
    if eje_sel:
        filtered_df = filtered_df[filtered_df['Eje'].isin(eje_sel)]
    if disc_sel:
        filtered_df = filtered_df[filtered_df['Disciplina'].isin(disc_sel)]
    if search:
        filtered_df = filtered_df[
            filtered_df['Artista'].str.contains(search, case=False, na=False) |
            filtered_df['Propuesta'].str.contains(search, case=False, na=False)
        ]
    
    # --- RENDERIZADO DE TARJETAS ---
    if filtered_df.empty:
        st.info("✨ No se encontraron resultados que coincidan con tu búsqueda.")
    else:
        st.write(f"Se encontraron **{len(filtered_df)}** propuestas")
        
        # Crear columnas para la rejilla (grid)
        cols = st.columns(3) # 3 tarjetas por fila en pantallas grandes
        
        for idx, row in filtered_df.reset_index().iterrows():
            # Limpiar número de WhatsApp
            ws_num = str(row['WhatsApp']).replace('+', '').replace(' ', '').replace('-', '')
            
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
st.caption("Plataforma de Gestión Cultural - 2026")
