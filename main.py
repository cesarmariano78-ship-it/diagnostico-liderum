import streamlit as st
import plotly.graph_objects as go
import requests
import datetime
import random

# 1. SETUP VISUAL LIDERUM (Identidade Visual)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    label, p, span, div { color: #FFFFFF !important; font-size: 18px !important; }
    .stButton>button { 
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important; 
        color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; border: none; border-radius: 5px;
    }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }
    .stExpander { border: 1px solid rgba(212, 175, 55, 0.3) !important; background-color: rgba(255, 255, 255, 0.05) !important; }
    </style>
    """, unsafe_allow_html=True)

# URL EXTRAÍDA DA SUA IMAGEM (image_dd0739.png)
URL_WEBHOOK = "https://script.google.com/macros/s/AKfycbwrbNk635ZiqpX0U7TRvkYfTQJsC3sO6m4KbBFEDruHLiaGDmhEax0wsd6FIkNlovM/exec"

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# 2. LISTA COMPLETA DAS 45 PERGUNTAS (9 Dimensões)
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

# --- ETAPA 1: DIAGNÓSTICO ---
if st.session_state.etapa == 'questoes':
    if st.button("🧪 MODO TESTE RÁPIDO: PREENCHER TUDO"):
        for i in range(45): st.session_state[f"q_{i}"] = random.randint(3, 5)
        st.session_state.etapa = 'captura'
        st.rerun()

    q_idx = 0
    for cat, perguntas in questoes_lista:
        with st.expander(f"✨ DIMENSÃO: {cat.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"R_{q_idx}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{q_idx}", label_visibility="collapsed")
                q_idx += 1
    
    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        if sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None) == 45:
            st.session_state.etapa = 'captura'
            st.rerun()
        else: st.error("⚠️ Responda todas as 45 questões.")

# --- ETAPA 2: CADASTRO E ENVIO ---
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🔒 RESULTADO DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Cargo")
            
            if st.form_submit_button("GERAR MEU LAUDO AGORA"):
                if all([nome, email, whatsapp, cargo]):
                    # Cálculos das Notas por Dimensão
                    scores = []
                    for i in range(0, 45, 5):
                        soma = sum(st.session_state[f"q_{j}"] for j in range(i, i+5))
                        scores.append(soma)
                    
                    st.session_state.scores = scores
                    st.session_state.total = sum(scores)
                    t = st.session_state.total
                    st.session_state.zona = "ELITE" if t > 200 else "OSCILAÇÃO" if t > 122 else "SOBREVIVÊNCIA"
                    st.session_state.dados_lead = {"nome": nome, "email": email}
                    
                    # Payload para o Webhook
                    payload = {
                        "nome": nome, "email": email, "whatsapp": whatsapp,
                        "cargo": cargo, "pontos": t, "zona": st.session_state.zona
                    }
                    try:
                        requests.post(URL_WEBHOOK, json=payload, timeout=10)
                        st.session_state.etapa = 'resultado'
                        st.rerun()
                    except: st.error("Falha ao salvar dados, mas vamos gerar seu laudo.")
                else: st.warning("Preencha todos os campos.")

# --- ETAPA 3: LAUDO E GRÁFICO DE RADAR ---
elif st.session_state.etapa == 'resultado':
    st.markdown(f"## Olá, {st.session_state.dados_lead['nome']}! Aqui está sua análise.")
    
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown(f"### Pontuação Total: **{st.session_state.total} / 225**")
        st.markdown(f"### Zona de Governança: **{st.session_state.zona}**")
        
        # Laudo de Feedback baseado na Zona
        if st.session_state.zona == "ELITE":
            st.info("📊 **LAUDO:** Você possui uma governança de alto nível. Seu desafio agora é a manutenção da constância e a modelagem de novos sucessores.")
        elif st.session_state.zona == "OSCILAÇÃO":
            st.warning("📊 **LAUDO:** Sua performance alterna entre picos de excelência e vales de inércia. É necessário estabilizar seus processos de disciplina.")
        else:
            st.error("📊 **LAUDO:** Sua governança pessoal está em estado crítico. O foco imediato deve ser na recuperação da disciplina básica e visão de futuro.")

    with col_r:
        # Gráfico de Radar usando Plotly
        categories = ['Visão', 'Recompensa', 'Análise', 'Governança', 'Modelagem', 'Narrativa', 'Crenças', 'Excelência', 'Postura']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=st.session_state.scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(212, 175, 55, 0.4)',
            line=dict(color='#D4AF37')
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,12,26,1)",
                radialaxis=dict(visible=True, range=[0, 25], color="white")
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

    if st.button("RECOMEÇAR DIAGNÓSTICO"):
        st.session_state.etapa = 'questoes'
        st.rerun()
