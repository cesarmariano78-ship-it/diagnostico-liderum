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

    if not st.session_state.submission_id:
        st.session_state.submission_id = str(uuid.uuid4())

    checkout_url = _build_eduzz_checkout_url(st.session_state.submission_id)

    # Topo
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

    # Corpo (Radar + Laudo)
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

        st.markdown(f"""
        <details class="laudo-details">
          <summary>
            <div class="btn-brasil">📄 Clique aqui para expandir e ler o seu Laudo</div>
          </summary>
          <div class="laudo-text">
            <pre style="white-space: pre-wrap; margin: 0; font-family: inherit;">
{laudo_texto}
            </pre>
          </div>
        </details>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider-half'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='card' style='margin-top:18px;'>
        <h3>Próximo passo lógico</h3>
        Acesse o Laudo Completo + Plano de Ação para:
        <ul>
        <li>Prioridade clara</li>
        <li>Plano de 7 dias</li>
        <li>Plano de 30 dias</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='text-align: center; margin: 22px 0 6px 0;'>
            <a href='{checkout_url}' target='_blank' style='text-decoration: none;'>
                <div style='
                    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
                    color: #001226;
                    padding: 22px 44px;
                    font-weight: 900;
                    border-radius: 10px;
                    display: inline-block;
                    width: 100%;
                    max-width: 760px;
                    font-size: 22px;
                '>
                    QUERO MEU LAUDO COMPLETO + PLANO DE AÇÃO →
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rodapé WhatsApp
    wa_url = (
        "https://wa.me/5581986245870?"
        "text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM"
        "%20e%20quero%20conhecer%20as%20soluções."
    )

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    col_wa_l, col_wa_r = st.columns([1, 1])
    with col_wa_r:
        st.markdown(
            f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div class="btn-outline-brasil">Fale com nossa equipe</div>
            </a>
            """,
            unsafe_allow_html=True,
        )
