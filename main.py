import streamlit as st
import plotly.graph_objects as go
import requests
import time
import datetime

# ---------------------------------------
# CONFIG
# ---------------------------------------
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbzpgNSVxPbMgFG_yk5UNvucWROJzN6VUlpv5mVeW-gUw4ZySZOwLzhOa6lr1oVfWYo/exec"

# ---------------------------------------
# EVENT DISPATCH (PADRÃO OBRIGATÓRIO)
# ---------------------------------------
def dispatch_event(event_name, etapa="", submission_id=""):
    payload = {
        "event_name": event_name,
        "etapa": etapa,
        "submission_id": submission_id
    }
    try:
        requests.post(URL_WEBHOOK, json=payload, timeout=5)
    except:
        pass

# ---------------------------------------
# CSS
# ---------------------------------------
st.markdown("""
<style>
.stApp { background-color: #000c1a; color: #FFFFFF; }
.top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }
div[data-testid="stMetric"] {
  background-color: rgba(212, 175, 55, 0.05);
  border: 1px solid #D4AF37;
  padding: 15px;
  border-radius: 10px;
}
label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
.stButton>button {
  background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
  color: #001226 !important;
  width: 100%;
  font-weight: bold;
  padding: 15px;
  border-radius: 8px;
  font-size: 18px !important;
}
.card {
  background-color: rgba(255,255,255,0.03);
  border: 1px solid rgba(212,175,55,0.25);
  padding: 22px;
  border-radius: 14px;
}
.small { font-size: 15px !important; color: rgba(255,255,255,0.75) !important; }
.highlight { color: #D4AF37 !important; font-weight: bold; }
.question-card {
  background-color: rgba(255,255,255,0.03);
  border: 1px solid rgba(212,175,55,0.18);
  padding: 18px;
  border-radius: 12px;
  margin: 14px 0;
}
.question-text {
  font-size: 21px !important;
  line-height: 1.4;
  color: #FFFFFF !important;
  margin: 0 0 10px 0;
}
.laudo-container {
  background-color: rgba(255, 255, 255, 0.03);
  padding: 28px;
  border-radius: 15px;
  border-left: 6px solid #D4AF37;
  margin-top: 10px;
  line-height: 1.7;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] textarea {
  color: #001226 !important;
  background: #FFFFFF !important;
  border-radius: 8px !important;
}
div[data-testid="stTextInput"] input::placeholder {
  color: rgba(0,18,38,0.55) !important;
}
div[data-testid="stTextInput"] label {
  color: #FFFFFF !important;
}
button[kind="primary"] {
  background: rgba(212,175,55,0.18) !important;
  border: 1px solid #D4AF37 !important;
  color: #D4AF37 !important;
  font-weight: 800 !important;
}
button[kind="primary"]:hover {
  background: rgba(212,175,55,0.28) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# ESTADO
# ---------------------------------------
if "etapa" not in st.session_state:
    st.session_state.etapa = "intro"

if "event_aberto" not in st.session_state:
    st.session_state.event_aberto = False

if "event_oferta" not in st.session_state:
    st.session_state.event_oferta = False

if "total" not in st.session_state:
    st.session_state.total = 0

if "scores" not in st.session_state:
    st.session_state.scores = [0] * 9

if "zona" not in st.session_state:
    st.session_state.zona = ""

if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""

if "answers_json" not in st.session_state:
    st.session_state.answers_json = [None] * 45

# ---------------------------------------
# EVENTO: diagnostico_aberto
# ---------------------------------------
if not st.session_state.event_aberto:
    dispatch_event("diagnostico_aberto", etapa="inicio", submission_id="")
    st.session_state.event_aberto = True

# ---------------------------------------
# DADOS
# ---------------------------------------
dimensoes = [
    ("CLAREZA", "Capacidade de manter direção, prioridades e foco mesmo diante de pressão, excesso de demandas e ruído externo.", [
        "Mantenho clareza sobre o que é prioridade, mesmo quando surgem muitas demandas ao mesmo tempo.",
        "Meus objetivos de curto, médio e longo prazo estão claros e registrados, e planejo minhas ações com base neles.",
        "Mesmo pressionado ou cansado, continuo sabendo o que precisa ser feito primeiro.",
        "Consigo dizer “não” ao que não é prioridade sem me sentir culpado ou confuso.",
        "Sinto que minhas ações diárias estão alinhadas com a direção que quero para minha vida e carreira, na maior parte do tempo."
    ]),
    ("AUTOGESTÃO", "Capacidade de regular pensamentos, emoções e comportamentos sem depender de motivação externa.", [
        "Consigo manter meu comportamento alinhado ao que decidi, mesmo quando meu estado emocional oscila.",
        "Quando me sinto frustrado ou sobrecarregado, consigo me reorganizar sem perder totalmente o ritmo.",
        "Na maior parte do tempo, não dependo de motivação ou estímulos externos para cumprir o que é importante.",
        "Tenho consciência dos meus estados internos ao longo do dia e, na maioria das vezes, consigo agir assertivamente, independente do meu estado interno.",
        "Consigo retomar o controle rapidamente quando percebo que estou “saindo do eixo”."
    ]),
    ("PERCEPÇÃO CRÍTICA", "Capacidade de se observar, aprender com erros e ajustar rotas sem colapsar emocionalmente.", [
        "Consigo perceber quando meus padrões de comportamento precisam mudar, especialmente quando algo não funciona como eu esperava.",
        "Costumo olhar para meus erros com acolhimento, buscando aprendizado, sem me punir excessivamente.",
        "Consigo identificar rapidamente quando estou me sabotando.",
        "Aceito feedbacks sem entrar automaticamente em defesa.",
        "Uso meus erros como fonte de aprendizado, e não como motivo para me maltratar ou me castigar."
    ]),
    ("CELEBRAÇÃO", "Capacidade de reconhecer avanços, reforçar progresso e sustentar energia ao longo do processo.", [
        "Costumo comemorar pequenos avanços, mesmo quando parecem pouco significativos.",
        "Costumo celebrar pequenas conquistas sem perder o foco no próximo passo.",
        "Tenho o hábito de reconhecer meu próprio esforço e evolução.",
        "No dia a dia, costumo olhar mais para o que deu certo do que para os erros ou para o que falta.",
        "Celebrar meu progresso é um hábito comum e contribui para que eu me mantenha engajado e consistente ao longo do tempo."
    ]),
    ("APRENDIZADO ACELERADO", "Capacidade de aprender com rapidez, ajustar comportamento e evoluir a partir da experiência.", [
        "Aprendo com meus erros e ajusto meu comportamento sem repetir o mesmo padrão por muito tempo.",
        "Quando algo não está funcionando, busco novas formas de fazer, em vez de insistir no mesmo caminho.",
        "Aprendo observando pessoas mais experientes e aplico o que aprendo na prática.",
        "Testo novas abordagens mesmo correndo o risco de errar ou sair da zona de conforto.",
        "Mudo de opinião sem problemas, quando encontro uma ideia melhor que a minha"
    ]),
    ("REGULAÇÃO COGNITIVA (Self-Talk)", "Capacidade de regular pensamentos, interpretações e avaliações internas a serviço da ação.", [
        "Consigo perceber quando meus pensamentos começam a me atrapalhar ou me desorganizar.",
        "Quando algo dá errado, reorganizo meus pensamentos antes de tomar decisões impulsivas.",
        "Sou consciente dos meus pensamentos e eles me ajudam a agir, em vez de me paralisar ou desmotivar.",
        "Consigo questionar pensamentos negativos ou distorcidos, em vez de aceitá-los automaticamente.",
        "Mesmo em momentos difíceis, mantenho uma forma de pensar que sustenta ação e clareza."
    ]),
    ("AUTOIMAGEM (CRENÇAS)", "Conjunto de crenças que dirigem decisões e comportamento.", [
        "Sou capaz de aprender, me adaptar e melhorar continuamente.",
        "Tenho consciência de quando alguma crença limita minhas decisões ou ações.",
        "Costumo questionar minhas verdades para perceber quais delas não fazem mais sentido.",
        "Minha autoimagem me impulsiona à ação, não à paralisação.",
        "Acredito que vivo alinhado com a vida e os resultados que desejo construir."
    ]),
    ("AUTOPERFORMANCE", "Compromisso com evolução pessoal contínua e melhoria em relação a si mesmo.", [
        "Meço minha performance com base no meu próprio progresso, não em comparação com os outros.",
        "Tenho clareza sobre meus pontos fortes e sobre onde preciso evoluir.",
        "Sou comprometido em entregar o meu melhor dentro das condições que tenho.",
        "Sou meu principal ponto de referência para medir minha evolução, e observo quem está à frente com admiração, não com comparação negativa.",
        "Mesmo sob pressão, mantenho um padrão de qualidade nas minhas entregas."
    ]),
    ("AUTORRESPONSABILIDADE", "Capacidade de assumir escolhas, agir sobre o que controla e sair da posição de vítima.", [
        "Assumo responsabilidade pelas escolhas que faço, mesmo quando os resultados não são os esperados.",
        "Evito colocar a culpa em fatores externos quando algo não dá certo.",
        "Quando identifico um problema, foco no que posso fazer, e não no que não controlo.",
        "Costumo agir para mudar situações desconfortáveis em vez de reclamar delas.",
        "Reconheço que sou o principal responsável pelos meus resultados."
    ])
]

def simular_processamento():
    msgs = [
        "Processando suas respostas…",
        "Calculando sua Zona de Governança…",
        "Montando seu Radar por Dimensões…",
        "Gerando seu Direcionamento Estratégico…",
        "Finalizando…"
    ]
    box = st.empty()
    with st.spinner("Aguarde…"):
        for m in msgs:
            box.markdown(f"<p class='small'>🔎 {m}</p>", unsafe_allow_html=True)
            time.sleep(2.4)
    box.empty()

def calcular_zona(total: int) -> str:
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
    col1, col2 = st.columns([1.35, 0.65])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Bem-vindo ao Protocolo LIDERUM")
        st.markdown("""
Este diagnóstico não é um teste, nem um julgamento sobre quem você é.  
Ele foi criado para ajudar você a observar com mais clareza como está hoje sua forma de conduzir decisões, emoções, comportamento e direção.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### As 9 dimensões")
        for nome, desc, _ in dimensoes:
            st.markdown(f"**{nome}:** <span class='small'>{desc}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("INICIAR MEU DIAGNÓSTICO"):
        dispatch_event("diagnostico_iniciado", etapa="inicio", submission_id="")
        st.session_state.etapa = "questoes"
        st.rerun()

# ---------------------------------------
# QUESTÕES
# ---------------------------------------
elif st.session_state.etapa == "questoes":
    q_idx = 0
    respondidas = 0

    for dim_nome, dim_desc, perguntas in dimensoes:
        with st.expander(f"✨ DIMENSÃO: {dim_nome}"):
            for p in perguntas:
                st.radio(
                    p,
                    [1, 2, 3, 4, 5],
                    index=None,
                    key=f"q_{q_idx}",
                    horizontal=True
                )
                if st.session_state.get(f"q_{q_idx}") is not None:
                    respondidas += 1
                q_idx += 1

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if respondidas == 45:
            st.session_state.answers_json = [int(st.session_state[f"q_{i}"]) for i in range(45)]
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
    with st.form("lead_form"):
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")
        empresa = st.text_input("Empresa")
        cargo = st.text_input("Cargo")

        submit = st.form_submit_button("LIBERAR MEU LAUDO AGORA", type="primary")

        if submit and all([nome, email, whatsapp, empresa, cargo]):
            total = int(st.session_state.total)
            zona = calcular_zona(total)
            st.session_state.zona = zona
            st.session_state.nome_usuario = nome

            simular_processamento()

            dispatch_event(
                "diagnostico_concluido",
                etapa="resultado",
                submission_id=""
            )

            st.session_state.etapa = "resultado"
            st.rerun()

# ---------------------------------------
# RESULTADO
# ---------------------------------------
elif st.session_state.etapa == "resultado":
    if not st.session_state.event_oferta:
        dispatch_event(
            "oferta_laudo_exibida",
            etapa="resultado",
            submission_id=""
        )
        st.session_state.event_oferta = True

    st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    st.metric("Zona de Governança", st.session_state.zona)

    dispatch_event(
        "clique_laudo",
        etapa="resultado",
        submission_id=""
    )

    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
            <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
                        color: #001226; padding: 18px 40px; font-weight: 900; border-radius: 10px;
                        display: inline-block; width: 100%; max-width: 680px; font-size: 20px;'>
                ADQUIRIR LAUDO COMPLETO COM IA →
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
