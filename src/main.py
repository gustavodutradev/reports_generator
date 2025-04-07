import pandas as pd
import requests
from src.report_generator import ReportGenerator
import dotenv
import os

dotenv.load_dotenv()

API_URL = os.getenv("API_URL")


def main(output_folder, template_text):
    try:
        print("Disparando solicitação para a API BTG...")
        response = requests.post(API_URL)

        if response.status_code not in [200, 202]:
            raise Exception(
                f"Erro ao solicitar dados: {response.status_code} - {response.text}"
            )

        data = response.json()
        if "data" not in data:
            raise Exception("Dados de rentabilidade não encontrados na resposta.")

        df = pd.DataFrame(data["data"])
        if df.empty:
            raise ValueError("Nenhum dado retornado pela API.")

        report_generator = ReportGenerator(output_folder, template_text, df)
        report_generator.save_report()

        return True
    except Exception as e:
        print(f"Erro ao criar relatórios: {e}")
        return False
