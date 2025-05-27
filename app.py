import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
from queries.queries import (
    taxa_positividade_sangue_por_estado,
    casos_positivos_por_genero,
    total_testes_por_faixa_etaria,
    positivos_por_raca,
    positivos_por_escolaridade
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
        st.subheader("Filtros")
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            mes_opcao = st.selectbox("Mês", ["Todos", "setembro", "outubro", "novembro"])
            mes_param = None if mes_opcao == "Todos" else mes_opcao

        with col_f2:
            estados_disponiveis = [
                "Todos", "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
                "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais",
                "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte",
                "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
            ]
            estado_opcao = st.selectbox("Estado", estados_disponiveis)
            estado_param = None if estado_opcao == "Todos" else estado_opcao


        # Análises por Estado
        st.header('Análises por Estado')
        st.divider()

        # Separação em colunas
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Mapa de Casos por Estado")

            df = taxa_positividade_sangue_por_estado(mes_param, estado_param)
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

        with col2:
            st.subheader("Taxa de Contaminação por Estado")

            df_sorted = df.sort_values(by="taxa_positividade", ascending=True)

            fig_bar = px.bar(
                df_sorted,
                x="taxa_positividade",
                y="estado",
                orientation='h',
                color="taxa_positividade",
                color_continuous_scale=['#8ae4ff', '#0c5ab5'],
                labels={"taxa_positividade": "% Positivos", "estado": "Estado"},
                height=600
            )

            fig_bar.update_layout(
                xaxis_title="% de Positivos",
                yaxis_title="Estado",
                margin=dict(l=0, r=0, t=30, b=0),
            )

            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Análises por Características Demográficas
        st.header('Análises por Características Demográficas')
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Casos Positivos por Gênero")

            df_sexo = casos_positivos_por_genero(mes_param, estado_param)
            fig_sexo = px.pie(
                df_sexo,
                names='sexo',
                values='positivos',
                hole=0.5,
                color_discrete_sequence=['#0c5ab5', '#07a6d5']
            )
            fig_sexo.update_layout(
                showlegend=True,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig_sexo, use_container_width=True)
            
            st.subheader("Casos Positivos por Cor/Raça")
            df_cor = positivos_por_raca(mes_param, estado_param)

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
            st.subheader("Testes por Faixa Etária")

            df_idade = total_testes_por_faixa_etaria(mes_param, estado_param)

            fig_linhas = px.line(
                df_idade,
                x="faixa_etaria",
                y=["positivos"],
                markers=True,
                labels={"value": "Quantidade", "faixa_etaria": "Faixa Etária", "variable": "Tipo"}
            )

            st.plotly_chart(fig_linhas, use_container_width=True)

            st.subheader("Casos Positivos por Escolaridade")
            df_esc = positivos_por_escolaridade(mes_param, estado_param)

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