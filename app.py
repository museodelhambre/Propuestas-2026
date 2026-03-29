import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Museo del Hambre - Propuestas 2026",
    page_icon="🎨",
    layout="wide"
)

# 2. Estilo CSS (Tu diseño original intacto)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 24px;
        transition: transform 0.2s;
        min-height: 380px;
        display: flex;
        flex-direction: column;
    }
    .card:hover { transform: translateY(-4px); }
    .title { color: #1e3a8a; font-size: 20px; font-weight: 800; margin-bottom: 4px; }
    .artist { color: #3b82f6; font-size: 15px; font-weight: 600; margin-bottom: 12px; }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 700;
        margin-right: 5px;
        margin-bottom: 10px;
    }
    .badge-eje { background-color: #dbeafe; color: #1e40af; }
    .badge-disc { background-color: #f1f5f9; color: #475569; }
    .description { color: #475569; font-size: 13px; line-height: 1.5; margin-bottom: 15px; flex-grow: 1; }
    .btn-container { display: flex; gap: 8px; margin-top: auto; }
    .contact-btn {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 700;
        color: white !important;
    }
    .btn-mail { background-color: #1e3a8a; }
    .btn-ws { background-color: #25d366; }
    </style>
""", unsafe_allow_html=True)

# 3. Función Robusta para cargar datos
@st.cache_data
def load_data():
    file_path = 'propuestas.csv'
    if not os.path.exists(file_path): return None
    
    try:
        # Leemos el CSV tratando de ignorar errores de encoding
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip() # Limpiar espacios
        
        # BUSCADOR INTELIGENTE DE COLUMNAS (Para evitar el KeyError)
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
            
        df = df.rename(columns=new_cols)
        
        # Verificar que las columnas críticas existan, si no, crearlas vacías para que no explote
        for critical in ['Artista', 'Propuesta', 'Eje', 'Disciplina', 'Descripción', 'Mail', 'WhatsApp']:
            if critical not in df.columns:
                df[critical] = "No disponible"
                
        return df
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return None

# 4. Ejecución de la App
df = load_data()

if df is None:
    st.error("### ❌ No se encontró 'propuestas.csv'")
    st.info("Asegúrate de que el nombre del archivo en GitHub sea exactamente ese.")
else:
    # --- FILTROS SIDEBAR ---
    st.sidebar.header("🎯 Filtros")
    
    ejes = sorted(df['Eje'].unique().tolist())
    eje_sel = st.sidebar.multiselect("Eje Temático", ejes)
    
    discs = sorted(df['Disciplina'].unique().tolist())
    disc_sel = st.sidebar.multiselect("Disciplina", discs)
    
    # --- CUERPO PRINCIPAL ---
    st.title("🎨 Propuestas Culturales 2026")
    search = st.text_input("🔍 Buscar artista o propuesta...", placeholder="Ej: Museo...")

    # Filtrado lógico
    f_df = df.copy()
    if eje_sel: f_df = f_df[f_df['Eje'].isin(eje_sel)]
    if disc_sel: f_df = f_df[f_df['Disciplina'].isin(disc_sel)]
    if search:
        f_df = f_df[f_df['Artista'].astype(str).str.contains(search, case=False) | 
                    f_df['Propuesta'].astype(str).str.contains(search, case=False)]

    # --- RENDERIZADO ---
    if f_df.empty:
        st.info("No hay resultados para esta búsqueda.")
    else:
        st.write(f"Viendo {len(f_df)} propuestas")
        cols = st.columns(3)
        
        for i, row in f_df.reset_index().iterrows():
            # Limpiar WhatsApp
            ws = str(row['WhatsApp']).replace('+', '').replace(' ', '').split('.')[0]
            
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
                        <div class="btn-container">
                            <a href="mailto:{row['Mail']}" class="contact-btn btn-mail">📧 Mail</a>
                            <a href="https://wa.me/{ws}" target="_blank" class="contact-btn btn-ws">💬 WhatsApp</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Museo del Hambre - 2026")
