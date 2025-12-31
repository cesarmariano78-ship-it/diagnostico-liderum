import streamlit as st
import plotly.graph_objects as go
import requests
import time

# 1. IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    .top-banner { background-color: #000c1a; height: 50px; width: 100%; border-bottom: 1px solid rgba(212, 175, 55, 0.2); margin-bottom: 20px; }
    div[data-testid="stMetric"] { background-color: rgba(212, 175, 55, 0.05); border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; }
    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

    /* Botões (inclui submit de form) */
    .stButton>button, button[kind="primary"] {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important;
        width: 100%;
        font-weight: bold;
        padding: 15px;
        border-radius: 8px;
        font-size: 18px !important;
        border: none !important;
    }

    /* Perguntas */
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 10px; }

    /* Blocos */
    .laudo-container { background-color: rgba(255, 255, 255, 0.03); padding: 35px; border-radius: 15px; border-left: 6px solid #D4AF37; margin-top: 25px; line-height: 1.7; }
    .highlight { color: #D4AF37 !important; font-weight: bold; }
    .card { background-color: rgba(255,255,255,0.03); border: 1px solid rgba(212,175,55,0.25); padding: 22px; border-radius: 14px; }
    .small { font-size: 15px !important; color: rgba(255,255,255,0.75) !important; }

    /* Inputs: corrigir texto branco em campo branco (ilegível) */
    div[data-baseweb="input"] input {
        background-color: #FFFFFF !important;
        color: #001226 !important;
    }
    div[data-baseweb="textarea"] textarea {
        background-color: #FFFFFF !important;
        color: #001226 !important;
    }
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: rgba(0,18,38,0.55) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# ESTADO
# -----------------------------
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'intro'
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
# DADOS (MANTIDOS)
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
# ETAPA 0: INTRO (ATUALIZADA)
# -----------------------------
if st.session_state.etapa == 'intro':
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Bem-vindo ao Protocolo LIDERUM")
    st.markdown("""
Este diagnóstico não é um teste, nem um julgamento sobre quem você é.  
Ele foi criado para ajudar você a observar com mais clareza como está hoje sua forma de conduzir decisões, emoções, comportamento e direção.

Não existem respostas certas ou erradas. O valor deste processo está na honestidade das suas respostas, não na pontuação final.  
Quanto mais **sincero** você for, mais preciso será o seu resultado.
""")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("### Como responder às perguntas")
    st.markdown("""
- Use a escala de 1 a 5 considerando como você age na maior parte do tempo, e não em dias excepcionais.  
- Evite responder pelo que você gostaria de ser. Responda pelo que você realmente faz.  
- Se ficar em dúvida entre duas notas, escolha a menor.

Este diagnóstico mede consistência, não intenção.
""")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("### Privacidade e sigilo")
    st.markdown("""
Suas respostas são confidenciais e utilizadas exclusivamente para gerar seu diagnóstico e direcionamento personalizado.  
Nenhuma informação será compartilhada ou utilizada fora desse contexto.
""")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    if st.button("INICIAR MEU DIAGNÓSTICO"):
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
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            empresa = st.text_input("Empresa")
            cargo = st.text_input("Cargo")

            if st.form_submit_button("LIBERAR MEU LAUDO AGORA"):
                if all([nome, email, whatsapp, empresa, cargo]):
                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona = z
                    st.session_state.nome_usuario = nome

                    payload = {
                        "nome": nome,
                        "email": email,
                        "whatsapp": whatsapp,
                        "empresa": empresa,
                        "cargo": cargo,
                        "pontos": t,
                        "zona": z
                    }

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
            O foco agora é **blindar constância** e evitar a cegueira da eficiência. Quem está no topo não pode relaxar na base.""", unsafe_allow_html=True)
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown(f"""<span class='highlight'>{st.session_state.nome_usuario}</span>, você está na zona de **Oscilação**.
            Sua performance alterna entre picos e quedas. O ponto crítico costuma ser **ritmo operacional + narrativa interna**. Aqui, o objetivo é estabilizar execução e reduzir dependência emocional.""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<span class='highlight'>{st.session_state.nome_usuario}</span>, você está em **Modo de Sobrevivência**.
            Isso sugere colapso de governança (agenda, energia e disciplina). A intervenção precisa ser simples e vital: **não é fazer mais, é fazer o certo, com método.**""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' style='margin-top:14px;'>", unsafe_allow_html=True)
        st.markdown("### O que você recebe no Laudo Completo (IA)")
        st.markdown("""
- Leitura aprofundada das 9 dimensões (forças, riscos e travas)  
- Interpretação objetiva da sua zona (o que está causando isso)  
- Plano de ação prático (7 dias + 30 dias) com foco em execução  
- Priorização: o que atacar primeiro para subir de nível  
""")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Próximo Passo</h3>", unsafe_allow_html=True)
    st.write("Se você quer o plano completo (com ações), acesse abaixo.")

    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 25px;'>
            <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001226; padding: 20px 45px; font-weight: bold; border-radius: 8px; display: inline-block; width: 100%; max-width: 600px; font-size: 20px;'>
                    ADQUIRIR MEU LAUDO COMPLETO (R$47)
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)
