pip install -r requirements.txt
python -m streamlit run dashboard/app.py

# RPA & Financial Dashboard Challenge

![Dashboard Demo](docs/dashboard_demo.gif)

# RPA & Financial Dashboard Challenge

Desafio técnico desenvolvido para avaliação da vaga de **Desenvolvedor RPA**.

O projeto possui duas partes principais:

1. **Painel financeiro com dados do Banco Central**
2. **Automação RPA simulando interação de usuário no navegador**

O objetivo é demonstrar habilidades em:

* consumo de APIs
* transformação de dados
* análise de indicadores econômicos
* construção de dashboards
* automação de processos via navegador

---

# Estrutura do Projeto

```
rpa-bcb-challenge
│
├── dashboard
│   └── app.py                # Dashboard Streamlit
│
├── rpa
│   └── demoqa_bot.py        # Automação DemoQA
│
├── outputs                  # Outputs gerados pela automação
│
├── assets
│   └── documento_teste.pdf  # Arquivo utilizado no upload
│
├── requirements.txt
└── README.md
```

---

# Parte 1 — Painel Econômico (Banco Central)

O painel consome dados diretamente da API pública do Banco Central (BCData / SGS).

Fonte oficial:

* SELIC (série 11)
* USD/BRL (série 1)
* IPCA (série 433)

Dados obtidos via API:

https://api.bcb.gov.br/dados/serie/bcdata.sgs

A atualização dos dados ocorre automaticamente sempre que o dashboard é executado.

---

# Janela Temporal

Foi utilizada uma janela mínima de **2022 até o presente**, garantindo mais de **24 meses de histórico**, conforme solicitado no desafio.

---

# KPIs Implementados

Os seguintes indicadores foram calculados:

### SELIC

* SELIC atual (último valor disponível)
* variação da SELIC nos últimos 30 dias

### USD/BRL

* valor atual
* retorno percentual em 7 dias
* retorno percentual em 30 dias

### Volatilidade Cambial

* volatilidade de 30 dias baseada em retornos diários

### Inflação

* IPCA acumulado em 12 meses (derivado da variação mensal)

---

# Análises Adicionais

Foram incluídas análises exploratórias e insights automáticos.

### 1 — Alerta de pressão cambial

O sistema calcula o **percentil 90 do histórico do USD/BRL**.

Caso o valor atual esteja acima desse limite, o dashboard gera um alerta indicando possível pressão cambial.

---

### 2 — Correlação entre USD e SELIC

Foi calculada a correlação histórica entre as séries:

* USD/BRL
* SELIC

Essa análise permite observar possíveis relações entre política monetária e câmbio.

---

### 3 — Volatilidade móvel

Foi implementado um cálculo de **volatilidade rolling de 30 dias**, permitindo identificar períodos de maior instabilidade no câmbio.

---

# Estrutura do Painel

O dashboard foi dividido em duas páginas:

### Página Executiva

Foco em leitura rápida para gestores:

* principais KPIs
* tendências recentes
* insights automáticos

### Página de Detalhamento

Permite exploração dos dados:

* séries históricas completas
* gráficos de tendência
* tabela de dados

---

# Filtros

O painel possui filtros de período:

* 30 dias
* 90 dias
* 180 dias
* histórico completo

Isso permite análises rápidas de curto e médio prazo.

---

# Como Executar o Dashboard

1 — criar ambiente virtual

```
python -m venv venv
```

2 — ativar ambiente

Windows:

```
venv\Scripts\activate
```

3 — instalar dependências

```
pip install -r requirements.txt
```

4 — executar o dashboard

```
python -m streamlit run dashboard/app.py
```

O painel abrirá automaticamente no navegador.

---

# Parte 2 — Automação RPA

A segunda parte do desafio consiste em uma automação de navegador utilizando o site de testes:

https://demoqa.com

A automação simula ações de usuário como:

* preenchimento de formulário
* seleção de checkboxes
* extração de dados de tabela
* upload de arquivo

---

# Cenários Implementados

### Text Box

* preenchimento de formulário
* submissão
* extração do resultado exibido na página

Output:

```
outputs/text_box_result.json
```

---

### Check Box

* expansão da árvore
* seleção dos itens:

```
Commands
General
```

---

### Web Tables

Extração dos dados da tabela:

Campos:

* First Name
* Last Name
* Age
* Email
* Salary
* Department

Outputs gerados:

```
outputs/webtables_extract.csv
outputs/webtables_summary.json
```

Resumo inclui:

* total de registros
* média salarial
* registros por departamento

---

### Upload

Realiza upload de um arquivo localizado em:

```
assets/documento_teste.pdf
```

Valida o nome do arquivo na interface.

Output:

```
outputs/upload_result.json
```

---

# Evidências

Foi gravado um vídeo demonstrando:

* execução ponta a ponta
* geração dos outputs
* funcionamento do dashboard

Duração: 2–5 minutos.

---

# Tecnologias Utilizadas

* Python
* Streamlit
* Pandas
* Requests
* Playwright (automação)

---

# Considerações Finais

O projeto foi estruturado com foco em:

* **reprodutibilidade**
* **clareza analítica**
* **automação end-to-end**
* **organização de código**

A solução permite atualização automática dos dados e execução das automações com um único comando.

---

OBS PARA AJUSTAR:
Plotly para garantir a integridade da escala temporal, impedindo que usuários internos visualizem períodos fora do escopo da análise contábil.
