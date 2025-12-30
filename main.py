import streamlit as st
import pandas as pd
import datetime
import random
from streamlit_gsheets import GSheetsConnection

# 1. SETUP VISUAL
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")
st.markdown("<style>.stApp { background-color: #000c1a; color: #FFFFFF; } label, p { color: #FFFFFF !important; }</style>", unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO LIDERUM")

# ETAPA 1: QUESTÕES (MODO TESTE ATIVO)
if st.session_state.etapa == 'questoes':
    if st.button("🧪 MODO TESTE: PREENCHER TUDO"):
        st.session_state.total = random.randint(150, 240)
        st.session_state.etapa = 'captura'
        st.rerun()
    st.info("Responda ou use o botão de teste acima.")

# ETAPA 2: GRAVAÇÃO NATIVA (A FORMA CORRETA)
elif st.session_state.etapa == 'captura':
    with st.form("lead_form"):
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
        if st.form_submit_button("LIBERAR MEU RESULTADO"):
            try:
                # CONEXÃO LIMPA: O Streamlit lê o Secrets [connections.gsheets] sozinho
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                # Lê a aba Sheet1
                df = conn.read(worksheet="Sheet1")
                
                nova_linha = pd.DataFrame([{
                    "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nome": nome, 
                    "Email": email, 
                    "Pontuacao_Total": st.session_state.total,
                    "Zona": "Teste OK"
                }])
                
                # Atualiza a planilha
                conn.update(worksheet="Sheet1", data=pd.concat([df, nova_linha], ignore_index=True))
                st.session_state.etapa = 'resultado'
                st.rerun()
            except Exception as e:
                st.error(f"❌ ERRO: {e}")

elif st.session_state.etapa == 'resultado':
    st.success("✅ DADOS GRAVADOS COM SUCESSO!")
    st.write(f"Sua Pontuação: {st.session_state.total}")
    if st.button("RECOMEÇAR"):
        st.session_state.etapa = 'questoes'
        st.rerun()
