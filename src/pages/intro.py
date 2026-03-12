# src/pages/intro.py
import uuid
import streamlit as st
from src.events import send_event

def render_intro() -> None:
    # Banner igual ao seu app atual
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

    col_c = st.columns([1, 2.2, 1])[1]

    with col_c:
        st.markdown("<div class='card intro-center'>", unsafe_allow_html=True)

        st.markdown(
            "<h4 style='text-align:center; margin: 0 0 6px 0; letter-spacing: 0.08em; opacity: 0.90;'>PROTOCOLO LIDERUM</h4>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h1 style='text-align:center; margin: 0 0 14px 0; font-size: 2.1rem;'>Diagnóstico de Governança Pessoal</h1>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <p style="text-align:center; margin: 0 0 10px 0; font-size: 1.05rem;">
              <strong>Descubra seu tipo de governança em 6–8 minutos</strong><br/>
              e veja por que você oscila — mesmo sendo competente.
            </p>
            <p style="text-align:center; margin: 0 0 12px 0;">
              Resultado personalizado + leitura objetiva + próximo passo claro.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        st.markdown(
            "<p style='text-align:center; margin: 12px 0 16px 0;'>"
            "Se você não entende onde sua governança quebra, você continua recomeçando."
            "</p>",
            unsafe_allow_html=True,
        )

        cta_l, cta_c, cta_r = st.columns([1, 2, 1])
        with cta_c:
            if st.button("QUERO MEU DIAGNÓSTICO AGORA →", key="cta_intro_top"):
                if not st.session_state.get("submission_id"):
                    st.session_state.submission_id = str(uuid.uuid4())

                send_event("diagnostico_iniciado", etapa="intro")

                st.session_state.etapa = "questoes"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
