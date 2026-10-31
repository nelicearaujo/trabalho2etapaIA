"""Motor de inferência ponderada do consultor de carreiras.

As perguntas, regras, pesos e recomendações ficam em regras_carreiras.json.
Este módulo apenas interpreta a base de conhecimento e aplica as respostas do
perfil a ela.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


ARQUIVO_REGRAS = Path(__file__).with_name("regras_carreiras.json")


def carregar_base_conhecimento(caminho: Path = ARQUIVO_REGRAS) -> Dict[str, Any]:
    """Carrega e valida minimamente a base de conhecimento externa."""
    with caminho.open(encoding="utf-8") as arquivo:
        base = json.load(arquivo)

    campos_obrigatorios = ("trilhas", "regras", "penalidades", "perguntas")
    ausentes = [campo for campo in campos_obrigatorios if campo not in base]
    if ausentes:
        raise ValueError("Base de conhecimento incompleta: " + ", ".join(ausentes))
    return base


BASE_CONHECIMENTO = carregar_base_conhecimento()
TRILHAS = {
    chave: dados["nome"] for chave, dados in BASE_CONHECIMENTO["trilhas"].items()
}


def _valor_numerico(valor: Any) -> Optional[float]:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _fator_condicao(condicao: Dict[str, Any], respostas: Dict[str, Any]) -> Optional[float]:
    """Retorna a intensidade de uma condição ou None quando ela não foi atendida."""
    campo = condicao["campo"]
    if campo not in respostas:
        return None

    valor = respostas[campo]
    if "valor" in condicao and valor != condicao["valor"]:
        return None
    if "valores" in condicao and valor not in condicao["valores"]:
        return None

    minimo = condicao.get("minimo")
    maximo = condicao.get("maximo")
    if minimo is None and maximo is None:
        return 1.0

    numero = _valor_numerico(valor)
    if numero is None:
        return None
    if minimo is not None and numero < minimo:
        return None
    if maximo is not None and numero > maximo:
        return None

    escala = BASE_CONHECIMENTO["metadados"]["escala_likert"]
    limite = float(escala["maximo"])
    return min(max(numero / limite, 0.0), 1.0)


def _avaliar_regra(regra: Dict[str, Any], respostas: Dict[str, Any]) -> Optional[float]:
    fatores = [
        _fator_condicao(condicao, respostas)
        for condicao in regra["condicoes"]
    ]
    if any(fator is None for fator in fatores):
        return None

    resultado = 1.0
    for fator in fatores:
        resultado *= fator
    return regra["peso"] * resultado


def _respostas_para_motor(respostas: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza respostas novas e mantém o formato categórico da primeira etapa."""
    normalizadas = dict(respostas)
    normalizadas.setdefault("objetivo", "desenvolvimento")
    return normalizadas


def _peso_maximo(trilha: str, respostas: Dict[str, Any]) -> float:
    """Calcula o denominador somente com regras aplicáveis ao formato recebido."""
    peso = 0.0
    for regra in BASE_CONHECIMENTO["regras"]:
        if regra["trilha"] != trilha:
            continue
        if all(condicao["campo"] in respostas for condicao in regra["condicoes"]):
            peso += regra["peso"]
    return peso


def _ranking(pontuacoes: Dict[str, float], justificativas: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    ordenado = sorted(
        pontuacoes.items(),
        key=lambda item: (item[1], len(justificativas[item[0]]), TRILHAS[item[0]]),
        reverse=True,
    )
    return [
        {"posicao": posicao, "chave": chave, "nome": TRILHAS[chave], "pontos": round(pontos, 2)}
        for posicao, (chave, pontos) in enumerate(ordenado, start=1)
    ]


def analisar_gaps(trilha: str, conhecimentos: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Identifica competências abaixo do nível esperado para uma posição Júnior."""
    conhecimentos = conhecimentos or {}
    gaps = []
    for competencia in BASE_CONHECIMENTO["trilhas"][trilha]["competencias_junior"]:
        atual = _valor_numerico(conhecimentos.get(competencia["dominio"], 1)) or 1.0
        esperado = competencia["nivel_junior"]
        if atual < esperado:
            gaps.append(
                {
                    "id": competencia["id"],
                    "competencia": competencia["nome"],
                    "dominio": competencia["dominio"],
                    "nivel_atual": int(atual),
                    "nivel_esperado": esperado,
                    "lacuna": round(esperado - atual, 1),
                    "tecnologias": competencia["tecnologias"],
                    "descricao": "Elevar este conhecimento até o nível esperado para uma primeira oportunidade Júnior.",
                }
            )
    return gaps


def gerar_roadmap(trilha: str, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Prioriza o roadmap pelos gaps e retorna certificações e projeto de portfólio."""
    dados = BASE_CONHECIMENTO["trilhas"][trilha]
    tecnologias_prioritarias = []
    for gap in gaps:
        for tecnologia in gap["tecnologias"]:
            if tecnologia not in tecnologias_prioritarias:
                tecnologias_prioritarias.append(tecnologia)

    return {
        "tecnologias_prioritarias": tecnologias_prioritarias,
        "etapas": sorted(dados["roadmap"], key=lambda etapa: etapa["ordem"]),
        "certificacoes": dados["certificacoes"],
        "projeto_portfolio": dados["projeto_portfolio"],
    }


def recomendar(respostas: Dict[str, Any]) -> Dict[str, Any]:
    """Processa um perfil e retorna compatibilidade, gaps e plano de ação."""
    respostas_motor = _respostas_para_motor(respostas)
    pontuacoes = {chave: 0.0 for chave in TRILHAS}
    justificativas = {chave: [] for chave in TRILHAS}
    regras_acionadas = []

    for regra in BASE_CONHECIMENTO["regras"]:
        pontos = _avaliar_regra(regra, respostas_motor)
        if pontos is not None:
            pontuacoes[regra["trilha"]] += pontos
            justificativas[regra["trilha"]].append(regra["justificativa"])
            regras_acionadas.append(regra["id"])

    if not regras_acionadas:
        for regra in BASE_CONHECIMENTO.get("afinidades", []):
            pontos = _avaliar_regra(regra, respostas_motor)
            if pontos is not None:
                pontuacoes[regra["trilha"]] += pontos
                justificativas[regra["trilha"]].append(regra["justificativa"])
                regras_acionadas.append(regra["id"])

    penalidades_aplicadas = []
    for penalidade in BASE_CONHECIMENTO["penalidades"]:
        pontos = _avaliar_regra(penalidade, respostas_motor)
        if pontos is not None:
            trilha = penalidade["trilha"]
            pontuacoes[trilha] = max(0.0, pontuacoes[trilha] - pontos)
            justificativas[trilha].append("Atenuação: " + penalidade["justificativa"])
            penalidades_aplicadas.append(penalidade["id"])

    ranking_pontos = _ranking(pontuacoes, justificativas)
    ranking = []
    for item in ranking_pontos:
        maximo = _peso_maximo(item["chave"], respostas_motor)
        compatibilidade = (item["pontos"] / maximo * 100) if maximo else 0.0
        ranking.append(dict(item, compatibilidade=round(min(compatibilidade, 100.0), 1)))

    ranking.sort(key=lambda item: (item["compatibilidade"], item["pontos"], -item["posicao"]), reverse=True)
    for posicao, item in enumerate(ranking, start=1):
        item["posicao"] = posicao

    principal = ranking[0]
    trilha_plano = respostas.get("trilha_escolhida", principal["chave"])
    gaps = analisar_gaps(trilha_plano, respostas.get("conhecimentos"))
    roadmap = gerar_roadmap(trilha_plano, gaps)
    motivos = justificativas[principal["chave"]]
    if not motivos:
        motivos = ["Nenhuma regra específica foi acionada; a compatibilidade pode ser refinada com mais informações."]

    return {
        "chave": principal["chave"],
        "trilha": principal["nome"],
        "pontuacao": principal["pontos"],
        "compatibilidade": principal["compatibilidade"],
        "justificativas": motivos,
        "ranking": ranking,
        "top3": ranking[:3],
        "alternativas": ranking[1:3],
        "regras_acionadas": len(regras_acionadas),
        "ids_regras_acionadas": regras_acionadas,
        "penalidades_aplicadas": penalidades_aplicadas,
        "gaps": gaps,
        "roadmap": roadmap,
    }
