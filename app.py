import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
from queries.infectados import taxa_positividade_sangue_por_estado

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
    aba1, aba2 = st.tabs(['Dashboard', 'Tabela'])

    # Aba Dashboard
    with aba1:
        st.header('Dashboard')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Mapa de Casos por Estado")

            df = taxa_positividade_sangue_por_estado()
            df['estado'] = df['estado'].str.title()

            geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

            fig = px.choropleth(
                df,
                geojson=geojson_url,
                locations='estado',
                featureidkey='properties.name',
                color='taxa_positividade',
                color_continuous_scale='Reds',
                hover_data=['positivos', 'total_testes'],
                labels={'taxa_positividade': '% Positivos'}
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

            st.plotly_chart(fig, use_container_width=True)