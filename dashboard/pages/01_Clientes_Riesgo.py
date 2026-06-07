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
    page_title="Clientes en Riesgo",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Clientes en Riesgo")
    render_header(
        title="Clientes en Riesgo",
        subtitle="Prioriza clientes con mayor probabilidad de abandono.",
    )

    clientes = [f"C-{1000 + i}" for i in range(1, 61)]
    territorios = ["Norte", "Centro", "Sur"]
    canales = ["Retail", "Digital", "Distribuidor"]
    ventas = [120000 - i * 1500 for i in range(60)]
    coolers = [i % 4 for i in range(60)]
    score_churn = [98 - i for i in range(60)]

    cliente_data = pd.DataFrame(
        {
            "Cliente": clientes,
            "Territorio": [territorios[i % len(territorios)] for i in range(len(clientes))],
            "Canal": [canales[i % len(canales)] for i in range(len(clientes))],
            "Ventas": ventas,
            "Coolers": coolers,
            "Score Churn": score_churn,
        }
    )
    cliente_data["Nivel Riesgo"] = cliente_data["Score Churn"].apply(
        lambda value: "Alto" if value >= 70 else "Medio" if value >= 45 else "Bajo"
    )
    cliente_data["Score Churn"] = cliente_data["Score Churn"].astype(str) + "%"
    cliente_data["Ventas"] = cliente_data["Ventas"].apply(lambda x: f"${x:,.0f}")

    st.markdown("<div class='section-title'>Filtros Avanzados</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Segmenta y encuentra clientes en riesgo con precisión.</div>", unsafe_allow_html=True)
    filter_col, insight_col = st.columns([1, 1], gap="large")

    with filter_col:
        territory = st.selectbox("Territorio", options=["Todos"] + territorios, index=0)
        canal = st.selectbox("Canal", options=["Todos"] + canales, index=0)
        riesgo = st.selectbox("Nivel de Riesgo", options=["Todos", "Alto", "Medio", "Bajo"], index=0)
        search = st.text_input("Buscar Cliente", value="")

    filtered = cliente_data.copy()
    if territory != "Todos":
        filtered = filtered[filtered["Territorio"] == territory]
    if canal != "Todos":
        filtered = filtered[filtered["Canal"] == canal]
    if riesgo != "Todos":
        filtered = filtered[filtered["Nivel Riesgo"] == riesgo]
    if search:
        filtered = filtered[filtered["Cliente"].str.contains(search, case=False)]

    with insight_col:
        score_mean = filtered["Score Churn"].str.replace("%", "").astype(int).mean() if len(filtered) else 0
        stats = {
            "Clientes Filtrados": len(filtered),
            "Alto Riesgo": len(filtered[filtered["Nivel Riesgo"] == "Alto"]),
            "Promedio Score": f"{score_mean:.1f}%" if len(filtered) else "N/A",
            "Clientes con Cooler": len(filtered[filtered["Coolers"] > 0]),
        }
        for key, value in stats.items():
            render_kpi_card(
                title=key,
                value=str(value),
                delta="",
                trend="up",
                icon="🔎",
                description="",
            )

    st.markdown("---")
    client_col, detail_col = st.columns([1.2, 0.8], gap="large")

    with client_col:
        st.markdown("<div class='section-title'>Top 20 Clientes en Riesgo</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Clientes priorizados por score de churn.</div>", unsafe_allow_html=True)
        filtered["Score Num"] = filtered["Score Churn"].str.replace("%", "").astype(int)
        top20 = filtered.sort_values("Score Num", ascending=False).head(20)
        fig = px.bar(
            top20,
            x="Score Num",
            y="Cliente",
            orientation="h",
            color="Nivel Riesgo",
            color_discrete_map={"Alto": "#EF4444", "Medio": "#F59E0B", "Bajo": "#22C55E"},
            labels={"Score Num": "Score Churn (%)"},
            template="plotly_dark",
        )
        fig.update_layout(height=520, xaxis_title="Score (%)", yaxis_title="Cliente")
        fig.update_traces(texttemplate="%{x}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with detail_col:
        client_choice = st.selectbox("Cliente Seleccionado", options=filtered['Cliente'].tolist() if len(filtered) else ["N/A"])
        if client_choice != "N/A":
            selected = filtered[filtered['Cliente'] == client_choice].iloc[0]
            cliente = selected['Cliente']
            territorio_det = selected['Territorio']
            canal_det = selected['Canal']
            score_det = selected['Score Churn']
            nivel_riesgo_det = selected['Nivel Riesgo']
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-label'>Cliente</p><p class='metric-value'>{cliente}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Territorio</p><p class='detail-value'>{territorio_det}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Canal</p><p class='detail-value'>{canal_det}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Score</p><p class='detail-value'>{score_det}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='detail-label'>Nivel de Riesgo</p><p class='detail-value'>{nivel_riesgo_det}</p>", unsafe_allow_html=True)
            recommendation_text = "Contactar con prioridad" if nivel_riesgo_det == "Alto" else "Monitorear de cerca" if nivel_riesgo_det == "Medio" else "Mantener seguimiento"
            st.markdown(f"<p class='detail-label'>Recomendación</p><p class='detail-value'>{recommendation_text}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No hay clientes seleccionables con los filtros actuales.")

    st.markdown("---")
    st.markdown(
        "#### Notas de usuario"
        "\n- Ajuste los filtros para encontrar rápidamente grupos de clientes con mayor probabilidad de abandono."
        "\n- Utilice el panel de detalle para decisiones de retención enfocadas."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
