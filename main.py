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

# Checkout Eduzz (base)
EDUZZ_CHECKOUT_BASE = "https://sun.eduzz.com/7977E15B9E"

# ---------------------------------------
# CSS (mantém estética + corrige inputs)
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

/* Tipografia global */
label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

/* Botões */
.stButton>button {
  background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
  color: #001226 !important;
  width: 100%;
  font-weight: bold;
  padding: 15px;
  border-radius: 8px;
  font-size: 18px !important;
}

/* Cards – moldura fina verde Brasil */
.card {
  background-color: rgba(255,255,255,0.02);
  border: 0.5px solid #1DB954; /* verde Brasil */
  padding: 22px;
  border-radius: 12px;
}

/* Barra horizontal fina (página toda) */
.divider-brasil {
  height: 2px;
  background-color: #1DB954;
  opacity: 0.85;
  width: 100%;
  border-radius: 2px;
  margin: 20px 0;
}

/* Divisor meia largura – usado dentro dos blocos (para não cortar a tela toda) */
.divider-half {
  height: 2px;
  background-color: #1DB954;
  opacity: 0.85;
  width: 100%;
  max-width: 520px;
  margin: 20px auto;      /* centraliza */
  border-radius: 2px;
}

.small { font-size: 15px !important; color: rgba(255,255,255,0.75) !important; }
.highlight { color: #D4AF37 !important; font-weight: bold; }

/* Questões: mais destaque */
.question-card {
  background-color: rgba(255,255,255,0.03);
  border: 1px solid rgba(212,175,55,0.18);
  padding: 18px;
  border-radius: 12px;
  margin: 14px 0;
}

/* Botão TESTE quase invisível */
button[data-testid="baseButton-secondary"] {
  opacity: 0.08;
  transform: scale(0.85);
}
button[data-testid="baseButton-secondary"]:hover {
  opacity: 0.25;
}

/* Laudo */
.laudo-container {
  background-color: rgba(255, 255, 255, 0.03);
  padding: 28px;
  border-radius: 15px;
  margin-top: 10px;
  line-height: 1.7;
}

/* Inputs: corrigir texto digitado (estava branco no branco) */
div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] textarea {
  color: #001226 !important;
  background: #FFFFFF !important;
  border-radius: 8px !important;
}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder {
  color: rgba(0,18,38,0.55) !important;
}

/* Label dos inputs */
div[data-testid="stTextInput"] label {
  color: #FFFFFF !important;
}

/* Botão do FORM (submit) - garante contraste */
button[kind="primary"] {
  background: rgba(212,175,55,0.18) !important;
  border: 1px solid #D4AF37 !important;
  color: #D4AF37 !important;
  font-weight: 800 !important;
}
button[kind="primary"]:hover {
  background: rgba(212,175,55,0.28) !important;
}

/* =========================
   MOLDURA GLOBAL — fina + verde Brasil
   ========================= */
:root { --br-green: #009C3B; }

div.block-container {
  border: 1px solid var(--br-green) !important;
  border-radius: 10px !important;
  padding: 18px 18px 28px 18px !important;
}

/* =========================
   BOTÃO EXPANDIR LAUDO (verde Brasil)
   ========================= */
details.laudo-details > summary {
  list-style: none;
  cursor: pointer;
  user-select: none;

  background: var(--br-green);
  color: #ffffff;
  border: 1px solid rgba(0,0,0,0.15);
  border-radius: 10px;

  padding: 16px 18px;
  font-weight: 900;
  font-size: 19.8px;
  text-align: center;
}

details.laudo-details > summary::-webkit-details-marker {
  display: none;
}

details.laudo-details[open] > summary {
  filter: brightness(0.95);
}

.laudo-body {
  margin-top: 14px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(212,175,55,0.20);
  border-radius: 12px;
  padding: 18px;
  line-height: 1.7;
}
/* =========================
   AJUSTE FINAL — CENTRALIZAÇÃO REAL DOS BOTÕES
   ========================= */

/* Centraliza o container do botão do Streamlit */
div.stButton {
  display: flex !important;
  justify-content: center !important;
}

/* Define largura fixa para não “puxar” visualmente para a esquerda */
div.stButton > button {
  width: 380px !important;     /* desktop */
  max-width: 100% !important;  /* mobile */
}
/* =========================
   BOTÃO TESTE (micro, discreto, canto)
   ========================= */
#teste-anchor + div[data-testid="stButton"] button {
  width: 14px !important;
  height: 14px !important;
  min-height: 14px !important;

  padding: 0 !important;
  border-radius: 999px !important;

  font-size: 0 !important;     /* “mata” o texto */
  line-height: 0 !important;

  opacity: 0.08 !important;   /* quase invisível */
  background: #ffffff !important;
  border: 1px solid rgba(255,255,255,0.25) !important;

  box-shadow: none !important;
}

#teste-anchor + div[data-testid="stButton"] button:hover {
  opacity: 0.22 !important;   /* aparece só no hover */
}


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

if "answers_json" not in st.session_state:
    st.session_state.answers_json = [None] * 45

if "submission_id" not in st.session_state:
    st.session_state.submission_id = ""

if "sent_events" not in st.session_state:
    st.session_state.sent_events = set()

# ---------------------------------------
# TRACKING (mínimo, dedupe, falha silenciosa)
# ---------------------------------------
def _now_utc_iso():
    return datetime.datetime.utcnow().isoformat()

def _send_event(event_name: str, etapa: str = "", meta: dict | None = None):
    try:
        submission_id = st.session_state.submission_id or ""
        dedupe_key = f"{event_name}:{submission_id}"
        if dedupe_key in st.session_state.sent_events:
            return

        payload = {
            "type": "event",
            "event_name": event_name,
            "timestamp": _now_utc_iso(),
            "submission_id": submission_id,
            "app_version": APP_VERSION,
            "etapa": etapa,
        }
        if isinstance(meta, dict) and meta:
            payload["meta"] = meta

        requests.post(URL_WEBHOOK, json=payload, timeout=6)
        st.session_state.sent_events.add(dedupe_key)
    except:
        pass

# ---------------------------------------
# TESTE (preencher 45 respostas em 1 clique - discreto e sem quebrar UX)
# ---------------------------------------
def _preencher_respostas_aleatorias():
    for i in range(45):
        st.session_state[f"q_{i}"] = random.randint(1, 5)

# ---------------------------------------
# DADOS (9 dimensões + 45 perguntas DEFINIDAS)
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

def _build_eduzz_checkout_url(submission_id: str) -> str:
    q = {"utm_content": submission_id or ""}
    return f"{EDUZZ_CHECKOUT_BASE}?{urllib.parse.urlencode(q)}"

def _texto_laudo_expandido(nome: str, total: int, zona: str) -> str:
    if zona == "OSCILAÇÃO":
        return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: OSCILAÇÃO

{nome}, seu padrão atual é de Oscilação.

Isso significa que você alterna entre períodos de boa entrega e momentos de queda, perda de foco ou desaceleração — mesmo tendo capacidade e repertório.

Na prática, o problema não está na sua competência, mas na instabilidade da sua autogestão e da regulação cognitiva, o que impacta diretamente:

constância de execução

clareza de prioridade

ritmo operacional

O efeito mais comum desse padrão é simples:
você até sabe o que fazer, mas não sustenta o mesmo nível de ação por tempo suficiente para gerar resultados consistentes.

O objetivo aqui não é motivar.
É estabilizar sua forma de se governar, para que a execução deixe de depender de emoção, contexto ou “fase boa”.

 O ponto de atenção

Quando a Oscilação não é tratada, ela costuma gerar:

muitos recomeços e pouca continuidade

decisões instáveis ou adiadas

desgaste mental desnecessário

sensação de esforço alto com retorno irregular

Seu gráfico mostra tendências.
O que ainda falta é clareza prática sobre onde intervir primeiro.
"""
    if zona == "ELITE":
        return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: ELITE

{nome}, seus resultados indicam que você está na Zona de Elite.

Isso significa que sua governança pessoal já opera em um nível elevado.
Você apresenta clareza, capacidade de execução e autonomia para conduzir sua vida com consistência acima da média.

O principal ponto de atenção nessa zona não é capacidade, nem esforço.
É a manutenção do nível ao longo do tempo.

Pessoas na Zona de Elite costumam executar bem, tomar boas decisões e sustentar resultados — mas podem operar no automático, deixando de revisar fundamentos essenciais como:

clareza contínua

rotina funcional

autorresponsabilidade ativa

Aqui, o trabalho não é corrigir falhas evidentes.
É refinar decisões, proteger o essencial e elevar a precisão da execução, para que o desempenho não dependa de contexto, fase ou excesso de carga.

Quem opera nesse nível não pode relaxar no fundamento —
porque é justamente o fundamento que sustenta a elite.

O objetivo agora é claro:
blindar constância, reduzir desgaste e transformar competência em impacto sustentado.
"""
    return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: SOBREVIVÊNCIA

{nome}, você está na Zona de Sobrevivência.

Isso indica que sua governança pessoal está operando no limite.
Energia, clareza, rotina e disciplina entraram em modo reativo, fazendo com que você funcione mais para apagar incêndios do que para construir avanço real.

Nesse estado, a vida passa a ser conduzida por urgências, demandas externas e cansaço acumulado.
Decisões deixam de ser estratégicas e passam a ser defensivas.

Normalmente, esse padrão aparece quando autogestão, clareza e regulação cognitiva estão fragilizadas ao mesmo tempo, gerando:

baixa previsibilidade

dificuldade de priorização

execução inconsistente

desgaste emocional elevado

Aqui, não é hora de fazer mais.
É hora de estancar perda de energia, reorganizar o essencial e recuperar capacidade mínima de condução.

O objetivo inicial na Zona de Sobrevivência é simples e vital:
parar o colapso, restaurar estabilidade básica e criar espaço interno para decisões melhores.

Sem isso, qualquer tentativa de evolução vira mais peso — e não solução.
"""

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; margin-top: 0;'>PROTOCOLO LIDERUM</h1>", unsafe_allow_html=True)

# ---------------------------------------
# ETAPA 0: INTRO (100% CENTRALIZADA)
# ---------------------------------------
if st.session_state.etapa == "intro":
    col_c = st.columns([1, 2.2, 1])[1]
    with col_c:
        st.markdown("<div class='card intro-center'>", unsafe_allow_html=True)

        st.markdown(
            "<h1 style='text-align:center; margin: 0 0 6px 0;'>PROTOCOLO LIDERUM</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h3 style='text-align:center; margin: 0 0 14px 0;'>Diagnóstico de Governança Pessoal</h3>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <p style="text-align:center; margin-top: 0;">
        Descubra, em poucos minutos, onde sua autoliderança está sólida —<br/>
        e onde ela está quebrando sua constância, foco e execução.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        # CTA principal (CENTRALIZADO)
        cta1_l, cta1_c, cta1_r = st.columns([1, 2, 1])
        with cta1_c:
            if st.button("Iniciar diagnóstico gratuito", key="cta_intro_top"):
                if not st.session_state.submission_id:
                    st.session_state.submission_id = str(uuid.uuid4())
                _send_event("diagnostico_iniciado", etapa="intro")
                st.session_state.etapa = "questoes"
                st.rerun()

        st.markdown("<p class='small' style='text-align:center;'>Leva de 6 a 8 minutos.</p>", unsafe_allow_html=True)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(212,175,55,0.18);'/>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Antes de começar</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Este diagnóstico não é um teste psicológico, nem um julgamento sobre quem você é.<br/>
        Ele foi criado para ajudar você a observar com mais clareza como está hoje a sua forma de conduzir
        decisões, emoções, comportamento e direção.
        </p>
        <p style="text-align:center; font-weight: 800;">
        Aqui não se mede intenção. Mede-se consistência.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Por que isso importa</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Muitas pessoas são competentes, estudam, se esforçam —<br/>
        mas os resultados oscilam porque a forma de se governar é instável.
        </p>
        <p style="text-align:center;">
        Este diagnóstico existe para revelar exatamente isso.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Privacidade e sigilo</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Suas respostas são confidenciais e usadas exclusivamente para gerar seu diagnóstico e direcionamento personalizado.<br/>
        Nenhuma informação será compartilhada.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        # CTA final (CENTRALIZADO) — voltou ao “miolo”
        cta2_l, cta2_c, cta2_r = st.columns([1, 2, 1])
        with cta2_c:
            if st.button("Iniciar diagnóstico gratuito", key="cta_intro_bottom"):
                if not st.session_state.submission_id:
                    st.session_state.submission_id = str(uuid.uuid4())
                _send_event("diagnostico_iniciado", etapa="intro")
                st.session_state.etapa = "questoes"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------
# ETAPA 1: QUESTÕES
# ---------------------------------------
elif st.session_state.etapa == "questoes":
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

    top_l, top_r = st.columns([0.97, 0.03])

    with top_r:
        st.markdown("<div id='teste-anchor'></div>", unsafe_allow_html=True)
        if st.button("•", key="btn_teste_micro", help="Preenche as 45 respostas aleatoriamente (uso interno)."):
      _preencher_respostas_aleatorias()
      st.rerun()


    q_idx = 0
    respondidas = 0

    for dim_nome, dim_desc, perguntas in dimensoes:
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
                    label_visibility="collapsed"
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.get(f"q_{q_idx}") is not None:
                    respondidas += 1
                q_idx += 1

    st.markdown(f"<p class='small'>Progresso: <span class='highlight'>{respondidas}/45</span> respostas concluídas.</p>", unsafe_allow_html=True)

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if respondidas == 45:
            st.session_state.answers_json = [int(st.session_state[f"q_{i}"]) for i in range(45)]
            st.session_state.scores = [
                sum(st.session_state[f"q_{j}"] for j in range(i, i + 5))
                for i in range(0, 45, 5)
            ]
            st.session_state.total = sum(st.session_state.scores)

            if not st.session_state.submission_id:
                st.session_state.submission_id = str(uuid.uuid4())
            _send_event("diagnostico_concluido", etapa="questoes")

            st.session_state.etapa = "captura"
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")

# ---------------------------------------
# ETAPA 2: CAPTURA
# ---------------------------------------
elif st.session_state.etapa == "captura":
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
                        "answers_json": [int(v) for v in st.session_state.answers_json]
                    }

                    simular_processamento()

                    ok = False
                    try:
                        r = requests.post(URL_WEBHOOK, json=payload, timeout=12)
                        if r is not None and getattr(r, "status_code", 0) == 200:
                            txt = (r.text or "").strip().upper()
                            if "OK" in txt:
                                ok = True
                    except:
                        pass

                    if ok:
                        _send_event("lead_enviado", etapa="captura")

                    st.session_state.etapa = "resultado"
                    st.rerun()
                else:
                    st.warning("Por favor, preencha todos os campos.")

# ---------------------------------------
# ETAPA 3: LAUDO
# ---------------------------------------
elif st.session_state.etapa == "resultado":
    st.markdown("""
    <style>
      .btn-brasil {
        background: #009C3B;
        color: #ffffff;
        border: 1px solid #009C3B;
        padding: 16px 22px;
        border-radius: 10px;
        font-weight: 900;
        display: inline-block;
        width: 100%;
        max-width: 720px;
        font-size: 20px;
        text-align: center;
        cursor: pointer;
      }

      .btn-outline-brasil {
        background: transparent;
        color: #009C3B;
        border: 1px solid #009C3B;
        padding: 12px 18px;
        border-radius: 10px;
        font-weight: 900;
        display: inline-block;
        width: 100%;
        text-align: center;
        cursor: pointer;
      }

      details.laudo-details { width: 100%; margin: 10px 0 0 0; }
      details.laudo-details > summary { list-style: none; outline: none; }
      details.laudo-details > summary::-webkit-details-marker { display: none; }

      .laudo-text {
        margin-top: 14px;
        padding: 18px 18px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,156,59,0.35);
        line-height: 1.7;
      }
    </style>
    """, unsafe_allow_html=True)

    # Garante submission_id e gera checkout_url (somente ETAPA 3)
    if not st.session_state.submission_id:
        st.session_state.submission_id = str(uuid.uuid4())
    checkout_url = _build_eduzz_checkout_url(st.session_state.submission_id)

    # =========================
    # TOPO DA PÁGINA
    # =========================
    st.markdown(
        f"### Análise Individual: <span class='highlight'>{st.session_state.nome_usuario.upper()}</span>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    with c2:
        st.metric("Zona de Governança", st.session_state.zona)

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    # =========================
    # CORPO (Radar + Laudo)
    # =========================
    col_l, col_r = st.columns([1.2, 0.8])

    with col_l:
        categorias_radar = [d[0].split(" (")[0] for d in dimensoes]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=st.session_state.scores,
            theta=categorias_radar,
            fill="toself",
            fillcolor="rgba(212, 175, 55, 0.35)",
            line=dict(color="#D4AF37", width=4)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,12,26,1)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 25],
                    color="#888",
                    gridcolor="rgba(212,175,55,0.1)"
                )
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            height=600,
            margin=dict(l=80, r=80, t=20, b=20),
            font=dict(color="white", size=16)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)

        nome = st.session_state.nome_usuario
        zona = st.session_state.zona

        # Texto do laudo (agora com f-string para preencher {nome}/{zona})
        if zona == "OSCILAÇÃO":
            laudo_texto = f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {st.session_state.total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: OSCILAÇÃO

{nome}, seu padrão atual é de Oscilação.

Isso significa que você alterna entre períodos de boa entrega e momentos de queda, perda de foco ou desaceleração — mesmo tendo capacidade e repertório.

Na prática, o problema não está na sua competência, mas na instabilidade da sua autogestão e da regulação cognitiva, o que impacta diretamente:

constância de execução

clareza de prioridade

ritmo operacional

O efeito mais comum desse padrão é simples:
você até sabe o que fazer, mas não sustenta o mesmo nível de ação por tempo suficiente para gerar resultados consistentes.

O objetivo aqui não é motivar.
É estabilizar sua forma de se governar, para que a execução deixe de depender de emoção, contexto ou “fase boa”.

⚠️ O ponto de atenção

Quando a Oscilação não é tratada, ela costuma gerar:

muitos recomeços e pouca continuidade

decisões instáveis ou adiadas

desgaste mental desnecessário

sensação de esforço alto com retorno irregular

Seu gráfico mostra tendências.
O que ainda falta é clareza prática sobre onde intervir primeiro.
""".strip()
        elif zona == "ELITE":
            laudo_texto = f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {st.session_state.total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: ELITE

{nome}, seus resultados indicam que você está na Zona de Elite.

Isso significa que sua governança pessoal já opera em um nível elevado.
Você apresenta clareza, capacidade de execução e autonomia para conduzir sua vida com consistência acima da média.

O principal ponto de atenção nessa zona não é capacidade, nem esforço.
É a manutenção do nível ao longo do tempo.

Pessoas na Zona de Elite costumam executar bem, tomar boas decisões e sustentar resultados — mas podem operar no automático, deixando de revisar fundamentos essenciais como:

clareza contínua

rotina funcional

autorresponsabilidade ativa

Aqui, o trabalho não é corrigir falhas evidentes.
É refinar decisões, proteger o essencial e elevar a precisão da execução, para que o desempenho não dependa de contexto, fase ou excesso de carga.

Quem opera nesse nível não pode relaxar no fundamento —
porque é justamente o fundamento que sustenta a elite.

O objetivo agora é claro:
blindar constância, reduzir desgaste e transformar competência em impacto sustentado.
""".strip()
        else:
            laudo_texto = f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {st.session_state.total} / 225
Zona de Governança: {zona}

 Direcionamento Estratégico
Zona de Governança: SOBREVIVÊNCIA

{nome}, você está na Zona de Sobrevivência.

Isso indica que sua governança pessoal está operando no limite.
Energia, clareza, rotina e disciplina entraram em modo reativo, fazendo com que você funcione mais para apagar incêndios do que para construir avanço real.

Nesse estado, a vida passa a ser conduzida por urgências, demandas externas e cansaço acumulado.
Decisões deixam de ser estratégicas e passam a ser defensivas.

Normalmente, esse padrão aparece quando autogestão, clareza e regulação cognitiva estão fragilizadas ao mesmo tempo, gerando:

baixa previsibilidade

dificuldade de priorização

execução inconsistente

desgaste emocional elevado

Aqui, não é hora de fazer mais.
É hora de estancar perda de energia, reorganizar o essencial e recuperar capacidade mínima de condução.

O objetivo inicial na Zona de Sobrevivência é simples e vital:
parar o colapso, restaurar estabilidade básica e criar espaço interno para decisões melhores.

Sem isso, qualquer tentativa de evolução vira mais peso — e não solução.
""".strip()

        st.markdown(f"""
<details class="laudo-details">
  <summary>
    <div class="btn-brasil">📄 Clique aqui para expandir e ler o seu Laudo</div>
  </summary>
  <div class="laudo-text">
    <pre style="white-space: pre-wrap; margin: 0; font-family: inherit;">{laudo_texto}</pre>
  </div>
</details>
        """, unsafe_allow_html=True)

        # Divisor meia largura (para não cortar a tela toda)
        st.markdown("<div class='divider-half'></div>", unsafe_allow_html=True)

        # Próximo passo lógico (UMA ÚNICA VEZ)
        st.markdown("<div class='card' style='margin-top:18px;'>", unsafe_allow_html=True)
        st.markdown("""
### Próximo passo lógico
Acesse o **Laudo Completo + Plano de Ação** e receba também a leitura clara das 9 dimensões com:

- Seu padrão atual e principais pontos de atenção  
- Interpretação objetiva da sua zona de governança  
- Priorização estratégica (o que atacar primeiro)  
- Plano de ação prático:
  - 07 dias para organização e foco
  - 30 dias para consolidação e consistência

O objetivo não é fazer mais.  
É agir com critério, clareza e execução sustentada, no nível que você está hoje.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # fecha .laudo-container

    # =========================
    # CTA CHECKOUT (fora do col_r, abaixo do bloco)
    # =========================
    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center; font-size:16px; opacity:0.85; margin: 10px 0 10px 0;'>"
        "Se você quer clareza prática sobre onde intervir primeiro — este é o próximo passo."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='text-align: center; margin: 22px 0 6px 0;'>
            <a href='{checkout_url}' target='_blank' style='text-decoration: none;'>
                <div style='
                    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
                    color: #001226;
                    padding: 22px 44px;
                    font-weight: 900;
                    border-radius: 10px;
                    display: inline-block;
                    width: 100%;
                    max-width: 760px;
                    font-size: 22px;
                '>
                    QUERO MEU LAUDO COMPLETO + PLANO DE AÇÃO →
                </div>
            </a>
        </div>

        <div style='text-align:center; margin-bottom: 18px;'>
            <span class='small'>Entrega imediata por e-mail • leitura direta • confidencial</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================
    # Rodapé (WhatsApp)
    # =========================
    wa_url = "https://wa.me/5581986245870?text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM%20e%20quero%20conhecer%20as%20soluções."

    st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)
    col_wa_l, col_wa_r = st.columns([1, 1])
    with col_wa_l:
        st.write("")
    with col_wa_r:
        st.markdown(
            f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div class="btn-outline-brasil">Fale com nossa equipe</div>
            </a>
            """,
            unsafe_allow_html=True
        )
