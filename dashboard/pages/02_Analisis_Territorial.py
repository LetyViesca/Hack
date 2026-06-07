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
    page_title="Análisis Territorial | Rose Intelligence",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    theme = get_theme_config()
    render_sidebar(active_page="Análisis Territorial")
    render_header(
        title="Análisis Territorial",
        subtitle="Identificación macro-geográfica del riesgo y concentración del churn.",
    )

    territory_data = pd.DataFrame({
        "Territorio": ["Norte", "Centro", "Sur"],
        "Churn": [6.8, 5.4, 10.2],
        "Clientes": [6200, 5200, 7050],
        "Ingresos": [1420000, 980000, 1280000],
        "Riesgo": [82, 68, 94],
        "Lat": [25.0, 19.4, 15.8],
        "Lon": [-100.0, -99.1, -92.9],
    })

    # Fila horizontal de KPIs Mandatorios
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        render_kpi_card(title="Territorios Analizados", value=str(len(territory_data)), icon="🌍", subtitle="Cobertura total")
    with kpi_cols[1]:
        render_kpi_card(title="Churn Promedios", value=f"{territory_data['Churn'].mean():.1f}%", delta=-0.4, icon="📊", subtitle="Vs. mes anterior")
    with kpi_cols[2]:
        critical_zone = territory_data.loc[territory_data["Churn"].idxmax(), "Territorio"]
        render_kpi_card(title="Foco de Atención Crítico", value=critical_zone, icon="🔥", subtitle="Zona de máxima pérdida", color="#FF2D6F")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Vista Geográfica Completa
    st.markdown("<div class='section-title'>Distribución Geográfica del Churn</div>", unsafe_allow_html=True)
    fig_map = px.scatter_geo(
        territory_data,
        lat="Lat",
        lon="Lon",
        size="Clientes",
        color="Churn",
        hover_name="Territorio",
        hover_data={"Clientes": True, "Churn": True, "Riesgo": True, "Lat": False, "Lon": False},
        projection="natural earth",
        color_continuous_scale="Blured",
        template=get_plotly_template(),
    )
    fig_map.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Gráficos Analíticos Auxiliares
    rank_col, heat_col = st.columns([1, 1], gap="large")

    with rank_col:
        st.markdown("<div class='section-title'>Riesgo de Churn Relativo por Zona</div>", unsafe_allow_html=True)
        fig_bar = px.bar(
            territory_data,
            x="Territorio",
            y="Churn",
            text="Churn",
            color="Territorio",
            color_discrete_map={"Norte": "#FF5C8A", "Centro": "#F9A8D4", "Sur": "#FF2D6F"},
            template=get_plotly_template(),
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_bar.update_layout(height=320, showlegend=False, yaxis_title="Churn %", xaxis_title=None)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with heat_col:
        st.markdown("<div class='section-title'>Matriz Multimétrica de Riesgo</div>", unsafe_allow_html=True)
        heatmap_values = territory_data.set_index("Territorio")[['Churn', 'Riesgo']].T
        fig_heat = px.imshow(
            heatmap_values,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            template=get_plotly_template(),
        )
        fig_heat.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Tabla Resumen Gerencial
    st.markdown("<div class='section-title'>Auditoría Operativa Territorial</div>", unsafe_allow_html=True)
    df_styled = territory_data.copy()
    df_styled["Ingresos"] = df_styled["Ingresos"].apply(lambda x: f"${x:,.0f}")
    df_styled["Churn"] = df_styled["Churn"].apply(lambda x: f"{x}%")
    st.dataframe(
        df_styled[["Territorio", "Churn", "Clientes", "Ingresos", "Riesgo"]], 
        use_container_width=True, 
        height=180
    )

except Exception as e:
    st.error(f"Error cargando el layout: {e}")