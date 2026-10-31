import pandas as pd
import streamlit as st

from motor_inferencia import BASE_CONHECIMENTO, TRILHAS, recomendar


st.set_page_config(
    page_title="Consultor de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
)


ESCALA = BASE_CONHECIMENTO["metadados"]["escala_likert"]
ROTULOS_ESCALA = {
    int(chave): valor for chave, valor in ESCALA["rotulos"].items()
}


def inicializar_estado() -> None:
    st.session_state.setdefault("etapa", 1)
    st.session_state.setdefault("perfil", {})
    st.session_state.setdefault("afinidades", {})
    st.session_state.setdefault("conhecimentos", {})
    st.session_state.setdefault("respostas", {})
    st.session_state.setdefault("resultado", None)


def avancar(etapa: int) -> None:
    st.session_state["etapa"] = etapa
    st.rerun()


def renderizar_navegacao() -> None:
    nomes = {1: "Perfil", 2: "Afinidades e conhecimento", 3: "Objetivos", 4: "Resultado"}
    etapa_atual = st.session_state["etapa"]
    st.progress(min(etapa_atual, 4) / 4, text=" → ".join(
        f"{'✓ ' if numero < etapa_atual else ''}{nome}"
        for numero, nome in nomes.items()
    ))


def rotulo_likert(valor: int) -> str:
    return f"{valor} — {ROTULOS_ESCALA[valor]}"


def renderizar_pergunta(pergunta: dict, valor_atual: int) -> int:
    return st.select_slider(
        pergunta["titulo"],
        options=list(range(ESCALA["minimo"], ESCALA["maximo"] + 1)),
        value=valor_atual,
        format_func=rotulo_likert,
        key=f"afinidade_{pergunta['id']}",
    )


def renderizar_etapa_perfil() -> None:
    st.header("Passo 1 — Perfil pessoal")
    st.write("Essas informações ajudam a contextualizar o diagnóstico e o plano de estudo.")
    perfil = st.session_state["perfil"]
    with st.form("form_perfil"):
        nome = st.text_input("Nome", value=perfil.get("nome", ""))
        nivel = st.selectbox(
            "Como você descreve seu nível atual em tecnologia?",
            ["Iniciante", "Básico", "Intermediário"],
            index=["iniciante", "basico", "intermediario"].index(perfil.get("nivel", "iniciante")),
        )
        tempo = st.select_slider(
            "Quanto tempo por semana você pode dedicar aos estudos?",
            options=[2, 4, 6, 8, 10, 12, 15],
            value=perfil.get("tempo_semanal", 4),
            format_func=lambda horas: f"{horas} horas",
        )
        continuar = st.form_submit_button("Continuar", type="primary", use_container_width=True)

    if continuar:
        st.session_state["perfil"] = {
            "nome": nome.strip(),
            "nivel": nivel.lower(),
            "tempo_semanal": tempo,
        }
        avancar(2)


def renderizar_etapa_afinidades() -> None:
    st.header("Passo 2 — Afinidades e conhecimento atual")
    st.write("Use a escala de 1 a 5. Não há resposta certa: o objetivo é representar seu momento atual.")
    afinidades = st.session_state["afinidades"]
    conhecimentos = st.session_state["conhecimentos"]

    with st.form("form_afinidades"):
        st.subheader("Afinidades")
        novas_afinidades = {}
        for pergunta in BASE_CONHECIMENTO["perguntas"]:
            novas_afinidades[pergunta["id"]] = renderizar_pergunta(
                pergunta, afinidades.get(pergunta["id"], 3)
            )

        st.subheader("Autopercepção de conhecimentos")
        st.caption("A avaliação será comparada ao conjunto de competências esperado para uma vaga Júnior.")
        novos_conhecimentos = {}
        for conhecimento in BASE_CONHECIMENTO["conhecimentos"]:
            novos_conhecimentos[conhecimento["id"]] = st.select_slider(
                conhecimento["nome"],
                options=list(range(ESCALA["minimo"], ESCALA["maximo"] + 1)),
                value=conhecimentos.get(conhecimento["id"], 1),
                format_func=rotulo_likert,
                help=conhecimento["descricao"],
                key=f"conhecimento_{conhecimento['id']}",
            )

        col_voltar, col_continuar = st.columns(2)
        voltar = col_voltar.form_submit_button("Voltar")
        continuar = col_continuar.form_submit_button("Continuar", type="primary")

    if voltar:
        st.session_state["afinidades"] = novas_afinidades
        st.session_state["conhecimentos"] = novos_conhecimentos
        avancar(1)
    if continuar:
        st.session_state["afinidades"] = novas_afinidades
        st.session_state["conhecimentos"] = novos_conhecimentos
        avancar(3)


def renderizar_etapa_objetivos() -> None:
    st.header("Passo 3 — Objetivos de carreira")
    st.write("Escolha o resultado profissional que mais gostaria de construir neste momento.")
    objetivos = BASE_CONHECIMENTO["objetivos"]
    ids_objetivos = [objetivo["id"] for objetivo in objetivos]
    nomes_objetivos = {objetivo["id"]: objetivo["nome"] for objetivo in objetivos}
    objetivo_atual = st.session_state["respostas"].get("objetivo", ids_objetivos[0])

    with st.form("form_objetivos"):
        objetivo = st.radio(
            "Qual é seu principal objetivo?",
            ids_objetivos,
            index=ids_objetivos.index(objetivo_atual),
            format_func=lambda identificador: nomes_objetivos[identificador],
        )
        col_voltar, col_finalizar = st.columns(2)
        voltar = col_voltar.form_submit_button("Voltar")
        finalizar = col_finalizar.form_submit_button("Gerar diagnóstico", type="primary")

    if voltar:
        avancar(2)
    if finalizar:
        respostas = dict(st.session_state["afinidades"])
        respostas["objetivo"] = objetivo
        respostas["conhecimentos"] = dict(st.session_state["conhecimentos"])
        st.session_state["respostas"] = respostas
        st.session_state["resultado"] = recomendar(respostas)
        avancar(4)


def renderizar_gaps(resultado: dict) -> None:
    st.subheader("Lacunas para o nível Júnior")
    if not resultado["gaps"]:
        st.success("Sua autopercepção já alcança o nível esperado nas competências avaliadas.")
        return

    gaps = pd.DataFrame(
        [
            {
                "Competência": gap["competencia"],
                "Nível atual": gap["nivel_atual"],
                "Nível esperado": gap["nivel_esperado"],
                "Tecnologias sugeridas": ", ".join(gap["tecnologias"]),
            }
            for gap in resultado["gaps"]
        ]
    )
    st.dataframe(gaps, hide_index=True, use_container_width=True)


def renderizar_roadmap(resultado: dict) -> None:
    roadmap = resultado["roadmap"]
    st.subheader("Roadmap de desenvolvimento")
    if roadmap["tecnologias_prioritarias"]:
        st.write("**Tecnologias prioritárias:** " + ", ".join(roadmap["tecnologias_prioritarias"]))
    for etapa in roadmap["etapas"]:
        with st.expander(f"Etapa {etapa['ordem']} — {etapa['titulo']}", expanded=etapa["ordem"] == 1):
            st.write("**Estudar:** " + ", ".join(etapa["tecnologias"]))
            st.write("**Entrega:** " + etapa["entrega"])

    col_cert, col_portfolio = st.columns(2)
    with col_cert:
        st.write("**Certificações para considerar**")
        for certificacao in roadmap["certificacoes"]:
            st.markdown(f"- {certificacao}")
    with col_portfolio:
        st.write("**Projeto para o portfólio**")
        st.write(roadmap["projeto_portfolio"])


def renderizar_resultado() -> None:
    resultado = st.session_state["resultado"]
    if not resultado:
        avancar(1)
        return

    st.header("Diagnóstico de carreira")
    nome = st.session_state["perfil"].get("nome")
    if nome:
        st.write(f"Perfil analisado: **{nome}**")

    trilha_plano_atual = st.session_state["respostas"].get("trilha_escolhida", resultado["chave"])
    trilha_plano = st.selectbox(
        "Trilha para detalhar o plano de ação",
        list(TRILHAS),
        index=list(TRILHAS).index(trilha_plano_atual),
        format_func=lambda chave: TRILHAS[chave],
    )
    if trilha_plano != trilha_plano_atual and st.button("Atualizar gaps e roadmap"):
        respostas = dict(st.session_state["respostas"])
        respostas["trilha_escolhida"] = trilha_plano
        st.session_state["respostas"] = respostas
        st.session_state["resultado"] = recomendar(respostas)
        st.rerun()

    st.success(f"Trilha mais compatível: {resultado['trilha']} — {resultado['compatibilidade']:.1f}%")
    st.subheader("Top 3 de compatibilidade")
    top3 = pd.DataFrame(
        [
            {"Posição": item["posicao"], "Trilha": item["nome"], "Compatibilidade (%)": item["compatibilidade"]}
            for item in resultado["top3"]
        ]
    )
    st.dataframe(top3, hide_index=True, use_container_width=True)

    ranking = pd.DataFrame(
        [{"Trilha": item["nome"], "Compatibilidade (%)": item["compatibilidade"]} for item in resultado["ranking"]]
    ).set_index("Trilha")
    st.bar_chart(ranking)

    st.subheader("Justificativa da recomendação")
    for motivo in resultado["justificativas"]:
        st.markdown(f"- {motivo}")

    renderizar_gaps(resultado)
    renderizar_roadmap(resultado)

    col_novo, col_reiniciar = st.columns(2)
    if col_novo.button("Refazer a análise", use_container_width=True):
        st.session_state["resultado"] = None
        avancar(1)
    col_reiniciar.caption(
        f"{resultado['regras_acionadas']} regra(s) acionada(s)"
        + (f" e {len(resultado['penalidades_aplicadas'])} penalidade(s) aplicada(s)." if resultado["penalidades_aplicadas"] else ".")
    )


inicializar_estado()
st.title("Consultor Inteligente de Carreiras em TI")
st.caption("Sistema especialista baseado em regras, pontuação ponderada e análise de competências.")
renderizar_navegacao()

if st.session_state["etapa"] == 1:
    renderizar_etapa_perfil()
elif st.session_state["etapa"] == 2:
    renderizar_etapa_afinidades()
elif st.session_state["etapa"] == 3:
    renderizar_etapa_objetivos()
else:
    renderizar_resultado()
