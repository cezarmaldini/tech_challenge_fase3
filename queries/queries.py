import pandas as pd
from config.db import get_engine

def taxa_positividade_sangue_por_estado(mes_nome=None, estado=None):
    engine = get_engine()
    query = """
        SELECT
            estado,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos,
            ROUND(
                100.0 * SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) / COUNT(*), 2
            ) AS taxa_positividade
        FROM dados_pnad
        WHERE (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY estado
        ORDER BY taxa_positividade DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

def casos_positivos_por_genero(mes_nome=None, estado=None):
    engine = get_engine()
    query = """
        SELECT
            sexo,
            COUNT(*) AS positivos
        FROM dados_pnad
        WHERE LOWER(exame_sangue) = 'positivo'
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY sexo;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

def total_testes_por_faixa_etaria(mes_nome=None, estado=None):
    engine = get_engine()
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
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY faixa_etaria
        ORDER BY faixa_etaria;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

def positivos_por_raca(mes_nome=None, estado=None):
    engine = get_engine()
    query = """
        SELECT
            cor,
            COUNT(*) AS total_casos_positivos
        FROM dados_pnad
        WHERE LOWER(exame_sangue) = 'positivo'
          AND cor IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY cor
        ORDER BY total_casos_positivos DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

def positivos_por_escolaridade(mes_nome=None, estado=None):
    engine = get_engine()
    query = """
        SELECT
            escolaridade,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos
        FROM dados_pnad
        WHERE escolaridade IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY escolaridade
        ORDER BY positivos DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)