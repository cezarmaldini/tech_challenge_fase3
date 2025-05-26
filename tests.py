import streamlit as st
import pandas as pd
from supabase import Client, create_client

# Suas credenciais Supabase — substitua pelas suas do dashboard
SUPABASE_URL = "https://kjmflmvmlayjmdhzqxbz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqbWZsbXZtbGF5am1kaHpxeGJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NjY1MzMsImV4cCI6MjA2MzQ0MjUzM30.m5qYdO9--IysVawnd48oX6vTIBbWOI-Ubisjxw5549A"  #

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def carregar_dados():
    supabase = get_supabase_client()
    response = supabase.table("dados_pnad").select("*").limit(100).execute()
    
    # response é um dict com keys: 'data', 'error', 'status_code'
    if response['error'] is None:
        return response['data']
    else:
        st.error(f"Erro na consulta: {response['error']['message']}")
        return []

def main():
    st.title("Teste de Consulta Supabase com supabase-py")

    data = carregar_dados()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.warning("Nenhum dado encontrado ou erro na consulta.")

if __name__ == "__main__":
    main()