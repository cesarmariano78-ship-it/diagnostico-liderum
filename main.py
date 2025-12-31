import streamlit as st
import plotly.graph_objects as go
import requests
import time
import datetime
import uuid

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

# -----------------------------
# CSS (SEM quebrar layout do Streamlit)
# -----------------------------
st.markdown("""
<style>
  .stApp { background-color: #000c1a; color: #FFFFFF; }
  .top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }

  /* Cards */
  .card { background-color: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.25); padding: 22px; border-radius: 14px; }
  .small { font-size: 15px; color: rgba(255,255,255,0.78); line-height: 1.5; }
  .highlight { color: #D4AF37; font-weight: 800; }

  /* Pergunta com destaque real (pedido seu) */
  .question-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(212,175,55,0.18);
    border-left: 5px solid #D4AF37;
    padding: 14px 16px;
    border-radius: 12px;
    margin-top: 16px;
    margin-bottom: 8px;
  }
  .question-text { font-size: 20px; color: #FFFFFF; line-height: 1.4; margin: 0; }

  /* Métricas */
  div[data-testid="stMetric"] {
    background-color: rgba(212, 175, 55, 0.05);
    border: 1px solid #D4AF37;
    padding: 15px;
    border-radius: 10px;
  }

  /* Botões (inclui form_submit_button) */
  .stButton>button, div.stFormSubmitButton>button {
    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
    color: #001226 !important;
    width: 100% !important;
    font-weight: 800 !important;
    padding: 14px 16px !important;
    border-radius: 10px !important;
    font-size: 18px !important;
    border: none !important;
  }
  .stButton>button:hover, div.stFormSubmitButton>button:hover {
    filter: brightness(1.05);
  }

  /* Inputs */
  input, textarea {
    background-color: rgba(255,255,255,0.04) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(212,175,55,0.18) !important;
    border-radius: 10px !important;
  }

  /* Texto padrão do app (sem hack global que quebra) */
  .stMarkdown, .stText, .stCaption, label, p { color: #FFFFFF !important; }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# ESTADO
# -----------------------------
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

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Webhook Google Apps Script (o seu)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# -----------------------------
# DIMENSÕES (NOMINALIZAÇÕES + DESCRITIVO + 45 ITENS)
# -----------------------------
dimensoes = [
    ("Clareza & Direção", "Prioridades, foco e decisão do que vem primeiro, mesmo com ruído e pressão.", [
        "Mantenho clareza do que é prioridade, mesmo quando surgem muitas demandas ao mesmo tempo.",
        "Meus objetivos (curto, médio e longo prazo) estão registrados e eu conduzo minhas ações com base neles.",
        "Mesmo cansado ou sob pressão, continuo sabendo o que precisa ser feito primeiro.",
        "Consigo dizer “não” ao que não é prioridade, sem entrar em culpa ou confusão.",
        "Na maior parte do tempo, minhas ações do dia estão alinhadas com a direção que eu quero para minha vida e carreira."
    ]),
    ("Autogestão", "Regular pensamentos, emoções e comportamento sem depender de motivação externa.", [
        "Consigo manter meu comportamento alinhado ao que decidi, mesmo quando meu estado emocional oscila.",
        "Quando fico frustrado ou sobrecarregado, consigo me reorganizar sem perder totalmente o ritmo.",
        "Não dependo de motivação ou estímulo externo para cumprir o que é importante.",
        "Tenho consciência dos meus estados internos ao longo do dia e consigo agir apesar deles quando necessário.",
        "Quando começo a “sair do eixo”, eu retomo o controle com rapidez."
    ]),
    ("Percepção Crítica", "Auto-observação e ajuste de rota sem colapsar ou se punir.", [
        "Aprendo com meus erros e ajusto meu comportamento sem repetir o mesmo padrão por muito tempo.",
        "Quando algo não está funcionando, busco novas formas de fazer em vez de insistir no mesmo caminho.",
        "Consigo identificar rapidamente quando estou me sabotando.",
        "Recebo feedback sem entrar automaticamente em defesa.",
        "Uso erros como fonte de aprendizado, não como motivo de punição ou autocobrança destrutiva."
    ]),
    ("Celebração", "Reconhecer progresso e reforçar energia para sustentar a jornada.", [
        "Reconheço e valorizo pequenos avanços, mesmo quando parecem simples.",
        "Consigo celebrar conquistas sem perder o foco no próximo passo.",
        "Tenho o hábito de reconhecer meu próprio esforço e evolução.",
        "No dia a dia, eu observo mais o que deu certo do que apenas o que faltou.",
        "Celebrar progresso faz parte da minha rotina e me ajuda a sustentar a disciplina no longo prazo."
    ]),
    ("Aprendizado & Repertório", "Capacidade de aprender rápido, modelar e ampliar alternativas práticas.", [
        "Quando percebo uma lacuna em mim, eu busco aprender com rapidez e coloco em prática.",
        "Eu observo pessoas eficientes e extraio comportamentos aplicáveis para a minha realidade.",
        "Eu testo novas abordagens mesmo correndo risco de errar.",
        "Eu ajusto minha forma de pensar e agir quando encontro métodos melhores.",
        "Eu consigo incorporar novas habilidades com consistência quando decido evoluir em algo."
    ]),
    ("Regulação Cognitiva", "Gestão do pensamento em tempo real para não virar ruído, autossabotagem ou paralisia.", [
        "Quando minha mente começa a acelerar, eu consigo reorganizar o pensamento antes de agir no impulso.",
        "Meus pensamentos, na maior parte do tempo, me ajudam a agir em vez de me paralisar ou desmotivar.",
        "Consigo observar e questionar pensamentos negativos/distorcidos em vez de aceitá-los como verdade.",
        "Quando fico ansioso ou tenso, consigo direcionar minha atenção para o que é controlável e útil.",
        "Eu consigo escolher uma interpretação mais funcional quando percebo que estou piorando um cenário na cabeça."
    ]),
    ("Crenças & Autoimagem", "Crenças operantes que sustentam (ou sabotam) decisões e execução.", [
        "Eu acredito que sou capaz de aprender, me adaptar e melhorar continuamente.",
        "Tenho consciência de quando alguma crença está limitando minhas decisões ou ações.",
        "Eu questiono “verdades antigas” para perceber o que já não faz sentido para minha fase atual.",
        "Minha autoimagem me impulsiona para a ação mais do que me trava por medo ou insegurança.",
        "Eu sinto que estou construindo uma vida coerente com os resultados que desejo criar."
    ]),
    ("Autoperformance", "Evolução a partir de si mesmo: padrão de entrega, qualidade e consistência sem viver de comparação.", [
        "Eu acompanho minha evolução com base no meu progresso e não apenas me comparando com outros.",
        "Sou comprometido em entregar meu melhor dentro das condições reais que eu tenho.",
        "Mesmo sob pressão, eu consigo manter um padrão de qualidade nas minhas entregas.",
        "Eu tenho clareza dos meus pontos fortes e do que preciso melhorar, e ajo sobre isso.",
        "Eu busco elevar meu padrão de execução sem depender de picos de humor ou motivação."
    ]),
    ("Autoresponsabilidade", "Postura ativa: assumir parte, agir e corrigir rota sem terceirizar.", [
        "Evito colocar a culpa em fatores externos quando algo não dá certo.",
        "Quando identifico um problema, foco primeiro no que posso fazer (antes do que não controlo).",
        "Costumo agir para mudar situações desconfortáveis em vez de apenas reclamar delas.",
        "Reconheço que sou um dos principais responsáveis diretos pelos meus resultados.",
        "Mesmo quando o cenário é difícil, eu busco uma ação prática para avançar um passo."
    ]),
]

# Labels do radar (curtos e limpos)
radar_labels = [
    "Clareza",
    "Autogestão",
    "Percepção",
    "Celebração",
    "Aprendizado",
    "Regulação",
    "Crenças",
    "Autoperf.",
    "Resp."
]

def simular_processamento():
    msgs = [
        "Processando suas respostas…",
        "Calculando sua Zona de Governança…",
        "Montando seu Radar de Dimensões…",
        "Gerando seu Direcionamento Estratégico…",
        "Finalizando…"
    ]
    placeholder = st.empty()
    with st.spinner("Aguarde…"):
        for m in msgs:
            placeholder.markdown(f"<p class='small'>🔎 {m}</p>", unsafe_allow_html=True)
            time.sleep(2.2)  # ~11s
    placeholder.empty()

def classificar_zona(total):
    # Você pode recalibrar depois (MVP)
    if total > 200:
        return "ELITE"
    elif total > 122:
        return "OSCILAÇÃO"
    else:
        return "SOBREVIVÊNCIA"

def postar_evento(payload: dict):
    """MVP de tracking: manda tudo para o webhook (Apps Script decide onde gravar)."""
    try:
        requests.post(URL_WEBHOOK, json=payload, timeout=10)
    except:
        pass

# -----------------------------
# ETAPA: INTRO
# -----------------------------
if st.session_state.etapa == "intro":
    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Bem-vindo ao Diagnóstico de Governança Pessoal")
        st.markdown("""
<p class='small'>
Isso <span class='highlight'>não é julgamento</span> e não é teste de “certo/errado”.  
É um retrato prático de como sua energia, foco e execução têm funcionado nas últimas semanas.
</p>
<p class='small'>
<b>Tempo:</b> 6 a 9 minutos.  
<b>Como responder:</b> marque de 1 a 5 (1 = raramente / 5 = quase sempre).  
<b>Regra de ouro:</b> responda pelo seu <b>estado real</b>, não pelo ideal.
</p>
<p class='small'>
<b>Privacidade:</b> seus dados são usados apenas para liberar seu resultado e, se você quiser, receber recomendações.
</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
        st.markdown("### O que você vai receber")
        st.markdown("""
<p class='small'>
• Um <b>Radar</b> com suas 9 dimensões  
• Sua <b>Zona de Governança</b> (visão macro do momento)  
• Um <b>direcionamento inicial</b> para subir de nível  
</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### As 9 dimensões (visão rápida)")
        for nome, desc, _ in dimensoes:
            st.markdown(f"**{nome}**<br><span class='small'>{desc}</span>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    if st.button("COMEÇAR AGORA"):
        postar_evento({
            "event": "start",
            "ts": datetime.datetime.utcnow().isoformat(),
            "session_id": st.session_state.session_id
        })
        st.session_state.etapa = "questoes"
        st.rerun()

# -----------------------------
# ETAPA: QUESTÕES
# -----------------------------
elif st.session_state.etapa == "questoes":
    st.markdown("""
<p class='small'>
<b>Como fazer:</b> clique em cada dimensão para abrir as 5 perguntas.  
Responda todas as 45 para liberar o diagnóstico.
</p>
    """, unsafe_allow_html=True)

    q_idx = 0
    respondidas = 0

    for dim_idx, (cat, _, perguntas) in enumerate(dimensoes):
        with st.expander(f"✨ DIMENSÃO {dim_idx+1}: {cat.upper()}"):
            for p in perguntas:
                st.markdown(f"<div class='question-box'><p class='question-text'>{p}</p></div>", unsafe_allow_html=True)
                st.radio(
                    f"R_{q_idx}",
                    [1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    key=f"q_{q_idx}",
                    label_visibility="collapsed"
                )
                if st.session_state.get(f"q_{q_idx}") is not None:
                    respondidas += 1
                q_idx += 1

    st.markdown(f"<p class='small'>Progresso: <span class='highlight'>{respondidas}/45</span> respostas concluídas.</p>", unsafe_allow_html=True)

    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if respondidas == 45:
            # scores por dimensão (5 perguntas cada)
            st.session_state.scores = [sum(st.session_state[f"q_{j}"] for j in range(i, i+5)) for i in range(0, 45, 5)]
            st.session_state.total = sum(st.session_state.scores)
            st.session_state.etapa = "captura"
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")

# -----------------------------
# ETAPA: CAPTURA
# -----------------------------
elif st.session_state.etapa == "captura":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO!</h3>", unsafe_allow_html=True)
        st.markdown("<p class='small' style='text-align:center;'>Preencha seus dados para liberar seu Radar e sua Zona.</p>", unsafe_allow_html=True)

        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            empresa = st.text_input("Empresa")
            cargo = st.text_input("Cargo")

            submit = st.form_submit_button("LIBERAR MEU LAUDO AGORA")

        if submit:
            if all([nome, email, whatsapp, empresa, cargo]):
                t = st.session_state.total
                z = classificar_zona(t)
                st.session_state.zona = z
                st.session_state.nome_usuario = nome

                # Respostas e scores (para laudo pago e automação)
                answers = [st.session_state.get(f"q_{i}") for i in range(45)]
                dim_scores = {
                    dimensoes[i][0]: st.session_state.scores[i] for i in range(9)
                }

                # Simula processamento (robustez percebida)
                simular_processamento()

                postar_evento({
                    "event": "lead_submit",
                    "ts": datetime.datetime.utcnow().isoformat(),
                    "session_id": st.session_state.session_id,
                    "nome": nome,
                    "email": email,
                    "whatsapp": whatsapp,
                    "empresa": empresa,
                    "cargo": cargo,
                    "total": t,
                    "zona": z,
                    "scores": st.session_state.scores,
                    "dim_scores": dim_scores,
                    "answers": answers
                })

                st.session_state.etapa = "resultado"
                st.rerun()
            else:
                st.warning("Por favor, preencha todos os campos.")

# -----------------------------
# ETAPA: RESULTADO
# -----------------------------
elif st.session_state.etapa == "resultado":
    st.markdown(
        f"### Análise Individual: <span class='highlight'>{st.session_state.nome_usuario.upper()}</span>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    with c2:
        st.metric("Zona de Governança", st.session_state.zona)

    st.write("---")

    col_l, col_r = st.columns([1.2, 0.8])

    with col_l:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=st.session_state.scores,
            theta=radar_labels,
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
        st.markdown("### 🔍 Direcionamento Estratégico")

        if st.session_state.zona == "ELITE":
            st.markdown(f"""
<p class='small'>
<span class='highlight'>{st.session_state.nome_usuario}</span>, seus resultados indicam <b>Governança de Elite</b>.
O foco agora é <b>blindar constância</b> e evitar a cegueira da eficiência.
Quem está bem não pode relaxar na base.
</p>
            """, unsafe_allow_html=True)
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown(f"""
<p class='small'>
<span class='highlight'>{st.session_state.nome_usuario}</span>, você está em <b>Oscilação</b>.
Normalmente isso é combinação de <b>ritmo operacional</b> + <b>regulação cognitiva</b>.
A meta aqui é estabilizar execução e reduzir dependência de estímulo emocional.
</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
<p class='small'>
<span class='highlight'>{st.session_state.nome_usuario}</span>, você está em <b>Modo de Sobrevivência</b>.
Isso sugere colapso de governança (agenda, energia e disciplina).
A intervenção precisa ser simples e vital: <b>não é fazer mais, é fazer o certo, com método.</b>
</p>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("### O que você recebe no Laudo Completo (IA)")
        st.markdown("""
<p class='small'>
• Leitura aprofundada das 9 dimensões (forças, riscos e travas)  
• Interpretação objetiva da sua Zona + prováveis causas  
• Plano de ação prático (7 dias + 30 dias) com foco em execução  
• Priorização: <b>o que atacar primeiro</b> para subir de nível  
</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Próximo Passo Estratégico</h3>", unsafe_allow_html=True)
    st.markdown("<p class='small' style='text-align:center;'>Se você quiser profundidade e um plano estruturado, aqui é o próximo passo.</p>", unsafe_allow_html=True)

    # Checkout
    checkout_url = "https://pay.hotmart.com/SEU_LINK"
    st.markdown(f"""
<div style='text-align: center; margin-bottom: 18px;'>
  <a href='{checkout_url}' target='_blank' style='text-decoration: none;'>
    <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
                color: #001226; padding: 18px 35px; font-weight: 900;
                border-radius: 10px; display: inline-block; width: 100%;
                max-width: 640px; font-size: 20px;'>
      ADQUIRIR MEU LAUDO COMPLETO COM IA →
    </div>
  </a>
</div>
    """, unsafe_allow_html=True)

    # WhatsApp
    wa_url = "https://wa.me/5581982602018?text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM%20e%20quero%20conhecer%20as%20soluções."
    st.markdown(f"""
<div style='text-align:left; margin-bottom: 10px;'>
  <a href='{wa_url}' target='_blank' style='text-decoration: none;'>
    <div style='background: rgba(212, 175, 55, 0.1);
                color: #D4AF37; border: 1px solid #D4AF37;
                padding: 12px 20px; font-weight: 800;
                border-radius: 8px; display: inline-block;'>
      FALE COM NOSSA EQUIPE
    </div>
  </a>
</div>
    """, unsafe_allow_html=True)

    # Refazer (discreto, mas útil)
    st.markdown("<p class='small'>Se quiser refazer com mais calma:</p>", unsafe_allow_html=True)
    if st.button("Refazer diagnóstico"):
        for i in range(45):
            if f"q_{i}" in st.session_state:
                st.session_state[f"q_{i}"] = None
        st.session_state.total = 0
        st.session_state.scores = [0] * 9
        st.session_state.zona = ""
        st.session_state.nome_usuario = ""
        st.session_state.etapa = "intro"
        st.rerun()
