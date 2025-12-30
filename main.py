import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. SETUP VISUAL (NÚMEROS GRANDES E BRANCOS)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background-color: #000c1a; color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    
    /* ESTILO DOS NÚMEROS 1 A 5 - MÁXIMA VISIBILIDADE */
    div[data-testid="stRadio"] label p { 
        color: #FFFFFF !important; 
        font-size: 30px !important; 
        font-weight: 900 !important;
    }
    div[role="radiogroup"] label { 
        background-color: #001f3f !important; 
        border: 2px solid #D4AF37 !important; 
        padding: 15px 35px !important; 
        border-radius: 10px; 
    }

    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid #D4AF37 !important; border-radius: 15px !important; padding: 35px !important; }
    .stButton>button, div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; font-weight: 700 !important; font-size: 20px !important;
        width: 100% !important; border: none !important; padding: 15px !important;
    }
    .question-text { font-size: 22px !important; color: #FFFFFF !important; margin-top: 35px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 12px; border-left: 12px solid #D4AF37; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# 45 PERGUNTAS (Resumidas para o código ficar limpo)
dimensoes_info = {
    "Visão e Alinhamento Estratégico": ["Eu tenho clareza sobre meus objetivos nos próximos meses.", "Meus objetivos pessoais e profissionais estão anotados.", "Mantenho meu foco mesmo com distrações externas.", "Revisito minha visão de futuro com frequência.", "Organizo minhas prioridades pelo que é importante."],
    "Recompensa e Reforço Positivo": ["Reconheço minhas próprias conquistas.", "Comemoro quando concluo uma etapa.", "Me elogio por atitudes positivas.", "Sinto orgulho do meu progresso.", "Crio momentos para celebrar avanços."],
    "Análise e Consciência de Padrões": ["Reviso meu comportamento criticamente.", "Reconheço erros e busco aprender.", "Percebo meus padrões de sabotagem.", "Ajusto rotas sem culpa quando erro.", "Busco feedbacks com abertura."],
    "Governança e Disciplina Operacional": ["Planejo minha rotina de forma organizada.", "Priorizo o importante antes do urgente.", "Mantenho constância sem motivação.", "Equilibro tarefas operacionais e estratégicas.", "Tenho hábitos que sustentam minha produtividade."],
    "Modelagem e Expansão de Repertório": ["Tenho consciência de comportamentos a mudar.", "Busco aprender com quem admiro.", "Replico métodos que funcionam para outros.", "Observo e mudo pensamentos limitantes.", "Incorporo novas habilidades com rapidez."],
    "Gestão da Narrativa e Mindset": ["Minha voz interna me incentiva.", "Percebo e ressignifico pensamentos punitivos.", "Converso comigo com respeito e firmeza.", "Silencio pensamentos sabotadores.", "Meu diálogo interno ajuda minhas ações."],
    "Arquitetura de Sistemas de Crenças": ["Acredito que sou capaz de evoluir sempre.", "Percebo quando ajo por crenças limitantes.", "Mudo minha realidade mudando crenças.", "Tenho crenças fortes sobre minha liderança.", "Identifico a origem das minhas crenças."],
    "Padrão de Entrega e Excelência": ["Me esforço para entregar o máximo.", "Percebo evolução na qualidade das entregas.", "Mantenho comprometimento sob pressão.", "Tenho clareza de pontos fortes e de melhoria.", "Entrego além do básico sempre."],
    "Postura Ativa e Protagonismo": ["Assumo responsabilidade pelas escolhas.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que controlo.", "Encaro desafios como oportunidades.", "Olho para mim antes de culpar o ambiente."]
}

if st.session_state.etapa == 'questoes':
    for dim, perguntas in dimensoes_info.items():
        with st.expander(f"✨ AVALIAR: {dim.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"{p}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{p}", label_visibility="collapsed")
    
    if st.button("FINALIZAR E PROCESSAR DIAGNÓSTICO"):
        if all(st.session_state.get(f"q_{p}") is not None for dim in dimensoes_info.values() for p in dim):
            st.session_state.notas = {dim: sum(st.session_state.get(f"q_{p}") for p in perguntas) for dim, perguntas in dimensoes_info.items()}
            st.session_state.total = sum(st.session_state.notas.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ Responda todas as 45 questões antes de prosseguir.")

elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 RESULTADO DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa e Cargo")
            if st.form_submit_button("LIBERAR MEU RESULTADO AGORA"):
                if nome and email and whatsapp and cargo:
                    # DEFINIÇÃO DO LAUDO (TEXTOS DENSOS)
                    t = st.session_state.total
                    if t <= 122: z, c, tx = "ZONA DE SOBREVIVÊNCIA", "🔴", "Sua pontuação indica que você está operando em Zona de Risco. Assuma o controle! O laudo detalhado traz o plano de ação prático."
                    elif t <= 200: z, c, tx = "ZONA DE OSCILAÇÃO", "🟠", "Você possui as competências necessárias, mas está preso em um ciclo de oscilação. Identifique os seus 'freios de mão invisíveis'."
                    else: z, c, tx = "ZONA DE ELITE", "🌟", "Parabéns! Sua pontuação o coloca em um patamar de elite. O laudo premium revela micro-oportunidades de expansão."
                    
                    st.session_state.res_zona, st.session_state.res_cor, st.session_state.res_txt = z, c, tx

                    # --- COMANDOS DE INTEGRAÇÃO GOOGLE SHEETS ---
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        nova = {"Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "Nome": nome, "Email": email, "WhatsApp": whatsapp, "Cargo": cargo, "Pontuacao_Total": t, "Zona": z}
                        conn.create(data=[nova])
                    except Exception as e:
                        st.warning(f"Atenção: Erro na conexão com a planilha. Verifique as permissões do Google. (Erro: {e})")
                    
                    with st.spinner('Processando dados estratégicos...'): time.sleep(10)
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else: st.warning("Preencha todos os campos para continuar.")

elif st.session_state.etapa == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>SEU MAPA ESTRATÉGICO DE PERFORMANCE</h2>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(st.session_state.notas.values()) + [list(st.session_state.notas.values())[0]], theta=list(st.session_state.notas.keys()) + [list(st.session_state.notas.keys())[0]], fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37', width=6)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=650)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{st.session_state.res_cor} STATUS: {st.session_state.res_zona}</h2><p style='margin-top:20px; font-size: 21px;'>{st.session_state.res_txt}</p></div>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO ESTRATÉGICO", "https://wa.me/5581986245870")
