import time
import streamlit as st
from typing import Optional
import plotly.graph_objs as go
from plotly import io as pio
from .theme import get_plotly_template

# Design System primitives for Rose Intelligence enterprise UI


def metric_card(
    label: str,
    value: float,
    fmt: str = ",.0f",
    delta: Optional[float] = None,
    icon: Optional[str] = None,
    subtitle: Optional[str] = None,
    color: Optional[str] = None,
    width: str = "100%",
    animate: bool = True,
    duration: float = 0.8,
) -> None:
    """
    Render a premium metric card with optional animated counter.
    """
    container = st.container()
    with container:
        st.markdown(
            "<div class='glass-card fade-in' style='padding:18px; min-height:130px; width:%s;'>" % width,
            unsafe_allow_html=True,
        )
        cols = st.columns([1, 3])
        with cols[0]:
            if icon:
                chip_style = f"background:{color};" if color else ""
                st.markdown(f"<div class='icon-chip' style='{chip_style}'>{icon}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<div class='metric-label'>{label}</div>", unsafe_allow_html=True)
            if subtitle:
                st.markdown(f"<div style='color:#CBD5E1; font-size:0.92rem; margin-bottom:8px;'>{subtitle}</div>", unsafe_allow_html=True)
            ph = st.empty()
            # Animated counter
            numeric_value = None
            try:
                numeric_value = float(str(value).replace(",", "").replace("%", "").replace("$", "").replace("M", ""))
            except Exception:
                numeric_value = None
            if numeric_value is not None and animate:
                steps = max(10, int(duration * 30))
                for i in range(1, steps + 1):
                    display_value = numeric_value * (i / steps)
                    ph.markdown(f"<div class='metric-value'>{display_value:{fmt}}</div>", unsafe_allow_html=True)
                    time.sleep(duration / steps)
            else:
                ph.markdown(f"<div class='metric-value'>{value}</div>", unsafe_allow_html=True)
            if delta is not None:
                arrow = "▲" if delta >= 0 else "▼"
                trend_color = "#22C55E" if delta >= 0 else "#EF4444"
                st.markdown(
                    f"<div style='margin-top:8px; color:{trend_color}; font-weight:600;'>{arrow} {abs(delta):.1f}%</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)


def glass_card(title: str, content: str = "", footer: Optional[str] = None) -> None:
    st.markdown("<div class='glass-card fade-in' style='padding:18px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700; color:#F8FAFC; margin-bottom:6px;'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#CBD5E1; font-size:0.95rem'>{content}</div>", unsafe_allow_html=True)
    if footer:
        st.markdown(f"<div style='color:#94A3B8; margin-top:10px; font-size:0.85rem'>{footer}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def chart_container(fig: go.Figure, height: int = 340, use_template: bool = True) -> None:
    placeholder = st.empty()
    with st.spinner("Cargando gráfico…"):
        # small simulated load animation
        time.sleep(0.12)
    if use_template:
        try:
            fig.update_layout(template=pio.templates.get(get_plotly_template(), "plotly_dark"))
        except Exception:
            fig.update_layout(template="plotly_dark")
    fig.update_layout(margin=dict(l=8, r=8, t=32, b=8), height=height)
    placeholder.plotly_chart(fig, use_container_width=True)


def recommendation_card(title: str, priority: str, impact: str, cost: str, difficulty: str, body: str) -> None:
    st.markdown("<div class='glass-card fade-in' style='padding:18px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:flex-start; gap:12px;'>"
                f"<div><div style='font-weight:700; color:#F8FAFC;'>{title}</div>"
                f"<div style='color:#CBD5E1; margin-top:6px;'>{body}</div></div>"
                f"<div style='text-align:right; min-width:150px;'>"
                f"<div style='font-size:0.86rem; color:#CBD5E1;'>Prioridad</div><div style='font-weight:700'>{priority}</div>"
                f"<div style='font-size:0.86rem; color:#CBD5E1; margin-top:6px;'>Impacto</div><div style='font-weight:700'>{impact}</div>"
                f"</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def risk_card(client_name: str, score: float, impact: str, details: str) -> None:
    color = "#F43F5E" if score > 0.6 else ("#F59E0B" if score > 0.35 else "#22C55E")
    st.markdown("<div class='glass-card fade-in' style='padding:14px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<div><div style='font-weight:700; color:#F8FAFC;'>{client_name}</div>"
                f"<div style='color:#CBD5E1; font-size:0.9rem;'>{details}</div></div>"
                f"<div style='text-align:right; min-width:120px;'>"
                f"<div style='font-size:0.82rem; color:#CBD5E1;'>Risk Score</div>"
                f"<div style='font-weight:800; color:{color}; font-size:1.5rem;'>{score:.2f}</div>"
                f"</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title: str, subtitle: Optional[str] = None) -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
