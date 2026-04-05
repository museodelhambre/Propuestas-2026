import streamlit as st
import pandas as pd
import os
import textwrap

# 1. Configuración de la página
st.set_page_config(
    page_title="Museo del Hambre - Propuestas 2026",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (Diseño Google con Tipografía de Contacto Agrandada)
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        min-height: 600px;
    }
    .title { color: #1a73e8; font-size: 22px; font-weight: 600; margin-bottom: 4px; }
    .artist { color: #5f6368; font-size: 16px; font-weight: 500; margin-bottom: 12px; }
    
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
    
    .description { color: #3c4043; font-size: 14.5px; line-height: 1.6; margin-bottom: 20px; flex-grow: 1; }

    .contact-box {
        background-color: #f8f9fa;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #eee;
        margin-top: auto;
    }

    .data-label { font-size: 11px; font-weight: 700; color: #70757a; text-transform: uppercase; margin-top: 8px; }
    
    .data-value-contact { 
        font-size: 20px; 
        font-weight: 700; 
        color: #1e293b; 
        margin-bottom: 12px;
        word-break: break-all;
    }
    .data-value { font-size: 14px; color: #202124; margin-bottom: 5px; }

    .ref-container { display: flex; gap: 8px; margin-top: 10px; margin-bottom: 15px; flex-wrap: wrap; }
    .ref-btn {
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none !important;
        text-align: center;
        min-width: 110px;
    }
    .ref-active { background-color: #e8f0fe; color: #1967d2 !important; border: 1px solid #1967d2; }
    .ref-inactive { background-color: #1a1a1a; color: #ffffff !important; border: 1px solid #000; cursor: not-allowed; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos desde Link RAW (Caché de 15 minutos)
@st.cache_data(ttl=900)
def load_data():
    url = "https://raw.githubusercontent.com/museodelhambre/Propuestas-2026/refs/heads/main/propuestas.csv"
    try:
        df = pd.read_csv(url, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        
        mapping = {
            'Nombre del Artista / Colectivo': 'Artista',
            'Nombre del contacto principal': 'Responsable',
            'Contacto (mail)': 'Mail',
            'Contacto (whatsapp)': 'WhatsApp',
            'Disciplina': 'Disciplina',
            'Nombre de la Propuesta': 'Propuesta',
            'Breve descripción de la obra': 'Descripción',
            'Eje temático': 'Eje',
            'Disponibilidad': 'Disponibilidad',
            'Comentarios': 'Comentarios'
        }
        df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
        
        cols_to_ensure = ['Artista', 'Responsable', 'Mail', 'WhatsApp', 'Disciplina', 'Propuesta', 'Descripción', 
                          'Referencia 1', 'Referencia 2', 'Referencia 3', 'Eje', 'Disponibilidad', 'Comentarios']
        
        for col in cols_to_ensure:
            if col not in df.columns: df[col] = ""
            df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except:
        return None

df = load_data()

if df is not None:
    # --- TÍTULO ---
    st.title("🎨 Catálogo de Propuestas 2026")
    
    # --- FILTROS ---
    st.markdown("### 🎯 Filtrar propuestas")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        eje_sel = st.multiselect("Eje Temático", sorted([x for x in df['Eje'].unique() if x != ""]))
    
    with col_f2:
        disc_sel = st.multiselect("Disciplina", sorted([x for x in df['Disciplina'].unique() if x != ""]))
    
    # --- BUSCADOR ---
    search = st.text_input("🔍 Buscar artista o propuesta...", placeholder="Escribe aquí...")

    # Filtrado lógico
    f_df = df.copy()
    if eje_sel: f_df = f_df[f_df['Eje'].isin(eje_sel)]
    if disc_sel: f_df = f_df[f_df['Disciplina'].isin(disc_sel)]
    if search:
        f_df = f_df[f_df['Artista'].str.contains(search, case=False) | f_df['Propuesta'].str.contains(search, case=False)]

    if f_df.empty:
        st.info("No hay resultados.")
    else:
        st.write(f"Mostrando {len(f_df)} propuestas")
        
        # Grid de tarjetas (3 columnas)
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            with cols[i % 3]:
                # Generar botones de referencia
                refs_html = ""
                for n in ["1", "2", "3"]:
                    link = row[f'Referencia {n}']
                    if link and link.lower() not in ["", "nan", "no disponible"]:
                        refs_html += f'<a href="{link}" target="_blank" class="ref-btn ref-active">Ref {n} 🔗</a>'
                    else:
                        refs_html += f'<span class="ref-btn ref-inactive">Ref {n} 🚫</span>'

                # Contenido de la tarjeta en HTML compacto
                card_content = f"""<div class="card"><div class="title">{row['Propuesta']}</div><div class="artist">{row['Artista']}</div><div class="badge-container"><span class="badge badge-eje">{row['Eje']}</span><span class="badge badge-disc">{row['Disciplina']}</span></div><div class="description">{row['Descripción']}</div><div class="data-label">📍 Referencias adjuntas:</div><div class="ref-container">{refs_html}</div><div class="contact-box"><div class="data-label">👤 Responsable</div><div class="data-value">{row['Responsable']}</div><div class="data-label">📧 Correo electrónico</div><div class="data-value-contact">{row['Mail']}</div><div class="data-label">📱 WhatsApp / Teléfono</div><div class="data-value-contact">{row['WhatsApp']}</div><div class="data-label">⏳ Disponibilidad</div><div class="data-value">{row['Disponibilidad']}</div><div class="data-label">💬 Comentarios</div><div class="data-value"><i>{row['Comentarios']}</i></div></div></div>"""
                st.markdown(card_content, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - 2026")
