import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
from queries.queries import taxa_positividade_sangue_por_estado, proporcao_genero

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
    
    # Carrega os percentuais
    homem_perc, mulher_perc = proporcao_genero()

    # Lê o HTML
    with open("components/genero.html", "r") as f:
        html = f.read().replace("{{HOMEM_PERC}}", f"{homem_perc:.1f}").replace("{{MULHER_PERC}}", f"{mulher_perc:.1f}")

    # Lê e injeta o CSS
    with open("styles/genero.css", "r") as f:
        css = f"<style>{f.read()}</style>"

    # Renderiza no Streamlit
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)