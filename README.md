# 📊 Tech Challenge | Fase 3

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 3** da Pós-Tech em Engenharia de Dados, com o objetivo de transformar os dados da **PNAD COVID-19**, disponibilizados pelo IBGE, em informações acessíveis e relevantes para a tomada de decisão em saúde pública.

---

## 🔍 1. Contextualização do Problema

Durante a pandemia de COVID-19, compreender o comportamento da população, os sintomas clínicos mais comuns e os impactos sociais e econômicos tornou-se uma prioridade para instituições de saúde.

O IBGE disponibilizou a pesquisa **PNAD COVID-19**, com dados valiosos, porém brutos e descentralizados.

Este projeto simula a contratação de um **Especialista em Data Analytics** por um hospital para:

- Analisar o comportamento populacional durante a pandemia.
- Identificar indicadores úteis para ações em futuros surtos.

---

## 🧩 2. Solução

Foi desenvolvida uma **arquitetura moderna de dados e analytics**, capaz de:

- Organizar e transformar dados brutos em camadas (Bronze, Silver, Gold) no **Microsoft Fabric**.
- Oferecer uma **interface interativa** via **Streamlit**.
- Fornecer insights sobre sintomas, renda, escolaridade, raça/cor e outros aspectos.

### Arquitetura da Solução

![Arquitetura da Solução](https://i.ibb.co/rKLb4C7G/Planejamento-de-Sprint-Quadro-1.jpg)

### Questionamentos Utilizados (Exemplos)

- `A002` – Idade do morador  
- `A003` – Sexo  
- `A004` – Cor ou raça  
- `B009B/D/F` – Resultados de exames (SWAB, sangue dedo, sangue veia)  
- `C007C`, `C01011` – Trabalho e faixa de rendimento  
- `D0031`, `D0051` – Programas sociais  
- `F001`, `F0022` – Dados de moradia  

### Meses Analisados

Setembro, Outubro e Novembro de 2020

### Acesse a Solução:
🔗 [tech-challenge-fase3.onrender.com](https://tech-challenge-fase3.onrender.com)

---

## 🔄 3. Pipeline de Dados

O pipeline segue a arquitetura **medalhão** e foi implementado no **Microsoft Fabric**:

| Camada | Descrição | Notebook |
|--------|-----------|----------|
| 🥉 Bronze | Dados brutos (CSV) carregados no Lakehouse. | – |
| 🥈 Silver | Limpeza, renomeação de colunas, padronização de formatos. | `nb_dados_silver.ipynb`, `nb_dicionarios_silver.ipynb` |
| 🥇 Gold | Agregações, joins, categorização e transformação para analytics. | `nb_dados_gold.ipynb` |

### Visualizações das Camadas

#### Bronze

![Dicionários](https://i.ibb.co/XTGMMRp/dict.png)
![Dados](https://i.ibb.co/NgGTKH5W/dados-pnad.png)

#### Silver

| `nb_dicionarios_silver.ipynb` | `nb_dados_silver.ipynb` |
|-------------------------------|---------------------------|
| ![Silver 1](https://i.ibb.co/4w9bsKv1/Planejamento-de-Sprint-Quadro-2.jpg) | ![Silver 2](https://i.ibb.co/twKtK800/Planejamento-de-Sprint-Quadro-3.jpg) |

#### Gold

| `nb_dados_gold.ipynb` |
|------------------------|
| ![Gold](https://i.ibb.co/mV8B6HVt/Planejamento-de-Sprint-Quadro-4.jpg) |

---

## 📈 4. Analytics

Interface desenvolvida com **Streamlit**:

- Dashboards por **estado e período**
- Filtros por **mês, estado e tipo de exame**
- Análises por **sexo, faixa etária, cor/raça, escolaridade e renda**
- Visualizações: **gráficos de barras, roscas e mapas interativos**

---

## 🛠️ 5. Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Microsoft Fabric** | Lakehouse, Notebooks, Delta/Parquet |
| **PySpark** | Processamento de dados |
| **SQL** | Consultas de análise |
| **Streamlit** | Interface Web |
| **Plotly** | Visualizações interativas |
| **GitHub** | Versionamento e CI/CD |
| **Render** | Hospedagem da aplicação |