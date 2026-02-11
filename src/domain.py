# src/domain.py
from __future__ import annotations

from typing import List, Tuple

Dimensao = Tuple[str, str, List[str]]

DIMENSOES: List[Dimensao] = [
    ("CLAREZA", "Capacidade de manter direção, prioridades e foco mesmo diante de pressão, excesso de demandas e ruído externo.", [
        "Mantenho clareza sobre o que é prioridade, mesmo quando surgem muitas demandas ao mesmo tempo.",
        "Meus objetivos de curto, médio e longo prazo estão claros e registrados, e planejo minhas ações com base neles.",
        "Mesmo pressionado ou cansado, continuo sabendo o que precisa ser feito primeiro.",
        "Consigo dizer “não” ao que não é prioridade sem me sentir culpado ou confuso.",
        "Sinto que minhas ações diárias estão alinhadas com a direção que quero para minha vida e carreira, na maior parte do tempo."
    ]),
    ("AUTOGESTÃO", "Capacidade de regular pensamentos, emoções e comportamentos sem depender de motivação externa.", [
        "Consigo manter meu comportamento alinhado ao que decidi, mesmo quando meu estado emocional oscila.",
        "Quando me sinto frustrado ou sobrecarregado, consigo me reorganizar sem perder totalmente o ritmo.",
        "Na maior parte do tempo, não dependo de motivação ou estímulos externos para cumprir o que é importante.",
        "Tenho consciência dos meus estados internos ao longo do dia e, na maioria das vezes, consigo agir assertivamente, independente do meu estado interno.",
        "Consigo retomar o controle rapidamente quando percebo que estou “saindo do eixo”."
    ]),
    ("PERCEPÇÃO CRÍTICA", "Capacidade de se observar, aprender com erros e ajustar rotas sem colapsar emocionalmente.", [
        "Consigo perceber quando meus padrões de comportamento precisam mudar, especialmente quando algo não funciona como eu esperava.",
        "Costumo olhar para meus erros com acolhimento, buscando aprendizado, sem me punir excessivamente.",
        "Consigo identificar rapidamente quando estou me sabotando.",
        "Aceito feedbacks sem entrar automaticamente em defesa.",
        "Uso meus erros como fonte de aprendizado, e não como motivo para me maltratar ou me castigar."
    ]),
    ("CELEBRAÇÃO", "Capacidade de reconhecer avanços, reforçar progresso e sustentar energia ao longo do processo.", [
        "Costumo comemorar pequenos avanços, mesmo quando parecem pouco significativos.",
        "Costumo celebrar pequenas conquistas sem perder o foco no próximo passo.",
        "Tenho o hábito de reconhecer meu próprio esforço e evolução.",
        "No dia a dia, costumo olhar mais para o que deu certo do que para os erros ou para o que falta.",
        "Celebrar meu progresso é um hábito comum e contribui para que eu me mantenha engajado e consistente ao longo do tempo."
    ]),
    ("APRENDIZADO ACELERADO", "Capacidade de aprender com rapidez, ajustar comportamento e evoluir a partir da experiência.", [
        "Aprendo com meus erros e ajusto meu comportamento sem repetir o mesmo padrão por muito tempo.",
        "Quando algo não está funcionando, busco novas formas de fazer, em vez de insistir no mesmo caminho.",
        "Aprendo observando pessoas mais experientes e aplico o que aprendo na prática.",
        "Testo novas abordagens mesmo correndo o risco de errar ou sair da zona de conforto.",
        "Mudo de opinião sem problemas, quando encontro uma ideia melhor que a minha"
    ]),
    ("REGULAÇÃO COGNITIVA (Self-Talk)", "Capacidade de regular pensamentos, interpretações e avaliações internas a serviço da ação.", [
        "Consigo perceber quando meus pensamentos começam a me atrapalhar ou me desorganizar.",
        "Quando algo dá errado, reorganizo meus pensamentos antes de tomar decisões impulsivas.",
        "Sou consciente dos meus pensamentos e eles me ajudam a agir, em vez de me paralisar ou desmotivar.",
        "Consigo questionar pensamentos negativos ou distorcidos, em vez de aceitá-los automaticamente.",
        "Mesmo em momentos difíceis, mantenho uma forma de pensar que sustenta ação e clareza."
    ]),
    ("AUTOIMAGEM (CRENÇAS)", "Conjunto de crenças que dirigem decisões e comportamento.", [
        "Sou capaz de aprender, me adaptar e melhorar continuamente.",
        "Tenho consciência de quando alguma crença limita minhas decisões ou ações.",
        "Costumo questionar minhas verdades para perceber quais delas não fazem mais sentido.",
        "Minha autoimagem me impulsiona à ação, não à paralisação.",
        "Acredito que vivo alinhado com a vida e os resultados que desejo construir."
    ]),
    ("AUTOPERFORMANCE", "Compromisso com evolução pessoal contínua e melhoria em relação a si mesmo.", [
        "Meço minha performance com base no meu próprio progresso, não em comparação com os outros.",
        "Tenho clareza sobre meus pontos fortes e sobre onde preciso evoluir.",
        "Sou comprometido em entregar o meu melhor dentro das condições que tenho.",
        "Sou meu principal ponto de referência para medir minha evolução, e observo quem está à frente com admiração, não com comparação negativa.",
        "Mesmo sob pressão, mantenho um padrão de qualidade nas minhas entregas."
    ]),
    ("AUTORRESPONSABILIDADE", "Capacidade de assumir escolhas, agir sobre o que controla e sair da posição de vítima.", [
        "Assumo responsabilidade pelas escolhas que faço, mesmo quando os resultados não são os esperados.",
        "Evito colocar a culpa em fatores externos quando algo não dá certo.",
        "Quando identifico um problema, foco no que posso fazer, e não no que não controlo.",
        "Costumo agir para mudar situações desconfortáveis em vez de reclamar delas.",
        "Reconheço que sou o principal responsável pelos meus resultados."
    ])
]

