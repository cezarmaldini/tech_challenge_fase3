from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

# Cache para evitar reconexões em cada reload
@st.cache_resource
def get_engine():
    user = "postgres.kjmflmvmlayjmdhzqxbz"
    password = "Z9OEnfDEnYxGpqEt"
    host = "aws-0-sa-east-1.pooler.supabase.com"
    port = "6543"
    database = "postgres"

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    return engine