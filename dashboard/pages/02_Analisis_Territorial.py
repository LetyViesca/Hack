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
    page_title="Análisis Territorial",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Análisis Territorial")
    render_header(
        title="Análisis Territorial",
        subtitle="Descubre regiones con mayor riesgo y su impacto en churn.",
    )

    territory_data = pd.DataFrame(
        {
            "Territorio": ["Norte", "Centro", "Sur"],
            "Churn": [6.8, 5.4, 10.2],
            "Clientes": [6200, 5200, 7050],
            "Ingresos": [1420000, 980000, 1280000],
            "Riesgo": [82, 68, 94],
            "Lat": [25.0, 19.4, 15.8],
            "Lon": [-100.0, -99.1, -92.9],
        }
    )

    render_kpi_card(
        title="Territorios Analizados",
        value=str(len(territory_data)),
        delta="",
        trend="up",
        icon="🌍",
        description="Zonas en evaluación para acción regional.",
    )
    render_kpi_card(
        title="Churn Promedio",
        value=f"{territory_data['Churn'].mean():.1f}%",
        delta="-0.4%",
        trend="down",
        icon="📊",
        description="Tendencia promedio de pérdida por región.",
    )
    render_kpi_card(
        title="Territorio Crítico",
        value=territory_data.loc[territory_data["Churn"].idxmax(), "Territorio"],
        delta="",
        trend="up",
        icon="🔥",
        description="Territorio con mayor urgencia de retención.",
    )

    st.markdown("---")

    st.markdown("<div class='section-title'>Mapa de Riesgo Territorial</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Geografía simulada con los territorios más expuestos.</div>", unsafe_allow_html=True)
    fig_map = px.scatter_geo(
        territory_data,
        lat="Lat",
        lon="Lon",
        size="Clientes",
        color="Churn",
        hover_name="Territorio",
        hover_data={"Clientes": True, "Churn": True, "Riesgo": True, "Lat": False, "Lon": False},
        projection="natural earth",
        color_continuous_scale="RdYlGn_r",
        labels={"Churn": "Churn (%)"},
        template="plotly_dark",
    )
    fig_map.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    rank_col, heat_col = st.columns([1, 1], gap="large")

    with rank_col:
        st.markdown("<div class='section-title'>Ranking Territorial</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Ordena las regiones por churn y riesgo.</div>", unsafe_allow_html=True)
        ranking = territory_data.sort_values("Churn", ascending=False)
        st.dataframe(ranking[["Territorio", "Churn", "Riesgo", "Clientes"]], use_container_width=True, height=380)

    with heat_col:
        st.markdown("<div class='section-title'>Heatmap de Riesgo</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Comparativa de métricas clave por territorio.</div>", unsafe_allow_html=True)
        heatmap_values = territory_data.set_index("Territorio")[['Churn', 'Clientes', 'Riesgo']].T
        fig_heat = px.imshow(
            heatmap_values,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdYlGn_r",
            labels={"x": "Territorio", "y": "Métrica", "color": "Valor"},
            template="plotly_dark",
        )
        fig_heat.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Territorio vs Churn %</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Comparativa clara de la probabilidad de pérdida por región.</div>", unsafe_allow_html=True)
    fig_bar = px.bar(
        territory_data,
        x="Territorio",
        y="Churn",
        text="Churn",
        color="Territorio",
        color_discrete_map={"Norte": "#3B82F6", "Centro": "#60A5FA", "Sur": "#EF4444"},
        labels={"Churn": "Churn (%)"},
        template="plotly_dark",
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    territory_data["Ingresos"] = territory_data["Ingresos"].apply(lambda x: f"${x:,.0f}")
    st.markdown("<div class='section-title'>Tabla Resumen Territorial</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Indicadores operativos y de impacto por territorio.</div>", unsafe_allow_html=True)
    st.dataframe(territory_data[["Territorio", "Churn", "Clientes", "Ingresos", "Riesgo"]], use_container_width=True, height=360)

    st.markdown("---")
    st.markdown(
        "#### Conclusión Ejecutiva"
        "\n- El Sur es el territorio crítico con churn de doble dígito."
        "\n- Centro es el mejor referente para mitigación regional."
        "\n- Monitorear semanalmente la operación para reducir el ritmo de abandono."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
