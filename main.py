import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. ESTÉTICA DE ALTO IMPACTO (CONTRASTE MÁXIMO PARA OS NÚMEROS)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: #000c1a; color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; font-size: 38px !important; }
    
    /* CORREÇÃO DOS NÚMEROS 1-5 (ALTO CONTRASTE) */
    div[data-testid="stRadio"] label p { 
        color: #FFFFFF !important; 
        font-size: 26px !important; 
        font-weight: 900 !important; 
        text-shadow: 2px 2px 4px #000000;
    }
    div[role="radiogroup"] label { 
        background: #1a3a5a !important; /* Azul sólido escuro */
        border: 2px solid #D4AF37 !important; 
        padding: 15px 35px !important; 
        border-radius: 10px; 
        margin-right: 15px; 
    }

    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid #D4AF37 !important; border-radius: 15px !important; padding: 35px !important; }
    label[data-testid="stWidgetLabel"] p { color: #FFFFFF !important; font-weight: 700 !important; font-size: 18px !important; }

    .stButton>button, div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; font-weight: 700 !important; font-size: 20px !important;
        width: 100% !important; border: none !important; padding: 15px !important;
        box-shadow: 0px 4px 20px rgba(212, 175, 55, 0.6) !important; text-transform: uppercase;
    }
    .question-text { font-size: 22px !important; color: #FFFFFF !important; margin-top: 35px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 12px; border-left: 10px solid #D4AF37; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

dimensoes_info = {
    "Visão e Alinhamento Estratégico": ["Eu tenho clareza sobre meus objetivos nos próximos meses.", "Meus objetivos pessoais e profissionais estão anotados e organizados.", "Eu consigo manter meu foco mesmo diante de distrações externas.", "Eu revisito minha visão de futuro com frequência para me orientar.", "Eu organizo minhas prioridades com base no que é realmente importante."],
    "Recompensa e Reforço Positivo": ["Eu reconheço minhas próprias conquistas, mesmo que pequenas.", "Eu costumo comemorar quando concluo uma etapa de um projeto.", "Eu me elogio por atitudes positivas que tomo no dia a dia.", "Eu consigo sentir orgulho do meu progresso, mesmo que não seja perfeito.", "Eu crio momentos intencionais para celebrar avanços."],
    "Análise e Consciência de Padrões": ["Eu costumo revisar meu comportamento com espírito crítico construtivo.", "Reconheço quando errei e busco aprender com isso.", "Consigo perceber meus padrões de sabotagem ou repetição de erros.", "Eu me permito ajustar rotas sem culpa quando percebo que errei.", "Busco feedbacks com abertura para rever minhas atitudes."],
    "Governança e Disciplina Operacional": ["Eu consigo planejar minha rotina de forma organizada e funcional.", "Eu priorizo o que é mais importante ao invés de apenas o urgente.", "Mantenho constância mesmo quando não estou motivado.", "Sou capaz de equilibrar tarefas operacionais e estratégicas.", "Tenho sistemas ou hábitos que sustentam minha produtividade."],
    "Modelagem e Expansão de Repertório": ["Eu tenho consciência de comportamentos que preciso mudar.", "Busco aprender com pessoas que têm resultados que admiro.", "Consigo replicar métodos ou atitudes que funcionam para outros.", "Observo meus pensamentos limitantes e consigo mudá-los.", "Eu crio estratégias para incorporar novas habilidades com rapidez."],
    "Gestão da Narrativa e Mindset": ["Minha voz interna me incentiva a seguir motivado.", "Percebo quando estou com pensamentos punitivos e ressignifico.", "Converso internamente comigo com respeito e firmeza.", "Eu consigo silenciar pensamentos sabotadores quando necessário.", "Tenho consciência de como meu diálogo interno afeta minhas ações."],
    "Arquitetura de Sistemas de Crenças": ["Acredito que sou capaz de aprender e evoluir constantemente.", "Percebo quando estou agindo a partir de crenças limitantes.", "Sei que posso mudar minhas realidades ao mudar minhas crenças.", "Tenho crenças fortalecedoras sobre minha capacidade de liderar.", "Identifico de onde vêm algumas das minhas crenças centrais."],
    "Padrão de Entrega e Excelência": ["Eu me esforço SEMPRE para entregar o meu máximo.", "Eu percebo evolução na qualidade das minhas ações e entregas.", "Mantenho comprometimento mesmo sob pressão.", "Tenho clareza dos meus pontos fortes e pontos de melhoria.", "Eu me cobro para entregar além do básico quando acredito."],
    "Padrão de Protagonismo": ["Eu assumo responsabilidade pelas minhas escolhas.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que está sob meu controle.", "Encaro desafios como oportunidades.", "Olho para mim antes de culpar o ambiente."]
}

if st.session_state.etapa == 'questoes':
    for dim, perguntas in dimensoes_info.items():
        with st.expander(f"✨ AVALIAR: {dim.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"{p}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"q_{p}", label_visibility="collapsed")
    
    if st.button("FINALIZAR DIAGNÓSTICO"):
        if all(st.session_state.get(f"q_{p}") is not None for dim in dimensoes_info.values() for p in dim):
            st.session_state.notas = {dim: sum(st.session_state.get(f"q_{p}") for p in perguntas) for dim, perguntas in dimensoes_info.items()}
            st.session_state.total = sum(st.session_state.notas.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ Responda todas as questões para prosseguir.")

elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 MAPA PRONTO!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail Estratégico")
            whatsapp = st.text_input("WhatsApp")
            cargo = st.text_input("Empresa e Cargo")
            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    # FIX: CALCULA TUDO ANTES DE QUALQUER ERRO (MATA O NAMEERROR)
                    total = st.session_state.total
                    if total <= 122: z, c, tx = "ZONA DE SOBREVIVÊNCIA", "🔴", "Sua pontuação indica Zona de Risco. Assuma o controle!"
                    elif total <= 200: z, c, tx = "ZONA DE OSCILAÇÃO", "🟠", "Você possui as competências, mas está preso no ciclo de oscilação."
                    else: z, c, tx = "ZONA DE ELITE", "🌟", "Parabéns! Performance de elite."
                    
                    st.session_state.res_zona, st.session_state.res_cor, st.session_state.res_txt = z, c, tx

                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        nova = {"Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "Nome": nome, "Email": email, "WhatsApp": whatsapp, "Cargo": cargo, "Pontuacao_Total": total, "Zona": z}
                        conn.create(data=[nova])
                    except: pass
                    
                    with st.spinner('Gerando Mapa...'): time.sleep(10)
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos.")

elif st.session_state.etapa == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>SEU MAPA ESTRATÉGICO DE PERFORMANCE</h2>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(st.session_state.notas.values()) + [list(st.session_state.notas.values())[0]], theta=list(st.session_state.notas.keys()) + [list(st.session_state.notas.keys())[0]], fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37', width=6)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=650)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{st.session_state.res_cor} STATUS: {st.session_state.res_zona}</h2><p style='margin-top:15px; font-size: 20px;'>{st.session_state.res_txt}</p></div>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO ESTRATÉGICO", "https://wa.me/5581986245870")
