import pandas as pd
from config.db import get_engine

# Consulta que faz o cálculo do Total de Pessoas Entrevistadas, Total de Testes Realizados e Total de Testes Positivos
def metricas_gerais(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    query = """
        SELECT
            COUNT(*) AS total_entrevistados,
            COUNT({col_exame}) AS total_testes,
            SUM(CASE WHEN LOWER({col_exame}) = 'positivo' THEN 1 ELSE 0 END) AS total_positivos
        FROM dados_pnad
        WHERE 1=1
    """
    if mes_nome:
        query += " AND mes_nome = %(mes_nome)s"
    if estado:
        query += " AND estado = %(estado)s"
    query = query.format(col_exame=coluna_exame)

    engine = get_engine()
    params = {'mes_nome': mes_nome, 'estado': estado}
    return pd.read_sql(query, con=engine, params={k: v for k, v in params.items() if v})

# Consulta que calcula a quantidade casos positivos por estado
def casos_positivos_estados(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
        SELECT
            estado,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER({coluna_exame}) = 'positivo' THEN 1 ELSE 0 END) AS positivos,
            ROUND(
                100.0 * SUM(CASE WHEN LOWER({coluna_exame}) = 'positivo' THEN 1 ELSE 0 END) / COUNT(*), 2
            ) AS taxa_positividade
        FROM dados_pnad
        WHERE (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY estado
        ORDER BY taxa_positividade DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

# Consulta que calcula os casos positivos por gênero
def casos_positivos_por_genero(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
        SELECT
            sexo,
            COUNT(*) AS positivos
        FROM dados_pnad
        WHERE LOWER({coluna_exame}) = 'positivo'
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY sexo
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

# Consulta que calcula os casos positivos por faixa etária
def casos_positivos_faixa_etaria(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
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
            SUM(CASE WHEN LOWER({coluna_exame}) = 'positivo' THEN 1 ELSE 0 END) AS positivos
        FROM dados_pnad
        WHERE idade IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY faixa_etaria
        ORDER BY faixa_etaria;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

# Consulta que calcula a quantidade de casos por Cor/Raça
def casos_positivos_raca(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
        SELECT
            cor,
            COUNT(*) AS total_casos_positivos
        FROM dados_pnad
        WHERE LOWER({coluna_exame}) = 'positivo'
          AND cor IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY cor
        ORDER BY total_casos_positivos DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

# Consulta que calcula os casos positivos por escolaridade
def casos_positivos_escolaridade(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
        SELECT
            escolaridade,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER({coluna_exame}) = 'positivo' THEN 1 ELSE 0 END) AS positivos
        FROM dados_pnad
        WHERE escolaridade IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY escolaridade
        ORDER BY positivos DESC;
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

# Consulta que calcula os casos positivos por Bolsa Família e Auxílio Emergencial
def casos_positivos_auxilio(mes=None, estado=None, exame='exame_sangue'):
    conditions = ["LOWER({}) = 'positivo'".format(exame)]
    if mes:
        conditions.append("mes_nome = %(mes)s")
    if estado:
        conditions.append("estado = %(estado)s")
    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            bolsa_familia,
            auxilio,
            COUNT(*) AS positivos
        FROM dados_pnad
        WHERE {where_clause}
        GROUP BY bolsa_familia, auxilio
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine, params={"mes": mes, "estado": estado})

# Consulta que calcula os casos positivos por faixa de renda
def casos_positivos_renda(mes_nome=None, estado=None, coluna_exame='exame_sangue'):
    engine = get_engine()
    query = f"""
        SELECT
            faixa_renda,
            "faixa_rendimentoId",
            COUNT(*) AS positivos
        FROM dados_pnad
        WHERE LOWER({coluna_exame}) = 'positivo'
          AND faixa_renda IS NOT NULL
          AND "faixa_rendimentoId" IS NOT NULL
          AND (%(mes_nome)s IS NULL OR mes_nome = %(mes_nome)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
        GROUP BY faixa_renda, "faixa_rendimentoId"
        ORDER BY "faixa_rendimentoId";
    """
    params = {"mes_nome": mes_nome, "estado": estado}
    return pd.read_sql(query, con=engine, params=params)

def tabela_dados_filtrados(mes=None, estado=None, sexo=None, cor=None, escolaridade=None, faixa_renda=None):
    engine = get_engine()
    query = """
        SELECT
            mes_nome,
            estado,
            CASE
                WHEN idade BETWEEN 0 AND 17 THEN '0-17'
                WHEN idade BETWEEN 18 AND 29 THEN '18-29'
                WHEN idade BETWEEN 30 AND 44 THEN '30-44'
                WHEN idade BETWEEN 45 AND 59 THEN '45-59'
                WHEN idade >= 60 THEN '60+'
                ELSE 'Desconhecida'
            END AS faixa_etaria,
            sexo,
            cor,
            escolaridade,
            exame_swab,
            exame_dedo,
            exame_sangue,
            faixa_renda
        FROM dados_pnad
        WHERE (%(mes)s IS NULL OR mes_nome = %(mes)s)
          AND (%(estado)s IS NULL OR estado = %(estado)s)
          AND (%(sexo)s IS NULL OR sexo = %(sexo)s)
          AND (%(cor)s IS NULL OR cor = %(cor)s)
          AND (%(escolaridade)s IS NULL OR escolaridade = %(escolaridade)s)
          AND (%(faixa_renda)s IS NULL OR faixa_renda = %(faixa_renda)s)
        LIMIT 100
    """
    params = {
        "mes": mes,
        "estado": estado,
        "sexo": sexo,
        "cor": cor,
        "escolaridade": escolaridade,
        "faixa_renda": faixa_renda
    }
    return pd.read_sql(query, con=engine, params=params)