# src/styles.py
import streamlit as st

def inject_base_styles() -> None:
    st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

    # remove header e ajuste topo
    st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { margin-top: -80px; }
    </style>
    """, unsafe_allow_html=True)

def inject_app_styles() -> None:
    # seu CSS completo (mantido)
    st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    .top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }

    div[data-testid="stMetric"] {
      background-color: rgba(212, 175, 55, 0.05);
      border: 1px solid #D4AF37;
      padding: 15px;
      border-radius: 10px;
    }

    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

    .stButton>button {
      background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
      color: #001226 !important;
      width: 100%;
      font-weight: bold;
      padding: 15px;
      border-radius: 8px;
      font-size: 18px !important;
    }

    .card {
      background-color: rgba(255,255,255,0.02);
      border: 0.5px solid #1DB954;
      padding: 22px;
      border-radius: 12px;
    }

    .divider-brasil {
      height: 2px;
      background-color: #1DB954;
      opacity: 0.85;
      width: 100%;
      border-radius: 2px;
      margin: 20px 0;
    }

    .divider-half {
      height: 2px;
      background-color: #1DB954;
      opacity: 0.85;
      width: 100%;
      max-width: 520px;
      margin: 20px auto;
      border-radius: 2px;
    }

    .small { font-size: 15px !important; color: rgba(255,255,255,0.75) !important; }
    .highlight { color: #D4AF37 !important; font-weight: bold; }

    .question-card {
      background-color: rgba(255,255,255,0.03);
      border: 1px solid rgba(212,175,55,0.18);
      padding: 18px;
      border-radius: 12px;
      margin: 14px 0;
    }

    button[data-testid="baseButton-secondary"] {
      opacity: 0.08;
      transform: scale(0.85);
    }
    button[data-testid="baseButton-secondary"]:hover { opacity: 0.25; }

    .laudo-container {
      background-color: rgba(255, 255, 255, 0.03);
      padding: 28px;
      border-radius: 15px;
      margin-top: 10px;
      line-height: 1.7;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] textarea {
      color: #001226 !important;
      background: #FFFFFF !important;
      border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
      color: rgba(0,18,38,0.55) !important;
    }

    div[data-testid="stTextInput"] label { color: #FFFFFF !important; }

    button[kind="primary"] {
      background: rgba(212,175,55,0.18) !important;
      border: 1px solid #D4AF37 !important;
      color: #D4AF37 !important;
      font-weight: 800 !important;
    }
    button[kind="primary"]:hover {
      background: rgba(212,175,55,0.28) !important;
    }

    :root { --br-green: #009C3B; }

    div.block-container {
      border: 1px solid var(--br-green) !important;
      border-radius: 10px !important;
      padding: 18px 18px 28px 18px !important;
    }

    div.stButton {
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
    }

    </style>
    """, unsafe_allow_html=True)

