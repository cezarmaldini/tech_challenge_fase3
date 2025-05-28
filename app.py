# Importar Bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from queries.queries import (
    casos_positivos_estados,
    casos_positivos_por_genero,
    casos_positivos_faixa_etaria,
    casos_positivos_raca,
    casos_positivos_escolaridade,
    casos_positivos_auxilio,
    casos_positivos_renda,
    metricas_gerais
)

# Confiuração inicial da aplicação
st.set_page_config(
    page_title='Analytics | PNAD COVID 19',
    page_icon='📊',
    layout='wide'
)

# Navegação da Aplicação
with st.sidebar:
    option = option_menu(
        menu_title="Navegação",
        options=["Home", "Dashboard"],
        icons=["house", "bar-chart"],
        menu_icon="card-list",
        default_index=0
    )

# Página Apresentação do Projeto
if option == 'Home':
    st.title("📊 Tech Challenge | Fase 3")
    st.markdown("---")

    # 1. Contextualização do Problema
    st.header("🔍 Contextualização do Problema")
    st.markdown("""
    Durante a pandemia de COVID-19, compreender o comportamento da população, os sintomas clínicos mais comuns e os impactos sociais e econômicos 
    tornou-se uma prioridade para instituições de saúde. Pensando nisso, o governo brasileiro disponibilizou a pesquisa **PNAD COVID-19**, 
    realizada pelo IBGE, com o intuito de monitorar esses impactos de forma contínua.

    Agora, imagine que você foi contratado como **Especialista em Data Analytics** por um grande hospital, com a missão de analisar como a população 
    se comportou durante aquele período e quais indicadores seriam essenciais para o planejamento estratégico diante de um possível novo surto da doença.

    Apesar de sua contratação ser recente, sua equipe identificou na PNAD COVID-19 uma fonte rica e confiável de dados para orientar decisões clínicas, 
    demográficas e econômicas. No entanto, a base é extensa, descentralizada e bruta — o que dificulta a obtenção de insights rápidos.

    Com base em até 20 questionamentos da pesquisa e dados de três meses selecionados, a solução visa fornecer ao hospital uma visão clara sobre o 
    impacto da COVID-19 e apoiar ações preventivas e estratégicas no futuro.
    """)

    st.markdown("---")

    # 2. Solução
    st.header("🧩 Solução")
    st.markdown("""
    Para responder ao desafio proposto, foi desenvolvida uma **arquitetura moderna de dados e analytics**, capaz de transformar os dados brutos da PNAD COVID-19 
    em informações acessíveis, relevantes e interativas.

    A solução é composta por:

    - **Ingestão e tratamento dos dados** utilizando arquitetura em camadas (Bronze, Silver, Gold) no Microsoft Fabric.
    - **Interface interativa** para análises exploratórias via Streamlit, hospedada na nuvem.
    """)

    st.markdown('##### Arquitetura da Solução:')
    st.image("https://i.ibb.co/rKLb4C7G/Planejamento-de-Sprint-Quadro-1.jpg", use_container_width=True)

    st.markdown('##### Questionamentos utilizados:')
    st.markdown("""
    - **A002:** Idade do morador.
    - **A003:** Sexo.
    - **A004:** Cor ou raça.
    - **A005:** Escolaridade.
    - **B009B:** Resultados do exame SWAB.
    - **B009D:** Resultados do exame de sangue através do dedo.
    - **B009F:** Resultados do exame de sangue através da veia do braço.
    - **C007C:** Tipo de trabalho, cargo ou função.
    - **C01011:** Faixa de rendimento.
    - **D0031:** Bolsa Família.
    - **D0051:** Auxílio emergencial.
    - **F001:** Domicílio.
    - **F0022:** Número da faixa do aluguel.
    """)

    st.markdown("""
    ##### Meses analisados:
    Setembro, Outubro e Novembro de 2020    
    """)

    st.markdown('##### A solução está disponível em:')
    st.markdown('https://tech-challenge-fase3.onrender.com')

    st.markdown("---")

    # 3. Pipeline de Dados
    st.header("🔄 Pipeline de Dados (ETL)")
    st.markdown("""
    A construção do pipeline de dados segue o conceito da arquitetura **medalhão** e foi implementada no **Microsoft Fabric**, garantindo qualidade, rastreabilidade e performance:

    | Camada | Descrição | Notebook |
    |--------|-----------|----------|
    | 🥉 **Bronze** | Dados brutos carregados diretamente dos arquivos disponibilizados pelo IBGE, sem qualquer modificação. |  |
    | 🥈 **Silver** | Aplicação de filtros, limpeza de dados desnecessárias, colunas renomeadas, formatos de dados. | `nb_dados_silver.ipynb` e `nb_dicionarios_silver.ipynb`|
    | 🥇 **Gold** | Transformações finais com agregações, categorização, mesclagens (joins) e preparação para análises. | `nb_dados_gold.ipynb` |
    """)

    st.markdown('##### 🥉 Camada Bronze')
    st.markdown("""
    Nessa camada os dados são carregados manualmente no Files do Lakehouse, seguindo a estrutura da imagem: 
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://i.ibb.co/XTGMMRp/dict.png", caption='Dicionários', use_container_width=True)
    with col2:
        st.image("https://i.ibb.co/NgGTKH5W/dados-pnad.png", caption='Dados', use_container_width=True)

    st.markdown('##### 🥈 Camada Silver')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Arquivo: nb_dicionarios_silver.ipynb**
        
        Processa os arquivos de dicionários armazenados na camada bronze e carrega na camada silver em formato parquet.
        """)
        st.image('https://i.ibb.co/4w9bsKv1/Planejamento-de-Sprint-Quadro-2.jpg', use_container_width=True)

    with col2:
        st.markdown("""
        **Arquivo: nb_dados_silver.ipynb**
        
        Processa os arquivos de dicionários armazenados na camada bronze e carrega na camada silver em formato parquet.
        """)
        st.image('https://i.ibb.co/twKtK800/Planejamento-de-Sprint-Quadro-3.jpg', use_container_width=True)

    st.markdown('##### 🥇 Camada Gold')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Arquivo: nb_dados_gold.ipynb**
        
        Processa dados armazenados na camada silver no formato parquet, faz as transformações necessárias para a fase de analytics
        e carrega na camada gold em formato delta table.
        """)
        st.image('https://i.ibb.co/mV8B6HVt/Planejamento-de-Sprint-Quadro-4.jpg', use_container_width=True)
        

    st.markdown("---")

    # 4. Analytics
    st.header("📈 Analytics")
    st.markdown("""
    A camada de **Analytics** foi desenvolvida com a biblioteca **Streamlit**, proporcionando uma interface interativa e acessível para exploração dos dados.

    Funcionalidades principais:

    - Dashboards com análises por estado, características demograficas, de trabalho e renda.
    - Filtros de mês, estado e tipos de exames
    - Análises por **gênero, idade, raça/cor, escolaridade e renda**
    - **Gráficos interativos**: barras, roscas, mapas
    """)

    st.markdown("---")

    # 5. Tecnologias Utilizadas
    st.header("🛠️ Tecnologias Utilizadas")
    st.markdown("""
    A solução foi desenvolvida com um conjunto de ferramentas modernas, voltadas para tratamento de dados em larga escala, visualização interativa e implantação em nuvem:

    - **Microsoft Fabric:** Lakehouse, Notebooks, OneLake
    - **PySpark:** Processamento de dados
    - **SQL:** Consultas para análises gráficas
    - **Streamlit:** Construção da interface web
    - **Plotly:** Plotagem de gráficos e visuais interativos
    - **GitHub:** Versionamento e CI/CD
    - **Render:** Deploy
    """)

    st.markdown("---")

    # 6. Estrutura do Repositório
    st.header("📁 Estrutura do Repositório")
    st.markdown("""
    O projeto foi versionado e está disponível publicamente no GitHub:

    🔗 [Acesse o repositório no GitHub](https://github.com/cezarmaldini/tech_challenge_fase3)

    A estrutura do repositório foi organizada para garantir **manutenibilidade, legibilidade e separação de responsabilidades**:

    | Diretório/Arquivo | Descrição |
    |-------------------|-----------|
    | `app.py` | Arquivo principal da aplicação Streamlit. |
    | `config/` | Contém scripts de configuração, como conexão com banco de dados (`db.py`). |
    | `queries/` | Contém o módulo de consultas SQL utilizadas nos dashboards (`queries.py`). |
    | `notebooks/` | Notebooks utilizados nas etapas de ingestão, tratamento e transformação dos dados. |
    | `requirements.txt` | Lista de dependências para ambiente Python. |
    | `.streamlit/config.toml` | Arquivo de configuração da interface do Streamlit. |
    | `README.md` | Descrição do projeto, instruções de execução e propósito. |

    A organização do repositório segue boas práticas de projetos em ciência de dados e engenharia de dados, com separação entre camada de aplicação, lógica de dados e notebooks exploratórios.
    """)

    st.markdown("---")

    st.success("Projeto finalizado com arquitetura moderna, dados de qualidade e análises acessíveis.")

# Página Dashboard
elif option == 'Dashboard':
    st.title('Data Analytics | PNAD COVID 19')
    st.markdown('##### Perído: setembro, outubro e novembro de 2020')

    # Filtros
    with st.expander('Filtros'):
        col1, col2, col3 = st.columns(3)

        # Filtro de Meses
        with col1:
            mes_opcao = st.selectbox("Mês", ["Todos", "setembro", "outubro", "novembro"])
            mes_param = None if mes_opcao == "Todos" else mes_opcao

        # Filtro de Estados
        with col2:
            estados_disponiveis = [
                "Todos", "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
                "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais",
                "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte",
                "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
            ]
            estado_opcao = st.selectbox("Estado", estados_disponiveis)
            estado_param = None if estado_opcao == "Todos" else estado_opcao

            # Filtro de Tipo de Exame
        with col3:
            tipo_exame_dict = {
            "Coleta de Sangue": "exame_sangue",
            "Coleta de Sangue Furo no Dedo": "exame_dedo",
            "SWAB": "exame_swab"
            }

            tipo_exame_selecionado = st.selectbox(
                "Tipo de Exame",
                options=list(tipo_exame_dict.keys()),
                index=0
            )

            exame_param = tipo_exame_dict[tipo_exame_selecionado]

    # Métricas Gerais
    st.header('Métricas Gerais')
    met = metricas_gerais(mes_param, estado_param, exame_param)

    def format_brl(n):
        return f"{n:,}".replace(",", ".")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Pessoas Entrevistadas", format_brl(met.total_entrevistados.iloc[0]))
    col2.metric("Total de Testes Realizados", format_brl(met.total_testes.iloc[0]))
    col3.metric("Total de Testes Positivos", format_brl(met.total_positivos.iloc[0]))
        
    st.divider()

    # Análises por Estado
    st.header('Análise por Estado')

    st.markdown("#### Mapa de Casos por Estado")

    df = casos_positivos_estados(mes_param, estado_param, exame_param)
    df['estado'] = df['estado'].str.title()

    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

    fig = px.choropleth(
        df,
        geojson=geojson_url,
        locations='estado',
        featureidkey='properties.name',
        color='positivos',  # alterado aqui
        color_continuous_scale=['#8ae4ff', '#0c5ab5'],
        hover_data=['positivos', 'total_testes'],
        labels={'positivos': 'Casos Positivos'}  # alterado aqui
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)
        
    st.divider()
        
    # Análises por Características Demográficas
    st.header('Análise por Características Demográficas')

    col1, col2 = st.columns(2)
    with col1:
        # Casos Positivos por Cor/Raça
        st.markdown("#### Casos Positivos por Cor/Raça")
        df_cor = casos_positivos_raca(mes_param, estado_param, exame_param)

        fig_cor = px.bar(
            df_cor,
            x="cor",
            y="total_casos_positivos",
            color="total_casos_positivos",
            color_continuous_scale=['#8ae4ff', '#0c5ab5'],
            labels={"cor": "Cor/Raça", "total_casos_positivos": "Casos Positivos"},
            height=500
        )

        fig_cor.update_layout(xaxis_title="Cor/Raça", yaxis_title="Casos Positivos")
        st.plotly_chart(fig_cor, use_container_width=True)
        
    with col2:
        # Casos Positivos por Faixa Etária
        st.markdown("#### Casos Positivos por Faixa Etária")

        df_idade = casos_positivos_faixa_etaria(mes_param, estado_param, exame_param)

        fig_linhas = px.line(
            df_idade,
            x="faixa_etaria",
            y=["positivos"],
            markers=True,
            labels={"value": "Quantidade", "faixa_etaria": "Faixa Etária", "variable": "Tipo"}
        )

        st.plotly_chart(fig_linhas, use_container_width=True)
        
    col1, col2 = st.columns(2)
    with col1:
        # Casos Positivos por Gênero
        st.markdown("#### Casos Positivos por Gênero")
        df_sexo = casos_positivos_por_genero(mes_param, estado_param, exame_param)
        fig_sexo = px.pie(
            df_sexo,
            names='sexo',
            values='positivos',
            hole=0.60,
            color_discrete_sequence=['#0c5ab5', '#07a6d5']
        )
        fig_sexo.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_sexo, use_container_width=True)
        
    with col2:
        # Casos Positivos por Escolaridade
        st.markdown("#### Casos Positivos por Escolaridade")
        df_esc = casos_positivos_escolaridade(mes_param, estado_param, exame_param)

        df_esc = df_esc.sort_values(by="positivos", ascending=True)

        fig_esc = px.bar(
            df_esc,
            x="positivos",
            y="escolaridade",
            orientation='h',
            color="positivos",
            color_continuous_scale=['#8ae4ff', '#0c5ab5'],
            labels={"escolaridade": "Escolaridade"},
            height=500
        )

        fig_esc.update_layout(xaxis_title="", yaxis_title="Escolaridade")
        st.plotly_chart(fig_esc, use_container_width=True)
        
    st.divider()

    # Análises por Trabalho e Renda
    st.header('Análise por Trabalho e Renda')

    col1, col2 = st.columns(2)

    with col1:
        # Casos positivos por Bolsa Família
        st.markdown("#### Casos Positivos e Bolsa Família")

        df_aux = casos_positivos_auxilio(mes_param, estado_param, exame_param)

        df_bolsa = df_aux.groupby("bolsa_familia", as_index=False)["positivos"].sum()

        fig_bolsa = px.pie(
            df_bolsa,
            names='bolsa_familia',
            values='positivos',
            hole=0.60,
            color_discrete_sequence=['#0c5ab5', '#07a6d5']
        )
        fig_bolsa.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_bolsa, use_container_width=True)

    with col2:
        # Casos positivos por auxílio emergencial
        st.markdown("#### Casos Positivos e Auxílio Emergencial")

        df_auxilio = df_aux.groupby("auxilio", as_index=False)["positivos"].sum()

        fig_auxilio = px.pie(
            df_auxilio,
            names='auxilio',
            values='positivos',
            hole=0.60,
            color_discrete_sequence=['#0c5ab5', '#07a6d5']
        )
        fig_auxilio.update_layout(
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_auxilio, use_container_width=True)

    # Casos Positivos por Faixa de Renda
    st.markdown("### Casos Positivos por Faixa de Renda")
    df_renda = casos_positivos_renda(mes_param, estado_param, exame_param)

    fig_renda = px.bar(
        df_renda,
        x="faixa_renda",
        y="positivos",
        color="positivos",
        color_continuous_scale=['#8ae4ff', '#0c5ab5'],
        labels={"faixa_renda": "Faixa de Renda", "positivos": "Casos Positivos"}
    )
    st.plotly_chart(fig_renda, use_container_width=True)
