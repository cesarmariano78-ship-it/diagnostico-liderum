import streamlit as st
import plotly.graph_objects as go

# 1. ESTÉTICA METÁLICA LIDERUM
st.set_page_config(page_title="Protocolo LIDERUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: linear-gradient(180deg, #001f3f 0%, #000c1a 100%); color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
    h1 { color: #D4AF37 !important; font-family: 'Playfair Display', serif !important; text-align: center; }
    
    /* ESTILO DOS BOTÕES (CORREÇÃO DE VISIBILIDADE) */
    .stButton>button {
        background: linear-gradient(180deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001226 !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4) !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Estilo do Card Centralizado */
    .stForm { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(212, 175, 55, 0.3) !important; border-radius: 15px !important; padding: 30px !important; }
    
    .question-text { font-size: 19px !important; color: #FFFFFF !important; margin-top: 20px; }
    
    /* Estilo dos Números 1-5 */
    div[data-testid="stRadio"] label p { color: #FFFFFF !important; font-size: 20px !important; font-weight: 700 !important; }
    div[role="radiogroup"] label { background: rgba(255, 255, 255, 0.1) !important; padding: 10px 20px !important; border-radius: 5px; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'etapa' not in st.session_state: st.session_state.etapa = 'questoes'

st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='100'></div>", unsafe_allow_html=True)
st.title("PROTOCOLO DE GOVERNANÇA PESSOAL LIDERUM")

# DIMENSÕES E PERGUNTAS
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
        with st.expander(f"📌 AVALIAR: {dim.upper()}"):
            soma = 0
            for p in perguntas:
                st.markdown(f"<p class='question-text'>{p}</p>", unsafe_allow_html=True)
                # AJUSTE: index=None faz com que nada venha marcado por padrão
                n = st.radio(f"Nota para {p}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=p)
                soma += n if n is not None else 0
            respostas[dim] = soma if all(st.session_state.get(pg) is not None for pg in perguntas) else None
    
    if st.button("FINALIZAR E GERAR DIAGNÓSTICO"):
        # VERIFICAÇÃO SE TODAS FORAM RESPONDIDAS
        todas_respondidas = True
        for dim, perguntas in dimensoes_info.items():
            for p in perguntas:
                if st.session_state.get(p) is None:
                    todas_respondidas = False
                    break
        
        if todas_respondidas:
            # Calcula as notas finais se tudo estiver ok
            notas_finais = {}
            for dim, perguntas in dimensoes_info.items():
                notas_finais[dim] = sum(st.session_state.get(p) for p in perguntas)
            
            st.session_state.notas = notas_finais
            st.session_state.total = sum(notas_finais.values())
            st.session_state.etapa = 'captura'
            st.rerun()
        else:
            st.error("⚠️ Atenção: Para um diagnóstico preciso, você precisa responder todas as questões antes de finalizar.")

elif st.session_state.etapa == 'captura':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🔒 SEU RESULTADO ESTÁ PRONTO!</h3>", unsafe_allow_html=True)
        with st.form("leads"):
            nome = st.text_input("Nome Completo", placeholder="Como deseja ser chamado?")
            email = st.text_input("E-mail Profissional", placeholder="Seu melhor e-mail")
            whatsapp = st.text_input("WhatsApp (com DDD)", placeholder="(00) 00000-0000")
            cargo = st.text_input("Empresa e Cargo", placeholder="Ex: Diretor na Indústria X")
            if st.form_submit_button("LIBERAR MEU DIAGNÓSTICO"):
                if nome and email and whatsapp and cargo:
                    st.session_state.etapa = 'resultado'
                    st.rerun()
                else:
                    st.warning("Por favor, preencha todos os campos para liberar seu gráfico.")

elif st.session_state.etapa == 'resultado':
    categories = list(st.session_state.notas.keys())
    values = list(st.session_state.notas.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25], color="white", gridcolor="rgba(255,255,255,0.2)")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550, font=dict(color="white", size=11))
    st.plotly_chart(fig, use_container_width=True)

    total = st.session_state.total
    if total <= 122:
        zona, cor = "ZONA DE SOBREVIVÊNCIA", "🔴"
        texto = f"Sua pontuação de {total}/225 indica que você está operando em Zona de Risco..."
    elif total <= 200:
        zona, cor = "ZONA DE OSCILAÇÃO", "🟠"
        texto = f"Sua pontuação de {total}/225 revela que você possui as competências necessárias, mas está preso em um ciclo de oscilação..."
    else:
        zona, cor = "ZONA DE ELITE", "🌟"
        texto = f"Parabéns! Sua pontuação de {total}/225 coloca você em um patamar muito acima da média..."

    st.markdown(f"<div class='zone-card'><h2 style='color: #D4AF37; margin:0;'>{cor} STATUS: {zona}</h2><p style='margin-top:15px; font-size: 18px;'>{texto}</p></div>", unsafe_allow_html=True)
    st.link_button("💎 SOLICITAR ACESSO AO LAUDO ESTRATÉGICO", "https://wa.me/5581986245870")
