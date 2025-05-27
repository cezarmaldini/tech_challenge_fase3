import pandas as pd
from config.db import get_engine

def taxa_positividade_sangue_por_estado(mes_nome=None):
    where_clause = f"WHERE mes_nome = '{mes_nome}'" if mes_nome else ""
    
    query = f"""
        SELECT
            estado,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos,
            ROUND(
                100.0 * SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) / COUNT(*), 2
            ) AS taxa_positividade
        FROM dados_pnad
        {where_clause}
        GROUP BY estado
        ORDER BY taxa_positividade DESC;
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def casos_positivos_por_genero():
    query = """
        SELECT
            sexo,
            COUNT(*) AS positivos
        FROM dados_pnad
        WHERE LOWER(exame_sangue) = 'positivo'
        GROUP BY sexo
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def total_testes_por_faixa_etaria():
    query = """
        SELECT
            CASE
                WHEN idade BETWEEN 0 AND 17 THEN '0-17'
                WHEN idade BETWEEN 18 AND 29 THEN '18-29'
                WHEN idade BETWEEN 30 AND 44 THEN '30-44'
                WHEN idade BETWEEN 45 AND 59 THEN '45-59'
                WHEN idade >= 60 THEN '60+'
                ELSE 'Desconhecida'
            END AS faixa_etaria,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos
        FROM dados_pnad
        WHERE idade IS NOT NULL
        GROUP BY faixa_etaria
        ORDER BY faixa_etaria;
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def positivos_por_raca():
    query = """
        SELECT
            cor,
            COUNT(*) AS total_casos_positivos
        FROM dados_pnad
        WHERE LOWER(exame_sangue) = 'positivo'
        AND cor IS NOT NULL
        GROUP BY cor
        ORDER BY total_casos_positivos DESC
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def positivos_por_escolaridade():
    query = """
        SELECT
            escolaridade,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos
        FROM dados_pnad
        WHERE escolaridade IS NOT NULL
        GROUP BY escolaridade
        ORDER BY positivos DESC
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)