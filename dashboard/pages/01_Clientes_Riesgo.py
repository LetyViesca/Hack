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
from ml.model_service import predict_risk
from services.data_service import build_analytics_frame, score_to_level

st.set_page_config(
    page_title="Clientes en Riesgo | Rose Intelligence",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    apply_theme()
    theme = get_theme_config()
    render_sidebar(active_page="Clientes en Riesgo")
    render_header(
        title="Clientes en Riesgo",
        subtitle="Prioriza clientes con mayor probabilidad de abandono comercial.",
    )

    scored = predict_risk(build_analytics_frame()).copy()
    cliente_data = scored[["customer_name", "territory", "channel", "total_sales", "num_coolers", "score_risk", "risk_level"]].rename(
        columns={
            "customer_name": "Cliente",
            "territory": "Territorio",
            "channel": "Canal",
            "total_sales": "Ventas",
            "num_coolers": "Coolers",
            "score_risk": "Score Churn",
            "risk_level": "Nivel Riesgo",
        }
    )
    territorios = sorted(cliente_data["Territorio"].dropna().unique().tolist())
    canales = sorted(cliente_data["Canal"].dropna().unique().tolist())

    # Sección de Control Superior (Grid de Filtros)
    st.markdown("<div class='section-title'>Filtros de Segmentación</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Modifica los parámetros para auditar subsegmentos específicos.</div>", unsafe_allow_html=True)
    
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        territory = st.selectbox("Territorio", options=["Todos"] + territorios, index=0)
    with f2:
        canal = st.selectbox("Canal", options=["Todos"] + canales, index=0)
    with f3:
        riesgo = st.selectbox("Nivel de Riesgo", options=["Todos", "Alto", "Medio", "Bajo"], index=0)
    with f4:
        search = st.text_input("Buscar ID Cliente", value="", placeholder="Ej: C-1005")

    # Pipeline de filtrado
    filtered = cliente_data.copy()
    if territory != "Todos":
        filtered = filtered[filtered["Territorio"] == territory]
    if canal != "Todos":
        filtered = filtered[filtered["Canal"] == canal]
    if riesgo != "Todos":
        filtered = filtered[filtered["Nivel Riesgo"] == riesgo]
    if search:
        filtered = filtered[filtered["Cliente"].str.contains(search, case=False)]

    # KPIs dinámicos alineados correctamente en fila horizontal
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    kpi_cols = st.columns(4)
    score_mean = filtered["Score Churn"].mean() if len(filtered) else 0
    
    with kpi_cols[0]:
        render_kpi_card(title="Clientes Filtrados", value=len(filtered), icon="👥", subtitle="Volumen en vista")
    with kpi_cols[1]:
        render_kpi_card(title="Casos Críticos (Alto)", value=len(filtered[filtered["Nivel Riesgo"] == "Alto"]), icon="🚨", subtitle="Prioridad inmediata", color="#FF2D6F")
    with kpi_cols[2]:
        render_kpi_card(title="Promedio Score Churn", value=f"{score_mean:.1f}%", icon="📈", subtitle="Probabilidad promedio")
    with kpi_cols[3]:
        render_kpi_card(title="Equipos en Riesgo", value=filtered[filtered["Coolers"] > 0]["Coolers"].sum(), icon="🧊", subtitle="Coolers expuestos")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Bloque de Análisis Visual e Individual
    client_col, detail_col = st.columns([1.3, 0.7], gap="large")

    with client_col:
        st.markdown("<div class='section-title'>Top 20 Clientes con Mayor Probabilidad de Pérdida</div>", unsafe_allow_html=True)
        if not filtered.empty:
            top20 = filtered.sort_values("Score Churn", ascending=False).head(20)
            
            fig = px.bar(
                top20,
                x="Score Churn",
                y="Cliente",
                orientation="h",
                color="Nivel Riesgo",
                color_discrete_map={"Alto": "#FF2D6F", "Medio": "#F59E0B", "Bajo": "#10B981"},
                labels={"Score Churn": "Score Churn (%)"},
                template=get_plotly_template(),
            )
            fig.update_layout(
                height=480, 
                xaxis_title="Score de Churn (%)", 
                yaxis_title=None,
                yaxis={'categoryorder':'total ascending'}
            )
            fig.update_traces(texttemplate="%{x}%", textposition="outside")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No hay datos disponibles para graficar con los filtros seleccionados.")

    with detail_col:
        st.markdown("<div class='section-title'>Ficha de Acción Individual</div>", unsafe_allow_html=True)
        client_choice = st.selectbox("Seleccione un cliente para auditar:", options=filtered['Cliente'].tolist() if len(filtered) else ["N/A"])
        
        if client_choice != "N/A":
            selected = filtered[filtered['Cliente'] == client_choice].iloc[0]
            recommendation_text = "🔴 Contactar inmediatamente vía Dirección Comercial." if selected['Nivel Riesgo'] == "Alto" else "🟡 Agendar llamada de seguimiento preventivo." if selected['Nivel Riesgo'] == "Medio" else "🟢 Mantener flujo estándar de atención."
            accent_color = "#FF2D6F" if selected['Nivel Riesgo'] == "Alto" else "#F59E0B" if selected['Nivel Riesgo'] == "Medio" else "#10B981"

            # Tarjeta de Detalle Ejecutivo Ultra Limpia
            st.markdown(f"""
            <div class='glass-card' style='border-left: 5px solid {accent_color};'>
                <p class='metric-label' style='margin:0;'>ID CLIENTE</p>
                <h2 style='margin:0 0 15px 0; font-weight:800; color:{theme["text"]};'>{selected['Cliente']}</h2>
                
                <table style='width:100%; border-collapse:collapse; font-size:0.95rem;'>
                    <tr style='border-bottom: 1px solid {theme["border"]};'><td style='padding:8px 0; color:{theme["text_secondary"]};'>Territorio</td><td style='padding:8px 0; text-align:right; font-weight:600;'>{selected['Territorio']}</td></tr>
                    <tr style='border-bottom: 1px solid {theme["border"]};'><td style='padding:8px 0; color:{theme["text_secondary"]};'>Canal de Venta</td><td style='padding:8px 0; text-align:right; font-weight:600;'>{selected['Canal']}</td></tr>
                    <tr style='border-bottom: 1px solid {theme["border"]};'><td style='padding:8px 0; color:{theme["text_secondary"]};'>Ventas Anualizadas</td><td style='padding:8px 0; text-align:right; font-weight:600; color:#10B981;'>${selected['Ventas']:,.0f}</td></tr>
                    <tr style='border-bottom: 1px solid {theme["border"]};'><td style='padding:8px 0; color:{theme["text_secondary"]};'>Coolers Asignados</td><td style='padding:8px 0; text-align:right; font-weight:600;'>{selected['Coolers']} u.</td></tr>
                    <tr style='border-bottom: 1px solid {theme["border"]};'><td style='padding:8px 0; color:{theme["text_secondary"]};'>Score Churn</td><td style='padding:8px 0; text-align:right; font-weight:700; color:#FF2D6F;'>{selected['Score Churn']}%</td></tr>
                </table>
                <div style='margin-top: 20px; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 8px;'>
                    <p class='metric-label' style='margin:0 0 4px 0;'>ESTRATEGIA RECOMENDADA</p>
                    <p style='margin:0; font-weight:600; font-size:0.92rem; color:{theme["text"]};'>{recommendation_text}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Sin registros coincidentes.")

except Exception as e:
    st.error(f"Error operativo en la pantalla: {e}")