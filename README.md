Dashboard Financeiro & RPA Challenge – DemoQA Automation

Este repositório contém dois projetos distintos desenvolvidos em Python:
- Dashboard Financeiro 
- Painel interativo desenvolvido com Python + Streamlit para análise de indicadores econômicos no Brasil, integrando dados do Banco Central do Brasil e Boletim Focus.

RPA Challenge – Automação DemoQA
Automação de testes e extração de dados do site DemoQA, com geração de outputs em CSV e JSON.

Parte 1 – Dashboard Financeiro
🎯 Objetivo
- Monitorar indicadores macroeconômicos relevantes
- Visualizar expectativas de mercado
- Apoiar análise executiva e tomada de decisão

📊 Indicadores Monitorados
- SELIC	Taxa básica de juros da economia brasileira
- USD/BRL	Taxa de câmbio Real/Dólar
- IPCA	Índice oficial de inflação do Brasil

📈 Estrutura do Dashboard

Página Executiva:

- KPIs principais: SELIC, USD/BRL, Retorno do dólar (7 e 30 dias), Volatilidade, IPCA acumulado
- Análises adicionais: correlação móvel USD x SELIC, alerta de percentil 90 do histórico, curva de expectativas do mercado (Boletim Focus)

Página de Detalhamento:

- Série histórica de SELIC, USD/BRL e IPCA
- Variações do dólar (M/M e Y/Y)
- Visualização de dados brutos filtrados por período

🗂 Arquivos do Painel e Camada de Dados
- Arquivo do painel: dashboard.py (Streamlit)
- 
**Instruções de abertura/uso:**

pip install -r requirements.txt
streamlit run dashboard.py

Abrirá o dashboard no navegador.

Camada de dados: Scripts Python que capturam dados do Banco Central (API SGS) e do Boletim Focus (API Olinda).

data_fetch_bcb.py – captura séries históricas SELIC, USD/BRL e IPCA

data_fetch_focus.py – captura expectativas de mercado

Estes scripts podem ser executados para atualizar os dados periodicamente.

Dados utilizados: séries históricas do Banco Central e previsões do Boletim Focus, armazenadas localmente em .csv temporários ou diretamente processadas pelo painel.



Parte 2 – RPA Challenge – DemoQA Automation

Descrição:
Automação de quatro cenários no site DemoQA:
- Text Box: Preenche campos de texto e salva resultados em JSON.
- Check Box: Seleciona checkboxes, expande árvore e registra resultado.
- Web Tables: Extrai dados de tabelas HTML, salva CSV e gera resumo JSON.
- Upload de arquivo: Faz upload de arquivo local e salva nome do arquivo enviado em JSON.

**Pré-requisitos**:

Python 3.9+
Virtualenv ou venv

**Dependências:**

pip install -r requirements.txt

Recomendado: rodar com headless=False para visualizar a execução.

Dashboard Financeiro & RPA Challenge – DemoQA Automation

Este repositório contém dois projetos distintos desenvolvidos em Python:

Dashboard Financeiro – Monitoramento Macroeconômico
Painel interativo desenvolvido com Python + Streamlit para análise de indicadores econômicos no Brasil, integrando dados do Banco Central do Brasil e Boletim Focus.

RPA Challenge – Automação DemoQA
Automação de testes e extração de dados do site DemoQA
, com geração de outputs em CSV e JSON.

Parte 1 – Dashboard Financeiro
🎯 Objetivo

Monitorar indicadores macroeconômicos relevantes

Visualizar expectativas de mercado

Apoiar análise executiva e tomada de decisão

📊 Indicadores Monitorados
Indicador	Descrição
SELIC	Taxa básica de juros da economia brasileira
USD/BRL	Taxa de câmbio Real/Dólar
IPCA	Índice oficial de inflação do Brasil
📈 Estrutura do Dashboard
Página Executiva

KPIs principais: SELIC, USD/BRL, Retorno do dólar (7 e 30 dias), Volatilidade, IPCA acumulado

Análises adicionais: correlação móvel USD x SELIC, alerta de percentil 90 do histórico, curva de expectativas do mercado (Boletim Focus)

Página de Detalhamento

Série histórica de SELIC, USD/BRL e IPCA

Variações do dólar (M/M e Y/Y)

Visualização de dados brutos filtrados por período

🗂 Arquivos do Painel e Camada de Dados

Arquivo do painel: dashboard.py (Streamlit)
Instruções de abertura/uso:

pip install -r requirements.txt
streamlit run dashboard.py

Abrirá o dashboard no navegador.

Camada de dados: Scripts Python que capturam dados do Banco Central (API SGS) e do Boletim Focus (API Olinda).

data_fetch_bcb.py – captura séries históricas SELIC, USD/BRL e IPCA

data_fetch_focus.py – captura expectativas de mercado

Estes scripts podem ser executados para atualizar os dados periodicamente.

Dados utilizados: séries históricas do Banco Central e previsões do Boletim Focus, armazenadas localmente em .csv temporários ou diretamente processadas pelo painel.

Parte 2 – RPA Challenge – DemoQA Automation
Descrição

Automação de quatro cenários no site DemoQA:

Text Box: Preenche campos de texto e salva resultados em JSON.

Check Box: Seleciona checkboxes, expande árvore e registra resultado.

Web Tables: Extrai dados de tabelas HTML, salva CSV e gera resumo JSON.

Upload de arquivo: Faz upload de arquivo local e salva nome do arquivo enviado em JSON.

Pré-requisitos

Python 3.9+

Virtualenv ou venv

Dependências:

pip install -r requirements.txt

Recomendado: rodar com headless=False para visualizar a execução.

Estrutura de Pastas
rpa-bcb-challenge/
├─ assets/                   # Arquivos para upload
│  └─ documento_teste.pdf
├─ outputs/                  # Resultados gerados
│  ├─ text_box_result.json
│  ├─ webtables_extract.csv
│  ├─ webtables_summary.json
│  └─ upload_result.json
├─ rpa_challenge.py          # Script principal
└─ requirements.txt
Execução

Ative seu ambiente virtual e execute:

python rpa_challenge.py

Após a execução, os resultados estarão na pasta outputs/.


**Pontos de melhoria para versões futuras**

_Painel Dashboard:_

- Aplicar brandbook da marca (cores, fontes, ícones personalizados)
- Ajustar linguagens e termos de acordo com áreas de foco
- Ajustes de fluidez e agilidade na interface
- Possibilidade de envio automático de resumos de dados (diário, semanal ou mensal)

_RPA Challenge:_

- Melhorar fluidez e velocidade da automação
- Reduzir tempo de execução de ponta a ponta

**Horas de Trabalho**
Dia/Horário/Atividades

Quinta-feira	9h às 16h:	Construção do painel e conexão com APIs
Sexta-feira	8h às 18h:	Construção do RPA (automação de cenários)
Segunda-feira	7h às 12:45:	Revisão de dados, certificação de resultados, testes, limpeza de arquivos e ajustes finais

**Observações sobre o tempo:**

- A maior parte do tempo foi dedicada a garantir que os dados fossem capturados corretamente e à validação dos outputs do RPA.
- Ajustes de interface e branding são planejados para versões futuras.

**Observações Gerais**

Bloqueio automático de anúncios e iframes no RPA para evitar interferência.

Outputs (CSV e JSON) são gerados apenas se os dados estiverem disponíveis.

Para adicionar novos cenários na automação, utilize a mesma abordagem page.evaluate ou page.locator.****
