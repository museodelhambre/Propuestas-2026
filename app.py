import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Museo del Hambre - Propuestas 2026",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (El diseño de Google AI que elegiste con ajustes para los datos)
st.markdown("""
    <style>
    /* Fondo general más claro, estilo Google */
    .main {
        background-color: #f0f4f8;
    }
    /* Tarjetas estilo 'Material Design' */
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
        display: flex;
        flex-direction: column;
        min-height: 480px; /* Un poco más alto para los datos extra */
    }
    .card:hover {
        box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
    }
    /* Títulos estilo Google */
    .title {
        color: #1a73e8;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 19px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .artist {
        color: #5f6368;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 12px;
    }
    /* Badges */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 12px;
    }
    .badge-eje { background-color: #e8f0fe; color: #1967d2; }
    .badge-disc { background-color: #f1f3f4; color: #3c4043; }
    
    .description {
        color: #3c4043;
        font-size: 13.5px;
        line-height: 1.6;
        margin-bottom: 15px;
        flex-grow: 1;
    }

    /* Estilo para los datos de contacto (No botones) */
    .contact-info-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #eee;
        margin-top: 10px;
    }
    .data-label {
        font-size: 11px;
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
    .data-value a {
        color: #1a73e8;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Carga de datos robusta
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        
        # Mapeo inteligente de columnas para evitar KeyErrors
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
        
        # Aseguramos que todas las columnas existan y sean texto
        for col in ['Artista', 'Propuesta', 'Eje', 'Disciplina', 'Descripción', 'Mail', 'WhatsApp', 'Referencia']:
            if col not in df.columns:
                df[col] = "No disponible"
            else:
                df[col] = df[col].fillna("No disponible").astype(str)
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}"); return None

df = load_data()

if df is not None:
    # --- FILTROS ---
    st.sidebar.header("🎯 Filtros")
    ejes_lista = sorted([x for x in df['Eje'].unique() if x != "No disponible"])
    eje_sel = st.sidebar.multiselect("Eje Temático", ejes_lista)
    
    discs_lista = sorted([x for x in df['Disciplina'].unique() if x != "No disponible"])
    disc_sel = st.sidebar.multiselect("Disciplina", discs_lista)
    
    st.title("🎨 Catálogo de Propuestas 2026")
    search = st.text_input("🔍 Buscar artista o propuesta...", placeholder="Ej: Museo...")

    # Lógica de filtrado
    f_df = df.copy()
    if eje_sel: f_df = f_df[f_df['Eje'].isin(eje_sel)]
    if disc_sel: f_df = f_df[f_df['Disciplina'].isin(disc_sel)]
    if search:
        f_df = f_df[f_df['Artista'].str.contains(search, case=False) | 
                    f_df['Propuesta'].str.contains(search, case=False)]

    # --- RENDERIZADO ---
    if f_df.empty:
        st.info("No se encontraron resultados.")
    else:
        st.write(f"Mostrando *{len(f_df)}* propuestas")
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
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
                        
                        <div class="contact-info-box">
                            <div class="data-label">📍 Referencia</div>
                            <div class="data-value"><a href="{row['Referencia']}" target="_blank">Abrir enlace</a></div>
                            
                            <div class="data-label">📧 Correo electrónico</div>
                            <div class="data-value">{row['Mail']}</div>
                            
                            <div class="data-label">📱 WhatsApp / Teléfono</div>
                            <div class="data-value">{row['WhatsApp']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - Plataforma de Gestión 2026")
