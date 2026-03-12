from __future__ import annotations

import os
import streamlit as st

APP_VERSION = "mvp-0.1"

# Checkout Eduzz (base)
EDUZZ_CHECKOUT_BASE = "https://sun.eduzz.com/7977E15B9E"

def get_webhook_url() -> str:
    """
    Prioridade:
    1) st.secrets["URL_WEBHOOK"]
    2) env var URL_WEBHOOK
    """
    try:
        v = st.secrets.get("URL_WEBHOOK", "")
        if v:
            return v
    except Exception:
        pass
    return os.getenv("URL_WEBHOOK", "")
