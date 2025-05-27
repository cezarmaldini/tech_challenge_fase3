import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from queries.queries import (
    taxa_positividade_sangue_por_estado,
    casos_positivos_por_genero,
    total_testes_por_faixa_etaria,
    positivos_por_raca,
    positivos_por_escolaridade,
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
        options=["Analytics", "ChatBot"],
        icons=["bar-chart", "robot"],
        menu_icon="card-list",
        default_index=0
    )

# Página Analytics
if option == 'Analytics':
    st.title('Data Analytics | PNAD COVID 19')

    # Abas: Dashboard e Tabela
    aba1, aba2 = st.tabs(['📊 Dashboard', '📅 Tabela'])

    # Aba Dashboard
    with aba1:
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

        # Separação em colunas
        st.markdown("#### Mapa de Casos por Estado")

        df = taxa_positividade_sangue_por_estado(mes_param, estado_param, exame_param)
        df['estado'] = df['estado'].str.title()

        geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

        fig = px.choropleth(
            df,
            geojson=geojson_url,
            locations='estado',
            featureidkey='properties.name',
            color='taxa_positividade',
            color_continuous_scale=['#8ae4ff', '#0c5ab5'],
            hover_data=['positivos', 'total_testes'],
            labels={'taxa_positividade': '% Positivos'}
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Análises por Características Demográficas
        st.header('Análise por Características Demográficas')

        col1, col2 = st.columns(2)
        with col1:
            # Casos Positivos por Cor/Raça
            st.markdown("#### Casos Positivos por Cor/Raça")
            df_cor = positivos_por_raca(mes_param, estado_param, exame_param)

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

            df_idade = total_testes_por_faixa_etaria(mes_param, estado_param, exame_param)

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
            df_esc = positivos_por_escolaridade(mes_param, estado_param, exame_param)

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