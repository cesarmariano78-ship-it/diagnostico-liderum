import streamlit as st
import plotly.graph_objects as go
import time
import datetime
import pandas as pd
import random
import re
from streamlit_gsheets import GSheetsConnection

# 1. FUNÇÃO DE LIMPEZA (Cura o erro de 65 caracteres automaticamente)
def sanitize_private_key(pem: str) -> str:
    if pem is None: return ""
    # Remove caracteres invisíveis e normaliza quebras
    pem = pem.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n").strip()
    # Garante que o cabeçalho e rodapé estejam corretos
    pem = pem.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")
    pem = pem.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
    # Extrai apenas o miolo da chave
    m = re.search(r"-----BEGIN PRIVATE KEY-----\s*(.*?)\s*-----END PRIVATE KEY-----", pem, flags=re.DOTALL)
    if not m: return pem
    body = m.group(1)
    # Remove qualquer coisa que não seja Base64 (espaços, tabs, etc)
    body = re.sub(r"[^A-Za-z0-9+/=]", "", body)
    # Reconstrói a chave no padrão exigido pelo Google
    body = "\n".join(body[i:i+64] for i in range(0, len(body), 64))
    return f"-----BEGIN PRIVATE KEY-----\n{body}\n-----END PRIVATE KEY-----\n"

# 2. SETUP VISUAL LIDERUM
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000c1a; color: #FFFFFF; }
    label, p, .stTextInput label { color: #FFFFFF !important; font-size: 18px !important; font-weight: 600 !important; }
    .stButton>button { background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important; color: #001226 !important; width: 100%; font-weight: bold; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# CATEGORIAS
categorias = ["Visão", "Recompensa", "Análise", "Governança", "Modelagem", "Narrativa", "Crenças", "Excelência", "Protagonismo"]

# ETAPA 1: QUESTÕES
if st.session_state.etapa == 'questoes':
    # ATALHO PARA NÃO RESPONDER 45 VEZES
    if st.button("🧪 MODO TESTE: PREENCHER TUDO E IR PARA PLANILHA"):
        for i in range(45): st.session_state[f"q_{i}"] = random.randint(3, 5)
        st.session_state.total = sum(st.session_state[f"q_{i}"] for i in range(45))
        st.session_state.etapa = 'captura'
        st.rerun()

    st.info("Responda as questões ou use o Modo Teste acima.")

# ETAPA 2: CAPTURA E GRAVAÇÃO (ONDE A LIMPEZA ACONTECE)
elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa e Cargo")
            
            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    try:
                        # PEGA AS CREDENCIAIS E "LAVA" A CHAVE PRIVADA
                        creds = dict(st.secrets["connections"]["gsheets"])
                        creds["private_key"] = sanitize_private_key(creds["private_key"])
                        
                        # CONECTA USANDO A CHAVE JÁ LIMPA
                        conn = st.connection("gsheets", type=GSheetsConnection, **creds)
                        df_existente = conn.read(worksheet="Sheet1")
                        
                        # MONTA A LINHA COM OS NOMES EXATOS DA SUA PLANILHA
                        nova = pd.DataFrame([{
                            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Nome": nome, "Email": email, "WhatsApp": whatsapp, 
                            "Cargo": cargo, "Pontuacao_Total": st.session_state.total, 
                            "Zona": "Teste Conexão"
                        }])
                        
                        conn.update(worksheet="Sheet1", data=pd.concat([df_existente, nova], ignore_index=True))
                        st.session_state.etapa = 'resultado'
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ ERRO MESMO COM A LIMPEZA: {e}")
                else: st.warning("Preencha todos os campos.")

# ETAPA 3: SUCESSO
elif st.session_state.etapa == 'resultado':
    st.success("✅ DADOS ENVIADOS! Verifique sua planilha.")
    st.write(f"Pontuação: {st.session_state.total}")
    if st.button("RECOMEÇAR"):
        st.session_state.etapa = 'questoes'
        st.rerun()
