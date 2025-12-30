import streamlit as st
import plotly.graph_objects as go
import time

# 1. ENGENHARIA VISUAL LIDERUM (MÁXIMO IMPACTO)
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: linear-gradient(180deg, #001f3f 0%, #000c1a 100%); color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; font-size: 40px !important; }
    
    /* CARD CENTRALIZADO */
    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(212, 175, 55, 0.3) !important; border-radius: 15px !important; padding: 40px !important; }
    
    /* BOTÃO DOURADO VISÍVEL */
    .stButton>button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 5px 20px rgba(212, 175, 55, 0.5) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .question-text { font-size: 20px !important; color: #FFFFFF !important; margin-top: 25px; text-shadow: 1px 1px 2px black; }
    div[data-testid="stRadio"] label p { color: #FFFFFF !important; font-size: 22px !important; font-weight: 700 !important; }
    div[role="radiogroup"] label { background: rgba(255, 255, 255, 0.1) !important; padding: 12px 25px !important; border-radius: 8px; margin-right: 15px; }
    .zone-card { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 10px; border-left: 10px solid #D4AF37; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='100'></div>", unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# 2. DIMENSÕES E PERGUNTAS (45 ITENS)
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
                st.radio(f"Nota para {p}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=p)
    
    if st.button("FINALIZAR E PROCESSAR DIAGNÓSTICO"):
        # VERIFICAÇÃO RIGOROSA
        todas_respondidas = True
        for dim, perguntas in dimensoes_info.items():
            for p in perguntas:
                if st.session_state.get(p) is None:
                    todas_respondidas = False
                    break
        
        if todas_respondidas:
            notas_finais = {dim: sum(st.session_state.get(p) for p in perguntas) for dim, perguntas in dimensoes_info.items()}
            st.session_state.notas = notas_finais
            st.session_state.total = sum(notas_finais.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ O Protocolo exige 100% de preenchimento para garantir a precisão científica do seu laudo.")

elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 SEU MAPA ESTÁ PRONTO!</h3>", unsafe_allow_html=True)
        st.write("Insira seus dados para liberar o acesso ao Gráfico de Governança:")
        with st.form("leads"):
            st.text_input("Nome Completo", key="form_nome")
            st.text_input("E-mail Estratégico", key="form_email")
            st.text_input("WhatsApp (DDD)", key="form_whatsapp")
            st.text_input("Empresa e Cargo", key="form_cargo")
            if st.form_submit_button("LIBERAR MEU RESULTADO AGORA"):
                if all([st.session_state.form_nome, st.session_state.form_email, st.session_state.form_whatsapp, st.session_state.form_cargo]):
                    with st.spinner('Analisando correlações... Gerando Mapa de Governança...'):
                        time.sleep(3) # O suspense que gera valor
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Preencha todos os campos para prosseguir.")

elif st.session_state.etapa == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>MAPA DE GOVERNANÇA PESSOAL</h2>", unsafe_allow_html=True)
    
    # 3. GRÁFICO "GLOW UP" COM CORES DINÂMICAS
    categories = list(st.session_state.notas.keys())
    values = list(st.session_state.notas.values())
    
    # Define a cor baseada na performance total
    total = st.session_state.total
    if total <= 122: color_hex, glow = '#CD7F32', 'rgba(205, 127, 50, 0.4)' # Bronze
    elif total <= 200: color_hex, glow = '#D4AF37', 'rgba(212, 175, 55, 0.4)' # Ouro
    else: color_hex, glow = '#FFD700', 'rgba(255, 215, 0, 0.6)' # Ouro Brilhante

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], theta=categories + [categories[0]],
        fill='toself', fillcolor=glow,
        line=dict(color=color_hex, width=4),
        marker=dict(size=10, color='white', line=dict(color=color_hex, width=2))
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(tickfont=dict(size=13, color="white", family="Montserrat"))
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=650
    )
    st.plotly_chart(fig, use_container_width=True)

    # TEXTOS DE ZONA (Conforme sua revisão)
    if total <= 122:
        status, cor_emoji, texto = "ZONA DE SOBREVIVÊNCIA", "🔴", "Sua pontuação indica Zona de Risco. Mas isso é comum até em líderes experientes. Está pronto para crescer exponencialmente? Assuma o controle! O laudo detalhado (R$ 47) traz o plano de ação prático."
    elif total <= 200:
        status, cor_emoji, texto = "ZONA DE OSCILAÇÃO", "🟠", "Você possui as competências, mas está preso no ciclo de oscilação. O peso operacional trava seu salto. Identifique as dimensões que são seu 'freio de mão invisível' com nosso laudo completo e plano de ação."
    else:
        status, cor_emoji, texto = "ZONA DE ELITE", "🌟", "Parabéns! Performance muito acima do mercado. Mas autoliderança exige manutenção constante. O laudo premium revela micro-oportunidades de expansão para você nunca oscilar."

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{cor_emoji} {status}</h2><p style='margin-top:15px; font-size: 18px;'>{texto}</p></div>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO ESTRATÉGICO", "https://wa.me/5581986245870")
