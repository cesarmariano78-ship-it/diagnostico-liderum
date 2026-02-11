# main.py
import streamlit as st

from src.styles import inject_base_styles, inject_app_styles
from src.state import init_state
from src.events import flush_pending_events
from src.pages.intro import render_intro
from src.pages.questoes import render_questoes
from src.pages.captura import render_captura
from src.pages.resultado import render_resultado

def main() -> None:
    inject_base_styles()
    inject_app_styles()
    init_state()

    # best-effort: tenta reenviar tracking pendente sem travar a UI
    flush_pending_events(timeout=1.5)

    # HEADER
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; margin-top: 0;'>PROTOCOLO LIDERUM</h1>", unsafe_allow_html=True)

    etapa = st.session_state.etapa

    if etapa == "intro":
        render_intro()
    elif etapa == "questoes":
        render_questoes()
    elif etapa == "captura":
        render_captura()
    elif etapa == "resultado":
        render_resultado()
    else:
        # fallback seguro
        st.session_state.etapa = "intro"
        st.rerun()

if __name__ == "__main__":
    main()
