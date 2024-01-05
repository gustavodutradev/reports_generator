import os
import pandas as pd
from datetime import datetime, timedelta
import locale


class InvestmentReports:
    def __init__(self, file_path: str, output_folder: str):
        self.file_path = file_path
        self.output_folder = output_folder
        self.data = None

    def read_csv(self):
        self.data = pd.read_excel(self.file_path, header=1)

    def get_previous_month(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        today = datetime.now()
        first_day = today.replace(day=1)
        previous_month = first_day - timedelta(days=1)
        month_string = previous_month.strftime('%B')

        return month_string.capitalize()

    def load_template_text(self):
        current_folder = os.path.dirname(__file__)
        template_text = os.path.join(current_folder,
                                     '..',
                                     'data',
                                     'template.txt')
        with open(template_text, 'r') as file:
            template = file.read()

        return template

    def generate_costumer_report(self, costumer_data):
        template_text = str(self.load_template_text())
        periodo = str(self.get_previous_month()).capitalize()
        nome = str(costumer_data['Nome']).capitalize()
        rentabilidade_mes = round(float(costumer_data['Rentabilidade mês']), 2)
        cdi = round(float(costumer_data['% CDI']), 2)
        balanço = round(float(costumer_data['Lucro/Prejuízo']), 2)

        text = template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=rentabilidade_mes,
            cdi=cdi, balanço=balanço
            )
        return text

    def save_reports(self):
        if self.data is not None:
            for _, row in self.data.iterrows():
                if 'Assessor' in row.index:
                    advisor = row['Assessor']
                    client_text = self.generate_costumer_report(row)
                    client_name = row['Nome']
                    client_folder = os.path.join(self.output_folder,
                                                 str(advisor))
                    os.makedirs(client_folder, exist_ok=True)
                    client_file_path = os.path.join(
                        client_folder,
                        f"{client_name}.txt"
                        )

                    with open(client_file_path, 'w') as file:
                        file.write(client_text)

                else:
                    print("A coluna Assessor não foi encontrada")
        print("Relatórios gerados com sucesso!")


file_path = input("Digite o caminho completo para a planilha: ")
output_folder = input("Digite o caminho completo para salvar os relatórios: ")

reports = InvestmentReports(file_path, output_folder)
reports.read_csv()
reports.save_reports()
