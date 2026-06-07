import streamlit as st
import plotly.io as pio

PRIMARY = "#FF2D6F"
SECONDARY = "#FF5C8A"
ACCENT = "#FB7185"
ACCENT_2 = "#F9A8D4"
ACCENT_3 = "#FDA4AF"

DARK = {
    "background": "#0F172A",
    "surface": "#111827",
    "card": "rgba(255,255,255,0.06)",
    "glass": "rgba(15,23,42,0.65)",
    "border": "rgba(255,255,255,0.08)",
    "text": "#F8FAFC",
    "text_secondary": "#CBD5E1",
}

LIGHT = {
    "background": "#F8FAFC",
    "surface": "#E2E8F0",
    "card": "rgba(255,255,255,0.80)",
    "glass": "rgba(255,255,255,0.75)",
    "border": "rgba(15,23,42,0.08)",
    "text": "#0F172A",
    "text_secondary": "#475569",
}

def get_theme_config() -> dict:
    if "ri_theme" not in st.session_state:
        st.session_state["ri_theme"] = "dark"
    return LIGHT if st.session_state["ri_theme"] == "light" else DARK

def apply_theme() -> None:
    theme = get_theme_config()
    is_light = st.session_state["ri_theme"] == "light"
    
    theme_css = f"""
    <style>
    :root {{
        color-scheme: {'light' if is_light else 'dark'};
        font-family: 'Inter', system-ui, sans-serif;
    }}
    /* Forzar fondo de la app */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {theme['background']} !important;
    }}
    /* Remover márgenes superiores nativos molestos */
    [data-testid="stMainBlockContainer"] {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}
    /* Ocultar decoradores por defecto de Streamlit */
    [data-testid="stHeader"], footer, #MainMenu {{
        visibility: hidden !important;
        display: none !important;
    }}
    /* Estilos globales de tarjetas */
    .glass-card {{
        background: {theme['card']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 16px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        padding: 20px;
        transition: transform .2s ease, box-shadow .2s ease;
    }}
    .glass-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }}
    .sidebar-link {{
        color: {theme['text']} !important;
        text-decoration: none !important;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    .sidebar-link:hover {{
        background: rgba(255, 255, 255, 0.05);
        padding-left: 20px;
    }}
    .sidebar-link.active {{
        background: linear-gradient(90deg, {PRIMARY}, {SECONDARY}) !important;
        color: #FFFFFF !important;
        box-shadow: 0 8px 20px rgba(225,29,72,0.2);
    }}
    .icon-chip {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(255,255,255,0.08);
        font-size: 1.1rem;
    }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    # Configuración del Template de Plotly
    try:
        template_name = "rose_intel_light" if is_light else "rose_intel_dark"
        if template_name not in pio.templates:
            base_template = pio.templates["plotly_white"] if is_light else pio.templates["plotly_dark"]
            pio.templates[template_name] = base_template
            
        pio.templates[template_name].layout.update(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], family="Inter, sans-serif"),
            colorway=[PRIMARY, SECONDARY, ACCENT, ACCENT_2, ACCENT_3],
            margin=dict(l=20, r=20, t=40, b=20)
        )
    except Exception:
        pass

def get_plotly_template() -> str:
    return "rose_intel_light" if st.session_state.get("ri_theme", "dark") == "light" else "rose_intel_dark"