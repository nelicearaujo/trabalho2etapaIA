# Matriz de decisão

Esta matriz resume a organização da base de conhecimento. Os pesos, textos das justificativas e recomendações completas estão em `regras_carreiras.json`.

## Regras de compatibilidade gradual

As regras `A01` a `A30` usam respostas de 1 a 5. Uma condição com `minimo` só é atendida quando a resposta alcança o limite; o fator aplicado à regra é proporcional à intensidade da resposta.

| Grupo | Trilha | Evidências consideradas |
|---|---|---|
| A01–A03 | Back-end | lógica, programação, bancos de dados e objetivo de desenvolvimento |
| A04–A06 | Front-end/UI/UX | design, experiência do usuário, qualidade e desenvolvimento |
| A07–A09 | Ciência de Dados | matemática, dados, programação e objetivo de dados |
| A10–A12 | Engenharia de Dados | dados, bancos, infraestrutura e objetivo de dados |
| A13–A15 | Cibersegurança | segurança, infraestrutura, lógica e objetivo de segurança |
| A16–A18 | DevOps/SRE | automação, infraestrutura, cloud e objetivo de infraestrutura |
| A19–A21 | Cloud Architecture | cloud, infraestrutura, lógica e objetivo de infraestrutura |
| A22–A24 | Mobile | mobile, design, programação e objetivo de desenvolvimento |
| A25–A27 | QA | qualidade, lógica, programação e objetivo de qualidade |
| A28–A30 | Product Management | produto, comunicação, gestão e objetivo de produto |

## Regras de compatibilidade categórica

As regras `R01` a `R30` preservam as combinações categóricas da primeira versão do sistema. Elas também são carregadas do JSON e permitem executar os testes anteriores sem misturar conhecimento ao código.

| Grupo | Trilha | Combinações principais |
|---|---|---|
| R01–R03 | Back-end | lógica/funcionalidades, Python/algoritmos, bancos/regras de negócio |
| R04–R06 | Front-end/UI/UX | interfaces/produto, JavaScript/visual, criatividade/experiência |
| R07–R09 | Ciência de Dados | matemática/estatística, Python/modelos, matemática/insights |
| R10–R12 | Engenharia de Dados | pipelines/dados, SQL/integração, sistemas/infraestrutura de dados |
| R13–R15 | Cibersegurança | segurança/proteção, Linux/vulnerabilidades, investigação/sistemas seguros |
| R16–R18 | DevOps/SRE | automação/entrega contínua, Linux/infraautomação, sistemas/disponibilidade |
| R19–R21 | Cloud Architecture | cloud/infraestrutura, cloud/escalabilidade, sistemas/infraestrutura |
| R22–R24 | Mobile | aplicativos/produto, JavaScript/aplicativos, criatividade/aplicativo |
| R25–R27 | QA | testes/qualidade, testes/investigação, detalhismo/confiabilidade |
| R28–R30 | Product Management | priorização/valor, comunicação/colaboração, gestão/valor |

## Penalidades

As regras `P01` a `P05` reduzem a pontuação quando há conflito entre afinidades. Exemplos: baixa programação associada a forte interesse visual reduz Back-end; baixa automação associada a forte infraestrutura reduz DevOps; baixa comunicação associada a forte interesse em produto reduz Product Management.

## Cálculo

Para cada regra atendida:

```text
pontuação da regra = peso × fator da condição 1 × fator da condição 2 × ...
```

A compatibilidade é calculada por trilha:

```text
compatibilidade (%) = pontuação final ÷ peso máximo aplicável × 100
```

O resultado é limitado ao intervalo de 0% a 100%, ordenado e usado para selecionar o Top 3. Em caso de empate, o número de evidências acionadas é usado como critério de desempate.
