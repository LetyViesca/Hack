import streamlit as st
from datetime import datetime

MENU_ITEMS = [
    {"name": "Dashboard", "path": "dashboard/app.py", "icon": "📊"},
    {"name": "Clientes en Riesgo", "path": "dashboard/pages/01_Clientes_Riesgo.py", "icon": "⚠️"},
    {"name": "Análisis Territorial", "path": "dashboard/pages/02_Analisis_Territorial.py", "icon": "🗺️"},
    {"name": "Análisis Coolers", "path": "dashboard/pages/03_Analisis_Coolers.py", "icon": "🧊"},
    {"name": "Predicción Individual", "path": "dashboard/pages/04_Prediccion_Individual.py", "icon": "🎯"},
    {"name": "Recomendaciones", "path": "dashboard/pages/05_Recomendaciones.py", "icon": "🧩"},
]


def render_sidebar(active_page: str) -> None:
    st.sidebar.markdown("<div style='padding-top:6px;'></div>", unsafe_allow_html=True)
    for item in MENU_ITEMS:
        active_class = "active" if item["name"] == active_page else ""
        link = f"?page={item['path']}"
        st.sidebar.markdown(
            f"<a href='{link}' class='sidebar-link {active_class}' style='display:flex; align-items:center; gap:12px; padding:14px 16px;'>"
            f"<span class='icon-chip'>{item['icon']}</span><span style='font-weight:700; font-size:0.98rem;'>{item['name']}</span>"
            f"</a>",
            unsafe_allow_html=True,
        )
    st.sidebar.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='color:#CBD5E1; font-size:0.84rem; padding:0 16px;'>Navegación ejecutiva - selecciona un área de análisis.</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
