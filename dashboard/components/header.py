import streamlit as st
from datetime import datetime


def render_header(title: str, subtitle: str) -> None:
    if "ri_theme" not in st.session_state:
        st.session_state["ri_theme"] = "dark"
    now = datetime.now().strftime("%d %b %Y · %H:%M")
    theme_mode = st.session_state["ri_theme"]

    header_html = f"""
    <div style='margin:0; padding:0;'>
      <div class='glass-card' style='width:100%; height:140px; min-height:140px; padding:24px; border-radius:24px; display:flex; align-items:center; justify-content:space-between; gap:18px;'>
        <div style='display:flex; align-items:center; gap:14px; min-width:0;'>
          <div style='width:52px; height:52px; border-radius:14px; background: linear-gradient(135deg, #FF2D6F, #FF5C8A); display:flex; align-items:center; justify-content:center; font-size:1.3rem; box-shadow: 0 16px 40px rgba(255,45,111,0.22);'>🌹</div>
          <div style='min-width:0;'>
            <div style='font-size:1.1rem; font-weight:800; color:{"#0F172A" if theme_mode == "light" else "#F8FAFC"};'>Rose Intelligence</div>
            <div style='font-size:0.9rem; color:{"#475569" if theme_mode == "light" else "#CBD5E1"}; margin-top:4px;'>{subtitle}</div>
          </div>
        </div>
        <div style='display:flex; align-items:center; gap:12px; flex-wrap:wrap;'>
          <div class='breadcrumb' style='padding:10px 14px; border-radius:14px; background:rgba(255,255,255,0.04); color:{"#475569" if theme_mode == "light" else "#CBD5E1"};'>PLATAFORMA / CHURN ANALYTICS / {title}</div>
          <div class='badge-pill'>Fecha {now}</div>
          <div style='position:relative;'>
            <button style='background:transparent; border:none; color:{"#0F172A" if theme_mode == "light" else "#F8FAFC"}; padding:10px 12px; border-radius:12px;'>🔔</button>
            <span style='position:absolute; top:2px; right:2px; background:#FF2D6F; color:#fff; font-size:10px; padding:3px 6px; border-radius:999px;'>3</span>
          </div>
          <div style='display:flex; align-items:center; gap:6px;'>
            <div style='display:flex; gap:6px;'>
              <div class='theme-pill' style='padding:8px 12px; border-radius:12px; background:{"#FF2D6F" if theme_mode == "dark" else "rgba(255,255,255,0.92)"}; color:{"#fff" if theme_mode == "dark" else "#0F172A"}; font-weight:700;'>🌙 Dark</div>
              <div class='theme-pill' style='padding:8px 12px; border-radius:12px; background:{"rgba(255,255,255,0.92)" if theme_mode == "light" else "transparent"}; color:{"#0F172A" if theme_mode == "light" else "#F8FAFC"}; border:1px solid rgba(255,255,255,0.12); font-weight:700;'>☀️ Light</div>
            </div>
          </div>
          <div style='display:flex; align-items:center; gap:8px;'>
            <div style='text-align:right; font-size:0.88rem; color:{"#475569" if theme_mode == "light" else "#CBD5E1"};'>Ana Martínez</div>
            <img src='https://via.placeholder.com/40x40.png?text=A' style='width:40px; height:40px; border-radius:12px; border:1px solid rgba(255,255,255,0.12);' />
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
