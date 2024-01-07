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
            for _, row in self.data.iterrows():
                advisor = row['Assessor']
                data_processor = DataProcessor(self.data, self.template_text)
                client_text = data_processor.generate_customer_report(row)
                client_name = row['Nome']
                client_folder = os.path.join(self.output_folder, str(advisor))
                os.makedirs(client_folder, exist_ok=True)
                client_file_path = os.path.join(
                    client_folder,
                    f"{client_name}.docx"
                )
                doc = Document()
                
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(client_text)
                font = run.font
                font.name = 'Arial'

                doc.save(client_file_path)

        print("Relatórios gerados com sucesso!")
