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
    page_title="Análisis de Coolers | Rose Intelligence",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    theme = get_theme_config()
    render_sidebar(active_page="Análisis Coolers")
    render_header(
        title="Análisis de Coolers",
        subtitle="Evaluación del impacto del parque de activos fríos instalados sobre la fidelidad.",
    )

    # Dataset Generator
    clients = [f"C-{2000 + i}" for i in range(1, 61)]
    territorios = ["Norte", "Centro", "Sur"]
    canales = ["Retail", "Digital", "Distribuidor"]

    client_data = pd.DataFrame({
        "Cliente": clients,
        "Territorio": [territorios[i % len(territorios)] for i in range(len(clients))],
        "Canal": [canales[i % len(canales)] for i in range(len(clients))],
        "Coolers": [i % 4 for i in range(len(clients))],
        "Score Churn": [95 - (i % 40) for i in range(len(clients))],
        "Ventas": [150000 - i * 1800 for i in range(len(clients))],
    })
    client_data["Nivel Riesgo"] = client_data["Score Churn"].apply(
        lambda value: "Alto" if value >= 65 else "Medio" if value >= 40 else "Bajo"
    )
    client_data["Estado de Activo"] = client_data["Coolers"].apply(lambda x: "Con Cooler Asignado" if x > 0 else "Sin Cooler")

    # Layout de KPIs en Fila Distribuida Correctamente
    st.markdown("<div class='section-title'>Estado Global de Equipos</div>", unsafe_allow_html=True)
    row = st.columns(4)
    with row[0]:
        render_kpi_card(title="Total Coolers Desplegados", value=str(client_data["Coolers"].sum()), icon="🧊", subtitle="Inventario en campo")
    with row[1]:
        render_kpi_card(title="Clientes Cubiertos", value=str((client_data["Coolers"] > 0).sum()), delta=7.0, trend="up", icon="📦", subtitle="Con presencia física")
    with row[2]:
        render_kpi_card(title="Clientes Desprotegidos", value=str((client_data["Coolers"] == 0).sum()), delta=-3.0, trend="down", icon="🚫", subtitle="Sin activos asignados")
    with row[3]:
        render_kpi_card(title="Riesgo Promedio General", value=f"{client_data['Score Churn'].mean():.1f}%", icon="⚠️", subtitle="Probabilidad global")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Distribución y Análisis Gráfico
    viz_left, viz_right = st.columns([1, 1], gap="large")

    with viz_left:
        st.markdown("<div class='section-title'>Penetración de Activos Fríos</div>", unsafe_allow_html=True)
        fig_donut = px.pie(
            client_data,
            names="Estado de Activo",
            hole=0.6,
            color="Estado de Activo",
            color_discrete_map={"Con Cooler Asignado": "#FF2D6F", "Sin Cooler": "rgba(255,255,255,0.15)"},
            template=get_plotly_template(),
        )
        fig_donut.update_traces(textposition="outside", textinfo="percent+label")
        fig_donut.update_layout(height=340, margin=dict(t=20, b=20, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with viz_right:
        st.markdown("<div class='section-title'>Riesgo Churn Medio por Densidad de Coolers</div>", unsafe_allow_html=True)
        bar_data = client_data.groupby("Coolers")["Score Churn"].mean().reset_index()
        fig_bar = px.bar(
            bar_data,
            x="Coolers",
            y="Score Churn",
            text="Score Churn",
            labels={"Score Churn": "Riesgo Promedio (%)", "Coolers": "Cantidad de Coolers"},
            template=get_plotly_template(),
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_color="#FF5C8A")
        fig_bar.update_layout(height=340, yaxis_title="Riesgo Promedio %", xaxis_title="Coolers por Cliente")
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Hallazgos Ejecutivos Estilizados
    st.markdown(f"""
    <div class='statement-card' style='border-left: 4px solid #FF2D6F; background:{theme["card"]}; padding:20px; border-radius:12px;'>
        <h4 style='margin:0 0 8px 0; color:#FF2D6F; font-weight:700;'>Correlación Crítica Hallada</h4>
        <ul style='margin:0; padding-left:20px; color:{theme["text_secondary"]}; line-height:1.6;'>
            <li>Los clientes con alta concentración de activos fríos (3 o más) registran repuntes severos en el score de abandono.</li>
            <li>Se requiere una auditoría técnica en los puntos con mayor volumen para descartar problemas de desabasto u operación de los equipos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Tabla Resumen Operativa Completa
    st.markdown("<div class='section-title'>Matriz Detallada: Clientes y Cobertura</div>", unsafe_allow_html=True)
    st.dataframe(
        client_data[["Cliente", "Territorio", "Canal", "Coolers", "Score Churn", "Nivel Riesgo"]]
        .sort_values(["Coolers", "Score Churn"], ascending=[False, False]),
        use_container_width=True,
        height=320,
    )

except Exception as e:
    st.error(f"Error en la ejecución de la pantalla de activos: {e}")