import streamlit as st
import plotly.io as pio

# Rose Intelligence palette
PRIMARY = "#FF2D6F"
SECONDARY = "#FF5C8A"
ACCENT = "#FB7185"
ACCENT_2 = "#F9A8D4"
ACCENT_3 = "#FDA4AF"

DARK = {
    "background": "#0F172A",
    "surface": "#111827",
    "card": "rgba(255,255,255,0.08)",
    "glass": "rgba(255,255,255,0.12)",
    "border": "rgba(255,255,255,0.12)",
    "text": "#F8FAFC",
    "text_secondary": "#CBD5E1",
}

LIGHT = {
    "background": "#F7F8FB",
    "surface": "#E2E8F0",
    "card": "rgba(255,255,255,0.92)",
    "glass": "rgba(255,255,255,0.84)",
    "border": "rgba(15,23,42,0.12)",
    "text": "#0F172A",
    "text_secondary": "#475569",
}


def get_theme_config() -> dict:
    mode = st.session_state.get("ri_theme", "dark")
    return LIGHT if mode == "light" else DARK


def apply_theme() -> None:
    theme = get_theme_config()
    theme_css = f"""
    <style>
    :root {{
        color-scheme: {'light' if st.session_state.get('ri_theme','dark') == 'light' else 'dark'};
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        background: {theme['background']};
        color: {theme['text']};
    }}
    html, body, #root {{
        background: {theme['background']} !important;
    }}
    body, html, #root, .streamlit-container, .stApp {{
        background: {theme['background']} !important;
    }}
    .block-container, .stApp .main, .stApp .block-container {{
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1.75rem !important;
        padding-right: 1.75rem !important;
        background: transparent !important;
    }}
    .main > div:first-child, .stApp > main > div:nth-child(1), .css-1lsmgbg.e1fqkh3o2, .css-18e3th9, .css-1d391kg, .css-1v3fvcr {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    .stSidebar {{
        background: linear-gradient(180deg, rgba(15,23,42,0.95), rgba(15,23,42,0.88)) !important;
        border-right: 1px solid {theme['border']} !important;
        backdrop-filter: blur(20px);
    }}
    .css-1lsmgbg.e1fqkh3o2, .css-18e3th9, .css-1d391kg, .css-1v3fvcr {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    header {{
        display:none !important;
    }}
    [data-testid="stHeader"]{{
        display:none !important;
    }}
    [data-testid="stToolbar"]{{
        display:none !important;
    }}
    [data-testid="stDecoration"]{{
        display:none !important;
    }}
    [data-testid="stStatusWidget"]{{
        display:none !important;
    }}
    #MainMenu{{
        display:none !important;
    }}
    footer{{
        display:none !important;
    }}
    .glass-card {{
        background: {'rgba(255,255,255,0.88)' if st.session_state.get('ri_theme','dark') == 'light' else 'rgba(15,23,42,0.90)'};
        border: 1px solid {theme['border']};
        border-radius: 24px;
        backdrop-filter: blur(24px);
        box-shadow: 0 24px 80px rgba(0,0,0,0.18);
        transition: transform .25s ease, box-shadow .25s ease, opacity .3s ease;
    }}
    .glass-card:hover {{
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 28px 90px rgba(0,0,0,0.22);
    }}
    .theme-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 10px 14px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.1);
        color: {theme['text']};
        background: rgba(255,255,255,0.08);
        font-weight: 700;
        font-size: 0.95rem;
    }}
    .glass-panel {{
        background: {theme['glass']};
        border: 1px solid {theme['border']};
        border-radius: 22px;
        backdrop-filter: blur(20px);
        padding: 22px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.22);
    }}
    .section-title {{
        font-size: 1.35rem;
        font-weight: 700;
        color: {theme['text']};
        margin-bottom: 0.35rem;
    }}
    .section-subtitle {{
        color: {theme['text_secondary']};
        margin-top: 0;
        margin-bottom: 1.2rem;
        font-size: 0.98rem;
    }}
    .breadcrumb {{
        color: {theme['text_secondary']};
        letter-spacing: 0.06em;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }}
    .badge-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255,255,255,0.08);
        color: {theme['text']};
        border-radius: 999px;
        padding: 0.45rem 0.9rem;
        font-size: 0.9rem;
    }}
    .metric-label {{
        color: {theme['text_secondary']};
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }}
    .metric-value {{
        color: {theme['text']};
        font-size: 2.35rem;
        margin: 0;
        line-height: 1;
        font-weight: 700;
        letter-spacing: -0.03em;
    }}
    .detail-card {{
        background: rgba(255,255,255,0.08);
        border: 1px solid {theme['border']};
        border-radius: 22px;
        padding: 18px;
        backdrop-filter: blur(18px);
    }}
    .detail-label {{
        color: {theme['text_secondary']};
        margin: 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }}
    .detail-value {{
        color: {theme['text']};
        font-size: 1.05rem;
        margin: 0.3rem 0 0.9rem 0;
        font-weight: 600;
    }}
    .statement-card {{
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: 18px;
        color: {theme['text']};
        line-height: 1.6;
    }}
    .sidebar-link {{
        color: {theme['text']};
        text-decoration: none;
        display: block;
        padding: 12px 14px;
        border-radius: 14px;
        margin-bottom: 6px;
        transition: all 0.22s cubic-bezier(.2,.9,.2,1);
        position: relative;
    }}
    .sidebar-link:hover {{
        transform: translateX(6px);
        box-shadow: 0 6px 24px rgba(225,29,72,0.08);
    }}
    .sidebar-link.active {{
        background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
        color: #FFFFFF !important;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(225,29,72,0.18), 0 0 20px rgba(244,63,94,0.06) inset;
    }}
    .sidebar-link.active .icon-chip {{
        box-shadow: 0 6px 20px rgba(225,29,72,0.18);
    }}
    .icon-chip {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(255,255,255,0.03);
        margin-right: 0.75rem;
        font-size: 1.05rem;
    }}
    .quick-links a {{
        color: {theme['text']};
        text-decoration: none;
    }}
    .quick-links a:hover {{
        text-decoration: underline;
    }}
    /* Animations */
    .fade-in {{
        animation: fadeIn .5s ease both;
    }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity:1; transform: translateY(0); }} }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    # Create a reusable Plotly template for Rose Intelligence based on the selected mode
    try:
        template_name = "rose_intel_light" if st.session_state.get("ri_theme", "dark") == "light" else "rose_intel_dark"
        base_template = pio.templates["plotly_white"] if template_name == "rose_intel_light" else pio.templates["plotly_dark"]
        if template_name not in pio.templates:
            pio.templates[template_name] = base_template
        legend_bg = "rgba(255,255,255,0.82)" if template_name == "rose_intel_light" else "rgba(17,24,39,0.6)"
        axis_line_color = "rgba(15,23,42,0.18)" if template_name == "rose_intel_light" else "rgba(255,255,255,0.12)"
        text_color = theme["text"]
        pio.templates[template_name].layout.update(
            paper_bgcolor=theme["background"],
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text_color, family="Inter, system-ui, -apple-system"),
            legend=dict(bgcolor=legend_bg, bordercolor=theme["border"], borderwidth=1, font=dict(color=text_color)),
            margin=dict(l=10, r=10, t=40, b=10),
            hoverlabel=dict(bgcolor="#0B1220" if template_name == "rose_intel_dark" else "rgba(15,23,42,0.9)", font_size=12, font_family="Inter, sans-serif"),
            xaxis=dict(showgrid=False, zeroline=False, linecolor=axis_line_color, tickfont=dict(color=theme["text_secondary"])),
            yaxis=dict(showgrid=False, zeroline=False, linecolor=axis_line_color, tickfont=dict(color=theme["text_secondary"])),
            colorway=[PRIMARY, SECONDARY, ACCENT, ACCENT_2, ACCENT_3],
        )
    except Exception:
        pass


def get_plotly_template() -> str:
    return "rose_intel_light" if st.session_state.get("ri_theme", "dark") == "light" else "rose_intel_dark"
