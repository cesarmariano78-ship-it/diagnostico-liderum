# src/pages/resultado.py
from __future__ import annotations

import urllib.parse
import uuid
import streamlit as st

from src.config import EDUZZ_CHECKOUT_BASE
from src.domain import DIMENSOES
from src.charts import build_radar
from src.laudo import texto_laudo

def _build_eduzz_checkout_url(submission_id: str) -> str:
    q = {"utm_content": submission_id or ""}
    return f"{EDUZZ_CHECKOUT_BASE}?{urllib.parse.urlencode(q)}"

def render_resultado() -> None:
    st.markdown("""
    <style>
      .btn-brasil {
        background: #009C3B;
        color: #ffffff;
        border: 1px solid #009C3B;
        padding: 16px 22px;
        border-radius: 10px;
        font-weight: 900;
        display: inline-block;
        width: 100%;
        max-width: 720px;
        font-size: 20px;
        text-align: center;
        cursor: pointer;
      }

      .btn-outline-brasil {
        background: transparent;
        color: #009C3B;
        border: 1px solid #009C3B;
        padding: 12px 18px;
        border-radius: 10px;
        font-weight: 900;
        display: inline-block;
        width: 100%;
        text-align: center;
        cursor: pointer;
      }

      details.laudo-details { width: 100%; margin: 10px 0 0 0; }
      details.laudo-details > summary { list-style: none; outline: none; }
      details.laudo-details > summary::-webkit-details-marker { display: none; }

      .laudo-text {
        margin-top: 14px;
        padding: 18px 18px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,156,59,0.35);
        line-height: 1.7;
      }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.submission_id:
        st.session_state.submission_id = str(uuid.uuid4())
    checkout_url = _build_eduzz_checkout_url(st.session_state.submission_id)

    st.markdown(
        f"### Análise Individual: <span class='highlight'>{st.session_state.nome_usuario.upper()}</span>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    with c2:
        st.metric("Zona de Governança", st.session_state.zona)

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 0.8])

    with col_l:
        categorias = [d[0].split(" (")[0] for d in DIMENSOES]
        fig = build_radar(st.session_state.scores, categorias)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)

        nome = st.session_state.nome_usuario
        zona = st.session_state.zona
        total = int(st.session_state.total)

        laudo_texto = texto_laudo(zona, nome, total)

        st.markdown(f"<div class='laudo-text'><pre style='white-space: pre-wrap;'>{laudo_texto}</pre></div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<a class='btn-brasil' href='{checkout_url}' target='_blank'>QUERO MEU LAUDO COMPLETO (R$ 29,90)</a>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

