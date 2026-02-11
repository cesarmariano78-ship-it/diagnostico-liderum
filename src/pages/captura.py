# src/pages/captura.py
from __future__ import annotations

import datetime
import uuid
import streamlit as st

from src.events import send_event, send_submission
from src.scoring import calcular_zona

def _simular_processamento() -> None:
    import time
    msgs = [
        "Processando suas respostas…",
        "Calculando sua Zona de Governança…",
        "Montando seu Radar por Dimensões…",
        "Gerando seu Direcionamento Estratégico…",
        "Finalizando…",
    ]
    box = st.empty()
    with st.spinner("Aguarde…"):
        for m in msgs:
            box.markdown(f"<p class='small'>🔎 {m}</p>", unsafe_allow_html=True)
            time.sleep(2.4)
    box.empty()

def render_captura() -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO</h3>", unsafe_allow_html=True)
        st.markdown("<p class='small' style='text-align:center;'>Preencha seus dados para liberar seu Radar e sua Zona.</p>", unsafe_allow_html=True)

        with st.form("lead_form"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            empresa = st.text_input("Empresa")
            cargo = st.text_input("Cargo")

            submit = st.form_submit_button("LIBERAR MEU LAUDO AGORA", type="primary")

            if submit:
                if all([nome, email, whatsapp, empresa, cargo]):
                    total = int(st.session_state.total)
                    zona = calcular_zona(total)

                    st.session_state.zona = zona
                    st.session_state.nome_usuario = nome

                    if not st.session_state.submission_id:
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
                        "answers_json": [int(v) for v in st.session_state.answers_json],
                    }

                    _simular_processamento()

                    ok = send_submission(payload, timeout=12)
                    if ok:
                        send_event("lead_enviado", etapa="captura")

                    st.session_state.etapa = "resultado"
                    st.rerun()
                else:
                    st.warning("Por favor, preencha todos os campos.")

