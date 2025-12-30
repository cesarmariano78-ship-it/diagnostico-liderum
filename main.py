
import streamlit as st
import plotly.graph_objects as go
import requests
import time  # <- novo (para simular processamento com mensagens)

# 1. IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    .top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }
    div[data-testid="stMetric"] { background-color: rgba(212, 175, 55, 0.05); border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; }
    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
    .stButton>button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; border-radius: 8px; font-size: 18px !important;
    }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 10px; }
    .laudo-container { background-color: rgba(255, 255, 255, 0.03); padding: 35px; border-radius: 15px; border-left: 6px solid #D4AF37; margin-top: 25px; line-height: 1.7; }
    .highlight { color: #D4AF37 !important; font-weight: bold; }
    .card { background-color: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.25); padding: 22px; border-radius: 14px; }
    .small { font-size: 15px !important; color: rgba(255,255,255,0.75) !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# ESTADO
# -----------------------------
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'intro'   # <- novo: tela de recepção
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'scores' not in st.session_state:
    st.session_state.scores = [0] * 9
if 'zona' not in st.session_state:
    st.session_state.zona = ""
if 'nome_usuario' not in st.session_state:
    st.session_state.nome_usuario = ""

URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# -----------------------------
# DADOS
# -----------------------------
questoes_lista = [
    ("Visão e Alinhamento Estratégico", ["Eu tenho clareza sobre meus objetivos nos próximos meses.", "Meus objetivos pessoais e profissionais estão anotados.", "Mantenho meu foco mesmo com distrações externas.", "Revisito minha visão de futuro com frequência.", "Organizo minhas prioridades pelo que é importante."]),
    ("Recompensa e Reforço Positivo", ["Reconheço minhas próprias conquistas.", "Comemoro quando concluo uma etapa.", "Me elogio por atitudes positivas.", "Sinto orgulho do meu progresso.", "Crio momentos para celebrar avanços."]),
    ("Análise e Consciência de Padrões", ["Reviso meu comportamento criticamente.", "Reconheço erros e busco aprender.", "Percebo meus padrões de sabotagem.", "Ajusto rotas sem culpa quando erro.", "Busco feedbacks com abertura."]),
    ("Governança e Disciplina Operacional", ["Planejo minha rotina de forma organizada.", "Priorizo o importante antes do urgente.", "Mantenho constância sem motivação.", "Equilibro tarefas operacionais e estratégicas.", "Tenho hábitos que sustentam minha produtividade."]),
    ("Modelagem e Expansão de Repertório", ["Tenho consciência de comportamentos a mudar.", "Busco aprender com quem admiro.", "Replico métodos que funcionam para outros.", "Observo e mudo pensamentos limitantes.", "Incorporo novas habilidades com rapidez."]),
    ("Gestão da Narrativa e Mindset", ["Minha voz interna me incentiva.", "Percebo e ressignifico pensamentos punitivos.", "Converso comigo com respeito e firmeza.", "Silencio pensamentos sabotadores.", "Meu diálogo interno ajuda minhas ações."]),
    ("Arquitetura de Sistemas de Crenças", ["Acredito que sou capaz de aprender e evoluir sempre.", "Percebo quando ajo por crenças limitantes.", "Mudo minha realidade mudando crenças.", "Tenho crenças fortes sobre minha liderança.", "Identifico a origem das minhas crenças."]),
    ("Padrão de Entrega e Excelência", ["Me esforço para entregar o máximo.", "Percebo evolução na qualidade das entregas.", "Mantenho comprometimento sob pressão.", "Tenho clareza de pontos fortes e de melhoria.", "Entrego além do básico sempre."]),
    ("Postura Ativa e Protagonismo", ["Assumo responsabilidade pelas escolhas.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que controlo.", "Encaro desafios como oportunidades.", "Olho para mim antes de culpar o ambiente."])
]

dimensoes_resumo = [
    ("Visão & Alinhamento", "Clareza de objetivos, prioridades e direção."),
    ("Recompensa", "Reforço positivo, motivação e sustentação emocional."),
    ("Consciência de Padrões", "Autopercepção, ajustes e aprendizado sem culpa."),
    ("Disciplina Operacional", "Rotina, execução e constância no que importa."),
    ("Modelagem", "Aprender com referências e expandir repertório."),
    ("Narrativa Interna", "Diálogo interno, autocontrole e mentalidade."),
    ("Crenças", "Crenças limitantes vs. crenças fortalecedoras."),
    ("Excelência", "Padrão de entrega, qualidade e consistência sob pressão."),
    ("Protagonismo", "Responsabilidade, ação e postura ativa.")
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
            time.sleep(2.2)  # ~11s total
    placeholder.empty()

# -----------------------------
# ETAPA 0: INTRO (novo)
# -----------------------------
if st.session_state.etapa == 'intro':
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Bem-vindo ao seu Diagnóstico de Governança Pessoal")
        st.markdown("""
        **O que é:** um protocolo rápido para mapear como você está dirigindo sua energia, foco e disciplina nas últimas semanas.  
        **Tempo:** 6 a 9 minutos.  
        **Como responder:** marque de **1 a 5** (sendo 1 = raramente / 5 = quase sempre).  
        **Importante:** responda no seu estado real, não no ideal.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
        st.markdown("### O que você vai receber")
        st.markdown("""
        - Um **Radar** com suas 9 dimensões
        - Sua **Zona de Governança** (visão macro do momento)
        - Um **direcionamento inicial** para subir de nível
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### As 9 dimensões (visão rápida)")
        for nome, desc in dimensoes_resumo:
            st.markdown(f"**{nome}:** <span class='small'>{desc}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    if st.button("COMEÇAR AGORA"):
        st.session_state.etapa = 'questoes'
        st.rerun()

# -----------------------------
# ETAPA 1: QUESTÕES
# -----------------------------
elif st.session_state.etapa == 'questoes':
    st.markdown("<p class='small'>Instrução: clique em cada dimensão para abrir as perguntas. Responda todas as 45 para liberar o diagnóstico.</p>", unsafe_allow_html=True)

    q_idx = 0
    respondidas = 0

    for cat, perguntas in questoes_lista:
        with st.expander(f"✨ DIMENSÃO: {cat.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
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
            st.session_state.scores = [sum(st.session_state[f"q_{j}"] for j in range(i, i+5)) for i in range(0, 45, 5)]
            st.session_state.total = sum(st.session_state.scores)
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões para liberar o laudo.")

# -----------------------------
# ETAPA 2: CAPTURA
# -----------------------------
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO!</h3>", unsafe_allow_html=True)
        st.markdown("<p class='small' style='text-align:center;'>Preencha seus dados para liberar seu Radar e sua Zona.</p>", unsafe_allow_html=True)

        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa / Cargo")

            if st.form_submit_button("LIBERAR MEU LAUDO AGORA"):
                if all([nome, email, whatsapp, cargo]):
                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona = z
                    st.session_state.nome_usuario = nome

                    payload = {"nome": nome, "email": email, "whatsapp": whatsapp, "cargo": cargo, "pontos": t, "zona": z}

                    # SIMULA PROCESSAMENTO (robustez percebida)
                    simular_processamento()

                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                    except:
                        pass

                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Por favor, preencha todos os campos.")

# -----------------------------
# ETAPA 3: LAUDO
# -----------------------------
elif st.session_state.etapa == 'resultado':
    st.markdown(f"### Análise Individual: <span class='highlight'>{st.session_state.nome_usuario.upper()}</span>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Pontuação Total", f"{st.session_state.total} / 225")
    with c2:
        st.metric("Zona de Governança", st.session_state.zona)

    st.write("---")

    col_l, col_r = st.columns([1.2, 0.8])

    with col_l:
        categories = ['Visão', 'Recompensa', 'Análise', 'Governança', 'Modelagem', 'Narrativa', 'Crenças', 'Excelência', 'Postura']
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
            margin=dict(l=100, r=100, t=20, b=20),
            font=dict(color="white", size=16)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Direcionamento Estratégico")

        if st.session_state.zona == "ELITE":
            st.markdown(f"""<span class='highlight'>{st.session_state.nome_usuario}</span>, seus resultados indicam uma **Governança de Elite**.
            O foco agora é **blindar constância** e evitar a cegueira da eficiência. Autoliderança é processo vivo: quem está no topo não pode relaxar na base.""", unsafe_allow_html=True)
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown(f"""<span class='highlight'>{st.session_state.nome_usuario}</span>, você está na zona de **Oscilação**.
            Sua performance alterna entre picos e quedas. O ponto crítico costuma ser **ritmo operacional + narrativa interna**. O objetivo aqui é estabilizar execução e reduzir dependência de estímulo emocional.""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<span class='highlight'>{st.session_state.nome_usuario}</span>, você está em **Modo de Sobrevivência**.
            Isso sugere colapso de governança (agenda, energia e disciplina). A intervenção precisa ser simples, imediata e vital: **não é fazer mais, é fazer o certo, com método.**""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
        st.markdown("### O que você recebe no Laudo Completo (IA)")
        st.markdown("""
        - Leitura aprofundada das 9 dimensões (forças, riscos e travas)
        - Interpretação objetiva da sua Zona + o que está causando isso
        - Plano de ação prático (7 dias + 30 dias) com foco em execução
        - Priorização: **o que atacar primeiro** para subir de nível
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Próximo Passo Estratégico</h3>", unsafe_allow_html=True)
    st.write("Este laudo mostra seu cenário atual. Para subir de nível, você precisa de profundidade e execução guiada.")

    # BOTÃO DE CHECKOUT CENTRALIZADO
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 25px;'>
            <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001226; padding: 20px 45px; font-weight: bold; border-radius: 8px; display: inline-block; width: 100%; max-width: 600px; font-size: 20px;'>
                    ADQUIRIR MEU LAUDO ESTRATÉGICO COMPLETO COM IA →
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # BOTÃO FALE COM NOSSA EQUIPE
    wa_url = "https://wa.me/5581982602018?text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM%20e%20quero%20conhecer%20as%20soluções."
    st.markdown(f"""
        <div style='text-align: left; margin-bottom: 12px;'>
            <a href='{wa_url}' target='_blank' style='text-decoration: none;'>
                <div style='background: rgba(212, 175, 55, 0.1); color: #D4AF37; border: 1px solid #D4AF37; padding: 12px 25px; font-weight: bold; border-radius: 5px; display: inline-block;'>
                    💬 FALE COM NOSSA EQUIPE
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # REFAZER (discreto)
    st.markdown("<p class='small'>Se quiser refazer o protocolo com mais calma:</p>", unsafe_allow_html=True)
    if st.button("Refazer diagnóstico"):
        # Limpa respostas
        for i in range(45):
            if f"q_{i}" in st.session_state:
                st.session_state[f"q_{i}"] = None
        st.session_state.total = 0
        st.session_state.scores = [0]*9
        st.session_state.zona = ""
        st.session_state.nome_usuario = ""
        st.session_state.etapa = 'intro'
        st.rerun()
