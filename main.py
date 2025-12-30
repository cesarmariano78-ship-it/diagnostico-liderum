import streamlit as st
import plotly.graph_objects as go
import time
import datetime
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# 1. SETUP VISUAL LIDERUM (NOMES BRANCOS PARA VISIBILIDADE)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background-color: #000c1a; color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; }
    
    /* NOMES DOS CAMPOS EM BRANCO */
    label, .stTextInput label, p { color: #FFFFFF !important; font-size: 18px !important; font-weight: 600 !important; }
    
    div[data-testid="stRadio"] label p { color: #FFFFFF !important; font-size: 24px !important; font-weight: 800 !important; }
    div[role="radiogroup"] label { background-color: #001f3f !important; border: 2px solid #D4AF37 !important; padding: 10px 25px !important; border-radius: 8px; margin-right: 10px; }
    .stForm { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid #D4AF37 !important; border-radius: 15px !important; padding: 30px !important; }
    .stButton>button, div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; font-weight: 700 !important; font-size: 20px !important;
        width: 100% !important; border: none !important; padding: 15px !important;
    }
    .question-text { font-size: 20px !important; color: #FFFFFF !important; margin-top: 25px; border-bottom: 1px solid rgba(212, 175, 55, 0.1); padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# CATEGORIAS
categorias = ["Visão e Alinhamento Estratégico", "Recompensa e Reforço Positivo", "Análise e Consciência de Padrões", "Governança e Disciplina Operacional", "Modelagem e Expansão de Repertório", "Gestão da Narrativa e Mindset", "Arquitetura de Sistemas de Crenças", "Padrão de Entrega e Excelência", "Postura Ativa e Protagonismo"]

# ETAPA 1: QUESTÕES
if st.session_state.etapa == 'questoes':
    # --- BOTÃO DE ATALHO DE TESTE ---
    if st.button("🧪 MODO TESTE: PULAR PARA CADASTRO"):
        for i in range(45): st.session_state[f"q_{i}"] = random.randint(3, 5)
        st.session_state.total = sum(st.session_state[f"q_{i}"] for i in range(45))
        st.session_state.etapa = 'captura'
        st.rerun()

    q_idx = 0
    for cat in categorias:
        with st.expander(f"✨ DIMENSÃO: {cat.upper()}"):
            for p_num in range(5):
                st.markdown(f"<p class='question-text'>Pergunta {p_num + 1} de {cat}</p>", unsafe_allow_html=True)
                st.radio(f"R_{q_idx}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{q_idx}", label_visibility="collapsed")
                q_idx += 1
    
    if st.button("PROCESSAR MEU DIAGNÓSTICO"):
        respondidas = sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None)
        if respondidas == 45:
            st.session_state.total = sum(st.session_state.get(f"q_{i}") for i in range(45))
            st.session_state.etapa = 'captura'
            st.rerun()
        else: st.error(f"⚠️ Responda todas as 45 questões.")

# ETAPA 2: CAPTURA E GRAVAÇÃO
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 RESULTADO DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa e Cargo")
            
            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    t = st.session_state.total
                    z = "ZONA DE ELITE" if t > 200 else "ZONA DE OSCILAÇÃO" if t > 122 else "ZONA DE SOBREVIVÊNCIA"
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        df_existente = conn.read(worksheet="Sheet1")
                        
                        # NOMES DAS COLUNAS CONFERIDOS UM POR UM
                        nova = pd.DataFrame([{
                            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Nome": nome,
                            "Email": email,
                            "WhatsApp": whatsapp,
                            "Cargo": cargo,
                            "Pontuacao_Total": t,
                            "Zona": z
                        }])
                        
                        conn.update(worksheet="Sheet1", data=pd.concat([df_existente, nova], ignore_index=True))
                        st.session_state.etapa = 'resultado'
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ ERRO TÉCNICO AO SALVAR: {e}")
                else: st.warning("Preencha todos os campos.")

# ETAPA 3: SUCESSO
elif st.session_state.etapa == 'resultado':
    st.success("✅ Diagnóstico enviado com sucesso!")
    st.write(f"Sua Pontuação Total: {st.session_state.total}")
    if st.button("RECOMEÇAR"):
        st.session_state.etapa = 'questoes'
        st.rerun()
