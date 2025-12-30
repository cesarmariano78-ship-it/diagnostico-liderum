import streamlit as st
import plotly.graph_objects as go
import requests
import datetime
import time
import json
from urllib.parse import urlencode

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

CHECKOUT_URL = "https://pay.hotmart.com/SEU_LINK"  # <-- troque
WHATSAPP_URL = "https://wa.me/5581982602018?text=Ol%C3%A1!%20Acabei%20de%20fazer%20meu%20Diagn%C3%B3stico%20LIDERUM%20e%20quero%20conhecer%20as%20solu%C3%A7%C3%B5es."

# Para capturar UTM (opcional)
# Exemplo: ...streamlit.app/?utm_source=meta&utm_campaign=diag&utm_content=v1
query_params = st.query_params
utm_data = {
    "utm_source": query_params.get("utm_source", ""),
    "utm_medium": query_params.get("utm_medium", ""),
    "utm_campaign": query_params.get("utm_campaign", ""),
    "utm_content": query_params.get("utm_content", ""),
    "utm_term": query_params.get("utm_term", "")
}

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp { background-color: #000c1a; color: #FFFFFF; }
.top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }
label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

div[data-testid="stMetric"] {
    background-color: rgba(212, 175, 55, 0.05);
    border: 1px solid #D4AF37;
    padding: 15px;
    border-radius: 10px;
}

.stButton>button {
    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
    color: #001226 !important;
    width: 100%;
    font-weight: bold;
    padding: 15px;
    border-radius: 8px;
    font-size: 18px !important;
    border: none !important;
}

.secondary-btn a { text-decoration: none; }
.secondary-btn .box {
    background: rgba(212, 175, 55, 0.08);
    color: #D4AF37;
    border: 1px solid #D4AF37;
    padding: 12px 25px;
    font-weight: bold;
    border-radius: 8px;
    display: inline-block;
}

.question-text {
    font-size: 19px !important;
    color: #FFFFFF !important;
    margin-top: 18px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.10);
    padding-bottom: 10px;
}

.card {
    background-color: rgba(255, 255, 255, 0.03);
    padding: 22px;
    border-radius: 15px;
    border-left: 6px solid #D4AF37;
    margin-top: 10px;
    line-height: 1.6;
}

.highlight { color: #D4AF37 !important; font-weight: bold; }

.small { font-size: 15px !important; color: rgba(255,255,255,0.82) !important; }

hr { border-color: rgba(212,175,55,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "etapa" not in st.session_state: st.session_state.etapa = "home"   # home -> questoes -> captura -> processando -> resultado
if "total" not in st.session_state: st.session_state.total = 0
if "scores" not in st.session_state: st.session_state.scores = [0] * 9
if "zona" not in st.session_state: st.session_state.zona = ""
if "nome_usuario" not in st.session_state: st.session_state.nome_usuario = ""
if "event_id" not in st.session_state:
    st.session_state.event_id = f"diag_{int(time.time())}"

def log_event(event_name: str, extra: dict | None = None):
    payload = {
        "type": "event",
        "event_id": st.session_state.event_id,
        "event": event_name,
        "ts": datetime.datetime.now().isoformat(),
        **utm_data
    }
    if extra:
        payload.update(extra)
    try:
        requests.post(URL_WEBHOOK, json=payload, timeout=6)
    except:
        pass

st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# =========================
# QUESTIONS (placeholder)
# IMPORTANTE:
# - Mantenha 9 dimensões
# - Cada dimensão precisa ter 5 perguntas (total 45)
# - Aqui eu deixei a sua estrutura e você só troca os textos.
# =========================

dimensoes = [
    ("Clareza e Direção", [
        "Mantenho clareza sobre o que é prioridade, mesmo quando surgem muitas demandas ao mesmo tempo.",
        "Meus objetivos de curto, médio e longo prazo estão registrados e eu organizo minhas ações com base neles.",
        "Mesmo pressionado ou cansado, continuo sabendo o que precisa ser feito primeiro.",
        "Consigo dizer “não” ao que não é prioridade sem me sentir culpado ou confuso.",
        "Sinto que minhas ações diárias estão alinhadas com a direção que quero para minha vida e carreira na maior parte do tempo.",
    ]),
    ("Autogestão", [
        "Consigo manter meu comportamento alinhado ao que decidi, mesmo quando meu estado emocional oscila.",
        "Quando me sinto frustrado ou sobrecarregado, consigo me reorganizar sem perder totalmente o ritmo.",
        "Não dependo de motivação ou estímulo externo para cumprir o que é importante.",
        "Tenho consciência dos meus estados internos ao longo do dia e ajo apesar deles quando necessário.",
        "Consigo retomar o controle rapidamente quando estou “saindo do eixo”.",
    ]),
    ("Percepção Crítica", [
        "Quando algo não funciona, eu ajusto o que faço em vez de insistir no mesmo padrão por muito tempo.",
        "Olho para meus erros com firmeza e respeito, sem me punir nem me justificar.",
        "Consigo identificar rapidamente quando estou me sabotando.",
        "Aceito feedbacks sem entrar automaticamente em defesa.",
        "Uso meus erros como aprendizado, não como motivo para me maltratar.",
    ]),
    ("Celebração", [
        "Comemoro pequenos avanços, mesmo quando parecem pouco.",
        "Celebro conquistas sem perder o foco no próximo passo.",
        "Reconheço meu esforço e evolução com consistência.",
        "No dia a dia, olho mais para o que deu certo do que para o que faltou.",
        "Celebrar meu progresso me ajuda a sustentar energia no longo prazo.",
    ]),
    # As próximas 5 dimensões: você troca depois com a versão final
    ("Aprendizado Acelerado", [
        "Quando algo não está funcionando, busco novas formas de fazer em vez de insistir no mesmo caminho.",
        "Testo abordagens novas mesmo correndo risco de errar.",
        "Aprendo com pessoas de referência e transformo isso em ação prática.",
        "Consigo incorporar uma habilidade nova quando ela é necessária.",
        "Eu evoluo meu repertório com consistência, não só por impulso.",
    ]),
    ("Regulação Cognitiva", [
        "Quando algo dá errado, reorganizo meus pensamentos antes de tomar decisões impulsivas.",
        "Sou consciente dos meus pensamentos e eles me ajudam a agir, em vez de me paralisar ou desmotivar.",
        "Consigo questionar pensamentos negativos ou distorcidos, em vez de aceitá-los automaticamente.",
        "Consigo reduzir ruído mental e recuperar foco quando necessário.",
        "Meu diálogo mental tende a ser firme, claro e orientado a solução.",
    ]),
    ("Crenças Operantes", [
        "Sou capaz de aprender, me adaptar e melhorar continuamente.",
        "Percebo quando uma crença limita minhas decisões ou ações.",
        "Questiono “verdades antigas” para ver o que ainda faz sentido.",
        "Minha autoimagem me impulsiona a agir, não me paralisa.",
        "Acredito que estou construindo uma vida coerente com os resultados que desejo.",
    ]),
    ("Autoperformance", [
        "Eu meço minha evolução pelo meu próprio progresso, não por comparação com os outros.",
        "Busco melhorar um pouco a cada ciclo, com consistência.",
        "Entrego meu melhor dentro das condições reais que tenho hoje.",
        "Mesmo sob pressão, mantenho um padrão de qualidade nas minhas entregas.",
        "Quando erro, volto para o processo e ajusto com maturidade.",
    ]),
    ("Autorresponsabilidade", [
        "Evito colocar a culpa em fatores externos quando algo não dá certo.",
        "Quando identifico um problema, foco no que posso fazer — não no que não controlo.",
        "Eu ajo para mudar situações desconfortáveis em vez de apenas reclamar delas.",
        "Reconheço que sou o maior responsável direto pelos meus resultados.",
        "Assumo responsabilidade por escolhas e consequências, mesmo quando é desconfortável.",
    ]),
]

# Flatten 45 questions
questoes_flat = []
for dname, pergs in dimensoes:
    questoes_flat.extend([(dname, p) for p in pergs])

# =========================
# HOME (Tela 0)
# =========================
if st.session_state.etapa == "home":
    log_event("view_home")

    st.markdown("""
    <div class="card">
      <div class="highlight" style="font-size:22px;">Antes de começar</div>
      <div class="small" style="margin-top:8px;">
        • Leva cerca de <b>4 a 6 minutos</b><br/>
        • Não é julgamento — é um retrato do momento atual<br/>
        • Seus dados são usados para liberar seu laudo e direcionar recomendações<br/>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div style="font-size:18px; margin-bottom:10px;">
        Como responder:
      </div>
      <div class="small">
        Marque de <b>1</b> (discordo totalmente) a <b>5</b> (concordo totalmente), pensando no seu comportamento real das últimas semanas.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("COMEÇAR DIAGNÓSTICO"):
        log_event("start_clicked")
        st.session_state.etapa = "questoes"
        st.rerun()

# =========================
# QUESTOES
# =========================
elif st.session_state.etapa == "questoes":
    log_event("view_questions")

    st.markdown("""
    <div class="card">
      <div class="highlight" style="font-size:18px;">Instrução rápida</div>
      <div class="small" style="margin-top:6px;">
        Clique em cada dimensão para responder. Você só avança quando completar as 45 perguntas.
      </div>
    </div>
    """, unsafe_allow_html=True)

    q_idx = 0
    for dim_name, pergs in dimensoes:
        with st.expander(f"✨ DIMENSÃO: {dim_name.upper()}"):
            for p in pergs:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(
                    f"R_{q_idx}",
                    [1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    key=f"q_{q_idx}",
                    label_visibility="collapsed",
                )
                q_idx += 1

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        answered = sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None)
        if answered == 45:
            # scores por dimensão (5 perguntas cada)
            st.session_state.scores = [
                sum(st.session_state[f"q_{j}"] for j in range(i, i + 5))
                for i in range(0, 45, 5)
            ]
            st.session_state.total = sum(st.session_state.scores)

            log_event("questions_completed", {
                "total": st.session_state.total,
                "scores": json.dumps(st.session_state.scores),
            })

            st.session_state.etapa = "captura"
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")

# =========================
# CAPTURA
# =========================
elif st.session_state.etapa == "captura":
    log_event("view_capture")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>DIAGNÓSTICO CONCLUÍDO</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small' style='text-align:center; margin-bottom:10px;'>Preencha para liberar seu laudo agora.</div>", unsafe_allow_html=True)

        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            empresa = st.text_input("Empresa")
            cargo = st.text_input("Cargo")

            submit = st.form_submit_button("LIBERAR MEU LAUDO AGORA")

            if submit:
                if all([nome, email, whatsapp, empresa, cargo]):
                    st.session_state.nome_usuario = nome.strip()

                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona = z

                    # Captura respostas individuais (q1..q45)
                    respostas = [st.session_state.get(f"q_{i}") for i in range(45)]

                    payload = {
                        "type": "lead",
                        "event_id": st.session_state.event_id,
                        "ts": datetime.datetime.now().isoformat(),
                        "nome": nome,
                        "email": email,
                        "whatsapp": whatsapp,
                        "empresa": empresa,
                        "cargo": cargo,
                        "total": t,
                        "zona": z,
                        "scores": st.session_state.scores,
                        "respostas": respostas,
                        **utm_data
                    }

                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                    except:
                        pass

                    log_event("lead_submitted", {"zona": z, "total": t})
                    st.session_state.etapa = "processando"
                    st.rerun()
                else:
                    st.warning("Por favor, preencha todos os campos.")

# =========================
# PROCESSANDO (spinner + mensagens)
# =========================
elif st.session_state.etapa == "processando":
    log_event("view_processing")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='highlight' style='font-size:20px;'>Gerando seu laudo…</div>", unsafe_allow_html=True)

    msg = st.empty()
    bar = st.progress(0)

    steps = [
        "Organizando suas respostas…",
        "Calculando padrões por dimensão…",
        "Identificando pontos de força e risco…",
        "Montando direcionamento estratégico…",
        "Finalizando…"
    ]

    total_seconds = 11  # 10-12s, como você pediu
    tick = total_seconds / len(steps)

    for i, s in enumerate(steps, start=1):
        msg.markdown(f"<div class='small'>{s}</div>", unsafe_allow_html=True)
        bar.progress(int((i / len(steps)) * 100))
        time.sleep(tick)

    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.etapa = "resultado"
    st.rerun()

# =========================
# RESULTADO
# =========================
elif st.session_state.etapa == "resultado":
    log_event("view_result")

    st.markdown(f"### Análise Individual: <span class='highlight'>{st.session_state.nome_usuario.upper()}</span>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    with c2:
        st.metric("Zona de Governança", st.session_state.zona)

    st.write("---")

    col_l, col_r = st.columns([1.2, 0.8])

    with col_l:
        categories = [d[0].split(" ")[0] if len(d[0]) > 16 else d[0] for d in dimensoes]  # rótulos menores
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=st.session_state.scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(212, 175, 55, 0.35)',
            line=dict(color='#D4AF37', width=4)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,12,26,1)",
                radialaxis=dict(visible=True, range=[0, 25], color="#888", gridcolor="rgba(212,175,55,0.1)")
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            height=600,
            margin=dict(l=80, r=80, t=20, b=20),
            font=dict(color="white", size=16)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Direcionamento Estratégico")

        nome = st.session_state.nome_usuario
        zona = st.session_state.zona

        if zona == "ELITE":
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, sua pontuação indica uma governança pessoal acima da média.
            O foco agora é blindar constância e evitar a “cegueira da eficiência”: fazer muito, mas perder direção.
            Se quiser profundidade, o laudo completo destrincha suas 9 dimensões e entrega um plano prático.
            """, unsafe_allow_html=True)

        elif zona == "OSCILAÇÃO":
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, você está em zona de oscilação.
            Há picos de entrega e vales de inércia — normalmente por instabilidade de rotina, pressão e ruído mental.
            O laudo completo aponta exatamente onde sua energia está vazando e te dá um plano de execução.
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, você está em modo de sobrevivência.
            Não é “falta de força”: é falta de estrutura e intervenção no ponto vital certo.
            O laudo completo mostra o que está te minando e quais ações reconstroem controle e direção.
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Próximo passo</h3>", unsafe_allow_html=True)
    st.markdown("<div class='small' style='text-align:center;'>Se você quer o plano completo (com ações), acesse abaixo.</div>", unsafe_allow_html=True)

    # Botão de checkout com tracking
    if st.button("ADQUIRIR MEU LAUDO COMPLETO (R$47)"):
        log_event("checkout_clicked", {"checkout_url": CHECKOUT_URL})
        st.markdown(f"<meta http-equiv='refresh' content='0;url={CHECKOUT_URL}'>", unsafe_allow_html=True)

    st.markdown("<div class='secondary-btn' style='margin-top:10px;'>"
                f"<a href='{WHATSAPP_URL}' target='_blank'>"
                "<div class='box'>FALE COM NOSSA EQUIPE</div>"
                "</a></div>", unsafe_allow_html=True)

    # Recomeçar (eu deixei, mas discreto; você decide manter ou remover)
    with st.expander("Precisa refazer o diagnóstico?"):
        st.markdown("<div class='small'>Se você respondeu no impulso ou quer refazer com calma, reinicie.</div>", unsafe_allow_html=True)
        if st.button("RECOMEÇAR DIAGNÓSTICO"):
            log_event("restart_clicked")
            # limpa respostas
            for i in range(45):
                if f"q_{i}" in st.session_state:
                    del st.session_state[f"q_{i}"]
            st.session_state.total = 0
            st.session_state.scores = [0]*9
            st.session_state.zona = ""
            st.session_state.nome_usuario = ""
            st.session_state.etapa = "home"
            st.rerun()
