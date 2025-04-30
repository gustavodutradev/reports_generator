import os
import re
from datetime import datetime
import pandas as pd
from docx import Document
from src.data_processor import DataProcessor
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
        with open(statistics_file_path, "w", encoding="utf-8") as file:
            for advisor, info in advisors_info.items():
                file.write(f"Assessor: {advisor}\n")
                file.write(f"Quantidade de clientes: {len(info['clientes'])}\n")
                file.write(f"Quantidade de relatórios gerados: {info['relatorios']}\n\n")

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
        if self.data is None or self.data.empty:
            raise ValueError("DataFrame vazio ou None.")

        existing = set()
        total_clients = 0
        advisors_info = {}

        for _, row in self.data.iterrows():
            raw_nr = row.get("nr_conta")
            if pd.isna(raw_nr):
                self.failed_reports.append(raw_nr)
                continue
            try:
                conta_int = int(raw_nr)
            except (ValueError, TypeError):
                self.failed_reports.append(raw_nr)
                continue

            conta = f"{conta_int:09d}"

            nome_raw = self.mapa_clientes.get(conta)
            assessor = self.mapa_assessores.get(conta)
            if not nome_raw or not assessor:
                self.failed_reports.append(conta)
                continue

            parts = nome_raw.split()
            nome_arquivo = " ".join(p.capitalize() for p in parts[:2])
            nome_texto = parts[0].capitalize()

            # Gera o texto do relatório
            dp = DataProcessor(self.data, self.template_text)
            texto = dp.generate_customer_report(row, nome_texto)

            # Pasta de período (ex: "2025.03")
            _, ano_ref, mes_ref = dp.get_reference_date()
            mes_str = f"{mes_ref:02d}"
            period_folder = f"{ano_ref}.{mes_str}"

            # Cria o diretório: output/Assessor/2025.03/
            pasta = os.path.join(self.output_folder, assessor, period_folder)
            os.makedirs(pasta, exist_ok=True)

            # Nome do arquivo
            base_name = f"{nome_arquivo}_{conta}_Performance_{ano_ref}_{mes_str}.docx"
            safe_name = self.clean_filename(base_name)
            full_path = os.path.join(pasta, safe_name)

            # Evita sobrescrever
            if full_path in existing:
                suffix = datetime.now().strftime("%H%M%S")
                safe_name = safe_name.replace(".docx", f"_{suffix}.docx")
                full_path = os.path.join(pasta, safe_name)
            existing.add(full_path)

            # Salva o documento
            doc = Document()
            doc.add_paragraph(texto)
            doc.save(full_path)

            total_clients += 1
            advisors_info.setdefault(assessor, {"clientes": set(), "relatorios": 0})
            advisors_info[assessor]["clientes"].add(conta)
            advisors_info[assessor]["relatorios"] += 1

        # Finaliza com estatísticas
        self.generate_statistics(total_clients, len(existing), advisors_info)
        print("Relatórios criados com sucesso!")
        return True