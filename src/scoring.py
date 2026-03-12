# src/scoring.py
from __future__ import annotations

from typing import List, Tuple

def calcular_zona(total: int) -> str:
    if total > 200:
        return "ELITE"
    if total > 122:
        return "OSCILAÇÃO"
    return "SOBREVIVÊNCIA"

def calcular_scores_e_total(respostas_45: List[int]) -> Tuple[List[int], int]:
    # 9 dimensões, 5 perguntas cada
    scores = [sum(respostas_45[i:i+5]) for i in range(0, 45, 5)]
    total = sum(scores)
    return scores, total

