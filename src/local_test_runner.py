import pandas as pd
from src.report_generator import ReportGenerator


def main_teste_local(csv_path, template_path, output_folder):
    try:
        df = pd.read_csv(csv_path)

        if df.empty:
            raise ValueError("Arquivo CSV está vazio.")

        print(f"Arquivo CSV lido com sucesso. Total de linhas: {len(df)}")

        generator = ReportGenerator(output_folder, template_path, df)
        generator.save_report()

        print("Relatórios gerados com sucesso (modo teste local).")
    except Exception as e:
        print(f"Erro durante o processamento de teste: {e}")
