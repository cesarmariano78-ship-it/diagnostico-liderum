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
        color: #001226 !important; width: 100%; font-weight: bold; padding: 18px; border: none; border-radius: 8px; font-size: 20px !important;
    }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }
    .highlight { color: #D4AF37; font-weight: bold; }
    .stExpander { border: 1px solid rgba(212, 175, 55, 0.3) !important; background-color: rgba(255, 255, 255, 0.05) !important; }
    </style>
    """, unsafe_allow_html=True)

# URL QUE JÁ FUNCIONOU NO SEU TESTE (Extraída de image_dd0739.png)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FIkNlovM/exec"

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# 2. LISTA COMPLETA DAS 45 PERGUNTAS (9 DIMENSÕES)
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

# ETAPA 1: DIAGNÓSTICO
if st.session_state.etapa == 'questoes':
    if st.button("🧪 MODO TESTE RÁPIDO (PREENCHER TUDO)"):
        for i in range(45): st.session_state[f"q_{i}"] = random.randint(3, 5)
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
            scores = [sum(st.session_state[f"q_{j}"] for j in range(i, i+5)) for i in range(0, 45, 5)]
            st.session_state.scores = scores
            st.session_state.total = sum(scores)
            st.session_state.etapa = 'captura'; st.rerun()
        else: st.error("⚠️ Responda todas as 45 questões.")

# ETAPA 2: CADASTRO E GRAVAÇÃO
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
                    except: 
                        # Se houver erro de rede, ainda assim mostra o laudo para não perder o cliente
                        st.session_state.etapa = 'resultado'; st.rerun()
                else: st.warning("Preencha todos os campos.")

# ETAPA 3: LAUDO, RADAR E CHECKOUT (ISCA PAGA)
elif st.session_state.etapa == 'resultado':
    st.markdown(f"## Análise Final: {st.session_state.nome_usuario}")
    col_l, col_r = st.columns([1.2, 0.8])
    
    with col_l:
        categories = ['Visão', 'Recompensa', 'Análise', 'Governança', 'Modelagem', 'Narrativa', 'Crenças', 'Excelência', 'Postura']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=st.session_state.scores, theta=categories, fill='toself', fillcolor='rgba(212, 175, 55, 0.3)', line=dict(color='#D4AF37')))
        fig.update_layout(polar=dict(bgcolor="rgba(0,12,26,1)", radialaxis=dict(visible=True, range=[0, 25], color="white")), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white", size=12))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown(f"### Pontuação: <span class='highlight'>{st.session_state.total} / 225</span>", unsafe_allow_html=True)
        st.markdown(f"### Zona: <span class='highlight'>{st.session_state.zona}</span>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("### 🔍 Resumo de Governança")
        if st.session_state.zona == "ELITE": st.success("Você está no topo da pirâmide de governança pessoal. Foco em manutenção.")
        elif st.session_state.zona == "OSCILAÇÃO": st.warning("Sua performance é inconstante. Necessário estabilizar processos.")
        else: st.error("Estado Crítico: Sua governança pessoal está colapsada. Foco na recuperação básica.")

    st.write("---")
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>🚀 Desbloqueie seu Laudo Estratégico Completo</h2>", unsafe_allow_html=True)
    st.markdown("""
        Adquira agora o seu **Laudo Completo LIDERUM com Inteligência Artificial** e receba um plano de ação personalizado de 30 dias para subir de zona.
    """)
    
    # Link da Hotmart (Isenta de erros)
    link_pagamento = "https://pay.hotmart.com/SEU_LINK_AQUI"
    st.markdown(f"""
        <div style='text-align: center;'>
            <a href='{link_pagamento}' target='_blank'>
                <button style='background: linear-gradient(180deg, #28a745 0%, #218838 100%); color: white; border: none; padding: 22px 45px; font-size: 24px; font-weight: bold; border-radius: 12px; cursor: pointer; width: 100%; max-width: 600px;'>
                    QUERO MEU LAUDO ESTRATÉGICO COM IA →
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RECOMEÇAR"):
        st.session_state.etapa = 'questoes'; st.rerun()
