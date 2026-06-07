import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_card import render_kpi_card

st.set_page_config(
    page_title="Recomendaciones Estratégicas",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Recomendaciones Estratégicas")
    render_header(
        title="Recomendaciones Estratégicas",
        subtitle="Acciones priorizadas para reducir churn y recuperar clientes.",
    )

    recommendations = pd.DataFrame(
        {
            "Acción": ["Visita comercial", "Descuento", "Reposición de cooler", "Capacitación"],
            "Impacto": [92, 78, 85, 73],
            "Esfuerzo": [70, 55, 60, 45],
            "Prioridad": [1, 2, 3, 4],
            "Clientes Potenciales": [128, 94, 106, 82],
            "Ingresos Recuperables": [320000, 280000, 245000, 190000],
        }
    )

    render_kpi_card(
        title="Clientes Recuperables",
        value="410",
        delta="+8%",
        trend="up",
        icon="👥",
        description="Clientes con potencial de retención inmediata.",
    )
    render_kpi_card(
        title="Ingresos Recuperables",
        value="$1.04M",
        delta="+12%",
        trend="up",
        icon="💵",
        description="Valor económico asociado a clientes recuperables.",
    )
    render_kpi_card(
        title="Acciones Prioritarias",
        value="4",
        delta="",
        trend="up",
        icon="🚀",
        description="Iniciativas clave para la siguiente etapa.",
    )

    st.markdown("---")

    st.markdown("<div class='section-title'>Tarjetas de Recomendaciones</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Actividades ejecutivas propuestas para mitigar el churn.</div>", unsafe_allow_html=True)

    cards = [
        {"title": "Visita comercial", "text": "Intervención presencial para fortalecer relaciones y cerrar acuerdos.", "icon": "🤝"},
        {"title": "Descuento", "text": "Oferta selectiva de precio para retener segmentos críticos.", "icon": "🏷️"},
        {"title": "Reposición de cooler", "text": "Reinstalación enfocada en puntos con mayor incidencia de churn.", "icon": "🧊"},
        {"title": "Capacitación", "text": "Entrenamiento del equipo para mejorar la experiencia de cliente.", "icon": "📚"},
    ]
    cols = st.columns(4, gap="large")
    for column, card in zip(cols, cards):
        with column:
            st.markdown(
                f"<div class='glass-card' style='padding:24px; min-height:180px;'>"
                f"<div style='display:flex; align-items:center; gap:12px; margin-bottom:16px;'>"
                f"<div class='icon-chip'>{card['icon']}</div>"
                f"<div style='font-size:1rem; font-weight:700; color:#FFFFFF;'>{card['title']}</div>"
                f"</div>"
                f"<p style='color:#94A3B8; margin:0; line-height:1.7;'>{card['text']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.markdown("<div class='section-title'>Matriz Impacto vs Esfuerzo</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Visualiza las iniciativas según valor y complejidad.</div>", unsafe_allow_html=True)
    fig_matrix = px.scatter(
        recommendations,
        x="Esfuerzo",
        y="Impacto",
        text="Acción",
        size="Impacto",
        color="Impacto",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
    )
    fig_matrix.update_traces(textposition="top center")
    fig_matrix.update_layout(height=520)
    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Ranking de Acciones</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Ordena las iniciativas según prioridad estratégica.</div>", unsafe_allow_html=True)
    rank = recommendations.sort_values("Prioridad")
    st.dataframe(rank[["Prioridad", "Acción", "Impacto", "Esfuerzo", "Clientes Potenciales", "Ingresos Recuperables"]], use_container_width=True, height=360)

    st.markdown("---")

    recommendations["Ingresos Recuperables"] = recommendations["Ingresos Recuperables"].apply(lambda x: f"${x:,.0f}")
    st.markdown("<div class='section-title'>Tabla de Priorización</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Modelo operativo para lanzar las acciones de mayor retorno.</div>", unsafe_allow_html=True)
    st.dataframe(recommendations, use_container_width=True, height=340)

    st.markdown("---")

    st.markdown(
        "#### Conclusión Estratégica"
        "\n- Priorizando visitas comerciales y reposición de coolers se maximiza la recuperación."
        "\n- Descuentos deben usarse como complemento táctico con control de margen."
        "\n- Capacitación asegura la escalabilidad de las acciones de retención."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
