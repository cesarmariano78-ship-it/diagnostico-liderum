import streamlit as st
import plotly.graph_objects as go
import requests
import time
import datetime

# ---------------------------------------
# CONFIG
# ---------------------------------------
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbzpgNSVxPbMgFG_yk5UN5vucWROJzN6VUlpv5mVeW-gUw4ZySZOwLzhOa6lr1oVfWYo/exec"

# ---------------------------------------
# EVENT TRACKING
# ---------------------------------------
def send_event(event_name, etapa="", submission_id=""):
    payload = {
        "event_name": event_name,
        "etapa": etapa,
        "submission_id": submission_id
    }
    requests.post(URL_WEBHOOK, json=payload, timeout=5)

# A) App abriu
send_event("diagnostico_aberto", etapa="inicio")

# ---------------------------------------
# CSS
# ---------------------------------------
st.markdown("""
<style>
.stApp { background-color: #000c1a; color: #FFFFFF; }
.top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }
label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# ESTADO
# ---------------------------------------
if "etapa" not in st.session_state:
    st.session_state.etapa = "intro"

if "total" not in st.session_state:
    st.session_state.total = 0

if "scores" not in st.session_state:
    st.session_state.scores = [0] * 9

if "zona" not in st.session_state:
    st.session_state.zona = ""

if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""

if "submission_id" not in st.session_state:
    st.session_state.submission_id = ""

# ---------------------------------------
# DADOS
# ---------------------------------------
dimensoes = [
    ("CLAREZA", "", ["Q1","Q2","Q3","Q4","Q5"]),
    ("AUTOGESTÃO", "", ["Q6","Q7","Q8","Q9","Q10"]),
    ("PERCEPÇÃO CRÍTICA", "", ["Q11","Q12","Q13","Q14","Q15"]),
    ("CELEBRAÇÃO", "", ["Q16","Q17","Q18","Q19","Q20"]),
    ("APRENDIZADO ACELERADO", "", ["Q21","Q22","Q23","Q24","Q25"]),
    ("REGULAÇÃO COGNITIVA", "", ["Q26","Q27","Q28","Q29","Q30"]),
    ("AUTOIMAGEM", "", ["Q31","Q32","Q33","Q34","Q35"]),
    ("AUTOPERFORMANCE", "", ["Q36","Q37","Q38","Q39","Q40"]),
    ("AUTORRESPONSABILIDADE", "", ["Q41","Q42","Q43","Q44","Q45"]),
]

def calcular_zona(total):
    if total > 200:
        return "ELITE"
    if total > 122:
        return "OSCILAÇÃO"
    return "SOBREVIVÊNCIA"

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO LIDERUM")

# ---------------------------------------
# INTRO
# ---------------------------------------
if st.session_state.etapa == "intro":
    if st.button("INICIAR MEU DIAGNÓSTICO"):
        send_event("diagnostico_iniciado", etapa="inicio")  # B)
        st.session_state.etapa = "questoes"
        st.rerun()

# ---------------------------------------
# QUESTÕES
# ---------------------------------------
elif st.session_state.etapa == "questoes":
    q_idx = 0
    respondidas = 0

    for _, _, perguntas in dimensoes:
        for _ in perguntas:
            st.radio(
                f"Q{q_idx}",
                [1, 2, 3, 4, 5],
                index=None,
                key=f"q_{q_idx}",
                horizontal=True
            )
            if st.session_state.get(f"q_{q_idx}") is not None:
                respondidas += 1
            q_idx += 1

    if st.button("PROCESSAR MEU DIAGNÓSTICO") and respondidas == 45:
        st.session_state.scores = [
            sum(st.session_state[f"q_{j}"] for j in range(i, i + 5))
            for i in range(0, 45, 5)
        ]
        st.session_state.total = sum(st.session_state.scores)
        st.session_state.etapa = "captura"
        st.rerun()

# ---------------------------------------
# CAPTURA
# ---------------------------------------
elif st.session_state.etapa == "captura":
    with st.form("lead"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        submit = st.form_submit_button("LIBERAR")

        if submit:
            answers_json = [int(st.session_state[f"q_{i}"]) for i in range(45)]
            submission_id = datetime.datetime.utcnow().isoformat()
            st.session_state.submission_id = submission_id

            send_event(
                "diagnostico_concluido",
                etapa="resultado",
                submission_id=submission_id
            )  # C)

            payload = {
                "timestamp": submission_id,
                "nome": nome,
                "email": email,
                "pontos_total": st.session_state.total,
                "zona": calcular_zona(st.session_state.total),
                "scores_dimensoes": st.session_state.scores,
                "answers_json": answers_json
            }
            requests.post(URL_WEBHOOK, json=payload, timeout=10)

            st.session_state.etapa = "resultado"
            st.rerun()

# ---------------------------------------
# RESULTADO
# ---------------------------------------
elif st.session_state.etapa == "resultado":
    send_event(
        "oferta_laudo_exibida",
        etapa="resultado",
        submission_id=st.session_state.submission_id
    )  # D)

    st.write("Oferta do Laudo")

    if st.button("ADQUIRIR LAUDO"):
        send_event(
            "clique_laudo",
            etapa="resultado",
            submission_id=st.session_state.submission_id
        )  # E)
