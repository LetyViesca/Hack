import os
import sys
import streamlit as st
import plotly.graph_objects as go

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from components.theme import apply_theme
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_card import render_kpi_card

st.set_page_config(
    page_title="Predicción Individual",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    render_sidebar(active_page="Predicción Individual")
    render_header(
        title="Predicción Individual",
        subtitle="Simula el riesgo de churn de un cliente específico.",
    )

    form_col, result_col = st.columns([1, 1], gap="large")

    with form_col:
        st.markdown("<div class='glass-card' style='padding:24px;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Formulario de Evaluación</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Ingresa los atributos clave del cliente.</div>", unsafe_allow_html=True)
        with st.form(key="client_risk_form"):
            territorio = st.selectbox("Territorio", ["Norte", "Centro", "Sur"])
            canal = st.selectbox("Canal", ["Retail", "Digital", "Distribuidor"])
            ventas = st.number_input("Ventas", min_value=0, value=85000, step=5000)
            coolers = st.slider("Coolers", min_value=0, max_value=5, value=1)
            antiguedad = st.slider("Antigüedad Cliente (años)", min_value=0, max_value=15, value=4)
            frecuencia = st.selectbox("Frecuencia Compra", ["Semanal", "Quincenal", "Mensual"])
            submit_button = st.form_submit_button("Calcular Riesgo")
        st.markdown("</div>", unsafe_allow_html=True)

    with result_col:
        st.markdown("<div class='glass-card' style='padding:24px;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Resultado</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Riesgo estimado y guía de acción.</div>", unsafe_allow_html=True)
        if submit_button:
            score = 36
            score += 10 if territorio == "Sur" else 4 if territorio == "Norte" else 6
            score += 8 if canal == "Distribuidor" else 3 if canal == "Digital" else 0
            score += 8 if ventas < 80000 else -3 if ventas > 130000 else 0
            score += coolers * 6
            score += 6 if antiguedad < 2 else 2 if antiguedad < 5 else -2
            score += {"Semanal": 0, "Quincenal": 5, "Mensual": 10}[frecuencia]
            score = min(max(score, 5), 98)
            nivel = "Alto" if score >= 70 else "Medio" if score >= 45 else "Bajo"
            color = "#22C55E" if nivel == "Bajo" else "#F59E0B" if nivel == "Medio" else "#EF4444"
            trend_icon = "📊" if nivel == "Medio" else "⚠️" if nivel == "Alto" else "✅"

            st.markdown(f"<p class='metric-label'>Score de Churn</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value'>{score:.0f}%</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-label'>Nivel de Riesgo</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-value' style='color:{color};'>{nivel}</p>", unsafe_allow_html=True)

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    number={"suffix": "%", "font": {"color": "#FFFFFF", "size": 32}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                        "bar": {"color": color},
                        "bgcolor": "rgba(255,255,255,0.05)",
                        "steps": [
                            {"range": [0, 45], "color": "#22C55E"},
                            {"range": [45, 70], "color": "#F59E0B"},
                            {"range": [70, 100], "color": "#EF4444"},
                        ],
                    },
                )
            )
            gauge.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=40, b=0), height=360)
            st.plotly_chart(gauge, use_container_width=True)

            recommendation = (
                "Acción: Activar un plan de retención urgente con incentivo de fidelidad."
                if nivel == "Alto"
                else "Acción: Monitoreo cercano y comunicación proactiva."
                if nivel == "Medio"
                else "Acción: Mantener relación y fortalecer experiencia de cliente."
            )
            st.markdown(f"<div class='statement-card'>{trend_icon} {recommendation}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='detail-label'>Complete el formulario y presione Calcular Riesgo para obtener el score.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "#### Mensaje Ejecutivo"
        "\n- La evaluación individual permite validar hipótesis de riesgo antes de ejecutar campañas."
        "\n- Use este modelo como guía rápida de decisiones comerciales."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
