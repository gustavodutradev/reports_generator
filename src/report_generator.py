import os
from data_processor import DataProcessor
from docx import Document
import pandas as pd
import re

class ReportGenerator:
    def __init__(self, output_folder, template_text, data):
        self.data = data
        self.output_folder = output_folder
        self.template_text = template_text
        self.failed_reports = []

    def clean_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', '', str(filename))
    
    def generate_statistics(self, total_clients, total_reports):
        advisors_clients = {}
        advisors_reports = {}

        for index, item in self.data.iterrows():
            if not isinstance(item, pd.Series):
                continue

            advisor = item.get('Assessor', '')
            client_name = item.get('Nome completo', '')
            client_account = item.get('Conta', '')

            if advisor == '0':  # Ignorar o assessor "0"
                continue

            if advisor not in advisors_clients:
                advisors_clients[advisor] = set()  # Usar um conjunto para garantir clientes únicos
            
            # Usar uma tupla (nome, conta) como chave
            client_key = (client_name, client_account)
            advisors_clients[advisor].add(client_key)

            advisors_reports[advisor] = advisors_reports.get(advisor, 0) + 1

        statistics_file_path = os.path.join(self.output_folder, "statistics.txt")

        with open(statistics_file_path, 'w') as file:
            for advisor, clients in advisors_clients.items():
                num_clients = len(clients)
                num_reports = advisors_reports.get(advisor, 0)
                file.write(f"Assessor: {advisor}\n")
                file.write(f"Quantidade de clientes: {num_clients}\n")
                file.write(f"Quantidade de relatórios gerados: {num_reports}\n\n")

            if total_clients != total_reports:
                file.write(f"Aviso: o número total de clientes ({total_clients}) não é igual ao número de relatórios gerados ({total_reports}).\n\n")

            if self.failed_reports:
                file.write("Relatórios não gerados para os seguintes clientes:\n")
                for client in self.failed_reports:
                    file.write(f"- {client}\n")

        print(f"Estatísticas geradas e salvas em: {statistics_file_path}")
    
    def save_report(self):
        if self.data is not None:
            try:
                existing_files = {}
                total_clients = 0
                for index, item in self.data.iterrows():
                    if not isinstance(item, pd.Series):
                        continue
                    
                    client_name = item.get('Nome completo', '')
                    advisor = item.get('Assessor', '')

                    if not client_name or not advisor:
                        print(f"Ignorando linha inválida na planilha: {item}")
                        continue

                    data_processor = DataProcessor(self.data, self.template_text)
                    client_text = data_processor.generate_customer_report(item)
                    client_account = str(item['Conta']).split('.')[0]

                    periodo = data_processor.get_reference_date()
                    ano_referencia = periodo[1]
                    mes_referencia_numero = periodo[2]

                    # Criar a estrutura de pastas por assessor e período (mês e ano)
                    advisor_folder = os.path.join(self.output_folder, str(advisor))
                    periodo_folder = os.path.join(advisor_folder, f"{ano_referencia}.{mes_referencia_numero}")
                    try:
                        os.makedirs(periodo_folder, exist_ok=True)
                    except OSError:
                        print(f"Erro ao criar pasta {periodo_folder}")

                    client_file_name = self.clean_filename(f"{client_name}_Performance_{ano_referencia}_{mes_referencia_numero}.docx")


                    if client_file_name in existing_files:

                        client_file_name = f"{client_name}_Performance_{client_account}_{ano_referencia}_{mes_referencia_numero}.docx"

                    existing_files[client_file_name] = True

                    client_file_path = os.path.join(periodo_folder, client_file_name)

                    doc = Document()
                    paragraph = doc.add_paragraph()
                    run = paragraph.add_run(client_text)
                    font = run.font
                    font.name = 'Arial'

                    doc.save(client_file_path)

                    total_clients += 1

                total_reports = len(existing_files)
                if total_clients != total_reports:
                    print(f"Aviso: o número total de clientes ({total_clients}) não é igual ao número de relatórios gerados ({total_reports}).")

                    missing_reports_clients = set()
                    for index, item in self.data.iterrows():
                        client_name = item.get('Nome completo', '')
                        client_account = item.get('Conta', '')
                        client_key = (client_name, client_account)
                        if client_key not in existing_files:
                            missing_reports_clients.add(client_name)

                    # Armazenar os clientes para os quais os relatórios não foram gerados
                    self.failed_reports = list(missing_reports_clients)

                self.generate_statistics(total_clients, total_reports)

            except Exception as e:
                raise (f"Erro ao criar relatórios: {e}")
        else:
            raise ValueError("Dados não encontrados no arquivo.")

        print(f"Relatórios gerados com sucesso!")
