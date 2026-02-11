# src/pages/questoes.py
import streamlit as st
from src.events import send_event
from src.domain import DIMENSOES

def render_questoes() -> None:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Como responder")
    st.markdown(
        """
- Use a escala de 1 a 5 considerando **como você age na maior parte do tempo**.  
- Evite responder pelo que gostaria de ser. Responda pelo que você realmente faz.  
- Se ficar em dúvida entre duas notas, **escolha a menor**.  
- Este diagnóstico mede **consistência**, não intenção.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    st.markdown(
        "<p class='small'>Instrução: clique em cada dimensão para abrir as perguntas. "
        "Responda todas as 45 para liberar o diagnóstico.</p>",
        unsafe_allow_html=True,
    )

    respondidas = 0
    q_idx = 0

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

    st.markdown(
        f"<p class='small'>Progresso: "
        f"<span class='highlight'>{respondidas}/45</span> respostas concluídas.</p>",
        unsafe_allow_html=True,
    )

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if respondidas == 45:
            # Monta respostas e scores como no seu app original
            st.session_state.answers_json = [
                int(st.session_state[f"q_{i}"]) for i in range(45)
            ]

            st.session_state.scores = [
                sum(st.session_state[f"q_{j}"] for j in range(i, i + 5))
                for i in range(0, 45, 5)
            ]

            st.session_state.total = sum(st.session_state.scores)

            if not st.session_state.get("submission_id"):
                import uuid
                st.session_state.submission_id = str(uuid.uuid4())

            # ✅ TRACKING CORRETO (novo padrão)
            send_event("diagnostico_concluido", etapa="questoes")

            st.session_state.etapa = "captura"
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")
