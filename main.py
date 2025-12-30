import streamlit as st
import plotly.graph_objects as go
import requests
import re

# =========================================================
# 1) CONFIG + IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
# =========================================================
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #000c1a; color: #FFFFFF; }

.top-banner {
    background-color: #000c1a;
    height: 16px;
    width: 100%;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    margin-bottom: 18px;
}

div[data-testid="stMetric"] {
    background-color: rgba(212, 175, 55, 0.05);
    border: 1px solid rgba(212, 175, 55, 0.55);
    padding: 15px;
    border-radius: 10px;
}

label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

.stButton>button {
    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
    color: #001226 !important;
    width: 100%;
    font-weight: 800;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px !important;
    border: 0 !important;
}

.small-btn .stButton>button {
    padding: 10px !important;
    font-size: 16px !important;
}

.question-text {
    font-size: 18px !important;
    color: #FFFFFF !important;
    margin-top: 16px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.12);
    padding-bottom: 10px;
}

.card {
    background-color: rgba(255, 255, 255, 0.03);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid rgba(212, 175, 55, 0.18);
}

.laudo-container {
    background-color: rgba(255, 255, 255, 0.03);
    padding: 28px;
    border-radius: 15px;
    border-left: 6px solid #D4AF37;
    margin-top: 12px;
    line-height: 1.7;
}

.highlight { color: #D4AF37 !important; font-weight: 800; }
.muted { color: rgba(255,255,255,0.78) !important; font-size: 16px !important; }
hr { border: none; border-top: 1px solid rgba(212,175,55,0.12); margin: 18px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2) STATE
# =========================================================
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"   # NOVO: começa na página de boas-vindas

if "total" not in st.session_state:
    st.session_state.total = 0

if "scores" not in st.session_state:
    st.session_state.scores = [0] * 9

if "zona" not in st.session_state:
    st.session_state.zona = ""

if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""

# URL webhook (Google Apps Script)
URL_WEBHOOK = "https://script.google.com/ma_
