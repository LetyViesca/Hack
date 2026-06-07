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
    page_title="Análisis de Coolers",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Análisis Coolers")
    render_header(
        title="Análisis de Coolers",
        subtitle="Evalúa la influencia de los coolers en el churn de clientes.",
    )

    clients = [f"C-{2000 + i}" for i in range(1, 61)]
    territorios = ["Norte", "Centro", "Sur"]
    canales = ["Retail", "Digital", "Distribuidor"]

    client_data = pd.DataFrame(
        {
            "Cliente": clients,
            "Territorio": [territorios[i % len(territorios)] for i in range(len(clients))],
            "Canal": [canales[i % len(canales)] for i in range(len(clients))],
            "Coolers": [i % 4 for i in range(len(clients))],
            "Score Churn": [95 - (i % 40) for i in range(len(clients))],
            "Ventas": [150000 - i * 1800 for i in range(len(clients))],
        }
    )
    client_data["Nivel Riesgo"] = client_data["Score Churn"].apply(
        lambda value: "Alto" if value >= 65 else "Medio" if value >= 40 else "Bajo"
    )
    client_data["Clientes con Cooler"] = client_data["Coolers"].apply(lambda x: "Con Cooler" if x > 0 else "Sin Cooler")
    client_data["Ventas"] = client_data["Ventas"].apply(lambda x: f"${x:,.0f}")

    metrics = [
        {
            "title": "Total Coolers",
            "value": str(client_data["Coolers"].sum()),
            "delta": "+12%",
            "trend": "up",
            "icon": "🧊",
            "description": "Inventario de equipos instalados.",
        },
        {
            "title": "Clientes con Cooler",
            "value": str((client_data["Coolers"] > 0).sum()),
            "delta": "+7%",
            "trend": "up",
            "icon": "📦",
            "description": "Clientes con presencia de cooler.",
        },
        {
            "title": "Clientes sin Cooler",
            "value": str((client_data["Coolers"] == 0).sum()),
            "delta": "-3%",
            "trend": "down",
            "icon": "🚫",
            "description": "Clientes sin instalación activa.",
        },
        {
            "title": "Riesgo Promedio",
            "value": f"{client_data['Score Churn'].mean():.1f}%",
            "delta": "+4.2%",
            "trend": "up",
            "icon": "⚠️",
            "description": "Promedio del score de churn.",
        },
    ]

    st.markdown("<div class='section-title'>KPIs de Coolers</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Métricas esenciales para el análisis de equipos y riesgo.</div>", unsafe_allow_html=True)
    row = st.columns(4, gap="large")
    for column, metric in zip(row, metrics):
        with column:
            render_kpi_card(
                title=metric["title"],
                value=metric["value"],
                delta=metric["delta"],
                trend=metric["trend"],
                icon=metric["icon"],
                description=metric["description"],
            )

    st.markdown("---")

    st.markdown("<div class='section-title'>Clientes con Cooler vs Sin Cooler</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Proporción de clientes con instalación activa frente a sin instalación.</div>", unsafe_allow_html=True)
    fig_donut = px.pie(
        client_data,
        names="Clientes con Cooler",
        hole=0.55,
        color="Clientes con Cooler",
        color_discrete_map={"Con Cooler": "#3B82F6", "Sin Cooler": "#F59E0B"},
        template="plotly_dark",
    )
    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    fig_donut.update_layout(height=420)
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Riesgo según Coolers</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Relación entre cantidad de coolers y score de churn promedio.</div>", unsafe_allow_html=True)
    bar_data = client_data.groupby("Coolers")["Score Churn"].mean().reset_index()
    fig_bar = px.bar(
        bar_data,
        x="Coolers",
        y="Score Churn",
        text="Score Churn",
        labels={"Score Churn": "Riesgo Promedio (%)", "Coolers": "Coolers"},
        color="Score Churn",
        color_continuous_scale="RdYlGn_r",
        template="plotly_dark",
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Coolers vs Score de Churn</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Distribución del riesgo en función de la cantidad de coolers.</div>", unsafe_allow_html=True)
    fig_scatter = px.scatter(
        client_data,
        x="Coolers",
        y="Score Churn",
        color="Nivel Riesgo",
        color_discrete_map={"Alto": "#EF4444", "Medio": "#F59E0B", "Bajo": "#22C55E"},
        hover_data={"Cliente": True, "Territorio": True, "Canal": True, "Ventas": True},
        labels={"Score Churn": "Score Churn (%)", "Coolers": "Coolers"},
        size="Score Churn",
        template="plotly_dark",
    )
    fig_scatter.update_layout(height=520)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    st.markdown(
        "<div class='statement-card'>"
        "<h4>Hallazgos Clave</h4>"
        "<ul style='margin:0; padding-left:18px; color:#94A3B8;'>"
        "<li>Los clientes con 1 o más coolers tienen un score de churn significativo.</li>"
        "<li>El riesgo promedio crece junto al número de coolers instalados.</li>"
        "<li>Los clientes con 3 coolers deben figurar en el plan inmediato de retención.</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("<div class='section-title'>Tabla Resumen</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Vista detallada de la correlación de coolers y churn.</div>", unsafe_allow_html=True)
    st.dataframe(
        client_data[["Cliente", "Territorio", "Canal", "Coolers", "Score Churn", "Nivel Riesgo", "Ventas"]]
        .sort_values(["Coolers", "Score Churn"], ascending=[False, False]),
        use_container_width=True,
        height=420,
    )

    st.markdown("---")
    st.markdown(
        "#### Conclusión Estratégica"
        "\n- El análisis sugiere que los coolers son un punto crítico de atención en la retención."
        "\n- Priorizar acciones concretas en clientes con alto número de coolers."
        "\n- Utilizar estos hallazgos para diseñar paquetes de servicio y fidelización."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
