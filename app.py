import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Catálogo de Propuestas Culturales",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (Manteniendo tu diseño y agregando etiquetas de datos)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        min-height: 520px;
    }
    .title { color: #1e3a8a; font-size: 20px; font-weight: 800; margin-bottom: 4px; line-height: 1.2; }
    .artist { color: #3b82f6; font-size: 15px; font-weight: 600; margin-bottom: 12px; }
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
    
    /* Nuevas etiquetas para mostrar los datos de contacto */
    .data-label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        margin-top: 8px;
        text-transform: uppercase;
    }
    .data-value {
        font-size: 13px;
        color: #1e293b;
        margin-bottom: 4px;
        word-break: break-all;
    }
    .description {
        color: #475569;
        font-size: 13.5px;
        line-height: 1.5;
        margin-bottom: 15px;
        margin-top: 10px;
        flex-grow: 1;
    }
    .btn-container { display: flex; gap: 8px; margin-top: 15px; }
    .contact-btn {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 700;
        color: white !important;
    }
    .btn-mail { background-color: #1e3a8a; }
    .btn-ws { background-color: #25d366; }
    </style>
""", unsafe_allow_html=True)

# 3. Carga de datos con mapeo de REFERENCIA
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        
        # Mapeo inteligente (incluyendo Referencia)
        mapping = {
            'Nombre del Artista / Colectivo': 'Artista',
            'Disciplina': 'Disciplina',
            'Nombre de la Propuesta': 'Propuesta',
            'Breve descripción de la obra': 'Descripción',
            'Contacto (mail)': 'Mail',
            'Contacto (whatsapp)': 'WhatsApp',
            'Eje temático': 'Eje',
            'Referencia Adjunta': 'Referencia',
            'Referencia': 'Referencia'
        }
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        
        # Asegurar columnas y limpiar vacíos
        for col in ['Artista', 'Propuesta', 'Eje', 'Disciplina', 'Descripción', 'Mail', 'WhatsApp', 'Referencia']:
            if col not in df.columns: df[col] = "No disponible"
            df[col] = df[col].fillna("No disponible").astype(str)
            
        return df
    except Exception as e:
        st.error(f"Error: {e}"); return None

df = load_data()

if df is not None:
    # FILTROS
    st.sidebar.header("🎯 Filtros")
    eje_sel = st.sidebar.multiselect("Eje Temático", sorted([x for x in df['Eje'].unique() if x != "No disponible"]))
    disc_sel = st.sidebar.multiselect("Disciplina", sorted([x for x in df['Disciplina'].unique() if x != "No disponible"]))
    
    st.title("🎨 Catálogo de Propuestas 2026")
    search = st.text_input("🔍 Buscar artista o propuesta...", placeholder="Escribe aquí...")

    # Filtrado
    f_df = df.copy()
    if eje_sel: f_df = f_df[f_df['Eje'].isin(eje_sel)]
    if disc_sel: f_df = f_df[f_df['Disciplina'].isin(disc_sel)]
    if search:
        f_df = f_df[f_df['Artista'].str.contains(search, case=False) | f_df['Propuesta'].str.contains(search, case=False)]

    # RENDERIZADO
    if f_df.empty:
        st.info("No hay resultados.")
    else:
        st.write(f"Mostrando *{len(f_df)}* propuestas")
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            # Limpiar WhatsApp para el link
            ws_link = row['WhatsApp'].split('.')[0].replace('+', '').replace(' ', '')
            
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="card">
                        <div class="title">{row['Propuesta']}</div>
                        <div class="artist">{row['Artista']}</div>
                        <div>
                            <span class="badge badge-eje">{row['Eje']}</span>
                            <span class="badge badge-disc">{row['Disciplina']}</span>
                        </div>
                        
                        <div class="description">{row['Descripción']}</div>
                        
                        <div class="data-label">📍 Referencia:</div>
                        <div class="data-value"><a href="{row['Referencia']}" target="_blank">Ver link adjunto</a></div>
                        
                        <div class="data-label">📧 Correo:</div>
                        <div class="data-value">{row['Mail']}</div>
                        
                        <div class="data-label">📱 WhatsApp:</div>
                        <div class="data-value">{row['WhatsApp']}</div>
                        
                        <div class="btn-container">
                            <a href="mailto:{row['Mail']}" class="contact-btn btn-mail">📧 Escribir</a>
                            <a href="https://wa.me/{ws_link}" target="_blank" class="contact-btn btn-ws">💬 WhatsApp</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Plataforma Museo del Hambre - 2026")
