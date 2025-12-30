import streamlit as st
import plotly.graph_objects as go
import requests
import re

# =========================================================
# 1) CONFIG + IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
# =========================================================
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #000c1a; color: #FFFFFF; }

.top-banner {
    background-color: #000c1a;
    height: 16px;
    width: 100%;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    margin-bottom: 18px;
}

div[data-testid="stMetric"] {
    background-color: rgba(212, 175, 55, 0.05);
    border: 1px solid rgba(212, 175, 55, 0.55);
    padding: 15px;
    border-radius: 10px;
}

label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }

.stButton>button {
    background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
    color: #001226 !important;
    width: 100%;
    font-weight: 800;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px !important;
    border: 0 !important;
}

.small-btn .stButton>button {
    padding: 10px !important;
    font-size: 16px !important;
}

.question-text {
    font-size: 18px !important;
    color: #FFFFFF !important;
    margin-top: 16px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.12);
    padding-bottom: 10px;
}

.card {
    background-color: rgba(255, 255, 255, 0.03);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid rgba(212, 175, 55, 0.18);
}

.laudo-container {
    background-color: rgba(255, 255, 255, 0.03);
    padding: 28px;
    border-radius: 15px;
    border-left: 6px solid #D4AF37;
    margin-top: 12px;
    line-height: 1.7;
}

.highlight { color: #D4AF37 !important; font-weight: 800; }
.muted { color: rgba(255,255,255,0.78) !important; font-size: 16px !important; }
hr { border: none; border-top: 1px solid rgba(212,175,55,0.12); margin: 18px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2) STATE
# =========================================================
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"   # NOVO: começa na página de boas-vindas

if "total" not in st.session_state:
    st.session_state.total = 0

if "scores" not in st.session_state:
    st.session_state.scores = [0] * 9

if "zona" not in st.session_state:
    st.session_state.zona = ""

if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""

# URL webhook (Google Apps Script)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# =========================================================
# 3) PERGUNTAS (45) — 9 dimensões x 5
# =========================================================
questoes_lista = [
    ("Visão e Alinhamento Estratégico", [
        "Eu tenho clareza sobre meus objetivos nos próximos meses.",
        "Meus objetivos pessoais e profissionais estão anotados.",
        "Mantenho meu foco mesmo com distrações externas.",
        "Revisito minha visão de futuro com frequência.",
        "Organizo minhas prioridades pelo que é importante."
    ]),
    ("Recompensa e Reforço Positivo", [
        "Reconheço minhas próprias conquistas.",
        "Comemoro quando concluo uma etapa.",
        "Me elogio por atitudes positivas.",
        "Sinto orgulho do meu progresso.",
        "Crio momentos para celebrar avanços."
    ]),
    ("Análise e Consciência de Padrões", [
        "Reviso meu comportamento criticamente.",
        "Reconheço erros e busco aprender.",
        "Percebo meus padrões de sabotagem.",
        "Ajusto rotas sem culpa quando erro.",
        "Busco feedbacks com abertura."
    ]),
    ("Governança e Disciplina Operacional", [
        "Planejo minha rotina de forma organizada.",
        "Priorizo o importante antes do urgente.",
        "Mantenho constância sem motivação.",
        "Equilibro tarefas operacionais e estratégicas.",
        "Tenho hábitos que sustentam minha produtividade."
    ]),
    ("Modelagem e Expansão de Repertório", [
        "Tenho consciência de comportamentos a mudar.",
        "Busco aprender com quem admiro.",
        "Replico métodos que funcionam para outros.",
        "Observo e mudo pensamentos limitantes.",
        "Incorporo novas habilidades com rapidez."
    ]),
    ("Gestão da Narrativa e Mindset", [
        "Minha voz interna me incentiva.",
        "Percebo e ressignifico pensamentos punitivos.",
        "Converso comigo com respeito e firmeza.",
        "Silencio pensamentos sabotadores.",
        "Meu diálogo interno ajuda minhas ações."
    ]),
    ("Arquitetura de Sistemas de Crenças", [
        "Acredito que sou capaz de aprender e evoluir sempre.",
        "Percebo quando ajo por crenças limitantes.",
        "Mudo minha realidade mudando crenças.",
        "Tenho crenças fortes sobre minha liderança.",
        "Identifico a origem das minhas crenças."
    ]),
    ("Padrão de Entrega e Excelência", [
        "Me esforço para entregar o máximo.",
        "Percebo evolução na qualidade das entregas.",
        "Mantenho comprometimento sob pressão.",
        "Tenho clareza de pontos fortes e de melhoria.",
        "Entrego além do básico sempre."
    ]),
    ("Postura Ativa e Protagonismo", [
        "Assumo responsabilidade pelas escolhas.",
        "Evito colocar culpa em fatores externos.",
        "Ajo com rapidez para mudar o que controlo.",
        "Encaro desafios como oportunidades.",
        "Olho para mim antes de culpar o ambiente."
    ])
]

# =========================================================
# 4) HELPERS
# =========================================================
def contar_respondidas():
    answered = 0
    for i in range(45):
        if st.session_state.get(f"q_{i}") is not None:
            answered += 1
    return answered

def normalizar_whatsapp(w):
    if not w:
        return ""
    digits = re.sub(r"\D", "", w)
    return digits

def email_valido(e):
    if not e:
        return False
    return "@" in e and "." in e

# =========================================================
# ETAPA 0: BOAS-VINDAS (NOVO)
# =========================================================
if st.session_state.etapa == "inicio":
    c1, c2 = st.columns([1.25, 0.75])
    with c1:
        st.markdown("""
        <div class="card">
            <h2 style="margin-top: 0;">Bem-vindo ao Diagnóstico de Governança Pessoal</h2>
            <p class="muted">
                Este diagnóstico mede seu nível atual de governança em 9 dimensões práticas.
                Ao final, você recebe sua pontuação, sua zona e um direcionamento inicial.
            </p>
            <hr/>
            <p><span class="highlight">Como funciona:</span></p>
            <ul>
                <li>São <b>45 perguntas</b> (9 dimensões × 5 perguntas).</li>
                <li>Escala <b>1 a 5</b> (1 = discordo totalmente / 5 = concordo totalmente).</li>
                <li>Leva em média <b>6–10 minutos</b>.</li>
            </ul>
            <p class="muted">
                Responda com honestidade — isso não é “teste de certo/errado”. É um mapa do seu momento.
            </p>
            <hr/>
            <p class="muted">
                <b>Privacidade:</b> seus dados são usados para liberar o laudo e orientar soluções. Sem spam.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3 style="margin-top: 0;">Antes de começar</h3>
            <p class="muted">
                Para evitar confusão: você vai clicar em cada dimensão e responder 5 perguntas.
                No final, você clica em <b>PROCESSAR MEU DIAGNÓSTICO</b>.
            </p>
            <hr/>
        </div>
        """, unsafe_allow_html=True)

        if st.button("COMEÇAR DIAGNÓSTICO"):
            st.session_state.etapa = "questoes"
            st.rerun()

# =========================================================
# ETAPA 1: QUESTÕES
# =========================================================
elif st.session_state.etapa == "questoes":
    answered = contar_respondidas()
    progresso = answered / 45

    # Header de instrução + progresso
    st.markdown("""
    <div class="card">
        <h3 style="margin-top: 0;">Instruções rápidas</h3>
        <p class="muted" style="margin-bottom: 0;">
            Passo 1) Abra cada dimensão abaixo e responda as 5 perguntas (escala 1–5).<br/>
            Passo 2) Quando completar 45/45, clique em <b>PROCESSAR MEU DIAGNÓSTICO</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    colp1, colp2, colp3 = st.columns([1.2, 1.0, 0.8])
    with colp1:
        st.progress(progresso)
    with colp2:
        st.metric("Respondidas", f"{answered} / 45")
    with colp3:
        faltam = 45 - answered
        st.metric("Faltam", str(faltam))

    st.write("")

    # Render das perguntas (mantendo sua estrutura, mas com clareza em cima)
    q_idx = 0
    for cat, perguntas in questoes_lista:
        with st.expander(f"✨ DIMENSÃO: {cat.upper()}", expanded=False):
            st.markdown(f"<p class='muted'>Responda as 5 perguntas desta dimensão.</p>", unsafe_allow_html=True)
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
                q_idx += 1

    st.write("")

    # Botão processar (só habilita quando completo)
    pode_processar = (answered == 45)
    if st.button("PROCESSAR MEU DIAGNÓSTICO", disabled=not pode_processar):
        st.session_state.scores = [
            sum(st.session_state[f"q_{j}"] for j in range(i, i + 5))
            for i in range(0, 45, 5)
        ]
        st.session_state.total = sum(st.session_state.scores)
        st.session_state.etapa = "captura"
        st.rerun()

    if not pode_processar and answered > 0:
        st.warning("⚠️ Você precisa responder todas as 45 questões para liberar o diagnóstico.")

# =========================================================
# ETAPA 2: CAPTURA (LEADS)
# =========================================================
elif st.session_state.etapa == "captura":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO!</h3>", unsafe_allow_html=True)
        st.markdown("<p class='muted' style='text-align:center;'>Preencha abaixo para liberar seu laudo.</p>", unsafe_allow_html=True)

        with st.form("lead_form", clear_on_submit=False):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa / Cargo")

            submitted = st.form_submit_button("LIBERAR MEU LAUDO AGORA")

            if submitted:
                wpp_norm = normalizar_whatsapp(whatsapp)

                if not all([nome, email, whatsapp, cargo]):
                    st.warning("Por favor, preencha todos os campos.")
                elif not email_valido(email):
                    st.warning("Digite um e-mail válido.")
                elif len(wpp_norm) < 10:
                    st.warning("Digite um WhatsApp válido (com DDD).")
                else:
                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona, st.session_state.nome_usuario = z, nome

                    payload = {
                        "nome": nome,
                        "email": email,
                        "whatsapp": wpp_norm,
                        "cargo": cargo,
                        "pontos": t,
                        "zona": z
                    }

                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                    except:
                        pass

                    st.session_state.etapa = "resultado"
                    st.rerun()

# =========================================================
# ETAPA 3: LAUDO
# =========================================================
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

    # Radar
    with col_l:
        categories = ["Visão", "Recompensa", "Análise", "Governança", "Modelagem", "Narrativa", "Crenças", "Excelência", "Postura"]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=st.session_state.scores,
            theta=categories,
            fill="toself",
            fillcolor="rgba(212, 175, 55, 0.35)",
            line=dict(color="#D4AF37", width=4)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,12,26,1)",
                radialaxis=dict(visible=True, range=[0, 25], color="#888", gridcolor="rgba(212,175,55,0.1)")
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            height=560,
            margin=dict(l=90, r=90, t=20, b=20),
            font=dict(color="white", size=16)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Copy do direcionamento (mantive sua base, só deixando mais “pé no chão”)
    with col_r:
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Direcionamento Estratégico")

        nome = st.session_state.nome_usuario
        if st.session_state.zona == "ELITE":
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, seus resultados indicam uma <b>Governança de Elite</b>.
            O foco agora é <b>blindar constância</b> e evitar a armadilha da eficiência sem direção.
            Autoliderança é processo vivo: ajuste fino + consistência.
            <br/><br/>
            Se quiser, você pode acessar o <b>Laudo Completo</b> (mais profundo) com plano de ação estruturado.
            """, unsafe_allow_html=True)
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, você está na zona de <b>Oscilação</b>.
            Seu padrão alterna entre picos e quedas — normalmente por dependência de estímulo externo,
            energia emocional ou falta de sistema mínimo.
            <br/><br/>
            O próximo passo é estabilizar o operacional e cortar ruído interno (narrativa sabotadora).
            Se quiser, acesse o <b>Laudo Completo</b> com plano de execução.
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <span class='highlight'>{nome}</span>, você está em <b>Modo de Sobrevivência</b>.
            Isso costuma aparecer como: agenda fora de controle, baixa energia, excesso de urgência e pouca direção.
            <br/><br/>
            Aqui a prioridade é <b>intervenção simples e imediata</b>: reduzir sangramentos e recuperar governança mínima.
            Se quiser, acesse o <b>Laudo Completo</b> com um plano de ação estruturado para os próximos 7–30 dias.
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Próximo Passo Estratégico</h3>", unsafe_allow_html=True)
    st.write("Este laudo aponta sua zona atual. Para avançar com método e execução, você precisa de profundidade e plano.")

    # BOTÃO DE CHECKOUT (trocar link)
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 22px;'>
            <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
                            color: #001226; padding: 18px 40px; font-weight: 900; border-radius: 10px;
                            display: inline-block; width: 100%; max-width: 640px; font-size: 20px;'>
                    ADQUIRIR LAUDO COMPLETO →
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # BOTÃO WHATSAPP (ajustar número/texto)
    wa_url = "https://wa.me/5581982602018?text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM%20e%20quero%20conhecer%20as%20soluções."
    st.markdown(f"""
        <div style='text-align: left;'>
            <a href='{wa_url}' target='_blank' style='text-decoration: none;'>
                <div style='background: rgba(212, 175, 55, 0.1);
                            color: #D4AF37; border: 1px solid #D4AF37;
                            padding: 12px 22px; font-weight: 900; border-radius: 8px; display: inline-block;'>
                    FALE COM NOSSA EQUIPE
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='small-btn'>", unsafe_allow_html=True)
    if st.button("REFAZER DIAGNÓSTICO"):
        # Limpa respostas
        for i in range(45):
            if f"q_{i}" in st.session_state:
                st.session_state[f"q_{i}"] = None
        st.session_state.total = 0
        st.session_state.scores = [0] * 9
        st.session_state.zona = ""
        st.session_state.nome_usuario = ""
        st.session_state.etapa = "inicio"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

