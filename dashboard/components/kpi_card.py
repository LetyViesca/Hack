import streamlit as st
from .design_system import metric_card
from typing import Optional


def _parse_delta(delta_value):
    if delta_value is None:
        return None
    if isinstance(delta_value, (int, float)):
        return float(delta_value)
    delta_str = str(delta_value).replace("%", "").replace("+", "").strip()
    try:
        return float(delta_str)
    except ValueError:
        return None


def render_kpi_card(
    title: str,
    value,
    icon: Optional[str] = None,
    trend: Optional[str] = None,
    color: Optional[str] = None,
    subtitle: Optional[str] = None,
    delta: Optional[float] = None,
    description: str = "",
) -> None:
    # Wrapper for design_system.metric_card to keep compatibility with page calls.
    delta_value = _parse_delta(delta)
    if delta_value is None and trend is not None:
        delta_value = 1.0 if trend == "up" else -1.0 if trend == "down" else 0.0
    label = title
    subtext = subtitle or description
    metric_card(
        label=label,
        value=value,
        delta=delta_value,
        icon=icon,
        subtitle=subtext,
        color=color,
        animate=True,
    )
