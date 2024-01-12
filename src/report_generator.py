import os
from data_processor import DataProcessor
from docx import Document

class ReportGenerator:
    def __init__(self, output_folder, template_text, data):
        self.data = data
        self.output_folder = output_folder
        self.template_text = template_text
    
    def save_report(self):
        if self.data is not None:
            try:
                existing_files = {}
                for item in self.data:

                    advisor = item['Assessor']
                    data_processor = DataProcessor(self.data, self.template_text)
                    client_text = data_processor.generate_customer_report(item)
                    client_name = item['Nome completo']
                    client_account = item['Conta']

                    periodo = data_processor.get_reference_date()
                    ano_referencia = periodo[1]
                    mes_referencia_numero = periodo[2]

                    # Criar a estrutura de pastas por assessor e período (mês e ano)
                    advisor_folder = os.path.join(self.output_folder, str(advisor))
                    periodo_folder = os.path.join(advisor_folder, f"{ano_referencia}.{mes_referencia_numero}")
                    os.makedirs(periodo_folder, exist_ok=True)

                    client_file_name = f"{client_name}_Performance_{ano_referencia}_{mes_referencia_numero}.docx"


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

            except FileNotFoundError:
                raise FileNotFoundError("Arquivo não encontrado.")
        else:
            raise ValueError("Dados não encontrados no arquivo.")

        print("Relatórios gerados com sucesso!")
