import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. ARQUITETURA VISUAL DE ALTO PADRÃO
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: linear-gradient(180deg, #001f3f 0%, #000c1a 100%); color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; font-size: 38px !important; }
    
    /* FORMULÁRIO CENTRALIZADO ESTILO CARD */
    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(212, 175, 55, 0.4) !important; border-radius: 15px !important; padding: 40px !important; }
    label[data-testid="stWidgetLabel"] p { color: #FFFFFF !important; font-weight: 700 !important; font-size: 16px !important; }

    /* BOTÃO DOURADO */
    .stButton>button, div.stFormSubmitButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important; font-weight: 700 !important; font-size: 18px !important;
        width: 100% !important; border: none !important; padding: 15px !important;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.5) !important; text-transform: uppercase;
    }

    .question-text { font-size: 20px !important; color: #FFFFFF !important; margin-top: 30px; }
    div[role="radiogroup"] label { background: rgba(255, 255, 255, 0.1) !important; padding: 12px 25px !important; border-radius: 8px; margin-right: 15px; border: 1px solid rgba(212, 175, 55, 0.2); }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 10px; border-left: 10px solid #D4AF37; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='80'></div>", unsafe_allow_html=True)
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
    "Postura Ativa e Protagonismo": ["Eu assumo responsabilidade pelas minhas escolhas e resultados.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que está sob meu controle.", "Encaro desafios como oportunidades de crescimento.", "Costumo olhar para mim antes de culpar o ambiente."]
}

if st.session_state.etapa == 'questoes':
    respostas = {}
    for dim, perguntas in dimensoes_info.items():
        with st.expander(f"✨ AVALIAR: {dim.upper()}"):
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                st.radio(f"{p}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=p, label_visibility="collapsed")
    
    if st.button("FINALIZAR E PROCESSAR DIAGNÓSTICO"):
        if all(st.session_state.get(p) is not None for dim in dimensoes_info.values() for p in dim):
            st.session_state.notas = {dim: sum(st.session_state.get(p) for p in perguntas) for dim, perguntas in dimensoes_info.items()}
            st.session_state.total = sum(st.session_state.notas.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ O Protocolo exige 100% de preenchimento para garantir a precisão do laudo.")

elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 MAPA DE GOVERNANÇA DISPONÍVEL!</h3>", unsafe_allow_html=True)
        with st.form("lead_form"):
            nome = st.text_input("Nome Completo", key="l_nome")
            email = st.text_input("E-mail Estratégico", key="l_email")
            whatsapp = st.text_input("WhatsApp com DDD", key="l_whatsapp")
            cargo = st.text_input("Empresa e Cargo", key="l_cargo")
            if st.form_submit_button("LIBERAR MEU RESULTADO"):
                if all([nome, email, whatsapp, cargo]):
                    # --- SALVAMENTO NA PLANILHA ---
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        zona_lead = "Elite" if st.session_state.total > 200 else "Oscilação" if st.session_state.total > 122 else "Sobrevivência"
                        nova_linha = {
                            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Nome": nome, "Email": email, "WhatsApp": whatsapp, "Cargo": cargo,
                            "Pontuacao_Total": st.session_state.total, "Zona": zona_lead
                        }
                        conn.create(data=[nova_linha])
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}") # Debug se falhar
                    
                    place = st.empty()
                    msgs = ["Calibrando dimensões...", "Cruzando 45 pontos de dados...", "Identificando padrões de sabotagem...", "Sincronizando modelos de autoliderança...", "Finalizando seu Mapa de Governança..."]
                    for m in msgs:
                        place.info(f"⏳ {m}")
                        time.sleep(2)
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos para prosseguir.")

elif st.session_state.etapa == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>SEU MAPA ESTRATÉGICO DE PERFORMANCE</h2>", unsafe_allow_html=True)
    categories = list(st.session_state.notas.keys())
    values = list(st.session_state.notas.values())
    total = st.session_state.total
    color_hex = '#FFD700' if total > 200 else '#D4AF37' if total > 122 else '#CD7F32'
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color=color_hex, width=5), marker=dict(size=12, color='white', line=dict(color=color_hex, width=2))))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.1)"), angularaxis=dict(tickfont=dict(size=14, color="white"))), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=650)
    st.plotly_chart(fig, use_container_width=True)

    if total <= 122:
        status, cor, txt = "ZONA DE SOBREVIVÊNCIA", "🔴", "Sua pontuação indica Zona de Risco. Mas isso é comum até em líderes experientes. Está pronto para crescer exponencialmente? Assuma o controle! Ao solicitar seu laudo completo, você terá acesso à estrutura detalhada que traz consciência e um plano de ação com ferramentas práticas."
    elif total <= 200:
        status, cor, txt = "ZONA DE OSCILAÇÃO", "🟠", "Você possui as competências necessárias, mas está preso em um ciclo de oscilação. Você sente que 'está quase lá', mas o peso operacional constante trava seu próximo salto. Para prosperar de forma sustentável, você precisa identificar quais são as dimensões que estão agindo como seu 'freio de mão invisível'. Ao adquirir nosso laudo completo, você recebe o diagnóstico profundo e o Plano de Ação Estratégico."
    else:
        status, cor, txt = "ZONA DE ELITE", "🌟", "Parabéns! Sua pontuação coloca você em um patamar muito acima do mercado. Porém, a autoliderança em alto nível exige manutenção constante para não se tornar complacente. Para você que já performa no topo, nosso Laudo Premium oferece a estrutura de Diagnóstico de Detalhe, revelando as micro-oportunidades de expansão."

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{cor} STATUS: {zona}</h2><p style='margin-top:15px; font-size: 19px;'>{txt}</p></div>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO ESTRATÉGICO", "https://wa.me/5581986245870")
