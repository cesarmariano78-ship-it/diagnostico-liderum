import streamlit as st
import plotly.graph_objects as go

# 1. ENGENHARIA VISUAL: ALTO CONTRASTE E ESTÉTICA DE ELITE
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');

    /* Fundo Azul Metálico com Brilho */
    .stApp {
        background: linear-gradient(180deg, #001f3f 0%, #000c1a 100%);
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    /* Títulos em Dourado Serifado */
    h1 {
        color: #D4AF37 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 42px !important;
        text-shadow: 2px 4px 8px rgba(0,0,0,0.6);
        text-align: center;
    }

    /* Perguntas com Leitura de Elite */
    .question-text {
        font-size: 20px !important;
        font-weight: 500;
        color: #FFFFFF !important;
        margin-top: 25px;
        margin-bottom: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
    }

    /* --- CORREÇÃO DE VISIBILIDADE DOS NÚMEROS --- */
    /* Força o texto dos números a ser BRANCO PURO e visível */
    div[data-testid="stRadio"] label p {
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }

    /* Estiliza o container de cada número para destaque */
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 10px 25px !important;
        border-radius: 8px !important;
        margin-right: 15px !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        transition: 0.3s !important;
    }

    /* Cor do número quando SELECIONADO (Dourado Liderum) */
    div[role="radiogroup"] [data-checked="true"] {
        background: rgba(212, 175, 55, 0.5) !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Esconde o label técnico do Streamlit */
    label[data-testid="stWidgetLabel"] { display: none !important; }

    /* Botão Final de Comando */
    .stButton>button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%);
        color: #001f3f;
        border-radius: 4px;
        font-weight: 700;
        font-size: 24px;
        padding: 20px;
        width: 100%;
        border: none;
        box-shadow: 0px 5px 25px rgba(212, 175, 55, 0.5);
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# ESPAÇO PARA LOGO
st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='120'></div>", unsafe_allow_html=True)

st.markdown("<h1>PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 18px; letter-spacing: 3px;'>MAPEAMENTO DE PERFORMANCE EM 9 DIMENSÕES</p>", unsafe_allow_html=True)
st.write("---")

# 2. DIMENSÕES E PERGUNTAS (45 ITENS)
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
    with st.expander(f"✨ AVALIAR: {dim.upper()}"):
        soma = 0
        for p in perguntas:
            st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
            # Sistema de Escolha 1-5
            n = st.radio(f"Nota para {p}", [1, 2, 3, 4, 5], index=2, horizontal=True, key=p)
            soma += n
        respostas[dim] = soma

st.write("---")

if st.button("GERAR DIAGNÓSTICO DE PERFORMANCE"):
    st.balloons()
    
    categories = list(respostas.keys())
    values = list(respostas.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.2)")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<h3>SUA PERFORMANCE POR DIMENSÃO</h3>", unsafe_allow_html=True)
    for dim, score in respostas.items():
        cor = "🔴" if score <= 10 else "🟠" if score <= 17 else "🟢" if score <= 22 else "🌟"
        st.markdown(f"<div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #D4AF37;'><b>{cor} {dim}</b>: {score}/25</div>", unsafe_allow_html=True)

    # BOTÃO WHATSAPP FINAL
    st.link_button("💎 AGENDAR ANÁLISE COM O EXPERT", "https://wa.me/5581986245870")
