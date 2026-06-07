import streamlit as st

def get_theme_config():
    """Retorna la configuración de colores oficial de Rose Intelligence."""
    return {
        "primary": "#FF2D6F",          # Rosa Neón Core
        "background": "#0D0E12",       # Fondo Oscuro Profundo Muted
        "card": "rgba(22, 25, 35, 0.65)", # Tarjeta con Transparencia (Glassmorphism)
        "text": "#FFFFFF",             # Texto Principal Blanco Puro
        "text_secondary": "#94A3B8",   # Texto Secundario Gris Slate
        "border": "rgba(255, 45, 111, 0.15)", # Bordes sutiles rosa neón
        "accent": "#10B981"            # Verde Esmeralda para KPI positivos
    }

def apply_theme():
    """Inyecta el CSS global premium para forzar el layout corporativo impecable."""
    theme = get_theme_config()
    
    css = f"""
    <style>
        /* Imponer fondo oscuro profundo y eliminar parpadeos de color */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {theme["background"]} !important;
            color: {theme["text"]} !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}
        
        /* Estilizar barra lateral (Sidebar) con opacidad elegante */
        [data-testid="stSidebar"] {{
            background-color: rgba(15, 17, 23, 0.85) !important;
            border-right: 1px solid {theme["border"]} !important;
            backdrop-filter: blur(12px);
        }}

        /* Forzar visibilidad de textos en títulos y subtítulos */
        h1, h2, h3, h4, h5, h6, p, span, label {{
            color: {theme["text"]} !important;
        }}
        
        /* Contenedores Premium con Efecto Glassmorphism (Transparencias y Desenfoque) */
        .glass-card, [data-testid="stMetric"] {{
            background: {theme["card"]} !important;
            backdrop-filter: blur(16px) saturate(120%);
            -webkit-backdrop-filter: blur(16px) saturate(120%);
            border: 1px solid {theme["border"]} !important;
            border-radius: 14px !important;
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        /* Animación suave hover al pasar el mouse por las tarjetas */
        .glass-card:hover, [data-testid="stMetric"]:hover {{
            transform: translateY(-4px);
            border-color: rgba(255, 45, 111, 0.4) !important;
            box-shadow: 0 12px 40px 0 rgba(255, 45, 111, 0.1) !important;
        }}

        /* Reparar y estilizar los contenedores nativos de métricas de Streamlit */
        [data-testid="stMetricValue"] {{
            color: {theme["text"]} !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin-top: 4px !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {theme["text_secondary"]} !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}

        /* Ocultar bloques duplicados molestos del Theme Switcher que rompen el Header */
        [data-testid="stHorizontalBlock"] button {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: {theme["text"]} !important;
            border-radius: 8px !important;
        }}
        
        /* Clases auxiliares de control de títulos de sección */
        .section-title {{
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: {theme["text"]} !important;
            margin-bottom: 6px !important;
            letter-spacing: -0.02em;
        }}
        
        .section-subtitle {{
            font-size: 0.9rem !important;
            color: {theme["text_secondary"]} !important;
            margin-bottom: 20px !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_plotly_template():
    """Genera una plantilla oscura estilizada para gráficos de Plotly."""
    theme = get_theme_config()
    import plotly.graph_objects as go
    
    template = go.layout.Template()
    template.layout.paper_bgcolor = "rgba(0,0,0,0)" # Transparente para usar el fondo del contenedor
    template.layout.plot_bgcolor = "rgba(0,0,0,0)"
    template.layout.font = dict(color=theme["text"], family="Inter")
    template.layout.hoverlabel = dict(bgcolor=theme["background"], font_color=theme["text"])
    
    return template