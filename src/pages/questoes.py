# src/pages/questoes.py
from __future__ import annotations

import random
import streamlit as st

from src.domain import DIMENSOES
from src.events import send_event
from src.scoring import calcular_scores_e_total

def _preencher_respostas_aleatorias() -> None:
    for i in range(45):
        st.session_state[f"q_{i}"] = random.randint(1, 5)

def render_questoes() -> None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Como responder")
    st.markdown("""
- Use a escala de 1 a 5 considerando **como você age na maior parte do tempo**.  
- Evite responder pelo que gostaria de ser. Responda pelo que você realmente faz.  
- Se ficar em dúvida entre duas notas, **escolha a menor**.  
- Este diagnóstico mede **consistência**, não intenção.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)
    st.markdown("<p class='small'>Instrução: clique em cada dimensão para abrir as perguntas. Responda todas as 45 para liberar o diagnóstico.</p>", unsafe_allow_html=True)

    top_l, top_r = st.columns([0.985, 0.015])
    with top_r:
        if st.button("•", key="btn_teste_micro", help="Preenche as 45 respostas aleatoriamente (uso interno)."):
            _preencher_respostas_aleatorias()
            st.rerun()

    st.markdown("""
    <style>
    button[data-testid="baseButton-secondary"][title="Preenche as 45 respostas aleatoriamente (uso interno)."]{
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0 !important;
      margin: 0 !important;
      min-width: 10px !important;
      height: 10px !important;
      line-height: 10px !important;
      color: rgba(255,255,255,0.70) !important;
      font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    q_idx = 0
    respondidas = 0

    for dim_nome, dim_desc, perguntas in DIMENSOES:
        with st.expander(f"✨ DIMENSÃO: {dim_nome}"):
            st.markdown(f"<p class='small'>{dim_desc}</p>", unsafe_allow_html=True)

            for p in perguntas:
                st.markdown("<div class='question-card'>", unsafe_allow_html=True)
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(
                    f"R_{q_idx}",
                    [1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    key=f"q_{q_idx}",
                    label_visibility="collapsed",
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.get(f"q_{q_idx}") is not None:
                    respondidas += 1
                q_idx += 1

    st.markdown(f"<p class='small'>Progresso: <span class='highlight'>{respondidas}/45</span> respostas concluídas.</p>", unsafe_allow_html=True)

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if respondidas == 45:
            respostas = [int(st.session_state[f"q_{i}"]) for i in range(45)]
            scores, total = calcular_scores_e_total(respostas)

            st.session_state.answers_json = respostas
            st.session_state.scores = scores
            st.session_state.total = total

            if not st.session_state.submission_id:
                # manter comportamento atual: gerar aqui se não existir
                import uuid
                st.session_state.submission_id = str(uuid.uuid4())

            send_event("diagnostico_concluido", etapa="questoes")

            st.session_state.etapa = "captura"
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")

