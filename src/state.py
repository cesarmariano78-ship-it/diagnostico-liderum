# src/state.py
import streamlit as st

def init_state() -> None:
    defaults = {
        "etapa": "intro",
        "total": 0,
        "scores": [0] * 9,
        "zona": "",
        "nome_usuario": "",
        "answers_json": [None] * 45,
        "submission_id": "",
        "sent_events": set(),
        "pending_events": [],  # fila local (melhora resiliencia)
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

