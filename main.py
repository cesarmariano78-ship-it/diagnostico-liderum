import streamlit as st
import plotly.graph_objects as go
import requests
import time
import datetime
import uuid
import random
import urllib.parse

# ---------------------------------------
# CONFIG
# ---------------------------------------
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbzpgNSVxPbMgFG_yk5UN5vucWROJzN6VUlpv5mVeW-gUw4ZySZOwLzhOa6lr1oVfWYo/exec"
APP_VERSION = "mvp-0.1"
EDUZZ_CHECKOUT_BASE = "https://sun.eduzz.com/7977E15B9E"

# ---------------------------------------
# CSS
# ---------------------------------------
st.markdown("""
<style>
:root { --br-green:#009C3B; }

.stApp { background-color:#000c1a; color:#fff; }
.top-banner { height:40px; border-bottom:1px solid rgba(0,156,59,.45); }

label,p,span,div { color:#fff !important; font-size:18px !important; }

/* Cards */
.card{
  background:rgba(255,255,255,.02);
  border:1px solid var(--br-green);
  border-radius:10px;
  padding:22px;
}

/* Moldura achatada (faixa baixa) */
.divider-brasil{
  height:6px;
  background:var(--br-green);
  border-radius:4px;
  margin:18px 0;
  opacity:.9;
}

/* Botões padrão */
.stButton>button{
  background:linear-gradient(180deg,#D4AF37 0%,#B8860B 100%) !important;
  color:#001226 !important;
  width:100%;
  padding:16px;
  font-weight:900;
  border-radius:8px;
}

/* TESTE quase invisível */
button[data-testid="baseButton-secondary"]{
  opacity:.05;
  width:14px;
  height:14px;
  padding:0;
}

/* Laudo */
.laudo-container{
  background:rgba(255,255,255,.03);
  padding:26px;
  border-left:6px solid #D4AF37;
  border-radius:14px;
}

/* Inputs */
input,textarea{
  color:#001226 !important;
  background:#fff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# STATE
# ---------------------------------------
for k,v in {
    "etapa":"intro","total":0,"scores":[0]*9,"zona":"",
    "nome_usuario":"","answers_json":[None]*45,
    "submission_id":"","sent_events":set()
}.items():
    if k not in st.session_state: st.session_state[k]=v

# ---------------------------------------
# TRACKING
# ---------------------------------------
def _now(): return datetime.datetime.utcnow().isoformat()
def _send_event(name, etapa=""):
    try:
        sid = st.session_state.submission_id or ""
        key = f"{name}:{sid}"
        if key in st.session_state.sent_events: return
        requests.post(URL_WEBHOOK,json={
            "type":"event","event_name":name,
            "timestamp":_now(),"submission_id":sid,
            "app_version":APP_VERSION,"etapa":etapa
        },timeout=6)
        st.session_state.sent_events.add(key)
    except: pass

# ---------------------------------------
# DADOS
# ---------------------------------------
dimensoes = [
 ("CLAREZA","",["","","","",""]),
 ("AUTOGESTÃO","",["","","","",""]),
 ("PERCEPÇÃO CRÍTICA","",["","","","",""]),
 ("CELEBRAÇÃO","",["","","","",""]),
 ("APRENDIZADO ACELERADO","",["","","","",""]),
 ("REGULAÇÃO COGNITIVA","",["","","","",""]),
 ("AUTOIMAGEM","",["","","","",""]),
 ("AUTOPERFORMANCE","",["","","","",""]),
 ("AUTORRESPONSABILIDADE","",["","","","",""]),
]

def calcular_zona(t):
    return "ELITE" if t>200 else "OSCILAÇÃO" if t>122 else "SOBREVIVÊNCIA"

def checkout_url():
    return f"{EDUZZ_CHECKOUT_BASE}?{urllib.parse.urlencode({'utm_content':st.session_state.submission_id})}"

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

# ---------------------------------------
# ETAPA 0 — INTRO (TERMINA NO CTA)
# ---------------------------------------
if st.session_state.etapa=="intro":
    col = st.columns([1,2,1])[1]
    with col:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center'>PROTOCOLO LIDERUM</h1>",unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center'>Diagnóstico de Governança Pessoal</h3>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Descubra onde sua autoliderança sustenta — e onde ela quebra execução.</p>",unsafe_allow_html=True)
        st.markdown("<div class='divider-brasil'></div>",unsafe_allow_html=True)

        if st.button("Iniciar diagnóstico gratuito"):
            st.session_state.submission_id=str(uuid.uuid4())
            _send_event("diagnostico_iniciado","intro")
            st.session_state.etapa="questoes"
            st.rerun()

        st.markdown("<p class='small' style='text-align:center'>Leva 6 a 8 minutos</p>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

# ---------------------------------------
# ETAPA 1 — QUESTÕES
# ---------------------------------------
elif st.session_state.etapa=="questoes":
    st.markdown("<div class='card'><h3>Como responder</h3></div>",unsafe_allow_html=True)
    st.markdown("<div class='divider-brasil'></div>",unsafe_allow_html=True)

    if st.button("TESTE"):
        for i in range(45): st.session_state[f"q_{i}"]=random.randint(1,5)

    resp=0; idx=0
    for d,_,qs in dimensoes:
        with st.expander(d):
            for _ in qs:
                st.radio("",[1,2,3,4,5],key=f"q_{idx}",horizontal=True,label_visibility="collapsed")
                if st.session_state.get(f"q_{idx}") is not None: resp+=1
                idx+=1

    if st.button("PROCESSAR MEU DIAGNÓSTICO") and resp==45:
        st.session_state.total=sum(st.session_state[f"q_{i}"] for i in range(45))
        st.session_state.zona=calcular_zona(st.session_state.total)
        _send_event("diagnostico_concluido","questoes")
        st.session_state.etapa="captura"
        st.rerun()

# ---------------------------------------
# ETAPA 2 — CAPTURA
# ---------------------------------------
elif st.session_state.etapa=="captura":
    with st.form("lead"):
        n=st.text_input("Nome"); e=st.text_input("Email"); w=st.text_input("WhatsApp")
        if st.form_submit_button("LIBERAR MEU LAUDO"):
            st.session_state.nome_usuario=n
            st.session_state.etapa="resultado"
            st.rerun()

# ---------------------------------------
# ETAPA 3 — RESULTADO (ÚNICA COM PRÓXIMO PASSO)
# ---------------------------------------
elif st.session_state.etapa=="resultado":
    st.markdown("<h3>Resultado</h3>",unsafe_allow_html=True)

    st.markdown(f"""
<details>
<summary style="background:#009C3B;color:#fff;padding:16px;border-radius:10px;text-align:center;font-weight:900">
Clique aqui para expandir e ler o seu Laudo
</summary>
<pre>{st.session_state.zona}</pre>
</details>
""",unsafe_allow_html=True)

    st.markdown("<div class='divider-brasil'></div>",unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center'>Próximo Passo</h3>",unsafe_allow_html=True)
    st.markdown(f"""
<div style='text-align:center'>
<a href="{checkout_url()}" target="_blank">
<div style="background:#D4AF37;padding:22px;border-radius:10px;font-weight:900">
QUERO MEU LAUDO COMPLETO + PLANO DE AÇÃO →
</div></a></div>
""",unsafe_allow_html=True)

    wa="https://wa.me/5581986245870"
    st.markdown(f"""
<div style='display:flex;justify-content:flex-end;margin-top:18px'>
<a href="{wa}" target="_blank" style="border:1px solid #009C3B;padding:12px 18px;border-radius:10px;color:#009C3B;font-weight:900;text-decoration:none">
Fale com nossa equipe
</a></div>
""",unsafe_allow_html=True)
