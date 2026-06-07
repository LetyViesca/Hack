import streamlit as st

MENU_ITEMS = [
    {"name": "Dashboard", "path": "app", "icon": "📊"},
    {"name": "Clientes en Riesgo", "path": "01_Clientes_Riesgo", "icon": "⚠️"},
    {"name": "Análisis Territorial", "path": "02_Analisis_Territorial", "icon": "🗺️"},
    {"name": "Análisis Coolers", "path": "03_Analisis_Coolers", "icon": "🧊"},
    {"name": "Predicción Individual", "path": "04_Prediccion_Individual", "icon": "🎯"},
    {"name": "Recomendaciones", "path": "05_Recomendaciones", "icon": "🧩"},
]

def render_sidebar(active_page: str) -> None:
    st.sidebar.markdown(
        "<div style='padding: 10px 0px;'><h3 style='margin:0; font-size:1.1rem; opacity:0.8;'>Navegación</h3></div>", 
        unsafe_allow_html=True
    )
    
    for item in MENU_ITEMS:
        active_class = "active" if item["name"] == active_page else ""
        
        # En Streamlit multipágina nativo, apuntamos al nombre del archivo directamente si está expuesto
        link = f"/{item['path']}" if item['path'] != "app" else "/"
        
        st.sidebar.markdown(
            f"<a href='{link}' target='_self' class='sidebar-link {active_class}'>"
            f"<span class='icon-chip'>{item['icon']}</span>"
            f"<span>{item['name']}</span>"
            f"</a>",
            unsafe_allow_html=True,
        )