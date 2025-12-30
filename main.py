import streamlit as st
import plotly.graph_objects as go
import requests
import datetime
import random

# 1. IDENTIDADE VISUAL LIDERUM (Dark Blue & Gold)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
    .stButton>button { 
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important; 
        color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; border-radius: 5px;
    }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 10px; }
    .laudo-container { background-color: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-top: 20px; }
    .highlight { color: #D4AF37; font-weight: bold; font-size: 22px; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO (SEGURANÇA CONTRA QUEBRAS)
if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'
if 'total' not in st.session_state: st.session_state.total = 0
if 'scores' not in st.session_state: st.session_state.scores = [0] * 9

# URL VALIDADA QUE ESTÁ SALVANDO NA SUA PLANILHA
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# 3. LISTA INTEGRAL DAS 45 PERGUNTAS (9 DIMENSÕES)
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

# --- ETAPA 1: QUESTÕES ---
if st.session_state.etapa == 'questoes':
    if st.button("🧪 MODO TESTE RÁPIDO"):
        st.session_state.scores = [random.randint(18, 25) for _ in range(9)]
        st.session_state.total = sum(st.session_state.scores)
        st.session_state.etapa = 'captura'; st.rerun()

    q_idx = 0
    for cat, perguntas in questoes_lista:
        with st.expander(f"✨ DIMENSÃO: {cat.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"R_{q_idx}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{q_idx}", label_visibility="collapsed")
                q_idx += 1
    
    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None) == 45:
            st.session_state.scores = [sum(st.session_state[f"q_{j}"] for j in range(i, i+5)) for i in range(0, 45, 5)]
            st.session_state.total = sum(st.session_state.scores)
            st.session_state.etapa = 'captura'; st.rerun()
        else: st.error("⚠️ Responda todas as 45 questões.")

# --- ETAPA 2: CADASTRO E SALVAMENTO ---
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 RESULTADO DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
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
                        st.session_state.etapa = 'resultado'; st.rerun()
                    except: st.session_state.etapa = 'resultado'; st.rerun()
                else: st.warning("Preencha todos os campos.")

# --- ETAPA 3: LAUDO COM RADAR E CTA SUTIL (O SEU LAYOUT) ---
elif st.session_state.etapa == 'resultado':
    st.markdown(f"## Análise Individual: {st.session_state.nome_usuario}")
    col_l, col_r = st.columns([1.3, 0.7])
    
    with col_l:
        # Gráfico de Radar Profissional (Plotly)
        categories = ['Visão', 'Recompensa', 'Análise', 'Governança', 'Modelagem', 'Narrativa', 'Crenças', 'Excelência', 'Postura']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=st.session_state.scores, theta=categories, fill='toself', fillcolor='rgba(212, 175, 55, 0.3)', line=dict(color='#D4AF37')))
        fig.update_layout(polar=dict(bgcolor="rgba(0,12,26,1)", radialaxis=dict(visible=True, range=[0, 25], color="white")), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white", size=13))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown(f"### Pontuação: <span class='highlight'>{st.session_state.total} / 225</span>", unsafe_allow_html=True)
        st.markdown(f"### Zona de Governança: <span class='highlight'>{st.session_state.zona}</span>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)
        if st.session_state.zona == "ELITE":
            st.markdown("**DIRECIONAMENTO ESTRATÉGICO:** Você possui uma governança de alto nível. O seu desafio agora é a manutenção da constância absoluta e evitar a cegueira da zona de conforto.")
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown("**DIRECIONAMENTO ESTRATÉGICO:** Sua performance oscila entre picos de excelência e vales de inércia. É necessário estabilizar seus processos básicos.")
        else:
            st.markdown("**DIRECIONAMENTO ESTRATÉGICO:** Alerta Crítico: Sua governança pessoal está colapsada. Você opera em modo de sobrevivência. A intervenção deve ser imediata.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    # CHAMADA SUTIL PARA O LAUDO PAGO
    st.markdown("<h3 style='text-align: center;'>Próximo Passo Estratégico</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Este diagnóstico gratuito aponta sua zona atual. Para subir de nível, você precisa de profundidade. O nosso <b>Laudo Estratégico Completo LIDERUM</b> analisa cada uma das suas respostas com IA para entregar um plano de ação personalizado.</p>", unsafe_allow_html=True)
    
    # CTA DOURADO LIDERUM
    st.markdown(f"""
        <div style='text-align: center; margin-top: 15px;'>
            <a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001226; padding: 15px 45px; font-weight: bold; border-radius: 5px; display: inline-block; font-size: 19px;'>
                    ADQUIRIR MEU LAUDO ESTRATÉGICO COMPLETO COM IA →
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RECOMEÇAR DIAGNÓSTICO"):
        st.session_state.etapa = 'questoes'; st.rerun()
