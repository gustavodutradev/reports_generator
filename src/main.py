import dotenv
import pandas as pd
from sqlalchemy import text
from src.utils.cache_relations import engine
from src.report_generator import ReportGenerator

dotenv.load_dotenv()

def main(output_folder, template_text, ano, mes):
    """ Gera relatórios de rentabilidade a partir do banco de dados."""
    data_ref = f"{ano}-{int(mes):02d}-01"

    # Consulta de rentabilidade mensal
    query_mtd = text(
        """
        SELECT nr_conta, profitability_mtd, cdi_mtd, profit_mtd
        FROM public.rentabilidade_mensal_por_carteira
        WHERE mes_referencia = :data_ref
        """
    )
    df_mtd = pd.read_sql_query(query_mtd, engine, params={"data_ref": data_ref})

    # Consulta de rentabilidade acumulada
    query_12m = text(
        """
        SELECT nr_conta, profitability_12m, cdi_12m, profit_12m
        FROM public.rentabilidade_acumulada_por_carteira
        WHERE mes_referencia = :data_ref
        """
    )
    df_ac = pd.read_sql_query(query_12m, engine, params={"data_ref": data_ref})

    # Validação de dados
    if df_mtd.empty and df_ac.empty:
        print(f"Erro: não há dados para {data_ref}")
        return False

    # União dos DataFrames
    df = df_mtd.merge(df_ac, on="nr_conta", how="outer")

    # Geração dos relatórios
    report_generator = ReportGenerator(output_folder, template_text, df)
    report_generator.save_report()

    return True
