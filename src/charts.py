# src/charts.py
from __future__ import annotations

import plotly.graph_objects as go

def build_radar(scores: list[int], categorias: list[str]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categorias,
        fill="toself",
        fillcolor="rgba(212, 175, 55, 0.35)",
        line=dict(color="#D4AF37", width=4),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,12,26,1)",
            radialaxis=dict(
                visible=True,
                range=[0, 25],
                color="#888",
                gridcolor="rgba(212,175,55,0.1)",
            ),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        height=600,
        margin=dict(l=80, r=80, t=20, b=20),
        font=dict(color="white", size=16),
    )
    return fig

