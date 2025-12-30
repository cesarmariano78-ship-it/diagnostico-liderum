import streamlit as st
import plotly.graph_objects as go
import datetime
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# 1. SETUP VISUAL LIDERUM
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    label, p, .stTextInput label { color: #FFFFFF !important; font-size: 18px !important; font-weight: 600 !important; }
    .stButton>button { background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important; color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; }
    .question-text { font-size: 18px !important; color: #FFFFFF !important; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# LISTA DE CATEGORIAS E PERGUNTAS (45 ITENS)
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

# ETAPA 1: QUESTÕES
if st.session_state.etapa == 'questoes':
    if st.button("🧪 MODO TESTE: PREENCHER TUDO"):
        for i in range(45): st.session_state[f"q_{i}"] = random.randint(3, 5)
        st.session_state.total = sum(st.session_state[f"q_{i}"] for i in range(45))
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
            st.session_state.total = sum(st.session_state.get(f"q_{i}") for i in range(45))
            st.session_state.etapa = 'captura'
            st.rerun()
        else: st.error("⚠️ Responda todas as 45 questões.")

# ETAPA 2: CAPTURA E GRAVAÇÃO (USANDO O SECRETS AUTOMÁTICO)
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 RESULTADO DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome, email = st.text_input("Nome Completo"), st.text_input("E-mail Estratégico")
            whatsapp, cargo = st.text_input("WhatsApp"), st.text_input("Empresa e Cargo")
            
            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    t = st.session_state.total
                    z = "ZONA DE ELITE" if t > 200 else "ZONA DE OSCILAÇÃO" if t > 122 else "ZONA DE SOBREVIVÊNCIA"
                    try:
                        # CONEXÃO AUTOMÁTICA (Lê do Secrets [connections.gsheets])
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        
                        # Tenta ler a aba. Se o nome estiver errado, ele avisará.
                        df_existente = conn.read(worksheet="Sheet1")
                        
                        nova = pd.DataFrame([{
                            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Nome": nome, "Email": email, "WhatsApp": whatsapp, 
                            "Cargo": cargo, "Pontuacao_Total": t, "Zona": z
                        }])
                        
                        conn.update(worksheet="Sheet1", data=pd.concat([df_existente, nova], ignore_index=True))
                        st.session_state.etapa = 'resultado'
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ ERRO NA PLANILHA: {e}")
                        st.info("Dica: Verifique se o nome da aba é 'Sheet1' ou 'Página1'.")
                else: st.warning("Preencha todos os campos.")

# ETAPA 3: SUCESSO
elif st.session_state.etapa == 'resultado':
    st.success("✅ FUNCIONOU! Verifique sua planilha agora.")
    st.write(f"Sua Pontuação Total: {st.session_state.total}")
    if st.button("RECOMEÇAR"):
        st.session_state.etapa = 'questoes'
        st.rerun()
