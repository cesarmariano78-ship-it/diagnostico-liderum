# ---------------------------------------
# ETAPA 0: INTRO (100% CENTRALIZADA)
# ---------------------------------------
if st.session_state.etapa == "intro":
    col_c = st.columns([1, 2.2, 1])[1]
    with col_c:
        st.markdown("<div class='card intro-center'>", unsafe_allow_html=True)

        st.markdown(
            "<h1 style='text-align:center; margin: 0 0 6px 0;'>PROTOCOLO LIDERUM</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h3 style='text-align:center; margin: 0 0 14px 0;'>Diagnóstico de Governança Pessoal</h3>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <p style="text-align:center; margin-top: 0;">
        Descubra, em poucos minutos, onde sua autoliderança está sólida —<br/>
        e onde ela está quebrando sua constância, foco e execução.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        # CTA principal (CENTRALIZADO)
        cta1_l, cta1_c, cta1_r = st.columns([1, 2, 1])
        with cta1_c:
            if st.button("Iniciar diagnóstico gratuito", key="cta_intro_top"):
                if not st.session_state.submission_id:
                    st.session_state.submission_id = str(uuid.uuid4())
                _send_event("diagnostico_iniciado", etapa="intro")
                st.session_state.etapa = "questoes"
                st.rerun()

        st.markdown("<p class='small' style='text-align:center;'>Leva de 6 a 8 minutos.</p>", unsafe_allow_html=True)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(212,175,55,0.18);'/>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Antes de começar</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Este diagnóstico não é um teste psicológico, nem um julgamento sobre quem você é.<br/>
        Ele foi criado para ajudar você a observar com mais clareza como está hoje a sua forma de conduzir
        decisões, emoções, comportamento e direção.
        </p>
        <p style="text-align:center; font-weight: 800;">
        Aqui não se mede intenção. Mede-se consistência.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Por que isso importa</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Muitas pessoas são competentes, estudam, se esforçam —<br/>
        mas os resultados oscilam porque a forma de se governar é instável.
        </p>
        <p style="text-align:center;">
        Este diagnóstico existe para revelar exatamente isso.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin: 0 0 10px 0;'>Privacidade e sigilo</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;">
        Suas respostas são confidenciais e usadas exclusivamente para gerar seu diagnóstico e direcionamento personalizado.<br/>
        Nenhuma informação será compartilhada.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='divider-brasil'></div>", unsafe_allow_html=True)

        # CTA final (CENTRALIZADO) — voltou ao “miolo”
        cta2_l, cta2_c, cta2_r = st.columns([1, 2, 1])
        with cta2_c:
            if st.button("Iniciar diagnóstico gratuito", key="cta_intro_bottom"):
                if not st.session_state.submission_id:
                    st.session_state.submission_id = str(uuid.uuid4())
                _send_event("diagnostico_iniciado", etapa="intro")
                st.session_state.etapa = "questoes"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
