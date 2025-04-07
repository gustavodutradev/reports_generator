import os
from src.data_processor import DataProcessor
from docx import Document
import pandas as pd
import re
from src.utils.cache_relations import carregar_mapas_relacionamento


class ReportGenerator:
    def __init__(self, output_folder, template_text, data):
        self.data = data
        self.output_folder = output_folder
        self.template_text = template_text
        self.failed_reports = []
        self.mapa_clientes, self.mapa_assessores = carregar_mapas_relacionamento()

    def clean_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', "", str(filename))

    def generate_statistics(self, total_clients, total_reports, advisors_info):
        statistics_file_path = os.path.join(self.output_folder, "feedback.txt")

        with open(statistics_file_path, "w") as file:
            for advisor, info in advisors_info.items():
                file.write(f"Assessor: {advisor}\n")
                file.write(f"Quantidade de clientes: {len(info['clientes'])}\n")
                file.write(
                    f"Quantidade de relatórios gerados: {info['relatorios']}\n\n"
                )

            if total_clients != total_reports:
                file.write(
                    f"Aviso: o número total de clientes ({total_clients}) não é igual ao número de relatórios gerados ({total_reports}).\n\n"
                )

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
                advisors_info = {}

                for _, item in self.data.iterrows():
                    conta = str(item.get("cod_carteira")).zfill(9)
                    nome_raw = self.mapa_clientes.get(conta, "Cliente")
                    nome_partes = nome_raw.split()[:2]
                    nome_cliente = " ".join(p.capitalize() for p in nome_partes)
                    assessor = self.mapa_assessores.get(conta, "Assessor")

                    if not nome_cliente or not assessor:
                        print(
                            f"Ignorando linha com conta {conta} por dados incompletos."
                        )
                        continue

                    data_processor = DataProcessor(self.data, self.template_text)
                    client_text = data_processor.generate_customer_report(item, nome_cliente)

                    periodo = data_processor.get_reference_date()
                    ano_referencia, mes_referencia = periodo[1], periodo[2]

                    # Estrutura de pastas
                    folder_path = os.path.join(
                        self.output_folder,
                        assessor,
                        f"{ano_referencia}.{mes_referencia}",
                    )
                    os.makedirs(folder_path, exist_ok=True)

                    file_name = self.clean_filename(
                        f"{nome_cliente}_Performance_{ano_referencia}_{mes_referencia}.docx"
                    )
                    file_path = os.path.join(folder_path, file_name)

                    if file_name in existing_files:
                        file_name = self.clean_filename(
                            f"{nome_cliente}_{conta}_Performance_{ano_referencia}_{mes_referencia}.docx"
                        )
                        file_path = os.path.join(folder_path, file_name)

                    existing_files[file_name] = True

                    doc = Document()
                    run = doc.add_paragraph().add_run(client_text)
                    run.font.name = "Arial"
                    doc.save(file_path)

                    # Estatísticas
                    total_clients += 1
                    if assessor not in advisors_info:
                        advisors_info[assessor] = {"clientes": set(), "relatorios": 0}
                    advisors_info[assessor]["clientes"].add((nome_cliente, conta))
                    advisors_info[assessor]["relatorios"] += 1

                total_reports = len(existing_files)
                self.generate_statistics(total_clients, total_reports, advisors_info)

            except Exception as e:
                raise Exception(f"Erro ao criar relatórios: {e}")
        else:
            raise ValueError("Dados não encontrados no arquivo.")

        print(f"Relatórios gerados com sucesso!")
