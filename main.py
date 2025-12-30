import streamlit as st
import plotly.graph_objects as go

# 1. ESTÉTICA METÁLICA LIDERUM
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: linear-gradient(180deg, #001f3f 0%, #000c1a 100%); color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; }
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; }
    div[data-testid="stRadio"] label p { color: #FFFFFF !important; font-size: 20px !important; font-weight: 700 !important; }
    div[role="radiogroup"] label { background: rgba(255, 255, 255, 0.1) !important; padding: 10px 20px !important; border-radius: 5px; margin-right: 10px; }
    .stButton>button { background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%); color: #001f3f; font-weight: 700; font-size: 22px; width: 100%; height: 3.5em; border: none; box-shadow: 0px 5px 20px rgba(212, 175, 55, 0.4); }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 5px; border-left: 8px solid #D4AF37; margin-bottom: 20px; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# GESTÃO DE ESTADO
if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='100'></div>", unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# DIMENSÕES E PERGUNTAS (45 ITENS)
dimensoes_info = {
    "Visão e Alinhamento Estratégico": ["Eu tenho clareza sobre meus objetivos nos próximos meses.", "Meus objetivos pessoais e profissionais estão anotados e organizados.", "Eu consigo manter meu foco mesmo diante de distrações externas.", "Eu revisito minha visão de futuro com frequência para me orientar.", "Eu organizo minhas prioridades com base no que é realmente importante."],
    "Recompensa e Reforço Positivo": ["Eu reconheço minhas próprias conquistas, mesmo que pequenas.", "Eu costumo comemorar quando concluo uma etapa de um projeto.", "Eu me elogio por atitudes positivas que tomo no dia a dia.", "Eu consigo sentir orgulho do meu progresso, mesmo que não seja perfeito.", "Eu crio momentos intencionais para celebrar avanços."],
    "Análise e Consciência de Padrões": ["Eu costumo revisar meu comportamento com espírito crítico construtivo.", "Reconheço quando errei e busco aprender com isso.", "Consigo perceber meus padrões de sabotagem ou repetição de erros.", "Eu me permito ajustar rotas sem culpa quando percebo que errei.", "Busco feedbacks com abertura para rever minhas atitudes."],
    "Governança e Disciplina Operacional": ["Eu consigo planejar minha rotina de forma organizada e funcional.", "Eu priorizo o que é mais importante al invés de apenas o urgente.", "Mantenho constância mesmo quando não estou motivado.", "Sou capaz de equilibrar tarefas operacionais e estratégicas.", "Tenho sistemas ou hábitos que sustentam minha produtividade."],
    "Modelagem e Expansão de Repertório": ["Eu tenho consciência de comportamentos que preciso mudar.", "Busco aprender com pessoas que têm resultados que admiro.", "Consigo replicar métodos ou atitudes que funcionam para outros.", "Observo meus pensamentos limitantes e consigo mudá-los.", "Eu crio estratégias para incorporar novas habilidades com rapidez."],
    "Gestão da Narrativa e Mindset": ["Minha voz interna me incentiva a seguir motivado.", "Percebo quando estou com pensamentos punitivos e ressignifico.", "Converso internamente comigo com respeito e firmeza.", "Eu consigo silenciar pensamentos sabotadores quando necessário.", "Tenho consciência de como meu diálogo interno afeta minhas ações."],
    "Arquitetura de Sistemas de Crenças": ["Acredito que sou capaz de aprender e evoluir constantemente.", "Percebo quando estou agindo a partir de crenças limitantes.", "Sei que posso mudar minhas realidades ao mudar minhas crenças.", "Tenho crenças fortalecedoras sobre minha capacidade de liderar.", "Identifico de onde vêm algumas das minhas crenças centrais."],
    "Padrão de Entrega e Excelência": ["Eu me esforço SEMPRE para entregar o meu máximo.", "Eu percebo evolução na qualidade das minhas ações e entregas.", "Mantenho comprometimento mesmo sob pressão.", "Tenho clareza dos meus pontos fortes e pontos de melhoria.", "Eu me cobro para entregar além do básico quando acredito."],
    "Postura Ativa e Protagonismo": ["Eu assumo responsabilidade pelas minhas escolhas e resultados.", "Evito colocar culpa em fatores externos.", "Ajo com rapidez para mudar o que está sob meu controle.", "Encaro desafios como oportunidades de crescimento.", "Costumo olhar para mim antes de culpar o ambiente."]
}

if st.session_state.etapa == 'questoes':
    respostas = {}
    for dim, perguntas in dimensoes_info.items():
        with st.expander(f"📌 AVALIAR: {dim.upper()}"):
            soma = 0
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                n = st.radio(f"Nota para {p}", [1, 2, 3, 4, 5], index=2, horizontal=True, key=p)
                soma += n
            respostas[dim] = soma
    
    if st.button("FINALIZAR E GERAR DIAGNÓSTICO"):
        st.session_state.notas = respostas
        st.session_state.total = sum(respostas.values())
        st.session_state.etapa = 'captura'
        st.rerun()

elif st.session_state.etapa == 'captura':
    st.markdown("### 🔒 SEU RESULTADO ESTÁ PRONTO!")
    st.write("Identificamos oscilações importantes em suas dimensões de performance. Preencha seus dados para visualizar seu Gráfico de Governança:")
    with st.form("leads"):
        st.text_input("Nome Completo", key="nome")
        st.text_input("E-mail Profissional", key="email")
        st.text_input("WhatsApp (DDD)", key="whatsapp")
        st.text_input("Empresa e Cargo", key="cargo")
        if st.form_submit_button("LIBERAR DIAGNÓSTICO"):
            st.session_state.etapa = 'resultado'
            st.rerun()

elif st.session_state.etapa == 'resultado':
    categories = list(st.session_state.notas.keys())
    values = list(st.session_state.notas.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.2)")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500, font=dict(color="white", size=11))
    st.plotly_chart(fig, use_container_width=True)

    total = st.session_state.total
    if total <= 122:
        zona, cor = "ZONA DE SOBREVIVÊNCIA", "🔴"
        texto = "Sua pontuação indica que você está operando em Zona de Risco. Mas, para te tranquilizar, quero dizer que isso é mais comum do que você imagina, até mesmo em líderes experientes. Você está pronto para ajustar alguns pontos e crescer de forma exponencial? Assuma o controle! Se você quiser ter acesso ao laudo detalhado por apenas R$ 47, você receberá uma estrutura completa que traz consciência e um plano de ação com ferramentas e exercícios práticos para desenvolver as áreas que estão te atrapalhando."
    elif total <= 200:
        zona, cor = "ZONA DE OSCILAÇÃO", "🟠"
        texto = "Você sente que está quase lá, mas o peso operacional te trava. Adquira o nosso laudo completo e receba o diagnóstico profundo, onde você vai entender melhor quais dimensões estão sendo o seu freio de mão invisível. Além disso, você receberá o plano de ação com ferramentas práticas para você decolar e prosperar em seus resultados."
    else:
        zona, cor = "ZONA DE ELITE", "🌟"
        texto = "Parabéns! Você está performando muito acima do mercado. Porém, eu sei (e você sabe) que a autoliderança é algo que deve estar em constante desenvolvimento. Para você que já está performando em alto nível, ao adquirir o nosso laudo premium, você vai receber uma estrutura de diagnóstico detalhada e profunda para entender como age em cada uma das áreas, além de ferramentas para dar manutenção e expansão naquelas que precisam de maior cuidado ou que são o seu maior gargalo hoje."

    st.markdown(f"""
    <div class='zone-card'>
        <h2 style='color: #D4AF37; margin:0;'>{cor} STATUS: {zona}</h2>
        <p style='margin-top:15px; font-size: 18px;'>{texto}</p>
        <p style='font-style: italic; color: #B8860B; margin-top:10px;'>Pontuação de Governança: {total}/225</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>DESEJA O LAUDO COMPLETO E O PLANO DE AÇÃO?</h3>", unsafe_allow_html=True)
    st.link_button("💎 ADQUIRIR LAUDO COMPLETO LIDERUM", "https://wa.me/5581986245870")
