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
    .stMetric { background-color: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #D4AF37; }
    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
    .stButton>button { 
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important; 
        color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; border-radius: 8px; font-size: 20px !important;
    }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 10px; }
    .laudo-container { background-color: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 15px; border-left: 6px solid #D4AF37; margin-top: 25px; line-height: 1.6; }
    .highlight { color: #D4AF37 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE ESTADO
if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'
if 'total' not in st.session_state: st.session_state.total = 0
if 'scores' not in st.session_state: st.session_state.scores = [0] * 9

# URL QUE JÁ ESTÁ FUNCIONANDO (image_dd0739.png)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FlKnIovM/exec"

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# LISTA INTEGRAL DAS 45 PERGUNTAS
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
        else: st.error("⚠️ Responda todas as 45 questões para gerar o laudo.")

# --- ETAPA 2: CAPTURA (image_ddd5ac.png) ---
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 DIAGNÓSTICO CONCLUÍDO!</h3>", unsafe_allow_html=True)
        st.write("Preencha os dados abaixo para desbloquear sua devolutiva individual e o gráfico de radar.")
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa / Cargo")
            if st.form_submit_button("LIBERAR MEU LAUDO AGORA"):
                if all([nome, email, whatsapp, cargo]):
                    t = st.session_state.total
                    z = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.zona, st.session_state.nome_usuario = z, nome
                    payload = {"nome": nome, "email": email, "whatsapp": whatsapp, "cargo": cargo, "pontos": t, "zona": z}
                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                        st.session_state.etapa = 'resultado'; st.rerun()
                    except: st.session_state.etapa = 'resultado'; st.rerun()
                else: st.warning("Por favor, preencha todos os campos para prosseguir.")

# --- ETAPA 3: LAUDO DE ALTO IMPACTO ---
elif st.session_state.etapa == 'resultado':
    st.markdown(f"## Protocolo LIDERUM: {st.session_state.nome_usuario}")
    
    # Cabeçalho com Notas em Destaque
    c1, c2 = st.columns(2)
    with c1: st.metric("Sua Pontuação Total", f"{st.session_state.total} / 225")
    with c2: st.metric("Zona de Performance", st.session_state.zona)
    
    st.write("---")
    
    col_l, col_r = st.columns([1.1, 0.9])
    
    with col_l:
        # Radar Plotly com tamanho aumentado
        categories = ['Visão', 'Recompensa', 'Análise', 'Governança', 'Modelagem', 'Narrativa', 'Crenças', 'Excelência', 'Postura']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=st.session_state.scores, theta=categories, fill='toself', fillcolor='rgba(212, 175, 55, 0.3)', line=dict(color='#D4AF37', width=3)))
        fig.update_layout(
            polar=dict(bgcolor="rgba(0,12,26,1)", radialaxis=dict(visible=True, range=[0, 25], color="#888", gridcolor="rgba(212,175,55,0.2)")),
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)", height=550, margin=dict(l=80, r=80, t=20, b=20),
            font=dict(color="white", size=15)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='laudo-container'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Devolutiva Estratégica")
        if st.session_state.zona == "ELITE":
            st.markdown(f"""
            Parabéns, <span class='highlight'>{st.session_state.nome_usuario}</span>. Seus resultados indicam uma **Governança de Elite**. 
            Você possui clareza estratégica e disciplina operacional acima da média. Seu maior risco agora é a **cegueira da eficiência**: quando o sistema roda tão bem que você para de questionar as novas fronteiras. 
            O foco deve ser na blindagem da sua rotina e na modelagem de sucessão.
            """, unsafe_allow_html=True)
        elif st.session_state.zona == "OSCILAÇÃO":
            st.markdown(f"""
            Atenção, <span class='highlight'>{st.session_state.nome_usuario}</span>. Sua performance é marcada por **intermitência**. 
            Você vive ciclos de 'explosão de produtividade' seguidos de vales de inércia ou apagamento de incêndios. Isso acontece porque sua governança pessoal ainda é refém de estímulos externos ou do seu estado emocional. 
            É necessário estabilizar seus pilares de disciplina básica para parar de 'patinar' e começar a tracionar de verdade.
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            Alerta Crítico, <span class='highlight'>{st.session_state.nome_usuario}</span>. Seus dados indicam que você está em **Modo de Sobrevivência**. 
            Sua governança pessoal está colapsada e você provavelmente sente que está perdendo o controle sobre sua agenda e seus resultados. 
            Não é falta de capacidade, é falta de método. A intervenção nos seus hábitos de liderança e organização deve ser sua prioridade absoluta antes que o esgotamento ocorra.
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    
    # CTAs Estratégicos
    st.markdown("<h3 style='text-align: center;'>Próximo Passo para sua Evolução</h3>", unsafe_allow_html=True)
    st.write("Este laudo superficial é o seu 'ponto de partida'. Para um plano de ação personalizado, escolha uma das opções abaixo:")
    
    bt1, bt2 = st.columns(2)
    with bt1:
        # Link do Checkout Hotmart
        st.markdown(f"<div style='text-align: center;'><a href='https://pay.hotmart.com/SEU_LINK' target='_blank' style='text-decoration: none;'><div style='background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001226; padding: 15px 20px; font-weight: bold; border-radius: 8px; display: inline-block; width: 100%;'>DESBLOQUEAR LAUDO COMPLETO (IA) →</div></a></div>", unsafe_allow_html=True)
    with bt2:
        # Link do WhatsApp
        whatsapp_link = "https://wa.me/5581982602018?text=Ola!%20Acabei%20de%20fazer%20o%20Diagnostico%20LIDERUM%20e%20gostaria%20de%20falar%20sobre%20as%20soluções."
        st.link_button("💬 FALAR COM NOSSO TIME AGORA", whatsapp_link)
