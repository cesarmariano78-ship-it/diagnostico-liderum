# src/laudo.py
from __future__ import annotations

def texto_laudo(zona: str, nome: str, total: int) -> str:
    if zona == "OSCILAÇÃO":
        return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

Direcionamento Estratégico
Zona de Governança: OSCILAÇÃO

{nome}, seu padrão atual é de Oscilação.

Isso significa que você alterna entre períodos de boa entrega e momentos de queda, perda de foco ou desaceleração — mesmo tendo capacidade e repertório.

Na prática, o problema não está na sua competência, mas na instabilidade da sua autogestão e da regulação cognitiva, o que impacta diretamente:

- constância de execução
- clareza de prioridade
- ritmo operacional

O efeito mais comum desse padrão é simples:
você até sabe o que fazer, mas não sustenta o mesmo nível de ação por tempo suficiente para gerar resultados consistentes.

O objetivo aqui não é motivar.
É estabilizar sua forma de se governar, para que a execução deixe de depender de emoção, contexto ou “fase boa”.

⚠️ O ponto de atenção

Quando a Oscilação não é tratada, ela costuma gerar:

- muitos recomeços e pouca continuidade
- decisões instáveis ou adiadas
- desgaste mental desnecessário
- sensação de esforço alto com retorno irregular

Seu gráfico mostra tendências.
O que ainda falta é clareza prática sobre onde intervir primeiro.
""".strip()

    if zona == "ELITE":
        return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

Direcionamento Estratégico
Zona de Governança: ELITE

{nome}, seus resultados indicam que você está na Zona de Elite.

Isso significa que sua governança pessoal já opera em um nível elevado.
Você apresenta clareza, capacidade de execução e autonomia para conduzir sua vida com consistência acima da média.

O principal ponto de atenção nessa zona não é capacidade, nem esforço.
É a manutenção do nível ao longo do tempo.

Pessoas na Zona de Elite costumam executar bem, tomar boas decisões e sustentar resultados — mas podem operar no automático, deixando de revisar fundamentos essenciais como:

- clareza contínua
- rotina funcional
- autorresponsabilidade ativa

Aqui, o trabalho não é corrigir falhas evidentes.
É refinar decisões, proteger o essencial e elevar a precisão da execução, para que o desempenho não dependa de contexto, fase ou excesso de carga.

O objetivo agora é claro:
blindar constância, reduzir desgaste e transformar competência em impacto sustentado.
""".strip()

    # SOBREVIVÊNCIA
    return f"""PROTOCOLO LIDERUM

Análise Individual: {nome}

Pontuação Total: {total} / 225
Zona de Governança: {zona}

Direcionamento Estratégico
Zona de Governança: SOBREVIVÊNCIA

{nome}, você está na Zona de Sobrevivência.

Isso indica que sua governança pessoal está operando no limite.
Energia, clareza, rotina e disciplina entraram em modo reativo, fazendo com que você funcione mais para apagar incêndios do que para construir avanço real.

Nesse estado, a vida passa a ser conduzida por urgências, demandas externas e cansaço acumulado.
Decisões deixam de ser estratégicas e passam a ser defensivas.

Normalmente, esse padrão aparece quando autogestão, clareza e regulação cognitiva estão fragilizadas ao mesmo tempo, gerando:

- baixa previsibilidade
- dificuldade de priorização
- execução inconsistente
- desgaste emocional elevado

Aqui, não é hora de fazer mais.
É hora de estancar perda de energia, reorganizar o essencial e recuperar capacidade mínima de condução.

O objetivo inicial na Zona de Sobrevivência é simples e vital:
parar o colapso, restaurar estabilidade básica e criar espaço interno para decisões melhores.

Sem isso, qualquer tentativa de evolução vira mais peso — e não solução.
""".strip()

