import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from components.theme import apply_theme, get_theme_config, get_plotly_template
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_card import render_kpi_card

st.set_page_config(
    page_title="Recomendaciones Estratégicas | Rose Intelligence",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    theme = get_theme_config()
    render_sidebar(active_page="Recomendaciones")
    render_header(
        title="Recomendaciones Estratégicas",
        subtitle="Acciones y planes tácticos priorizados por retorno económico estimado.",
    )

    recommendations = pd.DataFrame({
        "Acción": ["Visita Comercial Directa", "Descuento Táctico", "Reposición de Cooler", "Capacitación de Canal"],
        "Impacto": [92, 78, 85, 73],
        "Esfuerzo": [70, 55, 60, 45],
        "Prioridad": [1, 2, 3, 4],
        "Clientes Potenciales": [128, 94, 106, 82],
        "Ingresos Recuperables": [320000, 280000, 245000, 190000],
    })

    # Fila de métricas agregadas
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        render_kpi_card(title="Pool Global de Clientes Recuperables", value="410", delta=8.0, trend="up", icon="👥", subtitle="Segmento Target")
    with kpi_cols[1]:
        render_kpi_card(title="Ingreso Total en Riesgo Mitigable", value="$1.04M", delta=12.0, trend="up", icon="💵", subtitle="Valor de recuperación", color="#10B981")
    with kpi_cols[2]:
        render_kpi_card(title="Iniciativas Estratégicas Clave", value="4", icon="🚀", subtitle="Foco operativo")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Bloques de iniciativas tácticas en Columnas Nativas Limpias
    st.markdown("<div class='section-title'>Matriz de Iniciativas Inmediatas</div>", unsafe_allow_html=True)
    cards = [
        {"title": "Visita Comercial Directa", "text": "Intervención presencial corporativa para renovación de contratos de exclusividad.", "icon": "🤝"},
        {"title": "Descuento Táctico", "text": "Ajuste temporal sobre margen en familias críticas para frenar la migración.", "icon": "🏷️"},
        {"title": "Reposición de Cooler", "text": "Sustitución física de activos obsoletos en puntos identificados de alta pérdida.", "icon": "🧊"},
        {"title": "Capacitación de Canal", "text": "Despliegue de consultoría operativa al distribuidor para optimizar la rotación de producto.", "icon": "📚"},
    ]
    
    card_cols = st.columns(4)
    for index, card in enumerate(cards):
        with card_cols[index]:
            st.markdown(f"""
            <div class='glass-card' style='min-height:160px; padding:18px;'>
                <div style='display:flex; align-items:center; gap:10px; margin-bottom:12px;'>
                    <div class='icon-chip' style='width:30px; height:30px; font-size:1rem;'>{card['icon']}</div>
                    <span style='font-weight:700; color:{theme["text"]}; font-size:0.95rem;'>{card['title']}</span>
                </div>
                <p style='color:{theme["text_secondary"]}; margin:0; line-height:1.5; font-size:0.88rem;'>{card['text']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Matriz Cuadrante Eficiencia
    st.markdown("<div class='section-title'>Análisis de Eficiencia: Impacto vs Esfuerzo</div>", unsafe_allow_html=True)
    fig_matrix = px.scatter(
        recommendations,
        x="Esfuerzo",
        y="Impacto",
        text="Acción",
        size="Clientes Potenciales",
        color="Impacto",
        color_continuous_scale="Viridis",
        template=get_plotly_template(),
    )
    fig_matrix.update_traces(textposition="top center", marker=dict(opacity=0.85))
    fig_matrix.update_layout(height=360, margin=dict(t=30, b=10))
    st.plotly_chart(fig_matrix, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Tabla de Priorización Corporativa
    st.markdown("<div class='section-title'>Priorización del Portafolio de Proyectos</div>", unsafe_allow_html=True)
    df_output = recommendations.copy()
    df_output["Ingresos Recuperables"] = df_output["Ingresos Recuperables"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(
        df_output.sort_values("Prioridad"), 
        use_container_width=True, 
        height=180
    )

except Exception as e:
    st.error(f"Error procesando recomendaciones estratégicas: {e}")