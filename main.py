import streamlit as st
import plotly.graph_objects as go
import time
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. SETUP VISUAL E CSS
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background-color: #000c1a; color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; }
    
    /* NÚMEROS 1 A 5 - VISIBILIDADE MÁXIMA */
    div[data-testid="stRadio"] label p { color: #FFFFFF !important; font-size: 28px !important; font-weight: 900 !important; }
    div[role="radiogroup"] label { background-color: #001f3f !important; border: 2px solid #D4AF37 !important; padding: 15px 35px !important; border-radius: 8px; margin-right: 15px; }

    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid #D4AF37 !important; border-radius: 15px !important; padding: 35px !important; }
    .stButton>button, div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; font-weight: 700 !important; font-size: 20px !important;
        width: 100% !important; border: none !important; padding: 15px !important;
    }
    .question-text { font-size: 22px !important; color: #FFFFFF !important; margin-top: 35px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 12px; border-left: 12px solid #D4AF37; margin-bottom: 30px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: 
    st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# LISTA OFICIAL DE QUESTÕES (45 ITENS)
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

# ETAPA 1: PERGUNTAS
if st.session_state.etapa == 'questoes':
    q_idx = 0
    for cat, perguntas in questoes_lista:
        with st.expander(f"✨ AVALIAR: {cat.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"R_{q_idx}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{q_idx}", label_visibility="collapsed")
                q_idx += 1
    
    if st.button("FINALIZAR E PROCESSAR DIAGNÓSTICO"):
        respondidas = sum(1 for i in range(45) if st.session_state.get(f"q_{i}") is not None)
        
        if respondidas == 45:
            notas_finais = {}
            atual = 0
            for cat, pergs in questoes_lista:
                notas_cat = sum(st.session_state.get(f"q_{i}") for i in range(atual, atual + 5))
                notas_finais[cat] = notas_cat
                atual += 5
            
            st.session_state.notas = notas_finais
            st.session_state.total = sum(notas_finais.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error(f"⚠️ Atenção: Você respondeu {respondidas} de 45 questões. Por favor, revise os blocos acima.")

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
                    if t <= 122: z, c, tx = "ZONA DE SOBREVIVÊNCIA", "🔴", "Sua pontuação indica que você está operando em Zona de Risco..."
                    elif t <= 200: z, z, tx = "ZONA DE OSCILAÇÃO", "🟠", "Você possui as competências necessárias, mas está preso em um ciclo de oscilação..."
                    else: z, c, tx = "ZONA DE ELITE", "🌟", "Parabéns! Sua pontuação o coloca em um patamar muito acima da média..."
                    
                    st.session_state.res_zona, st.session_state.res_cor, st.session_state.res_txt = z, c, tx

                    # TENTATIVA DE GRAVAÇÃO NA PLANILHA
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        # O nome 'Sheet1' abaixo deve ser igual ao nome da aba na sua planilha do Google
                        df_existente = conn.read(worksheet="Sheet1") 
                        
                        nova_linha = pd.DataFrame([{
                            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Nome": nome,
                            "Email": email,
                            "WhatsApp": whatsapp,
                            "Cargo": cargo,
                            "Pontuacao_Total": t,
                            "Zona": z
                        }])
                        
                        df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
                        conn.update(worksheet="Sheet1", data=df_atualizado)
                        st.success("Diagnóstico registrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao salvar dados: {e}. Verifique se a aba da planilha se chama 'Sheet1'.")
                    
                    with st.spinner('Gerando seu gráfico estratégico...'):
                        time.sleep(2)
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos.")

# ETAPA 3: LAUDO ESTRATÉGICO
elif st.session_state.etapa == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>SEU MAPA ESTRATÉGICO DE PERFORMANCE</h2>", unsafe_allow_html=True)
    
    # Gerar Gráfico Radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(st.session_state.notas.values()) + [list(st.session_state.notas.values())[0]],
        theta=list(st.session_state.notas.keys()) + [list(st.session_state.notas.keys())[0]],
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.4)',
        line=dict(color='#D4AF37', width=6)
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white")),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=650
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{st.session_state.res_cor} STATUS: {st.session_state.res_zona}</h2><p style='margin-top:20px; font-size: 21px;'>{st.session_state.res_txt}</p></div>", unsafe_allow_html=True)
    
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO COMPLETO (IA)", "https://wa.me/5581986245870")
