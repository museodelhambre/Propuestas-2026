import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Museo del Hambre - Propuestas 2026",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (Google Design con ajustes de fuentes y botones)
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
    
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 10px;
    }
    .badge-eje { background-color: #e8f0fe; color: #1967d2; }
    .badge-disc { background-color: #f1f3f4; color: #3c4043; }
    
    .description { color: #3c4043; font-size: 14px; line-height: 1.6; margin-bottom: 15px; }

    .contact-box {
        background-color: #f8f9fa;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #eee;
        margin-top: auto;
    }

    .data-label { font-size: 11px; font-weight: 700; color: #70757a; text-transform: uppercase; margin-top: 8px; }
    
    /* TIPOGRAFIA AGRANDADA PARA CONTACTOS */
    .data-value-contact { font-size: 18px; font-weight: 600; color: #202124; margin-bottom: 10px; }
    .data-value { font-size: 13px; color: #202124; margin-bottom: 5px; }

    /* BOTONES DE REFERENCIA */
    .ref-container { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
    .ref-btn {
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        text-decoration: none !important;
        text-align: center;
        min-width: 100px;
    }
    .ref-active { background-color: #e8f0fe; color: #1967d2 !important; border: 1px solid #1967d2; }
    .ref-inactive { background-color: #202124; color: #ffffff !important; cursor: not-allowed; opacity: 0.8; border: 1px solid #000; }
</style>
""", unsafe_allow_html=True)

# 3. Carga de datos con mapeo actualizado
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
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
        
        # Columnas a asegurar
        cols_to_fix = ['Artista', 'Responsable', 'Mail', 'WhatsApp', 'Disciplina', 'Propuesta', 'Descripción', 
                       'Referencia 1', 'Referencia 2', 'Referencia 3', 'Eje', 'Disponibilidad', 'Comentarios']
        
        for col in cols_to_fix:
            if col not in df.columns: df[col] = ""
            df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except: return None

df = load_data()

if df is not None:
    # FILTROS
    st.sidebar.header("🎯 Filtros")
    eje_sel = st.sidebar.multiselect("Eje Temático", sorted([x for x in df['Eje'].unique() if x != ""]))
    disc_sel = st.sidebar.multiselect("Disciplina", sorted([x for x in df['Disciplina'].unique() if x != ""]))
    
    st.title("🎨 Catálogo de Propuestas 2026")
    search = st.text_input("🔍 Buscar artista o propuesta...")

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
        st.write(f"Viendo *{len(f_df)}* propuestas")
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            with cols[i % 3]:
                # Lógica para botones de referencia
                refs_html = ""
                for n in ["1", "2", "3"]:
                    val = row[f'Referencia {n}']
                    if val != "" and val.lower() != "no disponible":
                        refs_html += f'<a href="{val}" target="_blank" class="ref-btn ref-active">Referencia {n} 🔗</a>'
                    else:
                        refs_html += f'<span class="ref-btn ref-inactive">Referencia {n} 🚫</span>'

                card_html = f"""
<div class="card">
    <div class="title">{row['Propuesta']}</div>
    <div class="artist">{row['Artista']}</div>
    <div>
        <span class="badge badge-eje">{row['Eje']}</span>
        <span class="badge badge-disc">{row['Disciplina']}</span>
    </div>
    <div class="description">{row['Descripción']}</div>
    
    <div class="data-label">📍 Referencias adjuntas:</div>
    <div class="ref-container">{refs_html}</div>

    <div class="contact-box">
        <div class="data-label">👤 Responsable</div>
        <div class="data-value">{row['Responsable']}</div>
        
        <div class="data-label">📧 Correo electrónico</div>
        <div class="data-value-contact">{row['Mail']}</div>
        
        <div class="data-label">📱 WhatsApp / Teléfono</div>
        <div class="data-value-contact">{row['WhatsApp']}</div>
        
        <div class="data-label">⏳ Disponibilidad</div>
        <div class="data-value">{row['Disponibilidad']}</div>
        
        <div class="data-label">💬 Comentarios</div>
        <div class="data-value"><i>{row['Comentarios']}</i></div>
    </div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - Plataforma de Gestión 2026")
