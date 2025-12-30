import streamlit as st
import plotly.graph_objects as go
import requests
import time
import random

# =========================================================
# 1) IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
# =========================================================
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
.question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 14px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 8px; }
.laudo-container { background-color: rgba(255, 255, 255, 0.03); padding: 35px; border-radius: 15px; border-left: 6px solid #D4AF37; margin-top: 25px; line-height: 1.7; }
.highlight { color: #D4AF37 !important; font-weight: bold; }

.box {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(212,175,55,0.25);
  border-radius: 12px;
  padding: 16px 18px;
  margin: 12px 0 18px 0;
}
.small { font-size: 15px !important; color: rgba(255,255,255,0.8) !important; }
.hr { border-bottom: 1px solid rgba(212,175,55,0.12); margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2) STATE
# =========================================================
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'intro'  # NOVO: começa em boas-vindas

if 'total' not in st.session_state:
    st.session_state.total = 0

if 'scores' not in st.session_state:
    st.session_state.scores = [0] * 9

if 'zona' not in st.session_state:
    st.session_state.zona = ""

if 'nome_usuario' not in st.session_state:
    st.session_state.nome_usuario = ""

# URL WEBHOOK (mantido)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# =========================================================
# 3) CONTEÚDO: 45 perguntas (9 dimensões x 5)
# =========================================================
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

dim_resumo = {
    "Visão e Alinhamento Estratégico": "Clareza de direção, prioridades e foco no que importa.",
    "Recompensa e Reforço Positivo": "Capacidade de reforçar progresso e sustentar motivação interna.",
    "Análise e Consciência de Padrões": "Autoanálise, aprendizado com erros e percepção de sabotagens.",
    "Governança e Disciplina Operacional": "Rotina, execução consistente e gestão do urgente x importante.",
    "Modelagem e Expansão de Repertório": "Aprender rápido, modelar referências e ampliar habilidades.",
    "Gestão da Narrativa e Mindset": "Diálogo interno, ressignificação e firmeza emocional.",
    "Arquitetura de Sistemas de Crenças": "Crenças que sustentam (ou travam) evolução e liderança.",
    "Padrão de Entrega e Excelência": "Qualidade, consistência sob pressão e padrão acima do básico.",
    "Postura Ativa e Protagonismo": "Responsabilidade, ação e controle do que depende de você."
}

# =========================================================
# 4) ETAPA 0: INTRO (NOVA)
# =========================================================
if st.session_state.etapa == 'intro':
    st.markdown("""
    <div class="box">
      <div><span class="highlight">O que é:</span> um diagnóstico rápido de Governança Pessoal (9 dimensões).</div>
      <div class="small">Tempo estimado: 6 a 10 minutos. Você responde 45 itens (1 a 5) e recebe seu mapa no final.</div>
      <div class="hr"></div>
      <div><span class="highlight">Como funciona:</span></div>
      <div class="small">1) Responda todas as perguntas com sinceridade.</div>
      <div class="small">2) Informe seus dados para liberar o resultado.</div>
      <div class="small">3) Você recebe pontuação total, zona e o radar por dimensão.</div>
      <div class="hr"></div>
      <div class="small">Observação: não existe “nota perfeita”. O valor aqui é precisão e consistência.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("COMEÇAR DIAGNÓSTICO"):
            st.session_state.etapa = 'questoes'
            st.rerun()

# =========================================================
# 5) ETAPA 1: QUESTÕES
# =========================================================
elif st.session_state.etapa == 'questoes':

    respondidas = sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None)
    st.markdown(f"<div class='box'><div><span class='highlight'>Instruções rápidas:</span> use a escala de 1 a 5. Responda pensando nos últimos 30 dias.</div><div class='small'>Progresso: {respondidas}/45 respondidas.</div></div>", unsafe_allow_html=True)

    q_idx = 0
    for cat, perguntas in questoes_lista:
        with st.expander(f"DIMENSÃO: {cat.upper()}"):
            st.caption(dim_resumo.get(cat, ""))
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

    colA, colB = st.columns([2, 1])
    with colA:
        if st.button("PROCESSAR MEU DIAGNÓSTICO"):
            if sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None) == 45:
                st.session_state.scores = [sum(st.session_state[f"q_{j}"] for j in range(i, i+5)) for i in range(0, 45, 5)]
                st.session_state.total = sum(st.session_state.scores)
                st.session_state.etapa = 'captura'
                st.rerun()
            else:
                st.error("Responda todas as 45 questões para liberar o diagnóstico.")

    with colB:
        with st.expander("Opções"):
            confirmar = st.checkbox("Confirmo que quero reiniciar e perder minhas respostas.")
            if st.button("REINICIAR DIAGNÓSTICO") and confirmar:
                # limpa respostas
                for i in range(45):
                    if f"q_{i}" in st.session_state:
                        del st.session_state[f"q_{i}"]
                st.session_state.total = 0
                st.session_state.scores = [0]*9
                st.session_state.zona = ""
                st.session_state.nome_usuario = ""
                st.session_state.etapa = "intro"
                st.rerun()

# =========================================================
# 6) ETAPA 2: CAPTURA
# =========================================================
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>DIAGNÓSTICO CONCLUÍDO</h3>", unsafe_allow_html=True)
        st.markdown("<div class='small' style='text-align:center;'>Preencha seus dados para liberar o resultado e seu radar por dimensão.</div>", unsafe_allow_html=True)

        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa / Cargo")

            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona, st.session_state.nome_usuario = z, nome

                    payload = {"nome": nome, "email": email, "whatsapp": whatsapp, "cargo": cargo, "pontos": t, "zona": z}
                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                    except:
                        pass

                    # NOVO: etapa intermediária de processamento (percepção de robustez)
                    st.session_state.etapa = 'processando'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos para liberar o resultado.")

# =========================================================
# 7) ETAPA 2.5: PROCESSANDO (NOVA)
# =========================================================
elif st.session_state.etapa == 'processando':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.markdown("<div><span class='highlight'>Processando seu diagnóstico…</span></div>", unsafe_allow_html=True)

        mensagens = [
            "Validando consistência das respostas…",
            "Calculando pontuação por dimensão…",
            "Gerando seu mapa de governança…",
            "Preparando direcionamento estratégico…",
            "Finalizando visualização do radar…"
        ]

        prog = st.progress(0)
        area = st.empty()

        total_steps = 50  # ~10s (50 * 0.2)
        for i in range(total_steps):
            prog.progress((i + 1) / total_steps)
            if i % 10 == 0:
                area.markdown(f"<div class='small'>{random.choice(mensagens)}</div>", unsafe_allow_html=True)
            time.sleep(0.2)

        st.markdown("<div class='small'>Concluído. Abrindo seu resultado…</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(0.6)
    st.session_state.etapa = 'resultado'
    st.rerun()

# =========================================================
# 8) ETAPA 3: RESULTADO
# =========================================================
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
        st.markdown("### Direcionamento Estratégico")

        if st.session_state.zona == "ELITE":
            texto = (
                f"<span class='highlight'>{st.session_state.nome_usuario}</span>, seus resultados indicam <b>Governança de Elite</b>. "
                "O foco agora é blindar constância e evitar a cegueira da eficiência. "
                "Autoliderança é um processo vivo: seu próximo ganho está em refinamento e expansão."
            )
        elif st.session_state.zona == "OSCILAÇÃO":
            texto = (
                f"<span class='highlight'>{st.session_state.nome_usuario}</span>, você está na zona de <b>Oscilação</b>. "
                "Sua performance alterna entre picos e vales porque a disciplina ainda depende de estímulos externos. "
                "Para tracionar, você precisa estabilizar os pilares operacionais e silenciar a narrativa sabotadora."
            )
        else:
            texto = (
                f"<span class='highlight'>{st.session_state.nome_usuario}</span>, você está em <b>Sobrevivência</b>. "
                "Sua governança pessoal está em colapso e isso costuma se refletir em agenda, energia e consistência. "
                "A intervenção precisa ser objetiva: menos esforço aleatório, mais método aplicado nos pontos vitais."
            )

        st.markdown(texto, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")

    # NOVO: explica claramente o que muda no laudo completo (antes do botão)
    st.markdown("<h3 style='text-align: center;'>Próximo Passo</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="box">
      <div><span class="highlight">Você já recebeu:</span> sua zona + sua pontuação + seu radar por dimensão.</div>
      <div class="hr"></div>
      <div><span class="highlight">No Laudo Completo (IA) você recebe:</span></div>
      <div class="small">• Interpretação detalhada dimensão por dimensão (forças e gargalos).</div>
      <div class="small">• Plano de ação prático (7 dias + 30 dias) com prioridade e sequência.</div>
      <div class="small">• Três focos de intervenção imediata para subir de nível mais rápido.</div>
      <div class="small">• Recomendações de rotina e checkpoints para manter consistência.</div>
    </div>
    """, unsafe_allow_html=True)

    # 1) BOTÃO CHECKOUT
    st.markdown("""
        <div style='text-align: center; margin-bottom: 18px;'>
            <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001226; padding: 20px 45px; font-weight: bold; border-radius: 8px; display: inline-block; width: 100%; max-width: 650px; font-size: 20px;'>
                    ADQUIRIR LAUDO COMPLETO COM IA
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # 2) BOTÃO WHATSAPP
    wa_url = "https://wa.me/5581982602018?text=Olá!%20Acabei%20de%20fazer%20meu%20Diagnóstico%20LIDERUM%20e%20quero%20conhecer%20as%20soluções."
    st.markdown(f"""
        <div style='text-align: left;'>
            <a href='{wa_url}' target='_blank' style='text-decoration: none;'>
                <div style='background: rgba(212, 175, 55, 0.1); color: #D4AF37; border: 1px solid #D4AF37; padding: 12px 25px; font-weight: bold; border-radius: 5px; display: inline-block;'>
                    FALE COM NOSSA EQUIPE
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("Opções"):
        confirmar = st.checkbox("Confirmo que quero reiniciar e perder minhas respostas.", key="confirmar_reiniciar_final")
        if st.button("REINICIAR DIAGNÓSTICO", key="reiniciar_final") and confirmar:
            for i in range(45):
                if f"q_{i}" in st.session_state:
                    del st.session_state[f"q_{i}"]
            st.session_state.total = 0
            st.session_state.scores = [0]*9
            st.session_state.zona = ""
            st.session_state.nome_usuario = ""
            st.session_state.etapa = "intro"
            st.rerun()
