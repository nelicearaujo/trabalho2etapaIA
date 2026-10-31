# Sistema Especialista para Carreiras em TI

Projeto da disciplina Inteligência Artificial do curso de Ciência da Computação.

**Instituição:** Centro Universitário Presidente Antônio Carlos — UNIPAC Barbacena<br>
**Professor:** Felipe Roncalli de Paula Carneiro<br>
**Data:** 22/10/2026<br>
**Nome:** ______________________________________________

## Objetivo

O sistema atua como um consultor de carreiras e desenvolvimento profissional. A partir de respostas graduais sobre afinidades, objetivos e conhecimentos atuais, ele:

- calcula a compatibilidade com dez trilhas de tecnologia;
- apresenta um Top 3 com percentuais de aderência;
- aplica penalidades a combinações conflitantes;
- identifica lacunas para o nível Júnior;
- sugere tecnologias, certificações e um projeto de portfólio.

As recomendações são orientativas e representam uma heurística acadêmica baseada nas regras cadastradas na base de conhecimento.

## Trilhas avaliadas

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Tecnologias

- Python 3.10 ou superior
- Streamlit
- Pandas
- JSON
- Git

O motor de inferência foi desenvolvido no próprio projeto com soma ponderada de atributos. Não há dependência de uma biblioteca externa de regras.

## Estrutura do projeto

```text
consultor-carreiras-ti/
├── app.py
├── motor_inferencia.py
├── regras_carreiras.json
├── testes_personas.py
├── matriz_decisao.md
├── requirements.txt
└── README.md
```

### Responsabilidade dos arquivos

- `regras_carreiras.json`: perguntas, objetivos, pesos, regras, penalidades, competências Júnior, roadmap, certificações e projetos.
- `motor_inferencia.py`: leitura da base, avaliação das condições, cálculo ponderado, ranking, gaps e plano de ação.
- `app.py`: interface Streamlit em etapas.
- `testes_personas.py`: testes das dez trilhas, regras legadas, perfis graduais e casos de compatibilidade.
- `matriz_decisao.md`: resumo das regras principais da base de conhecimento.

## Como executar

Crie um ambiente virtual e instale as dependências:

### macOS e Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Inicie a aplicação:

```bash
streamlit run app.py
```

## Fluxo da aplicação

### 1. Perfil pessoal

O usuário informa nome, nível atual e tempo semanal disponível para estudos.

### 2. Afinidades e conhecimento

As afinidades são respondidas em escala Likert de 1 a 5. A mesma escala registra a autopercepção em programação, dados, infraestrutura, segurança, cloud, design, mobile, qualidade e produto.

### 3. Objetivos

O usuário seleciona o resultado profissional que deseja priorizar: desenvolvimento, dados, infraestrutura, segurança, qualidade ou produto.

### 4. Diagnóstico

O motor avalia as condições da base externa, multiplica os pesos pela intensidade das respostas, subtrai penalidades quando necessário e normaliza a pontuação pelo peso máximo aplicável à trilha.

O resultado exibe o Top 3, um gráfico com as dez compatibilidades, justificativas, gaps para Júnior e o roadmap.

## Base de conhecimento

O arquivo `regras_carreiras.json` é carregado dinamicamente pelo motor. Cada regra possui:

```json
{
  "id": "A07",
  "trilha": "dados",
  "condicoes": [
    {"campo": "matematica", "minimo": 4},
    {"campo": "dados", "minimo": 4}
  ],
  "peso": 6,
  "justificativa": "Matemática e análise de dados são afinidades fortes para Ciência de Dados."
}
```

Condições com `valor` ou `valores` atendem respostas categóricas. Condições com `minimo` e `maximo` atendem respostas numéricas e recebem o fator proporcional da escala. As penalidades usam o mesmo formato e reduzem a pontuação de perfis conflitantes.

## Testes

Execute:

```bash
python testes_personas.py
```

São verificados 45 casos: 13 personas, dois perfis com respostas graduais e as 30 combinações principais de regras. Também são conferidos o número de trilhas, o Top 3, os percentuais, os gaps e o roadmap.

## Observação

As pontuações e os pesos são parâmetros do modelo acadêmico. A base pode ser refinada sem alteração do motor, bastando editar `regras_carreiras.json` e executar novamente os testes.
