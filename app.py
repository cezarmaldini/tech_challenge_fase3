import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu

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

# Página ChatBot
if option == 'ChatBot':
    st.title('🤖 ChatBot Analytics | PNAD COVID 19')