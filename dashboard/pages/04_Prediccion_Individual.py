import os
import sys
import streamlit as st
import plotly.graph_objects as go

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from components.theme import apply_theme, get_theme_config, get_plotly_template
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_card import render_kpi_card

st.set_page_config(
    page_title="Predicción Individual | Rose Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    theme = get_theme_config()
    render_sidebar(active_page="Predicción Individual")
    render_header(
        title="Predicción Individual",
        subtitle="Simulación bajo demanda del riesgo de abandono para clientes específicos.",
    )

    form_col, result_col = st.columns([1, 1], gap="large")

    with form_col:
        st.markdown("<div class='section-title'>Parámetros del Cliente</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Configura los atributos operativos del cliente para calcular el riesgo en tiempo real.</div>", unsafe_allow_html=True)
        
        # Formulario integrado elegantemente con CSS
        with st.form(key="client_risk_form", clear_on_submit=False):
            territorio = st.selectbox("Territorio de Operación", ["Norte", "Centro", "Sur"])
            canal = st.selectbox("Canal Comercial", ["Retail", "Digital", "Distribuidor"])
            ventas = st.number_input("Facturación Anualizada ($)", min_value=0, value=85000, step=5000)
            coolers = st.slider("Unidades de Coolers en Comodato", min_value=0, max_value=5, value=1)
            antiguedad = st.slider("Antigüedad del Cliente (Años)", min_value=0, max_value=15, value=4)
            frecuencia = st.selectbox("Frecuencia de Surtido", ["Semanal", "Quincenal", "Mensual"])
            
            submit_button = st.form_submit_button("Ejecutar Modelo Predictivo")

    with result_col:
        st.markdown("<div class='section-title'>Diagnóstico Prescriptivo</div>", unsafe_allow_html=True)
        
        if submit_button:
            # Algoritmo de simulación determinista refinado
            score = 36
            score += 12 if territorio == "Sur" else 4 if territorio == "Norte" else 6
            score += 8 if canal == "Distribuidor" else 3 if canal == "Digital" else 0
            score += 8 if ventas < 80000 else -4 if ventas > 130000 else 0
            score += coolers * 6
            score += 6 if antiguedad < 2 else 2 if antiguedad < 5 else -3
            score += {"Semanal": 0, "Quincenal": 6, "Mensual": 12}[frecuencia]
            score = min(max(score, 5), 98)
            
            nivel = "Alto" if score >= 70 else "Medio" if score >= 45 else "Bajo"
            color_alerta = "#FF2D6F" if nivel == "Alto" else "#F59E0B" if nivel == "Medio" else "#10B981"
            icon_alerta = "🚨" if nivel == "Alto" else "📊" if nivel == "Medio" else "✅"

            # Gráfico de Aguja Profesional Avanzado
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    number={"suffix": "%", "font": {"color": theme["text"], "size": 36, "family": "Inter"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": theme["text_secondary"], "tickwidth": 1},
                        "bar": {"color": color_alerta},
                        "bgcolor": "rgba(255,255,255,0.03)",
                        "steps": [
                            {"range": [0, 45], "color": "rgba(16, 185, 129, 0.15)"},
                            {"range": [45, 70], "color": "rgba(245, 158, 11, 0.15)"},
                            {"range": [70, 100], "color": "rgba(255, 45, 111, 0.15)"},
                        ],
                    },
                )
            )
            gauge.update_layout(
                template=get_plotly_template(), 
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                margin=dict(l=30, r=30, t=40, b=0), 
                height=260
            )
            st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})

            # Tarjeta de Recomendación de Salida
            recommendation = (
                "Plan de Retención Prioritario: Desplegar bonificación por volumen e intervención gerencial."
                if nivel == "Alto"
                else "Plan de Monitoreo Preventivo: Ejecutar llamada de servicio y verificar estatus de activos."
                if nivel == "Medio"
                else "Flujo Estándar: Mantener la estrategia actual de atención periódica."
            )
            
            st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid {color_alerta}; margin-top:15px; padding: 16px;'>
                <div style='display:flex; align-items:center; gap:10px; margin-bottom:6px;'>
                    <span style='font-size:1.2rem;'>{icon_alerta}</span>
                    <strong style='color:{theme["text"]}; font-size:1.05rem;'>Riesgo Detectado: {nivel.upper()}</strong>
                </div>
                <p style='margin:0; color:{theme["text_secondary"]}; font-size:0.92rem; line-height:1.5;'>{recommendation}</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info("Por favor complete los campos de la izquierda y presione 'Ejecutar Modelo Predictivo' para visualizar el análisis de riesgo.")

except Exception as e:
    st.error(f"Error crítico en interfaz predictiva: {e}")