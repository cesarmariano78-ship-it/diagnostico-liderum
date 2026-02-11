# src/pages/captura.py
import uuid
import datetime
import requests
import streamlit as st

from src.events import send_event
from src.config import URL_WEBHOOK
from src.scoring import calcular_zona
from src.utils import simular_processamento  # mantém seu comportamento visual

def render_captura() -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p class='small' style='text-align:center;'>"
            "Preencha seus dados para liberar seu Radar e sua Zona.</p>",
            unsafe_allow_html=True,
        )

        with st.form("lead_form"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            empresa = st.text_input("Empresa")
            cargo = st.text_input("Cargo")

            submit = st.form_submit_button(
                "LIBERAR MEU LAUDO AGORA", type="primary"
            )

            if submit:
                if all([nome, email, whatsapp, empresa, cargo]):

                    total = int(st.session_state.total)
                    zona = calcular_zona(total)

                    st.session_state.zona = zona
                    st.session_state.nome_usuario = nome

                    if not st.session_state.get("submission_id"):
                        st.session_state.submission_id = str(uuid.uuid4())

                    payload = {
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "submission_id": st.session_state.submission_id,
                        "nome": nome,
                        "email": email,
                        "whatsapp": whatsapp,
                        "empresa": empresa,
                        "cargo": cargo,
                        "pontos_total": total,
                        "zona": zona,
                        "scores_dimensoes": st.session_state.scores,
                        "answers_json": [
                            int(v) for v in st.session_state.answers_json
                        ],
                    }

                    simular_processamento()

                    ok = False
                    try:
                        r = requests.post(
                            URL_WEBHOOK, json=payload, timeout=12
                        )
                        if getattr(r, "status_code", 0) == 200:
                            txt = (r.text or "").strip().upper()
                            if "OK" in txt:
                                ok = True
                    except Exception:
                        ok = False

                    if ok:
                        # ✅ TRACKING CORRETO (novo padrão)
                        send_event("lead_enviado", etapa="captura")

                    st.session_state.etapa = "resultado"
                    st.rerun()

                else:
                    st.warning("Por favor, preencha todos os campos.")
