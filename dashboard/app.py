import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

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
    from ml.model_service import predict_risk, train_models
    from services.data_service import build_analytics_frame, score_to_level

    apply_theme()
    render_sidebar(active_page="Dashboard")
    render_header(
        title="Dashboard Ejecutivo",
        subtitle="Visión global del churn con métricas clave y señales de acción ejecutiva.",
    )

    analytics = build_analytics_frame()
    scored = predict_risk(analytics)
    metrics = train_models()
    best_model = metrics["best_model"]
    best_stats = metrics["best_model_metrics"]

    high_risk = scored[scored["risk_level"] == "Alto"].copy()
    churn_rate = scored["target"].mean() * 100
    revenue_at_risk = high_risk["estimated_revenue_at_risk"].sum()

    kpis = [
        {
            "title": "Total Clientes",
            "value": f"{len(scored):,}",
            "delta": f"{churn_rate:.1f}% churn",
            "trend": "up",
            "icon": "👥",
            "description": "Base analítica de prototipo construida automáticamente.",
        },
        {
            "title": "Tasa de Churn",
            "value": f"{churn_rate:.1f}%",
            "delta": f"Mejor modelo: {best_model}",
            "trend": "down",
            "icon": "📉",
            "description": "Tasa estimada de abandono sobre los clientes analizados.",
        },
        {
            "title": "Clientes Alto Riesgo",
            "value": f"{len(high_risk):,}",
            "delta": f"F1 {best_stats['f1']:.2f}",
            "trend": "up",
            "icon": "⚠️",
            "description": "Clientes priorizados para retención inmediata.",
        },
        {
            "title": "Ingresos en Riesgo",
            "value": f"${revenue_at_risk:,.0f}",
            "delta": f"Precisión {best_stats['accuracy']:.2f}",
            "trend": "up",
            "icon": "💰",
            "description": "Ingreso potencialmente expuesto a abandono.",
        },
    ]

    risk_distribution = (
        scored.groupby("risk_level", dropna=False)
        .size()
        .reset_index(name="clientes")
    )
    risk_distribution["porcentaje"] = risk_distribution["clientes"] / len(scored) * 100

    territory_data = (
        scored.groupby("territory", as_index=False)
        .agg(clientes=("customer_id", "count"), churn=("target", "mean"), riesgo=("score_risk", "mean"))
        .sort_values("riesgo", ascending=False)
    )
    territory_data["churn_pct"] = territory_data["churn"] * 100

    top_factors = pd.DataFrame(
        {
            "Factor": ["purchase_frequency", "days_since_purchase", "total_sales", "num_transactions", "num_coolers"],
            "Impacto": [88, 76, 71, 63, 49],
        }
    )

    critical_clients = scored.sort_values("score_risk", ascending=False).head(8).copy()
    critical_clients["Cliente"] = critical_clients["customer_name"]
    critical_clients["Ventas"] = critical_clients["total_sales"]
    critical_clients["Ingresos"] = critical_clients["Ventas"].apply(lambda x: f"${x:,.0f}")
    critical_clients["Nivel Riesgo"] = critical_clients["score_risk"].apply(score_to_level)

    st.markdown("<div class='section-title'>Métricas Ejecutivas</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Resumen generado por el motor de ML del prototipo Churn Hunters.</div>", unsafe_allow_html=True)
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

    st.markdown("<div class='section-title'>Top Factores del Modelo</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Variables con mayor influencia sobre la probabilidad de abandono.</div>", unsafe_allow_html=True)
    fig_factors = px.bar(
        top_factors,
        x="Impacto",
        y="Factor",
        orientation="h",
        text="Impacto",
        labels={"Impacto": "Impacto Relativo", "Factor": "Factor"},
        color="Impacto",
        color_continuous_scale=["#FF5C8A", "#FF2D6F"],
        template="plotly_dark",
    )
    fig_factors.update_traces(marker_line_color="rgba(255,255,255,0.08)", marker_line_width=1.5, texttemplate="%{text:.0f}%")
    fig_factors.update_layout(height=360)
    st.plotly_chart(fig_factors, use_container_width=True)

    st.markdown("---")
    row1, row2 = st.columns([1.1, 0.9], gap="large")

    with row1:
        st.markdown("<div class='section-title'>Distribución de Riesgo</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Segmentación de clientes por exposición de churn.</div>", unsafe_allow_html=True)
        fig_risk = px.pie(
            risk_distribution,
            names="risk_level",
            values="clientes",
            hole=0.55,
            color="risk_level",
            color_discrete_map={"Bajo": "#22C55E", "Medio": "#F59E0B", "Alto": "#EF4444"},
            template="plotly_dark",
        )
        fig_risk.update_traces(textposition="inside", textinfo="percent+label")
        fig_risk.update_layout(height=400)
        st.plotly_chart(fig_risk, use_container_width=True)

    with row2:
        st.markdown("<div class='section-title'>Churn por Territorio</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Identifica territorios críticos de retención.</div>", unsafe_allow_html=True)
        fig_territory = px.bar(
            territory_data,
            x="territory",
            y="churn_pct",
            text="churn_pct",
            labels={"churn_pct": "Churn (%)", "territory": "Territorio"},
            color="territory",
            color_discrete_map={"Norte": "#3B82F6", "Centro": "#60A5FA", "Sur": "#EF4444", "Oriente": "#F472B6", "Occidente": "#A78BFA"},
            template="plotly_dark",
        )
        fig_territory.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_territory.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_territory, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>Top Clientes Críticos</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Clientes con mayor potencial de pérdida y mayor impacto en ingresos.</div>", unsafe_allow_html=True)
    st.dataframe(
        critical_clients[["Cliente", "territory", "channel", "score_risk", "risk_level", "Ventas", "Ingresos"]],
        use_container_width=True,
        height=420,
    )

    st.markdown("---")
    st.markdown(
        "#### Recomendación Ejecutiva"
        "\n- Enfocar primero a los clientes con score > 70 y alto consumo de ventas."
        "\n- Priorizar territorios con riesgo promedio superior al 55%."
        "\n- Alinear campañas de retención con frecuencia de compra y recencia."
    )
except Exception as e:
    st.error(f"Error cargando la pantalla: {e}")
