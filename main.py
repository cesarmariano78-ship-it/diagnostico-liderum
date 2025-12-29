import streamlit as st
import plotly.graph_objects as go

# 1. ENGENHARIA VISUAL: AZUL METÁLICO E FONTES DE ELITE
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&family=Playfair+Display:wght@700&display=swap');

    /* Fundo Metálico Azul */
    .stApp {
        background: linear-gradient(135deg, #001226 0%, #001f3f 50%, #001226 100%);
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    /* Títulos em Dourado com Fonte Serifada */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Playfair Display', serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Estilização dos Seletores (Sliders) */
    .stSelectSlider label { color: #D4AF37 !important; font-weight: 600 !important; }
    
    /* Botão de Alta Performance */
    .stButton>button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
        color: #001f3f;
        border: none;
        border-radius: 4px;
        font-weight: 700;
        font-size: 20px;
        padding: 15px;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.5); }

    /* Cards de Devolutiva Refinados */
    .feedback-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 25px;
        border-radius: 2px;
        border-left: 8px solid #D4AF37;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ESPAÇO PARA LOGO (Substitua a URL abaixo pela sua logo)
st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='100'></div>", unsafe_allow_html=True)

st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")
st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 20px; letter-spacing: 2px;'>Mapeamento de Alta Performance em 9 Dimensões</p>", unsafe_allow_html=True)
st.write("---")

# 2. DIMENSÕES E PERGUNTAS (45 ITENS COM NOMES ESTRATÉGICOS)
dimensoes_premium = {
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

respostas = {}

for dim, perguntas in dimensoes_premium.items():
    with st.expander(f"▼ {dim.upper()}"):
        soma = 0
        for p in perguntas:
            n = st.select_slider(p, options=[1, 2, 3, 4, 5], value=3, key=p)
            soma += n
        respostas[dim] = soma

st.write("---")

if st.button("PROCESSAR RESULTADOS ESTRATÉGICOS"):
    # Gráfico de Radar Dourado Metálico
    categories = list(respostas.keys())
    values = list(respostas.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(212,175,55,0.2)")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=11))
    st.plotly_chart(fig, use_container_width=True)

    st.header("RELATÓRIO DE GOVERNANÇA")
    for dim, score in respostas.items():
        if score <= 10: status, cor = "CRÍTICO", "🔴"
        elif score <= 17: status, cor = "ALERTA", "🟠"
        elif score <= 22: status, cor = "EFICIENTE", "🟢"
        else: status, cor = "ELITE", "🌟"
        
        st.markdown(f"""
            <div class="feedback-card">
                <h3 style="text-align: left; margin: 0;">{cor} {dim}: {score}/25</h3>
                <p style="color: {cor}; font-weight: 700;">NÍVEL ATUAL: {status}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Agende seu Debriefing com o Expert</h3>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR SESSÃO ESTRATÉGICA", "https://wa.me/SEUNUMERO")
