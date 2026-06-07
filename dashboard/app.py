import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_card import render_kpi_card

st.set_page_config(
    page_title="Churn Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Dashboard")
    render_header(
        title="Dashboard Ejecutivo",
        subtitle="Visión global del churn con métricas clave y señales de acción ejecutiva.",
    )

    kpis = [
        {
            "title": "Base de Clientes",
            "value": "18,450",
            "delta": "+3.2%",
            "trend": "up",
            "icon": "👥",
            "description": "Crecimiento en la base total de clientes.",
        },
        {
            "title": "Tasa de Churn",
            "value": "7.8%",
            "delta": "-0.6%",
            "trend": "down",
            "icon": "📉",
            "description": "Reducción estable en la tasa de abandono.",
        },
        {
            "title": "Clientes Alto Riesgo",
            "value": "2,210",
            "delta": "+14.8%",
            "trend": "up",
            "icon": "⚠️",
            "description": "Crecimiento en clientes prioritarios.",
        },
        {
            "title": "Ingresos en Riesgo",
            "value": ".2M",
            "delta": "+8.5%",
            "trend": "up",
            "icon": "💰",
            "description": "Ingresos que requieren mitigación inmediata.",
        },
    ]

    risk_factors = pd.DataFrame(
        {
            "Factor": ["Caída de Ventas", "Territorio", "Frecuencia de Compra", "Coolers"],
            "Impacto": [88, 75, 63, 48],
        }
    )

    risk_distribution = pd.DataFrame(
        {
            "Nivel": ["Bajo", "Medio", "Alto"],
            "Porcentaje": [34, 43, 23],
        }
    )

    territory_data = pd.DataFrame(
        {
            "Territorio": ["Norte", "Centro", "Sur"],
            "Churn": [6.8, 5.4, 10.2],
            "Clientes": [6200, 5200, 7050],
            "Riesgo": [76, 64, 92],
        }
    )

    critical_clients = pd.DataFrame(
        {
            "Cliente": ["C-1024", "C-2145", "C-3301", "C-4150", "C-5287"],
            "Territorio": ["Sur", "Norte", "Sur", "Centro", "Norte"],
            "Score Churn": [92, 88, 86, 84, 81],
            "Ventas": [120000, 98000, 110000, 95000, 82000],
            "Coolers": [0, 1, 0, 2, 0],
        }
    )
    critical_clients["Nivel Riesgo"] = critical_clients["Score Churn"].apply(
        lambda score: "Alto" if score >= 70 else "Medio"
    )
    critical_clients["Ingresos"] = critical_clients["Ventas"].apply(lambda x: f"${x:,.0f}")

    st.markdown("<div class='section-title'>Métricas Ejecutivas</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Resumen rápido para la dirección y el comité de riesgos.</div>", unsafe_allow_html=True)
    cols = st.columns(4, gap="large")
    for col, metric in zip(cols, kpis):
        with col:
            render_kpi_card(
                title=metric["title"],
                value=metric["value"],
                delta=metric["delta"],
                trend=metric["trend"],
                icon=metric["icon"],
                description=metric["description"],
            )

    st.markdown("---")

    st.markdown("<div class='section-title'>Factores de Riesgo</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Las variables que más influyen en la probabilidad de churn.</div>", unsafe_allow_html=True)
    fig_factors = px.bar(
        risk_factors,
        x="Impacto",
        y="Factor",
        orientation="h",
        text="Impacto",
        labels={"Impacto": "Impacto Relativo", "Factor": "Factor"},
        color="Impacto",
        color_continuous_scale=["#3B82F6", "#0D6EFD"],
        template="plotly_dark",
    )
    fig_factors.update_traces(marker_line_color="#0F172A", marker_line_width=1.5, texttemplate="%{text:.0f}%")
    fig_factors.update_layout(height=400)
    st.plotly_chart(fig_factors, use_container_width=True)

    st.markdown("---")
    row1, row2 = st.columns([1.1, 0.9], gap="large")

    with row1:
        st.markdown("<div class='section-title'>Distribución de Riesgo</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Segmentación de clientes por exposición de churn.</div>", unsafe_allow_html=True)
        fig_risk = px.pie(
            risk_distribution,
            names="Nivel",
            values="Porcentaje",
            hole=0.55,
            color="Nivel",
            color_discrete_map={"Bajo": "#22C55E", "Medio": "#F59E0B", "Alto": "#EF4444"},
            template="plotly_dark",
        )
        fig_risk.update_traces(textposition="inside", textinfo="percent+label")
        fig_risk.update_layout(height=400)
        st.plotly_chart(fig_risk, use_container_width=True)

    with row2:
        st.markdown("<div class='section-title'>Churn por Territorio</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Identifica regiones críticas de retención.</div>", unsafe_allow_html=True)
        fig_territory = px.bar(
            territory_data,
            x="Territorio",
            y="Churn",
            text="Churn",
            labels={"Churn": "Churn (%)"},
            color="Territorio",
            color_discrete_map={"Norte": "#3B82F6", "Centro": "#60A5FA", "Sur": "#EF4444"},
            template="plotly_dark",
        )
        fig_territory.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_territory.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_territory, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Top Clientes Críticos</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Clientes con mayor score de churn y mayor potencial de ingresos.</div>", unsafe_allow_html=True)
    st.dataframe(critical_clients, use_container_width=True, height=420)

    st.markdown("---")

    st.markdown(
        "#### Recomendación Ejecutiva"
        "\n- Enfocar el primer nivel de atención en clientes con score superior a 80%."
        "\n- Coordinar acciones en Sur y Norte para mitigar el riesgo inmediato."
        "\n- Alinear los equipos comerciales con los factores de riesgo clave." 
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
