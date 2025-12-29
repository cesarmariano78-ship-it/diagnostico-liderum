import streamlit as st
import plotly.graph_objects as go

# 1. ESTÉTICA DE ALTA PERFORMANCE (CSS PERSONALIZADO)
st.set_page_config(page_title="LIDERUM - Diagnóstico de Autoliderança", layout="wide")

st.markdown("""
    <style>
    /* Fundo Azul Marinho Metálico */
    .stApp { background-color: #001f3f; color: white; }
    
    /* Estilização de Títulos em Dourado */
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Playfair Display', serif; text-align: center; }
    
    /* Cards de Pergunta */
    .stSelectSlider label { color: #FFFFFF !important; font-size: 16px !important; font-weight: 500; }
    
    /* Botão de Ação LIDERUM */
    .stButton>button { 
        background-color: #D4AF37; 
        color: #001f3f; 
        border-radius: 5px; 
        font-weight: bold; 
        font-size: 22px;
        border: none;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f1c40f; color: #000; transform: translateY(-2px); }
    
    /* Feedback Boxes */
    .feedback-card { 
        background-color: rgba(255, 255, 255, 0.05); 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 6px solid #D4AF37; 
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 DIAGNÓSTICO DE AUTOLIDERANÇA LIDERUM")
st.markdown("<p style='text-align: center; font-size: 18px;'>Mapeie sua Governança Pessoal em 9 Dimensões Estratégicas</p>", unsafe_allow_html=True)
st.write("---")

# 2. BASE DE DADOS: 9 DIMENSÕES E 45 PERGUNTAS (DO SEU DOC)
dados_diagnostico = {
    "Direção": ["Eu tenho clareza sobre meus objetivos nos próximos meses.", "Meus objetivos pessoais e profissionais estão anotados e organizados.", "Eu consigo manter meu foco mesmo diante de distrações externas.", "Eu revisito minha visão de futuro com frequência para me orientar.", "Eu organizo minhas prioridades com base no que é realmente importante."],
    "Celebração": ["Eu reconheço minhas próprias conquistas, mesmo que pequenas.", "Eu costumo comemorar quando concluo uma etapa de um projeto.", "Eu me elogio por atitudes positivas que tomo no dia a dia.", "Eu consigo sentir orgulho do meu progresso, mesmo que não seja perfeito.", "Eu crio momentos intencionais para celebrar avanços."],
    "Autocrítica": ["Eu costumo revisar meu comportamento com espírito crítico construtivo.", "Reconheço quando errei e busco aprender com isso.", "Consigo perceber meus padrões de sabotagem ou repetição de erros.", "Eu me permito ajustar rotas sem culpa quando percebo que errei.", "Busco feedbacks com abertura para rever minhas atitudes."],
    "Autogestão Estratégica": ["Eu consigo planejar minha rotina de forma organizada e funcional.", "Eu priorizo o que é mais importante ao invés de apenas o urgente.", "Mantenho constância mesmo quando não estou motivado.", "Sou capaz de equilibrar tarefas operacionais e estratégicas.", "Tenho sistemas ou hábitos que sustentam minha produtividade."],
    "Aprendizado Acelerado": ["Eu tenho consciência de comportamentos que preciso mudar.", "Busco aprender com pessoas que têm resultados que admiro.", "Consigo replicar métodos ou atitudes que funcionam para outros.", "Observo meus pensamentos limitantes e consigo mudá-los.", "Eu crio estratégias para incorporar novas habilidades com rapidez."],
    "Diálogo Interno": ["Minha voz interna me incentiva a seguir motivado.", "Percebo quando estou com pensamentos punitivos e ressignifico.", "Converso internamente comigo com respeito e firmeza.", "Eu consigo silenciar pensamentos sabotadores quando necessário.", "Tenho consciência de como meu diálogo interno afeta minhas ações."],
    "Crenças": ["Acredito que sou capaz de aprender e evoluir constantemente.", "Percebo quando estou agindo a partir de crenças limitantes.", "Sei que posso mudar minhas realidades ao mudar minhas crenças.", "Tenho crenças fortalecedoras sobre minha capacidade de liderar.", "Identifico de onde vêm algumas das minhas crenças centrais."],
    "Autoperformance": ["Eu me esforço SEMPRE para entregar o meu máximo.", "Eu percebo evolução na qualidade das minhas ações e entregas.", "Mantenho comprometimento mesmo sob pressão.", "Tenho clareza dos meus pontos fortes e pontos de melhoria.", "Eu me cobro para entregar além do básico quando acredito."],
    "Autorresponsabilidade": ["Eu assumo responsabilidade pelas minhas escolhas e resultados.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que está sob meu controle.", "Encaro desafios como oportunidades de crescimento.", "Costumo olhar para mim antes de culpar o ambiente."]
}

# 3. COLETA DE RESPOSTAS
respostas_totais = {}

st.info("Responda com honestidade: 1 (Nunca) a 5 (Sempre)")

for dim, perguntas in dados_diagnostico.items():
    with st.expander(f"📍 {dim.upper()}"):
        soma_dimensao = 0
        for p in perguntas:
            nota = st.select_slider(p, options=[1, 2, 3, 4, 5], value=3, key=p)
            soma_dimensao += nota
        respostas_totais[dim] = soma_dimensao

st.write("---")

# 4. PROCESSAMENTO E EXIBIÇÃO
if st.button("ANALISAR MINHA PERFORMANCE"):
    # Gráfico de Radar em Dourado
    categories = list(respostas_totais.keys())
    values = list(respostas_totais.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        line_color='#D4AF37',
        fillcolor='rgba(212, 175, 55, 0.4)'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.2)")),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Devolutivas Dinâmicas
    st.header("📋 Relatório de Governança Pessoal")
    
    for dim, total in respostas_totais.items():
        if total <= 10: status = "CRÍTICO"; cor = "#e74c3c"
        elif total <= 17: status = "ALERTA"; cor = "#e67e22"
        elif total <= 22: status = "EFICIENTE"; cor = "#2ecc71"
        else: status = "ELITE"; cor = "#f1c40f"
        
        st.markdown(f"""
            <div class="feedback-card">
                <h3 style="text-align: left; margin: 0; font-size: 20px;">{dim}: {total}/25</h3>
                <p style="color: {cor}; font-weight: bold; margin-bottom: 5px;">NÍVEL {status}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.success("Diagnóstico concluído. Clique no botão abaixo para sua sessão estratégica.")
    st.link_button("💎 AGENDAR CONSULTORIA DE ALTA PERFORMANCE", "https://wa.me/SEUNUMERO")
