import pandas as pd
from config.db import get_engine

def taxa_positividade_sangue_por_estado():
    query = """
        SELECT
            estado,
            COUNT(*) AS total_testes,
            SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) AS positivos,
            ROUND(
                100.0 * SUM(CASE WHEN LOWER(exame_sangue) = 'positivo' THEN 1 ELSE 0 END) / COUNT(*), 2
            ) AS taxa_positividade
        FROM dados_pnad
        GROUP BY estado
        ORDER BY taxa_positividade DESC;
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)