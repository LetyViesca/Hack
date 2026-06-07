import streamlit as st
from datetime import datetime
from .theme import get_theme_config

def render_header(title: str, subtitle: str) -> None:
    if "ri_theme" not in st.session_state:
        st.session_state["ri_theme"] = "dark"
        
    theme = get_theme_config()
    is_light = st.session_state["ri_theme"] == "light"
    now = datetime.now().strftime("%d %b %Y · %H:%M")
    
    # Columnas estructurales para Layout Superior nativo e interactivo
    col_info, col_actions = st.columns([1.2, 1.0])
    
    with col_info:
        header_html = f"""
        <div style='display:flex; align-items:center; gap:16px; margin-bottom: 20px;'>
          <div style='width:48px; height:48px; border-radius:12px; background: linear-gradient(135deg, #FF2D6F, #FF5C8A); display:flex; align-items:center; justify-content:center; font-size:1.3rem; box-shadow: 0 10px 25px rgba(255,45,111,0.3);'>🌹</div>
          <div>
            <div style='font-size:1.3rem; font-weight:800; color:{theme["text"]}; line-height:1.1;'>Rose Intelligence</div>
            <div style='font-size:0.88rem; color:{theme["text_secondary"]}; margin-top:2px;'>{subtitle}</div>
          </div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        
    with col_actions:
        # Fila de utilidades alineadas a la derecha usando columnas internas de Streamlit
        c1, c2, c3 = st.columns([1, 1, 1.2])
        
        with c1:
            st.caption(f"📅 **Actualizado**\n{now}")
        
        with c2:
            # Botón interactivo real para switchear el tema de la aplicación
            label_theme = "☀️ Modo Claro" if is_light else "🌙 Modo Oscuro"
            if st.button(label_theme, use_container_width=True, key="btn_theme_toggle"):
                st.session_state["ri_theme"] = "dark" if is_light else "light"
                st.rerun()
                
        with c3:
            # Perfil de usuario estilizado
            profile_html = f"""
            <div style='display:flex; align-items:center; gap:8px; justify-content: flex-end;'>
              <div style='text-align:right; font-size:0.85rem;'>
                <div style='font-weight:700; color:{theme["text"]};'>Ana Martínez</div>
                <div style='font-size:0.75rem; color:{theme["text_secondary"]};'>Analista Senior</div>
              </div>
              <img src='https://api.dicebear.com/7.x/avataaars/svg?seed=Ana' style='width:36px; height:36px; border-radius:10px; background:rgba(255,255,255,0.1);' />
            </div>
            """
            st.markdown(profile_html, unsafe_allow_html=True)
            
    st.markdown(f"<div style='font-size:0.8rem; font-weight:700; color:{PRIMARY}; letter-spacing:0.05em; margin-bottom:1.5rem;'>PLATAFORMA / CHURN ANALYTICS / {title.upper()}</div>", unsafe_allow_html=True)