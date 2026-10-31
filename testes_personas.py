"""Testes do motor legado e do fluxo de pontuação gradual."""
from motor_inferencia import BASE_CONHECIMENTO, TRILHAS, recomendar

PERSONAS = [
    {
        "nome": "Perfil analítico / Ciência de Dados",
        "respostas": {
            "matematica": "alta",
            "atividade": "estatistica",
            "ferramenta": "python",
            "entrega": "insights",
            "estilo": "investigativo",
        },
        "esperado": "dados",
    },
    {
        "nome": "Perfil infraestrutura e segurança",
        "respostas": {
            "matematica": "media",
            "atividade": "seguranca",
            "ferramenta": "linux_redes",
            "entrega": "protecao",
            "estilo": "investigativo",
        },
        "esperado": "seguranca",
    },
    {
        "nome": "Perfil visual / Front-end",
        "respostas": {
            "matematica": "media",
            "atividade": "interfaces",
            "ferramenta": "javascript",
            "entrega": "produto_usuario",
            "estilo": "criativo",
        },
        "esperado": "frontend",
    },
    {
        "nome": "Perfil negócios / Produto",
        "respostas": {
            "matematica": "baixa",
            "atividade": "priorizacao",
            "ferramenta": "gestao",
            "entrega": "valor_negocio",
            "estilo": "colaborativo",
        },
        "esperado": "produto",
    },
    {
        "nome": "Perfil back-end / Bancos de dados",
        "respostas": {
            "matematica": "media",
            "atividade": "bancos",
            "ferramenta": "sql",
            "entrega": "regras_negocio",
            "estilo": "sistemas",
        },
        "esperado": "backend",
    },
    {
        "nome": "Perfil back-end / Algoritmos e Python",
        "respostas": {
            "matematica": "media",
            "atividade": "algoritmos",
            "ferramenta": "python",
            "entrega": "funcionalidades",
            "estilo": "sistemas",
        },
        "esperado": "backend",
    },
    {
        "nome": "Perfil front-end / Visual e JavaScript",
        "respostas": {
            "matematica": "media",
            "atividade": "visual",
            "ferramenta": "javascript",
            "entrega": "produto_usuario",
            "estilo": "criativo",
        },
        "esperado": "frontend",
    },
    {
        "nome": "Perfil UI/UX e Produto sem combinação exata",
        "respostas": {
            "matematica": "media",
            "atividade": "interfaces",
            "ferramenta": "gestao",
            "entrega": "confiabilidade",
            "estilo": "criativo",
        },
        "esperado": "frontend",
    },
    {
        "nome": "Perfil engenharia de dados",
        "respostas": {
            "matematica": "alta",
            "atividade": "pipelines",
            "ferramenta": "sql",
            "entrega": "dados_disponiveis",
            "estilo": "sistemas",
        },
        "esperado": "engenharia_dados",
    },
    {
        "nome": "Perfil DevOps / Automação",
        "respostas": {
            "matematica": "media",
            "atividade": "automacao",
            "ferramenta": "linux_redes",
            "entrega": "entrega_continua",
            "estilo": "sistemas",
        },
        "esperado": "devops",
    },
    {
        "nome": "Perfil cloud / Escalabilidade",
        "respostas": {
            "matematica": "media",
            "atividade": "escalabilidade",
            "ferramenta": "cloud",
            "entrega": "infraestrutura",
            "estilo": "sistemas",
        },
        "esperado": "cloud",
    },
    {
        "nome": "Perfil mobile / Aplicativos",
        "respostas": {
            "matematica": "baixa",
            "atividade": "aplicativos",
            "ferramenta": "javascript",
            "entrega": "aplicativo",
            "estilo": "criativo",
        },
        "esperado": "mobile",
    },
    {
        "nome": "Perfil QA / Qualidade",
        "respostas": {
            "matematica": "media",
            "atividade": "testes",
            "ferramenta": "testes",
            "entrega": "qualidade",
            "estilo": "detalhista",
        },
        "esperado": "qa",
    },
]


PERSONAS_GRADUAIS = [
    {
        "nome": "Perfil gradual de DevOps",
        "respostas": {
            "matematica": 3,
            "logica": 4,
            "programacao": 3,
            "design": 1,
            "experiencia_usuario": 2,
            "dados": 2,
            "banco_dados": 2,
            "infraestrutura": 5,
            "seguranca": 2,
            "automacao": 5,
            "cloud": 5,
            "mobile": 1,
            "qualidade": 3,
            "produto": 1,
            "comunicacao": 2,
            "gestao": 2,
            "objetivo": "infraestrutura",
            "conhecimentos": {"infraestrutura": 2, "automacao": 1, "cloud": 1},
        },
        "esperado": "devops",
    },
    {
        "nome": "Perfil gradual de dados",
        "respostas": {
            "matematica": 5,
            "logica": 3,
            "programacao": 3,
            "design": 2,
            "experiencia_usuario": 2,
            "dados": 5,
            "banco_dados": 3,
            "infraestrutura": 2,
            "seguranca": 1,
            "automacao": 2,
            "cloud": 2,
            "mobile": 1,
            "qualidade": 3,
            "produto": 2,
            "comunicacao": 2,
            "gestao": 2,
            "objetivo": "dados",
            "conhecimentos": {"programacao": 2, "dados": 1, "banco_dados": 2},
        },
        "esperado": "dados",
    },
]


def perfil_base(**alteracoes):
    respostas = {
        "matematica": "baixa",
        "atividade": "interfaces",
        "ferramenta": "nenhuma",
        "entrega": "confiabilidade",
        "estilo": "neutro",
    }
    respostas.update(alteracoes)
    return respostas


COMBINACOES_REGRAS = [
    ("R01", perfil_base(atividade="logica", entrega="funcionalidades"), "backend"),
    ("R02", perfil_base(atividade="algoritmos", ferramenta="python"), "backend"),
    ("R03", perfil_base(atividade="bancos", entrega="regras_negocio"), "backend"),
    ("R04", perfil_base(atividade="interfaces", entrega="produto_usuario"), "frontend"),
    ("R05", perfil_base(atividade="visual", ferramenta="javascript"), "frontend"),
    ("R06", perfil_base(atividade="experiencia_usuario", estilo="criativo"), "frontend"),
    ("R07", perfil_base(matematica="alta", atividade="estatistica"), "dados"),
    ("R08", perfil_base(atividade="modelos", ferramenta="python"), "dados"),
    ("R09", perfil_base(matematica="media", entrega="insights"), "dados"),
    ("R10", perfil_base(atividade="pipelines", entrega="dados_disponiveis"), "engenharia_dados"),
    ("R11", perfil_base(atividade="integracao_dados", ferramenta="sql"), "engenharia_dados"),
    ("R12", perfil_base(entrega="infraestrutura_dados", estilo="sistemas"), "engenharia_dados"),
    ("R13", perfil_base(atividade="seguranca", entrega="protecao"), "seguranca"),
    ("R14", perfil_base(atividade="vulnerabilidades", ferramenta="linux_redes"), "seguranca"),
    ("R15", perfil_base(entrega="sistemas_seguros", estilo="investigativo"), "seguranca"),
    ("R16", perfil_base(atividade="automacao", entrega="entrega_continua"), "devops"),
    ("R17", perfil_base(atividade="infra_automacao", ferramenta="linux_redes"), "devops"),
    ("R18", perfil_base(entrega="disponibilidade", estilo="sistemas"), "devops"),
    ("R19", perfil_base(atividade="cloud", entrega="infraestrutura"), "cloud"),
    ("R20", perfil_base(atividade="escalabilidade", ferramenta="cloud"), "cloud"),
    ("R21", perfil_base(entrega="infraestrutura", estilo="sistemas"), "cloud"),
    ("R22", perfil_base(atividade="aplicativos", entrega="produto_usuario"), "mobile"),
    ("R23", perfil_base(atividade="aplicativos", ferramenta="javascript"), "mobile"),
    ("R24", perfil_base(entrega="aplicativo", estilo="criativo"), "mobile"),
    ("R25", perfil_base(atividade="testes", entrega="qualidade"), "qa"),
    ("R26", perfil_base(atividade="investigar_erros", ferramenta="testes"), "qa"),
    ("R27", perfil_base(entrega="confiabilidade", estilo="detalhista"), "qa"),
    ("R28", perfil_base(atividade="priorizacao", entrega="valor_negocio"), "produto"),
    ("R29", perfil_base(atividade="comunicacao", estilo="colaborativo"), "produto"),
    ("R30", perfil_base(entrega="valor_negocio", ferramenta="gestao"), "produto"),
]


def executar_testes():
    aprovados = 0
    casos = [
        (persona["nome"], persona["respostas"], persona["esperado"])
        for persona in PERSONAS
    ]
    casos.extend(
        (persona["nome"], persona["respostas"], persona["esperado"])
        for persona in PERSONAS_GRADUAIS
    )
    casos.extend(
        (f"Combinação {regra}", respostas, esperado)
        for regra, respostas, esperado in COMBINACOES_REGRAS
    )

    for nome, respostas, esperado in casos:
        resultado = recomendar(respostas)
        passou = (
            resultado["chave"] == esperado
            and resultado["pontuacao"] > 0
            and resultado["regras_acionadas"] > 0
            and len(resultado["top3"]) == 3
            and all(0 <= item["compatibilidade"] <= 100 for item in resultado["ranking"])
        )
        status = "APROVADO" if passou else "FALHOU"
        print(f"{status}: {nome}")
        print(f"  Esperado: {esperado}")
        print(f"  Obtido:   {resultado['chave']} ({resultado['trilha']})")
        print(f"  Evidências: {resultado['pontuacao']} ponto(s), {resultado['regras_acionadas']} regra(s)")
        if passou:
            aprovados += 1

    print(f"\nResultado: {aprovados}/{len(casos)} casos aprovados.")
    if aprovados != len(casos):
        raise SystemExit(1)

    assert len(TRILHAS) == 10
    assert len(BASE_CONHECIMENTO["trilhas"]) == 10
    resultado = recomendar(PERSONAS_GRADUAIS[0]["respostas"])
    assert resultado["gaps"]
    assert resultado["roadmap"]["tecnologias_prioritarias"]
    assert resultado["roadmap"]["certificacoes"]
    print("Validações adicionais: Top 3, percentuais, gaps e roadmap aprovados.")


if __name__ == "__main__":
    executar_testes()
