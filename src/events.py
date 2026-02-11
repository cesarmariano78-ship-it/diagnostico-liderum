# src/events.py
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

import requests
import streamlit as st

from src.config import APP_VERSION, get_webhook_url

def _now_utc_iso() -> str:
    return datetime.datetime.utcnow().isoformat()

def flush_pending_events(timeout: float = 2.0) -> None:
    """
    Tenta reenviar eventos pendentes (best-effort).
    Não bloqueia UX. Falha silenciosa.
    """
    url = get_webhook_url()
    if not url:
        return

    pending = st.session_state.get("pending_events", [])
    if not pending:
        return

    still_pending = []
    for payload in pending:
        try:
            requests.post(url, json=payload, timeout=timeout)
        except Exception:
            still_pending.append(payload)

    st.session_state.pending_events = still_pending

def send_event(event_name: str, etapa: str = "", meta: Optional[Dict[str, Any]] = None, timeout: float = 2.0) -> None:
    """
    Tracking mínimo, dedupe por (event_name + submission_id).
    Se falhar, entra em pending_events.
    """
    try:
        submission_id = st.session_state.submission_id or ""
        dedupe_key = f"{event_name}:{submission_id}"
        if dedupe_key in st.session_state.sent_events:
            return

        payload: Dict[str, Any] = {
            "type": "event",
            "event_name": event_name,
            "timestamp": _now_utc_iso(),
            "submission_id": submission_id,
            "app_version": APP_VERSION,
            "etapa": etapa,
        }
        if meta:
            payload["meta"] = meta

        url = get_webhook_url()
        if not url:
            # sem webhook configurado -> marca como enviado para não spammar
            st.session_state.sent_events.add(dedupe_key)
            return

        try:
            requests.post(url, json=payload, timeout=timeout)
            st.session_state.sent_events.add(dedupe_key)
        except Exception:
            # fila local (não trava navegação)
            st.session_state.pending_events.append(payload)
    except Exception:
        pass

def send_submission(payload: Dict[str, Any], timeout: float = 6.0) -> bool:
    """
    Envia submissão completa (lead + respostas).
    Retorna True se o webhook respondeu OK/200.
    """
    url = get_webhook_url()
    if not url:
        return False

    try:
        r = requests.post(url, json=payload, timeout=timeout)
        if r is not None and getattr(r, "status_code", 0) == 200:
            txt = (r.text or "").strip().upper()
            return "OK" in txt
    except Exception:
        pass
    return False

